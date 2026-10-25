# Navigační kategorie

Python modul `investor_db/navigation.py` mapuje pouze explicitně známé výrazy na stabilní ID a české názvy. Neznámé fragmenty a vysvětlující poznámky se nestávají položkami filtrů. Jde o navigační pomůcku, nikoli nové ověření investičního mandátu.

Sektorově otevřené a široké technologické zaměření mají vlastní kategorie; nezahrnují automaticky všechny sektory. Jednoznačná synonyma sdílejí ID. Původní tvrzení, jejich stavy a zdroje zůstávají v detailu.

Výslovné rozpětí `pre-seed až Series A` se rozvine na Pre-seed, Seed a Series A. Kombinace oddělené středníkem přidávají jednotlivé rozpoznané fáze. Obecné early-stage se nerozvíjí na konkrétní kola; growth je samostatný. Kategorie uchovávají `claim_ids` a `source_statuses`; omezená opora je viditelná také ve filtru.

Frontend čte kategorie z datového balíčku. Formulář i sdílená URL používají stejná ID; čitelný název v URL se převede na ID, neznámá hodnota se odstraní. Filtry neovlivňují úplnost stažených exportů.

Na výslovný pokyn uživatele zůstává všech 18 atributových hodnocení v původním zařazení, se stejnými metadaty a metrikami. Tato úprava neposuzuje jejich původ znovu.
