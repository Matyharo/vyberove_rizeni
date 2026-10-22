# Záznam práce s AI

- `conversation-snapshot.md`: mechanicky vyexportovaný autentický výřez této relace (uživatel + veřejné odpovědi asistenta). Je průběžný, ne finální nativní export.
- `snapshot-manifest.json`: ID relace, hash a délka lokálního záznamu při exportu, počet zpráv a vynechané kategorie.
- `WORKLOG.md`: shrnutí skutečných pokynů, kontrol a chyb. Není transcript.

Filtrace vynechává interní instrukce, interní uvažování, technická metadata prostředí a surové výstupy nástrojů. Domovská cesta uživatele je nahrazena `[USER_HOME]`. Původní lokální záznam není zveřejněn celý; snapshot obsahuje původní text vybraných veřejných zpráv bez rekonstruování.

Po skončení konverzace doplnit nativní export jako `conversation-export.md` a zkontrolovat soukromé údaje. U Codex CLI je zdokumentován `/export`; projekt používá Codex Desktop. Nativní export zatím nebyl proveden a příkaz Claude Code `/export` se netvrdí jako použitý.

## Dokončení nativního exportu

Dne 22. 10. 2026 byl skutečně vyzkoušen Codex CLI v0.163.0-alpha.11:

```powershell
Set-Location 'C:\Users\ferst\Desktop\Vyberove_Rizeni'
codex resume 01a1627f-38f8-7cd0-b6e6-7e61e2a3d1a7 --no-alt-screen --no-daemon
```

CLI odmítlo převzít relaci: `This conversation is open in another app. Close it there and press R to continue here.` Nebyla spuštěna nová práce modelu ani vytvořena kopie chatu. CLI bylo ukončeno klávesou q. Export nebyl vytvořen.

Pro dokončení:

1. Po skončení odpovědi zavřít tento chat v desktopové aplikaci (nearchivovat ani nemazat).
2. V samostatném PowerShellu spustit příkazy výše. Pokud CLI nabídne pokračování kvůli TERM=dumb, potvrdit y. Pokud stále zobrazuje zámek, zavřít desktopovou aplikaci a stisknout R v CLI.
3. Po načtení uložené relace zadat přímo do CLI:

```text
/export C:/Users/ferst/Desktop/Vyberove_Rizeni/ai-log/conversation-export.md
```

4. Ověřit hlášení o uložení a ukončit CLI příkazem `/quit` nebo Ctrl+C. Poté lze znovu otevřít desktopový chat.
5. Před zveřejněním zkontrolovat export na soukromé údaje. Nevkládat surový rollout obsahující interní instrukce a uvažování. Případné redakce výslovně uvést; nepřepisovat historii ani nepřidávat rekonstruované zprávy.
6. Spustit `python -m investor_db check-release`, zaznamenat skutečný způsob exportu a po kontrole uložit export do Git historie a zveřejnit.

Oficiální dokumentace: https://learn.chatgpt.com/docs/developer-commands#export-a-conversation-with-export . Dokumentace vyžaduje export po skončení aktuálního tahu. Zelený checklist sám neověřuje obsah ani autenticitu souboru.
