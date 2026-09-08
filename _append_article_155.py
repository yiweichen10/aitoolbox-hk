# -*- coding: utf-8 -*-
import json, re, os

DRAFT = '_article_155_draft.txt'
JSONP = 'data/articles_en.json'

raw = open(DRAFT, encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
assert len(parts) == 2, 'meta/body separator missing'
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()

# meta leak guard
assert not content.startswith('TITLE:'), 'META LEAK: content starts with TITLE'
assert 'SLUG:' not in content[:200], 'META LEAK: SLUG in body head'

slug = meta['SLUG'].strip()
title = meta['TITLE'].strip()
pk = meta['KEYWORDS'].split('|')[0].strip()

# slug uniqueness
data = json.load(open(JSONP, encoding='utf-8'))
exist = {a['slug'] for a in data}
assert slug not in exist, f'slug collision: {slug}'

# keyword assertions
assert content.count(pk) == 4, f'PK count {content.count(pk)} != 4'
banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge','as an AI','in conclusion']
assert not [b for b in banned if b.lower() in content.lower()], 'banned word present'
for lt in meta['KEYWORDS'].split('|')[1:]:
    assert content.lower().count(lt.lower()) >= 1, f'long-tail missing: {lt}'
# internal links exist
links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
assert len(links) >= 2, f'links {len(links)} < 2'
arts = {a['slug'] for a in data}
for l in links:
    parts_l = [p for p in l.strip('/').split('/') if p]
    assert parts_l[0] == 'articles', f'not an article link: {l}'
    assert parts_l[1] in arts, f'link target missing: {l}'

entry = {
    'title': title,
    'slug': slug,
    'date': meta['DATE'].strip(),
    'dateFull': meta['DATE'].strip(),
    'category': meta['CATEGORY'].strip(),
    'description': meta['DESCRIPTION'].strip(),
    'keywords': [k.strip() for k in meta['KEYWORDS'].split('|')],
    'content': content,
}
data.append(entry)
json.dump(data, open(JSONP, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('appended. total articles:', len(data))
print('new slug:', slug)
print('content words:', len(content.split()))
