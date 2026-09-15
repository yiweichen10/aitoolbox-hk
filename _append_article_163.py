# -*- coding: utf-8 -*-
"""Append article #163 to data/articles_en.json (pit #8: extract body after \\n---\\n)."""
import json, shutil

shutil.copy('data/articles_en.json', 'data/articles_en.json.20260916.bak')

raw = open('_article_163_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = {}
for line in parts[0].strip().splitlines():
    if ':' in line:
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()
content = parts[1].strip()

assert not content.startswith('TITLE:'), 'meta leaked into content'
assert content.count(meta['KEYWORDS'].split('|')[0].strip()) == 4, 'PK count != 4'

entry = {
    "title": meta['TITLE'],
    "slug": meta['SLUG'],
    "date": meta['DATE'],
    "dateFull": "September 16, 2026",
    "category": meta['CATEGORY'],
    "description": meta['DESCRIPTION'],
    "keywords": [k.strip() for k in meta['KEYWORDS'].split('|') if k.strip()],
    "content": content,
}

arts = json.load(open('data/articles_en.json', encoding='utf-8'))
assert not any(a['slug'] == entry['slug'] for a in arts), 'slug duplicate'
arts.append(entry)
json.dump(arts, open('data/articles_en.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# verify round-trip
arts2 = json.load(open('data/articles_en.json', encoding='utf-8'))
last = arts2[-1]
print('total:', len(arts2))
print('slug:', last['slug'])
print('content starts:', last['content'][:60])
print('content words:', len(last['content'].split()))
print('pk:', last['content'].count('AI user research tools'))
