# Globální rozsah a náklady

Stav rešerše 22. 10. 2026. **Pracovní rozsah: přibližně 6 000–24 000 veřejně doložitelných investorů po kontrole 10 000–40 000 kandidátů.** Jde o scénář pro plánování, ne změřené pokrytí a ne odhad všech investorů na světě. Střední scénář je 12 000 přijatých z 20 000 kandidátů.

## Z čeho vychází řád velikosti

| Veřejný podklad | Co skutečně říká | Co z něj nelze tvrdit |
|---|---|---|
| [NVCA Yearbook 2026](https://nvca.org/2026-nvca-yearbook/) | 2 984 existujících VC firem v USA k 31. 12. 2025 | Není to počet všech amerických PE, angels ani všech aktivních investorů |
| [Invest Europe, annual activity statistics](https://www.investeurope.eu/publications-policy/publications/2025/activity-data-dashboard/) | Roční sběr pokrývá přes 1 750 evropských PE/VC firem | Počet reportujících není úplný trh ani seznam k volnému převzetí |
| [OpenVC, dokumentace filtrů](https://docs.openvc.app/en/articles/13228069-filter-the-right-investors), 22. 2. 2026 | Veřejně deklaruje přes 16 000 tech investorů; různé typy, ověřené i z veřejných zdrojů sestavené profily | Nejde o 16 000 unikátních VC správců, nezávisle ověřenou přesnost ani automatické svolení ke scrapingu |
| [Deloitte, Defining the Family Office Landscape 2024](https://www.deloitte.com/za/en/services/deloitte-private/about/defining-the-family-office-landscape.html) | Odhad 8 030 single family offices v roce 2024 | Nejde o rok 2026, veřejné jmenné záznamy nebo automaticky přímé investory do firem |

Všechny čtyři stránky byly otevřeny při rešerši 22. 10. 2026. Čísla **nesčítáme**: evropské, americké a globální katalogy se překrývají, mají různé definice a jednotky. Opakované pobočky a fondy téhož správce odstraníme. Hongkongský newsletter nalezený vyhledáváním nebyl po otevření čitelný kvůli ochraně webu, proto jeho počet členů nepoužíváme jako ověřený podklad.

Rozpětí kandidátů 10–40 tisíc vychází řádově z globálního katalogu přes 16 tisíc tech profilů, doplnění PE a méně zastoupených regionů a následné deduplikace. Přijetí 60 % je **pracovní předpoklad**, nikoli výsledek našeho záměrně kontrastního vzorku. Citlivost je velká: při 20 tisících kandidátů znamená přijetí 40/60/80 % databázi 8/12/16 tisíc záznamů. Interval 6–24 tisíc je obálka vybraných scénářů, nikoli statistický interval spolehlivosti.

## Kdo bude reálně dostupný

- **VC a PE:** nejlépe dosažitelné organizace s vlastním webem, portfoliem, tiskovými zprávami a asociačním profilem. První expanze: USA/Kanada a Evropa, dále Indie, Japonsko, Korea, Singapur a Austrálie; zbylé regiony podle dostupnosti lokálních zdrojů. Čínské, latinskoamerické, africké a MENA zdroje vyžadují zvláštní jazykové a lokální ověřování. Konkrétní počty po regionech zatím nejsou změřené.
- **Family offices:** jen veřejně vystupující kanceláře s doloženou přímou investicí. Investice do fondu nejsou důkazem přímého investování do firem. Z Deloitte nelze odvodit, kolik jmen splní naši definici. Pro rozpočet počítáme se stovkami až nižšími tisíci takových subjektů; jde o hypotézu k ověření, ne doložený výsledek.
- **Angels a velcí soukromí investoři:** jen osoby veřejně jmenované v konkrétní transakci a rozlišitelné od jmenovců. Případné členství v angel síti je discovery, ne důkaz transakce. Odhad majetku nebudeme používat jako dostupný investiční kapitál. Úplné světové pokrytí této kategorie není z veřejných zdrojů obhajitelné.

Nejdříve otestovat dalších 50 kandidátů na region a typ. Vyhodnotit dostupnost zdrojů, překryvy, čas a skutečnou přijatelnost; až poté zúžit globální interval. Capture–recapture zatím nepoužíváme: zdroje nejsou nezávislé a nemáme změřené překryvy.

## Očekávaná spolehlivost

Pro identitu a zařazení je návrhovým cílem precision alespoň 95 %. **Zatím to není naměřený výsledek.** Hraniční případy zůstávají v karanténě. Pilot je převážně český institucionální VC a neopravňuje přenést přesnost na soukromé osoby ani jiné regiony.

Podklady u jednotlivých polí mají jinou kvalitu. V českém pilotu je běžný ticket s oporou v aktuálně dostupném primárním zdroji a bez zjištěného rozporu u 8/11 organizací; srovnatelný celkový spravovaný kapitál pouze u 2/11, navíc self-reported a bez data ocenění. U Purple uvádí web 250–400 tis. EUR, firemní LinkedIn 250–500 tis. EUR; proto ticket do této úplnosti nepočítáme. To je úplnost, nikoli přesnost. Historické částky a velikosti jednotlivých fondů jsou dostupné častěji, ale jejich sloučení do současného AUM by bylo chybné. Nedoložené hodnoty zůstávají prázdné i při globálním rozšíření.

V produkci kontrolovat všechny nově přijaté identity člověkem a navíc náhodný audit již přijatých záznamů po regionech/typech. Pro představu: při 73 náhodně kontrolovaných pozitivních případech bez chyby je dolní hranice oboustranného 95% Wilsonova intervalu přibližně 95 %. Tento výpočet nelze použít na náš záměrný vzorek jako důkaz celosvětové přesnosti. Duplicity, zastaralost a správnost peněžních veličin vyhodnocovat zvlášť.

## Rozpočtový model

Všechny částky jsou v USD, bez měnových převodů a DPH. Kód výpočtu: `investor_db/costs.py`; vstupy: `data/cost_assumptions.json`; výsledek: `exports/cost_estimate.json`. Čísla níže jsou zaokrouhlená na celé dolary.

`první sběr = (počet kandidátů × strojový náklad + počet kandidátů × minuty kontroly / 60 × hodinová sazba + implementace + infrastruktura) × (1 + rezerva)`

| Předpoklad / výsledek | Nízký | Základní | Vysoký |
|---|---:|---:|---:|
| Kandidáti | 10 000 | 20 000 | 40 000 |
| Přijatí při předpokladu 60 % | 6 000 | 12 000 | 24 000 |
| Lidská kontrola každého kandidáta | 4 min | 8 min | 15 min |
| Kontrolor, USD/h | 25 | 35 | 50 |
| Celkem kontrola, hodiny | 667 | 2 667 | 10 000 |
| Strojové hledání/extrakce, USD/kandidát | 0,05 | 0,25 | 1,00 |
| Implementace, hodiny × USD/h | 80 × 50 | 160 × 50 | 320 × 75 |
| Infrastruktura prvního sběru, USD | 100 | 300 | 1 000 |
| Rezerva | 15 % | 20 % | 30 % |
| **První sběr celkem, USD** | **24 457** | **127 960** | **734 500** |
| **Za přijatý záznam, USD** | **4,08** | **10,66** | **30,60** |
| **Čtvrtletní aktualizace, USD** | **1 323** | **12 360** | **123 500** |

Čtvrtletní aktualizace předpokládá levnou strojovou kontrolu všech přijatých záznamů a lidskou kontrolu 10/20/35 % změněných případů v délce 3/5/10 minut. Nepočítá automaticky nové investory; ty stojí navíc podle prvního modelu. Fixní provoz aktualizace je 100/300/1 000 USD za čtvrtletí. Rozpočet pokrývá zjištění a evidenci zveřejněných údajů, nikoli získání neveřejného kapitálu nebo záruku úplnosti všech polí.

Strojové částky jsou **předpokládaná nákladová obálka**, nikoli ověřené API ceníky. Projekt nyní žádné placené API ani API klíč nepoužívá. Přímé náklady pilotního modelu/tokenů nejsou z této konverzace přiřaditelné ke každému záznamu. Ani lidský čas není zatím změřen: kontrola čeká na člověka. Po ručním pilotu nahradit předpoklady časomírou; při API implementaci přidat skutečnou spotřebu tokenů, cenu vybraného modelu a opakované pokusy. Tvrdit, že je dnešní rozpočet pilotem kalibrovaný, by bylo nepravdivé.

Hlavní náklad je kontrola kvality. V základním scénáři stojí lidská kontrola přibližně 93 333 USD před rezervou. Samotné zlevnění modelu proto nezlevní projekt o řád; důležitější je přesné vyhledání zdrojů, rozlišení entity a zkrácení času kontrolora.
