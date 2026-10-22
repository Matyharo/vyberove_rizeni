# Spolehlivá databáze investorů

Praktická úloha A pro Junior AI Developer. Výsledek: malý evidenční pilot českých VC investorů, reprodukovatelné CSV/JSON/SQLite, plán a scénář globálního rozšíření. Veřejný repozitář: [Matyharo/vyberove_rizeni](https://github.com/Matyharo/vyberove_rizeni). Termín: 30. 10. 2026.

<!-- METRICS:START -->
Publikováno **11 investorů** z 20 zmrazených kandidátů; lidská klasifikace 20/20. Původní AI: {'needs_review': 2, 'exclude': 8, 'include': 10}. Aktuální AI: {'needs_review': 1, 'exclude': 8, 'include': 11}. Lidská reference: {'include': 11, 'exclude': 9}. 47 zdrojů, 121 tvrzení, 13 investičních důkazů.

**Precision původních pozitivních klasifikací: 10/10 na záměrně vybraném vzorku.** Recall v kontrolovaném seznamu: 10/11; původní abstence Purple snižuje recall. To neznamená 100% správnost celé databáze ani odhad přesnosti světového trhu. Lidský audit atributů: 0 kontrol; správnost atributů je samostatná veličina.

Úplnost supported atributů publikovaných investorů: sectors 10/11; stage 10/11; ticket 8/11; total_investment_capital 2/11. Úplnost není přesnost.
<!-- METRICS:END -->

## Co otevřít

- [Pilot se zdroji a třemi rozhodnutími](reports/PILOT.md) - hlavní výsledek.
- [Přesnost a úplnost](reports/ACCURACY.md) - rozsah měření a omezení Wilsonova intervalu.
- [Plán a pravidla](PLAN.md), [globální rozsah a náklady](reports/GLOBAL_SCOPE_AND_COST.md).
- [Datový model](docs/DATA_MODEL.md), [ověření databáze](reports/DATABASE_TESTING.md).
- [18 tvrzení pro lidský audit](reports/CLAIM_AUDIT.md) a [vyplnitelný CSV přehled](exports/claim_audit_worksheet.csv).
- [Cílená rešerše kapitálu](reports/CAPITAL_RESEARCH.md) - rozsah hledání a rozlišení veličin.

## Spuštění

Python 3.11 nebo novější, pouze standardní knihovna. Build je offline, bez instalace balíčků, crawleru a placeného API. Z kořene repozitáře:

```console
python -m investor_db validate
python research/audit_database.py
python -m unittest discover -s tests -v
python -m investor_db build
python -m investor_db check-release
```

Build obnoví exporty, metriky a generované reporty; lidské řádky nepřepisuje, pro nová tvrzení pouze přidává prázdné řádky. Souhrn se publikuje jen při shodě aktuální AI include a lidského include. Needs_review, chybějící reference a rozpory se nepublikují. Původní AI predikce jsou zmrazené a slouží k měření, aktuální AI k evidenci a člověk jako klasifikační reference. Lighthouse zůstává podle AI nevyřešenou identitou, člověk vyloučil původní discovery kandidát; není automaticky ztotožněn s českým fondem.

`check-release` kontroluje lokální podmínky a přítomnost GitHub URL, nikoli pravdivost faktů, veřejnou dostupnost repozitáře nebo dokončení atributového auditu. Export konverzace je volitelný doplněk; zadání vyžaduje popis práce s AI v README.

## Exporty a omezení

`exports/investor_summary.csv` je publikovaný přehled. Normalizované `investors.csv`/JSON a SQLite obsahují evidenci organizací včetně příznaku published; SQL pohled published_investors obsahuje publikované. Claims, sources, transactions, funds a decisions uchovávají původ údajů. JSON/CSV příznaky a SQL pohled claim_verification odvozují lidské ověření z review souborů. Klasifikace investora nepotvrzuje jeho finanční údaje. Přesné definice jsou v datovém modelu.

Pilot je záměrný kontrastní výběr, nikoli náhodný soupis trhu. Genesis a ARX jsou skuteční PE investoři mimo úzký VC pilot, nikoli obecně neinvestoři. Jednotkou je organizace/značka, fondy jsou oddělené; právní struktury a registrace nebyly kompletně auditovány. Česká kontaktní adresa neprokazuje fyzickou návštěvu kanceláře ani český domicil fondu.

Současná AUM jsou self-reported bez data ocenění. Historické AUM, jednotlivé fondy, cíle fundraisingu, proinvestované částky a disponibilní kapitál zůstávají oddělené. Null není nula ani chyba. Nová omezená rešerše nezjistila další srovnatelné současné AUM. Zdroje se mohou měnit; offline build reprodukuje uložený přepis, nikoli živé weby. Testy dokazují vlastnosti kódu a exportů, nikoli pravdivost zdrojů.

Globální rozsah a náklady jsou transparentní scénáře, nikoli změřený globální trh nebo skutečné náklady pilotu. Lidská klasifikace proběhla, její čas nebyl měřen. Skutečné tokeny a náklady nejsou přiřaditelné; zpětně je neodhadujeme.

## Jak jsem pracoval s AI

Použitý nástroj: Codex, jeden asistent, bez delegovaných subagentů a samostatného API. Původní pokyny uživatele byly předané zadání, výběr varianty A a pokračování; později uživatel zvolil společnou klasifikační kontrolu v chatu. Detailní metodiku a strukturu navrhla AI. Aktuální podrobné zadání finálních oprav je novým skutečným pokynem, nikoli zpětně rekonstruovaným původním promptem.

AI připravila plán, zmrazila kandidáty a první predikce, otevřela veřejné zdroje, přepsala výroky s původem a vytvořila validátor, exporty a testy. Rešerše probíhala webovým nástrojem, nikoli automatickým crawlerem. research/curate_pilot.py je historický přepis; aktuální pravdou pro build je data/pilot.json.

Kontroly mají tři vrstvy: AI opravuje vlastní přepis; kód ověřuje strukturu a reprodukovatelnost; uživatel poskytl skutečné klasifikační štítky v sedmi kolech, uložené v review/labels.csv a review/round-*.md. Klasifikační štítky nejsou systematickým auditem všech atributů. review/claims.csv se nevyplňuje za člověka.

Konkrétní chyby AI: záměny jmenovců Lighthouse a hledání neověřených domén Nation1; přehlédnutí adresy Purple vedoucí k původní abstenci; odvozování mandátu Reflex z portfolia, následně snížené na partial; nesprávné SQLite placeholdery a nezavřená spojení na Windows; ručně přepsaný rozpočet, který neodpovídal výpočtu. Opravy jsou evidované v [WORKLOG](ai-log/WORKLOG.md). Nové opravy odstraňují pevné human_verified=False, oddělují rozhodnutí a metriky a připravují skutečně prázdný atributový audit.

Uživatelem dodaný redigovaný Markdown export a průběžný snapshot zůstávají doplňkovými historickými podklady s manifesty v [ai-log](ai-log/README.md). Způsob nativního exportu nebyl nezávisle potvrzen; obsah není rekonstruován ani doplňován o tuto novou etapu.

## Ověření a zbývající práce

Aktuální výsledky kontrol a stav CI pro konkrétní commit: [FINAL_CHECKS.md](reports/FINAL_CHECKS.md). Zelený lokální checklist nedokazuje pravdivost externích zdrojů.

Lidská klasifikace je dokončena. Zbývá otevřít zdroje u 18 připravených tvrzení, posoudit přesnou hodnotu, význam a datum, vyplnit odpovídající řádky review/claims.csv a znovu sestavit výstupy. Vybraná tvrzení zahrnují i rozpory, historické částky a částečné mandáty. Přesnost atributů zůstává do té doby nezměřena. Existující lidská rozhodnutí ani původní predikce nebyly kvůli výsledkům změněny.
