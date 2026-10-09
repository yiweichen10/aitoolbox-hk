# -*- coding: utf-8 -*-
"""Append article #186 to data/articles_en.json (aitoolbox.hk)."""
import json
import re
import shutil

DATA = 'data/articles_en.json'
DRAFT = '_article_186_draft.txt'

raw = open(DRAFT, encoding='utf-8').read()
head, body = raw.split('\n---\n', 1)
meta = {}
for line in head.strip().splitlines():
    if ':' in line:
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()

content = body.strip()

# --- guard: no meta leakage ---
assert not content.startswith('TITLE:'), 'meta leak: content starts with TITLE:'
assert 'SLUG:' not in content[:200], 'meta leak: SLUG in leading content'

# --- guard: internal links resolve ---
links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
assert len(links) >= 2, 'need >=2 internal links'
import os
for l in links:
    assert os.path.isdir(l.strip('/')), 'missing link target: ' + l

arts = json.load(open(DATA, encoding='utf-8'))
slug = meta['SLUG']
assert not any(a.get('slug') == slug for a in arts), 'duplicate slug'

entry = {
    'title': meta['TITLE'],
    'slug': slug,
    'date': meta['DATE'],
    'dateFull': 'October 10, 2026',
    'category': meta['CATEGORY'],
    'description': meta['DESCRIPTION'],
    'keywords': [k.strip() for k in meta['KEYWORDS'].split('|')],
    'content': content,
}

arts.append(entry)
json.dump(arts, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# --- verify round trip ---
reloaded = json.load(open(DATA, encoding='utf-8'))
last = reloaded[-1]
print('total articles:', len(reloaded))
print('slug:', last['slug'])
print('words:', len(last['content'].split()))
print('PK count:', last['content'].count('AI SOC platforms'))
print('links:', re.findall(r'\[[^\]]+\]\((/[^)]+)\)', last['content']))
print('meta leak:', last['content'].startswith('TITLE:'))
