# -*- coding: utf-8 -*-
import json

raw = open('_article_159_draft.txt', encoding='utf-8').read()
meta_part, body = raw.split('\n---\n', 1)   # 坑#4/#8
meta = dict(line.split(':', 1) for line in meta_part.strip().splitlines() if ':' in line)
content = body.strip()

assert not content.startswith('TITLE:'), 'meta leaked into content'
assert content[:20] != '', 'empty content'

entry = {
    'title': meta['TITLE'].strip(),
    'slug': meta['SLUG'].strip(),
    'date': meta['DATE'].strip(),
    'dateFull': 'September 12, 2026',
    'category': meta['CATEGORY'].strip(),
    'description': meta['DESCRIPTION'].strip(),
    'keywords': [k.strip() for k in meta['KEYWORDS'].split('|')],
    'content': content,
}

arts = json.load(open('data/articles_en.json', encoding='utf-8'))
assert entry['slug'] not in [a['slug'] for a in arts], 'slug duplicate'
arts.append(entry)
json.dump(arts, open('data/articles_en.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# verify
arts2 = json.load(open('data/articles_en.json', encoding='utf-8'))
assert len(arts2) == 159
last = arts2[-1]
assert last['slug'] == entry['slug']
assert not last['content'].startswith('TITLE:')
print('OK: appended', entry['slug'], '| words:', len(last['content'].split()), '| pk:', last['content'].count('SOC 2 compliance automation'))
