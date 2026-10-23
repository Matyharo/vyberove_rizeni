Proveď finální opravy projektu https://github.com/Matyharo/vyberove_rizeni tak, aby byl konzistentní a připravený k odevzdání praktické úlohy na Junior AI Developer.

Nejdříve přečti aktuální stav repozitáře a jeho pokyny. Níže uvedené problémy ověř proti současnému kódu. Potom rovnou implementuj potřebné opravy, regeneruj výstupy a spusť kontroly. Nestačí pouze navrhnout změny.

## Kontext zadání

Cílem je spolehlivá databáze skutečných investorů. Zadání vyžaduje plán a pravidla zařazení, ověření na menším pilotu, zdroje a data dokládající investiční činnost, ručně změřenou přesnost, odhad globálního rozsahu a nákladů a pravdivý popis práce s AI.

Zachovej současný rozsah projektu. Nepřidávej frontend, rozsáhlý crawler ani placené API.

## 1. Sjednoť rozhodnutí AI a lidskou kontrolu

Prověř zejména `reports/PILOT.md`, `data/pilot.json`, `review/labels.csv`, exporty a generátor v `investor_db/core.py`.

- Odstraň zastaralá tvrzení, že dokončená ruční kontrola stále čeká na člověka.
- V přehledu jasně rozliš původní predikci AI, aktuální rozhodnutí AI a lidské referenční rozhodnutí.
- U Lighthouse vysvětli rozdíl mezi nevyřešenou identitou podle AI a lidským vyloučením původního discovery kandidáta. Nezaměňuj jej automaticky s českým fondem stejného názvu.
- Jednoznačně definuj, podle jakého rozhodnutí se investor dostává do finálního publikovaného přehledu. Nevyřešené případy nesmějí působit jako ověření investoři.
- Oprav generátor i zdrojová data tam, kde je to potřeba. Ruční oprava vygenerovaného Markdownu nestačí.

Neměň zmrazené kandidáty ani původní predikce kvůli lepším výsledkům. Zachovej existující lidské štítky.

## 2. Zpřesni prezentaci metrik

V `reports/ACCURACY.md`, README a souvisejících výstupech:

- Nahraď obecné označení „Ruční přesnost: 100 %“ přesným názvem měřené veličiny.
- Pokud aktuální data stále odpovídají původnímu stavu, uveď: „Precision původních pozitivních klasifikací: 10/10 na záměrně vybraném vzorku.“
- Doplň recall 10/11 v rámci kontrolovaného seznamu a vysvětli vliv abstence u Purple.
- Počty a procenta odvozuj z dat, ne z natvrdo napsaných hodnot.
- Rozlišuj precision klasifikace, správnost jednotlivých atributů a úplnost dat.
- Viditelně uveď, že 10/10 neznamená 100% správnost celé databáze ani odhad přesnosti na světovém trhu.
- Zachovej správné vysvětlení omezeného významu Wilsonova intervalu pro tento záměrný vzorek.

## 3. Oprav význam příznaků lidského ověření

Prověř `human_verified` v CSV, SQLite, JSON a kódu. V souhrnném exportu byl nastaven pevně na `False`.

- Rozliš ověření klasifikace investora od ověření jeho atributů.
- Zvol jasné názvy polí a popiš jejich přesný význam v datovém modelu.
- Hodnoty odvozuj ze skutečně vyplněných lidských kontrol.
- Potvrzení, že subjekt patří mezi investory, nesmí automaticky označit všechny jeho finanční údaje za ručně ověřené.
- Změny konzistentně promítni do exportů, dokumentace a relevantních testů.

## 4. Připrav malý audit atributů člověkem

Aktuálně může být klasifikace dokončená, ale přesnost jednotlivých tvrzení nezměřená.

- Ověř skutečný stav `review/claims.csv` a metrik.
- Pokud atributový audit není dokončen, předem stanov a zdokumentuj pravidlo výběru malé vzorky přibližně 15-20 tvrzení napříč investory.
- Zahrň sektory, investiční fáze, obvyklé výše investic a kapitálové údaje. Nevybírej jen snadná nebo zjevně správná tvrzení.
- Připrav přehled s ID tvrzení, hodnotou, přesnou URL, kontrolní otázkou a prázdným místem pro lidské rozhodnutí.
- Odděl chybějící údaje od pozitivních faktických tvrzení. Nezjištěná hodnota není automaticky nesprávný údaj.
- Lidské štítky, identitu kontrolora, datum ani dobu kontroly nikdy nevymýšlej a nevyplňuj za mě.
- Pokud podklady posoudíš sám, označ to pouze jako kontrolu AI.

Dokonči všechny opravy nezávislé na mé odpovědi. Na konci mi předlož konkrétní podklady pro zbývající lidskou kontrolu.

## 5. Doplň cílenou rešerši kapitálu

U přijatých investorů s chybějícím `total_investment_capital` proveď přiměřenou doplňující rešerši veřejných zdrojů, přednostně oficiálních webů, zpráv investorů a institucionálních zdrojů.

- Zachovej rozlišení AUM, velikosti jednotlivého fondu, cílového fundraisingu, proinvestované částky a disponibilního kapitálu.
- Nesčítej historické fondy do současného AUM.
- Datum návštěvy stránky nepovažuj za datum platnosti částky.
- Nové údaje zapisuj s přesným zdrojem, významem, rozsahem, datem a stavem ověření.
- Pokud srovnatelný celkový kapitál nenajdeš, ponech chybějící hodnotu a zdokumentuj rozsah hledání. Nevymýšlej náhradní odhad.
- Pokud narazíš na rozpor, zachovej oba výroky a vysvětli nejistotu.

Podle výsledků aktualizuj úplnost a souhrny. Pokud nemáš přístup k webu, tento krok výslovně označ jako neprovedený.

## 6. Sjednoť finální dokumentaci

Prověř README, PILOT, ACCURACY, GLOBAL_SCOPE_AND_COST, DATA_MODEL, WORKLOG, dokumentaci exportu konverzace a release metadata.

- Odstraň zastaralé informace o čekající lidské kontrole a neověřených CI bězích, pokud už existují ověřené výsledky.
- Historické záznamy zachovej jako historii. Zřetelně je odděl od současného stavu.
- V rozpočtu uveď, že lidská kontrola klasifikace proběhla, ale její čas nebyl měřen.
- Zpětně neodhaduj skutečný čas ani spotřebu tokenů. Náklady ponech jako transparentní scénář, pokud nemáš nová naměřená data.
- Nepřidávej automatický požadavek na nativní export konverzace. Citované zadání požaduje popis práce s AI v README; existující export může zůstat doplňkovým podkladem.
- README uprav tak, aby hodnotitel rychle našel výsledek, způsob spuštění, hlavní omezení a popis práce s AI.
- Skutečné pokyny uživatele neprezentuj jako podrobnější, než byly. Nevymýšlej zpětně prompty, subagenty ani lidská rozhodnutí.
- Při nových úpravách českých textů používej pro pomlčku symbol `-`.

## 7. Ověř funkčnost a reprodukovatelnost

Spusť příslušné kontroly projektu, zejména:

```console
python -m investor_db validate
python research/audit_database.py
python -m unittest discover -s tests -v
python -m investor_db build
python -m investor_db check-release
```

Po buildu ověř shodu reportů, metrik a exportů. Opakované sestavení nesmí přepsat lidské štítky ani vrátit zastaralé texty.

Doplň pouze smysluplné regresní testy změněného chování, zejména odvození příznaků ověření a rozlišení rozhodnutí AI a člověka. Testy nepovažuj za důkaz pravdivosti externích zdrojů.

Pokud je dostupný GitHub, ověř stav CI pro konkrétní kontrolovaný commit. Bez přístupu výsledek netvrď.

## Výstup

Na závěr stručně napiš:

1. Co bylo skutečně opraveno.
2. Jaké kontroly proběhly a s jakým výsledkem.
3. Co zůstává omezením řešení.
4. Co přesně ještě potřebuji ověřit já jako člověk.

Neoznačuj neprovedené kroky za hotové. Neměň externí repozitář ani neprováděj push, pokud to není autorizované v aktuální relaci.