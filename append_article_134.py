# -*- coding: utf-8 -*-
import json, sys

DATA = "C:/Users/27040/WorkBuddy/20260321092139/seo-site-en/data/articles_en.json"
DRAFT = "C:/Users/27040/WorkBuddy/automation-2026-05-24-22-17-38/_article_134_draft.txt"

raw = open(DRAFT, encoding='utf-8').read()
parts = raw.split('\n---\n', 1)          # pitfall #4: do NOT split('---')
if len(parts) != 2:
    print('ERROR: draft missing --- separator'); sys.exit(1)
meta_lines = parts[0].strip().splitlines()
meta = {}
for line in meta_lines:
    if ':' in line:
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()
content = parts[1].strip()               # pitfall #8: only the body, no meta leak

# meta leak guard
if content.startswith('TITLE:') or 'SLUG:' in content[:200]:
    print('ERROR: meta leaked into content'); sys.exit(1)

slug = meta['SLUG']
d = json.load(open(DATA, encoding='utf-8'))
if any(a['slug'] == slug for a in d):
    print('ERROR: slug already exists:', slug); sys.exit(1)

pk = meta['KEYWORDS'].split('|')[0].strip()
if content.count(pk) != 4:
    print('ERROR: PK count =', content.count(pk), '(expected 4)'); sys.exit(1)

new_article = {
    "title": meta['TITLE'],
    "slug": slug,
    "date": meta['DATE'],
    "dateFull": meta['DATE'],
    "category": meta['CATEGORY'],
    "description": meta['DESCRIPTION'],
    "keywords": [k.strip() for k in meta['KEYWORDS'].split('|')],
    "content": content,
}
d.append(new_article)
json.dump(d, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print('Appended article #%d: %s' % (len(d), slug))
print('words:', len(content.split()), '| PK count:', content.count(pk))
print('keywords:', len(new_article['keywords']))
