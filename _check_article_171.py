# -*- coding: utf-8 -*-
import re, os, json
raw = open('_article_171_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()

print('TITLE:', meta['TITLE'].strip())
print('SLUG :', meta['SLUG'].strip())
print('CAT  :', meta['CATEGORY'].strip())
print('words:', len(content.split()), '(target 2200-2800)')

pk = meta['KEYWORDS'].split('|')[0].strip()
print('PK =', repr(pk), '-> count', content.count(pk), '(need 4)')

banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge',
          'as an AI','in conclusion']
print('banned:', [b for b in banned if b.lower() in content.lower()])

print('--- long tails ---')
for lt in meta['KEYWORDS'].split('|')[1:]:
    c = content.lower().count(lt.strip().lower())
    print(('OK ' if c else 'MISS'), lt.strip(), c)

links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('links:', len(links))
for l in links:
    tgt = l.strip('/')
    print('   ', os.path.isdir(os.path.join('.', tgt)), l)

# tables
tbl = [ln for ln in content.splitlines() if ln.strip().startswith('|')]
print('table lines:', len(tbl))
rows = 0
for ln in tbl:
    cells = [c for c in ln.strip().strip('|').split('|')]
    if set(''.join(cells).replace(' ','')) <= set('-:') and cells:
        continue
    rows += 1
    print('   cols=', len(cells), '|', ln[:60])
print('table data+header rows:', rows)

faq = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
print('FAQ section:', bool(faq))
if faq:
    print('  FAQ H3:', re.findall(r'### (.+)', faq.group(1)))

print('H2s:', re.findall(r'\n## (.+)', content))
