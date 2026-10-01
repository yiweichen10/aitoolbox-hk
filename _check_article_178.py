# -*- coding: utf-8 -*-
import re, os, json

raw = open('_article_178_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()

print('=== META ===')
for k in ['TITLE', 'SLUG', 'CATEGORY', 'DATE']:
    print(k, '=', meta.get(k, 'MISSING').strip())

wc = len(content.split())
print('\n=== WORD COUNT ===')
print('words:', wc, 'OK' if 2200 <= wc <= 2800 else '!!! OUT OF RANGE')

print('\n=== PRIMARY KEYWORD (must be exactly 4) ===')
pk = meta['KEYWORDS'].split('|')[0].strip()
print('pk =', repr(pk), '-> count =', content.count(pk))

print('\n=== LONG-TAIL KEYWORDS (all must be >=1) ===')
missing = []
for lt in meta['KEYWORDS'].split('|')[1:]:
    lt = lt.strip()
    n = content.lower().count(lt.lower())
    if n == 0:
        missing.append(lt)
    print(f'  {lt!r:45} {n}x', 'MISSING !!!' if n == 0 else '')

print('\n=== BANNED WORDS (must be 0) ===')
banned = ['leverage', 'utilize', 'seamlessly', 'game-changing', 'empower', 'streamline',
          'delve into', 'transformative', 'comprehensive', 'revolutionize', 'cutting-edge',
          'as an AI', 'in conclusion']
hits = [b for b in banned if b.lower() in content.lower()]
print('banned hits:', hits if hits else 'NONE - OK')

print('\n=== INTERNAL LINKS (>=2, targets must exist) ===')
links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('count:', len(links))
for l in links:
    tgt = l.strip('/')
    exists = os.path.isdir(tgt)
    print(f'  {l:110} exists={exists}', '' if exists else '  !!! TARGET MISSING')
if len(links) < 2:
    print('!!! TOO FEW LINKS')

print('\n=== COMPARISON TABLE (>=4 rows x 4 cols) ===')
tbl = [ln for ln in content.splitlines() if ln.strip().startswith('|')]
rows = len(tbl)
if rows >= 2:
    sep = [ln for ln in tbl if set(ln.replace('|', '').replace('-', '').replace(':', '').strip()) == set()]
    data_rows = rows - len(sep) - 1
    cols = len([c for c in tbl[0].split('|') if c.strip()])
    print(f'table lines={rows}, data_rows={data_rows}, cols={cols}',
          'OK' if data_rows >= 4 and cols >= 4 else '!!! TOO SMALL')
else:
    print('!!! NO TABLE FOUND')

print('\n=== FAQ SECTION (H2 + >=3 H3) ===')
m = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
if not m:
    print('!!! FAQ H2 MISSING')
else:
    h3 = re.findall(r'^### (.+)$', m.group(1), re.M)
    print('h3 count:', len(h3), 'OK' if len(h3) >= 3 else '!!! TOO FEW')
    for h in h3:
        print('   -', h)

print('\n=== STRUCTURE ===')
h2s = re.findall(r'^## (.+)$', content, re.M)
print('H2 count:', len(h2s))
for h in h2s:
    print('   -', h)

print('\n=== SUMMARY ===')
problems = []
if not (2200 <= wc <= 2800):
    problems.append(f'word count {wc}')
if content.count(pk) != 4:
    problems.append(f'PK count {content.count(pk)} (need 4)')
if missing:
    problems.append(f'missing long-tails: {missing}')
if hits:
    problems.append(f'banned words: {hits}')
if len(links) < 2:
    problems.append('links < 2')
print('RESULT:', 'ALL GREEN' if not problems else 'ISSUES -> ' + '; '.join(problems))
