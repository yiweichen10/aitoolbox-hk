# -*- coding: utf-8 -*-
"""Append article #157 to data/articles_en.json. Extract body via split('\n---\n', 1) — never f.read() full (pit #8)."""
import json

raw = open('_article_157_draft.txt', encoding='utf-8').read()
head, body = raw.split('\n---\n', 1)
body = body.strip()

meta = {}
for line in head.strip().splitlines():
    if ':' in line:
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()

assert not body.startswith('TITLE:'), 'meta leaked into body!'
assert body[:100].find('SLUG:') == -1, 'meta leaked into body!'

entry = {
    'title': meta['TITLE'],
    'slug': meta['SLUG'],
    'date': meta['DATE'],
    'dateFull': 'September 10, 2026',
    'category': meta['CATEGORY'],
    'description': meta['DESCRIPTION'],
    'keywords': [k.strip() for k in meta['KEYWORDS'].split('|')],
    'content': body,
}

path = 'data/articles_en.json'
with open(path, encoding='utf-8') as f:
    arts = json.load(f)

assert not any(a['slug'] == entry['slug'] for a in arts), 'slug duplicate!'
arts.append(entry)

with open(path, 'w', encoding='utf-8') as f:
    json.dump(arts, f, ensure_ascii=False, indent=2)

# verify roundtrip
arts2 = json.load(open(path, encoding='utf-8'))
last = arts2[-1]
print('count:', len(arts2))
print('slug:', last['slug'])
print('words:', len(last['content'].split()))
print('pk:', last['content'].count('AI scheduling assistant'))
print('starts ok:', not last['content'].startswith('TITLE:'))
print('json ok: True')
