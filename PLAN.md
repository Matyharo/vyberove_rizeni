# Plán: spolehlivá databáze investorů

Verze 1, vytvořeno 22. 10. 2026 před sestavením pilotu.

## 1. Cíl a jednotka záznamu

Databáze má doložit, kdo skutečně investuje do soukromých firem, do čeho a s jakým mandátem. Není katalogem firem s výrazem „capital“ v názvu. Jednotkou je investiční organizace nebo veřejně působící individuální investor. Správce a jeho fondy vedeme odděleně, propojené identifikátorem; pět fondů jednoho správce není pět nezávislých investorů. Právní sídlo, kancelář a investiční geografie jsou různé atributy.

## 2. Pravidla zařazení

Globální rozsah: VC, private equity, family offices s doloženými přímými investicemi, angels a soukromí investoři s veřejně doloženými transakcemi do firem. Velikost osobního majetku není důkazem investiční činnosti ani investičním kapitálem.

Pro přijetí musí subjekt splnit všechny podmínky:

1. Rozlišitelná identita: oficiální web, jednoznačný název, geografie a podle dostupnosti právní identifikátor.
2. Doložená přímá kapitálová nebo konvertibilní investice do alespoň jedné pojmenované firmy. Pouhé tvrzení „investujeme“ nestačí.
3. Určitelný typ investora z jeho mandátu a transakcí. Při překryvu použijeme více kategorií a zdůvodnění.
4. Dostupný veřejný důkaz a datum kontroly; k aktivitě také datum oznámení nebo transakce, jsou-li zveřejněna.

Aktivita: oznámená investice v posledních 24 měsících znamená `recent_activity_evidenced`. Starší doložený investor může být přijat jako `historical_activity_only`; nebudeme jej vydávat za aktuálně investujícího. Nezjištěná nedávná transakce není důkazem neaktivity.

Vyloučíme poradce, právníky, asociace, databáze, crowdfundingové zprostředkovatele, samotné akcelerátory bez přímé investice, grantové programy, bankovní úvěrové produkty a správce veřejně obchodovaných portfolií. Corporate VC je přípustné, má-li skutečný investiční mandát a transakce. Fondy fondů označíme zvlášť a mimo pilot přímých investorů.

Rozhodnutí má tři stavy: `include`, `exclude`, `needs_review`. Nejasný případ se nedostane do publikované tabulky ověřených investorů.

## 3. Pilot a výběr kandidátů

Pilot: organizace s doloženou českou kanceláří, které přímo investují venture kapitál. Nejde o všechny investory investující v Česku ani pouze o fondy právně domicilované v ČR. Důvod: lokální jazyk, dostupnost primárních zdrojů a zvládnutelná kontrola identity.

Před kontrolou zmrazíme seznam 20 kandidátů z veřejných seznamů CzechStartups/CzechInvest a plných i přidružených členů české CVCA. Zapíšeme přesnou metodu výběru a pořadí. Hraniční kandidáty ponecháme v rozhodovacím protokolu, aby nebyl výsledek tvořen jen z předem známých správných fondů. Pokud bude výběr záměrný, neoznačíme ho za náhodný ani reprezentativní.

Cíl pilotu: přibližně 10–15 přijatých organizací, nikoli předem garantovaný počet. Vyloučené a nejasné případy zůstávají auditovatelné. Počet se nesmí uměle doplňovat podle výsledků.

## 4. Důkazy a datový model

Každý údaj má vlastní vazbu na zdroj, nikoli pouze jeden odkaz na řádek. Evidujeme URL, vydavatele, název stránky, datum publikace, datum kontroly, stručnou parafrázi důkazu a případné datum platnosti. Neznámé datum zůstává prázdné; datum návštěvy ho nenahrazuje.

Tabulky:

- `candidates`: identita, původ kandidáta, rozhodnutí a důvod.
- `investors`: název, typ, web, česká přítomnost, aktivita a vazby na důkazy.
- `claims`: investor, atribut, hodnota, jednotka, rozsah, stav ověření, source_id.
- `sources`: původ a data zdrojů.
- `transactions`: investor, portfolio firma, datum, druh data, zdroj; výše kola odděleně od příspěvku investora.
- `review`: původní rozhodnutí, kontrolní štítek, kontrolor, datum a zdůvodnění.

Povinné atributy: sektor, fáze a druh firem, obvyklá výše investice, investiční kapitál. U nezveřejněné hodnoty uvedeme `not_disclosed` nebo `not_found`, ne nulu a ne odhad AI. Změříme úplnost těchto atributů zvlášť od správnosti zařazení.

Peníze: původní měna, minimum/maximum, referenční období a explicitní druh veličiny: `manager_aum`, `fund_closed_size`, `fund_target_size`, `invested_to_date`, `dry_powder`. Cílový fundraising není získaný kapitál. Historicky získané fondy nesčítáme do současného AUM. Částka celého investičního kola není ticket jednoho investora. Pokud celkový kapitál není zveřejněn, řekneme to přímo.

## 5. Sběr a ověření

1. Discovery z veřejných asociací a ekosystémových seznamů.
2. Normalizace domén a názvů, kontrola duplicit a rozlišení značky/správce/fondu.
3. Primární zdroj investora pro mandát, ticket a kapitál; datované oznámení investice pro činnost.
4. U transakcí hledat potvrzení portfoliovou firmou nebo dalším nezávislým vydavatelem. Dvě kopie stejné tiskové zprávy nejsou dva nezávislé důkazy.
5. Rozpory uchovat jako různé výroky s datem a rozsahem. Novější údaj má přednost pouze při stejné veličině a srovnatelném rozsahu.
6. AI navrhuje extrakci s identifikátorem zdroje. Validátor kontroluje strukturu; člověk kontroluje význam. Struktura sama nedokládá pravdivost.

Veřejný přístup není automatické povolení k hromadnému kopírování. Respektujeme podmínky webů, limity přístupu a robots pravidla. Pilot uchová stručné faktické výpisky a odkazy; nebude publikovat celé cizí stránky. Osobní kontakty ani odhady majetku nejsou potřeba.

## 6. Měření přesnosti

Před opravami zmrazit predikce. U všech 20 kandidátů ručně stanovit referenční rozhodnutí podle stejných pravidel a otevřených zdrojů. Ideálně kontroluje uživatel bez zobrazení původního rozhodnutí AI. Do té doby jde pouze o kontrolu AI provedenou AI, nikoli nezávislé ruční měření.

Hlavní metrika: precision = TP / (TP + FP), kde pozitivní znamená „patří mezi VC s českou kanceláří a doloženou investicí“. Uvést počty i 95% Wilsonův interval; malý vzorek nedokazuje globální spolehlivost. Pokud nejsou žádná pozitivní rozhodnutí, precision je nedefinovaná.

Vedlejší metriky: matice záměn, recall pouze uvnitř kontrolovaného seznamu (ne pokrytí českého trhu), podíl nevyřešených případů, úplnost atributů, správnost jednotlivých tvrzení a podíl tvrzení s dohledatelnou oporou. U každé metriky uvést čitatel a jmenovatel. Rozhodnutí `needs_review` vykázat zvlášť, neskrýt je ze statistiky.

Oddělit původní výsledky a opravený dataset. Není přípustné změřit pouze již opravená data a prezentovat to jako původní výkon.

## 7. Odhad pokrytí a globálních nákladů

Zatím bez číselného odhadu: český seznam neumožňuje obhajitelnou extrapolaci na svět. Nejdřív zjistit počty institucí ve veřejných seznamech několika regionů a jejich překryvy. Angels a family offices mají zásadně horší veřejné pokrytí; neexistuje doložený úplný seznam všech soukromých investorů.

Výstupem bude interval počtu dohledatelných organizací podle typu a regionu, se zdrojem, datem a předpoklady. Nezaměníme dohledatelné instituce s celkovou populací. Spolehlivost identity, typu, ticketu a kapitálu odhadneme zvlášť.

Model nákladů: C = discovery + N_kandidátů × (získání zdrojů + extrakce + validace) + N_kontrol × ruční kontrola + deduplikace + provoz. API ceny ověřit k datu výpočtu; tokeny a lidský čas skutečně měřit na pilotu. Lidskou hodinovou sazbu označit jako scénář, nikoli pozorovanou cenu. Uvést nízký/základní/vysoký scénář a oddělit první sběr od čtvrtletní aktualizace.

## 8. Výchozí zdroje discovery

- CzechStartups: https://czechstartups.gov.cz/en/startup-ecosystem/investors/
- Česká CVCA: https://cvca.cz/en/membership/
- CzechInvest, popis CEE Funding Map: https://czechinvest.gov.cz/en/Homepage/News/May-2026/The-CEE-Funding-Map-provides-an-overview-of-active-investors-in-Central-and-Eastern-Europe

Kontrola dostupnosti ve vyhledávání: 22. 10. 2026. Tyto odkazy zatím nejsou důkazem správnosti jednotlivých investorů.

## 9. Pořadí realizace a hotový výsledek

1. Plán, datový model, pravidla a zmrazení kandidátů.
2. Sběr pilotu s auditovatelnými výroky a rozhodnutími.
3. Validátor, export CSV/JSON/SQLite a kontrolní přehled.
4. Skutečná ruční kontrola a výpočet metrik.
5. Odhad světového pokrytí a nákladů podložený zdroji a pilotem.
6. README, autentický export konverzací, kontrola reprodukovatelnosti a veřejný GitHub repozitář.

Termín odevzdání: 30. 10. 2026. Poslední den ponechat na kontrolu a odevzdání. V tomto commitu je hotový pouze plán; dataset, naměřená přesnost a globální odhad dosud neexistují.

## 10. Stav po technické etapě — 22. 10. 2026

Předchozí věta popisuje historický stav prvního commitu; aktuální stav je v README. Pilot má 20 kandidátů a zmrazené původní predikce. Následný přepis má 11 předběžně přijatých organizací, 8 vyloučených a 1 nevyřešenou identitu. CSV, SQLite, metriky, validační kód a rozpočtové scénáře jsou připravené; 17 testů lokálně prochází.

Upřesnění české přítomnosti: zdroj musí uvádět office/kontaktní adresu nebo deklarované ústředí a primární lokalitu. Samotná česká investiční geografie, registrace fondu či bydliště partnera nestačí. Provoz kanceláře nebyl fyzicky ověřen.

Globální rozsah je zatím zdrojově ukotvený plánovací interval, nikoli změřený světový soupis. Lidský čas a API spotřeba nejsou měřeny; rozpočet používá transparentní předpoklady. Přesnost proti člověku zůstává nezměřená. Uživatel si vybral společnou ruční kontrolu zdrojů v chatu. Nezodpovězené štítky AI nevyplňuje.
