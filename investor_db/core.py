"""Validation, transparent metrics, and deterministic exports.

Supported means a source supports a statement, NOT that a human audited it.
No code here infers AUM, replaces missing values, or calls a model.
"""
from __future__ import annotations

import calendar
import csv
import hashlib
import json
import math
import re
import sqlite3
import tempfile
from collections import Counter
from contextlib import closing
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

LABELS = {"include", "exclude", "needs_review"}
STATUSES = {"supported", "inferred", "partial", "not_found", "not_disclosed",
            "historical_unconfirmed", "undated_reference"}
REQUIRED = ("name", "website", "investor_type", "czech_office", "sectors", "stage",
            "geography", "ticket", "total_investment_capital")
REVIEW_FIELDS = ("candidate_id", "label", "reviewer", "reviewed_on", "reason", "source_ids")
CLAIM_REVIEW_FIELDS = ("claim_id", "label", "reviewer", "reviewed_on", "reason")


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dump_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def unique(rows, label):
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError(f"Duplicate {label} ID")
    return set(ids)


def valid_url(value):
    url = urlparse(value)
    return url.scheme in {"https", "http"} and bool(url.hostname) and not url.username and not url.password


def date_bounds(value, precision):
    """Preserve year precision; never pretend January 1 is an observed day."""
    if precision == "unknown":
        if value is not None:
            raise ValueError("Unknown date must be null")
        return None
    if precision == "day" and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value or ""):
        point = date.fromisoformat(value)
        return point, point
    if precision == "year" and re.fullmatch(r"\d{4}", value or ""):
        year = int(value)
        return date(year, 1, 1), date(year, 12, 31)
    raise ValueError(f"Invalid {precision} date: {value}")


def cutoff_date(as_of):
    year = as_of.year - 2
    return date(year, as_of.month, min(as_of.day, calendar.monthrange(year, as_of.month)[1]))


def activity(transactions, as_of):
    threshold = cutoff_date(date.fromisoformat(as_of))
    known = [date_bounds(t["date"], t["date_precision"]) for t in transactions]
    if any(bounds and bounds[0] >= threshold for bounds in known):
        return "recent_activity_evidenced"
    if known and all(bounds and bounds[1] < threshold for bounds in known):
        return "historical_activity_only"
    return "activity_date_unknown"


def money(value, ticket=False):
    if not isinstance(value, dict) or value.get("currency") not in {"EUR", "USD", "CZK"}:
        raise ValueError("Money needs an explicit supported currency")
    keys = ("min", "max") if ticket else ("amount",)
    for key in keys:
        if type(value.get(key)) not in {int, float} or not math.isfinite(value[key]) or value[key] <= 0:
            raise ValueError("Money must be finite and positive; missing is null, not zero")
    if ticket and (value["min"] > value["max"] or not value.get("basis")):
        raise ValueError("Invalid ticket range or missing basis")


def validate(pilot, candidates, predictions):
    as_of = date.fromisoformat(pilot["as_of"])
    cids = unique(candidates["candidates"], "candidate")
    sids = unique(pilot["sources"], "source")
    iids = unique(pilot["investors"], "investor")
    unique(pilot["claims"], "claim")
    unique(pilot["transactions"], "transaction")
    fids = unique(pilot["funds"], "fund")
    if not iids <= cids:
        raise ValueError("Investor missing from frozen candidate set")
    for src in pilot["sources"]:
        if not valid_url(src["url"]) or not all(src.get(k) for k in ("title", "publisher", "evidence_summary")):
            raise ValueError(f"Incomplete source {src['id']}")
        checked = date.fromisoformat(src["accessed_on"])
        if checked > as_of or (src["published_on"] and date.fromisoformat(src["published_on"]) > checked):
            raise ValueError("Source date in future")
    for claim in pilot["claims"]:
        if claim["source_id"] not in sids or claim["investor_id"] not in iids:
            raise ValueError("Claim has dangling reference")
        if claim["status"] not in STATUSES:
            raise ValueError("Invalid claim status")
        if claim["status"] in {"not_found", "not_disclosed"} and claim["value"] is not None:
            raise ValueError("Missing claim must have null value")
        if claim["status"] not in {"not_found", "not_disclosed"} and claim["value"] is None:
            raise ValueError("Non-missing claim cannot be null")
        if claim["scope"].startswith("fund:") and claim["scope"][5:] not in fids:
            raise ValueError("Unknown fund scope")
        if claim.get("valid_as_of") and date.fromisoformat(claim["valid_as_of"]) > as_of:
            raise ValueError("Claim date in future")
        if claim["value"] is not None:
            if claim["field"] == "ticket":
                money(claim["value"], ticket=True)
            if claim["field"] in {"capital_reference", "total_investment_capital"}:
                money(claim["value"])
            if claim["field"] == "total_investment_capital":
                if claim["value"]["metric"] != "manager_aum" or claim["scope"] not in {"manager", "organization"}:
                    raise ValueError("Targets, fund sizes or invested capital cannot masquerade as total AUM")
    for tx in pilot["transactions"]:
        if tx["investor_id"] not in iids or tx["source_id"] not in sids or not tx["company"].strip():
            raise ValueError("Transaction has dangling reference or no named company")
        if not set(tx["corroborating_source_ids"]) <= sids:
            raise ValueError("Unknown corroborating source")
        bounds = date_bounds(tx["date"], tx["date_precision"])
        if bounds and bounds[0] > as_of:
            raise ValueError("Future transaction")
        if not tx.get("date_kind") or tx["evidence_kind"] != "named_investment":
            raise ValueError("Transaction needs evidence and date kind")
        for field in ("round_amount", "investor_contribution"):
            if tx[field] is not None:
                money(tx[field])
        if tx["investor_contribution"] is not None and not tx.get("contribution_source_id"):
            raise ValueError("Contribution needs separate explicit evidence")
        if tx.get("contribution_source_id") and tx["contribution_source_id"] not in sids:
            raise ValueError("Unknown contribution evidence source")
    for row in pilot.get("out_of_scope", []):
        if row["candidate_id"] not in cids or not set(row["source_ids"]) <= sids:
            raise ValueError("Out-of-scope classification has dangling reference")
    for fund in pilot["funds"]:
        if fund["investor_id"] not in iids or fund["source_id"] not in sids:
            raise ValueError("Fund has dangling reference")
    for collection, key in ((pilot["decisions"], "prediction"), (predictions["predictions"], "prediction")):
        ids = [row["candidate_id"] for row in collection]
        if len(ids) != len(set(ids)) or set(ids) != cids:
            raise ValueError("Exactly one decision per frozen candidate required")
        for row in collection:
            if row[key] not in LABELS or not row["reason"] or not set(row["source_ids"]) <= sids:
                raise ValueError("Invalid decision or source")
    for row in pilot["decisions"]:
        if row["prediction"] == "include":
            iid = row["candidate_id"]
            if iid not in iids:
                raise ValueError("Accepted candidate missing investor record")
            facts = {c["field"]: c for c in pilot["claims"] if c["investor_id"] == iid}
            if not set(REQUIRED) <= facts.keys():
                raise ValueError("Accepted investor missing required fields, including explicit missing values")
            if not facts["czech_office"]["value"] or facts["czech_office"]["status"] != "supported":
                raise ValueError("Accepted investor needs evidenced Czech presence")
            if not any(t["investor_id"] == iid for t in pilot["transactions"]):
                raise ValueError("Accepted investor has no named investment")
    return True


def wilson(successes, total):
    if not total:
        return None
    z = 1.959963984540054
    p = successes / total
    divisor = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / divisor
    half = z * math.sqrt(p * (1-p) / total + z*z / (4 * total*total)) / divisor
    return [max(0, centre - half), min(1, centre + half)]


def read_review(path, known_ids, *, claims=False):
    if not Path(path).exists():
        return []
    with Path(path).open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        expected = CLAIM_REVIEW_FIELDS if claims else REVIEW_FIELDS
        if reader.fieldnames != list(expected):
            raise ValueError(f"Review CSV columns must be {expected}")
        rows = list(reader)
    key = "claim_id" if claims else "candidate_id"
    ids = [row[key] for row in rows]
    if len(ids) != len(set(ids)) or not set(ids) <= known_ids:
        raise ValueError("Duplicate or unknown review ID")
    labels = {"supported", "incorrect", "uncertain"} if claims else LABELS
    completed = []
    for row in rows:
        if not row["label"]:
            if any(row[k] for k in expected if k != key):
                raise ValueError("Partially filled review row without label")
            continue
        if row["label"] not in labels or not all(row[k].strip() for k in ("reviewer", "reviewed_on", "reason")):
            raise ValueError("Review needs valid label, human reviewer, date and reason")
        if re.search(r"\b(ai|codex|claude|gpt|assistant|agent)\b", row["reviewer"], flags=re.I):
            raise ValueError("AI cannot be the human reference reviewer")
        if date.fromisoformat(row["reviewed_on"]) > date.today():
            raise ValueError("Review date in future")
        completed.append(row)
    return completed


def classification_metrics(predictions, reviews):
    preds = {r["candidate_id"]: r["prediction"] for r in predictions}
    gold = {r["candidate_id"]: r["label"] for r in reviews}
    if len(preds) != len(predictions) or len(gold) != len(reviews) or not gold.keys() <= preds.keys():
        raise ValueError("Unknown or duplicate IDs in metrics")
    matrix = {p: {g: 0 for g in sorted(LABELS)} for p in sorted(LABELS)}
    for iid, label in gold.items():
        if label not in LABELS or preds[iid] not in LABELS:
            raise ValueError("Invalid metric label")
        matrix[preds[iid]][label] += 1
    tp = matrix["include"]["include"]
    fp = matrix["include"]["exclude"]
    unresolved_positive = matrix["include"]["needs_review"]
    predicted_positive = sum(p == "include" for p in preds.values())
    evaluated_positive = tp + fp
    fn = matrix["exclude"]["include"]
    abstained_positive = matrix["needs_review"]["include"]
    positives = tp + fn + abstained_positive
    return dict(
        human_reviewed=len(reviews), candidates=len(preds), pending=len(preds)-len(reviews),
        initial_decisions=dict(Counter(preds.values())), matrix=matrix,
        precision={"numerator": tp, "denominator": evaluated_positive,
                   "value": tp / evaluated_positive if evaluated_positive else None,
                   "wilson_95": wilson(tp, evaluated_positive),
                   "scope": "Only reviewed, resolved initial positive predictions; not a random population estimate"},
        reviewed_initial_positive=evaluated_positive,
        initial_positive_total=predicted_positive,
        initial_positive_not_resolved=predicted_positive - evaluated_positive,
        reviewed_but_unresolved_positive=unresolved_positive,
        precision_bounds_all_initial_positives=(
            [tp/predicted_positive, (tp + predicted_positive-evaluated_positive)/predicted_positive]
            if predicted_positive else None),
        recall_in_reviewed_candidate_set={"numerator": tp, "denominator": positives,
                                          "value": tp/positives if positives else None},
        false_negatives_excluding_abstentions=fn, abstained_true_positives=abstained_positive,
        note="No human review => precision null, never 100%. Wilson interval is descriptive for this purposive sample, not global coverage.",
    )


def first_claim(pilot, iid, field):
    return next(c for c in pilot["claims"] if c["investor_id"] == iid and c["field"] == field)


def publication_ids(pilot, reviews):
    """Publish only agreement between current AI and a resolved human include."""
    human = {r["candidate_id"]: r["label"] for r in reviews}
    return {d["candidate_id"] for d in pilot["decisions"]
            if d["prediction"] == "include" and human.get(d["candidate_id"]) == "include"}


def verification_flags(pilot, iid, reviews, claim_reviews):
    factual = {c["id"] for c in pilot["claims"] if c["investor_id"] == iid and c["value"] is not None}
    supported = {r["claim_id"] for r in claim_reviews if r["label"] == "supported"}
    return dict(classification_human_verified=any(r["candidate_id"] == iid and r["label"] == "include" for r in reviews),
                attributes_human_verified=bool(factual) and factual <= supported)


def coverage(pilot, ids=None):
    if ids is None:
        ids = [d["candidate_id"] for d in pilot["decisions"] if d["prediction"] == "include"]
    result = {}
    for field in ("sectors", "stage", "ticket", "total_investment_capital"):
        cs = [first_claim(pilot, iid, field) for iid in ids]
        n = sum(c["value"] is not None and c["status"] == "supported" for c in cs)
        result[field] = dict(numerator=n, denominator=len(ids), fraction=n/len(ids) if ids else None)
    return result


def write_csv(path, rows, fields=None):
    if not fields:
        fields = list(rows[0]) if rows else []
    with Path(path).open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            # JSON fields round-trip without conflating null with numeric zero.
            writer.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v
                             for k, v in row.items()})


def review_templates(root, candidates, pilot):
    folder = root / "review"
    folder.mkdir(exist_ok=True)
    for name, ids, fields, key in (
        ("labels.csv", [c["id"] for c in candidates["candidates"]], REVIEW_FIELDS, "candidate_id"),
        ("claims.csv", [c["id"] for c in pilot["claims"]], CLAIM_REVIEW_FIELDS, "claim_id"),
    ):
        path = folder / name
        if not path.exists():
            write_csv(path, [{field: iid if field == key else "" for field in fields} for iid in ids], list(fields))
        else:
            with path.open(encoding="utf-8-sig", newline="") as file:
                reader = csv.DictReader(file)
                if reader.fieldnames != list(fields):
                    raise ValueError("Unexpected review template columns")
                present = {row[key] for row in reader}
            missing = [iid for iid in ids if iid not in present]
            if missing:
                # Append only; never replace an existing human annotation.
                with path.open("a", encoding="utf-8", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=fields)
                    for iid in missing:
                        writer.writerow({field: iid if field == key else "" for field in fields})


def _sqlite_export(path, pilot, candidates, predictions, reviews, claim_reviews):
    tmp = path.with_suffix(".tmp.sqlite")
    if tmp.exists():
        raise ValueError(f"Temporary output already exists: {tmp}")
    with closing(sqlite3.connect(tmp)) as db, db:
        db.executescript("""
        PRAGMA foreign_keys = ON;
        CREATE TABLE candidates(id TEXT PRIMARY KEY, name TEXT NOT NULL, discovery TEXT NOT NULL);
        CREATE TABLE sources(id TEXT PRIMARY KEY, url TEXT NOT NULL, publisher TEXT NOT NULL,
          title TEXT NOT NULL, published_on TEXT, accessed_on TEXT NOT NULL, kind TEXT NOT NULL,
          access_method TEXT NOT NULL, evidence_summary TEXT NOT NULL);
        CREATE TABLE investors(id TEXT PRIMARY KEY REFERENCES candidates(id), name TEXT NOT NULL,
          website TEXT NOT NULL, entity_level TEXT NOT NULL,
          classification_human_verified INTEGER NOT NULL, attributes_human_verified INTEGER NOT NULL,
          published INTEGER NOT NULL);
        CREATE TABLE funds(id TEXT PRIMARY KEY, investor_id TEXT NOT NULL REFERENCES investors(id),
          name TEXT NOT NULL, source_id TEXT NOT NULL REFERENCES sources(id));
        CREATE TABLE claims(id TEXT PRIMARY KEY, investor_id TEXT NOT NULL REFERENCES investors(id),
          field TEXT NOT NULL, value_json TEXT NOT NULL, source_id TEXT NOT NULL REFERENCES sources(id),
          scope TEXT NOT NULL, valid_as_of TEXT, status TEXT NOT NULL, note TEXT NOT NULL);
        CREATE TABLE transactions(id TEXT PRIMARY KEY, investor_id TEXT NOT NULL REFERENCES investors(id),
          company TEXT NOT NULL, source_id TEXT NOT NULL REFERENCES sources(id), date TEXT,
          date_precision TEXT NOT NULL, date_kind TEXT NOT NULL, round_amount_json TEXT NOT NULL,
          investor_contribution_json TEXT NOT NULL, note TEXT NOT NULL,
          contribution_source_id TEXT REFERENCES sources(id));
        CREATE TABLE out_of_scope_classifications(candidate_id TEXT PRIMARY KEY REFERENCES candidates(id),
          investor_type TEXT NOT NULL, source_ids_json TEXT NOT NULL, note TEXT NOT NULL);
        CREATE TABLE transaction_sources(transaction_id TEXT REFERENCES transactions(id),
          source_id TEXT REFERENCES sources(id), PRIMARY KEY(transaction_id, source_id));
        CREATE TABLE decisions(candidate_id TEXT PRIMARY KEY REFERENCES candidates(id),
          prediction TEXT NOT NULL, reason TEXT NOT NULL);
        CREATE TABLE decision_sources(candidate_id TEXT REFERENCES decisions(candidate_id),
          source_id TEXT REFERENCES sources(id), PRIMARY KEY(candidate_id, source_id));
        CREATE TABLE initial_predictions(candidate_id TEXT PRIMARY KEY REFERENCES candidates(id),
          prediction TEXT NOT NULL, reason TEXT NOT NULL);
        CREATE TABLE human_reviews(candidate_id TEXT PRIMARY KEY REFERENCES candidates(id),
          label TEXT NOT NULL, reviewer TEXT NOT NULL, reviewed_on TEXT NOT NULL, reason TEXT NOT NULL, source_ids TEXT NOT NULL);
        CREATE TABLE human_claim_reviews(claim_id TEXT PRIMARY KEY REFERENCES claims(id),
          label TEXT NOT NULL, reviewer TEXT NOT NULL, reviewed_on TEXT NOT NULL, reason TEXT NOT NULL);
        CREATE INDEX claims_by_investor_field ON claims(investor_id,field);
        CREATE INDEX transactions_by_investor ON transactions(investor_id);
        CREATE VIEW published_investors AS SELECT * FROM investors WHERE published=1;
        CREATE VIEW claim_verification AS
          SELECT c.id AS claim_id, h.label AS human_review_label,
          CASE WHEN c.value_json != 'null' AND h.label='supported' THEN 1 ELSE 0 END AS attribute_human_verified
          FROM claims c LEFT JOIN human_claim_reviews h ON h.claim_id=c.id;
        """)
        db.executemany("INSERT INTO candidates VALUES (:id,:name,:discovery)", candidates["candidates"])
        for table in ("sources", "investors", "funds"):
            for row in pilot[table]:
                if table == "investors":
                    row = dict(row, **verification_flags(pilot, row["id"], reviews, claim_reviews),
                               published=row["id"] in publication_ids(pilot, reviews))
                columns = ",".join(row)
                db.execute(f"INSERT INTO {table} ({columns}) VALUES ({','.join('?' for _ in row)})", tuple(row.values()))
        for c in pilot["claims"]:
            db.execute("INSERT INTO claims VALUES (?,?,?,?,?,?,?,?,?)",
                       (c["id"], c["investor_id"], c["field"], json.dumps(c["value"], ensure_ascii=False),
                        c["source_id"], c["scope"], c["valid_as_of"], c["status"], c["note"]))
        for t in pilot["transactions"]:
            db.execute("INSERT INTO transactions VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                       (t["id"], t["investor_id"], t["company"], t["source_id"], t["date"], t["date_precision"],
                        t["date_kind"], json.dumps(t["round_amount"]), json.dumps(t["investor_contribution"]), t["note"], t.get("contribution_source_id")))
            db.executemany("INSERT INTO transaction_sources VALUES (?,?)", [(t["id"], s) for s in t["corroborating_source_ids"]])
        for table, rows in (("decisions", pilot["decisions"]), ("initial_predictions", predictions["predictions"])):
            db.executemany(f"INSERT INTO {table} VALUES (?,?,?)", [(d["candidate_id"], d["prediction"], d["reason"]) for d in rows])
        db.executemany("INSERT INTO decision_sources VALUES (?,?)", [(d["candidate_id"], s) for d in pilot["decisions"] for s in d["source_ids"]])
        db.executemany("INSERT INTO human_reviews VALUES (:candidate_id,:label,:reviewer,:reviewed_on,:reason,:source_ids)", reviews)
        db.executemany("INSERT INTO human_claim_reviews VALUES (:claim_id,:label,:reviewer,:reviewed_on,:reason)", claim_reviews)
        db.executemany("INSERT INTO out_of_scope_classifications VALUES (?,?,?,?)",
                       [(r["candidate_id"], r["investor_type"], json.dumps(r["source_ids"]), r["note"]) for r in pilot.get("out_of_scope", [])])
        if db.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("SQLite referential integrity failed")
    tmp.replace(path)


def sqlite_export(path, pilot, candidates, predictions, reviews, claim_reviews):
    # A failed build cannot leave a half-written database at the output path.
    with tempfile.TemporaryDirectory(prefix="investor-build-", dir=path.parent) as folder:
        temp_path = Path(folder) / "investors.sqlite"
        _sqlite_export(temp_path, pilot, candidates, predictions, reviews, claim_reviews)
        temp_path.replace(path)


def markdown(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def display(value):
    if value is None:
        return "nezjištěno"
    if isinstance(value, dict):
        if "min" in value:
            return f"{value['min']:,}-{value['max']:,} {value['currency']} ({value['basis']})"
        bound = {"greater_than": ">", "approximate": "cca "}.get(value.get("bound"), "")
        suffix = f" ({value['metric']})" if value.get("metric") else ""
        return f"{bound}{value['amount']:,} {value['currency']}{suffix}"
    return str(value)


def claim_audit_packet(root, pilot, claim_reviews):
    config_path = root / 'data/claim_audit_sample.json'
    if not config_path.exists():
        return
    config = read_json(config_path)
    claims = {c['id']: c for c in pilot['claims']}
    sources = {s['id']: s for s in pilot['sources']}
    reviews = {r['claim_id']: r for r in claim_reviews}
    lines = ['# Malý lidský audit atributů', '', config['selection_rule'], '',
             'Výběr byl stanoven před vyplněním lidských štítků. Jde o záměrný rizikový audit, nikoli reprezentativní odhad. Kontroly AI nejsou lidské štítky.', '',
             'Vyplňte odpovídající řádky v review/claims.csv: label (supported / incorrect / uncertain), reviewer, reviewed_on a reason. Datum, identitu ani čas za kontrolora nedoplňujeme. Čas lze nově měřit; historický čas zůstává neznámý.', '',
             '| ID tvrzení | Hodnota | Stav AI | Přesná URL | Kontrolní otázka | Lidský štítek |', '|---|---|---|---|---|---|']
    rows = []
    for cid in config['claim_ids']:
        c = claims[cid]
        if c['value'] is None:
            raise ValueError('Missing values cannot be positive factual audit claims')
        question = ('Dokládá zdroj přesně částku, měnu, rozsah (fond/správce), typ kapitálu a datum? Nejde o cíl, historickou částku nebo proinvestovaný kapitál vydávaný za AUM?'
                    if c['field'] in {'capital_reference', 'total_investment_capital'} else
                    'Dokládá zdroj celé rozpětí, měnu a význam ticketu? Porovnejte i alternativní tvrzení stejného investora.' if c['field'] == 'ticket' else
                    'Dokládá zdroj tento investiční mandát, nebo jde pouze o odvození z portfolia?')
        r = reviews.get(cid, {})
        url = sources[c['source_id']]['url']
        lines.append(f"| {cid} | {markdown(display(c['value']))} | {c['status']} | {url} | {question} | {r.get('label', '')} |")
        rows.append(dict(claim_id=cid, value=display(c['value']), source_url=url, question=question,
                         **{k: r.get(k, '') for k in CLAIM_REVIEW_FIELDS if k != 'claim_id'}))
    lines.extend(['', '## Chybějící údaje - samostatná kontrola rozsahu hledání', '',
                  'Následující null nejsou pozitivní faktická tvrzení a nevstupují do přesnosti atributů. Nezjištěná hodnota není automaticky chyba. Rozsah nové rešerše: [CAPITAL_RESEARCH.md](CAPITAL_RESEARCH.md).', ''])
    for c in pilot['claims']:
        if c['value'] is None:
            lines.append(f"- {c['id']}: {c['status']}; [{c['source_id']}]({sources[c['source_id']]['url']}).")
    (root / 'reports/CLAIM_AUDIT.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    write_csv(root / 'exports/claim_audit_worksheet.csv', rows)


def report(root, pilot, candidates, metrics, predictions, reviews):
    srcs = {s["id"]: s for s in pilot["sources"]}
    dest = root / "reports"
    dest.mkdir(exist_ok=True)
    lines = ["# Pilot českých VC investorů", "", f"Stav zdrojů: {pilot['as_of']}. Lidská klasifikace: {metrics['classification']['human_reviewed']}/{metrics['classification']['candidates']}. Audit atributů: {metrics['claims']['human_reviewed']} kontrol.", "",
             "Lidské potvrzení klasifikace neznamená ověření všech atributů. Částky jsou self-reported nebo historické; prázdná hodnota není nula.", "",
             "Publikovaný přehled vyžaduje současně aktuální AI include a lidské include. Nevyřešené nebo rozporné případy se nepublikují. Úplné evidence zůstávají v normalizovaných exportech.", "",
             "Lighthouse: AI dosud nerozřešila identitu discovery kandidáta; člověk původní kandidát vyloučil. Jde o odlišná rozhodnutí, nikoli automatické ztotožnění s českým fondem stejného názvu.", "",
             "| Investor | Původní AI | Aktuální AI | Lidská reference | Publikován | Důvod AI |", "|---|---|---|---|---|---|"]
    initial = {d['candidate_id']: d['prediction'] for d in predictions['predictions']}
    human = {r['candidate_id']: r['label'] for r in reviews}
    published = publication_ids(pilot, reviews)
    names = {c["id"]: c["name"] for c in candidates["candidates"]}
    for d in pilot["decisions"]:
        iid = d['candidate_id']
        lines.append(f"| {names[iid]} | {initial[iid]} | {d['prediction']} | {human.get(iid, 'nezkontrolováno')} | {'ano' if iid in published else 'ne'} | {markdown(d['reason'])} |")
    for inv in pilot["investors"]:
        iid = inv["id"]
        if iid not in published:
            continue
        txs = [t for t in pilot["transactions"] if t["investor_id"] == iid]
        lines.extend(["", f"## {inv['name']}", "", f"Aktivita: `{activity(txs, pilot['as_of'])}`. Jednotka: investiční organizace, nikoli počet jednotlivých fondů.", "",
                      "| Údaj | Hodnota | Stav | Zdroj / kontrola | Poznámka |", "|---|---|---|---|---|"])
        for c in (c for c in pilot["claims"] if c["investor_id"] == iid):
            src = srcs[c["source_id"]]
            lines.append(f"| {c['field']} | {markdown(display(c['value']))} | {c['status']} | [{src['id']}]({src['url']}) / {src['accessed_on']} | {markdown(c['note'])} |")
        lines.extend(["", "Důkaz skutečné investice:", ""])
        for tx in txs:
            src = srcs[tx["source_id"]]
            lines.append(f"- **{tx['company']}** — {tx['date'] or 'datum neznámé'} ({tx['date_kind']}, přesnost {tx['date_precision']}); [{src['title']}]({src['url']}); kontrola {src['accessed_on']}. {tx['note']}")
            if tx["investor_contribution"] is not None:
                evidence = srcs[tx["contribution_source_id"]]
                lines.append(f"  Vlastní vklad investora: **{display(tx['investor_contribution'])}**; [výslovný důkaz částky]({evidence['url']}).")
    if pilot.get("out_of_scope"):
        lines.extend(["", "## Samostatně evidovaní investoři mimo VC pilot", ""])
        for row in pilot["out_of_scope"]:
            links = "; ".join(f"[{sid}]({srcs[sid]['url']})" for sid in row["source_ids"])
            lines.append(f"- **{names[row['candidate_id']]}** — {row['investor_type']}. {row['note']} Zdroje: {links}.")
    (dest / "PILOT.md").write_text(("\n".join(lines) + "\n").replace('—', '-').replace('–', '-'), encoding="utf-8")
    p = metrics["classification"]["precision"]
    val = f"{p['value']:.1%}" if p["value"] is not None else "NEZMĚŘENO — chybí ruční referenční štítky"
    if p["value"] is not None and metrics["classification"]["pending"]:
        val = f"PRŮBĚŽNĚ {p['numerator']}/{p['denominator']} vyhodnocených pozitivních predikcí správně; kontrola vzorku není dokončena"
    recall = metrics['classification']['recall_in_reviewed_candidate_set']
    quality = ["# Výsledek měření", "", f"Precision původních pozitivních klasifikací: **{p['numerator']}/{p['denominator']} na záměrně vybraném vzorku** ({val}).", "",
               f"Zkontrolováno člověkem: {metrics['classification']['human_reviewed']}/{metrics['classification']['candidates']} kandidátů. Precision TP/(TP+FP).", "",
               f"Recall v kontrolovaném seznamu: {recall['numerator']}/{recall['denominator']} ({recall['value']:.1%}). Původní abstence u Purple s lidským include snižuje recall; opravená AI predikce nepřepisuje původní měření." if recall['value'] is not None else "Recall nebyl změřen.", "",
               "Výsledek precision neznamená 100% správnost celé databáze ani odhad přesnosti na světovém trhu. Správnost atributů se měří odděleně; úplnost měří dostupnost údajů, nikoli jejich pravdivost.", "",
               f"Audit pozitivních faktických tvrzení: {metrics['claims']['human_reviewed']} lidských kontrol; přesnost {metrics['claims']['accuracy'] if metrics['claims']['accuracy'] is not None else 'nezměřena'}. Podklady: [CLAIM_AUDIT.md](CLAIM_AUDIT.md).", "",
               "Bez lidské kontroly neuvádíme procento přesnosti. Automatická validace kontroluje strukturu, nikoli pravdivost.", "",
               "## Úplnost přijatých organizací", "", "Počítají se jen tvrzení se stavem supported; historické a částečné hodnoty jsou v datech, ale tuto úplnost nezvyšují.", "",
               "| Pole | Doloženo |", "|---|---|"]
    for field, value in metrics["coverage"].items():
        quality.append(f"| {field} | {value['numerator']}/{value['denominator']} |")
    quality.extend(["", "Úplné výsledky, abstence, nezkontrolované pozitivní predikce a matice záměn: [metrics.json](../exports/metrics.json).",
                    "", "Wilsonův interval je při malé záměrné vzorce pouze popisný. Nejde o odhad celosvětové přesnosti ani recall trhu."])
    (dest / "ACCURACY.md").write_text(("\n".join(quality) + "\n").replace('—', '-').replace('–', '-'), encoding="utf-8")
    readme = root / 'README.md'
    if readme.exists():
        text = readme.read_text(encoding='utf-8')
        start, end = '<!-- METRICS:START -->', '<!-- METRICS:END -->'
        if start in text and end in text:
            block = (f"{start}\n"
                     f"Publikováno **{len(published)} investorů** z {metrics['classification']['candidates']} zmrazených kandidátů; lidská klasifikace {metrics['classification']['human_reviewed']}/{metrics['classification']['candidates']}. "
                     f"Původní AI: {metrics['classification']['initial_decisions']}. Aktuální AI: {dict(Counter(d['prediction'] for d in pilot['decisions']))}. Lidská reference: {dict(Counter(r['label'] for r in reviews))}. "
                     f"{len(pilot['sources'])} zdrojů, {len(pilot['claims'])} tvrzení, {len(pilot['transactions'])} investičních důkazů.\n\n"
                     f"**Precision původních pozitivních klasifikací: {p['numerator']}/{p['denominator']} na záměrně vybraném vzorku.** "
                     f"Recall v kontrolovaném seznamu: {recall['numerator']}/{recall['denominator']}; původní abstence Purple snižuje recall. "
                     f"To neznamená 100% správnost celé databáze ani odhad přesnosti světového trhu. "
                     f"Lidský audit atributů: {metrics['claims']['human_reviewed']} kontrol; správnost atributů je samostatná veličina.\n\n"
                     "Úplnost supported atributů publikovaných investorů: " + '; '.join(f"{k} {v['numerator']}/{v['denominator']}" for k, v in metrics['coverage'].items()) + f". Úplnost není přesnost.\n{end}")
            text = text[:text.index(start)] + block + text[text.index(end)+len(end):]
            readme.write_text(text, encoding='utf-8')
    packet = ["# Podklady pro ruční kontrolu", "", f"Klasifikace zkontrolována: {metrics['classification']['human_reviewed']}/{metrics['classification']['candidates']}. Zdroje níže zůstávají podkladem pro opakovanou kontrolu. Zbývající atributový audit: [CLAIM_AUDIT.md](CLAIM_AUDIT.md).", "",
              "Pozitivní případ: skutečný přímý VC investor s českou kanceláří a konkrétní doloženou investicí. PE může být skutečný investor, ale mimo tento VC pilot.", "",
              "Otevřete původní zdroje, nespoléhejte na parafráze AI. Datum přístupu nenahrazuje datum transakce. K nejasné identitě patří needs_review."]
    by_decision = {d["candidate_id"]: d for d in pilot["decisions"]}
    for candidate in candidates["candidates"]:
        packet.extend(["", f"## {candidate['id']} — {candidate['name']}", ""])
        for sid in by_decision[candidate["id"]]["source_ids"]:
            src = srcs[sid]
            packet.append(f"- [{src['title']}]({src['url']}) — {src['publisher']}; publikace {src['published_on'] or 'neuvedena'}; přístup {src['accessed_on']}.")
    (dest / "REVIEW_PACKET.md").write_text(("\n".join(packet) + "\n").replace('—', '-').replace('–', '-'), encoding="utf-8")


def build(root):
    pilot = read_json(root / "data/pilot.json")
    candidates = read_json(root / "data/candidates.json")
    predictions = read_json(root / "data/predictions.json")
    if hashlib.sha256((root / "data/candidates.json").read_bytes().replace(b"\r\n", b"\n")).hexdigest() != predictions["candidate_sha256"]:
        raise ValueError("Frozen candidate file changed")
    validate(pilot, candidates, predictions)
    review_templates(root, candidates, pilot)
    reviews = read_review(root / "review/labels.csv", {c["id"] for c in candidates["candidates"]})
    for row in reviews:
        if not row["source_ids"].strip() or not set(row["source_ids"].split(";")) <= {s["id"] for s in pilot["sources"]}:
            raise ValueError("Review must cite known source IDs separated by semicolons")
    claim_reviews = read_review(root / "review/claims.csv", {c["id"] for c in pilot["claims"]}, claims=True)
    out = root / "exports"
    out.mkdir(exist_ok=True)
    factual_ids = {c['id'] for c in pilot['claims'] if c['value'] is not None}
    factual_reviews = [r for r in claim_reviews if r['claim_id'] in factual_ids]
    resolved_claims = [r for r in factual_reviews if r["label"] != "uncertain"]
    accepted = publication_ids(pilot, reviews)
    human_labels = {r['candidate_id']: r['label'] for r in reviews}
    initial_labels = {r['candidate_id']: r['prediction'] for r in predictions['predictions']}
    current_labels = {r['candidate_id']: r['prediction'] for r in pilot['decisions']}
    metrics = dict(as_of=pilot["as_of"], classification=classification_metrics(predictions["predictions"], reviews),
                   coverage=coverage(pilot, accepted),
                   claims={"human_reviewed": len(factual_reviews), "total": len(factual_ids),
                           "missing_value_reviews": len(claim_reviews)-len(factual_reviews),
                           "correct": sum(r["label"] == "supported" for r in resolved_claims),
                           "resolved": len(resolved_claims),
                           "accuracy": sum(r["label"] == "supported" for r in resolved_claims)/len(resolved_claims) if resolved_claims else None},
                   source_link_coverage={"numerator": len(pilot["claims"]), "denominator": len(pilot["claims"]),
                                         "meaning": "Structural reference coverage only; missing-value search scope also has sources; not claim truth"})
    dump_json(out / "metrics.json", metrics)
    for table in ("sources", "investors", "claims", "transactions", "funds", "decisions"):
        rows = pilot[table]
        if table == 'investors':
            rows = [dict(r, **verification_flags(pilot, r['id'], reviews, claim_reviews), published=r['id'] in accepted) for r in rows]
            dump_json(out / 'investors.json', rows)
        if table == 'claims':
            labels = {r['claim_id']: r['label'] for r in claim_reviews}
            rows = [dict(r, attribute_human_verified=r['value'] is not None and labels.get(r['id']) == 'supported', human_review_label=labels.get(r['id'])) for r in rows]
            dump_json(out / 'claims.json', rows)
        fields = list(dict.fromkeys(key for row in rows for key in row))
        write_csv(out / f"{table}.csv", rows, fields)
    if pilot.get("out_of_scope"):
        write_csv(out / "out_of_scope.csv", pilot["out_of_scope"])
    summary = []
    for inv in pilot["investors"]:
        if inv["id"] not in accepted:
            continue
        iid = inv["id"]
        row = {"id": iid, "name": inv["name"], **verification_flags(pilot, iid, reviews, claim_reviews),
               "initial_ai_prediction": initial_labels[iid], "current_ai_prediction": current_labels[iid],
               "human_reference_label": human_labels.get(iid),
               "activity": activity([t for t in pilot["transactions"] if t["investor_id"] == iid], pilot["as_of"])}
        for field in ("sectors", "stage", "ticket", "total_investment_capital"):
            c = first_claim(pilot, iid, field)
            row[field] = display(c["value"])
            row[field+"_status"] = c["status"]
            row[field+"_source_url"] = next(s["url"] for s in pilot["sources"] if s["id"] == c["source_id"])
            row[field+"_human_verified"] = c['value'] is not None and any(r['claim_id'] == c['id'] and r['label'] == 'supported' for r in claim_reviews)
        summary.append(row)
    summary_fields = ['id', 'name', 'classification_human_verified', 'attributes_human_verified',
                      'initial_ai_prediction', 'current_ai_prediction', 'human_reference_label', 'activity']
    for field in ('sectors', 'stage', 'ticket', 'total_investment_capital'):
        summary_fields.extend([field, field+'_status', field+'_source_url', field+'_human_verified'])
    write_csv(out / "investor_summary.csv", summary, summary_fields)
    sqlite_export(out / "investors.sqlite", pilot, candidates, predictions, reviews, claim_reviews)
    report(root, pilot, candidates, metrics, predictions, reviews)
    claim_audit_packet(root, pilot, claim_reviews)
    dump_json(out / "manifest.json", {str(p.relative_to(root)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest()
                                    for p in (root / "data/candidates.json", root / "data/predictions.json", root / "data/pilot.json",
                                              root / "review/labels.csv", root / "review/claims.csv", root / "data/claim_audit_sample.json") if p.exists()})
    return metrics
