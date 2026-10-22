"""Read-only SQL audit of the published SQLite artifact."""
import json
import sqlite3
from contextlib import closing
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def audit(path):
    with closing(sqlite3.connect(path.resolve().as_uri() + '?mode=ro', uri=True)) as db:
        checks = {}
        checks['sqlite_integrity'] = db.execute('PRAGMA integrity_check').fetchall() == [('ok',)]
        checks['foreign_keys'] = not db.execute('PRAGMA foreign_key_check').fetchall()
        tables = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        counts = {t: db.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0] for t in tables}
        checks['all_candidates_have_review'] = not db.execute('SELECT c.id FROM candidates c LEFT JOIN human_reviews h ON c.id=h.candidate_id WHERE h.candidate_id IS NULL').fetchall()
        checks['accepted_have_investment_and_source'] = not db.execute('''SELECT h.candidate_id FROM human_reviews h
          LEFT JOIN investors i ON i.id=h.candidate_id
          WHERE h.label='include' AND (i.id IS NULL OR NOT EXISTS
          (SELECT 1 FROM transactions t JOIN sources s ON s.id=t.source_id WHERE t.investor_id=i.id AND t.date IS NOT NULL AND s.url LIKE 'https://%'))''').fetchall()
        checks['claims_have_sources'] = not db.execute("SELECT c.id FROM claims c LEFT JOIN sources s ON s.id=c.source_id WHERE s.id IS NULL OR s.url NOT LIKE 'https://%'").fetchall()
        checks['json_payloads_valid'] = True
        for query in ['SELECT value_json FROM claims', 'SELECT round_amount_json FROM transactions', 'SELECT investor_contribution_json FROM transactions', 'SELECT source_ids_json FROM out_of_scope_classifications']:
            for (payload,) in db.execute(query):
                try:
                    json.loads(payload)
                except (TypeError, ValueError):
                    checks['json_payloads_valid'] = False
        checks['human_source_ids_resolve'] = True
        ids = {r[0] for r in db.execute('SELECT id FROM sources')}
        for (source_ids,) in db.execute('SELECT source_ids FROM human_reviews'):
            if not set(source_ids.split(';')) <= ids:
                checks['human_source_ids_resolve'] = False
        counts['human_include'] = db.execute("SELECT COUNT(*) FROM human_reviews WHERE label='include'").fetchone()[0]
        counts['human_exclude'] = db.execute("SELECT COUNT(*) FROM human_reviews WHERE label='exclude'").fetchone()[0]
        return {'checks': checks, 'counts': counts, 'passed': all(checks.values())}


if __name__ == '__main__':
    result = audit(ROOT / 'exports/investors.sqlite')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['passed'] else 1)
