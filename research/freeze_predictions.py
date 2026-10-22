"""Run once before corrections; refuses to overwrite the frozen predictions."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
pilot = json.loads((root / "data/pilot.json").read_text(encoding="utf-8"))
content = {
    "frozen_on": pilot["as_of"],
    "method": "Predikce po první extrakci, před opravami následnou kontrolou AI. Nejde o výkon automatického klasifikátoru.",
    "candidate_sha256": hashlib.sha256((root / "data/candidates.json").read_bytes().replace(b"\r\n", b"\n")).hexdigest(),
    "predictions": pilot["decisions"],
}
with (root / "data/predictions.json").open("x", encoding="utf-8") as file:
    json.dump(content, file, ensure_ascii=False, indent=2)
    file.write("\n")
