# Výsledek měření

Precision původních pozitivních klasifikací: **10/10 na záměrně vybraném vzorku** (100.0%).

Zkontrolováno člověkem: 20/20 kandidátů. Precision TP/(TP+FP).

Recall v kontrolovaném seznamu: 10/11 (90.9%). Původní abstence u Purple s lidským include snižuje recall; opravená AI predikce nepřepisuje původní měření.

Výsledek precision neznamená 100% správnost celé databáze ani odhad přesnosti na světovém trhu. Správnost atributů se měří odděleně; úplnost měří dostupnost údajů, nikoli jejich pravdivost.

Lidský audit atributů: 18 kontrol, 12 supported, 0 incorrect, 6 uncertain. Shoda vyřešených tvrzení s lidskou referencí: 12/12. Uncertain jsou mimo jmenovatel; nejde o potvrzení všech kontrolovaných ani všech databázových atributů. Supported u historického nebo rozporného údaje potvrzuje oporu v příslušném zdroji, nikoli současnou platnost či vyřešení rozporu. Podklady: [CLAIM_AUDIT.md](CLAIM_AUDIT.md).

Bez lidské kontroly neuvádíme procento přesnosti. Automatická validace kontroluje strukturu, nikoli pravdivost.

## Úplnost přijatých organizací

Počítají se jen tvrzení se stavem supported; historické a částečné hodnoty jsou v datech, ale tuto úplnost nezvyšují.

| Pole | Doloženo |
|---|---|
| sectors | 10/11 |
| stage | 10/11 |
| ticket | 8/11 |
| total_investment_capital | 2/11 |

Úplné výsledky, abstence, nezkontrolované pozitivní predikce a matice záměn: [metrics.json](../exports/metrics.json).

Wilsonův interval je při malé záměrné vzorce pouze popisný. Nejde o odhad celosvětové přesnosti ani recall trhu.
