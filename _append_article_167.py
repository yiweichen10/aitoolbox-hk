# -*- coding: utf-8 -*-
import json, re

raw = open('_article_167_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)   # 坑#4：不能用 split('---')
meta = {}
for line in parts[0].strip().splitlines():
    if ':' in line:
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()
content = parts[1].strip()

month_map = {'01':'January','02':'February','03':'March','04':'April','05':'May','06':'June',
             '07':'July','08':'August','09':'September','10':'October','11':'November','12':'December'}
date = meta['DATE']
dateFull = f"{month_map[date[5:7]]} {int(date[8:10])}, {date[:4]}"

art = {
    'title': meta['TITLE'],
    'slug': meta['SLUG'],
    'date': date,
    'dateFull': dateFull,
    'category': meta['CATEGORY'],
    'description': meta['DESCRIPTION'],
    'keywords': [k.strip() for k in meta['KEYWORDS'].split('|')],
    'content': content,
}

# 坑#8 检查：meta 泄漏
assert not content.startswith('TITLE:'), 'META LEAK'
assert 'SLUG:' not in content[:200], 'META LEAK 200'
pk = meta['KEYWORDS'].split('|')[0].strip()
assert content.count(pk) == 4, f'PK={content.count(pk)}'
w = len(content.split())
assert 2200 <= w <= 2800, f'words={w}'

path = 'data/articles_en.json'
a = json.load(open(path, encoding='utf-8'))
assert not any(x['slug'] == art['slug'] for x in a), 'slug dup'
a.append(art)
json.dump(a, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# 回读验证
b = json.load(open(path, encoding='utf-8'))
last = b[-1]
print('appended:', last['slug'])
print('count:', len(b))
print('words:', len(last['content'].split()))
print('pk:', last['content'].count(pk))
print('start:', last['content'][:60])
