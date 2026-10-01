# -*- coding: utf-8 -*-
"""Append article #178 to data/articles_en.json"""
import json, shutil, io, os
from datetime import date

SRC = '_article_178_draft.txt'
JSON_PATH = 'data/articles_en.json'
BAK = 'data/articles_en.json.20261002.bak'

# --- backup ---
if not os.path.exists(BAK):
    shutil.copy(JSON_PATH, BAK)
    print('[backup]', BAK)
else:
    print('[backup] already exists, skipped:', BAK)

# --- parse draft (pitfall #4/#8: split on newline-delimited separator only) ---
raw = io.open(SRC, encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
assert len(parts) == 2, 'draft separator not found'
meta_block, content = parts[0].strip(), parts[1].strip()

def field(name):
    for line in meta_block.splitlines():
        if line.startswith(name + ':'):
            return line.split(':', 1)[1].strip()
    raise KeyError(name)

title = field('TITLE')
slug = field('SLUG')
category = field('CATEGORY')
d = field('DATE')
description = field('DESCRIPTION')
keywords = [k.strip() for k in field('KEYWORDS').split('|') if k.strip()]

# meta-leak guard (pitfall #8)
assert not content.startswith('TITLE:'), 'META LEAK: content starts with TITLE:'
assert 'SLUG:' not in content[:200], 'META LEAK: SLUG found in first 200 chars'
print('[meta-leak check] clean')

month_map = {'01': 'January', '02': 'February', '03': 'March', '04': 'April',
             '05': 'May', '06': 'June', '07': 'July', '08': 'August',
             '09': 'September', '10': 'October', '11': 'November', '12': 'December'}
date_full = f"{month_map[d[5:7]]} {int(d[8:10])}, {d[0:4]}"

data = json.load(io.open(JSON_PATH, encoding='utf-8'))
assert isinstance(data, list), 'expected top-level list'
assert not any(a.get('slug') == slug for a in data), 'DUPLICATE SLUG: ' + slug

entry = {
    'title': title,
    'slug': slug,
    'date': d,
    'dateFull': date_full,
    'category': category,
    'description': description,
    'keywords': keywords,
    'content': content,
}
data.append(entry)

with io.open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# --- verify round-trip ---
check = json.load(io.open(JSON_PATH, encoding='utf-8'))
last = check[-1]
assert last['slug'] == slug, 'round-trip slug mismatch'
assert not last['content'].startswith('TITLE:'), 'round-trip meta leak'
print('[appended] total articles:', len(check))
print('  title   :', last['title'][:90])
print('  slug    :', last['slug'])
print('  category:', last['category'], '| date:', last['date'], '/', last['dateFull'])
print('  words   :', len(last['content'].split()))
print('  keywords:', len(last['keywords']))
print('  PK count:', last['content'].count(last['keywords'][0]), '(want 4)')
