# -*- coding: utf-8 -*-
"""Append article #166 to data/articles_en.json (meta-safe: body only)."""
import json, io

DRAFT = '_article_166_draft.txt'
DATA = 'data/articles_en.json'

raw = open(DRAFT, encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()          # 坑#8: 只取正文，禁止 f.read() 全量

assert not content.startswith('TITLE:'), 'META LEAK'
assert 'SLUG:' not in content[:300], 'META LEAK'

slug = meta['SLUG'].strip()
title = meta['TITLE'].strip()
date = meta['DATE'].strip()
category = meta['CATEGORY'].strip()
description = meta['DESCRIPTION'].strip()
keywords = [k.strip() for k in meta['KEYWORDS'].split('|') if k.strip()]

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']
y, m, d = (int(x) for x in date.split('-'))
date_full = f'{MONTHS[m-1]} {d}, {y}'

with io.open(DATA, encoding='utf-8') as f:
    data = json.load(f)

arts = data if isinstance(data, list) else data.get('articles')
assert isinstance(arts, list), 'unexpected json shape'
assert not any(a.get('slug') == slug for a in arts), f'DUPLICATE SLUG: {slug}'

article = {
    'title': title,
    'slug': slug,
    'date': date,
    'dateFull': date_full,
    'category': category,
    'description': description,
    'keywords': keywords,
    'content': content,
}
arts.append(article)

with io.open(DATA, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# re-read verification
with io.open(DATA, encoding='utf-8') as f:
    check = json.load(f)
car = check if isinstance(check, list) else check.get('articles')
last = [a for a in car if a.get('slug') == slug][0]
print('total articles:', len(car))
print('slug:', last['slug'])
print('meta leak:', last['content'].strip().startswith('TITLE:') or 'SLUG:' in last['content'][:300])
print('words:', len(last['content'].split()))
print('PK count:', last['content'].count(keywords[0]))
print('keywords:', len(keywords))
