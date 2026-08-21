# -*- coding: utf-8 -*-
"""Article #137 self-check: keyword density, long-tail, banned words, word count, links."""
import json, re, sys

DRAFT = open('_article_137_draft.txt', encoding='utf-8').read()
ARTICLES = json.load(open('data/articles_en.json', encoding='utf-8'))
EXISTING_SLUGS = {a['slug'] for a in ARTICLES}

PK = 'ai payroll software 2026'
LONG_TAILS = [
    'gusto vs rippling',
    'ai payroll software pricing',
    'rippling pricing per employee',
    'deel eor pricing',
    'adp run pricing',
    'onpay vs gusto',
    'best payroll software for small business',
    'global payroll software',
    'automatic payroll processing',
    'payroll tax penalties',
]
BANNED = ['leverage', 'utilize', 'seamlessly', 'game-changing', 'empower', 'streamline',
          'delve into', 'transformative', 'comprehensive', 'revolutionize', 'cutting-edge',
          'as an AI', 'in conclusion']

errors = []

# 1. Word count
words = len(re.findall(r"[A-Za-z0-9$%+\-']+", DRAFT))
print(f'Word count: {words} (target 2200-2800)')
if not (2200 <= words <= 2800):
    errors.append(f'WORD COUNT {words} out of range')

# 2. Primary keyword exact count (case-insensitive)
pk_count = len(re.findall(r'ai payroll software 2026', DRAFT, re.IGNORECASE))
print(f'Primary keyword "{PK}" exact occurrences: {pk_count} (target 4)')
if pk_count != 4:
    errors.append(f'PK count {pk_count} != 4')

# 3. Long-tail presence
missing = []
for lt in LONG_TAILS:
    n = len(re.findall(re.escape(lt), DRAFT, re.IGNORECASE))
    status = 'OK' if n >= 1 else 'MISSING'
    print(f'  long-tail [{status}] {lt}: {n}x')
    if n < 1:
        missing.append(lt)
if missing:
    errors.append(f'Missing long-tails: {missing}')

# 4. Banned words
banned_hits = []
for b in BANNED:
    if re.search(r'\b' + re.escape(b) + r'\b', DRAFT, re.IGNORECASE):
        banned_hits.append(b)
print(f'Banned words found: {banned_hits if banned_hits else "NONE"}')
if banned_hits:
    errors.append(f'Banned: {banned_hits}')

# 5. FAQ structure
h2s = re.findall(r'^## (.+)$', DRAFT, re.M)
h3s = re.findall(r'^### (.+)$', DRAFT, re.M)
print(f'H2 count: {len(h2s)} -> {h2s}')
print(f'H3 count: {len(h3s)}')
if not any('frequently asked' in h.lower() for h in h2s):
    errors.append('No FAQ H2')
if len(h3s) < 3:
    errors.append(f'FAQ H3 < 3 ({len(h3s)})')

# 6. Comparison table rows/cols
tables = re.findall(r'(\|.+\|(?:\n\|.+\|)+)', DRAFT)
for i, t in enumerate(tables):
    lines = t.strip().split('\n')
    rows = [l for l in lines if l.strip().startswith('|') and not re.match(r'^\|[\s:\-\|]+\|$', l)]
    cols = rows[0].count('|') - 1 if rows else 0
    data_rows = len(rows) - 2  # minus header + separator
    print(f'Table {i+1}: {data_rows} data rows x {cols} cols')
    if data_rows < 4 or cols < 4:
        errors.append(f'Table {i+1}: {data_rows}x{cols} too small')

# 7. Internal links exist
links = re.findall(r'\]\((/articles/[a-z0-9\-]+/)\)', DRAFT)
print(f'Internal links: {len(links)}')
for l in links:
    slug = l.strip('/').split('/')[-1]
    exists = slug in EXISTING_SLUGS
    print(f'  {"OK" if exists else "MISSING"} {slug}')
    if not exists:
        errors.append(f'Broken internal link: {slug}')

# 8. Title/description/keywords sanity for append script
print()
if errors:
    print('FAIL:')
    for e in errors:
        print('  -', e)
    sys.exit(1)
else:
    print('ALL CHECKS PASSED')
