"""Apply evidence supplied in the second human review; preserve frozen predictions.

Run once on the current pilot, not on the initial research transcription.
"""
from pathlib import Path
from investor_db.core import read_json, dump_json

root = Path(__file__).resolve().parents[1]
p = read_json(root / "data/pilot.json")

def add_source(sid, url, publisher, title, summary, published=None, kind="investor"):
    if any(s["id"] == sid for s in p["sources"]):
        return
    p["sources"].append(dict(id=sid, url=url, publisher=publisher, title=title,
                             evidence_summary=summary, published_on=published,
                             accessed_on="2026-10-22", kind=kind, access_method="web_tool_open"))

add_source("tapaya-primary", "https://www.tapaya.com/en/blog/tapaya-raises-1m-pre-seed-to-turn-any-device-into-a-payment-terminal",
           "Tapaya", "Tapaya raises EUR 1M pre-seed", "Příjemce potvrzuje kolo 1 mil. EUR vedené Passion Capital se spoluvedoucí účastí DEPO. Jde o celé kolo, ne vklad DEPO.", "2026-04-28", "portfolio_company")
add_source("sampling-human", "https://www.inibio.eu/news/i%26i-bio-invests-%241.5-million-in-sampling-human-to-support-the-development-of-engineered-cells-for-single-cell-analysis",
           "i&i Bio", "i&i Bio invests $1.5M in Sampling Human", "Fond oznamuje vlastní investici 1,5 mil. USD do Sampling Human. Patička rozlišuje lucemburský fond a pražského poradce Biotech Investments.", "2022-04-12")
add_source("genesis-home", "https://www.genesis.cz/", "Genesis Capital", "Private equity and growth equity strategies",
           "Vlastní web výslovně rozlišuje PE a growth equity fondy a uvádí pražskou adresu. Nejde o VC mandát.")

for tx in p["transactions"]:
    if tx["investor_id"] == "depo" and tx["company"] == "Tapaya":
        tx.update(source_id="tapaya-primary", date="2026-04-28", date_precision="day", date_kind="announcement",
                  corroborating_source_ids=["depo-tapaya"],
                  note="Datum a účast potvrzuje přímo Tapaya. 1 mil. EUR je celé kolo, vklad DEPO není zveřejněn v použitém zdroji.")
if not any(t["id"] == "tx-inibio-sampling-human" for t in p["transactions"]):
    p["transactions"].append(dict(id="tx-inibio-sampling-human", investor_id="inibio", company="Sampling Human",
                                 source_id="sampling-human", corroborating_source_ids=["inibio-home"], date="2022-04-12",
                                 date_precision="day", date_kind="announcement", round_amount=None,
                                 investor_contribution=dict(amount=1500000, currency="USD"),
                                 contribution_source_id="sampling-human", evidence_kind="named_investment",
                                 note="1,5 mil. USD je výslovně vlastní investice i&i Bio, nikoli výše celého kola; historický důkaz z roku 2022."))
office = next(c for c in p["claims"] if c["id"] == "inibio.czech_office.1")
office.update(value="Biotech Investments, s.r.o. — investiční poradce fondu, Pobřežní 394/12, Praha 8",
              source_id="inibio-home", note="Česká kancelář poradce reprezentuje investiční organizaci v pilotu. Samotný fond je domicilován v Lucembursku.")
for field, value in (("fund_domicile", "Lucembursko — i&i Biotech Fund I SCSp"),
                     ("investment_adviser", "Biotech Investments, s.r.o., Praha")):
    cid = f"inibio.{field}.1"
    if not any(c["id"] == cid for c in p["claims"]):
        p["claims"].append(dict(id=cid, investor_id="inibio", field=field, value=value,
                                source_id="inibio-home", scope="fund" if field == "fund_domicile" else "organization",
                                valid_as_of=None, status="supported", note="Doplněno po druhém kole skutečné ruční kontroly."))
for d in p["decisions"]:
    extras = {"depo": ["tapaya-primary"], "inibio": ["sampling-human"], "genesis": ["genesis-home"]}.get(d["candidate_id"], [])
    d["source_ids"] = list(dict.fromkeys(d["source_ids"] + extras))
p["out_of_scope"] = [dict(candidate_id="genesis", investor_type="private_equity; growth_equity",
                           source_ids=["genesis-home", "genesis"],
                           note="Skutečný investor uchovaný samostatně mimo VC pilot na výslovný pokyn uživatele. Nejde o zařazení do ověřené globální databáze.")]
dump_json(root / "data/pilot.json", p)
