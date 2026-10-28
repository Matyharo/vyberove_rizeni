# Archiv kontrol do 25. 10. 2026

Historické záznamy. Aktuální stav: [FINAL_CHECKS.md](FINAL_CHECKS.md).

# Aktuální ověření - 25. 10. 2026

Výchozí commit 680276e845b48aea839370b270da470284c19002. Nové lokální úpravy nejsou commitnuté, pushnuté ani nasazené.

Prošly validate, databázový audit (7 invariantů), všech 34 Python testů, build, check-release a všech 5 JavaScript testů. Opakovaný build vytvořil byte-identické exporty, webový balíček a README. Datové vstupy a review soubory odpovídají HEAD po normalizaci konců řádků. Všech 18 atributových hodnocení zůstalo na výslovný pokyn uživatele ve stejném zařazení, se stejnými metadaty a metrikami (12 supported, 6 uncertain).

Chromium přes Playwright ověřil normalizované nabídky, rozvinutí explicitního rozpětí do Seed, nezahrnutí obecného early-stage do Seed, shodu formuláře a sdílené URL, převod původního názvu sektoru v URL a reset. Při šířkách 1536, 768 a 390 px nevzniká horizontální přetečení dokumentu. Bez runtime a console chyb. Browser plugin nebyl dostupný; použit lokální Playwright. Skript a screenshot zůstávají mimo repozitář v pracovních vizualizacích.

Živý web i data odpověděly HTTP 200. Úspěšné [Pages nasazení](https://github.com/Matyharo/vyberove_rizeni/actions/runs/39939284199) patří commitu e3469cbe969b4a5b99ec65561ecd432c6e30f01d; úspěšné [CI](https://github.com/Matyharo/vyberove_rizeni/actions/runs/39940157324) patří výchozímu 680276e. Tyto běhy nepotvrzují nové lokální změny. Přesné důkazy: [PUBLICATION_STATUS.json](PUBLICATION_STATUS.json).

---

# Historické ověření

# Aktuální ověření po zápisu atributového auditu

Provedeno 22. 10. 2026 nad lokálním stromem vycházejícím z commitu fdae4afd30b5c29f24c0c84ce7a1f9e1c683f318. Předchozí finální opravy již byly pushnuty v tomto výchozím commitu. Nové změny obsahující atributové štítky zatím nebyly commitnuty ani pushnuty.

Všech pět požadovaných příkazů prošlo (exit 0): validate, research/audit_database.py, unittest discover -s tests -v, build a check-release. Prošlo všech 28 testů a všech sedm databázových invariantů. Nový regresní test ověřuje, že uncertain ani kontroly null nezvyšují přesnost pozitivních tvrzení.

Další build vytvořil byte-identické exporty včetně SQLite, generované reporty i metrikový blok README. Zachoval oba review soubory. Zmrazené kandidáty, původní predikce, lidskou klasifikaci, samotná tvrzení v pilot.json i výběr auditovaných ID porovnání s výchozím commitem potvrdilo jako nezměněné.

Nově je zapsáno 18 skutečně dodaných atributových rozhodnutí: 12 supported, 6 uncertain, 0 incorrect. Kontrolor Ferstl, datum 2026-10-22, podle potvrzení uživatele v chatu. Shoda vyřešených tvrzení je 12/12; šest uncertain je mimo jmenovatel a ostatní databázová tvrzení nebyla tímto auditem potvrzena. Čas nebyl dodán ani odhadován. Rozpor Purple a historická/neurčená data kapitálu zůstávají zachovány.

Aktuální strojové výsledky: [FINAL_CHECKS.json](FINAL_CHECKS.json), [DATABASE_AUDIT.json](DATABASE_AUDIT.json). Šest otevřených případů a dodané důvody: [CLAIM_AUDIT.md](CLAIM_AUDIT.md), [claims.csv](../review/claims.csv).

Vzdálený CI běh pro tento výchozí commit nebyl v této etapě ověřován. Starší pokusy níže se vztahují pouze ke staršímu uvedenému commitu a nejsou důkazem výsledku CI nových změn.

---

# Historický protokol před dodáním atributových štítků

Následující část zachovává tehdejší stav; údaje o prázdném auditu a nepushnutých finálních opravách již nepopisují současnost.

# Finální lokální ověření

Provedeno 22. 10. 2026 nad lokálně upraveným stromem, výchozí commit 9fe06728dafb2ec008cff790b2fa1f02d7b94b39. Změny nebyly pushnuty.

| Příkaz | Výsledek |
|---|---|
| python -m investor_db validate | prošel (exit 0) |
| python research/audit_database.py | prošel (exit 0) |
| python -m unittest discover -s tests -v | prošel (exit 0) |
| python -m investor_db build | prošel (exit 0) |
| python -m investor_db check-release | prošel (exit 0) |

Všech 27 testů prošlo. SQLite audit: všech sedm invariantů splněno; integrity_check ok a žádné porušené cizí klíče. Strojové výsledky: [FINAL_CHECKS.json](FINAL_CHECKS.json), [DATABASE_AUDIT.json](DATABASE_AUDIT.json).

Další build vytvořil byte-identické exporty včetně SQLite, generované reporty i metrikový blok README. Review soubory se nezměnily. Kandidáti, původní predikce a lidská klasifikace jsou shodné s výchozím commitem po normalizaci konců řádků. Existující řádky claims.csv zůstaly stejné; pouze pět nových prázdných řádků bylo přidáno pro nové kapitálové výroky. Žádný atributový lidský štítek nebyl vyplněn. Audit má 18 tvrzení napříč 11 investory.

Nové regresní kontroly ověřují publikaci jen při shodě AI a člověka, Lighthouse a Purple ve třech rozhodnutích, odvození klasifikačních a atributových příznaků napříč CSV/JSON/SQLite, zachování lidských řádků při opakovaném buildu a nepovinný export konverzace. Syntetické štítky v dočasných testovacích kopiích nejsou lidským měřením.

## GitHub CI

Pro konkrétní commit 9fe06728dafb2ec008cff790b2fa1f02d7b94b39 konektor vrátil prázdný seznam PR workflow běhů a prázdný seznam combined statusů. První endpoint filtruje pouze PR běhy, druhý nemusí zahrnovat Actions check runs: prázdné seznamy nedokazují úspěch ani absenci CI. Přímý shellový dotaz na GitHub API selhal na DNS; webový přístup k Actions stránce také selhal. Úspěšný vzdálený běh tedy nebyl ověřen. Lokální změny nemají nový vzdálený commit ani CI běh.

## Limity a lidský krok

Přesnost externích tvrzení testy nepotvrzují. Klasifikace je dokončena, atributová přesnost zůstává nezměřena; připravené podklady jsou [CLAIM_AUDIT.md](CLAIM_AUDIT.md). Doplňující rešerše kapitálu byla provedena AI v omezeném veřejném rozsahu, bez dalšího srovnatelného současného AUM. Lidský čas ani tokeny nebyly zpětně odhadovány.
