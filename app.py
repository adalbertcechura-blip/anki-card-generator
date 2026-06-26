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

# --- DYNAMICKÉ CSS PRO ANKI KARTY ---

def get_anki_css(theme_name):
    base_css = """
.card {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  padding: 20px;
  border-radius: 12px;
  max-width: 550px;
  margin: 0 auto;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.card-field {
  margin-bottom: 15px;
  text-align: left;
}

.card-field:last-child {
  margin-bottom: 0;
}

.field-label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: block;
  margin-bottom: 4px;
  padding-bottom: 2px;
}

.field-value {
  font-size: 16px;
  line-height: 1.5;
}

/* Svislý seznam obrázků pod sebou */
.photo-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin: 15px 0;
  align-items: center;
}

.photo-container {
  width: 100%;
  max-width: 480px;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s ease-in-out;
}

.photo-container:hover {
  transform: scale(1.02);
}

.photo-container img {
  width: 100%;
  height: auto;
  max-height: 350px;
  object-fit: cover;
  display: block;
  cursor: zoom-in;
}

.no-photo-placeholder {
  padding: 40px;
  border: 2px dashed;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 15px;
  text-align: center;
}

.card-divider {
  border: 0;
  height: 1px;
  margin: 15px 0;
}
"""

    if theme_name == "Světlý režim (vždy světlé)" or theme_name == "Světlý režim":
        color_css = """
.card {
  color: #2D3748;
  background-color: #F7FAFC;
}
.field-label {
  color: #718096;
  border-bottom: 1px solid #EDF2F7;
}
.field-value {
  color: #2D3748;
}
.photo-container {
  border: 2px solid #ffffff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.no-photo-placeholder {
  border-color: #CBD5E0;
  color: #718096;
}
.card-divider {
  background: #E2E8F0;
}
"""
    elif theme_name == "Tmavý režim (vždy tmavé)" or theme_name == "Tmavý režim":
        color_css = """
.card {
  color: #E2E8F0;
  background-color: #1A202C;
}
.field-label {
  color: #A0AEC0;
  border-bottom: 1px solid #4A5568;
}
.field-value {
  color: #E2E8F0;
}
.photo-container {
  border: 2px solid #2D3748;
  box-shadow: 0 4px 8px rgba(0,0,0,0.4);
}
.no-photo-placeholder {
  border-color: #4A5568;
  color: #A0AEC0;
}
.card-divider {
  background: #4A5568;
}
"""
    else:  # Obojetné (automaticky přepínatelné)
        color_css = """
/* Výchozí světlý vzhled */
.card {
  color: #2D3748;
  background-color: #F7FAFC;
}
.field-label {
  color: #718096;
  border-bottom: 1px solid #EDF2F7;
}
.field-value {
  color: #2D3748;
}
.photo-container {
  border: 2px solid #ffffff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.no-photo-placeholder {
  border-color: #CBD5E0;
  color: #718096;
}
.card-divider {
  background: #E2E8F0;
}

/* Tmavý vzhled pro Anki Night Mode */
.nightMode.card {
  background-color: #1A202C;
  color: #E2E8F0;
}
.nightMode .field-label {
  color: #A0AEC0;
  border-color: #4A5568;
}
.nightMode .field-value {
  color: #E2E8F0;
}
.nightMode .photo-container {
  border-color: #2D3748;
  box-shadow: 0 4px 8px rgba(0,0,0,0.4);
}
.nightMode .no-photo-placeholder {
  border-color: #4A5568;
  color: #A0AEC0;
}
.nightMode .card-divider {
  background: #4A5568;
}

/* Podpora prefers-color-scheme pro ostatní klienty */
@media (prefers-color-scheme: dark) {
  .card {
    background-color: #1A202C;
    color: #E2E8F0;
  }
  .field-label {
    color: #A0AEC0;
    border-color: #4A5568;
  }
  .field-value {
    color: #E2E8F0;
  }
  .photo-container {
    border-color: #2D3748;
    box-shadow: 0 4px 8px rgba(0,0,0,0.4);
  }
  .no-photo-placeholder {
    border-color: #4A5568;
    color: #A0AEC0;
  }
  .card-divider {
    background: #4A5568;
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

# 1. iNaturalist + Wikipedie botanický modul
def fetch_inaturalist_data(species_name, max_photos=4, scientific_desc=True):
    headers = {'User-Agent': 'AnkiSpeciesGenerator/1.0 (contact: adalb@example.com)'}
    res_data = {
        'common_name': "",
        'description': "",
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
        except Exception:
            pass

    if scientific_desc:
        encoded_slug = urllib.parse.quote(species_name.replace(' ', '_'))
        url_wiki_en = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&titles={encoded_slug}&format=json"
        try:
            r_en = requests.get(url_wiki_en, headers=headers, timeout=5)
            if r_en.status_code == 200:
                pages = r_en.json().get('query', {}).get('pages', {})
                page = list(pages.values())[0]
                if 'extract' in page:
                    text = page['extract']
                    
                    sections = {}
                    current_section = "Lead"
                    current_content = []
                    
                    lines = text.split('\n')
                    for line in lines:
                        match = re.match(r'^==\s*(.*?)\s*==$', line)
                        if match:
                            sections[current_section.strip().lower()] = '\n'.join(current_content).strip()
                            current_section = match.group(1)
                            current_content = []
                        else:
                            current_content.append(line)
                    sections[current_section.strip().lower()] = '\n'.join(current_content).strip()
                    
                    desc = ""
                    for k in sections:
                        if 'description' in k or 'morphology' in k:
                            desc = sections[k]
                            break
                    
                    habitat = ""
                    for k in sections:
                        if 'habitat' in k or 'distribution' in k or 'ecology' in k:
                            habitat = sections[k]
                            break
                            
                    desc_html = ""
                    if desc:
                        desc_trunc = desc[:1500] + "..." if len(desc) > 1500 else desc
                        formatted_desc = desc_trunc.replace('\n', '<br>')
                        desc_html += f'<div class="scientific-section"><strong>Morphology & Description:</strong><br>{formatted_desc}</div>'
                    if habitat:
                        habitat_trunc = habitat[:1000] + "..." if len(habitat) > 1000 else habitat
                        formatted_hab = habitat_trunc.replace('\n', '<br>')
                        if desc_html:
                            desc_html += "<br>"
                        desc_html += f'<div class="scientific-section"><strong>Habitat & Distribution:</strong><br>{formatted_hab}</div>'
                        
                    if not desc_html and sections.get('lead'):
                        lead_trunc = sections['lead'][:1000] + "..." if len(sections['lead']) > 1000 else sections['lead']
                        formatted_lead = lead_trunc.replace('\n', '<br>')
                        desc_html = f'<div class="scientific-section"><strong>Summary:</strong><br>{formatted_lead}</div>'
                        
                    res_data['description'] = desc_html
                    res_data['source'] = 'Wikipedia (EN - Scientific)'
        except Exception:
            pass
    else:
        encoded_slug = urllib.parse.quote(species_name.replace(' ', '_'))
        url_wiki_cs = f"https://cs.wikipedia.org/api/rest_v1/page/summary/{encoded_slug}"
        try:
            r_wiki = requests.get(url_wiki_cs, headers=headers, timeout=5)
            if r_wiki.status_code == 200:
                wiki_cs = r_wiki.json()
                if wiki_cs.get('type') != 'disambiguation':
                    res_data['description'] = clean_html(wiki_cs.get('extract_html') or wiki_cs.get('extract', ''))
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
                            if 'square.jpg' in photo_url and photo_obj.get('medium_url') is None:
                                photo_url = photo_url.replace('square.jpg', 'medium.jpg')
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
        if res_data['source'] == 'Nenalezeno':
            res_data['source'] = 'iNaturalist'
        else:
            res_data['source'] += ' + iNaturalist'
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
                        if res_data['source'] == 'Nenalezeno':
                            res_data['source'] = f'Wikipedia ({lang.upper()})'
                        break
            except Exception:
                pass
                
    return res_data

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
    if any(k in col_name.lower() for k in ['photo', 'obrázk', 'obrazk', 'image', 'fotk', 'url', 'pic', 'molekula', 'náhled']):
        return True
    if isinstance(sample_val, str) and (sample_val.startswith('http://') or sample_val.startswith('https://')):
        return True
    return False

# --- STREAMLIT ROZHRANÍ ---

# Načtení databáze států pro zeměpisný modul
countries_db = load_countries_db()

st.set_page_config(
    page_title="Univerzální Anki Generátor",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
    .main-title {
        font-family: 'Outfit', 'Inter', sans-serif;
        color: #1E3A8A;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        color: #4B5563;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⚡ Univerzální Anki Generátor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Nahrajte tabulku, obohaťte ji o data přes API a libovolně namapujte líc a rub kartiček.</div>', unsafe_allow_html=True)

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

# --- NAHRÁNÍ SOUBORU ---
col_file1, col_file2 = st.columns([4, 1])
with col_file1:
    uploaded_file = st.file_uploader("Nahrajte tabulku (Excel .xlsx nebo CSV)", type=["csv", "xlsx"])

reload_clicked = False
with col_file2:
    if uploaded_file is not None:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True) # zarovnání spaceru
        reload_clicked = st.button("🔄 Znovu načíst čistý soubor")

if uploaded_file is not None:
    if st.session_state.df is None or reload_clicked:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
                if len(df.columns) <= 1:
                    df = pd.read_csv(uploaded_file, sep=';')
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
            st.success("Tabulka úspěšně načtena do paměti!")
        except Exception as e:
            st.error(f"Nepodařilo se načíst soubor: {e}")

if st.session_state.df is not None:
    df = st.session_state.df
    columns = list(df.columns)
    
    st.markdown("### 📊 Náhled tabulky v paměti")
    st.dataframe(df.head(5), use_container_width=True)
    st.caption(f"Celkem řádků: **{len(df)}** | Sloupců: **{len(columns)}**")
    
    # --- KROK 2: OBOHACENÍ DATA (API ENHANCERS S TÉMATICKÝM VÝBĚREM) ---
    st.markdown("---")
    
    # Inicializace persistentního konfigurátoru v session_state (aby přežil přepínání záložek)
    if "api_config" not in st.session_state or not st.session_state.api_config:
        st.session_state.api_config = {
            "selected_api_topic": "🌿 Biologie",
            "enable_inat": False,
            "inat_col": columns[0] if columns else "",
            "inat_max": 4,
            "inat_desc": "Vědecký anglický (popis, habitat, listy...)",
            "enable_gbif": False,
            "gbif_col": columns[0] if columns else "",
            "enable_uniprot": False,
            "uniprot_col": columns[0] if columns else "",
            "enable_icd10": False,
            "icd_col": columns[0] if columns else "",
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
            "country_col": columns[0] if columns else "",
            "enable_chem": False,
            "chem_col": columns[0] if columns else "",
            "enable_onthisday": False,
            "otd_col": columns[0] if columns else "",
            "enable_wiki_img": False,
            "wiki_col": columns[0] if columns else "",
            "wiki_max": 3,
            "enable_wiki_gen": False,
            "wiki_gen_col": columns[0] if columns else "",
            "wiki_gen_lang": "Čeština (cs)"
        }

    # Zajištění validních sloupců (pokud by se změnil DataFrame bez kompletního promazání)
    cfg = st.session_state.api_config
    col_keys = ["inat_col", "gbif_col", "uniprot_col", "icd_col", "trans_col", "tts_col", 
                "dict_col", "country_col", "chem_col", "otd_col", "wiki_col", "wiki_gen_col"]
    for col_key in col_keys:
        if col_key not in cfg or cfg[col_key] not in columns:
            cfg[col_key] = columns[0] if columns else ""

    languages = {
        "Angličtina": "en", "Čeština": "cs", "Němčina": "de", 
        "Španělština": "es", "Francouzština": "fr", "Italština": "it", "Ruština": "ru"
    }


    # Horizontální radio jako taby – přežije rerun
    st.markdown("""
    <style>
    div[role="radiogroup"] > label { 
        display: inline-flex; margin-right: 4px;
        padding: 8px 16px; border-radius: 8px 8px 0 0;
        background: rgba(128, 128, 128, 0.15); 
        border: 1px solid rgba(128, 128, 128, 0.3);
        border-bottom: none; cursor: pointer; font-weight: 500;
        color: inherit !important;
    }
    div[role="radiogroup"] > label p {
        color: inherit !important;
        margin: 0 !important;
        font-weight: inherit !important;
    }
    div[role="radiogroup"] > label:hover {
        background: rgba(128, 128, 128, 0.25);
    }
    div[role="radiogroup"] > label:has(input:checked) {
        background: #1D4ED8 !important; 
        border-color: #1D4ED8 !important;
        color: white !important; 
        font-weight: 700;
    }
    div[role="radiogroup"] > label:has(input:checked) p {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

    topics = ["🌿 Biologie", "🩺 Medicína", "🗣️ Jazyky", "🌍 Zeměpis", "🧪 Chemie", "🏛️ Historie", "🔍 Obecné"]
    curr_topic = cfg.get("selected_api_topic", "🌿 Biologie")
    try:
        topic_idx = topics.index(curr_topic)
    except ValueError:
        topic_idx = 0

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

    if selected_topic == "🌿 Biologie":
        st.markdown("#### 🌿 Moduly pro biologii a mikrobiologii")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            cfg["enable_inat"] = st.checkbox(
                "Aktivovat iNaturalist (Botanika & Zoologie)", 
                value=cfg.get("enable_inat", False),
                key="w_enable_inat"
            )
            
            inat_col_val = cfg.get("inat_col", columns[0])
            try:
                inat_col_idx = columns.index(inat_col_val)
            except ValueError:
                inat_col_idx = 0
            cfg["inat_col"] = st.selectbox(
                "Sloupec s latinským názvem druhu", 
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
            
            desc_options = ["Vědecký anglický (popis, habitat, listy...)", "Stručný český (Wikipedie)"]
            inat_desc_val = cfg.get("inat_desc", desc_options[0])
            try:
                inat_desc_idx = desc_options.index(inat_desc_val)
            except ValueError:
                inat_desc_idx = 0
            cfg["inat_desc"] = st.selectbox(
                "Typ popisů", 
                options=desc_options, 
                index=inat_desc_idx,
                key="w_inat_desc"
            )
            
        with col_b2:
            cfg["enable_gbif"] = st.checkbox(
                "Aktivovat GBIF Taxonomii (kmen, třída, čeleď...)", 
                value=cfg.get("enable_gbif", False),
                key="w_enable_gbif"
            )
            
            gbif_col_val = cfg.get("gbif_col", columns[0])
            try:
                gbif_col_idx = columns.index(gbif_col_val)
            except ValueError:
                gbif_col_idx = 0
            cfg["gbif_col"] = st.selectbox(
                "Sloupec s latinským názvem k zařazení", 
                options=columns, 
                index=gbif_col_idx,
                key="w_gbif_col"
            )
            
            cfg["enable_uniprot"] = st.checkbox(
                "Aktivovat UniProt (Funkce proteinů & genů)", 
                value=cfg.get("enable_uniprot", False),
                key="w_enable_uniprot"
            )
            
            uniprot_col_val = cfg.get("uniprot_col", columns[0])
            try:
                uniprot_col_idx = columns.index(uniprot_col_val)
            except ValueError:
                uniprot_col_idx = 0
            cfg["uniprot_col"] = st.selectbox(
                "Sloupec s názvem genu (např. TP53)", 
                options=columns, 
                index=uniprot_col_idx,
                key="w_uniprot_col"
            )

    elif selected_topic == "🩺 Medicína":
        st.markdown("#### 🩺 Moduly pro medicínu a klinické obory")
        cfg["enable_icd10"] = st.checkbox(
            "Aktivovat MKN-10 (Mezinárodní klasifikace nemocí / ICD-10)", 
            value=cfg.get("enable_icd10", False),
            key="w_enable_icd10"
        )
        
        icd_col_val = cfg.get("icd_col", columns[0])
        try:
            icd_col_idx = columns.index(icd_col_val)
        except ValueError:
            icd_col_idx = 0
        cfg["icd_col"] = st.selectbox(
            "Sloupec s názvem diagnózy nebo kódem", 
            options=columns, 
            index=icd_col_idx,
            key="w_icd_col"
        )

    elif selected_topic == "🗣️ Jazyky":
        st.markdown("#### 🗣️ Moduly pro cizí jazyky a slovní zásobu")
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

    elif selected_topic == "🌍 Zeměpis":
        st.markdown("#### 🌍 Moduly pro zeměpis a státy")
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

    elif selected_topic == "🧪 Chemie":
        st.markdown("#### 🧪 Moduly pro chemii")
        cfg["enable_chem"] = st.checkbox(
            "Aktivovat PubChem (molekuly, hmotnost, IUPAC)", 
            value=cfg.get("enable_chem", False),
            key="w_enable_chem"
        )
        
        chem_col_val = cfg.get("chem_col", columns[0])
        try:
            chem_col_idx = columns.index(chem_col_val)
        except ValueError:
            chem_col_idx = 0
        cfg["chem_col"] = st.selectbox(
            "Sloupec s názvem sloučeniny (anglicky)", 
            options=columns, 
            index=chem_col_idx,
            key="w_chem_col"
        )

    elif selected_topic == "🏛️ Historie":
        st.markdown("#### 🏛️ Moduly pro historii a společenské vědy")
        cfg["enable_onthisday"] = st.checkbox(
            "Aktivovat kalendárium 'Tento den v historii'", 
            value=cfg.get("enable_onthisday", False),
            key="w_enable_onthisday"
        )
        
        otd_col_val = cfg.get("otd_col", columns[0])
        try:
            otd_col_idx = columns.index(otd_col_val)
        except ValueError:
            otd_col_idx = 0
        cfg["otd_col"] = st.selectbox(
            "Sloupec s datem (např. 26.6., June 26, 06/26)", 
            options=columns, 
            index=otd_col_idx,
            key="w_otd_col"
        )

    elif selected_topic == "🔍 Obecné":
        st.markdown("#### 🔍 Obecné a encyklopedické vyhledávání")
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            cfg["enable_wiki_img"] = st.checkbox(
                "Aktivovat Wikimedia Commons vyhledávač obrázků", 
                value=cfg.get("enable_wiki_img", False),
                key="w_enable_wiki_img"
            )
            
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
                "Max fotek na řádek", 
                1, 5, 
                value=cfg.get("wiki_max", 3),
                key="w_wiki_max"
            )
            
        with col_g2:
            cfg["enable_wiki_gen"] = st.checkbox(
                "Aktivovat obecné vyhledávání na Wikipedii", 
                value=cfg.get("enable_wiki_gen", False),
                key="w_enable_wiki_gen"
            )
            
            wiki_gen_col_val = cfg.get("wiki_gen_col", columns[0])
            try:
                wiki_gen_col_idx = columns.index(wiki_gen_col_val)
            except ValueError:
                wiki_gen_col_idx = 0
            cfg["wiki_gen_col"] = st.selectbox(
                "Sloupec s tématem pro Wikipedii", 
                options=columns, 
                index=wiki_gen_col_idx,
                key="w_wiki_gen_col"
            )
            
            wiki_gen_lang_options = ["Čeština (cs)", "Angličtina (en)"]
            wiki_gen_lang_val = cfg.get("wiki_gen_lang", wiki_gen_lang_options[0])
            try:
                wiki_gen_lang_idx = wiki_gen_lang_options.index(wiki_gen_lang_val)
            except ValueError:
                wiki_gen_lang_idx = 0
            cfg["wiki_gen_lang"] = st.selectbox(
                "Jazyk Wikipedie pro vyhledání", 
                options=wiki_gen_lang_options, 
                index=wiki_gen_lang_idx,
                key="w_wiki_gen_lang"
            )

    # Přehled aktivních modulů
    active = [k.replace("enable_","") for k in ["enable_inat","enable_gbif","enable_uniprot","enable_icd10",
              "enable_trans","enable_tts","enable_dict","enable_country","enable_chem",
              "enable_onthisday","enable_wiki_img","enable_wiki_gen"] if cfg.get(k, False)]
    if active:
        st.info(f"✅ Aktivní moduly: **{', '.join(active)}**")


    st.markdown("---")
    
    # Spuštění obohacení
    if st.button("⚡ Spustit obohacení dat (API)"):
        # Načíst aktuální hodnoty ze session_state (přežijí přepnutí tabu)
        cfg = st.session_state.api_config
        enable_inat = cfg.get("enable_inat", False)
        enable_gbif = cfg.get("enable_gbif", False)
        enable_uniprot = cfg.get("enable_uniprot", False)
        enable_icd10 = cfg.get("enable_icd10", False)
        enable_trans = cfg.get("enable_trans", False)
        enable_tts = cfg.get("enable_tts", False)
        enable_dict = cfg.get("enable_dict", False)
        enable_wiki_img = cfg.get("enable_wiki_img", False)
        enable_wiki_gen = cfg.get("enable_wiki_gen", False)
        enable_chem = cfg.get("enable_chem", False)
        enable_onthisday = cfg.get("enable_onthisday", False)
        enable_country = cfg.get("enable_country", False)
        trans_src = cfg.get("trans_src", "Angličtina")
        trans_tgt = cfg.get("trans_tgt", "Čeština")
        
        inat_col = cfg.get("inat_col", columns[0] if columns else "")
        inat_max_photos = cfg.get("inat_max", 4)
        inat_desc_type = cfg.get("inat_desc", "Vědecký anglický (popis, habitat, listy...)")
        gbif_col = cfg.get("gbif_col", columns[0] if columns else "")
        uniprot_col = cfg.get("uniprot_col", columns[0] if columns else "")
        icd10_col = cfg.get("icd_col", columns[0] if columns else "")
        trans_col = cfg.get("trans_col", columns[0] if columns else "")
        tts_col = cfg.get("tts_col", columns[0] if columns else "")
        tts_lang = cfg.get("tts_lang", "Angličtina")
        dict_col = cfg.get("dict_col", columns[0] if columns else "")
        chem_col = cfg.get("chem_col", columns[0] if columns else "")
        onthisday_col = cfg.get("otd_col", columns[0] if columns else "")
        wiki_img_col = cfg.get("wiki_col", columns[0] if columns else "")
        wiki_max_photos = cfg.get("wiki_max", 3)
        wiki_gen_col = cfg.get("wiki_gen_col", columns[0] if columns else "")
        wiki_gen_lang = cfg.get("wiki_gen_lang", "Čeština (cs)")
        country_col = cfg.get("country_col", columns[0] if columns else "")


        progress_bar = st.progress(0.0)
        status = st.empty()
        
        new_df = df.copy()
        
        # Vytvoření nových sloupců v DataFrame
        if enable_inat:
            new_df["[iNat] Český název"] = ""
            new_df["[iNat] Popis"] = ""
            new_df["[iNat] Obrázky (URL)"] = ""
        if enable_gbif:
            new_df["[Taxonomie] Říše"] = ""
            new_df["[Taxonomie] Kmen"] = ""
            new_df["[Taxonomie] Třída"] = ""
            new_df["[Taxonomie] Řád"] = ""
            new_df["[Taxonomie] Čeleď"] = ""
            new_df["[Taxonomie] Rod"] = ""
        if enable_uniprot:
            new_df["[UniProt] Protein"] = ""
            new_df["[UniProt] Funkce"] = ""
        if enable_icd10:
            new_df["[MKN-10] Kód"] = ""
            new_df["[MKN-10] Název diagnózy"] = ""
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
        if enable_chem:
            new_df["[Chemie] Molekula (URL)"] = ""
            new_df["[Chemie] Systematický název"] = ""
            new_df["[Chemie] Molekulová hmotnost"] = ""
        if enable_onthisday:
            new_df["[Historie] Události"] = ""
        if enable_wiki_gen:
            new_df["[Wikipedie] Název"] = ""
            new_df["[Wikipedie] Shrnutí"] = ""
            new_df["[Wikipedie] Náhled (URL)"] = ""
        if enable_country:
            new_df["[Zeměpis] Český název"] = ""
            new_df["[Zeměpis] Hlavní město"] = ""
            new_df["[Zeměpis] Region"] = ""
            new_df["[Zeměpis] Jazyky"] = ""
            new_df["[Zeměpis] Měna"] = ""
            new_df["[Zeměpis] Rozloha"] = ""
            new_df["[Zeměpis] Vlajka (URL)"] = ""
            
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
                
                is_sci = (inat_desc_type == "Vědecký anglický (popis, habitat, listy...)")
                inat_data = fetch_inaturalist_data(sp_clean, inat_max_photos, scientific_desc=is_sci)
                
                if inat_data['source'] == 'Nenalezeno':
                    unfound_list.append({'Řádek': idx + 1, 'Položka': raw_sp, 'Modul': 'iNaturalist'})
                
                new_df.at[idx, "[iNat] Český název"] = inat_data['common_name']
                new_df.at[idx, "[iNat] Popis"] = inat_data['description']
                new_df.at[idx, "[iNat] Obrázky (URL)"] = ";".join(inat_data['photo_urls'])
                
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
                
            # 3. UniProt Proteiny
            if enable_uniprot:
                gene = str(row[uniprot_col]).strip()
                uniprot_data = fetch_uniprot_data(gene)
                if uniprot_data['source'] == 'Nenalezeno':
                    unfound_list.append({'Řádek': idx + 1, 'Položka': gene, 'Modul': 'UniProt'})
                new_df.at[idx, "[UniProt] Protein"] = uniprot_data['protein_name']
                new_df.at[idx, "[UniProt] Funkce"] = uniprot_data['function']
                
            # 4. MKN-10 ICD-10
            if enable_icd10:
                med_query = str(row[icd10_col]).strip()
                icd_data = fetch_icd10_data(med_query)
                if icd_data['source'] == 'Nenalezeno':
                    unfound_list.append({'Řádek': idx + 1, 'Položka': med_query, 'Modul': 'MKN-10'})
                new_df.at[idx, "[MKN-10] Kód"] = icd_data['code']
                new_df.at[idx, "[MKN-10] Název diagnózy"] = icd_data['name']
                
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
                
            # 9. PubChem chemický modul
            if enable_chem:
                ch = str(row[chem_col]).strip()
                chem_data = fetch_chemistry_data(ch)
                if not chem_data['iupac']:
                    unfound_list.append({'Řádek': idx + 1, 'Položka': ch, 'Modul': 'PubChem Chemie'})
                new_df.at[idx, "[Chemie] Molekula (URL)"] = chem_data['img_url']
                new_df.at[idx, "[Chemie] Systematický název"] = chem_data['iupac']
                new_df.at[idx, "[Chemie] Molekulová hmotnost"] = chem_data['weight']
                
            # 10. Kalendárium On This Day
            if enable_onthisday:
                dt = str(row[onthisday_col]).strip()
                otd_data = fetch_on_this_day_events(dt)
                if otd_data['source'] == 'Nenalezeno':
                    unfound_list.append({'Řádek': idx + 1, 'Položka': dt, 'Modul': 'Kalendárium'})
                new_df.at[idx, "[Historie] Události"] = otd_data['events']
                
            # 11. Wikipedie obecná
            if enable_wiki_gen:
                cpt = str(row[wiki_gen_col]).strip()
                w_lang = "cs" if "Čeština" in wiki_gen_lang else "en"
                wiki_gen_data = fetch_wikipedia_general(cpt, w_lang)
                if wiki_gen_data['source'] == 'Nenalezeno':
                    unfound_list.append({'Řádek': idx + 1, 'Položka': cpt, 'Modul': f'Wikipedie ({w_lang.upper()})'})
                new_df.at[idx, "[Wikipedie] Název"] = wiki_gen_data['title']
                new_df.at[idx, "[Wikipedie] Shrnutí"] = wiki_gen_data['summary']
                new_df.at[idx, "[Wikipedie] Náhled (URL)"] = wiki_gen_data['img_url']
                
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
        st.success("⚡ Obohocení dat úspěšně dokončeno! Tabulka byla rozšířena o nové sloupce.")
        st.rerun()

    # --- KROK 3: MAPOVÁNÍ KARET (FRONT / BACK DESIGNER) ---
    st.markdown("---")
    st.markdown("### 🎨 Mapování stran a vzhled kartiček")
    
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
        
        st.markdown("##### ↕️ Uspořádání sloupců na líci:")
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
        default_back = [c for c in columns if c not in front_cols]
        back_cols = st.multiselect(
            "Vyberte sloupce, které se zobrazí na RUBU karty:",
            options=columns,
            default=default_back if default_back else columns,
            key="back_cols_multiselect"
        )
        sync_ordered_cols(back_cols, "back_cols_ordered")
        
        st.markdown("##### ↕️ Uspořádání sloupců na rubu:")
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
        st.markdown("#### 🎨 Barevný vzhled")
        card_theme = st.selectbox(
            "Barevný režim karet:",
            [
                "Obojetný (automaticky přepínatelný)",
                "Světlý režim (vždy světlé)",
                "Tmavý režim (vždy tmavé)"
            ],
            index=0
        )
        
    # Stylování sloupců
    all_selected_cols = list(dict.fromkeys(st.session_state.front_cols_ordered + st.session_state.back_cols_ordered))
    if all_selected_cols:
        st.markdown("#### ⚙️ Pokročilé nastavení zobrazení sloupců")
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
        st.markdown("#### 👁️ Vizuální náhled jedné kartičky (první řádek v tabulce)")
        preview_row = df.iloc[0]
        col_pre1, col_pre2 = st.columns(2)
        
        # Výpočet barev pro náhled v Streamlit
        preview_bg = "#F7FAFC"
        preview_fg = "#2D3748"
        preview_border = "#EDF2F7"
        preview_label = "#718096"
        preview_shadow = "rgba(0, 0, 0, 0.05)"
        
        if card_theme == "Tmavý režim (vždy tmavé)":
            preview_bg = "#1A202C"
            preview_fg = "#E2E8F0"
            preview_border = "#4A5568"
            preview_label = "#A0AEC0"
            preview_shadow = "rgba(0, 0, 0, 0.3)"
            
        with col_pre1:
            st.markdown("**LÍC (Front Side):**")
            st.markdown(f'<div style="background-color: {preview_bg}; border: 1px solid {preview_border}; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px {preview_shadow}; color: {preview_fg};">', unsafe_allow_html=True)
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
                label_html = f'<span style="font-size: 10px; font-weight: bold; color: {preview_label}; text-transform: uppercase; border-bottom: 1px solid {preview_border}; display: block; margin-bottom: 4px; padding-bottom: 2px;">{label_text}</span>' if show_label else ''
                
                if is_image_col(c, val):
                    urls = [u.strip() for u in str(val).split(';') if u.strip()]
                    if label_html:
                        st.markdown(label_html, unsafe_allow_html=True)
                    for url in urls:
                        st.markdown(f'<div style="width: 100%; max-width: 450px; border-radius: 8px; overflow: hidden; border: 2px solid {preview_border}; margin: 10px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"><img src="{url}" style="width: 100%; height: auto; max-height: 250px; object-fit: cover; display: block;"></div>', unsafe_allow_html=True)
                elif str(c).startswith("[TTS]"):
                    st.warning(f"🔊 Výslovnost (Audio): {str(val).split(';')[0]}")
                else:
                    if label_html:
                        st.markdown(label_html, unsafe_allow_html=True)
                    val_str = str(val)
                    if not re.search(r'<[a-zA-Z0-9/]+[^>]*>', val_str):
                        val_str = val_str.replace('\n', '<br>')
                    st.markdown(f'<div{val_style_attr}>{val_str}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_pre2:
            st.markdown("**RUB (Back Side):**")
            st.markdown(f'<div style="background-color: {preview_bg}; border: 1px solid {preview_border}; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px {preview_shadow}; color: {preview_fg};">', unsafe_allow_html=True)
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
                label_html = f'<span style="font-size: 10px; font-weight: bold; color: {preview_label}; text-transform: uppercase; border-bottom: 1px solid {preview_border}; display: block; margin-bottom: 4px; padding-bottom: 2px;">{label_text}</span>' if show_label else ''
                
                if is_image_col(c, val):
                    urls = [u.strip() for u in str(val).split(';') if u.strip()]
                    if label_html:
                        st.markdown(label_html, unsafe_allow_html=True)
                    for url in urls:
                        st.markdown(f'<div style="width: 100%; max-width: 450px; border-radius: 8px; overflow: hidden; border: 2px solid {preview_border}; margin: 10px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"><img src="{url}" style="width: 100%; height: auto; max-height: 250px; object-fit: cover; display: block;"></div>', unsafe_allow_html=True)
                elif str(c).startswith("[TTS]"):
                    st.warning(f"🔊 Výslovnost (Audio): {str(val).split(';')[0]}")
                else:
                    if label_html:
                        st.markdown(label_html, unsafe_allow_html=True)
                    val_str = str(val)
                    if not re.search(r'<[a-zA-Z0-9/]+[^>]*>', val_str):
                        val_str = val_str.replace('\n', '<br>')
                    st.markdown(f'<div{val_style_attr}>{val_str}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # --- KROK 4: EXPORT DO ANKI BALÍČKU ---
    st.markdown("---")
    st.markdown("### 📦 Generování Anki Balíčku")
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        deck_name_input = st.text_input("Název balíčku (Anki Deck Name)", value="Hadce_2026")
    with col_exp2:
        subdeck_col_choice = st.selectbox(
            "Rozdělit do podbalíčků podle sloupce (volitelně):",
            ["— Bez rozdělení —"] + columns,
            index=0
        )
    
    if st.button("📦 Generovat Anki balíček (.apkg)"):
        clear_temp_on_finish = True
        if not st.session_state.front_cols_ordered and not st.session_state.back_cols_ordered:
            st.error("Musíte vybrat alespoň jeden sloupec pro Líc nebo Rub kartičky!")
        else:
            temp_dir = tempfile.mkdtemp()
            media_dir = os.path.join(temp_dir, "media")
            os.makedirs(media_dir, exist_ok=True)
            
            progress_bar = st.progress(0.0)
            status = st.empty()
            
            processed_notes = []
            downloaded_media = []
            
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
                            
                        # Obrázkový sloupec
                        if is_image_col(col, val):
                            urls = [u.strip() for u in str(val).split(';') if u.strip()]
                            local_filenames = []
                            
                            for img_idx, url in enumerate(urls):
                                try:
                                    ext = ".jpg"
                                    if ".png" in url.lower():
                                        ext = ".png"
                                    elif ".jpeg" in url.lower():
                                        ext = ".jpeg"
                                        
                                    safe_col = slugify(col)
                                    safe_filename = f"media_{row_idx}_{safe_col}_{img_idx}{ext}"
                                    local_path = os.path.join(media_dir, safe_filename)
                                    
                                    r_img = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
                                    if r_img.status_code == 200:
                                        with open(local_path, 'wb') as f:
                                            f.write(r_img.content)
                                        local_filenames.append(safe_filename)
                                        downloaded_media.append(local_path)
                                except Exception:
                                    pass
                            
                            if local_filenames:
                                img_tags = "".join([
                                    f'<div class="photo-container">'
                                    f'<a href="{fn}" target="_blank"><img src="{fn}"></a>'
                                    f'</div>'
                                    for fn in local_filenames
                                ])
                                html_parts.append(
                                    f'<div class="card-field field-{slugify(col)}">'
                                    f'{label_html}'
                                    f'<div class="photo-list">{img_tags}</div>'
                                    f'</div>'
                                )
                        
                        # Běžný textový sloupec (včetně HTML popisků z Wikipedie/Kalendária)
                        else:
                            val_str = str(val)
                            # Pokud neobsahuje HTML značky, nahradíme konce řádků za <br>
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
                
            status.text("Zapisuji Anki soubor (.apkg)...")
            
            # Sestavení balíčku
            model_id = get_stable_id(deck_name_input + "_model_universal")
            deck_id = get_stable_id(deck_name_input)
            
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
                        'afmt': ANKI_AFMT,
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
                note = genanki.Note(
                    model=anki_model,
                    fields=[
                        note_data['front'],
                        note_data['back']
                    ],
                    guid=genanki.guid_for(note_data['guid_src'])
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
            
            anki_package = genanki.Package(list(decks.values()))
            anki_package.media_files = downloaded_media
            anki_package.write_to_file(apkg_path)
            
            status.text("🎉 Anki balíček byl úspěšně vygenerován!")
            
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
                
            st.success("🎉 Anki balíček byl úspěšně vygenerován!")
            st.rerun()

    # --- ZOBRAZENÍ STAHUJÍCÍCH TLAČÍTEK (VŽDY KDYŽ JSOU K DISPOZICI V STATE) ---
    if st.session_state.generated_apkg_data is not None:
        st.markdown("---")
        st.markdown("### 📥 Stažení výsledků")
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.download_button(
                label="💾 Stáhnout .apkg soubor (Anki Balíček)",
                data=st.session_state.generated_apkg_data,
                file_name=st.session_state.generated_apkg_filename,
                mime="application/octet-stream",
                key="download_apkg_btn"
            )
            st.info(f"Balíček obsahuje **{st.session_state.notes_count}** kartiček a **{st.session_state.media_count}** souborů.")
            
        with col_res2:
            if st.session_state.unfound_csv_data is not None:
                st.warning(f"⚠️ Některé položky nebyly při obohacení nalezeny.")
                st.download_button(
                    label="💾 Stáhnout seznam nenalezených položek (.csv)",
                    data=st.session_state.unfound_csv_data,
                    file_name="nenalezene_polozky.csv",
                    mime="text/csv",
                    key="download_csv_btn"
                )
            else:
                st.success("🎉 Všechny položky byly úspěšně zpracovány!")

