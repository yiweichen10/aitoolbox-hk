# -*- coding: utf-8 -*-
import re, os, json

raw = open('_article_161_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()
pk = meta['KEYWORDS'].split('|')[0].strip()

words = len(content.split())
print('words:', words, 'OK' if 2200 <= words <= 2800 else 'FAIL')

pkc = content.count(pk)
print('pk:', pkc, 'OK' if pkc == 4 else 'FAIL')

banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge',
          'as an AI','in conclusion']
hit = [b for b in banned if b.lower() in content.lower()]
print('banned:', hit, 'OK' if not hit else 'FAIL')

for lt in meta['KEYWORDS'].split('|')[1:]:
    c = content.lower().count(lt.strip().lower())
    print(f'LT [{lt.strip()}]:', c, 'OK' if c >= 1 else 'MISSING')

links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('links:', links)
for l in links:
    target = l.rstrip('/').split('/')[-1]
    ok = os.path.isdir(os.path.join('articles', target)) or os.path.isdir(os.path.join('tools', target))
    print('  target', l, 'OK' if ok else 'MISSING-DIR')

rows = [l for l in content.splitlines() if l.strip().startswith('|')]
sep = [l for l in rows if re.match(r'^\|[\s\-|]+\|$', l.strip())]
ncols_first = rows[0].count('|') - 1 if rows else 0
print('table rows (excl sep+header):', len(rows) - len(sep) - 1, '| cols:', ncols_first)

faq = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
h3 = re.findall(r'^### ', faq.group(1), re.M) if faq else []
print('faq h3 count:', len(h3), 'OK' if len(h3) >= 3 else 'FAIL')

print('meta leak:', 'FAIL' if content.startswith('TITLE:') else 'OK')
print('slug:', meta.get('SLUG'), '| date:', meta.get('DATE'), '| category:', meta.get('CATEGORY'))
