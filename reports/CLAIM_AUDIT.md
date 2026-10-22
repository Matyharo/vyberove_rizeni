# Malý lidský audit atributů

Předem pevný záměrný stratifikovaný výběr 18 pozitivních tvrzení napříč všemi 11 investory: 4 sektory, 4 fáze, 5 ticketů a 5 kapitálových údajů. Povinně zahrnuje oba rozporné tickety Purple, historický ticket Tensor, oba částečné mandáty Reflex, historický kapitál Credo, obě nesrovnatelné částky i&i Bio a obě současná self-reported AUM. Zbývající místa pokrývají další investory a typy atributů. Seznam ID je zmrazen v data/claim_audit_sample.json; nemění se podle výsledků kontroly. Výběr není náhodný a zvýrazňuje rizikové výroky.

Výběr byl stanoven před vyplněním lidských štítků. Jde o záměrný rizikový audit, nikoli reprezentativní odhad. Kontroly AI nejsou lidské štítky.

Vyplňte odpovídající řádky v review/claims.csv: label (supported / incorrect / uncertain), reviewer, reviewed_on a reason. Datum, identitu ani čas za kontrolora nedoplňujeme. Čas lze nově měřit; historický čas zůstává neznámý.

| ID tvrzení | Hodnota | Stav AI | Přesná URL | Kontrolní otázka | Lidský štítek |
|---|---|---|---|---|---|
| credo.sectors.1 | Bez pevné sektorové teze; technologičtí zakladatelé | supported | https://www.credoventures.com/ | Dokládá zdroj tento investiční mandát, nebo jde pouze o odvození z portfolia? |  |
| depo.sectors.1 | Defence; space; fintech; Industry 4.0; energie | supported | https://depoventures.com/ | Dokládá zdroj tento investiční mandát, nebo jde pouze o odvození z portfolia? |  |
| inibio.sectors.1 | Life sciences; drug discovery; medtech; diagnostika; AI ve zdravotnictví | supported | https://www.inibio.eu/ | Dokládá zdroj tento investiční mandát, nebo jde pouze o odvození z portfolia? |  |
| reflex.sectors.1 | Technologické firmy; mandát sektorů není na použité stránce formalizován | partial | https://www.reflexcapital.com/ | Dokládá zdroj tento investiční mandát, nebo jde pouze o odvození z portfolia? |  |
| inven.stage.1 | growth | supported | https://cvca.cz/en/inven-capital-2/ | Dokládá zdroj tento investiční mandát, nebo jde pouze o odvození z portfolia? |  |
| tilia.stage.1 | early-stage | supported | https://tilia.vc/ | Dokládá zdroj tento investiční mandát, nebo jde pouze o odvození z portfolia? |  |
| jt.stage.1 | pre-seed až Series A | supported | https://www.jtventures.cz/ | Dokládá zdroj tento investiční mandát, nebo jde pouze o odvození z portfolia? |  |
| reflex.stage.1 | startup / venture; přesné fáze nezjištěny | partial | https://www.jtventures.cz/blog/grid-online-prinasi-lepe-zaplacene-kuryry-levnejsi-dopravu-i-mene-aut-ve-mestech-rika-ondrej-kratky | Dokládá zdroj tento investiční mandát, nebo jde pouze o odvození z portfolia? |  |
| kaya.ticket.1 | 1,000,000-3,000,000 USD (ticket) | supported | https://www.kaya.vc/ | Dokládá zdroj celé rozpětí, měnu a význam ticketu? Porovnejte i alternativní tvrzení stejného investora. |  |
| nation1.ticket.1 | 100,000-1,000,000 USD (typical_first_investment) | supported | https://n1.rocks/ | Dokládá zdroj celé rozpětí, měnu a význam ticketu? Porovnejte i alternativní tvrzení stejného investora. |  |
| tensor.ticket.1 | 250,000-1,000,000 EUR (preferred_investment) | historical_unconfirmed | https://cvca.cz/en/tensor-ventures/ | Dokládá zdroj celé rozpětí, měnu a význam ticketu? Porovnejte i alternativní tvrzení stejného investora. |  |
| purple.ticket.1 | 250,000-400,000 EUR (initial_ticket) | partial | https://www.purple-ventures.com/ | Dokládá zdroj celé rozpětí, měnu a význam ticketu? Porovnejte i alternativní tvrzení stejného investora. |  |
| purple.ticket.2 | 250,000-500,000 EUR (initial_ticket) | undated_reference | https://cz.linkedin.com/company/purple-ventures | Dokládá zdroj celé rozpětí, měnu a význam ticketu? Porovnejte i alternativní tvrzení stejného investora. |  |
| credo.capital_reference.1 | 170,000,000 EUR (manager_aum) | historical_unconfirmed | https://cvca.cz/en/credo-ventures-2/ | Dokládá zdroj přesně částku, měnu, rozsah (fond/správce), typ kapitálu a datum? Nejde o cíl, historickou částku nebo proinvestovaný kapitál vydávaný za AUM? |  |
| inibio.capital_reference.1 | cca 47,000,000 EUR (fund_closed_size) | historical_unconfirmed | https://www.inibio.eu/news/experienced-businessmen-join-forces-with-excellent-science%2C-invest-%E2%82%AC2m-in-the-fund-at-the-iocb | Dokládá zdroj přesně částku, měnu, rozsah (fond/správce), typ kapitálu a datum? Nejde o cíl, historickou částku nebo proinvestovaný kapitál vydávaný za AUM? |  |
| inibio.capital_reference.2 | >53,000,000 EUR (fund_reported_managed_capital) | undated_reference | https://www.inibio.eu/news/experienced-businessmen-join-forces-with-excellent-science%2C-invest-%E2%82%AC2m-in-the-fund-at-the-iocb | Dokládá zdroj přesně částku, měnu, rozsah (fond/správce), typ kapitálu a datum? Nejde o cíl, historickou částku nebo proinvestovaný kapitál vydávaný za AUM? |  |
| kaya.total_investment_capital.1 | 500,000,000 USD (manager_aum) | supported | https://www.kaya.vc/ | Dokládá zdroj přesně částku, měnu, rozsah (fond/správce), typ kapitálu a datum? Nejde o cíl, historickou částku nebo proinvestovaný kapitál vydávaný za AUM? |  |
| nation1.total_investment_capital.1 | 60,000,000 USD (manager_aum) | supported | https://n1.rocks/ | Dokládá zdroj přesně částku, měnu, rozsah (fond/správce), typ kapitálu a datum? Nejde o cíl, historickou částku nebo proinvestovaný kapitál vydávaný za AUM? |  |

## Chybějící údaje - samostatná kontrola rozsahu hledání

Následující null nejsou pozitivní faktická tvrzení a nevstupují do přesnosti atributů. Nezjištěná hodnota není automaticky chyba. Rozsah nové rešerše: [CAPITAL_RESEARCH.md](CAPITAL_RESEARCH.md).

- credo.total_investment_capital.1: not_found; [credo-home](https://www.credoventures.com/).
- depo.total_investment_capital.1: not_found; [depo-home](https://depoventures.com/).
- inibio.total_investment_capital.1: not_found; [inibio-home](https://www.inibio.eu/).
- inven.total_investment_capital.1: not_found; [inven-home](https://www.invencapital.cz/).
- tensor.total_investment_capital.1: not_found; [tensor-home](https://tensor.ventures/).
- tilia.total_investment_capital.1: not_found; [tilia-home](https://tilia.vc/).
- purple.total_investment_capital.1: not_found; [purple-home](https://www.purple-ventures.com/).
- jt.total_investment_capital.1: not_found; [jt-home](https://www.jtventures.cz/).
- reflex.geography.1: not_found; [reflex-home](https://www.reflexcapital.com/).
- reflex.ticket.1: not_found; [reflex-home](https://www.reflexcapital.com/).
- reflex.total_investment_capital.1: not_found; [reflex-home](https://www.reflexcapital.com/).
