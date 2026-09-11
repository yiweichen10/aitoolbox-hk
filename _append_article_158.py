# -*- coding: utf-8 -*-
"""Append article #158 to data/articles_en.json (single write, meta-safe)."""
import json

raw = open('_article_158_draft.txt', encoding='utf-8').read()
meta_raw, content = raw.split('\n---\n', 1)
content = content.strip()
assert not content.startswith('TITLE:'), 'meta leak!'

meta = {}
for line in meta_raw.strip().splitlines():
    if ':' in line:
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()

slug = meta['SLUG']
data = json.load(open('data/articles_en.json', encoding='utf-8'))
assert not any(a['slug'] == slug for a in data), 'duplicate slug!'

entry = {
    'title': meta['TITLE'],
    'slug': slug,
    'date': meta['DATE'],
    'dateFull': meta['DATE'],
    'category': meta['CATEGORY'],
    'description': meta['DESCRIPTION'],
    'keywords': [k.strip() for k in meta['KEYWORDS'].split('|')],
    'content': content,
}
data.append(entry)

with open('data/articles_en.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# verify
d2 = json.load(open('data/articles_en.json', encoding='utf-8'))
last = d2[-1]
print('total:', len(d2))
print('slug:', last['slug'])
print('words:', len(last['content'].split()))
print('pk:', last['content'].count('workflow automation tools'))
print('starts-with-meta:', last['content'].strip().startswith('TITLE:'))
print('json-ok: True')
