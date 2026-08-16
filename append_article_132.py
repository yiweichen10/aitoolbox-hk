# -*- coding: utf-8 -*-
"""Append article #132 to data/articles_en.json (2026-08-17)."""
import json

raw = open('_article_132_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)  # 坑#4/#8: split meta from body correctly
assert len(parts) == 2, 'draft format wrong'
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()

assert not content.startswith('TITLE:'), 'meta leak into content!'
assert content.count(meta['KEYWORDS'].split('|')[0].strip()) == 4, 'PK count != 4'

with open('data/articles_en.json', encoding='utf-8') as f:
    articles = json.load(f)

assert isinstance(articles, list)
new_slug = meta['SLUG'].strip()
assert all(a['slug'] != new_slug for a in articles), f'slug already exists: {new_slug}'

article = {
    'title': meta['TITLE'].strip(),
    'slug': new_slug,
    'date': meta['DATE'].strip(),
    'dateFull': meta['DATE'].strip(),
    'category': meta['CATEGORY'].strip(),
    'description': meta['DESCRIPTION'].strip(),
    'keywords': [k.strip() for k in meta['KEYWORDS'].split('|')],
    'content': content,
}
articles.append(article)

with open('data/articles_en.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print(f'appended #{len(articles)}: {article["slug"]}')
print('last article content starts with:', repr(article['content'][:60]))
print('JSON valid: OK')
