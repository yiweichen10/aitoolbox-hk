# -*- coding: utf-8 -*-
import re, os

raw = open('_article_168_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()

print('=== META LEAK CHECK ===')
print('starts with TITLE:', content.startswith('TITLE:'), '| 200c has SLUG:', 'SLUG:' in content[:200])

print('\n=== WORDS ===')
print('words:', len(content.split()), '(target 2200-2800)')

kws = [k.strip() for k in meta['KEYWORDS'].split('|')]
pk = kws[0]
print('\n=== PK ===')
print('PK =', repr(pk), '-> count:', content.count(pk), '(need exactly 4)')

print('\n=== LONG TAILS ===')
for lt in kws[1:]:
    c = content.lower().count(lt.lower())
    print(('OK ' if c >= 1 else 'MISSING'), lt, '->', c)

print('\n=== BANNED ===')
banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge',
          'as an AI','in conclusion']
print([b for b in banned if b.lower() in content.lower()])

print('\n=== LINKS ===')
links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('links:', links)
for l in links:
    p = l.strip('/')
    ok = os.path.isdir(p)
    print(('OK ' if ok else 'BROKEN'), l)

print('\n=== TABLES ===')
blocks = re.findall(r'((?:^\|.*\n)+)', content, re.M)
for i, b in enumerate(blocks, 1):
    lines = [x for x in b.strip().splitlines() if x.startswith('|')]
    sep = [x for x in lines if re.match(r'^\|[\s\-:|]+\|$', x)]
    data = [x for x in lines if x not in sep]
    cols = len(data[0].split('|')) - 2 if data else 0
    print(f'table{i}: datarows={len(data)-1} cols={cols}')

print('\n=== FAQ ===')
m = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
if m:
    h3s = re.findall(r'### (.+)', m.group(1))
    print('H3 count:', len(h3s))
    for h in h3s:
        print('  -', h)
else:
    print('NO FAQ SECTION')

print('\n=== H2 LIST ===')
for h in re.findall(r'^## (.+)', content, re.M):
    print('  -', h)
