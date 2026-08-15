# -*- coding: utf-8 -*-
"""Self-check for article #131 draft."""
import re, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

raw = open('_article_131_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()

print('=== WORDS ===')
words = len(content.split())
print('word count:', words, '| OK' if 2200 <= words <= 2800 else '| FAIL')

print('\n=== PRIMARY KEYWORD ===')
pk = meta['KEYWORDS'].split('|')[0].strip()
n = content.count(pk)
print(f'PK "{pk}" exact count: {n} | {"OK" if n == 4 else "FAIL"}')
for i, line in enumerate(content.splitlines()):
    if pk in line:
        print('  found in line:', line[:90])

print('\n=== BANNED WORDS ===')
banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline','delve into',
          'transformative','comprehensive','revolutionize','cutting-edge','as an AI','in conclusion']
found = [b for b in banned if b.lower() in content.lower()]
print('banned found:', found if found else 'NONE - clean')

print('\n=== LONG-TAIL KEYWORDS ===')
for kw in meta['KEYWORDS'].split('|')[1:]:
    cnt = content.lower().count(kw.lower().strip())
    print(f'  {cnt}x  {kw.strip()}')

print('\n=== INTERNAL LINKS ===')
arts = json.load(open('data/articles_en.json', encoding='utf-8'))
tools = json.load(open('data/tools_en.json', encoding='utf-8'))
links = re.findall(r'\[([^\]]+)\]\((/[^)]+)\)', content)
for text, href in links:
    slug = href.strip('/').split('/')[-1]
    if href.startswith('/articles/'):
        valid = any(slug == a.get('slug') for a in arts)
    else:
        valid = any(slug == t.get('slug') for t in tools)
    print(f'  {text} -> {href} | valid: {valid}')
print('  total links:', len(links))

print('\n=== TABLE ===')
table_lines = [l for l in content.splitlines() if l.strip().startswith('|')]
header_rows = [l for l in table_lines if '---' not in l]
print('table data rows (incl header):', len(header_rows))
if header_rows:
    print('cols in header:', header_rows[0].count('|') - 1)

print('\n=== FAQ ===')
h2 = re.findall(r'^## (.+)$', content, re.M)
h3 = re.findall(r'^### (.+)$', content, re.M)
print('H2:', h2)
print('H3 count:', len(h3))
for h in h3:
    print('  ###', h)
faq = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
if faq:
    faq_h3 = re.findall(r'^### (.+)$', faq.group(1), re.M)
    print('FAQ section H3 count:', len(faq_h3), '| OK' if len(faq_h3) >= 3 else '| FAIL')
