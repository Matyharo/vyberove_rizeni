# Chování statického registru

Jeden read-only tok: přehled -> investor -> původ údaje. Neexistují žádné mutace dat, přihlášení, platby, selection ani CRUD.

| Capability | Canonical owner | Source of truth | Allowed variants | Verification |
|---|---|---|---|---|
| Select/Listbox | native select v frontend/index.html | initFilters v app.js | Popup vlastní OS | Klávesnicová volba v browser QA |
| Form | filters v index.html | writeFilters v app.js | Lokální kombinované filtry | novalidate, skutečné label, reset |
| Date | dateText v frontend/model.js | Zdrojové date-only hodnoty | cs-CZ, UTC, rok | Model test zachování roční přesnosti |
| Scrollbar | frontend/style.css | Globální baseline | Tabulka vodorovně, detail svisle | Browser QA, computed styles |
| Dialog | syncRoute / closeDetail v app.js | Nativní dialog.showModal | Investor, metodika, exporty | Escape, close, focus trap a návrat |
| Data a publikace | investor_db/core.py -> investor_db/web.py | publication_ids | Pouze publikované organizace | Python integrační testy |
| Stav a navigace | URL search + hash, app.js | URL | Sdílené filtry a #investor=id | Zpět, direct link, zachování filtrů |

Hledání je lokální, bez diakritiky. Sektor a fáze používají explicitně normalizované navigační kategorie se stabilními ID, shodnými pro formulář a URL. Obecné early-stage neimplikuje konkrétní kola. Částečná opora je výslovně uvedena, nevzniká nová přesná klasifikace. Částky nelze řadit. Všechny exporty vždy obsahují celý publikovaný pilot bez ohledu na filtry.

Načítání má klidný indikátor, chyby vlastní text a retry, prázdný výsledek reset. Načítání se přeruší po 15 sekundách; není nekonečný spinner. Do načtení jsou filtry inertní. URL s nepublikovaným či neznámým ID ukáže vysvětlení, nikoli neověřeného investora.

Ověření atributu se vztahuje jen k danému tvrzení a skutečně dodané referenci s kontrolorem a datem. Supported u dvou různých ticketů Purple znamená potvrzený přepis obou zdrojů, nikoli vyřešenou současnou strategii. Výchozí stav filtrování dostupnosti odpovídá coverage pipeline: supported, nenulová hodnota, bez otevřeného rozporu.

Frontend neposílá dotazy na žádné vzdálené API. Zdrojové odkazy lze otevřít vědomou akcí uživatele. Nedostupná externí stránka není závadou statického balíčku, ale zdrojovým omezením. Texty neobsahují domyšlené kontrolory ani zpětně odhadované časy.
