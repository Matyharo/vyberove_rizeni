"""Add the Openvibe evidence supplied by the human reviewer, without changing predictions."""
from pathlib import Path
from investor_db.core import read_json, dump_json

root = Path(__file__).resolve().parents[1]
pilot = read_json(root / "data/pilot.json")
if not any(t["id"] == "tx-tensor-openvibe" for t in pilot["transactions"]):
    pilot["transactions"].append(dict(
        id="tx-tensor-openvibe", investor_id="tensor", company="Openvibe",
        source_id="tensor-news", corroborating_source_ids=[], date="2025-01-28",
        date_precision="day", date_kind="embedded_announcement",
        round_amount=dict(amount=800000, currency="USD", composition="seed_round"),
        investor_contribution=None, evidence_kind="named_investment",
        note="Ve zprávě shrnuté v newsletteru je 28. 1. 2025 uveden Tensor jako vedoucí investor seed kola. 800 tis. USD je celá částka kola; vlastní vklad Tensoru nezjištěn."))
dump_json(root / "data/pilot.json", pilot)
path = root / "README.md"
readme = path.read_text(encoding="utf-8")
start = readme.index("**Výsledek technické etapy:**")
end = readme.index("\n\n", start)
readme = readme[:start] + "**Výsledek technické etapy:** 20 kandidátů, 11 předběžně přijatých VC organizací, 8 vyloučených a 1 nevyřešená identita podle AI. 45 veřejných zdrojů, 116 tvrzení a 13 investičních důkazů. Ručně zkontrolováno **12/20 kandidátů**: Credo, DEPO, i&i Bio, INVEN, KAYA, N1 a Tensor include; BDO, původní Lighthouse, Genesis, ARX a AKAT exclude z VC pilotu. Genesis a ARX jsou samostatně evidováni jako PE / growth equity, respektive PE investoři. Z původních pozitivních predikcí je vyhodnoceno 7/10, všechny správně; konečná přesnost ještě není známá." + readme[end:]
readme = readme.replace("Po třetím kontrolním kole je čitatel i jmenovatel 5, ale dalších 5", "Po čtvrtém kontrolním kole je čitatel i jmenovatel 7, ale další 3")
path.write_text(readme, encoding="utf-8")
