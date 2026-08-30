# -*- coding: utf-8 -*-
import json, re

raw = open('_article_147_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)          # 坑#4: 不能 split('---')
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()               # 坑#8: 取正文，不含 meta 头

# 防 meta 泄漏
assert not content.startswith('TITLE:'), 'META LEAKED INTO CONTENT!'
assert 'SLUG:' not in content[:200], 'META LEAKED INTO CONTENT!'

slug = meta['SLUG'].strip()
assert slug == 'best-ai-interview-copilot-tools-2026-final-round-ai-vs-interviews-chat-vs-lockedin-ai-vs-huru'

data = json.load(open('data/articles_en.json', encoding='utf-8'))
existing = {a['slug'] for a in data}
assert slug not in existing, f'slug {slug} already exists!'

keywords = [k.strip() for k in meta['KEYWORDS'].split('|') if k.strip()]
pk = keywords[0]
# PK 精确 4 次（正文）
assert content.count(pk) == 4, f'PK count = {content.count(pk)}, need 4'

# 内链校验
links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
assert len(links) >= 2, f'internal links = {len(links)}'
art_slugs = {a['slug'] for a in data}
bad = [l for l in links if l.startswith('/articles/') and l.strip('/').split('/')[1] not in art_slugs]
assert not bad, f'bad article links: {bad}'

entry = {
    "title": meta['TITLE'].strip(),
    "slug": slug,
    "date": meta['DATE'].strip(),
    "dateFull": "August 31, 2026",
    "category": meta['CATEGORY'].strip(),
    "description": meta['DESCRIPTION'].strip(),
    "keywords": keywords,
    "content": content,
}
data.append(entry)
json.dump(data, open('data/articles_en.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('appended. total articles:', len(data))
print('PK count:', content.count(pk))
print('links:', links)
