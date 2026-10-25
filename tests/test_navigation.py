import unittest
from pathlib import Path

from investor_db.core import read_json
from investor_db.navigation import navigation_categories

ROOT = Path(__file__).resolve().parents[1]


def claim(field, value, status='supported'):
    return dict(id='test.' + field, field=field, value=value, status=status)


class NavigationTests(unittest.TestCase):
    def ids(self, field, value):
        return {c['id'] for c in navigation_categories([claim(field, value)], field)}

    def test_notes_are_not_sectors_and_open_mandate_does_not_match_every_sector(self):
        self.assertEqual(self.ids('sectors', 'Bez pevné sektorové teze; technologičtí zakladatelé'), {'sector-open'})
        self.assertEqual(self.ids('sectors', 'mandát sektorů není na použité stránce formalizován'), set())
        self.assertEqual(self.ids('sectors', 'Sektorově agnostické; B2B, B2C, marketplaces'), {'sector-open'})
        self.assertEqual(self.ids('stage', 'startup / venture; přesné fáze nezjištěny'), set())

    def test_explicit_synonyms_and_case_merge_without_duplicate_categories(self):
        cs = navigation_categories([claim('sectors', 'AI; artificial intelligence; UMĚLÁ INTELIGENCE; FINTECH')], 'sectors')
        self.assertEqual({c['id'] for c in cs}, {'ai', 'fintech'})
        self.assertTrue(all(c['claim_ids'] == ['test.sectors'] for c in cs))
        self.assertEqual(self.ids('sectors', 'Defence; defense'), {'defence'})

    def test_stage_combinations_and_explicit_range_expand_only_known_rounds(self):
        self.assertEqual(self.ids('stage', 'pre-seed; seed'), {'pre-seed', 'seed'})
        self.assertEqual(self.ids('stage', 'pre-seed až Series A'), {'pre-seed', 'seed', 'series-a'})
        self.assertEqual(self.ids('stage', 'seed; Series A'), {'seed', 'series-a'})
        self.assertEqual(self.ids('stage', 'early-stage'), {'early-stage'})
        self.assertEqual(self.ids('stage', 'growth'), {'growth'})

    def test_real_claims_are_unchanged_and_partial_support_is_traceable(self):
        pilot = read_json(ROOT / 'data/pilot.json')
        before = repr(pilot['claims'])
        for iid in ('credo', 'jt', 'reflex'):
            cs = [c for c in pilot['claims'] if c['investor_id'] == iid]
            categories = navigation_categories(cs, 'sectors')
            self.assertTrue(all(c['claim_ids'] and c['source_statuses'] for c in categories))
            if iid == 'reflex':
                self.assertEqual(categories[0]['source_statuses'], ['partial'])
        self.assertEqual(before, repr(pilot['claims']))
