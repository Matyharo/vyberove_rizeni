"""SQLite behavior tests using a fresh export and the actual reviewed inputs."""
import json
import csv
import shutil
import sqlite3
import tempfile
import unittest
import io
from contextlib import closing
from contextlib import redirect_stdout
from unittest.mock import patch
from pathlib import Path

from investor_db.core import build, read_json, write_csv, CLAIM_REVIEW_FIELDS
from investor_db.__main__ import main
from research.audit_database import audit

ROOT = Path(__file__).resolve().parents[1]


class DatabaseTests(unittest.TestCase):
    def test_optional_conversation_export_is_not_release_blocker(self):
        (self.root / 'release.json').write_text(json.dumps({'public_repository_url': 'https://github.com/Matyharo/vyberove_rizeni'}), encoding='utf-8')
        self.db.close()
        with patch('sys.argv', ['investor_db', 'check-release', '--root', str(self.root)]), redirect_stdout(io.StringIO()):
            self.assertEqual(main(), 0)

    def test_one_attribute_review_updates_all_formats_without_verifying_all(self):
        path = self.root / 'review/claims.csv'
        with path.open(encoding='utf-8-sig', newline='') as file:
            rows = list(csv.DictReader(file))
        for r in rows:
            if r['claim_id'] == 'credo.ticket.1':
                r.update(label='supported', reviewer='TEST FIXTURE ONLY', reviewed_on='2026-10-22', reason='Synthetic reference for export regression only')
        write_csv(path, rows, CLAIM_REVIEW_FIELDS)
        before = path.read_bytes()
        self.db.close()
        metrics = build(self.root)
        self.assertEqual(metrics['claims']['accuracy'], 1)
        self.assertEqual(metrics['claims']['resolved'], 1)
        claims = read_json(self.root / 'exports/claims.json')
        self.assertTrue(next(c for c in claims if c['id']=='credo.ticket.1')['attribute_human_verified'])
        self.assertFalse(next(i for i in read_json(self.root / 'exports/investors.json') if i['id']=='credo')['attributes_human_verified'])
        with closing(sqlite3.connect(self.path)) as db:
            self.assertEqual(db.execute("SELECT attribute_human_verified FROM claim_verification WHERE claim_id='credo.ticket.1'").fetchone()[0], 1)
        with (self.root / 'exports/investor_summary.csv').open(encoding='utf-8-sig', newline='') as file:
            credo = next(r for r in csv.DictReader(file) if r['id']=='credo')
        self.assertEqual(credo['ticket_human_verified'], 'True')
        self.assertEqual(credo['attributes_human_verified'], 'False')
        build(self.root)
        self.assertEqual(before, path.read_bytes())

    def test_derived_flags_agree_across_exports(self):
        investors = read_json(self.root / 'exports/investors.json')
        self.assertTrue(all(r['classification_human_verified'] for r in investors))
        self.assertFalse(any(r['attributes_human_verified'] for r in investors))
        with (self.root / 'exports/investor_summary.csv').open(encoding='utf-8-sig', newline='') as file:
            summary = list(csv.DictReader(file))
        self.assertEqual({r['id'] for r in summary}, {r['id'] for r in investors if r['published']})
        self.assertTrue(all(r['classification_human_verified']=='True' and r['attributes_human_verified']=='False' for r in summary))
        self.assertEqual(self.db.execute('SELECT SUM(classification_human_verified), SUM(attributes_human_verified) FROM investors').fetchone(), (len(investors), 0))
        self.assertEqual(self.db.execute('SELECT SUM(attribute_human_verified) FROM claim_verification').fetchone()[0], 0)
        pilot_report = (self.root / 'reports/PILOT.md').read_text(encoding='utf-8')
        self.assertIn('| Purple Ventures | needs_review | include | include | ano |', pilot_report)
        self.assertIn('| Lighthouse Ventures | needs_review | needs_review | exclude | ne |', pilot_report)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='db-test-', dir=ROOT)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for folder in ['data', 'review']:
            shutil.copytree(ROOT / folder, self.root / folder)
        build(self.root)
        self.path = self.root / 'exports/investors.sqlite'
        self.db = sqlite3.connect(self.path)
        self.addCleanup(self.db.close)
        self.db.execute('PRAGMA foreign_keys=ON')

    def test_published_and_fresh_database_pass_read_only_audit(self):
        for path in [ROOT / 'exports/investors.sqlite', self.path]:
            result = audit(path)
            self.assertTrue(result['passed'], result)

    def test_counts_and_values_match_canonical_input(self):
        pilot = read_json(self.root / 'data/pilot.json')
        for table in ['investors', 'sources', 'claims', 'transactions', 'funds']:
            self.assertEqual(self.db.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0], len(pilot[table]))
        actual = {r[0]: r[1:] for r in self.db.execute('SELECT id, investor_id, field, value_json, source_id, status FROM claims')}
        for c in pilot['claims']:
            investor, field, value, source, status = actual[c['id']]
            self.assertEqual((investor, field, json.loads(value), source, status), (c['investor_id'], c['field'], c['value'], c['source_id'], c['status']))
        with closing(sqlite3.connect(ROOT / 'exports/investors.sqlite')) as published:
            self.assertEqual('\n'.join(self.db.iterdump()), '\n'.join(published.iterdump()))

    def test_sqlite_rejects_orphan_duplicate_and_null(self):
        statements = [
            "UPDATE claims SET source_id='missing-source' WHERE id=(SELECT id FROM claims LIMIT 1)",
            "INSERT INTO candidates SELECT * FROM candidates LIMIT 1",
            "UPDATE investors SET website=NULL WHERE id=(SELECT id FROM investors LIMIT 1)",
            "DELETE FROM sources WHERE id=(SELECT source_id FROM claims LIMIT 1)",
        ]
        for sql in statements:
            with self.subTest(sql=sql), self.assertRaises(sqlite3.IntegrityError):
                self.db.execute(sql)
            self.db.rollback()
        self.assertTrue(audit(self.path)['passed'])

    def test_rebuild_preserves_data_and_human_reviews(self):
        before = '\n'.join(self.db.iterdump())
        labels = (self.root / 'review/labels.csv').read_bytes()
        claims = (self.root / 'review/claims.csv').read_bytes()
        predictions = (self.root / 'data/predictions.json').read_bytes()
        self.db.close()
        build(self.root)
        with closing(sqlite3.connect(self.path)) as rebuilt:
            self.assertEqual(before, '\n'.join(rebuilt.iterdump()))
        self.assertEqual(labels, (self.root / 'review/labels.csv').read_bytes())
        self.assertEqual(claims, (self.root / 'review/claims.csv').read_bytes())
        self.assertEqual(predictions, (self.root / 'data/predictions.json').read_bytes())

    def test_money_semantics_survive_sql_queries(self):
        row = self.db.execute("SELECT round_amount_json, investor_contribution_json, contribution_source_id FROM transactions WHERE id='tx-inibio-sampling-human'").fetchone()
        self.assertIsNone(json.loads(row[0]))
        self.assertEqual(json.loads(row[1]), {'amount': 1500000, 'currency': 'USD'})
        self.assertEqual(row[2], 'sampling-human')
        row = self.db.execute("SELECT round_amount_json, investor_contribution_json FROM transactions WHERE id='tx-tensor-openvibe'").fetchone()
        self.assertEqual(json.loads(row[0])['amount'], 800000)
        self.assertIsNone(json.loads(row[1]))


if __name__ == '__main__':
    unittest.main()
