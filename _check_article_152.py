# -*- coding: utf-8 -*-
import re, sys, json, os

raw = open('_article_152_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()

# meta leak guard
assert not content.startswith('TITLE:'), "META LEAK: content starts with TITLE"
assert 'SLUG:' not in content[:200], "META LEAK: SLUG in content head"

kws = meta['KEYWORDS'].split('|')
pk = kws[0].strip()
longtail = [k.strip() for k in kws[1:] if k.strip()]

words = len(content.split())
pk_count = content.lower().count(pk.lower())

banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge',
          'as an ai','in conclusion']
banned_hit = [b for b in banned if b.lower() in content.lower()]

links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)

# table: rows starting with '|' minus separator rows, minus header
table_rows = [l for l in content.splitlines() if l.strip().startswith('|')]
data_rows = [l for l in table_rows if not re.match(r'^\s*\|[\s:|-]+\|\s*$', l)]
# header + data rows
table_ok = len(data_rows) >= 5  # 1 header + >=4 data

# FAQ
m = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
faq_h3 = re.findall(r'###\s+', m.group(1)) if m else []

print('WORDS      :', words, 'OK' if 2200 <= words <= 2800 else 'FAIL')
print('PK         :', repr(pk), '=', pk_count, 'OK' if pk_count == 4 else 'FAIL')
for lt in longtail:
    c = content.lower().count(lt.lower())
    print('  longtail  :', repr(lt), '=', c, 'OK' if c >= 1 else 'FAIL')
print('BANNED     :', banned_hit if banned_hit else 'none OK')
print('LINKS      :', links, 'OK' if len(links) >= 2 else 'FAIL')
print('TABLE rows :', len(data_rows), 'OK' if table_ok else 'FAIL')
print('FAQ H3     :', len(faq_h3), 'OK' if len(faq_h3) >= 3 else 'FAIL')

ok = (2200 <= words <= 2800 and pk_count == 4 and not banned_hit and len(links) >= 2
      and table_ok and len(faq_h3) >= 3 and all(content.lower().count(lt.lower()) >= 1 for lt in longtail))
print('\nALL OK' if ok else '\nFAIL')
sys.exit(0 if ok else 1)
