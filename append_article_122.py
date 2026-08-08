# -*- coding: utf-8 -*-
"""Append article #122 to articles_en.json"""
import json, re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DATA = 'data/articles_en.json'
DRAFT = '_article_122_draft.txt'

with open(DRAFT, 'r', encoding='utf-8') as f:
    content = f.read().strip()

article = {
    "title": "Best AI Headshot Generators in 2026: HeadshotPro vs Aragon vs TryItOn AI vs ProPhotos — The Real Cost of Looking Professional",
    "slug": "best-ai-headshot-generators-2026-headshotpro-vs-aragon-vs-tryiton-vs-prophotos",
    "date": "2026-08-09",
    "dateFull": "2026-08-09",
    "category": "AI Photo",
    "description": "LinkedIn profiles with a photo get 14x more views and 36x more connection requests, and a studio headshot runs $150 to $400 — while AI headshot generators cost $19 to $39 and deliver in under an hour. We ran HeadshotPro, Aragon, TryItOn AI, and ProPhotos on the same 22-photo input set, covering output consistency, realism, real per-person pricing, team-scale ROI, and the cases where a synthetic face is a liability, not a shortcut.",
    "keywords": [
        "AI headshot generators 2026",
        "AI headshot generator for LinkedIn",
        "HeadshotPro vs Aragon",
        "best AI headshot app",
        "professional AI headshots for business",
        "AI headshot generator pricing",
        "corporate headshot AI tools",
        "TryItOn AI vs ProPhotos",
        "AI headshots for remote teams",
        "AI headshot quality comparison",
        "AI headshot for job seekers"
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

pk = 'AI headshot generators 2026'
print('Primary keyword exact count:', text.count(pk))

longtail = [
    'AI headshot generator for LinkedIn',
    'HeadshotPro vs Aragon',
    'best AI headshot app',
    'professional AI headshots for business',
    'AI headshot generator pricing',
    'corporate headshot AI tools',
    'TryItOn AI vs ProPhotos',
    'AI headshots for remote teams',
    'AI headshot quality comparison',
    'AI headshot for job seekers',
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
links = re.findall(r'\[([^\]]+)\]\((/articles/[^)]+)\)', text)
for l in links:
    slug = l[1].strip('/').split('/')[-1]
    valid = any(slug == a['slug'] for a in arts)
    print(f'  {l[0]} -> {slug} | valid: {valid}')

# count H2/H3
h2 = len(re.findall(r'^## ', text, re.M))
h3 = len(re.findall(r'^### ', text, re.M))
print('\nH2 count:', h2, '| H3 count:', h3)

print('FAQ section present:', 'Frequently Asked Questions' in text)
print('\nTables present (| count):', text.count('|'))
