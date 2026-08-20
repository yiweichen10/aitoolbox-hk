# -*- coding: utf-8 -*-
"""Append Article #136: Best AI Proposal Software 2026 to data/articles_en.json"""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DATA = 'data/articles_en.json'

with open('_article_136_draft.txt', 'r', encoding='utf-8') as f:
    content = f.read().strip()

article = {
    "title": "Best AI Proposal Software 2026: PandaDoc vs Qwilr vs Proposify vs Loopio — The Real Cost of Chasing Deals by Hand",
    "slug": "best-ai-proposal-software-2026-pandadoc-vs-qwilr-vs-proposify-vs-loopio",
    "date": "2026-08-21",
    "dateFull": "2026-08-21",
    "category": "AI Sales",
    "description": "The average proposal takes 2.5 hours to build and closes 43% of the time — speed to send doubles your odds. Here is the data-first comparison of the best AI proposal software in 2026: PandaDoc vs Qwilr vs Proposify vs Loopio, priced by what they actually cost and who they actually fit.",
    "keywords": [
        "ai proposal software 2026",
        "pandadoc pricing",
        "qwilr pricing",
        "proposify vs pandadoc",
        "loopio pricing",
        "ai proposal generator",
        "rfp response software",
        "free proposal software",
        "interactive proposal software",
        "proposal win rate",
        "proposal software for agencies"
    ],
    "content": content
}

with open(DATA, 'r', encoding='utf-8') as f:
    articles = json.load(f)

slugs = [a.get('slug') for a in articles]
if article['slug'] in slugs:
    print('ALREADY EXISTS, abort')
    sys.exit(1)

articles.append(article)
with open(DATA, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print(f'OK: total articles now {len(articles)}')
print(f'Added: #{len(articles)} {article["slug"]}')
