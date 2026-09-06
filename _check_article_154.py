# -*- coding: utf-8 -*-
import re, sys

raw = open('_article_154_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()

pk = meta['KEYWORDS'].split('|')[0].strip()
print('PK =', repr(pk))
print('words:', len(content.split()))
print('pk count:', content.count(pk), '(must be 4)')
assert content.count(pk) == 4, 'PK count != 4'

banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge',
          'as an AI','in conclusion']
hits = [b for b in banned if b.lower() in content.lower()]
print('banned hits:', hits)
assert not hits, 'banned words found'

print('--- long-tail hits ---')
lt_missing = []
for lt in meta['KEYWORDS'].split('|')[1:]:
    c = content.lower().count(lt.lower())
    print(f'  {lt}: {c}')
    if c < 1:
        lt_missing.append(lt)
assert not lt_missing, f'MISSING long-tails: {lt_missing}'

links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('internal links:', links)
assert len(links) >= 2, 'need >=2 internal links'

# verify link targets exist (article or tool dirs)
import os
bad = []
for ln in links:
    if ln.startswith('/articles/'):
        slug = ln[len('/articles/'):].rstrip('/')
        if not os.path.isdir(os.path.join('articles', slug)):
            bad.append(ln)
    elif ln.startswith('/tools/'):
        slug = ln[len('/tools/'):].rstrip('/')
        if not os.path.isdir(os.path.join('tools', slug)):
            bad.append(ln)
print('bad link targets:', bad)
assert not bad, f'broken internal links: {bad}'

# table: count | rows minus separator rows
rows = [l for l in content.splitlines() if l.strip().startswith('|')]
sep = [l for l in rows if re.match(r'^\s*\|[\s:|-]+\|\s*$', l)]
data_rows = [l for l in rows if l not in sep]
print('table data rows:', len(data_rows), 'cols in first:', data_rows[0].count('|')-1 if data_rows else 0)
assert len(data_rows) >= 4, 'table needs >=4 rows'
assert (data_rows[0].count('|')-1) >= 4, 'table needs >=4 cols'

# FAQ
m = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
faq = m.group(1) if m else ''
h3 = re.findall(r'###\s+([^\n]+)', faq)
print('FAQ H3 count:', len(h3), h3)
assert len(h3) >= 3, 'FAQ needs >=3 H3'

print('\nALL CHECKS PASSED')
