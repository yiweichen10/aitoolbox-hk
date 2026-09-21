# -*- coding: utf-8 -*-
"""Append article #168 to data/articles_en.json (aitoolbox.hk English site)."""
import json, re, io

DRAFT = '_article_168_draft.txt'
DATA = 'data/articles_en.json'

raw = open(DRAFT, encoding='utf-8').read()
parts = raw.split('\n---\n', 1)          # pitfall #4: never split('---')
meta_lines = parts[0].strip().splitlines()
meta = {}
for line in meta_lines:
    if ':' in line:
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()
content = parts[1].strip()               # pitfall #8: body only, no meta leak

assert not content.startswith('TITLE:'), 'meta leak!'
assert 'SLUG:' not in content[:200], 'meta leak!'

title = meta['TITLE']
slug = meta['SLUG']
date = meta['DATE']
cat = meta['CATEGORY']
desc = meta['DESCRIPTION']
keywords = [k.strip() for k in meta['KEYWORDS'].split('|')]

arts = json.load(open(DATA, encoding='utf-8'))
assert all(a.get('slug') != slug for a in arts), 'slug already exists!'

# match the field shape of the most recent entry
sample = arts[-1]
print('reference entry keys:', list(sample.keys()))
print('reference dateFull:', sample.get('dateFull'))

y, m, d = date.split('-')
MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December']
date_full = f"{MONTHS[int(m)-1]} {int(d)}, {y}"

new = {
    'title': title,
    'slug': slug,
    'date': date,
    'dateFull': date_full,
    'category': cat,
    'description': desc,
    'keywords': keywords,
    'content': content,
}
for k in sample.keys():
    if k not in new:
        print('NOTE: reference has extra key not set:', k)

arts.append(new)
json.dump(arts, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# verify
chk = json.load(open(DATA, encoding='utf-8'))
last = chk[-1]
print('total articles:', len(chk))
print('slug:', last['slug'])
print('words:', len(last['content'].split()))
print('meta leak:', last['content'].startswith('TITLE:') or 'SLUG:' in last['content'][:200])
print('pk count:', last['content'].count(keywords[0]))
print('links:', re.findall(r'\[[^\]]+\]\((/[^)]+)\)', last['content']))
