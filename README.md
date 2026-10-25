# Databáze investorů

Doložený pilot investorů s českou přítomností pro praktickou úlohu Junior AI Developer. Investiční zaměření, částky, zdroje a nejistota údajů na jednom místě.

**[Otevřít živou aplikaci](https://matyharo.github.io/vyberove_rizeni/)**

Živý web byl ověřen jako dostupný. Nasazená verze vychází z commitu `e3469cb`; následující cílené úpravy filtrů jsou zatím lokální. [Přesný stav publikace a kontrol](reports/FINAL_CHECKS.md).

<!-- METRICS:START -->
**11 publikovaných investorů** z 20 kandidátů; klasifikační kontrola 20/20. 47 zdrojů, 121 tvrzení a 13 investičních důkazů.

Obvyklá investice doložena bez rozporu u 8/11 investorů; celkový spravovaný kapitál u 2/11. Jde o úplnost, nikoli přesnost.

Precision původních pozitivních klasifikací: **10/10 na záměrném vzorku**. Recall pouze v kontrolovaném seznamu: **10/11**. Výsledek nepotvrzuje správnost celé databáze ani světového trhu.
<!-- METRICS:END -->

## Lokální spuštění

Python 3.11+, pouze standardní knihovna. Build funguje offline, nevyžaduje API klíč ani instalaci frontendových balíčků.

```console
python -m investor_db build
python -m http.server 8000 --bind 127.0.0.1 --directory site
```

Otevřete [localhost:8000](http://127.0.0.1:8000/). Adresář `site/` obsahuje kompletní statickou aplikaci, JSON a exporty; generuje se ze zdrojů v `frontend/` a datové pipeline. Filtry jsou navigační pomůcka, nikoli nezávisle ověřená klasifikace. Sektorově otevřené zaměření neznamená všechny sektory a neurčité early-stage se nepřevádí na přesné fáze.

## Metodika, výsledek a omezení

- [Plán a pravidla zařazení](PLAN.md), [pilot se zdroji](reports/PILOT.md).
- [Měření a úplnost](reports/ACCURACY.md), [atributová hodnocení](reports/CLAIM_AUDIT.md).
- [Globální rozsah a scénář nákladů](reports/GLOBAL_SCOPE_AND_COST.md).
- [Datový model](docs/DATA_MODEL.md), [normalizace filtrů](docs/NAVIGATION.md).
- [Spuštění, Pages a browser QA](docs/WEB.md), [databázové kontroly](reports/DATABASE_TESTING.md).
- [Aktuální kontroly a publikace](reports/FINAL_CHECKS.md), [archiv konverzací s AI](ai-log/README.md), [protokol práce](ai-log/WORKLOG.md).

Pilot je malý záměrný výběr, nikoli úplný nebo reprezentativní soupis trhu. Genesis a ARX jsou skuteční PE investoři mimo VC pilot. Null není nula. Historické AUM, velikost fondu, cíl fundraisingu a proinvestovaná částka zůstávají oddělené. Oba tickety Purple mají vlastní zdroje a nevyřešenou aktuální platnost. Právní struktury nebyly kompletně auditovány a weby se mohou změnit. Globální počty a náklady jsou transparentní scénáře; čas skutečné kontroly ani tokeny se zpětně neodhadují.

## Práce s AI a kontrola výstupů

Projekt vznikal s jedním asistentem Codex, bez subagentů a samostatného placeného API. Uživatel zadal úlohu, vybral variantu A a následně dodával pokyny a klasifikační reference. AI navrhla metodiku, provedla veřejnou rešerši a přepis tvrzení, implementovala Python pipeline a statický frontend. Skutečná zadání a konverzace jsou archivované; detailnější prompty nejsou zpětně rekonstruované.

Kontrola odděluje původní zmrazené predikce, aktuální AI rozhodnutí, klasifikační reference a jednotlivé atributové záznamy. Validátor a testy ověřují strukturu, metriky a reprodukovatelnost, nikoli pravdivost externích zdrojů. Existujících 18 atributových hodnocení bylo na následný výslovný pokyn uživatele v této etapě ponecháno beze změny včetně jejich zařazení a metrik; oprava jejich původu nebyla provedena.

Konkrétní chyby: záměny jmenovců Lighthouse, přehlédnutá adresa Purple vedoucí k původní abstenci, příliš přesný mandát Reflex odvozený z portfolia a chybné směšování poznámek s kategoriemi filtrů. Historie oprav a původní exporty zůstávají dohledatelné v [WORKLOG](ai-log/WORKLOG.md).

## Kontroly

```console
python -m investor_db validate
python research/audit_database.py
python -m unittest discover -s tests -v
node --test frontend/tests/*.test.mjs
python -m investor_db build
python -m investor_db check-release
```

Node.js slouží pouze k vývojovým testům; aplikace ani Python build jej nepotřebují. Build nepřepisuje review soubory ani zmrazené predikce. CSV a JSON ke stažení obsahují celý publikovaný pilot bez ohledu na aktivní filtry. Publikace nových změn vyžaduje samostatný push a ruční spuštění Pages podle [provozního návodu](docs/WEB.md).
