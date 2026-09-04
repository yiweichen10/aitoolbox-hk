# -*- coding: utf-8 -*-
import json, re

PATH = 'data/articles_en.json'
raw = open('_article_152_draft.txt', encoding='utf-8').read()
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
print('PK count:', content.lower().count(keywords[0].lower()))
