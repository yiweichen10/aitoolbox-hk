# -*- coding: utf-8 -*-
"""Self-check for article #133 before append (no bash -c, per skill pitfall #3)."""
import re, json, os

raw = open('_article_133_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
assert len(parts) == 2, 'draft format wrong'
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()

pk = meta['KEYWORDS'].split('|')[0].strip()
print('PK =', repr(pk))
print('words:', len(content.split()))
print('PK count:', content.count(pk), '(need == 4)')

banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge',
          'as an AI','in conclusion']
hits = [b for b in banned if b.lower() in content.lower()]
print('banned hits:', hits)

print('--- long-tail presence ---')
for lt in meta['KEYWORDS'].split('|')[1:]:
    lt = lt.strip()
    c = content.lower().count(lt.lower())
    print(f'  {c:2d}  {lt}')

links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('--- internal links:', len(links), '---')
for l in links:
    exists = False
    if l.startswith('/articles/'):
        slug = l.split('/')[2]
        exists = any(a['slug'] == slug for a in json.load(open('data/articles_en.json',encoding='utf-8')))
    elif l.startswith('/tools/'):
        slug = l.split('/')[2]
        exists = any(t['slug'] == slug for t in json.load(open('data/tools_en.json',encoding='utf-8')))
    print(f'  {l}  exists={exists}')

# table: count table rows (lines starting with | ) minus separator
table_lines = [l for l in content.splitlines() if l.strip().startswith('|')]
sep = [l for l in table_lines if re.match(r'^\s*\|[\s:|-]+\|\s*$', l)]
rows = [l for l in table_lines if l not in sep]
cols = max(l.count('|')-1 for l in table_lines if l not in sep)
print(f'--- table: {len(rows)} data rows x {cols} cols (need >=4 rows, >=4 cols) ---')

# FAQ
m = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
faq = m.group(1) if m else ''
h3 = re.findall(r'###\s+', faq)
print('FAQ H2 present:', bool(m), '| H3 count:', len(h3), '(need >=3)')
