# -*- coding: utf-8 -*-
import json, re

PATH = 'data/articles_en.json'
raw = open('_article_146_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()

# assert no meta leak
assert not content.startswith('TITLE:'), 'META LEAK: content starts with TITLE'
assert 'SLUG:' not in content[:300], 'META LEAK: SLUG in content head'

slug = meta['SLUG'].strip()
title = meta['TITLE'].strip()
date = meta['DATE'].strip()
cat = meta['CATEGORY'].strip()
desc = meta['DESCRIPTION'].strip()
kw = meta['KEYWORDS'].strip()  # pipe-separated string

data = json.load(open(PATH, encoding='utf-8'))
assert slug not in [a['slug'] for a in data], f'DUPLICATE slug {slug}'
assert len(content.split()) >= 2200 and len(content.split()) <= 2800, f'word count {len(content.split())} out of range'

entry = {
    'title': title,
    'slug': slug,
    'date': date,
    'dateFull': date,
    'category': cat,
    'description': desc,
    'keywords': kw,
    'content': content,
}
data.append(entry)
json.dump(data, open(PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# re-validate
chk = json.load(open(PATH, encoding='utf-8'))
assert chk[-1]['slug'] == slug
print('appended OK. total articles:', len(chk))
print('PK in content:', chk[-1]['content'].count('ai background remover'))
links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', chk[-1]['content'])
print('internal links:', links)
