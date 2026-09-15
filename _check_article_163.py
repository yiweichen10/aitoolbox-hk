# -*- coding: utf-8 -*-
import re, os, json

raw = open('_article_163_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)   # pit #4
meta_lines = parts[0].strip().splitlines()
meta = {}
for line in meta_lines:
    if ':' in line:
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()
content = parts[1].strip()

pk = meta['KEYWORDS'].split('|')[0].strip()
print('words:', len(content.split()))
print('pk count:', content.count(pk), '(must == 4)')

banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge',
          'as an AI','in conclusion']
found = [b for b in banned if b.lower() in content.lower()]
print('banned:', found)

lts = [x.strip() for x in meta['KEYWORDS'].split('|')[1:] if x.strip()]
for lt in lts:
    print('LT:', lt, content.lower().count(lt.lower()))

links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('links:', links)
for l in links:
    target = l.strip('/').rstrip('/')
    print('  exists?', l, os.path.isdir(target))

# table rows
table_rows = [l for l in content.splitlines() if l.strip().startswith('|')]
sep_rows = [l for l in table_rows if re.match(r'^\|[\s:\-|]+\|$', l.strip())]
print('table data rows:', len(table_rows) - len(sep_rows) - 2*len([l for l in table_rows if l.strip().startswith('| Tool') or l.strip().startswith('| Dimension')]))

# FAQ
faq = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
h3s = re.findall(r'^### ', faq.group(1), re.M) if faq else []
print('FAQ H3 count:', len(h3s))

# slug uniqueness
arts = json.load(open('data/articles_en.json', encoding='utf-8'))
print('slug dup?', any(a['slug'] == meta['SLUG'] for a in arts))
print('next idx:', len(arts) + 1)
# tools dir check
print('tools/fireflies.ai dir?', os.path.isdir('tools/fireflies.ai'))
