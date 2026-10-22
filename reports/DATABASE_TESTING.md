# Ověření databáze

Lokální běh 22. 10. 2026: aktuální výsledky automatických testů a počet kontrol jsou v [FINAL_CHECKS.md](FINAL_CHECKS.md). Původní sada 22 testů byla rozšířena o regresní kontroly publikace a odvození lidského ověření. Samostatný read-only audit prošel všemi sedmi kontrolami. Strojový výsledek: DATABASE_AUDIT.json.

## Co bylo skutečně ověřeno

- SQLite integrity_check = ok, foreign_key_check bez chyb.
- Všech 20 kandidátů má lidský verdikt. Všech 11 zařazených má navázaný datovaný investiční důkaz a veřejný zdroj.
- Všechna evidovaná tvrzení má existující zdroj; JSON hodnoty jsou čitelné. Zdrojová ID v lidských rozhodnutích existují, přestože jsou v tabulce uložená jako seznam v textu.
- Počty a hodnoty tvrzení odpovídají kanonickému JSON vstupu. Publikovaná databáze má stejný logický SQL dump jako nový export ze skutečných vstupů včetně lidských štítků.
- Opakované sestavení zachovává SQL obsah, lidské štítky i původní predikce.
- Na dočasné kopii byly záměrně vyvolány čtyři chyby: neexistující zdroj, duplicitní primární klíč, NULL v povinném sloupci a smazání používaného zdroje. SQLite všechny odmítlo; transakce se vrátily zpět.
- SQL dotazy zachovávají rozdíl mezi celým kolem a vlastním vkladem: Sampling Human má doložený vlastní vklad 1,5 mil. USD a neznámé celé kolo; Openvibe má celé kolo 800 tis. USD a neznámý vlastní vklad Tensor.

## Opakování kontroly

```console
python -m unittest discover -s tests -v
python research/audit_database.py
python -m investor_db check-release
```

Audit otevírá publikovanou databázi v režimu pouze pro čtení. Testy zápisu a nového sestavení pracují v dočasných adresářích a publikovanou databázi nemění. GitHub Actions spouštějí tuto sadu a samostatný audit; výše uvedený výsledek pochází z lokálního běhu.

## Příklad použití

```sql
SELECT i.name, t.company, t.date, t.date_precision, s.url
FROM published_investors i
JOIN transactions t ON t.investor_id = i.id
JOIN sources s ON s.id = t.source_id
ORDER BY i.name, t.date;
```

Konečný seznam zařazených používá published_investors se shodou aktuálního AI include a lidského include; decisions obsahuje pracovní rozhodnutí AI, initial_predictions původní zmrazené predikce.

Při vlastním zápisu je potřeba na každém SQLite spojení provést `PRAGMA foreign_keys=ON`; jde o vlastnost SQLite, nikoli trvalé nastavení souboru. DB je primárně reprodukovatelný export, nikoli samostatná služba pro příjem libovolných zápisů. Obchodní pravidla (například správný význam peněžních veličin) kontroluje Python validátor před exportem; SQL schéma samo všechna nevynucuje.

Technické testy nedokládají pravdivost webových údajů, dnešní dostupnost URL ani globální úplnost. Přesnost klasifikace subjektů vychází ze samostatné ruční kontroly; malý atributový audit je evidovaný odděleně a neprokazuje přesnost všech atributů. Zátěžový test nebyl pro tento malý offline pilot proveden.
