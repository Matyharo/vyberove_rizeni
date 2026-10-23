"""The static package must preserve publication and the original evidence."""
import csv
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from investor_db.core import build, publication_ids, read_json, read_review, REVIEW_FIELDS

ROOT = Path(__file__).resolve().parents[1]


class StaticWebTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='web-test-', dir=ROOT)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ('data', 'review', 'frontend'):
            shutil.copytree(ROOT / name, self.root / name)
        shutil.copyfile(ROOT / 'release.json', self.root / 'release.json')

    def payload(self):
        return read_json(self.root / 'site/data.json')

    def test_package_matches_publication_and_keeps_conflicts_and_review_origin(self):
        build(self.root)
        pilot = read_json(self.root / 'data/pilot.json')
        reviews = read_review(self.root / 'review/labels.csv', {d['candidate_id'] for d in pilot['decisions']})
        payload = self.payload()
        self.assertEqual({i['id'] for i in payload['investors']}, publication_ids(pilot, reviews))
        self.assertEqual(payload['metrics'], read_json(self.root / 'exports/metrics.json'))
        purple = next(i for i in payload['investors'] if i['id'] == 'purple')
        tickets = [c for c in purple['claims'] if c['field'] == 'ticket']
        self.assertEqual({c['value']['max'] for c in tickets}, {400000, 500000})
        self.assertEqual(len({c['source_id'] for c in tickets}), 2)
        self.assertTrue(any(r['field'] == 'ticket' for r in purple['conflicts']))
        self.assertEqual(purple['classification']['reference']['reviewer'], 'Ferstl')
        for claim in tickets:
            self.assertEqual(claim['review']['reviewer'], 'Ferstl')
        self.assertTrue(all(not i['attributes_human_verified'] for i in payload['investors']))
        for inv in payload['investors']:
            for tx in inv['transactions']:
                original = next(t for t in pilot['transactions'] if t['id'] == tx['id'])
                self.assertEqual(tx, original)
        self.assertEqual((self.root / 'site/exports/investor_summary.csv').read_bytes(), (self.root / 'exports/investor_summary.csv').read_bytes())
        sources = {s['id'] for s in payload['sources']}
        self.assertTrue(all(c['source_id'] in sources for i in payload['investors'] for c in i['claims']))

    def test_publication_change_and_rebuild_preserve_reference_records(self):
        path = self.root / 'review/labels.csv'
        with path.open(encoding='utf-8-sig', newline='') as file:
            rows = list(csv.DictReader(file))
        next(r for r in rows if r['candidate_id'] == 'credo')['label'] = 'exclude'
        from investor_db.core import write_csv
        write_csv(path, rows, REVIEW_FIELDS)
        labels = path.read_bytes()
        claims = (self.root / 'review/claims.csv').read_bytes()
        predictions = (self.root / 'data/predictions.json').read_bytes()
        build(self.root)
        self.assertNotIn('credo', {i['id'] for i in self.payload()['investors']})
        before = {str(p.relative_to(self.root / 'site')): p.read_bytes() for p in (self.root / 'site').rglob('*') if p.is_file()}
        build(self.root)
        self.assertEqual(before, {str(p.relative_to(self.root / 'site')): p.read_bytes() for p in (self.root / 'site').rglob('*') if p.is_file()})
        self.assertEqual(labels, path.read_bytes())
        self.assertEqual(claims, (self.root / 'review/claims.csv').read_bytes())
        self.assertEqual(predictions, (self.root / 'data/predictions.json').read_bytes())
