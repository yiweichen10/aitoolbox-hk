# -*- coding: utf-8 -*-
import re, json, os

raw = open('_article_143_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)   # 坑#4
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()

pk = meta['KEYWORDS'].split('|')[0].strip()
print('PK =', repr(pk))
words = content.split()
print('WORDS:', len(words), '(need 2200-2800)')

pkc = content.count(pk)
print('PK count:', pkc, '(need == 4)')

banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge',
          'as an AI','in conclusion']
hits = [b for b in banned if b.lower() in content.lower()]
print('BANNED hits:', hits, '(need [])')

print('--- long-tail check ---')
lt_miss = []
for lt in meta['KEYWORDS'].split('|')[1:]:
    c = content.lower().count(lt.lower())
    if c == 0:
        lt_miss.append(lt)
    print(f'  {c:2d}  {lt}')
print('MISSING long-tails:', lt_miss, '(need [])')

links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('INTERNAL LINKS:', links, '(need >=2)')

# verify link targets exist
art = json.load(open('data/articles_en.json', encoding='utf-8'))
art_slugs = {a.get('slug') for a in art}
tool = json.load(open('data/tools_en.json', encoding='utf-8'))
tool_slugs = {t.get('slug') for t in tool}
bad = []
for l in links:
    base = l.strip('/').rstrip('/')
    # strip known prefixes to get the slug
    for p in ('articles/', 'tools/'):
        if base.startswith(p):
            base = base[len(p):]
    base = base.rstrip('/')
    ok = base in art_slugs or base in tool_slugs
    if not ok:
        bad.append(l)
    print('  target', l, '-> slug', base, 'OK' if ok else 'MISSING')
print('BAD LINKS:', bad, '(need [])')

# table: count | rows (header + separator + data)
table_lines = [l for l in content.splitlines() if l.strip().startswith('|')]
data_rows = [l for l in table_lines if not re.match(r'^\|[\s:|-]+\|$', l.strip())]
cols = [len(l.split('|')) for l in table_lines]
print('TABLE lines:', len(table_lines), 'data rows:', len(data_rows), 'cols sample:', cols[:3], '(need >=4 rows x >=4 cols)')

# FAQ
m = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
if m:
    h3 = re.findall(r'###\s+', m.group(1))
    print('FAQ H3 count:', len(h3), '(need >=3)')
    print('FAQ H3:', re.findall(r'###\s+(.+)', m.group(1)))
else:
    print('FAQ section MISSING')

# meta leak check
print('META LEAK (content starts with TITLE):', content.startswith('TITLE:'))

# PK occurrences locations
idxs = [m.start() for m in re.finditer(re.escape(pk), content)]
print('PK positions:', idxs)
# show context of each
for i in idxs:
    print('   ...', content[max(0,i-40):i+len(pk)+10].replace('\n',' '), '...')
