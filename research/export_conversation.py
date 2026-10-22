"""Filtered authentic user/assistant snapshot of ONE explicitly selected rollout.

Excludes internal instructions, reasoning and raw tool outputs. No reconstructed
dialogue. Native final /export is recommended after the conversation completes.
"""
import argparse
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("rollout", type=Path)
parser.add_argument("--expected-session-id", required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
raw = args.rollout.read_bytes()
records = [json.loads(line) for line in raw.decode("utf-8").splitlines() if line.strip()]
meta = next(r["payload"] for r in records if r["type"] == "session_meta")
if meta["id"] != args.expected_session_id or Path(meta["cwd"]).resolve() != root:
    raise SystemExit("Session ID / workspace mismatch; refusing unrelated conversation")

def redact(text):
    text = text.replace(str(Path.home()), "[USER_HOME]")
    text = text.replace(str(Path.home()).replace("\\", "/"), "[USER_HOME]")
    return re.sub(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b", "[REDACTED_API_KEY_PATTERN]", text)

messages = []
excluded = Counter()
for record in records:
    if record["type"] != "response_item":
        continue
    item = record["payload"]
    if item.get("type") != "message" or item.get("role") not in {"user", "assistant"} or item.get("channel") == "analysis":
        excluded[item.get("type", "unknown")] += 1
        continue
    text = "\n".join(part.get("text", "") for part in item.get("content", []) if part.get("type") in {"input_text", "output_text", "text"})
    if not text.strip():
        continue
    if text.startswith(("<environment_context>", "<external_codex_apps_open_page>")):
        excluded["environment_or_page_metadata"] += 1
        continue
    messages.append((record.get("timestamp", ""), item["role"], redact(text)))

lines = ["# Autentický výřez konverzace v Codexu", "",
         "Tento soubor je mechanický export uživatelských a veřejných asistentských zpráv z lokálního záznamu této relace. Není přepisem vytvořeným z paměti ani nativním příkazem Claude /export.", "",
         "Jde o průběžný snapshot: neobsahuje zprávy vzniklé po jeho vytvoření. Vyloučeny jsou interní instrukce, interní uvažování, technická metadata prostředí a surové výstupy nástrojů. Domovská cesta uživatele je nahrazena [USER_HOME]; vzory API klíčů by byly redigovány. Provedené kroky a opravy shrnuje ai-log/WORKLOG.md. Pro finální odevzdání doplnit nativní export po skončení práce.", ""]
for timestamp, role, text in messages:
    lines.extend([f"## {timestamp} — {role}", "", text, ""])
(root / "ai-log/conversation-snapshot.md").write_text("\n".join(lines), encoding="utf-8")
(root / "ai-log/snapshot-manifest.json").write_text(json.dumps({
    "session_id": meta["id"], "created_utc": datetime.now(timezone.utc).isoformat(),
    "source_prefix_sha256": hashlib.sha256(raw).hexdigest(), "source_bytes_at_snapshot": len(raw),
    "source_last_record_timestamp": records[-1].get("timestamp"), "exported_messages": len(messages),
    "excluded_item_counts": dict(excluded), "format": "filtered user-visible messages, not native complete export"
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Exported {len(messages)} authentic messages; no tool outputs, internal instructions or reasoning.")
