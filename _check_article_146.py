# -*- coding: utf-8 -*-
import re, json, sys

raw = open('_article_146_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()
pk = meta['KEYWORDS'].split('|')[0].strip()

print('words:', len(content.split()))
print('PK exact count:', content.count(pk), '(need 4)')
print('PK occurrences at:', [m.start() for m in re.finditer(re.escape(pk), content)])

banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge',
          'as an AI','in conclusion']
hits = [b for b in banned if b.lower() in content.lower()]
print('BANNED hits:', hits if hits else 'NONE')

print('--- long-tail counts ---')
miss = []
for lt in meta['KEYWORDS'].split('|')[1:]:
    c = content.lower().count(lt.lower())
    print(f'{lt:42s}: {c}')
    if c == 0: miss.append(lt)
print('MISSING long-tail:', miss if miss else 'NONE')

links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('--- internal links ---', links)
bad = []
arts = json.load(open('data/articles_en.json'))
art_slugs = {a['slug'] for a in arts}
tools = json.load(open('data/tools_en.json'))
tool_slugs = {t['slug'] for t in tools}
for ln in links:
    if ln.startswith('/articles/'):
        s = ln[len('/articles/'):].rstrip('/')
        if s not in art_slugs: bad.append(('article', ln))
    elif ln.startswith('/tools/'):
        s = ln[len('/tools/'):].rstrip('/')
        if s not in tool_slugs: bad.append(('tool', ln))
print('BAD links:', bad if bad else 'NONE')

# table rows
tlines = [l for l in content.splitlines() if l.strip().startswith('|')]
sep = [l for l in tlines if re.match(r'^\|[\s:\-|]+\|$', l)]
rows = [l for l in tlines if l not in sep]
print('--- table: data rows (excl header+sep):', len(rows)-1, '(need >=4), cols:', len(rows[1].split('|'))-2 if rows else 0)

# FAQ
m = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
h3 = re.findall(r'###\s+([^\n]+)', m.group(1)) if m else []
print('--- FAQ H3 count:', len(h3), h3)
print('FAQ H2 present:', bool(m))
