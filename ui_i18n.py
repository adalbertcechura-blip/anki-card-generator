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
    "1. Vstupní data a správa souborů": "1. Input Data & File Management",
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
    "Vlastní data": "Custom Data",
    "Testovací data": "Sample Data",
    "Předpřipravené ukázkové sady z různých oborů.": "Pre-prepared sample datasets from various fields.",
    "Způsob zadání vlastních dat:": "Custom data input method:",
    "Nahrát soubor (Excel, CSV, TXT, APKG)": "Upload file (Excel, CSV, TXT, APKG)",
    "Vložit seznam ručně (textové pole)": "Paste list manually (text box)",
    "Nahrajte jeden nebo více souborů (Excel .xlsx, CSV, TXT nebo balíček Anki .apkg / .colpkg):": "Upload one or more files (Excel .xlsx, CSV, TXT, or Anki .apkg / .colpkg):",
    "Vyberte kategorii / list:": "Select category / sheet:",
    "Způsob načtení souborů:": "File loading mode:",
    "Nahradit stávající data": "Replace existing data",
    "Připojit k existující tabulce": "Append to existing table",
    "Přidat k existující tabulce": "Add to existing table",
    "Načíst jako nový seznam": "Load as new list",
    "Sloučit a doplnit (Zachovat historii učení pro existující druhy a přidat nové druhy z tabulky)": "Merge & update (Keep study history for existing species and add new species from table)",
    "Detekován balíček Anki + tabulka Excel/CSV (Inteligentní sloučení se zachováním historie učení)": "Detected Anki package + Excel/CSV table (Smart merge preserving study history)",
    "Propojení sloupců a priorita zdroje:": "Column mapping & source priority:",
    "Způsob párování sloupců mezi tabulkou a balíčkem Anki:": "Column matching mode between table and Anki package:",
    "Automaticky spárovat sloupce (např. Popis ↔ Poznámky, České jméno ↔ Český název, Fotografie ↔ Obrázek)": "Auto-match columns (e.g. Description ↔ Notes, Czech Name, Photo ↔ Image)",
    "Vlastní propojení sloupců (ruční přiřazení)": "Custom column mapping (manual)",
    "Při nalezení druhu v obou zdrojích upřednostnit data z:": "When a species exists in both sources, prefer data from:",
    "Tabulky (Excel/CSV) – texty a poznámky z tabulky přepíší Anki (doporučeno)": "Table (Excel/CSV) – table texts overwrite Anki (recommended)",
    "Balíčku Anki – zachovat původní texty a data z Anki": "Anki package – keep original Anki texts and data",
    "Vlastní výběr zdroje pro každý sloupec zvlášť": "Custom source per column",
    "Jak naložit se seznamem druhů?": "How to handle the species list?",
    "Pouze druhy z tabulky (Ponechat pouze druhy z tabulky a z Anki přenést historii učení)": "Only species from table (Keep table species and transfer Anki study history)",
    "Pro každý sloupec z tabulky zvolte odpovídající pole z Anki. Pokud mají oba zdroje hodnotu, zvolte který zdroj má přednost:": "For each table column select the matching Anki field and priority:",
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
    "Vložte seznam položek (jeden na každý řádek):": "Paste list of items (one per line):",
    "Seznam položek je prázdný.": "Item list is empty.",
    "Ze souboru se nepodařilo načíst žádná data.": "Could not load any data from the file.",

    # Step 2: Preview & editing & nomenclature
    "Náhled tabulky (prvních 5 položek)": "Table Preview (first 5 rows)",
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
    "Vymaže všechny duplicitní záznamy podle prvního sloupce tabulky.": "Removes duplicate rows based on the first column.",
    "V tabulce nebyly nalezeny žádné duplicity.": "No duplicates found in the table.",
    "**2. Smazání nepotřebného sloupce**": "**2. Delete unused column**",
    "Smazat sloupec": "Delete column",
    "**2. Smazání konkrétního řádku**": "**2. Delete specific row**",
    "Položka k odstranění:": "Item to remove:",
    "Smazat řádek": "Delete row",
    "Vyberte položku ze seznamu a odstraňte ji z tabulky.": "Select an item from the list and remove it from the table.",
    "**3. Převedení na druhovou úroveň**": "**3. Convert to species level**",
    "Převést na druhovou úroveň": "Convert to species level",
    "Odstraní ze jmen taxonů poddruhy, variety a agregáty (subsp., var., agg.) a automaticky sloučí vzniklé duplicity.": "Strips subspecies, varieties, and aggregates (subsp., var., agg.) and merges resulting duplicates.",
    "Zdroj nomenklaturního převodníku:": "Nomenclature converter source:",
    "Nastavení mapování sloupců převodníku:": "Converter column mapping settings:",
    "Sloupec se starým / původním jménem (synonymem):": "Column with old / original name (synonym):",
    "Sloupec s novým / platným jménem:": "Column with new / accepted name:",
    "Sloupec v načtené tabulce k převodu:": "Column in loaded table to convert:",
    "Sloupec se jmény k vyčištění:": "Column with names to clean:",
    "Cíl převodu:": "Conversion target:",
    "Nahradit hodnoty ve stávajícím sloupci": "Replace values in existing column",
    "Vytvořit nový sloupec": "Create new column",
    "Název nového sloupce:": "New column name:",
    "Ignorovat velikost písmen (case-insensitive)": "Ignore case (case-insensitive)",
    "Očistit autorské zkratky a infraspecifické taxony při párování (L., DC., subsp., var.)": "Strip author abbreviations and infraspecific ranks when matching (L., DC., subsp., var.)",
    "Zahrnout online databázi synonym (GBIF Backbone Taxonomy & iNaturalist API) pro stará synonyma (např. Lychnis viscaria -> Viscaria vulgaris)": "Include online synonym database (GBIF Backbone Taxonomy & iNaturalist API)",
    "Provést převod a sjednocení nomenklatury": "Run nomenclature conversion & unification",
    "Nahrajte převodní tabulku (2 sloupce: Původní jméno / Nové jméno)": "Upload conversion table (2 columns: Old name / New name)",
    "Uložit převodník do trvalé knihovny jako (např. pladias_cz_to_inat):": "Save converter to permanent library as:",
    "Uložit do knihovny": "Save to library",

    # Custom photos & curator
    "Umožňuje nahrát vlastní fotografie z vašeho počítače, spárovat je s tabulkou citací/autorů a přiřadit je ke konkrétním řádkům v hlavní tabulce.": "Upload your own photos, pair them with a citations/authors table, and assign them to rows in the main table.",
    "1. Průvodce: Fotky + tabulka citací (Doporučeno)": "1. Wizard: Photos + citations table (Recommended)",
    "2. Jednotlivé přiřazení k druhu": "2. Assign to individual species",
    "3. Rychlé párování podle názvu souboru": "3. Batch match by filename",
    "4. Pokročilý výběr z databází (Pladias / iNat / Wikimedia)": "4. Advanced Database Photo Picker (Pladias / iNat / Wikimedia)",
    "3-krokový průvodce spárováním fotografií a citací": "3-step photo & citation pairing wizard",
    "Krok 1: Nahrání fotografií ze souborů": "Step 1: Upload photo files",
    "Krok 2: Nahrání tabulky se zdroji / autory a spárování mezi sebou": "Step 2: Upload sources/authors table and pair",
    "Krok 3: Párování s hlavní tabulkou dat": "Step 3: Pair with main data table",
    "Vyberte fotografie z vašeho počítače (můžete vybrat více souborů najednou):": "Select photos from your computer (multiple files allowed):",
    "Nahrajte tabulku obsahující sloupce Soubor a Autor (Excel .xlsx nebo CSV):": "Upload table with File and Author columns (Excel .xlsx or CSV):",
    "Sloupec se jménem souboru:": "Filename column:",
    "Sloupec s autorem / citací:": "Author / citation column:",
    "Spárovat fotografie s citacemi (Krok 2)": "Pair photos with citations (Step 2)",
    "Způsob párování k řádkům v hlavní tabulce:": "Row matching method in main table:",
    "Který sloupec v hlavní tabulce obsahuje jména souborů:": "Which column in main table contains filenames:",
    "Uložit fotografie do sloupce v hlavní tabulce:": "Save photos to column in main table:",
    "Přiřadit spárované fotografie do hlavní tabulky (Krok 3)": "Assign paired photos to main table (Step 3)",
    "Nejprve prosím nahrajte fotografie v Kroku 1!": "Please upload photos in Step 1 first!",
    "Vyberte druh pro přiřazení fotografie:": "Select species to assign photo to:",
    "Popisek / autor fotografie (např. Vlastní foto – detail květu):": "Photo caption / author (e.g. Own photo – flower detail):",
    "Přidat / Přiřadit fotografie k druhu": "Add / Assign photos to species",
    "Vymazat všechny fotky tohoto druhu": "Delete all photos of this species",
    "Uložit citaci": "Save citation",
    "Pokročilý výběr fotografií z databází pro jednotlivé druhy": "Advanced Database Photo Picker per Species",
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

    # Step 3: Enrichment modules & tabs
    "Téma modulu:": "Module topic:",
    "Biologie – Moduly": "Biology – Modules",
    "Obecná biologie": "General Biology",
    "Botanika": "Botany",
    "Mechorosty": "Bryophytes",
    "Houby": "Fungi",
    "Lišejníky": "Lichens",
    "Řasy & Rozsivky": "Algae & Diatoms",
    "Zoologie": "Zoology",
    "Registry ČR": "Czech Registries",
    "Vybrat vše v této kategorii": "Select all in this category",
    "Obecná nastavení biologie": "General Biology Settings",
    "Specifická nastavení pro botaniku (Rostliny)": "Botany Settings (Plants)",
    "Specifická nastavení pro mechorosty (Mechy, Játrovky, Hlevíky)": "Bryophyte Settings (Mosses, Liverworts, Hornworts)",
    "Specifická nastavení pro houby (Mykologie)": "Fungi Settings (Mycology)",
    "Specifická nastavení pro lišejníky (DaLiBor – dalib.cz)": "Lichen Settings (DaLiBor – dalib.cz)",
    "Specifická nastavení pro řasy a rozsivky": "Algae & Diatoms Settings",
    "Specifická nastavení pro zoologii": "Zoology Settings",
    "Národní databáze a registry ČR": "Czech National Databases & Registries",
    "Aktivní moduly (0): Žádný modul není vybrán.": "Active modules (0): No module selected.",
    "Přeskočit položky, které již mají data vyplněná (nepřepisovat existující hodnoty)": "Skip items that already have data filled (do not overwrite existing values)",
    "Přeskočit již vyplněné buňky (rychlé doplnění chybějících dat)": "Skip already filled cells (fast fill of missing data)",
    "Spustit obohacení dat (API)": "Run Data Enrichment (API)",
    "Spustit obohacování dat": "Run Data Enrichment",
    "Profil obohacení pro kategorii (1 kliknutí):": "Category enrichment preset (1 click):",
    "-- Vlastní výběr nástrojů --": "-- Custom module selection --",
    "**Limit fotografií**": "**Photo Limit**",
    "Počet fotek na položku:": "Photos per item:",
    "iNaturalist (České jméno & Obrázky)": "iNaturalist (Czech Name & Images)",
    "iNaturalist mapa pozorování": "iNaturalist observation map",
    "Územní filtr pro pozorování iNaturalist:": "Geographic filter for iNaturalist observations:",
    "Zadejte název území (např. Benešov, Klatovy, Šumava, Krkonoše):": "Enter region name (e.g. Prague, Bohemia, Alps):",
    "GBIF taxonomie": "GBIF Taxonomy",
    "Wikimedia Commons vyhledávač obrázků": "Wikimedia Commons image search",
    "Odkaz na Wikipedii": "Wikipedia link",
    "Stáhne anglický popis z Wikipedie – funguje pro rostliny i živočichy.": "Fetches English description from Wikipedia – works for plants and animals.",
    "Fotky z Pladias.cz": "Photos from Pladias.cz",
    "Max fotek z Pladias.cz na řádek": "Max Pladias.cz photos per row",
    "Použít náhradní fotku, pokud vybraná část není dostupná": "Use fallback photo if selected plant part is unavailable",
    "Vyberte kategorie / části rostliny (každá se načte do samostatného sloupce):": "Select categories / plant parts (each into its own column):",
    "Mapa rozšíření v ČR (Pladias.cz)": "Czech Republic distribution map (Pladias.cz)",
    "Mapa rozšíření ČR z Pladias.cz": "CZ distribution map from Pladias.cz",
    "Územní filtr / výřez pro mapu z Pladias.cz:": "Geographic filter / crop for Pladias.cz map:",
    "Zadejte název území v ČR (např. Benešov, Klatovy, Šumava, Třeboňsko, Beskydy):": "Enter Czech region name (e.g. Benešov, Šumava, Krkonoše):",
    "Český botanický popis a znaky z Pladias.cz": "Czech botanical description & traits from Pladias.cz",
    "Vyberte vlastnosti druhu (vytvoří se samostatné sloupce):": "Select species traits (creates separate columns):",
    "Česká botanická taxonomie (Pladias.cz)": "Czech botanical taxonomy (Pladias.cz)",
    "Stáhnout také české jméno druhu z Pladias.cz": "Also fetch Czech species name from Pladias.cz",
    "Botanický popis z Květeny ČR (ibot.cas.cz PDF)": "Botanical description from Flora of the Czech Rep. (ibot.cas.cz PDF)",
    "Rozsah popisu z Květeny ČR:": "Flora of CZ description scope:",
    "Zkrácený popis (limit znaků)": "Shortened description (character limit)",
    "Kompletní popis (plné znění kapitoly z Květeny ČR)": "Full description (complete chapter from Flora of CZ)",
    "Maximální délka popisu (počet znaků):": "Max description length (characters):",
    "Červený seznam ČR (AOPK ČR – Kategorie ohrožení)": "Czech Red List (AOPK ČR – Threat category)",
    "Přidat samostatný sloupec: Odkaz na Červený seznam (PDF / Portál)": "Add separate column: Red List link (PDF / Portal)",
    "Ellenbergovy indikační hodnoty pro ČR (L, T, M, R, N, S)": "Ellenberg indicator values for CZ (L, T, M, R, N, S)",
    "Výskyt v biotopech ČR": "Occurrence in Czech habitats",
    "Katalog nepůvodních druhů rostlin ČR (status, původ)": "Catalogue of Alien Plants of CZ (status, origin)",
    "Fotografie a mikroskopie mechorostů (GBIF / iNaturalist)": "Bryophyte photos & microscopy (GBIF / iNaturalist)",
    "Čerpá z mezinárodních bryologických repozitářů GBIF Bryophytes, iNaturalist, Wikimedia Commons a BryophytePortal.": "Fetches from GBIF Bryophytes, iNaturalist, Wikimedia Commons, and BryophytePortal.",
    "Odborný popis mechorostu (habitus, gametofyt, sporofyt, ekologie)": "Bryophyte description (habitus, gametophyte, sporophyte, ecology)",
    "Odkaz na bryologický portál (BryophytePortal / BBS / Bryo.cz)": "Bryological portal link (BryophytePortal / BBS / Bryo.cz)",
    "Český popis z Mykologie.net": "Czech description from Mykologie.net",
    "Vědecké jméno z Mykologie.net": "Scientific name from Mykologie.net",
    "Max fotek z Mykologie.net na řádek": "Max Mykologie.net photos per row",
    "Max fotek z GBIF Houby na řádek": "Max GBIF Fungi photos per row",
    "Fotky lišejníků z DaLiBor (Atlas českých lišejníků)": "Lichen photos from DaLiBor (Atlas of Czech Lichens)",
    "Český popis a ekologie z DaLiBor": "Czech description & ecology from DaLiBor",
    "Max fotek z DaLiBor na řádek": "Max DaLiBor photos per row",
    "Taxonomie & autorita řas a rozsivek (DiatomBase / WoRMS / AlgaeBase)": "Algae & Diatom taxonomy & authority (DiatomBase / WoRMS / AlgaeBase)",
    "Odkaz na vyhledávání na AlgaeBase": "AlgaeBase search link",
    "**Řasy a sinice (AlgaeBase):**": "**Algae & Cyanobacteria (AlgaeBase):**",
    "Max fotek z GBIF Zoologie na řádek": "Max GBIF Zoology photos per row",
    "Hlasy ptáků (Xeno-canto)": "Bird songs & calls (Xeno-canto)",
    "**Typ nahrávky** (lze kombinovat):": "**Recording type** (can combine):",
    "Zpěv (song)": "Song",
    "Hlas / volání (call)": "Call",
    "Počet nahrávek na typ": "Recordings per type",
    "Nahrávky se stáhnou jako MP3 a přiloží do Anki balíčku.": "Recordings are downloaded as MP3 and bundled into the Anki deck.",
    "Max fotek z iNat na řádek": "Max iNaturalist photos per row",
    "Max fotek z Wikimedia Commons na řádek": "Max Wikimedia Commons photos per row",
    "Doplnit vědecké jméno": "Fill scientific name",
    "České jméno z iNaturalist a fotky": "Czech name & photos from iNaturalist",
    "Stáhnout popis druhu z Wikipedie": "Fetch species description from Wikipedia",
    "Obrázky z Wikimedia Commons": "Images from Wikimedia Commons",
    "**Výslovnost latiny:**": "**Latin pronunciation:**",
    "Latinská hlasová výslovnost [TTS Latina]": "Latin voice pronunciation [TTS Latin]",
    "Český fonetický přepis latiny [Fonetická výslovnost]": "Czech phonetic transcription of Latin [Phonetics]",
    "Fonetická výslovnost latiny (český přepis)": "Latin phonetic transcription (Czech phonetics)",
    "Hlasová výslovnost (Google TTS)": "Voice pronunciation (Google TTS)",
    "Jazyk výslovnosti": "Pronunciation language",
    "Výslovnost (Audio TTS)": "Pronunciation (Audio TTS)",
    "Překladač": "Translator",
    "Zdrojový jazyk": "Source language",
    "Cílový jazyk": "Target language",
    "Překlad textu": "Text translation",
    "Anglický výkladový slovník": "English explanatory dictionary",
    "Modul států (hlavní město, region, měna, vlajka...)": "Countries module (capital, region, currency, flag...)",

    # Step 4: Output tabs
    "1. Balíček do Anki (.apkg)": "1. Anki Deck (.apkg)",
    "1. Balíček pro Anki (.apkg)": "1. Anki Deck (.apkg)",
    "2. Obsidian & Webový přehrávač (.zip)": "2. Obsidian & Web Player (.zip)",
    "2. Kartičky pro mobil i PC (.zip / HTML / Obsidian)": "2. Mobile & PC Cards (.zip / HTML / Obsidian)",
    "3. Studijní brožura v PDF (.pdf)": "3. Study Booklet (.pdf)",
    "4. Editovatelný dokument Word (.docx)": "4. Editable Word Document (.docx)",

    # Anki Tab
    "Návrh kartiček Anki (Líc / Rub) a export": "Anki Card Design (Front / Back) & Export",
    "1. Lícová strana": "1. Front Side",
    "2. Rubová strana": "2. Back Side",
    "1. Líc kartičky (Otázka / Přední strana)": "1. Card Front (Question)",
    "2. Rub kartičky (Odpověď / Zadní strana)": "2. Card Back (Answer)",
    "Vyberte sloupce na LÍCI karty:": "Select columns for card FRONT:",
    "Vyberte sloupce na líc kartičky (např. obrázky):": "Select columns for card front (e.g. images):",
    "Vyberte sloupce na rub kartičky (např. název, popis):": "Select columns for card back (e.g. name, description):",
    "Změnit pořadí sloupců na líci (⇧ / ▲ / ▼ / ⇩)": "Reorder front columns (⇧ / ▲ / ▼ / ⇩)",
    "Změnit pořadí sloupců na rubu (⇧ / ▲ / ▼ / ⇩)": "Reorder back columns (⇧ / ▲ / ▼ / ⇩)",
    "Pořadí můžete měnit tlačítky na úplný začátek (⇧), o jednu pozici výše (▲) / níže (▼), nebo na úplný konec (⇩):": "Reorder using buttons: move to top (⇧), up (▲), down (▼), or bottom (⇩):",
    "Pokročilé nastavení zobrazení sloupců (formátování textu)": "Advanced Column Display Settings (text formatting)",
    "Vizuální náhled kartičky": "Visual Card Preview",
    "Živý náhled v reálném čase": "Live real-time preview",
    "Líc": "Front",
    "Na líci nejsou vybrány žádné sloupce.": "No columns selected for front.",
    "Na rubu nejsou vybrány žádné sloupce.": "No columns selected for back.",
    "Vyberte sloupce na líci nebo rubu pro zobrazení náhledu kartičky.": "Select front or back columns to display card preview.",
    "Vzhled a chování Anki kartičky": "Anki Card Appearance & Behavior",
    "Barevné téma kartičky:": "Card color theme:",
    "Barevný režim karet:": "Card color mode:",
    "Obojetný (automaticky přepínatelný)": "Adaptive (auto light/dark)",
    "Světlý režim (vždy světlé)": "Light mode (always light)",
    "Tmavý režim (vždy tmavé)": "Dark mode (always dark)",
    "Zobrazení po kliknutí na odpověď:": "Display after clicking Answer:",
    "Pod sebe (líc + rub)": "Stacked (front + back)",
    "Na druhou stranu (pouze rub)": "Back side only",
    "Zobrazovat autory a licence (CC) u fotografií a nahrávek": "Show authors and CC licenses on photos and audio",
    "Režim zkoušení v Anki (Typ kartiček)": "Anki Study Mode (Card Type)",
    "Způsob testování:": "Testing mode:",
    "Standardní (otočení kliknutím)": "Standard (click to flip)",
    "Vepisovací (psaní z klávesnice)": "Type-in (keyboard input)",
    "Pole, které má uživatel vepsat z klávesnice:": "Field for user to type in:",
    "Anki zobrazí na líci textové pole. Po stisku Enter automaticky písmeno po písmenu zkontroluje pravopis (zeleně správná písmena, červeně překlepy a chyby).": "Anki displays a text box on the front. Pressing Enter checks spelling letter-by-letter.",
    "Nastavení a export balíčku Anki": "Anki Deck Settings & Export",
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
    "Přidat štítky (tags) ke kartičkám podle hodnoty ve sloupci": "Add tags to cards based on column value",
    "Sloupec pro přidělení štítku:": "Column for tag assignment:",
    "Hodnota ve sloupci pro označení (např. 1, u, ucitel):": "Cell value to match (e.g. 1, u, teacher):",
    "Název štítku v Anki (tag):": "Anki tag name:",
    "Vlastní popis balíčku (zobrazí se v Anki pod názvem balíčku):": "Custom deck description (shown in Anki under deck name):",
    "Připojit oficiální citace a licence použitých zdrojů k popisu balíčku": "Attach official citations & licenses of used sources to deck description",
    "Náhled kompletního popisu balíčku pro Anki": "Preview complete Anki deck description",
    "Nápověda: Hláška 'Prosím aktualizujte na nejnovější verzi Anki' nebo použití na iPhone": "Help: 'Please update to the latest Anki' message or iPhone usage",
    "Vynutit nová ID karet v Anki (vytvořit jako nové karty místo aktualizace existujících)": "Force new Anki card IDs (create new cards instead of updating existing)",
    "Současně vygenerovat i balíček pro Obsidian / Karty.html (.zip) se stejným rozvržením": "Also generate Obsidian / Karty.html (.zip) package with the same layout",
    "Generovat balíček pro Anki (.apkg)": "Generate Anki Package (.apkg)",
    "Musíte vybrat alespoň jeden sloupec pro Líc nebo Rub kartičky.": "You must select at least one column for Front or Back.",
    "Připravuji seznam médií ke stažení...": "Preparing media download list...",
    "Sestavuji kartičky...": "Building cards...",
    "Zapisuji balíček Anki (.apkg)...": "Writing Anki package (.apkg)...",
    "Balíček Anki byl úspěšně vygenerován.": "Anki package generated successfully.",
    "Balíčky pro Anki (.apkg) i Obsidian (.zip) byly úspěšně vygenerovány!": "Both Anki (.apkg) and Obsidian (.zip) packages generated successfully!",
    "Balíčky pro Obsidian (.zip) i Anki (.apkg) byly úspěšně vygenerovány!": "Both Obsidian (.zip) and Anki (.apkg) packages generated successfully!",

    # Obsidian Tab
    "Export kartiček (.zip) – Webový přehrávač & Obsidian (Zdarma pro iPhone, iPad i PC)": "Card Export (.zip) – Web Player & Obsidian (Free for iPhone, iPad & PC)",
    "Překlopit rozvržení z Anki (Líc, Rub i formátování)": "Copy layout from Anki (Front, Back & formatting)",
    "Rozvržení líce, rubu a formátování bylo překlopeno z Anki do Obsidianu.": "Front, back & formatting layout copied from Anki to Obsidian.",
    "Název složky / balíčku v Obsidianu:": "Obsidian folder / package name:",
    "Režim kartiček pro Spaced Repetition:": "Spaced Repetition card mode:",
    "Jednosměrné (?) - líc na rub (Doporučeno)": "One-way (?) - front to back (Recommended)",
    "Obousměrné (??) - líc na rub i rub na líc": "Bidirectional (??) - front to back & back to front",
    "1. Otázka / Líc kartičky": "1. Card Front / Question",
    "2. Odpověď / Rub kartičky": "2. Card Back / Answer",
    "Sloupce zobrazené před otočením (např. foto):": "Columns shown before flip (e.g. photo):",
    "Sloupce zobrazené po otočení (jméno, popis):": "Columns shown after flip (name, description):",
    "Pokročilé nastavení zobrazení sloupců (formátování textu v Obsidianu)": "Advanced Column Display Settings (Obsidian formatting)",
    "Připojit návod pro iPhone (00_NAVOD_JAK_POUZIVAT.md)": "Include iPhone guide (00_NAVOD_JAK_POUZIVAT.md)",
    "Vytvořit hlavní rejstřík (00_Atlas_a_Prehled.md)": "Create main index (00_Atlas_a_Prehled.md)",
    "Dvě možnosti použití zdarma (Obsidian & Karty.html)": "Two free ways to use (Obsidian & Karty.html)",
    "Současně vygenerovat i balíček pro Anki (.apkg) se stejným rozvržením": "Also generate Anki (.apkg) package with the same layout",
    "Generovat balíček pro Obsidian (.zip)": "Generate Obsidian Package (.zip)",
    "Musíte vybrat alespoň jeden sloupec pro otázku (líc) nebo odpověď (rub).": "You must select at least one column for front or back.",
    "Připravuji seznam médií pro Obsidian...": "Preparing Obsidian media list...",
    "Balíček pro Obsidian byl úspěšně vygenerován.": "Obsidian package generated successfully.",
    "Balíček pro Obsidian (.zip) byl úspěšně vytvořen a je připraven ke stažení!": "Obsidian package (.zip) created and ready to download!",

    # PDF & DOCX Tabs
    "Nastavení exportu studijní brožury (PDF)": "Study Booklet Export Settings (PDF)",
    "Obsah a sloupce brožury": "Booklet Content & Columns",
    "Výběr a pořadí sloupců pro tisk do PDF:": "Select and order columns for PDF:",
    "Sloupce do PDF brožury:": "Columns for PDF booklet:",
    "Vyberte sloupce z tabulky a upravte jejich pořadí v brožuře.": "Select table columns and arrange their order in the booklet.",
    "Formátování sloupců v PDF (tabulka vs. samostatný text, tučně, kurzíva)": "PDF Column Formatting (table vs. paragraph, bold, italic)",
    "Nastavte, zda se má sloupec vložit do přehledové tabulky vlastností nebo jako samostatný odstavec textu, a upravte styl písma či popisek.": "Configure whether each column goes into the properties table or as a standalone paragraph, and adjust font style or label.",
    "Záhlaví a texty": "Header & Texts",
    "Název brožury / atlasu:": "Booklet / Atlas Title:",
    "Podtitul / doplňující text v záhlaví brožury:": "Subtitle / header note:",
    "Sloupec pro názvy položek v PDF:": "Column for item titles in PDF:",
    "Zobrazit původní název z 1. sloupce v závorce": "Show original name from 1st column in parentheses",
    "Vzhled a rozvržení": "Appearance & Layout",
    "Vzhled a rozvržení tisku": "Print Appearance & Layout",
    "Nastavení formátu stránek, vazby a velikosti médií.": "Page size, binding, and media size settings.",
    "Formát rozvržení stránek:": "Page layout format:",
    "Kompaktní brožurka (více druhů za sebou)": "Compact booklet (multiple species per page)",
    "Kompaktní (Plynulý text za sebou)": "Compact (continuous flow)",
    "1 druh na stránku (Atlasový list / Kartotéka)": "1 species per page (Atlas sheet / Card)",
    "1 druh na stránku (Konec stránky za každým druhem / Kartotéka)": "1 species per page (page break after each species)",
    "Dvojstrana pro taxon (1 strana obrázky, protilehlá strana popis)": "2-page spread per taxon (1 page images, 1 page text)",
    "Formát stránky:": "Page size:",
    "A4 (Standardní)": "A4 (Standard)",
    "A5 (Kompaktní sešit)": "A5 (Compact booklet)",
    "Typ tisku a vazba:": "Print type & binding:",
    "Standardní": "Standard",
    "Standardní (postupné stránky pro čtení)": "Standard (sequential reading pages)",
    "Sešitová vazba (Brožura / Booklet – tiskový arch pro přeložení napůl)": "Saddle-stitch booklet (print imposition for folding in half)",
    "Knižní vazba po složkách (6 listů / 24 stran na složku)": "Book signatures (6 sheets / 24 pages per signature)",
    "Knižní vazba po složkách (8 listů / 32 stran na složku)": "Book signatures (8 sheets / 32 pages per signature)",
    "Velikost textu (%):": "Text size (%):",
    "Velikost fotografií (%):": "Photo size (%):",
    "Okraje stránky:": "Page margins:",
    "Úzké (více místa pro fotky)": "Narrow (more room for photos)",
    "Širší (knižní)": "Wide (book margins)",
    "Rozložení fotek:": "Photo grid layout:",
    "Automaticky (natěsno)": "Automatic (compact)",
    "2 sloupce (velké fotky vedle sebe)": "2 columns (large photos side-by-side)",
    "3 sloupce (kompaktní řada)": "3 columns (compact row)",
    "Umístění mapy rozšíření:": "Distribution map placement:",
    "Pod tabulkou vlastností (doporučeno)": "Below properties table (recommended)",
    "V horní galerii s fotkami": "In top photo gallery",
    "V galerii mezi fotografiemi": "Inside photo gallery",
    "Počet fotografií a map na druh:": "Photos and maps per species:",
    "Počet fotografií na druh:": "Photos per species:",
    "Pouze 1 (hlavní foto / mapa)": "Only 1 (main photo / map)",
    "Až 2": "Up to 2",
    "Až 2 (dominantní velká zobrazení)": "Up to 2 (large dominant views)",
    "Až 4": "Up to 4",
    "Až 4 (doporučeno: 2 fotky + 2 mapy)": "Up to 4 (recommended: 2 photos + 2 maps)",
    "Až 4 (klasická mřížka 2×2 s předností map)": "Up to 4 (classic 2×2 grid prioritizing maps)",
    "Až 6": "Up to 6",
    "Až 6 (doporučeno: 4 fotky + 2 mapy)": "Up to 6 (recommended: 4 photos + 2 maps)",
    "Doplňkové prvky": "Additional Elements",
    "Vložit na začátek obsah / rejstřík položek": "Insert table of contents / index at start",
    "Rozvržení obsahu (TOC):": "Table of contents (TOC) layout:",
    "Generovat QR kódy pro webové odkazy a audio": "Generate QR codes for web links and audio",
    "Automaticky připojit závěrečnou bibliografii": "Automatically attach final bibliography",
    "Generovat PDF brožuru": "Generate PDF Booklet",
    "Generovat celou PDF brožuru (.pdf)": "Generate Full PDF Booklet (.pdf)",
    "Studijní brožura v PDF byla úspěšně vygenerována.": "PDF study booklet generated successfully.",
    "PDF brožura je připravena ke stažení a tisku.": "PDF booklet is ready to download and print.",
    "Interaktivní náhled PDF (1. položka)": "Interactive PDF Preview (1st item)",
    "Rychlý náhled 1. položky (PDF)": "Quick Preview 1st Item (PDF)",
    "Rychlý náhled 1. položky v PDF byl úspěšně vygenerován.": "Quick preview of 1st item in PDF generated successfully.",
    "Zavřít náhled": "Close preview",
    "Musíte vybrat alespoň jeden sloupec v Kroku 3 (Mapování stran).": "You must select at least one column in Step 3.",
    "Vyberte sloupce z tabulky pro export do formátu Word (.docx).": "Select table columns to export to Word (.docx).",
    "Název dokumentu:": "Document title:",
    "Podtitul / doplňující text v záhlaví dokumentu:": "Subtitle / header note:",
    "Sloupec pro názvy položek ve Wordu:": "Column for item titles in Word:",
    "Vytvoří plně editovatelný dokument Word se zachováním stylů.": "Creates a fully editable Word document preserving styles.",
    "Rozvržení položek:": "Item layout:",
    "Rozvržení a export": "Layout & Export",
    "Připravuji podklady a stahuji fotografie pro dokument Word...": "Preparing assets and downloading photos for Word document...",
    "Dokument Microsoft Word (.docx) byl úspěšně vygenerován.": "Microsoft Word document (.docx) generated successfully.",
    "Dokument Word (.docx) je připraven k úpravám a tisku.": "Word document (.docx) is ready for editing and printing.",

    # Citations, Downloads, Tools & Manuals
    "Vybrat vše": "Select all",
    "Dle sloupců (auto)": "By columns (auto)",
    "Zrušit vše": "Clear all",
    "Uvést tyto zdroje a citace v závěrečném přehledu:": "Include these sources and citations in bibliography:",
    "Můžete ručně naklikat nebo upravit zdroje, které se mají uvést na konci výstupu (ideální např. při nahrání tabulky, která byla obohacena dříve):": "Manually select or adjust sources to include in the bibliography:",
    "Stáhnout .apkg balíček pro Anki": "Download Anki Package (.apkg)",
    "Stáhnout balíček kartiček (.zip – obsahuje i index.html přehrávač)": "Download Card Package (.zip – includes index.html player)",
    "Balíček kartiček (.zip) je připraven. Můžete jej otevřít rovnou poklepáním na index.html uvnitř, nebo naimportovat do přehrávače či Obsidianu.": "Card package (.zip) is ready. Double-click index.html inside or import into Obsidian.",
    "⬇Stáhnout samostatný přehrávač (Karty.html)": "⬇ Download Standalone Player (Karty.html)",
    "Samostatný webový přehrávač (Karty.html) funguje plně offline a umožňuje pohodlné procvičování na libovolném zařízení.": "Standalone web player (Karty.html) works completely offline on any device.",
    "Stáhnout studijní brožuru (.pdf)": "Download Study Booklet (.pdf)",
    "Stáhnout dokument Word (.docx)": "Download Word Document (.docx)",
    "Stáhnout seznam nenalezených položek (.csv)": "Download unfound items list (.csv)",
    "Některé položky nebyly při obohacení nalezeny.": "Some items were not found during enrichment.",
    "Všechny položky byly úspěšně zpracovány.": "All items were processed successfully.",
    "Log chyb stahování": "Download Error Log",
    "Samostatný přehrávač kartiček (Karty.html)": "Standalone Card Player (Karty.html)",
    "Batch Replacer (Čištění a úprava tabulek)": "Batch Replacer (Table Cleaning & Editing)",
    "*(Jednosouborová HTML aplikace bez nutnosti instalace).*": "*(Single-file HTML app, no installation required).*",
    "*(Poznámka: Tento přehrávač je také automaticky přibalen uvnitř každého vygenerovaného .zip balíčku jako index.html).*": "*(Note: This player is also bundled inside every generated .zip package as index.html).*",
    "Kompletní uživatelské příručky v PDF ke stažení": "Complete PDF User Manuals for Download",
    "Všechny příručky jsou zpracovány s plnou podporou české diakritiky, obsahují přehledné kapitoly, postupy a doporučení.": "All manuals include step-by-step chapters, workflows, and tips.",
    "Rychlé tipy pro efektivní studium a řešení potíží": "Quick Tips for Effective Study & Troubleshooting",
    "1. Jak efektivně studovat poznávačky": "1. How to Study Species Effectively",
    "2. Bezplatné používání na iPhone / iPad": "2. Free Usage on iPhone / iPad",
    "3. Řešení hlášky 'Prosím aktualizujte na nejnovější verzi Anki'": "3. Fixing 'Please update to the latest Anki version'",
    "4. Párování sloupců při slučování s novou tabulkou": "4. Column Mapping When Merging a New Table",
    "**Webový přehrávač (Karty.html)** slouží pro rychlé, bezpečné a pohodlné offline procvičování přímo ve webovém prohlížeči (na PC, mobilu i tabletu).": "**Web Player (Karty.html)** lets you practice offline directly in your browser on PC, phone, or tablet.",

    # Column style controls
    "Tučné": "Bold",
    "Kurzíva": "Italic",
    "Velikost písma:": "Font size:",
    "Vlastní název pole:": "Custom field label:",
    "Vlastní popisek:": "Custom label:",
    "Zobrazení:": "Display:",
    "Styl textu:": "Text style:",
    "Zobrazit název pole:": "Show field label:",
    "Zobrazit název pole": "Show field label",
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
    (re.compile(r'^Aktivní moduly \((\d+)\):\s*(.+)$'), r'Active modules (\1): \2'),
    (re.compile(r'^Sloupec s vědeckým jménem (.+)$'), r'Column with scientific name (\1)'),
    (re.compile(r'^Sloupec se jménem (.+)$'), r'Column with name (\1)'),
    (re.compile(r'^Max fotek z (.+?) na řádek$'), r'Max \1 photos per row'),
    (re.compile(r'^Stahuji a optimalizuji média \((\d+)/(\d+)\)\.\.\.$'), r'Downloading and optimizing media (\1/\2)...'),
    (re.compile(r'^Stahuji multimediální soubory pro Obsidian \((\d+)/(\d+)\)\.\.\.$'), r'Downloading Obsidian media files (\1/\2)...'),
    (re.compile(r'^(\w+) \((\d+) položek\)$'), r'\1 (\2 items)'),
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

    # Strip leading markdown heading hashes (### , #### , ##### , ###### )
    m_hdr = re.match(r'^(#{1,6}\s+)(.+)$', stripped)
    if m_hdr:
        prefix, body = m_hdr.group(1), m_hdr.group(2).strip()
        if body in CZ_TO_EN:
            return prefix + CZ_TO_EN[body]

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
