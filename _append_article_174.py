# -*- coding: utf-8 -*-
import json

DRAFT = '_article_174_draft.txt'
DATA = 'data/articles_en.json'

raw = open(DRAFT, encoding='utf-8').read()
head, body = raw.split('\n---\n', 1)
content = body.strip()

meta = {}
for line in head.strip().splitlines():
    if ':' in line:
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()

assert not content.startswith('TITLE:'), 'meta leak'
assert 'SLUG:' not in content[:200], 'meta leak'

arts = json.load(open(DATA, encoding='utf-8'))
assert not any(a['slug'] == meta['SLUG'] for a in arts), 'duplicate slug'

arts.append({
    'title': meta['TITLE'],
    'slug': meta['SLUG'],
    'date': meta['DATE'],
    'dateFull': 'September 28, 2026',
    'category': meta['CATEGORY'],
    'description': meta['DESCRIPTION'],
    'keywords': [k.strip() for k in meta['KEYWORDS'].split('|')],
    'content': content,
})

json.dump(arts, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('appended, total articles:', len(arts))
print('last slug:', arts[-1]['slug'])
print('content words:', len(arts[-1]['content'].split()))
print('pk count:', arts[-1]['content'].count('AI customer data platform software'))
