# -*- coding: utf-8 -*-
import re, os, json

raw = open('_article_176_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()

print('=== WORDS ===', len(content.split()), '(target 2200-2800)')

pk = meta['KEYWORDS'].split('|')[0].strip()
print('=== PK ===', repr(pk), '->', content.count(pk), '(need 4)')

banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge',
          'as an AI','in conclusion']
print('=== BANNED ===', [b for b in banned if b.lower() in content.lower()])

print('=== LONG TAILS ===')
for lt in meta['KEYWORDS'].split('|')[1:]:
    lt = lt.strip()
    print('  %-45s %d' % (lt, content.lower().count(lt.lower())))

links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('=== LINKS ===', len(links))
tools = json.load(open('data/tools_en.json', encoding='utf-8'))
tl = tools if isinstance(tools, list) else tools.get('tools', tools)
tslugs = {t['slug'] for t in tl}
for l in links:
    seg = l.strip('/').split('/')
    kind, slug = seg[0], '/'.join(seg[1:])
    if kind == 'tools':
        ok = slug in tslugs
    else:
        ok = os.path.isdir(os.path.join(kind, slug))
    print('  ', l, 'exists=', ok)

# tables
rows = [l for l in content.splitlines() if l.strip().startswith('|')]
sep = [l for l in rows if re.match(r'^\s*\|[\s\-:|]+\|\s*$', l)]
print('=== TABLE ROWS ===', len(rows), 'sep lines:', len(sep))
blocks, cur = [], []
for l in content.splitlines():
    if l.strip().startswith('|'):
        cur.append(l)
    else:
        if cur: blocks.append(cur); cur = []
if cur: blocks.append(cur)
for i, b in enumerate(blocks):
    ncols = len([c for c in b[0].split('|')[1:-1]])
    print('  table%d: %d data rows x %d cols' % (i+1, len(b)-2, ncols))

# FAQ
m = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
h3 = re.findall(r'^### ', m.group(1), re.M) if m else []
print('=== FAQ H3 ===', len(h3))
for x in re.findall(r'^### (.+)$', m.group(1), re.M) if m else []:
    print('  -', x)

print('=== H2 LIST ===')
for x in re.findall(r'^## (.+)$', content, re.M):
    print('  -', x)
