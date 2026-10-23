# Záznam práce s AI

**Aktuální stav k 23. 10. 2026:** v repozitáři jsou oba dosud dodané exporty konverzací. Jde o archiv dostupných podkladů tohoto projektu, nikoli ověřený export všech chatů účtu. Zprávy nebyly rekonstruovány. Způsob nativního exportu není nezávisle ověřen.

| Soubor | Rozsah a původ |
|---|---|
| [conversation-export.md](conversation-export.md) | Starší uživatelem dodaná konverzace včetně sedmi kol klasifikace. Původ a redakce: [export-manifest.json](export-manifest.json). |
| [conversation-export-2026-10-23.md](conversation-export-2026-10-23.md) | Nově dodaná konverzace: finální opravy, malý atributový audit, frontend a potvrzení pushe e3469cb. Původ, hash a přesné redakce: [export-manifest-2026-10-23.json](export-manifest-2026-10-23.json). |
| [prompts/final-repairs.md](prompts/final-repairs.md) | Skutečný text zadání finálních oprav, v exportu původně pouze odkazovaný jako lokální příloha. |
| [prompts/frontend.md](prompts/frontend.md) | Skutečný text zadání frontendu, v exportu původně pouze odkazovaný jako lokální příloha. |

Nový export vynechává 22 technických bloků nástrojů a jejich výstupy, anonymizuje dvě zbývající domovské cesty a nahrazuje tři lokální obrazové odkazy textovými poznámkami. Snímky a samotný obrázkový koncept nejsou součástí textového archivu. Pro oba skutečné texty zadání jsou rovněž uloženy hashe v novém manifestu. Historické výroky o čekajících krocích se nepřepisují na dnešní stav. Starší soubory zůstaly beze změny.


- `conversation-snapshot.md`: mechanicky vyexportovaný autentický výřez této relace (uživatel + veřejné odpovědi asistenta). Je průběžný, ne finální nativní export.
- `snapshot-manifest.json`: ID relace, hash a délka lokálního záznamu při exportu, počet zpráv a vynechané kategorie.
- `WORKLOG.md`: shrnutí skutečných pokynů, kontrol a chyb. Není transcript.

Filtrace vynechává interní instrukce, interní uvažování, technická metadata prostředí a surové výstupy nástrojů. Domovská cesta uživatele je nahrazena `[USER_HOME]`. Původní lokální záznam není zveřejněn celý; snapshot obsahuje původní text vybraných veřejných zpráv bez rekonstruování.

## Historie exportu

Před dodáním souboru uživatelem byl vyzkoušen nativní CLI export; pokus skončil kvůli zámku otevřené desktopové relace. Export tím nevznikl. Později uživatel dodal Markdown a jeho redakce je zachycena v manifestu. Detailní historický záznam zůstává ve WORKLOG.md. Žádný nový nativní export není vyžadován: citované zadání požaduje popis práce s AI v README. Exporty zůstávají doplňkovými podklady. Jejich rozsah a konec zachycují jednotlivé manifesty.

Nové kolo malého atributového auditu je zaznamenáno v WORKLOG.md a review/claims.csv. Starší export nebyl přepsán; toto kolo je nyní zachyceno v nově dodaném exportu z 23. 10. 2026.
