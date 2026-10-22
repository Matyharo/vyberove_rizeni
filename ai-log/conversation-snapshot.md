# Autentický výřez konverzace v Codexu

Tento soubor je mechanický export uživatelských a veřejných asistentských zpráv z lokálního záznamu této relace. Není přepisem vytvořeným z paměti ani nativním příkazem Claude /export.

Jde o průběžný snapshot: neobsahuje zprávy vzniklé po jeho vytvoření. Vyloučeny jsou interní instrukce, interní uvažování, technická metadata prostředí a surové výstupy nástrojů. Domovská cesta uživatele je nahrazena [USER_HOME]; vzory API klíčů by byly redigovány. Provedené kroky a opravy shrnuje ai-log/WORKLOG.md. Pro finální odevzdání doplnit nativní export po skončení práce.

## 2026-10-22T07:24:43.599Z — user

Dostal jsem se dál ve výběrovém řízení. Viz email:

Dobrý deň, pán Ferstl,

ďakujem za Vašu prihlášku na pozíciu Junior AI Developer. Rád Vám oznamujem, že postupujete do ďalšieho kola výberového konania. Jeho súčasťou je praktická úloha, ktorá nám ukáže, ako pristupujete k problému a ako pracujete s AI. Pripravil som dve zadania, vyberte si jedno z nich.

Pracovať môžete v Claude Code alebo v podobnom nástroji. Ak nestihnete všetko, uprednostnite podstatné časti a uveďte, čo v riešení chýba. V README prosím popíšte, ako ste s AI pracovali (aké pokyny dostali agenti, ako ste kontrolovali ich výstup a kde sa pomýlili). Ak Vám v zadaní niečo nebude jasné, rozhodnite podľa seba a v README zdôvodnite, prečo ste sa tak rozhodli. S otázkami sa na mňa môžete kedykoľvek obrátiť aj odpoveďou na tento e-mail.

ZADANIE A: Spoľahlivá databáza investorov

Úloha sa týka databázy investorov do firiem: VC fondov, private equity, family office, angel investorov a veľkých súkromných investorov. Kľúčová je spoľahlivosť dát: každý záznam musí byť skutočný investor, nie náhodná firma. Pri každom investorovi musí byť uvedené, v akom sektore pôsobí, do čoho bežne investuje a v akej výške, aký má celkový investičný kapitál a odkiaľ tieto informácie pochádzajú.

Začnite plánom. Z neho musí byť jasné, kto v databáze bude a kto nie, teda podľa akých pravidiel subjekt zaradíte alebo vyradíte. Popíšte tiež, ako overíte pravosť a správne zaradenie záznamov. Odhadnite, aký okruh investorov je možné z verejných zdrojov získať, približne koľko ich bude a aká bude spoľahlivosť dát. Uveďte, z čoho odhad vychádza.

Plán následne overte na menšej vzorke, napríklad na VC fondoch v jednej krajine. Pri každom zázname uveďte zdroj a dátum, ktoré dokladajú, že subjekt skutočne investuje. Na ručne overenej vzorke zmerajte presnosť. Na záver odhadnite náklady na rozšírenie na celý svet.

Používajte výhradne verejne dostupné dáta.

ZADANIE B: Konverzná landing page

Cieľom je landing page s porovnaním ETF obchodovaných na NYSE pre českého drobného investora, ktorý prichádza z reklamy na mobile a stránke venuje len niekoľko sekúnd. Stránka má fungovať ako lead magnet: ponúknuť návštevníkovi hodnotu a výmenou za ňu získať jeho kontakt. Pekný dizajn nestačí, stránka musí byť optimalizovaná na prínos kontaktov. Zároveň nesmie pôsobiť ako základný výstup od Claude. Dizajn aj texty majú byť premyslené pre túto cieľovú skupinu. Pri hodnotení sa budem riadiť hlavne otázkou, či by sme na ňu mohli zajtra spustiť reklamu.

Určte cieľovú skupinu, čo návštevník dostane výmenou za kontakt a v ktorom momente oň požiadate. Hodnota by mala byť zrejmá ešte pred vyplnením formulára. Navrhnite aj dve verzie reklamy. Prvá obrazovka stránky by mala nadväzovať na prísľub reklamy a okamžite komunikovať, čo návštevník získa.

Výber interaktívnych prvkov, napríklad porovnania fondov, kalkulačky poplatkov alebo skladania portfólia, nechávam na Vás. Každý z nich by mal viesť ku kontaktu. Formulár by mal mať čo najmenej polí. Premyslite aj to, čo návštevník dostane po jeho odoslaní.

Použite skutočné dáta s uvedením zdroja a merajte celú cestu od príchodu po odoslanie formulára. V README zdôvodnite poradie sekcií, uveďte očakávanú konverziu a tri hypotézy na A/B test zoradené podľa očakávaného dopadu. Stránku nasaďte na bezplatný hosting, napríklad Vercel.

Riešenie prosím zašlite do 30. 10. 2026 ako odpoveď na tento e-mail. Priložte odkaz na verejný repozitár na GitHube a pri zadaní B aj URL stránky. V repozitári by mal byť výsledok (pri zadaní A plán, dáta zo vzorky so zdrojom pri každom údaji a výsledok merania presnosti, pri zadaní B obe verzie reklamy), kód s priebežnou históriou commitov a v priečinku ai-log export konverzácií s Claude Code (príkaz /export).

Teším sa na Vaše riešenie.


## 2026-10-22T07:25:06.769Z — assistant

Tady už hodnotí hlavně **úsudek, kontrolu práce AI a schopnost dotáhnout řešení**, ne jen to, jestli dokážeš vygenerovat funkční kód. Termín je **30. října**, takže máme osm dní.

**Za mě bych předběžně volil zadání A.** Má jasně ohraničitelný pilot a můžeš na něm dobře ukázat vývojářské schopnosti: datový model, sběr dat, validaci, práci se zdroji a měření kvality. Silný výsledek může být menší databáze, kde každý údaj obstojí při kontrole. Největší past je zaměnit kapitál správce, velikost konkrétního fondu a běžnou výši investice nebo vydávat chybějící údaje za odhady bez opory.

**B bych vybral, pokud chceš předvést hlavně produktové myšlení a frontend.** Je vizuálně působivější, ale rozsah je větší, než vypadá: reklamy, návaznost první obrazovky, skutečná data, mobilní použitelnost, funkční sběr kontaktů, doručení slíbené hodnoty, analytika a nasazení. Navíc je potřeba ověřit, co přesně znamená nabídka ETF obchodovaných na NYSE pro českého drobného investora. To může zásadně ovlivnit obsah stránky.

U obou variant bych od začátku dodržel tyto zásady:

- **Nejdřív napsat rozhodnutí a kritéria úspěchu.** Až potom implementovat.
- **Commitovat průběžně** po smysluplných krocích, aby historie ukazovala skutečný postup.
- **Vést `ai-log` od první práce.** Uchovat původní konverzace a vedle nich stručný přehled pokynů, kontrol, chyb AI a oprav.
- **Oddělit ověřené výsledky od předpokladů.** U A například naměřenou přesnost od odhadu globálního pokrytí; u B skutečně otestované měření od očekávané konverze.
- **Nechat čas na nezávislou kontrolu a README.** Právě tam vysvětlíš, proč řešení stojí za důvěru.

Zadání výslovně připouští nástroj podobný Claude Code, takže Codex dává smysl. Požadavek na export ale nesmíme obejít vymyšleným přepisem: odevzdáme autentický záznam použitého nástroje a v README vysvětlíme jeho formát.

**Kterou variantu chceš zvolit — A, nebo B?** Pokud zatím váháš, napiš, jestli se chceš v tom výběrku profilovat spíš jako člověk na data a automatizaci, nebo na weby a produkt; podle toho rozhodneme.

## 2026-10-22T07:26:19.035Z — user

Můžeme A.


## 2026-10-22T07:26:23.776Z — assistant

Začnu plánem pro zadání A a zkontroluji pracovní složku. Pilot předběžně omezím na VC investory v Česku; v plánu stanovím pravidla zařazení, požadované důkazy a způsob měření přesnosti.

## 2026-10-22T07:26:52.162Z — assistant

První průzkum ukazuje důležitou past: veřejné seznamy míchají fondy, poradce, platformy i asociace. Použiji je proto jen k hledání kandidátů; zařazení bude vyžadovat důkaz konkrétní investice. Také oddělím velikost fondu, kapitál pod správou a cílovou částku fundraisingu, aby databáze nesrovnávala různé veličiny.

## 2026-10-22T07:28:37.864Z — assistant

Začali jsme zadáním A. Připravil jsem [plán projektu]([USER_HOME]/Desktop/Vyberove_Rizeni/PLAN.md), [README]([USER_HOME]/Desktop/Vyberove_Rizeni/README.md) a první Git commit.

Pilot zaměříme na **VC investory s českou kanceláří**. Plán stanoví pravidla zařazení, zdroje pro každý údaj a měření přesnosti. Chybějící kapitál přiznáme; cílovou velikost fondu nebudeme zaměňovat za skutečně získané peníze.

Dalším krokem je sestavení a zmrazení seznamu kandidátů před ověřováním. **Dataset ani výsledky měření zatím hotové nejsou.**

## 2026-10-22T07:30:51.291Z — user

Tak pokračuj.


## 2026-10-22T07:30:56.287Z — assistant

Sestavím seznam kandidátů, ověřím investory a doplním auditovatelný datový model, validátor a exporty. Výsledky kontroly AI oddělím od ruční kontroly člověkem, kterou budeš muset před odevzdáním skutečně provést.

## 2026-10-22T07:32:28.178Z — assistant

Seznam 20 kandidátů je uložený v samostatném commitu. Našel jsem i konkrétní problém ve zdroji: profil „Lighthouse venture“ na CzechStartups odkazuje na jinou doménu než český fond. Takové záměny zaznamenám v rozhodovacím protokolu. U Credo a DEPO se navíc aktuální investiční rozpětí na vlastním webu liší od údajů v asociaci; oba údaje zachovám s vysvětlením.

## 2026-10-22T07:34:15.268Z — assistant

Pilot už má podklady pro investiční zaměření i konkrétní transakce. U kapitálu se potvrzuje, proč musí mít každý údaj vlastní význam a datum: web může uvádět historicky proinvestovanou částku, velikost jednoho fondu nebo kapitál pod správou. Databáze je zachová odděleně a u nejasných údajů přizná omezení. Teď připravuji zpracování dat a kontrolní výstupy.

## 2026-10-22T07:42:26.474Z — assistant

Databáze nyní obsahuje 11 předběžně přijatých investorů, 8 vyloučených subjektů a 1 nevyřešenou identitu. Opravil jsem i vlastní přehlédnutí: adresu Purple Ventures jsem našel až v patičce webu; původní nerozhodnutý výsledek zůstal zachovaný pro měření.

Export do SQLite už funguje. Testy ještě odhalily problém se zavíráním databázového souboru na Windows, který opravuji.

## 2026-10-22T07:44:01.234Z — assistant

Všech 16 testů teď prochází. Základní výstupy i podklady pro ruční kontrolu jsou uložené v Git historii.

Ještě doplním odhad globálního rozsahu a nákladů a finální README. Pro autentický export této konverzace použiji také pokyny dovednosti `openai-docs`, abychom odevzdali skutečný záznam práce.

## 2026-10-22T07:49:08.693Z — user

<send_user_message_question_reply>
[{"questionItemId":"[\"request_user_input_async\",\"call_a5b777d225454b11afe49981d66082b7\",0]","question":"Pro skutečné měření přesnosti bude potřeba tvoje ruční kontrola zdrojů pro 20 kandidátů. Připravil jsem reports/REVIEW_PACKET.md bez rozhodnutí AI a review/labels.csv k vyplnění. Jak chceš kontrolu provést, až dokončím technickou část?","answer":"Projdeme zdroje společně v chatu"}]
</send_user_message_question_reply>


## 2026-10-22T07:49:14.797Z — assistant

Projdeme je společně v chatu. Dokončím podklady a pak ti budu dávat malé skupiny kandidátů s odkazy a jasnými kritérii; tvoje rozhodnutí zapíšu jako skutečné ruční hodnocení.

U Purple Ventures jsem teď našel další užitečný rozpor: vlastní web a firemní LinkedIn uvádějí rozdílnou horní hranici prvního ticketu. Českou adresu LinkedIn potvrzuje, ale investiční rozpětí označím jako nejednoznačné.

## 2026-10-22T07:54:04.190Z — assistant

Podklady jsou hotové: pilot, CSV a SQLite exporty, odhad globálních nákladů, README i autentický průběžný výřez konverzace. Prochází všech 17 testů. Kontrola odevzdání správně hlásí zbývající práci: naše ruční hodnocení, finální export konverzace a veřejný repozitář.

Uložím tuto etapu do historie a začneme prvními třemi kandidáty.

## 2026-10-22T07:54:30.901Z — assistant

Technická část je připravená v [README]([USER_HOME]/Desktop/Vyberove_Rizeni/README.md): data, zdroje, SQLite, odhad nákladů a 17 procházejících testů. Přesnost zatím poctivě uvádíme jako nezměřenou.

Začneme ruční kontrolou **3 z 20 kandidátů**. Otevři odkazy a posuď, zda jde o přímého VC investora s českou kanceláří a doloženou investicí do konkrétní firmy.

| Kandidát | Podklady |
|---|---|
| **Credo Ventures** | [Mandát a kancelář](https://www.credoventures.com/), [investice potvrzená Axoflow](https://axoflow.com/blog/7m-to-improve-security-data-quality) |
| **BDO Czech Republic** | [Popis činnosti v profilu CVCA](https://cvca.cz/en/bdo-czech-republic-s-r-o-2/) |
| **Lighthouse venture** | [Původní profil a jeho odkaz](https://czechstartups.gov.cz/investori_en/lighthouse-venture/), [český Lighthouse Ventures](https://lhv.vc/about-us/) — zkontroluj zejména totožnost subjektů |

**Jak rozhoduješ u každého: zařadit, vyřadit, nebo nelze rozhodnout?** Přidej krátký důvod; zaznamenám tvoje skutečné hodnocení.

## 2026-10-22T08:01:19.387Z — user

Credo Ventures - přímí investor do Axoflow s českou kanceláří v Praze
BDO Czech Republic - poskytují klientům služby v oblastech auditu, účetnictví, daní, práva, informačních technologií, digitalizace, finančního, transakčního a podnikového poradenství či znalectví.
Účastníme se mj. na lokálních a přeshraničních transakcích primárně s fondy Private Equity, dále pak s VC fondy a ostatními investory z řad strategických i rodinných. BDO napomáhá transakcím nejčastěji o velikosti stovek milionů až jednotek miliard Kč. Zároveň máme bohaté zkušenosti s poradenstvím u transakcí a firem z oblasti startupů a VC investic. 
Lighthouse venture - Ne, podle údajů na jejich webech jde o dva různé subjekty se stejným názvem Lighthouse Ventures.


## 2026-10-22T08:01:25.876Z — assistant

Zapíšu tvoje hodnocení: Credo zařadit, BDO vyřadit jako poradce a původního kandidáta Lighthouse vyřadit kvůli odlišné identitě. Potom přepočítám průběžné metriky a připravím další trojici.

## 2026-10-22T08:02:35.034Z — assistant

Zapsáno: **Credo zařadit, BDO vyřadit, původního Lighthouse vyřadit kvůli jiné identitě.** Máme hotové 3/20 kontrol.

Pokračujeme další trojicí. Kritérium zůstává: **přímý VC investor s českou kanceláří a konkrétní doloženou investicí**. Skutečný PE investor může být mimo tento VC pilot.

| Kandidát | Podklady |
|---|---|
| **DEPO Ventures** | [Investiční zaměření](https://depoventures.com/), [investice do Tapaya a kontaktní adresa](https://depoventures.com/latest/turning-any-smartphone-into-a-payment-terminal-czech-fintech-tapaya-has-raised-eur-1-million) |
| **i&i Biotech Fund** | [Strategie a portfolio](https://www.inibio.eu/), [pražská adresa a profil](https://cvca.cz/en/biotech-investments/) |
| **Genesis Capital** | [Typy investic a portfolio](https://cvca.cz/en/genesis-capital-equity-s-r-o-2/) |

U každého prosím napiš **zařadit / vyřadit / nelze rozhodnout** a stručný důvod.

## 2026-10-22T08:04:14.580Z — user

Do VC pilotu zařadit DEPO Ventures a i&i Biotech Fund. Genesis Capital evidovat samostatně jako PE / growth equity investora.





| Kandidát                       | Přímé VC investování                                                                                                                                                                                                 | Česká kancelář                                                                                                                                                                                                                          | Konkrétní doložená investice                                                                                                                                                                                                                                                                                                                                                                                                      | Verdikt                                |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| **DEPO Ventures**              | Ano. Investuje do raných technologických startupů a provozuje VC fondy.                                                                                                                                              | Plynární 10, Praha 7. ([DepoVentures.com](https://depoventures.com/?utm_source=chatgpt.com "Index"))                                                                                                                                    | **Tapaya, duben 2026** - DEPO se účastnilo jako spoluvedoucí investor pre-seed kola v celkové výši **1 mil. EUR**. Částka představuje celé kolo, nikoli samotný vklad DEPO. Potvrzuje ji přímo Tapaya. ([tapaya.com](https://www.tapaya.com/en/blog/tapaya-raises-1m-pre-seed-to-turn-any-device-into-a-payment-terminal?utm_source=chatgpt.com "Tapaya raises €1M pre-seed to turn any device into a payment terminal, Tapaya")) | **Zařadit**                            |
| **i&i Biotech Fund / i&i Bio** | Ano. Specializovaný early-stage VC fond pro biotechnologie, diagnostiku a medtech.                                                                                                                                   | Pobřežní 394/12, Praha 8 - kancelář investičního poradce **Biotech Investments, s.r.o.** Samotný fond sídlí v Lucembursku. ([inibio.eu](https://www.inibio.eu/?utm_source=chatgpt.com "i\&i Bio: early stage biotech venture capital")) | **Sampling Human, duben 2022** - fond oznámil vlastní investici **1,5 mil. USD** do vývoje buněčné diagnostiky. ([i&i Bio](https://www.inibio.eu/news/i%26i-bio-invests-%241.5-million-in-sampling-human-to-support-the-development-of-engineered-cells-for-single-cell-analysis?utm_source=chatgpt.com "i\&i Bio invests $1.5M in Sampling Human to support the development of engineered cells for single cell analysis"))      | **Zařadit**                            |
| **Genesis Capital**            | Přímý investor ano, ale doložené zaměření je **private equity a growth equity**, včetně akvizic a manažerských odkupů. ([Genesis Capital](https://www.genesis.cz/?utm_source=chatgpt.com "https://www.genesis.cz/")) | Na Šafránce 22, Praha 10.                                                                                                                                                                                                               | CVCA uvádí konkrétní portfoliové investice, například **Borcad CZ, TES Vsetín a Hecht Motors**. ([CVCA](https://cvca.cz/en/genesis-capital-equity-s-r-o-2/?utm_source=chatgpt.com "Genesis Capital Equity s.r.o."))                                                                                                                                                                                                               | **Mimo VC pilot - PE / growth equity** |



## 2026-10-22T08:04:25.340Z — assistant

Zapíšu DEPO a i&i Bio jako zařazené do VC pilotu a Genesis odděleně jako PE / growth equity investora. Ověřím také nové primární zdroje, které jsi doplnil, a zachovám rozlišení mezi celým kolem Tapaya a vlastním vkladem i&i Bio do Sampling Human.

## 2026-10-22T08:06:45.092Z — assistant

Zapsáno. **Máme zkontrolováno 6/20 kandidátů.** Genesis je samostatně veden jako PE / growth equity investor.

Doplnil jsem datum investice do Tapaya a vlastní vklad i&i Bio do Sampling Human. Česká kancelář poradce a lucemburský domicil fondu jsou oddělené. Všech 17 testů prochází.

Další trojice, se stejnými kritérii pro VC pilot:

| Kandidát | Podklady |
|---|---|
| **INVEN Capital** | [Mandát a kancelář](https://www.invencapital.cz/), [účast potvrzená Andercore](https://www.andercore.com/press/andercore-secures-40m-series-b-for-ai-driven-industrial-trade-platform) |
| **KAYA VC** | [Mandát a kanceláře](https://www.kaya.vc/), [investice do E2B potvrzená spoluinvestorem](https://www.insightpartners.com/ideas/e2b-raises-a-21m-series-a-to-offer-cloud-for-ai-agents-to-fortune-100/) |
| **ARX Equity Partners** | [Investiční zaměření a portfolio](https://cvca.cz/en/arx-equity-partners-2/) |

Prosím opět **zařadit / vyřadit / nelze rozhodnout**, se stručným důvodem.

## 2026-10-22T08:08:44.005Z — user

Do VC pilotu zařadit INVEN Capital a KAYA VC. ARX Equity Partners evidovat mimo pilot jako PE investora.





| Kandidát                | Přímé VC investování                                                                                                                  | Česká kancelář                                                                                                                     | Konkrétní doložená investice                                                                                                                                                                                                                                                                                                                    | Verdikt                |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| **INVEN Capital**       | Ano. VC fond zaměřený na **climate tech v Evropě a Izraeli**, s investicemi 2-30 mil. EUR.                                            | **Pod Křížkem 1773/2, Praha 4 - Braník**. ([invencapital.cz](https://www.invencapital.cz/?utm_source=chatgpt.com "Inven Capital")) | **Andercore, 11. 2. 2026** - společnost přímo potvrzuje vstup INVEN do Series B financování v celkovém objemu **40 mil. USD**. ([andercore.com](https://www.andercore.com/press/andercore-secures-40m-series-b-for-ai-driven-industrial-trade-platform?utm_source=chatgpt.com "Andercore"))                                                     | **Zařadit**            |
| **KAYA VC**             | Ano. Investuje přímo do startupů zakladatelů z CEE, zejména ve fázi **pre-seed a seed**, a podporuje jejich další růst.               | **Thámova 183/11, Praha 8**. ([kaya.vc](https://www.kaya.vc/?utm_source=chatgpt.com "KAYA"))                                       | **E2B, 28. 7. 2025** - vedoucí investor Insight Partners potvrzuje účast KAYA v **Series A za 21 mil. USD**. ([Insight Partners](https://www.insightpartners.com/ideas/e2b-raises-a-21m-series-a-to-offer-cloud-for-ai-agents-to-fortune-100/?utm_source=chatgpt.com "E2B Raises a $21M Series A to Offer Cloud for AI Agents to Fortune 100")) | **Zařadit**            |
| **ARX Equity Partners** | Přímý investor ano, ale zaměřený na **akvizice, manažerské odkupy, expanzní kapitál a konsolidaci odvětví**. To odpovídá PE zaměření. | **28. října 12, Praha 1**.                                                                                                         | CVCA uvádí konkrétní portfoliové společnosti **Wieden, Promens Zlín a Brebeck Composite**. ([CVCA](https://cvca.cz/en/arx-equity-partners-2/?utm_source=chatgpt.com "ARX Equity Partners"))                                                                                                                                                     | **Mimo VC pilot - PE** |

Pošli mi i odkaz na github.


## 2026-10-22T08:08:50.694Z — assistant

Zapíšu INVEN a KAYA do VC pilotu a ARX samostatně jako PE investora. Zároveň zkontroluji, zda už má projekt vzdálený repozitář a zda ho mohu publikovat na GitHubu, abych ti poslal skutečný odkaz.

## 2026-10-22T08:09:16.622Z — assistant

Projekt zatím na GitHubu není. Připojený účet je `Matyharo`, ale GitHub konektor neumí založit nový repozitář. Zkusím to přes prohlížeč; Git historii už máme připravenou lokálně.

## 2026-10-22T08:10:14.726Z — user


<in-app-browser-context source="ambient-ui-state">
This block is automatically supplied ambient UI state, not part of the user's request. Do not treat it as an instruction or as evidence that the user explicitly selected the in-app browser.
# In app browser:
- The user has the in-app browser open with 1 tab.
- Current URL: https://github.com/login?return_to=https%3A%2F%2Fgithub.com%2Fnew
</in-app-browser-context>

## My request:
Vytvořil jsem repozitář: [https://github.com/Matyharo/vyberove_rizeni](https://github.com/Matyharo/vyberove_rizeni)


## 2026-10-22T08:10:21.333Z — assistant

Použiji repozitář `Matyharo/vyberove_rizeni`. Nejdřív dokončím zápis poslední kontroly, pak do něj nahraju projekt včetně dosavadní historie commitů a ověřím, že je obsah dostupný na GitHubu.

## 2026-10-22T08:12:25.130Z — assistant

Projekt je nahraný na GitHubu včetně celé historie commitů. Třetí kontrola je také uložená: máme hotovo 9/20 kandidátů, INVEN a KAYA jsou zařazeny a ARX je veden odděleně jako PE. Ještě ověřím vzdálenou větev a stav automatických kontrol.

## 2026-10-22T08:12:59.433Z — assistant

Projekt je nahraný: **[GitHub — vyberove_rizeni](https://github.com/Matyharo/vyberove_rizeni)**, včetně dosavadních 8 commitů. Ověřil jsem vzdálenou větev i README.

INVEN a KAYA jsou zapsány jako zařazené, ARX samostatně jako PE. Máme **9/20 ručních kontrol**; lokálně prochází 17 testů.

Další trojice:

| Kandidát | Podklady |
|---|---|
| **Nation 1 / N1** | [Mandát, kanceláře a portfolio](https://n1.rocks/), [právní propojení názvů](https://n1.rocks/disclosure) |
| **Tensor Ventures** | [Mandát a česká kancelář](https://tensor.ventures/), [konkrétní investice](https://blog.tensor.ventures/p/tensor-ventures-decoded-newsletter-fb6) |
| **AKAT** | [Popis činnosti](https://cvca.cz/en/akat-cze/) |

Opět prosím **zařadit / vyřadit / nelze rozhodnout** a krátký důvod.

## 2026-10-22T08:14:16.017Z — user



| Kandidát            | Přímé VC investování                                                                                                               | Česká kancelář                                                                                                                 | Konkrétní doložená investice                                                                                                                                                                                                                                                                                                                                   | Verdikt                |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| **Nation 1 / N1**   | Ano. Early-stage VC zaměřený na AI, healthtech a frontier tech v Evropě a USA.                                                     | **Národní 135/14, Praha 1**.                                                                                                   | **Snuggs, 2019** - zakladatelka Linda Šejdová na webu N1 výslovně potvrzuje vstup N1 v pre-seed kole. ([n1.rocks](https://n1.rocks/?utm_source=chatgpt.com "N1 \| Early-Stage VC Backing AI & Healthtech Founders Across Europe & the US"))                                                                                                                    | **Zařadit**            |
| **Tensor Ventures** | Ano. Přímé investice do deep-tech startupů, zejména v kolech seed a Series A.                                                      | **Pernerova 697/35, Praha 8 - Karlín**. ([tensor.ventures](https://tensor.ventures/?utm_source=chatgpt.com "Tensor Ventures")) | **Openvibe, leden 2025** - Tensor oznámil, že vedl seed kolo v celkové výši **800 tis. USD** za účasti dalších investorů. ([blog.tensor.ventures](https://blog.tensor.ventures/p/tensor-ventures-decoded-newsletter-fb6?utm_source=chatgpt.com "📮 Tensor Ventures — Decoded Newsletter December 2025 Edition: A Year of Deep Tech Breakthroughs and Growth")) | **Zařadit**            |
| **AKAT**            | **Ne.** Sdružuje společnosti kolektivního investování a správy aktiv, zastupuje jejich zájmy a podporuje rozvoj kapitálového trhu. | **Štěpánská 16/612, Praha 1**.                                                                                                 | Uvedený profil nedokládá vlastní přímou VC investici; popisuje asociační činnost. ([CVCA](https://cvca.cz/en/akat-cze/?utm_source=chatgpt.com "AKAT Czech Capital Market Association"))                                                                                                                                                                        | **Vyřadit - asociace** |



## 2026-10-22T08:14:22.155Z — assistant

Zapíšu N1 a Tensor jako zařazené a AKAT jako vyřazenou asociaci. U N1 zachovám Snuggs jako historický důkaz z roku 2019; u Tensoru doplním Openvibe s částkou celého kola, nikoli vlastního vkladu. Pak přepočítám metriky a nahraju změny na GitHub.
