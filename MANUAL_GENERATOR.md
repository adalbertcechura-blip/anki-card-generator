# Uživatelská příručka: Generátor kartiček Anki

*Komplexní webový nástroj pro automatizovanou tvorbu multimediálních studijních kartiček z biologických a obecných databází.*

---

## 1. Úvod a přehled aplikace

Generátor kartiček Anki byl vyvinut s cílem maximálně zjednodušit a zrychlit přípravu studijních materiálů pro poznávací zkoušky (poznávačky) z botaniky, zoologie a dalších oborů.

Aplikace funguje v několika přímočarých krocích:
1. **Načtení seznamu druhů** nebo tabulky.
2. **Automatické obohacení** o fotografie, české názvy, hlasy ptáků, taxonomii a popisy z ověřených světových i národních databází (GBIF, iNaturalist, Pladias, Xeno-canto, Wikipedie).
3. **Vizuální návrh kartičky** (výběr obsahu pro líc a rub, rozvržení a barevné téma).
4. **Export hotového balíčku (`.apkg`)** připraveného k okamžitému importu do Anki na počítači i mobilu.

<!-- [ZDE JE MOŽNÉ VLOŽIT OBRÁZEK / SNÍMEK OBRAZOVKY ÚVODNÍHO ROZHRANÍ APLIKACE] -->

---

## 2. Krok 1: Vstup dat a příprava seznamu

Aplikace nabízí dva pohodlné způsoby zadání dat:

### A. Nahrání souboru
- **Excel (`.xlsx`) nebo CSV (`.csv`):** Vhodné, pokud již máte tabulku s více sloupci (např. vědecké jméno, čeleď, poznámky, rozlišení oboru).
- **Textový soubor (`.txt`):** Obyčejný seznam, kde každý řádek představuje jeden druh.

### B. Přímé vložení textu
- Zkopírujte seznam vědeckých jmen z libovolného dokumentu a vložte jej do textového pole. Každý druh uveďte na samostatný řádek.

### Převod na druhovou úroveň
V praxi se v seznamech často objevují poddruhy, variety či agregáty (např. *Taraxacum officinale agg.*, *Pinus mugo subsp. mugo*). Veřejné databáze však fotografie a data nejlépe párují na základní binomické jméno.
- Pomocí tlačítka **„Převést na druhovou úroveň (odstranit subsp., var., agg.)“** aplikace jedním kliknutím očistí vybraný sloupec, což zajistí maximální úspěšnost při dohledávání dat.

<!-- [ZDE JE MOŽNÉ VLOŽIT OBRÁZEK / SNÍMEK OBRAZOVKY KROKU 1 A ČIŠTĚNÍ DAT] -->

---

## 3. Krok 2: Automatické obohacení dat (Moduly)

V tomto kroku můžete aktivovat specializovaná rozšíření:

### 🌿 Botanika
- **GBIF – Květ / List:** Automaticky stáhne kvalitní fotografie konkrétních rostlinných orgánů z mezinárodní databáze *Global Biodiversity Information Facility*.
- **Pladias.cz:** Vygeneruje přímý odkaz do české národní botanické databáze Pladias pro zobrazení podrobných map rozšíření a ekologických nároků.

### 🐦 Zoologie
- **GBIF – Zoologie:** Dohledá fotografie živočichů v přirozeném prostředí.
- **Hlasy ptáků (Xeno-canto):** Vyhledá nahrávky hlasů a zpěvů z největší světové ornitologické zvukové databáze. Nahrávky jsou vloženy přímo do kartičky v podobě přehrávače (umožňuje spuštění, pozastavení i posun).

### 🌍 Všeobecná biologie
- **iNaturalist:** Vyhledá ověřené **české jméno** a komunitní fotografie v terénu.
- **Popis z Wikipedie:** Získá strukturovaný morfologický a biologický popis.
- **Taxonomie (GBIF):** Automaticky doplní vyšší taxonomické kategorie (říše, kmen, třída, řád, čeleď, rod).
- **Wikimedia Commons:** Vyhledávač dodatečných volně šiřitelných fotografií.

*Poznámka:* Pokud některý druh v databázi chybí, aplikace vás po dokončení upozorní a nabídne stažení CSV souboru se seznamem nenalezených položek.

<!-- [ZDE JE MOŽNÉ VLOŽIT OBRÁZEK / SNÍMEK OBRAZOVKY ZÁLOŽEK BOTANIKY A ZOOLOGIE] -->

---

## 4. Krok 3: Návrh a styl kartiček

V této fázi rozhodujete, co přesně bude na přední a zadní straně kartičky:

1. **Líc (Otázka):** Zvolte položky, které se zobrazí jako zadání (např. pouze fotografie, vědecké jméno nebo zvuková nahrávka).
2. **Rub (Odpověď):** Zvolte informace, které se odhalí po otočení kartičky (např. české jméno, čeleď, popis, doplňující fotografie, odkaz na Pladias).
3. **Rozvržení odpovědi:**
   - *Pod sebe (líc + rub):* Po otočení zůstává otázka viditelná a odpověď se zobrazí pod ní.
   - *Na druhou stranu (pouze rub):* Po otočení se zobrazí čistě zadní strana.
4. **Vzhled kartičky:**
   - Výchozí **tmavý biologický styl** (přírodní lesní tóny, šetrný k očím při nočním studiu).
   - Světlý styl nebo automatické přizpůsobení podle nastavení vašeho systému/Anki.

V reálném čase vidíte **živý interaktivní náhled**, který přesně odpovídá tomu, jak bude karta vypadat v Anki.

<!-- [ZDE JE MOŽNÉ VLOŽIT OBRÁZEK / SNÍMEK ŽIVÉHO NÁHLEDU KARTIČKY] -->

---

## 5. Krok 4: Export a rozlišení penza (Štítky)

Před stažením balíčku můžete nastavit organizaci karet:

- **Název balíčku (Deck Name):** Pojmenujte svůj balíček (např. *Botanika – Cévnaté rostliny*).
- **Rozdělení do podbalíčků:** Volitelně můžete karty automaticky roztřídit podle vybraného sloupce (např. podle čeledí).
- **Štítky (Tags) pro učitelské vs. odborné penzum:**
  Pokud vaše tabulka obsahuje sloupec rozlišující náročnost (např. `1` pro učitelské penzum a `0` pro odborné), zaškrtněte možnost *Přidat štítky (tags) ke kartičkám podle hodnoty ve sloupci*.
  Zadejte hodnotu (např. `1` nebo `u`) a název štítku (např. `ucitele`). Všechny odpovídající kartičky budou v Anki označeny tímto štítkem, což studentům umožní snadné filtrování.

Kliknutím na **Generovat balíček (.apkg)** se vytvoří kompletní soubor obsahující všechny karty, šablony, stažené fotografie i zvukové záznamy.

<!-- [ZDE JE MOŽNÉ VLOŽIT OBRÁZEK / SNÍMEK TLAČÍTKA EXPORTU A STAŽENÍ BALÍČKU] -->

---

## 6. Kontakt a podpora

V případě dotazů, námětů na vylepšení nebo nahlášení chyb kontaktujte autora:

- **E-mail:** [adalbert.cechura@gmail.com](mailto:adalbert.cechura@gmail.com)

---

## 7. Právní doložka a zřeknutí se odpovědnosti (Disclaimer)

Tato aplikace slouží jako studijní a organizační pomůcka. Veškerá doplňující data, taxonomické klasifikace, popisy, fotografie a zvukové nahrávky jsou automaticky stahovány prostřednictvím veřejných programových rozhraní (API) externích vědeckých a komunitních databází (GBIF, iNaturalist, Pladias, Xeno-canto, Wikipedie, Wikimedia Commons).

Autor aplikace **nenese žádnou právní ani faktickou odpovědnost** za:
- případnou věcnou, taxonomickou či terminologickou nepřesnost v datech poskytnutých třetími stranami,
- chybné určení druhů na fotografiích pocházejících z komunitních zdrojů,
- případné změny či výpadky v dostupnosti externích služeb a API,
- výsledky zkoušek či studijní hodnocení dosažené s využitím vygenerovaných materiálů.

Uživatelům se doporučuje klíčové taxonomické znaky a studijní penzum před zkouškou ověřit v doporučené studijní literatuře.
