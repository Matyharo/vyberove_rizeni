"""Small, explicit navigation vocabulary, not an independent sector assessment.

Only recognized expressions are mapped. Source claims and their statuses remain
untouched; unknown text is kept in the evidence, never guessed into a category.
"""
import re
import unicodedata


def key(value):
    text = ''.join(c for c in unicodedata.normalize('NFD', value) if not unicodedata.combining(c))
    return re.sub(r'\s+', ' ', text.casefold()).strip()


SECTORS = [
    ('sector-open', 'Sektorově otevřené zaměření', ['Bez pevné sektorové teze', 'Sektorově agnostické', 'Sektorově agnostický impact']),
    ('technology', 'Široké technologické zaměření', ['Digitální, fyzická a spotřebitelská ekonomika', 'široké technologické zaměření', 'Purpose-driven technologické inovace', 'Technologické firmy']),
    ('defence', 'Obranné technologie', ['Defence', 'Defense', 'obranné technologie']),
    ('space', 'Kosmické technologie', ['space', 'kosmické technologie']),
    ('fintech', 'Fintech', ['fintech', 'financial technology']),
    ('industry', 'Průmyslové technologie', ['Industry 4.0', 'průmyslové technologie']),
    ('energy', 'Energetika', ['energie', 'energy', 'energetika']),
    ('life-sciences', 'Life sciences', ['Life sciences']),
    ('drug-discovery', 'Vývoj léčiv', ['drug discovery', 'vývoj léčiv']),
    ('medtech', 'Medtech', ['medtech', 'medical technology']),
    ('diagnostics', 'Diagnostika', ['diagnostika', 'diagnostics']),
    ('ai-health', 'AI ve zdravotnictví', ['AI ve zdravotnictví']),
    ('climate', 'Klimatické technologie', ['Climate tech', 'climate technology']),
    ('ai', 'Umělá inteligence', ['AI', 'artificial intelligence', 'umělá inteligence']),
    ('healthtech', 'Zdravotnické technologie', ['healthtech', 'health tech']),
    ('frontier', 'Frontier tech', ['frontier tech']),
    ('deep-tech', 'Deep tech', ['Deep tech', 'deeptech']),
    ('quantum', 'Kvantové technologie', ['quantum', 'quantum computing']),
    ('computational-biotech', 'Výpočetní biotechnologie', ['computational biotech']),
    ('sustainable-tech', 'Udržitelné technologie', ['sustainable tech', 'sustainable technology']),
    ('impact', 'Dopadové investice', ['Sektorově agnostický impact', 'environmentální a sociální dopad']),
]
STAGES = [
    ('inception', 'Vznik firmy (inception)', ['inception', 'od založení']),
    ('pre-seed', 'Pre-seed', ['pre-seed']),
    ('seed', 'Seed', ['seed']),
    ('series-a', 'Series A', ['Series A']),
    ('early-stage', 'Raná fáze (early-stage)', ['early-stage', 'early stage']),
    ('growth', 'Růstová fáze (growth)', ['growth']),
]
# An explicit, unambiguous range is the only expansion rule. Early-stage and
# vague "startup / venture" do not imply any particular financing rounds.
STAGE_RANGES = {key('pre-seed až Series A'): ['pre-seed', 'seed', 'series-a']}


def navigation_categories(claims, field):
    vocabulary = SECTORS if field == 'sectors' else STAGES
    labels = {cid: label for cid, label, _ in vocabulary}
    aliases = {}
    for cid, _, expressions in vocabulary:
        for expression in expressions:
            aliases.setdefault(key(expression), []).append(cid)
    categories = {}
    for claim in claims:
        if claim['field'] != field or not isinstance(claim['value'], str):
            continue
        for token in claim['value'].split(';'):
            ids = STAGE_RANGES.get(key(token), []) if field == 'stage' else []
            ids = ids or aliases.get(key(token), [])
            for cid in ids:
                category = categories.setdefault(cid, dict(id=cid, label=labels[cid], claim_ids=[], source_statuses=[]))
                if claim['id'] not in category['claim_ids']:
                    category['claim_ids'].append(claim['id'])
                if claim['status'] not in category['source_statuses']:
                    category['source_statuses'].append(claim['status'])
    return sorted(categories.values(), key=lambda c: c['id'])
