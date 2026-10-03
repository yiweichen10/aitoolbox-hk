# -*- coding: utf-8 -*-
"""Append article #180 to data/articles_en.json after validating SEO constraints."""
import json
import os
import re
import shutil
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE_DIR, '_article_180_draft.txt')
JSON_PATH = os.path.join(BASE_DIR, 'data', 'articles_en.json')
BAK = os.path.join(BASE_DIR, 'data', 'articles_en.json.20261004.bak')

if not os.path.exists(BAK):
    shutil.copy2(JSON_PATH, BAK)
    print('[backup]', BAK)

with open(SRC, encoding='utf-8') as stream:
    raw = stream.read()
parts = raw.split('\n---\n', 1)
assert len(parts) == 2, 'draft separator not found'
meta = {}
for line in parts[0].strip().splitlines():
    if ':' in line:
        key, value = line.split(':', 1)
        meta[key.strip()] = value.strip()
content = parts[1].strip()

required = ('TITLE', 'SLUG', 'CATEGORY', 'DATE', 'DESCRIPTION', 'KEYWORDS')
for key in required:
    assert key in meta, 'missing metadata: ' + key
keywords = [item.strip() for item in meta['KEYWORDS'].split('|') if item.strip()]
assert len(keywords) >= 6, 'need a primary and at least five long-tail keywords'
primary_keyword = keywords[0]
assert content.count(primary_keyword) == 4, 'primary keyword count must be exactly 4'
word_count = len(content.split())
assert 2200 <= word_count <= 2800, 'word count outside range: %d' % word_count
assert '## Frequently Asked Questions' in content, 'FAQ heading missing'
assert len([line for line in content.splitlines() if line.startswith('### ')]) >= 3, 'need at least three FAQ questions'
assert len([line for line in content.splitlines() if line.startswith('|')]) >= 6, 'comparison table needs a header and four tool rows'
assert len(re.findall(r'\[[^]]+\]\(/articles/[^)]+\)', content)) >= 2, 'need at least two internal links'
banned = ['leverage', 'utilize', 'seamlessly', 'game-changing', 'empower', 'streamline',
          'delve into', 'transformative', 'comprehensive', 'revolutionize', 'cutting-edge',
          'as an AI', 'in conclusion']
for phrase in banned:
    assert phrase.lower() not in content.lower(), 'banned phrase found: ' + phrase

date = datetime.strptime(meta['DATE'], '%Y-%m-%d')
with open(JSON_PATH, encoding='utf-8') as stream:
    data = json.load(stream)
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
with open(JSON_PATH, 'w', encoding='utf-8') as stream:
    json.dump(data, stream, ensure_ascii=False, indent=2)
    stream.write('\n')
with open(JSON_PATH, encoding='utf-8') as stream:
    check = json.load(stream)
last = check[-1]
assert last['slug'] == meta['SLUG'], 'round-trip slug mismatch'
assert last['content'].count(primary_keyword) == 4, 'round-trip primary keyword count mismatch'
assert not last['content'].startswith('TITLE:'), 'round-trip metadata leak'
print('[meta-leak check] clean')
print('[appended] total articles:', len(check))
print('  title   :', last['title'])
print('  slug    :', last['slug'])
print('  words   :', word_count)
print('  keywords:', len(keywords))
print('  PK count:', last['content'].count(primary_keyword), '(want 4)')
