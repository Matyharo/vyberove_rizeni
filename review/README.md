# Aktuální stav kontroly

Klasifikace všech kandidátů je dokončena v labels.csv. Čas nebyl měřen. První kolo atributového auditu bylo vyplněno kontrolorem Ferstl dne 22. 10. 2026: 12 supported a 6 uncertain z 18 předem vybraných tvrzení. Výsledky jsou v [CLAIM_AUDIT.md](../reports/CLAIM_AUDIT.md) a [CSV přehledu](../exports/claim_audit_worksheet.csv). Vyplňujte odpovídající řádky claims.csv, nikoli vygenerovaný report. Label, reviewer, reviewed_on a reason musí být skutečné; nejistotu označte uncertain. Po doplnění spusťte build a kontroly. Kontrola klasifikace nenahrazuje kontrolu atributů.

Následuje původní metodika kontroly, zachovaná jako postup pro opakované kontroly:

# Skutečná ruční kontrola

Referenční rozhodnutí pocházejí od uživatele Ferstl ze sedmi kol kontroly v chatu dne 22. 10. 2026. AI je pouze přepsala do `labels.csv`; dokončeno 20/20 kandidátů. Podrobnosti jsou v `round-01.md` až `round-07.md`. Testovací štítky žijí pouze v dočasných adresářích testů. Následující postup popisuje metodiku kontroly; první kolo samostatné atributové kontroly je nově zapsané, nejisté případy zůstávají otevřené.

1. Otevřete `reports/REVIEW_PACKET.md`, který neobsahuje predikce AI. Nejprve nečtěte tabulku rozhodnutí v `reports/PILOT.md`.
2. U každého z 20 kandidátů otevřete zdroje. Posuďte identitu, VC mandát, českou přítomnost a konkrétní investici podle `PLAN.md`.
3. Do `labels.csv` doplňte `label` (`include`, `exclude`, `needs_review`), vlastní jméno/iniciály, datum ve formátu YYYY-MM-DD, stručné zdůvodnění a ID použitých zdrojů oddělená středníkem. CSV je oddělené čárkou; text s čárkou dejte do uvozovek. Neměňte záhlaví a ID.
4. Nejasný subjekt označte `needs_review`; nejde o automatické vyloučení. U Genesis a ARX hodnotíte VC pilot, nikoli otázku, zda vůbec investují.
5. U tvrzení v `claims.csv` lze samostatně doplnit `supported`, `incorrect` nebo `uncertain`. `not_found` hodnotí jen rozsah provedeného hledání, nikoli důkaz, že údaj nikde neexistuje. Při opravě přidejte poznámku a zachovejte původní predikce.
6. Spusťte `python -m investor_db build`. Přepočítá se precision, matice záměn, interval a úplnost. Vstupy review se nepřepisují.

Precision pracuje s původními predikcemi v `data/predictions.json`, nikoli s opravenými rozhodnutími v `data/pilot.json`. První predikce: 10 include, 8 exclude, 2 needs_review. Po následné kontrole AI bylo Purple změněno na include. Tento rozdíl není nezávislé lidské měření.

Pro měření času si zapište začátek a konec kontroly a počet zkontrolovaných kandidátů. Budou sloužit ke kalibraci globálního rozpočtu; zatím žádný naměřený lidský čas netvrdíme.
