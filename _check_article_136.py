# -*- coding: utf-8 -*-
"""Self-check for Article #136 draft."""
import re, sys, io, json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

raw = open('_article_136_draft.txt', encoding='utf-8').read()
content = raw.strip()

pk = 'ai proposal software 2026'
long_tails = [
    'pandadoc pricing',
    'qwilr pricing',
    'proposify vs pandadoc',
    'loopio pricing',
    'ai proposal generator',
    'rfp response software',
    'free proposal software',
    'interactive proposal software',
    'proposal win rate',
    'proposal software for agencies',
]
banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge',
          'as an AI','in conclusion']

print('words:', len(content.split()), '(target 2200-2800)')
print('pk count:', content.count(pk), '(target 4)')
print('banned:', [b for b in banned if b.lower() in content.lower()])
missing_lt = [lt for lt in long_tails if content.lower().count(lt.lower()) == 0]
print('long-tail missing:', missing_lt)
for lt in long_tails:
    print('  ', lt, '->', content.lower().count(lt.lower()))

links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('links:', links)
print('num links:', len(links))

# table check: header row + separator + data rows
lines = content.splitlines()
table_start = None
for i, ln in enumerate(lines):
    if ln.strip().startswith('|') and 'PandaDoc' in ln:
        table_start = i
        break
if table_start is not None:
    data_rows = 0
    for ln in lines[table_start+2:]:
        if ln.strip().startswith('|') and set(ln.replace('|','').replace('-','').strip()) != set():
            data_rows += 1
        else:
            break
    print('table data rows:', data_rows, '(target >=4)')
else:
    print('table: NOT FOUND')

# FAQ check
faq = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
h3s = re.findall(r'^### (.+)$', faq.group(1), re.M) if faq else []
print('FAQ H3 count:', len(h3s))
for h in h3s:
    print('  ###', h)

# PK location check
for m in re.finditer(re.escape(pk), content):
    line = content[:m.start()].count('\n') + 1
    print('PK at line', line)
