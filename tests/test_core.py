import copy
import csv
import io
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from contextlib import closing, redirect_stdout, redirect_stderr
from unittest.mock import patch
from investor_db.__main__ import main

from investor_db.core import (activity, build, classification_metrics, date_bounds,
                              read_json, read_review, validate, wilson, write_csv, REVIEW_FIELDS)
from investor_db.costs import estimate

ROOT = Path(__file__).resolve().parents[1]


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.pilot = read_json(ROOT / "data/pilot.json")
        self.candidates = read_json(ROOT / "data/candidates.json")
        self.predictions = read_json(ROOT / "data/predictions.json")

    def check(self):
        return validate(self.pilot, self.candidates, self.predictions)

    def test_actual_data(self):
        self.assertTrue(self.check())

    def test_broken_provenance(self):
        self.pilot["claims"][0]["source_id"] = "made-up"
        with self.assertRaisesRegex(ValueError, "dangling"):
            self.check()

    def test_duplicate_investor(self):
        self.pilot["investors"].append(self.pilot["investors"][0])
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            self.check()

    def test_no_portfolio_evidence(self):
        self.pilot["transactions"] = [t for t in self.pilot["transactions"] if t["investor_id"] != "credo"]
        with self.assertRaisesRegex(ValueError, "no named investment"):
            self.check()

    def test_target_cannot_be_total_aum(self):
        c = next(c for c in self.pilot["claims"] if c["id"] == "kaya.total_investment_capital.1")
        c["value"]["metric"] = "fund_target_size"
        with self.assertRaisesRegex(ValueError, "masquerade"):
            self.check()

    def test_round_cannot_be_attributed_contribution(self):
        self.pilot["transactions"][0]["investor_contribution"] = {"amount": 7000000, "currency": "USD"}
        with self.assertRaisesRegex(ValueError, "separate explicit evidence"):
            self.check()

    def test_zero_not_missing(self):
        next(c for c in self.pilot["claims"] if c["field"] == "ticket")["value"]["min"] = 0
        with self.assertRaisesRegex(ValueError, "positive"):
            self.check()

    def test_future_transaction(self):
        self.pilot["transactions"][0].update(date="2027-01-01", date_precision="day")
        with self.assertRaisesRegex(ValueError, "Future transaction"):
            self.check()


class MetricTests(unittest.TestCase):
    def test_cost_model_includes_all_candidate_review_and_refresh(self):
        config = read_json(ROOT / "data/cost_assumptions.json")
        result = estimate(config["scenarios"][1])
        self.assertAlmostEqual(result["initial_total_usd"], 127960)
        self.assertAlmostEqual(result["quarterly_refresh_usd"], 12360)
        self.assertAlmostEqual(result["review_hours"], 20000 * 8 / 60)

    def test_empty_review_is_not_perfect_precision(self):
        result = classification_metrics([dict(candidate_id="a", prediction="include")], [])
        self.assertIsNone(result["precision"]["value"])
        self.assertEqual(result["precision_bounds_all_initial_positives"], [0, 1])

    def test_abstentions_and_pending_are_visible(self):
        preds = [dict(candidate_id=i, prediction=p) for i, p in zip("abcde", ["include", "include", "include", "needs_review", "exclude"])]
        reviews = [dict(candidate_id=i, label=g) for i, g in zip("abcd", ["include", "exclude", "needs_review", "include"])]
        result = classification_metrics(preds, reviews)
        self.assertEqual(result["precision"]["value"], 0.5)
        self.assertEqual(result["pending"], 1)
        self.assertEqual(result["initial_positive_not_resolved"], 1)
        self.assertEqual(result["abstained_true_positives"], 1)
        self.assertEqual(result["recall_in_reviewed_candidate_set"]["value"], 0.5)

    def test_wilson_small_sample_not_certainty(self):
        low, high = wilson(10, 10)
        self.assertAlmostEqual(low, 0.7224672, places=6)
        self.assertAlmostEqual(high, 1)

    def test_year_does_not_invent_day(self):
        lo, hi = date_bounds("2025", "year")
        self.assertNotEqual(lo, hi)
        self.assertEqual(activity([dict(date="2025", date_precision="year")], "2026-10-22"), "recent_activity_evidenced")
        self.assertEqual(activity([dict(date="2024", date_precision="year")], "2026-10-22"), "activity_date_unknown")
        self.assertEqual(activity([dict(date="2019", date_precision="year")], "2026-10-22"), "historical_activity_only")

    def test_unknown_reference_id_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unknown"):
            classification_metrics([dict(candidate_id="a", prediction="include")], [dict(candidate_id="b", label="include")])


class IntegrationTests(unittest.TestCase):
    def test_clean_offline_build_and_sqlite(self):
        with tempfile.TemporaryDirectory(prefix="investor-test-", dir=ROOT) as folder:
            root = Path(folder)
            (root / "data").mkdir()
            for name in ("pilot.json", "predictions.json", "candidates.json"):
                (root / "data" / name).write_bytes((ROOT / "data" / name).read_bytes())
            metrics = build(root)
            self.assertIsNone(metrics["classification"]["precision"]["value"])
            before = (root / "review/labels.csv").read_bytes()
            build(root)
            self.assertEqual(before, (root / "review/labels.csv").read_bytes())
            with closing(sqlite3.connect(root / "exports/investors.sqlite")) as db:
                self.assertEqual(db.execute("SELECT COUNT(*) FROM candidates").fetchone()[0], 20)
                self.assertEqual(db.execute("SELECT COUNT(*) FROM transactions").fetchone()[0], 11)
                self.assertEqual(db.execute("PRAGMA foreign_key_check").fetchall(), [])
                self.assertEqual(db.execute("PRAGMA integrity_check").fetchone()[0], "ok")
            self.assertTrue((root / "reports/REVIEW_PACKET.md").exists())
            (root / "release.json").write_text('{"public_repository_url":null}', encoding="utf-8")
            with patch("sys.argv", ["investor_db", "check-release", "--root", str(root)]), redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()) as errors:
                self.assertEqual(main(), 2)
                self.assertIn("Missing public GitHub", errors.getvalue())
            pilot_path = root / "data/pilot.json"
            pilot = read_json(pilot_path)
            added = copy.deepcopy(pilot["claims"][0])
            added["id"] = "credo.additional_review_claim"
            pilot["claims"].append(added)
            pilot_path.write_text(json.dumps(pilot, ensure_ascii=False), encoding="utf-8")
            review_before = (root / "review/claims.csv").read_bytes()
            build(root)
            review_after = (root / "review/claims.csv").read_bytes()
            self.assertTrue(review_after.startswith(review_before))
            self.assertIn(b"credo.additional_review_claim", review_after)

    def test_ai_cannot_fill_human_gold(self):
        with tempfile.TemporaryDirectory(prefix="investor-test-", dir=ROOT) as folder:
            path = Path(folder) / "review.csv"
            write_csv(path, [dict(candidate_id="a", label="include", reviewer="Codex", reviewed_on="2026-10-22", reason="Checked", source_ids="s")], REVIEW_FIELDS)
            with self.assertRaisesRegex(ValueError, "AI cannot"):
                read_review(path, {"a"})

    def test_real_human_review_changes_metrics_not_predictions(self):
        with tempfile.TemporaryDirectory(prefix="investor-test-", dir=ROOT) as folder:
            root = Path(folder)
            (root / "data").mkdir()
            for name in ("pilot.json", "predictions.json", "candidates.json"):
                (root / "data" / name).write_bytes((ROOT / "data" / name).read_bytes())
            build(root)
            path = root / "review/labels.csv"
            with path.open(encoding="utf-8-sig", newline="") as file:
                rows = list(csv.DictReader(file))
            rows[0].update(label="include", reviewer="TEST FIXTURE ONLY", reviewed_on="2026-10-22", reason="Synthetic unit-test label, never actual evaluation", source_ids="axoflow")
            write_csv(path, rows, REVIEW_FIELDS)
            original = (root / "data/predictions.json").read_bytes()
            metrics = build(root)
            self.assertEqual(metrics["classification"]["precision"]["value"], 1)
            self.assertEqual(metrics["classification"]["pending"], 19)
            self.assertEqual(original, (root / "data/predictions.json").read_bytes())


if __name__ == "__main__":
    unittest.main()
