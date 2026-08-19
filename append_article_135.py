# -*- coding: utf-8 -*-
"""Append Article #135: Best AI UI/UX Design Tools 2026 to data/articles_en.json"""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DATA = 'data/articles_en.json'

with open('_article_135_draft.txt', 'r', encoding='utf-8') as f:
    content = f.read()

article = {
    "title": "Best AI UI/UX Design Tools 2026: v0 vs Bolt.new vs Figma AI vs Uizard — Design-to-Code Without the Design Department",
    "slug": "best-ai-ui-ux-design-tools-2026-v0-vs-bolt-vs-figma-ai-vs-uizard",
    "date": "2026-08-20",
    "dateFull": "2026-08-20",
    "category": "AI Design",
    "description": "UI/UX design consumes 15–25% of an app budget before a developer writes code. Here is the data-first comparison of the best AI UI/UX design tools in 2026 — v0 vs Bolt.new vs Figma AI vs Uizard (plus Lovable) — priced by what they actually cost and who they actually fit.",
    "keywords": [
        "ai ui/ux design tools 2026",
        "v0 vs bolt.new",
        "ai design to code tool",
        "figma ai pricing",
        "uizard vs figma",
        "lovable vs bolt.new",
        "ai ui generator from text",
        "bolt.new pricing",
        "v0 pricing",
        "ai prototyping tool",
        "best ai tool for ui design"
    ],
    "content": content
}

with open(DATA, 'r', encoding='utf-8') as f:
    articles = json.load(f)

# 防重复追加
slugs = [a.get('slug') for a in articles]
if article['slug'] in slugs:
    print('ALREADY EXISTS, abort')
    sys.exit(1)

articles.append(article)
with open(DATA, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print(f'OK: total articles now {len(articles)}')
print(f'Added: #{len(articles)} {article["slug"]}')
