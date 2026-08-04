# -*- coding: utf-8 -*-
"""Append article #118 to articles_en.json"""
import json, re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DATA = 'data/articles_en.json'
DRAFT = '_article_118_draft.txt'

with open(DRAFT, 'r', encoding='utf-8') as f:
    content = f.read().strip()

article = {
    "title": "Best AI Web Scraping Tools in 2026: Browse AI vs Octoparse vs Apify vs ScrapingBee — The Real Cost of Manual Data Collection",
    "slug": "best-ai-web-scraping-tools-2026-browse-ai-vs-octoparse-vs-apify-vs-scrapingbee",
    "date": "2026-08-05",
    "dateFull": "2026-08-05",
    "category": "AI Web Scraping",
    "description": "Global web scraping revenue hit $6.35 billion in 2024 and is compounding at 9.4% a year (Grand View Research), yet 70% of small teams still collect business data by hand. We ran Browse AI, Octoparse, Apify, and ScrapingBee against the same three jobs — bulk extraction, price monitoring, and contact pulls — and priced them at three team sizes.",
    "keywords": [
        "AI web scraping tools 2026",
        "Browse AI vs Octoparse",
        "Apify vs ScrapingBee",
        "AI data extraction tools",
        "web scraping pricing comparison",
        "no-code web scraping tools",
        "AI web scraping for lead generation",
        "best web scraping API",
        "web scraping ROI",
        "AI scraping tools for ecommerce",
        "data extraction automation pricing"
    ],
    "content": content
}

with open(DATA, 'r', encoding='utf-8') as f:
    arts = json.load(f)

# dedup by slug
arts = [a for a in arts if a.get('slug') != article['slug']]
arts.append(article)

with open(DATA, 'w', encoding='utf-8') as f:
    json.dump(arts, f, ensure_ascii=False, indent=2)

print('Total articles now:', len(arts))

# ============ COMPLIANCE CHECKS ============
text = content
words = len(text.split())
print('Word count:', words)

pk = 'AI web scraping tools 2026'
print('Primary keyword exact count:', text.count(pk))

import re as _re
locs = [m.start() for m in _re.finditer(_re.escape(pk), text, _re.IGNORECASE)]
print('Primary keyword CI count:', len(locs))

longtail = [
    'Browse AI vs Octoparse',
    'Apify vs ScrapingBee',
    'AI data extraction tools',
    'web scraping pricing comparison',
    'no-code web scraping tools',
    'AI web scraping for lead generation',
    'best web scraping API',
    'web scraping ROI',
    'AI scraping tools for ecommerce',
    'data extraction automation pricing',
]
print('\nLong-tail keywords:')
for kw in longtail:
    n = text.lower().count(kw.lower())
    print(f'  {n}x  {kw}')

banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline','delve into',
          'transformative','comprehensive','revolutionize','cutting-edge','as an AI','in conclusion']
print('\nBanned words check:')
found = []
for b in banned:
    if b.lower() in text.lower():
        found.append(b)
        print(f'  FOUND: {b}')
if not found:
    print('  NONE - clean')

print('\nInternal links:')
links = _re.findall(r'\[([^\]]+)\]\((/articles/[^)]+)\)', text)
for l in links:
    print(' ', l)
    slug = l[1].strip('/').split('/')[-1]
    valid = any(slug == a['slug'] for a in arts)
    print('   valid:', valid)

# count H2/H3
h2 = len(_re.findall(r'^## ', text, _re.M))
h3 = len(_re.findall(r'^### ', text, _re.M))
print('\nH2 count:', h2, '| H3 count:', h3)

print('FAQ section present:', 'Frequently Asked Questions' in text)
print('\nTables present (| count):', text.count('|'))
