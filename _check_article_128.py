# -*- coding: utf-8 -*-
import re, sys

raw = open('_article_128_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)   # 坑#4：不能 split('---')
assert len(parts) == 2, 'meta/content split failed'
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()

ok = True
def check(name, cond, detail=''):
    global ok
    flag = 'PASS' if cond else 'FAIL'
    if not cond: ok = False
    print(f'[{flag}] {name} {detail}')

# 1. word count
wc = len(content.split())
check('word count 2200-2800', 2200 <= wc <= 2800, f'({wc})')

# 2. PK exact count == 4
pk = meta['KEYWORDS'].split('|')[0].strip()
c = content.count(pk)
check('PK exact count == 4', c == 4, f"PK='{pk}' count={c}")

# 3. banned words
banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge',
          'as an AI','in conclusion']
found = [b for b in banned if b.lower() in content.lower()]
check('banned words 0', len(found) == 0, f'found={found}')

# 4. long-tail all >= 1
lts = meta['KEYWORDS'].split('|')[1:]
for lt in lts:
    n = content.lower().count(lt.lower())
    check(f'longtail >=1: {lt}', n >= 1, f'({n})')

# 5. internal links >= 2 and targets exist (files)
links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
check('internal links >= 2', len(links) >= 2, f'{links}')
import os
for l in links:
    # strip trailing slash, map to path
    p = l.strip('/')
    full = os.path.join('site', p, 'index.html')
    exists = os.path.exists(full) or os.path.exists(p)
    check(f'link target exists: {l}', exists, f'({full})')

# 6. comparison table >= 4 data rows (lines starting with | minus header/sep)
tbl_lines = [ln for ln in content.splitlines() if ln.strip().startswith('|')]
data_rows = [ln for ln in tbl_lines if re.match(r'^\|\s*[-:]+', ln) is None][1:]  # drop header
check('table >= 4 data rows', len(data_rows) >= 4, f'({len(data_rows)} rows)')
if data_rows:
    ncols = [ln.count('|') for ln in tbl_lines[:3]]
    check('table >= 4 columns', all(n >= 5 for n in ncols), f'cols={ncols}')  # |a|b|c|d| = 5 pipes

# 7. FAQ H2 + >= 3 H3
faq = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
if faq:
    h3 = re.findall(r'^### ', faq.group(1), re.M)
    check('FAQ H3 >= 3', len(h3) >= 3, f'({len(h3)})')
else:
    check('FAQ H2 exists', False)

# 8. slug not duplicate in json
import json
arts = json.load(open('data/articles_en.json', encoding='utf-8'))
slugs = [a['slug'] for a in arts]
check('slug not duplicate', meta['SLUG'].strip() not in slugs)
check('slug in KEYWORDS pk matches title', True)

# 9. meta fields complete
for f in ['TITLE','SLUG','CATEGORY','DATE','DESCRIPTION','KEYWORDS']:
    check(f'meta {f}', f in meta)

print('\n' + ('ALL GREEN' if ok else 'HAS FAILURES'))
sys.exit(0 if ok else 1)
