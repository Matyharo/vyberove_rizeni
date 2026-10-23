Doplň do existujícího projektu https://github.com/Matyharo/vyberove_rizeni profesionální, funkční frontend pro prohlížení databáze investorů.

Nejdříve přečti pokyny repozitáře, README, datový model, aktuální exporty a Python build. Potom řešení přímo implementuj a ověř v prohlížeči. Nezůstávej u návrhu.

## Cíl

Projekt je praktická úloha na pozici Junior AI Developer. Jeho hlavní hodnotou je spolehlivost údajů, dohledatelnost zdrojů a práce s nejistotou.

Frontend má hodnotiteli během první minuty ukázat:
- Kteří investoři jsou v publikovaném pilotu.
- Do čeho a v jakých částkách investují.
- Z čeho jednotlivé údaje vycházejí.
- Které informace chybějí, jsou historické nebo si odporují.

Vytvoř přehlednou aplikaci s tabulkou investorů a detailním panelem. Rozsah drž přiměřený hotovému datovému projektu.

## 1. Architektura a napojení dat

- Pokud projekt nemá frontendový stack, použij HTML, CSS a moderní JavaScript bez frameworku a bez zbytečných závislostí.
- Frontend musí fungovat jako statická aplikace připravená pro GitHub Pages.
- Data připravuj z existujícího Python buildu do jednoho vhodného JSON souboru. Názvy investorů, údaje, metriky ani počty nekopíruj ručně do UI.
- JSON musí zachovat publikovatelnost záznamů, tvrzení, zdroje, transakce, peněžní veličiny, nejistotu a skutečný původ ověření.
- Podmínky publikace přebírej ze současné pipeline. Frontend nesmí samostatně rozhodovat, kdo je ověřený investor.
- Vygeneruj úplný samostatný adresář webu včetně potřebných dat a exportů.
- Používej relativní cesty, aby aplikace fungovala také pod `/vyberove_rizeni/`.
- Žádný další backend, databázový server, přihlášení ani placené API.
- Build musí fungovat offline ze současných vstupních dat.

Zachovej existující CLI, exporty a reprodukovatelnost projektu.

## 2. Vizuální návrh

Vytvoř čisté analytické rozhraní připomínající kvalitní pracovní nástroj.

- Světlé pozadí, tmavý čitelný text, tlumená zelená nebo petrolejová jako hlavní akcent.
- Výrazná typografická hierarchie, promyšlené rozestupy a jemné oddělení obsahu.
- Upřednostni přehlednou tabulku před mřížkou velkých karet.
- Bez obřího marketingového úvodu, dekorativních grafů, generických ilustrací a zbytečných animací.
- Česká lokalizace včetně diakritiky, dat a formátování čísel.
- Texty stavů musí být srozumitelné i člověku, který nezná interní názvy polí.
- Pro pomlčky v českých textech používej znak `-`.
- Použij systémové písmo nebo lokálně dostupné fonty, bez závislosti na externí fontové službě.

V aplikaci zobrazuj užitečné informace o investorech. Technické podrobnosti buildu patří do README.

## 3. Hlavní přehled

V horní části zobraz:
- Název „Databáze investorů“.
- Krátký popis, že jde o pilot investorů s českou přítomností.
- Datum stavu dat převzaté z datasetu.
- Odkazy na metodiku, exporty a repozitář.

Přidej několik stručných ukazatelů odvozených z dat:
- Počet publikovaných investorů.
- Počet prověřovaných kandidátů.
- Dostupnost obvyklé výše investice.
- Dostupnost celkového spravovaného kapitálu.

Každý ukazatel musí mít jasný význam a případně čitatel i jmenovatel. Nezobrazuj obecný ukazatel „100% přesnost“.

Tabulka investorů:
- Název.
- Zaměření.
- Investiční fáze.
- Obvyklá výše investice.
- Celkový spravovaný kapitál, pokud je doložen.
- Upozornění na omezení údajů.
- Srozumitelná akce pro otevření detailu.

Použij stručné souhrny. Dlouhé texty zobraz v detailu.

## 4. Vyhledávání, filtry a řazení

Implementuj:
- Vyhledávání podle názvu a textu zaměření, bez rozlišení velikosti písmen a české diakritiky.
- Filtry podle sektoru a investiční fáze.
- Filtr dostupnosti údajů o ticketu nebo celkovém kapitálu.
- Řazení podle názvu.
- Počet aktuálně zobrazených výsledků.
- Tlačítko pro vymazání filtrů.
- Přehledný stav bez výsledků.

Filtry kombinuj a jejich volby odvozuj z dat. Zachovej význam částečných nebo odvozených údajů; nevytvářej zdání přesné klasifikace tam, kde chybí.

Částky v různých měnách nesrovnávej číselným řazením bez stanoveného kurzu a data. Měnové převody pro tuto verzi nezaváděj.

## 5. Detail investora

Kliknutím otevři postranní panel na desktopu a vhodný celostránkový detail na mobilu.

Detail musí obsahovat:
- Název a oficiální web.
- Typ investora a doloženou českou přítomnost.
- Sektory, investiční fáze a geografii.
- Běžný ticket s měnou a vysvětlením významu rozpětí.
- Kapitálové údaje s přesným označením veličiny.
- Konkrétní doložené investice do pojmenovaných firem.
- Zdroj, datum kontroly a dostupné datum publikace nebo platnosti.
- Stručné důvody zařazení a omezení důkazů.

U jednotlivých atributů umožni snadno zobrazit zdroj a poznámku. Stav ověření připojuj ke konkrétnímu údaji.

Rozliš:
- Celkový spravovaný kapitál organizace.
- Velikost konkrétního fondu.
- Cíl fundraisingu.
- Historicky proinvestovanou částku.
- Disponibilní kapitál, pokud je skutečně doložen.
- Částku celého investičního kola a vlastní příspěvek investora.

Null zobrazuj jako „Nezjištěno“, nikoli 0. Stav `not_found` neprezentuj jako důkaz, že údaj nebyl nikdy zveřejněn.

## 6. Nejistota a rozpory jako hlavní přednost

Viditelně a věcně rozliš:
- Doloženo zdrojem.
- Částečně doloženo.
- Odvozeno.
- Historický údaj.
- Údaj bez data platnosti.
- Rozpor mezi zdroji.
- Nezjištěno.

Stavy nesmějí být rozlišitelné pouze barvou. Přidej krátké vysvětlení jejich významu.

Zvláštní pozornost věnuj Purple Ventures:
- Zobraz obě doložená rozpětí ticketu.
- U každého zachovej jeho zdroj.
- Vysvětli, že se zdroje liší a aktuální platnost není vyřešena.
- Nevytvářej nové sjednocené rozpětí.

Také historické údaje Credo a Tensor nesmějí vypadat jako potvrzené současné hodnoty.

Nepřebírej automaticky označení „lidské ověření“ pouze z názvu souboru nebo pole. Původ kontroly musí být doložený. Pokud existující dokumentace zaměňuje kontrolu asistenta za osobní kontrolu člověkem, popiš a oprav tuto nesrovnalost bez vymýšlení nového kontrolora nebo lidských rozhodnutí. Zachovej původní záznam a historii změny.

## 7. Metodika a exporty

Přidej stručnou sekci nebo samostatný panel „Metodika a kvalita dat“:
- Pravidla zařazení.
- Rozlišení investora, správce a fondu.
- Význam zdrojů a dat.
- Rozdíl mezi přesností klasifikace a úplností atributů.
- Omezení malého záměrného vzorku.
- Omezení aktuálnosti a veřejné dostupnosti údajů.

Pokud zobrazíš precision nebo recall, uveď jejich konkrétní rozsah, čitatel a jmenovatel. Nejisté případy nezaměňuj za prokázané chyby ani potvrzené údaje.

Umožni stáhnout existující publikovaný přehled CSV a relevantní JSON. Odkazy musí fungovat ve výsledném statickém webu. Export jasně označ jako celý publikovaný dataset nebo aktuálně filtrovaný výběr podle skutečného chování.

## 8. Přístupnost a interakce

- Responzivní zobrazení pro mobil i desktop.
- Sémantické HTML a správné popisky formulářů.
- Dostatečný kontrast a viditelný focus.
- Plná obsluha klávesnicí.
- Detail musí jít zavřít tlačítkem i klávesou Escape.
- Po zavření vrať focus na prvek, který detail otevřel.
- Pokud je detail modální, správně řiď focus a přístupnost pozadí.
- Umožni přímý odkaz na investora přes URL a správné chování tlačítka Zpět.
- Funkční stavy načítání, chyby načtení dat a prázdných výsledků.
- Datové texty bezpečně vkládej jako text. Zdrojové URL ověřuj a nepovoluj nebezpečná schémata.

## 9. GitHub Pages a dokumentace

- Připrav sestavení a workflow pro GitHub Pages kompatibilní se současným CI.
- Zachovej dosavadní validační kontroly.
- Před sestavením webu ověř vstupní data.
- Do README doplň jednoduchý postup lokálního spuštění přes HTTP server, sestavení a publikace.
- Pokud je nutné ručně změnit nastavení Pages v GitHubu, uveď přesný zbývající krok.
- Nevymýšlej veřejnou URL jako již funkční. Dostupnost potvrď až skutečným ověřením.
- Veřejné nasazení ani push neprováděj bez autorizace v aktuální relaci.

## 10. Ověření hotového výsledku

Spusť existující testy, validaci, build a audit databáze.

Frontend skutečně otevři v prohlížeči a ověř:
1. Shodu publikovaných investorů s datovou pipeline.
2. Vyhledávání včetně diakritiky.
3. Kombinaci filtrů, jejich reset a prázdný výsledek.
4. Detail investora, Escape, focus a navigaci Zpět.
5. Obě rozporná rozpětí Purple.
6. Správné označení chybějících a historických částek.
7. Funkčnost zdrojových odkazů a exportů.
8. Mobilní i desktopové rozložení.
9. Fungování pod cestou `/vyberove_rizeni/`.
10. Absenci chyb v konzoli.

Doplň jen přiměřené regresní testy důležitého chování. Ověř, že opakovaný build nepřepisuje existující kontrolní záznamy.

Pokud nějaké ověření nemůžeš provést, napiš přesně které. Netvrď, že jsi aplikaci otestoval v prohlížeči, pokud jsi ji pouze přečetl v kódu.

## Výsledek práce

Dodej dokončenou implementaci. Na závěr stručně uveď:
- Co frontend umí.
- Jak jej spustit.
- Jaké kontroly skutečně prošly.
- Co zbývá pro veřejné zpřístupnění.
- Jaká omezení zůstávají.

Běžné implementační a vizuální volby rozhodni samostatně podle těchto požadavků.