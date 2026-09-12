# -*- coding: utf-8 -*-
"""Append article #160 (AI localization tools) to data/articles_en.json."""
import json, sys

raw = open('_article_160_draft.txt', encoding='utf-8').read()
# pitfall #4/#8: split on '\n---\n' once; never read full file as content
meta_raw, content = raw.split('\n---\n', 1)
content = content.strip()
assert not content.startswith('TITLE:'), 'meta leak!'
assert 'SLUG:' not in content[:300], 'meta leak!'

meta = {}
for line in meta_raw.strip().splitlines():
    if ':' in line:
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()

slug = meta['SLUG']
title = meta['TITLE']
date = meta['DATE']
month_map = {'01': 'January', '02': 'February', '03': 'March', '04': 'April',
             '05': 'May', '06': 'June', '07': 'July', '08': 'August',
             '09': 'September', '10': 'October', '11': 'November', '12': 'December'}
date_full = '%s %s, %s' % (month_map[date[5:7]], int(date[8:10]), date[:4])

record = {
    'title': title,
    'slug': slug,
    'date': date,
    'dateFull': date_full,
    'category': meta['CATEGORY'],
    'description': meta['DESCRIPTION'],
    'keywords': [k.strip() for k in meta['KEYWORDS'].split('|')],
    'content': content,
}

path = 'data/articles_en.json'
data = json.load(open(path, encoding='utf-8'))
assert isinstance(data, list), 'unexpected articles_en.json structure'
slugs = [x['slug'] for x in data]
assert slug not in slugs, 'duplicate slug: %s' % slug
data.append(record)
json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# verify round-trip
check = json.load(open(path, encoding='utf-8'))
last = check[-1]
assert last['slug'] == slug
assert last['content'] == content
print('appended:', len(check), 'articles total')
print('slug:', last['slug'])
print('words:', len(last['content'].split()))
print('pk count:', last['content'].count(record['keywords'][0]))
print('first 60 chars:', last['content'][:60])
