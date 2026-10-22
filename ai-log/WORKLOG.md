# Protokol práce s AI

Toto je shrnutí postupu, **nikoli originální transcript**. Veřejné zprávy jsou mechanicky exportované v conversation-snapshot.md; finální nativní export se doplní po skončení práce.

## Skutečné pokyny a rozdělení práce

Uživatel poskytl e-mail se zadáním, zvolil A („Můžeme A.“) a zadal „Tak pokračuj.“. Poté zvolil společnou ruční kontrolu v chatu. Pracoval jeden Codex asistent. Subagenti nebyli použiti; pokyny imaginárním agentům nedoplňujeme zpětně.

AI navrhla: pozitivní důkaz pojmenované přímé investice, oddělení správce a fondu, zdroj u každého tvrzení, explicitně chybějící hodnoty, 20 kandidátů, neměnné predikce, vlastní kontrolu oddělenou od lidského reference setu. Postup je zachycený v PLAN.md a commitech.

## Historie

- `16fa7a2`: plán před pilotem, výběrová pravidla a metodika přesnosti/nákladů.
- `d13828d`: 20 zmrazených kandidátů z asociace a ekosystémového seznamu, záměrný kontrastní výběr.
- `70498b1`: první extrakce a zmrazení 10 include / 8 exclude / 2 needs_review před opravami.
- `9c87e72`: validátor, exporty, SQL a testy; oprava Purple po první predikci; 11 include / 8 exclude / 1 needs_review.
- Další commity: zpřísnění atributů Reflexu, rozpor ticketů Purple, globální scénáře, dokumentace a autentický výřez konverzace.

## Kontrola dat

Discovery sloužilo jen k hledání. Asistent otevíral vlastní weby, zprávy portfoliových firem/spoluinvestorů a asociační profily. Výpisky jsou parafráze s URL a daty. Staré CVCA částky zůstávají historické; investor-contribution je null, pokud známe jen částku kola.

Datum známé jen jako rok není nahrazeno 1. lednem. U Tapaya nebylo v otevřené zprávě DEPO nalezeno datum publikace; nedávná aktivita není odvozena z crawl data. U grid.online evidujeme datum indexu článku zvlášť od samotné transakce.

Dva zdroje jsou jen u části případů a jejich nezávislost není garantována. Lidská kontrola ani audit právních registrací nebyly AI vymyšleny.

## Omyly a opravy

1. Jmenovci: chorvatská/kanadská CVCA, jiné JT Ventures, Lighthouse a N1. Výsledky byly rozpoznány jako nesouvisející. CzechStartups navíc u Lighthouse přímo odkazuje na jinou doménu; kandidát zůstává v karanténě.
2. Purple: první extrakce nedohledala adresu. Druhá kontrola ji našla v patičce; protože sídlo nemusí být kancelář, doplnil se firemní profil s Brnem jako ústředím a primární lokalitou. Původní predikce zůstala.
3. Purple ticket: web 250–400 tis. EUR, firemní LinkedIn 250–500 tis. EUR. Rozpětí není vymyšleně sjednoceno; první výrok je partial, alternativní reference zachována.
4. Reflex: charakteristika portfolia mohla být chybně čtena jako úplný sektorový/fázový mandát. Stav změněn na partial; geografie not_found. Kancelář není důkazem investičního regionu.
5. SQLite: první běh selhal na 11 parametrech pro 10 sloupců; opraveno. Další testy selhaly na dočasném adresáři mimo workspace a nezavřeném spojení na Windows. Dočasné soubory jsou nyní v projektu a spojení se explicitně zavírají.
6. Dvě orchestrace vyhledávání skončily SyntaxError kvůli zápisu JavaScriptu; nevytvořily data a byly opraveny.
7. Ruční přepis základní čtvrtletní aktualizace byl chybně 8 160 USD. Kódový přepočet dává 12 360 USD. Dokumentace opravena a přidán test.

## Zbývající lidská práce

Otevřít zdroje, posoudit kandidáty a zapsat skutečná rozhodnutí. Metriky pak pracují s původními predikcemi, ne opravenou tabulkou. Uživatel si zvolil kontrolu v chatu; jeho odpovědi zapíšeme s datem, identifikací kontrolora a zdroji. Nezodpovězené případy za něj nedoplníme.

Export je po posledním kole nutné obnovit. [Dokumentace Codexu](https://learn.chatgpt.com/docs/developer-commands#export-a-conversation-with-export) popisuje nativní `/export` pro CLI a doporučuje počkat na skončení tahu. Zde byl připraven filtrovací skript pro lokální záznam; netvrdíme spuštění Claude `/export`.

## První skutečná ruční kontrola — 22. 10. 2026

Uživatel potvrdil Credo jako přímého investora do Axoflow s pražskou kanceláří, u BDO doložil poradenskou činnost a odmítl ztotožnění původního Lighthouse s českým fondem. Zapsány štítky include/exclude/exclude; jejich interpretace a zdroje jsou v `review/round-01.md`. AI nedoplňovala další řádky. Přepočet: 3/20 zkontrolováno, 1/10 původních pozitivních predikcí vyhodnocena správně, dalších 9 čeká. Čas lidského ověřování není znám.

## Druhá skutečná ruční kontrola — 22. 10. 2026

Uživatel zařadil DEPO a i&i Bio a uložil Genesis evidovat samostatně jako PE / growth equity. Doplnil přímou zprávu Tapaya s datem a historickou investici i&i Bio do Sampling Human s konkrétním vlastním vkladem. AI zdroje otevřela, doplnila datum Tapaya, oddělila domicil fondu od kanceláře poradce a přidala u vlastního vkladu explicitní zdrojovou vazbu i do SQLite. Genesis je v samostatné klasifikační tabulce, nikoli mezi přijatými VC. Podrobnosti: `review/round-02.md`. Zkontrolováno 6/20 kandidátů; původní pozitivní predikce zatím 3/3 správně, sedm čeká. Čas opět není změřen.
