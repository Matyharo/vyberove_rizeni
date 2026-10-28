# Provoz a ověření webového přehledu

Statická aplikace používá HTML, CSS a JavaScript bez frameworku, backendu a externích fontů. Python build ověří data a vytvoří samostatný adresář `site/` včetně jednoho datového balíčku `data.json` a funkčních exportů. Zdrojový kód je ve `frontend/`; `site/` je generovaný a není verzovaný. Výběr přebírá ze stejné publikace jako souhrnné CSV. Názvy, částky ani počty nejsou ručně přepsané v UI.

```console
python -m investor_db build
python -m http.server 8000 --bind 127.0.0.1 --directory site
```

Otevřete [lokální přehled](http://127.0.0.1:8000/). Použijte HTTP server, nikoli otevření souboru přes file://. Web má hledání bez české diakritiky, kombinované filtry, řazení podle názvu, sdílení URL filtru a investora a zdroje u jednotlivých údajů. Detail se zavírá tlačítkem, Escape nebo Zpět a vrací focus na původní akci. Na mobilu zabírá celou obrazovku. Stažené CSV a JSON obsahují celý publikovaný pilot, ne aktuálně filtrovaný výběr.

Balíček zachovává původní stavy tvrzení, peněžní významy, obě rozpětí Purple, historické alternativy Credo a Tensor, transakce, zdroje a reference s kontrolorem a datem. Výraz „Reference dodaná uživatelem“ neznamená nezávislý audit všech údajů. Podmínku publikace vyhodnocuje Python, nikoli frontend. Filtry používají explicitně normalizované navigační kategorie z Python pipeline. Původní tvrzení se nemění. Podrobnosti jsou v [NAVIGATION.md](NAVIGATION.md).

### GitHub Pages

Workflow `validate.yml` kontroluje při pushi i PR Python a JavaScript (Node.js 22). Workflow `pages.yml` na PR sestaví a otestuje balíček bez publikace. Push do `main` po úspěšné validaci, buildu, auditu, Python/JavaScript testech a check-release automaticky nasadí GitHub Pages. Nasazení stejné větve se řadí do fronty.

Ruční nasazení: **Actions -> Build and publish investor browser -> Run workflow**, větev `main`, zaškrtnout **Publish the built site to GitHub Pages**. Bez zaškrtnutí proběhne jen build. Pages používá zdroj GitHub Actions; případné schválení prostředí závisí na nastavení repozitáře.

[Živý web](https://matyharo.github.io/vyberove_rizeni/), [aktuální kontroly a stav publikace](../reports/FINAL_CHECKS.md). Filtry jsou commitnuté v `ee46be4`; nasazení se dokládá samostatným během a commitem. Soubory a downloady používají relativní cesty; balíček byl historicky ověřen také pod `/vyberove_rizeni/`.

### Historické browser QA a opakování kontrol

```console
python -m investor_db validate
python -m investor_db build
python research/audit_database.py
python -m unittest discover -s tests -v
node --test frontend/tests/*.test.mjs
python -m investor_db check-release
```

Node.js je potřeba jen pro pět vývojových modelových testů, nikoli pro Python build nebo používání webu. Není potřeba npm install. Python integrační testy porovnávají web s publikací pipeline, zachování referencí, rozporů, peněžních hodnot a determinismus sestavení.

Browser QA 23. 10. 2026: Chromium při 1536x1024, 768x900 a 390x844. Ověřena shoda s pipeline, hledání včetně diakritiky, kombinované filtry/reset/prázdný stav, řazení, obě hodnoty Purple se zdroji, historické a chybějící hodnoty, detail/Escape/focus trap/návrat focusu/Zpět/přímé URL, tři skutečně stažené exporty a cesta `/vyberove_rizeni/`. Ověřeno také pomalé načítání, chyba dat a retry, prázdný dataset, reduced-motion a inertní vykreslení škodlivých textů/URL. Běžný tok byl bez konzolových varování a runtime chyb. Vestavěný prohlížeč byl po odstranění blokace lokálního socketu rovněž otevřen; systematické simulace běžely v lokálním Playwright Chromium.

Nejde o kompletní WCAG audit, fyzický telefon nebo kontrolu aktuální pravdivosti všech externích webů. Odkazy byly porovnány se zabalenými zdroji a povolenými schématy; jejich síťová dostupnost nebyla hromadně ověřována. Statický UI audit prošel v strict režimu. Ovládací tlačítka v základním HTML jsou neaktivní do navázání modulových obsluh, takže neexistují aktivní akce bez funkce. CSP záměrně nepovoluje inline obsluhy. Lint DESIGN.md prošel bez chyb; upozornění na tokeny se týkají dokumentačních komponent, runtime vlastní centrální CSS.

