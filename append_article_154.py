# -*- coding: utf-8 -*-
import json, re

PATH = 'data/articles_en.json'
raw = open('_article_154_draft.txt', encoding='utf-8').read()
meta_raw, content = raw.split('\n---\n', 1)
meta = dict(line.split(':', 1) for line in meta_raw.strip().splitlines() if ':' in line)
content = content.strip()

# meta leak guard
assert not content.startswith('TITLE:'), 'META LEAK'
assert 'SLUG:' not in content[:200], 'META LEAK'

slug = meta['SLUG'].strip()
title = meta['TITLE'].strip()
cat = meta['CATEGORY'].strip()
date = meta['DATE'].strip()
desc = meta['DESCRIPTION'].strip()
keywords = [k.strip() for k in meta['KEYWORDS'].split('|') if k.strip()]

# slug uniqueness
data = json.load(open(PATH, encoding='utf-8'))
assert not any(a['slug'] == slug for a in data), f'SLUG EXISTS: {slug}'

# internal link targets exist (articles)
existing = {a['slug'] for a in data}
links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
for ln in links:
    tgt = ln.strip('/').rstrip('/')
    parts = tgt.split('/')
    if parts[0] == 'articles':
        assert parts[1] in existing, f'ARTICLE LINK TARGET MISSING: {ln}'
print('links OK:', links)

# quality assertions (mirror _check_article_154.py)
pk = keywords[0]
assert content.count(pk) == 4, f'PK count={content.count(pk)}'
banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge',
          'as an ai','in conclusion']
assert not [b for b in banned if b.lower() in content.lower()], 'BANNED WORD'
for lt in keywords[1:]:
    assert content.lower().count(lt.lower()) >= 1, f'LONGTAIL MISSING: {lt}'
assert 2200 <= len(content.split()) <= 2800, f'WORDS={len(content.split())}'

entry = {
    'title': title,
    'slug': slug,
    'date': date,
    'dateFull': date + 'T07:00:00+08:00',
    'category': cat,
    'description': desc,
    'keywords': keywords,
    'content': content,
}
data.append(entry)
json.dump(data, open(PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('APPENDED. total articles:', len(data))
print('new content words:', len(content.split()))
print('PK count:', content.count(pk))
print('first 60 chars:', repr(content[:60]))
