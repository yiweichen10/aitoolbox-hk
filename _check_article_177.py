# -*- coding: utf-8 -*-
import re, os, json

raw = open('_article_177_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()
pk = meta['KEYWORDS'].split('|')[0].strip()

print('== words:', len(content.split()), '(target 2200-2800)')
print('== pk [%s]:' % pk, content.count(pk), '(need 4)')

banned = ['leverage', 'utilize', 'seamlessly', 'game-changing', 'empower', 'streamline',
          'delve into', 'transformative', 'comprehensive', 'revolutionize', 'cutting-edge',
          'as an ai', 'in conclusion']
print('== banned:', [b for b in banned if b.lower() in content.lower()])

print('== long-tails:')
for lt in meta['KEYWORDS'].split('|')[1:]:
    lt = lt.strip()
    c = content.lower().count(lt.lower())
    print('   ', ('OK ' if c >= 1 else 'MISS'), c, lt)

links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('== links:', len(links))
for l in links:
    tgt = l.strip('/')
    kind = tgt.split('/')[0]
    slug = tgt.split('/', 1)[1]
    ok = os.path.isdir(os.path.join(kind, slug))
    print('   ', ('OK ' if ok else 'MISS'), l)

# tables
rows = {}
for line in content.splitlines():
    if line.strip().startswith('|'):
        rows.setdefault('t', []).append(line)
tbl_lines = rows.get('t', [])
data_rows = [l for l in tbl_lines if not re.match(r'^\|[\s\-|:]+\|$', l.strip())]
# count header rows heuristically: lines followed by a separator
seps = sum(1 for l in tbl_lines if re.match(r'^\|[\s\-|:]+\|$', l.strip()))
print('== tables:', seps, 'data-ish rows:', len(data_rows) - seps, '(need >=4 rows x 4 cols)')
for l in data_rows[:14]:
    print('     cols=%d' % (l.count('|') - 1), l[:95])

# FAQ
m = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
h3 = re.findall(r'^### ', m.group(1), re.M) if m else []
print('== FAQ h3:', len(h3), '(need >=3)')

# structure
print('== H2s:')
for h in re.findall(r'^## (.+)$', content, re.M):
    print('   ', h)

# meta leak check
print('== meta leak:', content.strip().startswith('TITLE:') or 'SLUG:' in content[:200])
