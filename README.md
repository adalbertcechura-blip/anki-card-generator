# 🌿 Generátor kartiček Anki & Vzdělávacích tiskových brožur

Komplexní webová aplikace v Pythonu (Streamlit) pro biology, učitele, studenty a přírodovědce. Umožňuje z pouhého seznamu taxonů automaticky dotáhnout ověřené vědecké fotografie, morfologické popisy, českou taxonomii, mapy rozšíření, ekologické nároky, nahrávky hlasů ptáků a interaktivní QR kódy – a následně vygenerovat **balíček pro Anki (`.apkg`)** s multimédii nebo **tiskovou brožuru v PDF** (včetně knižní/sešitové vazby pro oboustranný tisk).

---

## 🚀 Rychlé spuštění

### 1. Spuštění ve Windows (nejjednodušší)
Pokud máte stažený repozitář na počítači s Windows, stačí poklepat na:
```bat
Spustit.bat
```
Skript automaticky aktivuje virtuální prostředí (`venv`), zkontroluje závislosti a spustí aplikaci v prohlížeči.

### 2. Manuální spuštění přes terminál
```powershell
# 1. Klonování repozitáře
git clone https://github.com/vase-jmeno/anki-card-generator.git
cd anki-card-generator

# 2. Vytvoření a aktivace virtuálního prostředí
python -m venv venv
.\venv\Scripts\activate   # Na Linuxu/macOS: source venv/bin/activate

# 3. Instalace závislostí
pip install -r requirements.txt

# 4. Spuštění aplikace
streamlit run app.py
```

Aplikace se otevře na adrese `http://localhost:8501`.

---

## 📖 Průvodce aplikací (3 jednoduché kroky)

```
┌─────────────────────────┐     ┌─────────────────────────┐     ┌─────────────────────────┐
│         KROK 1          │     │         KROK 2          │     │         KROK 3          │
│   Vstup & Vyčištění     │ ──> │    Obohacení přes API   │ ──> │   Náhled, Anki & PDF    │
│  (Nahrání, deduplikace) │     │ (Pladias, GBIF, fotky)  │     │  (Export .apkg & tisk)  │
└─────────────────────────┘     └─────────────────────────┘     └─────────────────────────┘
```

### 1. Krok: Vstup dat & Příprava taxonů
* **Nahrání souborů:** Podporuje `.xlsx`, `.csv` i čisté textové seznamy `.txt`. Lze nahrát **více souborů najednou** (automaticky se spojí).
* **Ruční vložení:** Můžete vložit seznam taxonů do textového pole a zvolit buď *Načíst jako nový seznam*, nebo *Přidat k existující tabulce*.
* **Automatická deduplikace:** Aplikace při načtení automaticky odstraní duplicity a informuje o počtu vyčištěných řádků. K dispozici je i tlačítko `🧹 Odstranit duplicity`.
* **Smazání konkrétního taxonu:** Přímo v tabulce můžete vybrat a jedním kliknutím odstranit nechtěný řádek.
* **🎯 Převést na druhovou úroveň:** Odstraní označení poddruhů a variet (`subsp.`, `var.`, `agg.`, `f.`) pro lepší dohledatelnost v mezinárodních databázích a automaticky sloučí vzniklé duplicity.
* **Sjednocení nomenklatury:** Vestavěný převodník synonym (např. *Danihelka 2012* vs. *Klíč 2019*).
* **Vlastní fotografie:** Možnost nahrát vlastní fotografie z terénu/mikroskopu k jednotlivým taxonům s náhledovou minigalerií a správou snímků.

---

### 2. Krok: Automatické obohacení dat
Aplikace integruje specializované moduly rozdělené do přehledných záložek:

| Skupina | Podporované databáze a zdroje dat |
|---|---|
| **🌿 Botanika** | **Pladias.cz** (oficiální REST API: filtrování fotografií podle orgánů a částí rostliny – habitus, květ, plod/semeno, list, stonek, kmen/borka, herbářové položky a Clo-Pla skeny; mapy rozšíření v ČR, profil taxonu)<br>**Pladias Taxonomie** (česká školní taxonomie: čeleď, řád, třída dle Klíče ke květeně ČR)<br>**GBIF Rostliny** (makrofotografie květu, listu a herbářových položek s licencí CC) |
| **🍃 Mechorosty** | **GBIF Bryophytes**, **BryophytePortal**, mikrofotografie a popisy sporofytu/gametofytu |
| **🍄 Houby** | **Mykologie.net** (české popisy a fotografie plodnic), **GBIF Fungi** |
| **🪨 Lišejníky** | **DaLiBor** (databáze lišejníků ČR – popisy stélek, substrát, chemismus, fotky) |
| **🔬 Řasy & Rozsivky** | **DiatomBase**, **AlgaeBase** (odborné profily a taxonomie řas) |
| **🐦 Zoologie** | **GBIF Zoologie** (fotografie živočichů), **Xeno-canto** (nahrávky zpěvu a hlasů ptáků) |
| **📋 Registry ČR** | **Klíč ke květeně ČR (2019)** (česká jména a autorské citace)<br>**Červený seznam ČR** (kategorie ohrožení CR, EN, VU...)<br>**Katalog nepůvodních druhů** (invazní status: archeofyt, neofyt)<br>**Biotopy ČR** & **Ellenbergovy indikační hodnoty** (světlo, vlhkost, půda...) |
| **🗣️ Jazyky & Zeměpis** | **Google TTS** (hlasová výslovnost v latině i moderních jazycích), **Český fonetický přepis latiny**, **Anglický výkladový slovník**, **Státy světa** (vlajky, měny, hlavní města) |

---

### 3. Krok: Mapování kartiček, Náhled & Export

#### A. Export do Anki (`.apkg`)
* **Vizuální designér:** Vyberte, které sloupce se mají zobrazit na **líci** a na **rubu** karty.
* **Přizpůsobení stylů:** U textových polí lze nastavit tučné písmo, kurzívu i velikost.
* **Živý náhled v reálném čase:** Interaktivní náhled lícové i rubové strany přesně tak, jak bude vypadat v Anki.
* **Generování `.apkg` balíčku:** Všechny obrázky a MP3 nahrávky jsou uloženy přímo do balíčku – funguje offline v Anki na počítači, mobilu (AnkiDroid / AnkiMobile) i webu.

#### B. Generátor tiskových brožur v PDF
* **Formáty:** A4 i A5 (karta druhu / souvislý text).
* **Knižní a sešitová vazba:** Pokročilá archová montáž (impozice stránek) pro oboustranný tisk složek po 4, 6 nebo 8 listech. Po vytištění stačí listy přeložit uprostřed a sešít.
* **Interaktivní QR kódy:** Automaticky generované velké QR kódy pro okamžitý poslech hlasů ptáků nebo otevření herbářových položek přímo z papíru pomocí mobilu.
* **Kompletní bibliografie:** Automatické generování citací všech použitých databází (Pladias, Červený seznam, Xeno-canto...).

---

## 🛠️ Požadavky na systém
* Python 3.9 nebo novější
* Doporučené knihovny: `streamlit`, `pandas`, `openpyxl`, `genanki`, `reportlab`, `pypdf`, `pillow`, `beautifulsoup4`, `requests`, `qrcode`

---

## 📜 Citace a poděkování
Tento generátor využívá otevřená vědecká data a děkuje autorům a správcům databází:
* **Pladias** – Databáze české flóry a vegetace (*Botanický ústav AV ČR*, Chytrý et al. 2021)
* **Klíč ke květeně České republiky** (Kaplan, Danihelka et al. 2019)
* **Katalog nepůvodních druhů rostlin ČR** (Pyšek et al. 2022)
* **DaLiBor** – Databáze lišejníků ČR (*Botanický ústav AV ČR*)
* **GBIF** – Global Biodiversity Information Facility
* **Xeno-canto Foundation** – Zvukové nahrávky ptáků světa
* **Plants of the World Online (POWO)** – Royal Botanic Gardens, Kew
* **Animal Diversity Web (ADW)** – University of Michigan Museum of Zoology
