# -*- coding: utf-8 -*-
"""Self-check for _article_132_draft.txt (2026-08-17)."""
import re

raw = open('_article_132_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)  # 坑#4: cannot split('---') plain
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()
pk = meta['KEYWORDS'].split('|')[0].strip()  # 坑#5: strip leading space

print('=== META ===')
print('title:', meta['TITLE'])
print('slug:', meta['SLUG'])
print('category:', meta['CATEGORY'])
print('date:', meta['DATE'])
print('pk:', pk)
print('longtails:', meta['KEYWORDS'].split('|')[1:])

print('\n=== COUNTS ===')
words = len(content.split())
print('words:', words, '(need 2200-2800)', 'OK' if 2200 <= words <= 2800 else 'FAIL')

pk_count = content.count(pk)
print('pk count:', pk_count, '(need == 4)', 'OK' if pk_count == 4 else 'FAIL')

banned = ['leverage', 'utilize', 'seamlessly', 'game-changing', 'empower', 'streamline',
          'delve into', 'transformative', 'comprehensive', 'revolutionize', 'cutting-edge',
          'as an AI', 'in conclusion']
hits = [b for b in banned if b.lower() in content.lower()]
print('banned words:', hits if hits else 'NONE', 'OK' if not hits else 'FAIL')

print('\n=== LONGTAILS ===')
allok = True
for lt in meta['KEYWORDS'].split('|')[1:]:
    lt = lt.strip()
    n = content.lower().count(lt.lower())
    if n < 1:
        allok = False
    print(f'{lt}: {n}', 'OK' if n >= 1 else 'FAIL')

print('\n=== LINKS ===')
links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('links:', links)
print('link count:', len(links), 'OK' if len(links) >= 2 else 'FAIL')
for l in links:
    path = l.strip('/')
    exists = False
    if path.startswith('tools/') or path.startswith('articles/'):
        import os
        exists = os.path.exists(path)
    print(f'  {l} -> exists={exists}')

print('\n=== TABLE ===')
tbl = re.search(r'(\|.*\|[\s\S]*?)(?=\n\n|\Z)', content)
rows = [line for line in content.splitlines() if line.strip().startswith('|')]
print('total pipe rows:', len(rows), '(header+separator+data; need >= 5)')
if rows:
    cols = rows[0].count('|') - 1
    print('columns:', cols, '(need >= 4)')
    data_rows = [r for r in rows if not re.match(r'^\|[\s\-|]+\|$', r)]
    print('data rows (excl separator):', len(data_rows), '(need >= 4)')

print('\n=== FAQ ===')
faq = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
if faq:
    h3 = re.findall(r'^### (.+)$', faq.group(1), re.M)
    print('FAQ H3 count:', len(h3), 'OK' if len(h3) >= 3 else 'FAIL')
    for h in h3:
        print('  -', h)
else:
    print('FAQ section NOT FOUND - FAIL')

print('\n=== META LEAK CHECK ===')
print('content starts with TITLE?:', content.strip().startswith('TITLE:'), 'OK' if not content.strip().startswith('TITLE:') else 'FAIL')

print('\n=== H2 LIST ===')
for h2 in re.findall(r'^## (.+)$', content, re.M):
    print('  H2:', h2)
