# -*- coding: utf-8 -*-
import re, os, sys

raw = open('_article_165_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()

fail = []

w = len(content.split())
print('words:', w, 'OK' if 2200 <= w <= 2800 else 'FAIL')
if not (2200 <= w <= 2800):
    fail.append('words')

kws = [k.strip() for k in meta['KEYWORDS'].split('|')]
pk = kws[0]
pkc = content.count(pk)
print('PK:', pk, '=>', pkc, 'OK' if pkc == 4 else 'FAIL')
if pkc != 4:
    fail.append('pk')

banned = ['leverage', 'utilize', 'seamlessly', 'game-changing', 'empower', 'streamline',
          'delve into', 'transformative', 'comprehensive', 'revolutionize', 'cutting-edge',
          'as an AI', 'in conclusion']
hits = [b for b in banned if b.lower() in content.lower()]
print('banned:', hits, 'OK' if not hits else 'FAIL')
if hits:
    fail.append('banned')

print('--- long tails ---')
for lt in kws[1:]:
    n = len(re.findall(re.escape(lt), content, re.I))
    flag = 'OK' if n >= 1 else 'FAIL'
    print(f'  {lt} => {n} {flag}')
    if n < 1:
        fail.append('lt:' + lt)

links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('--- links ---')
for l in links:
    target = l.strip('/').split('?')[0]
    ok = os.path.isdir(target)
    print(f'  {l} exists={ok}')
    if not ok:
        fail.append('link:' + l)
if len(links) < 2:
    fail.append('links<2')

def table_rows(tbl):
    lines = [l for l in tbl.strip().splitlines() if l.strip().startswith('|')]
    data = [l for l in lines if not re.match(r'^\|[\s\-|:]+\|$', l.strip())]
    return len(data) - 1, len(lines[0].split('|')) - 2

tables = re.findall(r'(?:^\|.*\n)+', content, re.M)
print('--- tables ---')
for i, t in enumerate(tables, 1):
    r, c = table_rows(t)
    print(f'  table{i}: rows={r} cols={c}', 'OK' if r >= 4 and c >= 4 else 'FAIL')
    if not (r >= 4 and c >= 4):
        fail.append(f'table{i}')

faq = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
h3 = re.findall(r'^### ', faq.group(1), re.M) if faq else []
print('FAQ H2:', bool(faq), 'H3 count:', len(h3), 'OK' if faq and len(h3) >= 3 else 'FAIL')
if not (faq and len(h3) >= 3):
    fail.append('faq')

print('--- H2s ---')
for h in re.findall(r'^## .*', content, re.M):
    print('  ', h)

print('--- PK occurrences ---')
for m in re.finditer(re.escape(pk), content):
    s = max(0, m.start() - 40)
    print('   ...', content[s:m.end() + 30].replace('\n', ' '))

print()
print('RESULT:', 'ALL PASS' if not fail else 'FAIL -> ' + ', '.join(fail))
sys.exit(0 if not fail else 1)
