# -*- coding: utf-8 -*-
"""Curated Duolingo-style language courses (EN C1, DE B1, FR A2-B1) for Karty Pro."""

import json


def get_lang_courses_json():
    courses = {
        "en": {
            "id": "course_en_c1",
            "lang": "en",
            "ttsLang": "en-GB",
            "label": "🇬🇧 EN · C1",
            "title": "Angličtina · C1 Pokročilá",
            "accentClass": "course-en",
            "topics": [
                {
                    "id": "en_t1",
                    "name": "Inverze a důraz (C1)",
                    "ruleTitle": "Inverze po záporných výrazech",
                    "ruleHtml": """
                      <p>Když věta v pokročilé angličtině začíná záporným nebo omezujícím příslovcem (<em>Never, Seldom, Rarely, Not only, Little, No sooner</em>), mění se slovosled na tázací: <strong>pomocné sloveso + podmět + sloveso</strong>.</p>
                      <table style="width:100%; border-collapse:collapse; margin-top:8px; font-size:0.86rem;">
                        <tr><th style="text-align:left; border-bottom:1px solid var(--border-color); padding:4px;">Běžně</th><th style="text-align:left; border-bottom:1px solid var(--border-color); padding:4px;">S inverzí (C1)</th></tr>
                        <tr><td style="padding:4px;">I have never seen it.</td><td style="padding:4px;"><strong>Never have I</strong> seen it.</td></tr>
                        <tr><td style="padding:4px;">She didn't know.</td><td style="padding:4px;"><strong>Little did she</strong> know.</td></tr>
                        <tr><td style="padding:4px;">He not only won...</td><td style="padding:4px;"><strong>Not only did he</strong> win...</td></tr>
                      </table>""",
                    "cards": [
                        {"id": "enc1_1", "q": "Nikdy jsem neviděl tak dechberoucí výhled.", "a": "Never have I seen such a breathtaking view.", "note": "Po 'Never' na začátku věty následuje inverze: have + I + seen.", "cloze": "[Never] [have] I seen such a breathtaking view."},
                        {"id": "enc1_2", "q": "Netušila, co ji druhý den čeká.", "a": "Little did she know what awaited her the next day.", "note": "Po 'Little' v záporném smyslu použijeme 'did she know'.", "cloze": "[Little] [did] she know what awaited her the next day."},
                        {"id": "enc1_3", "q": "Nejenže vyhrál závod, ale také překonal rekord.", "a": "Not only did he win the race, but he also broke the record.", "note": "Not only + pomocné sloveso (did) + podmět + holý infinitiv.", "cloze": "Not only [did] he [win] the race, but he also broke the record."},
                        {"id": "enc1_4", "q": "Zřídkakdy jsme svědky takové štědrosti.", "a": "Seldom do we witness such generosity.", "note": "Seldom na začátku věty vyžaduje inverzi (do we witness).", "cloze": "[Seldom] [do] we witness such generosity."},
                        {"id": "enc1_5", "q": "Jen co jsme dorazili, začalo hustě pršet.", "a": "No sooner had we arrived than it started pouring.", "note": "Vazba: No sooner + had + podmět + V3 + than.", "cloze": "No sooner [had] we arrived [than] it started pouring."},
                        {"id": "enc1_6", "q": "Teprve později jsem si uvědomil svou chybu.", "a": "Only later did I realize my mistake.", "note": "Po 'Only later / Only then' následuje inverze.", "cloze": "Only later [did] I [realize] my mistake."},
                        {"id": "enc1_7", "q": "Za žádných okolností nesmíte tuto smlouvu podepsat.", "a": "Under no circumstances must you sign this contract.", "note": "Under no circumstances + modální sloveso + podmět.", "cloze": "Under no circumstances [must] you [sign] this contract."},
                        {"id": "enc1_8", "q": "Málokdy byl tým tak dobře připravený.", "a": "Rarely has the team been so well prepared.", "note": "Rarely + has + the team + been.", "cloze": "[Rarely] [has] the team been so well prepared."},
                        {"id": "enc1_9", "q": "Sotva jsem odešel z domu, zazvonil telefon.", "a": "Hardly had I left the house when the phone rang.", "note": "Vazba: Hardly + had + podmět + V3 + when.", "cloze": "[Hardly] had I left the house [when] the phone rang."},
                        {"id": "enc1_10", "q": "V žádném případě bych takovou nabídku neodmítl.", "a": "In no way would I turn down such an offer.", "note": "In no way + would + podmět + sloveso.", "cloze": "In no way [would] I [turn] down such an offer."}
                    ]
                },
                {
                    "id": "en_t2",
                    "name": "Idiomy v byznysu a praxi",
                    "ruleTitle": "C1 Idiomy a kolokace v kontextu",
                    "ruleHtml": """
                      <p>Na úrovni C1 nestačí znát význam slov – důležité jsou ustálené obraty a kolokace:</p>
                      <ul style="padding-left:18px; margin-top:6px; line-height:1.55;">
                        <li><strong>cut corners</strong> = odbývat práci / šidit kvalitu</li>
                        <li><strong>bite the bullet</strong> = zatnout zuby a udělat něco nepříjemného</li>
                        <li><strong>get the ball rolling</strong> = rozhýbat věci / začít</li>
                        <li><strong>on the same page</strong> = mít stejné pochopení / být zajedno</li>
                        <li><strong>play it by ear</strong> = improvizovat podle situace</li>
                      </ul>""",
                    "cards": [
                        {"id": "enc2_1", "q": "Pokud jde o bezpečnost, nikdy bychom neměli šidit kvalitu.", "a": "We should never cut corners when it comes to safety.", "note": "cut corners = odbývat práci, šetřit na úkor kvality.", "cloze": "We should never [cut] [corners] when it comes to safety."},
                        {"id": "enc2_2", "q": "Musím zatnout zuby a konečně zavolat zubaři.", "a": "I have to bite the bullet and finally call the dentist.", "note": "bite the bullet = odhodlat se k něčemu nepříjemnému.", "cloze": "I have to [bite] the [bullet] and finally call the dentist."},
                        {"id": "enc2_3", "q": "Pojďme se ujistit, že jsme před schůzkou všichni zajedno.", "a": "Let us make sure we are all on the same page before the meeting.", "note": "be on the same page = mít společnou shodu.", "cloze": "Let us make sure we are all on the [same] [page] before the meeting."},
                        {"id": "enc2_4", "q": "Zkrátka a dobře, projekt předčil všechna očekávání.", "a": "To put it in a nutshell, the project exceeded all expectations.", "note": "To put it in a nutshell = stručně řečeno.", "cloze": "To put it in a [nutshell], the project [exceeded] all expectations."},
                        {"id": "enc2_5", "q": "Nemáme pevný plán, tak uvidíme podle situace.", "a": "We have no fixed plan, so we will play it by ear.", "note": "play it by ear = improvizovat podle vývoje.", "cloze": "We have no fixed plan, so we will [play] it by [ear]."},
                        {"id": "enc2_6", "q": "Jen si z tebe dělám legraci, neber to vážně.", "a": "I am only pulling your leg, do not take it seriously.", "note": "pull someone's leg = dobírat si někoho.", "cloze": "I am only [pulling] your [leg], do not take it seriously."},
                        {"id": "enc2_7", "q": "Tím jsi trefil hřebíček na hlavičku.", "a": "You really hit the nail on the head with that remark.", "note": "hit the nail on the head = přesně to vystihnout.", "cloze": "You really hit the [nail] on the [head] with that remark."},
                        {"id": "enc2_8", "q": "Bylo to štěstí v neštěstí, že nám uletělo letadlo.", "a": "Missing that flight turned out to be a blessing in disguise.", "note": "a blessing in disguise = zlé pro něco dobré.", "cloze": "Missing that flight turned out to be a [blessing] in [disguise]."},
                        {"id": "enc2_9", "q": "Přestaň chodit kolem horké kaše a řekni mi pravdu.", "a": "Stop beating around the bush and tell me the truth.", "note": "beat around the bush = vyhýbat se přímé odpovědi.", "cloze": "Stop [beating] around the [bush] and tell me the truth."},
                        {"id": "enc2_10", "q": "Ber jeho sliby s velkou rezervou.", "a": "You should take his promises with a pinch of salt.", "note": "with a pinch of salt = s rezervou.", "cloze": "You should take his promises with a [pinch] of [salt]."}
                    ]
                },
                {
                    "id": "en_t3",
                    "name": "Kondicionály a nuance (C1)",
                    "ruleTitle": "Smíšené kondicionály a zdvořilé vazby",
                    "ruleHtml": """
                      <p>Pokročilé podmínkové věty kombinují časy a vynechávají <em>if</em>:</p>
                      <ul style="padding-left:18px; margin-top:6px; line-height:1.55;">
                        <li><strong>Had I known...</strong> = If I had known... (minulost)</li>
                        <li><strong>Were I in your shoes...</strong> = If I were... (přítomnost)</li>
                        <li><strong>Mixed:</strong> If I had taken that job, I <strong>would be</strong> living in London now.</li>
                        <li><strong>Subjunctive:</strong> They insisted that he <strong>be</strong> present.</li>
                      </ul>""",
                    "cards": [
                        {"id": "enc3_1", "q": "Kdybych to byl věděl dřív, jednal bych úplně jinak.", "a": "Had I known earlier, I would have acted completely differently.", "note": "Formální 3. kondicionál bez 'if': Had + podmět + V3.", "cloze": "[Had] I [known] earlier, I would have acted completely differently."},
                        {"id": "enc3_2", "q": "Být na tvém místě, tu nabídku bych okamžitě přijal.", "a": "Were I in your shoes, I would accept the offer immediately.", "note": "Formální 2. kondicionál: Were I...", "cloze": "[Were] I in your shoes, I [would] accept the offer immediately."},
                        {"id": "enc3_3", "q": "Kdybych býval studoval medicínu, byl bych teď lékařem.", "a": "If I had studied medicine, I would be a doctor now.", "note": "Smíšený kondicionál: minulá podmínka + přítomný důsledek.", "cloze": "If I had studied medicine, I [would] [be] a doctor now."},
                        {"id": "enc3_4", "q": "Trvali na tom, aby byl na schůzce přítomen.", "a": "They insisted that he be present at the meeting.", "note": "Subjunctive po insist/suggest/recommend: holý infinitiv (be).", "cloze": "They insisted that he [be] [present] at the meeting."},
                        {"id": "enc3_5", "q": "Už je nejvyšší čas, abychom ten problém vyřešili.", "a": "It is high time we resolved this issue.", "note": "Po 'It is high time + podmět' následuje Past Simple.", "cloze": "It is high time we [resolved] this [issue]."},
                        {"id": "enc3_6", "q": "Kéž bych jí včera neřekl tu poznámku.", "a": "I wish I had not made that remark yesterday.", "note": "Lítost nad minulostí: I wish + Past Perfect.", "cloze": "I wish I [had] not [made] that remark yesterday."},
                        {"id": "enc3_7", "q": "Navzdory nepříznivému počasí jsme dorazili včas.", "a": "Despite the adverse weather, we arrived on time.", "note": "Po Despite nikdy nepíšeme 'of'.", "cloze": "[Despite] the [adverse] weather, we arrived on time."},
                        {"id": "enc3_8", "q": "Mluvíš-li tiše, nikoho neprobudíš.", "a": "Provided that you speak softly, you will wake nobody.", "note": "Provided that = za předpokladu, že.", "cloze": "[Provided] that you speak [softly], you will wake nobody."}
                    ]
                }
            ]
        },
        "de": {
            "id": "course_de_b1",
            "lang": "de",
            "ttsLang": "de-DE",
            "label": "🇩🇪 DE · B1",
            "title": "Němčina · B1 Středně pokročilá",
            "accentClass": "course-de",
            "topics": [
                {
                    "id": "de_t1",
                    "name": "Cestování a doprava (B1)",
                    "ruleTitle": "Vedlejší věty se spojkou weil a dass",
                    "ruleHtml": """
                      <p>Spojky <strong>weil</strong> (protože), <strong>obwohl</strong> (ačkoliv) a <strong>dass</strong> (že) posouvají určité sloveso na <strong>úplný konec věty</strong>.</p>
                      <p style="margin-top:6px;">Rody podstatných jmen v německém režimu jsou barevně odlišené: <span style="color:#60a5fa; font-weight:700;">der (modrá)</span>, <span style="color:#f87171; font-weight:700;">die (červená)</span>, <span style="color:#4ade80; font-weight:700;">das (zelená)</span>.</p>
                      <div style="margin-top:8px; padding:8px; background:var(--bg-main); border-radius:8px; font-size:0.86rem;">
                        Ich bleibe zu Hause, <strong>weil</strong> ich krank <strong>bin</strong>.
                      </div>""",
                    "cards": [
                        {"id": "deb1_1", "q": "Zmeškal jsem přípoj, protože vlak měl zpoždění.", "a": "Ich habe den Anschluss verpasst, weil der Zug Verspätung hatte.", "note": "Spojka 'weil' posouvá určité sloveso (hatte) na úplný konec věty.", "cloze": "Ich habe den Anschluss verpasst, [weil] der Zug Verspätung [hatte]."},
                        {"id": "deb1_2", "q": "Jedu na nádraží vlakem, protože je to rychlejší.", "a": "Ich fahre mit dem Zug zum Bahnhof, weil es schneller ist.", "note": "Po předložce 'mit' je vždy 3. pád (der Zug → mit dem Zug).", "cloze": "Ich fahre [mit] [dem] Zug zum Bahnhof, weil es schneller ist."},
                        {"id": "deb1_3", "q": "Chtěl bych si rezervovat jednolůžkový pokoj na dvě noci.", "a": "Ich möchte ein Einzelzimmer für zwei Nächte reservieren.", "note": "das Zimmer (střední rod) → ein Einzelzimmer; předložka 'für' pojí 4. pád.", "cloze": "Ich möchte [ein] Einzelzimmer [für] zwei Nächte reservieren."},
                        {"id": "deb1_4", "q": "Promiňte, na kterém nástupišti odjíždí vlak do Berlína?", "a": "Entschuldigung, auf welchem Gleis fährt der Zug nach Berlin ab?", "note": "abfahren je odlučitelné sloveso: fährt ... ab.", "cloze": "Entschuldigung, auf welchem Gleis [fährt] der Zug nach Berlin [ab]?"},
                        {"id": "deb1_5", "q": "Ačkoliv silně prší, půjdeme dnes na procházku.", "a": "Obwohl es stark regnet, gehen wir heute spazieren.", "note": "Když věta začíná vedlejší větou (Obwohl...), v hlavní větě následuje sloveso hned po čárce (gehen wir).", "cloze": "[Obwohl] es stark [regnet], gehen wir heute spazieren."},
                        {"id": "deb1_6", "q": "Včera jsem zapomněl pas doma na stole.", "a": "Gestern habe ich den Reisepass zu Hause auf dem Tisch vergessen.", "note": "der Reisepass (4. pád → den Reisepass), der Tisch (3. pád místa → auf dem Tisch).", "cloze": "Gestern habe ich [den] Reisepass zu Hause auf [dem] Tisch vergessen."},
                        {"id": "deb1_7", "q": "Musíme v Praze přestoupit na jiný autobus.", "a": "Wir müssen in Prag in einen anderen Bus umsteigen.", "note": "der Bus (4. pád směru po 'in') → in einen anderen Bus.", "cloze": "Wir müssen in Prag in [einen] anderen Bus [umsteigen]."},
                        {"id": "deb1_8", "q": "Nevím, zda letadlo přistane včas.", "a": "Ich weiß nicht, ob das Flugzeug pünktlich landet.", "note": "Spojka 'ob' (zda) posouvá sloveso (landet) na konec.", "cloze": "Ich weiß nicht, [ob] das Flugzeug pünktlich [landet]."},
                        {"id": "deb1_9", "q": "Kde si mohu koupit zpáteční jízdenku?", "a": "Wo kann ich eine Rückfahrkarte kaufen?", "note": "die Karte (ženský rod) → eine Rückfahrkarte.", "cloze": "Wo kann ich [eine] Rückfahrkarte [kaufen]?"},
                        {"id": "deb1_10", "q": "Zavazadlo bylo příliš těžké, proto jsem musel připlatit.", "a": "Das Gepäck war zu schwer, deshalb musste ich nachzahlen.", "note": "Po 'deshalb' následuje ihned sloveso (musste ich).", "cloze": "Das Gepäck war zu schwer, [deshalb] [musste] ich nachzahlen."}
                    ]
                },
                {
                    "id": "de_t2",
                    "name": "Rody a předložky (B1)",
                    "ruleTitle": "Předložky se 3. a 4. pádem + rody",
                    "ruleHtml": """
                      <p>Zapamatuj si základní rozdělení předložek:</p>
                      <ul style="padding-left:18px; margin-top:6px; line-height:1.55;">
                        <li><strong>Vždy 3. pád (Dativ):</strong> <em>mit, nach, bei, seit, von, zu, aus</em></li>
                        <li><strong>Vždy 4. pád (Akkusativ):</strong> <em>für, ohne, gegen, durch, um</em></li>
                        <li><strong>Podle otázky (Kde? = 3. pád / Kam? = 4. pád):</strong> <em>in, an, auf, unter, über, neben</em></li>
                      </ul>""",
                    "cards": [
                        {"id": "deb2_1", "q": "Stůl stojí v pokoji vedle okna.", "a": "Der Tisch steht im Zimmer neben dem Fenster.", "note": "Otázka 'Kde?' → 3. pád (das Zimmer → im Zimmer, das Fenster → dem Fenster).", "cloze": "[Der] Tisch steht im Zimmer neben [dem] Fenster."},
                        {"id": "deb2_2", "q": "Dám tu knihu na stůl.", "a": "Ich lege das Buch auf den Tisch.", "note": "Otázka 'Kam?' (pohyb) → 4. pád (der Tisch → auf den Tisch).", "cloze": "Ich lege [das] Buch auf [den] Tisch."},
                        {"id": "deb2_3", "q": "Bydlím v Německu už tři roky.", "a": "Ich wohne schon seit drei Jahren in Deutschland.", "note": "Předložka 'seit' se pojí s 3. pádem a přítomným časem.", "cloze": "Ich wohne schon [seit] drei Jahren [in] Deutschland."},
                        {"id": "deb2_4", "q": "Ten dárek je pro mou sestru.", "a": "Das Geschenk ist für meine Schwester.", "note": "Po 'für' je 4. pád (die Schwester → meine Schwester).", "cloze": "[Das] Geschenk ist [für] meine Schwester."},
                        {"id": "deb2_5", "q": "Bez své bundy nikam nejdu.", "a": "Ohne meine Jacke gehe ich nirgendwohin.", "note": "Po 'ohne' je vždy 4. pád (die Jacke).", "cloze": "[Ohne] meine [Jacke] gehe ich nirgendwohin."},
                        {"id": "deb2_6", "q": "Po práci jdu vždy do kavárny.", "a": "Nach der Arbeit gehe ich immer ins Café.", "note": "die Arbeit → nach der Arbeit (3. pád); ins = in das (4. pád).", "cloze": "[Nach] [der] Arbeit gehe ich immer ins Café."},
                        {"id": "deb2_7", "q": "Kočka spí pod křeslem.", "a": "Die Katze schläft unter dem Sessel.", "note": "der Sessel → unter dem Sessel (3. pád – poloha).", "cloze": "[Die] Katze schläft unter [dem] Sessel."},
                        {"id": "deb2_8", "q": "Mluvil jsem o tom s šéfem.", "a": "Ich habe darüber mit dem Chef gesprochen.", "note": "der Chef → mit dem Chef (3. pád).", "cloze": "Ich habe darüber [mit] [dem] Chef gesprochen."}
                    ]
                },
                {
                    "id": "de_t3",
                    "name": "Konjunktiv II a práce (B1)",
                    "ruleTitle": "Zdvořilost a přání (Konjunktiv II)",
                    "ruleHtml": """
                      <p>Pro zdvořilé žádosti a nesplněná přání používáme <strong>Konjunktiv II</strong>:</p>
                      <ul style="padding-left:18px; margin-top:6px; line-height:1.55;">
                        <li><strong>Ich hätte gern...</strong> = Dal(a) bych si / Rád(a) bych měl(a)...</li>
                        <li><strong>Könnten Sie mir helfen?</strong> = Mohl byste mi pomoci?</li>
                        <li><strong>Ich würde gern...</strong> = Rád bych... (+ infinitiv na konci)</li>
                      </ul>""",
                    "cards": [
                        {"id": "deb3_1", "q": "Mohl byste mi prosím tu větu zopakovat?", "a": "Könnten Sie mir bitte diesen Satz wiederholen?", "note": "Könnten Sie... je zdvořilá prosba.", "cloze": "[Könnten] Sie mir bitte diesen Satz [wiederholen]?"},
                        {"id": "deb3_2", "q": "Rád bych si objednal dvě housky a kávu.", "a": "Ich hätte gern zwei Brötchen und einen Kaffee.", "note": "Ich hätte gern + 4. pád (der Kaffee → einen Kaffee).", "cloze": "Ich [hätte] gern zwei Brötchen und [einen] Kaffee."},
                        {"id": "deb3_3", "q": "Kdybych měl více času, učil bych se každý den.", "a": "Wenn ich mehr Zeit hätte, würde ich jeden Tag lernen.", "note": "Podmínka s Konjunktivem II: hätte ... würde lernen.", "cloze": "Wenn ich mehr Zeit [hätte], [würde] ich jeden Tag lernen."},
                        {"id": "deb3_4", "q": "Doporučuji ti, abys tu příležitost využil.", "a": "Ich empfehle dir, diese Gelegenheit zu nutzen.", "note": "Infinitiv s 'zu' na konci věty (zu nutzen).", "cloze": "Ich empfehle dir, diese [Gelegenheit] [zu] nutzen."},
                        {"id": "deb3_5", "q": "Podle mého názoru je to výborný nápad.", "a": "Meiner Meinung nach ist das eine ausgezeichnete Idee.", "note": "Meiner Meinung nach = podle mého názoru.", "cloze": "[Meiner] Meinung [nach] ist das eine ausgezeichnete Idee."},
                        {"id": "deb3_6", "q": "Musíme si na schůzku připravit prezentaci.", "a": "Wir müssen für die Besprechung eine Präsentation vorbereiten.", "note": "die Besprechung, die Präsentation (ženský rod).", "cloze": "Wir müssen für [die] Besprechung eine Präsentation [vorbereiten]."}
                    ]
                }
            ]
        },
        "fr": {
            "id": "course_fr_a2b1",
            "lang": "fr",
            "ttsLang": "fr-FR",
            "label": "🇫🇷 FR · A2–B1",
            "title": "Francouzština · A2–B1 Střední",
            "accentClass": "course-fr",
            "topics": [
                {
                    "id": "fr_t1",
                    "name": "Kavárna a město (A2–B1)",
                    "ruleTitle": "Zdvořilé objednávání a členy",
                    "ruleHtml": """
                      <p>Ve francouzštině používáme ke zdvořilému přání kondicionál <strong>je voudrais</strong> (chtěl bych) a před podstatnými jmény stojí téměř vždy člen (<em>un, une, le, la, du, de la</em>).</p>
                      <div style="margin-top:8px; padding:8px; background:var(--bg-main); border-radius:8px; font-size:0.86rem;">
                        <strong>Je voudrais</strong> un café et <strong>de l'</strong>eau, s'il vous plaît.
                      </div>""",
                    "cards": [
                        {"id": "fra1_1", "q": "Chtěl bych kávu a sklenici vody, prosím.", "a": "Je voudrais un café et un verre d'eau, s'il vous plaît.", "note": "Vazba množství: un verre d'eau (bez členu po 'de').", "cloze": "Je [voudrais] un café et un verre [d'eau], s'il vous plaît."},
                        {"id": "fra1_2", "q": "Promiňte, kde je nejbližší nádraží?", "a": "Excusez-moi, où se trouve la gare la plus proche ?", "note": "se trouver = nacházet se; la plus proche = nejbližší.", "cloze": "Excusez-moi, où se trouve la [gare] la plus [proche] ?"},
                        {"id": "fra1_3", "q": "Účet, prosím. Mohu platit kartou?", "a": "L'addition, s'il vous plaît. Je peux payer par carte ?", "note": "payer par carte = platit kartou.", "cloze": "[L'addition], s'il vous plaît. Je peux payer par [carte] ?"},
                        {"id": "fra1_4", "q": "Každé ráno kupuji čerstvý chléb v pekařství.", "a": "Chaque matin, j'achète du pain frais à la boulangerie.", "note": "Dělivý člen: du pain (trochu chleba / chléb obecně).", "cloze": "Chaque matin, j'achète [du] pain frais à la [boulangerie]."},
                        {"id": "fra1_5", "q": "Dnes je krásně, půjdeme se projít do parku.", "a": "Aujourd'hui il fait beau, nous allons nous promener au parc.", "note": "au = à + le (do parku / v parku).", "cloze": "[Aujourd'hui] il fait beau, nous allons nous promener [au] parc."},
                        {"id": "fra1_6", "q": "Jdu pěšky, protože metro nejede.", "a": "Je vais à pied parce que le métro ne marche pas.", "note": "à pied (pěšky), en métro / en bus (dopravním prostředkem).", "cloze": "Je vais [à] [pied] parce que le métro ne marche pas."},
                        {"id": "fra1_7", "q": "Kolik stojí zpáteční jízdenka do Lyonu?", "a": "Combien coûte un billet aller-retour pour Lyon ?", "note": "aller-retour = zpáteční.", "cloze": "[Combien] coûte un [billet] aller-retour pour Lyon ?"},
                        {"id": "fra1_8", "q": "Mohl byste prosím mluvit trochu pomaleji?", "a": "Pourriez-vous parler un peu plus lentement, s'il vous plaît ?", "note": "Pourriez-vous = mohl byste (zdvořilý kondicionál).", "cloze": "[Pourriez-vous] parler un peu plus [lentement], s'il vous plaît ?"}
                    ]
                },
                {
                    "id": "fr_t2",
                    "name": "Minulé časy a zájmena y / en",
                    "ruleTitle": "Passé composé vs. Imparfait + y / en",
                    "ruleHtml": """
                      <p><strong>Passé composé</strong> vyjadřuje ukončený děj v minulosti (<em>Hier, je suis allé...</em>). <strong>Imparfait</strong> popisuje stav nebo zvyk (<em>Quand j'étais petit...</em>).</p>
                      <ul style="padding-left:18px; margin-top:6px; line-height:1.55;">
                        <li><strong>y</strong> nahrazuje místo po <em>à / dans / sur</em>: <em>J'y vais.</em> (Jdu tam.)</li>
                        <li><strong>en</strong> nahrazuje množství s <em>de / du / des</em>: <em>J'en veux.</em> (Chci toho.)</li>
                      </ul>""",
                    "cards": [
                        {"id": "fra2_1", "q": "Včera jsem šel s přáteli do kina.", "a": "Hier, je suis allé au cinéma avec des amis.", "note": "Sloveso pohybu 'aller' tvoří passé composé s pomocným 'être'.", "cloze": "Hier, je [suis] [allé] au cinéma avec des amis."},
                        {"id": "fra2_2", "q": "Když jsem byl malý, často jsem si hrál na zahradě.", "a": "Quand j'étais petit, je jouais souvent dans le jardin.", "note": "Opakovaný zvyk a stav v minulosti = imparfait (étais, jouais).", "cloze": "Quand j'[étais] petit, je [jouais] souvent dans le jardin."},
                        {"id": "fra2_3", "q": "Jedeš do Paříže? – Ano, jedu tam zítra.", "a": "Tu vas à Paris ? Oui, j'y vais demain.", "note": "Zájmeno 'y' stojí před slovesem a nahrazuje 'à Paris'.", "cloze": "Tu vas à Paris ? Oui, j'[y] [vais] demain."},
                        {"id": "fra2_4", "q": "Chceš kávu? – Ano, dám si trochu.", "a": "Tu veux du café ? Oui, j'en veux bien.", "note": "Zájmeno 'en' nahrazuje 'du café'.", "cloze": "Tu veux du café ? Oui, j'[en] [veux] bien."},
                        {"id": "fra2_5", "q": "Bydlím v Praze už dva roky.", "a": "J'habite à Prague depuis deux ans.", "note": "Děj začal v minulosti a stále trvá → depuis + přítomný čas.", "cloze": "J'habite à Prague [depuis] deux [ans]."},
                        {"id": "fra2_6", "q": "Nikdy nezapomenu na tu cestu.", "a": "Je n'oublierai jamais ce voyage.", "note": "Zápor 'ne ... jamais' obklopuje sloveso.", "cloze": "Je [n'oublierai] [jamais] ce voyage."},
                        {"id": "fra2_7", "q": "Navzdory dešti jsme vyšli ven.", "a": "Malgré la pluie, nous sommes sortis.", "note": "sortir tvoří passé composé s être (nous sommes sortis).", "cloze": "[Malgré] la pluie, nous [sommes] sortis."},
                        {"id": "fra2_8", "q": "Musíš být opatrný, když prší.", "a": "Il faut que tu sois prudent quand il pleut.", "note": "Po 'Il faut que' následuje subjonctif (être → sois).", "cloze": "Il faut que tu [sois] [prudent] quand il pleut."}
                    ]
                },
                {
                    "id": "fr_t3",
                    "name": "Názory a konverzace (B1)",
                    "ruleTitle": "Vyjadřování názoru ve francouzštině",
                    "ruleHtml": """
                      <p>Užitečné obraty pro úroveň B1:</p>
                      <ul style="padding-left:18px; margin-top:6px; line-height:1.55;">
                        <li><strong>À mon avis...</strong> = Podle mého názoru...</li>
                        <li><strong>Je pense que...</strong> = Myslím si, že...</li>
                        <li><strong>Cependant / Pourtant</strong> = Nicméně / Přesto</li>
                        <li><strong>Ça ne fait rien.</strong> = To nevadí.</li>
                      </ul>""",
                    "cards": [
                        {"id": "fra3_1", "q": "Podle mého názoru je to výborný nápad.", "a": "À mon avis, c'est une excellente idée.", "note": "À mon avis = podle mého názoru.", "cloze": "À mon [avis], c'est une [excellente] idée."},
                        {"id": "fra3_2", "q": "Co si o tom projektu myslíš?", "a": "Qu'est-ce que tu penses de ce projet ?", "note": "penser de = mít názor na něco.", "cloze": "Qu'est-ce que tu [penses] de ce [projet] ?"},
                        {"id": "fra3_3", "q": "To nevadí, můžeme začít zítra.", "a": "Ça ne fait rien, nous pouvons commencer demain.", "note": "Ça ne fait rien = to nevadí.", "cloze": "Ça ne fait [rien], nous pouvons [commencer] demain."},
                        {"id": "fra3_4", "q": "Je to těžké, nicméně se chci zlepšit.", "a": "C'est difficile, cependant je veux m'améliorer.", "note": "cependant = nicméně, avšak.", "cloze": "C'est difficile, [cependant] je veux [m'améliorer]."},
                        {"id": "fra3_5", "q": "To je škoda, že nemůžeš přijít!", "a": "C'est dommage que tu ne puisses pas venir !", "note": "Po 'C'est dommage que' je subjonctif (puisses).", "cloze": "C'est [dommage] que tu ne [puisses] pas venir !"},
                        {"id": "fra3_6", "q": "Doufám, že se brzy uvidíme.", "a": "J'espère que nous nous verrons bientôt.", "note": "Po 'espérer que' používáme oznamovací způsob (budoucí čas).", "cloze": "J'[espère] que nous nous verrons [bientôt]."}
                    ]
                }
            ]
        }
    }
    return json.dumps(courses, ensure_ascii=False)


def get_lang_glossary_json():
    # Lightweight word-by-word glossary for Tap-to-Peek on example/target sentences
    glossary = {
        # EN
        "never": "nikdy (příslovce)", "have": "mít / pomocné sloveso", "seen": "viděl (V3 od see)",
        "such": "takový (zájmeno)", "breathtaking": "dechberoucí (příd. jm.)", "view": "výhled (podst. jm.)",
        "little": "málo / sotva (příslovce)", "know": "vědět (sloveso)", "awaited": "čekalo (sloveso)",
        "race": "závod (podst. jm.)", "broke": "překonal (min. od break)", "record": "rekord (podst. jm.)",
        "seldom": "zřídkakdy (příslovce)", "witness": "být svědkem (sloveso)", "generosity": "štědrost (podst. jm.)",
        "sooner": "dříve (příslovce)", "arrived": "dorazili (sloveso)", "pouring": "lít jako z konve (sloveso)",
        "realize": "uvědomit si (sloveso)", "mistake": "chyba (podst. jm.)", "circumstances": "okolnosti (podst. jm.)",
        "contract": "smlouva (podst. jm.)", "rarely": "zřídka (příslovce)", "prepared": "připravený (příd. jm.)",
        "hardly": "sotva (příslovce)", "turn": "otočit / odmítnout (sloveso)", "offer": "nabídka (podst. jm.)",
        "cut": "krátit / řezat (sloveso)", "corners": "rohy (cut corners = odbývat)", "safety": "bezpečnost (podst. jm.)",
        "bite": "kousnout (sloveso)", "bullet": "kulka (bite the bullet = zatnout zuby)", "meeting": "schůzka (podst. jm.)",
        "nutshell": "skořápka (in a nutshell = stručně)", "exceeded": "překonal (sloveso)", "expectations": "očekávání (podst. jm.)",
        "fixed": "pevný (příd. jm.)", "ear": "ucho (play it by ear = improvizovat)", "pulling": "tahání (pull leg = dobírat si)",
        "remark": "poznámka (podst. jm.)", "flight": "let (podst. jm.)", "blessing": "požehnání (podst. jm.)",
        "disguise": "přestrojení (podst. jm.)", "bush": "keř (beat around the bush = chodit kolem kaše)", "truth": "pravda (podst. jm.)",
        "promises": "sliby (podst. jm.)", "pinch": "špetka (podst. jm.)", "salt": "sůl (podst. jm.)",
        "known": "věděl (V3 od know)", "earlier": "dříve (příslovce)", "acted": "jednal (sloveso)",
        "differently": "jinak (příslovce)", "shoes": "boty (in your shoes = na tvém místě)", "accept": "přijmout (sloveso)",
        "immediately": "okamžitě (příslovce)", "studied": "studoval (sloveso)", "medicine": "medicína (podst. jm.)",
        "insisted": "trvali na (sloveso)", "present": "přítomen (příd. jm.)", "resolved": "vyřešili (sloveso)",
        "issue": "problém (podst. jm.)", "despite": "navzdory (předložka)", "adverse": "nepříznivý (příd. jm.)",
        "weather": "počasí (podst. jm.)", "provided": "za předpokladu (spojka)", "softly": "tiše (příslovce)",
        # DE
        "ich": "já (zájmeno)", "habe": "mám / pomocné sloveso", "den": "ten (člen 4. pád m.)",
        "anschluss": "přípoj (der, 4. pád)", "verpasst": "zmeškal (sloveso)", "weil": "protože (spojka)",
        "der": "ten (člen m.)", "zug": "vlak (der)", "verspätung": "zpoždění (die)", "hatte": "měl (sloveso)",
        "fahre": "jedu (sloveso)", "mit": "s (předložka + 3. pád)", "dem": "tomu (člen 3. pád)",
        "bahnhof": "nádraží (der)", "schneller": "rychlejší (příd. jm.)", "möchte": "chtěl bych (sloveso)",
        "einzelzimmer": "jednolůžkový pokoj (das)", "zwei": "dva (číslovka)", "nächte": "noci (die, mn. č.)",
        "reservieren": "rezervovat (sloveso)", "entschuldigung": "promiňte (podst. jm.)", "gleis": "nástupiště (das)",
        "fährt": "jede (sloveso)", "obwohl": "ačkoliv (spojka)", "stark": "silně (příslovce)",
        "regnet": "prší (sloveso)", "gehen": "jdeme (sloveso)", "heute": "dnes (příslovce)",
        "spazieren": "procházet se (sloveso)", "gestern": "včera (příslovce)", "reisepass": "cestovní pas (der)",
        "tisch": "stůl (der)", "vergessen": "zapomněl (sloveso)", "müssen": "musíme (sloveso)",
        "umsteigen": "přestoupit (sloveso)", "weiß": "vím (sloveso)", "ob": "zda (spojka)",
        "flugzeug": "letadlo (das)", "pünktlich": "včas (příslovce)", "landet": "přistane (sloveso)",
        "rückfahrkarte": "zpáteční jízdenka (die)", "kaufen": "koupit (sloveso)", "gepäck": "zavazadlo (das)",
        "schwer": "těžké (příd. jm.)", "deshalb": "proto (příslovce)", "nachzahlen": "doplatit (sloveso)",
        "steht": "stojí (sloveso)", "zimmer": "pokoj (das)", "neben": "vedle (předložka)",
        "fenster": "okno (das)", "lege": "položím (sloveso)", "buch": "kniha (das)",
        "wohne": "bydlím (sloveso)", "seit": "od / už (předložka + 3. pád)", "jahren": "let (3. pád)",
        "geschenk": "dárek (das)", "für": "pro (předložka + 4. pád)", "schwester": "sestra (die)",
        "ohne": "bez (předložka + 4. pád)", "jacke": "bunda (die)", "arbeit": "práce (die)",
        "katze": "kočka (die)", "schläft": "spí (sloveso)", "unter": "pod (předložka)",
        "sessel": "křeslo (der)", "darüber": "o tom (příslovce)", "chef": "šéf (der)",
        "gesprochen": "mluvil (sloveso)", "könnten": "mohl byste (Konj. II)", "satz": "věta (der)",
        "wiederholen": "zopakovat (sloveso)", "hätte": "měl bych (Konj. II)", "brötchen": "housky (das)",
        "kaffee": "káva (der)", "zeit": "čas (die)", "würde": "bych (Konj. II)", "lernen": "učit se (sloveso)",
        "empfehle": "doporučuji (sloveso)", "gelegenheit": "příležitost (die)", "nutzen": "využít (sloveso)",
        "meinung": "názor (die)", "ausgezeichnete": "výborná (příd. jm.)", "idee": "nápad (die)",
        "besprechung": "porada (die)", "präsentation": "prezentace (die)", "vorbereiten": "připravit (sloveso)",
        # FR
        "je": "já (zájmeno)", "voudrais": "chtěl bych (kondicionál)", "café": "káva (le)",
        "verre": "sklenice (le)", "eau": "voda (l')", "plaît": "prosím (s'il vous plaît)",
        "excusez": "promiňte (sloveso)", "trouve": "nachází se (sloveso)", "gare": "nádraží (la)",
        "proche": "blízký (příd. jm.)", "addition": "účet (l')", "peux": "mohu (sloveso)",
        "payer": "platit (sloveso)", "carte": "karta (la)", "chaque": "každý (zájmeno)",
        "matin": "ráno (le)", "achète": "kupuji (sloveso)", "pain": "chléb (le)",
        "frais": "čerstvý (příd. jm.)", "boulangerie": "pekařství (la)", "aujourd'hui": "dnes (příslovce)",
        "fait": "dělá / je (počasí)", "beau": "krásně (příd. jm.)", "promener": "procházet se (sloveso)",
        "parc": "park (le)", "pied": "noha (à pied = pěšky)", "métro": "metro (le)",
        "marche": "funguje / jde (sloveso)", "combien": "kolik (příslovce)", "coûte": "stojí (sloveso)",
        "billet": "jízdenka (le)", "pourriez": "mohl byste (kondicionál)", "parler": "mluvit (sloveso)",
        "lentement": "pomalu (příslovce)", "hier": "včera (příslovce)", "suis": "jsem (être)",
        "allé": "šel (min. od aller)", "cinéma": "kino (le)", "avec": "s (předložka)",
        "amis": "přátelé (les)", "quand": "když (spojka)", "étais": "byl jsem (imparfait)",
        "petit": "malý (příd. jm.)", "jouais": "hrál jsem si (imparfait)", "souvent": "často (příslovce)",
        "jardin": "zahrada (le)", "demain": "zítra (příslovce)", "veux": "chci (sloveso)",
        "habite": "bydlím (sloveso)", "depuis": "už / od (předložka)", "ans": "roky (les)",
        "oublierai": "zapomenu (bud. čas)", "jamais": "nikdy (příslovce)", "voyage": "cesta (le)",
        "malgré": "navzdory (předložka)", "pluie": "déšť (la)", "sortis": "vyšli (min. od sortir)",
        "faut": "je třeba (falloir)", "sois": "abys byl (subjonctif)", "prudent": "opatrný (příd. jm.)",
        "pleut": "prší (sloveso)", "avis": "názor (l')", "excellente": "výborná (příd. jm.)",
        "idée": "nápad (l')", "penses": "myslíš (sloveso)", "projet": "projekt (le)",
        "rien": "nic (ça ne fait rien = to nevadí)", "commencer": "začít (sloveso)",
        "difficile": "těžký (příd. jm.)", "cependant": "nicméně (příslovce)", "améliorer": "zlepšit (sloveso)",
        "dommage": "škoda (c'est dommage)", "puisses": "abys mohl (subjonctif)", "venir": "přijít (sloveso)",
        "espère": "doufám (sloveso)", "verrons": "uvidíme se (bud. čas)", "bientôt": "brzy (příslovce)",
    }
    return json.dumps(glossary, ensure_ascii=False)
