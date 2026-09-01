# -*- coding: utf-8 -*-
import re, json, os
raw = open('_article_148_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()

pk = meta['KEYWORDS'].split('|')[0].strip()
print('PK =', repr(pk))
print('words:', len(content.split()))
print('PK count:', content.count(pk), '(must be 4)')

banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge',
          'as an AI','in conclusion']
hits = [b for b in banned if b.lower() in content.lower()]
print('BANNED hits:', hits)

print('--- long-tail counts ---')
for lt in meta['KEYWORDS'].split('|')[1:]:
    lt=lt.strip()
    c = content.lower().count(lt.lower())
    print(('OK ' if c>=1 else 'MISSING '), lt, '=', c)

links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('links:', links)
for l in links:
    d = 'articles/'+l.split('/')[-2] if l.startswith('/articles/') else l
    print('  exists:', os.path.isdir(d), d)

# table rows with >=4 cols
rows = [l for l in content.splitlines() if l.strip().startswith('|') and '---' not in l]
data_rows = [r for r in rows if not set(r.strip()) <= set('|-: ')]
print('table data rows:', len(data_rows), '| cols each:', [r.count('|')-1 for r in data_rows])

# FAQ
m = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
faq = m.group(1) if m else ''
h3 = re.findall(r'###\s+', faq)
print('FAQ H3 count:', len(h3))

# meta leak check
print('starts with TITLE?:', content.startswith('TITLE:'))
print('has SLUG in content?:', 'SLUG:' in content[:200])
