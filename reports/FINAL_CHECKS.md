# Aktuální ověření — 28. 10. 2026

Filtry jsou commitnuté a pushnuté v `ee46be42985757ffe9a6eb360e5070e899ef00d6`. Jeho [Python CI](https://github.com/Matyharo/vyberove_rizeni/actions/runs/40191344487) prošlo. Starší formulace o necommitnutých filtrech již neplatí.

## Lokální kontroly

Validate, databázový audit, 34 Python testů, 5 JavaScript testů, build a check-release prošly. Datové vstupy a uživatelská hodnocení se v této etapě nemění. Technické testy nepotvrzují pravdivost externích tvrzení.

## CI a publikace

Validace při každém pushi i PR zahrnuje Python a JavaScript. Pages po úspěšném buildu a kontrolách automaticky nasazuje push do `main`; ruční spuštění zůstává možné. PR nic nepublikuje.

Aplikační verze `4487fb744a0949082e9e236987a99a0acb3392d6` má úspěšné [CI](https://github.com/Matyharo/vyberove_rizeni/actions/runs/40654005018) i [Pages nasazení](https://github.com/Matyharo/vyberove_rizeni/actions/runs/40654005133). Web a všech sedm kontrolovaných souborů odpověděly HTTP 200. HTML, JavaScript, CSS, data a exporty odpovídají lokálnímu buildu po normalizaci konců řádků Windows/Linux; čtyři soubory jsou byte-identické. [Přesný stav](PUBLICATION_STATUS.json), [porovnání souborů](LIVE_PACKAGE_CHECK.json). Následující dokumentační commit pouze zapisuje tyto výsledky; aplikační zdroje a data nemění.

## Omezení a historie

Šest nejistých atributových hodnocení zůstává otevřených. Původ ani metriky uživatelských referencí se nemění. Browser QA nebylo při této dokumentační a CI úpravě opakováno.

[Historické protokoly](FINAL_CHECKS_HISTORY.md), [strojové kontroly](FINAL_CHECKS.json), [databázový audit](DATABASE_AUDIT.json).
