"""Preserve ARX separately as PE, as directed in the third human review."""
from pathlib import Path
from investor_db.core import read_json, dump_json

root = Path(__file__).resolve().parents[1]
pilot = read_json(root / "data/pilot.json")
if not any(row["candidate_id"] == "arx" for row in pilot.get("out_of_scope", [])):
    pilot.setdefault("out_of_scope", []).append(dict(
        candidate_id="arx", investor_type="private_equity", source_ids=["arx"],
        note="Skutečný PE investor s akvizicemi, management buyout a expanzním kapitálem. Na pokyn uživatele evidován odděleně mimo VC pilot; nejde o prohlášení za neinvestora."))
dump_json(root / "data/pilot.json", pilot)

readme_path = root / "README.md"
readme = readme_path.read_text(encoding="utf-8")
start = readme.index("**Výsledek technické etapy:**")
end = readme.index("\n\n", start)
readme = readme[:start] + "**Výsledek technické etapy:** 20 kandidátů, 11 předběžně přijatých VC organizací, 8 vyloučených a 1 nevyřešená identita podle AI. 45 veřejných zdrojů, 116 tvrzení a 12 investičních důkazů. Ručně zkontrolováno **9/20 kandidátů**: Credo, DEPO, i&i Bio, INVEN a KAYA include; BDO, původní Lighthouse, Genesis a ARX exclude z VC pilotu. Genesis a ARX jsou evidováni samostatně jako PE / growth equity, respektive PE investoři. Z původních pozitivních predikcí je vyhodnoceno 5/10, všechny správně; konečná přesnost ještě není známá." + readme[end:]
readme = readme.replace("Po druhém kontrolním kole je čitatel i jmenovatel 3, ale dalších 7", "Po třetím kontrolním kole je čitatel i jmenovatel 5, ale dalších 5")
readme = readme.replace("finální nativní export konverzace a URL veřejného GitHub repozitáře", "finální nativní export konverzace")
if "https://github.com/Matyharo/vyberove_rizeni" not in readme:
    readme = readme.replace("## Co otevřít", "Veřejný repozitář: https://github.com/Matyharo/vyberove_rizeni\n\n## Co otevřít")
readme_path.write_text(readme, encoding="utf-8")
