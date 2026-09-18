# -*- coding: utf-8 -*-
"""Self-check for article #166 (AI document extraction / IDP)."""
import re, os, json

raw = open('_article_166_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()

meta_leak = content.strip().startswith('TITLE:') or 'SLUG:' in content[:200]
print('meta leak:', meta_leak)
assert not meta_leak, 'META LEAK'

words = len(content.split())
print('words:', words, 'OK' if 2200 <= words <= 2800 else '*** OUT OF RANGE ***')

kws = [k.strip() for k in meta['KEYWORDS'].split('|')]
pk = kws[0]
n = content.count(pk)
print('PK:', repr(pk), 'count =', n, 'OK' if n == 4 else '*** MUST BE 4 ***')

banned = ['leverage', 'utilize', 'seamlessly', 'game-changing', 'empower', 'streamline',
          'delve into', 'transformative', 'comprehensive', 'revolutionize', 'cutting-edge',
          'as an AI', 'in conclusion']
hits = [b for b in banned if b.lower() in content.lower()]
print('banned hits:', hits, 'OK' if not hits else '*** BANNED ***')

print('--- long tails ---')
missing = []
for lt in kws[1:]:
    c = len(re.findall(re.escape(lt), content, re.IGNORECASE))
    flag = 'OK' if c >= 1 else '*** MISSING ***'
    if c == 0:
        missing.append(lt)
    print(f'  {lt!r}: {c}  {flag}')
print('MISSING:', missing)

print('--- internal links ---')
links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('links:', links)
bad = []
for l in links:
    rel = l.strip('/')
    local = os.path.join('.', rel)
    ok = os.path.isdir(local) or os.path.isfile(os.path.join(local, 'index.html'))
    print('  ', l, 'exists' if ok else '*** 404 ***')
    if not ok:
        bad.append(l)
print('link count OK' if len(links) >= 2 and not bad else '*** LINK PROBLEM ***')

print('--- tables ---')
tables = []
cur = []
for line in content.splitlines():
    if line.strip().startswith('|'):
        cur.append(line)
    else:
        if len(cur) >= 3:
            tables.append(cur)
        cur = []
if len(cur) >= 3:
    tables.append(cur)
for i, t in enumerate(tables, 1):
    cols = len([c for c in t[0].split('|') if c.strip()])
    rows = len(t) - 2
    print(f'  table {i}: {rows} data rows x {cols} cols', 'OK' if rows >= 4 and cols >= 4 else '*** TOO SMALL ***')
print('tables:', len(tables), 'OK' if len(tables) >= 1 else '*** NO TABLE ***')

print('--- FAQ ---')
m = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
h3 = re.findall(r'### (.+)', m.group(1)) if m else []
print('FAQ H3 count:', len(h3), 'OK' if len(h3) >= 3 else '*** NEEDS 3+ ***')
for q in h3:
    print('  -', q)

print('--- GSC hash check ---')
print('slug:', meta['SLUG'])
print('category:', meta['CATEGORY'])
