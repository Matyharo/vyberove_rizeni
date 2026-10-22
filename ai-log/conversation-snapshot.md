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
