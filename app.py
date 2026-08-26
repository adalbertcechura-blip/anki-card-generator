import streamlit as st
import pandas as pd
import requests
import os
import re
import urllib.parse
import unicodedata
import shutil
import hashlib
import tempfile
import genanki
import time
import json

# --- NAČTENÍ GLOBÁLNÍ KONFIGURACE (API klíče pro správce) ---
def _load_global_config() -> dict:
    """
    Načte sdílenou konfiguraci z bezpečných zdrojů:
    1. Streamlit Secrets (při běhu na Streamlit Cloud: st.secrets["XC_API_KEY"] nebo .streamlit/secrets.toml)
    2. Proměnné prostředí (XC_API_KEY, ...)
    3. Lokální soubor config.json (který je v .gitignore a nenahrává se na GitHub)
    """
    cfg = {}
    # 1. Soubor config.json (lokální vývoj)
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    if os.path.isfile(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                d = json.load(f)
                if d.get("xc_api_key"):
                    cfg["xc_api_key"] = str(d["xc_api_key"]).strip()
        except Exception:
            pass
    # 2. Proměnné prostředí
    if os.environ.get("XC_API_KEY"):
        cfg["xc_api_key"] = str(os.environ["XC_API_KEY"]).strip()
    # 3. Streamlit Secrets (Streamlit Cloud dashboard nebo .streamlit/secrets.toml)
    try:
        if "XC_API_KEY" in st.secrets and st.secrets["XC_API_KEY"]:
            cfg["xc_api_key"] = str(st.secrets["XC_API_KEY"]).strip()
        elif "xc_api_key" in st.secrets and st.secrets["xc_api_key"]:
            cfg["xc_api_key"] = str(st.secrets["xc_api_key"]).strip()
    except Exception:
        pass
    return cfg

GLOBAL_CONFIG = _load_global_config()

# --- DYNAMICKÉ CSS PRO ANKI KARTY ---

def get_anki_css(theme_name):
    base_css = """
.card {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  padding: 22px;
  border-radius: 8px;
  max-width: 560px;
  margin: 0 auto;
  line-height: 1.5;
}

.card-field {
  margin-bottom: 14px;
  text-align: left;
}

.card-field:last-child {
  margin-bottom: 0;
}

.field-label {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  display: block;
  margin-bottom: 4px;
  padding-bottom: 2px;
}

.field-value {
  font-size: 15px;
  line-height: 1.55;
}

.photo-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 12px 0;
  align-items: center;
}

.photo-container {
  width: 100%;
  max-width: 480px;
  border-radius: 6px;
  overflow: hidden;
}

.photo-container img {
  width: 100%;
  height: auto;
  object-fit: contain;
  display: block;
}

.no-photo-placeholder {
  padding: 30px;
  border: 1px dashed;
  border-radius: 6px;
  font-size: 14px;
  margin-bottom: 12px;
  text-align: center;
}

.card-divider {
  border: 0;
  height: 1px;
  margin: 14px 0;
}

audio {
  width: 100%;
  max-width: 420px;
  height: 34px;
  border-radius: 6px;
  margin-top: 4px;
  display: block;
}
"""

    if theme_name == "Světlý režim (vždy světlé)" or theme_name == "Světlý režim":
        color_css = """
.card {
  color: #1e2923;
  background-color: #f7faf8;
  border: 1px solid #dce8e0;
}
.field-label {
  color: #4d735d;
  border-bottom: 1px solid #e1ece5;
}
.field-value {
  color: #1e2923;
}
.photo-container {
  border: 1px solid #d0e0d6;
}
.no-photo-placeholder {
  border-color: #cbdad1;
  color: #5c826c;
}
.card-divider {
  background: #dce8e0;
}
"""
    elif theme_name == "Tmavý režim (vždy tmavé)" or theme_name == "Tmavý režim":
        color_css = """
.card {
  color: #e5ede8;
  background-color: #121c16;
  border: 1px solid #23362b;
}
.field-label {
  color: #8da897;
  border-bottom: 1px solid #23362b;
}
.field-value {
  color: #e5ede8;
}
.photo-container {
  border: 1px solid #2a4234;
}
.no-photo-placeholder {
  border-color: #23362b;
  color: #8da897;
}
.card-divider {
  background: #23362b;
}
"""
    else:  # Obojetné (automaticky přepínatelné)
        color_css = """
.card {
  color: #1e2923;
  background-color: #f7faf8;
  border: 1px solid #dce8e0;
}
.field-label {
  color: #4d735d;
  border-bottom: 1px solid #e1ece5;
}
.field-value {
  color: #1e2923;
}
.photo-container {
  border: 1px solid #d0e0d6;
}
.no-photo-placeholder {
  border-color: #cbdad1;
  color: #5c826c;
}
.card-divider {
  background: #dce8e0;
}

.nightMode.card {
  background-color: #121c16;
  color: #e5ede8;
  border: 1px solid #23362b;
}
.nightMode .field-label {
  color: #8da897;
  border-color: #23362b;
}
.nightMode .field-value {
  color: #e5ede8;
}
.nightMode .photo-container {
  border-color: #2a4234;
}
.nightMode .no-photo-placeholder {
  border-color: #23362b;
  color: #8da897;
}
.nightMode .card-divider {
  background: #23362b;
}

@media (prefers-color-scheme: dark) {
  .card {
    background-color: #121c16;
    color: #e5ede8;
    border: 1px solid #23362b;
  }
  .field-label {
    color: #8da897;
    border-color: #23362b;
  }
  .field-value {
    color: #e5ede8;
  }
  .photo-container {
    border-color: #2a4234;
  }
  .no-photo-placeholder {
    border-color: #23362b;
    color: #8da897;
  }
  .card-divider {
    background: #23362b;
  }
}
"""
    return base_css + color_css


ANKI_QFMT = """
<div class="card">
  {{Front}}
</div>
"""

ANKI_AFMT = """
<div class="card">
  {{Front}}
  <hr class="card-divider">
  {{Back}}
</div>
"""

# --- POMOCNÉ FUNKCE ---

def check_image_quality(file_path):
    """
    Ověří pouze existenci a neprázdnost staženého souboru.
    Odstraňuje přísné filtry na ostrost a rozlišení, aby se předešlo chybnému vyřazení snímků.
    """
    try:
        import os
        return os.path.exists(file_path) and os.path.getsize(file_path) > 0
    except Exception:
        return False

def detect_audio_extension(content: bytes, default_ext: str = ".mp3") -> str:
    """Detekuje správnou příponu audio souboru na základě hlavičky (magic bytes)."""
    if not content:
        return default_ext
    if content.startswith(b'RIFF') and b'WAVE' in content[:16]:
        return ".wav"
    if content.startswith(b'ID3') or content.startswith(b'\xff\xfb') or content.startswith(b'\xff\xf3') or content.startswith(b'\xff\xf2'):
        return ".mp3"
    if content.startswith(b'fLaC'):
        return ".flac"
    if content.startswith(b'OggS'):
        return ".ogg"
    if content.startswith(b'ftyp') or b'M4A' in content[:16]:
        return ".m4a"
    return default_ext

def slugify(value):
    """Vytvoří bezpečný název pro soubor."""
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '_', value)

def get_stable_id(name):
    """Vygeneruje stabilní 32bitové celé číslo na základě textu."""
    return int(hashlib.md5(name.encode('utf-8')).hexdigest()[:8], 16)

def clean_html(text):
    """Odstraní nepovolené HTML tagy, ale ponechá základní formátování."""
    if not text:
        return ""
    text = re.sub(r'</?(?!b|i|u|em|strong|p|br|div|span)[a-zA-Z0-9]+[^>]*>', '', text)
    return text.strip()

def get_value_css(col):
    """Vrátí inline CSS styl pro hodnotu sloupce na základě nastavení."""
    styles = []
    if 'col_styles' in st.session_state and col in st.session_state.col_styles:
        style = st.session_state.col_styles[col]
        if style.get("bold"):
            styles.append("font-weight: bold")
        if style.get("italic"):
            styles.append("font-style: italic")
        size = style.get("size")
        if size == "Malé (12px)":
            styles.append("font-size: 12px")
        elif size == "Střední (16px)":
            styles.append("font-size: 16px")
        elif size == "Velké (20px)":
            styles.append("font-size: 20px")
        elif size == "Obrovské (24px)":
            styles.append("font-size: 24px")
    return "; ".join(styles)

def sync_ordered_cols(selected_cols, state_key):
    """Synchronizuje vybrané sloupce s uspořádaným seznamem v session_state."""
    if state_key not in st.session_state:
        st.session_state[state_key] = []
    current_ordered = st.session_state[state_key]
    # Ponechat pouze ty, které jsou stále vybrané
    new_ordered = [c for c in current_ordered if c in selected_cols]
    # Přidat ty, které jsou vybrané, ale ještě nejsou v seznamu
    for c in selected_cols:
        if c not in new_ordered:
            new_ordered.append(c)
    st.session_state[state_key] = new_ordered

# --- DATUM PARSER PRO ON THIS DAY ---

def parse_date(date_str):
    """Rozparsuje datum v různých formátech na (měsíc, den)."""
    if not date_str or pd.isna(date_str):
        return None, None
    date_str = str(date_str).strip().lower()
    
    # Formát: MM/DD nebo M/D
    match1 = re.match(r'^(\d{1,2})/(\d{1,2})$', date_str)
    if match1:
        return int(match1.group(1)), int(match1.group(2))
        
    # Formát: DD.MM. nebo D.M.
    match2 = re.match(r'^(\d{1,2})\.\s*(\d{1,2})\.?$', date_str)
    if match2:
        return int(match2.group(2)), int(match2.group(1))
        
    # České měsíce
    cz_months = {
        'leden': 1, 'ledna': 1,
        'unor': 2, 'unora': 2, 'únor': 2, 'února': 2,
        'brezen': 3, 'brezna': 3, 'březen': 3, 'března': 3,
        'duben': 4, 'dubna': 4,
        'kveten': 5, 'kvetna': 5, 'květen': 5, 'května': 5,
        'cerven': 6, 'cervna': 6, 'červen': 6, 'června': 6,
        'cervenec': 7, 'cervence': 7, 'červenec': 7, 'července': 7,
        'srpen': 8, 'srpna': 8,
        'zari': 9, 'září': 9,
        'rijen': 10, 'rijna': 10, 'říjen': 10, 'října': 10,
        'listopad': 11, 'listopadu': 11,
        'prosinec': 12, 'prosince': 12
    }
    
    match3 = re.match(r'^(\d{1,2})\.\s*([a-zžáíěuořčšý]+)$', date_str)
    if match3:
        day = int(match3.group(1))
        month_name = match3.group(2)
        # Odstraníme diakritiku pro bezpečné porovnání
        month_clean = unicodedata.normalize('NFKD', month_name).encode('ascii', 'ignore').decode('ascii')
        for k, v in cz_months.items():
            k_clean = unicodedata.normalize('NFKD', k).encode('ascii', 'ignore').decode('ascii')
            if month_clean == k_clean:
                return v, day
            
    # Anglické měsíce
    en_months = {
        'january': 1, 'jan': 1, 'february': 2, 'feb': 2, 'march': 3, 'mar': 3,
        'april': 4, 'apr': 4, 'may': 5, 'june': 6, 'jun': 6, 'july': 7, 'jul': 7,
        'august': 8, 'aug': 8, 'september': 9, 'sep': 9, 'october': 10, 'oct': 10,
        'november': 11, 'nov': 11, 'december': 12, 'dec': 12
    }
    
    # June 26
    match4 = re.match(r'^([a-z]+)\s*(\d{1,2})$', date_str)
    if match4:
        month_name = match4.group(1)
        day = int(match4.group(2))
        if month_name in en_months:
            return en_months[month_name], day
            
    # 26 June
    match5 = re.match(r'^(\d{1,2})\s*([a-z]+)$', date_str)
    if match5:
        day = int(match5.group(1))
        month_name = match5.group(2)
        if month_name in en_months:
            return en_months[month_name], day
            
    return None, None

# --- ENHANCER API FUNKCE ---

# 1. iNaturalist botanický modul
def fetch_inaturalist_data(species_name, max_photos=4):
    headers = {'User-Agent': 'AnkiSpeciesGenerator/1.0 (contact: adalb@example.com)'}
    res_data = {
        'common_name': "",
        'photo_urls': [],
        'source': 'Nenalezeno'
    }
    
    encoded_name = urllib.parse.quote(species_name)
    search_url = f"https://api.inaturalist.org/v1/taxa?q={encoded_name}&locale=cs"
    
    taxon_id = None
    try:
        r_inat = requests.get(search_url, timeout=5)
        if r_inat.status_code == 200:
            results = r_inat.json().get('results', [])
            if results:
                best_match = results[0]
                for res in results:
                    if res.get('name', '').lower() == species_name.lower():
                        best_match = res
                        break
                taxon_id = best_match.get('id')
                res_data['common_name'] = best_match.get('preferred_common_name', '')
                res_data['source'] = 'iNaturalist'
    except Exception:
        pass

    if not res_data['common_name']:
        encoded_slug = urllib.parse.quote(species_name.replace(' ', '_'))
        url_wiki_cs = f"https://cs.wikipedia.org/api/rest_v1/page/summary/{encoded_slug}"
        try:
            r_wiki = requests.get(url_wiki_cs, headers=headers, timeout=5)
            if r_wiki.status_code == 200:
                wiki_cs = r_wiki.json()
                if wiki_cs.get('type') != 'disambiguation':
                    res_data['common_name'] = wiki_cs.get('title', '')
                    res_data['source'] = 'Wikipedia (CS)'
        except Exception:
            pass

    # Stažení fotek z iNaturalist
    inat_photos = []
    if taxon_id:
        detail_url = f"https://api.inaturalist.org/v1/taxa/{taxon_id}?locale=cs"
        try:
            r_detail = requests.get(detail_url, timeout=5)
            if r_detail.status_code == 200:
                detail_results = r_detail.json().get('results', [])
                if detail_results:
                    taxon_detail = detail_results[0]
                    taxon_photos = taxon_detail.get('taxon_photos', [])
                    for tp in taxon_photos:
                        photo_obj = tp.get('photo', {})
                        photo_url = photo_obj.get('medium_url') or photo_obj.get('small_url') or photo_obj.get('url')
                        if photo_url:
                            if 'square' in photo_url:
                                photo_url = photo_url.replace('square', 'medium')
                            if photo_url not in inat_photos:
                                inat_photos.append(photo_url)
                                
                    if len(inat_photos) < max_photos:
                        obs_url = f"https://api.inaturalist.org/v1/observations?taxon_id={taxon_id}&photos=true&per_page=10"
                        r_obs = requests.get(obs_url, timeout=5)
                        if r_obs.status_code == 200:
                            obs_results = r_obs.json().get('results', [])
                            for obs in obs_results:
                                if len(inat_photos) >= max_photos:
                                    break
                                for op in obs.get('photos', []):
                                    op_url = op.get('url')
                                    if op_url:
                                        if 'square' in op_url:
                                            op_url = op_url.replace('square', 'medium')
                                        if op_url not in inat_photos:
                                            inat_photos.append(op_url)
                                            if len(inat_photos) >= max_photos:
                                                break
        except Exception:
            pass

    if inat_photos:
        res_data['photo_urls'] = inat_photos[:max_photos]
    else:
        for lang in ['cs', 'en']:
            encoded_slug = urllib.parse.quote(species_name.replace(' ', '_'))
            url_wiki = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{encoded_slug}"
            try:
                r_wiki = requests.get(url_wiki, headers=headers, timeout=5)
                if r_wiki.status_code == 200:
                    wiki = r_wiki.json()
                    thumb = wiki.get('thumbnail', {}).get('source')
                    if thumb:
                        res_data['photo_urls'].append(thumb)
                        break
            except Exception:
                pass
                
    return res_data


def fetch_wiki_description(species_name):
    """
    Stáhne vědecký anglický popis druhu z Wikipedie.
    Funguje pro rostliny i živočichy – hledá sekce popis, morfologie,
    habitat, distribuce, ekologie, chování, výskyt aj.
    """
    headers = {'User-Agent': 'AnkiSpeciesGenerator/1.0 (contact: adalb@example.com)'}
    
    if not species_name or pd.isna(species_name):
        return ""
    species_name = str(species_name).strip()
    if not species_name:
        return ""

    # Klíčová slova pro sekce platné pro rostliny I živočichy
    DESC_KEYS   = {'description', 'morphology', 'appearance', 'physical', 'plumage', 'identification'}
    HABITAT_KEYS = {'habitat', 'distribution', 'ecology', 'range', 'behaviour', 'behavior', 'diet', 'feeding'}

    try:
        encoded_slug = urllib.parse.quote(species_name.replace(' ', '_'))
        url_wiki_en = (
            f"https://en.wikipedia.org/w/api.php"
            f"?action=query&prop=extracts&explaintext=1"
            f"&titles={encoded_slug}&format=json&redirects=1"
        )
        r_en = requests.get(url_wiki_en, headers=headers, timeout=8)
        if r_en.status_code != 200:
            return ""
        pages = r_en.json().get('query', {}).get('pages', {})
        page = list(pages.values())[0]
        if 'missing' in page or 'extract' not in page:
            return ""
        text = page['extract']

        # Rozsekat text na sekce (== Název ==)
        sections = {}
        current_section = "lead"
        current_content = []
        for line in text.split('\n'):
            m = re.match(r'^==\s*(.*?)\s*==$', line)
            if m:
                sections[current_section.lower()] = '\n'.join(current_content).strip()
                current_section = m.group(1)
                current_content = []
            else:
                current_content.append(line)
        sections[current_section.lower()] = '\n'.join(current_content).strip()

        def find_section(keys):
            for k, v in sections.items():
                if any(kw in k for kw in keys) and v:
                    return v
            return ""

        desc    = find_section(DESC_KEYS)
        habitat = find_section(HABITAT_KEYS)

        desc_html = ""
        if desc:
            t = (desc[:1500] + "…") if len(desc) > 1500 else desc
            desc_html += f'<div class="scientific-section"><strong>Description:</strong><br>{t.replace(chr(10), "<br>")}</div>'
        if habitat:
            t = (habitat[:1000] + "…") if len(habitat) > 1000 else habitat
            if desc_html:
                desc_html += "<br>"
            desc_html += f'<div class="scientific-section"><strong>Habitat / Ecology:</strong><br>{t.replace(chr(10), "<br>")}</div>'

        # Záložní: úvodní odstavec (lead)
        if not desc_html:
            lead = sections.get('lead', '')
            if lead:
                t = (lead[:1200] + "…") if len(lead) > 1200 else lead
                desc_html = f'<div class="scientific-section"><strong>Summary:</strong><br>{t.replace(chr(10), "<br>")}</div>'

        return desc_html
    except Exception:
        return ""

# Legacy alias
def fetch_plant_description(species_name, scientific_desc=True):
    return fetch_wiki_description(species_name)


# 2. GBIF Taxonomický modul
def fetch_gbif_taxonomy(species_name):
    res = {
        "kingdom": "", "phylum": "", "class": "", 
        "order": "", "family": "", "genus": "", 
        "source": "Nenalezeno"
    }
    if not species_name or pd.isna(species_name):
        return res
    species_name = str(species_name).strip()
    if not species_name:
        return res
        
    url = f"https://api.gbif.org/v1/species/match?name={urllib.parse.quote(species_name)}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data.get('matchType') != 'NONE':
                res["kingdom"] = data.get("kingdom", "")
                res["phylum"] = data.get("phylum", "")
                res["class"] = data.get("class", "")
                res["order"] = data.get("order", "")
                res["family"] = data.get("family", "")
                res["genus"] = data.get("genus", "")
                res["source"] = "GBIF Taxonomy"
    except Exception:
        pass
    return res

def slugify_species_name(name):
    """Odstraní autorská označení, závorky a vytvoří bezpečný název souboru."""
    if not name or pd.isna(name):
        return "druh"
    name = str(name).strip()
    name = re.sub(r'\s*\(.*\)\s*', '', name).strip()
    name = re.sub(r'\s+sp(p)?\.?$', '', name).strip()
    return slugify(name)

def fetch_gbif_plant_photos(species_name, get_kvet=True, get_list=True):
    """
    Vyhledá fotografii květu a/nebo listu z GBIF API (vždy pouze 1 obrázek pro každý).
    """
    photos = {
        "kvet": "",
        "list": "",
        "source": "Nenalezeno"
    }

    if not species_name or pd.isna(species_name):
        return photos
    species_name = str(species_name).strip()
    if not species_name:
        return photos

    try:
        clean_name = re.sub(r'\s*\(.*\)\s*', '', species_name).strip()
        clean_name = re.sub(r'\s+sp(p)?\.?$', '', clean_name).strip()
        
        match_url = "https://api.gbif.org/v1/species/match"
        match_params = {
            "name": clean_name,
            "kingdom": "Plantae",
            "strict": "true"
        }
        
        r_match = requests.get(match_url, params=match_params, timeout=8)
        if r_match.status_code != 200:
            return photos
            
        match_data = r_match.json()
        if match_data.get("matchType") == "NONE":
            return photos
            
        usage_key = match_data.get("usageKey")
        if not usage_key:
            return photos

        # Keywords pro detekci orgánů
        kvet_keywords = ["flower", "flos", "inflorescence", "fleur", "blüte"]
        list_keywords = ["leaf", "leaves", "folium", "feuille", "blatt"]

        # Seznam dotazů na pozorování (prioritizujeme Pl@ntNet verified observations)
        queries = []
        if get_kvet or get_list:
            queries = [
                {"taxonKey": usage_key, "mediaType": "StillImage", "datasetKey": "7a3679ef-5582-4aaa-81f0-8c2545cafc81", "limit": 40},
                {"taxonKey": usage_key, "mediaType": "StillImage", "datasetKey": "14d5676a-2c54-4f94-9023-1e8dcd822aa0", "limit": 40},
                {"taxonKey": usage_key, "mediaType": "StillImage", "basisOfRecord": "HUMAN_OBSERVATION", "limit": 40}
            ]

        for params in queries:
            if (not get_kvet or photos["kvet"]) and (not get_list or photos["list"]):
                break
                
            try:
                r_occ = requests.get("https://api.gbif.org/v1/occurrence/search", params=params, timeout=8)
                if r_occ.status_code == 200:
                    results = r_occ.json().get("results", [])
                    for occ in results:
                        media_list = occ.get("media", [])
                        for media in media_list:
                            if media.get("type") != "StillImage":
                                continue
                            img_url = media.get("identifier")
                            if not img_url:
                                continue
                                
                            title = str(media.get("title", "")).lower()
                            desc = str(media.get("description", "")).lower()
                            
                            # Květ
                            if get_kvet and not photos["kvet"] and any(kw in title or kw in desc for kw in kvet_keywords):
                                photos["kvet"] = img_url
                                photos["source"] = "GBIF Occurrence"
                            # List
                            elif get_list and not photos["list"] and any(kw in title or kw in desc for kw in list_keywords):
                                photos["list"] = img_url
                                photos["source"] = "GBIF Occurrence"
                                    
            except Exception:
                pass
    except Exception:
        pass

    return photos

def fetch_gbif_zoo_photos(species_name, max_photos=3):
    """
    Vyhledá fotky živočichů z GBIF API (occurrence search) pro daný taxon.
    """
    photos = []
    if not species_name or pd.isna(species_name):
        return photos
    species_name = str(species_name).strip()
    if not species_name:
        return photos
    try:
        clean_name = re.sub(r'\s*\(.*\)\s*', '', species_name).strip()
        clean_name = re.sub(r'\s+sp(p)?\.?$', '', clean_name).strip()
        
        match_url = "https://api.gbif.org/v1/species/match"
        match_params = {
            "name": clean_name,
            "strict": "true"
        }
        r_match = requests.get(match_url, params=match_params, timeout=5)
        if r_match.status_code == 200:
            match_data = r_match.json()
            usage_key = match_data.get("usageKey")
            if usage_key:
                occ_url = "https://api.gbif.org/v1/occurrence/search"
                occ_params = {
                    "taxonKey": usage_key,
                    "mediaType": "StillImage",
                    "limit": 30
                }
                r_occ = requests.get(occ_url, params=occ_params, timeout=8)
                if r_occ.status_code == 200:
                    results = r_occ.json().get("results", [])
                    for occ in results:
                        if len(photos) >= max_photos:
                            break
                        media_list = occ.get("media", [])
                        for media in media_list:
                            if media.get("type") == "StillImage" and media.get("identifier"):
                                img_url = media.get("identifier")
                                if img_url not in photos:
                                    photos.append(img_url)
                                    if len(photos) >= max_photos:
                                        break
    except Exception:
        pass
    return photos

def fetch_bird_sounds_xenocanto(species_name, sound_types=None, max_sounds=1, api_key=""):
    """
    Stáhne přímé MP3 URL hlasů ptáků z databáze Xeno-canto (API v3).
    sound_types: list např. ["song", "call"] – stáhne nahrávky pro každý typ.
    Vrátí seznam (url, sound_type) tuplů.
    """
    if sound_types is None:
        sound_types = ["song"]
    results = []
    if not species_name or pd.isna(species_name):
        return results
    species_name = str(species_name).strip()
    if not species_name:
        return results

    if not api_key:
        api_key = GLOBAL_CONFIG.get("xc_api_key", "ae76d0eb5372097da7669f153dff1ffbc57a3e51")

    headers = {"User-Agent": "AnkiCardGenerator/1.0 (educational use)"}

    def _clean(name):
        name = re.sub(r'\s*\(.*?\)\s*', ' ', name).strip()
        name = re.sub(r'\s*\[.*?\]\s*', ' ', name).strip()
        name = re.sub(r'\s+(subsp|ssp|var|agg|s\.l|s\.s|sensu)\.?\S*', '', name, flags=re.I).strip()
        name = re.sub(r'\s+(L\.|Linnaeus|Brisson|Gmelin|Latham|Vieillot|Boddaert|Pallas|Temminck|Bonaparte|Degland|Lesson|Cuvier|Kaup|Boie|Gould|Brehm|Naumann)\b.*$', '', name, flags=re.I).strip()
        return " ".join(name.split())

    clean_name = _clean(species_name)

    # Pokud název obsahuje české znaky nebo není binomický latinský, zkusíme zjistit vědecký název přes iNaturalist
    sci_name = clean_name
    parts = clean_name.split()
    is_likely_czech = any(ord(c) > 127 for c in clean_name)
    if is_likely_czech or len(parts) != 2:
        try:
            r_tax = requests.get(
                "https://api.inaturalist.org/v1/taxa",
                params={"q": clean_name, "locale": "cs", "per_page": 3},
                headers=headers,
                timeout=5
            )
            if r_tax.status_code == 200:
                tax_results = r_tax.json().get("results", [])
                if tax_results:
                    matched_sci = tax_results[0].get("name", "")
                    if matched_sci:
                        sci_name = _clean(matched_sci)
        except Exception:
            pass

    sci_parts = sci_name.split()

    for stype in sound_types:
        try:
            queries_to_try = []
            if len(sci_parts) >= 2:
                # 1. Specifický druh s typem a kvalitou A
                queries_to_try.append(f'sp:"{sci_parts[0]} {sci_parts[1]}" type:{stype} q:A')
                # 2. Specifický druh s typem (jakákoliv kvalita)
                queries_to_try.append(f'sp:"{sci_parts[0]} {sci_parts[1]}" type:{stype}')
                # 3. Specifický druh obecně
                queries_to_try.append(f'sp:"{sci_parts[0]} {sci_parts[1]}"')
            else:
                queries_to_try.append(f'gen:{sci_parts[0]} type:{stype} q:A')
                queries_to_try.append(f'gen:{sci_parts[0]} type:{stype}')

            recordings = []
            for q_str in queries_to_try:
                params = {"query": q_str, "key": api_key, "per_page": 10}
                r = requests.get("https://xeno-canto.org/api/3/recordings", params=params, headers=headers, timeout=10)
                if r.status_code == 200:
                    recordings = r.json().get("recordings", [])
                    if recordings:
                        break

            def sort_key(rec):
                q_order = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}
                q_val = q_order.get(rec.get("q", "E"), 5)
                fn = str(rec.get("file-name", "")).lower()
                # MP3 soubory mají prioritu před nekomprimovanými WAV kvůli univerzální kompatibilitě napříč všemi verzemi Anki
                fmt_order = 0 if fn.endswith(".mp3") else 1
                return (fmt_order, q_val)

            recordings = sorted(recordings, key=sort_key)
            count = 0
            for rec in recordings:
                if count >= max_sounds:
                    break
                file_url = rec.get("file", "")
                if file_url and not file_url.startswith("http"):
                    file_url = "https:" + file_url
                if file_url:
                    # Vyhneme se duplicitám stejné URL
                    if not any(r[0] == file_url for r in results):
                        results.append((file_url, stype))
                        count += 1
        except Exception:
            pass
    return results


# 3. UniProt Gene & Protein modul
def fetch_uniprot_data(gene_name):
    res = {"protein_name": "", "function": "", "source": "Nenalezeno"}
    if not gene_name or pd.isna(gene_name):
        return res
    gene_name = str(gene_name).strip()
    if not gene_name:
        return res
        
    url = f"https://rest.uniprot.org/uniprotkb/search?query=gene:{urllib.parse.quote(gene_name)}+AND+organism_id:9606&format=json&size=1"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            results = data.get("results", [])
            if results:
                entry = results[0]
                desc = entry.get("proteinDescription", {})
                rec_name = desc.get("recommendedName", {})
                if rec_name:
                    res["protein_name"] = rec_name.get("fullName", {}).get("value", "")
                elif desc.get("submissionNames"):
                    res["protein_name"] = desc["submissionNames"][0].get("fullName", {}).get("value", "")
                
                comments = entry.get("comments", [])
                for c in comments:
                    if c.get("commentType") == "FUNCTION":
                        texts = c.get("texts", [])
                        if texts:
                            res["function"] = texts[0].get("value", "")
                            break
                res["source"] = "UniProt"
    except Exception:
        pass
    return res

# 4. MKN-10 (ICD-10) Klinický vyhledávač
def fetch_icd10_data(query):
    res = {"code": "", "name": "", "source": "Nenalezeno"}
    if not query or pd.isna(query):
        return res
    query = str(query).strip()
    if not query:
        return res
        
    url = f"https://clinicaltables.nlm.nih.gov/api/icd10cm/v3/search?terms={urllib.parse.quote(query)}&sf=code,name"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if len(data) >= 4 and data[3]:
                res["code"] = data[3][0][0]
                res["name"] = data[3][0][1]
                res["source"] = "NIH ICD-10"
    except Exception:
        pass
    return res

# 5. Wikimedia Commons obrázkový modul
def fetch_wikimedia_images(query, max_photos=4):
    if not query or pd.isna(query):
        return []
    query = str(query).strip()
    if not query:
        return []
    
    headers = {'User-Agent': 'AnkiCardGen/1.0 (contact: adalb@example.com)'}
    search_query = f"filetype:bitmap|drawing {query}"
    url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(search_query)}&gsrnamespace=6&gsrlimit={max_photos}&prop=imageinfo&iiprop=url&format=json"
    
    photos = []
    try:
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            data = r.json()
            pages = data.get('query', {}).get('pages', {})
            for p in pages.values():
                imageinfo = p.get('imageinfo', [])
                if imageinfo:
                    img_url = imageinfo[0].get('url')
                    if img_url and img_url not in photos:
                        photos.append(img_url)
    except Exception:
        pass
    return photos[:max_photos]

# 6. MyMemory Překladač modul
def translate_text(text, src="en", target="cs"):
    if not text or pd.isna(text):
        return ""
    text = str(text).strip()
    if not text:
        return ""
    url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair={src}|{target}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            return data.get('responseData', {}).get('translatedText', "")
    except Exception:
        pass
    return ""

# 7. English Dictionary API modul
def fetch_dictionary_data(word):
    res = {"phonetic": "", "definition": "", "example": ""}
    if not word or pd.isna(word):
        return res
    word = str(word).strip()
    if not word:
        return res
    
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{urllib.parse.quote(word)}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and data:
                entry = data[0]
                res["phonetic"] = entry.get("phonetic", "")
                if not res["phonetic"] and entry.get("phonetics"):
                    for ph in entry["phonetics"]:
                        if ph.get("text"):
                            res["phonetic"] = ph["text"]
                            break
                
                meanings = entry.get("meanings", [])
                if meanings:
                    defs = meanings[0].get("definitions", [])
                    if defs:
                        res["definition"] = defs[0].get("definition", "")
                        res["example"] = defs[0].get("example", "")
    except Exception:
        pass
    return res

# 8. PubChem chemický modul
def fetch_chemistry_data(compound_name):
    res = {"iupac": "", "weight": "", "img_url": ""}
    if not compound_name or pd.isna(compound_name):
        return res
    compound_name = str(compound_name).strip()
    if not compound_name:
        return res
        
    encoded_name = urllib.parse.quote(compound_name)
    res["img_url"] = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{encoded_name}/PNG"
    
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{encoded_name}/property/IUPACName,MolecularWeight/JSON"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            props = data.get("PropertyTable", {}).get("Properties", [])
            if props:
                res["iupac"] = props[0].get("IUPACName", "")
                res["weight"] = props[0].get("MolecularWeight", "")
    except Exception:
        pass
    return res

# 9. Dějepisné kalendárium (On This Day)
def fetch_on_this_day_events(date_str):
    res = {"events": "", "source": "Nenalezeno"}
    month, day = parse_date(date_str)
    if not month or not day:
        return res
        
    headers = {'User-Agent': 'AnkiCardGen/1.0 (contact: adalb@example.com)'}
    m_str = f"{month:02d}"
    d_str = f"{day:02d}"
    
    url = f"https://en.wikipedia.org/api/rest_v1/feed/onthisday/all/{m_str}/{d_str}"
    try:
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            events = r.json().get('events', [])
            events_html = []
            for ev in events[:4]:
                year = ev.get('year')
                text = ev.get('text')
                if year and text:
                    events_html.append(f'<div style="margin-bottom: 8px;"><strong>{year}</strong>: {text}</div>')
            res["events"] = "".join(events_html)
            res["source"] = f"Wikipedia On This Day ({m_str}/{d_str})"
    except Exception:
        pass
    return res

# 10. Wikipedie obecný encyklopedický modul
def fetch_wikipedia_general(concept, lang="cs"):
    res = {"title": "", "summary": "", "img_url": "", "source": "Nenalezeno"}
    if not concept or pd.isna(concept):
        return res
    concept = str(concept).strip()
    if not concept:
        return res
        
    headers = {'User-Agent': 'AnkiCardGen/1.0 (contact: adalb@example.com)'}
    encoded_name = urllib.parse.quote(concept.replace(' ', '_'))
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{encoded_name}"
    
    try:
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data.get('type') != 'disambiguation':
                res["title"] = data.get("title", "")
                res["summary"] = clean_html(data.get("extract_html") or data.get("extract", ""))
                res["img_url"] = data.get("thumbnail", {}).get("source", "")
                res["source"] = f"Wikipedia ({lang.upper()})"
    except Exception:
        pass
    return res

# 11. Zeměpisný modul (Stát, hlavní město, region, populace, vlajka)
@st.cache_data
def load_countries_db():
    try:
        url = "https://raw.githubusercontent.com/mledoze/countries/master/dist/countries.json"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return []

def fetch_country_data(query, db):
    res = {
        "common_name": "",
        "official_name": "",
        "capital": "",
        "region": "",
        "subregion": "",
        "languages": "",
        "currencies": "",
        "area": "",
        "flag_url": "",
        "source": "Nenalezeno"
    }
    if not query or not db:
        return res
        
    q = str(query).strip().lower()
    match = None
    
    # Hledání shody (anglický název, oficiální název, národní názvy, překlady, ISO kódy)
    for c in db:
        names = []
        names.append(c.get('name', {}).get('common', '').lower())
        names.append(c.get('name', {}).get('official', '').lower())
        
        native = c.get('name', {}).get('native', {})
        for l in native:
            names.append(native[l].get('common', '').lower())
            names.append(native[l].get('official', '').lower())
            
        trans = c.get('translations', {})
        for l in trans:
            names.append(trans[l].get('common', '').lower())
            names.append(trans[l].get('official', '').lower())
            
        names.append(c.get('cca2', '').lower())
        names.append(c.get('cca3', '').lower())
        
        if q in names:
            match = c
            break
            
    # Pokud se nepodaří přesná shoda, zkusíme vyhledat jako podřetězec
    if not match:
        for c in db:
            common = c.get('name', {}).get('common', '').lower()
            trans = c.get('translations', {})
            cz_common = trans.get('ces', {}).get('common', '').lower() if 'ces' in trans else ''
            if q in common or (cz_common and q in cz_common):
                match = c
                break
                
    if match:
        trans = match.get('translations', {})
        
        # České common jméno, pokud existuje
        if 'ces' in trans:
            res["common_name"] = trans['ces'].get('common', match.get('name', {}).get('common', ''))
            res["official_name"] = trans['ces'].get('official', match.get('name', {}).get('official', ''))
        else:
            res["common_name"] = match.get('name', {}).get('common', '')
            res["official_name"] = match.get('name', {}).get('official', '')
            
        cap = match.get('capital', [])
        res["capital"] = cap[0] if cap else ""
        res["region"] = match.get('region', '')
        res["subregion"] = match.get('subregion', '')
        
        langs = match.get('languages', {})
        res["languages"] = ", ".join(langs.values())
        
        curs = match.get('currencies', {})
        cur_list = []
        for code, details in curs.items():
            name = details.get('name', '')
            symbol = details.get('symbol', '')
            cur_list.append(f"{name} ({code}) {symbol}".strip())
        res["currencies"] = ", ".join(cur_list)
        
        area = match.get('area')
        if area:
            res["area"] = f"{area:,} km²".replace(",", " ")
            
        cca2 = match.get('cca2', '')
        if cca2:
            res["flag_url"] = f"https://flagsapi.com/{cca2.upper()}/flat/64.png"
            
        res["source"] = "GitHub Countries Database"
        
    return res

# --- DETEKCE OBRÁZKOVÉHO SLOUPCE ---

def is_image_col(col_name, sample_val):
    """Určí, zda sloupec obsahuje obrázkové URL odkazy."""
    # Audio a textové odkazy ignorujeme (nejsou to obrázky)
    non_img_prefixes = ["[Pladias]", "[Wikipedie] Odkaz", "[Wikipedie] Odka", "[Zvuky]", "[TTS]"]
    if any(col_name.startswith(pfx) for pfx in non_img_prefixes):
        return False
    if any(k in col_name.lower() for k in ['photo', 'obrázk', 'obrazk', 'image', 'fotk', 'molekula', 'náhled', 'květ', 'kvet', 'list']):
        return True
    if isinstance(sample_val, str) and (sample_val.startswith('http://') or sample_val.startswith('https://')):
        # Pokud je to audio URL, není to obrázek
        if sample_val.endswith('.mp3') or 'xeno-canto.org' in sample_val or 'translate_tts' in sample_val:
            return False
        return True
    return False

# --- STREAMLIT ROZHRANÍ ---

# Načtení databáze států pro zeměpisný modul
countries_db = load_countries_db()

st.set_page_config(
    page_title="Generátor kartiček Anki",
    layout="wide"
)

st.markdown("""
<style>
    /* Globální tmavé biologické téma (přírodní tmavě zelené tóny, čistý moderní web) */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #0c140f !important;
        color: #e5ede7 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    }
    
    .main-title {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        color: #f2f8f4 !important;
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 0.25rem;
    }
    .subtitle {
        color: #8da897 !important;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
    
    /* Nadpisy, odstavce, popisky widgetů a seznamy */
    h1, h2, h3, h4, h5, h6 {
        color: #f2f8f4 !important;
        font-weight: 600 !important;
    }
    
    p, span, label, li, small, caption, th, td {
        color: #d1e0d6 !important;
    }
    
    hr {
        border-color: #1c2e22 !important;
    }
    
    /* Tlačítka - běžný, plochý styl webové stránky bez glass efektu */
    .stButton > button {
        background-color: #1e5c38 !important;
        color: #f4faf6 !important;
        border: 1px solid #2b7a4d !important;
        border-radius: 5px !important;
        padding: 7px 16px !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        box-shadow: none !important;
        transition: background-color 0.15s ease, border-color 0.15s ease !important;
    }
    .stButton > button:hover {
        background-color: #267347 !important;
        border-color: #389c62 !important;
        color: #ffffff !important;
        transform: none !important;
        box-shadow: none !important;
    }
    .stButton > button:active {
        background-color: #17472c !important;
    }
    
    /* Download tlačítka */
    .stDownloadButton > button {
        background-color: #17442a !important;
        color: #f4faf6 !important;
        border: 1px solid #2b7a4d !important;
        border-radius: 5px !important;
        padding: 7px 16px !important;
        font-weight: 500 !important;
        box-shadow: none !important;
    }
    .stDownloadButton > button:hover {
        background-color: #205c39 !important;
        border-color: #389c62 !important;
        color: #ffffff !important;
    }
    
    /* Vstupy a výběry */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div,
    div[data-baseweb="select"] > div {
        background-color: #121d16 !important;
        border-color: #23362a !important;
        color: #e5ede7 !important;
        border-radius: 5px !important;
    }
    div[data-baseweb="select"] > div:hover,
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #389c62 !important;
    }
    
    /* Taby */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        border-bottom: 1px solid #1c2e22 !important;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border: 1px solid transparent !important;
        border-bottom: 2px solid transparent !important;
        border-radius: 4px 4px 0 0 !important;
        color: #7d9a86 !important;
        font-weight: 500 !important;
        padding: 8px 16px !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #142018 !important;
        border-color: #1c2e22 #1c2e22 transparent #1c2e22 !important;
        border-bottom: 2px solid #2e8b57 !important;
        color: #eaf5ee !important;
        font-weight: 600 !important;
    }
    
    /* Radio a zaškrtávací pole */
    .stCheckbox span, .stRadio span {
        color: #d1e0d6 !important;
    }
    
    /* Notifikace a hlášení */
    div[data-testid="stAlert"] {
        border-radius: 5px !important;
        border: 1px solid #22382b !important;
        background-color: #111d15 !important;
        color: #d1e0d6 !important;
    }
    
    /* Výjimka pro náhled kartičky (řídí se vybraným tématem) */
    .card-preview-container,
    .card-preview-container *,
    .card-preview-container p,
    .card-preview-container span,
    .card-preview-container div,
    .card-preview-container strong,
    .card-preview-container [data-testid="stMarkdownContainer"] p,
    .card-preview-container [data-testid="stMarkdownContainer"] span,
    .card-preview-container [data-testid="stMarkdownContainer"] strong,
    .card-preview-container [data-testid="stMarkdownContainer"] div {
        color: inherit !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Generátor kartiček Anki</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Nahrajte tabulku, obohaťte ji o data přes API a sestavte líc a rub kartiček.</div>', unsafe_allow_html=True)

# Inicializace stavu
if 'df' not in st.session_state:
    st.session_state.df = None
if 'enhancements_applied' not in st.session_state:
    st.session_state.enhancements_applied = False
if 'unfound_list' not in st.session_state:
    st.session_state.unfound_list = []
if 'generated_apkg_data' not in st.session_state:
    st.session_state.generated_apkg_data = None
if 'generated_apkg_filename' not in st.session_state:
    st.session_state.generated_apkg_filename = ""
if 'unfound_csv_data' not in st.session_state:
    st.session_state.unfound_csv_data = None
if 'notes_count' not in st.session_state:
    st.session_state.notes_count = 0
if 'media_count' not in st.session_state:
    st.session_state.media_count = 0
if 'front_cols_ordered' not in st.session_state:
    st.session_state.front_cols_ordered = []
if 'back_cols_ordered' not in st.session_state:
    st.session_state.back_cols_ordered = []
if 'col_styles' not in st.session_state:
    st.session_state.col_styles = {}

# --- METODA VSTUPU DAT ---
input_method = st.radio("Metoda vstupu dat:", ["Nahrát soubor (Excel, CSV, TXT)", "Vložit seznam ručně (textové pole)"], horizontal=True)

uploaded_file = None
text_input_value = ""

if input_method == "Nahrát soubor (Excel, CSV, TXT)":
    col_file1, col_file2 = st.columns([4, 1])
    with col_file1:
        uploaded_file = st.file_uploader("Nahrajte soubor (Excel .xlsx, CSV nebo TXT)", type=["csv", "xlsx", "txt"])

    reload_clicked = False
    with col_file2:
        if uploaded_file is not None:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            reload_clicked = st.button("Znovu načíst soubor")

    if uploaded_file is not None:
        if st.session_state.df is None or reload_clicked:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                    if len(df.columns) <= 1:
                        df = pd.read_csv(uploaded_file, sep=';')
                elif uploaded_file.name.endswith('.txt'):
                    content = uploaded_file.read().decode('utf-8')
                    lines = content.splitlines()
                    species_list = [line.strip() for line in lines if line.strip()]
                    df = pd.DataFrame(species_list, columns=["Vědecké jméno"])
                else:
                    df = pd.read_excel(uploaded_file)
                st.session_state.df = df
                st.session_state.enhancements_applied = False
                st.session_state.unfound_list = []
                st.session_state.generated_apkg_data = None
                st.session_state.generated_apkg_filename = ""
                st.session_state.unfound_csv_data = None
                st.session_state.notes_count = 0
                st.session_state.media_count = 0
                st.session_state.front_cols_ordered = []
                st.session_state.back_cols_ordered = []
                st.session_state.col_styles = {}
                st.session_state.api_config = {}
                st.success("Soubor byl úspěšně načten.")
            except Exception as e:
                st.error(f"Nepodařilo se načíst soubor: {e}")
else:
    st.markdown("##### Vložte seznam druhů (jeden druh na každý řádek):")
    text_input_value = st.text_area("Seznam druhů:", height=150, placeholder="Např.:\nPlantago lanceolata\nBellis perennis\nTaraxacum officinale", key="manual_species_input")
    
    if "last_manual_input" not in st.session_state:
        st.session_state.last_manual_input = ""
        
    trigger_load = False
    if text_input_value and text_input_value != st.session_state.last_manual_input:
        st.session_state.last_manual_input = text_input_value
        trigger_load = True
        
    if st.button("Načíst vložený seznam") or trigger_load:
        lines = text_input_value.splitlines()
        species_list = [line.strip() for line in lines if line.strip()]
        if species_list:
            df = pd.DataFrame(species_list, columns=["Vědecké jméno"])
            st.session_state.df = df
            st.session_state.enhancements_applied = False
            st.session_state.unfound_list = []
            st.session_state.generated_apkg_data = None
            st.session_state.generated_apkg_filename = ""
            st.session_state.unfound_csv_data = None
            st.session_state.notes_count = 0
            st.session_state.media_count = 0
            st.session_state.front_cols_ordered = []
            st.session_state.back_cols_ordered = []
            st.session_state.col_styles = {}
            st.session_state.api_config = {}
            st.success(f"Načteno {len(species_list)} položek do paměti.")
            st.rerun()
        else:
            if not trigger_load:
                st.error("Seznam druhů je prázdný.")

if st.session_state.df is not None:
    df = st.session_state.df
    columns = list(df.columns)
    
    st.markdown("### Náhled tabulky")
    st.dataframe(df.head(5), use_container_width=True)
    st.caption(f"Celkem řádků: **{len(df)}** | Sloupců: **{len(columns)}**")
    
    col_clean1, col_clean2 = st.columns([2, 3])
    with col_clean1:
        clean_col_choice = st.selectbox("Sloupec se jmény k vyčištění:", options=columns, index=0, key="clean_col_choice")
    with col_clean2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("Vyčistit vědecká jména (odstranit subsp., var., agg.)"):
            def clean_botanical_name(name):
                if not name or pd.isna(name):
                    return name
                name_str = str(name).strip()
                cleaned = re.sub(r'\s+(subsp|ssp|var|f|agg|sect|nothosubsp)\.?(\s+.*|$)', '', name_str, flags=re.IGNORECASE)
                return cleaned.strip()
            
            st.session_state.df[clean_col_choice] = st.session_state.df[clean_col_choice].apply(clean_botanical_name)
            st.success("Jména byla úspěšně vyčištěna.")
            st.rerun()
    
    # --- KROK 2: OBOHACENÍ DAT ---
    st.markdown("---")
    
    # Inicializace persistentního konfigurátoru v session_state (aby přežil přepínání záložek)
    if "api_config" not in st.session_state or not st.session_state.api_config:
        st.session_state.api_config = {
            "selected_api_topic": "Biologie",
            "enable_inat": False,
            "inat_col": columns[0] if columns else "",
            "inat_max": 4,
            "enable_desc": False,
            "desc_col": columns[0] if columns else "",
            "desc_type": "Vědecký anglický (popis, habitat, listy...)",
            "enable_gbif": False,
            "gbif_col": columns[0] if columns else "",
            "enable_gbif_kvet": False,
            "enable_gbif_list": False,
            "gbif_photo_col": columns[0] if columns else "",
            "enable_pladias": False,
            "pladias_col": columns[0] if columns else "",
            "enable_gbif_zoo": False,
            "gbif_zoo_col": columns[0] if columns else "",
            "gbif_zoo_max": 3,
            "enable_bird_sounds": False,
            "bird_sounds_col": columns[0] if columns else "",
            "bird_sounds_song": True,
            "bird_sounds_call": False,
            "bird_sounds_max": 1,
            "xc_api_key": GLOBAL_CONFIG.get("xc_api_key", ""),
            "card_layout": "pod sebe",
            "enable_wiki_link": False,
            "wiki_link_col": columns[0] if columns else "",
            "enable_wiki_img": False,
            "wiki_col": columns[0] if columns else "",
            "wiki_max": 3,
            "enable_trans": False,
            "trans_col": columns[0] if columns else "",
            "trans_src": "Angličtina",
            "trans_tgt": "Čeština",
            "enable_tts": False,
            "tts_col": columns[0] if columns else "",
            "tts_lang": "Angličtina",
            "enable_dict": False,
            "dict_col": columns[0] if columns else "",
            "enable_country": False,
            "country_col": columns[0] if columns else ""
        }

    # Zajištění validních sloupců (pokud by se změnil DataFrame bez kompletního promazání)
    cfg = st.session_state.api_config
    col_keys = ["inat_col", "gbif_col", "gbif_photo_col", "desc_col", "pladias_col", 
                "gbif_zoo_col", "bird_sounds_col", "wiki_link_col", "wiki_col", "trans_col", "tts_col", 
                "dict_col", "country_col"]
    for col_key in col_keys:
        if col_key not in cfg or cfg[col_key] not in columns:
            cfg[col_key] = columns[0] if columns else ""

    languages = {
        "Angličtina": "en", "Čeština": "cs", "Němčina": "de", 
        "Španělština": "es", "Francouzština": "fr", "Italština": "it", "Ruština": "ru"
    }

    topics = ["Biologie", "Jazyky", "Zeměpis"]
    curr_topic = cfg.get("selected_api_topic", "Biologie")
    if curr_topic not in topics:
        curr_topic = "Biologie"
    topic_idx = topics.index(curr_topic)

    selected_topic = st.radio(
        "Téma modulu:",
        topics,
        index=topic_idx,
        horizontal=True,
        key="selected_api_topic_widget",
        label_visibility="collapsed"
    )
    cfg["selected_api_topic"] = selected_topic
    
    st.markdown("<hr style='margin:0 0 12px 0'>", unsafe_allow_html=True)

    col_t_title, col_t_btn1, col_t_btn2 = st.columns([3, 1.2, 1.2])
    with col_t_title:
        st.markdown(f"#### {selected_topic} – Moduly")
    with col_t_btn1:
        if st.button("Zaškrtnout vše", key="btn_check_all_topic"):
            if selected_topic == "Biologie":
                for k in ["enable_gbif_kvet", "enable_gbif_list", "enable_pladias", "enable_gbif_zoo", "enable_bird_sounds", "enable_inat", "enable_desc", "enable_gbif", "enable_wiki_img", "enable_wiki_link"]:
                    cfg[k] = True
                    st.session_state[f"w_{k}"] = True
            elif selected_topic == "Jazyky":
                for k in ["enable_trans", "enable_tts", "enable_dict"]:
                    cfg[k] = True
                    st.session_state[f"w_{k}"] = True
            elif selected_topic == "Zeměpis":
                for k in ["enable_country"]:
                    cfg[k] = True
                    st.session_state[f"w_{k}"] = True
            st.rerun()
    with col_t_btn2:
        if st.button("Zrušit výběr", key="btn_uncheck_all_topic"):
            if selected_topic == "Biologie":
                for k in ["enable_gbif_kvet", "enable_gbif_list", "enable_pladias", "enable_gbif_zoo", "enable_bird_sounds", "enable_inat", "enable_desc", "enable_gbif", "enable_wiki_img", "enable_wiki_link"]:
                    cfg[k] = False
                    st.session_state[f"w_{k}"] = False
            elif selected_topic == "Jazyky":
                for k in ["enable_trans", "enable_tts", "enable_dict"]:
                    cfg[k] = False
                    st.session_state[f"w_{k}"] = False
            elif selected_topic == "Zeměpis":
                for k in ["enable_country"]:
                    cfg[k] = False
                    st.session_state[f"w_{k}"] = False
            st.rerun()

    if selected_topic == "Biologie":
        # Podzáložky Botanika a Zoologie
        tab_botanika, tab_zoologie = st.tabs(["Botanika", "Zoologie"])
        
        with tab_botanika:
            st.markdown("##### Specifická nastavení pro botaniku")
            cfg["enable_gbif_kvet"] = st.checkbox(
                "Aktivovat GBIF fotky - Květ", 
                value=cfg.get("enable_gbif_kvet", False),
                key="w_enable_gbif_kvet"
            )
            cfg["enable_gbif_list"] = st.checkbox(
                "Aktivovat GBIF fotky - List", 
                value=cfg.get("enable_gbif_list", False),
                key="w_enable_gbif_list"
            )
            if cfg.get("enable_gbif_kvet", False) or cfg.get("enable_gbif_list", False):
                gbif_photo_col_val = cfg.get("gbif_photo_col", columns[0])
                try:
                    gbif_photo_col_idx = columns.index(gbif_photo_col_val)
                except ValueError:
                    gbif_photo_col_idx = 0
                cfg["gbif_photo_col"] = st.selectbox(
                    "Sloupec se jménem druhu pro GBIF fotky", 
                    options=columns, 
                    index=gbif_photo_col_idx,
                    key="w_gbif_photo_col"
                )
                
            cfg["enable_pladias"] = st.checkbox(
                "Aktivovat odkaz na Pladias",
                value=cfg.get("enable_pladias", False),
                key="w_enable_pladias"
            )
            if cfg.get("enable_pladias", False):
                pladias_col_val = cfg.get("pladias_col", columns[0])
                try:
                    pladias_col_idx = columns.index(pladias_col_val)
                except ValueError:
                    pladias_col_idx = 0
                cfg["pladias_col"] = st.selectbox(
                    "Sloupec s vědeckým jménem druhu pro Pladias",
                    options=columns, 
                    index=pladias_col_idx,
                    key="w_pladias_col"
                )
                
        with tab_zoologie:
            st.markdown("##### Specifická nastavení pro zoologii")
            cfg["enable_gbif_zoo"] = st.checkbox(
                "Aktivovat GBIF fotky - Zoologie",
                value=cfg.get("enable_gbif_zoo", False),
                key="w_enable_gbif_zoo"
            )
            if cfg.get("enable_gbif_zoo", False):
                gbif_zoo_col_val = cfg.get("gbif_zoo_col", columns[0])
                try:
                    gbif_zoo_col_idx = columns.index(gbif_zoo_col_val)
                except ValueError:
                    gbif_zoo_col_idx = 0
                cfg["gbif_zoo_col"] = st.selectbox(
                    "Sloupec s vědeckým jménem druhu pro zoologii",
                    options=columns, 
                    index=gbif_zoo_col_idx,
                    key="w_gbif_zoo_col"
                )
                cfg["gbif_zoo_max"] = st.slider(
                    "Max fotek z GBIF Zoologie na řádek",
                    1, 5,
                    value=cfg.get("gbif_zoo_max", 3),
                    key="w_gbif_zoo_max"
                )
            
            st.markdown("---")
            cfg["enable_bird_sounds"] = st.checkbox(
                "Aktivovat hlasy ptáků (Xeno-canto)",
                value=cfg.get("enable_bird_sounds", False),
                key="w_enable_bird_sounds"
            )
            if cfg.get("enable_bird_sounds", False):
                bird_col_val = cfg.get("bird_sounds_col", columns[0])
                try:
                    bird_col_idx = columns.index(bird_col_val)
                except ValueError:
                    bird_col_idx = 0
                cfg["bird_sounds_col"] = st.selectbox(
                    "Sloupec s vědeckým jménem druhu (Xeno-canto)",
                    options=columns, 
                    index=bird_col_idx,
                    key="w_bird_sounds_col"
                )
                st.markdown("**Typ nahrávky** (lze kombinovat):")
                c_song, c_call = st.columns(2)
                with c_song:
                    cfg["bird_sounds_song"] = st.checkbox(
                        "Zpěv (song)",
                        value=cfg.get("bird_sounds_song", True),
                        key="w_bird_sounds_song"
                    )
                with c_call:
                    cfg["bird_sounds_call"] = st.checkbox(
                        "Hlas / volání (call)",
                        value=cfg.get("bird_sounds_call", False),
                        key="w_bird_sounds_call"
                    )
                cfg["bird_sounds_max"] = st.slider(
                    "Počet nahrávek na typ",
                    1, 3,
                    value=cfg.get("bird_sounds_max", 1),
                    key="w_bird_sounds_max"
                )
                cfg["xc_api_key"] = GLOBAL_CONFIG.get("xc_api_key", "")
                st.caption("Nahrávky se stáhnou jako MP3 a přiloží do Anki balíčku.")

        # Společná část pod záložkami
        st.markdown("<hr style='margin: 15px 0 10px 0;'>", unsafe_allow_html=True)
        st.markdown("##### Obecná nastavení biologie")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            cfg["enable_inat"] = st.checkbox(
                "Aktivovat iNaturalist (České jméno & Obrázky)", 
                value=cfg.get("enable_inat", False),
                key="w_enable_inat"
            )
            if cfg.get("enable_inat", False):
                inat_col_val = cfg.get("inat_col", columns[0])
                try:
                    inat_col_idx = columns.index(inat_col_val)
                except ValueError:
                    inat_col_idx = 0
                cfg["inat_col"] = st.selectbox(
                    "Sloupec s vědeckým jménem druhu (iNaturalist)", 
                    options=columns, 
                    index=inat_col_idx,
                    key="w_inat_col"
                )
                cfg["inat_max"] = st.slider(
                    "Max fotek z iNat na řádek", 
                    1, 5, 
                    value=cfg.get("inat_max", 4),
                    key="w_inat_max"
                )

            st.markdown("---")
            cfg["enable_desc"] = st.checkbox(
                "Aktivovat vědecký popis druhu (Wikipedie EN)", 
                value=cfg.get("enable_desc", False),
                key="w_enable_desc"
            )
            if cfg.get("enable_desc", False):
                desc_col_val = cfg.get("desc_col", columns[0])
                try:
                    desc_col_idx = columns.index(desc_col_val)
                except ValueError:
                    desc_col_idx = 0
                cfg["desc_col"] = st.selectbox(
                    "Sloupec s vědeckým jménem druhu pro popis", 
                    options=columns, 
                    index=desc_col_idx,
                    key="w_desc_col"
                )
                st.caption("Stáhne anglický vědecký popis z Wikipedie – funguje pro rostliny i živočichy.")
                
        with col_b2:
            cfg["enable_gbif"] = st.checkbox(
                "Aktivovat GBIF Taxonomii (kmen, třída, čeleď...)", 
                value=cfg.get("enable_gbif", False),
                key="w_enable_gbif"
            )
            if cfg.get("enable_gbif", False):
                gbif_col_val = cfg.get("gbif_col", columns[0])
                try:
                    gbif_col_idx = columns.index(gbif_col_val)
                except ValueError:
                    gbif_col_idx = 0
                cfg["gbif_col"] = st.selectbox(
                    "Sloupec s vědeckým jménem k zařazení", 
                    options=columns, 
                    index=gbif_col_idx,
                    key="w_gbif_col"
                )
                
            st.markdown("---")
            cfg["enable_wiki_img"] = st.checkbox(
                "Aktivovat Wikimedia Commons vyhledávač obrázků", 
                value=cfg.get("enable_wiki_img", False),
                key="w_enable_wiki_img"
            )
            if cfg.get("enable_wiki_img", False):
                wiki_col_val = cfg.get("wiki_col", columns[0])
                try:
                    wiki_col_idx = columns.index(wiki_col_val)
                except ValueError:
                    wiki_col_idx = 0
                cfg["wiki_col"] = st.selectbox(
                    "Sloupec s vyhledávaným slovem pro obrázek", 
                    options=columns, 
                    index=wiki_col_idx,
                    key="w_wiki_col"
                )
                cfg["wiki_max"] = st.slider(
                    "Max fotek z Wikimedia Commons na řádek", 
                    1, 5, 
                    value=cfg.get("wiki_max", 3),
                    key="w_wiki_max"
                )
                
            st.markdown("---")
            cfg["enable_wiki_link"] = st.checkbox(
                "Aktivovat odkaz na Wikipedii",
                value=cfg.get("enable_wiki_link", False),
                key="w_enable_wiki_link"
            )
            if cfg.get("enable_wiki_link", False):
                wiki_link_col_val = cfg.get("wiki_link_col", columns[0])
                try:
                    wiki_link_col_idx = columns.index(wiki_link_col_val)
                except ValueError:
                    wiki_link_col_idx = 0
                cfg["wiki_link_col"] = st.selectbox(
                    "Sloupec s vědeckým jménem pro Wikipedii",
                    options=columns, 
                    index=wiki_link_col_idx,
                    key="w_wiki_link_col"
                )

    elif selected_topic == "Jazyky":
        st.markdown("#### Moduly pro cizí jazyky a slovní zásobu")
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            cfg["enable_trans"] = st.checkbox(
                "Aktivovat překladač", 
                value=cfg.get("enable_trans", False),
                key="w_enable_trans"
            )
            
            trans_col_val = cfg.get("trans_col", columns[0])
            try:
                trans_col_idx = columns.index(trans_col_val)
            except ValueError:
                trans_col_idx = 0
            cfg["trans_col"] = st.selectbox(
                "Sloupec s textem k překladu", 
                options=columns, 
                index=trans_col_idx,
                key="w_trans_col"
            )
            
            lang_keys = list(languages.keys())
            trans_src_val = cfg.get("trans_src", "Angličtina")
            try:
                trans_src_idx = lang_keys.index(trans_src_val)
            except ValueError:
                trans_src_idx = 0
            cfg["trans_src"] = st.selectbox(
                "Zdrojový jazyk", 
                options=lang_keys, 
                index=trans_src_idx,
                key="w_trans_src"
            )
            
            trans_tgt_val = cfg.get("trans_tgt", "Čeština")
            try:
                trans_tgt_idx = lang_keys.index(trans_tgt_val)
            except ValueError:
                trans_tgt_idx = 1 if len(lang_keys) > 1 else 0
            cfg["trans_tgt"] = st.selectbox(
                "Cílový jazyk", 
                options=lang_keys, 
                index=trans_tgt_idx,
                key="w_trans_tgt"
            )
            
        with col_l2:
            cfg["enable_tts"] = st.checkbox(
                "Aktivovat hlasovou výslovnost (Google TTS)", 
                value=cfg.get("enable_tts", False),
                key="w_enable_tts"
            )
            
            tts_col_val = cfg.get("tts_col", columns[0])
            try:
                tts_col_idx = columns.index(tts_col_val)
            except ValueError:
                tts_col_idx = 0
            cfg["tts_col"] = st.selectbox(
                "Sloupec s textem k namluvení", 
                options=columns, 
                index=tts_col_idx,
                key="w_tts_col"
            )
            
            tts_lang_val = cfg.get("tts_lang", "Angličtina")
            try:
                tts_lang_idx = lang_keys.index(tts_lang_val)
            except ValueError:
                tts_lang_idx = 0
            cfg["tts_lang"] = st.selectbox(
                "Jazyk výslovnosti", 
                options=lang_keys, 
                index=tts_lang_idx,
                key="w_tts_lang"
            )
            
            cfg["enable_dict"] = st.checkbox(
                "Aktivovat anglický výkladový slovník", 
                value=cfg.get("enable_dict", False),
                key="w_enable_dict"
            )
            
            dict_col_val = cfg.get("dict_col", columns[0])
            try:
                dict_col_idx = columns.index(dict_col_val)
            except ValueError:
                dict_col_idx = 0
            cfg["dict_col"] = st.selectbox(
                "Sloupec s anglickým slovem k definici", 
                options=columns, 
                index=dict_col_idx,
                key="w_dict_col"
            )

    elif selected_topic == "Zeměpis":
        st.markdown("#### Moduly pro zeměpis a státy")
        cfg["enable_country"] = st.checkbox(
            "Aktivovat modul států (hlavní město, region, měna, vlajka...)", 
            value=cfg.get("enable_country", False),
            key="w_enable_country"
        )
        
        country_col_val = cfg.get("country_col", columns[0])
        try:
            country_col_idx = columns.index(country_col_val)
        except ValueError:
            country_col_idx = 0
        cfg["country_col"] = st.selectbox(
            "Sloupec s názvem státu (česky nebo anglicky)", 
            options=columns, 
            index=country_col_idx,
            key="w_country_col"
        )

    # Přehled aktivních modulů
    active = [k.replace("enable_","") for k in ["enable_inat","enable_gbif","enable_gbif_kvet",
              "enable_gbif_list","enable_pladias","enable_gbif_zoo","enable_wiki_link",
              "enable_trans","enable_tts","enable_dict","enable_country",
              "enable_wiki_img"] if cfg.get(k, False)]
    if active:
        st.info(f"Aktivní moduly: **{', '.join(active)}**")

    st.markdown("---")
    
    # Spuštění obohacení
    if st.button("Spustit obohacení dat (API)"):
        # Načíst aktuální hodnoty ze session_state (přežijí přepnutí tabu)
        cfg = st.session_state.api_config
        enable_inat = cfg.get("enable_inat", False)
        enable_gbif = cfg.get("enable_gbif", False)
        enable_desc = cfg.get("enable_desc", False)
        enable_gbif_kvet = cfg.get("enable_gbif_kvet", False)
        enable_gbif_list = cfg.get("enable_gbif_list", False)
        enable_pladias = cfg.get("enable_pladias", False)
        enable_gbif_zoo = cfg.get("enable_gbif_zoo", False)
        enable_bird_sounds = cfg.get("enable_bird_sounds", False)
        enable_wiki_link = cfg.get("enable_wiki_link", False)
        enable_trans = cfg.get("enable_trans", False)
        enable_tts = cfg.get("enable_tts", False)
        enable_dict = cfg.get("enable_dict", False)
        enable_wiki_img = cfg.get("enable_wiki_img", False)
        enable_country = cfg.get("enable_country", False)
        trans_src = cfg.get("trans_src", "Angličtina")
        trans_tgt = cfg.get("trans_tgt", "Čeština")
        
        inat_col = cfg.get("inat_col", columns[0] if columns else "")
        inat_max_photos = cfg.get("inat_max", 4)
        desc_col = cfg.get("desc_col", columns[0] if columns else "")
        desc_type_val = cfg.get("desc_type", "Vědecký anglický (popis, habitat, listy...)")
        gbif_col = cfg.get("gbif_col", columns[0] if columns else "")
        gbif_photo_col = cfg.get("gbif_photo_col", columns[0] if columns else "")
        pladias_col = cfg.get("pladias_col", columns[0] if columns else "")
        gbif_zoo_col = cfg.get("gbif_zoo_col", columns[0] if columns else "")
        gbif_zoo_max = cfg.get("gbif_zoo_max", 3)
        bird_sounds_col = cfg.get("bird_sounds_col", columns[0] if columns else "")
        bird_sounds_song = cfg.get("bird_sounds_song", True)
        bird_sounds_call = cfg.get("bird_sounds_call", False)
        bird_sounds_max = cfg.get("bird_sounds_max", 1)
        xc_api_key = cfg.get("xc_api_key") or GLOBAL_CONFIG.get("xc_api_key", "")
        wiki_link_col = cfg.get("wiki_link_col", columns[0] if columns else "")
        trans_col = cfg.get("trans_col", columns[0] if columns else "")
        tts_col = cfg.get("tts_col", columns[0] if columns else "")
        tts_lang = cfg.get("tts_lang", "Angličtina")
        dict_col = cfg.get("dict_col", columns[0] if columns else "")
        wiki_img_col = cfg.get("wiki_col", columns[0] if columns else "")
        wiki_max_photos = cfg.get("wiki_max", 3)
        country_col = cfg.get("country_col", columns[0] if columns else "")
 
 
        progress_bar = st.progress(0.0)
        status = st.empty()
        
        new_df = df.copy()
        
        # Vytvoření nových sloupců v DataFrame
        if enable_inat:
            new_df["[iNat] České jméno"] = ""
            new_df["[iNat] Obrázky (URL)"] = ""
        if enable_desc:
            new_df["[Popis] Botanický popis"] = ""
        if enable_gbif:
            new_df["[Taxonomie] Říše"] = ""
            new_df["[Taxonomie] Kmen"] = ""
            new_df["[Taxonomie] Třída"] = ""
            new_df["[Taxonomie] Řád"] = ""
            new_df["[Taxonomie] Čeleď"] = ""
            new_df["[Taxonomie] Rod"] = ""
        if enable_wiki_img:
            new_df["[Wikimedia] Obrázky (URL)"] = ""
        if enable_trans:
            new_df[f"[Překlad] {trans_tgt}"] = ""
        if enable_tts:
            new_df["[TTS] Výslovnost (Audio)"] = ""
        if enable_dict:
            new_df["[Slovník] Výslovnost (Text)"] = ""
            new_df["[Slovník] Definice"] = ""
            new_df["[Slovník] Příkladová věta"] = ""
        if enable_country:
            new_df["[Zeměpis] Český název"] = ""
            new_df["[Zeměpis] Hlavní město"] = ""
            new_df["[Zeměpis] Region"] = ""
            new_df["[Zeměpis] Jazyky"] = ""
            new_df["[Zeměpis] Měna"] = ""
            new_df["[Zeměpis] Rozloha"] = ""
            new_df["[Zeměpis] Vlajka (URL)"] = ""
            
        if enable_gbif_kvet:
            new_df["[GBIF] Květ"] = ""
        if enable_gbif_list:
            new_df["[GBIF] List"] = ""
        if enable_pladias:
            new_df["[Pladias] Odkaz"] = ""
        if enable_gbif_zoo:
            new_df["[GBIF] Zoologie"] = ""
        if enable_wiki_link:
            new_df["[Wikipedie] Odkaz"] = ""
        if enable_bird_sounds:
            new_df["[Zvuky] Hlasy ptáků"] = ""
            
        unfound_list = []
        total = len(df)
        
        for idx, row in df.iterrows():
            progress_bar.progress((idx + 1) / total)
            status.text(f"Obohacuji řádek {idx+1}/{total}...")
            
            # 1. iNaturalist
            if enable_inat:
                raw_sp = str(row[inat_col]).strip()
                sp = re.sub(r'\s*\(.*\)\s*', '', raw_sp).strip()
                sp_clean = re.sub(r'\s+sp(p)?\.?$', '', sp).strip()
                
                inat_data = fetch_inaturalist_data(sp_clean, inat_max_photos)
                
                if inat_data['source'] == 'Nenalezeno':
                    unfound_list.append({'Řádek': idx + 1, 'Položka': raw_sp, 'Modul': 'iNaturalist'})
                
                new_df.at[idx, "[iNat] České jméno"] = inat_data['common_name']
                new_df.at[idx, "[iNat] Obrázky (URL)"] = ";".join(inat_data['photo_urls'])
                
            # 1b. Vědecký popis druhu (rostliny i živočichové)
            if enable_desc:
                raw_sp = str(row[desc_col]).strip()
                sp = re.sub(r'\s*\(.*\)\s*', '', raw_sp).strip()
                sp_clean = re.sub(r'\s+sp(p)?\.?$', '', sp).strip()
                
                desc_text = fetch_wiki_description(sp_clean)
                
                if not desc_text:
                    unfound_list.append({'Řádek': idx + 1, 'Položka': raw_sp, 'Modul': 'Vědecký popis (Wikipedie)'})
                
                new_df.at[idx, "[Popis] Botanický popis"] = desc_text
                
            # 2. GBIF Taxonomie
            if enable_gbif:
                raw_sp = str(row[gbif_col]).strip()
                sp = re.sub(r'\s*\(.*\)\s*', '', raw_sp).strip()
                sp_clean = re.sub(r'\s+sp(p)?\.?$', '', sp).strip()
                gbif_data = fetch_gbif_taxonomy(sp_clean)
                if gbif_data['source'] == 'Nenalezeno':
                    unfound_list.append({'Řádek': idx + 1, 'Položka': raw_sp, 'Modul': 'GBIF Taxonomie'})
                new_df.at[idx, "[Taxonomie] Říše"] = gbif_data['kingdom']
                new_df.at[idx, "[Taxonomie] Kmen"] = gbif_data['phylum']
                new_df.at[idx, "[Taxonomie] Třída"] = gbif_data['class']
                new_df.at[idx, "[Taxonomie] Řád"] = gbif_data['order']
                new_df.at[idx, "[Taxonomie] Čeleď"] = gbif_data['family']
                new_df.at[idx, "[Taxonomie] Rod"] = gbif_data['genus']
                
            # GBIF Vyhledávač fotek rostlin (Květ / List)
            if enable_gbif_kvet or enable_gbif_list:
                raw_sp = str(row[gbif_photo_col]).strip()
                gbif_photo_data = fetch_gbif_plant_photos(raw_sp, get_kvet=enable_gbif_kvet, get_list=enable_gbif_list)
                
                found_any = any(gbif_photo_data[k] for k in ["kvet", "list"])
                if not found_any:
                    unfound_list.append({'Řádek': idx + 1, 'Položka': raw_sp, 'Modul': 'GBIF Fotografie'})
                
                if enable_gbif_kvet:
                    new_df.at[idx, "[GBIF] Květ"] = gbif_photo_data["kvet"]
                if enable_gbif_list:
                    new_df.at[idx, "[GBIF] List"] = gbif_photo_data["list"]

            # 5. Wikimedia Commons
            if enable_wiki_img:
                kw = str(row[wiki_img_col]).strip()
                wiki_urls = fetch_wikimedia_images(kw, wiki_max_photos)
                if not wiki_urls:
                    unfound_list.append({'Řádek': idx + 1, 'Položka': kw, 'Modul': 'Wikimedia Commons'})
                new_df.at[idx, "[Wikimedia] Obrázky (URL)"] = ";".join(wiki_urls)
                
            # 6. Překlad
            if enable_trans:
                txt = str(row[trans_col]).strip()
                src_code = languages[trans_src]
                tgt_code = languages[trans_tgt]
                translated = translate_text(txt, src_code, tgt_code)
                new_df.at[idx, f"[Překlad] {trans_tgt}"] = translated
                
            # 7. Google TTS
            if enable_tts:
                txt = str(row[tts_col]).strip()
                lang_code = languages[tts_lang]
                if txt:
                    new_df.at[idx, "[TTS] Výslovnost (Audio)"] = f"{txt};{lang_code}"
                    
            # 8. Dictionary API
            if enable_dict:
                wd = str(row[dict_col]).strip()
                dict_data = fetch_dictionary_data(wd)
                if not dict_data['definition']:
                    unfound_list.append({'Řádek': idx + 1, 'Položka': wd, 'Modul': 'Slovník'})
                new_df.at[idx, "[Slovník] Výslovnost (Text)"] = dict_data['phonetic']
                new_df.at[idx, "[Slovník] Definice"] = dict_data['definition']
                new_df.at[idx, "[Slovník] Příkladová věta"] = dict_data['example']
                
            # Pladias odkaz
            if enable_pladias:
                raw_sp = str(row[pladias_col]).strip()
                sp_clean = re.sub(r'\s*\(.*\)\s*', '', raw_sp).strip()
                sp_clean = re.sub(r'\s+sp(p)?\.?$', '', sp_clean).strip()
                encoded_sp = urllib.parse.quote(sp_clean)
                new_df.at[idx, "[Pladias] Odkaz"] = f"https://pladias.cz/taxon/overview/{encoded_sp}"
                
            # GBIF Zoologie fotky
            if enable_gbif_zoo:
                raw_sp = str(row[gbif_zoo_col]).strip()
                zoo_photos = fetch_gbif_zoo_photos(raw_sp, max_photos=gbif_zoo_max)
                if not zoo_photos:
                    unfound_list.append({'Řádek': idx + 1, 'Položka': raw_sp, 'Modul': 'GBIF Zoologie'})
                new_df.at[idx, "[GBIF] Zoologie"] = ";".join(zoo_photos)
                
            # Wikipedia odkaz
            if enable_wiki_link:
                raw_sp = str(row[wiki_link_col]).strip()
                sp_clean = re.sub(r'\s*\(.*\)\s*', '', raw_sp).strip()
                sp_clean = re.sub(r'\s+sp(p)?\.?$', '', sp_clean).strip()
                slug_sp = sp_clean.replace(' ', '_')
                new_df.at[idx, "[Wikipedie] Odkaz"] = f"https://cs.wikipedia.org/wiki/{slug_sp}"
                
            # Hlasy ptáků (Xeno-canto API v3)
            if enable_bird_sounds:
                raw_sp = str(row[bird_sounds_col]).strip()
                sound_types_req = []
                if bird_sounds_song:
                    sound_types_req.append("song")
                if bird_sounds_call:
                    sound_types_req.append("call")
                if not sound_types_req:
                    sound_types_req = ["song"]
                sound_results = fetch_bird_sounds_xenocanto(
                    raw_sp,
                    sound_types=sound_types_req,
                    max_sounds=bird_sounds_max,
                    api_key=xc_api_key
                )
                if not sound_results:
                    unfound_list.append({'Řádek': idx + 1, 'Položka': raw_sp, 'Modul': 'Hlasy ptáků (Xeno-canto)'})
                # Uložit jako "url|typ;url|typ"
                new_df.at[idx, "[Zvuky] Hlasy ptáků"] = ";".join(f"{u}|{t}" for u, t in sound_results)
                
            # 12. Zeměpis & Státy
            if enable_country:
                c_name = str(row[country_col]).strip()
                c_data = fetch_country_data(c_name, countries_db)
                if c_data['source'] == 'Nenalezeno':
                    unfound_list.append({'Řádek': idx + 1, 'Položka': c_name, 'Modul': 'Zeměpis'})
                new_df.at[idx, "[Zeměpis] Český název"] = c_data['common_name']
                new_df.at[idx, "[Zeměpis] Hlavní město"] = c_data['capital']
                new_df.at[idx, "[Zeměpis] Region"] = f"{c_data['region']} ({c_data['subregion']})" if c_data['subregion'] else c_data['region']
                new_df.at[idx, "[Zeměpis] Jazyky"] = c_data['languages']
                new_df.at[idx, "[Zeměpis] Měna"] = c_data['currencies']
                new_df.at[idx, "[Zeměpis] Rozloha"] = c_data['area']
                new_df.at[idx, "[Zeměpis] Vlajka (URL)"] = c_data['flag_url']
                
            time.sleep(0.4)
            
        st.session_state.df = new_df
        st.session_state.enhancements_applied = True
        st.session_state.unfound_list = unfound_list
        st.success("Obohacení dat bylo úspěšně dokončeno. Tabulka byla rozšířena o nové sloupce.")
        st.rerun()

    # --- KROK 3: MAPOVÁNÍ KARET (FRONT / BACK DESIGNER) ---
    st.markdown("---")
    st.markdown("### Mapování stran a vzhled kartiček")
    
    col_lay1, col_lay2, col_lay3 = st.columns([2, 2, 1])
    
    with col_lay1:
        st.markdown("#### 1. Lícová strana (Front)")
        front_cols = st.multiselect(
            "Vyberte sloupce, které se zobrazí na LÍCI karty:",
            options=columns,
            default=[columns[0]] if columns else [],
            key="front_cols_multiselect"
        )
        sync_ordered_cols(front_cols, "front_cols_ordered")
        
        st.markdown("##### Uspořádání sloupců na líci:")
        for i, col in enumerate(st.session_state.front_cols_ordered):
            if col not in st.session_state.col_styles:
                sample_val = ""
                if st.session_state.df is not None and not st.session_state.df.empty and col in st.session_state.df.columns:
                    sample_val = st.session_state.df[col].iloc[0]
                is_img = is_image_col(col, sample_val)
                st.session_state.col_styles[col] = {
                    "bold": False,
                    "italic": False,
                    "size": "Výchozí",
                    "custom_label": col,
                    "show_label": not is_img
                }
            
            c_name, c_up, c_down = st.columns([6, 1, 1])
            with c_name:
                st.write(f"**{col}**")
            with c_up:
                if st.button("▲", key=f"up_front_{col}_{i}"):
                    if i > 0:
                        st.session_state.front_cols_ordered[i], st.session_state.front_cols_ordered[i-1] = st.session_state.front_cols_ordered[i-1], st.session_state.front_cols_ordered[i]
                        st.rerun()
            with c_down:
                if st.button("▼", key=f"down_front_{col}_{i}"):
                    if i < len(st.session_state.front_cols_ordered) - 1:
                        st.session_state.front_cols_ordered[i], st.session_state.front_cols_ordered[i+1] = st.session_state.front_cols_ordered[i+1], st.session_state.front_cols_ordered[i]
                        st.rerun()
        
    with col_lay2:
        st.markdown("#### 2. Rubová strana (Back)")
        default_back = [c for c in columns if c not in front_cols and not c.startswith("[")]
        if not default_back and columns:
            default_back = [columns[0]]
        back_cols = st.multiselect(
            "Vyberte sloupce, které se zobrazí na RUBU karty:",
            options=columns,
            default=default_back,
            key="back_cols_multiselect"
        )
        sync_ordered_cols(back_cols, "back_cols_ordered")
        
        st.markdown("##### Uspořádání sloupců na rubu:")
        for i, col in enumerate(st.session_state.back_cols_ordered):
            if col not in st.session_state.col_styles:
                sample_val = ""
                if st.session_state.df is not None and not st.session_state.df.empty and col in st.session_state.df.columns:
                    sample_val = st.session_state.df[col].iloc[0]
                is_img = is_image_col(col, sample_val)
                st.session_state.col_styles[col] = {
                    "bold": False,
                    "italic": False,
                    "size": "Výchozí",
                    "custom_label": col,
                    "show_label": not is_img
                }
            
            c_name, c_up, c_down = st.columns([6, 1, 1])
            with c_name:
                st.write(f"**{col}**")
            with c_up:
                if st.button("▲", key=f"up_back_{col}_{i}"):
                    if i > 0:
                        st.session_state.back_cols_ordered[i], st.session_state.back_cols_ordered[i-1] = st.session_state.back_cols_ordered[i-1], st.session_state.back_cols_ordered[i]
                        st.rerun()
            with c_down:
                if st.button("▼", key=f"down_back_{col}_{i}"):
                    if i < len(st.session_state.back_cols_ordered) - 1:
                        st.session_state.back_cols_ordered[i], st.session_state.back_cols_ordered[i+1] = st.session_state.back_cols_ordered[i+1], st.session_state.back_cols_ordered[i]
                        st.rerun()
        
    with col_lay3:
        st.markdown("#### Vzhled a rozvržení")
        card_theme = st.selectbox(
            "Barevný režim karet:",
            [
                "Obojetný (automaticky přepínatelný)",
                "Tmavý režim (vždy tmavé)",
                "Světlý režim (vždy světlé)"
            ],
            index=0
        )
        st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
        card_layout_choice = st.radio(
            "Zobrazení po kliknutí na odpověď:",
            ["Pod sebe (líc + rub)", "Na druhou stranu (pouze rub)"],
            index=0,
            key="card_layout_radio"
        )
        
    # Stylování sloupců
    all_selected_cols = list(dict.fromkeys(st.session_state.front_cols_ordered + st.session_state.back_cols_ordered))
    if all_selected_cols:
        st.markdown("#### Pokročilé nastavení zobrazení sloupců")
        for col in all_selected_cols:
            if col not in st.session_state.col_styles:
                sample_val = ""
                if st.session_state.df is not None and not st.session_state.df.empty and col in st.session_state.df.columns:
                    sample_val = st.session_state.df[col].iloc[0]
                is_img = is_image_col(col, sample_val)
                st.session_state.col_styles[col] = {
                    "bold": False,
                    "italic": False,
                    "size": "Výchozí",
                    "custom_label": col,
                    "show_label": not is_img
                }
            
            style = st.session_state.col_styles[col]
            with st.expander(f"Nastavení zobrazení sloupce: {col}"):
                sc1, sc2, sc3 = st.columns(3)
                with sc1:
                    style["bold"] = st.checkbox("Tučné (Bold)", value=style["bold"], key=f"style_bold_{col}")
                    style["italic"] = st.checkbox("Kurzíva (Italic)", value=style["italic"], key=f"style_italic_{col}")
                with sc2:
                    sizes = ["Výchozí", "Malé (12px)", "Střední (16px)", "Velké (20px)", "Obrovské (24px)"]
                    current_idx = sizes.index(style["size"]) if style["size"] in sizes else 0
                    style["size"] = st.selectbox(
                        "Velikost písma:",
                        sizes,
                        index=current_idx,
                        key=f"style_size_{col}"
                    )
                with sc3:
                    style["show_label"] = st.checkbox("Zobrazit název sloupce", value=style["show_label"], key=f"style_show_lbl_{col}")
                    style["custom_label"] = st.text_input("Vlastní název sloupce:", value=style["custom_label"], key=f"style_cust_lbl_{col}")
        
    # Náhled karty
    if st.session_state.front_cols_ordered or st.session_state.back_cols_ordered:
        st.markdown("#### Vizuální náhled kartičky (1. řádek tabulky)")
        preview_row = df.iloc[0]
        col_pre1, col_pre2 = st.columns(2)
        
        # Výpočet barev pro náhled
        if card_theme == "Světlý režim (vždy světlé)":
            preview_bg = "#f7faf8"
            preview_fg = "#1e2923"
            preview_border = "#dce8e0"
            preview_label = "#4d735d"
        else:
            preview_bg = "#121c16"
            preview_fg = "#e5ede8"
            preview_border = "#23362b"
            preview_label = "#8da897"
            
        with col_pre1:
            st.markdown("**LÍC (Front):**")
            st.markdown(f'<div class="card-preview-container" style="background-color: {preview_bg}; border: 1px solid {preview_border}; border-radius: 6px; padding: 18px; color: {preview_fg};">', unsafe_allow_html=True)
            for c in st.session_state.front_cols_ordered:
                val = preview_row[c]
                if pd.isna(val) or str(val).strip() == "":
                    continue
                
                # Načíst styly
                show_label = True
                label_text = c
                if c in st.session_state.col_styles:
                    show_label = st.session_state.col_styles[c].get("show_label", True)
                    label_text = st.session_state.col_styles[c].get("custom_label", c)
                
                val_css = get_value_css(c)
                val_style_attr = f' style="{val_css}; color: {preview_fg};"' if val_css else f' style="color: {preview_fg};"'
                label_html = f'<span style="font-size: 11px; font-weight: 600; color: {preview_label}; text-transform: uppercase; border-bottom: 1px solid {preview_border}; display: block; margin-bottom: 4px; padding-bottom: 2px;">{label_text}</span>' if show_label else ''
                
                if is_image_col(c, val):
                    urls = [u.strip() for u in str(val).split(';') if u.strip()]
                    if label_html:
                        st.markdown(label_html, unsafe_allow_html=True)
                    for url in urls:
                        st.markdown(f'<div style="width: 100%; max-width: 450px; border-radius: 6px; overflow: hidden; border: 1px solid {preview_border}; margin: 8px 0;"><img src="{url}" style="width: 100%; height: auto; object-fit: contain; display: block;"></div>', unsafe_allow_html=True)
                elif str(c).startswith("[TTS]"):
                    st.info(f"Výslovnost (Audio): {str(val).split(';')[0]}")
                elif c == "[Zvuky] Hlasy ptáků":
                    entries = [e.strip() for e in str(val).split(';') if e.strip()]
                    if label_html:
                        st.markdown(label_html, unsafe_allow_html=True)
                    for entry in entries:
                        if '|' in entry:
                            su, stype = entry.rsplit('|', 1)
                        else:
                            su, stype = entry, "song"
                        su = su.strip()
                        if not su.startswith('http'):
                            continue
                        type_label = "Zpěv" if stype == "song" else "Hlas"
                        st.caption(type_label)
                        st.audio(su)
                else:
                    if label_html:
                        st.markdown(label_html, unsafe_allow_html=True)
                    val_str = str(val)
                    if val_str.startswith("http://") or val_str.startswith("https://"):
                        if "pladias.cz" in val_str:
                            val_str = f'<a href="{val_str}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Otevřít profil na Pladias.cz</a>'
                        elif "wikipedia.org" in val_str:
                            val_str = f'<a href="{val_str}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Otevřít profil na Wikipedii</a>'
                    elif not re.search(r'<[a-zA-Z0-9/]+[^>]*>', val_str):
                        val_str = val_str.replace('\n', '<br>')
                    st.markdown(f'<div{val_style_attr}>{val_str}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_pre2:
            st.markdown("**RUB (Back):**")
            st.markdown(f'<div class="card-preview-container" style="background-color: {preview_bg}; border: 1px solid {preview_border}; border-radius: 6px; padding: 18px; color: {preview_fg};">', unsafe_allow_html=True)
            if card_layout_choice != "Na druhou stranu (pouze rub)":
                st.markdown(f'<span style="color: {preview_label}; font-size: 11px;">[ Zde se zobrazí líc karty ]</span><hr style="margin: 12px 0; border: 0; border-top: 1px solid {preview_border};">', unsafe_allow_html=True)
            for c in st.session_state.back_cols_ordered:
                val = preview_row[c]
                if pd.isna(val) or str(val).strip() == "":
                    continue
                
                # Načíst styly
                show_label = True
                label_text = c
                if c in st.session_state.col_styles:
                    show_label = st.session_state.col_styles[c].get("show_label", True)
                    label_text = st.session_state.col_styles[c].get("custom_label", c)
                
                val_css = get_value_css(c)
                val_style_attr = f' style="{val_css}; color: {preview_fg};"' if val_css else f' style="color: {preview_fg};"'
                label_html = f'<span style="font-size: 11px; font-weight: 600; color: {preview_label}; text-transform: uppercase; border-bottom: 1px solid {preview_border}; display: block; margin-bottom: 4px; padding-bottom: 2px;">{label_text}</span>' if show_label else ''
                
                if is_image_col(c, val):
                    urls = [u.strip() for u in str(val).split(';') if u.strip()]
                    if label_html:
                        st.markdown(label_html, unsafe_allow_html=True)
                    for url in urls:
                        st.markdown(f'<div style="width: 100%; max-width: 450px; border-radius: 6px; overflow: hidden; border: 1px solid {preview_border}; margin: 8px 0;"><img src="{url}" style="width: 100%; height: auto; object-fit: contain; display: block;"></div>', unsafe_allow_html=True)
                elif str(c).startswith("[TTS]"):
                    st.info(f"Výslovnost (Audio): {str(val).split(';')[0]}")
                elif c == "[Zvuky] Hlasy ptáků":
                    entries = [e.strip() for e in str(val).split(';') if e.strip()]
                    if label_html:
                        st.markdown(label_html, unsafe_allow_html=True)
                    for entry in entries:
                        if '|' in entry:
                            su, stype = entry.rsplit('|', 1)
                        else:
                            su, stype = entry, "song"
                        su = su.strip()
                        if not su.startswith('http'):
                            continue
                        type_label = "Zpěv" if stype == "song" else "Hlas"
                        st.caption(type_label)
                        st.audio(su)
                else:
                    if label_html:
                        st.markdown(label_html, unsafe_allow_html=True)
                    val_str = str(val)
                    if val_str.startswith("http://") or val_str.startswith("https://"):
                        if "pladias.cz" in val_str:
                            val_str = f'<a href="{val_str}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Otevřít profil na Pladias.cz</a>'
                        elif "wikipedia.org" in val_str:
                            val_str = f'<a href="{val_str}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Otevřít profil na Wikipedii</a>'
                    elif not re.search(r'<[a-zA-Z0-9/]+[^>]*>', val_str):
                        val_str = val_str.replace('\n', '<br>')
                    st.markdown(f'<div{val_style_attr}>{val_str}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # --- KROK 4: EXPORT DO ANKI BALÍČKU ---
    st.markdown("---")
    st.markdown("### Generování balíčku Anki")
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        deck_name_input = st.text_input("Název balíčku (Anki Deck Name)", value="balíček")
    with col_exp2:
        subdeck_col_choice = st.selectbox(
            "Rozdělit do podbalíčků podle sloupce (volitelně):",
            ["— Bez rozdělení —"] + columns,
            index=0
        )
    
    if st.button("Generovat balíček (.apkg)"):
        st.session_state.api_errors = []
        clear_temp_on_finish = True
        if not st.session_state.front_cols_ordered and not st.session_state.back_cols_ordered:
            st.error("Musíte vybrat alespoň jeden sloupec pro Líc nebo Rub kartičky.")
        else:
            temp_dir = tempfile.mkdtemp()
            media_dir = os.path.join(temp_dir, "media")
            os.makedirs(media_dir, exist_ok=True)
            
            progress_bar = st.progress(0.0)
            status = st.empty()
            
            processed_notes = []
            downloaded_media = []
            
            card_layout_mode = st.session_state.get("card_layout_radio", "Pod sebe (líc + rub)")
            is_only_back = (card_layout_mode == "Na druhou stranu (pouze rub)")
            total = len(df)
            
            for idx, row in df.iterrows():
                progress_bar.progress((idx + 1) / total)
                status.text(f"Stahuji média a sestavuji kartu {idx+1}/{total}...")
                
                # Sestavení strany HTML
                def compile_side_html(selected_cols, row_idx, row_data):
                    html_parts = []
                    for col in selected_cols:
                        val = row_data[col]
                        if pd.isna(val) or str(val).strip() == "" or str(val).lower() == "nan":
                            continue
                            
                        # Načíst nastavení stylů pro tento sloupec
                        show_label = True
                        label_text = col
                        if 'col_styles' in st.session_state and col in st.session_state.col_styles:
                            show_label = st.session_state.col_styles[col].get("show_label", True)
                            label_text = st.session_state.col_styles[col].get("custom_label", col)
                        
                        val_css = get_value_css(col)
                        val_style_attr = f' style="{val_css}"' if val_css else ''
                        label_html = f'<span class="field-label">{label_text}</span>' if show_label else ''
                        
                        # TTS hlasový modul
                        if str(col).startswith("[TTS]"):
                            parts = str(val).split(';')
                            if len(parts) >= 2:
                                text_to_speak = parts[0].strip()
                                lang_code = parts[1].strip()
                                if text_to_speak and lang_code:
                                    try:
                                        safe_txt = slugify(text_to_speak)[:20]
                                        safe_filename = f"tts_{row_idx}_{safe_txt}_{lang_code}.mp3"
                                        local_path = os.path.join(media_dir, safe_filename)
                                        
                                        tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl={lang_code}&client=tw-ob&q={urllib.parse.quote(text_to_speak)}"
                                        r_audio = requests.get(tts_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
                                        if r_audio.status_code == 200:
                                            with open(local_path, 'wb') as f:
                                                f.write(r_audio.content)
                                            downloaded_media.append(local_path)
                                            html_parts.append(f"[sound:{safe_filename}]")
                                    except Exception:
                                        pass
                            continue
                            
                        # Xeno-canto hlasy ptáků (MP3/WAV URLs ze záznamu – formát "url|typ;url|typ")
                        if col == "[Zvuky] Hlasy ptáků":
                            entries = [e.strip() for e in str(val).split(';') if e.strip()]
                            for s_idx, entry in enumerate(entries):
                                if '|' in entry:
                                    sound_url, stype = entry.rsplit('|', 1)
                                else:
                                    sound_url, stype = entry, "song"
                                sound_url = sound_url.strip()
                                if not sound_url.startswith('http'):
                                    continue
                                raw_sp_name = str(row_data[row_data.index[0]]) if len(row_data) > 0 else f"druh_{row_idx}"
                                try:
                                    safe_sp = slugify(raw_sp_name)[:20]
                                    if not safe_sp:
                                        safe_sp = f"druh_{row_idx}"
                                    r_snd = requests.get(
                                        sound_url,
                                        headers={'User-Agent': 'Mozilla/5.0'},
                                        timeout=20, allow_redirects=True
                                    )
                                    if r_snd.status_code == 200 and len(r_snd.content) > 0:
                                        audio_content = r_snd.content
                                        ext = detect_audio_extension(audio_content, default_ext=".mp3")
                                        safe_filename = f"xc_{row_idx}_{s_idx}_{safe_sp}_{stype}{ext}"
                                        local_path = os.path.join(media_dir, safe_filename)
                                        with open(local_path, 'wb') as f:
                                            f.write(audio_content)
                                        if local_path not in downloaded_media:
                                            downloaded_media.append(local_path)
                                        type_label = "Zpěv" if stype == "song" else "Hlas"
                                        html_parts.append(
                                            f'<div class="card-field field-{slugify(col)}">'
                                            f'{label_html}'
                                            f'<div class="field-value">'
                                            f'<span style="font-weight: 600; font-size: 13px; display: block; margin-bottom: 2px;">{type_label}</span>'
                                            f'<audio controls controlslist="nodownload" preload="none" src="{safe_filename}"></audio>'
                                            f'</div>'
                                            f'</div>'
                                        )
                                except Exception as e:
                                    if 'api_errors' not in st.session_state:
                                        st.session_state.api_errors = []
                                    st.session_state.api_errors.append(f"Druh: {raw_sp_name}, Zvuk: {sound_url}, Chyba: {str(e)}")
                            continue
                            
                        # Speciální GBIF obrázkové sloupce
                        is_gbif_photo = col in ["[GBIF] Habitus", "[GBIF] Květ", "[GBIF] List", "[GBIF] Plod", "[GBIF] Herbář"]
                        if is_gbif_photo and is_image_col(col, val):
                            urls = [u.strip() for u in str(val).split(';') if u.strip()]
                            
                            for url in urls:
                                if url.startswith('http://') or url.startswith('https://'):
                                    try:
                                        ext = ".jpg"
                                        if ".png" in url.lower():
                                            ext = ".png"
                                        elif ".jpeg" in url.lower():
                                            ext = ".jpeg"
                                            
                                        organ_map = {
                                            "[GBIF] Habitus": "habitus",
                                            "[GBIF] Květ": "kvet",
                                            "[GBIF] List": "list",
                                            "[GBIF] Plod": "plod",
                                            "[GBIF] Herbář": "herbar"
                                        }
                                        organ = organ_map.get(col, "foto")
                                        
                                        species_col = st.session_state.api_config.get("gbif_photo_col", columns[0])
                                        raw_species = str(row_data[species_col]).strip()
                                        clean_species = slugify_species_name(raw_species) if raw_species else f"druh_{row_idx}"
                                        
                                        safe_filename = f"{clean_species}_{organ}{ext}"
                                        local_path = os.path.join(media_dir, safe_filename)
                                        
                                        r_img = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=8)
                                        if r_img.status_code == 200:
                                            with open(local_path, 'wb') as f:
                                                f.write(r_img.content)
                                            
                                            if check_image_quality(local_path):
                                                downloaded_media.append(local_path)
                                                
                                                img_tag = f'<div class="photo-container"><img src="{safe_filename}"></div>'
                                                html_parts.append(
                                                    f'<div class="card-field field-{slugify(col)}">'
                                                    f'{label_html}'
                                                    f'<div class="photo-list">{img_tag}</div>'
                                                    f'</div>'
                                                )
                                                break
                                            else:
                                                if os.path.exists(local_path):
                                                    os.remove(local_path)
                                    except Exception as e:
                                        if 'api_errors' not in st.session_state:
                                            st.session_state.api_errors = []
                                        st.session_state.api_errors.append(f"Druh: {raw_species}, Sloupec: {col}, URL: {url}, Chyba: {str(e)}")
                            continue

                        # Obrázkový sloupec (iNaturalist, Wikimedia, GBIF Zoologie, Vlajky...)
                        if is_image_col(col, val):
                            urls = [u.strip() for u in str(val).split(';') if u.strip()]
                            local_filenames = []
                            
                            raw_sp_name = str(row_data[columns[0]]).strip() if len(columns) > 0 else f"druh_{row_idx}"
                            clean_sp = slugify_species_name(raw_sp_name) if raw_sp_name else f"druh_{row_idx}"
                            
                            for img_idx, url in enumerate(urls):
                                if not url.startswith('http://') and not url.startswith('https://'):
                                    continue
                                try:
                                    ext = ".jpg"
                                    if ".png" in url.lower():
                                        ext = ".png"
                                    elif ".jpeg" in url.lower():
                                        ext = ".jpeg"
                                    elif ".webp" in url.lower():
                                        ext = ".webp"
                                        
                                    safe_col = slugify(col)[:12]
                                    url_hash = hashlib.sha256(url.encode('utf-8')).hexdigest()[:6]
                                    safe_filename = f"{clean_sp}_{safe_col}_{row_idx}_{img_idx}_{url_hash}{ext}"
                                    local_path = os.path.join(media_dir, safe_filename)
                                    
                                    r_img = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=12)
                                    if r_img.status_code == 200 and len(r_img.content) > 0:
                                        with open(local_path, 'wb') as f:
                                            f.write(r_img.content)
                                        if check_image_quality(local_path):
                                            local_filenames.append(safe_filename)
                                            if local_path not in downloaded_media:
                                                downloaded_media.append(local_path)
                                        else:
                                            if os.path.exists(local_path):
                                                os.remove(local_path)
                                except Exception as e:
                                    if 'api_errors' not in st.session_state:
                                        st.session_state.api_errors = []
                                    st.session_state.api_errors.append(f"Druh: {raw_sp_name}, Sloupec: {col}, URL: {url}, Chyba: {str(e)}")
                            
                            if local_filenames:
                                img_tags = "".join([
                                    f'<div class="photo-container">'
                                    f'<img src="{fn}">'
                                    f'</div>'
                                    for fn in local_filenames
                                ])
                                html_parts.append(
                                    f'<div class="card-field field-{slugify(col)}">'
                                    f'{label_html}'
                                    f'<div class="photo-list">{img_tags}</div>'
                                    f'</div>'
                                )
                        
                        # Speciální sloupce s hypertextovými odkazy (Pladias, Wikipedie)
                        elif col.startswith("[Pladias]") or (col.startswith("[Wikipedie]") and str(val).startswith("http")):
                            url = str(val).strip()
                            if "pladias.cz" in url:
                                link_label = "Otevřít profil na Pladias.cz"
                            else:
                                link_label = "Otevřít profil na Wikipedii"
                            html_parts.append(
                                f'<div class="card-field field-{slugify(col)}">'
                                f'{label_html}'
                                f'<div class="field-value"><a href="{url}" style="color: #48a973; font-weight: 600; text-decoration: underline; font-size: 0.95em;">{link_label}</a></div>'
                                f'</div>'
                            )
                            
                        # Běžný textový sloupec
                        else:
                            val_str = str(val)
                            if not re.search(r'<[a-zA-Z0-9/]+[^>]*>', val_str):
                                val_str = val_str.replace('\n', '<br>')
                                
                            html_parts.append(
                                f'<div class="card-field field-{slugify(col)}">'
                                f'{label_html}'
                                f'<div class="field-value"{val_style_attr}>{val_str}</div>'
                                f'</div>'
                            )
                    return "".join(html_parts)
                
                front_html = compile_side_html(st.session_state.front_cols_ordered, idx, row)
                back_html = compile_side_html(st.session_state.back_cols_ordered, idx, row)
                
                subdeck_val = ""
                if subdeck_col_choice != "— Bez rozdělení —":
                    raw_val = row.get(subdeck_col_choice)
                    if pd.notna(raw_val) and str(raw_val).strip() != "":
                        subdeck_val = str(raw_val).strip()
                        
                processed_notes.append({
                    'front': front_html,
                    'back': back_html,
                    'guid_src': str(row[columns[0]]) if columns else str(idx),
                    'subdeck_val': subdeck_val
                })
                
            status.text("Zapisuji balíček Anki (.apkg)...")
            
            # Sestavení balíčku
            schema_str = ",".join(st.session_state.front_cols_ordered) + "|" + ",".join(st.session_state.back_cols_ordered) + "|" + deck_name_input + "|" + card_layout_mode
            model_hash = hashlib.sha256(schema_str.encode('utf-8')).hexdigest()[:8]
            model_id = get_stable_id(deck_name_input + "_model_" + model_hash)
            deck_id = get_stable_id(deck_name_input)
            
            anki_afmt = """
<div class="card">
  {{Back}}
</div>
""" if is_only_back else ANKI_AFMT

            anki_model = genanki.Model(
                model_id,
                f'Universal Model for {deck_name_input}',
                fields=[
                    {'name': 'Front'},
                    {'name': 'Back'}
                ],
                templates=[
                    {
                        'name': 'Karta',
                        'qfmt': ANKI_QFMT,
                        'afmt': anki_afmt,
                    },
                ],
                css=get_anki_css(card_theme)
            )
            
            # Vytvoření balíčků (včetně podbalíčků)
            decks = {}
            parent_deck_id = get_stable_id(deck_name_input)
            parent_deck = genanki.Deck(parent_deck_id, deck_name_input)
            decks[deck_name_input] = parent_deck
            
            for note_data in processed_notes:
                content_hash = hashlib.sha256((note_data['front'] + "|" + note_data['back']).encode('utf-8')).hexdigest()[:8]
                note = genanki.Note(
                    model=anki_model,
                    fields=[
                        note_data['front'],
                        note_data['back']
                    ],
                    guid=genanki.guid_for(note_data['guid_src'] + "|" + model_hash + "|" + content_hash)
                )
                
                # Zjištění, do kterého balíčku karta patří
                target_deck_name = deck_name_input
                if subdeck_col_choice != "— Bez rozdělení —" and note_data.get('subdeck_val'):
                    target_deck_name = f"{deck_name_input}::{note_data['subdeck_val']}"
                    
                if target_deck_name not in decks:
                    sub_deck_id = get_stable_id(target_deck_name)
                    decks[target_deck_name] = genanki.Deck(sub_deck_id, target_deck_name)
                    
                decks[target_deck_name].add_note(note)
                
            apkg_filename = f"{slugify(deck_name_input)}.apkg"
            apkg_path = os.path.join(temp_dir, apkg_filename)
            
            unique_media = [f for f in list(dict.fromkeys(downloaded_media)) if os.path.exists(f) and os.path.getsize(f) > 0]
            anki_package = genanki.Package(list(decks.values()))
            anki_package.media_files = unique_media
            anki_package.write_to_file(apkg_path)
            
            status.text("Balíček Anki byl úspěšně vygenerován.")
            
            with open(apkg_path, "rb") as f:
                apkg_bytes = f.read()
                
            # Uložení výsledků do session_state pro perzistentní stahování
            st.session_state.generated_apkg_data = apkg_bytes
            st.session_state.generated_apkg_filename = apkg_filename
            st.session_state.notes_count = len(processed_notes)
            st.session_state.media_count = len(downloaded_media)
            
            if st.session_state.unfound_list:
                unfound_df = pd.DataFrame(st.session_state.unfound_list)
                st.session_state.unfound_csv_data = unfound_df.to_csv(index=False, encoding='utf-8-sig')
            else:
                st.session_state.unfound_csv_data = None
                
            if clear_temp_on_finish:
                shutil.rmtree(temp_dir, ignore_errors=True)
                
            st.success("Balíček Anki byl úspěšně vygenerován.")
            st.rerun()

    # --- ZOBRAZENÍ STAHUJÍCÍCH TLAČÍTEK (VŽDY KDYŽ JSOU K DISPOZICI V STATE) ---
    if st.session_state.generated_apkg_data is not None:
        st.markdown("---")
        st.markdown("### Stažení výsledků")
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.download_button(
                label="Stáhnout .apkg balíček",
                data=st.session_state.generated_apkg_data,
                file_name=st.session_state.generated_apkg_filename,
                mime="application/octet-stream",
                key="download_apkg_btn"
            )
            st.info(f"Balíček obsahuje **{st.session_state.notes_count}** kartiček a **{st.session_state.media_count}** souborů.")
            
        with col_res2:
            if st.session_state.unfound_csv_data is not None:
                st.warning("Některé položky nebyly při obohacení nalezeny.")
                st.download_button(
                    label="Stáhnout seznam nenalezených položek (.csv)",
                    data=st.session_state.unfound_csv_data,
                    file_name="nenalezene_polozky.csv",
                    mime="text/csv",
                    key="download_csv_btn"
                )
            else:
                st.success("Všechny položky byly úspěšně zpracovány.")
                
        if 'api_errors' in st.session_state and st.session_state.api_errors:
            with st.expander("Log chyb stahování"):
                for err in st.session_state.api_errors:
                    st.error(err)

