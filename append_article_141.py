#!/usr/bin/env python3
import json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE, 'data', 'articles_en.json')
DRAFT = os.path.join(BASE, '_article_141_draft.txt')

raw = open(DRAFT, encoding='utf-8').read()
# meta header is the lines before the first blank-line-separated block
meta_raw, content = raw.split('\n\n', 1)
meta = {}
for line in meta_raw.split('\n'):
    if ':' in line:
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()

title = meta['TITLE']
category = meta['CATEGORY']
date = meta['DATE']
keywords = [k.strip() for k in meta['KEYWORDS'].split(',') if k.strip()]

# description: first substantive sentence from content (data-backed opening)
first_para = content.strip().split('\n\n')[0]
desc = first_para[:300]
if '.' in desc:
    desc = desc[:desc.rfind('.')+1]
desc = ' '.join(desc.split())

slug = "best-ai-translation-tools-2026-deepl-vs-google-translate-vs-gemini-vs-claude"

with open(JSON_PATH, encoding='utf-8') as f:
    data = json.load(f)
articles = data['articles'] if isinstance(data, dict) else data

# prevent duplicate slug
if any(a.get('slug') == slug for a in articles):
    print('DUPLICATE slug, abort')
    raise SystemExit(1)

new = {
    'category': category,
    'title': title,
    'slug': slug,
    'date': date,
    'dateFull': date,
    'description': desc,
    'keywords': keywords,
    'content': content.strip(),
}
articles.append(new)

if isinstance(data, dict):
    data['articles'] = articles
with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('APPENDED article #', len(articles))
print('slug:', slug)
print('words:', len(re.findall(r"[A-Za-z0-9']+", content)))
print('PK count (ai translation tools 2026):', content.lower().count('ai translation tools 2026'))
