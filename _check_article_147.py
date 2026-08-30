# -*- coding: utf-8 -*-
import re, json, os

raw = open('_article_147_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()
pk = meta['KEYWORDS'].split('|')[0].strip()

print('PK =', repr(pk))
print('words:', len(content.split()))
print('pk count:', content.count(pk), '(need == 4)')

banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge',
          'as an ai','in conclusion']
hits = [b for b in banned if b.lower() in content.lower()]
print('banned hits:', hits)

print('--- long-tail ---')
for lt in meta['KEYWORDS'].split('|')[1:]:
    c = content.lower().count(lt.lower())
    print(('OK ' if c >= 1 else 'MISSING ') + lt + ' : ' + str(c))

links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('--- links ---')
for l in links: print(l)
# verify targets exist
data = json.load(open('data/articles_en.json'))
slugs = {a['slug'] for a in data}
art_dir = 'articles'
bad = []
for l in links:
    m = re.match(r'/articles/([^/]+)/$', l)
    if m and m.group(1) not in slugs:
        bad.append(l)
print('bad article links:', bad)

# FAQ
m = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
h3 = re.findall(r'### ', m.group(1)) if m else []
print('FAQ H3 count:', len(h3), '(need >= 3)')

# table rows
tbl_lines = [l for l in content.splitlines() if l.strip().startswith('|')]
data_rows = [l for l in tbl_lines if not re.match(r'\|[\s:\-\|]+\|', l)]
print('table data rows:', len(data_rows), '(need >= 4)')
print('table cols (first data row):', len(data_rows[0].split('|')) - 2 if data_rows else 0, '(need >= 4)')

print('--- meta leak check ---')
print('starts with TITLE?:', content.startswith('TITLE:'))
print('first 60 chars:', repr(content[:60]))
