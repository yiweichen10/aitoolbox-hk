# -*- coding: utf-8 -*-
import re, json, os
raw = open('_article_155_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()
pk = meta['KEYWORDS'].split('|')[0].strip()
print('PK =', repr(pk))
print('words:', len(content.split()))
print('pk count:', content.count(pk), '(expect 4)')
banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge',
          'as an AI','in conclusion']
hits = [b for b in banned if b.lower() in content.lower()]
print('banned hits:', hits)
print('--- long-tails ---')
for lt in meta['KEYWORDS'].split('|')[1:]:
    c = content.lower().count(lt.lower())
    print(('OK ' if c>=1 else 'MISSING '), lt, c)
links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('--- links ---', links)
# verify targets exist
arts = {a['slug'] for a in json.load(open('data/articles_en.json'))}
for l in links:
    ok = l.startswith('/articles/') and l.strip('/').split('/')[0]=='articles' and l[1:].rstrip('/') in arts
    # simpler: check file exists
    p = l.lstrip('/')
    exists = os.path.isdir(p) or os.path.isfile(p)
    print(l, 'dir-exists' if os.path.isdir(p) else ('file-exists' if os.path.isfile(p) else 'CHECK'))
# table rows
tbl_lines = [l for l in content.splitlines() if l.strip().startswith('|')]
# exclude separator rows
data_rows = [l for l in tbl_lines if not re.match(r'^\s*\|[\s:|-]+\|\s*$', l)]
print('table data rows (excl header+sep):', len(data_rows)-1)  # minus header
# FAQ
m = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
h3 = re.findall(r'###\s+([^\n]+)', m.group(1)) if m else []
print('FAQ H3 count:', len(h3), h3)
# check FAQ H3 not containing pk
for h in h3:
    if pk.lower() in h.lower():
        print('WARN: FAQ H3 contains PK ->', h)
