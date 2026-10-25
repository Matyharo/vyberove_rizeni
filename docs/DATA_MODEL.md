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

## Lidské ověření a publikace

Pole human_verified bylo odstraněno ze zdrojových investorů a exportů, protože směšovalo dva druhy kontroly. Zdrojová data/pilot.json uchovávají fakta a rozhodnutí AI; lidské příznaky se při každém buildu odvozují ze skutečně dokončených řádků review/labels.csv a review/claims.csv, nikoli ručně udržovaných booleanů.

- classification_human_verified: true pouze při platné dokončené lidské klasifikaci include daného investora. Neznamená potvrzení atributů. Lidské exclude a needs_review se uchovávají v human_reviews; tento příznak pozitivního potvrzení je u nich false.
- attributes_human_verified: true pouze pokud existuje alespoň jedno nenulové faktické tvrzení investora a všechna jeho nenulová tvrzení mají dokončenou lidskou kontrolu supported. Jediné incorrect, uncertain nebo nekontrolované tvrzení znamená false. Týká se výhradně evidovaných claims, nikoli transakcí, právních registrací nebo záruky úplnosti světa.
- attribute_human_verified: příznak jednoho nenulového tvrzení s lidským supported. human_review_label zachovává také incorrect a uncertain; absence je null. V CSV/JSON claims jsou pole přímo, v SQLite je ekvivalentní pohled claim_verification navázaný na human_claim_reviews.
- published: současná AI include A ZÁROVEŇ lidské include. Původní zmrazená predikce publikaci neřídí, používá se k měření klasifikace. Bez lidské reference se nic nepublikuje. Normalizované investors CSV/JSON/SQLite zachovávají všechny evidované organizace a příznak; investor_summary a SQL pohled published_investors obsahují pouze publikované. Detailní sekce PILOT obsahují publikované, rozhodovací tabulka všechny kandidáty.

Úplnost se počítá pro publikované investory a z podporovaných nenulových údajů. Přesnost atributů zahrnuje pouze nenulová tvrzení s vyřešenou lidskou referencí supported/incorrect; uncertain se počítají mezi kontroly, ale ne do jmenovatele přesnosti. Kontroly null mají vlastní missing_value_reviews a nevstupují do přesnosti pozitivních tvrzení. Prázdná hodnota není automaticky chyba. Malý předem určený audit má samostatný výběr data/claim_audit_sample.json; jeho tabulka se generuje a původní lidské řádky zůstávají zachovány.

capital_reference nově rozlišuje také committed_capital, available_for_new_investments a fund_target_size. Tyto částky nejsou manager_aum a nezvyšují úplnost total_investment_capital. Datum validity u historického plánu znamená datum oznámeného plánu; null výslovně znamená neurčený referenční okamžik. Nová rešerše a nejistoty jsou v reports/CAPITAL_RESEARCH.md.

## Statický webový balíček

`investor_db/web.py` po validaci a sestavení exportů vytváří `site/data.json`. Obsahuje pouze organizace z publication_ids s explicitním published=true, jejich nezměněné claims a transakce, fondy, související zdroje, classification (původní/aktuální AI a skutečná reference), metriky a původ kontrol. Claims připojují review se štítkem, kontrolorem, datem a důvodem; příznaky se odvozují ze stejných vstupů jako běžné exporty. Poznámky AI se nestávají lidskou referencí.

Pole conflicts prezentuje již zaznamenané rozpory: různé nenulové hodnoty téhož pole, jejichž kurátorská poznámka výslovně uvádí rozpor. Obsahuje původní ID tvrzení. Historické alternativy samotné nevytvářejí současný rozpor. Pole nemění tvrzení, klasifikaci ani metriky.

JSON nemá proměnlivý čas sestavení ani data kontroly odvozená z návštěvy UI, takže opakovaný offline build je deterministický. Do site se kopíruje souhrnné CSV a metriky. Frontend data needituje ani nezapisuje lidské kontroly. Null zůstává null a zobrazuje se jako Nezjištěno.

## Navigační vrstva webu

Datový balíček obsahuje odvozené `navigation.sectors` a `navigation.stage`: ID, název, `claim_ids` a `source_statuses`. Pravidla jsou v [NAVIGATION.md](NAVIGATION.md). Původní tvrzení ani 18 atributových hodnocení se tím nemění.
