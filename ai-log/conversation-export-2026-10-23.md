# Dodaný export konverzace - finální opravy a frontend

Uživatel dodal tento Markdown export 23. 10. 2026 a výslovně požádal o přidání na GitHub. Zprávy níže pocházejí z dodaného souboru, nejsou rekonstruované z paměti. Způsob nativního exportu nebyl nezávisle ověřen.

Veřejná verze vynechává celé technické bloky nástrojů včetně jejich výstupů, anonymizuje domovské cesty a nahrazuje lokální obrázkové odkazy textovými poznámkami. Původní seskupení „previous messages“ a historické výroky zůstávají zachované; jejich stav nemusí odpovídat současnosti. Lokální a relativní odkazy jsou součástí historického textu, nikoli slibem veřejné dostupnosti. Připojené soubory a obrázky nejsou tímto textovým exportem automaticky zahrnuty.

Rozsah: finální opravy databáze, první malý atributový audit a frontend až po potvrzení pushe e3469cb. Neobsahuje současnou žádost o archivaci ani následné zprávy. Starší konverzace zůstává samostatně v conversation-export.md; snapshot se s ní může překrývat. Manifest původu a redakcí: export-manifest-2026-10-23.json.

Skutečné texty příloh jsou dostupné samostatně: [zadání finálních oprav](prompts/final-repairs.md) a [zadání frontendu](prompts/frontend.md).

---

# Dolaď databázi investorů

> User context
>
> Attachments:
> - Proveď finální opravy projektu https://github.com/Matyharo/vyberove_rizeni tak,…: `[USER_HOME]/.codex/attachments/9f860b45-e03e-40ae-9608-45e00516c31c/Vložený text.txt`

<details><summary>8 previous messages</summary>

> Přečtu si zadání z přiloženého textu a zkontroluji stav projektu.
>
>
> Potvrdil jsem nesoulad: ruční klasifikace je dokončená, ale generátor stále používá obecné „Ruční přesnost“ a exportuje pevné `human_verified=False`. Oddělím klasifikaci od kontroly atributů, zpřesním pravidlo publikace a připravím audit tvrzení s prázdnými lidskými štítky. Současně doplním cílenou rešerši kapitálu.
>
>
> Nové zdroje zatím nepřinesly srovnatelné současné AUM pro chybějící organizace. Potvrzují ale důležité rozdíly: DEPO a Reflex uvádějí proinvestované částky, Purple cíl jednotlivého fondu a i&i Bio historickou velikost fondu. Tyto částky ponechám oddělené od celkového kapitálu. GitHub konektor nevrátil žádné PR běhy pro kontrolovaný commit; ostatní pokusy o přístup k Actions selhaly, takže úspěch CI zatím nemohu potvrdit.
>
>
> První kontrolní běh prošel: validace, databázový audit i všech 25 testů. Finální přehled teď vyžaduje shodu aktuálního AI `include` a lidského `include`; klasifikační potvrzení přitom neoznačuje atributy za ověřené. Ještě ověřím, že doplnění jednoho atributového štítku správně projde všemi exporty a že opakovaný build zachová lidské záznamy.
>
</details>

Opravy jsou provedené lokálně, bez pushe.

1. **Opraveno:** rozlišení původní AI, aktuální AI a lidské reference, pravidlo publikace, význam příznaků ověření, metriky a dokumentace. Exporty jsou regenerované. Zmrazené predikce ani existující lidské štítky se nezměnily.

2. **Kontroly:** všech pět požadovaných příkazů prošlo, včetně **27 testů** a databázového auditu. Opakovaný build vytvořil totožné výstupy. Podrobnosti jsou v [FINAL_CHECKS.md](./reports/FINAL_CHECKS.md).

3. **Omezení:** precision původních pozitivních klasifikací je **10/10**, recall **10/11** pouze v kontrolovaném seznamu. Přesnost atributů zůstává nezměřená. Doplňující rešerše nedoložila další srovnatelné současné AUM. Úspěšný vzdálený CI běh se nepodařilo ověřit.

4. **Tvůj zbývající krok:** posoudit [18 připravených tvrzení](./reports/CLAIM_AUDIT.md) podle odkazovaných zdrojů a vyplnit jejich řádky v [review/claims.csv](./review/claims.csv): `label`, `reviewer`, `reviewed_on`, `reason`. Lidské údaje jsem ponechal prázdné.

> Commitni to na git.

<details><summary>2 previous messages</summary>

> Zkontroluji změny a vytvořím lokální commit.
>
</details>

Vytvořen commit `fdae4af` na větvi `main`:

`Finalize investor review semantics, metrics and attribute audit`

Pracovní strom je čistý. Commit je lokální, push neproběhl.

> Prosím i o push.

<details><summary>2 previous messages</summary>

> Pushnu commit na `origin/main` a ověřím výsledek.
>
</details>

Push proběhl úspěšně na `origin/main`: commit [`fdae4af`](https://github.com/Matyharo/vyberove_rizeni/commit/fdae4af).

> | Tvrzení                              | Výsledek    | Zdůvodnění                                                                                                                                                                                                                                                                                                                                                                                                                    |
> | ------------------------------------ | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | `credo.sectors.1`                    | `supported` | Web popisuje přístup bez pevné investiční teze a podporu technických zakladatelů. ([credoventures.com](https://www.credoventures.com/?utm_source=chatgpt.com "Credo \| We back the most ambitious founders from CEE. Pre-everything."))                                                                                                                                                                                       |
> | `depo.sectors.1`                     | `supported` | Všech pět uvedených oblastí je výslovně uvedeno v investičních kritériích. ([DepoVentures.com](https://depoventures.com/?utm_source=chatgpt.com "Index"))                                                                                                                                                                                                                                                                     |
> | `inibio.sectors.1`                   | `supported` | Strategie uvádí life sciences, vývoj léčiv, medtech, diagnostiku a AI. ([inibio.eu](https://www.inibio.eu/?utm_source=chatgpt.com "i\&i Bio: early stage biotech venture capital"))                                                                                                                                                                                                                                           |
> | `reflex.sectors.1`                   | `uncertain` | Portfolio podporuje technologické zaměření, ale nedokládá úplný sektorový mandát. ([reflexcapital.com](https://www.reflexcapital.com/?utm_source=chatgpt.com "Reflex Capital"))                                                                                                                                                                                                                                               |
> | `inven.stage.1`                      | `uncertain` | Vyhledávací výpis CVCA uvádí růstovou fázi. Úplnou stránku se opakovaně nepodařilo načíst. ([CVCA](https://cvca.cz/en/inven-capital-2/?utm_source=chatgpt.com "Inven Capital"))                                                                                                                                                                                                                                               |
> | `tilia.stage.1`                      | `supported` | Web výslovně uvádí early stage. ([tilia.vc](https://tilia.vc/?utm_source=chatgpt.com "Tilia Impact Ventures"))                                                                                                                                                                                                                                                                                                                |
> | `jt.stage.1`                         | `supported` | Investiční kritéria uvádějí pre-seed až Series A. ([jtventures.cz](https://www.jtventures.cz/?utm_source=chatgpt.com "J\&T Ventures"))                                                                                                                                                                                                                                                                                        |
> | `reflex.stage.1`                     | `uncertain` | Článek dokládá investici do konkrétního startupu, nikoli obecný mandát investičních fází. ([J&T Ventures](https://www.jtventures.cz/blog/grid-online-prinasi-lepe-zaplacene-kuryry-levnejsi-dopravu-i-mene-aut-ve-mestech-rika-ondrej-kratky?utm_source=chatgpt.com "grid.online přináší lépe zaplacené kurýry, levnější dopravu i méně aut ve městech, říká Ondřej Krátký"))                                                 |
> | `kaya.ticket.1`                      | `supported` | Web uvádí ticket 1-3 miliony USD. ([kaya.vc](https://www.kaya.vc/?utm_source=chatgpt.com "KAYA"))                                                                                                                                                                                                                                                                                                                             |
> | `nation1.ticket.1`                   | `supported` | Web uvádí obvyklou první investici 100 tisíc až 1 milion USD. ([n1.rocks](https://n1.rocks/?utm_source=chatgpt.com "N1 \| Early-Stage VC Backing AI & Healthtech Founders Across Europe & the US"))                                                                                                                                                                                                                           |
> | `tensor.ticket.1`                    | `uncertain` | Výpis CVCA zachycuje začátek rozpětí, ale celé rozpětí se nepodařilo ověřit na načtené stránce. ([CVCA](https://cvca.cz/en/tensor-ventures/?utm_source=chatgpt.com "Tensor Ventures"))                                                                                                                                                                                                                                        |
> | `purple.ticket.1`                    | `supported` | Vlastní web uvádí počáteční ticket 250-400 tisíc EUR. Rozpor s LinkedIn zůstává. ([purple-ventures.com](https://www.purple-ventures.com/?utm_source=chatgpt.com "Úvod"))                                                                                                                                                                                                                                                      |
> | `purple.ticket.2`                    | `supported` | Firemní LinkedIn uvádí počáteční ticket 250-500 tisíc EUR. Nelze určit, který profil zachycuje novější mandát. ([LinkedIn](https://cz.linkedin.com/company/purple-ventures?utm_source=chatgpt.com "Purple Ventures"))                                                                                                                                                                                                         |
> | `credo.capital_reference.1`          | `uncertain` | Výpis CVCA uvádí spravované prostředky 170 milionů EUR. Úplnou stránku ani referenční datum se nepodařilo ověřit. ([CVCA](https://cvca.cz/en/credo-ventures-2/?utm_source=chatgpt.com "Credo Ventures"))                                                                                                                                                                                                                      |
> | `inibio.capital_reference.1`         | `uncertain` | Článek z 30. 11. 2022 dokládá přibližně 47 milionů EUR celkového kapitálu fondu. Neprokazuje však jednoznačně použitou kategorii `fund_closed_size`. ([i&i Bio](https://www.inibio.eu/news/experienced-businessmen-join-forces-with-excellent-science%2C-invest-%E2%82%AC2m-in-the-fund-at-the-iocb?utm_source=chatgpt.com "Experienced businessmen join forces with excellent science, invest €2M in the fund at the IOCB")) |
> | `inibio.capital_reference.2`         | `supported` | Doprovodný profil uvádí přes 53 milionů EUR ve správě fondu. Samostatné datum platnosti tohoto údaje chybí. ([i&i Bio](https://www.inibio.eu/news/experienced-businessmen-join-forces-with-excellent-science%2C-invest-%E2%82%AC2m-in-the-fund-at-the-iocb?utm_source=chatgpt.com "Experienced businessmen join forces with excellent science, invest €2M in the fund at the IOCB"))                                          |
> | `kaya.total_investment_capital.1`    | `supported` | Web uvádí celkové AUM 500 milionů USD. Jde o vlastní zveřejněný údaj bez data ocenění. ([kaya.vc](https://www.kaya.vc/?utm_source=chatgpt.com "KAYA"))                                                                                                                                                                                                                                                                        |
> | `nation1.total_investment_capital.1` | `supported` | Web uvádí 60 milionů USD ve správě přes dva fondy. Samostatné datum ocenění chybí. ([n1.rocks](https://n1.rocks/?utm_source=chatgpt.com "N1 \| Early-Stage VC Backing AI & Healthtech Founders Across Europe & the US"))                                                                                                                                                                                                      |

<details><summary>3 previous messages</summary>

> Zkontroluji tabulku proti připraveným 18 tvrzením. Před zápisem do lidských referencí potřebuji potvrdit původ kontroly a doplnit identitu kontrolora a datum, abych je nevymýšlel.
>
> Jsou to tvoje vlastní lidská rozhodnutí po kontrole zdrojů, nebo výstup AI? Pokud jde o lidskou kontrolu, napiš prosím také označení kontrolora a skutečné datum kontroly (YYYY-MM-DD).
>
</details>

Tabulka odpovídá všem 18 vybraným tvrzením: **12 supported, 6 uncertain**. Nejisté případy se nezapočítají do jmenovatele přesnosti.

Před zápisem potřebuji potvrdit: jde o tvoji vlastní lidskou kontrolu zdrojů, nebo výstup AI? U lidské kontroly doplň označení kontrolora a skutečné datum kontroly. Podle původního zadání tyto údaje nesmím vyplnit za tebe.

> **Jsou to tvoje vlastní lidská rozhodnutí po kontrole zdrojů, nebo výstup AI? Pokud jde o lidskou kontrolu, napiš prosím také označení kontrolora a skutečné datum kontroly (YYYY-MM-DD).**
>
> Ferstl 22.10.2026

<details><summary>4 previous messages</summary>

> Zapíšu všech 18 rozhodnutí jako lidskou kontrolu Ferstl ze dne 22. 10. 2026, přepočítám metriky a obnovím exporty i dokumentaci. Šest výsledků `uncertain` ponechám jako nejisté.
>
>
> Zapsáno: 12 `supported`, 6 `uncertain`, žádné `incorrect`. U vyřešených tvrzení je shoda s referencí 12/12; šest nejistých případů se do tohoto jmenovatele nepočítá. Rozpor ticketů Purple i omezení historických částek zůstávají zachované. Validace, databázový audit a všech 28 testů prošly; ještě ověřím opakovatelnost buildu a aktualizuji závěrečný protokol.
>
</details>

Zapsáno jako **Ferstl, 2026-10-22**:

- 12 `supported`, 6 `uncertain`.
- Shoda vyřešených tvrzení: **12/12**; nejisté případy jsou mimo jmenovatel.
- Exporty, metriky a dokumentace aktualizovány.
- Všech **28 testů**, validace, databázový audit a kontrola vydání prošly. Opakovaný build zachoval štítky.

Šest otevřených případů najdeš v [atributovém auditu](./reports/CLAIM_AUDIT.md). Rozpor Purple zůstává zachovaný.

Nové změny jsou zatím lokální, bez commitu a pushe.

> Push

<details><summary>2 previous messages</summary>

> Vytvořím commit posledních změn a pushnu ho na `origin/main`.
>
</details>

Push na `origin/main` proběhl úspěšně: commit [`336cf2e`](https://github.com/Matyharo/vyberove_rizeni/commit/336cf2e).

Pracovní strom je čistý.

> User context
>
> Attachments:
> - Doplň do existujícího projektu https://github.com/Matyharo/vyberove_rizeni prof…: `[USER_HOME]/.codex/attachments/08b9f495-edbd-4af3-9ca7-b2962bbf88b2/Vložený text.txt`

<details><summary>24 previous messages</summary>

> Přečtu si přiložené zadání a aktuální stav projektu.
>
>
> Použiji dovednosti pro návrh frontendu a jeho ověření v prohlížeči. Zachovám statický HTML/CSS/JavaScript bez závislostí a napojím data na současný Python build.
>
>
> Rozhraní postavím jako střízlivý pracovní přehled: bílá plocha, petrolejový akcent, kompaktní tabulka a detail se zdroji u každého údaje. Nejprve připravím vizuální koncept; nejistotu a rozpory zobrazím přímo u částek, nikoli jen v metodice.
>
>
> Viewed an image
>
>
> Data pro web budou vznikat v Pythonu až po validaci a převezmou stejný publikovaný seznam jako CSV. U kontrol zobrazím jejich skutečný původ: referenční rozhodnutí dodaná uživatelem a zapsaná asistentem, nikoli nezávislý audit celé databáze.
>
>
> Vestavěný prohlížeč při otevření lokálního serveru skončil timeoutem. Pro ověření použiji lokální Chromium přes Playwright; tato cesta umožní zkontrolovat i mobilní rozložení, klávesnici, historii a chybové stavy.
>
>
> Viewed an image
>
>
> Prohlížečové testy už potvrdily filtry, oba tickety Purple, exporty i chování na projektové cestě `/vyberove_rizeni/`. Odhalily také chybu při vracení focusu po zavření detailu: dvojí událost historie znovu vykreslila tabulku. Opravil jsem ji a pokračuji v mobilních a chybových scénářích.
>
>
> Viewed an image
>
>
> Viewed 2 images
>
>
> Desktop i mobilní scénáře nyní prošly, včetně simulované chyby načtení a opakovaného načtení dat. Web funguje i jako samostatná kopie pod `/vyberove_rizeni/`. Dokončuji README a workflow pro Pages; veřejné nasazení bude vyžadovat ruční spuštění, aby tento krok sám nic nepublikoval.
>
>
> Viewed 2 images
>
> Generated image
>
> [Lokální obrazová příloha vynechána: Generated image]
</details>

Hotovo. [Lokální náhled aplikace](http://127.0.0.1:8766/site/) je otevřený v prohlížeči.

- Tabulka, hledání bez diakritiky, kombinované filtry, řazení a detail se zdroji.
- Viditelné historické a chybějící údaje, obě rozpětí Purple, CSV/JSON exporty.
- Data generuje Python do samostatného adresáře `site/`.

Spuštění:

```console
python -m investor_db build
python -m http.server 8000 --directory site
```

Prošlo **30 Python testů, 4 JavaScript testy**, validace, databázový audit a kontrola vydání. V Chromium jsem ověřil desktop, tablet, mobil, klávesnici, historii, exporty i chybové stavy. Běžný tok byl bez konzolových chyb.

Pro zveřejnění zbývá push, nastavení Pages na **GitHub Actions** a ruční spuštění připraveného workflow podle [README](./README.md). **Push ani nasazení neproběhly.** Úplný audit přístupnosti ani dostupnosti všech externích zdrojů nebyl proveden.

[Lokální obrazová příloha vynechána: Přehled investorů]
[Lokální obrazová příloha vynechána: Mobilní detail Purple]

> Push

<details><summary>2 previous messages</summary>

> Vytvořím commit frontendu a pushnu ho na `origin/main`. Veřejné nasazení Pages zůstane vypnuté.
>
</details>

Push na `origin/main` proběhl: commit [`e3469cb`](https://github.com/Matyharo/vyberove_rizeni/commit/e3469cb).

Pracovní strom je čistý. GitHub Pages zatím není nasazený.
