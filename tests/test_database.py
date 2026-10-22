"""SQLite behavior tests using a fresh export and the actual reviewed inputs."""
import json
import shutil
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from investor_db.core import build, read_json
from research.audit_database import audit

ROOT = Path(__file__).resolve().parents[1]


class DatabaseTests(unittest.TestCase):
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
        predictions = (self.root / 'data/predictions.json').read_bytes()
        self.db.close()
        build(self.root)
        with closing(sqlite3.connect(self.path)) as rebuilt:
            self.assertEqual(before, '\n'.join(rebuilt.iterdump()))
        self.assertEqual(labels, (self.root / 'review/labels.csv').read_bytes())
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
