# -*- coding: utf-8 -*-
import re, os, json

raw = open('_article_167_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = {}
for line in parts[0].strip().splitlines():
    if ':' in line:
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()
content = parts[1].strip()
pk = meta['KEYWORDS'].split('|')[0].strip()

print('=== words:', len(content.split()), '(need 2200-2800)')
pkc = content.count(pk)
print('=== PK count:', pkc, '(need ==4)')
if pkc != 4:
    for i, m in enumerate(re.finditer(re.escape(pk), content)):
        pass
    # show case-insensitive hits to debug
    for m in re.finditer(re.escape(pk), content, re.I):
        ctx = content[max(0, m.start()-40):m.end()+20].replace('\n', ' ')
        print('   hit:', ctx)

banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge',
          'as an AI','in conclusion']
bb = [b for b in banned if b.lower() in content.lower()]
print('=== banned:', bb if bb else 'NONE')

for lt in meta['KEYWORDS'].split('|')[1:]:
    lt = lt.strip()
    c = content.lower().count(lt.lower())
    flag = 'OK ' if c >= 1 else 'MISSING'
    print(f'=== LT [{flag}] {c}x : {lt}')

links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('=== internal links:', len(links))
for l in links:
    ok = os.path.isdir(l.strip('/').replace('articles/', 'articles/').rstrip('/'))
    print('   ', l, '-> exists:', ok)

# tables
lines = content.splitlines()
tbl_rows = [l for l in lines if l.strip().startswith('|')]
sep_rows = [l for l in tbl_rows if re.match(r'^\|[\s\-|]+\|$', l.strip())]
print('=== table rows total:', len(tbl_rows), 'sep:', len(sep_rows), 'data:', len(tbl_rows)-len(sep_rows))
for i, l in enumerate(lines):
    if l.strip().startswith('|'):
        # count cols in first table header
        pass

# FAQ
m = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
h3s = re.findall(r'^### (.+)$', m.group(1), re.M) if m else []
print('=== FAQ H3 count:', len(h3s))
for h in h3s: print('   -', h)

# PK locations
print('=== PK locations:')
for m2 in re.finditer(re.escape(pk), content):
    line_no = content[:m2.start()].count('\n') + 1
    print(f'   line {line_no}: ...{content[max(0,m2.start()-50):m2.end()+30]}...'.replace(chr(10), ' '))

# meta leakage check
print('=== meta leak:', content.strip()[:60])
