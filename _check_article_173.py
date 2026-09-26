# -*- coding: utf-8 -*-
import re, os

raw = open('_article_173_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = {}
for line in parts[0].strip().splitlines():
    if ':' in line:
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()
content = parts[1].strip()

pk = meta['KEYWORDS'].split('|')[0].strip()
print('words:', len(content.split()))
print('PK:', pk, '->', content.count(pk))

banned = ['leverage', 'utilize', 'seamlessly', 'game-changing', 'empower', 'streamline',
          'delve into', 'transformative', 'comprehensive', 'revolutionize', 'cutting-edge',
          'as an AI', 'in conclusion']
print('banned:', [b for b in banned if b.lower() in content.lower()])

print('--- long tails ---')
for lt in meta['KEYWORDS'].split('|')[1:]:
    n = content.lower().count(lt.lower())
    print(('OK ' if n >= 1 else 'XX '), lt, n)

links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('links:', links)
for l in links:
    p = l.strip('/')
    print('   exists', p, os.path.isdir(p))

# tables
lines = content.splitlines()
tbl = [l for l in lines if l.strip().startswith('|')]
sep = [l for l in tbl if re.match(r'^\|[\s\-:|]+\|$', l.strip())]
rows_total = len(tbl) - len(sep)
print('table rows incl headers:', rows_total, '| separator lines:', len(sep))
for blk in re.findall(r'((?:^\|.*\|$\n?)+)', content, re.M):
    r = [x for x in blk.strip().splitlines() if not re.match(r'^\|[\s\-:|]+\|$', x.strip())]
    cols = len([c for c in r[0].split('|') if c.strip()]) if r else 0
    print('   table: data rows', len(r) - 1, 'cols', cols)

faq = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
h3 = re.findall(r'^### ', faq.group(1), re.M) if faq else []
print('FAQ H3 count:', len(h3))

print('meta leak:', content.strip().startswith('TITLE:'), 'SLUG:' in content[:200])
print('h2 count:', len(re.findall(r'^## ', content, re.M)))
