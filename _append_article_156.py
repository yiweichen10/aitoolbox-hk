# -*- coding: utf-8 -*-
"""Append article #156 to data/articles_en.json from draft file."""
import json, re

raw = open('_article_156_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)   # 坑#4/#8: 只按独立 --- 行拆一次，取正文
meta_block, content = parts[0], parts[1].strip()

meta = dict(line.split(':', 1) for line in meta_block.strip().splitlines() if ':' in line)
entry = {
    'title': meta['TITLE'].strip(),
    'slug': meta['SLUG'].strip(),
    'date': meta['DATE'].strip(),
    'dateFull': 'September 9, 2026',
    'category': meta['CATEGORY'].strip(),
    'description': meta['DESCRIPTION'].strip(),
    'keywords': [k.strip() for k in meta['KEYWORDS'].split('|')],
    'content': content,
}

# safety: no meta leak in content
assert not entry['content'].startswith('TITLE:'), 'META LEAK'
assert 'SLUG:' not in entry['content'][:200], 'META LEAK'

data = json.load(open('data/articles_en.json', encoding='utf-8'))
assert entry['slug'] not in {a['slug'] for a in data}, 'SLUG DUP'
data.append(entry)

with open('data/articles_en.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# verify round-trip
check = json.load(open('data/articles_en.json', encoding='utf-8'))
last = check[-1]
words = len(last['content'].split())
print('appended:', last['slug'])
print('total articles:', len(check))
print('words:', words)
print('pk:', last['content'].count('ai course platform'))
