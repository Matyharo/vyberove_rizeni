---
version: alpha
name: "Databáze investorů"
description: "Český pracovní přehled investorů a důkazů s viditelnou nejistotou."
colors:
  primary: "#17685b"
  background: "#f5f7f7"
  surface: "#ffffff"
  text: "#172e32"
  muted: "#526568"
  border: "#dce4e4"
  warning: "#805012"
  warningBackground: "#fff3df"
typography:
  sans:
    fontFamily: '"Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif'
  numeric:
    fontFamily: '"Segoe UI", system-ui, sans-serif'
rounded:
  DEFAULT: "6px"
spacing:
  section-gap: "24px"
  page-max: "1600px"
components:
  table: {}
  button: {}
  drawer: {}
  status: {}
---

# Investor evidence browser

## Overview

Pracovní registr pro českého hodnotitele praktické úlohy. První úkol: porovnat investory, poté dohledat význam částky a její zdroj. Registr má připomínat výzkumný pracovní list, nikoli investiční reklamu. Jediným výraznějším prvkem je evidence zdroje přímo pod konkrétním údajem. Žádné grafy, fotografie, externí fonty, přihlášení nebo editace dat.

Vizuální koncept vznikl nástrojem Image Gen jako náhled hlavního přehledu s detailem Purple. Koncept určuje kompozici a jazyk rozhraní, nikoli fakta: názvy, částky a data v aplikaci pocházejí výhradně z pipeline. Odlišné skutečné hodnoty mají přednost před ilustračním textem konceptu. Barvy a komponenty sdílí přehled, detail, metodika a exporty.

Runtime vlastní `frontend/style.css`. Tento dokument zrcadlí přijaté tokeny; nepřidává druhou generovací vrstvu. Mapping: colors.primary -> --accent; background -> --background; surface -> --surface; text -> --text; muted -> --muted; border -> --border; warning -> --warning; warningBackground -> --warning-bg. Typografie -> --font-body / --font-numeric; radius -> --radius. Odvozené odstíny hover, focus a scrollbaru jsou definovány pouze v témže :root.

## Colors

Bílý obsah na světle šedém vnějším pozadí. Petrolejové odkazy a focus, jemně zelená vybraná řádka. Jantarový stav vždy s textem vysvětluje omezení, nikoli chybu investora. Barva nikdy nenese význam sama. Výhradně světlé téma, respektování systémových vynucených kontrastů.

## Typography

Lokální systémový font s českou diakritikou. Nadpis 26-34 px, text aplikace 14 px, tabulka 13 px, pomocné texty 11-12 px. Peněžní hodnoty používají tabulární číslice. České formátování přes Intl, data v UTC pro bezpečné zobrazení date-only hodnot. Původní měny bez kurzových přepočtů. Zkratky AUM a ticket vždy dostanou lidské vysvětlení.

## Layout

Desktop: jedno přehledové plátno, čtyři souhrnné metriky, pás filtrů a sémantická tabulka. Všech 11 záznamů je záměrně vykresleno najednou; jde o omezený pilot, nikoli neomezený katalog. Výsledky mají přirozenou výšku dokumentu. Tabulka vlastní pouze vodorovný overflow, ostatní obsah nepřebírá její rozměry. Do 1100 px jsou filtry ve dvou sloupcích, do 640 px v jednom; metriky zůstávají ve dvou. Detail na mobilu vyplňuje viewport, na desktopu je v pravé části. Žádná skrytá akce závislá na hoveru.

## Elevation & Depth

Jemné dělicí čáry místo karet pro každý záznam. Jediný výraznější stín patří modálnímu detailu. Overlay neodsouvá přehled a pozadí je inertní pomocí native dialog showModal().

## Shapes

Ovládací prvky mají společný poloměr 6 px, datové řádky jsou pravoúhlé. Malé obdélníkové štítky jsou jen pro stav konkrétního údaje. Žádné dekorativní ikony ani samostatné symbolické logo.

## Components

- Tabulka: nativní table, řazení názvu tlačítkem s aria-sort. Název a akce Zobrazit jsou odkazy na stejný detail.
- Select: záměrně nativní select. Geometrii otevřeného popupu vlastní operační systém; nemáme vlastní listbox ani závislosti.
- Search: označený input, vlastní tlačítko vymazání, lokální vyhledávání bez diakritiky a IME-safe input.
- Dialog: společný modální drawer pro investora, metodiku a exporty. Close, Escape, návrat focusu, inertní pozadí, URL a Zpět jsou společná implementace v app.js.
- Zdroj: jedna DOM konstrukce sourceBlock, bezpečně ověřené http/https URL, nový panel s noopener. Hodnoty se vkládají textContent nebo createTextNode.
- Stavy: načítání, chyba s retry, prázdný dataset i výsledek filtrů, selected, hover, focus-visible. Změna počtu výsledků přes live region. Žádné native alert/confirm/prompt.
- Scrollbary: globální standardní i WebKit baseline, track/thumb/hover/active tokeny a forced-colors alternativa.
- Motion: pouze indikátor načítání; při reduced-motion je animace vypnuta. Žádné přechody, které zdržují práci.

## Do's and Don'ts

- U každé částky zachovat rozsah, měnu, datum a zdroj. Ověření klasifikace nepřenášet na atributy.
- Původ reference pojmenovat jako uživatelem dodanou kontrolu, kterou AI zapsala.
- Nikdy nevytvořit společný ticket ze dvou rozporných rozsahů.
- Historickou referenci ani cíl fundraisingu nevydávat za současné AUM.
- Filtry používají explicitní navigační kategorie z Python pipeline se stopou na původní tvrzení a jejich stav; kategorie nejsou nezávislé ověření mandátu.
