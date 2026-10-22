# Záznam práce s AI

**Aktuální stav:** uživatel dodal Markdown export. Veřejná redigovaná verze je `conversation-export.md`, manifest původu a úprav `export-manifest.json`. Odstraněny technické bloky nástrojů a anonymizovány domovské cesty. Zprávy nebyly rekonstruovány. Použitý nativní příkaz není nezávisle ověřen.


- `conversation-snapshot.md`: mechanicky vyexportovaný autentický výřez této relace (uživatel + veřejné odpovědi asistenta). Je průběžný, ne finální nativní export.
- `snapshot-manifest.json`: ID relace, hash a délka lokálního záznamu při exportu, počet zpráv a vynechané kategorie.
- `WORKLOG.md`: shrnutí skutečných pokynů, kontrol a chyb. Není transcript.

Filtrace vynechává interní instrukce, interní uvažování, technická metadata prostředí a surové výstupy nástrojů. Domovská cesta uživatele je nahrazena `[USER_HOME]`. Původní lokální záznam není zveřejněn celý; snapshot obsahuje původní text vybraných veřejných zpráv bez rekonstruování.

## Historie exportu

Před dodáním souboru uživatelem byl vyzkoušen nativní CLI export; pokus skončil kvůli zámku otevřené desktopové relace. Export tím nevznikl. Později uživatel dodal Markdown a jeho redakce je zachycena v manifestu. Detailní historický záznam zůstává ve WORKLOG.md. Žádný nový nativní export není vyžadován: citované zadání požaduje popis práce s AI v README. Existující soubory jsou doplňkové a neobsahují tuto novou etapu finálních oprav.
