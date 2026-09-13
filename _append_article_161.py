# -*- coding: utf-8 -*-
"""Append article #161 to data/articles_en.json (pipeline rule: split meta at '\\n---\\n')."""
import json

MONTHS = {m + 1: name for m, name in enumerate(
    ['January','February','March','April','May','June','July','August','September','October','November','December'])}

raw = open('_article_161_draft.txt', encoding='utf-8').read()
meta_part, content = raw.split('\n---\n', 1)
content = content.strip()

meta = {}
for line in meta_part.strip().splitlines():
    if ':' in line:
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()

slug = meta['SLUG']
date = meta['DATE']
year, mm = date[:4], int(date[5:7])
date_full = f"{MONTHS[mm]} {int(date[8:10])}, {year}"

arts = json.load(open('data/articles_en.json', encoding='utf-8'))
slugs = {a['slug'] for a in arts}
assert slug not in slugs, f"slug exists: {slug}"

entry = {
    "title": meta['TITLE'],
    "slug": slug,
    "date": date,
    "dateFull": date_full,
    "category": meta['CATEGORY'],
    "description": meta['DESCRIPTION'],
    "keywords": [k.strip() for k in meta['KEYWORDS'].split('|')],
    "content": content,
}
arts.append(entry)

with open('data/articles_en.json', 'w', encoding='utf-8') as f:
    json.dump(arts, f, ensure_ascii=False, indent=2)

# verify
arts2 = json.load(open('data/articles_en.json', encoding='utf-8'))
last = arts2[-1]
print('count:', len(arts2))
print('slug:', last['slug'])
print('words:', len(last['content'].split()))
print('meta leak:', 'FAIL' if last['content'].strip().startswith('TITLE:') else 'OK')
print('pk:', last['content'].count('AI process documentation tools'))
