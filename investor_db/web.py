"""Offline, deterministic packaging of the static evidence browser.

Publication is decided by core.publication_ids, never by the browser.
Only the published organizations and their evidence enter the web dataset.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from .navigation import navigation_categories


def build_site(root, pilot, candidates, predictions, reviews, claim_reviews, metrics, published):
    from .core import dump_json, verification_flags

    source = root / 'frontend'
    if not source.is_dir():
        # Core library tests and downstream data-only consumers need no web assets.
        return
    dest = root / 'site'
    dest.mkdir(exist_ok=True)
    for name in ('index.html', 'style.css', 'app.js', 'model.js'):
        shutil.copyfile(source / name, dest / name)
    (dest / '.nojekyll').write_text('', encoding='utf-8')
    claims_by_id = {r['claim_id']: r for r in claim_reviews}
    review_by_id = {r['candidate_id']: r for r in reviews}
    initial = {r['candidate_id']: r for r in predictions['predictions']}
    current = {r['candidate_id']: r for r in pilot['decisions']}
    investors = []
    source_ids = set()
    for inv in pilot['investors']:
        iid = inv['id']
        if iid not in published:
            continue
        claims = []
        for c in pilot['claims']:
            if c['investor_id'] != iid:
                continue
            row = dict(c, review=claims_by_id.get(c['id']),
                       attribute_human_verified=c['value'] is not None and
                       claims_by_id.get(c['id'], {}).get('label') == 'supported')
            claims.append(row)
            source_ids.add(c['source_id'])
        transactions = [t for t in pilot['transactions'] if t['investor_id'] == iid]
        for t in transactions:
            source_ids.update([t['source_id'], *t['corroborating_source_ids']])
            if t.get('contribution_source_id'):
                source_ids.add(t['contribution_source_id'])
        source_ids.update(current[iid]['source_ids'])
        source_ids.update(review_by_id[iid]['source_ids'].split(';'))
        source_ids.update(f['source_id'] for f in pilot['funds'] if f['investor_id'] == iid)
        # Existing curation explicitly records conflicting sources in notes.
        # Historical alternatives alone are not classified as current conflicts.
        conflicts = []
        for field in sorted({c['field'] for c in claims}):
            group = [c for c in claims if c['field'] == field and c['value'] is not None]
            values = {json.dumps(c['value'], sort_keys=True) for c in group}
            if len(values) > 1 and any(re.search(r'rozpor', c['note'], re.I) for c in group):
                conflicts.append(dict(field=field, claim_ids=[c['id'] for c in group],
                                      explanation='Zdroje uvádějí odlišné hodnoty. Aktuální platnost není vyřešena.'))
        investors.append(dict(inv, published=True,
                              **verification_flags(pilot, iid, reviews, claim_reviews),
                              claims=claims, transactions=transactions,
                              navigation={field: navigation_categories(claims, field) for field in ('sectors', 'stage')},
                              funds=[f for f in pilot['funds'] if f['investor_id'] == iid],
                              conflicts=conflicts,
                              classification=dict(initial_ai=initial[iid]['prediction'],
                                                  current_ai=current[iid]['prediction'],
                                                  reason=current[iid]['reason'],
                                                  source_ids=current[iid]['source_ids'],
                                                  reference=review_by_id[iid])))
    # Repository metadata is optional for data-only integration fixtures.
    metadata_path = root / 'release.json'
    metadata = json.loads(metadata_path.read_text(encoding='utf-8')) if metadata_path.exists() else {}
    payload = dict(schema_version=1, as_of=pilot['as_of'],
                   repository_url=metadata.get('public_repository_url'),
                   publication_rule='current_ai_include_and_human_reference_include',
                   review_provenance='Uživatelem dodané referenční štítky; AI provedla zápis. Nejde o nezávislý audit všech údajů.',
                   metrics=metrics, investors=investors,
                   sources=[s for s in pilot['sources'] if s['id'] in source_ids])
    dump_json(dest / 'data.json', payload)
    downloads = dest / 'exports'
    downloads.mkdir(exist_ok=True)
    shutil.copyfile(root / 'exports/investor_summary.csv', downloads / 'investor_summary.csv')
    shutil.copyfile(root / 'exports/metrics.json', downloads / 'metrics.json')

