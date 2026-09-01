# -*- coding: utf-8 -*-
import json, re

SRC = '_article_148_draft.txt'
JSON = 'data/articles_en.json'

raw = open(SRC, encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta_lines = parts[0].strip().splitlines()
meta = {}
for line in meta_lines:
    if ':' in line:
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()
content = parts[1].strip()

assert not content.startswith('TITLE:'), 'META LEAK: content starts with TITLE'
assert 'SLUG:' not in content[:200], 'META LEAK: SLUG in content head'

keywords = [k.strip() for k in meta['KEYWORDS'].split('|') if k.strip()]

entry = {
    'title': meta['TITLE'],
    'slug': meta['SLUG'],
    'date': meta['DATE'],
    'dateFull': meta['DATE'] + 'T07:30:00+08:00',
    'category': meta['CATEGORY'],
    'description': meta['DESCRIPTION'],
    'keywords': keywords,
    'content': content,
}

d = json.load(open(JSON, encoding='utf-8'))
assert entry['slug'] not in [a['slug'] for a in d], 'DUPLICATE SLUG'
d.append(entry)
json.dump(d, open(JSON, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# post-append verification
a = d[-1]
assert not a['content'].strip().startswith('TITLE:')
pk = keywords[0]
assert a['content'].count(pk) == 4, 'PK count off: %d' % a['content'].count(pk)
links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', a['content'])
assert len(links) >= 2, 'links < 2'
print('appended OK. total articles:', len(d))
print('slug:', a['slug'])
print('PK count:', a['content'].count(pk))
print('links:', links)
print('words:', len(a['content'].split()))
