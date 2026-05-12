import json
import os

article_path = r'C:\Users\27040\WorkBuddy\20260321092139\seo-site-en/data/article_draft_b2b.md'
json_path = r'C:\Users\27040\WorkBuddy\20260321092139\seo-site-en/data/articles_en.json'

with open(article_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_article = {
    "title": "Best AI Tools for B2B Marketing: The 2026 High-Performance Stack",
    "slug": "best-ai-tools-b2b-marketing-2026",
    "date": "2026-05-12",
    "dateFull": "May 12, 2026",
    "category": "AI Tools",
    "description": "Explore the best AI tools for B2B marketing in 2026. Learn how to use an AI B2B lead generation and sales automation to close bigger deals faster.",
    "keywords": "AI tools for B2B marketing, AI B2B lead generation, best AI for B2B content, AI B2B sales automation, B2B marketing AI generator, AI for B2B customer acquisition",
    "lang": "en",
    "type": "E",
    "content": content
}

with open(json_path, 'r', encoding='utf-8') as f:
    articles = json.load(f)

articles.append(new_article)

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(articles, f, indent=2, ensure_ascii=False)

print("Article appended successfully.")
