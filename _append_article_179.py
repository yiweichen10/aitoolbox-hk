# -*- coding: utf-8 -*-
"""Append article #179 to data/articles_en.json."""
import io
import json
import os
import shutil
from datetime import datetime

SRC = '_article_179_draft.txt'
JSON_PATH = 'data/articles_en.json'
BAK = 'data/articles_en.json.20261003.bak'

if not os.path.exists(BAK):
    shutil.copy(JSON_PATH, BAK)
    print('[backup]', BAK)
else:
    print('[backup] already exists, skipped:', BAK)

raw = io.open(SRC, encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
assert len(parts) == 2, 'draft separator not found'
meta_block, content = parts[0].strip(), parts[1].strip()

meta = {}
for line in meta_block.splitlines():
    if ':' in line:
        key, value = line.split(':', 1)
        meta[key.strip()] = value.strip()

required = ('TITLE', 'SLUG', 'CATEGORY', 'DATE', 'DESCRIPTION', 'KEYWORDS')
for key in required:
    assert key in meta, 'missing metadata: ' + key
assert not content.startswith('TITLE:'), 'META LEAK: content starts with TITLE:'
assert 'SLUG:' not in content[:200], 'META LEAK: SLUG found in first 200 chars'

keywords = [item.strip() for item in meta['KEYWORDS'].split('|') if item.strip()]
assert len(keywords) >= 6, 'need a primary and at least five long-tail keywords'
primary_keyword = keywords[0]
assert content.count(primary_keyword) == 4, 'primary keyword count: %d' % content.count(primary_keyword)
word_count = len(content.split())
assert 2200 <= word_count <= 2800, 'word count outside range: %d' % word_count
assert '## Frequently Asked Questions' in content, 'FAQ heading missing'
assert len([line for line in content.splitlines() if line.startswith('### ')]) >= 3, 'need at least three FAQ questions'

banned = ['leverage', 'utilize', 'seamlessly', 'game-changing', 'empower', 'streamline',
          'delve into', 'transformative', 'comprehensive', 'revolutionize', 'cutting-edge',
          'as an AI', 'in conclusion']
for phrase in banned:
    assert phrase.lower() not in content.lower(), 'banned phrase found: ' + phrase

date = datetime.strptime(meta['DATE'], '%Y-%m-%d')
data = json.load(io.open(JSON_PATH, encoding='utf-8'))
assert isinstance(data, list), 'expected top-level list'
assert not any(article.get('slug') == meta['SLUG'] for article in data), 'DUPLICATE SLUG: ' + meta['SLUG']

entry = {
    'title': meta['TITLE'],
    'slug': meta['SLUG'],
    'date': meta['DATE'],
    'dateFull': '%s %d, %d' % (date.strftime('%B'), date.day, date.year),
    'category': meta['CATEGORY'],
    'description': meta['DESCRIPTION'],
    'keywords': keywords,
    'content': content,
}
data.append(entry)
with io.open(JSON_PATH, 'w', encoding='utf-8') as stream:
    json.dump(data, stream, ensure_ascii=False, indent=2)

check = json.load(io.open(JSON_PATH, encoding='utf-8'))
last = check[-1]
assert last['slug'] == meta['SLUG'], 'round-trip slug mismatch'
assert last['content'].count(primary_keyword) == 4, 'round-trip primary keyword count mismatch'
assert not last['content'].startswith('TITLE:'), 'round-trip meta leak'
print('[meta-leak check] clean')
print('[appended] total articles:', len(check))
print('  title   :', last['title'])
print('  slug    :', last['slug'])
print('  category:', last['category'], '| date:', last['date'], '/', last['dateFull'])
print('  words   :', word_count)
print('  keywords:', len(last['keywords']))
print('  PK count:', last['content'].count(primary_keyword), '(want 4)')
