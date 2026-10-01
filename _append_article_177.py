# -*- coding: utf-8 -*-
import json, shutil

SRC = '_article_177_draft.txt'
DATA = 'data/articles_en.json'
BAK = 'data/articles_en.json.20261001.bak'

shutil.copy(DATA, BAK)
print('backup ->', BAK)

raw = open(SRC, encoding='utf-8').read()
meta_raw, content = raw.split('\n---\n', 1)
content = content.strip()
meta = {}
for line in meta_raw.strip().splitlines():
    if ':' in line:
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()

arts = json.load(open(DATA, encoding='utf-8'))
assert isinstance(arts, list)
slug = meta['SLUG']
assert not any(a['slug'] == slug for a in arts), 'DUPLICATE SLUG'

d = meta['DATE']
months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']
dateFull = '%s %d, %s' % (months[int(d[5:7]) - 1], int(d[8:10]), d[0:4])

arts.append({
    'title': meta['TITLE'],
    'slug': slug,
    'date': d,
    'dateFull': dateFull,
    'category': meta['CATEGORY'],
    'description': meta['DESCRIPTION'],
    'keywords': [k.strip() for k in meta['KEYWORDS'].split('|')],
    'content': content,
})
json.dump(arts, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('articles now:', len(arts))
print('dateFull:', dateFull)

a = arts[-1]
assert not a['content'].strip().startswith('TITLE:'), 'META LEAK'
assert 'SLUG:' not in a['content'][:200], 'META LEAK'
pk = meta['KEYWORDS'].split('|')[0].strip()
assert a['content'].count(pk) == 4, 'PK COUNT %d' % a['content'].count(pk)
print('meta leak: none; PK in stored content:', a['content'].count(pk))
print('stored words:', len(a['content'].split()))
