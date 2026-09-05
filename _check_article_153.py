# -*- coding: utf-8 -*-
import re, json
raw = open('_article_153_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta_raw, content = parts[0].strip(), parts[1].strip()
meta = dict(line.split(':', 1) for line in meta_raw.strip().splitlines() if ':' in line)
pk = meta['KEYWORDS'].split('|')[0].strip()
kws = [k.strip() for k in meta['KEYWORDS'].split('|') if k.strip()]

words = len(content.split())
print('WORDS:', words, '(target 2200-2800)', 'OK' if 2200 <= words <= 2800 else 'FAIL')

pkc = content.count(pk)
print('PK count:', pkc, repr(pk), 'OK' if pkc == 4 else 'FAIL')

banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge',
          'as an ai','in conclusion']
hits = [b for b in banned if b.lower() in content.lower()]
print('BANNED hits:', hits, 'OK' if not hits else 'FAIL')

print('--- long-tail (must all be >=1) ---')
for lt in kws[1:]:
    c = content.lower().count(lt.lower())
    print(f'  {lt:35s} {c}', 'OK' if c >= 1 else 'MISSING <<<')

links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('LINKS:', len(links), links, 'OK' if len(links) >= 2 else 'FAIL')

# table: rows starting with '|' minus separator rows
rows = [l for l in content.splitlines() if l.strip().startswith('|')]
sep = [l for l in rows if re.match(r'^\|[\s:|-]+\|$', l.strip())]
data_rows = [l for l in rows if l not in sep]
cols = max((r.count('|') - 1) for r in data_rows)
print('TABLE rows(excl header+sep):', len(data_rows)-1, 'cols:', cols,
      'OK' if len(data_rows)-1 >= 4 and cols >= 4 else 'FAIL')

faq = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
h3 = re.findall(r'### ', faq.group(1)) if faq else []
print('FAQ H3 count:', len(h3), 'OK' if len(h3) >= 3 else 'FAIL')

# meta leak guard
print('META LEAK:', 'YES' if content.startswith('TITLE:') or 'SLUG:' in content[:200] else 'no')
