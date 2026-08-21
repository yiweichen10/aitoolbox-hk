# -*- coding: utf-8 -*-
"""Append Article #137 (Best AI Payroll Software 2026) to data/articles_en.json."""
import json, io, sys

ARTICLES_PATH = 'data/articles_en.json'
DRAFT = open('_article_137_draft.txt', encoding='utf-8').read()

new_article = {
    "category": "AI HR",
    "title": "Best AI Payroll Software 2026: Gusto vs Rippling vs Deel vs ADP — Where the AI Actually Pays Off",
    "slug": "best-ai-payroll-software-2026-gusto-vs-rippling-vs-deel-vs-adp",
    "date": "2026-08-22",
    "dateFull": "2026-08-22",
    "description": ("The IRS collects over $7 billion in payroll penalties every year and one in five payrolls still "
                    "contains an error. Here is the data-first comparison of the best ai payroll software 2026: "
                    "Gusto vs Rippling vs Deel vs ADP, priced from vendor pages and buyer data."),
    "keywords": [
        "ai payroll software 2026",
        "gusto vs rippling",
        "ai payroll software pricing",
        "rippling pricing per employee",
        "deel eor pricing",
        "adp run pricing",
        "onpay vs gusto",
        "best payroll software for small business",
        "global payroll software",
        "automatic payroll processing",
        "payroll tax penalties",
    ],
    "content": DRAFT,
}

with open(ARTICLES_PATH, encoding='utf-8') as f:
    articles = json.load(f)

slugs = {a['slug'] for a in articles}
if new_article['slug'] in slugs:
    print(f"[ERROR] slug {new_article['slug']} already exists")
    sys.exit(1)

articles.append(new_article)
with open(ARTICLES_PATH, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=1)

print(f"[OK] appended. total articles now: {len(articles)}")
print(f"[OK] last: {articles[-1]['slug']}")
