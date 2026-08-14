# -*- coding: utf-8 -*-
import re
raw = open('_article_130_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)   # 坑#4：不能 split('---')
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()
pk = meta['KEYWORDS'].split('|')[0].strip()   # 坑#5：strip 前导空格
print('PK:', pk)
print('words:', len(content.split()))          # 2200-2800
print('pk count:', content.count(pk))          # == 4
banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge',
          'as an AI','in conclusion']
print('banned:', [b for b in banned if b.lower() in content.lower()])
for lt in meta['KEYWORDS'].split('|')[1:]:
    lt = lt.strip()
    print('LT:', lt, '->', content.lower().count(lt.lower()))
links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('links:', links)
# 表格行检查
table_lines = [l for l in content.splitlines() if l.startswith('|')]
print('table lines:', len(table_lines))
# FAQ 检查
faq = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
if faq:
    h3 = re.findall(r'^### ', faq.group(1), re.M)
    print('FAQ H3 count:', len(h3))
else:
    print('FAQ H2 NOT FOUND')
