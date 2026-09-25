# -*- coding: utf-8 -*-
import re, os, sys

RAW = '_article_172_draft.txt'
raw = open(RAW, encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
assert len(parts) == 2, 'meta separator missing'
meta = {}
for line in parts[0].strip().splitlines():
    if ':' in line:
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()
content = parts[1].strip()

kws = [k.strip() for k in meta['KEYWORDS'].split('|')]
pk = kws[0]

words = len(content.split())
print('words:', words, '(target 2200-2800)')
print('pk:', repr(pk), 'content count =', content.count(pk), '(must == 4)')

BANNED = ['leverage', 'utilize', 'seamlessly', 'game-changing', 'empower', 'streamline',
          'delve into', 'transformative', 'comprehensive', 'revolutionize', 'cutting-edge',
          'as an AI', 'in conclusion']
low = content.lower()
hits = [b for b in BANNED if b.lower() in low]
print('banned:', hits, '(must be [])')

print('--- long-tails ---')
missing = []
for k in kws[1:]:
    c = low.count(k.lower())
    if c == 0:
        missing.append(k)
    print('  %-45s %d' % (k, c))
print('MISSING:', missing)

links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('links:', links)
for l in links:
    tgt = l.strip('/').split('/')
    ok = os.path.isdir(os.path.join(tgt[0], tgt[1])) if len(tgt) == 2 else False
    print('   target exists:', ok, l)

# tables
tables = []
lines = content.splitlines()
i = 0
while i < len(lines):
    if lines[i].strip().startswith('|') and i + 1 < len(lines) and re.match(r'^\s*\|[\s\-:|]+\|\s*$', lines[i + 1]):
        cols = len([c for c in lines[i].strip().strip('|').split('|')])
        rows = 0
        j = i + 2
        while j < len(lines) and lines[j].strip().startswith('|'):
            rows += 1
            j += 1
        tables.append((rows, cols))
        i = j
    else:
        i += 1
print('tables (data_rows, cols):', tables, '(need >=1 with rows>=4, cols>=4)')

faq = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
if faq:
    h3 = re.findall(r'^### ', faq.group(1), re.M)
    print('FAQ H3 count:', len(h3), '(need >=3)')
else:
    print('FAQ section MISSING')

print('H2s:', re.findall(r'^## (.+)$', content, re.M))
print('starts with TITLE?:', content.startswith('TITLE:'))
