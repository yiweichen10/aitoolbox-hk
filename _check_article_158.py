# -*- coding: utf-8 -*-
import re, os, json

raw = open('_article_158_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta_lines = parts[0].strip().splitlines()
meta = {}
for line in meta_lines:
    if ':' in line:
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()
content = parts[1].strip()

print('title:', meta.get('TITLE'))
print('slug:', meta.get('SLUG'))
words = len(content.split())
print('words:', words, '->', 'OK' if 2200 <= words <= 2800 else 'FAIL')

pk = meta['KEYWORDS'].split('|')[0].strip()
pk_count = content.count(pk)
print('PK[%s]:' % pk, pk_count, '->', 'OK' if pk_count == 4 else 'FAIL')

banned = ['leverage', 'utilize', 'seamlessly', 'game-changing', 'empower', 'streamline',
          'delve into', 'transformative', 'comprehensive', 'revolutionize', 'cutting-edge',
          'as an AI', 'in conclusion']
hit = [b for b in banned if b.lower() in content.lower()]
print('banned:', hit, '->', 'OK' if not hit else 'FAIL')

fails = []
for lt in meta['KEYWORDS'].split('|')[1:]:
    c = content.lower().count(lt.lower().strip())
    print('LT[%s]:' % lt.strip(), c, '->', 'OK' if c >= 1 else 'FAIL')
    if c < 1:
        fails.append(lt)

links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('internal links:', links, '->', 'OK' if len(links) >= 2 else 'FAIL')

# verify link targets exist
targets_ok = True
for href in links:
    if href.startswith('/tools/'):
        p = os.path.join('tools', href[len('/tools/'):].strip('/'), 'index.html')
    elif href.startswith('/articles/'):
        p = os.path.join('articles', href[len('/articles/'):].strip('/'), 'index.html')
    else:
        p = None
    if p and not os.path.exists(p):
        print('MISSING TARGET:', p)
        targets_ok = False
print('targets exist:', 'OK' if targets_ok else 'FAIL')

# tables: count pipe rows
table_rows = [l for l in content.splitlines() if l.strip().startswith('|')]
sep_rows = [l for l in table_rows if re.match(r'^\|[\s\-|]+\|$', l.strip())]
data_rows = len(table_rows) - len(sep_rows)
# 2 tables, each has header row -> data rows = headers + body rows
print('table data rows (incl headers):', data_rows)
# check each table >= 4 body rows + header
cols_check = all(l.count('|') >= 5 for l in table_rows if not re.match(r'^\|[\s\-|]+\|$', l.strip()))
print('tables >=4 cols:', 'OK' if cols_check else 'FAIL')

# FAQ
faq = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
h3s = re.findall(r'^### (.+)$', faq.group(1), re.M) if faq else []
print('FAQ H3 count:', len(h3s), h3s, '->', 'OK' if len(h3s) >= 3 else 'FAIL')

# meta leak check
print('meta leak:', 'OK' if not content.startswith('TITLE:') else 'FAIL')
