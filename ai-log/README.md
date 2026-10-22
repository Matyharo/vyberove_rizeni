# Záznam práce s AI

- `conversation-snapshot.md`: mechanicky vyexportovaný autentický výřez této relace (uživatel + veřejné odpovědi asistenta). Je průběžný, ne finální nativní export.
- `snapshot-manifest.json`: ID relace, hash a délka lokálního záznamu při exportu, počet zpráv a vynechané kategorie.
- `WORKLOG.md`: shrnutí skutečných pokynů, kontrol a chyb. Není transcript.

Filtrace vynechává interní instrukce, interní uvažování, technická metadata prostředí a surové výstupy nástrojů. Domovská cesta uživatele je nahrazena `[USER_HOME]`. Původní lokální záznam není zveřejněn celý; snapshot obsahuje původní text vybraných veřejných zpráv bez rekonstruování.

Po skončení konverzace doplnit nativní export jako `conversation-export.md` a zkontrolovat soukromé údaje. U Codex CLI je zdokumentován `/export`; projekt používá Codex Desktop. Nativní export zatím nebyl proveden a příkaz Claude Code `/export` se netvrdí jako použitý.
