# Spolehlivá databáze investorů

Praktická úloha pro Junior AI Developer — zadání A.

## Aktuální stav

Projekt byl zahájen 22. 10. 2026. Nejdříve vznikl [plán](PLAN.md), před sběrem pilotních dat. Pilot bude ověřovat VC investory s doloženou českou kanceláří.

Zatím není hotový dataset, měření přesnosti, globální odhad ani publikovaný repozitář. Tento dokument není závěrečná zpráva.

## Práce s AI

Použitý nástroj: Codex. Uživatel poskytl zadání a vybral variantu A. AI navrhla český VC pilot, pravidla zařazení a ověřování. Plán vyžaduje důkazy pro jednotlivé údaje a odděluje různé druhy investičního kapitálu.

Při prvním vyhledávání se mezi výsledky objevila také chorvatská a kanadská asociace se zkratkou CVCA a nesouvisející zahraniční JT Ventures. Tyto výsledky nejsou českým investorům přiřazeny. Jde o příklad rizika záměny identity ve vyhledávání, nikoli o naměřenou chybu dokončeného datasetu.

AI nesmí vydávat vlastní opakovanou kontrolu za nezávislé ruční ověření. Kontrolní štítky člověka a autentický export konverzace se doplní až po jejich skutečném vzniku.

## Struktura

- `PLAN.md`: pravidla, pilot, zdroje, metodika přesnosti a nákladů.
- `ai-log/README.md`: pravidla uchování záznamu práce s AI.
