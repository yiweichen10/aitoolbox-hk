# -*- coding: utf-8 -*-
import json, shutil, datetime

DRAFT = '_article_175_draft.txt'
DATA = 'data/articles_en.json'

shutil.copy(DATA, DATA + '.20260929.bak')
print('backup ->', DATA + '.20260929.bak')

raw = open(DRAFT, encoding='utf-8').read()
parts = raw.split('\n---\n', 1)          # 坑#4 / 坑#8
meta = {}
for line in parts[0].strip().splitlines():
    if ':' in line:
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()
content = parts[1].strip()

assert not content.startswith('TITLE:'), 'meta leak!'
assert 'SLUG:' not in content[:200], 'meta leak!'

d = json.load(open(DATA, encoding='utf-8'))
assert not any(a['slug'] == meta['SLUG'] for a in d), 'slug exists: ' + meta['SLUG']

dt = datetime.date.fromisoformat(meta['DATE'])
entry = {
    'title': meta['TITLE'],
    'slug': meta['SLUG'],
    'date': meta['DATE'],
    'dateFull': dt.strftime('%B %d, %Y').replace(' 0', ' '),
    'category': meta['CATEGORY'],
    'description': meta['DESCRIPTION'],
    'keywords': [k.strip() for k in meta['KEYWORDS'].split('|')],
    'content': content,
}
d.append(entry)
json.dump(d, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('appended #%d :' % len(d), entry['slug'])
print('words in content:', len(content.split()))
print('pk count:', content.count(entry['keywords'][0]))

d2 = json.load(open(DATA, encoding='utf-8'))
print('reload ok, total =', len(d2))
print('last content head:', d2[-1]['content'][:60].replace('\n', ' '))
