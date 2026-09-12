# -*- coding: utf-8 -*-
import re, os, json
raw = open('_article_160_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = {}
for line in parts[0].strip().splitlines():
    if ':' in line:
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()
content = parts[1].strip()
pk = meta['KEYWORDS'].split('|')[0].strip()
print('TITLE:', meta['TITLE'])
print('SLUG:', meta['SLUG'])
print('words:', len(content.split()))
print('pk [%s]:' % pk, content.count(pk))
banned = ['leverage', 'utilize', 'seamlessly', 'game-changing', 'empower', 'streamline',
          'delve into', 'transformative', 'comprehensive', 'revolutionize', 'cutting-edge',
          'as an AI', 'in conclusion']
hits = [b for b in banned if b.lower() in content.lower()]
print('banned:', hits)
for lt in meta['KEYWORDS'].split('|')[1:]:
    lt = lt.strip()
    print('longtail [%s]:' % lt, content.lower().count(lt.lower()))
links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('links:', links)
for l in links:
    print('  target', l, 'exists:', os.path.isdir(l.strip('/')))
# table rows
table_lines = [l for l in content.splitlines() if l.strip().startswith('|')]
sep = [l for l in table_lines if re.match(r'^\|[\s\-|]+\|$', l.strip())]
print('table rows (excl header+sep):', len(table_lines) - len(sep) - 2 * content.count('| Platform |'))
# FAQ H3 count
faq = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
h3s = re.findall(r'^### (.+)$', faq.group(1), re.M) if faq else []
print('FAQ H3 count:', len(h3s))
for h in h3s:
    print('  H3:', h)
