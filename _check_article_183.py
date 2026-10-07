# -*- coding: utf-8 -*-
import re, os, json

raw = open('_article_183_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = dict(l.split(':', 1) for l in parts[0].strip().splitlines() if ':' in l)
content = parts[1].strip()

print('== meta ==')
for k in ('TITLE', 'SLUG', 'CATEGORY', 'DATE'):
    print(k, '=', meta.get(k, '').strip())
print('slug dup:', any(a.get('slug') == meta['SLUG'].strip() for a in json.load(open('data/articles_en.json', encoding='utf-8'))))

print('\n== words ==')
w = len(content.split())
print('words:', w, 'OK' if 2200 <= w <= 2800 else 'FAIL')

print('\n== PK ==')
kws = [k.strip() for k in meta['KEYWORDS'].split('|')]
pk = kws[0]
n = content.count(pk)
print('PK =', repr(pk), 'count =', n, 'OK' if n == 4 else 'FAIL')

print('\n== long-tails ==')
bad = []
for lt in kws[1:]:
    c = len(re.findall(re.escape(lt), content, re.I))
    if c < 1:
        bad.append(lt)
    print(' ', lt, '->', c)
print('longtail OK' if not bad else 'longtail FAIL ' + str(bad))

print('\n== banned words ==')
banned = ['leverage', 'utilize', 'seamlessly', 'game-changing', 'empower', 'streamline',
          'delve into', 'transformative', 'comprehensive', 'revolutionize', 'cutting-edge',
          'as an AI', 'in conclusion']
hit = [b for b in banned if b.lower() in content.lower()]
print('banned:', hit, 'OK' if not hit else 'FAIL')

print('\n== internal links ==')
links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
for l in links:
    print(' ', l, 'exists=' , os.path.isdir(l.strip('/')))
print('links:', len(links), 'OK' if len(links) >= 2 and all(os.path.isdir(l.strip('/')) for l in links) else 'FAIL')

print('\n== tables ==')
lines = content.splitlines()
tables = []
cur = []
for ln in lines:
    if ln.strip().startswith('|'):
        cur.append(ln)
    else:
        if len(cur) >= 3:
            cols = [c for c in cur[0].strip().strip('|').split('|')]
            rows = len(cur) - 2
            tables.append((rows, len(cols)))
        cur = []
print('tables (rows x cols):', tables)
print('table OK' if any(r >= 4 and c >= 4 for r, c in tables) else 'table FAIL')

print('\n== FAQ ==')
m = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
h3 = re.findall(r'^### (.+)$', m.group(1), re.M) if m else []
print('FAQ H3 count:', len(h3))
for h in h3:
    print('  -', h)
print('FAQ OK' if m and len(h3) >= 3 else 'FAQ FAIL')

print('\n== meta leakage ==')
print('starts with TITLE:', content.startswith('TITLE:'), '| SLUG in first 200:', 'SLUG:' in content[:200])
print('\nword budget check: content words =', w)
