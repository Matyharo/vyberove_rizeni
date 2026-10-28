# Aktuální stav - 25. 10. 2026

Doplněna explicitní navigační normalizace sektorů a fází, jednotný výklad URL a formuláře, kratší README a dokumentace. Uživatel upřesnil: „Nepřeřazuj těch 18 atributových hodnocení.“ Hodnocení, jejich zařazení, metadata a metriky proto zůstávají zachovány. Požadavek původního zadání na jejich přesun se neprovádí.

Živý web a úspěšné Pages nasazení e3469cb byly ověřeny; CI pro 680276e je úspěšné. Nové lokální změny dosud nejsou publikované. Konkrétní důkazy jsou v reports/PUBLICATION_STATUS.json, lokální kontroly v reports/FINAL_CHECKS.md.

# Historický stav protokolu

23. 10. 2026: na nové podrobné zadání uživatele doplněn statický read-only frontend. Datová a lidská klasifikace zůstaly zachovány. Nové změny nebyly zveřejněny ani pushnuty. Podrobnosti této etapy jsou na konci protokolu.

Klasifikace dokončena v sedmi kolech; následně uživatel dodal malý atributový audit 18 tvrzení (12 supported, 6 uncertain), kontrolor Ferstl, datum 22. 10. 2026. Čas klasifikace nebyl měřen. Markdown export je volitelný doplněk, bez nového požadavku na nativní export. Následující průběžné záznamy včetně tehdejších čekajících kroků jsou historie, nikoli současný seznam úkolů.

# Protokol práce s AI

Toto je shrnutí postupu, **nikoli originální transcript**. Veřejné zprávy jsou mechanicky exportované v conversation-snapshot.md; uživatelem dodaný Markdown export je doplňkový podklad. Nativní export není podmínkou zadání.

## Historie: skutečné pokyny a rozdělení práce

Uživatel poskytl e-mail se zadáním, zvolil A („Můžeme A.“) a zadal „Tak pokračuj.“. Poté zvolil společnou ruční kontrolu v chatu. Pracoval jeden Codex asistent. Subagenti nebyli použiti; pokyny imaginárním agentům nedoplňujeme zpětně.

AI navrhla: pozitivní důkaz pojmenované přímé investice, oddělení správce a fondu, zdroj u každého tvrzení, explicitně chybějící hodnoty, 20 kandidátů, neměnné predikce, vlastní kontrolu oddělenou od lidského reference setu. Postup je zachycený v PLAN.md a commitech.

## Historie

- `16fa7a2`: plán před pilotem, výběrová pravidla a metodika přesnosti/nákladů.
- `d13828d`: 20 zmrazených kandidátů z asociace a ekosystémového seznamu, záměrný kontrastní výběr.
- `70498b1`: první extrakce a zmrazení 10 include / 8 exclude / 2 needs_review před opravami.
- `9c87e72`: validátor, exporty, SQL a testy; oprava Purple po první predikci; 11 include / 8 exclude / 1 needs_review.
- Další commity: zpřísnění atributů Reflexu, rozpor ticketů Purple, globální scénáře, dokumentace a autentický výřez konverzace.

## Kontrola dat

Discovery sloužilo jen k hledání. Asistent otevíral vlastní weby, zprávy portfoliových firem/spoluinvestorů a asociační profily. Výpisky jsou parafráze s URL a daty. Staré CVCA částky zůstávají historické; investor-contribution je null, pokud známe jen částku kola.

Datum známé jen jako rok není nahrazeno 1. lednem. U Tapaya nebylo v otevřené zprávě DEPO nalezeno datum publikace; nedávná aktivita není odvozena z crawl data. U grid.online evidujeme datum indexu článku zvlášť od samotné transakce.

Dva zdroje jsou jen u části případů a jejich nezávislost není garantována. Lidská kontrola ani audit právních registrací nebyly AI vymyšleny.

## Omyly a opravy

1. Jmenovci: chorvatská/kanadská CVCA, jiné JT Ventures, Lighthouse a N1. Výsledky byly rozpoznány jako nesouvisející. CzechStartups navíc u Lighthouse přímo odkazuje na jinou doménu; kandidát zůstává v karanténě.
2. Purple: první extrakce nedohledala adresu. Druhá kontrola ji našla v patičce; protože sídlo nemusí být kancelář, doplnil se firemní profil s Brnem jako ústředím a primární lokalitou. Původní predikce zůstala.
3. Purple ticket: web 250–400 tis. EUR, firemní LinkedIn 250–500 tis. EUR. Rozpětí není vymyšleně sjednoceno; první výrok je partial, alternativní reference zachována.
4. Reflex: charakteristika portfolia mohla být chybně čtena jako úplný sektorový/fázový mandát. Stav změněn na partial; geografie not_found. Kancelář není důkazem investičního regionu.
5. SQLite: první běh selhal na 11 parametrech pro 10 sloupců; opraveno. Další testy selhaly na dočasném adresáři mimo workspace a nezavřeném spojení na Windows. Dočasné soubory jsou nyní v projektu a spojení se explicitně zavírají.
6. Dvě orchestrace vyhledávání skončily SyntaxError kvůli zápisu JavaScriptu; nevytvořily data a byly opraveny.
7. Ruční přepis základní čtvrtletní aktualizace byl chybně 8 160 USD. Kódový přepočet dává 12 360 USD. Dokumentace opravena a přidán test.

## Zbývající lidská práce

Otevřít zdroje, posoudit kandidáty a zapsat skutečná rozhodnutí. Metriky pak pracují s původními predikcemi, ne opravenou tabulkou. Uživatel si zvolil kontrolu v chatu; jeho odpovědi zapíšeme s datem, identifikací kontrolora a zdroji. Nezodpovězené případy za něj nedoplníme.

Export je po posledním kole nutné obnovit. [Dokumentace Codexu](https://learn.chatgpt.com/docs/developer-commands#export-a-conversation-with-export) popisuje nativní `/export` pro CLI a doporučuje počkat na skončení tahu. Zde byl připraven filtrovací skript pro lokální záznam; netvrdíme spuštění Claude `/export`.

## První skutečná ruční kontrola — 22. 10. 2026

Uživatel potvrdil Credo jako přímého investora do Axoflow s pražskou kanceláří, u BDO doložil poradenskou činnost a odmítl ztotožnění původního Lighthouse s českým fondem. Zapsány štítky include/exclude/exclude; jejich interpretace a zdroje jsou v `review/round-01.md`. AI nedoplňovala další řádky. Přepočet: 3/20 zkontrolováno, 1/10 původních pozitivních predikcí vyhodnocena správně, dalších 9 čeká. Čas lidského ověřování není znám.

## Druhá skutečná ruční kontrola — 22. 10. 2026

Uživatel zařadil DEPO a i&i Bio a uložil Genesis evidovat samostatně jako PE / growth equity. Doplnil přímou zprávu Tapaya s datem a historickou investici i&i Bio do Sampling Human s konkrétním vlastním vkladem. AI zdroje otevřela, doplnila datum Tapaya, oddělila domicil fondu od kanceláře poradce a přidala u vlastního vkladu explicitní zdrojovou vazbu i do SQLite. Genesis je v samostatné klasifikační tabulce, nikoli mezi přijatými VC. Podrobnosti: `review/round-02.md`. Zkontrolováno 6/20 kandidátů; původní pozitivní predikce zatím 3/3 správně, sedm čeká. Čas opět není změřen.

## Třetí skutečná ruční kontrola — 22. 10. 2026

Uživatel zařadil INVEN a KAYA a uložil ARX evidovat samostatně jako PE. Zapsáno 9/20 rozhodnutí, 5/10 původních pozitivních predikcí je vyhodnoceno správně; dalších pět čeká. Podrobnosti: `review/round-03.md`. Uživatel také založil repozitář Matyharo/vyberove_rizeni pro zveřejnění projektu; předchozí technické etapy byly vedeny lokálně.

## Čtvrtá skutečná ruční kontrola — 22. 10. 2026

Uživatel zařadil N1 a Tensor a vyřadil AKAT jako asociaci. Historický důkaz N1/Snuggs zůstává odlišen od současné aktivity. U Tensoru doplněn Openvibe s datem vloženého oznámení 28. 1. 2025 a celkovým seed kolem 800 tis. USD; vlastní vklad není odhadován. Podrobnosti `review/round-04.md`. Ručně ověřeno 12/20 kandidátů; sedm původních pozitivních predikcí správně, další tři nevyhodnoceny. Čas kontroly neznámý.

## Pátá skutečná ruční kontrola — 22. 10. 2026

Uživatel zařadil Tilia a Purple a vyřadil Fundlift jako crowdfundingovou platformu. Rozhodnutí zapsána odděleně od atributové kontroly. Hedepy ponecháno jako nedatovaný důkaz v poznámce kontroly; žádné datum či vlastní vklad nedoplňujeme odhadem. Celkem 15/20 rozhodnutí, osm původních pozitivních predikcí správně, dvě čekají. Purple zůstává v původní matici abstencí. Podrobnosti `review/round-05.md`.

## Šestá skutečná ruční kontrola — 22. 10. 2026

Uživatel zařadil J&T a Reflex a vyřadil Startovač. Zapsáno 18/20 rozhodnutí; všech deset původních pozitivních predikcí je potvrzeno. Výsledek platí pro záměrně vybraný vzorek. Zachováno rozlišení celkové velikosti kola grid.online od neznámých vlastních vkladů. Nový odkaz na kontaktní stránku Reflex je zachycen jako podklad uživatele v `review/round-06.md`. Čas kontroly nezměřen.

## Sedmá skutečná ruční kontrola — 22. 10. 2026

Uživatel vyřadil CVCA jako asociaci a Startupstart jako propojovací platformu. Dokončeno 20/20 referenčních klasifikací, 11 include a 9 exclude. Původní precision 10/10 a recall 10/11 v tomto účelovém vzorku. Atributová přesnost zůstává nezměřena, čas kontroly neznámý. Finální nativní export konverzace je stále samostatný zbývající krok; průběžný filtrovaný snapshot za něj nevydáváme. Viz `review/round-07.md`.

## Pokus o nativní export — 22. 10. 2026

Na pokyn uživatele AI ověřila oficiální dokumentaci a dostupnost Codex CLI, poté zkusila otevřít konkrétní existující relaci pouze pro export. První pokus narazil na zápis provozního stavu mimo sandbox; druhý s potřebným oprávněním a --no-daemon načetl historii, ale CLI ohlásilo zámek kvůli otevření v desktopové aplikaci. Nebyla spuštěna inference, fork ani nový agent. CLI ukončeno q. Nativní export nevznikl. Přesný postup pro dokončení po zavření desktopové relace je v ai-log/README.md; stav vydání zůstává awaiting_final_native_conversation_export.

## Dodání exportu uživatelem — 22. 10. 2026

Uživatel předal Markdown export konverzace v příloze. AI ověřila začátek, konec, přítomnost posledního kontrolního kola a vzory přihlašovacích údajů. Pro veřejnou verzi odstranila celé technické bloky nástrojů včetně vrácených instrukcí a anonymizovala domovské cesty; veřejné zprávy nebyly rekonstruovány. Výsledek conversation-export.md, kontrolní součty a přesné počty úprav v export-manifest.json. Způsob spuštění nativního exportu nelze ze souboru nezávisle potvrdit. Soubor končí před jeho předáním zpět asistentovi.

## Databázové ověření na pokyn uživatele — 22. 10. 2026

Doplněno pět testů nad novým SQLite exportem se skutečnými lidskými štítky: shoda s publikovaným SQL obsahem a JSON vstupy, opakovatelnost, peněžní význam a odmítání čtyř neplatných zápisů. Doplněn samostatný read-only audit sedmi invariantů a jeho spuštění v CI. Lokálně všech 22 testů a audit prošly. Limity SQL schématu a nutnost zapnutí FK na každém spojení jsou výslovně popsané v reports/DATABASE_TESTING.md.

## Finální opravy - 22. 10. 2026

Uživatel poskytl podrobné nové zadání finálních oprav. Pracoval jeden asistent bez subagentů. Odděleny původní a aktuální predikce AI od lidské reference, definována publikace shodou AI a člověka, odstraněn nejednoznačný příznak human_verified a doplněna odvozená klasifikační a atributová ověření. Připraven předem pevný audit 18 tvrzení bez vyplnění lidských rozhodnutí. AI otevřela oficiální a institucionální zdroje pro devět chybějících kapitálových údajů; nové pomocné částky nejsou současným AUM. Rozsah hledání je v reports/CAPITAL_RESEARCH.md. Odstraněna povinná kontrola exportu konverzace. Výsledky skutečných lokálních kontrol a omezení CI jsou v reports/FINAL_CHECKS.md. Nebyl proveden push ani změna vzdáleného repozitáře.

## Zápis lidského atributového auditu - 22. 10. 2026

Uživatel dodal tabulku 18 tvrzení se štítky a důvody. Na dotaz na původ, kontrolora a skutečné datum odpověděl „Ferstl 22.10.2026“. AI zapsala dodané výsledky s tímto označením a datem do review/claims.csv; nedoplňovala žádné vlastní lidské rozhodnutí. Dvanáct supported potvrzuje oporu ve zdroji u vyřešených tvrzení, šest uncertain zůstává mimo jmenovatel přesnosti. Neurčité mandáty Reflex, nedostupné úplné stránky CVCA a sporný význam fund_closed_size nejsou prohlášeny za chyby ani za ověřená fakta. Oba tickety Purple mají potvrzený přepis zdrojů, ale jejich rozpor a současnost nebyly vyřešeny. Čas kontroly nebyl dodán ani odhadován. Výsledky byly regenerovány; změny této etapy jsou lokální.

## Statický frontend - 23. 10. 2026

Uživatel výslovně rozšířil původní datový projekt o prohlížeč investorů s tabulkou, detailem, filtry, dohledatelnými zdroji a viditelnou nejistotou. AI pracovala bez subagentů. Náhled pracovního přehledu vznikl vestavěným Image Gen; sloužil pouze jako vizuální koncept, nikoli zdroj faktů. Vlastní implementace je HTML/CSS/JavaScript bez knihoven, nová část Python buildu sestavuje samostatný statický balíček ze skutečných dat. Frontend přebírá podmínku publikace a skutečně zapsané reference, nepřisuzuje AI kontrole nezávislost člověka.

Browser QA proběhla v Chromium pro desktop, tablet a mobilní viewport včetně přesné projektové cesty, URL, filtrů, exportů, focusu a chybových scénářů. Opravena dvojí obnova tabulky po změně historie, která rušila vrácený focus; absolutně umístěný přístupný caption dostal správného vlastníka scrollu, aby nerozšiřoval mobilní dokument. Testy zahrnuly škodlivé texty a URL v dočasně podvrženém datasetu; žádné takové řádky nebyly zapsány do skutečných dat. Zdrojové stránky nebyly hromadně ověřovány jako pravdivé ani dostupné.

První pokus vestavěného prohlížeče skončil timeoutem kvůli sandboxu lokálního serveru; po povoleném spuštění lokálního serveru mimo sandbox fungoval i náhled v aplikaci. Rozšířené testy využily lokální Playwright Chromium. Jednorázový lint DESIGN.md použil npm nástroj, bez přidání produkční závislosti. Počáteční statický audit nerozpoznával modulové addEventListener. Základní HTML nyní záměrně deaktivuje tlačítka do navázání obsluh, což současně zlepšuje chování při nenačteném JavaScriptu. Následný strict audit prošel bez nálezů; skutečné akce byly otestovány v prohlížeči. Workflow pro Pages se zveřejněním je připravené, ale vyžaduje výslovné ruční spuštění. Push ani nasazení nebyly provedeny. Souhrn ověření a pokyny jsou v README.

## Archivace další dodané konverzace - 23. 10. 2026

Uživatel dodal Markdown export „Dolaď databázi investorů“ a výslovně požádal o přidání na GitHub. AI zachovala starší exporty a připravila samostatný conversation-export-2026-10-23.md, který končí potvrzením pushe e3469cb. Vynecháno 22 technických bloků nástrojů včetně jejich výstupů, anonymizovány dvě zbývající domovské cesty a nahrazeny tři lokální obrazové odkazy textovými poznámkami. Žádné zprávy ani prompty nebyly rekonstruovány. Skutečné texty obou dříve dodaných zadání byly přidány samostatně do ai-log/prompts; původní export na ně obsahuje jen lokální odkazy. Manifest obsahuje hashe původních příloh i zveřejněných kopií a rozsah redakcí. Kontrola vzorů API klíčů, GitHub tokenů, soukromých klíčů a interních instrukčních značek v publikovaném textu nic nenalezla. Archiv není vydáván za kompletní historii všech chatů účtu. Tento záznam ani současná žádost nejsou zpětně připsány do dodaného transcriptu. Publikaci commitem a pushem uživatel autorizoval v aktuálním požadavku.

## Dotažení před odevzdáním — 28. 10. 2026

Uživatel schválil všechny čtyři připomínky z kontroly projektu. Opraven popis necommitnutých filtrů, historické kontroly přesunuty do archivu, JavaScript testy přidány do push CI. Pages po úspěšných kontrolách nasazuje push do main; ruční spuštění zůstává. Data ani uživatelská hodnocení se nemění. Nasazení se dokládá konkrétním během a commitem.
