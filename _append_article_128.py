# -*- coding: utf-8 -*-
"""Append article #128 to articles_en.json. Run from seo-site-en root."""
import json, re, sys

raw = open('_article_128_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()

article = {
    "title": meta['TITLE'].strip(),
    "slug": meta['SLUG'].strip(),
    "date": meta['DATE'].strip(),
    "dateFull": meta['DATE'].strip(),
    "category": meta['CATEGORY'].strip(),
    "description": meta['DESCRIPTION'].strip(),
    "keywords": [k.strip() for k in meta['KEYWORDS'].strip().split('|')],
    "content": content,
}

path = 'data/articles_en.json'
arts = json.load(open(path, encoding='utf-8'))
assert article['slug'] not in [a['slug'] for a in arts], 'slug already exists!'
arts.append(article)
json.dump(arts, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# validate
arts2 = json.load(open(path, encoding='utf-8'))
assert len(arts2) == len(arts)
last = arts2[-1]
assert last['slug'] == article['slug']
assert len(last['keywords']) >= 6
assert len(last['content']) > 2000
# internal links real in content
links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', last['content'])
assert len(links) >= 2, links
print(f"APPENDED #{len(arts2)}: {last['slug']}")
print('links:', links)
print('keywords:', last['keywords'])
