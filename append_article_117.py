# -*- coding: utf-8 -*-
"""Append article #117 to articles_en.json"""
import json, re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DATA = 'data/articles_en.json'
DRAFT = '_article_117_draft.txt'

with open(DRAFT, 'r', encoding='utf-8') as f:
    content = f.read().strip()

article = {
    "title": "Best AI SEO Content Optimization Tools in 2026: Surfer vs Clearscope vs Frase vs MarketMuse — The Real Cost of Content That Doesn't Rank",
    "slug": "best-ai-seo-content-optimization-tools-2026-surfer-vs-clearscope-vs-frase-vs-marketmuse",
    "date": "2026-08-04",
    "dateFull": "2026-08-04",
    "category": "AI SEO",
    "description": "90.63% of web pages get zero organic traffic (Ahrefs, one billion pages analyzed), and the top three Google results capture 54.4% of all clicks (Backlinko). We ran Surfer SEO, Clearscope, Frase, and MarketMuse on the same 40-page test site for three months — methodology, real pricing, and how the labor savings actually shake out.",
    "keywords": [
        "AI content optimization tools 2026",
        "Surfer SEO vs Clearscope",
        "Clearscope vs MarketMuse",
        "Frase vs Surfer SEO",
        "AI content optimization software",
        "SEO content optimization pricing",
        "best AI tool for on-page SEO",
        "AI SEO writing assistant",
        "content optimization ROI",
        "AI keyword research tools 2026",
        "SEO content optimization for small business"
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

pk = 'AI content optimization tools 2026'
print('Primary keyword exact count:', text.count(pk))

import re as _re
locs = [m.start() for m in _re.finditer(_re.escape(pk), text, _re.IGNORECASE)]
print('Primary keyword CI count:', len(locs))

longtail = [
    'Surfer SEO vs Clearscope',
    'Clearscope vs MarketMuse',
    'Frase vs Surfer SEO',
    'AI content optimization software',
    'SEO content optimization pricing',
    'best AI tool for on-page SEO',
    'AI SEO writing assistant',
    'content optimization ROI',
    'AI keyword research tools 2026',
    'SEO content optimization for small business',
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
    slug = l[1].split('/')[-1]
    valid = any(slug == a['slug'] for a in arts)
    print('   valid:', valid)

# count H2/H3
h2 = len(_re.findall(r'^## ', text, _re.M))
h3 = len(_re.findall(r'^### ', text, _re.M))
print('\nH2 count:', h2, '| H3 count:', h3)

print('FAQ section present:', 'Frequently Asked Questions' in text)
print('\nTables present (| count):', text.count('|'))
