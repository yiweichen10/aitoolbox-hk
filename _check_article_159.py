# -*- coding: utf-8 -*-
import re, os, json

raw = open('_article_159_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()
pk = meta['KEYWORDS'].split('|')[0].strip()

print('words:', len(content.split()))
print('pk:', content.count(pk))

banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge',
          'as an AI','in conclusion']
print('banned:', [b for b in banned if b.lower() in content.lower()])

for lt in meta['KEYWORDS'].split('|')[1:]:
    print('LT', lt, content.lower().count(lt.lower()))

links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('links:', links)
for l in links:
    p = l.replace('/articles/', 'articles/').replace('/tools/', 'tools/')
    p = p.rstrip('/') if p.rstrip('/').endswith(('2026','tools')) else p
    # rebuild expected dir
    if '/articles/' in l:
        d = 'articles/' + l.split('/articles/')[1].strip('/')
        print('  target exists:', os.path.isdir(d), d)
    elif '/tools/' in l:
        d = 'tools/' + l.split('/tools/')[1].strip('/')
        print('  target exists:', os.path.isdir(d), d)

# tables: count markdown table data rows
lines = content.splitlines()
tables = []
cur = []
for ln in lines:
    if ln.strip().startswith('|'):
        cur.append(ln)
    else:
        if cur:
            tables.append(cur)
            cur = []
if cur: tables.append(cur)
for i, tb in enumerate(tables):
    data_rows = [r for r in tb if not re.match(r'^\s*\|[\s\-|:]+\|\s*$', r)]
    ncols = max(r.count('|') - 1 for r in tb)
    print(f'table{i+1}: rows={len(data_rows)-1} (excl header) cols={ncols}')

faq = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
h3s = re.findall(r'^### ', faq.group(1), re.M) if faq else []
print('FAQ h3 count:', len(h3s))

# slug uniqueness
arts = json.load(open('data/articles_en.json', encoding='utf-8'))
slugs = [a['slug'] for a in arts]
print('slug dup:', meta['SLUG'].strip() in slugs)
print('article count now:', len(arts))
