# -*- coding: utf-8 -*-
import json, re, os

SRC = '_article_143_draft.txt'
JSON_PATH = 'data/articles_en.json'

raw = open(SRC, encoding='utf-8').read()
parts = raw.split('\n---\n', 1)           # 坑#4/#8：不能用 f.read() 全量当 content
assert len(parts) == 2, 'draft missing --- separator'
meta_lines = parts[0].strip().splitlines()
meta = {}
for line in meta_lines:
    if ':' in line:
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()
content = parts[1].strip()

# assertions
slug = meta['SLUG']
assert not content.startswith('TITLE:'), 'META LEAK: content starts with TITLE'
assert 'SLUG:' not in content[:200], 'META LEAK: slug in content head'
pk = meta['KEYWORDS'].split('|')[0].strip()
assert content.count(pk) == 4, f'PK count {content.count(pk)} != 4'
banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','transformative','comprehensive','revolutionize','cutting-edge',
          'as an AI','in conclusion']
assert not [b for b in banned if b.lower() in content.lower()], 'banned word present'
for lt in meta['KEYWORDS'].split('|')[1:]:
    assert content.lower().count(lt.lower()) >= 1, f'long-tail missing: {lt}'
links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
assert len(links) >= 2, f'internal links {len(links)} < 2'

d = json.load(open(JSON_PATH, encoding='utf-8'))
existing = {a.get('slug') for a in d}
assert slug not in existing, f'slug collision: {slug}'

entry = {
    'title': meta['TITLE'],
    'slug': slug,
    'date': meta['DATE'],
    'dateFull': meta['DATE'],
    'category': meta['CATEGORY'],
    'description': meta['DESCRIPTION'],
    'keywords': [k.strip() for k in meta['KEYWORDS'].split('|')],
    'content': content,
}
d.append(entry)
json.dump(d, open(JSON_PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('appended. total articles:', len(d))
print('new slug:', slug)
print('words:', len(content.split()))

# post-append leak recheck
chk = json.load(open(JSON_PATH, encoding='utf-8'))[-1]
assert not chk['content'].strip().startswith('TITLE:'), 'LEAK after append'
print('meta-leak recheck: OK')
