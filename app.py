def register_pdf_fonts():

    import os
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase.pdfmetrics import registerFontFamily

    font_candidates = [
        ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/ariali.ttf"),
        ("C:/Windows/Fonts/calibri.ttf", "C:/Windows/Fonts/calibrib.ttf", "C:/Windows/Fonts/calibrii.ttf"),
        ("C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/segoeuii.ttf"),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf"),
        ("/usr/share/fonts/truetype/freefont/FreeSans.ttf", "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", "/usr/share/fonts/truetype/freefont/FreeSansOblique.ttf"),
    ]
    fn_normal, fn_bold, fn_italic = "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"
    for norm_path, bold_path, ital_path in font_candidates:
        if os.path.exists(norm_path):
            try:
                pdfmetrics.registerFont(TTFont("CustomSans", norm_path))
                fn_normal = "CustomSans"
                if os.path.exists(bold_path):
                    pdfmetrics.registerFont(TTFont("CustomSans-Bold", bold_path))
                    fn_bold = "CustomSans-Bold"
                else:
                    fn_bold = fn_normal
                if os.path.exists(ital_path):
                    pdfmetrics.registerFont(TTFont("CustomSans-Italic", ital_path))
                    fn_italic = "CustomSans-Italic"
                else:
                    fn_italic = fn_normal

                registerFontFamily(
                    "CustomSans",
                    normal="CustomSans",
                    bold=fn_bold,
                    italic=fn_italic,
                    boldItalic=fn_bold
                )
                break
            except Exception:
                pass
    return fn_normal, fn_bold, fn_italic

def generate_citations_pdf():

    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    import io

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
    )
    fn_normal, fn_bold, fn_italic = register_pdf_fonts()
    styles = getSampleStyleSheet()
    styles['Normal'].fontName = fn_normal

    title_style = ParagraphStyle(
        'CitTitle',
        parent=styles['Heading1'],
        fontName=fn_bold,
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1b4332'),
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'CitSubtitle',
        parent=styles['Normal'],
        fontName=fn_italic,
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#555555'),
        spaceAfter=14
    )
    head_style = ParagraphStyle(
        'CitItemHead',
        parent=styles['Heading3'],
        fontName=fn_bold,
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#2d6a4f'),
        spaceBefore=8,
        spaceAfter=3
    )
    body_style = ParagraphStyle(
        'CitItemBody',
        parent=styles['Normal'],
        fontName=fn_normal,
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#222222'),
        spaceAfter=6
    )

    story = [
        Paragraph('Použité databáze, licence a citace zdrojů', title_style),
        Paragraph('Přehled vědeckých a odborných zdrojů využívaných generátorem kartiček a studijních materiálů.', subtitle_style),
        Spacer(1, 4)
    ]

    items = [
        ('1. Pladias.cz – databáze české flóry a vegetace',
         'Chytrý M., Danihelka J., Kaplan Z., Koutecký P., Řezníček J., Danihelka J. et al. (2021) <i>Pladias.cz Database of the Czech Flora and Vegetation</i>. – Preslia 93: 1–87. DOI: 10.23855/preslia.2021.001'),
        ('2. Klíč ke květeně České republiky (Kaplan et al. 2019)',
         'Kaplan Z., Danihelka J., Chrtek J., Kirschner J., Kubát K., Štech M. & Štěpánek J. (eds) (2019) <i>Klíč ke květeně České republiky [Key to the flora of the Czech Republic]</i>. Ed. 2. – Academia, Praha.'),
        ('3. Katalog nepůvodních druhů rostlin České republiky (Pyšek et al. 2022)',
         'Pyšek P., Sádlo J., Chrtek J. Jr., Chytrý M., Kaplan Z., Pergl J., Pokorná A., Axmanová I., Čuda J., Danihelka J., Dřevojan P., Hejda M., Kočár P., Moravcová L., Štajerová K., Vítková M. & Wild J. (2022) <i>Catalogue of alien plants of the Czech Republic (3rd edition)</i>. – Preslia 94: 447–577.'),
        ('4. Výskyt v biotopech České republiky',
         'Chytrý M. & Rafajová M. (2003) <i>Czech National Phytosociological Database</i>. – Ann. Bot. N. S. 3: 345–348.<br/>Sádlo J., Chytrý M. & Pyšek P. (2007) <i>Regional classification of plants according to their habitat preferences</i>. – Preslia 79: 303–342.'),
        ('5. Ellenbergovy indikační hodnoty pro flóru ČR',
         'Chytrý M., Tichý L., Dřevojan P., Sádlo J. & Zelený D. (2018) <i>Ellenberg-type indicator values for the Czech flora</i>. – Preslia 90: 83–103.'),
        ('6. Červené seznamy ohrožených druhů České republiky (AOPK ČR)',
         'Agentura ochrany přírody a krajiny ČR (AOPK ČR): <i>Červené seznamy ohrožených druhů ČR (cévnaté rostliny, houby, mechorosty, lišejníky, bezobratlí, obratlovci)</i>. – Příroda, Praha / portal23.nature.cz.'),
        ('7. Květena České republiky',
         'Hejný S. & Slavík B. (eds) (1988–2010) <i>Květena České republiky [Flora of the Czech Republic]</i>. Vol. 1–8. – Academia, Praha. Dostupné z: ibot.cas.cz'),
        ('8. Mykologie.net',
         'Vavřinec V. a kol. (2026) <i>Mykologická databáze mykologie.net</i>. www.mykologie.net'),
        ('9. DaLiBor – Databáze lišejníků České republiky',
         'Botanický ústav AV ČR & Masarykova univerzita. dalib.cz'),
        ('10. DiatomBase & AlgaeBase',
         'Kociolek J.P. et al. (2026) <i>DiatomBase</i>. diatombase.org | Guiry M.D. & Guiry G.M. (2026) <i>AlgaeBase</i>. algaebase.org'),
        ('11. Otevřená multimédia a licence Creative Commons',
         'Fotografie a zvukové nahrávky z mezinárodních repozitářů <i>iNaturalist</i>, <i>GBIF</i>, <i>Wikimedia Commons</i> a <i>Xeno-canto</i> jsou použity v souladu s licencemi Creative Commons (CC0, CC BY, CC BY-SA, CC BY-NC).')
    ]

    for title, desc in items:
        story.append(Paragraph(title, head_style))
        story.append(Paragraph(desc, body_style))
        story.append(Spacer(1, 2))

    doc.build(story)
    return buffer.getvalue()

import streamlit as st
import streamlit.components.v1 as components

def render_category_select_all_checkbox(cat_id, cat_keys, label="Vybrat vše v této kategorii"):

    all_checked = all(st.session_state.api_config.get(k, False) for k in cat_keys) if cat_keys else False
    chk_key = f"chk_cat_{cat_id}"
    if chk_key not in st.session_state or st.session_state.get(f"_prev_all_{cat_id}") != all_checked:
        st.session_state[chk_key] = all_checked
        st.session_state[f"_prev_all_{cat_id}"] = all_checked

    def _on_toggle():
        new_val = st.session_state[chk_key]
        for k in cat_keys:
            st.session_state.api_config[k] = new_val
            st.session_state[f"w_{k}"] = new_val

    st.checkbox(label, key=chk_key, on_change=_on_toggle)

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

_session = requests.Session()
_adapter = HTTPAdapter(
    pool_connections=50,
    pool_maxsize=100,
    max_retries=Retry(total=2, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
)
_session.mount("https://", _adapter)
_session.mount("http://", _adapter)
requests.get = _session.get
requests.head = _session.head
import functools
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
import concurrent.futures
import gc
import io
import math
import html
import base64
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
import pypdf
from reportlab.lib.pagesizes import A4, A5
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak, KeepTogether, HRFlowable, Flowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def _load_global_config() -> dict:
\
\
\
\
\

    cfg = {}

    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    if os.path.isfile(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                d = json.load(f)
                if d.get("xc_api_key"):
                    cfg["xc_api_key"] = str(d["xc_api_key"]).strip()
        except Exception:
            pass

    if os.environ.get("XC_API_KEY"):
        cfg["xc_api_key"] = str(os.environ["XC_API_KEY"]).strip()

    try:
        if "XC_API_KEY" in st.secrets and st.secrets["XC_API_KEY"]:
            cfg["xc_api_key"] = str(st.secrets["XC_API_KEY"]).strip()
        elif "xc_api_key" in st.secrets and st.secrets["xc_api_key"]:
            cfg["xc_api_key"] = str(st.secrets["xc_api_key"]).strip()
    except Exception:
        pass
    return cfg

GLOBAL_CONFIG = _load_global_config()

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

.photo-caption {
  font-size: 10px;
  padding: 3px 6px;
  text-align: right;
  line-height: 1.25;
  letter-spacing: 0.01em;
  word-break: break-word;
}

.audio-caption {
  font-size: 10px;
  padding: 2px 4px;
  margin-top: 2px;
  line-height: 1.2;
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

    type_ans_css = """
input#typeans {
  font-family: inherit;
  font-size: 1.1em;
  padding: 8px 12px;
  border-radius: 6px;
  border: 1.5px solid #2d6a4f;
  background-color: #ffffff;
  color: #111d14;
  width: 90%;
  max-width: 420px;
  margin: 12px auto;
  display: block;
  box-sizing: border-box;
}
code#typeans {
  font-family: monospace;
  font-size: 1.15em;
  padding: 6px 10px;
  border-radius: 5px;
  background: rgba(0, 0, 0, 0.06);
  color: #111d14;
  display: inline-block;
  margin: 8px auto;
}
.typeGood {
  background-color: #2e7d32 !important;
  color: #ffffff !important;
  padding: 2px 4px;
  border-radius: 3px;
}
.typeBad {
  background-color: #c62828 !important;
  color: #ffffff !important;
  padding: 2px 4px;
  border-radius: 3px;
  text-decoration: line-through;
}
.typeMissed {
  background-color: #546e7a !important;
  color: #ffffff !important;
  padding: 2px 4px;
  border-radius: 3px;
}
"""

    if theme_name == "Světlý režim (vždy světlé)" or theme_name == "Světlý režim":
        color_css = type_ans_css + """
.card {
  color: #1f2937;
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
}
.field-label {
  color: #6b7280;
  border-bottom: 1px solid #e5e7eb;
}
.field-value {
  color: #1f2937;
}
.photo-container {
  border: 1px solid #e5e7eb;
}
.photo-caption {
  color: #6b7280;
  background: rgba(0, 0, 0, 0.035);
  border-top: 1px solid #e5e7eb;
}
.audio-caption {
  color: #6b7280;
}
.no-photo-placeholder {
  border-color: #d1d5db;
  color: #6b7280;
}
.card-divider {
  background: #e5e7eb;
}
"""
    elif theme_name == "Tmavý režim (vždy tmavé)" or theme_name == "Tmavý režim":
        color_css = type_ans_css + """
.card {
  color: #f4f4f5;
  background-color: #2f2f31;
  border: 1px solid #3f3f46;
}
input#typeans {
  background-color: #202124 !important;
  color: #ffffff !important;
  border-color: #52525b !important;
}
code#typeans {
  background: rgba(255, 255, 255, 0.1) !important;
  color: #ffffff !important;
}
.field-label {
  color: #a1a1aa;
  border-bottom: 1px solid #3f3f46;
}
.field-value {
  color: #f4f4f5;
}
.photo-container {
  border: 1px solid #3f3f46;
}
.photo-caption {
  color: #a1a1aa;
  background: rgba(255, 255, 255, 0.05);
  border-top: 1px solid #3f3f46;
}
.audio-caption {
  color: #a1a1aa;
}
.no-photo-placeholder {
  border-color: #3f3f46;
  color: #a1a1aa;
}
.card-divider {
  background: #3f3f46;
}
"""
    else:
        color_css = type_ans_css + """
.card {
  color: #1f2937;
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
}
.field-label {
  color: #6b7280;
  border-bottom: 1px solid #e5e7eb;
}
.field-value {
  color: #1f2937;
}
.photo-container {
  border: 1px solid #e5e7eb;
}
.photo-caption {
  color: #6b7280;
  background: rgba(0, 0, 0, 0.035);
  border-top: 1px solid #e5e7eb;
}
.audio-caption {
  color: #6b7280;
}
.no-photo-placeholder {
  border-color: #d1d5db;
  color: #6b7280;
}
.card-divider {
  background: #e5e7eb;
}

/* Plná podpora standardního tmavého režimu Anki (.night_mode i .nightMode) */
.night_mode.card, .nightMode.card, .night_mode .card, .nightMode .card, body.night_mode .card, body.nightMode .card {
  background-color: #2f2f31 !important;
  color: #f4f4f5 !important;
  border: 1px solid #3f3f46 !important;
}
.night_mode input#typeans, .nightMode input#typeans, body.night_mode input#typeans, body.nightMode input#typeans {
  background-color: #202124 !important;
  color: #ffffff !important;
  border-color: #52525b !important;
}
.night_mode code#typeans, .nightMode code#typeans, body.night_mode code#typeans, body.nightMode code#typeans {
  background: rgba(255, 255, 255, 0.1) !important;
  color: #ffffff !important;
}
.night_mode .field-label, .nightMode .field-label, body.night_mode .field-label, body.nightMode .field-label {
  color: #a1a1aa !important;
  border-color: #3f3f46 !important;
}
.night_mode .field-value, .nightMode .field-value, body.night_mode .field-value, body.nightMode .field-value {
  color: #f4f4f5 !important;
}
.night_mode .photo-container, .nightMode .photo-container, body.night_mode .photo-container, body.nightMode .photo-container {
  border-color: #3f3f46 !important;
}
.night_mode .photo-caption, .nightMode .photo-caption, body.night_mode .photo-caption, body.nightMode .photo-caption {
  color: #a1a1aa !important;
  background: rgba(255, 255, 255, 0.05) !important;
  border-top: 1px solid #3f3f46 !important;
}
.night_mode .audio-caption, .nightMode .audio-caption, body.night_mode .audio-caption, body.nightMode .audio-caption {
  color: #a1a1aa !important;
}
.night_mode .no-photo-placeholder, .nightMode .no-photo-placeholder, body.night_mode .no-photo-placeholder, body.nightMode .no-photo-placeholder {
  border-color: #3f3f46 !important;
  color: #a1a1aa !important;
}
.night_mode .card-divider, .nightMode .card-divider, body.night_mode .card-divider, body.nightMode .card-divider {
  background: #3f3f46 !important;
}

@media (prefers-color-scheme: dark) {
  .card {
    background-color: #2f2f31 !important;
    color: #f4f4f5 !important;
    border: 1px solid #3f3f46 !important;
  }
  input#typeans {
    background-color: #202124 !important;
    color: #ffffff !important;
    border-color: #52525b !important;
  }
  code#typeans {
    background: rgba(255, 255, 255, 0.1) !important;
    color: #ffffff !important;
  }
  .field-label {
    color: #a1a1aa !important;
    border-color: #3f3f46 !important;
  }
  .field-value {
    color: #f4f4f5 !important;
  }
  .photo-container {
    border-color: #3f3f46 !important;
  }
  .photo-caption {
    color: #a1a1aa !important;
    background: rgba(255, 255, 255, 0.05) !important;
    border-top: 1px solid #3f3f46 !important;
  }
  .audio-caption {
    color: #a1a1aa !important;
  }
  .no-photo-placeholder {
    border-color: #3f3f46 !important;
    color: #a1a1aa !important;
  }
  .card-divider {
    background: #3f3f46 !important;
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

def check_image_quality(file_path):
\
\
\

    try:
        import os
        return os.path.exists(file_path) and os.path.getsize(file_path) > 0
    except Exception:
        return False

def save_optimized_image(img_bytes: bytes, target_path: str, max_dim: int = 800, quality: int = 80) -> bool:
\
\
\

    if not img_bytes or len(img_bytes) < 32:
        return False
    try:
        from PIL import Image, ImageOps
        import io
        with Image.open(io.BytesIO(img_bytes)) as img:
            img = ImageOps.exif_transpose(img)
            w, h = img.size
            if w <= 0 or h <= 0:
                return False
            if max_dim and (w > max_dim or h > max_dim):
                img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)

            if target_path.lower().endswith('.png') and img.mode in ('RGBA', 'LA'):
                img.save(target_path, format='PNG', optimize=True)
                return os.path.exists(target_path) and os.path.getsize(target_path) > 0

            img = img.convert('RGB')
            img.save(target_path, format='JPEG', quality=quality, optimize=True)
            return os.path.exists(target_path) and os.path.getsize(target_path) > 0
    except Exception:
        return False

def detect_audio_extension(content: bytes, default_ext: str = ".mp3") -> str:

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

    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '_', value)

def get_stable_id(name):

    return int(hashlib.md5(name.encode('utf-8')).hexdigest()[:8], 16)

def clean_html(text):

    if not text:
        return ""
    text = re.sub(r'</?(?!b|i|u|em|strong|p|br|div|span)[a-zA-Z0-9]+[^>]*>', '', text)
    return text.strip()

def get_value_css(col):

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

    if state_key not in st.session_state:
        st.session_state[state_key] = []
    current_ordered = st.session_state[state_key]

    new_ordered = [c for c in current_ordered if c in selected_cols]

    for c in selected_cols:
        if c not in new_ordered:
            new_ordered.append(c)
    st.session_state[state_key] = new_ordered

def get_smart_column_default(cols, cfg_dict, cfg_key, preferred_keywords, fallback_idx=0):

    if not cols:
        return 0
    val = cfg_dict.get(cfg_key)
    if val and val in cols:
        return cols.index(val)

    for kw in preferred_keywords:
        for idx, c in enumerate(cols):
            if kw.lower() in c.lower():
                return idx

    for idx, c in enumerate(cols):
        c_low = c.lower()
        if not c.startswith("[") and "vědecké jméno" not in c_low and "scientific" not in c_low:
            return idx
    return fallback_idx if fallback_idx < len(cols) else 0

def parse_date(date_str):

    if not date_str or pd.isna(date_str):
        return None, None
    date_str = str(date_str).strip().lower()

    match1 = re.match(r'^(\d{1,2})/(\d{1,2})$', date_str)
    if match1:
        return int(match1.group(1)), int(match1.group(2))

    match2 = re.match(r'^(\d{1,2})\.\s*(\d{1,2})\.?$', date_str)
    if match2:
        return int(match2.group(2)), int(match2.group(1))

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

        month_clean = unicodedata.normalize('NFKD', month_name).encode('ascii', 'ignore').decode('ascii')
        for k, v in cz_months.items():
            k_clean = unicodedata.normalize('NFKD', k).encode('ascii', 'ignore').decode('ascii')
            if month_clean == k_clean:
                return v, day

    en_months = {
        'january': 1, 'jan': 1, 'february': 2, 'feb': 2, 'march': 3, 'mar': 3,
        'april': 4, 'apr': 4, 'may': 5, 'june': 6, 'jun': 6, 'july': 7, 'jul': 7,
        'august': 8, 'aug': 8, 'september': 9, 'sep': 9, 'october': 10, 'oct': 10,
        'november': 11, 'nov': 11, 'december': 12, 'dec': 12
    }

    match4 = re.match(r'^([a-z]+)\s*(\d{1,2})$', date_str)
    if match4:
        month_name = match4.group(1)
        day = int(match4.group(2))
        if month_name in en_months:
            return en_months[month_name], day

    match5 = re.match(r'^(\d{1,2})\s*([a-z]+)$', date_str)
    if match5:
        day = int(match5.group(1))
        month_name = match5.group(2)
        if month_name in en_months:
            return en_months[month_name], day

    return None, None

VALID_CC_CODES = {'cc0', 'cc-by', 'cc-by-nc', 'cc-by-sa', 'cc-by-nc-sa', 'cc-by-nd', 'cc-by-nc-nd', 'public-domain', 'pdm'}

def is_cc_license(license_str: str) -> bool:

    if not license_str:
        return True
    ls = str(license_str).lower()
    if 'all-rights-reserved' in ls or 'all rights reserved' in ls or ('copyright' in ls and 'cc' not in ls):
        return False
    return any(k in ls for k in ["creative", "cc0", "cc_", "cc-", "publicdomain", "pdm", "by", "zero", "open", "gnu"])

def _format_inat_attribution(photo_obj: dict) -> str:

    attr = str(photo_obj.get('attribution') or "").strip()
    lic = str(photo_obj.get('license_code') or "").upper()
    if attr:
        clean_attr = re.sub(r'\(c\)', '©', attr, flags=re.I)
        clean_attr = re.sub(r',?\s*(some|all)\s+rights\s+reserved\s*', ' ', clean_attr, flags=re.I)
        clean_attr = re.sub(r'\s+', ' ', clean_attr).strip()
        if 'inaturalist' not in clean_attr.lower():
            clean_attr = f"{clean_attr} via iNaturalist"
        return clean_attr
    if lic:
        return f"iNaturalist ({lic})"
    return "iNaturalist (CC)"

def extract_gbif_attribution(media_obj: dict, occ_obj: dict = None) -> str:

    lic_raw = str(media_obj.get("license", "")).strip()
    lic_name = "CC BY"
    if "zero" in lic_raw.lower() or "cc0" in lic_raw.lower() or "publicdomain" in lic_raw.lower():
        lic_name = "CC0"
    elif "by-nc-sa" in lic_raw.lower():
        lic_name = "CC BY-NC-SA"
    elif "by-nc-nd" in lic_raw.lower():
        lic_name = "CC BY-NC-ND"
    elif "by-nc" in lic_raw.lower():
        lic_name = "CC BY-NC"
    elif "by-sa" in lic_raw.lower():
        lic_name = "CC BY-SA"
    elif "by-nd" in lic_raw.lower():
        lic_name = "CC BY-ND"
    elif "by" in lic_raw.lower() or "by_4" in lic_raw.lower() or "by_3" in lic_raw.lower():
        lic_name = "CC BY"
    elif lic_raw:
        lic_name = lic_raw.split('/')[-2].upper() if '/' in lic_raw else lic_raw

    author = media_obj.get("rightsHolder") or media_obj.get("creator")
    if not author and occ_obj:
        author = occ_obj.get("recordedBy") or occ_obj.get("institutionCode") or occ_obj.get("datasetName")
    if not author:
        author = "GBIF"
    author = str(author).strip()
    return f"© {author} ({lic_name} via GBIF)"

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
                        lic_code = str(photo_obj.get('license_code', '')).lower()

                        if lic_code and lic_code in VALID_CC_CODES:
                            photo_url = photo_obj.get('medium_url') or photo_obj.get('small_url') or photo_obj.get('url')
                            if photo_url:
                                if 'square' in photo_url:
                                    photo_url = photo_url.replace('square', 'medium')
                                attr_text = _format_inat_attribution(photo_obj)
                                entry = f"{photo_url}|{attr_text}"
                                if not any(p.split('|')[0] == photo_url for p in inat_photos):
                                    inat_photos.append(entry)

                    if len(inat_photos) < max_photos:
                        obs_url = f"https://api.inaturalist.org/v1/observations?taxon_id={taxon_id}&photos=true&license=cc0,cc-by,cc-by-nc,cc-by-sa,cc-by-nc-sa,cc-by-nd,cc-by-nc-nd&per_page=15"
                        r_obs = requests.get(obs_url, timeout=5)
                        if r_obs.status_code == 200:
                            obs_results = r_obs.json().get('results', [])
                            for obs in obs_results:
                                if len(inat_photos) >= max_photos:
                                    break
                                for op in obs.get('photos', []):
                                    op_lic = str(op.get('license_code', '')).lower()
                                    if op_lic and op_lic in VALID_CC_CODES:
                                        op_url = op.get('url')
                                        if op_url:
                                            if 'square' in op_url:
                                                op_url = op_url.replace('square', 'medium')
                                            attr_text = _format_inat_attribution(op)
                                            entry = f"{op_url}|{attr_text}"
                                            if not any(p.split('|')[0] == op_url for p in inat_photos):
                                                inat_photos.append(entry)
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
                        res_data['photo_urls'].append(f"{thumb}|Wikimedia Commons (CC BY-SA)")
                        break
            except Exception:
                pass

    return res_data

@functools.lru_cache(maxsize=4096)
def _cached_wiki_description(species_name: str) -> str:
\
\
\
\

    headers = {'User-Agent': 'AnkiSpeciesGenerator/1.0 (contact: adalb@example.com)'}

    if not species_name or pd.isna(species_name):
        return ""
    species_name = str(species_name).strip()
    if not species_name:
        return ""

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

        if not desc_html:
            lead = sections.get('lead', '')
            if lead:
                t = (lead[:1200] + "…") if len(lead) > 1200 else lead
                desc_html = f'<div class="scientific-section"><strong>Summary:</strong><br>{t.replace(chr(10), "<br>")}</div>'

        return desc_html
    except Exception:
        return ""

def fetch_wiki_description(species_name):
    if not species_name or pd.isna(species_name):
        return ""
    sp = str(species_name).strip()
    if not sp:
        return ""
    return _cached_wiki_description(sp)

def fetch_plant_description(species_name, scientific_desc=True):
    return fetch_wiki_description(species_name)

def gbif_class_to_category(kingdom, phylum, class_):
\
\
\
\

    k = (kingdom or "").strip()
    p = (phylum or "").strip()
    c = (class_ or "").strip()
    cl = c.lower()
    pl = p.lower()

    if not k:
        return ""

    if k == "Animalia":

        if cl in ("aves",):
            return "Ptáci (Aves)"
        if cl in ("mammalia",):
            return "Savci (Mammalia)"
        if cl in ("reptilia",):
            return "Plazi (Reptilia)"
        if cl in ("amphibia",):
            return "Obojživelníci (Amphibia)"
        if cl in ("actinopterygii", "chondrichthyes", "cephalaspidomorphi", "myxini", "sarcopterygii"):
            return "Ryby (Pisces)"

        if cl in ("insecta",):
            return "Hmyz (Insecta)"
        if cl in ("arachnida",):
            return "Pavoukovci (Arachnida)"
        if cl in ("malacostraca", "maxillopoda", "branchiopoda", "ostracoda"):
            return "Korýši (Crustacea)"
        if cl in ("gastropoda", "bivalvia", "cephalopoda", "polyplacophora"):
            return "Měkkýši (Mollusca)"
        if cl in ("polychaeta", "clitellata", "oligochaeta"):
            return "Kroužkovci (Annelida)"
        if cl in ("echinoidea", "asteroidea", "ophiuroidea", "holothuroidea", "crinoidea"):
            return "Ostnokožci (Echinodermata)"
        if pl in ("nematoda",):
            return "Hlístice (Nematoda)"
        if pl in ("platyhelminthes",):
            return "Ploštěnci (Platyhelminthes)"
        return "Živočichové – ostatní"

    if k == "Plantae":

        if pl in ("tracheophyta",) or cl in (
            "magnoliopsida", "liliopsida", "polypodiopsida",
            "pinopsida", "gnetopsida", "cycadopsida", "ginkgoopsida"
        ):
            if cl in ("liliopsida",):
                return "Jednoděložné rostliny (Liliopsida)"
            if cl in ("magnoliopsida",):
                return "Dvouděložné rostliny (Magnoliopsida)"
            if cl in ("polypodiopsida", "marattiopsida", "equisetopsida", "psilotopsida", "ophioglossopsida"):
                return "Kapradiny a přesličky"
            if cl in ("pinopsida", "gnetopsida", "cycadopsida", "ginkgoopsida"):
                return "Nahosemenné rostliny (Gymnospermae)"
            return "Cévnaté rostliny (Tracheophyta)"

        if pl in ("bryophyta",) or cl in ("bryopsida", "polytrichopsida", "tetraphidopsida"):
            return "Mechorosty – mechy (Bryophyta)"
        if pl in ("marchantiophyta",) or cl in ("marchantiopsida", "jungermanniopsida"):
            return "Mechorosty – játrovky (Marchantiophyta)"
        if pl in ("anthocerotophyta",) or cl in ("anthocerotopsida",):
            return "Mechorosty – hlevíky (Anthocerotophyta)"
        return "Rostliny (Plantae)"

    if k == "Fungi":
        if cl in ("agaricomycetes",):
            return "Houby – stopkovýtrusné (Agaricomycetes)"
        if cl in ("pezizomycetes", "sordariomycetes", "leotiomycetes", "dothideomycetes", "eurotiomycetes"):
            return "Houby – vřeckovýtrusné (Ascomycota)"
        if cl in ("tremellomycetes", "dacrymycetes",):
            return "Houby – rosolovité"
        if cl in ("ustilaginomycetes", "pucciniomycetes"):
            return "Houby – rzivky a sněti (Basidiomycota – parazité)"
        if pl in ("ascomycota",):
            return "Houby – vřeckovýtrusné (Ascomycota)"
        if pl in ("basidiomycota",):
            return "Houby – stopkovýtrusné (Basidiomycota)"
        if pl in ("mucoromycota", "zoopagomycota", "chytridiomycota"):
            return "Houby – nižší (Zygomycota / Chytridiomycota)"
        return "Houby (Fungi)"

    if k in ("Chromista", "Protozoa", "Protista"):
        if cl in ("bacillariophyceae", "coscinodiscophyceae", "fragilariophyceae", "mediophyceae"):
            return "Rozsivky (Bacillariophyta)"
        if cl in ("phaeophyceae",):
            return "Řasy – hnědé (Phaeophyceae)"
        if cl in ("chlorophyceae", "trebouxiophyceae", "ulvophyceae", "charophyceae"):
            return "Řasy – zelené (Chlorophyta)"
        if cl in ("rhodophyceae", "florideophyceae"):
            return "Řasy – červené (Rhodophyta)"
        if cl in ("dinophyceae",):
            return "Obrněnky (Dinophyta)"
        if cl in ("cyanophyceae", "synechococcophycideae"):
            return "Sinice (Cyanobacteria)"
        return "Řasy / Chromisté (různé)"

    if k == "Bacteria":
        return "Bakterie (Bacteria)"
    if k == "Archaea":
        return "Archea (Archaea)"
    if k == "Viruses":
        return "Viry"

    return f"Ostatní ({k})"

@functools.lru_cache(maxsize=4096)
def _cached_gbif_taxonomy(species_name: str):
    res = {
        "kingdom": "", "phylum": "", "class": "",
        "order": "", "family": "", "genus": "",
        "source": "Nenalezeno"
    }
    url = f"https://api.gbif.org/v1/species/match?name={urllib.parse.quote(species_name)}&strict=true"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data.get('matchType') not in ['NONE', 'HIGHERRANK'] and data.get('rank') not in ['KINGDOM', 'PHYLUM', 'CLASS']:
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

def fetch_gbif_taxonomy(species_name):
    if not species_name or pd.isna(species_name):
        return {
            "kingdom": "", "phylum": "", "class": "",
            "order": "", "family": "", "genus": "",
            "source": "Nenalezeno"
        }
    sp = str(species_name).strip()
    if not sp:
        return {
            "kingdom": "", "phylum": "", "class": "",
            "order": "", "family": "", "genus": "",
            "source": "Nenalezeno"
        }
    return _cached_gbif_taxonomy(sp).copy()

def slugify_species_name(name):

    if not name or pd.isna(name):
        return "druh"
    name = str(name).strip()
    name = re.sub(r'\s*\(.*\)\s*', '', name).strip()
    name = re.sub(r'\s+sp(p)?\.?$', '', name).strip()
    return slugify(name)

def get_map_font(size=12, bold=False):

    windir = os.environ.get("WINDIR", "C:\\Windows")
    font_names = (
        ["arialbd.ttf", "segoeuib.ttf", "calibrib.ttf", "DejaVuSans-Bold.ttf"]
        if bold else
        ["arial.ttf", "segoeui.ttf", "calibri.ttf", "DejaVuSans.ttf", "tahoma.ttf"]
    )
    for fn in font_names:
        fp = os.path.join(windir, "Fonts", fn)
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size, encoding="unic")
            except Exception:
                pass
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size, encoding="unic")
        except Exception:
            pass
    return ImageFont.load_default()

_PLADIAS_BASE_MAP_CACHE = None

def get_pladias_base_map():

    global _PLADIAS_BASE_MAP_CACHE
    if _PLADIAS_BASE_MAP_CACHE is not None:
        return _PLADIAS_BASE_MAP_CACHE.copy()

    minx, miny, maxx, maxy = 1335000, 6190000, 2105000, 6640000
    w, h = 800, 480
    wms_url = (
        f"https://geoserver.ibot.cas.cz/common/ows?service=WMS&version=1.1.1&request=GetMap"
        f"&LAYERS=commonStyles:squares"
        f"&STYLES=&SRS=EPSG:3857"
        f"&BBOX={minx},{miny},{maxx},{maxy}"
        f"&WIDTH={w}&HEIGHT={h}&FORMAT=image/png"
    )
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        r_wms = requests.get(wms_url, headers=headers, timeout=8)
        if r_wms.status_code == 200 and len(r_wms.content) > 1000:
            base_img = Image.open(io.BytesIO(r_wms.content)).convert("RGBA")
            _PLADIAS_BASE_MAP_CACHE = base_img
            return _PLADIAS_BASE_MAP_CACHE.copy()
    except Exception:
        pass

    blank = Image.new("RGBA", (w, h), (245, 248, 245, 255))
    _PLADIAS_BASE_MAP_CACHE = blank
    return _PLADIAS_BASE_MAP_CACHE.copy()

_TOPO_BASE_MAP_CACHE = {}

def get_topographic_base_map(minx=1335000, miny=6190000, maxx=2105000, maxy=6640000, w=800, h=480, light_layer=True):
\
\
\
\

    cache_key = f"{int(minx)}_{int(miny)}_{int(maxx)}_{int(maxy)}_{w}_{h}_{light_layer}"
    if cache_key in _TOPO_BASE_MAP_CACHE:
        return _TOPO_BASE_MAP_CACHE[cache_key].copy()

    url = (
        f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/export?"
        f"bbox={int(minx)},{int(miny)},{int(maxx)},{int(maxy)}&bboxSR=3857&imageSR=3857&size={w},{h}&format=png&f=image"
    )
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=6)
        if r.status_code == 200 and len(r.content) > 3000:
            img = Image.open(io.BytesIO(r.content)).convert("RGBA")
            if light_layer:

                white_wash = Image.new("RGBA", (w, h), (255, 255, 255, 255))
                img = Image.blend(img, white_wash, 0.16)
            _TOPO_BASE_MAP_CACHE[cache_key] = img
            return img.copy()
    except Exception:
        pass
    return None

PLADIAS_CATEGORY_MAPPING = {
    "Celá rostlina (habitus)": ("[Pladias.cz] Celá rostlina", {1}),
    "Květ / květenství": ("[Pladias.cz] Květ", {2}),
    "Plod / semeno": ("[Pladias.cz] Plod", {3}),
    "List": ("[Pladias.cz] List", {4}),
    "Stonek / lodyha": ("[Pladias.cz] Stonek", {5}),
    "Kmen / borka": ("[Pladias.cz] Kmen", {6}),
    "Herbář / sken (Clo-Pla)": ("[Pladias.cz] Herbář", {None, 7}),
    "Mikrofoto / detail": ("[Pladias.cz] Mikrofoto", {8}),
    "Všechny fotky dohromady (obecný sloupec)": ("[Pladias.cz] Fotky", None)
}

PLADIAS_PARTS_MAPPING = {
    "celek": {1},
    "cela": {1},
    "habitus": {1},
    "kvet": {2},
    "plod": {3},
    "semen": {3},
    "list": {4},
    "stonek": {5},
    "lodyh": {5},
    "kmen": {6},
    "bork": {6},
    "herbar": {None, 7},
    "clopla": {None, 7},
    "sken": {None, 7},
    "mikrofoto": {8},
    "detail": {8},
}

def resolve_target_pladias_successions(parts):
    if not parts:
        return None
    allowed = set()
    for p in parts:
        p_clean = ''.join(c for c in unicodedata.normalize('NFKD', str(p)) if unicodedata.category(c) != 'Mn').lower()
        for k, v in PLADIAS_PARTS_MAPPING.items():
            if k in p_clean:
                allowed.update(v)
    return allowed if allowed else None

def fetch_pladias_species_images(species_name):

    if not species_name or pd.isna(species_name):
        return []
    clean_sp = re.sub(r'\s*\(.*?\)\s*', ' ', str(species_name)).strip()
    clean_sp = re.sub(r'\s+sp(p)?\.?$', '', clean_sp).strip()
    clean_no_subsp = re.sub(r'\s+(subsp|ssp|var|f)\.?\s+.*$', '', clean_sp, flags=re.IGNORECASE).strip()
    if not clean_sp:
        clean_sp = species_name

    builtin_flora_synonyms = {
        "lychnis viscaria": "Viscaria vulgaris",
        "stipa calamagrostis": "Achnatherum calamagrostis",
        "steris viscaria": "Viscaria vulgaris"
    }

    candidates = []
    for s in [clean_sp, clean_no_subsp]:
        if s and s not in candidates:
            candidates.append(s)
        words = s.split()
        if len(words) >= 2:
            binom = f"{words[0]} {words[1]}"
            if binom not in candidates:
                candidates.append(binom)
            if binom.lower() in builtin_flora_synonyms:
                syn = builtin_flora_synonyms[binom.lower()]
                if syn not in candidates:
                    candidates.append(syn)
    if species_name not in candidates:
        candidates.append(species_name)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    for cand in candidates:
        q = urllib.parse.quote(cand)
        url = f"https://api.pladias.cz/prest/images?name_lat=eq.{q}&order=succession.asc.nullslast"
        try:
            r = requests.get(url, headers=headers, timeout=5)
            if r.status_code == 200:
                data = r.json()
                if data and isinstance(data, list) and len(data) > 0:
                    return data
        except Exception:
            pass

    for cand in candidates:
        words = cand.split()
        if len(words) >= 2:
            q_prefix = urllib.parse.quote(f"{words[0]} {words[1]}")
            url_ilike = f"https://api.pladias.cz/prest/images?name_lat=ilike.{q_prefix}*&order=succession.asc.nullslast"
            try:
                r = requests.get(url_ilike, headers=headers, timeout=5)
                if r.status_code == 200:
                    data = r.json()
                    if data and isinstance(data, list) and len(data) > 0:
                        return data
            except Exception:
                pass
    return []

def extract_pladias_category_photos(all_items, target_succ, max_photos=3, fallback=False):

    if not all_items:
        return []
    matched = all_items
    if target_succ is not None:
        filtered = [it for it in all_items if it.get('succession') in target_succ]
        if filtered:
            matched = filtered
        elif not fallback:
            return []
        else:
            matched = all_items

    photos = []
    for it in matched:
        fn = it.get('filename')
        succ = it.get('succession')
        if not fn:
            continue
        if succ is None or succ == 7:
            u = f"https://files.ibot.cas.cz/cevs/images/taxa/clopla/large/{fn}"
        else:
            u = f"https://files.ibot.cas.cz/cevs/images/taxa/large/{fn}"
        if u not in photos:
            photos.append(u)
            if len(photos) >= max_photos:
                break
    return photos

MUSHROOM_COLOR_ATLAS_DATA = {
    "aureoboletus mirabilis": ("aureoboletus_mirabilis", "Aureoboletus mirabilis (Admirable Bolete)"),
    "boletus edulis": ("boletus_edulis_var._edulis", "Boletus edulis (Hřib smrkový / King Bolete)"),
    "boletus rex-veris": ("boletus_rex-veris", "Boletus rex-veris (Spring King)"),
    "neoboletus praestigator": ("neoboletus_praestigator", "Neoboletus praestigator / luridiformis (Hřib kovář)"),
    "neoboletus luridiformis": ("neoboletus_praestigator", "Neoboletus luridiformis (Hřib kovář)"),
    "suillus bovinus": ("suillus_bovinus", "Suillus bovinus (Klouzek kravský)"),
    "suillus granulatus": ("suillus_granulatus", "Suillus granulatus (Klouzek zrnitý)"),
    "tapinella atrotomentosa": ("tapinella_atrotomentosa", "Tapinella atrotomentosa (Čechratka černohuňatá)"),
    "xerocomellus zelleri": ("xerocomellus_zelleri", "Xerocomellus zelleri"),
    "inonotus obliquus": ("inonotus_obliquus", "Inonotus obliquus (Rezavec šikmý / Chaga)"),
    "ramaria": ("ramaria", "Ramaria (Kuřátka)"),
    "polyozellus atrolazulinus": ("polyozellus_atrolazulinus", "Polyozellus atrolazulinus (Modrá liška)"),
    "turbinellus floccosus": ("turbinellus_floccosus", "Turbinellus floccosus"),
    "cortinarius californicus": ("cortinarius_californicus", "Cortinarius californicus"),
    "cortinarius neosanguineus": ("cortinarius_neosanguineus", "Cortinarius neosanguineus"),
    "cortinarius ominosus": ("cortinarius_ominosus", "Cortinarius ominosus"),
    "cortinarius sanguineus": ("cortinarius_sanguineus", "Cortinarius sanguineus (Pavučinec krvavý)"),
    "cortinarius smithii": ("cortinarius_smithii", "Cortinarius smithii"),
    "cortinarius subcroceofolius": ("cortinarius_subcroceofolius", "Cortinarius subcroceofolius"),
    "cortinarius uliginosus": ("cortinarius_uliginosus", "Cortinarius uliginosus (Pavučinec bažinný)"),
    "cortinarius violaceus": ("cortinarius_violaceus", "Cortinarius violaceus (Pavučinec fialový)"),
    "gymnopilus ventricosus": ("gymnopilus_ventricosus", "Gymnopilus ventricosus"),
    "hypholoma fasciculare": ("hypholoma_fasciculare", "Hypholoma fasciculare (Třepenitka svazčitá)"),
    "hypomyces lactifluorum": ("hypomyces_lactifluorum", "Hypomyces lactifluorum (Humří houba)"),
    "omphalotus olivascens": ("omphalotus_olivascens", "Omphalotus olivascens"),
    "boletopsis grisea": ("boletopsis_grisea", "Boletopsis grisea (Kornatec šedý)"),
    "hapalopilus nidulans": ("hapalopilus_nidulans", "Hapalopilus nidulans (Hlinák hnízdovitý)"),
    "phaeolus hispidoides": ("phaeolus_hispidoides", "Phaeolus hispidoides"),
    "phaeolus schweinitzii": ("phaeolus_hispidoides", "Phaeolus schweinitzii (Hnědák Schweinitzův)"),
    "pycnoporellus alboluteus": ("pycnoporellus_alboluteus", "Pycnoporellus alboluteus"),
    "pisolithus arhizus": ("pisolithus_arhizus", "Pisolithus arhizus (Hundsheimka / Řasnatka)"),
    "pisolithus tinctorius": ("pisolithus_arhizus", "Pisolithus tinctorius / arhizus (Řasnatka)"),
    "echinodontium tinctorium": ("echinodontium_tinctorium", "Echinodontium tinctorium"),
    "hydnellum aurantiacum": ("hydnellum_aurantiacum", "Hydnellum aurantiacum (Lošák oranžový)"),
    "hydnellum caeruleum": ("hydnellum_caeruleum", "Hydnellum caeruleum (Lošák modravý)"),
    "hydnellum fuscoindicum": ("hydnellum_fuscoindicum", "Hydnellum fuscoindicum"),
    "hydnellum peckii": ("hydnellum_peckii", "Hydnellum peckii (Lošák Peckův)"),
    "hydnellum regium": ("hydnellum_regium", "Hydnellum regium"),
    "hydnellum stereosarcinon": ("hydnellum_stereosarcinon", "Hydnellum stereosarcinon"),
    "hydnellum suaveolens": ("hydnellum_suaveolens", "Hydnellum suaveolens (Lošák vonný)"),
    "phellodon atratus": ("phellodon_atratus", "Phellodon atratus"),
    "phellodon niger": ("phellodon_niger", "Phellodon niger (Kornatec černý)"),
    "sarcodon squamosus": ("sarcodon_squamosus", "Sarcodon squamosus (Lošák šupinatý)")
}

def fetch_mushroom_color_atlas(species_name):

    if not species_name or pd.isna(species_name):
        return None
    sp_norm = ''.join(c for c in unicodedata.normalize('NFKD', str(species_name)) if unicodedata.category(c) != 'Mn').lower().strip()
    sp_norm = re.sub(r'\s*\(.*?\)\s*', ' ', sp_norm).strip()
    words = sp_norm.split()

    cand = None
    if len(words) >= 2:
        two_words = f"{words[0]} {words[1]}"
        if two_words in MUSHROOM_COLOR_ATLAS_DATA:
            cand = MUSHROOM_COLOR_ATLAS_DATA[two_words]
    if not cand and words and words[0] in MUSHROOM_COLOR_ATLAS_DATA:
        cand = MUSHROOM_COLOR_ATLAS_DATA[words[0]]
    if not cand:
        for k, v in MUSHROOM_COLOR_ATLAS_DATA.items():
            if k in sp_norm:
                cand = v
                break
    if not cand:
        return None

    slug, full_name = cand
    profile_url = f"https://mushroomcoloratlas.com/mushroom/{slug}/"
    return {
        "url": profile_url,
        "name": full_name,
        "slug": slug
    }

def resolve_inat_place_id(place_type_or_name: str) -> str:

    if not place_type_or_name:
        return "8264"
    p_raw = str(place_type_or_name).strip()
    p_lower = p_raw.lower()
    if any(w in p_lower for w in ["svět", "celý", "global", "vše", "all"]):
        return ""
    builtins = {
        "česká republika": "8264", "česko": "8264", "čr": "8264", "czechia": "8264",
        "hlavní město praha": "12800", "praha": "12800",
        "středočeský": "96854", "stredocesky": "96854",
        "jihočeský": "96851", "jihocesky": "96851",
        "plzeňský": "96853", "plzensky": "96853", "plzeň": "96853", "plzen": "96853",
        "karlovarský": "12799", "karlovarsky": "12799", "karlovy vary": "12799",
        "ústecký": "12868", "ustecky": "12868", "ústí nad labem": "12868", "ústí": "12868", "usti": "12868",
        "liberecký": "12802", "liberecky": "12802", "liberec": "12802",
        "královéhradecký": "12801", "kralovehradecky": "12801", "hradec králové": "12801", "hradec": "12801",
        "pardubický": "12805", "pardubicky": "12805", "pardubice": "12805",
        "vysočina": "96852", "vysocina": "96852", "kraj vysočina": "96852", "jihlava": "96852",
        "jihomoravský": "12798", "jihomoravsky": "12798", "brno": "29373",
        "olomoucký": "12804", "olomoucky": "12804", "olomouc": "12804",
        "zlínský": "12869", "zlinsky": "12869", "zlín": "12869", "zlin": "12869",
        "moravskoslezský": "12803", "moravskoslezsky": "12803", "ostrava": "12803",
        "slovensko": "8265", "slovakia": "8265",
        "německo": "7207", "germany": "7207",
        "rakousko": "8056", "austria": "8056",
        "polsko": "8259", "poland": "8259",
        "benešov": "98308", "šumava": "72199", "krkonoše": "72198"
    }
    for k, v in builtins.items():
        if k in p_lower:
            return v

    clean_query = re.sub(r'\b(kraj|okres|město|mesto|oblast|národní park|narodni park|np|republika|region)\b', '', p_lower, flags=re.IGNORECASE).strip()
    if not clean_query:
        clean_query = p_raw

    for query_candidate in [clean_query, p_raw]:
        try:
            url = f"https://api.inaturalist.org/v1/places/autocomplete?q={urllib.parse.quote(query_candidate)}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers, timeout=4)
            if r.status_code == 200:
                res = r.json().get('results', [])
                if res:
                    for item in res:
                        dname = item.get('display_name', '')
                        if 'CZ' in dname or 'Czechia' in dname:
                            return str(item.get('id'))
                    return str(res[0].get('id'))
        except Exception:
            pass
    return "8264"

def get_inat_observation_points(obs_url: str, limit: int = 40):

    if not obs_url or "inaturalist.org" not in obs_url:
        return []
    try:
        parsed = urllib.parse.urlparse(obs_url)
        params = urllib.parse.parse_qs(parsed.query)
        taxon_id = params.get("taxon_id", [""])[0]
        place_id = params.get("place_id", [""])[0]
        if not taxon_id:
            return []
        api_url = f"https://api.inaturalist.org/v1/observations?taxon_id={taxon_id}&per_page={limit}"
        if place_id:
            api_url += f"&place_id={place_id}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        r = requests.get(api_url, headers=headers, timeout=5)
        if r.status_code == 200:
            data = r.json()
            pts = []
            for item in data.get('results', []):
                loc = item.get('location')
                if loc:
                    p = [float(x) for x in loc.split(',')]
                    pts.append({"lat": p[0], "lon": p[1], "latitude": p[0], "longitude": p[1]})

            return pts
    except Exception:
        pass
    return []

def fetch_inaturalist_map_url(species_name, place_id="8264"):

    if not species_name or pd.isna(species_name):
        return ""
    clean_sp = re.sub(r'\s*\(.*?\)\s*', ' ', str(species_name)).strip()
    clean_sp = re.sub(r'\s+sp(p)?\.?$', '', clean_sp).strip()
    if not clean_sp:
        return ""
    try:
        url = f"https://api.inaturalist.org/v1/taxa?q={urllib.parse.quote(clean_sp)}&rank=species"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            results = r.json().get('results', [])
            if results:
                t_id = results[0].get('id')
                if t_id:
                    if place_id:
                        return f"https://www.inaturalist.org/observations?taxon_id={t_id}&place_id={place_id}"
                    else:
                        return f"https://www.inaturalist.org/observations?taxon_id={t_id}"
    except Exception:
        pass
    return ""

def fetch_pladias_photos(species_name, max_photos=3, parts=None, fallback=True):
\
\
\
\

    photos = []
    if not species_name or pd.isna(species_name):
        return photos
    species_name = str(species_name).strip()
    if not species_name:
        return photos

    clean_sp = re.sub(r'\s*\(.*?\)\s*', ' ', species_name).strip()
    clean_sp = re.sub(r'\s+sp(p)?\.?$', '', clean_sp).strip()
    if not clean_sp:
        clean_sp = species_name

    target_succ = resolve_target_pladias_successions(parts)

    candidates = [clean_sp]
    words = clean_sp.split()
    if len(words) >= 3 and not any(w in ['subsp.', 'ssp.', 'var.', 'f.', 'sect.', 'agg.'] for w in words):
        candidates.append(f"{words[0]} {words[1]}")
    if species_name not in candidates:
        candidates.append(species_name)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    items = []

    for cand in candidates:
        q = urllib.parse.quote(cand)
        url = f"https://api.pladias.cz/prest/images?name_lat=eq.{q}&order=succession.asc.nullslast"
        try:
            r = requests.get(url, headers=headers, timeout=5)
            if r.status_code == 200:
                data = r.json()
                if data and isinstance(data, list):
                    items = data
                    break
        except Exception:
            pass

    if not items and len(words) >= 2:
        q_prefix = urllib.parse.quote(f"{words[0]} {words[1]}")
        url_ilike = f"https://api.pladias.cz/prest/images?name_lat=ilike.{q_prefix}*&order=succession.asc.nullslast"
        try:
            r = requests.get(url_ilike, headers=headers, timeout=5)
            if r.status_code == 200:
                data = r.json()
                if data and isinstance(data, list):
                    items = data
        except Exception:
            pass

    if items:
        matched_items = items
        if target_succ is not None:
            filtered = [it for it in items if it.get('succession') in target_succ]
            if filtered:
                matched_items = filtered
            elif not fallback:
                return []
            else:
                matched_items = items

        for it in matched_items:
            fn = it.get('filename')
            succ = it.get('succession')
            if not fn:
                continue
            if succ is None or succ == 7:
                u = f"https://files.ibot.cas.cz/cevs/images/taxa/clopla/large/{fn}"
            else:
                u = f"https://files.ibot.cas.cz/cevs/images/taxa/large/{fn}"
            if u not in photos:
                photos.append(u)
                if len(photos) >= max_photos:
                    break
        if photos:
            return photos[:max_photos]
        elif not fallback:
            return []

    for q_name in [clean_sp, species_name]:
        url_pics = f"https://pladias.cz/taxon/pictures/{urllib.parse.quote(q_name)}"
        try:
            r = requests.get(url_pics, headers=headers, timeout=6)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                for a in soup.find_all('a', class_='pictureLink'):
                    href = a.get('href', '')
                    if 'cevs/images/taxa/' in href:
                        large_url = href.replace('/thumbs/', '/large/')
                        if large_url not in photos:
                            photos.append(large_url)
                            if len(photos) >= max_photos:
                                break

                if len(photos) < max_photos:
                    for img in soup.find_all('img'):
                        src = img.get('src', '')
                        if 'cevs/images/taxa/' in src:
                            large_url = src.replace('/thumbs/', '/large/')
                            if large_url not in photos:
                                photos.append(large_url)
                                if len(photos) >= max_photos:
                                    break
            if photos:
                break
        except Exception:
            pass

    return photos[:max_photos]

def render_pladias_distribution_map(species_name, output_path):
\
\
\

    if not species_name:
        return False
    species_name = str(species_name).strip()
    clean_sp = re.sub(r'\s*\(.*?\)\s*', ' ', species_name).strip()
    clean_sp = re.sub(r'\s+sp(p)?\.?$', '', clean_sp).strip()
    if not clean_sp:
        clean_sp = species_name

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    taxon_id = None
    for q_name in [clean_sp, species_name]:
        url_dist = f"https://pladias.cz/taxon/distribution/{urllib.parse.quote(q_name)}"
        try:
            r = requests.get(url_dist, headers=headers, timeout=6)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                map_div = soup.find('div', id='map') or soup.find('div', class_='distributionMap')
                if map_div and map_div.get('data-taxon-id'):
                    taxon_id = map_div.get('data-taxon-id')
                    break
        except Exception:
            pass

    if not taxon_id:
        return False

    minx, miny, maxx, maxy = 1335000, 6190000, 2105000, 6640000
    w, h = 800, 480
    base_img = get_pladias_base_map()
    topo_img = get_topographic_base_map(minx, miny, maxx, maxy, w=w, h=h, light_layer=True)

    canvas = Image.new("RGBA", (w, h + 46), (248, 250, 248, 255))
    if topo_img:
        canvas.paste(topo_img, (0, 0))
        canvas.paste(base_img, (0, 0), base_img)
    else:
        canvas.paste(base_img, (0, 0), base_img)

    def lon_lat_to_pixel(lon, lat):
        x_m = lon * 20037508.34 / 180.0
        y_m = math.log(math.tan((90.0 + lat) * math.pi / 360.0)) / (math.pi / 180.0)
        y_m = y_m * 20037508.34 / 180.0
        px = int((x_m - minx) / (maxx - minx) * w)
        py = int((maxy - y_m) / (maxy - miny) * h)
        return px, py

    draw = ImageDraw.Draw(canvas)

    url_neurceny = f"https://geoserver.ibot.cas.cz/pladias_wfs/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=neurceny&outputFormat=application/json&VIEWPARAMS=TAXON_ID:{taxon_id}"
    try:
        r_n = requests.get(url_neurceny, headers=headers, timeout=6)
        if r_n.status_code == 200:
            for f in r_n.json().get('features', []):
                coords = f.get('geometry', {}).get('coordinates')
                if coords and len(coords) == 2:
                    px, py = lon_lat_to_pixel(coords[0], coords[1])
                    r_dot = 3
                    draw.ellipse([px - r_dot, py - r_dot, px + r_dot, py + r_dot], fill=(160, 160, 160, 220), outline=(120, 120, 120, 255))
    except Exception:
        pass

    url_jisty = f"https://geoserver.ibot.cas.cz/pladias_wfs/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=jisty&outputFormat=application/json&VIEWPARAMS=TAXON_ID:{taxon_id}"
    try:
        r_j = requests.get(url_jisty, headers=headers, timeout=6)
        if r_j.status_code == 200:
            for f in r_j.json().get('features', []):
                coords = f.get('geometry', {}).get('coordinates')
                if coords and len(coords) == 2:
                    px, py = lon_lat_to_pixel(coords[0], coords[1])
                    r_dot = 3.5
                    draw.ellipse([px - r_dot, py - r_dot, px + r_dot, py + r_dot], fill=(20, 110, 50, 240), outline=(10, 60, 25, 255))
    except Exception:
        pass

    font_regular = get_map_font(12, bold=False)
    draw.rectangle([0, h, w, h + 46], fill=(238, 242, 239, 255), outline=(210, 220, 215, 255))

    draw.ellipse([18, h + 15, 26, h + 23], fill=(20, 110, 50, 240), outline=(10, 60, 25, 255))
    draw.text((32, h + 13), "Ověřený výskyt", font=font_regular, fill=(30, 40, 35, 255))

    draw.ellipse([140, h + 15, 148, h + 23], fill=(160, 160, 160, 220), outline=(120, 120, 120, 255))
    draw.text((154, h + 13), "Nerevidovaný údaj", font=font_regular, fill=(60, 70, 65, 255))

    attribution = "Zdroj dat: Pladias.cz"
    try:
        attr_bbox = font_regular.getbbox(attribution)
        attr_w = attr_bbox[2] - attr_bbox[0]
    except Exception:
        attr_w = 140
    draw.text((w - attr_w - 18, h + 13), attribution, font=font_regular, fill=(70, 90, 80, 255))

    final_img = canvas.convert("RGB")
    final_img.save(output_path, format="JPEG", quality=85, optimize=True)
    return os.path.exists(output_path) and os.path.getsize(output_path) > 0

@functools.lru_cache(maxsize=4096)
def _cached_pladias_taxonomy(sp_clean: str):
\
\
\

    res = {
        "phylum": "", "class": "", "order": "",
        "family": "", "genus": "", "czech_name": "", "source": "Nenalezeno"
    }
    if not sp_clean or pd.isna(sp_clean):
        return res
    raw = str(sp_clean).strip()
    raw = re.sub(r'\s*\(.*?\)\s*', ' ', raw).strip()
    raw = re.sub(r'\s+sp(p)?\.?$', '', raw).strip()
    if not raw:
        return res

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    words = raw.split()

    candidates = []
    if len(words) >= 2:
        binom = f"{words[0].capitalize()} {words[1].lower()}"
        candidates.append(binom)
        rest = " ".join(words[1:])
        candidates.append(f"{words[0].capitalize()} {rest}")
        if len(words) >= 3 and words[2].lower() in ['agg.', 'agg', 'sect.', 'subsp.', 'ssp.', 'var.']:
            candidates.append(f"{words[0].capitalize()} {words[1].lower()} {words[2]}")
    elif len(words) == 1:
        candidates.append(words[0].capitalize())

    if raw not in candidates:
        candidates.append(raw)

    soup = None
    for cand in candidates:
        url = f"https://pladias.cz/taxon/overview/{urllib.parse.quote(cand)}"
        try:
            r = requests.get(url, headers=headers, timeout=6)
            if r.status_code == 200 and '/taxon/overview/' in r.url:
                s_cand = BeautifulSoup(r.text, 'html.parser')
                if s_cand.find('ol', class_='breadcrumb'):
                    soup = s_cand
                    break
        except Exception:
            pass

    if not soup:
        genus_cand = words[0].capitalize() if words else ""
        if genus_cand and len(genus_cand) >= 3:
            try:
                r_gen = requests.get(f"https://pladias.cz/taxon/overview/{urllib.parse.quote(genus_cand)}", headers=headers, timeout=6)
                if r_gen.status_code == 200 and '/taxon/overview/' in r_gen.url:
                    s_gen = BeautifulSoup(r_gen.text, 'html.parser')
                    if s_gen.find('ol', class_='breadcrumb'):
                        soup = s_gen
            except Exception:
                pass

    if soup:
        bc = soup.find('ol', class_='breadcrumb')
        if bc:
            items = [li.get_text(strip=True) for li in bc.find_all('li')]
            nav_words = {'druhy', 'přehled', 'taxony', 'hledání'}
            clean_items = [it for it in items if it.lower() not in nav_words]
            if clean_items:
                res["source"] = "Pladias.cz"
                for rk in clean_items:
                    if rk.endswith('phyta'): res["phylum"] = rk
                    elif rk.endswith('opsida'): res["class"] = rk
                    elif rk.endswith('ales'): res["order"] = rk
                    elif rk.endswith('aceae'): res["family"] = rk

                last_it = clean_items[-1]
                res["genus"] = last_it.split()[0]

                if not res["phylum"] and (res["class"] or res["order"] or res["family"]):
                    res["phylum"] = "Tracheophyta"

        for h1_cand in soup.find_all('h1'):
            t_h1 = h1_cand.get_text(strip=True)
            if '\u2013' in t_h1 or '–' in t_h1 or '-' in t_h1:
                parts = re.split(r'\s*[\u2013\u2014\-]\s*', t_h1, maxsplit=1)
                if len(parts) > 1 and parts[1].strip() and 'pladias' not in parts[1].lower():
                    res["czech_name"] = parts[1].strip()
                    break
        if not res["czech_name"] and soup.title:
            t_title = soup.title.get_text(strip=True)
            title_parts = re.split(r'\s*[\u2013\u2014\-]\s*', t_title)
            if len(title_parts) >= 2 and title_parts[1].strip() and 'pladias' not in title_parts[1].lower():
                res["czech_name"] = title_parts[1].strip()

    return res

def fetch_pladias_taxonomy(species_name):
    if not species_name or pd.isna(species_name):
        return {
            "phylum": "", "class": "", "order": "",
            "family": "", "genus": "", "czech_name": "", "source": "Nenalezeno"
        }
    sp_clean = re.sub(r'\s*\(.*?\)\s*', ' ', str(species_name)).strip()
    sp_clean = re.sub(r'\s+sp(p)?\.?$', '', sp_clean).strip()
    if not sp_clean:
        return {
            "phylum": "", "class": "", "order": "",
            "family": "", "genus": "", "czech_name": "", "source": "Nenalezeno"
        }
    return _cached_pladias_taxonomy(sp_clean).copy()

CZ_REGION_BBOXES_3857 = {
    "12800": (1595000, 6440000, 1635000, 6480000, "Praha"),
    "96854": (1510000, 6380000, 1715000, 6530000, "Středočeský kraj"),
    "96851": (1530000, 6210000, 1720000, 6370000, "Jihočeský kraj"),
    "96853": (1400000, 6290000, 1550000, 6470000, "Plzeňský kraj"),
    "12799": (1340000, 6440000, 1475000, 6540000, "Karlovarský kraj"),
    "12868": (1440000, 6500000, 1620000, 6630000, "Ústecký kraj"),
    "12802": (1600000, 6540000, 1720000, 6635000, "Liberecký kraj"),
    "12801": (1690000, 6460000, 1830000, 6580000, "Královéhradecký kraj"),
    "12805": (1710000, 6380000, 1870000, 6485000, "Pardubický kraj"),
    "96852": (1670000, 6270000, 1810000, 6420000, "Kraj Vysočina"),
    "12798": (1760000, 6220000, 1950000, 6370000, "Jihomoravský kraj"),
    "12804": (1850000, 6350000, 1980000, 6500000, "Olomoucký kraj"),
    "12869": (1920000, 6270000, 2030000, 6385000, "Zlínský kraj"),
    "12803": (1910000, 6360000, 2080000, 6520000, "Moravskoslezský kraj"),
    "72199": (1460000, 6240000, 1565000, 6350000, "Šumava"),
    "72198": (1710000, 6550000, 1775000, 6605000, "Krkonoše"),
}

def render_inat_observation_map(obs_url, output_path, species_name=""):
\
\
\
\
\

    w, h = 800, 480
    minx, miny, maxx, maxy = 1335000, 6190000, 2105000, 6640000

    parsed = urllib.parse.urlparse(obs_url)
    params = urllib.parse.parse_qs(parsed.query)
    p_id = params.get("place_id", [""])[0]

    pts = get_inat_observation_points(obs_url, limit=60)

    def lon_lat_to_merc(lon, lat):
        x_m = lon * 20037508.34 / 180.0
        y_m = math.log(math.tan((90.0 + lat) * math.pi / 360.0)) / (math.pi / 180.0) * 20037508.34 / 180.0
        return x_m, y_m

    place_name = ""
    is_cropped = False
    crop_minx, crop_miny, crop_maxx, crop_maxy = minx, miny, maxx, maxy

    if p_id in CZ_REGION_BBOXES_3857:
        is_cropped = True
        r_minx, r_miny, r_maxx, r_maxy, place_name = CZ_REGION_BBOXES_3857[p_id]
        box_w = r_maxx - r_minx
        box_h = r_maxy - r_miny
        target_ratio = 800.0 / 480.0
        if box_w / box_h > target_ratio:
            diff_h = int(box_w / target_ratio) - box_h
            crop_miny = r_miny - diff_h // 2
            crop_maxy = r_maxy + diff_h // 2
            crop_minx = r_minx
            crop_maxx = r_maxx
        else:
            diff_w = int(box_h * target_ratio) - box_w
            crop_minx = r_minx - diff_w // 2
            crop_maxx = r_maxx + diff_w // 2
            crop_miny = r_miny
            crop_maxy = r_maxy
    else:

        merc_pts = [lon_lat_to_merc(p["lon"], p["lat"]) for p in pts if p.get("lon") and p.get("lat")]
        valid_pts = [(x, y) for x, y in merc_pts if minx <= x <= maxx and miny <= y <= maxy]
        if valid_pts:
            px_min = min(p[0] for p in valid_pts)
            px_max = max(p[0] for p in valid_pts)
            py_min = min(p[1] for p in valid_pts)
            py_max = max(p[1] for p in valid_pts)
            span_w = px_max - px_min
            span_h = py_max - py_min
            if span_w < 600000 or span_h < 350000:
                is_cropped = True
                pad_x = max(int(span_w * 0.4), 40000)
                pad_y = max(int(span_h * 0.4), 30000)
                b_w = max(span_w + 2 * pad_x, 160000)
                b_h = max(span_h + 2 * pad_y, 96000)
                target_ratio = 800.0 / 480.0
                if b_w / b_h > target_ratio:
                    b_h = int(b_w / target_ratio)
                else:
                    b_w = int(b_h * target_ratio)
                cx = (px_min + px_max) / 2
                cy = (py_min + py_max) / 2
                crop_minx = max(minx, cx - b_w / 2)
                crop_maxx = min(maxx, cx + b_w / 2)
                crop_miny = max(miny, cy - b_h / 2)
                crop_maxy = min(maxy, cy + b_h / 2)

    topo_img = get_topographic_base_map(crop_minx, crop_miny, crop_maxx, crop_maxy, w=w, h=h, light_layer=True)
    if not topo_img:

        base_grid = get_pladias_base_map()
        if is_cropped:

            gx1 = int((crop_minx - minx) / (maxx - minx) * w)
            gx2 = int((crop_maxx - minx) / (maxx - minx) * w)
            gy1 = int((maxy - crop_maxy) / (maxy - miny) * h)
            gy2 = int((maxy - crop_miny) / (maxy - miny) * h)
            gx1 = max(0, min(w - 10, gx1))
            gx2 = max(gx1 + 10, min(w, gx2))
            gy1 = max(0, min(h - 10, gy1))
            gy2 = max(gy1 + 10, min(h, gy2))
            topo_img = base_grid.crop((gx1, gy1, gx2, gy2)).resize((w, h), Image.Resampling.LANCZOS)
        else:
            topo_img = base_grid.copy()

    canvas = Image.new("RGBA", (w, h + 46), (248, 250, 248, 255))
    canvas.paste(topo_img, (0, 0))
    draw = ImageDraw.Draw(canvas)

    drawn_count = 0
    for p in pts:
        lat = p.get("lat")
        lon = p.get("lon")
        if lat and lon:
            x_m, y_m = lon_lat_to_merc(lon, lat)
            c_px = int((x_m - crop_minx) / (crop_maxx - crop_minx) * w)
            c_py = int((crop_maxy - y_m) / (crop_maxy - crop_miny) * h)
            if 0 <= c_px <= w and 0 <= c_py <= h:
                r_dot = 7 if is_cropped else 4
                draw.ellipse([c_px - r_dot - 1, c_py - r_dot - 1, c_px + r_dot + 1, c_py + r_dot + 1], fill=(255, 255, 255, 230))
                draw.ellipse([c_px - r_dot, c_py - r_dot, c_px + r_dot, c_py + r_dot], fill=(230, 75, 20, 245), outline=(160, 35, 10, 255), width=2 if is_cropped else 1)
                drawn_count += 1

    font_regular = get_map_font(12, bold=False)
    font_bold = get_map_font(12, bold=True)

    draw.rectangle([0, h, w, h + 46], fill=(238, 242, 239, 255), outline=(210, 220, 215, 255))
    draw.ellipse([18, h + 15, 26, h + 23], fill=(225, 80, 25, 240), outline=(170, 40, 10, 255))

    lbl = f" - {place_name}" if place_name else ""
    if is_cropped:
        if drawn_count > 0:
            count_str = f"Pozorování iNaturalist{lbl} ({drawn_count} nálezů)"
        else:
            count_str = f"Pozorování iNaturalist{lbl} (0 nálezů v území)"
    else:
        count_str = f"Pozorování iNaturalist ({drawn_count} nálezů v ČR)" if drawn_count > 0 else f"Pozorování iNaturalist ({len(pts)} nálezů)"

    draw.text((32, h + 13), count_str, font=font_regular, fill=(25, 35, 30, 255))

    attribution = "Zdroj: iNaturalist.org"
    try:
        attr_bbox = font_regular.getbbox(attribution)
        attr_w = attr_bbox[2] - attr_bbox[0]
    except Exception:
        attr_w = 140
    attr_x = w - attr_w - 18
    draw.text((attr_x, h + 13), attribution, font=font_regular, fill=(75, 95, 85, 255))

    try:
        left_bbox = font_regular.getbbox(count_str)
        left_end_x = 32 + (left_bbox[2] - left_bbox[0])
    except Exception:
        left_end_x = 32 + len(count_str) * 8

    sp_title = species_name.strip() if species_name else ""
    if sp_title:
        try:
            sp_bbox = font_bold.getbbox(sp_title)
            sp_w = sp_bbox[2] - sp_bbox[0]
        except Exception:
            sp_w = len(sp_title) * 8
        avail_w = attr_x - left_end_x - 30
        if avail_w >= sp_w + 16:
            mid_x = (left_end_x + attr_x - sp_w) // 2
            sp_x = max(left_end_x + 20, mid_x)
            if sp_x + sp_w <= attr_x - 10:
                draw.text((sp_x, h + 13), sp_title, font=font_bold, fill=(40, 65, 50, 255))

    final_img = canvas.convert("RGB")
    final_img.save(output_path, format="JPEG", quality=88, optimize=True)
    return os.path.exists(output_path) and os.path.getsize(output_path) > 0

def get_or_render_inat_map_image(species_name, obs_url):
\
\
\

    if not obs_url:
        return ""
    clean_sp = slugify_species_name(species_name) if species_name else "inat_obs"
    url_hash = hashlib.md5(str(obs_url).encode('utf-8')).hexdigest()[:8]
    cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_media")
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, f"{clean_sp}_inat_map_{url_hash}.jpg")
    if os.path.exists(cache_path) and os.path.getsize(cache_path) > 1000:
        return cache_path
    ok = render_inat_observation_map(obs_url, cache_path, species_name=species_name)
    if ok and os.path.exists(cache_path):
        return cache_path
    return ""

def get_or_render_pladias_map_image(species_name):
\
\

    if not species_name or pd.isna(species_name):
        return ""
    clean_sp = slugify_species_name(species_name)
    cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_media")
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, f"{clean_sp}_pladias_map_v2.jpg")
    if os.path.exists(cache_path) and os.path.getsize(cache_path) > 1000:
        return cache_path
    ok = render_pladias_distribution_map(species_name, cache_path)
    if ok and os.path.exists(cache_path):
        return cache_path
    return ""

def resolve_local_media_path(raw_path: str) -> str:

    if not raw_path:
        return ""
    clean = str(raw_path).strip()
    if clean.startswith("file:///"):
        clean = urllib.parse.unquote(clean[8:])
    elif clean.startswith("file://"):
        clean = urllib.parse.unquote(clean[7:])
    candidates = [
        clean,
        os.path.join(os.path.dirname(os.path.abspath(__file__)), clean),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom_media", os.path.basename(clean)),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_media", os.path.basename(clean)),
        os.path.join("custom_media", os.path.basename(clean)),
        os.path.join("test_media", os.path.basename(clean)),
    ]
    for c in candidates:
        if os.path.isfile(c):
            return os.path.abspath(c)
    return ""

def download_media_file(url: str, local_path: str) -> bool:

    if not url or not local_path:
        return False
    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        return True
    try:
        os.makedirs(os.path.dirname(os.path.abspath(local_path)), exist_ok=True)
    except Exception:
        pass
    url_str = str(url).strip()

    if "pladias.cz" in url_str and "distribution" in url_str:
        try:
            sp_m = url_str.split("distribution/")[-1].split("?")[0].strip().replace("%20", " ")
            if render_pladias_distribution_map(sp_m, local_path):
                return True
        except Exception:
            pass

    if "inaturalist.org" in url_str and "observations" in url_str:
        try:
            if render_inat_observation_map(url_str, local_path):
                return True
        except Exception:
            pass

    local_src = resolve_local_media_path(url_str)
    if local_src and os.path.isfile(local_src):
        try:
            shutil.copy2(local_src, local_path)
            if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
                return True
        except Exception:
            pass

    if url_str.startswith("data:image"):
        try:
            head, b64_data = url_str.split(",", 1)
            raw_bytes = base64.b64decode(b64_data)
            with open(local_path, "wb") as f_out:
                f_out.write(raw_bytes)
            return True
        except Exception:
            pass

    if url_str.startswith("http://") or url_str.startswith("https://"):
        try:
            r = requests.get(
                url_str,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                timeout=(3.0, 7.0)
            )
            if r.status_code == 404 and 'cevs/images/taxa/' in url_str:
                alt_url = url_str.replace('/taxa/large/', '/taxa/clopla/large/') if '/taxa/clopla/' not in url_str else url_str.replace('/taxa/clopla/large/', '/taxa/large/')
                try:
                    alt_resp = requests.get(alt_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}, timeout=(3.0, 7.0))
                    if alt_resp.status_code == 200:
                        r = alt_resp
                except Exception:
                    pass
            if r.status_code == 200 and len(r.content) > 0:
                if not save_optimized_image(r.content, local_path, max_dim=900, quality=82):
                    with open(local_path, "wb") as f_out:
                        f_out.write(r.content)
                return os.path.exists(local_path) and os.path.getsize(local_path) > 0
        except Exception:
            pass

    return False

def generate_obsidian_vault_zip(
    df: pd.DataFrame,
    output_zip_path: str,
    vault_name: str = "Studijni_Karticky",
    front_cols: list = None,
    back_cols: list = None,
    col_styles: dict = None,
    media_tasks: dict = None,
    include_guide: bool = True,
    include_index: bool = True,
    card_separator: str = "?"
) -> int:
\
\
\
\

    import zipfile, io, re, html, json, time
    if front_cols is None: front_cols = []
    if back_cols is None: back_cols = []
    if col_styles is None: col_styles = {}
    if media_tasks is None: media_tasks = {}

    v_slug = slugify(vault_name) or "Studijni_Karticky"
    zip_buffer = io.BytesIO()

    def _format_obs_field(col_name, val_str):
        if not val_str:
            return ""
        s = str(val_str).strip()
        if not s or s.lower() == "nan":
            return ""
        st_cfg = col_styles.get(col_name, {})
        txt_style = st_cfg.get("txt_style", "Výchozí")
        color = st_cfg.get("color", "Výchozí (šedá)")

        if s.startswith("http://") or s.startswith("https://"):
            link_lbl = "Otevřít odkaz"
            if "mykologie.net" in s: link_lbl = "Otevřít profil na Mykologie.net"
            elif "pladias.cz" in s: link_lbl = "Otevřít taxon na Pladias.cz"
            elif "biolib.cz" in s: link_lbl = "Otevřít taxon na BioLib.cz"
            elif "inaturalist.org" in s: link_lbl = "Zobrazit pozorování na iNaturalist"
            return f"[{link_lbl}]({s})"

        s = s.replace("\r\n", "\n").replace("\n\n", "<br><br>").replace("\n", "<br>")

        styled_val = s
        if txt_style == "Tučné":
            styled_val = f"**{s}**"
        elif txt_style == "Kurzíva":
            styled_val = f"*{s}*"
        elif txt_style == "Podtržené":
            styled_val = f"<u>{s}</u>"

        color_map = {
            "Zelená": "#4ade80",
            "Modrá": "#60a5fa",
            "Žlutá": "#fbbf24",
            "Červená": "#f87171",
            "Fialová": "#c084fc",
            "Šedá": "#9ca3af"
        }
        if color in color_map:
            styled_val = f'<span style="color:{color_map[color]}">{styled_val}</span>'

        return f"**{col_name}:** {styled_val}"

    preloaded_cards = []

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:

        if include_guide:
            readme_content = f"""# Jak používat tyto kartičky (Offline na mobilu i PC)

Tento balíček obsahuje kompletní studijní kartičky a poznámky s fotografiemi offline.

## Možnost 1: Okamžité spuštění bez instalace (iPhone, Android, PC)
1. Rozbalte stažený archiv `.zip` ve svém zařízení (na iPhonu v aplikaci **Soubory**, na Androidu v aplikaci **Správce souborů**).
2. Otevřete soubor **`index.html`** nebo **`Karty.html`** poklepáním.
3. Všechny kartičky se okamžitě zobrazí s fotografiemi, statistikami a možností učení (otáčení i vepisování)!

## Možnost 2: Aplikace Obsidian (iOS, Android, PC - 100% zdarma)
1. **Instalace Obsidianu:** Stáhněte si bezplatnou aplikaci **Obsidian** z App Store / Google Play.
2. **Přidání kartiček:**
   - Rozbalenou složku `{v_slug}` přesuňte do složky **Obsidian** na vašem zařízení / iCloudu.
   - V Obsidianu klikněte na *Open folder as vault* a vyberte tuto složku.
3. **Zkoušení kartiček (Spaced Repetition):**
   - V Nastavení Obsidianu zapněte komunitní doplněk **Spaced Repetition** (autor Stephen R. Adams).
   - V levém panelu klepněte na ikonu kartiček pro spuštění zkoušení.
"""
            zf.writestr(f"{v_slug}/00_NAVOD_JAK_POUZIVAT.md", readme_content.encode('utf-8'))
            zf.writestr("00_NAVOD_JAK_POUZIVAT.md", readme_content.encode('utf-8'))

        index_lines = [
            f"# Rejstřík a přehled: {vault_name}",
            "",
            f"Celkem položek: **{len(df)}**",
            "",
            "## Seznam položek:",
            ""
        ]

        for idx, row in df.iterrows():
            primary_name = str(row.iloc[0]).strip() if len(row) > 0 else f"Položka {idx + 1}"
            safe_filename = re.sub(r'[\\/*?:"<>|]', '_', primary_name).strip() or f"Polozka_{idx+1}"

            front_parts = []
            back_parts = []

            for col in front_cols:
                val = row.get(col)
                if pd.isna(val) or str(val).strip() == "" or str(val).lower() == "nan":
                    continue
                if check_col_is_image(col, df) or is_image_col(col, val):
                    entries = [u.strip() for u in str(val).split(';') if u.strip()]
                    for entry in entries:
                        raw_u = entry.split('|')[0].strip()
                        lpath = media_tasks.get(raw_u, "")
                        img_fn = os.path.basename(lpath) if lpath else os.path.basename(raw_u)
                        if not img_fn.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                            img_fn = f"{safe_filename}_{len(front_parts)}.jpg"
                        front_parts.append(f"![[{img_fn}]]")
                else:
                    front_parts.append(_format_obs_field(col, val))

            for col in back_cols:
                val = row.get(col)
                if pd.isna(val) or str(val).strip() == "" or str(val).lower() == "nan":
                    continue
                if check_col_is_image(col, df) or is_image_col(col, val):
                    entries = [u.strip() for u in str(val).split(';') if u.strip()]
                    for entry in entries:
                        raw_u = entry.split('|')[0].strip()
                        lpath = media_tasks.get(raw_u, "")
                        img_fn = os.path.basename(lpath) if lpath else os.path.basename(raw_u)
                        if not img_fn.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                            img_fn = f"{safe_filename}_back_{len(back_parts)}.jpg"
                        back_parts.append(f"![[{img_fn}]]")
                else:
                    back_parts.append(_format_obs_field(col, val))

            front_md = "\n".join(front_parts) if front_parts else f"**{primary_name}**"
            back_md = "\n".join(back_parts) if back_parts else "Popis není k dispozici"

            clean_tag_slug = re.sub(r'[^a-zA-Z0-9_\-\u00C0-\u017F]', '_', v_slug).strip('_') or "Karticky"
            deck_tag = f"#flashcards/{clean_tag_slug}"

            note_md = f"""---
tags:
  - flashcards
  - atlas
---

{deck_tag}

# {primary_name}
{front_md}
{card_separator}
{back_md}
"""
            zf.writestr(f"{v_slug}/{safe_filename}.md", note_md.encode('utf-8'))
            index_lines.append(f"- [[{safe_filename}|{primary_name}]]")

            preloaded_cards.append({
                "id": f"c_{idx}_{v_slug}",
                "title": primary_name,
                "front": front_md,
                "back": back_md,
                "interval": 0,
                "reps": 0,
                "ease": 2.5,
                "due": 0,
                "state": 0
            })

        if include_index:
            zf.writestr(f"{v_slug}/00_Atlas_a_Prehled.md", "\n".join(index_lines).encode('utf-8'))

        deck_obj = {
            "id": f"deck_{v_slug}",
            "name": vault_name,
            "createdAt": int(time.time() * 1000),
            "cards": preloaded_cards
        }
        deck_js_str = f"window.PRELOADED_DECK = {json.dumps(deck_obj, ensure_ascii=False)};"
        zf.writestr(f"{v_slug}/deck_data.js", deck_js_str.encode('utf-8'))
        zf.writestr("deck_data.js", deck_js_str.encode('utf-8'))

        karty_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Karty.html")
        if os.path.exists(karty_path):
            try:
                with open(karty_path, "r", encoding="utf-8") as f_k:
                    karty_str = f_k.read()

                karty_inlined = karty_str.replace("/* __INLINED_DECK_DATA__ */", deck_js_str)
                karty_bytes = karty_inlined.encode("utf-8")
                zf.writestr("index.html", karty_bytes)
                zf.writestr("Karty.html", karty_bytes)
                zf.writestr(f"{v_slug}/index.html", karty_bytes)
                zf.writestr(f"{v_slug}/Karty.html", karty_bytes)
            except Exception:
                pass

        if media_tasks:
            added_media = set()
            for raw_u, lpath in media_tasks.items():
                if lpath and os.path.exists(lpath) and os.path.isfile(lpath):
                    fn = os.path.basename(lpath)
                    if fn not in added_media:
                        try:
                            zf.write(lpath, f"{v_slug}/{fn}")
                            zf.write(lpath, fn)
                            added_media.add(fn)
                        except Exception:
                            pass

    zip_bytes = zip_buffer.getvalue()
    with open(output_zip_path, "wb") as f_out:
        f_out.write(zip_bytes)
    return len(zip_bytes)

def format_deck_description(desc_text):
\
\
\

    if not desc_text:
        return ""
    desc_text = str(desc_text).strip()
    if not desc_text:
        return ""

    raw_paras = re.split(r'\n\s*\n', desc_text)
    html_paras = []
    for para in raw_paras:
        para_clean = para.strip()
        if not para_clean:
            continue

        if re.search(r'^<(p|div|h[1-6]|table|ul|ol|hr)[^>]*>', para_clean, re.IGNORECASE):
            html_paras.append(para_clean)
        else:
            lines = [l.strip() for l in para_clean.split('\n')]
            joined_lines = "<br>".join(lines)
            html_paras.append(f"<p>{joined_lines}</p>")

    return "\n".join(html_paras)

_LOCAL_FLORA_DB_CACHE = None

def get_local_dataset_path(key_name: str) -> str:

    candidates = {
        "klic_2019": [
            r"C:\Users\adalb\Downloads\taxonList_legend_2025_12_15.xls",
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "taxonList_legend_2025_12_15.xls"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "taxonList_legend_2025_12_15.xls")
        ],
        "nepuvodni": [
            r"C:\Users\adalb\Downloads\P22401PysekSupplTableS3.xlsx",
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "P22401PysekSupplTableS3.xlsx"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "P22401PysekSupplTableS3.xlsx")
        ],
        "biotopy": [
            r"C:\Users\adalb\Downloads\habitats_cz.xlsx",
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "habitats_cz.xlsx"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "habitats_cz.xlsx")
        ],
        "ellenberg": [
            r"C:\Users\adalb\Downloads\ekologicke_indikacni_hodnoty.xlsx",
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "ekologicke_indikacni_hodnoty.xlsx"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "ekologicke_indikacni_hodnoty.xlsx")
        ],
        "cerveny_seznam": [
            r"C:\Users\adalb\Downloads\cervene-druhy-export.xlsx",
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "cervene-druhy-export.xlsx"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "cervene-druhy-export.xlsx"),
            r"C:\Users\adalb\Downloads\Cerveny_seznam_2017_(narodni_kategorie_ohrozeni).xlsx",
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "Cerveny_seznam_2017_(narodni_kategorie_ohrozeni).xlsx"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "Cerveny_seznam_2017_(narodni_kategorie_ohrozeni).xlsx")
        ]
    }
    for p in candidates.get(key_name, []):
        if os.path.exists(p):
            return p
    return ""

def load_local_flora_databases():

    global _LOCAL_FLORA_DB_CACHE
    if _LOCAL_FLORA_DB_CACHE is not None:
        return _LOCAL_FLORA_DB_CACHE

    db = {
        "klic_2019": {},
        "nepuvodni": {},
        "biotopy": {},
        "ellenberg": {},
        "cerveny_seznam": {}
    }

    def _norm(name_s):
        if not name_s or pd.isna(name_s):
            return ""
        s = str(name_s).strip()
        s = re.sub(r'\(.*?\)', '', s)
        s = re.sub(r'\s+(subsp|ssp|var|f|agg|sect|nothosubsp)\.?(\s+.*|$)', '', s, flags=re.IGNORECASE)
        parts = s.split()
        if len(parts) >= 2:
            s = f"{parts[0]} {parts[1]}"
        return re.sub(r'\s+', ' ', s).strip().lower()

    p1 = get_local_dataset_path("klic_2019")
    if p1 and os.path.exists(p1):
        try:
            df1 = pd.read_excel(p1, sheet_name="TaxonList")
            for _, r in df1.iterrows():
                name_lat = str(r.get("NameLatFinal", "")).strip() if pd.notna(r.get("NameLatFinal")) else ""
                if not name_lat:
                    continue
                auth_final = str(r.get("AuthorFinal", "")).strip() if pd.notna(r.get("AuthorFinal")) else ""
                name_cz = str(r.get("NameCzFinal", "")).strip() if pd.notna(r.get("NameCzFinal")) else ""
                key_lat = str(r.get("NameLatKey2019", "")).strip() if pd.notna(r.get("NameLatKey2019")) else ""
                key_auth = str(r.get("AuthorKey2019", "")).strip() if pd.notna(r.get("AuthorKey2019")) else ""
                key_cz = str(r.get("NameCzKey2019", "")).strip() if pd.notna(r.get("NameCzKey2019")) else ""

                full_sci = f"{name_lat} {auth_final}".strip()
                key_full = f"{key_lat} {key_auth}".strip()

                item = {
                    "name_lat": name_lat,
                    "author": auth_final,
                    "name_cz": name_cz,
                    "key_name_lat": key_lat,
                    "key_author": key_auth,
                    "key_name_cz": key_cz,
                    "full_sci": full_sci,
                    "key_full": key_full
                }
                for k in [name_lat, full_sci, key_lat, key_full]:
                    if k:
                        db["klic_2019"][k] = item
                        db["klic_2019"][k.lower()] = item
                        db["klic_2019"][_norm(k)] = item
        except Exception:
            pass

    p2 = get_local_dataset_path("nepuvodni")
    if p2 and os.path.exists(p2):
        try:
            df2 = pd.read_excel(p2, sheet_name="Table S3")
            res_map = {
                "neo": "neofyt (zavlečen po r. 1492)",
                "ar": "archeofyt (zavlečen před r. 1492)",
                "ar/neo": "archeofyt / neofyt"
            }
            inv_map = {
                "cas": "přechodně zavlečený (casual)",
                "nat": "naturalizovaný / zdomácnělý (naturalized)",
                "inv": "invazní (invasive)"
            }
            origin_map = {
                "AmN": "Severní Amerika", "AmS": "Jižní Amerika", "AmC": "Střední Amerika",
                "E": "Evropa", "M": "Středozemí (Mediterán)", "As": "Asie", "Af": "Afrika",
                "Aus": "Austrálie", "anec": "anecofyt (v kultuře)", "hybrid": "hybridní původ"
            }
            for _, r in df2.iterrows():
                tx = str(r.get("Taxon", "")).strip() if pd.notna(r.get("Taxon")) else ""
                if not tx:
                    continue
                auth = str(r.get("Author", "")).strip() if pd.notna(r.get("Author")) else ""
                fam = str(r.get("Family", "")).strip() if pd.notna(r.get("Family")) else ""
                res_raw = str(r.get("Residence time", "")).strip() if pd.notna(r.get("Residence time")) else ""
                inv_raw = str(r.get("Invasion status", "")).strip() if pd.notna(r.get("Invasion status")) else ""
                orig_raw = str(r.get("Origin", "")).strip() if pd.notna(r.get("Origin")) else ""
                first_rec = str(r.get("First record", "")).strip() if pd.notna(r.get("First record")) else ""

                res_label = res_map.get(res_raw.split()[0] if res_raw else "", res_raw)
                inv_label = inv_map.get(inv_raw, inv_raw)

                orig_parts = [origin_map.get(o, o) for o in orig_raw.split()]
                orig_label = ", ".join(orig_parts) if orig_parts else orig_raw

                summary_parts = []
                if inv_label:
                    summary_parts.append(f"Status: {inv_label}")
                if res_label:
                    summary_parts.append(f"Doba: {res_label}")
                if orig_label:
                    summary_parts.append(f"Původ: {orig_label}")
                if first_rec and first_rec != "nan":
                    try:
                        yr = int(float(first_rec))
                        summary_parts.append(f"1. nález: {yr}")
                    except Exception:
                        summary_parts.append(f"1. nález: {first_rec}")

                formatted = " | ".join(summary_parts)
                item = {
                    "taxon": tx, "author": auth, "family": fam,
                    "residence_time": res_label, "invasion_status": inv_label,
                    "origin": orig_label, "first_record": first_rec, "formatted": formatted
                }
                db["nepuvodni"][tx] = item
                db["nepuvodni"][tx.lower()] = item
                db["nepuvodni"][_norm(tx)] = item
        except Exception:
            pass

    p3 = get_local_dataset_path("biotopy")
    if p3 and os.path.exists(p3):
        try:
            df3 = pd.read_excel(p3)
            hab_cols = [c for c in df3.columns if c != "Taxon"]
            for _, r in df3.iterrows():
                tx = str(r.get("Taxon", "")).strip() if pd.notna(r.get("Taxon")) else ""
                if not tx:
                    continue
                present_habs = []
                opt_habs = []
                for h in hab_cols:
                    v = r.get(h)
                    if pd.notna(v) and str(v).strip() in ["1", "1.0", "2", "2.0"]:
                        clean_h = str(h).strip()
                        if str(v).strip() in ["2", "2.0"]:
                            opt_habs.append(clean_h)
                            present_habs.append(f"{clean_h} (optimum)")
                        else:
                            present_habs.append(clean_h)
                formatted = "; ".join(present_habs)
                item = {
                    "taxon": tx,
                    "habitats": present_habs,
                    "optimal_habitats": opt_habs,
                    "formatted": formatted,
                    "count": len(present_habs)
                }
                db["biotopy"][tx] = item
                db["biotopy"][tx.lower()] = item
                db["biotopy"][_norm(tx)] = item
        except Exception:
            pass

    p4 = get_local_dataset_path("ellenberg")
    if p4 and os.path.exists(p4):
        try:
            df4 = pd.read_excel(p4, sheet_name="Data")
            for _, r in df4.iterrows():
                tx = str(r.get("Name", "")).strip() if pd.notna(r.get("Name")) else ""
                if not tx:
                    continue
                l_val = r.get("L.CZ")
                t_val = r.get("T.CZ")
                m_val = r.get("M.CZ")
                r_val = r.get("R.CZ")
                n_val = r.get("N.CZ")
                s_val = r.get("S.CZ")

                def _fmt_val(v):
                    if pd.isna(v) or str(v) == 'nan' or str(v).strip() == '':
                        return None
                    if isinstance(v, float) and v.is_integer():
                        return str(int(v))
                    return str(v)

                parts = []
                if _fmt_val(l_val) is not None:
                    parts.append(f"Světlo (L): {_fmt_val(l_val)}")
                if _fmt_val(t_val) is not None:
                    parts.append(f"Teplota (T): {_fmt_val(t_val)}")
                if _fmt_val(m_val) is not None:
                    parts.append(f"Vlhkost (M): {_fmt_val(m_val)}")
                if _fmt_val(r_val) is not None:
                    parts.append(f"Reakce (R): {_fmt_val(r_val)}")
                if _fmt_val(n_val) is not None:
                    parts.append(f"Živiny (N): {_fmt_val(n_val)}")
                if _fmt_val(s_val) is not None:
                    parts.append(f"Salinita (S): {_fmt_val(s_val)}")

                formatted = " | ".join(parts)
                item = {
                    "name": tx, "L": l_val, "T": t_val, "M": m_val, "R": r_val, "N": n_val, "S": s_val,
                    "formatted": formatted
                }
                db["ellenberg"][tx] = item
                db["ellenberg"][tx.lower()] = item
                db["ellenberg"][_norm(tx)] = item
        except Exception:
            pass

    p5 = get_local_dataset_path("cerveny_seznam")
    if p5 and os.path.exists(p5):
        try:
            df5 = pd.read_excel(p5)
            is_aopk_export = len(df5.columns) >= 8 or any("skupina" in str(c).lower() or "zdroj" in str(c).lower() or "kategori" in str(c).lower() for c in df5.columns)
            if is_aopk_export:
                c_cz = df5.columns[0]
                c_lat = df5.columns[1]
                c_auth = df5.columns[2] if len(df5.columns) > 2 else ""
                c_grp_cz = df5.columns[3] if len(df5.columns) > 3 else ""
                c_grp_lat = df5.columns[4] if len(df5.columns) > 4 else ""
                c_cat_code = df5.columns[5] if len(df5.columns) > 5 else ""
                c_cat_desc = df5.columns[6] if len(df5.columns) > 6 else ""
                c_src = df5.columns[8] if len(df5.columns) > 8 else ""
                c_url = df5.columns[9] if len(df5.columns) > 9 else ""

                for _, r in df5.iterrows():
                    tx_lat = str(r.get(c_lat, "")).strip() if (c_lat and pd.notna(r.get(c_lat))) else ""
                    tx_cz = str(r.get(c_cz, "")).strip() if (c_cz and pd.notna(r.get(c_cz))) else ""
                    if not tx_lat and not tx_cz:
                        continue
                    cat_code = str(r.get(c_cat_code, "")).strip() if (c_cat_code and pd.notna(r.get(c_cat_code))) else ""
                    cat_desc = str(r.get(c_cat_desc, "")).strip() if (c_cat_desc and pd.notna(r.get(c_cat_desc))) else ""
                    if cat_code and cat_desc and cat_code != cat_desc:
                        formatted_cat = f"{cat_code} ({cat_desc})"
                    elif cat_desc:
                        formatted_cat = cat_desc
                    elif cat_code:
                        formatted_cat = cat_code
                    else:
                        formatted_cat = "Nezařazen / Bez kategorie"
                    author = str(r.get(c_auth, "")).strip() if (c_auth and pd.notna(r.get(c_auth))) else ""
                    tax_grp_cz = str(r.get(c_grp_cz, "")).strip() if (c_grp_cz and pd.notna(r.get(c_grp_cz))) else ""
                    tax_grp_lat = str(r.get(c_grp_lat, "")).strip() if (c_grp_lat and pd.notna(r.get(c_grp_lat))) else ""
                    tax_grp = f"{tax_grp_cz} ({tax_grp_lat})" if (tax_grp_cz and tax_grp_lat) else (tax_grp_cz or tax_grp_lat)
                    source_cit = str(r.get(c_src, "")).strip() if (c_src and pd.notna(r.get(c_src))) else ""
                    source_cit = re.sub(r'<[^>]+>', '', source_cit).strip()
                    url_link = str(r.get(c_url, "")).strip() if (c_url and pd.notna(r.get(c_url))) else ""
                    if url_link == "nan":
                        url_link = ""

                    item = {
                        "taxon": tx_lat or tx_cz,
                        "lat_name": tx_lat,
                        "cz_name": tx_cz,
                        "code": cat_code,
                        "category_desc": cat_desc,
                        "formatted": formatted_cat,
                        "author": author,
                        "group_cz": tax_grp_cz,
                        "group_lat": tax_grp_lat,
                        "group": tax_grp,
                        "source": source_cit,
                        "url": url_link
                    }
                    if tx_lat:
                        db["cerveny_seznam"][tx_lat] = item
                        db["cerveny_seznam"][tx_lat.lower()] = item
                        norm_lat = _norm(tx_lat)
                        if norm_lat:
                            db["cerveny_seznam"][norm_lat] = item
                    if tx_cz:
                        db["cerveny_seznam"][tx_cz] = item
                        db["cerveny_seznam"][tx_cz.lower()] = item
            else:
                cat_desc = {
                    "A1": "A1 (vyhynulý taxon – EX)",
                    "A2": "A2 (nezvěstný taxon – EW/RE)",
                    "A3": "A3 (nejasný případ – DD/vyhynulý)",
                    "C1r": "C1r (kriticky ohrožený vzácný – CR)",
                    "C1t": "C1t (kriticky ohrožený ustupující – CR)",
                    "C1b": "C1b (kriticky ohrožený vzácný a ustupující – CR)",
                    "C2r": "C2r (silně ohrožený vzácný – EN)",
                    "C2t": "C2t (silně ohrožený ustupující – EN)",
                    "C2b": "C2b (silně ohrožený vzácný a ustupující – EN)",
                    "C3": "C3 (ohrožený taxon – VU)",
                    "C4a": "C4a (vzácnější taxon vyžadující pozornost – NT)",
                    "C4b": "C4b (ustupující taxon vyžadující pozornost – NT)",
                    "taxon není zařazen do červeného seznamu": "Nezařazen (běžný taxon / LC)"
                }
                for _, r in df5.iterrows():
                    tx = str(r.get("Taxon", "")).strip() if pd.notna(r.get("Taxon")) else ""
                    if not tx:
                        continue
                    cat_raw = str(r.get("Hodnota [položka číselníku]", "")).strip()
                    desc = cat_desc.get(cat_raw, cat_raw)
                    item = {
                        "taxon": tx,
                        "lat_name": tx,
                        "cz_name": "",
                        "code": cat_raw,
                        "category_desc": desc,
                        "formatted": desc,
                        "author": "",
                        "group_cz": "Cévnaté rostliny",
                        "group_lat": "Tracheophyta",
                        "group": "Cévnaté rostliny (Tracheophyta)",
                        "source": "Grulich V. (2017) Červený seznam cévnatých rostlin ČR",
                        "url": ""
                    }
                    db["cerveny_seznam"][tx] = item
                    db["cerveny_seznam"][tx.lower()] = item
                    db["cerveny_seznam"][_norm(tx)] = item
        except Exception:
            pass

    _LOCAL_FLORA_DB_CACHE = db
    return db

def _query_local_db(section_name: str, species_name: str):
    if not species_name or pd.isna(species_name):
        return None
    db = load_local_flora_databases()
    sub_db = db.get(section_name, {})
    if not sub_db:
        return None
    s = str(species_name).strip()
    if s in sub_db:
        return sub_db[s]
    if s.lower() in sub_db:
        return sub_db[s.lower()]

    clean_s = re.sub(r'\(.*?\)', '', s)
    clean_s = re.sub(r'\s+(subsp|ssp|var|f|agg|sect|nothosubsp)\.?(\s+.*|$)', '', clean_s, flags=re.IGNORECASE)
    parts = clean_s.split()
    if len(parts) >= 2:
        norm_key = f"{parts[0]} {parts[1]}".strip().lower()
        if norm_key in sub_db:
            return sub_db[norm_key]
    return None

def query_klic_2019(species_name: str):
    return _query_local_db("klic_2019", species_name)

def query_nepuvodni_flora(species_name: str):
    return _query_local_db("nepuvodni", species_name)

def query_biotopy(species_name: str):
    return _query_local_db("biotopy", species_name)

def query_ellenberg(species_name: str):
    return _query_local_db("ellenberg", species_name)

def query_cerveny_seznam(species_name: str):
    return _query_local_db("cerveny_seznam", species_name)

_GENUS_PDF_TEXT_CACHE = {}

def get_genus_pdf_text(genus: str) -> str:
    g_clean = genus.strip().capitalize()
    if not g_clean:
        return ""
    if g_clean in _GENUS_PDF_TEXT_CACHE:
        return _GENUS_PDF_TEXT_CACHE[g_clean]

    url = f"https://files.ibot.cas.cz/cevs/images/taxa/kvetena_cr/{g_clean}.pdf"
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code != 200:
            _GENUS_PDF_TEXT_CACHE[g_clean] = ""
            return ""
        reader = pypdf.PdfReader(io.BytesIO(r.content))
        full_text = []
        for page in reader.pages:
            t = page.extract_text() or ""
            full_text.append(t)
        combined = "\n".join(full_text)
        _GENUS_PDF_TEXT_CACHE[g_clean] = combined
        return combined
    except Exception:
        _GENUS_PDF_TEXT_CACHE[g_clean] = ""
        return ""

def fetch_kvetena_cr_description(species_name: str, max_chars: int = 450) -> str:
\
\

    if not species_name or pd.isna(species_name):
        return ""

    s_clean = str(species_name).strip()
    s_clean = re.sub(r'\(.*?\)', '', s_clean)
    parts = s_clean.split()
    if not parts:
        return ""
    genus = parts[0].capitalize()
    if len(parts) < 2:
        return ""
    epithet = parts[1].lower()
    epithet_clean = re.sub(r'[^a-zA-Z]', '', epithet)
    if not epithet_clean:
        return ""

    pdf_text = get_genus_pdf_text(genus)
    if not pdf_text:
        return ""

    sp_patterns = [
        re.compile(rf'(?:^|\n)\s*(?:\d+[\.\,\s]+)?{genus}\s+{epithet_clean}\b[^\n]*', re.IGNORECASE),
        re.compile(rf'(?:^|\n)\s*\d+[\.\,\s]+[A-Z]\.?\s+{epithet_clean}\b[^\n]*', re.IGNORECASE),
        re.compile(rf'(?:^|\n)\s*{genus}\s+{epithet_clean}\b', re.IGNORECASE)
    ]

    match = None
    for p in sp_patterns:
        match = p.search(pdf_text)
        if match:
            break

    if not match:
        return ""

    start_pos = match.end()
    chunk = pdf_text[start_pos:start_pos + 4000]

    chunk = re.sub(r'Searchable PDF created by OCR\.space[^\n]*', '', chunk, flags=re.IGNORECASE)

    exs_match = re.search(r'(?:Exsik[aá]ty|Exs\.)\s*:[^\n]+(?:\n[^\n]+){1,6}?\n', chunk, re.IGNORECASE)
    sub_chunk = chunk
    if exs_match:
        sub_chunk = chunk[exs_match.end():]

    morph_patterns = [
        r'(?:^|\n)\s*([A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ][a-záčďéěíňóřšťúůýž\s–\-]{0,30}?(?:byliny|stromy|keře|polokeře|dřeviny|strom|keř|bylina)\b[^\n]*)',
        r'(?:^|\n)\s*([A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ][a-záčďéěíňóřšťúůýž\s–\-]{0,20}?\d+[\s–\-]+(?:\d+[\s–\-]*)?(?:cm|m|mm)\s+vys\.[^\n]*)',
        r'(?:^|\n)\s*(Oddenek\s+[^\n]*)',
        r'(?:^|\n)\s*(Lodyha\s+[^\n]*)',
        r'(?:^|\n)\s*(Kmen\s+[^\n]*)'
    ]

    desc_start = None
    for mp in morph_patterns:
        m_morph = re.search(mp, sub_chunk)
        if m_morph:
            desc_start = m_morph.start()
            sub_chunk = sub_chunk[desc_start:]
            break

    if not desc_start:
        lines = sub_chunk.split('\n')
        clean_lines = []
        for l in lines:
            l_s = l.strip()
            if not l_s:
                continue
            if re.match(r'^(Syn\.|Exsik[aá]ty|Lit\.|Tab\.|Icon\.|Extra fines|Herb\.)', l_s, re.IGNORECASE):
                continue
            if re.match(r'^[A-Z][a-z]+\s+[A-Z\s\.,\d\(\)\–\-]+$', l_s):
                continue
            clean_lines.append(l_s)
        sub_chunk = "\n".join(clean_lines)

    end_delimiters = [
        r'(?:Ekologie\s+a\s+fytocenologie|Ekologie|Fytocenologie)\s*:',
        r'(?:Rozšíření\s+v\s+ČR|Rozšíření|Výskyt\s+v\s+ČR)\s*:',
        r'Celkové\s+rozšíření\s*:',
        r'Variabilita\s*:',
        r'Význam\s*:',
        r'Poznámka\s*:',
        r'\n\s*\d+\.\s+[A-Z][a-z]+'
    ]

    for delim in end_delimiters:
        end_match = re.search(delim, sub_chunk, re.IGNORECASE)
        if end_match:
            sub_chunk = sub_chunk[:end_match.start()]

    sub_chunk = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', sub_chunk)
    sub_chunk = re.sub(r'\s*\n\s*', ' ', sub_chunk)
    sub_chunk = re.sub(r'\s+', ' ', sub_chunk).strip()

    if max_chars and max_chars > 0 and len(sub_chunk) > max_chars:
        sentences = re.split(r'(?<=\.)\s+', sub_chunk)
        accum = []
        curr_len = 0
        for s in sentences:
            if curr_len + len(s) <= max_chars or not accum:
                accum.append(s)
                curr_len += len(s)
            else:
                break
        sub_chunk = " ".join(accum)

    return sub_chunk

def build_deck_attribution(active_cols):
\
\
\
\

    sections = []

    has_pladias_photos = any("[Pladias.cz] Fotky" in str(c) for c in active_cols)
    has_pladias_map = any("[Pladias.cz] Mapa rozšíření" in str(c) for c in active_cols)
    has_pladias_any = any(("[Pladias]" in str(c) or "[Pladias.cz]" in str(c)) for c in active_cols)

    if has_pladias_any:
        p_parts = []
        p_parts.append("<p>Tento balíček využívá data z databáze <strong>Pladias.cz – databáze české flóry a vegetace</strong> (<a href=\"https://www.pladias.cz\">www.pladias.cz</a>).</p>")
        if has_pladias_photos:
            p_parts.append("<p>Fotografie rostlin pocházejí z databáze Pladias.cz.</p>")
        if has_pladias_map:
            p_parts.append("<p>Data o rozšíření a mapy výskytu: Wild J., Kaplan Z., Danihelka J. et al. (2019) <em>Plant distribution data for the Czech Republic integrated in the Pladias.cz database</em>. – Preslia 91: 1–24. <a href=\"https://doi.org/10.23855/preslia.2019.001\">https://doi.org/10.23855/preslia.2019.001</a></p>")
        p_parts.append("<p>Hlavní citace databáze: Chytrý M., Danihelka J., Kaplan Z., Wild J. et al. (2021) <em>Pladias.cz Database of the Czech Flora and Vegetation</em>. – Preslia 93: 1–87. <a href=\"https://doi.org/10.23855/preslia.2021.001\">https://doi.org/10.23855/preslia.2021.001</a></p>")
        p_parts.append("<p style=\"font-size: 0.85em; color: #777;\">Data jsou použita pro nekomerční výukové a studijní účely v souladu s Pravidly správy a použití databáze Pladias.cz.cz.</p>")
        sections.append("\n".join(p_parts))

    has_klic_any = any("[Klíč 2019]" in str(c) for c in active_cols)
    if has_klic_any:
        k_parts = []
        k_parts.append("<p>Názvosloví a taxonomické zařazení cévnatých rostlin vychází ze Seznamu cévnatých rostlin květeny České republiky (Klíč ke květeně ČR):</p>")
        k_parts.append("<p><strong>Kaplan Z., Danihelka J., Chrtek J., Kirschner J., Kubát K., Štech M. & Štěpánek J. (eds) (2019) <em>Klíč ke květeně České republiky [Key to the flora of the Czech Republic]</em>. Ed. 2. – Academia, Praha.</strong></p>")
        sections.append("\n".join(k_parts))

    has_nepuvodni_any = any("[Nepůvodní flóra]" in str(c) for c in active_cols)
    if has_nepuvodni_any:
        np_parts = []
        np_parts.append("<p>Informace o nepůvodních a invazních druzích rostlin ČR pocházejí z Katalogu nepůvodních druhů:</p>")
        np_parts.append("<p><strong>Pyšek P., Sádlo J., Chrtek J. Jr., Chytrý M., Kaplan Z., Pergl J., Pokorná A., Axmanová I., Čuda J., Doležal J., Dřevojan P., Hejda M., Kočár P., Kortz A., Lososová Z., Lustyk P., Skálová H., Štajerová K., Večeřa M., Vítková M., Wild J. & Danihelka J. (2022) <em>Catalogue of alien plants of the Czech Republic (3rd edition): species richness, status, distributions, habitats, regional invasion levels, introduction pathways and impacts</em>. – Preslia 94: 447–577. <a href=\"https://www.preslia.cz/article/view?id=11548\">https://www.preslia.cz/article/view?id=11548</a></strong></p>")
        sections.append("\n".join(np_parts))

    has_biotopy_any = any("[Biotopy]" in str(c) for c in active_cols)
    if has_biotopy_any:
        b_parts = []
        b_parts.append("<p>Výskyt taxonu v biotopech České republiky byl hodnocen pomocí údajů z České národní fytocenologické databáze:</p>")
        b_parts.append("<p><strong>Chytrý M. & Rafajová M. (2003) <em>Czech National Phytosociological Database: basic statistics of the available vegetation-plot data</em>. – Preslia 75: 1–15.</strong><br>Sádlo J., Chytrý M. & Pyšek P. (2007) <em>Regional invasion levels in the flora of the Czech Republic</em>. – Preslia 79: 81–96 (Appendix 1).</p>")
        sections.append("\n".join(b_parts))

    has_ellenberg_any = any("[Ekologie]" in str(c) or "[Ellenberg]" in str(c) for c in active_cols)
    if has_ellenberg_any:
        e_parts = []
        e_parts.append("<p>Ekologické indikační hodnoty pro českou květenu (světlo, teplota, vlhkost, reakce, živiny, salinita):</p>")
        e_parts.append("<p><strong>Chytrý M., Tichý L., Dřevojan P., Sádlo J. & Zelený D. (2018) <em>Ellenberg-type indicator values for the Czech flora</em>. – Preslia 90: 83–103. <a href=\"https://doi.org/10.23855/preslia.2018.083\">https://doi.org/10.23855/preslia.2018.083</a></strong></p>")
        sections.append("\n".join(e_parts))

    has_cerveny_any = any("[Červený seznam]" in str(c) for c in active_cols)
    if has_cerveny_any:
        cs_parts = []
        cs_parts.append("<p>Národní kategorie ohrožení organismů v České republice (AOPK ČR / nature.cz):</p>")
        cs_parts.append("<p><strong>Agentura ochrany přírody a krajiny ČR (AOPK ČR): <em>Červené seznamy ohrožených druhů České republiky (cévnaté rostliny, houby, mechorosty, lišejníky, bezobratlí, obratlovci)</em>. – Příroda, Praha / portal23.nature.cz.</strong></p>")
        sections.append("\n".join(cs_parts))

    has_kvetena_any = any("[Květena ČR]" in str(c) for c in active_cols)
    if has_kvetena_any:
        kv_parts = []
        kv_parts.append("<p>Botanické popisy cévnatých rostlin pocházejí z kompendia <strong>Květena České republiky</strong> (Hejný & Slavík et al. / Academia, Praha):</p>")
        kv_parts.append("<p><strong>Hejný S. & Slavík B. (eds) (1988–2010) <em>Květena České republiky [Flora of the Czech Republic]</em>. Vol. 1–8. – Academia, Praha.</strong></p>")
        kv_parts.append("<p style=\"font-size: 0.85em; color: #777;\">Zdroj: Botanický ústav AV ČR (files.ibot.cas.cz/cevs/images/taxa/kvetena_cr/). Použito pro nekomerční vzdělávací a studijní účely.</p>")
        sections.append("\n".join(kv_parts))

    has_myko_img = any("[Mykologie.net] Fotky" in str(c) for c in active_cols)
    has_myko_desc = any("[Mykologie.net] Popis" in str(c) for c in active_cols)
    has_myko_link = any("[Mykologie.net] Odkaz" in str(c) for c in active_cols)
    has_myko_any = any("[Mykologie.net]" in str(c) for c in active_cols)

    if has_myko_any:
        m_parts = []
        if has_myko_img and (has_myko_desc or has_myko_link):
            m_parts.append("<p>Obrázky hub, popisy a taxonomické informace použité v tomto balíčku pocházejí z mykologického portálu <strong>Mykologie.net</strong> (<a href=\"https://www.mykologie.net\">www.mykologie.net</a>).</p>")
        elif has_myko_img:
            m_parts.append("<p>Obrázky a fotografie hub použité v tomto balíčku pocházejí ze serveru <strong>Mykologie.net</strong> (<a href=\"https://www.mykologie.net\">www.mykologie.net</a>).</p>")
        elif has_myko_desc:
            m_parts.append("<p>Textové popisy a informace o houbách pocházejí ze serveru <strong>Mykologie.net</strong> (<a href=\"https://www.mykologie.net\">www.mykologie.net</a>).</p>")
        else:
            m_parts.append("<p>Odkazy a data o houbách použité v tomto balíčku odkazují na mykologický portál <strong>Mykologie.net</strong> (<a href=\"https://www.mykologie.net\">www.mykologie.net</a>).</p>")

        m_parts.append("<p style=\"font-size: 0.85em; color: #777;\">Zdroj: Mykologie.net – Houby v České republice. Všechna autorská práva k fotografiím a textům náleží autorům a serveru Mykologie.net. Použito pro nekomerční vzdělávací účely.</p>")
        sections.append("\n".join(m_parts))

    has_dalibor_any = any("[DaLiBor]" in str(c) for c in active_cols)
    if has_dalibor_any:
        d_parts = []
        d_parts.append("<p>Data, fotografie a popisy lišejníků pocházejí z portálu <strong>DaLiBor – Databáze lišejníků České republiky / Atlas českých lišejníků</strong> (<a href=\"https://dalib.cz\">dalib.cz</a>).</p>")
        d_parts.append("<p style=\"font-size: 0.85em; color: #777;\">Zdroj: DaLiBor (dalib.cz) – Atlas českých lišejníků. Autorská práva k fotografiím a textům náleží autorům a správcům portálu DaLiBor. Použito pro nekomerční vzdělávací účely.</p>")
        sections.append("\n".join(d_parts))

    has_diatom_any = any("[DiatomBase]" in str(c) for c in active_cols)
    if has_diatom_any:
        dt_parts = []
        dt_parts.append("<p>Taxonomická data a autority rozsivek pocházejí z databáze <strong>DiatomBase</strong> (<a href=\"https://www.diatombase.org\">www.diatombase.org</a>) / World Register of Marine Species (WoRMS).</p>")
        dt_parts.append("<p style=\"font-size: 0.85em; color: #777;\">Zdroj: DiatomBase. Použito pro nekomerční vzdělávací a studijní účely.</p>")
        sections.append("\n".join(dt_parts))

    has_algae_any = any("[AlgaeBase]" in str(c) for c in active_cols)
    if has_algae_any:
        a_parts = []
        a_parts.append("<p>Odkazy a data o řasách a sinicích odkazují na celosvětovou taxonomickou databázi <strong>AlgaeBase</strong> (<a href=\"https://www.algaebase.org\">www.algaebase.org</a>; Guiry, M.D. & Guiry, G.M.).</p>")
        a_parts.append("<p style=\"font-size: 0.85em; color: #777;\">Zdroj: AlgaeBase. World-wide electronic publication, National University of Ireland, Galway.</p>")
        sections.append("\n".join(a_parts))

    has_cc_media = any(
        "[iNat]" in str(c) or "[GBIF]" in str(c) or "[Wikimedia]" in str(c) or "[Zvuky]" in str(c)
        for c in active_cols
    )
    if has_cc_media:
        cc_parts = []
        cc_parts.append("<p><strong>Otevřené licence a multimédia (Creative Commons):</strong></p>")
        cc_parts.append("<p>Fotografie a audio nahrávky z mezinárodních repozitářů <strong>iNaturalist</strong>, <strong>GBIF</strong>, <strong>Wikimedia Commons</strong> a <strong>Xeno-canto</strong> jsou použity v souladu s jejich licencemi Creative Commons (CC0, CC BY, CC BY-SA, CC BY-NC, CC BY-NC-SA) s uvedením konkrétních autorů, držitelů práv a licencí přímo u jednotlivých položek.</p>")
        sections.append("\n".join(cc_parts))

    has_adw_any = any("[ADW]" in str(c) for c in active_cols)
    if has_adw_any:
        adw_parts = []
        adw_parts.append("<p>Zoologické popisy živočichů pocházejí z databáze <strong>Animal Diversity Web</strong> (University of Michigan Museum of Zoology, ADW) (<a href=\"https://animaldiversity.org\">animaldiversity.org</a>).</p>")
        adw_parts.append("<p style=\"font-size: 0.85em; color: #777;\">Zdroj: Myers, P., R. Espinosa, C. S. Parr, T. Jones, G. S. Hammond, and T. A. Dewey. 2024. The Animal Diversity Web (online). animaldiversity.org. Použito pro nekomerční vzdělávací účely.</p>")
        sections.append("\n".join(adw_parts))

    has_powo_any = any("[POWO Kew]" in str(c) for c in active_cols)
    if has_powo_any:
        powo_parts = []
        powo_parts.append("<p>Botanické popisy a distribuce rostlin pocházejí z mezinárodní databáze <strong>Plants of the World Online</strong> (Royal Botanic Gardens, Kew) (<a href=\"https://powo.science.kew.org\">powo.science.kew.org</a>).</p>")
        powo_parts.append("<p style=\"font-size: 0.85em; color: #777;\">Zdroj: POWO (2024). Plants of the World Online. Facilitated by the Royal Botanic Gardens, Kew. powo.science.kew.org. Použito pro nekomerční vzdělávací účely.</p>")
        sections.append("\n".join(powo_parts))

    has_eol_any = any("[EOL]" in str(c) for c in active_cols)
    if has_eol_any:
        eol_parts = []
        eol_parts.append("<p>Odkaz na encyklopedii druhů <strong>Encyclopedia of Life</strong> (<a href=\"https://eol.org\">eol.org</a>).</p>")
        eol_parts.append("<p style=\"font-size: 0.85em; color: #777;\">Zdroj: Encyclopedia of Life. eol.org. Použito pro nekomerční vzdělávací účely.</p>")
        sections.append("\n".join(eol_parts))

    return "\n<hr>\n".join(sections)

def transcribe_latin_to_czech_phonetics(latin_name: str) -> str:
\
\
\
\

    if not latin_name or pd.isna(latin_name):
        return ""
    text = str(latin_name).strip()
    if not text:
        return ""

    text = re.sub(r'\s*\(.*?\)\s*', ' ', text).strip()
    text = re.sub(r'\s+(subsp|ssp|var|f|agg|sect|nothosubsp)\.?(\s+.*|$)', '', text, flags=re.IGNORECASE).strip()

    words = text.split()
    phonetic_words = []

    for w in words:
        trail = ""
        m_trail = re.search(r'[^a-zA-ZáéíóúýčďěňřšťžůÁÉÍÓÚÝČĎĚŇŘŠŤŽŮ]+$', w)
        if m_trail:
            trail = m_trail.group(0)
            w = w[:-len(trail)]

        if not w:
            continue

        low = w.lower()

        vowels = "aeiouyéěáíóú"
        low = re.sub(rf'(?<![stx])ti(?=[{vowels}])', 'ci', low)

        low = re.sub(r'qu', 'kv', low)
        low = re.sub(r'gu(?=[aeiouyéěáíóú])', 'gv', low)
        low = re.sub(r'ph', 'f', low)
        low = re.sub(r'th', 't', low)
        low = re.sub(r'rh', 'r', low)
        low = re.sub(r'ae', 'é', low)
        low = re.sub(r'oe', 'é', low)

        low = re.sub(r'c(?![eiyéěh])', 'k', low)

        low = re.sub(rf'([{vowels}rlmn])s(?=[{vowels}mnlr])', r'\1z', low)

        low = re.sub(r'cc(?=[eiyéě])', 'kc', low)
        low = re.sub(r'cc', 'k', low)

        low = re.sub(r'x', 'ks', low)

        phonetic_words.append(f"[{low}]{trail}")

    return " ".join(phonetic_words)

@functools.lru_cache(maxsize=4096)
def _cached_diatombase_data(sp_clean: str):
\
\
\
\
\
\
\

    res = {
        "scientific_name": "",
        "authority": "",
        "status": "",
        "url": "",
        "classification": "",
        "source": "Nenalezeno"
    }
    if not species_name or pd.isna(species_name):
        return res
    sp_clean = str(species_name).strip()
    sp_clean = re.sub(r'\s*\(.*?\)\s*', ' ', sp_clean).strip()
    sp_clean = re.sub(r'\s+sp(p)?\.?$', '', sp_clean).strip()
    if not sp_clean:
        return res

    headers = {'User-Agent': 'AnkiSpeciesGenerator/1.0 (educational use)'}
    api_url = f"https://www.marinespecies.org/rest/AphiaRecordsByName/{urllib.parse.quote(sp_clean)}?like=false&marine_only=false"
    try:
        r = requests.get(api_url, headers=headers, timeout=6)
        if r.status_code == 200:
            records = r.json()
            if records and isinstance(records, list):
                rec = records[0]
                rec_str = str(rec).lower()

                is_diatom = (
                    rec.get("class") in ["Bacillariophyceae", "Coscinodiscophyceae", "Fragilariophyceae", "Mediophyceae"]
                    or rec.get("phylum") in ["Bacillariophyta", "Ochrophyta"]
                    or any(k in rec_str for k in ["bacillariophy", "diatom", "ochrophyta", "coscinodisco", "fragilariophy", "mediophy"])
                )
                if is_diatom:
                    res["scientific_name"] = rec.get("scientificname", sp_clean)
                    res["authority"] = rec.get("authority", "")
                    res["status"] = rec.get("status", "")
                    aphia_id = rec.get("AphiaID")
                    if aphia_id:
                        res["url"] = f"https://www.diatombase.org/aphia.php?p=taxdetails&id={aphia_id}"
                    tax_parts = []
                    for rank in ["class", "order", "family", "genus"]:
                        if rec.get(rank):
                            tax_parts.append(rec.get(rank))
                    res["classification"] = " › ".join(tax_parts)
                    res["source"] = "DiatomBase"
    except Exception:
        pass
    return res

def fetch_diatombase_data(species_name):
    if not species_name or pd.isna(species_name):
        return {
            "scientific_name": "", "authority": "", "status": "",
            "url": "", "classification": "", "source": "Nenalezeno"
        }
    sp_clean = str(species_name).strip()
    sp_clean = re.sub(r'\s*\(.*?\)\s*', ' ', sp_clean).strip()
    sp_clean = re.sub(r'\s+sp(p)?\.?$', '', sp_clean).strip()
    if not sp_clean:
        return {
            "scientific_name": "", "authority": "", "status": "",
            "url": "", "classification": "", "source": "Nenalezeno"
        }
    return _cached_diatombase_data(sp_clean).copy()

@functools.lru_cache(maxsize=4096)
def _cached_dalibor_data(species_name: str, max_photos: int = 3):
\
\
\
\
\
\

    res = {
        "scientific_name": "",
        "czech_name": "",
        "description": "",
        "photo_urls": [],
        "url": "",
        "source": "Nenalezeno"
    }
    if not species_name or pd.isna(species_name):
        return res
    sp_clean = str(species_name).strip()
    sp_clean = re.sub(r'\s*\(.*?\)\s*', ' ', sp_clean).strip()
    sp_clean = re.sub(r'\s+sp(p)?\.?$', '', sp_clean).strip()
    if not sp_clean:
        return res

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
    dalib_url = f"https://dalib.cz/taxon/info/{urllib.parse.quote(sp_clean)}"
    try:
        r = requests.get(dalib_url, headers=headers, timeout=8)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')

            photos = []
            for img in soup.find_all('img'):
                src = img.get('src', '')
                if '/image/' in src:
                    full_img = src.replace('/thumb/', '/web/')
                    full_img_url = urllib.parse.urljoin('https://dalib.cz', full_img)
                    if full_img_url not in photos:
                        photos.append(full_img_url)

            desc_parts = []
            content_div = soup.find('div', class_='content') or soup
            for p in content_div.find_all('p'):
                p_text = p.get_text(separator=' ', strip=True)
                if len(p_text) < 35:
                    continue

                if any(bad in p_text.lower() for bad in [
                    'botanick', 'copyright', 'počet záznamů', 'pocet zaznamu', 'poet zznam',
                    'kliknutím', 'menu', 'ascomycota', 'cookie', 'dalibor.cz',
                    'databáze lišejníků', 'atlas českých lišejníků', '©', 'v. v. i.', 'v.v.i.', 'všechna práva'
                ]):
                    continue
                if p_text not in desc_parts:
                    desc_parts.append(p_text)

            title_elem = soup.find('h1') or soup.find('h2')
            found_title = title_elem.get_text(strip=True) if title_elem else ""

            is_valid_dalibor = False
            if photos or desc_parts:
                is_valid_dalibor = True
            elif found_title and len(sp_clean.split()) >= 2:
                genus_name = sp_clean.split()[0].lower()
                if genus_name in found_title.lower() and "atlas" not in found_title.lower():
                    is_valid_dalibor = True

            if is_valid_dalibor:
                res["scientific_name"] = found_title if found_title else sp_clean
                res["url"] = dalib_url
                res["source"] = "DaLiBor (dalib.cz)"
                res["photo_urls"] = photos[:max_photos]
                if desc_parts:
                    res["description"] = "\n\n".join(desc_parts[:4])
    except Exception:
        pass
    return res

def fetch_dalibor_data(species_name, max_photos=3):
    if not species_name or pd.isna(species_name):
        return {'scientific_name': '', 'czech_name': '', 'description': '', 'photo_urls': [], 'url': '', 'source': 'Nenalezeno'}
    sp = str(species_name).strip()
    if not sp:
        return {'scientific_name': '', 'czech_name': '', 'description': '', 'photo_urls': [], 'url': '', 'source': 'Nenalezeno'}
    res = _cached_dalibor_data(sp, int(max_photos))
    return {k: (v.copy() if isinstance(v, list) else v) for k, v in res.items()}

def fetch_gbif_plant_photos(species_name, get_kvet=True, get_list=True, get_herbar=False):
\
\
\

    photos = {
        "kvet": "",
        "list": "",
        "herbar": "",
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

        kvet_keywords = ["flower", "flos", "inflorescence", "fleur", "blüte"]
        list_keywords = ["leaf", "leaves", "folium", "feuille", "blatt"]

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
                            if not is_cc_license(media.get("license")):
                                continue

                            title = str(media.get("title", "")).lower()
                            desc = str(media.get("description", "")).lower()
                            attr_text = extract_gbif_attribution(media, occ)

                            if get_kvet and not photos["kvet"] and any(kw in title or kw in desc for kw in kvet_keywords):
                                photos["kvet"] = f"{img_url}|{attr_text}"
                                photos["source"] = "GBIF Occurrence"

                            elif get_list and not photos["list"] and any(kw in title or kw in desc for kw in list_keywords):
                                photos["list"] = f"{img_url}|{attr_text}"
                                photos["source"] = "GBIF Occurrence"

            except Exception:
                pass

        if get_herbar and not photos["herbar"]:
            try:
                r_herb = requests.get(
                    "https://api.gbif.org/v1/occurrence/search",
                    params={"taxonKey": usage_key, "mediaType": "StillImage", "basisOfRecord": "PRESERVED_SPECIMEN", "limit": 20},
                    timeout=8
                )
                if r_herb.status_code == 200:
                    results = r_herb.json().get("results", [])
                    for occ in results:
                        media_list = occ.get("media", [])
                        for media in media_list:
                            if media.get("type") == "StillImage" or str(media.get("format", "")).startswith("image/"):
                                img_url = media.get("identifier")
                                if img_url and is_cc_license(media.get("license")):
                                    attr_text = extract_gbif_attribution(media, occ)
                                    photos["herbar"] = f"{img_url}|{attr_text}"
                                    photos["source"] = "GBIF Herbarium"
                                    break
                        if photos["herbar"]:
                            break
            except Exception:
                pass
    except Exception:
        pass

    return photos

def fetch_gbif_zoo_photos(species_name, max_photos=3):
\
\
\

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
            "kingdom": "Animalia",
            "strict": "true"
        }
        r_match = requests.get(match_url, params=match_params, timeout=5)
        if r_match.status_code == 200:
            match_data = r_match.json()
            if match_data.get("matchType") not in ["NONE", "HIGHERRANK"] and match_data.get("rank") not in ["KINGDOM", "PHYLUM", "CLASS"] and match_data.get("kingdom") == "Animalia":
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
                                    if img_url and is_cc_license(media.get("license")):
                                        if not any(p.split('|')[0] == img_url for p in photos):
                                            attr_text = extract_gbif_attribution(media, occ)
                                            photos.append(f"{img_url}|{attr_text}")
                                            if len(photos) >= max_photos:
                                                break
    except Exception:
        pass
    return photos

def fetch_gbif_fungi_photos(species_name, max_photos=3):
\
\
\

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
            "kingdom": "Fungi",
            "strict": "true"
        }
        r_match = requests.get(match_url, params=match_params, timeout=5)
        usage_key = None
        if r_match.status_code == 200:
            match_data = r_match.json()
            if match_data.get("matchType") not in ["NONE", "HIGHERRANK"] and match_data.get("rank") not in ["KINGDOM", "PHYLUM", "CLASS"] and match_data.get("kingdom") == "Fungi":
                usage_key = match_data.get("usageKey")

        if usage_key:
            occ_url = "https://api.gbif.org/v1/occurrence/search"
            occ_params = {
                "taxonKey": usage_key,
                "mediaType": "StillImage",
                "limit": 35
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
                            if img_url and is_cc_license(media.get("license")):
                                if not any(p.split('|')[0] == img_url for p in photos):
                                    attr_text = extract_gbif_attribution(media, occ)
                                    photos.append(f"{img_url}|{attr_text}")
                                    if len(photos) >= max_photos:
                                        break
    except Exception:
        pass
    return photos

@functools.lru_cache(maxsize=4096)
def _cached_mykologie_data(query_str: str, max_photos: int = 4):
\
\
\
\
\
\
\

    res = {
        'title': '',
        'czech_name': '',
        'latin_name': '',
        'description': '',
        'photo_urls': [],
        'url': '',
        'source': 'Nenalezeno'
    }
    if not query or pd.isna(query):
        return res
    query_str = str(query).strip()
    if not query_str:
        return res

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    clean_q = re.sub(r'\s*\(.*?\)\s*', ' ', query_str).strip()
    clean_q = re.sub(r'\s+sp(p)?\.?$', '', clean_q).strip()
    if not clean_q:
        clean_q = query_str

    def _do_search(search_term):
        s_url = f"https://www.mykologie.net/index.php?option=com_k2&view=itemlist&task=search&searchword={urllib.parse.quote(search_term)}"
        try:
            r = requests.get(s_url, headers=headers, timeout=8)
            if r.status_code != 200:
                return []
            soup = BeautifulSoup(r.text, 'html.parser')
            items = []
            for tag in soup.find_all(['h2', 'h3', 'div'], class_=re.compile(r'catItemHeader|catItemTitle|moduleItemTitle')):
                a = tag.find('a')
                if a and a.get('href') and '/item/' in a.get('href'):
                    items.append((a.get_text(strip=True), a.get('href')))
            if not items:
                for a in soup.find_all('a'):
                    href = a.get('href', '')
                    if '/item/' in href and a.get_text(strip=True):
                        items.append((a.get_text(strip=True), href))
            return items
        except Exception:
            return []

    try:
        found_items = _do_search(clean_q)

        if not found_items and (any(ord(c) > 127 for c in clean_q) or len(clean_q.split()) != 2):
            try:
                r_tax = requests.get(
                    "https://api.inaturalist.org/v1/taxa",
                    params={"q": clean_q, "locale": "cs", "per_page": 3},
                    headers=headers,
                    timeout=5
                )
                if r_tax.status_code == 200:
                    tax_results = r_tax.json().get("results", [])
                    if tax_results:
                        sci_candidate = tax_results[0].get("name", "")
                        if sci_candidate:
                            found_items = _do_search(sci_candidate)
            except Exception:
                pass

        if not found_items:
            return res

        q_words = [w.lower() for w in clean_q.split() if len(w) > 2]
        best_item = None
        for text, href in found_items:
            t_lower = text.lower()
            if clean_q.lower() in t_lower:
                best_item = (text, href)
                break
            if q_words and all(w in t_lower for w in q_words):
                best_item = (text, href)
                break

        if not best_item and q_words:
            for text, href in found_items:
                if q_words[0] in text.lower():
                    best_item = (text, href)
                    break

        if not best_item:
            best_item = found_items[0]

        item_href = best_item[1]
        full_url = urllib.parse.urljoin('https://www.mykologie.net', item_href)
        r_item = requests.get(full_url, headers=headers, timeout=8)
        if r_item.status_code != 200:
            return res

        item_soup = BeautifulSoup(r_item.text, 'html.parser')

        title_elem = item_soup.find('h2', class_='itemTitle')
        full_title = title_elem.get_text(strip=True) if title_elem else best_item[0]
        res['title'] = full_title
        res['url'] = full_url
        res['source'] = 'Mykologie.net'

        m_title = re.match(r'^(.*?)\s*\((.*?)\)$', full_title)
        if m_title:
            res['latin_name'] = m_title.group(1).strip()
            res['czech_name'] = m_title.group(2).strip()
        else:
            res['latin_name'] = full_title

        item_full_text = item_soup.find('div', class_='itemFullText') or item_soup.find('div', class_='itemIntroText')
        paragraphs = []
        images = []

        if item_full_text:
            for p in item_full_text.find_all('p'):
                for img in p.find_all('img'):
                    src = img.get('src', '')
                    if src:
                        img_url = urllib.parse.urljoin('https://www.mykologie.net', src)
                        if img_url not in images:
                            images.append(img_url)

                p_text = p.get_text(separator=' ', strip=True)
                if p_text and '(c)' not in p_text and '©' not in p_text:
                    if len(p_text) > 40:
                        paragraphs.append(p_text)

            for img in item_full_text.find_all('img'):
                src = img.get('src', '')
                if src:
                    img_url = urllib.parse.urljoin('https://www.mykologie.net', src)
                    if img_url not in images:
                        images.append(img_url)

            if paragraphs:
                res['description'] = '\n\n'.join(paragraphs)

        if not res['description']:
            meta_desc = item_soup.find('meta', property='og:description') or item_soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                res['description'] = meta_desc.get('content', '').strip()

        res['photo_urls'] = images[:max_photos]
    except Exception:
        pass

    return res

def fetch_bird_sounds_xenocanto(species_name, sound_types=None, max_sounds=1, api_key=""):
\
\
\
\

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

                queries_to_try.append(f'sp:"{sci_parts[0]} {sci_parts[1]}" type:{stype} q:A')

                queries_to_try.append(f'sp:"{sci_parts[0]} {sci_parts[1]}" type:{stype}')

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
                    if not any(r[0] == file_url for r in results):
                        rec_name = str(rec.get("rec", "")).strip()
                        lic_url = str(rec.get("lic", "")).strip().lower()
                        lic_short = "CC"
                        if "by-nc-sa" in lic_url:
                            lic_short = "CC BY-NC-SA"
                        elif "by-nc-nd" in lic_url:
                            lic_short = "CC BY-NC-ND"
                        elif "by-nc" in lic_url:
                            lic_short = "CC BY-NC"
                        elif "by-sa" in lic_url:
                            lic_short = "CC BY-SA"
                        elif "by" in lic_url:
                            lic_short = "CC BY"
                        elif "zero" in lic_url or "cc0" in lic_url:
                            lic_short = "CC0"
                        attr_text = f"© {rec_name} ({lic_short} via Xeno-canto)" if rec_name else f"Xeno-canto ({lic_short})"
                        results.append((file_url, stype, attr_text))
                        count += 1
        except Exception:
            pass
    return results

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

def fetch_wikimedia_images(query, max_photos=4):
    if not query or pd.isna(query):
        return []
    query = str(query).strip()
    if not query:
        return []

    headers = {'User-Agent': 'AnkiCardGen/1.0 (contact: adalb@example.com)'}
    search_query = f"filetype:bitmap|drawing {query}"
    url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(search_query)}&gsrnamespace=6&gsrlimit={max_photos}&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=800&format=json"

    photos = []
    try:
        r = requests.get(url, headers=headers, timeout=6)
        if r.status_code == 200:
            data = r.json()
            pages = data.get('query', {}).get('pages', {})
            for p in pages.values():
                imageinfo = p.get('imageinfo', [])
                if imageinfo:
                    img_url = imageinfo[0].get('thumburl') or imageinfo[0].get('url')
                    if img_url:
                        extmeta = imageinfo[0].get('extmetadata', {})
                        artist_raw = extmeta.get('Artist', {}).get('value', '')
                        if artist_raw:
                            artist = BeautifulSoup(artist_raw, 'html.parser').get_text(strip=True)
                        else:
                            artist = extmeta.get('Credit', {}).get('value', '')
                            if artist:
                                artist = BeautifulSoup(artist, 'html.parser').get_text(strip=True)
                        if not artist:
                            artist = "Wikimedia Commons"
                        artist = re.sub(r'\s+', ' ', artist).strip()[:40]
                        lic_short = extmeta.get('LicenseShortName', {}).get('value', '') or extmeta.get('UsageTerms', {}).get('value', '') or "CC BY-SA"
                        attr = f"© {artist} ({lic_short} via Wikimedia)"
                        entry = f"{img_url}|{attr}"
                        if not any(p.split('|')[0] == img_url for p in photos):
                            photos.append(entry)
    except Exception:
        pass
    return photos[:max_photos]

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

def fetch_mykologie_data(query, max_photos=4):
    if not query or pd.isna(query):
        return {'title': '', 'czech_name': '', 'latin_name': '', 'description': '', 'photo_urls': [], 'url': '', 'source': 'Nenalezeno'}
    q_str = str(query).strip()
    if not q_str:
        return {'title': '', 'czech_name': '', 'latin_name': '', 'description': '', 'photo_urls': [], 'url': '', 'source': 'Nenalezeno'}
    res = _cached_mykologie_data(q_str, int(max_photos))
    return {k: (v.copy() if isinstance(v, list) else v) for k, v in res.items()}

_COUNTRIES_DB_CACHE = None

def load_countries_db():
    global _COUNTRIES_DB_CACHE
    if _COUNTRIES_DB_CACHE is not None:
        return _COUNTRIES_DB_CACHE
    try:
        url = "https://raw.githubusercontent.com/mledoze/countries/master/dist/countries.json"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            _COUNTRIES_DB_CACHE = r.json()
            return _COUNTRIES_DB_CACHE
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

def fetch_bryophyte_photos(species_name, max_photos=3):

    if not species_name or pd.isna(species_name):
        return []
    sp = str(species_name).strip()
    if not sp:
        return []

    headers = {'User-Agent': 'AnkiCardGen/1.0 (contact: adalb@example.com)'}
    photos = []

    clean_sp = re.sub(r'\(.*?\)', '', sp)
    clean_sp = re.sub(r'\s+(subsp|ssp|var|f|agg)\.?(\s+.*|$)', '', clean_sp, flags=re.IGNORECASE).strip()

    try:
        m_url = f"https://api.gbif.org/v1/species/match?name={urllib.parse.quote(clean_sp)}"
        r_m = requests.get(m_url, headers=headers, timeout=5)
        if r_m.status_code == 200:
            m_data = r_m.json()
            usage_key = m_data.get('usageKey') or m_data.get('speciesKey')
            if usage_key:
                occ_url = f"https://api.gbif.org/v1/occurrence/search?taxonKey={usage_key}&mediaType=StillImage&limit=10"
                r_occ = requests.get(occ_url, headers=headers, timeout=6)
                if r_occ.status_code == 200:
                    occ_res = r_occ.json().get('results', [])
                    for occ in occ_res:
                        media = occ.get('media', [])
                        for m in media:
                            img_url = m.get('identifier')
                            if img_url and img_url.startswith('http'):
                                if not any(p.split('|')[0] == img_url for p in photos):
                                    rights = m.get('rightsHolder') or m.get('creator') or occ.get('recordedBy') or "GBIF / iNaturalist"
                                    lic = m.get('license', '')
                                    lic_clean = lic.split('/')[-2].upper() if '/' in lic else (lic or "CC BY")
                                    photos.append(f"{img_url}|© {rights} ({lic_clean} via GBIF)")
                                    if len(photos) >= max_photos:
                                        break
                        if len(photos) >= max_photos:
                            break
    except Exception:
        pass

    if len(photos) < max_photos:
        wiki_photos = fetch_wikimedia_images(clean_sp, max_photos=(max_photos - len(photos)))
        for wp in wiki_photos:
            if not any(p.split('|')[0] == wp.split('|')[0] for p in photos):
                photos.append(wp)

    return photos[:max_photos]

def fetch_bryophyte_description(species_name):

    return fetch_wiki_description(species_name)

def get_bryophyte_link(species_name):

    if not species_name or pd.isna(species_name):
        return ""
    sp = str(species_name).strip()
    return f"https://bryophyteportal.org/portal/taxa/index.php?taxon={urllib.parse.quote(sp)}"

def fetch_adw_description(species_name, max_chars=800):
\
\
\

    if not species_name or pd.isna(species_name): return ""
    sp_clean = re.sub(r'\s*\(.*\)\s*', '', str(species_name)).strip()
    sp_clean = re.sub(r'\s+sp(p)?\.?$', '', sp_clean).strip()
    words = sp_clean.split()
    if len(words) < 2: return ""
    account_name = f"{words[0].capitalize()}_{words[1].lower()}"
    url = f"https://animaldiversity.org/accounts/{account_name}/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        r = requests.get(url, headers=headers, timeout=6)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            sections = []
            target_headings = ['Physical Description', 'Habitat', 'Food Habits', 'Behavior', 'Reproduction', 'Lifespan']
            for h in soup.find_all(['h2', 'h3', 'h4']):
                htxt = h.get_text(strip=True)
                if any(th.lower() in htxt.lower() for th in target_headings):
                    p = h.find_next_sibling('p')
                    if p:
                        ptxt = p.get_text(strip=True)
                        if ptxt and len(ptxt) > 15:
                            sections.append(f"<b>{htxt}:</b> {ptxt}")
            if sections:
                full_txt = "<br/>".join(sections)
                if len(full_txt) > max_chars:
                    full_txt = full_txt[:max_chars].rsplit(' ', 1)[0] + "..."
                return full_txt
    except Exception:
        pass
    return ""

def get_adw_link(species_name):

    if not species_name or pd.isna(species_name): return ""
    sp_clean = re.sub(r'\s*\(.*\)\s*', '', str(species_name)).strip()
    sp_clean = re.sub(r'\s+sp(p)?\.?$', '', sp_clean).strip()
    words = sp_clean.split()
    if len(words) < 2: return ""
    account_name = f"{words[0].capitalize()}_{words[1].lower()}"
    return f"https://animaldiversity.org/accounts/{account_name}/"

def fetch_gbif_species_description(species_name, max_chars=800):
\
\

    if not species_name or pd.isna(species_name): return ""
    sp_clean = re.sub(r'\s*\(.*\)\s*', '', str(species_name)).strip()
    sp_clean = re.sub(r'\s+sp(p)?\.?$', '', sp_clean).strip()
    try:
        m_url = "https://api.gbif.org/v1/species/match"
        r_m = requests.get(m_url, params={"name": sp_clean, "strict": "true"}, timeout=5)
        if r_m.status_code == 200:
            m_data = r_m.json()
            if m_data.get("matchType") not in ["NONE", "HIGHERRANK"] and m_data.get("rank") not in ["KINGDOM", "PHYLUM", "CLASS"]:
                ukey = m_data.get("usageKey")
                if ukey:
                    d_url = f"https://api.gbif.org/v1/species/{ukey}/descriptions"
                    r_d = requests.get(d_url, timeout=6)
                    if r_d.status_code == 200:
                        results = r_d.json().get("results", [])
                        best_text = ""
                        best_source = ""
                        for item in results:
                            raw_desc = item.get("description", "")
                            if not raw_desc or len(raw_desc) < 30: continue
                            src = item.get("source", "")
                            dtype = str(item.get("type", "")).lower()
                            c_desc = re.sub(r'<[^>]+>', ' ', raw_desc)
                            c_desc = re.sub(r'\s+', ' ', c_desc).strip()
                            if len(c_desc) > len(best_text) or any(k in dtype for k in ['morphology', 'description', 'diagnosis']):
                                best_text = c_desc
                                best_source = src
                                if len(best_text) >= 200:
                                    break
                        if best_text:
                            if len(best_text) > max_chars:
                                best_text = best_text[:max_chars].rsplit(' ', 1)[0] + "..."
                            src_suffix = f" <i>(Zdroj: {best_source[:35]})</i>" if best_source else ""
                            return f"{best_text}{src_suffix}"
    except Exception:
        pass
    return ""

def fetch_powo_kew_description(species_name, max_chars=800):
\
\

    if not species_name or pd.isna(species_name): return ""
    sp_clean = re.sub(r'\s*\(.*\)\s*', '', str(species_name)).strip()
    sp_clean = re.sub(r'\s+sp(p)?\.?$', '', sp_clean).strip()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        s_url = "https://powo.science.kew.org/api/2/search"
        r_s = requests.get(s_url, params={"q": sp_clean}, headers=headers, timeout=5).json()
        results = r_s.get("results", [])
        if results:
            fqid = results[0].get("fqId")
            if fqid:
                t_url = f"https://powo.science.kew.org/api/2/taxon/{fqid}?fields=descriptions"
                r_t = requests.get(t_url, headers=headers, timeout=6).json()
                desc_obj = r_t.get("descriptions", {})
                texts = []
                for src_key, src_val in desc_obj.items():
                    if isinstance(src_val, dict):
                        d_dict = src_val.get("descriptions", {})
                        for h_key, h_list in d_dict.items():
                            if isinstance(h_list, list):
                                for item in h_list:
                                    raw = item.get("description", "")
                                    if raw:
                                        clean = re.sub(r'<[^>]+>', ' ', raw)
                                        clean = re.sub(r'\s+', ' ', clean).strip()
                                        if len(clean) > 30 and clean not in texts:
                                            texts.append(clean)
                if texts:
                    comb = " ".join(texts[:3])
                    if len(comb) > max_chars:
                        comb = comb[:max_chars].rsplit(' ', 1)[0] + "..."
                    return f"{comb} <i>(Zdroj: Royal Botanic Gardens, Kew)</i>"
    except Exception:
        pass
    return ""

def get_powo_kew_link(species_name):

    if not species_name or pd.isna(species_name): return ""
    sp_clean = re.sub(r'\s*\(.*\)\s*', '', str(species_name)).strip()
    sp_clean = re.sub(r'\s+sp(p)?\.?$', '', sp_clean).strip()
    return f"https://powo.science.kew.org/search?q={urllib.parse.quote(sp_clean)}"

def get_eol_link(species_name):

    if not species_name or pd.isna(species_name): return ""
    sp_clean = re.sub(r'\s*\(.*\)\s*', '', str(species_name)).strip()
    sp_clean = re.sub(r'\s+sp(p)?\.?$', '', sp_clean).strip()
    return f"https://eol.org/search?q={urllib.parse.quote(sp_clean)}"

def is_image_col(col_name, sample_val=None):

    col_str = str(col_name).strip()
    col_low = col_str.lower()

    text_indicators = [
        "odkaz", "odka", "popis", "fonetic", "zvuk", "tts", "kategorie", "status",
        "taxonomie", "autorita", "hodnoty", "výskyt", "český název", "cesky nazev",
        "říše", "rise", "kmen", "třída", "trida", "oddělení", "oddeleni",
        "řád", "rad", "čeleď", "celed", "podčeleď", "rod", "druh", "poddruh",
        "synonym", "areál", "areal", "synonyma"
    ]
    if any(k in col_low for k in text_indicators):
        return False
    if col_str.startswith(("[Pladias.cz] Odkaz", "[Pladias] Oddělení", "[Pladias] Třída", "[Pladias] Řád", "[Pladias] Čeleď", "[Pladias] Rod",
                           "[Mykologie.net] Odkaz", "[DaLiBor] Odkaz", "[Mechorosty] Odkaz",
                           "[DiatomBase] Odkaz", "[AlgaeBase] Odkaz", "[ADW] Odkaz", "[POWO Kew] Odkaz", "[EOL] Odkaz",
                           "[ADW] Biologický popis", "[GBIF] Vědecký popis", "[POWO Kew] Popis flóry",
                           "[GBIF] Říše", "[GBIF] Kmen", "[GBIF] Třída", "[GBIF] Řád", "[GBIF] Čeleď", "[GBIF] Rod", "[GBIF] Taxonomie",
                           "[Wikipedie]", "[Klíč 2019]", "[Nepůvodní flóra]", "[Biotopy]", "[Ekologie]", "[Červený seznam]", "[Květena ČR]")):
        return False

    if col_str in ["[Pladias] Mapa rozšíření", "[Pladias.cz] Mapa rozšíření"] or "mapa" in col_low or "mapy" in col_low:
        return True

    img_keywords = [
        'photo', 'foto', 'obrázk', 'obrazk', 'image', 'fotk', 'molekula', 'náhled',
        'květ', 'kvet', 'list', 'herbar', 'herbář', 'vlastní', 'vlastni', 'vlajka',
        'houb', 'hřib', 'zoolog', 'zvíř', 'živoč', 'ptác', 'pták', 'hmyz', 'motýl',
        'habitus', 'plod', 'šišk', 'výtrus', 'spora', 'podzemn'
    ]
    if any(k in col_low for k in img_keywords):
        return True

    if col_str.startswith(("[GBIF] Habitus", "[GBIF] Květ", "[GBIF] List", "[GBIF] Plod", "[GBIF] Herbář",
                           "[GBIF Zoologie] Foto", "[GBIF Houby] Foto", "[iNaturalist] Foto",
                           "[Pladias] Foto", "[Mykologie.net] Foto", "[DaLiBor] Foto",
                           "[Mechorosty] Foto", "[AlgaeBase] Foto", "[DiatomBase] Foto")):
        return True

    if isinstance(sample_val, str):
        first_part = sample_val.split(';')[0].split('|')[0].strip().lower()
        if any(first_part.endswith(x) for x in ['.jpg', '.jpeg', '.png', '.webp', '.gif']): return True
        if first_part.startswith(('http://', 'https://')):
            if any(ext in first_part for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif', 'images', 'upload', 'photos', 'wikimedia']):
                if not any(bad in first_part for bad in ['.mp3', '.wav', '.ogg', 'xeno-canto', 'translate_tts']):
                    return True
    return False

def check_col_is_image(col, df=None):

    sample_val = ""
    if df is not None and not df.empty and col in df.columns:
        try:
            series = df[col].dropna()
            series = series[series.astype(str).str.strip().str.lower().ne("none") & series.astype(str).str.strip().ne("")]
            if not series.empty:
                sample_val = str(series.iloc[0])
        except Exception:
            pass
    return is_image_col(col, sample_val)

def format_img_src_for_html(src_str: str) -> str:

    if not src_str:
        return ""
    src_str = str(src_str).strip()
    if "<img" in src_str:
        m = re.search(r'src=["\']([^"\']+)["\']', src_str)
        if m:
            src_str = m.group(1).strip()
    if src_str.startswith("http://") or src_str.startswith("https://") or src_str.startswith("data:image"):
        return src_str

    clean_p = src_str
    if clean_p.startswith("file:///"):
        clean_p = urllib.parse.unquote(clean_p[8:])
    elif clean_p.startswith("file://"):
        clean_p = urllib.parse.unquote(clean_p[7:])
    local_candidates = [
        clean_p,
        os.path.join(os.path.dirname(os.path.abspath(__file__)), clean_p),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom_media", os.path.basename(clean_p)),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_media", os.path.basename(clean_p)),
        os.path.join("custom_media", os.path.basename(clean_p)),
        os.path.join("test_media", os.path.basename(clean_p))
    ]
    for cand in local_candidates:
        if os.path.isfile(cand):
            try:
                with open(cand, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode("utf-8")
                ext = os.path.splitext(cand)[1].lower().lstrip(".")
                mime = "image/jpeg" if ext in ["jpg", "jpeg"] else f"image/{ext}" if ext else "image/png"
                return f"data:{mime};base64,{b64}"
            except Exception:
                pass
    return src_str

def normalize_match_key(val):

    import re, html
    if not val or pd.isna(val):
        return ""
    txt = str(val).strip()
    txt = html.unescape(txt)
    txt = re.sub(r'<[^>]+>', ' ', txt)
    txt = re.sub(r'\[sound:[^\]]+\]', '', txt)
    txt = re.sub(r'\[\[.*?\]\]', '', txt)
    txt = re.sub(r'\s+', ' ', txt).strip().lower()
    words = txt.split()
    if len(words) >= 2:
        return f"{words[0]} {words[1]}"
    return txt

def unpack_anki_card_fields(note_raw_dict, media_target_dir="custom_media"):
\
\
\
\
\

    import os, re
    from bs4 import BeautifulSoup

    sys_cols = {k: v for k, v in note_raw_dict.items() if k.startswith('_anki_') or k == '[Anki] Štítky'}
    data_cols = {k: v for k, v in note_raw_dict.items() if not k.startswith('_anki_') and k != '[Anki] Štítky'}

    col_names_low = [c.lower() for c in data_cols.keys()]
    if len(data_cols) > 2 and 'front' not in col_names_low and 'back' not in col_names_low:
        return note_raw_dict

    front_val = ""
    back_val = ""
    for k, v in data_cols.items():
        if k.lower() in ['front', 'líc', 'lic', 'otázka', 'otazka']:
            front_val = str(v)
        elif k.lower() in ['back', 'rub', 'odpověď', 'odpoved']:
            back_val = str(v)
        elif not front_val:
            front_val = str(v)
        elif not back_val:
            back_val = str(v)

    if not ('<' in front_val or '<' in back_val or 'card-field' in back_val):
        out_dict = dict(sys_cols)
        first = True
        for k, v in data_cols.items():
            if first and k.lower() in ['front', 'líc']:
                out_dict['Pojem'] = v
            elif k.lower() in ['back', 'rub']:
                out_dict['Popis'] = v
            else:
                out_dict[k] = v
            first = False
        return out_dict

    def _is_copyright_or_attribution(text: str) -> bool:
        if not text:
            return False
        t = str(text).strip()
        t_lower = t.lower()
        if t.startswith('©') or '©' in t:
            return True
        if '(c)' in t_lower or 'copyright' in t_lower:
            return True
        if 'cc by' in t_lower or 'cc-by' in t_lower or 'creative commons' in t_lower:
            return True
        if 'via inaturalist' in t_lower or 'uploaded by' in t_lower or ('inaturalist' in t_lower and ('via' in t_lower or 'by' in t_lower)):
            return True
        if t_lower.startswith(('autor:', 'foto:', 'fotografie:', 'licence:', 'zdroj:')):
            return True
        return False

    unpacked = {}

    soup_front = BeautifulSoup(front_val or "", "html.parser")

    for cap in soup_front.find_all(class_=re.compile(r'(photo-caption|audio-caption|caption)')):
        cap.decompose()
    for small in soup_front.find_all(['small', 'figcaption']):
        if _is_copyright_or_attribution(small.get_text()):
            small.decompose()

    front_imgs = []
    for img in soup_front.find_all('img'):
        src = img.get('src', '').strip()
        if src:
            if media_target_dir and os.path.exists(os.path.join(media_target_dir, src)):
                front_imgs.append(os.path.join(media_target_dir, src).replace('\\', '/'))
            else:
                front_imgs.append(src)
        img.decompose()
    if front_imgs:
        unpacked['Fotografie'] = "; ".join(front_imgs)

    front_text = soup_front.get_text(separator=' ', strip=True)
    if front_text and not _is_copyright_or_attribution(front_text):
        unpacked['Pojem'] = front_text

    soup_back = BeautifulSoup(back_val or "", "html.parser")
    for cap in soup_back.find_all(class_=re.compile(r'(photo-caption|audio-caption|caption)')):
        cap.decompose()
    for small in soup_back.find_all(['small', 'figcaption']):
        if _is_copyright_or_attribution(small.get_text()):
            small.decompose()

    card_fields = soup_back.find_all('div', class_=re.compile(r'card-field'))
    if card_fields:
        for cf in card_fields:
            lbl_el = cf.find(class_=re.compile(r'field-label'))
            val_el = cf.find(class_=re.compile(r'field-value'))
            label_text = lbl_el.get_text(strip=True) if lbl_el else ""

            link_el = cf.find('a')
            if link_el and link_el.get('href'):
                href = link_el['href']
                col_name = label_text or "Odkaz"
                if "mykologie.net" in href: col_name = "[Mykologie.net] Odkaz"
                elif "pladias.cz" in href: col_name = "[Pladias.cz] Odkaz"
                elif "wikipedia.org" in href: col_name = "[Wikipedie] Odkaz"
                elif "inaturalist.org" in href: col_name = "[iNaturalist] Odkaz"
                elif "biolib.cz" in href: col_name = "[BioLib] Odkaz"
                unpacked[col_name] = href
                continue

            back_cf_imgs = []
            for img in cf.find_all('img'):
                src = img.get('src', '').strip()
                if src:
                    if media_target_dir and os.path.exists(os.path.join(media_target_dir, src)):
                        back_cf_imgs.append(os.path.join(media_target_dir, src).replace('\\', '/'))
                    else:
                        back_cf_imgs.append(src)
            if back_cf_imgs:
                img_col = label_text if label_text else "Fotografie"
                if img_col in unpacked:
                    unpacked[img_col] += "; " + "; ".join(back_cf_imgs)
                else:
                    unpacked[img_col] = "; ".join(back_cf_imgs)
                continue

            audio_el = cf.find('audio')
            if audio_el and audio_el.get('src'):
                audio_src = audio_el['src']
                unpacked['[Zvuky] Nahrávka'] = audio_src
                continue

            if val_el:
                val_text = val_el.get_text(separator=' ', strip=True)
                if not _is_copyright_or_attribution(val_text):
                    col_name = label_text or "Popis"
                    unpacked[col_name] = val_text
            elif label_text:
                cf_text = cf.get_text(separator=' ', strip=True)
                val_text = cf_text.replace(label_text, '', 1).strip()
                if not _is_copyright_or_attribution(val_text):
                    unpacked[label_text] = val_text
    else:

        lines = soup_back.get_text(separator='\n').splitlines()
        current_field = "Popis"
        for line in lines:
            line_str = line.strip()
            if not line_str or _is_copyright_or_attribution(line_str): continue
            if ':' in line_str and len(line_str.split(':')[0]) < 30:
                parts = line_str.split(':', 1)
                col_name = parts[0].strip()
                val_text = parts[1].strip()
                if not _is_copyright_or_attribution(val_text):
                    unpacked[col_name] = val_text
                    current_field = col_name
            else:
                if current_field in unpacked:
                    unpacked[current_field] += " " + line_str
                else:
                    unpacked[current_field] = line_str

    is_pojem_bad = (
        'Pojem' not in unpacked
        or not str(unpacked['Pojem']).strip()
        or str(unpacked['Pojem']).strip().startswith('<')
        or _is_copyright_or_attribution(unpacked['Pojem'])
    )

    scientific_keys = [
        'Vědecké jméno', 'Vedecke jmeno', 'Vědecký název', 'Taxon', 'Druh',
        'Latinské jméno', 'Latinský název', 'scientific_name', 'Species'
    ]
    czech_keys = [
        'České jméno', 'Český název', 'ceske_jmeno', 'Czech name'
    ]

    for k in scientific_keys:
        if k in unpacked:
            val_p = unpacked[k]
            if is_pojem_bad:
                if val_p and not _is_copyright_or_attribution(val_p):
                    unpacked['Pojem'] = val_p
                    unpacked.pop(k, None)
                    is_pojem_bad = False
                    break
            else:
                if str(val_p).strip().lower() == str(unpacked.get('Pojem', '')).strip().lower():
                    unpacked.pop(k, None)
                break

    if is_pojem_bad:
        for k in czech_keys:
            if k in unpacked:
                val_p = unpacked[k]
                if val_p and not _is_copyright_or_attribution(val_p):
                    unpacked['Pojem'] = val_p
                    unpacked.pop(k, None)
                    is_pojem_bad = False
                    break

    if 'Pojem' in unpacked and (_is_copyright_or_attribution(unpacked['Pojem']) or not str(unpacked['Pojem']).strip()):
        del unpacked['Pojem']

    final_dict = dict(sys_cols)
    if 'Pojem' in unpacked:
        final_dict['Pojem'] = unpacked.pop('Pojem')
    for k, v in unpacked.items():
        final_dict[k] = v

    return final_dict

def normalize_col_key(s):

    if not s or pd.isna(s):
        return ""
    import unicodedata
    s = str(s).strip().lower()
    s = unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('utf-8')
    s = re.sub(r'\[.*?\]', '', s)
    s = re.sub(r'[^a-z0-9]', '', s)
    return s

SYNONYM_GROUPS = [
    {"pojem", "vedeckejmeno", "taxon", "druh", "latina", "latinsky", "nazev", "species", "scientificname"},
    {"ceskejmeno", "ceskynazev", "cesky", "czechname"},
    {"popis", "poznamky", "poznamka", "charakteristika", "text", "description", "notes", "vlastnipoznamky"},
    {"fotografie", "foto", "fotka", "fotky", "obrazek", "obrazky", "image", "images", "photo", "photos"},
    {"odkaz", "url", "link", "web", "profil"},
    {"celed", "family"},
    {"rad", "order"},
    {"trida", "class"},
    {"kmen", "phylum"},
    {"rise", "kingdom"}
]

def auto_match_columns(table_cols, apkg_cols):
\
\
\
\
\

    mapping = {}
    used_apkg = set()
    clean_apkg = [c for c in apkg_cols if not str(c).startswith('_anki_')]

    for tc in table_cols:
        norm_tc = normalize_col_key(tc)
        if not norm_tc: continue
        for ac in clean_apkg:
            if ac in used_apkg: continue
            norm_ac = normalize_col_key(ac)
            if norm_tc == norm_ac:
                mapping[tc] = ac
                used_apkg.add(ac)
                break

    for tc in table_cols:
        if tc in mapping: continue
        norm_tc = normalize_col_key(tc)
        if not norm_tc: continue

        matched_group = None
        for group in SYNONYM_GROUPS:
            if norm_tc in group:
                matched_group = group
                break

        if matched_group:
            for ac in clean_apkg:
                if ac in used_apkg: continue
                norm_ac = normalize_col_key(ac)
                if norm_ac in matched_group:
                    mapping[tc] = ac
                    used_apkg.add(ac)
                    break

    return mapping

def smart_merge_apkg_and_excel(
    apkg_df,
    table_df,
    col_mapping=None,
    source_priority="table",
    keep_only_table=False
):
\
\
\
\
\
\
\
\
\
\

    if col_mapping is None:
        col_mapping = auto_match_columns(table_df.columns, apkg_df.columns)

    excel_key_col = table_df.columns[0]

    if excel_key_col in col_mapping and col_mapping[excel_key_col] in apkg_df.columns:
        apkg_key_col = col_mapping[excel_key_col]
    elif 'Pojem' in apkg_df.columns:
        apkg_key_col = 'Pojem'
    else:
        non_sys = [c for c in apkg_df.columns if not str(c).startswith('_anki_')]
        apkg_key_col = non_sys[0] if non_sys else apkg_df.columns[0]

    inv_mapping = {ac: tc for tc, ac in col_mapping.items()}

    def is_empty(val):
        return pd.isna(val) or str(val).strip() == "" or str(val).lower() == "nan"

    apkg_map = {}
    for idx, row in apkg_df.iterrows():
        k = normalize_match_key(row.get(apkg_key_col))
        if k and k not in apkg_map:
            apkg_map[k] = row

    matched_count = 0
    matched_keys = set()
    new_rows = []

    for idx, row in table_df.iterrows():
        k = normalize_match_key(row.get(excel_key_col))
        row_dict = row.to_dict()

        if k in apkg_map:
            apkg_row = apkg_map[k]
            matched_keys.add(k)
            matched_count += 1

            row_dict['_anki_guid'] = apkg_row.get('_anki_guid')
            row_dict['_anki_id'] = apkg_row.get('_anki_id')
            row_dict['_anki_mid'] = apkg_row.get('_anki_mid')

            for tc, ac in col_mapping.items():
                if tc in row_dict and ac in apkg_row:
                    t_val = row_dict.get(tc)
                    a_val = apkg_row.get(ac)

                    prio = source_priority.get(tc, "table") if isinstance(source_priority, dict) else source_priority
                    if prio == "anki":

                        if not is_empty(a_val):
                            row_dict[tc] = a_val
                        elif not is_empty(t_val):
                            row_dict[tc] = t_val
                    else:

                        if not is_empty(t_val):
                            row_dict[tc] = t_val
                        elif not is_empty(a_val):
                            row_dict[tc] = a_val

            for ac, av in apkg_row.items():
                if str(ac).startswith('_anki_'): continue
                if ac not in inv_mapping:
                    if ac not in row_dict or is_empty(row_dict[ac]):
                        row_dict[ac] = av

        new_rows.append(row_dict)

    merged_df = pd.DataFrame(new_rows)

    unmatched_apkg_count = 0
    if not keep_only_table:
        extra_apkg_rows = []
        for idx, row in apkg_df.iterrows():
            k = normalize_match_key(row.get(apkg_key_col))
            if k and k not in matched_keys:
                row_dict = {}
                row_dict['_anki_guid'] = row.get('_anki_guid')
                row_dict['_anki_id'] = row.get('_anki_id')
                row_dict['_anki_mid'] = row.get('_anki_mid')

                for tc, ac in col_mapping.items():
                    if ac in row:
                        row_dict[tc] = row.get(ac)

                for ac, av in row.items():
                    if str(ac).startswith('_anki_'): continue
                    if ac not in inv_mapping:
                        row_dict[ac] = av

                for tc in table_df.columns:
                    if tc not in row_dict:
                        row_dict[tc] = ""

                extra_apkg_rows.append(row_dict)
                unmatched_apkg_count += 1

        if extra_apkg_rows:
            extra_df = pd.DataFrame(extra_apkg_rows)
            merged_df = pd.concat([merged_df, extra_df], ignore_index=True)

    return merged_df, matched_count, len(table_df) - matched_count, unmatched_apkg_count

def extract_apkg_to_dataframe(apkg_file_or_bytes, media_target_dir=None):
\
\
\
\
\

    import zipfile, sqlite3, json, tempfile, os, io
    import zstandard as zstd

    if media_target_dir is None:
        media_target_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom_media")
    os.makedirs(media_target_dir, exist_ok=True)

    temp_dir = tempfile.mkdtemp()

    if hasattr(apkg_file_or_bytes, 'read'):
        apkg_path = os.path.join(temp_dir, "temp_uploaded.apkg")
        with open(apkg_path, "wb") as f_out:
            apkg_file_or_bytes.seek(0)
            f_out.write(apkg_file_or_bytes.read())
    elif isinstance(apkg_file_or_bytes, (bytes, bytearray)):
        apkg_path = os.path.join(temp_dir, "temp_uploaded.apkg")
        with open(apkg_path, "wb") as f_out:
            f_out.write(apkg_file_or_bytes)
    else:
        apkg_path = str(apkg_file_or_bytes)

    with zipfile.ZipFile(apkg_path, 'r') as zf:
        file_list = zf.namelist()

        if 'media' in file_list:
            try:
                media_json = zf.read('media').decode('utf-8', errors='ignore')
                media_map = json.loads(media_json)
                for num_key, orig_fname in media_map.items():
                    if num_key in file_list:
                        target_file_path = os.path.join(media_target_dir, orig_fname)
                        with open(target_file_path, "wb") as mf:
                            mf.write(zf.read(num_key))
            except Exception:
                pass

        db_candidates = ['collection.anki21b', 'collection.anki21', 'collection.anki2']
        available_dbs = [c for c in db_candidates if c in file_list]

        if not available_dbs:
            raise ValueError("Soubor balíčku neobsahuje platnou Anki databázi (collection.anki21b / collection.anki2).")

        parsed_notes = []
        deck_name = "Importovaný balíček"

        for candidate in available_dbs:
            raw_db_bytes = zf.read(candidate)
            extracted_db_path = os.path.join(temp_dir, f"extracted_{candidate}.sqlite")

            if raw_db_bytes.startswith(b"\x28\xb5\x2f\xfd"):
                try:
                    dctx = zstd.ZstdDecompressor()
                    with open(extracted_db_path, "wb") as out_f:
                        dctx.copy_stream(io.BytesIO(raw_db_bytes), out_f)
                except Exception as e:
                    continue
            else:
                with open(extracted_db_path, "wb") as out_f:
                    out_f.write(raw_db_bytes)

            try:
                conn = sqlite3.connect(extracted_db_path)
                try:
                    conn.create_collation("unicase", lambda s1, s2: (s1.lower() > s2.lower()) - (s1.lower() < s2.lower()))
                except Exception:
                    pass
                cursor = conn.cursor()

                model_fields_map = {}
                try:
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='fields'")
                    if cursor.fetchone():
                        cursor.execute("SELECT ntid, name FROM fields ORDER BY ntid, ord")
                        for ntid, f_name in cursor.fetchall():
                            model_fields_map.setdefault(ntid, []).append(f_name)
                except Exception:
                    pass

                if not model_fields_map:
                    try:
                        cursor.execute("SELECT models FROM col")
                        col_row = cursor.fetchone()
                        if col_row and col_row[0]:
                            models = json.loads(col_row[0])
                            for mid_str, m_data in models.items():
                                mid = int(mid_str)
                                f_names = [fld['name'] for fld in m_data.get('flds', [])]
                                model_fields_map[mid] = f_names
                    except Exception:
                        pass

                try:
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='decks'")
                    if cursor.fetchone():
                        cursor.execute("SELECT name FROM decks WHERE name != 'Default' LIMIT 1")
                        drow = cursor.fetchone()
                        if drow and drow[0]:
                            deck_name = drow[0]
                except Exception:
                    pass

                if deck_name == "Importovaný balíček":
                    try:
                        cursor.execute("SELECT decks FROM col")
                        deck_row = cursor.fetchone()
                        if deck_row and deck_row[0]:
                            decks = json.loads(deck_row[0])
                            for did_str, d_data in decks.items():
                                if d_data.get('name') and d_data.get('name') != 'Default':
                                    deck_name = d_data.get('name')
                                    break
                    except Exception:
                        pass

                cursor.execute("SELECT id, guid, mid, flds, tags FROM notes")
                notes_rows = cursor.fetchall()

                cand_parsed = []
                for n_id, n_guid, n_mid, flds_str, tags_str in notes_rows:

                    if "aktualizujte na nejnovější verzi Anki" in flds_str or "update to the latest Anki version" in flds_str:
                        continue
                    fld_values = flds_str.split('\x1f')
                    fld_names = model_fields_map.get(n_mid, [f"Pole_{i+1}" for i in range(len(fld_values))])

                    note_row = {
                        '_anki_id': n_id,
                        '_anki_guid': n_guid,
                        '_anki_mid': n_mid
                    }
                    for i, fname in enumerate(fld_names):
                        val = fld_values[i] if i < len(fld_values) else ""
                        note_row[fname] = val
                    if tags_str and tags_str.strip():
                        note_row['[Anki] Štítky'] = tags_str.strip()

                    unpacked_row = unpack_anki_card_fields(note_row, media_target_dir=media_target_dir)
                    cand_parsed.append(unpacked_row)

                conn.close()

                if cand_parsed:
                    parsed_notes = cand_parsed
                    break
            except Exception:
                continue

    if not parsed_notes:
        raise ValueError("Balíček neobsahuje žádné platné karty (nebo obsahuje pouze kompatibilní zástupný text).")

    res_df = pd.DataFrame(parsed_notes)
    return res_df, deck_name

def impose_booklet_pdf(input_pdf_path: str, output_pdf_path: str, sheets_per_signature: int = 0) -> bool:
\
\
\
\
\
\

    try:
        reader = pypdf.PdfReader(input_pdf_path)
        num_orig_pages = len(reader.pages)
        if num_orig_pages == 0:
            return False

        orig_p0 = reader.pages[0]
        p_w = float(orig_p0.mediabox.width)
        p_h = float(orig_p0.mediabox.height)

        sheet_w = 2.0 * p_w
        sheet_h = p_h

        pages_per_sig = sheets_per_signature * 4 if sheets_per_signature > 0 else 0
        all_pages = list(reader.pages)

        writer = pypdf.PdfWriter()

        if pages_per_sig == 0:
            sig_chunks = [all_pages]
        else:
            sig_chunks = []
            for i in range(0, len(all_pages), pages_per_sig):
                sig_chunks.append(all_pages[i:i + pages_per_sig])

        for sig in sig_chunks:

            rem = len(sig) % 4
            if rem != 0:
                pad = 4 - rem
                for _ in range(pad):
                    sig.append(None)

            sig_len = len(sig)
            num_sheets = sig_len // 4

            for s in range(num_sheets):

                left_idx = sig_len - 1 - (s * 2)
                right_idx = s * 2

                back_left_idx = s * 2 + 1
                back_right_idx = sig_len - 2 - (s * 2)

                sheet_front = pypdf.PageObject.create_blank_page(width=sheet_w, height=sheet_h)
                if sig[left_idx] is not None:
                    sheet_front.merge_transformed_page(sig[left_idx], pypdf.Transformation().translate(tx=0, ty=0))
                if sig[right_idx] is not None:
                    sheet_front.merge_transformed_page(sig[right_idx], pypdf.Transformation().translate(tx=p_w, ty=0))
                writer.add_page(sheet_front)

                sheet_back = pypdf.PageObject.create_blank_page(width=sheet_w, height=sheet_h)
                if sig[back_left_idx] is not None:
                    sheet_back.merge_transformed_page(sig[back_left_idx], pypdf.Transformation().translate(tx=0, ty=0))
                if sig[back_right_idx] is not None:
                    sheet_back.merge_transformed_page(sig[back_right_idx], pypdf.Transformation().translate(tx=p_w, ty=0))
                writer.add_page(sheet_back)

        with open(output_pdf_path, "wb") as f_out:
            writer.write(f_out)
        return True
    except Exception:
        return False

class NumberedCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        self.doc_title = kwargs.pop('doc_title', '') if 'doc_title' in kwargs else ''
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        font_name = "CustomSans" if "CustomSans" in pdfmetrics.getRegisteredFontNames() else "Helvetica"
        self.setFont(font_name, 7.5)
        self.setFillColor(colors.HexColor("#64748b"))

        page_w, page_h = self._pagesize
        margin_x = 1.2 * cm if page_w < 16 * cm else 1.8 * cm

        if self._pageNumber > 1:
            header_text = getattr(self, 'doc_title', '') or "Studijní atlas a brožura"
            self.drawString(margin_x, page_h - 1.15 * cm, header_text[:70])
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(margin_x, page_h - 1.3 * cm, page_w - margin_x, page_h - 1.3 * cm)

        footer_text = f"Strana {self._pageNumber} z {page_count}"
        self.drawRightString(page_w - margin_x, 0.85 * cm, footer_text)
        self.drawString(margin_x, 0.85 * cm, "Generátor výukových materiálů a kartiček")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(margin_x, 1.1 * cm, page_w - margin_x, 1.1 * cm)
        self.restoreState()

def html_to_reportlab(html_text: str) -> str:

    if not html_text:
        return ""
    txt = str(html_text)
    txt = txt.replace("<p>", "").replace("</p>", "<br/><br/>")
    txt = txt.replace("<strong>", "<b>").replace("</strong>", "</b>")
    txt = txt.replace("<em>", "<i>").replace("</em>", "</i>")
    txt = txt.replace("<hr>", "<br/>" + "—" * 40 + "<br/>")
    txt = re.sub(r'<a\s+href="([^"]+)"[^>]*>(.*?)</a>', r'<a href="\1" color="#166534"><u>\2</u></a>', txt)
    txt = re.sub(r'<div[^>]*>', '', txt).replace('</div>', '')
    txt = re.sub(r'<span[^>]*>', '', txt).replace('</span>', '')
    txt = re.sub(r'<br\s*/?>', '<br/>', txt)
    return txt.strip()

def create_pdf_qr_drawing(url: str, size: float = 48):

    try:
        if not url or not url.startswith("http"):
            return None
        qr_widget = qr.QrCodeWidget(url.strip())
        b = qr_widget.getBounds()
        w = b[2] - b[0]
        h = b[3] - b[1]
        scale = size / w if w > 0 else 1.0
        d = Drawing(size, size, transform=[scale, 0, 0, scale, 0, 0])
        d.add(qr_widget)
        return d
    except Exception:
        return None

class TrackPage(Flowable):

    def __init__(self, item_id, tracker_dict):
        super().__init__()
        self.item_id = item_id
        self.tracker_dict = tracker_dict
        self.width = 0
        self.height = 0
    def wrap(self, aw, ah):
        return 0, 0
    def draw(self):
        self.tracker_dict[self.item_id] = self.canv._pageNumber

_img_dim_cache = {}

def _get_image_dims(lpath):
    if lpath in _img_dim_cache:
        return _img_dim_cache[lpath]
    try:
        with Image.open(lpath) as im:
            dims = im.size
            _img_dim_cache[lpath] = dims
            return dims
    except Exception:
        return 0, 0

def generate_pdf_booklet(
    df: pd.DataFrame,
    output_pdf_path: str,
    title: str = "Studijní atlas a brožura",
    subtitle: str = "",
    active_cols: list = None,
    layout_mode: str = "compact",
    page_format: str = "A4",
    imposition_mode: str = "Standardní (postupné stránky pro čtení)",
    font_scale: float = 1.0,
    include_toc: bool = True,
    media_dir: str = "",
    media_attributions: dict = None,
    media_tasks: dict = None,
    include_citations: bool = True,
    include_media_attribution: bool = True,
    col_styles: dict = None,
    include_qr_codes: bool = True,
    image_size_mode: str = "Standardní (vyvážená)",
    max_images_mode: str = "Až 6 (doporučeno: 4 fotky + 2 mapy)"
) -> bool:
\
\
\
\
\

    if active_cols is None:
        active_cols = list(df.columns)
    if media_attributions is None:
        media_attributions = {}
    if media_tasks is None:
        media_tasks = {}
    if col_styles is None:
        col_styles = {}

    fn_normal, fn_bold, fn_italic = register_pdf_fonts()

    if page_format == "A5":
        target_pagesize = A5
        margin_x = 1.3 * cm
        margin_top = 1.8 * cm
        margin_bot = 1.6 * cm
        page_h = 21.0 * cm
        available_width = 14.8 * cm - (2 * margin_x)
    else:
        target_pagesize = A4
        margin_x = 1.8 * cm
        margin_top = 2.0 * cm
        margin_bot = 1.8 * cm
        page_h = 29.7 * cm
        available_width = 21.0 * cm - (2 * margin_x)

    avail_page_h = page_h - margin_top - margin_bot

    avail_photo_budget = avail_page_h - 1.8 * cm

    styles = getSampleStyleSheet()
    styles['Normal'].fontName = fn_normal
    styles['BodyText'].fontName = fn_normal
    fs = float(font_scale)
    is_atlas_page = (layout_mode in ["page_per_species", "split_images_text"])

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName=fn_bold,
        fontSize=19 * fs if page_format == "A4" else 15 * fs,
        leading=23 * fs if page_format == "A4" else 18 * fs,
        textColor=colors.HexColor('#1b4332'),
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName=fn_italic,
        fontSize=9 * fs,
        leading=13 * fs,
        textColor=colors.HexColor('#475569'),
        spaceAfter=10
    )

    sp_title_style = ParagraphStyle(
        'SpeciesTitle',
        parent=styles['Normal'],
        fontName=fn_bold,
        fontSize=(14 if is_atlas_page else 12.5) * fs if page_format == "A4" else (12 if is_atlas_page else 11) * fs,
        leading=(17 if is_atlas_page else 15.5) * fs if page_format == "A4" else (15 if is_atlas_page else 13.5) * fs,
        textColor=colors.HexColor('#1b4332'),
        spaceBefore=2,
        spaceAfter=2
    )

    sp_phonetic_style = ParagraphStyle(
        'SpeciesPhonetic',
        parent=styles['Normal'],
        fontName=fn_italic,
        fontSize=9.5 * fs if is_atlas_page else 9 * fs,
        leading=12 * fs if is_atlas_page else 11.5 * fs,
        textColor=colors.HexColor('#2d6a4f'),
        spaceAfter=5 if is_atlas_page else 4
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName=fn_normal,
        fontSize=9 * fs if (is_atlas_page and page_format == "A4") else (8.5 * fs if page_format == "A4" else 7.8 * fs),
        leading=12.5 * fs if (is_atlas_page and page_format == "A4") else (11.5 * fs if page_format == "A4" else 10.5 * fs),
        textColor=colors.HexColor('#1e293b')
    )

    label_style = ParagraphStyle(
        'FieldLabel',
        parent=styles['Normal'],
        fontName=fn_bold,
        fontSize=9 * fs if (is_atlas_page and page_format == "A4") else (8.5 * fs if page_format == "A4" else 7.8 * fs),
        leading=12 * fs if (is_atlas_page and page_format == "A4") else (11 * fs if page_format == "A4" else 10 * fs),
        textColor=colors.HexColor('#334155')
    )

    desc_title_style = ParagraphStyle(
        'DescTitle',
        parent=styles['Normal'],
        fontName=fn_bold,
        fontSize=9.5 * fs if (is_atlas_page and page_format == "A4") else (9.0 * fs if page_format == "A4" else 8.0 * fs),
        leading=12.5 * fs if (is_atlas_page and page_format == "A4") else (11.5 * fs if page_format == "A4" else 10.5 * fs),
        textColor=colors.HexColor('#166534'),
        spaceBefore=4 if is_atlas_page else 3,
        spaceAfter=2
    )

    desc_body_style = ParagraphStyle(
        'DescBody',
        parent=styles['Normal'],
        fontName=fn_normal,
        fontSize=8.5 * fs if (is_atlas_page and page_format == "A4") else (8.0 * fs if page_format == "A4" else 7.5 * fs),
        leading=11.8 * fs if (is_atlas_page and page_format == "A4") else (11.0 * fs if page_format == "A4" else 10.0 * fs),
        textColor=colors.HexColor('#1e293b')
    )

    caption_style = ParagraphStyle(
        'PhotoCaption',
        parent=styles['Normal'],
        fontName=fn_italic,
        fontSize=7 * fs if is_atlas_page else 6.5 * fs,
        leading=9 * fs if is_atlas_page else 8.5 * fs,
        textColor=colors.HexColor('#64748b'),
        alignment=1
    )

    biblio_title_style = ParagraphStyle(
        'BiblioTitle',
        parent=styles['Normal'],
        fontName=fn_bold,
        fontSize=13 * fs,
        leading=16 * fs,
        textColor=colors.HexColor('#1b4332'),
        spaceAfter=6
    )

    biblio_body_style = ParagraphStyle(
        'BiblioBody',
        parent=styles['Normal'],
        fontName=fn_normal,
        fontSize=7.2 * fs,
        leading=9.8 * fs,
        textColor=colors.HexColor('#475569'),
        spaceAfter=3
    )

    def assemble_story(page_tracker=None, is_dummy=False):
        story = []
        clean_title = title.strip() or "Studijní atlas a brožura"
        story.append(Paragraph(clean_title, title_style))

        count_str = f"Počet zpracovaných položek: {len(df)}"
        desc_str = subtitle.strip() if subtitle else "Výukový materiál a studijní atlas vygenerovaný z databáze"
        story.append(Paragraph(f"{desc_str} • {count_str}", subtitle_style))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1b4332"), spaceBefore=0, spaceAfter=8))

        if include_toc and len(df) >= 2:
            story.append(Paragraph("Obsah a rejstřík položek", desc_title_style))
            story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#2d6a4f"), spaceBefore=1, spaceAfter=6))

            toc_items = []
            for idx_t, r_t in df.iterrows():
                item_n = str(r_t.iloc[0]).strip() if len(r_t) > 0 else f"Položka {idx_t+1}"
                cz_n = ""
                if "[Zeměpis] Český název" in r_t and pd.notna(r_t["[Zeměpis] Český název"]):
                    cz_n = f" ({str(r_t['[Zeměpis] Český název']).strip()})"
                elif "[Pladias] České jméno" in r_t and pd.notna(r_t["[Pladias] České jméno"]):
                    cz_n = f" ({str(r_t['[Pladias] České jméno']).strip()})"
                elif "[Taxonomie] Český název" in r_t and pd.notna(r_t["[Taxonomie] Český název"]):
                    cz_n = f" ({str(r_t['[Taxonomie] Český název']).strip()})"

                p_num_str = ""
                if page_tracker and idx_t in page_tracker:
                    p_num_str = f" <font color='#64748b'>— str. {page_tracker[idx_t]}</font>"
                elif is_atlas_page:
                    p_num_str = f" <font color='#64748b'>— str. {idx_t + 2}</font>"

                toc_items.append(f"<b>{idx_t+1}.</b> {item_n}{cz_n}{p_num_str}")

            half = (len(toc_items) + 1) // 2
            toc_col1 = toc_items[:half]
            toc_col2 = toc_items[half:]

            toc_table_rows = []
            for i_row in range(max(len(toc_col1), len(toc_col2))):
                t1 = Paragraph(toc_col1[i_row], body_style) if i_row < len(toc_col1) else Paragraph("", body_style)
                t2 = Paragraph(toc_col2[i_row], body_style) if i_row < len(toc_col2) else Paragraph("", body_style)
                toc_table_rows.append([t1, t2])

            t_toc = Table(toc_table_rows, colWidths=[available_width / 2.0, available_width / 2.0])
            t_toc.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('TOPPADDING', (0,0), (-1,-1), 1.5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
                ('LEFTPADDING', (0,0), (-1,-1), 2),
                ('RIGHTPADDING', (0,0), (-1,-1), 2),
            ]))
            story.append(t_toc)
            story.append(Spacer(1, 8))
            if is_atlas_page:
                story.append(PageBreak())
            else:
                story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#1b4332"), spaceBefore=4, spaceAfter=10))

        for idx, row in df.iterrows():
            species_header = []
            if page_tracker is not None:
                species_header.append(TrackPage(idx, page_tracker))

            primary_name = str(row.iloc[0]).strip() if len(row) > 0 else f"Položka {idx + 1}"
            sp_pronun = ""
            czech_name = ""

            if "[Latina] Fonetická výslovnost" in row and pd.notna(row["[Latina] Fonetická výslovnost"]):
                sp_pronun = str(row["[Latina] Fonetická výslovnost"]).strip()
            if "[Zeměpis] Český název" in row and pd.notna(row["[Zeměpis] Český název"]):
                czech_name = str(row["[Zeměpis] Český název"]).strip()
            elif "[Pladias] České jméno" in row and pd.notna(row["[Pladias] České jméno"]):
                czech_name = str(row["[Pladias] České jméno"]).strip()
            elif "[Taxonomie] Český název" in row and pd.notna(row["[Taxonomie] Český název"]):
                czech_name = str(row["[Taxonomie] Český název"]).strip()

            title_text = f"{idx + 1}. {primary_name}"
            if czech_name and czech_name.lower() not in primary_name.lower():
                title_text += f" ({czech_name})"

            species_header.append(Paragraph(title_text, sp_title_style))
            if sp_pronun:
                species_header.append(Paragraph(sp_pronun, sp_phonetic_style))

            gathered_photos = []
            gathered_maps = []
            for col in active_cols:
                val = row.get(col)
                if pd.isna(val) or str(val).strip() == "":
                    continue
                clean_sp = slugify_species_name(str(row.iloc[0])) if len(row) > 0 else f"druh_{idx}"

                if col in ["[Pladias] Mapa rozšíření", "[Pladias.cz] Mapa rozšíření"]:
                    safe_fn = f"{clean_sp}_pladias_map_{idx}.jpg"
                    lpath = os.path.join(media_dir, safe_fn)
                    if os.path.exists(lpath) and os.path.getsize(lpath) > 0:
                        _w, _h = _get_image_dims(lpath)
                        if _w > 0 and _h > 0 and not any(img[0] == lpath for img in gathered_maps):
                            gathered_maps.append((lpath, "Mapa rozšíření ČR", "Pladias.cz"))

                elif col in ["[iNaturalist] Mapa nálezů", "[iNaturalist] Mapa pozorování", "[iNat] Mapa pozorování"] or ("inat" in str(col).lower() and "map" in str(col).lower()):
                    safe_fn = f"{clean_sp}_inat_map_{idx}.jpg"
                    lpath = os.path.join(media_dir, safe_fn)
                    if os.path.exists(lpath) and os.path.getsize(lpath) > 0:
                        _w, _h = _get_image_dims(lpath)
                        if _w > 0 and _h > 0 and not any(img[0] == lpath for img in gathered_maps):
                            gathered_maps.append((lpath, "Mapa pozorování", "iNaturalist.org"))

                elif col in ["[GBIF] Habitus", "[GBIF] Květ", "[GBIF] List", "[GBIF] Plod", "[GBIF] Herbář"] and is_image_col(col, val):
                    organ_map = {"[GBIF] Habitus": "habitus", "[GBIF] Květ": "kvet", "[GBIF] List": "list", "[GBIF] Plod": "plod", "[GBIF] Herbář": "herbar"}
                    organ = organ_map.get(col, "foto")
                    raw_entries = [u.strip() for u in str(val).split(';') if u.strip()]
                    for u_idx, entry in enumerate(raw_entries):
                        url = entry.split('|', 1)[0].strip()
                        ext = ".jpg"
                        if ".png" in url.lower(): ext = ".png"
                        elif ".jpeg" in url.lower(): ext = ".jpeg"
                        safe_fn = f"{clean_sp}_{organ}{ext}" if u_idx == 0 else f"{clean_sp}_{organ}_{u_idx}{ext}"
                        lpath = os.path.join(media_dir, safe_fn)
                        if os.path.exists(lpath) and os.path.getsize(lpath) > 0:
                            attr = media_attributions.get(safe_fn, "")
                            if not any(img[0] == lpath for img in gathered_photos):
                                gathered_photos.append((lpath, col.replace("[GBIF] ", ""), attr))

                elif is_image_col(col, val):
                    raw_entries = [u.strip() for u in str(val).split(';') if u.strip()]
                    for img_idx, entry in enumerate(raw_entries):
                        if '|' in entry:
                            u_parts = entry.split('|', 1)
                            url = u_parts[0].strip()
                            attr_item = u_parts[1].strip()
                        else:
                            url = entry.strip()
                            attr_item = ""

                        if os.path.isfile(url):
                            lpath = url
                            attr = attr_item or media_attributions.get(url, "")
                            _w, _h = _get_image_dims(lpath)
                            if _w > 0 and _h > 0 and not any(img[0] == lpath for img in gathered_photos):
                                gathered_photos.append((lpath, col, attr))
                        elif url.startswith('http://') or url.startswith('https://'):
                            ext = ".jpg"
                            if ".png" in url.lower(): ext = ".png"
                            elif ".jpeg" in url.lower(): ext = ".jpeg"
                            elif ".webp" in url.lower(): ext = ".webp"
                            safe_col = slugify(col)[:12]
                            url_hash = hashlib.sha256(url.encode('utf-8')).hexdigest()[:6]
                            safe_fn = f"{clean_sp}_{safe_col}_{idx}_{img_idx}_{url_hash}{ext}"
                            lpath = os.path.join(media_dir, safe_fn)
                            if os.path.exists(lpath) and os.path.getsize(lpath) > 0:
                                attr = media_attributions.get(safe_fn, "") or attr_item
                                _w, _h = _get_image_dims(lpath)
                                if _w > 0 and _h > 0 and not any(img[0] == lpath for img in gathered_photos):
                                    gathered_photos.append((lpath, col, attr))

            limit = 6 if "6" in str(max_images_mode) else (2 if "2" in str(max_images_mode) else (1 if "1" in str(max_images_mode) else 4))

            display_imgs = []
            if gathered_maps and limit >= 4:
                num_maps = min(len(gathered_maps), 2)
                num_photos = min(len(gathered_photos), limit - num_maps)
                display_imgs = gathered_photos[:num_photos] + gathered_maps[:num_maps]
                if len(display_imgs) < limit:
                    for p in gathered_photos[num_photos:]:
                        if len(display_imgs) >= limit: break
                        if p not in display_imgs: display_imgs.append(p)
                    for m in gathered_maps[num_maps:]:
                        if len(display_imgs) >= limit: break
                        if m not in display_imgs: display_imgs.append(m)
            elif gathered_maps and limit == 2:
                if gathered_photos:
                    display_imgs = [gathered_photos[0], gathered_maps[0]]
                else:
                    display_imgs = gathered_maps[:2]
            elif gathered_maps and not gathered_photos:
                display_imgs = gathered_maps[:limit]
            else:
                display_imgs = gathered_photos[:limit]

            photo_flowables = []
            if display_imgs:
                num_imgs = len(display_imgs)

                img_scale = 1.0
                if "Velká" in image_size_mode:
                    img_scale = 1.25
                elif "Maximální" in image_size_mode:
                    img_scale = 1.55
                elif "Kompaktní" in image_size_mode or "Menší" in image_size_mode:
                    img_scale = 0.75

                def _make_img_or_spacer(lpath, tw, th):
                    if is_dummy:
                        return Spacer(tw, th)
                    return RLImage(lpath, width=tw, height=th)

                if layout_mode == "split_images_text":

                    if num_imgs == 1:
                        max_h = min(avail_photo_budget - 1.0 * cm, (19.0 * cm if page_format == "A4" else 12.5 * cm) * img_scale)
                        lpath, col_lbl, attr = display_imgs[0]
                        iw, ih = _get_image_dims(lpath)
                        aspect = ih / float(iw) if iw > 0 else 0.75
                        tw = available_width - 0.2 * cm
                        th = tw * aspect
                        if th > max_h:
                            th = max_h
                            tw = th / aspect
                        rl_img = _make_img_or_spacer(lpath, tw, th)
                        cap_text = (attr if include_media_attribution and attr else col_lbl) or ""
                        t_imgs = Table([[rl_img], [Paragraph(cap_text, caption_style)]], colWidths=[available_width])
                        t_imgs.setStyle(TableStyle([
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                            ('TOPPADDING', (0, 0), (-1, -1), 2),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                        ]))
                        photo_flowables.append(t_imgs)

                    elif num_imgs == 2:
                        max_h = min((avail_photo_budget - 2.0 * cm) / 2.0, (10.5 * cm if page_format == "A4" else 6.8 * cm) * img_scale)
                        row_cells = []
                        for lpath, col_lbl, attr in display_imgs:
                            iw, ih = _get_image_dims(lpath)
                            aspect = ih / float(iw) if iw > 0 else 0.75
                            tw = available_width - 0.2 * cm
                            th = tw * aspect
                            if th > max_h:
                                th = max_h
                                tw = th / aspect
                            rl_img = _make_img_or_spacer(lpath, tw, th)
                            cap_text = (attr if include_media_attribution and attr else col_lbl) or ""
                            row_cells.append([rl_img])
                            row_cells.append([Paragraph(cap_text, caption_style)])
                            row_cells.append([Spacer(1, 3)])
                        if row_cells:
                            t_imgs = Table(row_cells, colWidths=[available_width])
                            t_imgs.setStyle(TableStyle([
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                ('TOPPADDING', (0, 0), (-1, -1), 1.5),
                                ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
                            ]))
                            photo_flowables.append(t_imgs)

                    elif num_imgs == 3:
                        rem_h = avail_photo_budget - 2.2 * cm
                        max_h_top = min(rem_h * 0.53, (10.0 * cm if page_format == "A4" else 6.5 * cm) * img_scale)
                        max_h_bot = min(rem_h * 0.43, (8.5 * cm if page_format == "A4" else 5.5 * cm) * img_scale)
                        half_w = available_width / 2.0

                        lpath1, col_lbl1, attr1 = display_imgs[0]
                        iw1, ih1 = _get_image_dims(lpath1)
                        aspect1 = ih1 / float(iw1) if iw1 > 0 else 0.75
                        tw1 = available_width - 0.2 * cm
                        th1 = tw1 * aspect1
                        if th1 > max_h_top:
                            th1 = max_h_top
                            tw1 = th1 / aspect1
                        rl_img1 = _make_img_or_spacer(lpath1, tw1, th1)
                        cap_text1 = (attr1 if include_media_attribution and attr1 else col_lbl1) or ""

                        bot_imgs = []
                        bot_caps = []
                        for lpath, col_lbl, attr in display_imgs[1:]:
                            iw, ih = _get_image_dims(lpath)
                            aspect = ih / float(iw) if iw > 0 else 0.75
                            tw = half_w - 0.2 * cm
                            th = tw * aspect
                            if th > max_h_bot:
                                th = max_h_bot
                                tw = th / aspect
                            bot_imgs.append(_make_img_or_spacer(lpath, tw, th))
                            cap_text = (attr if include_media_attribution and attr else col_lbl) or ""
                            bot_caps.append(Paragraph(cap_text, caption_style))

                        t_grid_data = [
                            [rl_img1, ''],
                            [Paragraph(cap_text1, caption_style), ''],
                            [Spacer(1, 2), ''],
                            [bot_imgs[0], bot_imgs[1]],
                            [bot_caps[0], bot_caps[1]]
                        ]
                        t_imgs = Table(t_grid_data, colWidths=[half_w, half_w])
                        t_imgs.setStyle(TableStyle([
                            ('SPAN', (0, 0), (1, 0)),
                            ('SPAN', (0, 1), (1, 1)),
                            ('SPAN', (0, 2), (1, 2)),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                            ('TOPPADDING', (0, 0), (-1, -1), 1.5),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
                        ]))
                        photo_flowables.append(t_imgs)

                    elif num_imgs == 4:
                        half_w = available_width / 2.0
                        max_h = min((avail_photo_budget - 2.2 * cm) / 2.0, (9.2 * cm if page_format == "A4" else 6.0 * cm) * img_scale)
                        img_objs = []
                        cap_objs = []
                        for lpath, col_lbl, attr in display_imgs:
                            iw, ih = _get_image_dims(lpath)
                            aspect = ih / float(iw) if iw > 0 else 0.75
                            tw = half_w - 0.2 * cm
                            th = tw * aspect
                            if th > max_h:
                                th = max_h
                                tw = th / aspect
                            img_objs.append(_make_img_or_spacer(lpath, tw, th))
                            cap_text = (attr if include_media_attribution and attr else col_lbl) or ""
                            cap_objs.append(Paragraph(cap_text, caption_style))
                        if len(img_objs) == 4:
                            t_grid_data = [
                                [img_objs[0], img_objs[1]],
                                [cap_objs[0], cap_objs[1]],
                                [Spacer(1, 2), Spacer(1, 2)],
                                [img_objs[2], img_objs[3]],
                                [cap_objs[2], cap_objs[3]]
                            ]
                            t_imgs = Table(t_grid_data, colWidths=[half_w, half_w])
                            t_imgs.setStyle(TableStyle([
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                ('TOPPADDING', (0, 0), (-1, -1), 1.5),
                                ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
                            ]))
                            photo_flowables.append(t_imgs)

                    elif num_imgs in (5, 6):
                        half_w = available_width / 2.0
                        max_h = min((avail_photo_budget - 2.8 * cm) / 3.0, (5.8 * cm if page_format == "A4" else 3.8 * cm) * img_scale)
                        img_objs = []
                        cap_objs = []
                        for lpath, col_lbl, attr in display_imgs:
                            iw, ih = _get_image_dims(lpath)
                            aspect = ih / float(iw) if iw > 0 else 0.75
                            tw = half_w - 0.2 * cm
                            th = tw * aspect
                            if th > max_h:
                                th = max_h
                                tw = th / aspect
                            img_objs.append(_make_img_or_spacer(lpath, tw, th))
                            cap_text = (attr if include_media_attribution and attr else col_lbl) or ""
                            cap_objs.append(Paragraph(cap_text, caption_style))
                        if len(img_objs) == 5:
                            img_objs.append(Spacer(half_w - 0.2 * cm, 1))
                            cap_objs.append(Paragraph("", caption_style))
                        t_grid_data = [
                            [img_objs[0], img_objs[1]],
                            [cap_objs[0], cap_objs[1]],
                            [Spacer(1, 1.5), Spacer(1, 1.5)],
                            [img_objs[2], img_objs[3]],
                            [cap_objs[2], cap_objs[3]],
                            [Spacer(1, 1.5), Spacer(1, 1.5)],
                            [img_objs[4], img_objs[5]],
                            [cap_objs[4], cap_objs[5]]
                        ]
                        t_imgs = Table(t_grid_data, colWidths=[half_w, half_w])
                        t_imgs.setStyle(TableStyle([
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                            ('TOPPADDING', (0, 0), (-1, -1), 1.0),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 1.0),
                        ]))
                        photo_flowables.append(t_imgs)

                elif is_atlas_page and num_imgs in (5, 6):
                    grid_w = available_width / 2.0
                    cell_w = grid_w - 0.3 * cm
                    max_img_h = min(avail_photo_budget * 0.40 / 3.0, (3.8 * cm if page_format == "A4" else 2.6 * cm) * img_scale)
                    img_objs = []
                    cap_objs = []
                    for lpath, col_lbl, attr in display_imgs:
                        iw, ih = _get_image_dims(lpath)
                        aspect = ih / float(iw) if iw > 0 else 0.75
                        t_w = cell_w
                        t_h = t_w * aspect
                        if t_h > max_img_h:
                            t_h = max_img_h
                            t_w = t_h / aspect
                        img_objs.append(_make_img_or_spacer(lpath, t_w, t_h))
                        cap_text = (attr if include_media_attribution and attr else col_lbl) or ""
                        cap_objs.append(Paragraph(cap_text, caption_style))
                    if len(img_objs) == 5:
                        img_objs.append(Spacer(cell_w, 1))
                        cap_objs.append(Paragraph("", caption_style))
                    t_grid_data = [
                        [img_objs[0], img_objs[1]],
                        [cap_objs[0], cap_objs[1]],
                        [img_objs[2], img_objs[3]],
                        [cap_objs[2], cap_objs[3]],
                        [img_objs[4], img_objs[5]],
                        [cap_objs[4], cap_objs[5]]
                    ]
                    t_imgs = Table(t_grid_data, colWidths=[grid_w, grid_w])
                    t_imgs.setStyle(TableStyle([
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('TOPPADDING', (0, 0), (-1, -1), 1),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
                    ]))
                    photo_flowables.append(t_imgs)
                    photo_flowables.append(Spacer(1, 3))
                elif is_atlas_page and num_imgs == 4:
                    grid_w = available_width / 2.0
                    cell_w = grid_w - 0.3 * cm
                    max_img_h = min(avail_photo_budget * 0.45, (6.0 * cm if page_format == "A4" else 4.2 * cm) * img_scale)
                    img_objs = []
                    cap_objs = []
                    for lpath, col_lbl, attr in display_imgs:
                        iw, ih = _get_image_dims(lpath)
                        aspect = ih / float(iw) if iw > 0 else 0.75
                        t_w = cell_w
                        t_h = t_w * aspect
                        if t_h > max_img_h:
                            t_h = max_img_h
                            t_w = t_h / aspect
                        img_objs.append(_make_img_or_spacer(lpath, t_w, t_h))
                        cap_text = (attr if include_media_attribution and attr else col_lbl) or ""
                        cap_objs.append(Paragraph(cap_text, caption_style))
                    if len(img_objs) == 4:
                        t_grid_data = [
                            [img_objs[0], img_objs[1]],
                            [cap_objs[0], cap_objs[1]],
                            [img_objs[2], img_objs[3]],
                            [cap_objs[2], cap_objs[3]]
                        ]
                        t_imgs = Table(t_grid_data, colWidths=[grid_w, grid_w])
                        t_imgs.setStyle(TableStyle([
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                            ('TOPPADDING', (0, 0), (-1, -1), 2),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                        ]))
                        photo_flowables.append(t_imgs)
                        photo_flowables.append(Spacer(1, 4))
                else:

                    if is_atlas_page:
                        if page_format == "A5":
                            max_img_h = (8.0 * cm if num_imgs == 1 else (6.0 * cm if num_imgs == 2 else 4.5 * cm)) * img_scale
                        else:
                            max_img_h = (11.0 * cm if num_imgs == 1 else (8.5 * cm if num_imgs == 2 else (7.0 * cm if num_imgs == 3 else 5.5 * cm))) * img_scale

                        max_img_h = min(avail_photo_budget * 0.45, max_img_h)
                    else:
                        if page_format == "A5":
                            max_img_h = (4.8 * cm if num_imgs <= 2 else (3.8 * cm if num_imgs == 3 else 3.0 * cm)) * img_scale
                        else:
                            max_img_h = (6.4 * cm if num_imgs <= 2 else (5.2 * cm if num_imgs == 3 else 4.2 * cm)) * img_scale

                    cell_width = available_width / float(num_imgs)
                    img_cells = []
                    caption_cells = []
                    for lpath, col_lbl, attr in display_imgs:
                        iw, ih = _get_image_dims(lpath)
                        if iw <= 0 or ih <= 0:
                            continue
                        aspect = ih / float(iw)
                        target_w = cell_width - 0.3 * cm
                        target_h = target_w * aspect
                        if target_h > max_img_h:
                            target_h = max_img_h
                            target_w = target_h / aspect
                        img_cells.append(_make_img_or_spacer(lpath, target_w, target_h))
                        cap_text = (attr if include_media_attribution and attr else col_lbl) or ""
                        caption_cells.append(Paragraph(cap_text, caption_style))
                    if img_cells:
                        actual_num = len(img_cells)
                        actual_cell_w = available_width / float(actual_num)
                        t_imgs = Table([img_cells, caption_cells], colWidths=[actual_cell_w] * actual_num)
                        t_imgs.setStyle(TableStyle([
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                            ('TOPPADDING', (0, 0), (-1, -1), 2),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
                            ('LEFTPADDING', (0, 0), (-1, -1), 2),
                            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
                        ]))
                        photo_flowables.append(t_imgs)
                        photo_flowables.append(Spacer(1, 4))

            short_props = []
            long_descriptions = []
            links = []
            raw_links_data = []

            for col in active_cols:
                val = row.get(col)
                if pd.isna(val) or str(val).strip() == "" or str(val).lower() == "nan":
                    continue
                if is_image_col(col, val):
                    continue
                if str(col).startswith("[TTS]") or col == "[Zvuky] Hlasy ptáků" or col == "[Latina] Fonetická výslovnost":
                    continue
                if col == df.columns[0] and str(val).strip() == primary_name:
                    continue

                val_str = str(val).strip()
                col_cfg = col_styles.get(col, {}) if col_styles else {}
                custom_lbl = col_cfg.get("custom_label", "").strip() or col_cfg.get("label", "").strip() or col
                display_mode = col_cfg.get("display", "auto")
                text_style = col_cfg.get("style", "normal")

                if val_str.startswith("http://") or val_str.startswith("https://"):
                    link_label = custom_lbl if custom_lbl != col else "Odkaz"
                    if "pladias.cz" in val_str: link_label = "Pladias.cz (profil taxonu)"
                    elif "inaturalist.org" in val_str: link_label = "iNaturalist (mapa pozorování)"
                    elif "mushroomcoloratlas.com" in val_str: link_label = "Mushroom Color Atlas (pigmenty)"
                    elif "mykologie.net" in val_str: link_label = "Mykologie.net (profil)"
                    elif "dalib.cz" in val_str: link_label = "DaLiBor (atlas lišejníků)"
                    elif "diatombase.org" in val_str: link_label = "DiatomBase (WoRMS)"
                    elif "algaebase.org" in val_str: link_label = "AlgaeBase"
                    elif "wikipedia.org" in val_str: link_label = "Wikipedie"
                    links.append(f'<a href="{val_str}" color="#166534"><u>{link_label}</u></a>')
                    raw_links_data.append((val_str, link_label))
                    continue

                clean_val = html_to_reportlab(val_str)

                if text_style == "bold" or col_cfg.get("bold"):
                    clean_val = f"<b>{clean_val}</b>"
                elif text_style == "italic" or col_cfg.get("italic"):
                    clean_val = f"<i>{clean_val}</i>"
                elif text_style == "bold_italic":
                    clean_val = f"<b><i>{clean_val}</i></b>"

                is_known_desc = col in [
                    "[Květena ČR] Popis", "[Popis] Vědecký popis (Wikipedia)", "[Mykologie.net] Popis", "[DaLiBor] Popis",
                    "[ADW] Biologický popis", "[GBIF] Vědecký popis", "[POWO Kew] Popis flóry", "[Mechorosty] Popis"
                ]

                if display_mode == "table":
                    short_props.append((custom_lbl, clean_val))
                elif display_mode == "text":
                    long_descriptions.append((custom_lbl, clean_val))
                else:
                    if is_known_desc or len(val_str) > 120:
                        long_descriptions.append((custom_lbl, clean_val))
                    else:
                        short_props.append((custom_lbl, clean_val))

            property_flowables = []
            if short_props:
                kv_table_rows = []
                lbl_w = available_width * 0.28
                val_w = available_width * 0.72
                for lbl, v in short_props:
                    kv_table_rows.append([
                        Paragraph(f"<b>{lbl}:</b>", label_style),
                        Paragraph(v, body_style)
                    ])
                t_kv = Table(kv_table_rows, colWidths=[lbl_w, val_w])
                pad_v = 2.2 if is_atlas_page else 2.0
                t_kv.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('TOPPADDING', (0, 0), (-1, -1), pad_v),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), pad_v),
                    ('LEFTPADDING', (0, 0), (-1, -1), 3),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 3),
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
                    ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
                    ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#f1f5f9')),
                ]))
                property_flowables.append(t_kv)
                property_flowables.append(Spacer(1, 4))

            description_flowables = []
            for d_lbl, d_text in long_descriptions:
                description_flowables.append(Paragraph(d_lbl, desc_title_style))
                description_flowables.append(Paragraph(d_text, desc_body_style))
                description_flowables.append(Spacer(1, 3))

            media_flowables = []
            sound_col_val = row.get("[Zvuky] Hlasy ptáků")
            if sound_col_val and pd.notna(sound_col_val) and str(sound_col_val).strip():
                sound_entries = [e.strip() for e in str(sound_col_val).split(';') if e.strip()]
                for s_entry in sound_entries:
                    parts = s_entry.split('|')
                    s_url = parts[0].strip()
                    s_type = parts[1].strip() if len(parts) > 1 else "song"
                    s_attr = parts[2].strip() if len(parts) > 2 else ""
                    if s_url.startswith('http'):
                        qr_size_snd = 32 if is_atlas_page else 40
                        qr_d = create_pdf_qr_drawing(s_url, size=qr_size_snd) if include_qr_codes else None
                        t_lbl = "Zpěv" if s_type == "song" else "Hlas"
                        attr_sub = f'<br/><font size="6.5" color="#64748b">Autor nahrávky: {s_attr}</font>' if (include_media_attribution and s_attr) else ""
                        if include_qr_codes and qr_d:
                            desc_p = Paragraph(f'<b>Poslechnout nahrávku ({t_lbl}) – QR kód:</b><br/><font size="7.0" color="#166534"><a href="{s_url}">{s_url[:42]}...</a></font>{attr_sub}', body_style)
                            snd_w = (qr_size_snd / 28.35) * cm + 0.4 * cm
                            t_snd = Table([[qr_d, desc_p]], colWidths=[snd_w, available_width - snd_w])
                            t_snd.setStyle(TableStyle([
                                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
                                ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
                                ('TOPPADDING', (0,0), (-1,-1), 2),
                                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                                ('LEFTPADDING', (0,0), (-1,-1), 4),
                                ('RIGHTPADDING', (0,0), (-1,-1), 4),
                            ]))
                            media_flowables.append(t_snd)
                            media_flowables.append(Spacer(1, 3))
                        else:
                            desc_p = Paragraph(f'<b>Nahrávka ({t_lbl}):</b> <font size="7.5" color="#166534"><a href="{s_url}">{s_url}</a></font>{attr_sub}', body_style)
                            media_flowables.append(desc_p)
                            media_flowables.append(Spacer(1, 3))

            if include_qr_codes and raw_links_data:
                qr_link_cells = []
                qr_sz = 28 if is_atlas_page else 36
                for l_url, l_name in raw_links_data:
                    l_qr = create_pdf_qr_drawing(l_url, size=qr_sz)
                    action_txt = "Otevřít mapu" if "inaturalist.org" in l_url else "Otevřít odkaz"
                    l_p = Paragraph(f'<b>{l_name}</b><br/><font size="6.5" color="#166534"><a href="{l_url}">{action_txt} &rarr;</a></font>', body_style)
                    if l_qr:
                        qr_link_cells.append([l_qr, l_p])
                    else:
                        qr_link_cells.append(["", l_p])

                if qr_link_cells:
                    grid_rows = []
                    for idx_k in range(0, len(qr_link_cells), 2):
                        pair = qr_link_cells[idx_k:idx_k+2]
                        if len(pair) == 2:
                            grid_rows.append([pair[0][0], pair[0][1], pair[1][0], pair[1][1]])
                        else:
                            grid_rows.append([pair[0][0], pair[0][1], "", ""])
                    half_w = available_width / 2.0
                    qr_w = (qr_sz / 28.35) * cm + 0.3 * cm
                    desc_w = half_w - qr_w
                    t_links_grid = Table(grid_rows, colWidths=[qr_w, desc_w, qr_w, desc_w])
                    t_links_grid.setStyle(TableStyle([
                        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                        ('TOPPADDING', (0,0), (-1,-1), 1.5),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
                        ('LEFTPADDING', (0,0), (-1,-1), 2),
                        ('RIGHTPADDING', (0,0), (-1,-1), 2),
                    ]))
                    media_flowables.append(Paragraph("<b>Interaktivní odkazy (QR kódy):</b>", label_style))
                    media_flowables.append(t_links_grid)
                    media_flowables.append(Spacer(1, 3))
            elif links:
                links_html = " • ".join(links)
                media_flowables.append(Paragraph(f"<b>Odkazy:</b> {links_html}", body_style))
                media_flowables.append(Spacer(1, 3))

            if layout_mode == "split_images_text":

                story.extend(species_header)
                if photo_flowables:
                    story.extend(photo_flowables)
                else:
                    story.append(Paragraph("<font color='#64748b'><i>Pro tento taxon není k dispozici žádná fotografie.</i></font>", body_style))
                story.append(PageBreak())

                story.append(Paragraph(f"{title_text} – Popis a vlastnosti", sp_title_style))
                story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#1b4332"), spaceBefore=1, spaceAfter=5))
                if property_flowables:
                    story.extend(property_flowables)
                if description_flowables:
                    story.extend(description_flowables)
                if media_flowables:
                    story.extend(media_flowables)
                if idx < len(df) - 1:
                    story.append(PageBreak())

            elif is_atlas_page:

                story.extend(species_header)
                if photo_flowables:
                    story.extend(photo_flowables)
                if property_flowables:
                    story.extend(property_flowables)
                if description_flowables:
                    story.extend(description_flowables)
                if media_flowables:
                    story.extend(media_flowables)
                if idx < len(df) - 1:
                    story.append(PageBreak())

            else:

                c_items = species_header + photo_flowables + property_flowables + description_flowables + media_flowables
                if len(c_items) > 2:
                    story.append(KeepTogether(c_items[:2]))
                    story.extend(c_items[2:])
                else:
                    story.extend(c_items)
                if idx < len(df) - 1:
                    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceBefore=4, spaceAfter=6))

        if include_citations:
            story.append(PageBreak())
            story.append(Paragraph("Použitá literatura, zdroje dat a licence", biblio_title_style))
            story.append(HRFlowable(width="100%", thickness=1.0, color=colors.HexColor("#2d6a4f"), spaceBefore=2, spaceAfter=6))

            citations_data = [
                ("Pladias.cz", "Pladias.cz – Databáze české flóry a vegetace. Botanický ústav AV ČR, Průhonice. (pladias.cz)"),
                ("Klíč 2019", "Kaplan Z. et al. (2019): Klíč ke květeně České republiky. Academia, Praha, 1168 s."),
                ("Červený seznam ČR", "Grulich V. (2012): Red List of vascular plants of the Czech Republic: 3rd edition. Preslia 84: 631–645."),
                ("iNaturalist", "iNaturalist Community. Observation data & photos licensed under Creative Commons. (inaturalist.org)"),
                ("Mushroom Color Atlas", "Beeler J. (2024): The Mushroom Color Atlas – A Guide to Dyes and Pigments Made from Fungi. (mushroomcoloratlas.com)"),
                ("Mykologie.net", "Česká mykologická společnost a portál Mykologie.net."),
                ("GBIF", "Global Biodiversity Information Facility (GBIF.org) Backbone Taxonomy & Occurrences."),
                ("Wikimedia Commons", "Multimediální repozitář Wikimedia Foundation pod volnými licencemi Creative Commons.")
            ]
            for src_title, src_text in citations_data:
                story.append(Paragraph(f"<b>{src_title}:</b> {src_text}", biblio_body_style))

        return story

    def _canvas_factory(filename, **kwargs):
        c = NumberedCanvas(filename, **kwargs)
        c.doc_title = title.strip() or "Studijní atlas a brožura"
        return c

    page_tracker = {}
    if include_toc and len(df) >= 2:
        if is_atlas_page:
            n_items = len(df)
            if n_items <= 80:
                toc_pages = 1
            else:
                toc_pages = 1 + math.ceil((n_items - 80) / 90)
            pages_per_species = 2 if layout_mode == "split_images_text" else 1
            for idx_t in range(n_items):
                page_tracker[idx_t] = 1 + toc_pages + (idx_t * pages_per_species)
        else:
            try:
                pre_story = assemble_story(page_tracker=page_tracker, is_dummy=True)
                dummy_buf = io.BytesIO()
                doc_dummy = SimpleDocTemplate(
                    dummy_buf,
                    pagesize=target_pagesize,
                    leftMargin=margin_x,
                    rightMargin=margin_x,
                    topMargin=margin_top,
                    bottomMargin=margin_bot
                )
                doc_dummy.build(pre_story, canvasmaker=_canvas_factory)
            except Exception:
                page_tracker = {}

    story = assemble_story(page_tracker=page_tracker, is_dummy=False)

    is_imposition = "Standardní" not in imposition_mode
    if is_imposition:
        temp_single_path = output_pdf_path.replace(".pdf", "_raw_pages.pdf")
        doc_raw = SimpleDocTemplate(
            temp_single_path,
            pagesize=target_pagesize,
            leftMargin=margin_x,
            rightMargin=margin_x,
            topMargin=margin_top,
            bottomMargin=margin_bot
        )
        doc_raw.build(story, canvasmaker=_canvas_factory)

        sheets_sig = 0
        if "6 listů" in imposition_mode:
            sheets_sig = 6
        elif "8 listů" in imposition_mode:
            sheets_sig = 8

        ok = impose_booklet_pdf(temp_single_path, output_pdf_path, sheets_per_signature=sheets_sig)
        if not ok or not os.path.exists(output_pdf_path) or os.path.getsize(output_pdf_path) == 0:
            shutil.copy2(temp_single_path, output_pdf_path)
        try:
            if os.path.exists(temp_single_path):
                os.remove(temp_single_path)
        except Exception:
            pass
    else:
        doc = SimpleDocTemplate(
            output_pdf_path,
            pagesize=target_pagesize,
            leftMargin=margin_x,
            rightMargin=margin_x,
            topMargin=margin_top,
            bottomMargin=margin_bot
        )
        doc.build(story, canvasmaker=_canvas_factory)

    return True

def generate_docx_booklet(
    df: pd.DataFrame,
    output_docx_path: str,
    title: str = "Studijní atlas a brožura",
    subtitle: str = "",
    active_cols: list = None,
    layout_mode: str = "page_per_species",
    include_toc: bool = True,
    media_dir: str = "",
    media_attributions: dict = None,
    include_citations: bool = True,
    include_media_attribution: bool = True,
    col_styles: dict = None
) -> bool:
\
\
\
\

    import docx
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT

    if active_cols is None:
        active_cols = list(df.columns)
    if media_attributions is None:
        media_attributions = {}
    if col_styles is None:
        col_styles = {}

    doc = docx.Document()

    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    clean_title = title.strip() or "Studijní atlas a brožura"
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_after = Pt(2)
    r_title = p_title.add_run(clean_title)
    r_title.bold = True
    r_title.font.size = Pt(22)
    r_title.font.color.rgb = RGBColor(27, 67, 50)

    desc_str = subtitle.strip() if subtitle else "Výukový materiál a studijní atlas vygenerovaný z databáze"
    count_str = f"Počet zpracovaných položek: {len(df)}"
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(14)
    r_sub = p_sub.add_run(f"{desc_str} • {count_str}")
    r_sub.italic = True
    r_sub.font.size = Pt(10)
    r_sub.font.color.rgb = RGBColor(71, 85, 105)

    if include_toc and len(df) >= 2:
        p_toc_head = doc.add_paragraph()
        p_toc_head.paragraph_format.space_before = Pt(8)
        p_toc_head.paragraph_format.space_after = Pt(4)
        r_toc_h = p_toc_head.add_run("Obsah a rejstřík položek")
        r_toc_h.bold = True
        r_toc_h.font.size = Pt(13)
        r_toc_h.font.color.rgb = RGBColor(33, 106, 64)

        toc_items = []
        for idx_t, r_t in df.iterrows():
            item_n = str(r_t.iloc[0]).strip() if len(r_t) > 0 else f"Položka {idx_t+1}"
            cz_n = ""
            if "[Zeměpis] Český název" in r_t and pd.notna(r_t["[Zeměpis] Český název"]):
                cz_n = f" ({str(r_t['[Zeměpis] Český název']).strip()})"
            elif "[Taxonomie] Český název" in r_t and pd.notna(r_t["[Taxonomie] Český název"]):
                cz_n = f" ({str(r_t['[Taxonomie] Český název']).strip()})"
            toc_items.append(f"{idx_t+1}. {item_n}{cz_n}")

        half = (len(toc_items) + 1) // 2
        col1_items = toc_items[:half]
        col2_items = toc_items[half:]

        table_toc = doc.add_table(rows=max(len(col1_items), len(col2_items)), cols=2)
        table_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
        table_toc.autofit = True

        for r_idx in range(len(table_toc.rows)):
            row_cells = table_toc.rows[r_idx].cells
            if r_idx < len(col1_items):
                p1 = row_cells[0].paragraphs[0]
                p1.paragraph_format.space_after = Pt(2)
                p1.paragraph_format.space_before = Pt(2)
                r1 = p1.add_run(col1_items[r_idx])
                r1.font.size = Pt(9.5)
            if r_idx < len(col2_items):
                p2 = row_cells[1].paragraphs[0]
                p2.paragraph_format.space_after = Pt(2)
                p2.paragraph_format.space_before = Pt(2)
                r2 = p2.add_run(col2_items[r_idx])
                r2.font.size = Pt(9.5)

        if layout_mode == "page_per_species":
            doc.add_page_break()
        else:
            p_div = doc.add_paragraph()
            p_div.paragraph_format.space_after = Pt(12)

    for idx, row in df.iterrows():
        primary_name = str(row.iloc[0]).strip() if len(row) > 0 else f"Položka {idx + 1}"
        sp_pronun = ""
        czech_name = ""
        if "[Latina] Fonetická výslovnost" in row and pd.notna(row["[Latina] Fonetická výslovnost"]):
            sp_pronun = str(row["[Latina] Fonetická výslovnost"]).strip()
        if "[Zeměpis] Český název" in row and pd.notna(row["[Zeměpis] Český název"]):
            czech_name = str(row["[Zeměpis] Český název"]).strip()
        elif "[Taxonomie] Český název" in row and pd.notna(row["[Taxonomie] Český název"]):
            czech_name = str(row["[Taxonomie] Český název"]).strip()

        title_text = f"{idx + 1}. {primary_name}"
        if czech_name and czech_name.lower() not in primary_name.lower():
            title_text += f" ({czech_name})"

        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(8)
        p_sp.paragraph_format.space_after = Pt(2)
        r_sp = p_sp.add_run(title_text)
        r_sp.bold = True
        r_sp.font.size = Pt(15)
        r_sp.font.color.rgb = RGBColor(27, 67, 50)

        if sp_pronun:
            p_pr = doc.add_paragraph()
            p_pr.paragraph_format.space_after = Pt(6)
            r_pr = p_pr.add_run(sp_pronun)
            r_pr.italic = True
            r_pr.font.size = Pt(10)
            r_pr.font.color.rgb = RGBColor(45, 106, 79)

        found_images = []
        for col in active_cols:
            val = row.get(col)
            if pd.isna(val) or str(val).strip() == "":
                continue
            val_s = str(val).strip()
            if is_image_col(col, val):
                raw_entries = [u.strip() for u in val_s.split(';') if u.strip()]
                clean_sp = slugify_species_name(str(row.iloc[0])) if len(row) > 0 else f"druh_{idx}"
                for img_idx, entry in enumerate(raw_entries):
                    u = entry.split('|', 1)[0].strip()
                    attr_txt = entry.split('|', 1)[1].strip() if '|' in entry else ""
                    if os.path.isfile(u):
                        found_images.append((u, col, attr_txt))
                    elif media_dir and os.path.isdir(media_dir):
                        for f_cand in os.listdir(media_dir):
                            if clean_sp.lower() in f_cand.lower() and os.path.isfile(os.path.join(media_dir, f_cand)):
                                found_images.append((os.path.join(media_dir, f_cand), col, attr_txt))
                                break

        if found_images:
            display_imgs = found_images[:4]
            num = len(display_imgs)
            if num == 1:
                p_im = doc.add_paragraph()
                p_im.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_im.paragraph_format.space_after = Pt(2)
                try:
                    p_im.add_run().add_picture(display_imgs[0][0], width=Inches(4.8))
                    if include_media_attribution and display_imgs[0][2]:
                        p_cap = doc.add_paragraph()
                        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        p_cap.paragraph_format.space_after = Pt(6)
                        r_c = p_cap.add_run(display_imgs[0][2])
                        r_c.font.size = Pt(8)
                        r_c.font.color.rgb = RGBColor(100, 116, 139)
                except Exception:
                    pass
            elif num == 2:
                t_img = doc.add_table(rows=1, cols=2)
                t_img.alignment = WD_TABLE_ALIGNMENT.CENTER
                for ci, (lp, cl, at) in enumerate(display_imgs):
                    c_p = t_img.rows[0].cells[ci].paragraphs[0]
                    c_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    c_p.paragraph_format.space_after = Pt(2)
                    try:
                        c_p.add_run().add_picture(lp, width=Inches(2.8))
                        if include_media_attribution and at:
                            r_c = c_p.add_run(f"\n{at}")
                            r_c.font.size = Pt(8)
                            r_c.font.color.rgb = RGBColor(100, 116, 139)
                    except Exception:
                        pass
            elif num >= 3:
                rows_count = 2 if num == 4 else 1
                cols_count = 2 if num == 4 else 3
                t_img = doc.add_table(rows=rows_count, cols=cols_count)
                t_img.alignment = WD_TABLE_ALIGNMENT.CENTER
                img_flat = t_img.rows[0].cells + (t_img.rows[1].cells if rows_count == 2 else [])
                for ci, (lp, cl, at) in enumerate(display_imgs):
                    if ci < len(img_flat):
                        c_p = img_flat[ci].paragraphs[0]
                        c_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        c_p.paragraph_format.space_after = Pt(2)
                        try:
                            c_p.add_run().add_picture(lp, width=Inches(2.6 if cols_count == 2 else 1.9))
                            if include_media_attribution and at:
                                r_c = c_p.add_run(f"\n{at}")
                                r_c.font.size = Pt(7.5)
                                r_c.font.color.rgb = RGBColor(100, 116, 139)
                        except Exception:
                            pass

        short_props = []
        long_descriptions = []
        links = []

        for col in active_cols:
            val = row.get(col)
            if pd.isna(val) or str(val).strip() == "":
                continue
            val_s = str(val).strip()
            if col == df.columns[0] and val_s == primary_name:
                continue
            if col.startswith(("[TTS]", "[Zvuky]", "[Latina] Fonetická")):
                continue
            lbl = col_styles.get(col, {}).get("custom_label", col) if col in col_styles else col

            if val_s.startswith("http://") or val_s.startswith("https://"):
                links.append((lbl, val_s))
            elif len(val_s) > 120 or "popis" in col.lower():
                clean_desc = re.sub(r'<[^>]+>', '', val_s)
                long_descriptions.append((lbl, clean_desc))
            else:
                clean_v = re.sub(r'<[^>]+>', '', val_s)
                short_props.append((lbl, clean_v))

        inat_map_url = ""
        for c in row.index:
            if "inaturalist" in str(c).lower() and ("mapa" in str(c).lower() or "odkaz" in str(c).lower()):
                v_cand = str(row.get(c, "")).strip()
                if v_cand.startswith("http://") or v_cand.startswith("https://"):
                    inat_map_url = v_cand
                    break
        if not inat_map_url:
            try:
                raw_sp_cand = str(row.get("Pojem") or row.get("Položka / Název") or row.get("Vědecké jméno") or row.get("Přírodovědný název") or (row.iloc[0] if len(row) > 0 else "")).strip()
                if raw_sp_cand and raw_sp_cand.lower() != "nan":
                    inat_map_url = fetch_inaturalist_map_url(raw_sp_cand)
            except Exception:
                pass
        if inat_map_url and not any("inaturalist.org" in x[1] for x in links):
            links.append(("iNaturalist (mapa pozorování)", inat_map_url))

        if short_props:
            t_props = doc.add_table(rows=len(short_props), cols=2)
            t_props.alignment = WD_TABLE_ALIGNMENT.CENTER
            for r_i, (k, v) in enumerate(short_props):
                c0 = t_props.rows[r_i].cells[0]
                c1 = t_props.rows[r_i].cells[1]
                c0.width = Inches(2.0)
                c1.width = Inches(4.5)
                p0 = c0.paragraphs[0]
                p0.paragraph_format.space_before = Pt(2)
                p0.paragraph_format.space_after = Pt(2)
                r0 = p0.add_run(f"{k}:")
                r0.bold = True
                r0.font.size = Pt(9.5)
                r0.font.color.rgb = RGBColor(51, 65, 85)

                p1 = c1.paragraphs[0]
                p1.paragraph_format.space_before = Pt(2)
                p1.paragraph_format.space_after = Pt(2)
                r1 = p1.add_run(v)
                r1.font.size = Pt(9.5)
                r1.font.color.rgb = RGBColor(30, 41, 59)

        for d_lbl, d_txt in long_descriptions:
            p_dl = doc.add_paragraph()
            p_dl.paragraph_format.space_before = Pt(6)
            p_dl.paragraph_format.space_after = Pt(2)
            rd = p_dl.add_run(d_lbl)
            rd.bold = True
            rd.font.size = Pt(11)
            rd.font.color.rgb = RGBColor(22, 101, 52)

            p_dt = doc.add_paragraph()
            p_dt.paragraph_format.space_after = Pt(6)
            rd_t = p_dt.add_run(d_txt)
            rd_t.font.size = Pt(9.5)
            rd_t.font.color.rgb = RGBColor(30, 41, 59)

        if links:
            p_lk = doc.add_paragraph()
            p_lk.paragraph_format.space_before = Pt(4)
            p_lk.paragraph_format.space_after = Pt(6)
            r_lh = p_lk.add_run("Odkazy a zdroje: ")
            r_lh.bold = True
            r_lh.font.size = Pt(9.5)
            for l_lbl, l_url in links:
                r_l = p_lk.add_run(f"• {l_lbl} ({l_url}) ")
                r_l.font.size = Pt(8.5)
                r_l.font.color.rgb = RGBColor(22, 101, 52)

        if layout_mode == "page_per_species" and idx < len(df) - 1:
            doc.add_page_break()
        elif idx < len(df) - 1:
            p_sep = doc.add_paragraph()
            p_sep.paragraph_format.space_before = Pt(6)
            p_sep.paragraph_format.space_after = Pt(10)
            r_sep = p_sep.add_run("—" * 35)
            r_sep.font.color.rgb = RGBColor(203, 213, 225)

    if include_citations:
        doc.add_page_break()
        p_cit_h = doc.add_paragraph()
        p_cit_h.paragraph_format.space_before = Pt(10)
        p_cit_h.paragraph_format.space_after = Pt(4)
        rc_h = p_cit_h.add_run("Použitá literatura, zdroje dat a licence")
        rc_h.bold = True
        rc_h.font.size = Pt(15)
        rc_h.font.color.rgb = RGBColor(27, 67, 50)

        citations_data = [
            ("Pladias.cz", "Pladias.cz – Databáze české flóry a vegetace. Botanický ústav AV ČR, Průhonice. (pladias.cz)"),
            ("Klíč 2019", "Kaplan Z. et al. (2019): Klíč ke květeně České republiky. Academia, Praha, 1168 s."),
            ("Červený seznam ČR", "Grulich V. (2012): Red List of vascular plants of the Czech Republic: 3rd edition. Preslia 84: 631–645."),
            ("iNaturalist", "iNaturalist Community. Observation data & photos licensed under Creative Commons. (inaturalist.org)"),
            ("Mushroom Color Atlas", "Beeler J. (2024): The Mushroom Color Atlas – A Guide to Dyes and Pigments Made from Fungi. (mushroomcoloratlas.com)"),
            ("Mykologie.net", "Česká mykologická společnost a portál Mykologie.net."),
            ("GBIF", "Global Biodiversity Information Facility (GBIF.org) Backbone Taxonomy & Occurrences."),
            ("Wikimedia Commons", "Multimediální repozitář Wikimedia Foundation pod volnými licencemi Creative Commons.")
        ]
        for src_title, src_text in citations_data:
            p_c = doc.add_paragraph()
            p_c.paragraph_format.space_after = Pt(3)
            r_ct = p_c.add_run(f"• {src_title}: ")
            r_ct.bold = True
            r_ct.font.size = Pt(8.5)
            r_ct.font.color.rgb = RGBColor(51, 65, 85)
            r_cb = p_c.add_run(src_text)
            r_cb.font.size = Pt(8.5)
            r_cb.font.color.rgb = RGBColor(71, 85, 105)

    doc.save(output_docx_path)
    return os.path.exists(output_docx_path) and os.path.getsize(output_docx_path) > 0

countries_db = load_countries_db()

st.set_page_config(
    page_title="Generátor kartiček Anki",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "app_ui_theme" not in st.session_state:
    st.session_state.app_ui_theme = "Tmavý"

is_light_ui = st.session_state.get("app_ui_theme", "Tmavý") == "Světlý"

if is_light_ui:
    css_bg = "#f8faf8"
    css_fg = "#111d14"
    css_muted = "#2b5437"
    css_card_bg = "#ffffff"
    css_border = "#cfe0d5"
    css_input_bg = "#ffffff"
    css_input_fg = "#111d14"
    css_input_border = "#b7cfc0"
    css_btn_bg = "#216a40"
    css_btn_hover = "#195332"
    css_expander_bg = "#ffffff"
    css_title_color = "#0e1a11"
else:
    css_bg = "#060a08"
    css_fg = "#ffffff"
    css_muted = "#a2d7b4"
    css_card_bg = "#0b140e"
    css_border = "#264531"
    css_input_bg = "#0d1a12"
    css_input_fg = "#ffffff"
    css_input_border = "#2f573c"
    css_btn_bg = "#1e6a3c"
    css_btn_hover = "#28874d"
    css_expander_bg = "#09110c"
    css_title_color = "#ffffff"

st.markdown(f"""
<style>
    /* Skrytí sidebaru */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {{
        display: none !important;
    }}

    :root {{
        --bio-bg: {css_bg};
        --bio-fg: {css_fg};
        --bio-muted: {css_muted};
        --bio-card-bg: {css_card_bg};
        --bio-border: {css_border};
        --bio-input-bg: {css_input_bg};
        --bio-input-fg: {css_input_fg};
        --bio-input-border: {css_input_border};
        --bio-btn-bg: {css_btn_bg};
        --bio-btn-hover: {css_btn_hover};
    }}

    html, body, [data-testid="stAppViewContainer"], .stApp {{
        background-color: {css_bg} !important;
        color: {css_fg} !important;
        color-scheme: {"light" if st.session_state.app_ui_theme == "Světlý" else "dark"} !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    }}

    /* Horní lišta Streamlit */
    header[data-testid="stHeader"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"] {{
        background-color: {css_bg} !important;
        color: {css_fg} !important;
    }}
    header[data-testid="stHeader"] *,
    [data-testid="stToolbar"] * {{
        color: {css_fg} !important;
    }}

    .main-title {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        color: {css_title_color} !important;
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 0.25rem;
    }}
    .subtitle {{
        color: {css_muted} !important;
        font-size: 0.98rem;
        margin-bottom: 1.5rem;
        font-weight: 500;
    }}

    /* Nadpisy, odstavce a texty */
    h1, h2, h3, h4, h5, h6 {{
        color: {css_title_color} !important;
        font-weight: 600 !important;
    }}

    p, span, label, li, small, caption, th, td {{
        color: {css_fg} !important;
    }}

    hr {{
        border-color: {css_border} !important;
    }}

    /* Tlačítka formulářů a akcí - výrazná, jasně klikatelná tlačítka */
    .stButton > button,
    .stDownloadButton > button,
    [data-testid="stBaseButton-secondary"],
    [data-testid="stBaseButton-primary"] {{
        background-color: {css_btn_bg} !important;
        color: #ffffff !important;
        border: 1.5px solid #389c62 !important;
        border-radius: 6px !important;
        padding: 8px 18px !important;
        font-size: 0.92rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        cursor: pointer !important;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.18) !important;
        transition: all 0.15s ease-in-out !important;
    }}
    .stButton > button:hover,
    .stDownloadButton > button:hover,
    [data-testid="stBaseButton-secondary"]:hover,
    [data-testid="stBaseButton-primary"]:hover {{
        background-color: {css_btn_hover} !important;
        border-color: #52c480 !important;
        color: #ffffff !important;
        transform: translateY(-1.5px) !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.28) !important;
    }}
    .stButton > button:active,
    .stDownloadButton > button:active,
    [data-testid="stBaseButton-secondary"]:active,
    [data-testid="stBaseButton-primary"]:active {{
        transform: translateY(1px) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2) !important;
    }}

    /* Tlačítka nápovědy a ikony (?) - resetovat aby nebyly gigantické zelené */
    button[data-testid="stHelpPopover"],
    [data-testid="stHelpPopover"] button,
    [data-testid="stTooltipHoverTarget"] button,
    [data-testid="stTooltipHoverTarget"] {{
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        width: auto !important;
        height: auto !important;
        box-shadow: none !important;
        color: {css_muted} !important;
    }}
    button[data-testid="stHelpPopover"]:hover,
    [data-testid="stHelpPopover"] button:hover {{
        background: transparent !important;
        color: #389c62 !important;
    }}

    /* Vstupy a formuláře */
    .stTextInput input,
    .stTextArea textarea,
    input[type="text"],
    textarea {{
        background-color: {css_input_bg} !important;
        border: 1px solid {css_input_border} !important;
        color: {css_input_fg} !important;
        border-radius: 6px !important;
        font-size: 0.95rem !important;
    }}
    .stTextInput input:focus,
    .stTextArea textarea:focus {{
        border-color: #389c62 !important;
        outline: none !important;
    }}

    .stSelectbox > div > div,
    div[data-baseweb="select"] > div {{
        background-color: {css_input_bg} !important;
        border: 1px solid {css_input_border} !important;
        color: {css_input_fg} !important;
        border-radius: 6px !important;
    }}
    div[data-baseweb="select"] span {{
        color: {css_input_fg} !important;
    }}
    div[data-baseweb="select"] > div:hover {{
        border-color: #389c62 !important;
    }}

    /* Placeholder text */
    ::placeholder,
    input::placeholder,
    textarea::placeholder {{
        color: {css_muted} !important;
        opacity: 0.85 !important;
    }}

    /* Popovery, tooltips, dialogy, selectbox dropdowny a menu */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="tooltip"],
    div[role="tooltip"],
    [data-testid="stTooltipContent"],
    div[data-baseweb="menu"],
    ul[role="listbox"],
    li[role="option"],
    div[data-baseweb="modal"] {{
        background-color: {css_card_bg} !important;
        color: {css_fg} !important;
        border-color: {css_border} !important;
    }}
    li[role="option"] {{
        background-color: {css_card_bg} !important;
        color: {css_fg} !important;
    }}
    li[role="option"] * {{
        background-color: transparent !important;
        color: {css_fg} !important;
    }}
    li[role="option"]:hover,
    li[role="option"][aria-selected="true"],
    li[role="option"]:focus {{
        background-color: {"#e2eee6" if is_light_ui else "rgba(45, 120, 75, 0.35)"} !important;
        color: {"#0d381e" if is_light_ui else "#ffffff"} !important;
    }}
    li[role="option"]:hover *,
    li[role="option"][aria-selected="true"] * {{
        color: {"#0d381e" if is_light_ui else "#ffffff"} !important;
    }}

    /* Decentní menší tlačítka pro hromadné volby */
    .stButton button[kind="secondary"],
    .compact-btn button {{
        font-size: 0.82rem !important;
        padding: 4px 10px !important;
        background-color: {"#f1f5f2" if is_light_ui else "#15241b"} !important;
        color: {"#216a40" if is_light_ui else "#a5d8b8"} !important;
        border: 1px solid {"#cfe0d5" if is_light_ui else "#233e2b"} !important;
        border-radius: 4px !important;
        font-weight: 500 !important;
    }}
    .stButton button[kind="secondary"]:hover,
    .compact-btn button:hover {{
        background-color: {"#e4ede7" if is_light_ui else "#1b3323"} !important;
        color: {"#165030" if is_light_ui else "#c4ebd2"} !important;
        border-color: #389c62 !important;
    }}

    /* File uploader */
    [data-testid="stFileUploader"] section {{
        background-color: {css_card_bg} !important;
        border-color: {css_input_border} !important;
    }}
    [data-testid="stFileUploader"] section * {{
        color: {css_fg} !important;
    }}

    /* Vylepšené panely a karty uvnitř expanderů (Vysoký kontrast) */
    [data-testid="stExpander"] {{
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        margin-bottom: 14px !important;
    }}
    [data-testid="stExpander"] details {{
        border: none !important;
        background-color: transparent !important;
    }}
    [data-testid="stExpander"] details summary,
    [data-testid="stExpander"] summary {{
        background-color: {css_expander_bg} !important;
        border: 1.5px solid {css_border} !important;
        border-radius: 8px !important;
        padding: 12px 18px !important;
        color: {css_title_color} !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        transition: all 0.15s ease-in-out !important;
    }}
    [data-testid="stExpander"] summary:hover {{
        border-color: #389c62 !important;
        background-color: {"#f1f5f2" if is_light_ui else "#122017"} !important;
    }}
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {{
        background-color: {"#ffffff" if is_light_ui else "#080e0a"} !important;
        border: 1.5px solid {"#cfe0d5" if is_light_ui else "#25422f"} !important;
        border-radius: 8px !important;
        padding: 20px 22px !important;
        margin-top: 6px !important;
        box-shadow: {"0 4px 12px rgba(0,0,0,0.05)" if is_light_ui else "0 6px 20px rgba(0,0,0,0.5)"} !important;
    }}

    /* Rodilý kontejner Streamlit s ohraničením (border=True) */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: {"#ffffff" if is_light_ui else "#0b140e"} !important;
        border: 1.5px solid {"#cfe0d5" if is_light_ui else "#264531"} !important;
        border-radius: 8px !important;
    }}

    /* Skrytí komponentního iframe pro harmoniku */
    iframe[title="streamlit.components.v1.html"],
    div[data-testid="stCustomComponentV1"] {{
        display: none !important;
        height: 0px !important;
        min-height: 0px !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    .bio-badge {{
        display: inline-block;
        font-size: 0.82rem;
        font-weight: 700;
        padding: 4px 11px;
        border-radius: 12px;
        background: {"#e4efe7" if is_light_ui else "rgba(56, 175, 105, 0.18)"};
        border: 1px solid {"#bfd8c7" if is_light_ui else "rgba(56, 175, 105, 0.45)"};
        color: {"#1a5833" if is_light_ui else "#8ee6b2"};
    }}

    /* Konzistentní hierarchie tlačítek: Primární, Sekundární (Outline/Ghost), Destruktivní */
    button[kind="primary"],
    [data-testid="stBaseButton-primary"] {{
        background: linear-gradient(135deg, #227341 0%, #1a5c33 100%) !important;
        color: #ffffff !important;
        border: 1.5px solid #4cd185 !important;
        border-radius: 6px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 14px rgba(34, 115, 65, 0.4) !important;
        letter-spacing: 0.02em !important;
    }}
    button[kind="primary"]:hover,
    [data-testid="stBaseButton-primary"]:hover {{
        background: linear-gradient(135deg, #28884d 0%, #206f3e 100%) !important;
        border-color: #6ce49f !important;
        box-shadow: 0 6px 18px rgba(40, 136, 77, 0.5) !important;
        transform: translateY(-1.5px) !important;
    }}

    [data-testid="stBaseButton-secondary"],
    .stDownloadButton > button {{
        background-color: transparent !important;
        color: {css_fg} !important;
        border: 1.5px solid {"#8cbfa0" if is_light_ui else "#385c44"} !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        box-shadow: none !important;
    }}
    [data-testid="stBaseButton-secondary"]:hover,
    .stDownloadButton > button:hover {{
        background-color: {"#eaf3ee" if is_light_ui else "rgba(56, 156, 98, 0.16)"} !important;
        border-color: #3da86b !important;
        color: {"#14502d" if is_light_ui else "#ffffff"} !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.12) !important;
        transform: translateY(-1px) !important;
    }}

    /* Destruktivní akce */
    button[key*="uncheck"], button[key*="delete"], button[key*="dedup"], button[key*="clear"],
    [data-testid*="uncheck"] button, [data-testid*="delete"] button, [data-testid*="dedup"] button {{
        background-color: transparent !important;
        color: {"#5c6b61" if is_light_ui else "#a6b5ad"} !important;
        border: 1.5px solid {"#c8d6cd" if is_light_ui else "#3a4d41"} !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        box-shadow: none !important;
    }}
    button[key*="uncheck"]:hover, button[key*="delete"]:hover, button[key*="dedup"]:hover, button[key*="clear"]:hover,
    [data-testid*="uncheck"] button:hover, [data-testid*="delete"] button:hover, [data-testid*="dedup"] button:hover {{
        background-color: rgba(220, 53, 69, 0.18) !important;
        border-color: #dc3545 !important;
        color: #ff6b7a !important;
        box-shadow: 0 2px 6px rgba(220, 53, 69, 0.2) !important;
        transform: translateY(-1px) !important;
    }}

    /* Sjednocený přepínač formátů (Segmented control) */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 6px;
        border-bottom: 1.5px solid {css_border} !important;
        background-color: {"#edf3ef" if is_light_ui else "#101b14"} !important;
        padding: 5px 6px !important;
        border-radius: 8px !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 6px !important;
        color: {css_muted} !important;
        font-weight: 500 !important;
        padding: 7px 16px !important;
        box-shadow: none !important;
        transition: all 0.15s ease-in-out !important;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        color: {css_fg} !important;
        background-color: {"#e0ede5" if is_light_ui else "rgba(60, 150, 90, 0.12)"} !important;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: #237442 !important;
        border: 1px solid #3ea76b !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.22) !important;
    }}

    /* Dataframe a tabulky */
    [data-testid="stDataFrame"], [data-testid="stTable"] {{
        background-color: {css_card_bg} !important;
        border: 1px solid {css_border} !important;
        border-radius: 8px !important;
        color: {css_fg} !important;
    }}
    [data-testid="stDataFrame"] [data-testid="stElementToolbar"] {{
        background-color: {css_card_bg} !important;
    }}
    [data-testid="stDataFrame"] [data-testid="stElementToolbar"] button {{
        background-color: {css_input_bg} !important;
        color: {css_fg} !important;
        border: 1px solid {css_border} !important;
        padding: 4px 8px !important;
    }}

    /* Taby */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 6px;
        border-bottom: 1px solid {css_border} !important;
        background-color: transparent !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent !important;
        border: none !important;
        border-radius: 6px !important;
        color: {css_muted} !important;
        font-weight: 500 !important;
        padding: 6px 14px !important;
        box-shadow: none !important;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        color: {css_fg} !important;
        background-color: rgba(60, 150, 90, 0.08) !important;
    }}
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {{
        display: none !important;
        height: 0px !important;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: rgba(45, 120, 75, 0.22) !important;
        border: 1px solid #389c62 !important;
        color: {css_fg} !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
    }}

    /* Radio a zaškrtávací pole */
    .stCheckbox span, .stRadio span,
    .stCheckbox label p, .stRadio label p {{
        color: {css_fg} !important;
    }}
    div[data-testid="stCheckbox"] div[role="checkbox"] {{
        background-color: {css_input_bg} !important;
        border: 1px solid {css_input_border} !important;
    }}
    div[data-testid="stCheckbox"] div[role="checkbox"][aria-checked="true"] {{
        background-color: #216a40 !important;
        border-color: #389c62 !important;
    }}

    /* Notifikace a hlášení */
    div[data-testid="stAlert"] {{
        border-radius: 6px !important;
        border: 1px solid {css_border} !important;
        background-color: {css_card_bg} !important;
        color: {css_fg} !important;
    }}

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
    .card-preview-container [data-testid="stMarkdownContainer"] div {{
        color: inherit !important;
    }}
</style>
""", unsafe_allow_html=True)

components.html("""
<script>
function setupAccordion() {
    try {
        const parentDoc = window.parent.document;
        if (!parentDoc) return;
        const expanders = parentDoc.querySelectorAll('details[data-testid="stExpander"]');
        expanders.forEach(exp => {
            const summary = exp.querySelector('summary');
            if (!summary) return;
            const txt = summary.textContent.trim();
            if (/^[2-5]\\.\\s/.test(txt)) {
                exp.setAttribute('name', 'main_app_accordion');
                if (!exp.dataset.accordionBound) {
                    exp.dataset.accordionBound = 'true';
                    exp.addEventListener('toggle', () => {
                        if (exp.open) {
                            expanders.forEach(other => {
                                if (other !== exp && other.getAttribute('name') === 'main_app_accordion' && other.open) {
                                    other.open = false;
                                }
                            });
                        }
                    });
                }
            }
        });
    } catch (e) {}
}
setupAccordion();
const obs = new MutationObserver(() => setupAccordion());
obs.observe(window.parent.document.body, { childList: true, subtree: true });
</script>
""", height=0)

col_head1, col_head2 = st.columns([4.2, 1.8])
with col_head1:
    st.markdown('<div class="main-title">Generátor kartiček Anki</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Nahrajte tabulku, obohaťte ji o data přes API a sestavte líc a rub kartiček.</div>', unsafe_allow_html=True)
with col_head2:
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    theme_sel = st.radio(
        "Vzhled aplikace:",
        options=["Světlý režim", "Tmavý režim"],
        index=0 if st.session_state.app_ui_theme == "Světlý" else 1,
        horizontal=True,
        key="w_app_ui_theme_radio"
    )
    new_theme = "Světlý" if "Světlý" in theme_sel else "Tmavý"
    if new_theme != st.session_state.app_ui_theme:
        st.session_state.app_ui_theme = new_theme
        st.rerun()

@st.cache_data(show_spinner=False)
@st.cache_data(show_spinner=False)
def _read_batch_replacer_html():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "BatchReplacer.html")
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            pass
    return ""

@st.cache_data(show_spinner=False)
def _read_karty_html_bytes():
    karty_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Karty.html")
    if os.path.exists(karty_path):
        try:
            with open(karty_path, "rb") as f_k:
                return f_k.read()
        except Exception:
            pass
    return b""

@st.cache_data(show_spinner=False)
def _read_pdf_data(file_candidates):
    for f in file_candidates:
        if os.path.exists(f):
            try:
                with open(f, "rb") as fp:
                    return fp.read()
            except Exception:
                pass
    return None

def _compat_width():
    try:
        ver = tuple(map(int, re.findall(r'\d+', st.__version__)[:2]))
        if ver >= (1, 60):
            return {"width": "stretch"}
    except Exception:
        pass
    return {"use_container_width": True}

pdf_gen_data = _read_pdf_data(["O_generatoru.pdf", "O generátoru.pdf", "MANUAL_GENERATOR.pdf"])
pdf_anki_data = _read_pdf_data(["O_Anki.pdf", "O Anki.pdf", "MANUAL_ANKI.pdf"])
pdf_karty_data = _read_pdf_data(["O_Karty_html.pdf", "O_karty.pdf", "MANUAL_KARTY.pdf"])

if 'df' not in st.session_state:
    st.session_state.df = None
if 'enhancements_applied' not in st.session_state:
    st.session_state.enhancements_applied = False
if 'unfound_list' not in st.session_state:
    st.session_state.unfound_list = []
if 'generated_apkg_data' not in st.session_state:
    st.session_state.generated_apkg_data = None
if 'generated_obsidian_data' not in st.session_state:
    st.session_state.generated_obsidian_data = None
if 'generated_obsidian_filename' not in st.session_state:
    st.session_state.generated_obsidian_filename = "Studijni_Karticky_Obsidian.zip"
if 'generated_apkg_filename' not in st.session_state:
    st.session_state.generated_apkg_filename = ""
if 'generated_pdf_data' not in st.session_state:
    st.session_state.generated_pdf_data = None
if 'generated_pdf_filename' not in st.session_state:
    st.session_state.generated_pdf_filename = ""
if 'generated_docx_data' not in st.session_state:
    st.session_state.generated_docx_data = None
if 'generated_docx_filename' not in st.session_state:
    st.session_state.generated_docx_filename = ""
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

st.markdown("#### 1. Vstupní data a správa souborů")
col_custom_card, col_sep_card, col_test_card = st.columns([2.6, 0.4, 2.0], gap="small")

with col_custom_card:
    with st.container(border=True):
        st.markdown("##### Vlastní data")

        input_method = st.radio(
            "Způsob zadání vlastních dat:",
            ["Nahrát soubor (Excel, CSV, TXT, APKG)", "Vložit seznam ručně (textové pole)"],
            horizontal=True,
            key="w_input_method_choice"
        )

        uploaded_files = None
        text_input_value = ""

        if input_method == "Nahrát soubor (Excel, CSV, TXT, APKG)":
            uploaded_files = st.file_uploader(
                "Nahrajte jeden nebo více souborů (Excel .xlsx, CSV, TXT nebo balíček Anki .apkg / .colpkg):",
                type=["csv", "xlsx", "xls", "txt", "apkg", "colpkg"],
                accept_multiple_files=True,
                help="Můžete nahrát tabulku i balíček Anki současně. Program je inteligentně sloučí a zachová historii učení!"
            )

            merge_anki_policy = "merge_all"
            merge_source_prio = "table"
            custom_col_mapping = {}
            custom_col_prio = {}

            if uploaded_files:
                has_apkg_file = any(f.name.lower().endswith(('.apkg', '.colpkg')) for f in uploaded_files)
                has_table_file = any(f.name.lower().endswith(('.xlsx', '.xls', '.csv', '.txt')) for f in uploaded_files)
                is_mixed = has_apkg_file and (has_table_file or st.session_state.df is not None)

                if is_mixed:

                    peek_table_cols = []
                    peek_apkg_cols = []
                    for up_f in uploaded_files:
                        f_low = up_f.name.lower()
                        if f_low.endswith(('.xlsx', '.xls')):
                            try:
                                up_f.seek(0)
                                _p_df = pd.read_excel(up_f, nrows=1)
                                up_f.seek(0)
                                peek_table_cols.extend([str(c) for c in _p_df.columns if str(c).strip()])
                            except Exception: pass
                        elif f_low.endswith('.csv'):
                            try:
                                up_f.seek(0)
                                _p_df = pd.read_csv(up_f, nrows=1)
                                if len(_p_df.columns) <= 1:
                                    up_f.seek(0)
                                    _p_df = pd.read_csv(up_f, sep=';', nrows=1)
                                up_f.seek(0)
                                peek_table_cols.extend([str(c) for c in _p_df.columns if str(c).strip()])
                            except Exception: pass
                        elif f_low.endswith(('.apkg', '.colpkg')):
                            try:
                                up_f.seek(0)
                                _sub_apkg, _ = extract_apkg_to_dataframe(up_f)
                                up_f.seek(0)
                                peek_apkg_cols.extend([str(c) for c in _sub_apkg.columns if not str(c).startswith('_anki_')])
                            except Exception: pass

                    t_cols_avail = list(dict.fromkeys(peek_table_cols)) if peek_table_cols else (list(st.session_state.df.columns) if st.session_state.df is not None else [])
                    t_cols_clean = [c for c in t_cols_avail if not str(c).startswith('_anki_')]
                    a_cols_clean = list(dict.fromkeys(peek_apkg_cols))
                    auto_defaults = auto_match_columns(t_cols_clean, a_cols_clean)

                    with st.container(border=True):
                        st.markdown("##### 🔄 Detekován balíček Anki + tabulka Excel/CSV (Inteligentní sloučení se zachováním historie učení)")

                        col_m1, col_m2 = st.columns(2)
                        with col_m1:
                            merge_choice = st.radio(
                                "Jak naložit se seznamem druhů?",
                                [
                                    "Sloučit a doplnit (Zachovat historii učení pro existující druhy a přidat nové druhy z tabulky)",
                                    "Pouze druhy z tabulky (Ponechat pouze druhy z tabulky a z Anki přenést historii učení)"
                                ],
                                index=0,
                                key="merge_anki_policy_radio"
                            )
                            merge_anki_policy = "merge_all" if "Sloučit a doplnit" in merge_choice else "table_only"

                        with col_m2:
                            prio_choice = st.radio(
                                "Při nalezení druhu v obou zdrojích upřednostnit data z:",
                                [
                                    "🟢 Tabulky (Excel/CSV) – texty a poznámky z tabulky přepíší Anki (doporučeno)",
                                    "🔵 Balíčku Anki – zachovat původní texty a data z Anki",
                                    "⚙️ Vlastní výběr zdroje pro každý sloupec zvlášť"
                                ],
                                index=0,
                                key="merge_source_prio_radio"
                            )
                            if "Tabulky" in prio_choice:
                                merge_source_prio = "table"
                            elif "Balíčku Anki" in prio_choice:
                                merge_source_prio = "anki"
                            else:
                                merge_source_prio = "custom"

                        col_pair_mode = st.radio(
                            "Způsob párování sloupců mezi tabulkou a balíčkem Anki:",
                            [
                                "⚡ Automaticky spárovat sloupce (např. Popis ↔ Poznámky, České jméno ↔ Český název, Fotografie ↔ Obrázek)",
                                "🎯 Vlastní propojení sloupců (ruční přiřazení)"
                            ],
                            index=0 if merge_source_prio != "custom" else 1,
                            key="merge_col_pair_mode_radio"
                        )

                        show_manual_mapping = ("Vlastní propojení" in col_pair_mode) or (merge_source_prio == "custom")

                        if show_manual_mapping and t_cols_clean and a_cols_clean:
                            st.markdown("###### 🔗 Propojení sloupců a priorita zdroje:")
                            st.caption("Pro každý sloupec z tabulky zvolte odpovídající pole z Anki. Pokud mají oba zdroje hodnotu, zvolte který zdroj má přednost:")
                            for tc in t_cols_clean:
                                c_map1, c_map2 = st.columns([1.5, 1.0])
                                def_partner = auto_defaults.get(tc, "[Nespárovat / Ponechat samostatně]")
                                partner_opts = ["[Nespárovat / Ponechat samostatně]"] + a_cols_clean
                                p_idx = partner_opts.index(def_partner) if def_partner in partner_opts else 0

                                with c_map1:
                                    chosen_partner = st.selectbox(
                                        f"Sloupec z tabulky: **{tc}** ➔ Pole v Anki:",
                                        options=partner_opts,
                                        index=p_idx,
                                        key=f"col_map_sel_{slugify(tc)}"
                                    )
                                    if chosen_partner != "[Nespárovat / Ponechat samostatně]":
                                        custom_col_mapping[tc] = chosen_partner

                                with c_map2:
                                    if merge_source_prio == "custom" and chosen_partner != "[Nespárovat / Ponechat samostatně]":
                                        chosen_p = st.selectbox(
                                            f"Přednost pro **{tc}**:",
                                            options=["Tabulka (Excel/CSV)", "Balíček Anki"],
                                            index=0,
                                            key=f"col_prio_sel_{slugify(tc)}"
                                        )
                                        custom_col_prio[tc] = "table" if "Tabulka" in chosen_p else "anki"
                                    else:
                                        p_txt = "Tabulka (Excel)" if merge_source_prio == "table" else "Balíček Anki"
                                        st.markdown(f"<div style='padding-top: 28px; font-size: 0.85rem; color: #94a3b8;'>Přednost: <b>{p_txt}</b></div>", unsafe_allow_html=True)
                        else:
                            custom_col_mapping = auto_defaults

                c_mode, c_btn_r = st.columns([1.5, 1.2])
                with c_mode:
                    mode_upload = st.radio(
                        "Způsob načtení souborů:",
                        ["Nahradit stávající data", "Připojit k existující tabulce"],
                        horizontal=True,
                        key="radio_upload_mode"
                    )
                with c_btn_r:
                    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
                    reload_clicked = st.button("Zpracovat soubory", key="btn_reload_files", use_container_width=True, type="primary")
            else:
                reload_clicked = False
                mode_upload = "Nahradit stávající data"

            if uploaded_files and (st.session_state.df is None or reload_clicked):
                try:
                    apkg_dfs = []
                    table_dfs = []
                    apkg_loaded_info = []

                    for up_f in uploaded_files:
                        f_low = up_f.name.lower()
                        if f_low.endswith(('.apkg', '.colpkg')):
                            sub_df, imported_deck = extract_apkg_to_dataframe(up_f)
                            apkg_dfs.append(sub_df)
                            apkg_loaded_info.append((up_f.name, len(sub_df), imported_deck))
                        elif f_low.endswith('.csv'):
                            sub_df = pd.read_csv(up_f)
                            if len(sub_df.columns) <= 1:
                                up_f.seek(0)
                                sub_df = pd.read_csv(up_f, sep=';')
                            table_dfs.append(sub_df)
                        elif f_low.endswith('.txt'):
                            content = up_f.read().decode('utf-8', errors='replace')
                            lines = content.splitlines()
                            species_list = [line.strip() for line in lines if line.strip()]
                            table_dfs.append(pd.DataFrame(species_list, columns=["Pojem"]))
                        else:
                            try:
                                xl_obj = pd.ExcelFile(up_f)
                                if len(xl_obj.sheet_names) > 1:
                                    sheets_dfs = []
                                    for s_name in xl_obj.sheet_names:
                                        raw_s = pd.read_excel(up_f, sheet_name=s_name, header=None)
                                        if not raw_s.empty:
                                            first_cell = str(raw_s.iloc[0, 0]).strip()
                                            first_col_is_header = any(h in first_cell.lower() for h in ["jméno", "jmeno", "název", "nazev", "druh", "taxon", "species", "name", "id", "kategorie"])
                                            if not first_col_is_header:
                                                sub_s = pd.DataFrame({
                                                    "Pojem": raw_s[0].dropna().astype(str).str.strip(),
                                                    "Kategorie": s_name
                                                })
                                            else:
                                                sub_s = pd.read_excel(up_f, sheet_name=s_name)
                                                if "Kategorie" not in sub_s.columns:
                                                    sub_s["Kategorie"] = s_name
                                            sheets_dfs.append(sub_s)
                                    if sheets_dfs:
                                        table_dfs.append(pd.concat(sheets_dfs, ignore_index=True))
                                    else:
                                        table_dfs.append(pd.read_excel(up_f))
                                else:
                                    raw_s = pd.read_excel(up_f, header=None)
                                    if not raw_s.empty and len(raw_s.columns) == 1:
                                        first_cell = str(raw_s.iloc[0, 0]).strip()
                                        first_col_is_header = any(h in first_cell.lower() for h in ["jméno", "jmeno", "název", "nazev", "druh", "taxon", "species", "name", "id", "kategorie"])
                                        if not first_col_is_header and len(first_cell.split()) >= 1:
                                            table_dfs.append(pd.DataFrame(raw_s[0].dropna().astype(str).str.strip().tolist(), columns=["Pojem"]))
                                        else:
                                            table_dfs.append(pd.read_excel(up_f))
                                    else:
                                        table_dfs.append(pd.read_excel(up_f))
                            except Exception:
                                table_dfs.append(pd.read_excel(up_f))

                    combined_table_df = pd.concat(table_dfs, ignore_index=True) if table_dfs else None
                    combined_apkg_df = pd.concat(apkg_dfs, ignore_index=True) if apkg_dfs else None

                    if "Připojit" in mode_upload and st.session_state.df is not None:
                        if combined_table_df is not None:
                            combined_table_df = pd.concat([st.session_state.df, combined_table_df], ignore_index=True)
                        else:
                            combined_table_df = st.session_state.df.copy()

                    merge_msg = ""
                    if combined_apkg_df is not None and combined_table_df is not None:
                        keep_only = (merge_anki_policy == "table_only")
                        effective_prio = custom_col_prio if merge_source_prio == "custom" else merge_source_prio
                        final_df, matched_cnt, new_cnt, kept_cnt = smart_merge_apkg_and_excel(
                            combined_apkg_df, combined_table_df,
                            col_mapping=custom_col_mapping if custom_col_mapping else None,
                            source_priority=effective_prio,
                            keep_only_table=keep_only
                        )
                        prio_desc = "Tabulka (Excel)" if merge_source_prio == "table" else ("Balíček Anki" if merge_source_prio == "anki" else "Vlastní per sloupec")
                        pairs_desc = f" (spárováno {len(custom_col_mapping)} sloupců, přednost: {prio_desc})" if custom_col_mapping else ""
                        merge_msg = f" Sloučeno s balíčkem Anki{pairs_desc}: **{matched_cnt}** existujícím druhům byla zachována historie učení a GUID. Přidáno **{new_cnt}** nových druhů."
                        if kept_cnt > 0:
                            merge_msg += f" Ponecháno **{kept_cnt}** původních druhů z balíčku."
                    elif combined_table_df is not None:
                        final_df = combined_table_df
                    elif combined_apkg_df is not None:
                        final_df = combined_apkg_df
                    else:
                        final_df = pd.DataFrame()

                    if not final_df.empty:
                        orig_cnt = len(final_df)
                        key_col = final_df.columns[0]

                        norm_keys = final_df[key_col].apply(normalize_match_key)

                        if '_anki_guid' in final_df.columns:
                            final_df['__has_guid'] = final_df['_anki_guid'].notna() & (final_df['_anki_guid'].astype(str).str.strip() != '')
                            final_df = final_df.sort_values(by='__has_guid', ascending=False)
                            final_df['__norm_k'] = norm_keys
                            final_df = final_df.drop_duplicates(subset=['__norm_k']).drop(columns=['__has_guid', '__norm_k']).reset_index(drop=True)
                        else:
                            final_df['__norm_k'] = norm_keys
                            final_df = final_df.drop_duplicates(subset=['__norm_k']).drop(columns=['__norm_k']).reset_index(drop=True)
                        dups_cnt = orig_cnt - len(final_df)
                    else:
                        dups_cnt = 0

                    if apkg_loaded_info:
                        st.session_state.imported_apkg_deck_name = apkg_loaded_info[0][2]

                    st.session_state.df = final_df
                    st.session_state.enhancements_applied = False
                    st.session_state.unfound_list = []
                    st.session_state.generated_apkg_data = None
                    st.session_state.generated_apkg_filename = ""
                    st.session_state.generated_pdf_data = None
                    st.session_state.generated_pdf_filename = ""
                    st.session_state.unfound_csv_data = None
                    st.session_state.col_styles = {}
                    st.session_state.api_config = {}

                    msg = f"Úspěšně načteno **{len(final_df)}** položek."
                    if merge_msg:
                        msg += merge_msg
                    elif apkg_loaded_info:
                        msg += f" Z balíčku Anki '{apkg_loaded_info[0][2]}' načteno {apkg_loaded_info[0][1]} karet. Historie učení a GUID karet zůstanou při exportu 100% zachovány!"
                    if dups_cnt > 0:
                        msg += f" (Odstraněno {dups_cnt} duplicit)."
                    st.success(msg)
                    st.rerun()
                except Exception as e:
                    st.error(f"Nepodařilo se načíst soubory: {e}")
        else:
            text_input_value = st.text_area(
                "Vložte seznam položek (jeden na každý řádek):",
                height=130,
                placeholder="Např.:\nPlantago lanceolata\nBellis perennis\nTaraxacum officinale",
                key="manual_species_input"
            )

            col_btn_m1, col_btn_m2 = st.columns(2)
            with col_btn_m1:
                load_new_clicked = st.button("Načíst jako nový seznam", key="btn_manual_new", use_container_width=True)
            with col_btn_m2:
                append_clicked = st.button("Přidat k existující tabulce", key="btn_manual_append", use_container_width=True)

            if load_new_clicked or append_clicked:
                lines = text_input_value.splitlines()
                species_list = [line.strip() for line in lines if line.strip()]
                if species_list:
                    new_manual_df = pd.DataFrame(species_list, columns=["Pojem"])
                    if append_clicked and st.session_state.df is not None:
                        combined_df = pd.concat([st.session_state.df, new_manual_df], ignore_index=True)
                    else:
                        combined_df = new_manual_df

                    orig_len = len(combined_df)
                    combined_df = combined_df.drop_duplicates(subset=[combined_df.columns[0]]).reset_index(drop=True)
                    dups = orig_len - len(combined_df)

                    st.session_state.df = combined_df
                    st.session_state.enhancements_applied = False
                    st.session_state.unfound_list = []
                    st.session_state.generated_apkg_data = None
                    st.session_state.generated_apkg_filename = ""
                    st.session_state.generated_pdf_data = None
                    st.session_state.generated_pdf_filename = ""
                    st.session_state.unfound_csv_data = None
                    st.session_state.col_styles = {}
                    st.session_state.api_config = {}

                    msg = f"Načteno celkem {len(combined_df)} položek do paměti."
                    if dups > 0:
                        msg += f" (Odstraněno {dups} duplicit)."
                    st.success(msg)
                    st.rerun()
                else:
                    st.error("Seznam položek je prázdný.")

with col_sep_card:
    st.markdown('''
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:100%; min-height:280px;">
        <div style="flex:1; width:1px; background:var(--bio-border, #283a2e); opacity:0.6;"></div>
        <div style="margin:10px 0; font-size:11px; font-weight:700; color:var(--bio-muted, #7ea88f); padding:4px 8px; border-radius:12px; border:1px solid var(--bio-border, #283a2e); background:var(--bio-card-bg, #16231b);">NEBO</div>
        <div style="flex:1; width:1px; background:var(--bio-border, #283a2e); opacity:0.6;"></div>
    </div>
    ''', unsafe_allow_html=True)

with col_test_card:
    with st.container(border=True):
        st.markdown("##### Testovací data")
        st.caption("Předpřipravené ukázkové sady z různých oborů.")
        test_options = [
            "Všechny kategorie dohromady (29 položek)",
            "Kytky (3 položky)",
            "Houby (3 položky)",
            "Mechy (3 položky)",
            "Lišejníky (3 položky)",
            "Řasy (2 položky)",
            "Hmyz (3 položky)",
            "Ptáci (3 položky)",
            "Ostatní živočichové (3 položky)",
            "Státy (3 položky)",
            "Slovíčka (3 položky)"
        ]
        selected_test_sheet = st.selectbox(
            "Vyberte kategorii / list:",
            options=test_options,
            key="sel_test_sheet_category"
        )
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        load_test_btn = st.button("Načíst testovací data", use_container_width=True, key="btn_load_test_sample_all", type="primary")

        if load_test_btn:
            test_path_desktop = r"C:\Users\adalb\Desktop\Testovací soubor.xlsx"
            test_path_local = os.path.join(os.path.dirname(__file__), "Testovaci_soubor.xlsx")
            target_test_path = test_path_desktop if os.path.exists(test_path_desktop) else test_path_local

            try:
                xl_test = pd.ExcelFile(target_test_path)
                sheet_map = {
                    "Kytky": "Kytky",
                    "Houby": "Houby",
                    "Mechy": "Mechy",
                    "Lišejníky": "Lišejníky",
                    "Řasy": "Řasy",
                    "Hmyz": "Hmyz",
                    "Ptáci": "Ptáci",
                    "Ostatní živočichové": "Ostatní živočichové",
                    "Státy": "Státy",
                    "Slovíčka": "Slovíčka"
                }

                chosen_sheet = None
                if not selected_test_sheet.startswith("Všechny"):
                    for k, real_s in sheet_map.items():
                        if k in selected_test_sheet:
                            for actual_s in xl_test.sheet_names:
                                if k.lower() in actual_s.lower():
                                    chosen_sheet = actual_s
                                    break
                            if not chosen_sheet and real_s in xl_test.sheet_names:
                                chosen_sheet = real_s
                            break

                sheets_to_read = xl_test.sheet_names if (chosen_sheet is None) else [chosen_sheet]
                all_test_rows = []
                for s_name in sheets_to_read:
                    df_raw = pd.read_excel(target_test_path, sheet_name=s_name, header=None)
                    if not df_raw.empty:
                        items = df_raw[0].dropna().astype(str).str.strip().tolist()
                        for it in items:
                            if it and it.lower() != "nan":
                                all_test_rows.append({"Pojem": it, "Kategorie": s_name})

                if all_test_rows:
                    st.session_state.df = pd.DataFrame(all_test_rows)
                    st.session_state.enhancements_applied = False
                    st.session_state.unfound_list = []
                    st.session_state.generated_apkg_data = None
                    st.session_state.generated_apkg_filename = ""
                    st.session_state.generated_pdf_data = None
                    st.session_state.generated_pdf_filename = ""
                    st.session_state.generated_docx_data = None
                    st.session_state.generated_docx_filename = ""
                    st.session_state.unfound_csv_data = None
                    st.session_state.notes_count = 0
                    st.session_state.media_count = 0
                    st.session_state.front_cols_ordered = []
                    st.session_state.back_cols_ordered = []
                    st.session_state.col_styles = {}
                    st.session_state.api_config = {}
                    cat_desc = f"list '{chosen_sheet}'" if chosen_sheet else "všechny listy"
                    st.success(f"Úspěšně načteno {len(all_test_rows)} položek ({cat_desc}) ze souboru '{target_test_path}'.")
                    st.rerun()
                else:
                    st.error("Ze souboru se nepodařilo načíst žádná data.")
            except Exception as e:
                st.error(f"Chyba při čtení testovacího souboru: {e}")

if st.session_state.df is not None:
    df = st.session_state.df
    columns = [c for c in df.columns if not c.startswith('_anki_')]

    with st.expander("2. Náhled tabulky", expanded=False):
        c_th_title, c_th_badge = st.columns([3, 1.2])
        with c_th_title:
            st.markdown("##### Náhled tabulky (prvních 5 položek)")
        with c_th_badge:
            st.markdown(f'<div style="text-align: right; padding-top: 4px;"><span class="bio-badge">{len(df)} položek &bull; {len(columns)} sloupců</span></div>', unsafe_allow_html=True)

        preview_df = df[columns].head(5)
        tbl_headers = "".join([f"<th style='background-color: {css_input_bg}; color: {css_title_color}; padding: 10px 14px; text-align: left; font-size: 0.88rem; font-weight: 600; border-bottom: 2px solid {css_border};'>{h}</th>" for h in preview_df.columns])
        tbl_rows = []
        for r_idx, (_, r_data) in enumerate(preview_df.iterrows()):
            row_bg = css_card_bg if r_idx % 2 == 0 else css_bg
            tds = "".join([f"<td style='padding: 8px 14px; color: {css_fg}; font-size: 0.88rem; border-bottom: 1px solid {css_border};'>{str(v) if pd.notna(v) else ''}</td>" for v in r_data])
            tbl_rows.append(f"<tr style='background-color: {row_bg};'>{tds}</tr>")
        tbl_html = f"""
        <div style='overflow-x: auto; border: 1px solid {css_border}; border-radius: 8px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);'>
            <table style='width: 100%; border-collapse: collapse; font-family: inherit;'>
                <thead><tr>{tbl_headers}</tr></thead>
                <tbody>{' '.join(tbl_rows)}</tbody>
            </table>
        </div>
        """
        st.markdown(tbl_html, unsafe_allow_html=True)

        @st.cache_data(show_spinner=False)
        def _get_cached_table_exports(dataframe_obj):
            import io
            c_data = dataframe_obj.to_csv(index=False, encoding='utf-8-sig')
            e_buf = io.BytesIO()
            with pd.ExcelWriter(e_buf, engine='openpyxl') as writer:
                dataframe_obj.to_excel(writer, index=False)
            return c_data, e_buf.getvalue()

        csv_data, excel_data = _get_cached_table_exports(df)

        col_dummy, col_dl_right = st.columns([2.5, 1.5])
        with col_dl_right:
            c_csv, c_xlsx = st.columns(2, gap="small")
            with c_csv:
                st.download_button(
                    "Stáhnout (CSV)",
                    data=csv_data,
                    file_name="tabulka_dat.csv",
                    mime="text/csv",
                    key="dl_table_preview_csv",
                    use_container_width=True
                )
            with c_xlsx:
                st.download_button(
                    "Stáhnout (Excel)",
                    data=excel_data,
                    file_name="tabulka_dat.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="dl_table_preview_xlsx",
                    use_container_width=True
                )

        with st.expander("Nástroje pro úpravu dat", expanded=False):

            c_dedup_box, c_del_box = st.columns(2, gap="medium")
            with c_dedup_box:
                st.markdown("**1. Odstranění duplicitních řádků**")
                st.caption("Vymaže všechny duplicitní záznamy podle prvního sloupce tabulky.")
                if st.button("Odstranit duplicity", key="btn_manual_dedup_action", help="Vymaže všechny duplicitní řádky podle prvního sloupce", use_container_width=True):
                    before_len = len(st.session_state.df)
                    st.session_state.df = st.session_state.df.drop_duplicates(subset=[columns[0]]).reset_index(drop=True)
                    after_len = len(st.session_state.df)
                    rem = before_len - after_len
                    if rem > 0:
                        st.success(f"Odstraněno {rem} duplicit.")
                    else:
                        st.info("V tabulce nebyly nalezeny žádné duplicity.")
                    st.rerun()

            with c_del_box:
                st.markdown("**2. Smazání konkrétního řádku**")
                st.caption("Vyberte položku ze seznamu a odstraňte ji z tabulky.")
                all_items = df[columns[0]].dropna().astype(str).unique().tolist()
                c_del_sel, c_del_b = st.columns([2.6, 1.4], gap="small")
                with c_del_sel:
                    item_to_delete = st.selectbox("Položka k odstranění:", options=all_items, key="sb_delete_single_item", label_visibility="collapsed")
                with c_del_b:
                    if st.button("Smazat řádek", key="btn_confirm_delete_row", use_container_width=True):
                        st.session_state.df = st.session_state.df[st.session_state.df[columns[0]].astype(str) != str(item_to_delete)].reset_index(drop=True)
                        st.success(f"Položka '{item_to_delete}' byla úspěšně odstraněna.")
                        st.rerun()

            st.markdown("<hr style='margin: 14px 0; border: none; border-top: 1px solid rgba(120, 150, 130, 0.25);'>", unsafe_allow_html=True)

            st.markdown("**3. Převedení na druhovou úroveň**")
            st.caption("Odstraní ze jmen taxonů poddruhy, variety a agregáty (subsp., var., agg.) a automaticky sloučí vzniklé duplicity.")
            col_clean1, col_clean2, col_clean3 = st.columns([3.2, 2.2, 0.6], gap="small")
            with col_clean1:
                clean_col_choice = st.selectbox("Sloupec se jmény k vyčištění:", options=columns, index=0, key="clean_col_choice")
            with col_clean2:
                st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                btn_clean_run = st.button("Převést na druhovou úroveň", key="btn_clean_run_species", help="Odstraní subsp., var., agg. a automaticky sloučí vzniklé duplicity", use_container_width=True)
            with col_clean3:
                st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                with st.popover("?", help="Co znamená převod na druhovou úroveň?"):
                    st.markdown("""
                    **Co tato funkce dělá?**
                    * Odstraní ze jmen taxonů poddruhy (`subsp.`, `ssp.`), variety (`var.`), formy (`f.`), agregáty (`agg.`), sekce (`sect.`) apod.
                    * Ponechá pouze základní binomické jméno (*Rod + druh*).

                    **Proč to použít?**
                    * Mezinárodní databáze (GBIF, POWO Kew, Animal Diversity Web, Wikipedie) často lokální středoevropské poddruhy neznají, ale pro základní druh najdou kompletní fotografie, popisy a mapy.
                    * Po převodu aplikace **automaticky sloučí duplicitní řádky**, takže v tabulce nezůstane stejný druh dvakrát.
                    """)

            if btn_clean_run:
                def clean_botanical_name(name):
                    if not name or pd.isna(name):
                        return name
                    name_str = str(name).strip()
                    cleaned = re.sub(r'\s+(subsp|ssp|var|f|agg|sect|nothosubsp)\.?(\s+.*|$)', '', name_str, flags=re.IGNORECASE)
                    return cleaned.strip()

                st.session_state.df[clean_col_choice] = st.session_state.df[clean_col_choice].apply(clean_botanical_name)
                len_pre_dedup = len(st.session_state.df)
                st.session_state.df = st.session_state.df.drop_duplicates(subset=[clean_col_choice]).reset_index(drop=True)
                dedup_diff = len_pre_dedup - len(st.session_state.df)

                succ_msg = "Jména byla úspěšně převedena na druhovou úroveň."
                if dedup_diff > 0:
                    succ_msg += f" Automaticky sloučeno {dedup_diff} vzniklých duplicitních řádků."
                st.success(succ_msg)
                st.rerun()

            st.markdown("<hr style='margin: 14px 0; border: none; border-top: 1px solid rgba(120, 150, 130, 0.25);'>", unsafe_allow_html=True)

            with st.expander("Sjednocení a převod nomenklatury (Synonymika / Pladias.cz / iNaturalist / Vlastní převodník)", expanded=False):
                st.markdown(
                    "Umožňuje sjednotit nebo převést vědecká jména na platnou nomenklaturu (např. Pladias $\\leftrightarrow$ iNaturalist, stará synonyma na platná jména) "
                    "pomocí dvousloupcové převodní tabulky (CSV nebo Excel)."
                )

                nom_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nomenclatures")
                os.makedirs(nom_dir, exist_ok=True)
                saved_nom_files = [f for f in os.listdir(nom_dir) if f.endswith(('.csv', '.xlsx', '.tsv'))]

                nom_col1, nom_col2 = st.columns([1.5, 2])
                with nom_col1:
                    nom_target_col = st.selectbox(
                        "Sloupec v načtené tabulce k převodu:",
                        options=columns,
                        index=0,
                        key="nom_target_col_select"
                    )

                    klic_p = get_local_dataset_path("klic_2019")
                    source_options = ["Nahrát soubor převodníku (CSV / Excel)..."]
                    if klic_p:
                        source_options.append("Klíč ke květeně ČR (Kaplan et al. 2019)")
                    source_options += [f"Knihovna: {f}" for f in saved_nom_files]

                    nom_source_choice = st.selectbox(
                        "Zdroj nomenklaturního převodníku:",
                        options=source_options,
                        key="nom_source_choice"
                    )

                map_df = None
                loaded_source_name = ""

                with nom_col2:
                    if nom_source_choice == "Klíč ke květeně ČR (Kaplan et al. 2019)":
                        klic_p = get_local_dataset_path("klic_2019")
                        try:
                            map_df = pd.read_excel(klic_p)
                            loaded_source_name = "Klíč ke květeně ČR (Kaplan et al. 2019)"
                            st.info(f"Načten checklist z Klíče ke květeně ČR: **{len(map_df)}** taxonů.")
                        except Exception as e:
                            st.error(f"Chyba při načítání Klíče ke květeně: {e}")
                    elif nom_source_choice.startswith("Nahrát"):
                        uploaded_map_file = st.file_uploader(
                            "Nahrajte převodní tabulku (2 sloupce: Původní jméno / Nové jméno)",
                            type=["csv", "xlsx", "tsv"],
                            key="nom_file_uploader"
                        )
                        if uploaded_map_file is not None:
                            try:
                                if uploaded_map_file.name.endswith('.csv'):
                                    try:
                                        map_df = pd.read_csv(uploaded_map_file)
                                        if len(map_df.columns) <= 1:
                                            uploaded_map_file.seek(0)
                                            map_df = pd.read_csv(uploaded_map_file, sep=';')
                                    except Exception:
                                        uploaded_map_file.seek(0)
                                        map_df = pd.read_csv(uploaded_map_file, sep='\t')
                                elif uploaded_map_file.name.endswith('.tsv'):
                                    map_df = pd.read_csv(uploaded_map_file, sep='\t')
                                else:
                                    map_df = pd.read_excel(uploaded_map_file)
                                loaded_source_name = uploaded_map_file.name
                            except Exception as e:
                                st.error(f"Chyba při čtení převodníku: {e}")
                    else:
                        chosen_filename = nom_source_choice.replace("Knihovna: ", "").strip()
                        chosen_path = os.path.join(nom_dir, chosen_filename)
                        if os.path.isfile(chosen_path):
                            try:
                                if chosen_filename.endswith('.csv'):
                                    map_df = pd.read_csv(chosen_path)
                                    if len(map_df.columns) <= 1:
                                        map_df = pd.read_csv(chosen_path, sep=';')
                                elif chosen_filename.endswith('.tsv'):
                                    map_df = pd.read_csv(chosen_path, sep='\t')
                                else:
                                    map_df = pd.read_excel(chosen_path)
                                loaded_source_name = chosen_filename
                                st.info(f"Načten převodník z knihovny: **{chosen_filename}** ({len(map_df)} záznamů).")
                            except Exception as e:
                                st.error(f"Chyba při načítání souboru {chosen_filename}: {e}")

                if map_df is not None and not map_df.empty:
                    map_cols = list(map_df.columns)
                    st.markdown("##### Nastavení mapování sloupců převodníku:")
                    m_col1, m_col2, m_col3 = st.columns([1.5, 1.5, 1.5])

                    if "NameLatKey2019" in map_cols or "NameLatDanihelka2012" in map_cols:
                        src_col_options = ["Chytré párování (všechna synonyma: Klíč 2019, Danihelka 2012 i Final)"] + map_cols
                    else:
                        src_col_options = map_cols

                    def_src_idx = 0
                    def_tgt_idx = 0
                    if "NameLatFinal" in map_cols:
                        def_tgt_idx = map_cols.index("NameLatFinal")
                    elif "Platné jméno" in map_cols:
                        def_tgt_idx = map_cols.index("Platné jméno")
                    elif len(map_cols) > 1:
                        def_tgt_idx = 1

                    with m_col1:
                        src_map_col = st.selectbox(
                            "Sloupec se starým / původním jménem (synonymem):",
                            options=src_col_options,
                            index=def_src_idx,
                            key="nom_src_map_col"
                        )
                    with m_col2:
                        tgt_map_col = st.selectbox(
                            "Sloupec s novým / platným jménem:",
                            options=map_cols,
                            index=def_tgt_idx,
                            key="nom_tgt_map_col"
                        )
                    with m_col3:
                        dest_mode = st.radio(
                            "Cíl převodu:",
                            ["Nahradit hodnoty ve stávajícím sloupci", "Vytvořit nový sloupec"],
                            key="nom_dest_mode"
                        )

                    new_col_name = ""
                    if dest_mode == "Vytvořit nový sloupec":
                        new_col_name = st.text_input(
                            "Název nového sloupce:",
                            value=f"[Sjednoceno] {nom_target_col}",
                            key="nom_new_col_name"
                        )

                    opt_col1, opt_col2 = st.columns([2, 2])
                    with opt_col1:
                        nom_case_ins = st.checkbox(
                            "Ignorovat velikost písmen (case-insensitive)",
                            value=True,
                            key="nom_case_ins"
                        )
                        nom_strip_auth = st.checkbox(
                            "Očistit autorské zkratky a infraspecifické taxony při párování (L., DC., subsp., var.)",
                            value=True,
                            key="nom_strip_auth"
                        )
                    with opt_col2:
                        if nom_source_choice.startswith("Nahrát"):
                            save_lib_name = st.text_input(
                                "Uložit převodník do trvalé knihovny jako (např. pladias_cz_to_inat):",
                                value=os.path.splitext(loaded_source_name)[0] if loaded_source_name else "",
                                key="nom_save_lib_name"
                            )
                            if st.button("Uložit do knihovny", key="btn_save_nom_lib"):
                                if save_lib_name.strip():
                                    safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', save_lib_name.strip()) + ".csv"
                                    dest_save_path = os.path.join(nom_dir, safe_name)
                                    try:
                                        save_cols = [c for c in [src_map_col, tgt_map_col] if c in map_df.columns]
                                        if not save_cols:
                                            save_cols = map_df.columns[:2]
                                        map_df[save_cols].to_csv(dest_save_path, index=False, encoding="utf-8-sig")
                                        st.success(f"Převodník byl uložen do knihovny jako `{safe_name}`.")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Nepodařilo se uložit převodník: {e}")

                    nom_online_synonyms = st.checkbox(
                        "Zahrnout online databázi synonym (GBIF Backbone Taxonomy & iNaturalist API) pro stará synonyma (např. Lychnis viscaria -> Viscaria vulgaris)",
                        value=True,
                        key="nom_online_synonyms",
                        help="Pokud název není nalezen v lokálním checklistu, vyhledá jeho platný mezinárodní status v taxonomických databázích."
                    )

                    if st.button("Provést převod a sjednocení nomenklatury", key="btn_run_nomenclature_conversion"):
                        def _norm_k(s, strip_a):
                            if not s or pd.isna(s):
                                return ""
                            st_str = str(s).strip().replace('×', '').replace('x ', ' ')
                            if strip_a:
                                st_str = re.sub(r'\(.*?\)', '', st_str)
                                st_str = re.sub(r'\s+(subsp|ssp|var|f|agg|sect|nothosubsp)\.?(\s+.*|$)', '', st_str, flags=re.IGNORECASE)
                                parts = st_str.split()
                                if len(parts) >= 2:
                                    st_str = f"{parts[0]} {parts[1]}"
                            return re.sub(r'\s+', ' ', st_str).strip().lower()

                        mapping_exact = {}
                        mapping_lower = {}
                        mapping_norm = {}

                        is_smart_multi = str(src_map_col).startswith("Chytré párování")
                        if is_smart_multi:
                            syn_check_cols = [c for c in ["NameLatKey2019", "NameLatDanihelka2012", "NameLatFinal"] if c in map_df.columns]
                            if not syn_check_cols:
                                syn_check_cols = [map_cols[0]]
                        else:
                            syn_check_cols = [src_map_col] if src_map_col in map_df.columns else [map_cols[0]]

                        for _, r in map_df.iterrows():
                            t_val = str(r[tgt_map_col]).strip() if pd.notna(r[tgt_map_col]) else ""
                            if not t_val:
                                continue
                            for sc in syn_check_cols:
                                s_val = str(r[sc]).strip() if pd.notna(r[sc]) else ""
                                if s_val:
                                    mapping_exact[s_val] = t_val
                                    mapping_lower[s_val.lower()] = t_val
                                    if nom_strip_auth:
                                        nk = _norm_k(s_val, True)
                                        if nk:
                                            mapping_norm[nk] = t_val

                        builtin_cz_synonyms = {
                            "lychnis viscaria": "Viscaria vulgaris",
                            "stipa calamagrostis": "Achnatherum calamagrostis",
                            "taraxacum officinale": "Taraxacum sect. Taraxacum",
                            "centaurea jacea": "Centaurea jacea",
                            "steris viscaria": "Viscaria vulgaris"
                        }

                        def query_online_synonym(name_to_check):
                            if not nom_online_synonyms:
                                return None
                            clean = re.sub(r'\s*\(.*?\)\s*', ' ', str(name_to_check)).strip()
                            clean = re.sub(r'\s+(subsp|ssp|var|f)\.?\s+.*$', '', clean, flags=re.IGNORECASE).strip()
                            if clean.lower() in builtin_cz_synonyms:
                                return builtin_cz_synonyms[clean.lower()]
                            try:
                                url = f"https://api.gbif.org/v1/species/match?name={urllib.parse.quote(clean)}"
                                headers = {'User-Agent': 'Mozilla/5.0'}
                                r = requests.get(url, headers=headers, timeout=4)
                                if r.status_code == 200:
                                    data = r.json()
                                    if data.get('status') == 'SYNONYM' and data.get('accepted'):
                                        return data.get('accepted')
                                    elif data.get('species'):
                                        return data.get('species')
                            except Exception:
                                pass
                            return None

                        target_series = st.session_state.df[nom_target_col]
                        converted_values = []
                        change_log = []

                        for r_idx, val in enumerate(target_series):
                            val_str = str(val).strip() if pd.notna(val) else ""
                            res_val = val
                            matched = False

                            if val_str in mapping_exact:
                                res_val = mapping_exact[val_str]
                                matched = True
                            elif nom_case_ins and val_str.lower() in mapping_lower:
                                res_val = mapping_lower[val_str.lower()]
                                matched = True
                            elif nom_strip_auth:
                                nk = _norm_k(val_str, True)
                                if nk in mapping_norm:
                                    res_val = mapping_norm[nk]
                                    matched = True

                            if not matched and nom_online_synonyms and val_str:
                                online_res = query_online_synonym(val_str)
                                if online_res and online_res.lower() != val_str.lower():
                                    res_val = online_res
                                    matched = True

                            if matched and str(res_val).strip() != val_str:
                                change_log.append({
                                    "Řádek": r_idx + 1,
                                    "Původní hodnota": val,
                                    "Nová platná hodnota": res_val
                                })
                            converted_values.append(res_val)

                        if dest_mode == "Nahradit hodnoty ve stávajícím sloupci":
                            st.session_state.df[nom_target_col] = converted_values
                        else:
                            final_col = new_col_name.strip() if new_col_name.strip() else f"[Sjednoceno] {nom_target_col}"
                            st.session_state.df[final_col] = converted_values

                        st.session_state.nom_last_report = {
                            "total": len(target_series),
                            "changed_count": len(change_log),
                            "changes": change_log
                        }
                        st.success(f"Převod dokončen! Úspěšně sjednoceno/nahrazeno: **{len(change_log)}** z **{len(target_series)}** položek.")
                        st.rerun()

                if "nom_last_report" in st.session_state and st.session_state.nom_last_report:
                    rep = st.session_state.nom_last_report
                    st.markdown(f"**Výsledek posledního převodu:** Sjednoceno {rep['changed_count']} položek z celkových {rep['total']} řádků.")
                    if rep["changes"]:
                        rep_df = pd.DataFrame(rep["changes"])
                        st.dataframe(rep_df, **_compat_width())

            with st.expander("Vlastní fotografie a multimédia", expanded=False):
                if st.session_state.get("custom_photo_pairing_msg"):
                    st.success(f"{st.session_state['custom_photo_pairing_msg']}")
                st.markdown(
                    "Umožňuje nahrát vlastní fotografie z vašeho počítače (např. terénní snímky mechorostů, herbářové položky nebo schémata) "
                    "a přiřadit je ke konkrétním řádkům v tabulce."
                )

                custom_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom_media")
                os.makedirs(custom_dir, exist_ok=True)

                c_cust_tab1, c_cust_tab2 = st.tabs(["1. Přiřazení ke konkrétnímu druhu", "2. Hromadné nahrání podle názvu souboru"])

                with c_cust_tab1:
                    col_sp_pick, col_sp_up = st.columns([1.5, 2])
                    with col_sp_pick:
                        target_species_list = df[columns[0]].dropna().astype(str).unique().tolist()
                        selected_target_species = st.selectbox(
                            "Vyberte druh pro přiřazení fotografie:",
                            options=target_species_list,
                            key="custom_pick_species_select"
                        )
                        custom_photo_caption = st.text_input(
                            "Popisek / autor fotografie (např. Vlastní foto – detail květu):",
                            value="Vlastní foto",
                            key="custom_photo_caption_input"
                        )

                        if "[Vlastní] Fotografie" in st.session_state.df.columns:
                            sp_match_mask = st.session_state.df[columns[0]].astype(str).str.strip() == str(selected_target_species).strip()
                            existing_entries_str = ""
                            for idx_m in st.session_state.df[sp_match_mask].index:
                                existing_entries_str = str(st.session_state.df.at[idx_m, "[Vlastní] Fotografie"]).strip()
                                break

                            if existing_entries_str and existing_entries_str != "nan":
                                existing_items = [e.strip() for e in existing_entries_str.split(';') if e.strip()]
                                st.markdown(f"**Již přiřazené fotografie ({len(existing_items)}):**")
                                for e_idx, e_item in enumerate(existing_items):
                                    e_path = e_item.split('|')[0].strip() if '|' in e_item else e_item
                                    e_cap = e_item.split('|')[1].strip() if '|' in e_item else ""
                                    c_thumb, c_act = st.columns([3, 1])
                                    with c_thumb:
                                        if os.path.isfile(e_path):
                                            st.image(e_path, width=90, caption=e_cap)
                                        else:
                                            st.caption(f"{os.path.basename(e_path)} ({e_cap})")
                                    with c_act:
                                        if st.button("Smazat", key=f"del_cust_img_{selected_target_species}_{e_idx}", help="Odebrat tuto fotografii"):
                                            new_items = [it for it_idx, it in enumerate(existing_items) if it_idx != e_idx]
                                            new_str = "; ".join(new_items)
                                            for idx_m in st.session_state.df[sp_match_mask].index:
                                                st.session_state.df.at[idx_m, "[Vlastní] Fotografie"] = new_str
                                            st.rerun()
                                if st.button("Vymazat všechny fotky tohoto druhu", key=f"clear_all_cust_{selected_target_species}"):
                                    for idx_m in st.session_state.df[sp_match_mask].index:
                                        st.session_state.df.at[idx_m, "[Vlastní] Fotografie"] = ""
                                    st.rerun()

                    with col_sp_up:
                        uploaded_single_photos = st.file_uploader(
                            f"Vyberte nové obrázky pro druh: {selected_target_species}",
                            type=["jpg", "jpeg", "png", "webp"],
                            accept_multiple_files=True,
                            key="custom_single_uploader",
                            help="Můžete vybrat i více fotek najednou – všechny se připojí k tomuto druhu."
                        )
                        if uploaded_single_photos and st.button("Přidat / Přiřadit fotografie k druhu", key="btn_assign_custom_single"):
                            saved_paths = []
                            for up_f in uploaded_single_photos:
                                safe_base = slugify(selected_target_species)
                                dest_fn = f"{safe_base}_{hashlib.md5(up_f.name.encode()).hexdigest()[:6]}_{up_f.name}"
                                dest_path = os.path.join(custom_dir, dest_fn)
                                with open(dest_path, "wb") as f_out:
                                    f_out.write(up_f.getvalue())
                                saved_paths.append(f"{dest_path}|{custom_photo_caption.strip()}")

                            if "[Vlastní] Fotografie" not in st.session_state.df.columns:
                                st.session_state.df["[Vlastní] Fotografie"] = ""

                            sp_match_mask = st.session_state.df[columns[0]].astype(str).str.strip() == str(selected_target_species).strip()
                            for idx_m in st.session_state.df[sp_match_mask].index:
                                curr_val = str(st.session_state.df.at[idx_m, "[Vlastní] Fotografie"]).strip()
                                new_entries = "; ".join(saved_paths)
                                if curr_val and curr_val != "nan":
                                    st.session_state.df.at[idx_m, "[Vlastní] Fotografie"] = f"{curr_val}; {new_entries}"
                                else:
                                    st.session_state.df.at[idx_m, "[Vlastní] Fotografie"] = new_entries

                            succ_msg = f"K druhu '{selected_target_species}' bylo úspěšně přiřazeno {len(saved_paths)} fotografií."
                            st.session_state["custom_photo_pairing_msg"] = succ_msg
                            st.toast(f"{succ_msg}")
                            st.rerun()

                with c_cust_tab2:
                    st.markdown("Nahrajte více fotografií najednou. Aplikace automaticky spáruje název souboru (např. `Polytrichum_formosum.jpg` nebo `sedmikraska.png`) s odpovídajícím druhem v tabulce.")
                    uploaded_batch_photos = st.file_uploader(
                        "Vyberte fotografie pro hromadné spárování:",
                        type=["jpg", "jpeg", "png", "webp"],
                        accept_multiple_files=True,
                        key="custom_batch_uploader"
                    )
                    batch_caption = st.text_input("Výchozí popisek pro spárované fotografie:", value="Vlastní foto", key="custom_batch_caption")
                    if uploaded_batch_photos and st.button("Provést hromadné spárování", key="btn_run_custom_batch"):
                        matched_count = 0
                        if "[Vlastní] Fotografie" not in st.session_state.df.columns:
                            st.session_state.df["[Vlastní] Fotografie"] = ""

                        for up_f in uploaded_batch_photos:

                            f_stem = os.path.splitext(up_f.name)[0]
                            f_clean = re.sub(r'[^a-zA-Z0-9]', ' ', f_stem).strip().lower()

                            for r_idx, r_val in enumerate(st.session_state.df[columns[0]]):
                                r_clean = re.sub(r'[^a-zA-Z0-9]', ' ', str(r_val)).strip().lower()
                                if r_clean and (r_clean in f_clean or f_clean in r_clean or f_clean.startswith(r_clean.split()[0])):
                                    dest_fn = f"batch_{slugify(str(r_val))[:20]}_{up_f.name}"
                                    dest_path = os.path.join(custom_dir, dest_fn)
                                    with open(dest_path, "wb") as f_out:
                                        f_out.write(up_f.getvalue())

                                    entry = f"{dest_path}|{batch_caption.strip()}"
                                    curr_val = str(st.session_state.df.at[r_idx, "[Vlastní] Fotografie"]).strip()
                                    if curr_val and curr_val != "nan":
                                        st.session_state.df.at[r_idx, "[Vlastní] Fotografie"] = f"{curr_val}; {entry}"
                                    else:
                                        st.session_state.df.at[r_idx, "[Vlastní] Fotografie"] = entry
                                    matched_count += 1
                                    break

                        succ_msg = f"Hromadné párování dokončeno! Úspěšně přiřazeno {matched_count} z {len(uploaded_batch_photos)} fotografií."
                        st.session_state["custom_photo_pairing_msg"] = succ_msg
                        st.toast(f"{succ_msg}")
                        st.rerun()

        st.markdown("---")

        ALL_BIO_KEYS = [
            "enable_inat", "enable_inat_map", "enable_desc", "enable_gbif", "enable_wiki_img", "enable_wiki_link",
            "enable_pladias_photos", "enable_pladias_map", "enable_pladias", "enable_pladias_tax",
            "enable_gbif_kvet", "enable_gbif_list", "enable_gbif_herbar",
            "enable_bryo_photos", "enable_bryo_desc", "enable_bryo_link",
            "enable_mykologie_img", "enable_mykologie_desc", "enable_mykologie_link", "enable_gbif_fungi",
            "enable_dalibor_photos", "enable_dalibor_desc", "enable_dalibor_link",
            "enable_diatombase_taxon", "enable_diatombase_link", "enable_algaebase_link",
            "enable_gbif_zoo", "enable_bird_sounds",
            "enable_nepuvodni", "enable_biotopy", "enable_ellenberg", "enable_cerveny_seznam", "enable_cerveny_seznam_url", "enable_kvetena_cr",
            "enable_adw_desc", "enable_adw_link", "enable_gbif_desc", "enable_powo_desc", "enable_powo_link", "enable_eol_link"
        ]
        ALL_LANG_KEYS = ["enable_trans", "enable_tts", "enable_latin_tts", "enable_latin_phonetic", "enable_dict"]
        ALL_GEO_KEYS = ["enable_country"]
        ALL_MODULE_KEYS = ALL_BIO_KEYS + ALL_LANG_KEYS + ALL_GEO_KEYS

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
                "enable_gbif_herbar": False,
                "gbif_photo_col": columns[0] if columns else "",
                "enable_pladias": False,
                "pladias_col": columns[0] if columns else "",
                "enable_pladias_tax": False,
                "enable_pladias_czech_name": True,
                "pladias_tax_col": columns[0] if columns else "",
                "enable_pladias_photos": False,
                "pladias_photos_col": columns[0] if columns else "",
                "pladias_photos_max": 3,
                "pladias_photos_parts": [],
                "pladias_photos_fallback": False,
                "enable_pladias_map": False,
                "pladias_map_col": columns[0] if columns else "",
                "enable_klic_2019": False,
                "klic_2019_col": columns[0] if columns else "",
                "enable_nepuvodni": False,
                "nepuvodni_col": columns[0] if columns else "",
                "enable_biotopy": False,
                "biotopy_col": columns[0] if columns else "",
                "enable_ellenberg": False,
                "ellenberg_col": columns[0] if columns else "",
                "enable_cerveny_seznam": False,
                "enable_cerveny_seznam_url": False,
                "cerveny_seznam_col": columns[0] if columns else "",
                "enable_kvetena_cr": False,
                "kvetena_cr_col": columns[0] if columns else "",
                "kvetena_cr_max_chars": 450,
                "enable_bryo_photos": False,
                "bryo_photo_col": columns[0] if columns else "",
                "bryo_photos_max": 3,
                "enable_bryo_desc": False,
                "bryo_desc_col": columns[0] if columns else "",
                "enable_bryo_link": False,
                "bryo_link_col": columns[0] if columns else "",
                "enable_mykologie_img": False,
                "mykologie_img_col": columns[0] if columns else "",
                "mykologie_img_max": 3,
                "enable_mykologie_desc": False,
                "mykologie_desc_col": columns[0] if columns else "",
                "enable_mykologie_link": False,
                "mykologie_link_col": columns[0] if columns else "",
                "enable_dalibor_photos": False,
                "dalibor_photos_col": columns[0] if columns else "",
                "dalibor_photos_max": 3,
                "enable_dalibor_desc": False,
                "dalibor_desc_col": columns[0] if columns else "",
                "enable_dalibor_link": False,
                "dalibor_link_col": columns[0] if columns else "",
                "diatombase_taxon_col": columns[0] if columns else "",
                "enable_diatombase_taxon": False,
                "enable_diatombase_link": False,
                "diatombase_link_col": columns[0] if columns else "",
                "enable_algaebase_link": False,
                "algaebase_link_col": columns[0] if columns else "",
                "enable_gbif_fungi": False,
                "gbif_fungi_col": columns[0] if columns else "",
                "gbif_fungi_max": 3,
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
                "enable_latin_tts": False,
                "latin_tts_col": columns[0] if columns else "",
                "enable_latin_phonetic": False,
                "latin_phonetic_col": columns[0] if columns else "",
                "enable_dict": False,
                "dict_col": columns[0] if columns else "",
                "enable_country": False,
                "country_col": columns[0] if columns else ""
            }

        cfg = st.session_state.api_config

    with st.expander("3. Výběr modulů pro obohacení dat", expanded=False):

        with st.container(border=True):
            col_p_sel, col_p_photos = st.columns([3.5, 2.5], gap="large")
        with col_p_sel:
            preset_opts = [
                "-- Vlastní výběr nástrojů --",
                "Kytky (Botanika) – Jednoduchý mód (foto na líci; jména, čeleď a odkaz na rubu)",
                "Kytky (Botanika) – Pokročilý mód (všechny zdroje: habitus/květ/list, mapa ČR, Květena ČR, AOPK, Ellenberg, Biotopy...)",
                "Houby – Jednoduchý mód (foto na líci; jména, čeleď a profil na rubu)",
                "Houby – Pokročilý mód (Mykologie.net popis/jedlost, Mushroom Color Atlas, Červený seznam, GBIF...)",
                "Mechorosty – Jednoduchý mód (foto na líci; jména, čeleď a odkaz na rubu)",
                "Mechorosty – Pokročilý mód (Mechorosty ČR popis/ekologie, Červený seznam, GBIF...)",
                "Lišejníky – Jednoduchý mód (foto na líci; jména, čeleď a odkaz DaLiBor na rubu)",
                "Lišejníky – Pokročilý mód (DaLiBor foto/profil/ekologie/chemismus, Červený seznam, GBIF...)",
                "Řasy & Rozsivky – Jednoduchý mód (foto na líci; jména, čeleď a odkaz na rubu)",
                "Řasy & Rozsivky – Pokročilý mód (DiatomBase/AlgaeBase taxonomie WoRMS, popis, iNat...)",
                "Zoologie – Jednoduchý mód (foto na líci; jména, čeleď a odkaz na rubu)",
                "Zoologie – Pokročilý mód (foto, hlasy ptáků Xeno-canto, Červený seznam živočichů, GBIF, Wikipedia...)"
            ]
            chosen_preset = st.selectbox(
                "Profil obohacení pro kategorii (1 kliknutí):",
                options=preset_opts,
                index=0,
                key="w_category_preset_select",
                help="Jednoduchý mód zapne fotografie na líci a základní identifikační údaje s odkazem na rubu. Pokročilý mód aktivuje veškeré dostupné odborné registry a popisy pro danou kategorii."
            )

            if chosen_preset != st.session_state.get("_prev_applied_preset", ""):
                if chosen_preset != "-- Vlastní výběr nástrojů --":

                    for k_rst in ALL_BIO_KEYS:
                        cfg[k_rst] = False
                        st.session_state[f"w_{k_rst}"] = False

                    if "Kytky" in chosen_preset:
                        if "Jednoduchý" in chosen_preset:
                            cfg["enable_pladias_photos"] = True
                            cfg["enable_gbif"] = True
                            cfg["enable_pladias"] = True
                            st.session_state["w_enable_pladias_photos"] = True
                            st.session_state["w_enable_gbif"] = True
                            st.session_state["w_enable_pladias"] = True
                            st.session_state["front_cols_ordered"] = [c for c in columns if "pladias" in c.lower() and "foto" in c.lower() or "celá" in c.lower()] or ([columns[0]] if columns else [])
                            st.session_state["back_cols_ordered"] = [c for c in columns if c in [columns[0], "[GBIF] Čeleď", "[Pladias] Profil taxonu", "[Taxonomie] České jméno"]]
                        else:
                            for k_adv in ["enable_pladias_photos", "enable_pladias_map", "enable_pladias", "enable_pladias_tax",
                                          "enable_kvetena_cr", "enable_cerveny_seznam", "enable_ellenberg", "enable_biotopy",
                                          "enable_nepuvodni", "enable_gbif", "enable_desc", "enable_inat_map"]:
                                cfg[k_adv] = True
                                st.session_state[f"w_{k_adv}"] = True
                    elif "Houby" in chosen_preset:
                        if "Jednoduchý" in chosen_preset:
                            cfg["enable_mykologie_img"] = True
                            cfg["enable_gbif"] = True
                            cfg["enable_mykologie_link"] = True
                            st.session_state["w_enable_mykologie_img"] = True
                            st.session_state["w_enable_gbif"] = True
                            st.session_state["w_enable_mykologie_link"] = True
                        else:
                            for k_adv in ["enable_mykologie_img", "enable_mykologie_desc", "enable_mykologie_link",
                                          "enable_mushroom_color_atlas", "enable_cerveny_seznam", "enable_gbif", "enable_desc", "enable_inat_map"]:
                                cfg[k_adv] = True
                                st.session_state[f"w_{k_adv}"] = True
                    elif "Mechorosty" in chosen_preset:
                        if "Jednoduchý" in chosen_preset:
                            cfg["enable_bryo_photos"] = True
                            cfg["enable_gbif"] = True
                            cfg["enable_bryo_link"] = True
                            st.session_state["w_enable_bryo_photos"] = True
                            st.session_state["w_enable_gbif"] = True
                            st.session_state["w_enable_bryo_link"] = True
                        else:
                            for k_adv in ["enable_bryo_photos", "enable_bryo_desc", "enable_bryo_link", "enable_cerveny_seznam", "enable_gbif", "enable_inat_map"]:
                                cfg[k_adv] = True
                                st.session_state[f"w_{k_adv}"] = True
                    elif "Lišejníky" in chosen_preset:
                        if "Jednoduchý" in chosen_preset:
                            cfg["enable_dalibor_photos"] = True
                            cfg["enable_gbif"] = True
                            cfg["enable_dalibor_link"] = True
                            st.session_state["w_enable_dalibor_photos"] = True
                            st.session_state["w_enable_gbif"] = True
                            st.session_state["w_enable_dalibor_link"] = True
                        else:
                            for k_adv in ["enable_dalibor_photos", "enable_dalibor_desc", "enable_dalibor_link", "enable_cerveny_seznam", "enable_gbif", "enable_inat_map"]:
                                cfg[k_adv] = True
                                st.session_state[f"w_{k_adv}"] = True
                    elif "Řasy" in chosen_preset:
                        if "Jednoduchý" in chosen_preset:
                            cfg["enable_inat"] = True
                            cfg["enable_gbif"] = True
                            cfg["enable_diatombase_link"] = True
                            cfg["enable_algaebase_link"] = True
                            st.session_state["w_enable_inat"] = True
                            st.session_state["w_enable_gbif"] = True
                            st.session_state["w_enable_diatombase_link"] = True
                            st.session_state["w_enable_algaebase_link"] = True
                        else:
                            for k_adv in ["enable_inat", "enable_gbif", "enable_diatombase_taxon", "enable_diatombase_link", "enable_algaebase_link", "enable_desc", "enable_inat_map"]:
                                cfg[k_adv] = True
                                st.session_state[f"w_{k_adv}"] = True
                    elif "Zoologie" in chosen_preset:
                        if "Jednoduchý" in chosen_preset:
                            cfg["enable_gbif_zoo"] = True
                            cfg["enable_gbif"] = True
                            cfg["enable_wiki_link"] = True
                            st.session_state["w_enable_gbif_zoo"] = True
                            st.session_state["w_enable_gbif"] = True
                            st.session_state["w_enable_wiki_link"] = True
                        else:
                            for k_adv in ["enable_gbif_zoo", "enable_bird_sounds", "enable_cerveny_seznam", "enable_gbif", "enable_desc", "enable_adw_desc", "enable_inat_map"]:
                                cfg[k_adv] = True
                                st.session_state[f"w_{k_adv}"] = True

                    st.session_state["_prev_applied_preset"] = chosen_preset
                    st.rerun()

            with col_p_photos:
                st.markdown("**Limit fotografií**")
                if "_prev_bulk_slider" not in st.session_state:
                    st.session_state["_prev_bulk_slider"] = int(cfg.get("pladias_photos_max", 3))

                bulk_photo_count = st.slider(
                    "Počet fotek na položku:",
                    min_value=1,
                    max_value=6,
                    value=st.session_state["_prev_bulk_slider"],
                    key="w_bulk_photo_slider",
                    help="Hromadně nastaví maximální limit fotografií pro všechny povolené fotomoduly (Pladias.cz, iNaturalist, GBIF, Mykologie, DaLiBor...)"
                )

                if bulk_photo_count != st.session_state["_prev_bulk_slider"]:
                    st.session_state["_prev_bulk_slider"] = bulk_photo_count
                    cfg["pladias_photos_max"] = bulk_photo_count
                    cfg["inat_max"] = bulk_photo_count
                    cfg["wiki_max"] = bulk_photo_count
                    cfg["mykologie_img_max"] = bulk_photo_count
                    cfg["gbif_fungi_max"] = bulk_photo_count
                    cfg["dalibor_photos_max"] = bulk_photo_count
                    cfg["bryo_photos_max"] = bulk_photo_count
                    cfg["gbif_zoo_max"] = bulk_photo_count
                    for _k in ["w_pladias_photos_max", "w_inat_max", "w_wiki_max", "w_mykologie_img_max", "w_gbif_fungi_max", "w_dalibor_photos_max", "w_bryo_photos_max", "w_gbif_zoo_max"]:
                        st.session_state[_k] = bulk_photo_count

        col_keys = [
            "inat_col", "gbif_col", "gbif_photo_col", "desc_col", "pladias_col", "pladias_tax_col", "pladias_photos_col", "pladias_map_col",
            "klic_2019_col", "nepuvodni_col", "biotopy_col", "ellenberg_col", "cerveny_seznam_col", "kvetena_cr_col",
            "bryo_photo_col", "bryo_desc_col", "bryo_link_col",
            "mykologie_img_col", "mykologie_desc_col", "mykologie_link_col",
            "dalibor_photos_col", "dalibor_desc_col", "dalibor_link_col",
            "diatombase_taxon_col", "diatombase_link_col", "algaebase_link_col",
            "gbif_fungi_col", "gbif_zoo_col", "bird_sounds_col",
            "adw_col", "gbif_desc_col", "powo_col", "eol_col",
            "wiki_link_col", "wiki_col",
            "trans_col", "tts_col", "latin_tts_col", "latin_phonetic_col", "dict_col", "country_col"
        ]
        for col_key in col_keys:
            if col_key not in cfg or cfg[col_key] not in columns:
                cfg[col_key] = columns[0] if columns else ""

        languages = {
            "Angličtina": "en", "Čeština": "cs", "Němčina": "de",
            "Španělština": "es", "Francouzština": "fr", "Italština": "it", "Ruština": "ru", "Latina": "la"
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

        col_t_title, col_t_chk = st.columns([3.5, 1.5])
        with col_t_title:
            st.markdown(f"#### {selected_topic} – Moduly")
        with col_t_chk:
            topic_keys = ALL_BIO_KEYS if selected_topic == "Biologie" else (ALL_LANG_KEYS if selected_topic == "Jazyky" else ALL_GEO_KEYS)
            render_category_select_all_checkbox(f"topic_{selected_topic}", topic_keys)
        if selected_topic == "Biologie":

            tab_obecna, tab_botanika, tab_mechorosty, tab_houby, tab_lisejniky, tab_rasy, tab_zoologie, tab_registry = st.tabs([
                "Obecná biologie",
                "Botanika",
                "Mechorosty",
                "Houby",
                "Lišejníky",
                "Řasy & Rozsivky",
                "Zoologie",
                "Registry ČR"
            ])

            with tab_obecna:
                c_ob_t, c_ob_chk = st.columns([3.5, 1.5])
                with c_ob_t:
                    st.markdown("##### Obecná nastavení biologie")
                with c_ob_chk:
                    keys_obecna = ["enable_inat", "enable_inat_map", "enable_desc", "enable_gbif", "enable_wiki_img", "enable_wiki_link"]
                    render_category_select_all_checkbox("tab_obecna", keys_obecna)

                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    cfg["enable_inat"] = st.checkbox(
                        "iNaturalist (České jméno & Obrázky)",
                        value=cfg.get("enable_inat", False),
                        key="w_enable_inat"
                    )
                    cfg["enable_inat_map"] = st.checkbox(
                        "iNaturalist mapa pozorování",
                        value=cfg.get("enable_inat_map", False),
                        key="w_enable_inat_map",
                        help="Vygeneruje přímý odkaz a živou mapu pozorování druhu z iNaturalist s možností vlastního územního filtru."
                    )
                    if cfg.get("enable_inat_map", False):
                        inat_preset_options = [
                            "Česká republika (celá ČR)",
                            "Plzeňský kraj",
                            "Hlavní město Praha",
                            "Středočeský kraj",
                            "Jihočeský kraj",
                            "Karlovarský kraj",
                            "Ústecký kraj",
                            "Liberecký kraj",
                            "Královéhradecký kraj",
                            "Pardubický kraj",
                            "Kraj Vysočina",
                            "Jihomoravský kraj",
                            "Olomoucký kraj",
                            "Zlínský kraj",
                            "Moravskoslezský kraj",
                            "Slovensko",
                            "Německo",
                            "Rakousko",
                            "Polsko",
                            "Celý svět (bez filtru)",
                            "Vlastní území (okres, město, NP...)"
                        ]
                        current_place_val = cfg.get("inat_place_opt", "Česká republika (celá ČR)")
                        place_idx = 0
                        for _pi, _po in enumerate(inat_preset_options):
                            if _po == current_place_val or (current_place_val.startswith("Plzeň") and "Plzeň" in _po):
                                place_idx = _pi
                                break
                        inat_place_opt = st.selectbox(
                            "Územní filtr pro pozorování iNaturalist:",
                            options=inat_preset_options,
                            index=place_idx,
                            key="w_inat_place_opt"
                        )
                        cfg["inat_place_opt"] = inat_place_opt
                        if inat_place_opt.startswith("Vlastní"):
                            cfg["inat_custom_place"] = st.text_input(
                                "Zadejte název území (např. Benešov, Klatovy, Šumava, Krkonoše):",
                                value=cfg.get("inat_custom_place", "Benešov"),
                                key="w_inat_custom_place"
                            )
                            active_query = cfg.get("inat_custom_place", "")
                        else:
                            active_query = inat_place_opt
                        res_pid = resolve_inat_place_id(active_query)
                        pid_desc = f"ID území iNaturalist: **{res_pid}**" if res_pid else "Bez územního omezení (celosvětově)"
                        st.caption(f"Aktivní územní filtr: {pid_desc}")
                    if cfg.get("enable_inat", False) or cfg.get("enable_inat_map", False):
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
                    if cfg.get("enable_inat", False):
                        cfg["inat_max"] = st.slider(
                            "Max fotek z iNat na řádek",
                            1, 5,
                            value=cfg.get("inat_max", 4),
                            key="w_inat_max"
                        )

                    st.markdown("---")
                    cfg["enable_desc"] = st.checkbox(
                        "Stáhnout popis druhu z Wikipedie",
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
                        st.caption("Stáhne anglický popis z Wikipedie – funguje pro rostliny i živočichy.")

                with col_b2:
                    cfg["enable_gbif"] = st.checkbox(
                        "GBIF taxonomie",
                        value=cfg.get("enable_gbif", False),
                        key="w_enable_gbif",
                        help="Doplní vědecké taxonomické zařazení z globální databáze GBIF do sloupců [GBIF] Říše, [GBIF] Kmen atd."
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
                        "Wikimedia Commons vyhledávač obrázků",
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
                        "Odkaz na Wikipedii",
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

            with tab_botanika:
                c_bt_t, c_bt_chk = st.columns([3.5, 1.5])
                with c_bt_t:
                    st.markdown("##### Specifická nastavení pro botaniku (Rostliny)")
                with c_bt_chk:
                    keys_botanika = ["enable_pladias_photos", "enable_pladias_map", "enable_pladias", "enable_pladias_tax", "enable_gbif_kvet", "enable_gbif_list", "enable_gbif_herbar"]
                    render_category_select_all_checkbox("tab_botanika", keys_botanika)

                cfg["enable_pladias_tax"] = st.checkbox(
                    "Pladias.cz taxonomie",
                    value=cfg.get("enable_pladias_tax", False),
                    key="w_enable_pladias_tax",
                    help="Stáhne českou botanickou taxonomii z portálu Pladias.cz (Klíč / Květena ČR / Danihelka 2012) odpovídající českému školnímu pensu."
                )
                if cfg.get("enable_pladias_tax", False):
                    pladias_tax_col_val = cfg.get("pladias_tax_col", columns[0])
                    pladias_tax_col_idx = columns.index(pladias_tax_col_val) if pladias_tax_col_val in columns else 0
                    cfg["pladias_tax_col"] = st.selectbox(
                        "Sloupec s vědeckým jménem pro Pladias.cz taxonomii:",
                        options=columns,
                        index=pladias_tax_col_idx,
                        key="w_pladias_tax_col"
                    )
                    cfg["enable_pladias_czech_name"] = st.checkbox(
                        "Stáhnout také české jméno druhu z Pladias.cz",
                        value=cfg.get("enable_pladias_czech_name", True),
                        key="w_enable_pladias_czech_name",
                        help="Uloží oficiální české jméno rostliny z portálu Pladias.cz do sloupce [Pladias] České jméno a doplní jej i do prázdných položek sloupce České jméno."
                    )

                cfg["enable_pladias_photos"] = st.checkbox(
                    "Fotky z Pladias.cz",
                    value=cfg.get("enable_pladias_photos", False),
                    key="w_enable_pladias_photos"
                )
                if cfg.get("enable_pladias_photos", False):
                    pladias_photos_col_val = cfg.get("pladias_photos_col", columns[0])
                    try:
                        pladias_photos_col_idx = columns.index(pladias_photos_col_val)
                    except ValueError:
                        pladias_photos_col_idx = 0
                    cfg["pladias_photos_col"] = st.selectbox(
                        "Sloupec s vědeckým jménem druhu pro Pladias.cz fotky",
                        options=columns,
                        index=pladias_photos_col_idx,
                        key="w_pladias_photos_col"
                    )
                    cfg["pladias_photos_max"] = st.slider(
                        "Max fotek z Pladias.cz na řádek",
                        1, 5,
                        value=cfg.get("pladias_photos_max", 3),
                        key="w_pladias_photos_max"
                    )
                    _raw_def_parts = cfg.get("pladias_photos_parts", ["Celá rostlina (habitus)", "Květ / květenství", "List"])
                    _clean_def_parts = []
                    for _p in _raw_def_parts:
                        _c_p = re.sub(r'^[^\w]+', '', _p).strip()
                        for _valid in ["Celá rostlina (habitus)", "Květ / květenství", "Plod / semeno", "List", "Stonek / lodyha", "Kmen / borka", "Herbář / sken (Clo-Pla)", "Mikrofoto / detail", "Všechny fotky dohromady (obecný sloupec)"]:
                            if _c_p in _valid or _valid in _p:
                                _clean_def_parts.append(_valid)
                                break
                    if not _clean_def_parts:
                        _clean_def_parts = ["Celá rostlina (habitus)", "Květ / květenství", "List"]
                    cfg["pladias_photos_parts"] = st.multiselect(
                        "Vyberte kategorie / části rostliny (každá se načte do samostatného sloupce):",
                        options=[
                            "Celá rostlina (habitus)",
                            "Květ / květenství",
                            "Plod / semeno",
                            "List",
                            "Stonek / lodyha",
                            "Kmen / borka",
                            "Herbář / sken (Clo-Pla)",
                            "Mikrofoto / detail",
                            "Všechny fotky dohromady (obecný sloupec)"
                        ],
                        default=_clean_def_parts,
                        placeholder="Vyberte části rostliny...",
                        help="Každá vybraná kategorie vytvoří v tabulce vlastní samostatný sloupec (např. [Pladias] Květ, [Pladias] List). Můžete je pak na kartičce libovolně umístit na líc či rub.",
                        key="w_pladias_photos_parts"
                    )
                    cfg["pladias_photos_fallback"] = st.checkbox(
                        "Použít náhradní fotku, pokud vybraná část není dostupná",
                        value=cfg.get("pladias_photos_fallback", False),
                        help="Pokud je vypnuto (doporučeno), do sloupce se načtou výhradně fotografie dané části rostliny. Pokud je zapnuto a rostlina danou část vyfocenu nemá, použije se náhradní dostupná fotografie.",
                        key="w_pladias_photos_fallback"
                    )

                cfg["enable_pladias_map"] = st.checkbox(
                    "Mapa rozšíření ČR z Pladias.cz",
                    value=cfg.get("enable_pladias_map", False),
                    key="w_enable_pladias_map"
                )
                if cfg.get("enable_pladias_map", False):
                    pladias_map_col_val = cfg.get("pladias_map_col", columns[0])
                    try:
                        pladias_map_col_idx = columns.index(pladias_map_col_val)
                    except ValueError:
                        pladias_map_col_idx = 0
                    cfg["pladias_map_col"] = st.selectbox(
                        "Sloupec s vědeckým jménem druhu pro mapu z Pladias.cz.cz",
                        options=columns,
                        index=pladias_map_col_idx,
                        key="w_pladias_map_col"
                    )

                cfg["enable_pladias"] = st.checkbox(
                    "Odkaz na profil na Pladias.cz",
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
                        "Sloupec s vědeckým jménem druhu pro Pladias.cz odkaz",
                        options=columns,
                        index=pladias_col_idx,
                        key="w_pladias_col"
                    )

            with tab_mechorosty:
                c_mr_t, c_mr_chk = st.columns([3.5, 1.5])
                with c_mr_t:
                    st.markdown("##### Specifická nastavení pro mechorosty (Mechy, Játrovky, Hlevíky)")
                with c_mr_chk:
                    keys_mechorosty = ["enable_bryo_photos", "enable_bryo_desc", "enable_bryo_link"]
                    render_category_select_all_checkbox("tab_mechorosty", keys_mechorosty)

                st.caption("Čerpá z mezinárodních bryologických repozitářů GBIF Bryophytes, iNaturalist, Wikimedia Commons a BryophytePortal.")

                cfg["enable_bryo_photos"] = st.checkbox(
                    "Fotografie a mikroskopie mechorostů (GBIF / iNaturalist)",
                    value=cfg.get("enable_bryo_photos", False),
                    key="w_enable_bryo_photos"
                )
                if cfg.get("enable_bryo_photos", False):
                    bryo_p_col_val = cfg.get("bryo_photo_col", columns[0])
                    bryo_p_col_idx = columns.index(bryo_p_col_val) if bryo_p_col_val in columns else 0
                    c_bp1, c_bp2 = st.columns(2)
                    with c_bp1:
                        cfg["bryo_photo_col"] = st.selectbox(
                            "Sloupec s vědeckým jménem mechorostu:",
                            options=columns,
                            index=bryo_p_col_idx,
                            key="w_bryo_photo_col"
                        )
                    with c_bp2:
                        cfg["bryo_photos_max"] = st.slider(
                            "Počet fotografií na druh:",
                            1, 5,
                            value=cfg.get("bryo_photos_max", 3),
                            key="w_bryo_photos_max"
                        )

                cfg["enable_bryo_desc"] = st.checkbox(
                    "Odborný popis mechorostu (habitus, gametofyt, sporofyt, ekologie)",
                    value=cfg.get("enable_bryo_desc", False),
                    key="w_enable_bryo_desc"
                )
                if cfg.get("enable_bryo_desc", False):
                    bryo_d_col_val = cfg.get("bryo_desc_col", columns[0])
                    bryo_d_col_idx = columns.index(bryo_d_col_val) if bryo_d_col_val in columns else 0
                    cfg["bryo_desc_col"] = st.selectbox(
                        "Sloupec se jménem druhu pro popis:",
                        options=columns,
                        index=bryo_d_col_idx,
                        key="w_bryo_desc_col"
                    )

                cfg["enable_bryo_link"] = st.checkbox(
                    "Odkaz na bryologický portál (BryophytePortal / BBS / Bryo.cz)",
                    value=cfg.get("enable_bryo_link", False),
                    key="w_enable_bryo_link"
                )
                if cfg.get("enable_bryo_link", False):
                    bryo_l_col_val = cfg.get("bryo_link_col", columns[0])
                    bryo_l_col_idx = columns.index(bryo_l_col_val) if bryo_l_col_val in columns else 0
                    cfg["bryo_link_col"] = st.selectbox(
                        "Sloupec se jménem druhu pro odkaz:",
                        options=columns,
                        index=bryo_l_col_idx,
                        key="w_bryo_link_col"
                    )

            with tab_houby:
                c_hb_t, c_hb_chk = st.columns([3.5, 1.5])
                with c_hb_t:
                    st.markdown("##### Specifická nastavení pro houby (Mykologie)")
                with c_hb_chk:
                    keys_houby = ["enable_mykologie_img", "enable_mykologie_desc", "enable_mykologie_link", "enable_gbif_fungi", "enable_mushroom_color_atlas"]
                    render_category_select_all_checkbox("tab_houby", keys_houby)

                cfg["enable_mykologie_img"] = st.checkbox(
                    "Fotky z Mykologie.net",
                    value=cfg.get("enable_mykologie_img", False),
                    key="w_enable_mykologie_img"
                )
                if cfg.get("enable_mykologie_img", False):
                    myko_img_col_val = cfg.get("mykologie_img_col", columns[0])
                    try:
                        myko_img_col_idx = columns.index(myko_img_col_val)
                    except ValueError:
                        myko_img_col_idx = 0
                    cfg["mykologie_img_col"] = st.selectbox(
                        "Sloupec se jménem houby pro fotky z Mykologie.net",
                        options=columns,
                        index=myko_img_col_idx,
                        key="w_mykologie_img_col"
                    )
                    cfg["mykologie_img_max"] = st.slider(
                        "Max fotek z Mykologie.net na řádek",
                        1, 5,
                        value=cfg.get("mykologie_img_max", 3),
                        key="w_mykologie_img_max"
                    )

                cfg["enable_mykologie_desc"] = st.checkbox(
                    "Český popis z Mykologie.net",
                    value=cfg.get("enable_mykologie_desc", False),
                    key="w_enable_mykologie_desc"
                )
                if cfg.get("enable_mykologie_desc", False):
                    myko_desc_col_val = cfg.get("mykologie_desc_col", columns[0])
                    try:
                        myko_desc_col_idx = columns.index(myko_desc_col_val)
                    except ValueError:
                        myko_desc_col_idx = 0
                    cfg["mykologie_desc_col"] = st.selectbox(
                        "Sloupec se jménem houby pro popis z Mykologie.net",
                        options=columns,
                        index=myko_desc_col_idx,
                        key="w_mykologie_desc_col"
                    )

                cfg["enable_mykologie_link"] = st.checkbox(
                    "Odkaz na profil na Mykologie.net",
                    value=cfg.get("enable_mykologie_link", False),
                    key="w_enable_mykologie_link"
                )
                if cfg.get("enable_mykologie_link", False):
                    myko_link_col_val = cfg.get("mykologie_link_col", columns[0])
                    try:
                        myko_link_col_idx = columns.index(myko_link_col_val)
                    except ValueError:
                        myko_link_col_idx = 0
                    cfg["mykologie_link_col"] = st.selectbox(
                        "Sloupec se jménem houby pro odkaz na Mykologie.net",
                        options=columns,
                        index=myko_link_col_idx,
                        key="w_mykologie_link_col"
                    )

                st.markdown("---")
                cfg["enable_gbif_fungi"] = st.checkbox(
                    "GBIF fotky - Houby",
                    value=cfg.get("enable_gbif_fungi", False),
                    key="w_enable_gbif_fungi"
                )
                if cfg.get("enable_gbif_fungi", False):
                    gbif_fungi_col_val = cfg.get("gbif_fungi_col", columns[0])
                    try:
                        gbif_fungi_col_idx = columns.index(gbif_fungi_col_val)
                    except ValueError:
                        gbif_fungi_col_idx = 0
                    cfg["gbif_fungi_col"] = st.selectbox(
                        "Sloupec s vědeckým jménem druhu houby (GBIF)",
                        options=columns,
                        index=gbif_fungi_col_idx,
                        key="w_gbif_fungi_col"
                    )
                    cfg["gbif_fungi_max"] = st.slider(
                        "Max fotek z GBIF Houby na řádek",
                        1, 5,
                        value=cfg.get("gbif_fungi_max", 3),
                        key="w_gbif_fungi_max"
                    )

                st.markdown("---")
                cfg["enable_mushroom_color_atlas"] = st.checkbox(
                    "Mushroom Color Atlas (pigmenty a barviva z hub)",
                    value=cfg.get("enable_mushroom_color_atlas", False),
                    key="w_enable_mushroom_color_atlas",
                    help="Obohatí tabulku o odkaz na mezinárodní registr Mushroom Color Atlas (včetně popisu barevné palety a pigmentů) u barvířských druhů hub."
                )
                if cfg.get("enable_mushroom_color_atlas", False):
                    mca_col_val = cfg.get("mca_col", columns[0])
                    try:
                        mca_col_idx = columns.index(mca_col_val)
                    except ValueError:
                        mca_col_idx = 0
                    cfg["mca_col"] = st.selectbox(
                        "Sloupec se jménem houby pro Mushroom Color Atlas:",
                        options=columns,
                        index=mca_col_idx,
                        key="w_mca_col"
                    )

            with tab_lisejniky:
                c_ls_t, c_ls_chk = st.columns([3.5, 1.5])
                with c_ls_t:
                    st.markdown("##### Specifická nastavení pro lišejníky (DaLiBor – dalib.cz)")
                with c_ls_chk:
                    keys_lisejniky = ["enable_dalibor_photos", "enable_dalibor_desc", "enable_dalibor_link"]
                    render_category_select_all_checkbox("tab_lisejniky", keys_lisejniky)

                cfg["enable_dalibor_photos"] = st.checkbox(
                    "Fotky lišejníků z DaLiBor (Atlas českých lišejníků)",
                    value=cfg.get("enable_dalibor_photos", False),
                    key="w_enable_dalibor_photos"
                )
                if cfg.get("enable_dalibor_photos", False):
                    dalib_photos_col_val = cfg.get("dalibor_photos_col", columns[0])
                    try:
                        dalib_photos_col_idx = columns.index(dalib_photos_col_val)
                    except ValueError:
                        dalib_photos_col_idx = 0
                    cfg["dalibor_photos_col"] = st.selectbox(
                        "Sloupec s vědeckým jménem lišejníku pro fotky",
                        options=columns,
                        index=dalib_photos_col_idx,
                        key="w_dalibor_photos_col"
                    )
                    cfg["dalibor_photos_max"] = st.slider(
                        "Max fotek z DaLiBor na řádek",
                        1, 5,
                        value=cfg.get("dalibor_photos_max", 3),
                        key="w_dalibor_photos_max"
                    )

                cfg["enable_dalibor_desc"] = st.checkbox(
                    "Český popis a ekologie z DaLiBor",
                    value=cfg.get("enable_dalibor_desc", False),
                    key="w_enable_dalibor_desc"
                )
                if cfg.get("enable_dalibor_desc", False):
                    dalib_desc_col_val = cfg.get("dalibor_desc_col", columns[0])
                    try:
                        dalib_desc_col_idx = columns.index(dalib_desc_col_val)
                    except ValueError:
                        dalib_desc_col_idx = 0
                    cfg["dalibor_desc_col"] = st.selectbox(
                        "Sloupec s vědeckým jménem lišejníku pro popis",
                        options=columns,
                        index=dalib_desc_col_idx,
                        key="w_dalibor_desc_col"
                    )

                cfg["enable_dalibor_link"] = st.checkbox(
                    "Odkaz na profil na dalib.cz",
                    value=cfg.get("enable_dalibor_link", False),
                    key="w_enable_dalibor_link"
                )
                if cfg.get("enable_dalibor_link", False):
                    dalib_link_col_val = cfg.get("dalibor_link_col", columns[0])
                    try:
                        dalib_link_col_idx = columns.index(dalib_link_col_val)
                    except ValueError:
                        dalib_link_col_idx = 0
                    cfg["dalibor_link_col"] = st.selectbox(
                        "Sloupec s vědeckým jménem lišejníku pro odkaz",
                        options=columns,
                        index=dalib_link_col_idx,
                        key="w_dalibor_link_col"
                    )

            with tab_rasy:
                c_rs_t, c_rs_chk = st.columns([3.5, 1.5])
                with c_rs_t:
                    st.markdown("##### Specifická nastavení pro řasy a rozsivky")
                with c_rs_chk:
                    keys_rasy = ["enable_diatombase_taxon", "enable_diatombase_link", "enable_algaebase_link"]
                    render_category_select_all_checkbox("tab_rasy", keys_rasy)

                col_ras1, col_ras2 = st.columns(2)
                with col_ras1:
                    st.markdown("**Rozsivky (DiatomBase / WoRMS):**")
                    cfg["enable_diatombase_taxon"] = st.checkbox(
                        "Taxonomie & autorita (DiatomBase)",
                        value=cfg.get("enable_diatombase_taxon", False),
                        key="w_enable_diatombase_taxon"
                    )
                    if cfg.get("enable_diatombase_taxon", False):
                        dt_col_val = cfg.get("diatombase_taxon_col", columns[0])
                        try:
                            dt_col_idx = columns.index(dt_col_val)
                        except ValueError:
                            dt_col_idx = 0
                        cfg["diatombase_taxon_col"] = st.selectbox(
                            "Sloupec se jménem rozsivky (DiatomBase)",
                            options=columns,
                            index=dt_col_idx,
                            key="w_diatombase_taxon_col"
                        )

                    cfg["enable_diatombase_link"] = st.checkbox(
                        "Odkaz na profil na DiatomBase",
                        value=cfg.get("enable_diatombase_link", False),
                        key="w_enable_diatombase_link"
                    )
                    if cfg.get("enable_diatombase_link", False):
                        dt_link_val = cfg.get("diatombase_link_col", columns[0])
                        try:
                            dt_link_idx = columns.index(dt_link_val)
                        except ValueError:
                            dt_link_idx = 0
                        cfg["diatombase_link_col"] = st.selectbox(
                            "Sloupec se jménem pro odkaz na DiatomBase",
                            options=columns,
                            index=dt_link_idx,
                            key="w_diatombase_link_col"
                        )

                with col_ras2:
                    st.markdown("**Řasy a sinice (AlgaeBase):**")
                    cfg["enable_algaebase_link"] = st.checkbox(
                        "Odkaz na vyhledávání na AlgaeBase",
                        value=cfg.get("enable_algaebase_link", False),
                        key="w_enable_algaebase_link"
                    )
                    if cfg.get("enable_algaebase_link", False):
                        alg_link_val = cfg.get("algaebase_link_col", columns[0])
                        try:
                            alg_link_idx = columns.index(alg_link_val)
                        except ValueError:
                            alg_link_idx = 0
                        cfg["algaebase_link_col"] = st.selectbox(
                            "Sloupec s vědeckým jménem řasy (AlgaeBase)",
                            options=columns,
                            index=alg_link_idx,
                            key="w_algaebase_link_col"
                        )

            with tab_zoologie:
                c_zoo_t, c_zoo_chk = st.columns([3.5, 1.5])
                with c_zoo_t:
                    st.markdown("##### Specifická nastavení pro zoologii")
                with c_zoo_chk:
                    keys_zoologie = ["enable_gbif_zoo", "enable_bird_sounds"]
                    render_category_select_all_checkbox("tab_zoologie", keys_zoologie)

                cfg["enable_gbif_zoo"] = st.checkbox(
                    "GBIF fotky - Zoologie",
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
                    "Hlasy ptáků (Xeno-canto)",
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

            with tab_registry:
                c_rg_t, c_rg_chk = st.columns([3.5, 1.5])
                with c_rg_t:
                    st.markdown("##### Národní databáze a registry ČR")
                with c_rg_chk:
                    keys_registry = ["enable_nepuvodni", "enable_biotopy", "enable_ellenberg", "enable_cerveny_seznam", "enable_cerveny_seznam_url", "enable_kvetena_cr"]
                    render_category_select_all_checkbox("tab_registry", keys_registry)

                cfg["enable_nepuvodni"] = st.checkbox(
                    "Katalog nepůvodních druhů rostlin ČR (status, původ)",
                    value=cfg.get("enable_nepuvodni", False),
                    key="w_enable_nepuvodni"
                )
                if cfg.get("enable_nepuvodni", False):
                    nep_col_val = cfg.get("nepuvodni_col", columns[0])
                    nep_col_idx = columns.index(nep_col_val) if nep_col_val in columns else 0
                    cfg["nepuvodni_col"] = st.selectbox(
                        "Sloupec se jménem druhu pro nepůvodní flóru",
                        options=columns,
                        index=nep_col_idx,
                        key="w_nepuvodni_col"
                    )

                cfg["enable_biotopy"] = st.checkbox(
                    "Výskyt v biotopech ČR",
                    value=cfg.get("enable_biotopy", False),
                    key="w_enable_biotopy"
                )
                if cfg.get("enable_biotopy", False):
                    bio_col_val = cfg.get("biotopy_col", columns[0])
                    bio_col_idx = columns.index(bio_col_val) if bio_col_val in columns else 0
                    cfg["biotopy_col"] = st.selectbox(
                        "Sloupec se jménem druhu pro biotopy",
                        options=columns,
                        index=bio_col_idx,
                        key="w_biotopy_col"
                    )

                cfg["enable_ellenberg"] = st.checkbox(
                    "Ellenbergovy indikační hodnoty pro ČR (L, T, M, R, N, S)",
                    value=cfg.get("enable_ellenberg", False),
                    key="w_enable_ellenberg"
                )
                if cfg.get("enable_ellenberg", False):
                    ell_col_val = cfg.get("ellenberg_col", columns[0])
                    ell_col_idx = columns.index(ell_col_val) if ell_col_val in columns else 0
                    cfg["ellenberg_col"] = st.selectbox(
                        "Sloupec se jménem druhu pro Ellenbergovy hodnoty",
                        options=columns,
                        index=ell_col_idx,
                        key="w_ellenberg_col"
                    )

                cfg["enable_cerveny_seznam"] = st.checkbox(
                    "Červený seznam ČR (AOPK ČR – Kategorie ohrožení)",
                    value=cfg.get("enable_cerveny_seznam", False),
                    key="w_enable_cerveny_seznam"
                )
                if cfg.get("enable_cerveny_seznam", False):
                    cs_col_val = cfg.get("cerveny_seznam_col", columns[0])
                    cs_col_idx = columns.index(cs_col_val) if cs_col_val in columns else 0
                    cfg["cerveny_seznam_col"] = st.selectbox(
                        "Sloupec se jménem druhu pro Červený seznam ČR",
                        options=columns,
                        index=cs_col_idx,
                        key="w_cerveny_seznam_col"
                    )
                    cfg["enable_cerveny_seznam_url"] = st.checkbox(
                        "Přidat samostatný sloupec: Odkaz na Červený seznam (PDF / Portál)",
                        value=cfg.get("enable_cerveny_seznam_url", False),
                        key="w_enable_cerveny_seznam_url"
                    )

                cfg["enable_kvetena_cr"] = st.checkbox(
                    "Botanický popis z Květeny ČR (ibot.cas.cz PDF)",
                    value=cfg.get("enable_kvetena_cr", False),
                    key="w_enable_kvetena_cr"
                )
                if cfg.get("enable_kvetena_cr", False):
                    kv_col_val = cfg.get("kvetena_cr_col", columns[0])
                    kv_col_idx = columns.index(kv_col_val) if kv_col_val in columns else 0
                    cfg["kvetena_cr_col"] = st.selectbox(
                        "Sloupec s vědeckým jménem druhu pro Květenu ČR",
                        options=columns,
                        index=kv_col_idx,
                        key="w_kvetena_cr_col"
                    )
                    kv_mode = st.radio(
                        "Rozsah popisu z Květeny ČR:",
                        ["Zkrácený popis (limit znaků)", "Kompletní popis (plné znění kapitoly z Květeny ČR)"],
                        index=0 if not cfg.get("kvetena_cr_full", False) else 1,
                        horizontal=True,
                        key="w_kvetena_cr_mode"
                    )
                    cfg["kvetena_cr_full"] = (kv_mode.startswith("Kompletní"))
                    if not cfg["kvetena_cr_full"]:
                        cfg["kvetena_cr_max_chars"] = st.slider(
                            "Maximální délka popisu (počet znaků):",
                            150, 3000,
                            value=cfg.get("kvetena_cr_max_chars", 450),
                            step=50,
                            key="w_kvetena_cr_max_chars"
                        )
                    else:
                        cfg["kvetena_cr_max_chars"] = 0

        elif selected_topic == "Jazyky":
            col_l1, col_l2 = st.columns(2)
            with col_l1:
                cfg["enable_trans"] = st.checkbox(
                    "Překladač",
                    value=cfg.get("enable_trans", False),
                    key="w_enable_trans"
                )

                trans_col_idx = get_smart_column_default(columns, cfg, "trans_col", ["překlad", "text", "slovo", "angličtina", "english", "český název", "česky"])
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

                st.markdown("---")
                st.markdown("**Výslovnost latiny:**")
                cfg["enable_latin_tts"] = st.checkbox(
                    "Latinská hlasová výslovnost [TTS Latina]",
                    value=cfg.get("enable_latin_tts", False),
                    key="w_enable_latin_tts"
                )
                if cfg.get("enable_latin_tts", False):
                    lat_tts_col_idx = get_smart_column_default(columns, cfg, "latin_tts_col", ["vědecké", "latinsk", "taxon", "species", "scientific"])
                    cfg["latin_tts_col"] = st.selectbox(
                        "Sloupec s latinským názvem pro hlasové audio",
                        options=columns,
                        index=lat_tts_col_idx,
                        key="w_latin_tts_col"
                    )

                cfg["enable_latin_phonetic"] = st.checkbox(
                    "Český fonetický přepis latiny [Fonetická výslovnost]",
                    value=cfg.get("enable_latin_phonetic", False),
                    key="w_enable_latin_phonetic"
                )
                if cfg.get("enable_latin_phonetic", False):
                    lat_ph_col_idx = get_smart_column_default(columns, cfg, "latin_phonetic_col", ["vědecké", "latinsk", "taxon", "species", "scientific"])
                    cfg["latin_phonetic_col"] = st.selectbox(
                        "Sloupec s latinským jménem pro fonetický přepis",
                        options=columns,
                        index=lat_ph_col_idx,
                        key="w_latin_phonetic_col"
                    )

            with col_l2:
                cfg["enable_tts"] = st.checkbox(
                    "Hlasová výslovnost (Google TTS)",
                    value=cfg.get("enable_tts", False),
                    key="w_enable_tts"
                )

                tts_col_idx = get_smart_column_default(columns, cfg, "tts_col", ["slovo", "text", "anglick", "english", "výslovnost", "český"])
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
                    "Anglický výkladový slovník",
                    value=cfg.get("enable_dict", False),
                    key="w_enable_dict"
                )

                dict_col_idx = get_smart_column_default(columns, cfg, "dict_col", ["anglick", "english", "word", "slovo", "termín", "heslo"])
                cfg["dict_col"] = st.selectbox(
                    "Sloupec s anglickým slovem k definici",
                    options=columns,
                    index=dict_col_idx,
                    key="w_dict_col"
                )

        elif selected_topic == "Zeměpis":
            cfg["enable_country"] = st.checkbox(
                "Modul států (hlavní město, region, měna, vlajka...)",
                value=cfg.get("enable_country", False),
                key="w_enable_country"
            )

            country_col_idx = get_smart_column_default(columns, cfg, "country_col", ["stát", "země", "country", "state", "území", "národ"])
            cfg["country_col"] = st.selectbox(
                "Sloupec s názvem státu (česky nebo anglicky)",
                options=columns,
                index=country_col_idx,
                key="w_country_col"
            )

        MODULE_HUMAN_NAMES = {
            "enable_inat": "iNaturalist",
            "enable_inat_map": "iNaturalist mapa pozorování",
            "enable_desc": "Popis druhu",
            "enable_gbif": "GBIF taxonomie",
            "enable_wiki_img": "Wikimedia obrázky",
            "enable_wiki_link": "Wikipedie odkaz",
            "enable_pladias_photos": "Pladias.cz fotky",
            "enable_pladias_map": "Pladias.cz mapa",
            "enable_pladias": "Pladias.cz odkaz",
            "enable_pladias_tax": "Pladias.cz taxonomie",
            "enable_bryo_photos": "Mechorosty fotky",
            "enable_bryo_desc": "Mechorosty popis",
            "enable_bryo_link": "Mechorosty odkaz",
            "enable_mykologie_img": "Mykologie fotky",
            "enable_mykologie_desc": "Mykologie popis",
            "enable_mykologie_link": "Mykologie odkaz",
            "enable_gbif_fungi": "GBIF Houby",
            "enable_mushroom_color_atlas": "Mushroom Color Atlas",
            "enable_dalibor_photos": "DaLiBor fotky",
            "enable_dalibor_desc": "DaLiBor popis",
            "enable_dalibor_link": "DaLiBor odkaz",
            "enable_diatombase_taxon": "DiatomBase taxonomie",
            "enable_diatombase_link": "DiatomBase odkaz",
            "enable_algaebase_link": "AlgaeBase odkaz",
            "enable_gbif_zoo": "GBIF Zoologie",
            "enable_bird_sounds": "Hlasy ptáků",
            "enable_nepuvodni": "Nepůvodní flóra",
            "enable_biotopy": "Biotopy ČR",
            "enable_ellenberg": "Ellenbergovy hodnoty",
            "enable_cerveny_seznam": "Červený seznam ČR",
            "enable_cerveny_seznam_url": "Červený seznam odkaz",
            "enable_kvetena_cr": "Květena ČR",
            "enable_adw_desc": "ADW popis",
            "enable_adw_link": "ADW odkaz",
            "enable_gbif_desc": "GBIF popis",
            "enable_powo_desc": "POWO popis",
            "enable_powo_link": "POWO odkaz",
            "enable_eol_link": "EOL odkaz",
            "enable_trans": "Překladač",
            "enable_tts": "TTS výslovnost",
            "enable_latin_tts": "Latinská TTS",
            "enable_latin_phonetic": "Latinská fonetika",
            "enable_dict": "Výkladový slovník",
            "enable_country": "Modul států"
        }
        active_labels = [MODULE_HUMAN_NAMES[k] for k in ALL_MODULE_KEYS if k in MODULE_HUMAN_NAMES and cfg.get(k, False)]
        if active_labels:
            pills_html = " ".join([f'<span style="display:inline-block; font-size:11px; padding:2px 8px; border-radius:12px; margin:2px 4px 2px 0; background:rgba(56, 156, 98, 0.12); border:1px solid rgba(56, 156, 98, 0.35); color:{css_fg}; font-weight:500;">{lbl}</span>' for lbl in active_labels])
            st.markdown(f'<div style="margin: 4px 0 10px 0;"><span style="font-size:11.5px; font-weight:600; color:{css_muted}; margin-right:6px;">Aktivní moduly ({len(active_labels)}):</span>{pills_html}</div>', unsafe_allow_html=True)
        else:
            st.caption("Aktivní moduly (0): Žádný modul není vybrán.")

        st.markdown("---")

        skip_existing = st.checkbox(
            "Přeskočit položky, které již mají data vyplněná (nepřepisovat existující hodnoty)",
            value=True,
            key="cb_skip_existing_enrichment",
            help="Pokud sloupec nebo buňka již obsahuje informace (např. z importovaného balíčku nebo tabulky), stahování se pro daný druh přeskočí a stávající hodnota zůstane zachována."
        )

        btn_enrich_clicked = st.button("Spustit obohacení dat (API)", key="btn_run_api_enrichment_main", use_container_width=True, type="primary")

        if st.session_state.get("enrichment_success_info"):
            e_info = st.session_state.enrichment_success_info
            st.success(
                f"**Obohacení dat bylo úspěšně dokončeno!** Tabulka nyní obsahuje **{e_info['rows']} položek** a **{e_info['cols']} sloupců**." +
                (f" (Nenalezeno položek: {e_info['unfound']})" if e_info.get('unfound', 0) > 0 else "")
            )

        if btn_enrich_clicked:

            cfg = st.session_state.api_config
            enable_inat = cfg.get("enable_inat", False)
            enable_gbif = cfg.get("enable_gbif", False)
            enable_desc = cfg.get("enable_desc", False)
            enable_gbif_kvet = cfg.get("enable_gbif_kvet", False)
            enable_gbif_list = cfg.get("enable_gbif_list", False)
            enable_gbif_herbar = cfg.get("enable_gbif_herbar", False)
            enable_pladias_photos = cfg.get("enable_pladias_photos", False)
            enable_pladias_map = cfg.get("enable_pladias_map", False)
            enable_pladias = cfg.get("enable_pladias", False)
            enable_klic_2019 = cfg.get("enable_klic_2019", False)
            enable_nepuvodni = cfg.get("enable_nepuvodni", False)
            enable_biotopy = cfg.get("enable_biotopy", False)
            enable_ellenberg = cfg.get("enable_ellenberg", False)
            enable_cerveny_seznam = cfg.get("enable_cerveny_seznam", False)
            enable_cerveny_seznam_url = cfg.get("enable_cerveny_seznam_url", False)
            enable_kvetena_cr = cfg.get("enable_kvetena_cr", False)
            enable_bryo_photos = cfg.get("enable_bryo_photos", False)
            enable_bryo_desc = cfg.get("enable_bryo_desc", False)
            enable_bryo_link = cfg.get("enable_bryo_link", False)
            enable_mykologie_img = cfg.get("enable_mykologie_img", False)
            enable_mykologie_desc = cfg.get("enable_mykologie_desc", False)
            enable_mykologie_link = cfg.get("enable_mykologie_link", False)
            enable_inat_map = cfg.get("enable_inat_map", False)
            inat_map_col = cfg.get("inat_col", columns[0])
            enable_mushroom_color_atlas = cfg.get("enable_mushroom_color_atlas", False)
            mca_col = cfg.get("mca_col", columns[0])
            enable_dalibor_photos = cfg.get("enable_dalibor_photos", False)
            enable_dalibor_desc = cfg.get("enable_dalibor_desc", False)
            enable_dalibor_link = cfg.get("enable_dalibor_link", False)
            enable_diatombase_taxon = cfg.get("enable_diatombase_taxon", False)
            enable_diatombase_link = cfg.get("enable_diatombase_link", False)
            enable_algaebase_link = cfg.get("enable_algaebase_link", False)
            enable_gbif_fungi = cfg.get("enable_gbif_fungi", False)
            enable_gbif_zoo = cfg.get("enable_gbif_zoo", False)
            enable_bird_sounds = cfg.get("enable_bird_sounds", False)
            enable_wiki_link = cfg.get("enable_wiki_link", False)
            enable_trans = cfg.get("enable_trans", False)
            enable_tts = cfg.get("enable_tts", False)
            enable_latin_tts = cfg.get("enable_latin_tts", False)
            enable_latin_phonetic = cfg.get("enable_latin_phonetic", False)
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
            pladias_photos_col = cfg.get("pladias_photos_col", columns[0] if columns else "")
            pladias_photos_max = cfg.get("pladias_photos_max", 3)
            pladias_photos_parts = cfg.get("pladias_photos_parts", [])
            pladias_photos_fallback = cfg.get("pladias_photos_fallback", False)
            pladias_map_col = cfg.get("pladias_map_col", columns[0] if columns else "")
            pladias_col = cfg.get("pladias_col", columns[0] if columns else "")
            enable_pladias_tax = cfg.get("enable_pladias_tax", False)
            enable_pladias_czech_name = cfg.get("enable_pladias_czech_name", True)
            pladias_tax_col = cfg.get("pladias_tax_col", columns[0] if columns else "")
            klic_2019_col = cfg.get("klic_2019_col", columns[0] if columns else "")
            nepuvodni_col = cfg.get("nepuvodni_col", columns[0] if columns else "")
            biotopy_col = cfg.get("biotopy_col", columns[0] if columns else "")
            ellenberg_col = cfg.get("ellenberg_col", columns[0] if columns else "")
            cerveny_seznam_col = cfg.get("cerveny_seznam_col", columns[0] if columns else "")
            kvetena_cr_col = cfg.get("kvetena_cr_col", columns[0] if columns else "")
            kvetena_cr_max_chars = cfg.get("kvetena_cr_max_chars", 450)
            bryo_photo_col = cfg.get("bryo_photo_col", columns[0] if columns else "")
            bryo_photos_max = cfg.get("bryo_photos_max", 3)
            bryo_desc_col = cfg.get("bryo_desc_col", columns[0] if columns else "")
            bryo_link_col = cfg.get("bryo_link_col", columns[0] if columns else "")
            mykologie_img_col = cfg.get("mykologie_img_col", columns[0] if columns else "")
            mykologie_img_max = cfg.get("mykologie_img_max", 3)
            mykologie_desc_col = cfg.get("mykologie_desc_col", columns[0] if columns else "")
            mykologie_link_col = cfg.get("mykologie_link_col", columns[0] if columns else "")
            dalibor_photos_col = cfg.get("dalibor_photos_col", columns[0] if columns else "")
            dalibor_photos_max = cfg.get("dalibor_photos_max", 3)
            dalibor_desc_col = cfg.get("dalibor_desc_col", columns[0] if columns else "")
            dalibor_link_col = cfg.get("dalibor_link_col", columns[0] if columns else "")
            diatombase_taxon_col = cfg.get("diatombase_taxon_col", columns[0] if columns else "")
            diatombase_link_col = cfg.get("diatombase_link_col", columns[0] if columns else "")
            algaebase_link_col = cfg.get("algaebase_link_col", columns[0] if columns else "")
            gbif_fungi_col = cfg.get("gbif_fungi_col", columns[0] if columns else "")
            gbif_fungi_max = cfg.get("gbif_fungi_max", 3)
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
            latin_tts_col = cfg.get("latin_tts_col", columns[0] if columns else "")
            latin_phonetic_col = cfg.get("latin_phonetic_col", columns[0] if columns else "")
            dict_col = cfg.get("dict_col", columns[0] if columns else "")
            wiki_img_col = cfg.get("wiki_col", columns[0] if columns else "")
            wiki_max_photos = cfg.get("wiki_max", 3)
            country_col = cfg.get("country_col", columns[0] if columns else "")
            enable_adw_desc = cfg.get("enable_adw_desc", False)
            enable_adw_link = cfg.get("enable_adw_link", False)
            adw_col = cfg.get("adw_col", columns[0] if columns else "")
            enable_gbif_desc = cfg.get("enable_gbif_desc", False)
            gbif_desc_col = cfg.get("gbif_desc_col", columns[0] if columns else "")
            enable_powo_desc = cfg.get("enable_powo_desc", False)
            enable_powo_link = cfg.get("enable_powo_link", False)
            powo_col = cfg.get("powo_col", columns[0] if columns else "")
            enable_eol_link = cfg.get("enable_eol_link", False)
            eol_col = cfg.get("eol_col", columns[0] if columns else "")

            progress_bar = st.progress(0.0)
            status = st.empty()

            new_df = df.copy()

            def _ensure_new_col(col_name):
                if col_name not in new_df.columns:
                    new_df[col_name] = ""

            if enable_inat:
                _ensure_new_col("[iNat] České jméno")
                _ensure_new_col("[iNat] Obrázky (URL)")
            if enable_desc:
                _ensure_new_col("[Popis] Popis z Wikipedie")
            if enable_gbif:
                _ensure_new_col("[GBIF] Říše")
                _ensure_new_col("[GBIF] Kmen")
                _ensure_new_col("[GBIF] Třída")
                _ensure_new_col("[GBIF] Řád")
                _ensure_new_col("[GBIF] Čeleď")
                _ensure_new_col("[GBIF] Rod")
            if enable_wiki_img:
                _ensure_new_col("[Wikimedia] Obrázky (URL)")
            if enable_trans:
                _ensure_new_col(f"[Překlad] {trans_tgt}")
            if enable_tts:
                _ensure_new_col("[TTS] Výslovnost (Audio)")
            if enable_latin_tts:
                _ensure_new_col("[TTS] Latina")
            if enable_latin_phonetic:
                _ensure_new_col("[Latina] Fonetická výslovnost")
            if enable_dict:
                _ensure_new_col("[Slovník] Výslovnost (Text)")
                _ensure_new_col("[Slovník] Definice")
                _ensure_new_col("[Slovník] Příkladová věta")
            if enable_country:
                _ensure_new_col("[Zeměpis] Český název")
                _ensure_new_col("[Zeměpis] Hlavní město")
                _ensure_new_col("[Zeměpis] Region")
                _ensure_new_col("[Zeměpis] Jazyky")
                _ensure_new_col("[Zeměpis] Měna")
                _ensure_new_col("[Zeměpis] Rozloha")
                _ensure_new_col("[Zeměpis] Vlajka (URL)")

            if enable_pladias_photos:
                target_cats = pladias_photos_parts if pladias_photos_parts else ["Všechny fotky dohromady (obecný sloupec)"]
                for cat_opt in target_cats:
                    if cat_opt in PLADIAS_CATEGORY_MAPPING:
                        col_name = PLADIAS_CATEGORY_MAPPING[cat_opt][0]
                        _ensure_new_col(col_name)
            if enable_pladias_map:
                _ensure_new_col("[Pladias.cz] Mapa rozšíření")
            if enable_pladias:
                _ensure_new_col("[Pladias] Odkaz")
            if enable_pladias_tax:
                if enable_pladias_czech_name:
                    _ensure_new_col("[Pladias] České jméno")
                _ensure_new_col("[Pladias] Oddělení")
                _ensure_new_col("[Pladias] Třída")
                _ensure_new_col("[Pladias] Řád")
                _ensure_new_col("[Pladias] Čeleď")
                _ensure_new_col("[Pladias] Rod")
            if enable_klic_2019:
                _ensure_new_col("[Klíč 2019] Jméno & Autorita")
                _ensure_new_col("[Klíč 2019] České jméno")
            if enable_nepuvodni:
                _ensure_new_col("[Nepůvodní flóra] Invazní status & Původ")
            if enable_biotopy:
                _ensure_new_col("[Biotopy] Výskyt v biotopech ČR")
            if enable_ellenberg:
                _ensure_new_col("[Ekologie] Ellenbergovy hodnoty")
            if enable_cerveny_seznam:
                _ensure_new_col("[Červený seznam] Kategorie ohrožení")
                if enable_cerveny_seznam_url:
                    _ensure_new_col("[Červený seznam] Odkaz")
            if enable_kvetena_cr:
                _ensure_new_col("[Květena ČR] Popis druhu")
            if enable_bryo_photos:
                _ensure_new_col("[Mechorosty] Fotky")
            if enable_bryo_desc:
                _ensure_new_col("[Mechorosty] Popis")
            if enable_bryo_link:
                _ensure_new_col("[Mechorosty] Odkaz")
            if enable_mykologie_img:
                _ensure_new_col("[Mykologie.net] Fotky")
            if enable_mykologie_desc:
                _ensure_new_col("[Mykologie.net] Popis")
            if enable_mykologie_link:
                _ensure_new_col("[Mykologie.net] Odkaz")
            if enable_inat_map:
                _ensure_new_col("[iNaturalist] Mapa nálezů")
            if enable_mushroom_color_atlas:
                _ensure_new_col("[Mushroom Color Atlas] Odkaz")
            if enable_dalibor_photos:
                _ensure_new_col("[DaLiBor] Fotky")
            if enable_dalibor_desc:
                _ensure_new_col("[DaLiBor] Popis")
            if enable_dalibor_link:
                _ensure_new_col("[DaLiBor] Odkaz")
            if enable_diatombase_taxon:
                _ensure_new_col("[DiatomBase] Taxon & Autorita")
                _ensure_new_col("[DiatomBase] Taxonomie")
            if enable_diatombase_link:
                _ensure_new_col("[DiatomBase] Odkaz")
            if enable_algaebase_link:
                _ensure_new_col("[AlgaeBase] Odkaz")
            if enable_gbif_fungi:
                _ensure_new_col("[GBIF] Houby")
            if enable_gbif_zoo:
                _ensure_new_col("[GBIF] Zoologie")
            if enable_wiki_link:
                _ensure_new_col("[Wikipedie] Odkaz")
            if enable_bird_sounds:
                _ensure_new_col("[Zvuky] Hlasy ptáků")
            if enable_adw_desc:
                _ensure_new_col("[ADW] Biologický popis")
            if enable_adw_link:
                _ensure_new_col("[ADW] Odkaz")
            if enable_gbif_desc:
                _ensure_new_col("[GBIF] Vědecký popis")
            if enable_powo_desc:
                _ensure_new_col("[POWO Kew] Popis flóry")
            if enable_powo_link:
                _ensure_new_col("[POWO Kew] Odkaz")
            if enable_eol_link:
                _ensure_new_col("[EOL] Odkaz")

            def _is_val_empty(v):
                if v is None or pd.isna(v):
                    return True
                s = str(v).strip()
                return s == "" or s.lower() == "nan"

            def _enrich_single_row(idx, row):
                row_updates = {}
                row_unfounds = []

                def _is_target_filled(col_name):
                    if not skip_existing or col_name not in row:
                        return False
                    return not _is_val_empty(row.get(col_name))

                raw_main_val = str(row[columns[0]]).strip() if len(columns) > 0 else ""
                inat_data = None
                inat_cz = ""
                desc_text = ""
                gbif_data = None
                gbif_photo_data = None
                wiki_urls = []
                translated = ""
                p_photos = []
                k1 = None
                k2 = None
                k3 = None
                k4 = None
                k5 = None
                kv_desc = ""
                myko_data = None
                dalib_data = None
                diatom_data = None
                zoo_photos = []
                fungi_photos = []
                sound_results = []
                c_data = None
                dict_data = None

                k_flora_check = query_klic_2019(raw_main_val) or query_nepuvodni_flora(raw_main_val)
                k_red_check = query_cerveny_seznam(raw_main_val)
                is_flora_plant = bool(k_flora_check or (k_red_check and "cévnat" in k_red_check.get("group", "").lower()))

                if enable_inat_map and not _is_target_filled("[iNaturalist] Mapa nálezů"):
                    try:
                        raw_sp = str(row[inat_map_col]).strip()
                        sel_p_opt = cfg.get("inat_place_opt", "Česká republika")
                        cust_p = cfg.get("inat_custom_place", "") if sel_p_opt.startswith("Vlastní") else sel_p_opt
                        p_id = resolve_inat_place_id(cust_p)
                        m_url = fetch_inaturalist_map_url(raw_sp, place_id=p_id)
                        if m_url:
                            row_updates["[iNaturalist] Mapa nálezů"] = m_url
                    except Exception:
                        pass

                if enable_mushroom_color_atlas:
                    try:
                        raw_sp = str(row[mca_col]).strip()
                        mca_info = fetch_mushroom_color_atlas(raw_sp)
                        if mca_info:
                            row_updates["[Mushroom Color Atlas] Odkaz"] = mca_info["url"]
                    except Exception:
                        pass

                inat_check_cols = ["[iNat] České jméno", "[iNat] Obrázky (URL)"]
                if enable_inat and not (skip_existing and all(_is_target_filled(c) for c in inat_check_cols)):
                    try:
                        raw_sp = str(row[inat_col]).strip()
                        sp = re.sub(r'\s*\(.*\)\s*', '', raw_sp).strip()
                        sp_clean = re.sub(r'\s+sp(p)?\.?$', '', sp).strip()
                        inat_data = fetch_inaturalist_data(sp_clean, inat_max_photos)
                        if inat_data.get('source') == 'Nenalezeno':
                            row_unfounds.append({'Řádek': idx + 1, 'Položka': raw_sp, 'Modul': 'iNaturalist'})
                        inat_cz = inat_data.get('common_name', '')
                        if not skip_existing or not _is_target_filled("[iNat] České jméno"): row_updates["[iNat] České jméno"] = inat_cz
                        if not skip_existing or not _is_target_filled("[iNat] Obrázky (URL)"): row_updates["[iNat] Obrázky (URL)"] = ";".join(inat_data.get('photo_urls', []))
                    except Exception:
                        row_unfounds.append({'Řádek': idx + 1, 'Položka': str(row.get(inat_col, "")), 'Modul': 'iNaturalist (Chyba)'})

                if enable_desc and not _is_target_filled("[Popis] Popis z Wikipedie"):
                    try:
                        raw_sp = str(row[desc_col]).strip()
                        sp = re.sub(r'\s*\(.*\)\s*', '', raw_sp).strip()
                        sp_clean = re.sub(r'\s+sp(p)?\.?$', '', sp).strip()
                        desc_text = fetch_wiki_description(sp_clean)
                        if not desc_text:
                            row_unfounds.append({'Řádek': idx + 1, 'Položka': raw_sp, 'Modul': 'Popis z Wikipedie'})
                        row_updates["[Popis] Popis z Wikipedie"] = desc_text
                    except Exception:
                        row_unfounds.append({'Řádek': idx + 1, 'Položka': str(row.get(desc_col, "")), 'Modul': 'Popis z Wikipedie (Chyba)'})

                gbif_check_cols = ["[GBIF] Říše", "[GBIF] Kmen", "[GBIF] Třída", "[GBIF] Řád", "[GBIF] Čeleď", "[GBIF] Rod"]
                if enable_gbif and not (skip_existing and all(_is_target_filled(c) for c in gbif_check_cols)):
                    try:
                        raw_sp = str(row[gbif_col]).strip()
                        sp = re.sub(r'\s*\(.*\)\s*', '', raw_sp).strip()
                        sp_clean = re.sub(r'\s+sp(p)?\.?$', '', sp).strip()
                        gbif_data = fetch_gbif_taxonomy(sp_clean)
                        if gbif_data.get('source') == 'Nenalezeno':
                            row_unfounds.append({'Řádek': idx + 1, 'Položka': raw_sp, 'Modul': 'GBIF Taxonomie'})
                        if not skip_existing or not _is_target_filled("[GBIF] Říše"): row_updates["[GBIF] Říše"] = gbif_data.get('kingdom', '')
                        if not skip_existing or not _is_target_filled("[GBIF] Kmen"): row_updates["[GBIF] Kmen"] = gbif_data.get('phylum', '')
                        if not skip_existing or not _is_target_filled("[GBIF] Třída"): row_updates["[GBIF] Třída"] = gbif_data.get('class', '')
                        if not skip_existing or not _is_target_filled("[GBIF] Řád"): row_updates["[GBIF] Řád"] = gbif_data.get('order', '')
                        if not skip_existing or not _is_target_filled("[GBIF] Čeleď"): row_updates["[GBIF] Čeleď"] = gbif_data.get('family', '')
                        if not skip_existing or not _is_target_filled("[GBIF] Rod"): row_updates["[GBIF] Rod"] = gbif_data.get('genus', '')
                    except Exception:
                        row_unfounds.append({'Řádek': idx + 1, 'Položka': str(row.get(gbif_col, "")), 'Modul': 'GBIF Taxonomie (Chyba)'})

                if enable_wiki_img:
                    try:
                        kw = str(row[wiki_img_col]).strip()
                        wiki_urls = fetch_wikimedia_images(kw, wiki_max_photos)
                        if not wiki_urls:
                            row_unfounds.append({'Řádek': idx + 1, 'Položka': kw, 'Modul': 'Wikimedia Commons'})
                        row_updates["[Wikimedia] Obrázky (URL)"] = ";".join(wiki_urls)
                    except Exception:
                        row_unfounds.append({'Řádek': idx + 1, 'Položka': str(row.get(wiki_img_col, "")), 'Modul': 'Wikimedia Commons (Chyba)'})

                if enable_trans:
                    try:
                        txt = str(row[trans_col]).strip()
                        src_code = languages[trans_src]
                        tgt_code = languages[trans_tgt]
                        translated = translate_text(txt, src_code, tgt_code)
                        row_updates[f"[Překlad] {trans_tgt}"] = translated
                    except Exception:
                        pass

                if enable_tts:
                    txt = str(row[tts_col]).strip()
                    lang_code = languages[tts_lang]
                    if txt:
                        row_updates["[TTS] Výslovnost (Audio)"] = f"{txt};{lang_code}"

                if enable_latin_tts:
                    try:
                        raw_sp = str(row[latin_tts_col]).strip()
                        sp_clean = re.sub(r'\s*\(.*\)\s*', '', raw_sp).strip()
                        sp_clean = re.sub(r'\s+sp(p)?\.?$', '', sp_clean).strip()
                        if sp_clean:
                            row_updates["[TTS] Latina"] = f"{sp_clean};la"
                    except Exception:
                        pass

                if enable_latin_phonetic:
                    try:
                        raw_sp = str(row[latin_phonetic_col]).strip()
                        phonetic_val = transcribe_latin_to_czech_phonetics(raw_sp)
                        if phonetic_val:
                            row_updates["[Latina] Fonetická výslovnost"] = phonetic_val
                    except Exception:
                        pass

                if enable_dict:
                    try:
                        wd = str(row[dict_col]).strip()
                        dict_data = fetch_dictionary_data(wd)
                        if not dict_data.get('definition'):
                            row_unfounds.append({'Řádek': idx + 1, 'Položka': wd, 'Modul': 'Slovník'})
                        row_updates["[Slovník] Výslovnost (Text)"] = dict_data.get('phonetic', '')
                        row_updates["[Slovník] Definice"] = dict_data.get('definition', '')
                        row_updates["[Slovník] Příkladová věta"] = dict_data.get('example', '')
                    except Exception:
                        row_unfounds.append({'Řádek': idx + 1, 'Položka': str(row.get(dict_col, "")), 'Modul': 'Slovník (Chyba)'})

                if enable_pladias_photos:
                    try:
                        raw_sp = str(row[pladias_photos_col]).strip()
                        species_items = fetch_pladias_species_images(raw_sp)
                        target_cats = pladias_photos_parts if pladias_photos_parts else ["Všechny fotky dohromady (obecný sloupec)"]
                        has_any_photo = False
                        for cat_opt in target_cats:
                            if cat_opt in PLADIAS_CATEGORY_MAPPING:
                                col_name, succs = PLADIAS_CATEGORY_MAPPING[cat_opt]
                                cat_photos = extract_pladias_category_photos(
                                    species_items,
                                    succs,
                                    max_photos=pladias_photos_max,
                                    fallback=pladias_photos_fallback
                                )
                                if cat_photos:
                                    has_any_photo = True
                                    row_updates[col_name] = ";".join(cat_photos)
                        if has_any_photo:
                            is_flora_plant = True
                        else:
                            row_unfounds.append({'Řádek': idx + 1, 'Položka': raw_sp, 'Modul': 'Pladias.cz Fotky'})
                    except Exception:
                        row_unfounds.append({'Řádek': idx + 1, 'Položka': str(row.get(pladias_photos_col, "")), 'Modul': 'Pladias.cz Fotky (Chyba)'})

                p_tax_check = ["[Pladias] Oddělení", "[Pladias] Třída", "[Pladias] Řád", "[Pladias] Čeleď", "[Pladias] Rod"]
                if enable_pladias_czech_name:
                    p_tax_check.append("[Pladias] České jméno")
                if enable_pladias_tax and not (skip_existing and all(_is_target_filled(c) for c in p_tax_check)):
                    try:
                        raw_sp = str(row[pladias_tax_col]).strip()
                        p_tax = fetch_pladias_taxonomy(raw_sp)
                        if p_tax.get("source") != "Nenalezeno":
                            is_flora_plant = True
                            if enable_pladias_czech_name and p_tax.get("czech_name"):
                                cz_val = p_tax.get("czech_name", "").strip()
                                if not skip_existing or not _is_target_filled("[Pladias] České jméno"):
                                    row_updates["[Pladias] České jméno"] = cz_val
                                for c_cand in ["České jméno", "Český název", "ceske_jmeno"]:
                                    if c_cand in new_df.columns and not _is_target_filled(c_cand):
                                        row_updates[c_cand] = cz_val
                            if not skip_existing or not _is_target_filled("[Pladias] Oddělení"): row_updates["[Pladias] Oddělení"] = p_tax.get("phylum", "")
                            if not skip_existing or not _is_target_filled("[Pladias] Třída"): row_updates["[Pladias] Třída"] = p_tax.get("class", "")
                            if not skip_existing or not _is_target_filled("[Pladias] Řád"): row_updates["[Pladias] Řád"] = p_tax.get("order", "")
                            if not skip_existing or not _is_target_filled("[Pladias] Čeleď"): row_updates["[Pladias] Čeleď"] = p_tax.get("family", "")
                            if not skip_existing or not _is_target_filled("[Pladias] Rod"): row_updates["[Pladias] Rod"] = p_tax.get("genus", "")
                        else:
                            row_unfounds.append({'Řádek': idx + 1, 'Položka': raw_sp, 'Modul': 'Pladias.cz Taxonomie'})
                    except Exception:
                        row_unfounds.append({'Řádek': idx + 1, 'Položka': str(row.get(pladias_tax_col, "")), 'Modul': 'Pladias.cz Taxonomie (Chyba)'})

                if enable_klic_2019:
                    try:
                        raw_sp = str(row[klic_2019_col]).strip()
                        k1 = query_klic_2019(raw_sp)
                        if k1:
                            is_flora_plant = True
                            row_updates["[Klíč 2019] Jméno & Autorita"] = k1.get("key_full", "")
                            row_updates["[Klíč 2019] České jméno"] = k1.get("name_cz", "")
                        else:
                            row_unfounds.append({'Řádek': idx + 1, 'Položka': raw_sp, 'Modul': 'Klíč 2019'})
                    except Exception:
                        row_unfounds.append({'Řádek': idx + 1, 'Položka': str(row.get(klic_2019_col, "")), 'Modul': 'Klíč 2019 (Chyba)'})

                if enable_nepuvodni:
                    try:
                        raw_sp = str(row[nepuvodni_col]).strip()
                        k2 = query_nepuvodni_flora(raw_sp)
                        if k2:
                            is_flora_plant = True
                            row_updates["[Nepůvodní flóra] Invazní status & Původ"] = k2.get("formatted", "")
                        else:
                            row_updates["[Nepůvodní flóra] Invazní status & Původ"] = "Původní druh v ČR (není v katalogu nepůvodních)"
                    except Exception:
                        row_unfounds.append({'Řádek': idx + 1, 'Položka': str(row.get(nepuvodni_col, "")), 'Modul': 'Nepůvodní druhy (Chyba)'})

                if enable_biotopy:
                    try:
                        raw_sp = str(row[biotopy_col]).strip()
                        k3 = query_biotopy(raw_sp)
                        if k3 and k3.get("formatted"):
                            is_flora_plant = True
                            row_updates["[Biotopy] Výskyt v biotopech ČR"] = k3.get("formatted", "")
                        else:
                            row_unfounds.append({'Řádek': idx + 1, 'Položka': raw_sp, 'Modul': 'Biotopy ČR'})
                    except Exception:
                        row_unfounds.append({'Řádek': idx + 1, 'Položka': str(row.get(biotopy_col, "")), 'Modul': 'Biotopy ČR (Chyba)'})

                if enable_ellenberg:
                    try:
                        raw_sp = str(row[ellenberg_col]).strip()
                        k4 = query_ellenberg(raw_sp)
                        if k4 and k4.get("formatted"):
                            is_flora_plant = True
                            row_updates["[Ekologie] Ellenbergovy hodnoty"] = k4.get("formatted", "")
                        else:
                            row_unfounds.append({'Řádek': idx + 1, 'Položka': raw_sp, 'Modul': 'Ellenbergovy hodnoty'})
                    except Exception:
                        row_unfounds.append({'Řádek': idx + 1, 'Položka': str(row.get(ellenberg_col, "")), 'Modul': 'Ellenbergovy hodnoty (Chyba)'})

                if enable_pladias_map and not _is_target_filled("[Pladias.cz] Mapa rozšíření"):
                    try:
                        raw_sp = str(row[pladias_map_col]).strip()
                        sp_clean = re.sub(r'\s*\(.*\)\s*', '', raw_sp).strip()
                        sp_clean = re.sub(r'\s+sp(p)?\.?$', '', sp_clean).strip()
                        if is_flora_plant or query_klic_2019(sp_clean) or query_nepuvodni_flora(sp_clean):
                            row_updates["[Pladias.cz] Mapa rozšíření"] = f"https://pladias.cz/taxon/distribution/{urllib.parse.quote(sp_clean)}"
                        else:
                            row_updates["[Pladias.cz] Mapa rozšíření"] = ""
                    except Exception:
                        row_unfounds.append({'Řádek': idx + 1, 'Položka': str(row.get(pladias_map_col, "")), 'Modul': 'Pladias.cz Mapa (Chyba)'})

                if enable_pladias:
                    try:
                        raw_sp = str(row[pladias_col]).strip()
                        sp_clean = re.sub(r'\s*\(.*\)\s*', '', raw_sp).strip()
                        sp_clean = re.sub(r'\s+sp(p)?\.?$', '', sp_clean).strip()
                        if is_flora_plant or query_klic_2019(sp_clean) or query_nepuvodni_flora(sp_clean):
                            encoded_sp = urllib.parse.quote(sp_clean)
                            row_updates["[Pladias] Odkaz"] = f"https://pladias.cz/taxon/overview/{encoded_sp}"
                        else:
                            row_updates["[Pladias] Odkaz"] = ""
                    except Exception:
                        pass

                if enable_cerveny_seznam:
                    try:
                        raw_sp = str(row[cerveny_seznam_col]).strip()
                        k5 = query_cerveny_seznam(raw_sp)
                        if k5 and (k5.get("formatted") or k5.get("author")):
                            row_updates["[Červený seznam] Kategorie ohrožení"] = k5.get("formatted", "")
                            url_val = k5.get("url", "").strip()
                            if enable_cerveny_seznam_url and "[Červený seznam] Odkaz" in new_df.columns:
                                row_updates["[Červený seznam] Odkaz"] = url_val if url_val.startswith("http") else ""
                        else:
                            row_unfounds.append({'Řádek': idx + 1, 'Položka': raw_sp, 'Modul': 'Červený seznam ČR'})
                    except Exception:
                        row_unfounds.append({'Řádek': idx + 1, 'Položka': str(row.get(cerveny_seznam_col, "")), 'Modul': 'Červený seznam ČR (Chyba)'})

                if enable_kvetena_cr:
                    try:
                        raw_sp = str(row[kvetena_cr_col]).strip()
                        actual_max = 0 if cfg.get("kvetena_cr_full", False) else kvetena_cr_max_chars
                        kv_desc = fetch_kvetena_cr_description(raw_sp, max_chars=actual_max)
                        if kv_desc:
                            row_updates["[Květena ČR] Popis druhu"] = kv_desc
                        else:
                            row_unfounds.append({'Řádek': idx + 1, 'Položka': raw_sp, 'Modul': 'Květena ČR (Popis)'})
                    except Exception:
                        row_unfounds.append({'Řádek': idx + 1, 'Položka': str(row.get(kvetena_cr_col, "")), 'Modul': 'Květena ČR (Chyba)'})

                is_bryo = False
                if enable_bryo_photos or enable_bryo_desc or enable_bryo_link:
                    raw_sp_bryo = ""
                    try:
                        for c_cand in [bryo_photo_col if enable_bryo_photos else None,
                                       bryo_desc_col if enable_bryo_desc else None,
                                       bryo_link_col if enable_bryo_link else None]:
                            if c_cand and c_cand in row:
                                raw_sp_bryo = str(row[c_cand]).strip()
                                if raw_sp_bryo:
                                    break
                        if not raw_sp_bryo and len(columns) > 0:
                            raw_sp_bryo = str(row[columns[0]]).strip()

                        sp_bryo_clean = re.sub(r'\s*\(.*\)\s*', '', raw_sp_bryo).strip()
                        sp_bryo_clean = re.sub(r'\s+sp(p)?\.?$', '', sp_bryo_clean).strip()

                        if k5 and "mechorost" in str(k5.get("group", "")).lower():
                            is_bryo = True
                        elif gbif_data and gbif_data.get("phylum") in ["Bryophyta", "Marchantiophyta", "Anthocerotophyta"]:
                            is_bryo = True
                        elif not (is_flora_plant or dalib_data.get("source") != "Nenalezeno" or myko_data.get("source") != "Nenalezeno" or (c_data and c_data.get("common_name"))):
                            try:
                                _chk_b = requests.get(f"https://api.gbif.org/v1/species/match?name={urllib.parse.quote(sp_bryo_clean)}&strict=true", timeout=4).json()
                                if _chk_b.get("phylum") in ["Bryophyta", "Marchantiophyta", "Anthocerotophyta"] or (_chk_b.get("kingdom") == "Plantae" and _chk_b.get("matchType") not in ["NONE", "HIGHERRANK"] and _chk_b.get("class") in ["Bryopsida", "Sphagnopsida", "Jungermanniopsida", "Marchantiopsida", "Polytrichopsida"]):
                                    is_bryo = True
                            except Exception:
                                pass

                        if is_bryo:
                            if enable_bryo_photos:
                                b_photos = fetch_bryophyte_photos(sp_bryo_clean, max_photos=bryo_photos_max)
                                if b_photos:
                                    row_updates["[Mechorosty] Fotky"] = ";".join(b_photos[:bryo_photos_max])
                            if enable_bryo_desc:
                                b_desc = fetch_bryophyte_description(sp_bryo_clean)
                                if b_desc:
                                    row_updates["[Mechorosty] Popis"] = b_desc
                            if enable_bryo_link:
                                row_updates["[Mechorosty] Odkaz"] = f"https://bryophyteportal.org/portal/taxa/index.php?taxon={urllib.parse.quote(sp_bryo_clean)}"
                        else:
                            row_updates["[Mechorosty] Fotky"] = ""
                            row_updates["[Mechorosty] Popis"] = ""
                            row_updates["[Mechorosty] Odkaz"] = ""
                    except Exception:
                        pass

                if enable_mykologie_img or enable_mykologie_desc or enable_mykologie_link:
                    myko_check_cols = []
                    if enable_mykologie_img: myko_check_cols.append("[Mykologie.net] Fotky")
                    if enable_mykologie_desc: myko_check_cols.append("[Mykologie.net] Popis")
                    if enable_mykologie_link: myko_check_cols.append("[Mykologie.net] Odkaz")

                    if skip_existing and all(_is_target_filled(c) for c in myko_check_cols):
                        pass
                    else:
                        raw_val = ""
                        try:
                            for c_cand in [mykologie_img_col if enable_mykologie_img else None,
                                           mykologie_desc_col if enable_mykologie_desc else None,
                                           mykologie_link_col if enable_mykologie_link else None]:
                                if c_cand and c_cand in row:
                                    raw_val = str(row[c_cand]).strip()
                                    if raw_val:
                                        break
                            if not raw_val and len(columns) > 0:
                                raw_val = str(row[columns] if isinstance(columns, str) else columns[0]).strip()

                            myko_data = fetch_mykologie_data(raw_val, max_photos=mykologie_img_max if enable_mykologie_img else 4)
                            if myko_data.get('source') == 'Nenalezeno':
                                row_unfounds.append({'Řádek': idx + 1, 'Položka': raw_val, 'Modul': 'Mykologie.net'})

                            if enable_mykologie_img and (not skip_existing or not _is_target_filled("[Mykologie.net] Fotky")):
                                row_updates["[Mykologie.net] Fotky"] = ";".join(myko_data.get('photo_urls', []))
                            if enable_mykologie_desc and (not skip_existing or not _is_target_filled("[Mykologie.net] Popis")):
                                row_updates["[Mykologie.net] Popis"] = myko_data.get('description', '')
                            if enable_mykologie_link and (not skip_existing or not _is_target_filled("[Mykologie.net] Odkaz")):
                                url_val = myko_data.get('url', '')
                                row_updates["[Mykologie.net] Odkaz"] = url_val if (url_val and myko_data.get('source') != 'Nenalezeno') else ""
                        except Exception:
                            row_unfounds.append({'Řádek': idx + 1, 'Položka': str(raw_val), 'Modul': 'Mykologie.net (Chyba)'})

                if enable_dalibor_photos or enable_dalibor_desc or enable_dalibor_link:
                    dalib_check_cols = []
                    if enable_dalibor_photos: dalib_check_cols.append("[DaLiBor] Fotky")
                    if enable_dalibor_desc: dalib_check_cols.append("[DaLiBor] Popis")
                    if enable_dalibor_link: dalib_check_cols.append("[DaLiBor] Odkaz")

                    if skip_existing and all(_is_target_filled(c) for c in dalib_check_cols):
                        pass
                    else:
                        raw_val = ""
                        try:
                            for c_cand in [dalibor_photos_col if enable_dalibor_photos else None,
                                           dalibor_desc_col if enable_dalibor_desc else None,
                                           dalibor_link_col if enable_dalibor_link else None]:
                                if c_cand and c_cand in row:
                                    raw_val = str(row[c_cand]).strip()
                                    if raw_val:
                                        break
                            if not raw_val and len(columns) > 0:
                                raw_val = str(row[columns] if isinstance(columns, str) else columns[0]).strip()

                            dalib_data = fetch_dalibor_data(raw_val, max_photos=dalibor_photos_max if enable_dalibor_photos else 3)
                            if dalib_data.get('source') == 'Nenalezeno':
                                row_unfounds.append({'Řádek': idx + 1, 'Položka': raw_val, 'Modul': 'DaLiBor (Lišejníky)'})

                            if enable_dalibor_photos and (not skip_existing or not _is_target_filled("[DaLiBor] Fotky")):
                                row_updates["[DaLiBor] Fotky"] = ";".join(dalib_data.get('photo_urls', []))
                            if enable_dalibor_desc and (not skip_existing or not _is_target_filled("[DaLiBor] Popis")):
                                row_updates["[DaLiBor] Popis"] = dalib_data.get('description', '')
                            if enable_dalibor_link and (not skip_existing or not _is_target_filled("[DaLiBor] Odkaz")):
                                url_val = dalib_data.get('url', '')
                                row_updates["[DaLiBor] Odkaz"] = url_val if (url_val and dalib_data.get('source') != 'Nenalezeno') else ""
                        except Exception:
                            row_unfounds.append({'Řádek': idx + 1, 'Položka': str(raw_val), 'Modul': 'DaLiBor (Chyba)'})

                if enable_diatombase_taxon or enable_diatombase_link:
                    raw_val = ""
                    try:
                        for c_cand in [diatombase_taxon_col if enable_diatombase_taxon else None,
                                       diatombase_link_col if enable_diatombase_link else None]:
                            if c_cand and c_cand in row:
                                raw_val = str(row[c_cand]).strip()
                                if raw_val:
                                    break
                        if not raw_val and len(columns) > 0:
                            raw_val = str(row[columns] if isinstance(columns, str) else columns[0]).strip()

                        diatom_data = fetch_diatombase_data(raw_val)
                        if diatom_data.get('source') == 'Nenalezeno':
                            row_unfounds.append({'Řádek': idx + 1, 'Položka': raw_val, 'Modul': 'DiatomBase'})

                        if enable_diatombase_taxon:
                            taxon_str = diatom_data.get('scientific_name', '')
                            if diatom_data.get('authority'):
                                taxon_str += f" {diatom_data.get('authority')}"
                            row_updates["[DiatomBase] Taxon & Autorita"] = taxon_str
                            row_updates["[DiatomBase] Taxonomie"] = diatom_data.get('classification', '')
                        if enable_diatombase_link:
                            url_val = diatom_data.get('url', '')
                            row_updates["[DiatomBase] Odkaz"] = url_val if (url_val and diatom_data.get('source') != 'Nenalezeno') else ""
                    except Exception:
                        row_unfounds.append({'Řádek': idx + 1, 'Položka': str(raw_val), 'Modul': 'DiatomBase (Chyba)'})

                if enable_algaebase_link:
                    try:
                        raw_sp = str(row[algaebase_link_col]).strip()

                        is_algae_cand = (
                            (k5 and any(g in k5.get("group", "").lower() for g in ["řas", "sinic", "algae", "diatom"]))
                            or (diatom_data and diatom_data.get("source") != "Nenalezeno")
                        )
                        if sp_clean and is_algae_cand:
                            row_updates["[AlgaeBase] Odkaz"] = f"https://www.algaebase.org/search/species/?name={urllib.parse.quote(sp_clean)}"
                        else:
                            row_updates["[AlgaeBase] Odkaz"] = ""
                    except Exception:
                        row_unfounds.append({'Řádek': idx + 1, 'Položka': str(row.get(algaebase_link_col, "")), 'Modul': 'AlgaeBase (Chyba)'})

                if enable_gbif_fungi:
                    try:
                        raw_sp = str(row[gbif_fungi_col]).strip()
                        fungi_photos = fetch_gbif_fungi_photos(raw_sp, max_photos=gbif_fungi_max)
                        if not fungi_photos:
                            row_unfounds.append({'Řádek': idx + 1, 'Položka': raw_sp, 'Modul': 'GBIF Houby'})
                        row_updates["[GBIF] Houby"] = ";".join(fungi_photos)
                    except Exception:
                        row_unfounds.append({'Řádek': idx + 1, 'Položka': str(row.get(gbif_fungi_col, "")), 'Modul': 'GBIF Houby (Chyba)'})

                if enable_gbif_zoo:
                    try:
                        raw_sp = str(row[gbif_zoo_col]).strip()
                        zoo_photos = fetch_gbif_zoo_photos(raw_sp, max_photos=gbif_zoo_max)
                        if not zoo_photos:
                            row_unfounds.append({'Řádek': idx + 1, 'Položka': raw_sp, 'Modul': 'GBIF Zoologie'})
                        row_updates["[GBIF] Zoologie"] = ";".join(zoo_photos)
                    except Exception:
                        row_unfounds.append({'Řádek': idx + 1, 'Položka': str(row.get(gbif_zoo_col, "")), 'Modul': 'GBIF Zoologie (Chyba)'})

                if enable_wiki_link:
                    raw_sp = str(row[wiki_link_col]).strip()
                    sp_clean = re.sub(r'\s*\(.*\)\s*', '', raw_sp).strip()
                    sp_clean = re.sub(r'\s+sp(p)?\.?$', '', sp_clean).strip()
                    if sp_clean:
                        slug_sp = sp_clean.replace(' ', '_')
                        row_updates["[Wikipedie] Odkaz"] = f"https://cs.wikipedia.org/wiki/{slug_sp}"
                    else:
                        row_updates["[Wikipedie] Odkaz"] = ""

                if enable_bird_sounds:
                    try:
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
                            row_unfounds.append({'Řádek': idx + 1, 'Položka': raw_sp, 'Modul': 'Hlasy ptáků (Xeno-canto)'})
                        row_updates["[Zvuky] Hlasy ptáků"] = ";".join(f"{u}|{t}|{att}" if att else f"{u}|{t}" for u, t, att in sound_results)
                    except Exception:
                        row_unfounds.append({'Řádek': idx + 1, 'Položka': str(row.get(bird_sounds_col, "")), 'Modul': 'Hlasy ptáků (Chyba)'})

                if enable_country:
                    try:
                        c_name = str(row[country_col]).strip()
                        c_data = fetch_country_data(c_name, countries_db)
                        if c_data.get('source') == 'Nenalezeno':
                            row_unfounds.append({'Řádek': idx + 1, 'Položka': c_name, 'Modul': 'Zeměpis'})
                        row_updates["[Zeměpis] Český název"] = c_data.get('common_name', '')
                        row_updates["[Zeměpis] Hlavní město"] = c_data.get('capital', '')
                        row_updates["[Zeměpis] Region"] = f"{c_data['region']} ({c_data['subregion']})" if c_data.get('subregion') else c_data.get('region', '')
                        row_updates["[Zeměpis] Jazyky"] = c_data.get('languages', '')
                        row_updates["[Zeměpis] Měna"] = c_data.get('currencies', '')
                        row_updates["[Zeměpis] Rozloha"] = c_data.get('area', '')
                        row_updates["[Zeměpis] Vlajka (URL)"] = c_data.get('flag_url', '')
                    except Exception:
                        row_unfounds.append({'Řádek': idx + 1, 'Položka': str(row.get(country_col, "")), 'Modul': 'Zeměpis (Chyba)'})

                _gbif_kingdom = (gbif_data.get("kingdom", "") if gbif_data else "").strip()
                _gbif_phylum  = (gbif_data.get("phylum",  "") if gbif_data else "").strip()

                if enable_adw_desc or enable_adw_link:
                    _is_animal = _gbif_kingdom == "Animalia"
                    if not _is_animal:

                        pass
                    try:
                        raw_adw = str(row[adw_col]).strip() if adw_col in row else ""
                        if raw_adw and _is_animal:
                            if enable_adw_desc:
                                adw_res = fetch_adw_description(raw_adw)
                                if adw_res:
                                    row_updates["[ADW] Biologický popis"] = adw_res
                                else:
                                    row_unfounds.append({'Řádek': idx + 1, 'Položka': raw_adw, 'Modul': 'ADW (Popis živočicha)'})
                            if enable_adw_link:
                                adw_l = get_adw_link(raw_adw)
                                if adw_l:
                                    row_updates["[ADW] Odkaz"] = adw_l
                        elif raw_adw and not _is_animal:

                            pass
                    except Exception:
                        row_unfounds.append({'Řádek': idx + 1, 'Položka': str(row.get(adw_col, "")), 'Modul': 'ADW (Chyba)'})

                if enable_gbif_desc:
                    try:
                        raw_gb_d = str(row[gbif_desc_col]).strip() if gbif_desc_col in row else ""
                        if raw_gb_d:
                            gb_desc_res = fetch_gbif_species_description(raw_gb_d)
                            if gb_desc_res:

                                _en_words = {"the", "a", "an", "is", "are", "of", "in", "and", "with", "on",
                                             "from", "to", "by", "at", "or", "for", "this", "that", "it",
                                             "has", "have", "been", "body", "leaf", "stem", "root", "species",
                                             "found", "known", "described", "habitat", "color", "colour"}
                                _words = gb_desc_res.lower().split()
                                _en_count = sum(1 for w in _words if re.sub(r"[^a-z]", "", w) in _en_words)
                                _en_ratio = _en_count / max(len(_words), 1)
                                if _en_ratio >= 0.05:
                                    row_updates["[GBIF] Vědecký popis"] = gb_desc_res
                                else:
                                    row_unfounds.append({'Řádek': idx + 1, 'Položka': raw_gb_d, 'Modul': 'GBIF TreatmentBank (pouze cizí jazyk)'})
                            else:
                                row_unfounds.append({'Řádek': idx + 1, 'Položka': raw_gb_d, 'Modul': 'GBIF TreatmentBank (Popis)'})
                    except Exception:
                        row_unfounds.append({'Řádek': idx + 1, 'Položka': str(row.get(gbif_desc_col, "")), 'Modul': 'GBIF TreatmentBank (Chyba)'})

                if enable_powo_desc or enable_powo_link:
                    _is_plant = _gbif_kingdom == "Plantae" or (
                        is_flora_plant or is_bryo or
                        (k1 is not None) or (k3 and k3.get("formatted")) or
                        (p_photos and (p_photos.get("kvet") or p_photos.get("list")))
                    )
                    try:
                        raw_powo = str(row[powo_col]).strip() if powo_col in row else ""
                        if raw_powo and _is_plant:
                            if enable_powo_desc:
                                powo_res = fetch_powo_kew_description(raw_powo)
                                if powo_res:
                                    row_updates["[POWO Kew] Popis flóry"] = powo_res
                                else:
                                    row_unfounds.append({'Řádek': idx + 1, 'Položka': raw_powo, 'Modul': 'POWO Kew (Popis)'})
                            if enable_powo_link:
                                powo_l = get_powo_kew_link(raw_powo)
                                if powo_l:
                                    row_updates["[POWO Kew] Odkaz"] = powo_l
                        elif raw_powo and not _is_plant:
                            pass
                    except Exception:
                        row_unfounds.append({'Řádek': idx + 1, 'Položka': str(row.get(powo_col, "")), 'Modul': 'POWO Kew (Chyba)'})

                if enable_eol_link:
                    try:
                        raw_eol = str(row[eol_col]).strip() if eol_col in row else ""
                        if raw_eol:
                            eol_l = get_eol_link(raw_eol)
                            if eol_l:
                                row_updates["[EOL] Odkaz"] = eol_l
                    except Exception:
                        pass

                cat_label = ""

                if c_data and c_data.get("source") != "Nenalezeno" and c_data.get("common_name"):
                    cat_label = "Zeměpis (Státy)"

                elif gbif_data and gbif_data.get("source") != "Nenalezeno" and gbif_data.get("kingdom"):
                    gbif_cat = gbif_class_to_category(
                        gbif_data.get("kingdom", ""),
                        gbif_data.get("phylum", ""),
                        gbif_data.get("class", "")
                    )
                    if gbif_cat:

                        if "Houby" in gbif_cat and dalib_data and dalib_data.get("source") != "Nenalezeno":
                            cat_label = "Lišejníky (DaLiBor)"
                        else:
                            cat_label = gbif_cat

                elif dalib_data and dalib_data.get("source") != "Nenalezeno" and (dalib_data.get("photo_urls") or dalib_data.get("description")):
                    cat_label = "Lišejníky (DaLiBor)"
                elif myko_data and myko_data.get("source") != "Nenalezeno" and (myko_data.get("photo_urls") or myko_data.get("description")):
                    cat_label = "Houby (Mykologie.net)"
                elif diatom_data and diatom_data.get("source") != "Nenalezeno" and diatom_data.get("scientific_name"):
                    cat_label = "Rozsivky (DiatomBase)"
                elif sound_results:
                    cat_label = "Ptáci (Aves)"
                elif is_bryo or (b_photos if 'b_photos' in locals() and b_photos else False):
                    cat_label = "Mechorosty – mechy (Bryophyta)"
                elif is_flora_plant or k1 or (k3 and k3.get("formatted")) or (k4 and k4.get("formatted")) or (p_photos and (p_photos.get("kvet") or p_photos.get("list") or p_photos.get("herbar"))):
                    cat_label = "Cévnaté rostliny (Tracheophyta)"
                elif zoo_photos:
                    cat_label = "Živočichové – ostatní"
                elif fungi_photos:
                    cat_label = "Houby (Fungi)"

                elif k5 and k5.get("group"):
                    cat_label = k5.get("group")
                elif k_red_check and k_red_check.get("group"):
                    cat_label = k_red_check.get("group")

                else:
                    _existing_cat = ""
                    for _cat_col in ("[Kategorie]", "Kategorie", "kategorie"):
                        if _cat_col in new_df.columns:
                            _v = str(row.get(_cat_col, "")).strip()
                            if _v and _v not in ("nan", ""):
                                _existing_cat = _v
                                break
                    if _existing_cat:
                        ec = _existing_cat.lower()
                        if any(w in ec for w in ["rostlin", "cévnat", "tracheoph", "magnoliop", "liliop", "herb", "květ", "strom", "keř", "tráv"]):
                            cat_label = "Cévnaté rostliny (Tracheophyta)"
                        elif any(w in ec for w in ["mech", "játrovk", "hlevík", "bryoph", "marchant"]):
                            cat_label = "Mechorosty – mechy (Bryophyta)"
                        elif any(w in ec for w in ["houb", "fungi", "mycet", "basidio", "ascomyc", "agar"]):
                            cat_label = "Houby (Fungi)"
                        elif any(w in ec for w in ["lišejník", "lichen", "dalib"]):
                            cat_label = "Lišejníky (DaLiBor)"
                        elif any(w in ec for w in ["pták", "aves", "bird"]):
                            cat_label = "Ptáci (Aves)"
                        elif any(w in ec for w in ["savec", "mammal"]):
                            cat_label = "Savci (Mammalia)"
                        elif any(w in ec for w in ["hmyz", "insect"]):
                            cat_label = "Hmyz (Insecta)"
                        elif any(w in ec for w in ["rozsivk", "řas", "algae", "bacillario", "chloroph"]):
                            cat_label = "Rozsivky / Řasy"
                        elif any(w in ec for w in ["zeměpis", "stát", "kontinent", "geograph"]):
                            cat_label = "Zeměpis (Státy)"
                        elif any(w in ec for w in ["slovník", "jazyk", "vocab", "dict"]):
                            cat_label = "Jazyky a slovník"
                        else:
                            cat_label = _existing_cat

                if not cat_label:
                    if dict_data and dict_data.get("definition"):
                        cat_label = "Jazyky a slovník"
                    elif inat_cz or (inat_data and inat_data.get("source") != "Nenalezeno" and inat_data.get("photo_urls")):
                        cat_label = "iNaturalist"
                    else:
                        cat_label = "Ostatní / Nezařazeno"

                return idx, row_updates, row_unfounds

            total = len(df)
            unfound_list = []

            for idx, row in df.iterrows():
                pct = idx / total if total > 0 else 0.0
                progress_bar.progress(pct)
                current_item = str(row[columns[0]]).strip() if len(columns) > 0 else f"Položka {idx + 1}"
                status.text(f"Obohacování dat: {idx + 1}/{total} ({int(pct * 100)}%) — {current_item}...")

                try:
                    r_idx, r_updates, r_unfounds = _enrich_single_row(idx, row)
                    for c_col, c_val in r_updates.items():
                        new_df.at[r_idx, c_col] = c_val
                    unfound_list.extend(r_unfounds)
                except Exception:
                    pass

            progress_bar.progress(1.0)
            status.text(f"Obohacování dat dokončeno ({total}/{total} položek).")

            st.session_state.df = new_df
            st.session_state.enhancements_applied = True
            st.session_state.unfound_list = unfound_list
            st.session_state.enrichment_success_info = {
                "rows": len(new_df),
                "cols": len(new_df.columns),
                "unfound": len(unfound_list)
            }
            gc.collect()
            st.rerun()

    with st.expander("4. Výběr výstupního formátu a obsahu", expanded=False):

        active_cols_for_desc = list(dict.fromkeys(st.session_state.front_cols_ordered + st.session_state.back_cols_ordered))
        has_pladias = any(("[Pladias]" in str(c) or "[Pladias.cz]" in str(c)) for c in active_cols_for_desc)
        has_myko = any("[Mykologie.net]" in str(c) for c in active_cols_for_desc)
        has_dalibor = any("[DaLiBor]" in str(c) for c in active_cols_for_desc)
        has_diatom = any("[DiatomBase]" in str(c) for c in active_cols_for_desc)
        has_algae = any("[AlgaeBase]" in str(c) for c in active_cols_for_desc)
        has_attribution = has_pladias or has_myko or has_dalibor or has_diatom or has_algae
        default_attribution_desc = build_deck_attribution(active_cols_for_desc) if has_attribution else ""

        tab_anki, tab_obsidian, tab_pdf, tab_docx = st.tabs([
            "1. Balíček pro Anki (.apkg)",
            "2. Kartičky pro mobil i PC (.zip / HTML / Obsidian)",
            "3. Studijní brožura v PDF (.pdf)",
            "4. Dokument ve Wordu (.docx)"
        ])

        with tab_anki:
            st.markdown("#### Návrh kartiček Anki (Líc / Rub) a export")
            col_map_settings, col_visual_preview = st.columns([1.1, 0.9], gap="large")

            with col_map_settings:
                col_lay1, col_lay2 = st.columns(2)

                with col_lay1:
                    st.markdown("#### 1. Lícová strana")
                    front_cols = st.multiselect(
                        "Vyberte sloupce na LÍCI karty:",
                        options=columns,
                        default=[columns[0]] if columns else [],
                        key="front_cols_multiselect"
                    )
                    sync_ordered_cols(front_cols, "front_cols_ordered")

                    with st.expander("Změnit pořadí sloupců na líci (▲ / ▼)", expanded=False):
                        for i, col in enumerate(st.session_state.front_cols_ordered):
                            if col not in st.session_state.col_styles:
                                is_img = check_col_is_image(col, st.session_state.df)
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
                    st.markdown("#### 2. Rubová strana")
                    default_back = [c for c in columns if c not in front_cols and not c.startswith("[")]
                    if not default_back and columns:
                        default_back = [columns[0]]
                    back_cols = st.multiselect(
                        "Vyberte sloupce na RUBU karty:",
                        options=columns,
                        default=default_back,
                        key="back_cols_multiselect"
                    )
                    sync_ordered_cols(back_cols, "back_cols_ordered")

                    with st.expander("Změnit pořadí sloupců na rubu (▲ / ▼)", expanded=False):
                        for i, col in enumerate(st.session_state.back_cols_ordered):
                            if col not in st.session_state.col_styles:
                                is_img = check_col_is_image(col, st.session_state.df)
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

                st.markdown("#### Vzhled a rozvržení")
                c_theme1, c_theme2 = st.columns(2)
                with c_theme1:
                    card_theme = st.selectbox(
                        "Barevný režim karet:",
                        [
                            "Obojetný (automaticky přepínatelný)",
                            "Tmavý režim (vždy tmavé)",
                            "Světlý režim (vždy světlé)"
                        ],
                        index=0
                    )
                with c_theme2:
                    card_layout_choice = st.radio(
                        "Zobrazení po kliknutí na odpověď:",
                        ["Pod sebe (líc + rub)", "Na druhou stranu (pouze rub)"],
                        index=0,
                        key="card_layout_radio"
                    )
                show_media_attribution = st.checkbox(
                    "Zobrazovat autory a licence (CC) u fotografií a nahrávek",
                    value=True,
                    key="show_media_attribution"
                )

                st.markdown("#### Režim zkoušení v Anki (Typ kartiček)")
                c_mode1, c_mode2 = st.columns([1.1, 1.9])
                with c_mode1:
                    anki_card_test_type = st.radio(
                        "Způsob testování:",
                        ["Standardní (otočení kliknutím)", "Vepisovací (psaní z klávesnice)"],
                        index=0,
                        key="anki_card_test_type_radio"
                    )
                is_type_in = "Vepisovací" in anki_card_test_type
                st.session_state.is_type_in = is_type_in
                type_target_col = None
                with c_mode2:
                    if is_type_in:
                        type_options = st.session_state.back_cols_ordered if st.session_state.back_cols_ordered else columns
                        type_target_col = st.selectbox(
                            "Pole, které má uživatel vepsat z klávesnice:",
                            options=type_options,
                            index=0,
                            key="anki_type_target_col"
                        )
                        st.session_state.type_target_col = type_target_col
                        st.caption("Anki zobrazí na líci textové pole. Po stisku Enter automaticky písmeno po písmenu zkontroluje pravopis (zeleně správná písmena, červeně překlepy a chyby).")
                    else:
                        st.session_state.type_target_col = None

                all_selected_cols = list(dict.fromkeys(st.session_state.front_cols_ordered + st.session_state.back_cols_ordered))
                text_cols_to_style = [
                    c for c in all_selected_cols
                    if not (check_col_is_image(c, st.session_state.df) or is_image_col(c) or any(img_kw in c.lower() for img_kw in ["foto", "fotka", "obrázek", "obrazek", "habitus", "květ", "kvet", "list", "plod", "herbář", "herbar", "detail", "mikrofoto"]))
                ]
                if text_cols_to_style:
                    with st.expander("Pokročilé nastavení zobrazení sloupců (formátování textu)", expanded=False):
                        for col in text_cols_to_style:
                            if col not in st.session_state.col_styles:
                                st.session_state.col_styles[col] = {
                                    "bold": False,
                                    "italic": False,
                                    "size": "Výchozí",
                                    "custom_label": col,
                                    "show_label": True
                                }
                            style = st.session_state.col_styles[col]
                            st.markdown(f"**Sloupec: {col}**")
                            sc1, sc2, sc3 = st.columns([1.2, 1.4, 1.4])
                            with sc1:
                                style["bold"] = st.checkbox("Tučné", value=style["bold"], key=f"style_bold_{col}")
                                style["italic"] = st.checkbox("Kurzíva", value=style["italic"], key=f"style_italic_{col}")
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
                                style["show_label"] = st.checkbox("Zobrazit název pole", value=style["show_label"], key=f"style_show_lbl_{col}")
                                style["custom_label"] = st.text_input("Vlastní název pole:", value=style["custom_label"], key=f"style_cust_lbl_{col}")

            with col_visual_preview:
                st.markdown("#### Vizuální náhled kartičky")
                if st.session_state.front_cols_ordered or st.session_state.back_cols_ordered:
                    c_prev_r1, c_prev_r2 = st.columns([2, 1])
                    with c_prev_r1:
                        row_idx = st.number_input(
                            f"Náhled pro řádek (1 z {len(df)}):",
                            min_value=1,
                            max_value=max(1, len(df)),
                            value=1,
                            step=1,
                            key="card_preview_row_selector"
                        ) - 1
                    with c_prev_r2:
                        st.caption("Živý náhled v reálném čase")

                    preview_row = df.iloc[row_idx]
                    show_media_attr_val = st.session_state.get("show_media_attribution", True)

                    is_light_card_preview = (card_theme == "Světlý režim (vždy světlé)") or (card_theme == "Obojetný (automaticky přepínatelný)" and is_light_ui)
                    if is_light_card_preview:
                        preview_bg = "#ffffff"
                        preview_fg = "#1f2937"
                        preview_border = "#e5e7eb"
                        preview_label = "#6b7280"
                    else:
                        preview_bg = "#2f2f31"
                        preview_fg = "#f4f4f5"
                        preview_border = "#3f3f46"
                        preview_label = "#a1a1aa"

                    tab_prev_front, tab_prev_back = st.tabs(["Líc", "Rub"])

                    with tab_prev_front:
                        with st.container(border=True):
                            if not st.session_state.front_cols_ordered:
                                st.caption("Na líci nejsou vybrány žádné sloupce.")
                            for c in st.session_state.front_cols_ordered:
                                val = preview_row[c] if c in preview_row else ""
                                if pd.isna(val) or str(val).strip() == "":
                                    continue

                                show_label = True
                                label_text = c
                                if c in st.session_state.col_styles:
                                    show_label = st.session_state.col_styles[c].get("show_label", True)
                                    label_text = st.session_state.col_styles[c].get("custom_label", c)

                                val_css = get_value_css(c)
                                val_style_attr = f' style="{val_css}; color: {preview_fg} !important;"' if val_css else f' style="color: {preview_fg} !important;"'
                                label_html = f'<span style="font-size: 11px; font-weight: 600; color: {preview_label}; text-transform: uppercase; border-bottom: 1px solid {preview_border}; display: block; margin-bottom: 4px; padding-bottom: 2px;">{label_text}</span>' if show_label else ''

                                if c in ["[Pladias] Mapa rozšíření", "[Pladias.cz] Mapa rozšíření"]:
                                    if label_html:
                                        st.markdown(label_html, unsafe_allow_html=True)
                                    map_species = ""
                                    if "distribution/" in str(val):
                                        map_species = str(val).split("distribution/")[-1].split("?")[0].strip().replace("%20", " ")
                                    if not map_species and columns:
                                        map_species = str(preview_row.get(columns[0], "")).strip()
                                    map_img_path = get_or_render_pladias_map_image(map_species)
                                    if map_img_path and os.path.isfile(map_img_path):
                                        img_src = format_img_src_for_html(map_img_path)
                                        caption_html = f'<div style="font-size: 10px; color: {preview_label}; margin-top: 3px; text-align: center; opacity: 0.85;">Pladias.cz • Mapa rozšíření ČR</div>' if show_media_attr_val else ''
                                        st.markdown(f'<div style="width: 100%; max-width: 450px; border-radius: 6px; overflow: hidden; border: 1px solid {preview_border}; margin: 8px 0; padding-bottom: 4px;"><img src="{img_src}" style="width: 100%; height: auto; object-fit: contain; display: block;">{caption_html}</div>', unsafe_allow_html=True)
                                    else:
                                        st.markdown(f'<div style="padding: 10px; border-radius: 6px; border: 1px solid {preview_border}; background: rgba(0,0,0,0.04); margin: 6px 0;"><a href="{val}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Zobrazit mapu rozšíření na Pladias.cz ({map_species})</a></div>', unsafe_allow_html=True)
                                elif c in ["[iNaturalist] Mapa nálezů", "[iNaturalist] Mapa pozorování", "[iNat] Mapa pozorování"] or ("inat" in str(c).lower() and "map" in str(c).lower()):
                                    if label_html:
                                        st.markdown(label_html, unsafe_allow_html=True)
                                    map_species = str(preview_row.get(columns[0], "")).strip() if columns else ""
                                    map_img_path = get_or_render_inat_map_image(map_species, str(val))
                                    if map_img_path and os.path.isfile(map_img_path):
                                        img_src = format_img_src_for_html(map_img_path)
                                        caption_html = f'<div style="font-size: 10px; color: {preview_label}; margin-top: 3px; text-align: center; opacity: 0.85;">iNaturalist.org • Mapa pozorování</div>' if show_media_attr_val else ''
                                        st.markdown(f'<div style="width: 100%; max-width: 450px; border-radius: 6px; overflow: hidden; border: 1px solid {preview_border}; margin: 8px 0; padding-bottom: 4px;"><img src="{img_src}" style="width: 100%; height: auto; object-fit: contain; display: block;">{caption_html}</div>', unsafe_allow_html=True)
                                    else:
                                        st.markdown(f'<div style="padding: 10px; border-radius: 6px; border: 1px solid {preview_border}; background: rgba(0,0,0,0.04); margin: 6px 0;"><a href="{val}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Zobrazit mapu pozorování na iNaturalist.org</a></div>', unsafe_allow_html=True)
                                elif is_image_col(c, val):
                                    raw_entries = [u.strip() for u in str(val).split(';') if u.strip()]
                                    if label_html:
                                        st.markdown(label_html, unsafe_allow_html=True)
                                    for entry in raw_entries:
                                        if '|' in entry:
                                            u_parts = entry.split('|', 1)
                                            img_url = u_parts[0].strip()
                                            attr_txt = u_parts[1].strip()
                                        else:
                                            img_url = entry.strip()
                                            attr_txt = ""
                                        img_src = format_img_src_for_html(img_url)
                                        caption_html = f'<div style="font-size: 10px; color: {preview_label}; margin-top: 3px; text-align: center; opacity: 0.85;">{attr_txt}</div>' if (show_media_attr_val and attr_txt) else ''
                                        st.markdown(f'<div style="width: 100%; max-width: 450px; border-radius: 6px; overflow: hidden; border: 1px solid {preview_border}; margin: 8px 0; padding-bottom: 4px;"><img src="{img_src}" style="width: 100%; height: auto; object-fit: contain; display: block;">{caption_html}</div>', unsafe_allow_html=True)
                                elif str(c).startswith("[TTS]"):
                                    st.info(f"Výslovnost (Audio): {str(val).split(';')[0]}")
                                elif c == "[Zvuky] Hlasy ptáků":
                                    entries = [e.strip() for e in str(val).split(';') if e.strip()]
                                    if label_html:
                                        st.markdown(label_html, unsafe_allow_html=True)
                                    for entry in entries:
                                        parts = entry.split('|')
                                        su = parts[0].strip()
                                        stype = parts[1].strip() if len(parts) > 1 else "song"
                                        sattr = parts[2].strip() if len(parts) > 2 else ""
                                        if not su.startswith('http'):
                                            continue
                                        type_label = "Zpěv" if stype == "song" else "Hlas"
                                        if show_media_attr_val and sattr:
                                            st.caption(f"{type_label} • {sattr}")
                                        else:
                                            st.caption(type_label)
                                        st.audio(su)
                                else:
                                    if label_html:
                                        st.markdown(label_html, unsafe_allow_html=True)
                                    val_str = str(val)
                                    if val_str.startswith("http://") or val_str.startswith("https://"):
                                        if "pladias.cz" in val_str:
                                            val_str = f'<a href="{val_str}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Otevřít profil na Pladias.cz</a>'
                                        elif "mykologie.net" in val_str:
                                            val_str = f'<a href="{val_str}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Otevřít profil na Mykologie.net</a>'
                                        elif "dalib.cz" in val_str:
                                            val_str = f'<a href="{val_str}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Otevřít profil na DaLiBor</a>'
                                        elif "diatombase.org" in val_str:
                                            val_str = f'<a href="{val_str}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Otevřít profil na DiatomBase</a>'
                                        elif "algaebase.org" in val_str:
                                            val_str = f'<a href="{val_str}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Otevřít vyhledávání na AlgaeBase</a>'
                                        elif "inaturalist.org" in val_str:
                                            val_str = f'<a href="{val_str}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Otevřít mapu pozorování na iNaturalist.org &rarr;</a>'
                                        elif "mushroomcoloratlas.com" in val_str:
                                            val_str = f'<a href="{val_str}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Otevřít Mushroom Color Atlas (Pigmenty a barviva)</a>'
                                        elif "wikipedia.org" in val_str:
                                            val_str = f'<a href="{val_str}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Otevřít profil na Wikipedii</a>'
                                    elif not re.search(r'<[a-zA-Z0-9/]+[^>]*>', val_str):
                                        val_str = val_str.replace('\n', '<br>')
                                    st.markdown(f'<div{val_style_attr}>{val_str}</div>', unsafe_allow_html=True)
                            if is_type_in and type_target_col:
                                st.markdown(f"""
                                <div style="margin: 14px 0 6px 0; padding: 10px; border-radius: 6px; border: 1.5px dashed #389c62; background: rgba(56, 156, 98, 0.08); text-align: left;">
                                    <span style="font-size: 11px; font-weight: 700; color: {preview_label}; text-transform: uppercase; letter-spacing: 0.05em; display: block; margin-bottom: 4px;">Vepisovací pole v Anki:</span>
                                    <div style="padding: 7px 12px; background: {preview_bg}; color: {preview_label}; border: 1px solid {preview_border}; border-radius: 4px; font-family: monospace; font-size: 13px; opacity: 0.9;">
                                        [ Napište odpověď: {type_target_col} ]
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)

                    with tab_prev_back:
                        with st.container(border=True):
                            if card_layout_choice != "Na druhou stranu (pouze rub)":
                                st.markdown(f'<span style="color: {preview_label}; font-size: 11px;">[ Zde se zobrazí líc karty ]</span><hr style="margin: 12px 0; border: 0; border-top: 1px solid {preview_border};">', unsafe_allow_html=True)
                            if not st.session_state.back_cols_ordered:
                                st.caption("Na rubu nejsou vybrány žádné sloupce.")
                            for c in st.session_state.back_cols_ordered:
                                val = preview_row[c] if c in preview_row else ""
                                if pd.isna(val) or str(val).strip() == "":
                                    continue

                                show_label = True
                                label_text = c
                                if c in st.session_state.col_styles:
                                    show_label = st.session_state.col_styles[c].get("show_label", True)
                                    label_text = st.session_state.col_styles[c].get("custom_label", c)

                                val_css = get_value_css(c)
                                val_style_attr = f' style="{val_css}; color: {preview_fg} !important;"' if val_css else f' style="color: {preview_fg} !important;"'
                                label_html = f'<span style="font-size: 11px; font-weight: 600; color: {preview_label}; text-transform: uppercase; border-bottom: 1px solid {preview_border}; display: block; margin-bottom: 4px; padding-bottom: 2px;">{label_text}</span>' if show_label else ''

                                if c in ["[Pladias] Mapa rozšíření", "[Pladias.cz] Mapa rozšíření"]:
                                    if label_html:
                                        st.markdown(label_html, unsafe_allow_html=True)
                                    map_species = ""
                                    if "distribution/" in str(val):
                                        map_species = str(val).split("distribution/")[-1].split("?")[0].strip().replace("%20", " ")
                                    if not map_species and columns:
                                        map_species = str(preview_row.get(columns[0], "")).strip()
                                    map_img_path = get_or_render_pladias_map_image(map_species)
                                    if map_img_path and os.path.isfile(map_img_path):
                                        img_src = format_img_src_for_html(map_img_path)
                                        caption_html = f'<div style="font-size: 10px; color: {preview_label}; margin-top: 3px; text-align: center; opacity: 0.85;">Pladias.cz • Mapa rozšíření ČR</div>' if show_media_attr_val else ''
                                        st.markdown(f'<div style="width: 100%; max-width: 450px; border-radius: 6px; overflow: hidden; border: 1px solid {preview_border}; margin: 8px 0; padding-bottom: 4px;"><img src="{img_src}" style="width: 100%; height: auto; object-fit: contain; display: block;">{caption_html}</div>', unsafe_allow_html=True)
                                    else:
                                        st.markdown(f'<div style="padding: 10px; border-radius: 6px; border: 1px solid {preview_border}; background: rgba(0,0,0,0.04); margin: 6px 0;"><a href="{val}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Zobrazit mapu rozšíření na Pladias.cz ({map_species})</a></div>', unsafe_allow_html=True)
                                elif c in ["[iNaturalist] Mapa nálezů", "[iNaturalist] Mapa pozorování", "[iNat] Mapa pozorování"] or ("inat" in str(c).lower() and "map" in str(c).lower()):
                                    if label_html:
                                        st.markdown(label_html, unsafe_allow_html=True)
                                    map_species = str(preview_row.get(columns[0], "")).strip() if columns else ""
                                    map_img_path = get_or_render_inat_map_image(map_species, str(val))
                                    if map_img_path and os.path.isfile(map_img_path):
                                        img_src = format_img_src_for_html(map_img_path)
                                        caption_html = f'<div style="font-size: 10px; color: {preview_label}; margin-top: 3px; text-align: center; opacity: 0.85;">iNaturalist.org • Mapa pozorování</div>' if show_media_attr_val else ''
                                        st.markdown(f'<div style="width: 100%; max-width: 450px; border-radius: 6px; overflow: hidden; border: 1px solid {preview_border}; margin: 8px 0; padding-bottom: 4px;"><img src="{img_src}" style="width: 100%; height: auto; object-fit: contain; display: block;">{caption_html}</div>', unsafe_allow_html=True)
                                    else:
                                        st.markdown(f'<div style="padding: 10px; border-radius: 6px; border: 1px solid {preview_border}; background: rgba(0,0,0,0.04); margin: 6px 0;"><a href="{val}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Zobrazit mapu pozorování na iNaturalist.org</a></div>', unsafe_allow_html=True)
                                elif is_image_col(c, val):
                                    raw_entries = [u.strip() for u in str(val).split(';') if u.strip()]
                                    if label_html:
                                        st.markdown(label_html, unsafe_allow_html=True)
                                    for entry in raw_entries:
                                        if '|' in entry:
                                            u_parts = entry.split('|', 1)
                                            img_url = u_parts[0].strip()
                                            attr_txt = u_parts[1].strip()
                                        else:
                                            img_url = entry.strip()
                                            attr_txt = ""
                                        img_src = format_img_src_for_html(img_url)
                                        caption_html = f'<div style="font-size: 10px; color: {preview_label}; margin-top: 3px; text-align: center; opacity: 0.85;">{attr_txt}</div>' if (show_media_attr_val and attr_txt) else ''
                                        st.markdown(f'<div style="width: 100%; max-width: 450px; border-radius: 6px; overflow: hidden; border: 1px solid {preview_border}; margin: 8px 0; padding-bottom: 4px;"><img src="{img_src}" style="width: 100%; height: auto; object-fit: contain; display: block;">{caption_html}</div>', unsafe_allow_html=True)
                                elif str(c).startswith("[TTS]"):
                                    st.info(f"Výslovnost (Audio): {str(val).split(';')[0]}")
                                elif c == "[Zvuky] Hlasy ptáků":
                                    entries = [e.strip() for e in str(val).split(';') if e.strip()]
                                    if label_html:
                                        st.markdown(label_html, unsafe_allow_html=True)
                                    for entry in entries:
                                        parts = entry.split('|')
                                        su = parts[0].strip()
                                        stype = parts[1].strip() if len(parts) > 1 else "song"
                                        sattr = parts[2].strip() if len(parts) > 2 else ""
                                        if not su.startswith('http'):
                                            continue
                                        type_label = "Zpěv" if stype == "song" else "Hlas"
                                        if show_media_attr_val and sattr:
                                            st.caption(f"{type_label} • {sattr}")
                                        else:
                                            st.caption(type_label)
                                        st.audio(su)
                                else:
                                    if label_html:
                                        st.markdown(label_html, unsafe_allow_html=True)
                                    val_str = str(val)
                                    if val_str.startswith("http://") or val_str.startswith("https://"):
                                        if "pladias.cz" in val_str:
                                            val_str = f'<a href="{val_str}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Otevřít profil na Pladias.cz</a>'
                                        elif "mykologie.net" in val_str:
                                            val_str = f'<a href="{val_str}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Otevřít profil na Mykologie.net</a>'
                                        elif "dalib.cz" in val_str:
                                            val_str = f'<a href="{val_str}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Otevřít profil na DaLiBor</a>'
                                        elif "diatombase.org" in val_str:
                                            val_str = f'<a href="{val_str}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Otevřít profil na DiatomBase</a>'
                                        elif "algaebase.org" in val_str:
                                            val_str = f'<a href="{val_str}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Otevřít vyhledávání na AlgaeBase</a>'
                                        elif "inaturalist.org" in val_str:
                                            val_str = f'<a href="{val_str}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Otevřít mapu pozorování na iNaturalist.org &rarr;</a>'
                                        elif "mushroomcoloratlas.com" in val_str:
                                            val_str = f'<a href="{val_str}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Otevřít Mushroom Color Atlas (Pigmenty a barviva)</a>'
                                        elif "wikipedia.org" in val_str:
                                            val_str = f'<a href="{val_str}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Otevřít profil na Wikipedii</a>'
                                    elif not re.search(r'<[a-zA-Z0-9/]+[^>]*>', val_str):
                                        val_str = val_str.replace('\n', '<br>')
                                    st.markdown(f'<div{val_style_attr}>{val_str}</div>', unsafe_allow_html=True)
                            if is_type_in and type_target_col:
                                clean_ans = str(preview_row.get(type_target_col, "")).strip()
                                st.markdown(f"""
                                <div style="margin: 14px 0 6px 0; padding: 10px; border-radius: 6px; background: rgba(56, 156, 98, 0.12); border: 1px solid #389c62; text-align: left;">
                                    <span style="font-size: 11px; font-weight: 700; color: #216a40; text-transform: uppercase; letter-spacing: 0.05em; display: block; margin-bottom: 4px;">Kontrolovaná správná odpověď:</span>
                                    <span style="font-family: monospace; font-size: 14px; font-weight: bold; background: rgba(56, 156, 98, 0.18); padding: 3px 8px; border-radius: 4px; display: inline-block;">{clean_ans}</span>
                                </div>
                                """, unsafe_allow_html=True)

                else:
                    st.info("Vyberte sloupce na líci nebo rubu pro zobrazení náhledu kartičky.")

            st.markdown("#### Nastavení a export balíčku Anki")
            col_exp1, col_exp2 = st.columns(2)
            with col_exp1:
                default_deck_name = st.session_state.get("imported_apkg_deck_name", "balíček")
                deck_name_input = st.text_input("Název balíčku (Anki Deck Name)", value=default_deck_name, key="anki_deck_name_input")
            with col_exp2:
                subdeck_col_choice = st.selectbox(
                    "Rozdělit do podbalíčků podle sloupce (volitelně):",
                    ["— Bez rozdělení —"] + columns,
                    index=0,
                    key="anki_subdeck_choice"
                )

            enable_tagging = st.checkbox("Přidat štítky (tags) ke kartičkám podle hodnoty ve sloupci", value=False, key="anki_enable_tagging")
            tag_col = ""
            tag_match_val = ""
            tag_name_input = ""
            if enable_tagging:
                col_t1, col_t2, col_t3 = st.columns(3)
                with col_t1:
                    tag_col = st.selectbox("Sloupec pro přidělení štítku:", options=columns, index=0, key="anki_tag_col")
                with col_t2:
                    tag_match_val = st.text_input("Hodnota ve sloupci pro označení (např. 1, u, ucitel):", value="1", key="anki_tag_val")
                with col_t3:
                    tag_name_input = st.text_input("Název štítku v Anki (tag):", value="ucitele", key="anki_tag_name")

            deck_custom_desc = st.text_area(
                "Vlastní popis balíčku (zobrazí se v Anki pod názvem balíčku):",
                placeholder="Např.: Poznávačka rostlin České republiky: základní pensum druhů pro studenty...\nAutoři: ...",
                help="Text se zobrazí na úvodní obrazovce balíčku v Anki. Můžete sem uvést název předmětu, autory, účel balíčku atd.",
                height=95,
                key="w_deck_custom_desc"
            )

            auto_attach_citations = True
            if has_attribution:
                auto_attach_citations = st.checkbox(
                    "Automaticky připojit oficiální citace a licence použitých zdrojů",
                    value=True,
                    key="w_auto_attach_citations"
                )
                src_names = []
                if has_pladias: src_names.append("Pladias.cz")
                if has_myko: src_names.append("Mykologie.net")
                if has_dalibor: src_names.append("DaLiBor (dalib.cz)")
                if has_diatom: src_names.append("DiatomBase")
                if has_algae: src_names.append("AlgaeBase")
                st.caption(f"*Do popisu balíčku budou automaticky připojeny citace a uvedení zdrojů ({', '.join(src_names)}).*")

            full_desc_parts = []
            if deck_custom_desc and deck_custom_desc.strip():
                full_desc_parts.append(deck_custom_desc.strip())
            if auto_attach_citations and default_attribution_desc:
                full_desc_parts.append(default_attribution_desc)
            deck_desc_input = "\n\n".join(full_desc_parts)

            if deck_desc_input.strip():
                with st.expander("Náhled kompletního popisu balíčku pro Anki", expanded=False):
                    st.markdown(format_deck_description(deck_desc_input), unsafe_allow_html=True)

            with st.expander("ℹ️ Nápověda: Hláška 'Prosím aktualizujte na nejnovější verzi Anki' nebo použití na iPhone", expanded=False):
                st.markdown("""
                **1. Proč se tato hláška v programu Anki objevuje?**
                Generátor vytváří balíčky kompatibilní s moderním standardem Anki (Anki 23 a 24+). Pokud máte na počítači nainstalovanou starší verzi Anki (např. 2.1.x z minulých let), Anki zobrazí výzvu k aktualizaci.
                👉 **Řešení pro PC/Mac:** Stačí si stáhnout a nainstalovat bezplatnou aktualizaci z oficiálního webu [apps.ankiweb.net](https://apps.ankiweb.net). Všechny vaše dosavadní balíčky a postup zůstanou zachovány.

                **2. Jak používat kartičky na iPhone / iPad zdarma?**
                - Oficiální mobilní aplikace **AnkiMobile** pro iOS je placená (cca 700 Kč, jednorázově).
                - Neoficiální aplikace třetích stran v App Store (jako *AnkiPro* nebo *AnkiApp*) jsou placené kopie s předplatným a standardní `.apkg` nepodporují.
                - **Možnost zdarma A:** Použijte **bezplatný AnkiWeb** přímo v Safari na iPhone po bezplatné synchronizaci z PC.
                - **Možnost zdarma B (Doporučeno):** Použijte náš export do **Obsidianu (záložka 2 nahoře)** – aplikace Obsidian je na iPhone i iPad 100% zdarma, funguje plně offline a s bezplatným doplňkem *Spaced Repetition* se učíte úplně stejně jako v Anki!
                """)
            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            st.checkbox(
                "Vynutit nová ID karet v Anki (vytvořit jako nové karty místo aktualizace existujících)",
                value=False,
                key="cb_force_new_anki_cards",
                help="Zaškrtněte, pokud chcete v Anki vytvořit nový samostatný balíček a předejít přeskočení karet kvůli předchozím importům."
            )
            btn_gen_apkg_clicked = st.button("Generovat balíček pro Anki (.apkg)", key="btn_gen_apkg", use_container_width=True, type="primary")

            if btn_gen_apkg_clicked:
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

                    status.text("Připravuji seznam médií ke stažení...")
                    media_tasks = {}
                    media_attributions = {}
                    active_cols = list(dict.fromkeys(st.session_state.front_cols_ordered + st.session_state.back_cols_ordered))

                    for idx, row in df.iterrows():
                        for col in active_cols:
                            val = row[col]
                            if pd.isna(val) or str(val).strip() == "" or str(val).lower() == "nan":
                                continue

                            if str(col).startswith("[TTS]"):
                                parts = str(val).split(';')
                                if len(parts) >= 2:
                                    text_to_speak = parts[0].strip()
                                    lang_code = parts[1].strip()
                                    if text_to_speak and lang_code:
                                        safe_txt = slugify(text_to_speak)[:20]
                                        safe_filename = f"tts_{idx}_{safe_txt}_{lang_code}.mp3"
                                        tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl={lang_code}&client=tw-ob&q={urllib.parse.quote(text_to_speak)}"
                                        media_tasks[safe_filename] = (tts_url, 'audio')

                            elif col == "[Zvuky] Hlasy ptáků":
                                entries = [e.strip() for e in str(val).split(';') if e.strip()]
                                for s_idx, entry in enumerate(entries):
                                    parts = entry.split('|')
                                    sound_url = parts[0].strip()
                                    stype = parts[1].strip() if len(parts) > 1 else "song"
                                    attr_txt = parts[2].strip() if len(parts) > 2 else ""
                                    if not sound_url.startswith('http'):
                                        continue
                                    raw_sp_name = str(row[columns[0]]) if len(columns) > 0 else f"druh_{idx}"
                                    safe_sp = slugify(raw_sp_name)[:20] or f"druh_{idx}"
                                    safe_filename = f"xc_{idx}_{s_idx}_{safe_sp}_{stype}.mp3"
                                    media_tasks[safe_filename] = (sound_url, 'audio')
                                    if attr_txt:
                                        media_attributions[safe_filename] = attr_txt

                            elif col in ["[Pladias] Mapa rozšíření", "[Pladias.cz] Mapa rozšíření"]:
                                species_col = st.session_state.api_config.get("pladias_map_col", columns[0])
                                raw_species = str(row[species_col]).strip() if species_col in row else str(val).strip()
                                clean_species = slugify_species_name(raw_species) if raw_species else f"druh_{idx}"
                                safe_filename = f"{clean_species}_pladias_map_{idx}.jpg"
                                media_tasks[safe_filename] = (raw_species, 'pladias_map')

                            elif col in ["[GBIF] Habitus", "[GBIF] Květ", "[GBIF] List", "[GBIF] Plod", "[GBIF] Herbář"] and is_image_col(col, val):
                                raw_entries = [u.strip() for u in str(val).split(';') if u.strip()]
                                organ_map = {
                                    "[GBIF] Habitus": "habitus",
                                    "[GBIF] Květ": "kvet",
                                    "[GBIF] List": "list",
                                    "[GBIF] Plod": "plod",
                                    "[GBIF] Herbář": "herbar"
                                }
                                organ = organ_map.get(col, "foto")
                                species_col = st.session_state.api_config.get("gbif_photo_col", columns[0])
                                raw_species = str(row[species_col]).strip() if species_col in row else ""
                                clean_species = slugify_species_name(raw_species) if raw_species else f"druh_{idx}"

                                for u_idx, entry in enumerate(raw_entries):
                                    if '|' in entry:
                                        u_parts = entry.split('|', 1)
                                        url = u_parts[0].strip()
                                        attr_txt = u_parts[1].strip()
                                    else:
                                        url = entry.strip()
                                        attr_txt = ""

                                    if url.startswith('http://') or url.startswith('https://'):
                                        ext = ".jpg"
                                        if ".png" in url.lower():
                                            ext = ".png"
                                        elif ".jpeg" in url.lower():
                                            ext = ".jpeg"
                                        safe_filename = f"{clean_species}_{organ}{ext}" if u_idx == 0 else f"{clean_species}_{organ}_{u_idx}{ext}"
                                        media_tasks[safe_filename] = (url, 'image')
                                        if attr_txt:
                                            media_attributions[safe_filename] = attr_txt

                            elif is_image_col(col, val):
                                raw_entries = [u.strip() for u in str(val).split(';') if u.strip()]
                                raw_sp_name = str(row[columns[0]]).strip() if len(columns) > 0 else f"druh_{idx}"
                                clean_sp = slugify_species_name(raw_sp_name) if raw_sp_name else f"druh_{idx}"

                                for img_idx, entry in enumerate(raw_entries):
                                    if '|' in entry:
                                        u_parts = entry.split('|', 1)
                                        url = u_parts[0].strip()
                                        attr_txt = u_parts[1].strip()
                                    else:
                                        url = entry.strip()
                                        attr_txt = ""

                                    loc_src = ""
                                    if not url.startswith('http://') and not url.startswith('https://'):
                                        loc_src = resolve_local_media_path(url)
                                        if not loc_src:
                                            continue
                                    ext = ".jpg"
                                    if ".png" in url.lower():
                                        ext = ".png"
                                    elif ".jpeg" in url.lower():
                                        ext = ".jpeg"
                                    elif ".webp" in url.lower():
                                        ext = ".webp"
                                    safe_col = slugify(col)[:12]
                                    url_hash = hashlib.sha256(url.encode('utf-8')).hexdigest()[:6]
                                    safe_filename = f"{clean_sp}_{safe_col}_{idx}_{img_idx}_{url_hash}{ext}"
                                    if loc_src:
                                        media_tasks[safe_filename] = (loc_src, 'local_image')
                                    else:
                                        media_tasks[safe_filename] = (url, 'image')
                                    if attr_txt:
                                        media_attributions[safe_filename] = attr_txt

                    downloaded_media = []
                    total_tasks = len(media_tasks)
                    if total_tasks > 0:
                        status.text(f"Stahuji a optimalizuji média (0/{total_tasks})...")
                        progress_bar.progress(0.0)

                        def _download_task(item):
                            fname, (url, mtype) = item
                            local_path = os.path.join(media_dir, fname)
                            if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
                                return fname, local_path, True
                            try:
                                if mtype == 'pladias_map':
                                    if render_pladias_distribution_map(url, local_path):
                                        return fname, local_path, True
                                    return fname, local_path, False
                                elif mtype == 'local_image':
                                    if os.path.isfile(url):
                                        with open(url, "rb") as rf:
                                            fcontent = rf.read()
                                        if not save_optimized_image(fcontent, local_path, max_dim=800, quality=80):
                                            shutil.copy2(url, local_path)
                                        return fname, local_path, True
                                    return fname, local_path, False
                                r_resp = requests.get(
                                    url,
                                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                                    timeout=(2.5, 5.0)
                                )
                                if r_resp.status_code == 404 and 'cevs/images/taxa/' in url:
                                    alt_url = url.replace('/taxa/large/', '/taxa/clopla/large/') if '/taxa/clopla/' not in url else url.replace('/taxa/clopla/large/', '/taxa/large/')
                                    try:
                                        alt_resp = requests.get(
                                            alt_url,
                                            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                                            timeout=(2.5, 5.0)
                                        )
                                        if alt_resp.status_code == 200:
                                            r_resp = alt_resp
                                    except Exception:
                                        pass
                                if r_resp.status_code == 200 and len(r_resp.content) > 0:
                                    if mtype == 'image':
                                        if save_optimized_image(r_resp.content, local_path, max_dim=800, quality=80):
                                            if check_image_quality(local_path):
                                                return fname, local_path, True
                                            else:
                                                if os.path.exists(local_path):
                                                    os.remove(local_path)
                                    else:
                                        with open(local_path, 'wb') as f:
                                            f.write(r_resp.content)
                                        if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
                                            return fname, local_path, True
                            except Exception:
                                pass
                            return fname, local_path, False

                        completed_count = 0
                        with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
                            futures = {executor.submit(_download_task, item): item for item in media_tasks.items()}
                            try:
                                for future in concurrent.futures.as_completed(futures, timeout=75):
                                    completed_count += 1
                                    progress_bar.progress(completed_count / total_tasks)
                                    status.text(f"Stahuji a optimalizuji média: {completed_count}/{total_tasks} hotovo...")
                                    try:
                                        fname, local_path, success = future.result(timeout=1.0)
                                        if success:
                                            downloaded_media.append(local_path)
                                    except Exception:
                                        pass
                            except concurrent.futures.TimeoutError:
                                status.text(f"Časový limit pro pomalá média vypršel ({completed_count}/{total_tasks}). Pokračuji v sestavování balíčku...")

                    status.text("Sestavuji kartičky...")
                    progress_bar.progress(1.0)

                    processed_notes = []
                    card_layout_mode = st.session_state.get("card_layout_radio", "Pod sebe (líc + rub)")
                    is_only_back = (card_layout_mode == "Na druhou stranu (pouze rub)")
                    show_media_attr = st.session_state.get("show_media_attribution", True)
                    total = len(df)

                    def compile_side_html(selected_cols, row_idx, row_data):
                        html_parts = []
                        for col in selected_cols:
                            val = row_data[col]
                            if pd.isna(val) or str(val).strip() == "" or str(val).lower() == "nan":
                                continue

                            show_label = True
                            label_text = col
                            if 'col_styles' in st.session_state and col in st.session_state.col_styles:
                                show_label = st.session_state.col_styles[col].get("show_label", True)
                                label_text = st.session_state.col_styles[col].get("custom_label", col)

                            val_css = get_value_css(col)
                            val_style_attr = f' style="{val_css}"' if val_css else ''
                            label_html = f'<span class="field-label">{label_text}</span>' if show_label else ''

                            if str(col).startswith("[TTS]"):
                                parts = str(val).split(';')
                                if len(parts) >= 2:
                                    text_to_speak = parts[0].strip()
                                    lang_code = parts[1].strip()
                                    if text_to_speak and lang_code:
                                        safe_txt = slugify(text_to_speak)[:20]
                                        safe_filename = f"tts_{row_idx}_{safe_txt}_{lang_code}.mp3"
                                        local_path = os.path.join(media_dir, safe_filename)
                                        if os.path.exists(local_path):
                                            html_parts.append(f"[sound:{safe_filename}]")
                                continue

                            if col == "[Zvuky] Hlasy ptáků":
                                entries = [e.strip() for e in str(val).split(';') if e.strip()]
                                for s_idx, entry in enumerate(entries):
                                    parts = entry.split('|')
                                    sound_url = parts[0].strip()
                                    stype = parts[1].strip() if len(parts) > 1 else "song"
                                    if not sound_url.startswith('http'):
                                        continue
                                    raw_sp_name = str(row_data[row_data.index[0]]) if len(row_data) > 0 else f"druh_{row_idx}"
                                    safe_sp = slugify(raw_sp_name)[:20] or f"druh_{row_idx}"
                                    safe_filename = f"xc_{row_idx}_{s_idx}_{safe_sp}_{stype}.mp3"
                                    local_path = os.path.join(media_dir, safe_filename)
                                    if os.path.exists(local_path):
                                        type_label = "Zpěv" if stype == "song" else "Hlas"
                                        audio_caption_html = ""
                                        if show_media_attr and safe_filename in media_attributions and media_attributions[safe_filename]:
                                            audio_caption_html = f'<div class="audio-caption">{html.escape(media_attributions[safe_filename])}</div>'
                                        html_parts.append(
                                            f'<div class="card-field field-{slugify(col)}">'
                                            f'{label_html}'
                                            f'<div class="field-value">'
                                            f'<span style="font-weight: 600; font-size: 13px; display: block; margin-bottom: 2px;">{type_label}</span>'
                                            f'<audio controls controlslist="nodownload" preload="none" src="{safe_filename}"></audio>'
                                            f'{audio_caption_html}'
                                            f'</div>'
                                            f'</div>'
                                        )
                                continue

                            if col in ["[Pladias] Mapa rozšíření", "[Pladias.cz] Mapa rozšíření"]:
                                species_col = st.session_state.api_config.get("pladias_map_col", columns[0])
                                raw_species = str(row_data[species_col]).strip() if species_col in row_data else str(val).strip()
                                clean_species = slugify_species_name(raw_species) if raw_species else f"druh_{row_idx}"
                                safe_filename = f"{clean_species}_pladias_map_{row_idx}.jpg"
                                local_path = os.path.join(media_dir, safe_filename)
                                if os.path.exists(local_path):
                                    img_tag = f'<div class="photo-container"><img src="{safe_filename}"></div>'
                                    html_parts.append(
                                        f'<div class="card-field field-{slugify(col)}">'
                                        f'{label_html}'
                                        f'<div class="photo-list">{img_tag}</div>'
                                        f'</div>'
                                    )
                                continue

                            is_gbif_photo = col in ["[GBIF] Habitus", "[GBIF] Květ", "[GBIF] List", "[GBIF] Plod", "[GBIF] Herbář"]
                            if is_gbif_photo and is_image_col(col, val):
                                raw_entries = [u.strip() for u in str(val).split(';') if u.strip()]
                                organ_map = {
                                    "[GBIF] Habitus": "habitus",
                                    "[GBIF] Květ": "kvet",
                                    "[GBIF] List": "list",
                                    "[GBIF] Plod": "plod",
                                    "[GBIF] Herbář": "herbar"
                                }
                                organ = organ_map.get(col, "foto")
                                species_col = st.session_state.api_config.get("gbif_photo_col", columns[0])
                                raw_species = str(row_data[species_col]).strip() if species_col in row_data else ""
                                clean_species = slugify_species_name(raw_species) if raw_species else f"druh_{row_idx}"

                                for u_idx, entry in enumerate(raw_entries):
                                    if '|' in entry:
                                        url = entry.split('|', 1)[0].strip()
                                    else:
                                        url = entry.strip()
                                    ext = ".jpg"
                                    if ".png" in url.lower():
                                        ext = ".png"
                                    elif ".jpeg" in url.lower():
                                        ext = ".jpeg"
                                    safe_filename = f"{clean_species}_{organ}{ext}" if u_idx == 0 else f"{clean_species}_{organ}_{u_idx}{ext}"
                                    local_path = os.path.join(media_dir, safe_filename)
                                    if os.path.exists(local_path):
                                        caption_html = ""
                                        if show_media_attr and safe_filename in media_attributions and media_attributions[safe_filename]:
                                            caption_html = f'<div class="photo-caption">{html.escape(media_attributions[safe_filename])}</div>'
                                        img_tag = f'<div class="photo-container"><img src="{safe_filename}">{caption_html}</div>'
                                        html_parts.append(
                                            f'<div class="card-field field-{slugify(col)}">'
                                            f'{label_html}'
                                            f'<div class="photo-list">{img_tag}</div>'
                                            f'</div>'
                                        )
                                        break
                                continue

                            if is_image_col(col, val):
                                raw_entries = [u.strip() for u in str(val).split(';') if u.strip()]
                                local_filenames = []
                                raw_sp_name = str(row_data[columns[0]]).strip() if len(columns) > 0 else f"druh_{row_idx}"
                                clean_sp = slugify_species_name(raw_sp_name) if raw_sp_name else f"druh_{row_idx}"

                                for img_idx, entry in enumerate(raw_entries):
                                    if '|' in entry:
                                        url = entry.split('|', 1)[0].strip()
                                    else:
                                        url = entry.strip()
                                    if not url.startswith('http://') and not url.startswith('https://'):
                                        if not resolve_local_media_path(url):
                                            continue
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
                                    if os.path.exists(local_path):
                                        local_filenames.append(safe_filename)

                                if local_filenames:
                                    img_containers = []
                                    for fn in local_filenames:
                                        caption_html = ""
                                        if show_media_attr and fn in media_attributions and media_attributions[fn]:
                                            caption_html = f'<div class="photo-caption">{html.escape(media_attributions[fn])}</div>'
                                        img_containers.append(f'<div class="photo-container"><img src="{fn}">{caption_html}</div>')
                                    img_tags = "".join(img_containers)
                                    html_parts.append(
                                        f'<div class="card-field field-{slugify(col)}">'
                                        f'{label_html}'
                                        f'<div class="photo-list">{img_tags}</div>'
                                        f'</div>'
                                    )

                            elif col.startswith(("[Pladias]", "[Pladias.cz]")) or col.startswith("[Mykologie.net] Odkaz") or col.startswith("[DaLiBor] Odkaz") or col.startswith("[DiatomBase] Odkaz") or col.startswith("[AlgaeBase] Odkaz") or (col.startswith("[Wikipedie]") and str(val).startswith("http")):
                                url = str(val).strip()
                                if "pladias.cz" in url:
                                    link_label = "Otevřít profil na Pladias.cz"
                                elif "mykologie.net" in url:
                                    link_label = "Otevřít profil na Mykologie.net"
                                elif "dalib.cz" in url:
                                    link_label = "Otevřít profil na DaLiBor"
                                elif "diatombase.org" in url:
                                    link_label = "Otevřít profil na DiatomBase"
                                elif "algaebase.org" in url:
                                    link_label = "Otevřít vyhledávání na AlgaeBase"
                                else:
                                    link_label = "Otevřít profil na Wikipedii"
                                html_parts.append(
                                    f'<div class="card-field field-{slugify(col)}">'
                                    f'{label_html}'
                                    f'<div class="field-value"><a href="{url}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline; font-size: 0.95em;">{link_label}</a></div>'
                                    f'</div>'
                                )

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

                    is_type_in = st.session_state.get("is_type_in", False)
                    type_target_col = st.session_state.get("type_target_col")

                    for idx, row in df.iterrows():
                        front_html = compile_side_html(st.session_state.front_cols_ordered, idx, row)
                        back_html = compile_side_html(st.session_state.back_cols_ordered, idx, row)

                        clean_type_target = ""
                        if is_type_in and type_target_col:
                            raw_target = str(row.get(type_target_col, "")).strip()
                            clean_type_target = clean_html(raw_target).strip()
                            clean_type_target = re.sub(r'<[^>]*>', '', clean_type_target).strip()

                        subdeck_val = ""
                        if subdeck_col_choice != "— Bez rozdělení —":
                            raw_val = row.get(subdeck_col_choice)
                            if pd.notna(raw_val) and str(raw_val).strip() != "":
                                subdeck_val = str(raw_val).strip()

                        card_tags = []
                        if enable_tagging and tag_col and tag_name_input.strip():
                            cell_raw = str(row.get(tag_col, "")).strip()
                            match_targets = [m.strip().lower() for m in tag_match_val.split(",") if m.strip()]
                            if (match_targets and cell_raw.lower() in match_targets) or (not match_targets and cell_raw != ""):
                                clean_tag = re.sub(r'\s+', '_', tag_name_input.strip())
                                if clean_tag:
                                    card_tags.append(clean_tag)

                        anki_guid_val = str(row.get('_anki_guid', '')).strip() if '_anki_guid' in row and pd.notna(row.get('_anki_guid')) else None
                        if not anki_guid_val:
                            anki_guid_val = None

                        processed_notes.append({
                            'front': front_html,
                            'back': back_html,
                            'type_target': clean_type_target,
                            'guid_src': str(row[columns[0]]) if columns else str(idx),
                            'anki_guid': anki_guid_val,
                            'subdeck_val': subdeck_val,
                            'tags': card_tags
                        })

                    status.text("Zapisuji balíček Anki (.apkg)...")

                    schema_str = ",".join(st.session_state.front_cols_ordered) + "|" + ",".join(st.session_state.back_cols_ordered) + "|" + deck_name_input + "|" + card_layout_mode + "|" + str(is_type_in) + "|" + str(type_target_col)
                    model_hash = hashlib.sha256(schema_str.encode('utf-8')).hexdigest()[:8]

                    existing_mid = None
                    if '_anki_mid' in df.columns:
                        valid_mids = [m for m in df['_anki_mid'] if pd.notna(m) and str(m).strip().isdigit()]
                        if valid_mids:
                            try:
                                existing_mid = int(valid_mids[0])
                            except Exception:
                                existing_mid = None

                    force_new_guids = st.session_state.get("cb_force_new_anki_cards", False)
                    if existing_mid and not force_new_guids:
                        model_id = existing_mid
                    else:
                        model_id = get_stable_id(f"Universal_Model_{deck_name_input}")
                    deck_id = get_stable_id(deck_name_input)

                    if is_type_in and type_target_col:
                        anki_fields = [
                            {'name': 'Front'},
                            {'name': 'Back'},
                            {'name': 'TypeAnswer'}
                        ]
                        anki_qfmt = """
    <div class="card">
      {{Front}}
      {{type:TypeAnswer}}
    </div>
    """
                        if is_only_back:
                            anki_afmt = """
    <div class="card">
      {{type:TypeAnswer}}
      <hr class="card-divider">
      {{Back}}
    </div>
    """
                        else:
                            anki_afmt = """
    <div class="card">
      {{Front}}
      <hr class="card-divider">
      {{type:TypeAnswer}}
      {{Back}}
    </div>
    """
                    else:
                        anki_fields = [
                            {'name': 'Front'},
                            {'name': 'Back'}
                        ]
                        anki_qfmt = ANKI_QFMT
                        anki_afmt = """
    <div class="card">
      {{Back}}
    </div>
    """ if is_only_back else ANKI_AFMT

                    anki_model = genanki.Model(
                        model_id,
                        f'Universal Model for {deck_name_input}',
                        fields=anki_fields,
                        templates=[
                            {
                                'name': 'Karta',
                                'qfmt': anki_qfmt,
                                'afmt': anki_afmt,
                            },
                        ],
                        css=get_anki_css(card_theme)
                    )

                    formatted_deck_desc = format_deck_description(deck_desc_input)
                    decks = {}
                    parent_deck_id = get_stable_id(deck_name_input)
                    parent_deck = genanki.Deck(parent_deck_id, deck_name_input, description=formatted_deck_desc)
                    decks[deck_name_input] = parent_deck

                    for note_data in processed_notes:
                        content_hash = hashlib.sha256((note_data['front'] + "|" + note_data['back']).encode('utf-8')).hexdigest()[:8]
                        note_fields = [note_data['front'], note_data['back']]
                        if is_type_in and type_target_col:
                            note_fields.append(note_data.get('type_target', ''))

                        explicit_guid = note_data.get('anki_guid')
                        force_new_guids = st.session_state.get("cb_force_new_anki_cards", False)
                        if explicit_guid and not force_new_guids:
                            final_guid = explicit_guid
                        else:
                            final_guid = genanki.guid_for(note_data['guid_src'] + "|" + deck_name_input + ("|" + content_hash if force_new_guids else ""))

                        note = genanki.Note(
                            model=anki_model,
                            fields=note_fields,
                            tags=note_data.get('tags', []),
                            guid=final_guid
                        )

                        target_deck_name = deck_name_input
                        if subdeck_col_choice != "— Bez rozdělení —" and note_data.get('subdeck_val'):
                            target_deck_name = f"{deck_name_input}::{note_data['subdeck_val']}"

                        if target_deck_name not in decks:
                            sub_deck_id = get_stable_id(target_deck_name)
                            decks[target_deck_name] = genanki.Deck(sub_deck_id, target_deck_name, description=formatted_deck_desc)

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
                        gc.collect()

                    st.success("Balíček Anki byl úspěšně vygenerován.")
                    st.rerun()

        with tab_obsidian:
            st.markdown("#### Export kartiček (.zip) – Webový přehrávač & Obsidian (Zdarma pro iPhone, iPad i PC)")
            st.info("Vygenerovaný **.zip** balíček můžete otevřít **přímo v telefonu nebo PC** pomocí samostatného přehrávače (**Karty.html / index.html** uvnitř balíčku), nebo jej otevřít v bezplatné aplikaci **Obsidian** s doplňkem *Spaced Repetition*. Obě varianty jsou 100% zdarma, fungují offline a pamatují si postup učení!")

            col_obs_left, col_obs_right = st.columns([1.1, 0.9], gap="large")

            with col_obs_left:
                default_obs_vault = f"Atlas_{slugify(st.session_state.get('imported_apkg_deck_name', 'karticky'))}"
                obs_vault_name = st.text_input("Název složky / balíčku v Obsidianu:", value=default_obs_vault, key="obs_vault_name_input")
                obs_card_sep_mode = st.radio(
                    "Režim kartiček pro Spaced Repetition:",
                    ["Jednosměrné (?) - líc na rub (Doporučeno)", "Obousměrné (??) - líc na rub i rub na líc"],
                    index=0,
                    key="obs_card_sep_radio",
                    help="Jednosměrné používá '?' a zkouší vás z líce na rub (např. z fotky na název a popis). Obousměrné používá '??' a vytvoří z každého druhu dvě kartičky."
                )

                if "obs_front_cols_ordered" not in st.session_state:
                    st.session_state.obs_front_cols_ordered = list(st.session_state.front_cols_ordered) if st.session_state.front_cols_ordered else ([columns[0]] if columns else [])
                if "obs_back_cols_ordered" not in st.session_state:
                    st.session_state.obs_back_cols_ordered = list(st.session_state.back_cols_ordered) if st.session_state.back_cols_ordered else [c for c in columns if c not in st.session_state.obs_front_cols_ordered]
                if "obs_col_styles" not in st.session_state:
                    st.session_state.obs_col_styles = dict(st.session_state.col_styles) if st.session_state.col_styles else {}

                col_obs_front, col_obs_back = st.columns(2)
                with col_obs_front:
                    st.markdown("##### 1. Otázka / Líc kartičky")
                    obs_front_cols = st.multiselect(
                        "Sloupce zobrazené před otočením (např. foto):",
                        options=columns,
                        default=[c for c in st.session_state.obs_front_cols_ordered if c in columns],
                        key="obs_front_cols_multiselect"
                    )
                    sync_ordered_cols(obs_front_cols, "obs_front_cols_ordered")

                    with st.expander("Změnit pořadí sloupců na líci (▲ / ▼)", expanded=False):
                        for i, col in enumerate(st.session_state.obs_front_cols_ordered):
                            c_name, c_up, c_down = st.columns([6, 1, 1])
                            with c_name:
                                st.write(f"**{col}**")
                            with c_up:
                                if st.button("▲", key=f"obs_up_front_{col}_{i}"):
                                    if i > 0:
                                        st.session_state.obs_front_cols_ordered[i], st.session_state.obs_front_cols_ordered[i-1] = st.session_state.obs_front_cols_ordered[i-1], st.session_state.obs_front_cols_ordered[i]
                                        st.rerun()
                            with c_down:
                                if st.button("▼", key=f"obs_down_front_{col}_{i}"):
                                    if i < len(st.session_state.obs_front_cols_ordered) - 1:
                                        st.session_state.obs_front_cols_ordered[i], st.session_state.obs_front_cols_ordered[i+1] = st.session_state.obs_front_cols_ordered[i+1], st.session_state.obs_front_cols_ordered[i]
                                        st.rerun()

                with col_obs_back:
                    st.markdown("##### 2. Odpověď / Rub kartičky")
                    default_obs_back = [c for c in st.session_state.obs_back_cols_ordered if c in columns and c not in obs_front_cols]
                    obs_back_cols = st.multiselect(
                        "Sloupce zobrazené po otočení (jméno, popis):",
                        options=columns,
                        default=default_obs_back,
                        key="obs_back_cols_multiselect"
                    )
                    sync_ordered_cols(obs_back_cols, "obs_back_cols_ordered")

                    with st.expander("Změnit pořadí sloupců na rubu (▲ / ▼)", expanded=False):
                        for i, col in enumerate(st.session_state.obs_back_cols_ordered):
                            c_name, c_up, c_down = st.columns([6, 1, 1])
                            with c_name:
                                st.write(f"**{col}**")
                            with c_up:
                                if st.button("▲", key=f"obs_up_back_{col}_{i}"):
                                    if i > 0:
                                        st.session_state.obs_back_cols_ordered[i], st.session_state.obs_back_cols_ordered[i-1] = st.session_state.obs_back_cols_ordered[i-1], st.session_state.obs_back_cols_ordered[i]
                                        st.rerun()
                            with c_down:
                                if st.button("▼", key=f"obs_down_back_{col}_{i}"):
                                    if i < len(st.session_state.obs_back_cols_ordered) - 1:
                                        st.session_state.obs_back_cols_ordered[i], st.session_state.obs_back_cols_ordered[i+1] = st.session_state.obs_back_cols_ordered[i+1], st.session_state.obs_back_cols_ordered[i]
                                        st.rerun()

                obs_selected_cols = list(dict.fromkeys(st.session_state.obs_front_cols_ordered + st.session_state.obs_back_cols_ordered))
                obs_text_cols = [
                    c for c in obs_selected_cols
                    if not (check_col_is_image(c, df) or is_image_col(c) or any(img_kw in c.lower() for img_kw in ["foto", "fotka", "obrázek", "obrazek", "habitus", "květ", "kvet", "list", "plod", "herbář", "herbar", "detail", "mikrofoto"]))
                ]
                if obs_text_cols:
                    with st.expander("Pokročilé nastavení zobrazení sloupců (formátování textu v Obsidianu)", expanded=False):
                        for col in obs_text_cols:
                            if col not in st.session_state.obs_col_styles:
                                existing_s = st.session_state.col_styles.get(col, {})
                                st.session_state.obs_col_styles[col] = {
                                    "bold": existing_s.get("bold", False),
                                    "italic": existing_s.get("italic", False),
                                    "size": existing_s.get("size", "Výchozí"),
                                    "custom_label": existing_s.get("custom_label", col),
                                    "show_label": existing_s.get("show_label", True)
                                }
                            style = st.session_state.obs_col_styles[col]
                            st.markdown(f"**Sloupec: {col}**")
                            sc1, sc2, sc3 = st.columns([1.2, 1.4, 1.4])
                            with sc1:
                                style["bold"] = st.checkbox("Tučné", value=style["bold"], key=f"obs_style_bold_{col}")
                                style["italic"] = st.checkbox("Kurzíva", value=style["italic"], key=f"obs_style_italic_{col}")
                            with sc2:
                                sizes = ["Výchozí", "Malé (12px)", "Střední (16px)", "Velké (20px)", "Obrovské (24px)"]
                                current_idx = sizes.index(style["size"]) if style["size"] in sizes else 0
                                style["size"] = st.selectbox(
                                    "Velikost písma:",
                                    sizes,
                                    index=current_idx,
                                    key=f"obs_style_size_{col}"
                                )
                            with sc3:
                                style["show_label"] = st.checkbox("Zobrazit název pole", value=style["show_label"], key=f"obs_style_show_lbl_{col}")
                                style["custom_label"] = st.text_input("Vlastní název pole:", value=style["custom_label"], key=f"obs_style_cust_lbl_{col}")

                c_opt1, c_opt2 = st.columns(2)
                with c_opt1:
                    obs_include_index = st.checkbox("Vytvořit hlavní rejstřík (00_Atlas_a_Prehled.md)", value=True, key="obs_include_index_cb")
                with c_opt2:
                    obs_include_guide = st.checkbox("Připojit návod pro iPhone (00_NAVOD_JAK_POUZIVAT.md)", value=True, key="obs_include_guide_cb")

                with st.expander("📱 Dvě možnosti použití zdarma (Obsidian & Karty.html)", expanded=False):
                    st.markdown("""
                    **1. Samostatný přehrávač (Karty.html):**
                    - Přibalen přímo uvnitř vygenerovaného `.zip` souboru jako `index.html`.
                    - Stačí balíček stáhnout a otevřít v jakémkoliv prohlížeči na mobilu i PC.
                    - Žádná instalace ani registrace, 100% offline, chytré opakování (SM-2), zvětšování fotografií klepnutím, podpora více balíčků najednou.

                    **2. Aplikace Obsidian (iOS / Android / PC):**
                    - Bezplatná aplikace z App Store / Google Play.
                    - Složku z balíčku otevřete v Obsidianu jako nový trezor (*Vault*).
                    - V komunitních doplňcích zapnete *Spaced Repetition*.
                    """)
                    st.caption("💡 **Tip ke stažení:** Samostatný soubor přehrávače si můžete stáhnout níže v rozbalovací záložce **🛠️ Doplňkové nástroje** (nebo využít soubor `index.html` zabalený přímo v exportovaném .zip archivu).")
                    st.caption("ℹ️ **Webový přehrávač (Karty.html)** slouží pro rychlé, bezpečné a pohodlné offline procvičování přímo ve webovém prohlížeči (na PC, mobilu i tabletu).")

            with col_obs_right:
                st.markdown("#### Vizuální náhled kartičky")
                if st.session_state.obs_front_cols_ordered or st.session_state.obs_back_cols_ordered:
                    c_prev_r1, c_prev_r2 = st.columns([2, 1])
                    with c_prev_r1:
                        obs_row_idx = st.number_input(
                            f"Náhled pro řádek (1 z {len(df)}):",
                            min_value=1,
                            max_value=max(1, len(df)),
                            value=1,
                            step=1,
                            key="obs_card_preview_row_selector"
                        ) - 1
                    with c_prev_r2:
                        st.caption("Živý náhled v reálném čase")

                    preview_row = df.iloc[obs_row_idx]
                    show_media_attr_val = st.session_state.get("show_media_attribution", True)

                    preview_bg = "#ffffff" if is_light_ui else "#2f2f31"
                    preview_fg = "#111d14" if is_light_ui else "#f4faf6"
                    preview_border = "#cfe0d5" if is_light_ui else "#23362b"
                    preview_label = "#2d5438" if is_light_ui else "#8da897"

                    def get_obs_value_css(c):
                        s = st.session_state.obs_col_styles.get(c, {})
                        css_parts = []
                        if s.get("bold"): css_parts.append("font-weight: bold")
                        if s.get("italic"): css_parts.append("font-style: italic")
                        size = s.get("size", "Výchozí")
                        if size == "Malé (12px)": css_parts.append("font-size: 12px")
                        elif size == "Střední (16px)": css_parts.append("font-size: 16px")
                        elif size == "Velké (20px)": css_parts.append("font-size: 20px")
                        elif size == "Obrovské (24px)": css_parts.append("font-size: 24px")
                        return "; ".join(css_parts)

                    tab_prev_front_obs, tab_prev_back_obs = st.tabs(["Líc", "Rub"])

                    with tab_prev_front_obs:
                        with st.container(border=True):
                            if not st.session_state.obs_front_cols_ordered:
                                st.caption("Na líci nejsou vybrány žádné sloupce.")
                            for c in st.session_state.obs_front_cols_ordered:
                                val = preview_row[c] if c in preview_row else ""
                                if pd.isna(val) or str(val).strip() == "":
                                    continue

                                show_label = True
                                label_text = c
                                if c in st.session_state.obs_col_styles:
                                    show_label = st.session_state.obs_col_styles[c].get("show_label", True)
                                    label_text = st.session_state.obs_col_styles[c].get("custom_label", c) or c

                                val_css = get_obs_value_css(c)
                                val_style_attr = f' style="{val_css}; color: {preview_fg} !important;"' if val_css else f' style="color: {preview_fg} !important;"'
                                label_html = f'<span style="font-size: 11px; font-weight: 600; color: {preview_label}; text-transform: uppercase; border-bottom: 1px solid {preview_border}; display: block; margin-bottom: 4px; padding-bottom: 2px;">{label_text}</span>' if show_label else ''

                                if check_col_is_image(c, df) or is_image_col(c, val):
                                    raw_entries = [u.strip() for u in str(val).split(';') if u.strip()]
                                    if label_html:
                                        st.markdown(label_html, unsafe_allow_html=True)
                                    for entry in raw_entries:
                                        u_parts = entry.split('|', 1)
                                        img_url = u_parts[0].strip()
                                        attr_txt = u_parts[1].strip() if len(u_parts) > 1 else ""
                                        img_src = format_img_src_for_html(img_url)
                                        caption_html = f'<div style="font-size: 10px; color: {preview_label}; margin-top: 3px; text-align: center; opacity: 0.85;">{attr_txt}</div>' if (show_media_attr_val and attr_txt) else ''
                                        st.markdown(f'<div style="width: 100%; max-width: 450px; border-radius: 6px; overflow: hidden; border: 1px solid {preview_border}; margin: 8px 0; padding-bottom: 4px;"><img src="{img_src}" style="width: 100%; height: auto; object-fit: contain; display: block;">{caption_html}</div>', unsafe_allow_html=True)
                                elif c in ["[Pladias] Mapa rozšíření", "[Pladias.cz] Mapa rozšíření"]:
                                    if label_html:
                                        st.markdown(label_html, unsafe_allow_html=True)
                                    map_species = ""
                                    if "distribution/" in str(val):
                                        map_species = str(val).split("distribution/")[-1].split("?")[0].strip().replace("%20", " ")
                                    if not map_species and columns:
                                        map_species = str(preview_row.get(columns[0], "")).strip()
                                    map_img_path = get_or_render_pladias_map_image(map_species)
                                    if map_img_path and os.path.isfile(map_img_path):
                                        img_src = format_img_src_for_html(map_img_path)
                                        st.markdown(f'<div style="width: 100%; max-width: 450px; border-radius: 6px; overflow: hidden; border: 1px solid {preview_border}; margin: 8px 0; padding-bottom: 4px;"><img src="{img_src}" style="width: 100%; height: auto; object-fit: contain; display: block;"><div style="font-size: 10px; color: {preview_label}; margin-top: 3px; text-align: center; opacity: 0.85;">Pladias.cz • Mapa rozšíření ČR</div></div>', unsafe_allow_html=True)
                                    else:
                                        st.markdown(f'<div style="padding: 10px; border-radius: 6px; border: 1px solid {preview_border}; background: rgba(0,0,0,0.04); margin: 6px 0;"><a href="{val}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Zobrazit mapu rozšíření na Pladias.cz ({map_species})</a></div>', unsafe_allow_html=True)
                                elif c in ["[iNaturalist] Mapa nálezů", "[iNaturalist] Mapa pozorování", "[iNat] Mapa pozorování"] or ("inat" in str(c).lower() and "map" in str(c).lower()):
                                    if label_html:
                                        st.markdown(label_html, unsafe_allow_html=True)
                                    map_species = str(preview_row.get(columns[0], "")).strip() if columns else ""
                                    map_img_path = get_or_render_inat_map_image(map_species, str(val))
                                    if map_img_path and os.path.isfile(map_img_path):
                                        img_src = format_img_src_for_html(map_img_path)
                                        st.markdown(f'<div style="width: 100%; max-width: 450px; border-radius: 6px; overflow: hidden; border: 1px solid {preview_border}; margin: 8px 0; padding-bottom: 4px;"><img src="{img_src}" style="width: 100%; height: auto; object-fit: contain; display: block;"><div style="font-size: 10px; color: {preview_label}; margin-top: 3px; text-align: center; opacity: 0.85;">iNaturalist.org • Mapa pozorování</div></div>', unsafe_allow_html=True)
                                    else:
                                        st.markdown(f'<div style="padding: 10px; border-radius: 6px; border: 1px solid {preview_border}; background: rgba(0,0,0,0.04); margin: 6px 0;"><a href="{val}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Zobrazit mapu pozorování na iNaturalist.org</a></div>', unsafe_allow_html=True)
                                else:
                                    if label_html:
                                        st.markdown(label_html, unsafe_allow_html=True)
                                    val_str = str(val)
                                    if val_str.startswith("http://") or val_str.startswith("https://"):
                                        st.markdown(f'<div{val_style_attr}><a href="{val_str}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">{val_str}</a></div>', unsafe_allow_html=True)
                                    else:
                                        st.markdown(f'<div{val_style_attr}>{val_str}</div>', unsafe_allow_html=True)

                    with tab_prev_back_obs:
                        with st.container(border=True):
                            if not st.session_state.obs_back_cols_ordered:
                                st.caption("Na rubu nejsou vybrány žádné sloupce.")
                            for c in st.session_state.obs_back_cols_ordered:
                                val = preview_row[c] if c in preview_row else ""
                                if pd.isna(val) or str(val).strip() == "":
                                    continue

                                show_label = True
                                label_text = c
                                if c in st.session_state.obs_col_styles:
                                    show_label = st.session_state.obs_col_styles[c].get("show_label", True)
                                    label_text = st.session_state.obs_col_styles[c].get("custom_label", c) or c

                                val_css = get_obs_value_css(c)
                                val_style_attr = f' style="{val_css}; color: {preview_fg} !important;"' if val_css else f' style="color: {preview_fg} !important;"'
                                label_html = f'<span style="font-size: 11px; font-weight: 600; color: {preview_label}; text-transform: uppercase; border-bottom: 1px solid {preview_border}; display: block; margin-bottom: 4px; padding-bottom: 2px;">{label_text}</span>' if show_label else ''

                                if check_col_is_image(c, df) or is_image_col(c, val):
                                    raw_entries = [u.strip() for u in str(val).split(';') if u.strip()]
                                    if label_html:
                                        st.markdown(label_html, unsafe_allow_html=True)
                                    for entry in raw_entries:
                                        u_parts = entry.split('|', 1)
                                        img_url = u_parts[0].strip()
                                        attr_txt = u_parts[1].strip() if len(u_parts) > 1 else ""
                                        img_src = format_img_src_for_html(img_url)
                                        caption_html = f'<div style="font-size: 10px; color: {preview_label}; margin-top: 3px; text-align: center; opacity: 0.85;">{attr_txt}</div>' if (show_media_attr_val and attr_txt) else ''
                                        st.markdown(f'<div style="width: 100%; max-width: 450px; border-radius: 6px; overflow: hidden; border: 1px solid {preview_border}; margin: 8px 0; padding-bottom: 4px;"><img src="{img_src}" style="width: 100%; height: auto; object-fit: contain; display: block;">{caption_html}</div>', unsafe_allow_html=True)
                                elif c in ["[Pladias] Mapa rozšíření", "[Pladias.cz] Mapa rozšíření"]:
                                    if label_html:
                                        st.markdown(label_html, unsafe_allow_html=True)
                                    map_species = ""
                                    if "distribution/" in str(val):
                                        map_species = str(val).split("distribution/")[-1].split("?")[0].strip().replace("%20", " ")
                                    if not map_species and columns:
                                        map_species = str(preview_row.get(columns[0], "")).strip()
                                    map_img_path = get_or_render_pladias_map_image(map_species)
                                    if map_img_path and os.path.isfile(map_img_path):
                                        img_src = format_img_src_for_html(map_img_path)
                                        st.markdown(f'<div style="width: 100%; max-width: 450px; border-radius: 6px; overflow: hidden; border: 1px solid {preview_border}; margin: 8px 0; padding-bottom: 4px;"><img src="{img_src}" style="width: 100%; height: auto; object-fit: contain; display: block;"><div style="font-size: 10px; color: {preview_label}; margin-top: 3px; text-align: center; opacity: 0.85;">Pladias.cz • Mapa rozšíření ČR</div></div>', unsafe_allow_html=True)
                                    else:
                                        st.markdown(f'<div style="padding: 10px; border-radius: 6px; border: 1px solid {preview_border}; background: rgba(0,0,0,0.04); margin: 6px 0;"><a href="{val}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Zobrazit mapu rozšíření na Pladias.cz ({map_species})</a></div>', unsafe_allow_html=True)
                                elif c in ["[iNaturalist] Mapa nálezů", "[iNaturalist] Mapa pozorování", "[iNat] Mapa pozorování"] or ("inat" in str(c).lower() and "map" in str(c).lower()):
                                    if label_html:
                                        st.markdown(label_html, unsafe_allow_html=True)
                                    map_species = str(preview_row.get(columns[0], "")).strip() if columns else ""
                                    map_img_path = get_or_render_inat_map_image(map_species, str(val))
                                    if map_img_path and os.path.isfile(map_img_path):
                                        img_src = format_img_src_for_html(map_img_path)
                                        st.markdown(f'<div style="width: 100%; max-width: 450px; border-radius: 6px; overflow: hidden; border: 1px solid {preview_border}; margin: 8px 0; padding-bottom: 4px;"><img src="{img_src}" style="width: 100%; height: auto; object-fit: contain; display: block;"><div style="font-size: 10px; color: {preview_label}; margin-top: 3px; text-align: center; opacity: 0.85;">iNaturalist.org • Mapa pozorování</div></div>', unsafe_allow_html=True)
                                    else:
                                        st.markdown(f'<div style="padding: 10px; border-radius: 6px; border: 1px solid {preview_border}; background: rgba(0,0,0,0.04); margin: 6px 0;"><a href="{val}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">Zobrazit mapu pozorování na iNaturalist.org</a></div>', unsafe_allow_html=True)
                                else:
                                    if label_html:
                                        st.markdown(label_html, unsafe_allow_html=True)
                                    val_str = str(val)
                                    if val_str.startswith("http://") or val_str.startswith("https://"):
                                        st.markdown(f'<div{val_style_attr}><a href="{val_str}" target="_blank" style="color: #48a973; font-weight: 600; text-decoration: underline;">{val_str}</a></div>', unsafe_allow_html=True)
                                    else:
                                        st.markdown(f'<div{val_style_attr}>{val_str}</div>', unsafe_allow_html=True)

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            btn_gen_obs_clicked = st.button("Generovat balíček pro Obsidian (.zip)", key="btn_gen_obsidian", use_container_width=True, type="primary")

            if btn_gen_obs_clicked:
                if not obs_front_cols and not obs_back_cols:
                    st.error("Musíte vybrat alespoň jeden sloupec pro otázku (líc) nebo odpověď (rub).")
                else:
                    temp_dir = tempfile.mkdtemp()
                    media_dir = os.path.join(temp_dir, "media")
                    os.makedirs(media_dir, exist_ok=True)

                    progress_bar = st.progress(0.0)
                    status = st.empty()

                    status.text("Připravuji seznam médií pro Obsidian...")
                    media_tasks = {}
                    effective_front = st.session_state.obs_front_cols_ordered
                    effective_back = st.session_state.obs_back_cols_ordered
                    active_cols = list(dict.fromkeys(effective_front + effective_back))

                    for idx, row in df.iterrows():
                        for col in active_cols:
                            val = row[col]
                            if pd.isna(val) or str(val).strip() == "" or str(val).lower() == "nan":
                                continue
                            if check_col_is_image(col, df) or is_image_col(col, val):
                                raw_entries = [u.strip() for u in str(val).split(';') if u.strip()]
                                for pos, entry in enumerate(raw_entries):
                                    raw_u = entry.split('|')[0].strip()
                                    if not raw_u: continue
                                    sp_clean = slugify(str(row.iloc[0])) if len(row) > 0 else f"item_{idx}"
                                    ext = ".jpg"
                                    if raw_u.lower().endswith(".png"): ext = ".png"
                                    elif raw_u.lower().endswith(".webp"): ext = ".webp"
                                    media_tasks[raw_u] = os.path.join(media_dir, f"{sp_clean}_{slugify(col)}_{pos}{ext}")

                    total_m = len(media_tasks)
                    if total_m > 0:
                        status.text(f"Stahuji multimediální soubory (0/{total_m})...")
                        workers = min(12, os.cpu_count() * 2 if os.cpu_count() else 4)
                        done_m = 0
                        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
                            future_to_url = {executor.submit(download_media_file, u, p): u for u, p in media_tasks.items()}
                            for future in concurrent.futures.as_completed(future_to_url):
                                done_m += 1
                                progress_bar.progress(done_m / float(total_m) * 0.7)
                                status.text(f"Stahuji multimediální soubory ({done_m}/{total_m})...")
                                try:
                                    future.result()
                                except Exception:
                                    pass

                    progress_bar.progress(0.85)
                    status.text("Vytvářím Markdown karty a balíček .zip pro Obsidian...")

                    out_zip_filename = f"{slugify(obs_vault_name) or 'Studijni_Karticky'}.zip"
                    out_zip_path = os.path.join(temp_dir, out_zip_filename)

                    sel_card_sep = "??" if "Obousměrné" in st.session_state.get("obs_card_sep_radio", "") else "?"
                    generate_obsidian_vault_zip(
                        df=df,
                        output_zip_path=out_zip_path,
                        vault_name=obs_vault_name or "Studijni_Karticky",
                        front_cols=effective_front,
                        back_cols=effective_back,
                        col_styles=st.session_state.obs_col_styles,
                        media_tasks=media_tasks,
                        include_guide=obs_include_guide,
                        include_index=obs_include_index,
                        card_separator=sel_card_sep
                    )

                    with open(out_zip_path, "rb") as f_zip:
                        zip_bytes = f_zip.read()

                    st.session_state.generated_obsidian_data = zip_bytes
                    st.session_state.generated_obsidian_filename = out_zip_filename

                    progress_bar.progress(1.0)
                    status.text("Balíček pro Obsidian byl úspěšně vygenerován.")
                    shutil.rmtree(temp_dir, ignore_errors=True)
                    st.success("Balíček pro Obsidian (.zip) byl úspěšně vytvořen a je připraven ke stažení!")
                    st.rerun()

        with tab_pdf:
            col_pdf_left, col_pdf_right = st.columns([1.1, 0.9], gap="large")

            with col_pdf_left:
                with st.container(border=True):
                    st.markdown("##### Obsah a sloupce brožury")
                st.caption("Vyberte sloupce z tabulky a upravte jejich pořadí v brožuře.")
                if "pdf_cols_ordered" not in st.session_state or not st.session_state.pdf_cols_ordered:
                    _init_pdf_cols = list(dict.fromkeys(st.session_state.front_cols_ordered + st.session_state.back_cols_ordered))
                    st.session_state.pdf_cols_ordered = _init_pdf_cols if _init_pdf_cols else list(columns)

                pdf_cols_selected = st.multiselect(
                    "Sloupce do PDF brožury:",
                    options=columns,
                    default=[c for c in st.session_state.pdf_cols_ordered if c in columns],
                    key="pdf_cols_multiselect"
                )
                sync_ordered_cols(pdf_cols_selected, "pdf_cols_ordered")

                with st.expander("↕️ Změnit pořadí sloupců v brožuře", expanded=False):
                    st.caption("Sloupce se v brožuře zobrazí v tomto pořadí. Pořadí můžete měnit tlačítky na začátek/konec nebo o jednu pozici:")
                    for i_p, c_p in enumerate(st.session_state.pdf_cols_ordered):
                        c_pn, c_pt, c_pu, c_pd, c_pb = st.columns([5, 1, 1, 1, 1])
                        with c_pn:
                            st.write(f"**{i_p + 1}.** {c_p}")
                        with c_pt:
                            if st.button("⇪", key=f"top_pdf_col_{c_p}_{i_p}", help="Přesunout na začátek"):
                                if i_p > 0:
                                    val_c = st.session_state.pdf_cols_ordered.pop(i_p)
                                    st.session_state.pdf_cols_ordered.insert(0, val_c)
                                    st.rerun()
                        with c_pu:
                            if st.button("▲", key=f"up_pdf_col_{c_p}_{i_p}", help="Posunout o 1 výše"):
                                if i_p > 0:
                                    st.session_state.pdf_cols_ordered[i_p], st.session_state.pdf_cols_ordered[i_p-1] = st.session_state.pdf_cols_ordered[i_p-1], st.session_state.pdf_cols_ordered[i_p]
                                    st.rerun()
                        with c_pd:
                            if st.button("▼", key=f"down_pdf_col_{c_p}_{i_p}", help="Posunout o 1 níže"):
                                if i_p < len(st.session_state.pdf_cols_ordered) - 1:
                                    st.session_state.pdf_cols_ordered[i_p], st.session_state.pdf_cols_ordered[i_p+1] = st.session_state.pdf_cols_ordered[i_p+1], st.session_state.pdf_cols_ordered[i_p]
                                    st.rerun()
                        with c_pb:
                            if st.button("⇩", key=f"bot_pdf_col_{c_p}_{i_p}", help="Přesunout na konec"):
                                if i_p < len(st.session_state.pdf_cols_ordered) - 1:
                                    val_c = st.session_state.pdf_cols_ordered.pop(i_p)
                                    st.session_state.pdf_cols_ordered.append(val_c)
                                    st.rerun()

                if "pdf_col_styles" not in st.session_state:
                    st.session_state.pdf_col_styles = {}

                with st.expander("⚙️ Formátování sloupců v PDF (tabulka vs. samostatný text, tučně, kurzíva)", expanded=False):
                    st.caption("Nastavte, zda se má sloupec vložit do přehledové tabulky vlastností nebo jako samostatný odstavec textu, a upravte styl písma či popisek.")
                    display_opts = ["Automaticky", "Do tabulky vlastností", "Jako samostatný text"]
                    display_map = {"Automaticky": "auto", "Do tabulky vlastností": "table", "Jako samostatný text": "text"}
                    display_rev = {"auto": "Automaticky", "table": "Do tabulky vlastností", "text": "Jako samostatný text"}

                    style_opts = ["Normální (výchozí)", "Tučně (bold)", "Kurzívou (italic)", "Tučná kurzíva"]
                    style_map = {"Normální (výchozí)": "normal", "Tučně (bold)": "bold", "Kurzívou (italic)": "italic", "Tučná kurzíva": "bold_italic"}
                    style_rev = {"normal": "Normální (výchozí)", "bold": "Tučně (bold)", "italic": "Kurzívou (italic)", "bold_italic": "Tučná kurzíva"}

                    for col in st.session_state.pdf_cols_ordered:
                        if col not in st.session_state.pdf_col_styles:
                            st.session_state.pdf_col_styles[col] = {
                                "display": "auto",
                                "style": "normal",
                                "custom_label": col
                            }
                        cfg = st.session_state.pdf_col_styles[col]
                        st.markdown(f"**{col}**")
                        fc1, fc2, fc3 = st.columns([1.3, 1.2, 1.5])
                        with fc1:
                            cur_disp = display_rev.get(cfg.get("display", "auto"), "Automaticky")
                            new_disp = st.selectbox(
                                "Zobrazení:",
                                display_opts,
                                index=display_opts.index(cur_disp) if cur_disp in display_opts else 0,
                                key=f"pdf_disp_{col}"
                            )
                            cfg["display"] = display_map.get(new_disp, "auto")
                        with fc2:
                            cur_style = style_rev.get(cfg.get("style", "normal"), "Normální (výchozí)")
                            new_style = st.selectbox(
                                "Styl textu:",
                                style_opts,
                                index=style_opts.index(cur_style) if cur_style in style_opts else 0,
                                key=f"pdf_style_{col}"
                            )
                            cfg["style"] = style_map.get(new_style, "normal")
                        with fc3:
                            new_lbl = st.text_input(
                                "Vlastní popisek:",
                                value=cfg.get("custom_label", col),
                                key=f"pdf_lbl_{col}"
                            )
                            cfg["custom_label"] = new_lbl

                st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                st.markdown("##### Záhlaví a texty")
                pdf_title_input = st.text_input(
                    "Název brožury / atlasu:",
                    value=deck_name_input if 'deck_name_input' in locals() and deck_name_input != "balíček" else "Studijní atlas a brožura",
                    key="w_pdf_title"
                )
                pdf_custom_desc = st.text_area(
                    "Podtitul / doplňující text v záhlaví brožury:",
                    value=deck_custom_desc if 'deck_custom_desc' in locals() else "",
                    placeholder="Např.: Studijní materiál a přehled druhů pro studenty botaniky • Přírodovědecká fakulta\nAutoři: ...",
                    height=68,
                    key="w_pdf_custom_desc"
                )

            with col_pdf_right:
                with st.container(border=True):
                    st.markdown("##### Vzhled a rozvržení tisku")
                st.caption("Nastavení formátu stránek, vazby a velikosti médií.")
                pdf_layout_choice = st.radio(
                    "Formát rozvržení stránek:",
                    [
                        "Kompaktní brožurka (více druhů za sebou)",
                        "1 druh na stránku (Atlasový list / Kartotéka)",
                        "Dvojstrana pro taxon (1 strana obrázky, protilehlá strana popis)"
                    ],
                    index=0,
                    key="w_pdf_layout_radio",
                    help="Kompaktní: šetří papír. 1 druh na stránku: ucelený atlasový list. Dvojstrana pro taxon: na jedné stránce velká fotogalerie, na protilehlé stránce kompletní popis, vlastnosti a QR kódy."
                )

                c_fmt1, c_fmt2 = st.columns(2)
                with c_fmt1:
                    pdf_pagesize_choice = st.selectbox(
                        "Formát stránky:",
                        ["A4 (Standardní)", "A5 (Kompaktní sešit)"],
                        index=0,
                        key="w_pdf_pagesize"
                    )
                    pdf_font_scale_choice = st.selectbox(
                        "Velikost textu:",
                        ["Standardní (100 %)", "Menší / Kompaktní (90 %)", "Větší / Čitelný (115 %)"],
                        index=0,
                        key="w_pdf_font_scale"
                    )
                with c_fmt2:
                    pdf_imposition_choice = st.selectbox(
                        "Typ tisku a vazba:",
                        [
                            "Standardní (postupné stránky pro čtení)",
                            "Sešitová vazba (Brožura / Booklet – tiskový arch pro přeložení napůl)",
                            "Knižní vazba po složkách (6 listů / 24 stran na složku)",
                            "Knižní vazba po složkách (8 listů / 32 stran na složku)"
                        ],
                        index=0,
                        key="w_pdf_imposition",
                        help="Standardní: běžné stránky za sebou. Sešitová vazba: vytvoří tiskové archy (2 strany na list), které po oboustranném tisku stačí přeložit napůl a sešít na hřbetu. Knižní vazba: rozdělí tisk do knihařských složek po 6 nebo 8 listech pro vazbu knih."
                    )
                    pdf_img_size_choice = st.selectbox(
                        "Velikost fotografií:",
                        ["Standardní (vyvážená)", "Velká (dominantní fotky)", "Maximální (na celou plochu)", "Kompaktní (menší fotky)"],
                        index=0,
                        key="w_pdf_img_size",
                        help="Umožňuje zvětšit fotografie až na celou plochu stránky nebo je zmenšit ve prospěch textu."
                    )
                    pdf_max_imgs_choice = st.selectbox(
                        "Počet fotografií a map na druh:",
                        [
                            "Až 6 (doporučeno: 4 fotky + 2 mapy)",
                            "Až 4 (klasická mřížka 2×2 s předností map)",
                            "Až 2 (dominantní velká zobrazení)",
                            "Pouze 1 (hlavní foto / mapa)"
                        ],
                        index=0,
                        key="w_pdf_max_imgs",
                        help="Zajišťuje, že se mapy rozšíření ČR a pozorování iNaturalist nevynechají na úkor fotografií. Při volbě 'Až 6' se zobrazí až 4 fotografie i obě mapy současně."
                    )

                st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
                st.markdown("##### Doplňkové prvky")
                col_popt1, col_popt2 = st.columns(2)
                with col_popt1:
                    pdf_include_toc = st.checkbox("Vložit na začátek obsah / rejstřík položek", value=True, key="w_pdf_inc_toc")
                    pdf_include_qr_codes = st.checkbox("Generovat QR kódy pro webové odkazy a audio", value=True, key="w_pdf_inc_qr", help="Pokud je volba zapnuta, u vybraných odkazů a zvukových nahrávek se vytvoří interaktivní QR kódy. Pokud je vypnuta, odkazy se vypíší jako běžný text a QR kódy se nevytvářejí.")
                with col_popt2:
                    pdf_include_citations = st.checkbox("Automaticky připojit závěrečnou bibliografii", value=True, key="w_pdf_inc_cit")
                    pdf_include_attributions = st.checkbox("Zobrazovat autory a licence (CC) pod fotkami", value=True, key="w_pdf_inc_attr")

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            col_p_btn1, col_p_btn2 = st.columns([1, 1], gap="medium")
            with col_p_btn1:
                btn_preview_pdf_clicked = st.button("👁️ Rychlý náhled 1. položky (PDF)", key="btn_preview_pdf", use_container_width=True)
            with col_p_btn2:
                btn_generate_pdf_clicked = st.button("📖 Generovat celou PDF brožuru (.pdf)", key="btn_generate_pdf", use_container_width=True, type="primary")

            if st.session_state.get('pdf_preview_data') is not None:
                with st.expander("👁️ Interaktivní náhled PDF (1. položka)", expanded=True):
                    col_prev_dl, col_prev_cls = st.columns([3, 1])
                    with col_prev_dl:
                        st.download_button(
                            label="⬇️ Stáhnout náhled v PDF",
                            data=st.session_state.pdf_preview_data,
                            file_name=st.session_state.get('pdf_preview_filename', 'nahled_brozury.pdf'),
                            mime="application/pdf",
                            key="dl_btn_pdf_preview"
                        )
                    with col_prev_cls:
                        if st.button("❌ Zavřít náhled", key="btn_close_pdf_preview"):
                            st.session_state.pdf_preview_data = None
                            st.rerun()
                    b64_pdf = base64.b64encode(st.session_state.pdf_preview_data).decode('utf-8')
                    st.markdown(
                        f'<iframe src="data:application/pdf;base64,{b64_pdf}#toolbar=1&navpanes=0" width="100%" height="700px" style="border: 1px solid #cbd5e1; border-radius: 8px;"></iframe>',
                        unsafe_allow_html=True
                    )

            if btn_generate_pdf_clicked or btn_preview_pdf_clicked:
                is_preview = bool(btn_preview_pdf_clicked)
                target_df = df.head(1).copy() if is_preview else df

                st.session_state.api_errors = []
                active_cols_pdf = st.session_state.get('pdf_cols_ordered', list(dict.fromkeys(st.session_state.front_cols_ordered + st.session_state.back_cols_ordered)))
                if not active_cols_pdf:
                    st.error("Musíte vybrat alespoň jeden sloupec v Kroku 3 (Mapování stran).")
                else:
                    temp_dir = tempfile.mkdtemp()
                    media_dir = os.path.join(temp_dir, "media")
                    os.makedirs(media_dir, exist_ok=True)

                    progress_bar = st.progress(0.0)
                    status = st.empty()

                    status.text("Připravuji seznam fotografií ke stažení do PDF..." if not is_preview else "Připravuji média pro náhled...")
                    media_tasks = {}
                    media_attributions = {}

                    for idx, row in target_df.iterrows():
                        for col in active_cols_pdf:
                            val = row[col]
                            if pd.isna(val) or str(val).strip() == "" or str(val).lower() == "nan":
                                continue

                            if col in ["[Pladias] Mapa rozšíření", "[Pladias.cz] Mapa rozšíření"]:
                                species_col = st.session_state.api_config.get("pladias_map_col", columns[0])
                                raw_species = str(row[species_col]).strip() if species_col in row else str(val).strip()
                                clean_species = slugify_species_name(raw_species) if raw_species else f"druh_{idx}"
                                safe_filename = f"{clean_species}_pladias_map_{idx}.jpg"
                                media_tasks[safe_filename] = (raw_species, 'pladias_map')

                            elif col in ["[iNaturalist] Mapa nálezů", "[iNaturalist] Mapa pozorování", "[iNat] Mapa pozorování"] or ("inat" in str(col).lower() and "map" in str(col).lower()):
                                species_col = st.session_state.api_config.get("inat_col", columns[0])
                                raw_species = str(row[species_col]).strip() if species_col in row else ""
                                clean_species = slugify_species_name(raw_species) if raw_species else f"druh_{idx}"
                                safe_filename = f"{clean_species}_inat_map_{idx}.jpg"
                                media_tasks[safe_filename] = (str(val).strip(), 'inat_map', raw_species)

                            elif col in ["[GBIF] Habitus", "[GBIF] Květ", "[GBIF] List", "[GBIF] Plod", "[GBIF] Herbář"] and is_image_col(col, val):
                                raw_entries = [u.strip() for u in str(val).split(';') if u.strip()]
                                organ_map = {"[GBIF] Habitus": "habitus", "[GBIF] Květ": "kvet", "[GBIF] List": "list", "[GBIF] Plod": "plod", "[GBIF] Herbář": "herbar"}
                                organ = organ_map.get(col, "foto")
                                species_col = st.session_state.api_config.get("gbif_photo_col", columns[0])
                                raw_species = str(row[species_col]).strip() if species_col in row else ""
                                clean_species = slugify_species_name(raw_species) if raw_species else f"druh_{idx}"
                                for u_idx, entry in enumerate(raw_entries):
                                    if '|' in entry:
                                        u_parts = entry.split('|', 1)
                                        url = u_parts[0].strip()
                                        attr_txt = u_parts[1].strip()
                                    else:
                                        url = entry.strip()
                                        attr_txt = ""
                                    if url.startswith('http://') or url.startswith('https://'):
                                        ext = ".jpg"
                                        if ".png" in url.lower(): ext = ".png"
                                        elif ".jpeg" in url.lower(): ext = ".jpeg"
                                        safe_filename = f"{clean_species}_{organ}{ext}" if u_idx == 0 else f"{clean_species}_{organ}_{u_idx}{ext}"
                                        media_tasks[safe_filename] = (url, 'image')
                                        if attr_txt:
                                            media_attributions[safe_filename] = attr_txt

                            elif is_image_col(col, val):
                                raw_entries = [u.strip() for u in str(val).split(';') if u.strip()]
                                raw_sp_name = str(row[columns[0]]).strip() if len(columns) > 0 else f"druh_{idx}"
                                clean_sp = slugify_species_name(raw_sp_name) if raw_sp_name else f"druh_{idx}"
                                for img_idx, entry in enumerate(raw_entries):
                                    if '|' in entry:
                                        u_parts = entry.split('|', 1)
                                        url = u_parts[0].strip()
                                        attr_txt = u_parts[1].strip()
                                    else:
                                        url = entry.strip()
                                        attr_txt = ""
                                    if os.path.isfile(url):
                                        ext = os.path.splitext(url)[1].lower() or ".jpg"
                                        safe_col = slugify(col)[:12]
                                        url_hash = hashlib.sha256(url.encode('utf-8')).hexdigest()[:6]
                                        safe_filename = f"{clean_sp}_{safe_col}_{idx}_{img_idx}_{url_hash}{ext}"
                                        media_tasks[safe_filename] = (url, 'local_image')
                                        if attr_txt:
                                            media_attributions[safe_filename] = attr_txt
                                    elif url.startswith('http://') or url.startswith('https://'):
                                        ext = ".jpg"
                                        if ".png" in url.lower(): ext = ".png"
                                        elif ".jpeg" in url.lower(): ext = ".jpeg"
                                        elif ".webp" in url.lower(): ext = ".webp"
                                        safe_col = slugify(col)[:12]
                                        url_hash = hashlib.sha256(url.encode('utf-8')).hexdigest()[:6]
                                        safe_filename = f"{clean_sp}_{safe_col}_{idx}_{img_idx}_{url_hash}{ext}"
                                        media_tasks[safe_filename] = (url, 'image')
                                        if attr_txt:
                                            media_attributions[safe_filename] = attr_txt

                    total_tasks = len(media_tasks)
                    if total_tasks > 0:
                        status.text(f"Stahuji a optimalizuji obrázky pro PDF (0/{total_tasks})...")
                        progress_bar.progress(0.0)

                        def _download_pdf_img(item):
                            fname, task_data = item
                            url = task_data[0]
                            mtype = task_data[1]
                            local_path = os.path.join(media_dir, fname)
                            if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
                                return fname, local_path, True
                            try:
                                if mtype == 'pladias_map':
                                    if render_pladias_distribution_map(url, local_path):
                                        return fname, local_path, True
                                    return fname, local_path, False
                                elif mtype == 'inat_map':
                                    extra_sp = task_data[2] if len(task_data) > 2 else ""
                                    if render_inat_observation_map(url, local_path, species_name=extra_sp):
                                        return fname, local_path, True
                                    return fname, local_path, False
                                elif mtype == 'local_image':
                                    if os.path.isfile(url):
                                        with open(url, "rb") as rf:
                                            fcontent = rf.read()
                                        if save_optimized_image(fcontent, local_path, max_dim=800, quality=80):
                                            return fname, local_path, True
                                    return fname, local_path, False
                                r_resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}, timeout=(2.5, 5.0))
                                if r_resp.status_code == 200 and len(r_resp.content) > 0:
                                    if save_optimized_image(r_resp.content, local_path, max_dim=800, quality=80):
                                        return fname, local_path, True
                            except Exception:
                                pass
                            return fname, local_path, False

                        completed_count = 0
                        with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
                            futures = {executor.submit(_download_pdf_img, item): item for item in media_tasks.items()}
                            try:
                                for future in concurrent.futures.as_completed(futures, timeout=75):
                                    completed_count += 1
                                    progress_bar.progress(completed_count / total_tasks)
                                    status.text(f"Stahuji a optimalizuji obrázky: {completed_count}/{total_tasks} hotovo...")
                            except concurrent.futures.TimeoutError:
                                pass

                    status.text("Sázím a generuji PDF..." if is_preview else "Sázím a generuji PDF brožuru...")
                    progress_bar.progress(1.0)

                    if "Dvojstrana" in pdf_layout_choice:
                        pdf_layout_mode_param = "split_images_text"
                    elif "1 druh" in pdf_layout_choice:
                        pdf_layout_mode_param = "page_per_species"
                    else:
                        pdf_layout_mode_param = "compact"
                    page_fmt_param = "A5" if "A5" in pdf_pagesize_choice else "A4"

                    scale_map = {"Standardní (100 %)": 1.0, "Menší / Kompaktní (90 %)": 0.9, "Větší / Čitelný (115 %)": 1.15}
                    font_scale_val = scale_map.get(pdf_font_scale_choice, 1.0)

                    pdf_filename = f"{slugify(pdf_title_input)}.pdf"
                    pdf_path = os.path.join(temp_dir, pdf_filename)

                    try:
                        generate_pdf_booklet(
                            df=target_df,
                            output_pdf_path=pdf_path,
                            title=pdf_title_input,
                            subtitle=pdf_custom_desc,
                            active_cols=active_cols_pdf,
                            layout_mode=pdf_layout_mode_param,
                            page_format=page_fmt_param,
                            imposition_mode=pdf_imposition_choice,
                            font_scale=font_scale_val,
                            include_toc=(False if is_preview else pdf_include_toc),
                            media_dir=media_dir,
                            media_attributions=media_attributions,
                            media_tasks=media_tasks,
                            include_citations=(False if is_preview else pdf_include_citations),
                            include_media_attribution=pdf_include_attributions,
                            col_styles=st.session_state.get('pdf_col_styles', {}),
                            include_qr_codes=pdf_include_qr_codes,
                            image_size_mode=pdf_img_size_choice,
                            max_images_mode=pdf_max_imgs_choice
                        )

                        with open(pdf_path, "rb") as f:
                            pdf_bytes = f.read()

                        if is_preview:
                            st.session_state.pdf_preview_data = pdf_bytes
                            st.session_state.pdf_preview_filename = f"nahled_{slugify(pdf_title_input)}.pdf"
                            st.success("Rychlý náhled 1. položky v PDF byl úspěšně vygenerován.")
                        else:
                            st.session_state.generated_pdf_data = pdf_bytes
                            st.session_state.generated_pdf_filename = pdf_filename
                            st.success("Studijní brožura v PDF byla úspěšně vygenerována.")
                    except Exception as e:
                        st.error(f"Při generování PDF došlo k chybě: {e}")

                    shutil.rmtree(temp_dir, ignore_errors=True)
                    gc.collect()
                    st.rerun()

        with tab_docx:
            col_docx_left, col_docx_right = st.columns([1.1, 0.9], gap="large")

            with col_docx_left:
                with st.container(border=True):
                    st.markdown("##### Obsah a sloupce dokumentu")
                st.caption("Vyberte sloupce z tabulky pro export do formátu Word (.docx).")
                if "docx_cols_ordered" not in st.session_state or not st.session_state.docx_cols_ordered:
                    _init_docx_cols = list(dict.fromkeys(st.session_state.front_cols_ordered + st.session_state.back_cols_ordered))
                    st.session_state.docx_cols_ordered = _init_docx_cols if _init_docx_cols else list(columns)

                docx_cols_selected = st.multiselect(
                    "Sloupce do Word dokumentu:",
                    options=columns,
                    default=[c for c in st.session_state.docx_cols_ordered if c in columns],
                    key="docx_cols_multiselect"
                )
                sync_ordered_cols(docx_cols_selected, "docx_cols_ordered")

                with st.expander("Změnit pořadí sloupců ve Wordu (▲ / ▼)", expanded=False):
                    for i_d, c_d in enumerate(st.session_state.docx_cols_ordered):
                        c_dn, c_du, c_dd = st.columns([6, 1, 1])
                        with c_dn:
                            st.write(f"**{c_d}**")
                        with c_du:
                            if st.button("▲", key=f"up_docx_col_{c_d}_{i_d}"):
                                if i_d > 0:
                                    st.session_state.docx_cols_ordered[i_d], st.session_state.docx_cols_ordered[i_d-1] = st.session_state.docx_cols_ordered[i_d-1], st.session_state.docx_cols_ordered[i_d]
                                    st.rerun()
                        with c_dd:
                            if st.button("▼", key=f"down_docx_col_{c_d}_{i_d}"):
                                if i_d < len(st.session_state.docx_cols_ordered) - 1:
                                    st.session_state.docx_cols_ordered[i_d], st.session_state.docx_cols_ordered[i_d+1] = st.session_state.docx_cols_ordered[i_d+1], st.session_state.docx_cols_ordered[i_d]
                                    st.rerun()

                st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                st.markdown("##### Záhlaví a texty")
                docx_title_input = st.text_input(
                    "Název dokumentu:",
                    value=deck_name_input if 'deck_name_input' in locals() else "Studijní atlas a brožura",
                    key="w_docx_title"
                )
                docx_custom_desc = st.text_area(
                    "Podtitul / doplňující text v záhlaví dokumentu:",
                    value=deck_custom_desc if 'deck_custom_desc' in locals() else "",
                    placeholder="Např.: Výukový materiál a atlas druhů pro studenty biologie • Přírodovědecká fakulta",
                    height=68,
                    key="w_docx_custom_desc"
                )

            with col_docx_right:
                with st.container(border=True):
                    st.markdown("##### Rozvržení a export")
                st.caption("Vytvoří plně editovatelný dokument Word se zachováním stylů.")
                docx_layout_choice = st.selectbox(
                    "Rozvržení položek:",
                    ["1 druh na stránku (Konec stránky za každým druhem / Kartotéka)", "Kompaktní (Plynulý text za sebou)"],
                    index=0,
                    key="w_docx_layout"
                )

                st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                st.markdown("##### Doplňkové prvky")
                docx_include_toc = st.checkbox("Vložit na začátek obsah / rejstřík položek", value=True, key="w_docx_inc_toc")
                docx_include_citations = st.checkbox("Automaticky připojit závěrečnou bibliografii", value=True, key="w_docx_inc_cit")
                docx_include_attributions = st.checkbox("Zobrazovat autory a licence (CC) pod fotkami", value=True, key="w_docx_inc_attr")

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            btn_generate_docx_clicked = st.button("Generovat dokument ve Wordu (.docx)", key="btn_generate_docx", use_container_width=True, type="primary")

            if btn_generate_docx_clicked:
                st.session_state.api_errors = []
                active_cols_docx = st.session_state.get('docx_cols_ordered', list(dict.fromkeys(st.session_state.front_cols_ordered + st.session_state.back_cols_ordered)))
                if not active_cols_docx:
                    st.error("Musíte vybrat alespoň jeden sloupec v Kroku 3 (Mapování stran).")
                else:
                    temp_dir = tempfile.mkdtemp()
                    media_dir = os.path.join(temp_dir, "media")
                    os.makedirs(media_dir, exist_ok=True)

                    progress_bar = st.progress(0.0)
                    status = st.empty()
                    status.text("Připravuji podklady a stahuji fotografie pro dokument Word...")

                    media_tasks = {}
                    media_attributions = {}

                    for idx, row in df.iterrows():
                        for col in active_cols_docx:
                            val = row[col]
                            if pd.isna(val) or str(val).strip() == "" or str(val).lower() == "nan":
                                continue
                            if col in ["[Pladias] Mapa rozšíření", "[Pladias.cz] Mapa rozšíření"]:
                                species_col = st.session_state.api_config.get("pladias_map_col", columns[0])
                                raw_species = str(row[species_col]).strip() if species_col in row else str(val).strip()
                                clean_species = slugify_species_name(raw_species) if raw_species else f"druh_{idx}"
                                safe_filename = f"{clean_species}_pladias_map_{idx}.jpg"
                                media_tasks[safe_filename] = (raw_species, 'pladias_map')
                            elif is_image_col(col, val):
                                raw_entries = [u.strip() for u in str(val).split(';') if u.strip()]
                                clean_species = slugify_species_name(str(row.iloc[0])) if len(row) > 0 else f"druh_{idx}"
                                for img_idx, entry in enumerate(raw_entries):
                                    if '|' in entry:
                                        u_parts = entry.split('|', 1)
                                        url = u_parts[0].strip()
                                        attr_txt = u_parts[1].strip()
                                    else:
                                        url = entry.strip()
                                        attr_txt = ""
                                    if url.startswith('http://') or url.startswith('https://'):
                                        ext = ".jpg"
                                        if ".png" in url.lower(): ext = ".png"
                                        elif ".jpeg" in url.lower(): ext = ".jpeg"
                                        elif ".webp" in url.lower(): ext = ".webp"
                                        safe_col = slugify(col)[:12]
                                        url_hash = hashlib.sha256(url.encode('utf-8')).hexdigest()[:6]
                                        safe_filename = f"{clean_species}_{safe_col}_{idx}_{img_idx}_{url_hash}{ext}"
                                        media_tasks[safe_filename] = (url, 'image')
                                        if attr_txt:
                                            media_attributions[safe_filename] = attr_txt

                    total_tasks = len(media_tasks)
                    completed_tasks = 0
                    for safe_fn, (source_val, task_type) in media_tasks.items():
                        target_file = os.path.join(media_dir, safe_fn)
                        try:
                            if task_type == 'pladias_map':
                                render_pladias_distribution_map(source_val, target_file)
                            elif task_type == 'image':
                                r_img = requests.get(source_val, headers={'User-Agent': 'Mozilla/5.0'}, timeout=8)
                                if r_img.status_code == 200:
                                    save_optimized_image(r_img.content, target_file, max_dim=1200, quality=85)
                        except Exception:
                            pass
                        completed_tasks += 1
                        progress_bar.progress(float(completed_tasks) / float(max(1, total_tasks)))

                    status.text("Sestavuji dokument Microsoft Word (.docx)...")
                    docx_filename = f"{slugify(docx_title_input)}.docx"
                    docx_path = os.path.join(temp_dir, docx_filename)

                    try:
                        docx_layout_mode_param = "page_per_species" if "1 druh" in docx_layout_choice else "compact"
                        generate_docx_booklet(
                            df=df,
                            output_docx_path=docx_path,
                            title=docx_title_input,
                            subtitle=docx_custom_desc,
                            active_cols=active_cols_docx,
                            layout_mode=docx_layout_mode_param,
                            include_toc=docx_include_toc,
                            media_dir=media_dir,
                            media_attributions=media_attributions,
                            include_citations=docx_include_citations,
                            include_media_attribution=docx_include_attributions,
                            col_styles=st.session_state.get('col_styles', {})
                        )

                        with open(docx_path, "rb") as f:
                            docx_bytes = f.read()

                        st.session_state.generated_docx_data = docx_bytes
                        st.session_state.generated_docx_filename = docx_filename
                        st.success("Dokument Microsoft Word (.docx) byl úspěšně vygenerován.")
                    except Exception as e:
                        st.error(f"Při generování Word dokumentu došlo k chybě: {e}")

                    shutil.rmtree(temp_dir, ignore_errors=True)
                    gc.collect()
                    st.rerun()

    if st.session_state.generated_apkg_data is not None or st.session_state.get('generated_obsidian_data') is not None or st.session_state.generated_pdf_data is not None or st.session_state.generated_docx_data is not None:
        with st.expander("5. Stažení výsledků", expanded=False):

            col_res1, col_res2 = st.columns(2)
            with col_res1:
                if st.session_state.generated_apkg_data is not None:
                    st.download_button(
                        label="Stáhnout .apkg balíček pro Anki",
                        data=st.session_state.generated_apkg_data,
                        file_name=st.session_state.generated_apkg_filename,
                        mime="application/octet-stream",
                        key="download_apkg_btn"
                    )
                    st.info(f"Anki balíček obsahuje **{st.session_state.notes_count}** kartiček a **{st.session_state.media_count}** multimediálních souborů.")

                if st.session_state.get('generated_obsidian_data') is not None:
                    st.download_button(
                        label="Stáhnout balíček kartiček (.zip – obsahuje i index.html přehrávač)",
                        data=st.session_state.generated_obsidian_data,
                        file_name=st.session_state.get('generated_obsidian_filename', 'Studijni_Karticky.zip'),
                        mime="application/zip",
                        key="download_obsidian_btn"
                    )
                    st.success("Balíček kartiček (.zip) je připraven. Můžete jej otevřít rovnou poklepáním na index.html uvnitř, nebo naimportovat do přehrávače či Obsidianu.")
                    k_bytes = _read_karty_html_bytes()
                    if k_bytes:
                        st.download_button(
                            label="⬇️ Stáhnout samostatný přehrávač (Karty.html)",
                            data=k_bytes,
                            file_name="Karty.html",
                            mime="text/html",
                            key="btn_download_karty_standalone_blk5"
                        )
                        st.caption("ℹ️ Samostatný webový přehrávač (Karty.html) funguje plně offline a umožňuje pohodlné procvičování na libovolném zařízení.")

                if st.session_state.generated_pdf_data is not None:
                    st.download_button(
                        label="Stáhnout studijní brožuru (.pdf)",
                        data=st.session_state.generated_pdf_data,
                        file_name=st.session_state.generated_pdf_filename,
                        mime="application/pdf",
                        key="download_pdf_btn"
                    )
                    st.success("PDF brožura je připravena ke stažení a tisku.")

                if st.session_state.generated_docx_data is not None:
                    st.download_button(
                        label="Stáhnout dokument Word (.docx)",
                        data=st.session_state.generated_docx_data,
                        file_name=st.session_state.generated_docx_filename,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key="download_docx_btn"
                    )
                    st.success("Dokument Word (.docx) je připraven k úpravám a tisku.")

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

    st.markdown("---")
    with st.expander("🛠️ Doplňkové nástroje (Karty.html, Batch Replacer)", expanded=False):
        c_tool1, c_tool2 = st.columns(2, gap="medium")

        with c_tool1:
            st.markdown("##### 🗂️ Samostatný přehrávač kartiček (Karty.html)")
            st.markdown("""
            Kompletní samostatný HTML přehrávač pro offline studium na mobilu, tabletu i počítači:
            - **100% offline & soukromé:** Nevyžaduje instalaci, registraci ani internet.
            - **Chytré opakování (SM-2):** Algoritmus s hodnocením Znovu / Těžké / Dobré / Snadné.
            - **Vlastní denní limit:** Nastavení počtu nových karet za den a odhad doučení.
            - **Otáčecí i vepisovací karty:** Možnost procvičovat psaním s vizuálním diffem.
            - **Heatmapa & statistiky:** Kalendářní přehled učení a detailní Anki statistiky.
            """)
            k_bytes = _read_karty_html_bytes()
            if k_bytes:
                st.download_button(
                    label="⬇️ Stáhnout samostatný přehrávač (Karty.html)",
                    data=k_bytes,
                    file_name="Karty.html",
                    mime="text/html",
                    key="tools_dl_karty_html",
                    help="Stáhne samostatný HTML soubor přehrávače kartiček pro offline použití v prohlížeči.",
                    use_container_width=True
                )
                st.caption("*(Poznámka: Tento přehrávač je také automaticky přibalen uvnitř každého vygenerovaného .zip balíčku jako index.html).*")

        with c_tool2:
            st.markdown("##### 🧹 Batch Replacer (Čištění a úprava tabulek)")
            st.markdown("""
            Rychlý offline nástroj pro přípravu a normalizaci tabulkových dat:
            - **1. Hromadné nahrazování:** Dávková úprava textů podle tabulky pravidel.
            - **2. Chytré párování:** Párování synonym s referenčním seznamem (Fuzzy / Levenshtein shoda).
            - **3. Dvousloupcová kontrola:** Rychlé porovnání tabulek a odhalení chybějících položek.
            - **4. Generátor pravidel:** Automatické vytvoření pravidel z dvojic sloupců.
            """)
            br_html = _read_batch_replacer_html()
            if br_html:
                st.download_button(
                    label="⬇️ Stáhnout Batch Replacer (.html)",
                    data=br_html,
                    file_name="BatchReplacer.html",
                    mime="text/html",
                    key="tools_dl_batch_replacer",
                    help="Stáhne samostatný HTML soubor pro čištění dat v prohlížeči bez internetu.",
                    use_container_width=True
                )
                st.caption("*(Jednosouborová HTML aplikace bez nutnosti instalace).*")

    with st.expander("📖 Návody a tipy (PDF příručky, rady pro studium a řešení problémů)", expanded=False):
        st.markdown("#### 📚 Kompletní uživatelské příručky v PDF ke stažení")
        st.caption("Všechny příručky jsou zpracovány s plnou podporou české diakritiky, obsahují přehledné kapitoly, postupy a doporučení.")

        col_m1, col_m2, col_m3, col_m4 = st.columns(4, gap="small")
        with col_m1:
            if pdf_gen_data:
                st.download_button(
                    "📗 Návod: Generátor (PDF)",
                    data=pdf_gen_data,
                    file_name="O_generatoru.pdf",
                    mime="application/pdf",
                    key="man_dl_gen_pdf",
                    use_container_width=True
                )
        with col_m2:
            if pdf_anki_data:
                st.download_button(
                    "📘 Návod: Jak na Anki (PDF)",
                    data=pdf_anki_data,
                    file_name="O_Anki.pdf",
                    mime="application/pdf",
                    key="man_dl_anki_pdf",
                    use_container_width=True
                )
        with col_m3:
            if 'pdf_karty_data' in locals() and pdf_karty_data:
                st.download_button(
                    "📙 Návod: Karty.html (PDF)",
                    data=pdf_karty_data,
                    file_name="O_Karty_html.pdf",
                    mime="application/pdf",
                    key="man_dl_karty_pdf",
                    use_container_width=True
                )
        with col_m4:
            cit_pdf_data = generate_citations_pdf()
            st.download_button(
                "📄 Citace zdrojů (PDF)",
                data=cit_pdf_data,
                file_name="Citace_a_databaze.pdf",
                mime="application/pdf",
                key="man_dl_cit_pdf",
                use_container_width=True
            )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.markdown("#### 💡 Rychlé tipy pro efektivní studium a řešení potíží")

        c_tip_a, c_tip_b = st.columns(2, gap="medium")
        with c_tip_a:
            with st.container(border=True):
                st.markdown("##### 🧠 1. Jak efektivně studovat poznávačky")
                st.markdown("""
                - **Aktivní vybavování (Active Recall):** Vždy se snažte vybavit jméno druhu či znaky ještě před otočením kartičky. Pouhé pasivní prohlížení vytváří falešný pocit znalosti.
                - **Pravidelnost (Spaced Repetition):** 15 minut denně po dobu dvou týdnů je pro dlouhodobou paměť mnohem účinnější než 8 hodin biflování noc před zkouškou.
                - **Poctivé hodnocení:** Pokud jste váhali, volte *Těžké* nebo *Znovu*. Program se postará o naplánování přesně v momentě, kdy by hrozilo zapomnění.
                """)

            with st.container(border=True):
                st.markdown("##### 📱 2. Bezplatné používání na iPhone / iPad")
                st.markdown("""
                - **Možnost A (Karty.html – bez instalace):** Stáhněte si balíček pro Obsidian / Karty (.zip), v aplikaci *Soubory* na iPhonu jej rozbalte a klepněte na `index.html`. Otevře se v Safari a můžete se rovnou offline učit.
                - **Možnost B (Obsidian):** Stáhněte si bezplatnou aplikaci Obsidian z App Store, otevřete složku balíčku jako Vault a zapněte bezplatný komunitní doplněk *Spaced Repetition*.
                - **Možnost C (AnkiWeb):** Zaregistrujte se zdarma na [ankiweb.net](https://ankiweb.net), synchronizujte balíček z PC a v Safari na mobilu si uložte zástupce na plochu.
                """)

        with c_tip_b:
            with st.container(border=True):
                st.markdown("##### ⚠️ 3. Řešení hlášky 'Prosím aktualizujte na nejnovější verzi Anki'")
                st.markdown("""
                - **Proč se hláška objevuje?** Generátor vytváří balíčky podle moderního formátu Anki 24+ s kompresí Zstandard. Starší verze Anki na počítači (např. verze 2.1.x) tento formát nerozeznají a zobrazí upozornění.
                - **Řešení:** Stáhněte si bezplatnou aktualizaci přímo z oficiálního webu [apps.ankiweb.net](https://apps.ankiweb.net). Aktualizace je zdarma a všechny vaše stávající balíčky i postup učení zůstanou netknuté.
                """)

            with st.container(border=True):
                st.markdown("##### 🔄 4. Párování sloupců při slučování s novou tabulkou")
                st.markdown("""
                - Pokud máte v Anki rozečtený balíček a chcete k němu přidat nové druhy, nahrajte starý `.apkg` i nový Excel najednou.
                - Generátor automaticky zachová historii zkoušení u existujících druhů a přidá nové.
                - Pokud se sloupce jmenují jinak (např. *Poznámky* vs. *Popis*), v sekci *1. Načtení dat → Sloučení a doplnění* si můžete ručně určit propojení a nastavit prioritu, ze kterého souboru se mají data zachovat.
                """)

