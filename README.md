# Spolehlivá databáze investorů

Praktická úloha A pro Junior AI Developer. Plán vznikl před pilotem; historie začíná 22. 10. 2026.

**Výsledek technické etapy:** 20 kandidátů, 11 předběžně přijatých VC organizací, 8 vyloučených a 1 nevyřešená identita podle AI. 45 veřejných zdrojů, 116 tvrzení a 13 investičních důkazů. Ručně zkontrolováno **20/20 kandidátů**: Credo, DEPO, i&i Bio, INVEN, KAYA, N1, Tensor, Tilia, Purple, J&T a Reflex include; BDO, původní Lighthouse, Genesis, ARX, AKAT, Fundlift, Startovač, CVCA a Startupstart exclude z VC pilotu. Genesis a ARX jsou samostatně evidováni jako PE / growth equity, respektive PE investoři. Všech 10 původních pozitivních predikcí bylo posouzeno jako správných. Lidský výsledek: 11 include a 9 exclude z VC pilotu; původní abstence Purple je include a původní abstence Lighthouse exclude.

Veřejný repozitář: https://github.com/Matyharo/vyberove_rizeni

## Co otevřít

- [Plán a pravidla zařazení](PLAN.md) — původní metodika a pravidla pro chybějící údaje.
- [Pilot se zdroji u každého údaje](reports/PILOT.md) — hlavní čtenářský výstup.
- [Přesnost a úplnost](reports/ACCURACY.md) — nic nepředstírá lidské ověření.
- [Globální rozsah a náklady](reports/GLOBAL_SCOPE_AND_COST.md) — zdrojové kotvy, předpoklady a tři přepočitatelné scénáře.
- [Ověření databáze](reports/DATABASE_TESTING.md) — integrita, vazby, chybové zápisy a opakované sestavení.
- [Datový model](docs/DATA_MODEL.md) — význam veličin, dat a stavů tvrzení.
- [Podklady pro lidskou kontrolu](reports/REVIEW_PACKET.md) — bez predikcí AI; postup v [review/README.md](review/README.md).

## Spuštění

Python 3.11 nebo novější, pouze standardní knihovna. Není potřeba instalace balíčků, přístup k síti ani API klíč. Příkazy z kořene repozitáře:

```console
python -m investor_db validate
python research/audit_database.py
python -m unittest discover -s tests -v
python -m investor_db build
python -m investor_db check-release
```

`build` obnoví CSV, SQLite, metriky a přehledy. Existující lidské štítky nepřepisuje. `check-release` nyní prochází: ruční klasifikace, veřejná URL a export jsou přítomné. Je to kontrolní seznam, ne doklad pravosti lidských štítků nebo dostupnosti vzdáleného repozitáře.

Výstupy lze prohlédnout bez spuštění:

- `exports/investor_summary.csv`: přijatí investoři, URL u atributů a příznaky kvality.
- `exports/claims.csv`, `sources.csv`, `transactions.csv`, `funds.csv`, `decisions.csv`: úplný datový původ.
- `exports/investors.sqlite`: relační databáze s cizími klíči, původními predikcemi i případnými lidskými štítky.
- `exports/metrics.json`, `cost_estimate.json`: přepočitatelné výsledky.
- `data/candidates.json`, `predictions.json`: zmrazený výběr a první rozhodnutí AI. Neměnit při opravách výsledku.
- `data/pilot.json`: aktuální tvrzení a důkazy. Offline build reprodukuje přepis; nestahuje znovu živé weby.

## Proč tento rozsah

Pilot je záměrný kontrastní výběr českých VC organizací a kontrolních subjektů, nikoli náhodný soupis trhu. Omezení na VC umožňuje posoudit mandát. Genesis a ARX jsou skuteční PE investoři, ale mimo tento úzký pilot. V globální PE databázi by se prověřovali pro zařazení, nikoli zahodili jako „neinvestoři“.

Jednotkou je organizace či značka investora. Jednotlivé fondy jsou oddělené. Právní struktury nejsou úplně rozkryté; česká kancelář neznamená český domicil fondu. Českou přítomnost v pilotu dokládá kontaktní/office adresa nebo firemně deklarované ústředí; skutečný provoz kanceláře nebyl navštíven.

## Co ukázal pilot

Obvyklá velikost investice má bez zjištěného rozporu primární oporu u 8/11 přijatých organizací. U Tensoru existuje pouze nedatovaný asociační údaj; Reflex běžné rozpětí v použitých zdrojích neuvádí a Purple má rozpor mezi dvěma vlastními profily. Celkový spravovaný kapitál je uveden u 2/11 organizací, obě hodnoty self-reported bez data ocenění. Další historické částky a velikosti fondů jsou zachované jako jiné veličiny.

To jsou metriky **úplnosti**, nikoli přesnosti. Precision počítáme proti skutečným lidským rozhodnutím; bez nich je null. Po dokončení kontroly 20/20 kandidátů je precision původních pozitivních predikcí 10/10 na tomto záměrně vybraném vzorku. Recall v rámci vzorku je 10/11 (90,9 %), protože původní AI se u Purple zdržela rozhodnutí. Není to důkaz 100% přesnosti databáze. Matice záměn má i needs_review a recall se vztahuje pouze k prověřovanému seznamu.

Globálně plánujeme obálku 6–24 tisíc veřejně doložitelných záznamů po kontrole 10–40 tisíc kandidátů. Základní scénář prvního sběru je přibližně 128 tisíc USD; nejvíce stojí lidská kontrola. Odhad není kalibrovaný dosud chybějící časomírou lidské kontroly. Zdroje, definice a předpoklady jsou v globální zprávě.

## Jak jsem pracoval s AI

Použitý nástroj: **Codex**, jeden asistent, bez delegovaných subagentů a bez samostatného API. Skutečné pokyny uživatele byly předané zadání, výběr varianty A a pokračování. Detailní metodiku, strukturu a validační pravidla následně navrhla AI; nevydáváme je za uživatelem předem napsaný prompt.

Postup: nejdříve plán, poté zmrazení kandidátů, otevření veřejných zdrojů, přepis faktů s původem, strukturální validace a následná kontrola vlastního výstupu. Rešerše byla řízená asistentem přes webový nástroj, nikoli automatický crawler. `research/curate_pilot.py` zachycuje přepis; neměří výkon automatické extrakce.

Kontrola měla tři různé vrstvy:

1. AI znovu četla zdroje a opravovala vlastní přepis. Není to nezávislé ověření člověkem.
2. Validátor a testy kontrolují vazby, peněžní veličiny, data, nejistotu, metriky a skutečný export do SQLite.
3. Uživatel posoudil zdroje v sedmi kolech v chatu. Jeho skutečná rozhodnutí jsou zapsána do `review/labels.csv` a poznámek `review/round-*.md`; z nich vzniká ruční měření klasifikace, nikoli přesnosti všech atributů.

Konkrétní omyly a problémy:

- AI zkoušela neověřené varianty domén Nation1 a Lighthouse. Vyhledávání vracelo jmenovce. N1 je nakonec propojen se značkou Nation 1 přes právní disclosure. Lighthouse zůstává needs_review: discovery profil odkazuje na jinou entitu než český fond.
- AI přehlédla adresu Purple v patičce a nejprve se zdržela rozhodnutí. Pak doplnila potvrzení ústředí z firemního profilu. Původní predikce je zachována. Rozdílné tickety zůstaly označené.
- U Reflexu následná kontrola snížila sektor a fázi na partial a cílovou geografii na not_found. Kanceláře samy nedokládají investiční geografii.
- První SQLite export měl 11 placeholderů pro 10 sloupců. Opraveno a pokryto integračním testem. Windows testy také odhalily, že transakční context manager SQLite sám nezavírá spojení; opravili jsme uzavírání a umístění dočasných souborů.
- Ručně přepsaný základní čtvrtletní rozpočet neodpovídal přepočtu; opraven na 12 360 USD a pokryt testem.

Autentický průběžný výřez veřejných zpráv je v `ai-log/conversation-snapshot.md`, s popisem filtrace a manifestem. **Není to finální nativní export.** Uživatel následně dodal Markdown export celé dosavadní konverzace. Jeho veřejná redigovaná verze je v `ai-log/conversation-export.md`; původ a úpravy dokumentuje `ai-log/export-manifest.json`. Konkrétní použití příkazu /export nebylo nezávisle ověřeno. Podrobný protokol: [ai-log/WORKLOG.md](ai-log/WORKLOG.md).

## Ověření a zbývající práce

Lokálně prochází 22 testů a strukturální validace. Integrační test skutečně vytváří databázi, kontroluje cizí klíče, opakované sestavení a zachování štítků. Syntetické testovací štítky nejsou výsledkem měření. GitHub Actions mají stejné kontroly připravené; výsledek vzdáleného běhu zatím nebyl ověřen.

Ruční klasifikace všech 20 kandidátů je dokončena a výstupy přepočteny. Čas kontroly nebyl měřen; zpětně jej nevymýšlíme a rozpočet zůstává scénářovým odhadem. Kontrola jednotlivých atributů nebyla systematicky změřena. Uživatelem dodaný export je doplněn, redakce technických bloků a domovských cest jsou zdokumentované. Repozitář je připraven k odevzdání s uvedenými omezeními. URL je uvedena v `release.json` v poli `public_repository_url`. Lidská kontrola faktů, úplnost a veřejný zdroj jsou různé věci; žádnou nenahrazuje zelený test.

Termín: **30. 10. 2026**.
