# -*- coding: utf-8 -*-
import re, os, json

raw = open('_article_157_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)   # 坑#4
meta_lines = parts[0].strip().splitlines()
meta = {}
for line in meta_lines:
    if ':' in line:
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()
content = parts[1].strip()

pk = meta['KEYWORDS'].split('|')[0].strip()
print('title:', meta['TITLE'])
print('words:', len(content.split()), '(need 2200-2800)')
print('pk count:', content.count(pk), '(need exactly 4)')
print('pk occurrences:', [m.start() for m in re.finditer(re.escape(pk), content)])

banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge',
          'as an AI','in conclusion']
found = [b for b in banned if b.lower() in content.lower()]
print('banned:', found)

for lt in meta['KEYWORDS'].split('|')[1:]:
    lt = lt.strip()
    c = content.lower().count(lt.lower())
    print(f'longtail [{lt}]: {c}', 'OK' if c >= 1 else '*** MISSING ***')

links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('internal links:', links)
for l in links:
    p = l.strip('/').split('/')
    exists = os.path.isdir(os.path.join(p[0], p[1]) if len(p) > 1 else p[0])
    print('  target', l, 'exists:', exists)

# tables: rows starting with |
tbl_rows = [l for l in content.splitlines() if l.strip().startswith('|')]
print('table rows total:', len(tbl_rows))
# first table rows
tables = re.findall(r'((?:^\|.*\|\s*$\n?)+)', content, re.M)
for i, t in enumerate(tables):
    rows = [r for r in t.strip().splitlines() if not re.match(r'^\|[\s\-|]+\|$', r)]
    cols = rows[0].count('|') - 1
    print(f'table {i}: data rows={len(rows)-1}, cols={cols}')

faq = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
h3s = re.findall(r'^### (.+)$', faq.group(1), re.M) if faq else []
print('FAQ H3 count:', len(h3s))
for h in h3s: print('  -', h)

# meta leakage check
print('meta leak:', content[:200].startswith('TITLE:'))
# slug uniqueness
arts = json.load(open('data/articles_en.json', encoding='utf-8'))
print('slug exists already:', any(a['slug'] == meta['SLUG'] for a in arts))
print('article count now:', len(arts), '-> next #', len(arts)+1)
