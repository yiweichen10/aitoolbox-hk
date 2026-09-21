# -*- coding: utf-8 -*-
"""Append article #169 to data/articles_en.json"""
import json, re, os

DRAFT = '_article_169_draft.txt'
DATA = 'data/articles_en.json'

raw = open(DRAFT, encoding='utf-8').read()
head, content = raw.split('\n---\n', 1)   # 坑#8：必须 split('\n---\n',1)
meta = {}
for line in head.strip().splitlines():
    if ':' in line:
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()
content = content.strip()

assert not content.startswith('TITLE:'), 'meta leak!'
assert 'SLUG:' not in content[:300], 'meta leak!'

arts = json.load(open(DATA, encoding='utf-8'))
assert meta['SLUG'] not in {a['slug'] for a in arts}, 'duplicate slug!'

date = meta['DATE']
month = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May',
         '06': 'June', '07': 'July', '08': 'August', '09': 'September', '10': 'October',
         '11': 'November', '12': 'December'}[date[5:7]]
date_full = f"{month} {int(date[8:10])}, {date[:4]}"

rec = {
    'title': meta['TITLE'],
    'slug': meta['SLUG'],
    'date': date,
    'dateFull': date_full,
    'category': meta['CATEGORY'],
    'description': meta['DESCRIPTION'],
    'keywords': [k.strip() for k in meta['KEYWORDS'].split('|')],
    'content': content,
}
arts.append(rec)
json.dump(arts, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# verify
chk = json.load(open(DATA, encoding='utf-8'))
last = chk[-1]
print('total articles:', len(chk))
print('slug:', last['slug'])
print('dateFull:', last['dateFull'])
print('words:', len(last['content'].split()))
print('PK count:', last['content'].count(meta['KEYWORDS'].split('|')[0].strip()))
print('meta leak:', last['content'].strip().startswith('TITLE:'))
print('links:', re.findall(r'\[[^\]]+\]\((/[^)]+)\)', last['content']))
