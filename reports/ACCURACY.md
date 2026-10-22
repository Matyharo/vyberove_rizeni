# Výsledek měření

Precision původních pozitivních klasifikací: **10/10 na záměrně vybraném vzorku** (100.0%).

Zkontrolováno člověkem: 20/20 kandidátů. Precision TP/(TP+FP).

Recall v kontrolovaném seznamu: 10/11 (90.9%). Původní abstence u Purple s lidským include snižuje recall; opravená AI predikce nepřepisuje původní měření.

Výsledek precision neznamená 100% správnost celé databáze ani odhad přesnosti na světovém trhu. Správnost atributů se měří odděleně; úplnost měří dostupnost údajů, nikoli jejich pravdivost.

Audit pozitivních faktických tvrzení: 0 lidských kontrol; přesnost nezměřena. Podklady: [CLAIM_AUDIT.md](CLAIM_AUDIT.md).

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
