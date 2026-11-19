import re
import functools

CZ_TO_EN = {
    # Header & Theme & Language
    "Vzhled aplikace:": "App theme:",
    "Světlý režim": "Light mode",
    "Tmavý režim": "Dark mode",
    "Jazyk / Language:": "Language:",
    "Generátor kartiček Anki": "Anki Card Generator",
    "Nahrajte tabulku, obohaťte ji o data přes API a sestavte líc a rub kartiček.": "Upload a table, enrich it via APIs, and build card fronts, backs, or study booklets.",

    # Main expanders & tabs
    "1. Načtení dat": "1. Load Data",
    "2. Náhled tabulky": "2. Table Preview",
    "3. Výběr modulů pro obohacení dat": "3. Data Enrichment Modules",
    "4. Výběr výstupního formátu a obsahu": "4. Output Format & Content",
    "5. Stažení výsledků": "5. Download Results",
    "Doplňkové nástroje (Karty.html, Batch Replacer)": "Extra Tools (Karty.html, Batch Replacer)",
    "Návody a tipy (PDF příručky, rady pro studium a řešení problémů)": "Guides & Tips (PDF manuals, study advice & troubleshooting)",
    "Nástroje pro úpravu dat": "Data Editing Tools",
    "Editace textových sloupců a popisů (např. Pladias)": "Edit Text Columns & Descriptions (e.g. Pladias)",
    "Sjednocení a převod nomenklatury (Synonymika / Pladias.cz / iNaturalist / Vlastní převodník)": "Nomenclature Unification & Conversion (Synonyms / Pladias.cz / iNaturalist / Custom)",
    "Vlastní fotografie a multimédia": "Custom Photos & Media",
    "Výběr zdrojů dat a citací do bibliografie (volitelné)": "Data Sources & Bibliography Citations (optional)",

    # Step 1: Data loading
    "Zvolte zdroj dat:": "Choose data source:",
    "Nahrát Excel / CSV / TXT": "Upload Excel / CSV / TXT",
    "Nahrát stávající Anki balíček (.apkg)": "Upload existing Anki deck (.apkg)",
    "Vložit text / seznam ručně": "Paste text / list manually",
    "Sloučení a doplnění (Excel + stávající .apkg)": "Merge & Update (Excel + existing .apkg)",
    "Testovací sada (ukázková data)": "Sample Test Dataset",
    "Nahrajte soubor (Excel, CSV, TSV nebo TXT):": "Upload file (Excel, CSV, TSV, or TXT):",
    "Nahrajte Anki balíček (.apkg):": "Upload Anki deck (.apkg):",
    "Vyberte testovací sadu:": "Select sample dataset:",
    "Načíst testovací data": "Load sample data",
    "Načíst vložený seznam": "Load pasted list",
    "Zadejte nebo vložte seznam (každá položka na nový řádek):": "Enter or paste list (one item per line):",

    # Step 2: Preview & editing
    "##### Náhled tabulky (prvních 5 položek)": "##### Table Preview (first 5 rows)",
    "Stáhnout (CSV)": "Download (CSV)",
    "Stáhnout (Excel)": "Download (Excel)",
    "Způsob úpravy:": "Edit mode:",
    "Detailní úprava jednoho řádku (vhodné pro delší popisy)": "Single-row detailed editor (best for long descriptions)",
    "Hromadná úprava v tabulce": "Bulk spreadsheet editor",
    "Vyberte položku (řádek):": "Select item (row):",
    "Vyberte sloupec k úpravě:": "Select column to edit:",
    "Uložit změnu buňky": "Save cell change",
    "Sloupce zobrazené k úpravě:": "Columns shown for editing:",
    "Uložit změny z tabulky": "Save table changes",
    "**1. Odstranění duplicitních řádků**": "**1. Remove duplicate rows**",
    "Odstranit duplicity": "Remove duplicates",
    "**2. Smazání nepotřebného sloupce**": "**2. Delete unused column**",
    "Smazat sloupec": "Delete column",
    "**3. Převedení na druhovou úroveň**": "**3. Convert to species level**",

    # Custom photos & curator
    "1. Průvodce: Fotky + tabulka citací (Doporučeno)": "1. Wizard: Photos + citations table (Recommended)",
    "2. Jednotlivé přiřazení k druhu": "2. Assign to individual species",
    "3. Rychlé párování podle názvu souboru": "3. Batch match by filename",
    "4. Pokročilý výběr z databází (Pladias / iNat / Wikimedia)": "4. Advanced Database Photo Picker (Pladias / iNat / Wikimedia)",
    "#### Pokročilý výběr fotografií z databází pro jednotlivé druhy": "#### Advanced Database Photo Picker per Species",
    "Prohlédněte si kandidáty z Pladias.cz, iNaturalist, Wikimedia Commons nebo aktuální fotky v buňce a vyberte přesně ty, které chcete v kartičce/PDF ponechat.": "Browse candidates from Pladias.cz, iNaturalist, Wikimedia Commons, or current cell photos and pick the exact ones to keep.",
    "◀ Předchozí": "◀ Previous",
    "Další ▶": "Next ▶",
    "Vyberte druh / položku:": "Select species / item:",
    "Cílový sloupec v tabulce:": "Target table column:",
    "Zdroj kandidátů:": "Candidate source:",
    "Kandidátů:": "Candidates:",
    "Načíst náhledy kandidátů": "Load candidate previews",
    "Uložit vybrané fotky pro tento druh": "Save selected photos for this species",
    "Klikněte na **Načíst náhledy kandidátů** pro zobrazení dostupných fotografií ze zvoleného zdroje.": "Click **Load candidate previews** to view available photos from the selected source.",
    "Aktuální fotky v buňce": "Current photos in cell",
    "Pladias.cz (všechny fotky v pořadí)": "Pladias.cz (all photos in order)",
    "Pladias.cz – Celá rostlina (habitus)": "Pladias.cz – Whole plant (habitus)",
    "Pladias.cz – Květ / květenství": "Pladias.cz – Flower / inflorescence",
    "Pladias.cz – List": "Pladias.cz – Leaf",
    "Pladias.cz – Plod / semeno": "Pladias.cz – Fruit / seed",
    "Výchozí popisek pro spárované fotografie:": "Default caption for matched photos:",
    "Vyberte fotografie pro hromadné spárování:": "Select photos for batch matching:",
    "Provést hromadné spárování": "Run batch matching",

    # Step 3: Enrichment
    "Profil obohacení pro kategorii (1 kliknutí):": "Category enrichment preset (1 click):",
    "-- Vlastní výběr nástrojů --": "-- Custom module selection --",
    "**Limit fotografií**": "**Photo Limit**",
    "Počet fotek na položku:": "Photos per item:",
    "Přeskočit již vyplněné buňky (rychlé doplnění chybějících dat)": "Skip already filled cells (fast fill of missing data)",
    "Spustit obohacování dat": "Run Data Enrichment",
    "Fotky z Pladias.cz": "Photos from Pladias.cz",
    "Max fotek z Pladias.cz na řádek": "Max Pladias.cz photos per row",
    "Mapa rozšíření v ČR (Pladias.cz)": "Czech Republic distribution map (Pladias.cz)",
    "Český botanický popis a znaky z Pladias.cz": "Czech botanical description & traits (Pladias.cz)",
    "Česká botanická taxonomie (Pladias.cz)": "Czech botanical taxonomy (Pladias.cz)",
    "České jméno z iNaturalist a fotky": "Czech name & photos from iNaturalist",
    "Max fotek z iNat na řádek": "Max iNaturalist photos per row",
    "Stáhnout popis druhu z Wikipedie": "Fetch species description from Wikipedia",
    "Obrázky z Wikimedia Commons": "Images from Wikimedia Commons",
    "Max obrázků z Wikimedia Commons na řádek": "Max Wikimedia Commons images per row",
    "Taxonomie z GBIF": "Taxonomy from GBIF",
    "Latinská hlasová výslovnost [TTS Latina]": "Latin voice pronunciation [TTS Latin]",
    "Fonetická výslovnost latiny (český přepis)": "Latin phonetic transcription (Czech phonetics)",
    "Výslovnost (Audio TTS)": "Pronunciation (Audio TTS)",
    "Překlad textu": "Text translation",

    # Step 4: Output tabs
    "1. Balíček do Anki (.apkg)": "1. Anki Deck (.apkg)",
    "2. Obsidian & Webový přehrávač (.zip)": "2. Obsidian & Web Player (.zip)",
    "3. Studijní brožura v PDF (.pdf)": "3. Study Booklet (.pdf)",
    "4. Editovatelný dokument Word (.docx)": "4. Editable Word Document (.docx)",

    # Anki Tab
    "##### 1. Líc kartičky (Otázka / Přední strana)": "##### 1. Card Front (Question)",
    "##### 2. Rub kartičky (Odpověď / Zadní strana)": "##### 2. Card Back (Answer)",
    "Vyberte sloupce na líc kartičky (např. obrázky):": "Select columns for card front (e.g. images):",
    "Vyberte sloupce na rub kartičky (např. název, popis):": "Select columns for card back (e.g. name, description):",
    "Změnit pořadí sloupců na líci (⇧ / ▲ / ▼ / ⇩)": "Reorder front columns (⇧ / ▲ / ▼ / ⇩)",
    "Změnit pořadí sloupců na rubu (⇧ / ▲ / ▼ / ⇩)": "Reorder back columns (⇧ / ▲ / ▼ / ⇩)",
    "Pokročilé nastavení zobrazení sloupců (formátování textu)": "Advanced Column Display Settings (text formatting)",
    "#### Vzhled a chování Anki kartičky": "#### Anki Card Appearance & Behavior",
    "Barevné téma kartičky:": "Card color theme:",
    "Zobrazení po kliknutí na odpověď:": "Display after clicking Answer:",
    "Pod sebe (líc + rub)": "Stacked (front + back)",
    "Na druhou stranu (pouze rub)": "Back side only",
    "Zobrazovat autory a licence (CC) u fotografií a nahrávek": "Show authors and CC licenses on photos and audio",
    "#### Režim zkoušení v Anki (Typ kartiček)": "#### Anki Study Mode (Card Type)",
    "Způsob testování:": "Testing mode:",
    "Standardní (otočení kliknutím)": "Standard (click to flip)",
    "Vepisovací (psaní z klávesnice)": "Type-in (keyboard input)",
    "Pole, které má uživatel vepsat z klávesnice:": "Field for user to type in:",
    "#### Nastavení a export balíčku Anki": "#### Anki Deck Settings & Export",
    "Název balíčku (Anki Deck Name)": "Deck Name (Anki Deck Name)",
    "Rozdělit do podbalíčků podle sloupce (volitelně):": "Split into subdecks by column (optional):",
    "— Bez rozdělení —": "— No splitting —",
    "Pořadí kartiček při učení v Anki:": "Card study order in Anki:",
    "Podle pořadí v tabulce (od 1. řádku)": "Table order (from row 1)",
    "Obráceně (od posledního řádku)": "Reversed (from last row)",
    "Abecedně podle sloupce (A → Z)": "Alphabetical by column (A → Z)",
    "Abecedně podle sloupce (Z → A)": "Alphabetical by column (Z → A)",
    "Náhodně zamíchat": "Random shuffle",
    "Sloupec pro abecední seřazení:": "Column for alphabetical sorting:",
    "Vynutit nová ID karet v Anki (vytvořit jako nové karty místo aktualizace existujících)": "Force new Anki card IDs (create new cards instead of updating existing)",
    "Současně vygenerovat i balíček pro Obsidian / Karty.html (.zip) se stejným rozvržením": "Also generate Obsidian / Karty.html (.zip) package with the same layout",
    "Generovat balíček pro Anki (.apkg)": "Generate Anki Package (.apkg)",
    "Balíček Anki byl úspěšně vygenerován.": "Anki package generated successfully.",
    "Balíčky pro Anki (.apkg) i Obsidian (.zip) byly úspěšně vygenerovány!": "Both Anki (.apkg) and Obsidian (.zip) packages generated successfully!",

    # Obsidian Tab
    "#### Export kartiček (.zip) – Webový přehrávač & Obsidian (Zdarma pro iPhone, iPad i PC)": "#### Card Export (.zip) – Web Player & Obsidian (Free for iPhone, iPad & PC)",
    "Překlopit rozvržení z Anki (Líc, Rub i formátování)": "Copy layout from Anki (Front, Back & formatting)",
    "Název složky / balíčku v Obsidianu:": "Obsidian folder / package name:",
    "Režim kartiček pro Spaced Repetition:": "Spaced Repetition card mode:",
    "Jednosměrné (?) - líc na rub (Doporučeno)": "One-way (?) - front to back (Recommended)",
    "Obousměrné (??) - líc na rub i rub na líc": "Bidirectional (??) - front to back & back to front",
    "Pokročilé nastavení zobrazení sloupců (formátování textu v Obsidianu)": "Advanced Column Display Settings (Obsidian formatting)",
    "Současně vygenerovat i Anki balíček (.apkg) se stejným rozvržením": "Also generate Anki (.apkg) package with the same layout",
    "Generovat balíček pro Obsidian (.zip)": "Generate Obsidian Package (.zip)",

    # PDF Tab
    "#### Nastavení exportu studijní brožury (PDF)": "#### Study Booklet Export Settings (PDF)",
    "Výběr a pořadí sloupců pro tisk do PDF:": "Select and order columns for PDF:",
    "Formát rozvržení stránek:": "Page layout format:",
    "Kompaktní brožurka (více druhů za sebou)": "Compact booklet (multiple species per page)",
    "1 druh na stránku (Atlasový list / Kartotéka)": "1 species per page (Atlas sheet / Card)",
    "Dvojstrana pro taxon (1 strana obrázky, protilehlá strana popis)": "2-page spread per taxon (1 page images, 1 page text)",
    "Formát stránky:": "Page size:",
    "Typ tisku a vazba:": "Print type & binding:",
    "Velikost textu (%):": "Text size (%):",
    "Velikost fotografií (%):": "Photo size (%):",
    "Okraje stránky:": "Page margins:",
    "Rozložení fotek:": "Photo grid layout:",
    "Umístění mapy rozšíření:": "Distribution map placement:",
    "Pod tabulkou vlastností (doporučeno)": "Below properties table (recommended)",
    "V galerii mezi fotografiemi": "Inside photo gallery",
    "Počet fotografií a map na druh:": "Photos and maps per species:",
    "Až 6 (doporučeno: 4 fotky + 2 mapy)": "Up to 6 (recommended: 4 photos + 2 maps)",
    "Až 4 (doporučeno: 2 fotky + 2 mapy)": "Up to 4 (recommended: 2 photos + 2 maps)",
    "Generovat PDF brožuru": "Generate PDF Booklet",
    "Interaktivní náhled PDF (1. položka)": "Interactive PDF Preview (1st item)",

    # Citations & Downloads
    "Vybrat vše": "Select all",
    "Dle sloupců (auto)": "By columns (auto)",
    "Zrušit vše": "Clear all",
    "Uvést tyto zdroje a citace v závěrečném přehledu:": "Include these sources and citations in bibliography:",
    "Stáhnout .apkg balíček pro Anki": "Download Anki Package (.apkg)",
    "Stáhnout balíček kartiček (.zip – obsahuje i index.html přehrávač)": "Download Card Package (.zip – includes index.html player)",
    "⬇Stáhnout samostatný přehrávač (Karty.html)": "⬇ Download Standalone Player (Karty.html)",
    "Stáhnout studijní brožuru (.pdf)": "Download Study Booklet (.pdf)",
    "Stáhnout dokument Word (.docx)": "Download Word Document (.docx)",
    "Stáhnout seznam nenalezených položek (.csv)": "Download unfound items list (.csv)",
    "Tučné": "Bold",
    "Kurzíva": "Italic",
    "Velikost písma:": "Font size:",
    "Vlastní název pole:": "Custom field label:",
    "Zobrazit název pole:": "Show field label:",
    "Výchozí": "Default",
    "Malé (12px)": "Small (12px)",
    "Střední (16px)": "Medium (16px)",
    "Velké (20px)": "Large (20px)",
    "Obrovské (24px)": "Huge (24px)",
}

_REGEX_RULES = [
    (re.compile(r'^Sloupec:\s*(.+)$'), r'Column: \1'),
    (re.compile(r'^\*\*Sloupec:\s*(.+?)\*\*$'), r'**Column: \1**'),
    (re.compile(r'^Obsah buňky \((.+?)\):$'), r'Cell content (\1):'),
    (re.compile(r'^Vyberte fotografie pro `(.+?)` → `(.+?)`:$'), r'Select photos for `\1` → `\2`:'),
    (re.compile(r'^\*\*Vyberte fotografie pro `(.+?)` → `(.+?)`:\*\*$'), r'**Select photos for `\1` → `\2`:**'),
    (re.compile(r'^Vybrat #(\d+)(.*)$'), r'Select #\1\2'),
    (re.compile(r'^(\d+)\s+položek\s+&bull;\s+(\d+)\s+sloupců$'), r'\1 items &bull; \2 columns'),
    (re.compile(r'^Stahuji a optimalizuji média \((\d+)/(\d+)\)\.\.\.$'), r'Downloading and optimizing media (\1/\2)...'),
    (re.compile(r'^Stahuji multimediální soubory pro Obsidian \((\d+)/(\d+)\)\.\.\.$'), r'Downloading Obsidian media files (\1/\2)...'),
]

_UI_LANG_GETTER = None

def set_lang_getter(fn):
    global _UI_LANG_GETTER
    _UI_LANG_GETTER = fn

def is_en() -> bool:
    if _UI_LANG_GETTER is not None:
        try:
            return _UI_LANG_GETTER() == "en"
        except Exception:
            return False
    return False

def tr(text):
    if not isinstance(text, str) or not is_en():
        return text
    if text in CZ_TO_EN:
        return CZ_TO_EN[text]
    stripped = text.strip()
    if stripped in CZ_TO_EN:
        return CZ_TO_EN[stripped]
    for pat, repl in _REGEX_RULES:
        m = pat.match(stripped)
        if m:
            return pat.sub(repl, stripped)
    # HTML header / badge fallback
    if '<div class="main-title">' in text or '<div class="subtitle">' in text or 'položek &bull;' in text:
        out = text
        for cz, en in [
            ("Generátor kartiček Anki", "Anki Card Generator"),
            ("Nahrajte tabulku, obohaťte ji o data přes API a sestavte líc a rub kartiček.", "Upload a table, enrich it via APIs, and build card fronts, backs, or study booklets."),
        ]:
            out = out.replace(cz, en)
        out = re.sub(r'(\d+)\s+položek\s+&bull;\s+(\d+)\s+sloupců', r'\1 items &bull; \2 columns', out)
        return out
    return text

def install_streamlit_i18n(st_mod):
    if getattr(st_mod, "_i18n_installed", False):
        return
    st_mod._i18n_installed = True

    def _wrap_first_arg(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            if args and isinstance(args[0], str):
                args = (tr(args[0]),) + args[1:]
            elif "label" in kwargs and isinstance(kwargs["label"], str):
                kwargs["label"] = tr(kwargs["label"])
            elif "body" in kwargs and isinstance(kwargs["body"], str):
                kwargs["body"] = tr(kwargs["body"])
            if "help" in kwargs and isinstance(kwargs["help"], str):
                kwargs["help"] = tr(kwargs["help"])
            if "placeholder" in kwargs and isinstance(kwargs["placeholder"], str):
                kwargs["placeholder"] = tr(kwargs["placeholder"])
            return fn(*args, **kwargs)
        return wrapper

    def _wrap_choice(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            if args and isinstance(args[0], str):
                args = (tr(args[0]),) + args[1:]
            elif "label" in kwargs and isinstance(kwargs["label"], str):
                kwargs["label"] = tr(kwargs["label"])
            if "help" in kwargs and isinstance(kwargs["help"], str):
                kwargs["help"] = tr(kwargs["help"])
            if is_en() and "format_func" not in kwargs:
                kwargs["format_func"] = lambda x: tr(str(x))
            return fn(*args, **kwargs)
        return wrapper

    def _wrap_tabs(fn):
        @functools.wraps(fn)
        def wrapper(tabs, *args, **kwargs):
            if isinstance(tabs, (list, tuple)):
                tabs = [tr(t) if isinstance(t, str) else t for t in tabs]
            return fn(tabs, *args, **kwargs)
        return wrapper

    for name in [
        "markdown", "title", "header", "subheader", "caption", "text",
        "info", "warning", "error", "success", "toast",
        "expander", "button", "download_button", "checkbox",
        "text_input", "text_area", "slider", "number_input", "file_uploader"
    ]:
        orig = getattr(st_mod, name, None)
        if orig is not None:
            setattr(st_mod, name, _wrap_first_arg(orig))

    for cname in ["radio", "selectbox", "multiselect"]:
        orig = getattr(st_mod, cname, None)
        if orig is not None:
            setattr(st_mod, cname, _wrap_choice(orig))

    if hasattr(st_mod, "tabs"):
        st_mod.tabs = _wrap_tabs(st_mod.tabs)
