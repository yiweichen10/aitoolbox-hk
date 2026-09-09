# -*- coding: utf-8 -*-
import re, json, os

raw = open('_article_156_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()

pk = meta['KEYWORDS'].split('|')[0].strip()
print('words:', len(content.split()))
print('pk count:', content.count(pk))

banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge',
          'as an AI','in conclusion']
found_banned = [b for b in banned if b.lower() in content.lower()]
print('banned:', found_banned)

missing_lt = []
for lt in meta['KEYWORDS'].split('|')[1:]:
    lt = lt.strip()
    c = content.lower().count(lt.lower())
    print(f'lt [{lt}]: {c}')
    if c < 1:
        missing_lt.append(lt)
print('missing long-tails:', missing_lt)

# PK substring check in long-tails (would inflate count)
for lt in meta['KEYWORDS'].split('|')[1:]:
    lt = lt.strip()
    if pk.lower() in lt.lower():
        print('WARNING: long-tail contains PK:', lt)

links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('links:', links)

# verify link targets exist
tools = json.load(open('data/tools_en.json', encoding='utf-8'))
tool_slugs = {t['slug'] for t in tools}
arts = json.load(open('data/articles_en.json', encoding='utf-8'))
art_slugs = {a['slug'] for a in arts}
for l in links:
    m = re.match(r'/(tools|articles)/([^/]+)/?', l)
    if m:
        kind, slug = m.group(1), m.group(2)
        pool = tool_slugs if kind == 'tools' else art_slugs
        if slug not in pool:
            print('BROKEN LINK:', l)
        else:
            print('OK link:', l)
    else:
        print('UNPARSED LINK:', l)

# table rows: lines starting with | minus separator and header
tbl_lines = [l for l in content.splitlines() if l.strip().startswith('|')]
sep = [l for l in tbl_lines if re.match(r'^\|[\s\-|]+\|$', l.strip())]
data_rows = len(tbl_lines) - len(sep)
tables = content.count('|---')
print('table data rows total:', data_rows, '(tables:', tables, ')')

# FAQ section
faq = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
if faq:
    h3s = re.findall(r'^### ', faq.group(1), re.M)
    print('FAQ H3 count:', len(h3s))
else:
    print('NO FAQ SECTION')

# meta leakage check
print('meta leak:', content.strip()[:20])

# slug uniqueness
new_slug = meta['SLUG'].strip()
print('slug dup:', new_slug in art_slugs)
