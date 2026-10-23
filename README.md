# Spolehlivá databáze investorů

Praktická úloha A pro Junior AI Developer. Výsledek: malý evidenční pilot českých VC investorů, reprodukovatelné CSV/JSON/SQLite, plán a scénář globálního rozšíření. Veřejný repozitář: [Matyharo/vyberove_rizeni](https://github.com/Matyharo/vyberove_rizeni). Termín: 30. 10. 2026.

<!-- METRICS:START -->
Publikováno **11 investorů** z 20 zmrazených kandidátů; lidská klasifikace 20/20. Původní AI: {'needs_review': 2, 'exclude': 8, 'include': 10}. Aktuální AI: {'needs_review': 1, 'exclude': 8, 'include': 11}. Lidská reference: {'include': 11, 'exclude': 9}. 47 zdrojů, 121 tvrzení, 13 investičních důkazů.

**Precision původních pozitivních klasifikací: 10/10 na záměrně vybraném vzorku.** Recall v kontrolovaném seznamu: 10/11; původní abstence Purple snižuje recall. To neznamená 100% správnost celé databáze ani odhad přesnosti světového trhu. Lidský audit atributů: 18 kontrol, 12 supported, 0 incorrect, 6 uncertain. Shoda vyřešených tvrzení s lidskou referencí: 12/12. Uncertain jsou mimo jmenovatel; nejde o potvrzení všech kontrolovaných ani všech databázových atributů. Supported u historického nebo rozporného údaje potvrzuje oporu v příslušném zdroji, nikoli současnou platnost či vyřešení rozporu.

Úplnost supported atributů publikovaných investorů: sectors 10/11; stage 10/11; ticket 8/11; total_investment_capital 2/11. Úplnost není přesnost.
<!-- METRICS:END -->

## Co otevřít

- [Pilot se zdroji a třemi rozhodnutími](reports/PILOT.md) - hlavní výsledek.
- [Přesnost a úplnost](reports/ACCURACY.md) - rozsah měření a omezení Wilsonova intervalu.
- [Plán a pravidla](PLAN.md), [globální rozsah a náklady](reports/GLOBAL_SCOPE_AND_COST.md).
- [Datový model](docs/DATA_MODEL.md), [ověření databáze](reports/DATABASE_TESTING.md).
- [Výsledky auditu 18 tvrzení](reports/CLAIM_AUDIT.md) a [vyplnitelný CSV přehled](exports/claim_audit_worksheet.csv).
- [Cílená rešerše kapitálu](reports/CAPITAL_RESEARCH.md) - rozsah hledání a rozlišení veličin.

## Spuštění

### Webový přehled

Statická aplikace používá HTML, CSS a JavaScript bez frameworku, backendu a externích fontů. Python build ověří data a vytvoří samostatný adresář `site/` včetně jednoho datového balíčku `data.json` a funkčních exportů. Zdrojový kód je ve `frontend/`; `site/` je generovaný a není verzovaný. Výběr přebírá ze stejné publikace jako souhrnné CSV. Názvy, částky ani počty nejsou ručně přepsané v UI.

```console
python -m investor_db build
python -m http.server 8000 --bind 127.0.0.1 --directory site
```

Otevřete [lokální přehled](http://127.0.0.1:8000/). Použijte HTTP server, nikoli otevření souboru přes file://. Web má hledání bez české diakritiky, kombinované filtry, řazení podle názvu, sdílení URL filtru a investora a zdroje u jednotlivých údajů. Detail se zavírá tlačítkem, Escape nebo Zpět a vrací focus na původní akci. Na mobilu zabírá celou obrazovku. Stažené CSV a JSON obsahují celý publikovaný pilot, ne aktuálně filtrovaný výběr.

Balíček zachovává původní stavy tvrzení, peněžní významy, obě rozpětí Purple, historické alternativy Credo a Tensor, transakce, zdroje a reference s kontrolorem a datem. Výraz „Reference dodaná uživatelem“ neznamená nezávislý audit všech údajů. Podmínku publikace vyhodnocuje Python, nikoli frontend. Filtry sektorů a fází jsou doslovné části tvrzení, nevytvářejí novou přesnou taxonomii.

### GitHub Pages

Workflow `.github/workflows/pages.yml` sestaví a otestuje web na pull requestu nebo při ručním spuštění. Původní workflow validace zůstává zachovaný. Veřejné nasazení se spouští pouze ručně a standardně je vypnuté; samotný push do main nic nenasadí.

Po schválení zveřejnění:

1. Commitnout a pushnout připravené změny do repozitáře.
2. V repozitáři otevřít **Settings -> Pages -> Build and deployment -> Source -> GitHub Actions**.
3. Otevřít **Actions -> Build and publish investor browser -> Run workflow**, zvolit main a zaškrtnout **Publish the built site to GitHub Pages**.
4. Po dokončení deploy použít URL z prostředí github-pages a ověřit načtení. Případné schválení prostředí závisí na nastavení repozitáře.

Push ani nasazení této etapy nebyly provedeny. Žádná veřejná adresa webu není vydávána za ověřeně funkční. Samostatný balíček byl lokálně ověřen také pod `/vyberove_rizeni/`; vlastní soubory a downloady používají relativní cesty.

### Ověření frontendu

```console
python -m investor_db validate
python -m investor_db build
python research/audit_database.py
python -m unittest discover -s tests -v
node --test frontend/tests/*.test.mjs
python -m investor_db check-release
```

Node.js je potřeba jen pro čtyři vývojové modelové testy, nikoli pro Python build nebo používání webu. Není potřeba npm install. Python integrační testy porovnávají web s publikací pipeline, zachování referencí, rozporů, peněžních hodnot a determinismus sestavení.

Browser QA 23. 10. 2026: Chromium při 1536x1024, 768x900 a 390x844. Ověřena shoda s pipeline, hledání včetně diakritiky, kombinované filtry/reset/prázdný stav, řazení, obě hodnoty Purple se zdroji, historické a chybějící hodnoty, detail/Escape/focus trap/návrat focusu/Zpět/přímé URL, tři skutečně stažené exporty a cesta `/vyberove_rizeni/`. Ověřeno také pomalé načítání, chyba dat a retry, prázdný dataset, reduced-motion a inertní vykreslení škodlivých textů/URL. Běžný tok byl bez konzolových varování a runtime chyb. Vestavěný prohlížeč byl po odstranění blokace lokálního socketu rovněž otevřen; systematické simulace běžely v lokálním Playwright Chromium.

Nejde o kompletní WCAG audit, fyzický telefon nebo kontrolu aktuální pravdivosti všech externích webů. Odkazy byly porovnány se zabalenými zdroji a povolenými schématy; jejich síťová dostupnost nebyla hromadně ověřována. Statický UI audit prošel v strict režimu. Ovládací tlačítka v základním HTML jsou neaktivní do navázání modulových obsluh, takže neexistují aktivní akce bez funkce. CSP záměrně nepovoluje inline obsluhy. Lint DESIGN.md prošel bez chyb; upozornění na tokeny se týkají dokumentačních komponent, runtime vlastní centrální CSS.

### Datová pipeline

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

Konkrétní chyby AI: záměny jmenovců Lighthouse a hledání neověřených domén Nation1; přehlédnutí adresy Purple vedoucí k původní abstenci; odvozování mandátu Reflex z portfolia, následně snížené na partial; nesprávné SQLite placeholdery a nezavřená spojení na Windows; ručně přepsaný rozpočet, který neodpovídal výpočtu. Opravy jsou evidované v [WORKLOG](ai-log/WORKLOG.md). Nové opravy odstraňují pevné human_verified=False, oddělují rozhodnutí a metriky a připravily předem vybraný atributový audit. Uživatel následně dodal rozhodnutí a potvrdil kontrolora Ferstl a datum 22. 10. 2026; AI tyto štítky pouze zapsala.

Oba uživatelem dodané redigované Markdown exporty, skutečná zadání finálních oprav a frontendu a průběžný snapshot jsou v [archivu konverzací s AI](ai-log/README.md). Nový export z 23. 10. 2026 zachycuje také finální opravy, atributový audit a frontend až po push e3469cb. Manifesty uvádějí původ, kontrolní součty a redakce. Technické bloky nástrojů a lokální obrazové přílohy jsou vynechané; domovské cesty anonymizované. Způsob nativního exportu nebyl nezávisle potvrzen, obsah není rekonstruovaný.

## Ověření a zbývající práce

Aktuální výsledky kontrol a stav CI pro konkrétní commit: [FINAL_CHECKS.md](reports/FINAL_CHECKS.md). Zelený lokální checklist nedokazuje pravdivost externích zdrojů.

Lidská klasifikace i první kolo malého atributového auditu jsou zapsány. Šest uncertain případů vyžaduje další dohledání úplných zdrojů, mandátu nebo významu veličiny; konkrétní ID a důvody jsou v review/claims.csv a reports/CLAIM_AUDIT.md. Potvrzené rozporné tickety Purple se neslučují a historické částky se nemění na současné AUM. Audit nepokrývá všechny databázové atributy. Původní predikce a lidská klasifikace nebyly kvůli výsledkům změněny.
