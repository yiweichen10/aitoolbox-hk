# -*- coding: utf-8 -*-
import re, os, json

raw = open('_article_175_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = dict(l.split(':', 1) for l in parts[0].strip().splitlines() if ':' in l)
content = parts[1].strip()

pk = meta['KEYWORDS'].split('|')[0].strip()
print('== WORDS ==', len(content.split()), '(target 2200-2800)')
print('== PK ==', repr(pk), content.count(pk), '(need 4)')
for m in re.finditer(re.escape(pk), content):
    print('   ...', content[max(0, m.start()-60):m.end()+40].replace('\n', ' '))

banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge',
          'as an AI','in conclusion']
print('== BANNED ==', [b for b in banned if b.lower() in content.lower()])

print('== LONGTAILS ==')
miss = []
for lt in meta['KEYWORDS'].split('|')[1:]:
    lt = lt.strip()
    c = content.lower().count(lt.lower())
    if c == 0:
        miss.append(lt)
    print('  %-45s %d' % (lt, c))
print('  MISSING:', miss)

links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('== LINKS ==', links)
for l in links:
    tgt = l.strip('/')
    ok = os.path.isdir(tgt)
    print('   ', l, 'exists=', ok)

# tables
rows = [l for l in content.splitlines() if l.strip().startswith('|')]
print('== TABLE ROWS ==', len(rows))
tbl, cur = [], []
for l in rows:
    if l.strip().startswith('|---') or set(l.replace('|','').replace(' ','')) <= set('-:'):
        cur.append(l)
    else:
        cur.append(l)
# count per table block
blocks, b = [], []
prev_is_row = False
for l in content.splitlines():
    s = l.strip()
    if s.startswith('|'):
        b.append(s)
    else:
        if b: blocks.append(b); b = []
if b: blocks.append(b)
for i, blk in enumerate(blocks, 1):
    cols = blk[0].count('|') - 1
    data_rows = len(blk) - 2
    print('  table%d: %d cols x %d data rows' % (i, cols, data_rows))

faq = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
print('== FAQ H3 ==', len(re.findall(r'^### ', faq.group(1), re.M)) if faq else 'NO FAQ')
print('== H2 LIST ==')
for h in re.findall(r'^## (.+)$', content, re.M):
    print('   ', h)
print('== META LEAK ==', content.startswith('TITLE:') or 'SLUG:' in content[:200])
