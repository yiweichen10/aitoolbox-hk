# -*- coding: utf-8 -*-
import re, os
raw = open('_article_174_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()
kws = [k.strip() for k in meta['KEYWORDS'].split('|') if k.strip()]
pk = kws[0]
words = len(content.split())
print('words:', words, '(2200-2800)')
print('pk:', pk, '->', content.count(pk), '(need 4)')
banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge',
          'as an AI','in conclusion']
print('banned:', [b for b in banned if b.lower() in content.lower()])
print('--- long tails ---')
for lt in kws[1:]:
    print(' ', lt, content.lower().count(lt.lower()))
links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('links:')
for l in links:
    target = l.strip('/')
    exists = os.path.isdir(target)
    print('  ', l, 'exists=' , exists)
# tables
rows = [l for l in content.splitlines() if l.strip().startswith('|')]
print('table lines:', len(rows))
# FAQ
m = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
if m:
    h3 = re.findall(r'^### ', m.group(1), re.M)
    print('FAQ H3:', len(h3))
else:
    print('FAQ section MISSING')
print('H2 count:', len(re.findall(r'^## ', content, re.M)))
print('meta leak:', content.startswith('TITLE:'))
