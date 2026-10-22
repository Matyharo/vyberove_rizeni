# Datový model a význam výstupů

`data/pilot.json` je hlavní vstup pipeline; `research/curate_pilot.py` je původní transparentní přepis rešerše. Pro další aktualizace upravujte JSON a přidávejte nové výroky; znovuspuštění přepisu by aktualizace přepsalo. Přepis není automatický webový crawler ani test výkonu extrakce LLM.

| Tabulka | Jednotka a vazby |
|---|---|
| candidates | Zmrazená značka/subjekt, discovery zdroj; všech 20, včetně vyřazených |
| investors | Investiční organizace, FK do kandidátů; neslouží jako seznam právních fondů |
| funds | Konkrétně pojmenovaný nebo vymezený fond, FK do organizace a zdroje; není kompletní právní struktura správců |
| claims | Jeden výrok o jednom atributu, hodnota, stav, rozsah, datum platnosti a FK do zdroje |
| sources | URL, vydavatel, název, publikace/přístup odděleně, stručná parafráze |
| transactions | Konkrétní firma a investiční důkaz; přesnost data a jeho význam; výše kola odděleně od příspěvku |
| transaction_sources | Další potvrzující zdroje; samotná existence dvou zdrojů ještě nedokazuje jejich nezávislost |
| decisions | Aktuální rozhodnutí AI, důvod a vazby na zdroje |
| initial_predictions | Původní rozhodnutí zmrazená před opravami |
| human_reviews / human_claim_reviews | Jen skutečně vyplněné lidské referenční štítky |
| out_of_scope_classifications | Samostatná evidence skutečných investorů mimo VC pilot; Genesis jako PE / growth equity, FK do kandidátů |

CSV exporty zachovávají source_id; URL lze dohledat v sources.csv. Přehled investor_summary.csv obsahuje přímo URL u jednotlivých souhrnných atributů. Vnořené hodnoty v plných CSV jsou serializované jako JSON, kódování UTF-8 s BOM. SQLite ukládá claim value jako JSON, aby neztratil původní měnu, rozpětí a null. Čtenářský přehled se všemi výroky je `reports/PILOT.md`.

Transakce s doloženým vlastním vkladem má také `contribution_source_id`, v SQLite cizí klíč do sources. Po ruční kontrole byl takto doplněn vklad i&i Bio 1,5 mil. USD do Sampling Human. Částka celého kola Tapaya zůstává oddělená a vlastní vklad DEPO je null. Samostatné klasifikace se exportují do `exports/out_of_scope.csv`.

## Stavy tvrzení

- `supported`: otevřený zdroj výrok podporuje. Neznamená nezávislý audit ani potvrzení člověkem.
- `inferred`: výslovně označená klasifikace odvozená AI z doložených faktů.
- `partial`: zjištěná jen část požadovaného atributu, ne úplný mandát.
- `historical_unconfirmed`: starší či časově neurčený údaj, jehož současnou platnost netvrdíme.
- `undated_reference`: pomocná peněžní veličina bez samostatného referenčního data.
- `not_found`: při omezené rešerši v uvedených zdrojích nezjištěno. **Není to důkaz nezveřejnění.**
- `not_disclosed`: zdroj výslovně říká, že údaj nezveřejňuje; pilot tento stav zatím nepoužívá.

Neznámé číselné hodnoty jsou null, nikdy 0. Datum publikace stránky není datem ocenění AUM. U zdrojů bez publikace je null. U investic známe někdy jen rok nebo datum indexu článku, což výslovně zaznamenáváme.

`total_investment_capital` je v pilotu operacionalizován jako souhrnný spravovaný kapitál organizace, pokud jej zdroj výslovně uvádí. Není to dry powder. Samostatné `capital_reference` uchovává velikosti fondů, historické AUM a historicky investované částky. Nesmějí se automaticky sčítat. Současné srovnatelné AUM má pouze KAYA a N1, obě self-reported bez data ocenění.

## Limity reprodukovatelnosti

Build je offline reprodukovatelný z uloženého přepisu, ne z živých webů. Zdroje se mohou změnit a nemusí být dostupné. Uloženy jsou pouze stručné parafráze; obsah zdrojů není archivován v plném rozsahu. Kontrola URL, hashů a cizích klíčů nedokazuje pravost výroků. Právní identity a regulatorní licence nejsou v této etapě nezávisle prověřeny v rejstřících.
