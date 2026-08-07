# -*- coding: utf-8 -*-
"""Append article #121 to articles_en.json"""
import json, re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DATA = 'data/articles_en.json'
DRAFT = '_article_121_draft.txt'

with open(DRAFT, 'r', encoding='utf-8') as f:
    content = f.read().strip()

article = {
    "title": "Best AI Cold Email Tools in 2026: Instantly vs Smartlead vs Lemlist vs Woodpecker — The Real Cost of Cold Outreach",
    "slug": "best-ai-cold-email-tools-2026-instantly-vs-smartlead-vs-lemlist-vs-woodpecker",
    "date": "2026-08-08",
    "dateFull": "2026-08-08",
    "category": "AI Cold Email",
    "description": "Cold email reply rates sit between 1% and 5%, and Google's 2024 bulk-sender rules made delivery the whole game: SPF, DKIM, DMARC, one-click unsubscribe, and a spam rate under 0.3% or Gmail sends your outreach to trash. We ran Instantly, Smartlead, Lemlist, and Woodpecker as delivery infrastructure, not writing tools — covering mailbox rotation, warmup, AI personalization, sequence design, and the real per-month cost of each stack at three scales.",
    "keywords": [
        "AI cold email tools 2026",
        "Instantly vs Smartlead",
        "cold email outreach software",
        "Lemlist vs Woodpecker",
        "email warmup tools 2026",
        "best cold email tool for agencies",
        "AI cold email personalization",
        "cold email deliverability tools",
        "Smartlead vs Instantly pricing",
        "cold email automation ROI",
        "AI email sequence builders"
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

pk = 'AI cold email tools 2026'
print('Primary keyword exact count:', text.count(pk))

longtail = [
    'Instantly vs Smartlead',
    'cold email outreach software',
    'Lemlist vs Woodpecker',
    'email warmup tools 2026',
    'best cold email tool for agencies',
    'AI cold email personalization',
    'cold email deliverability tools',
    'Smartlead vs Instantly pricing',
    'cold email automation ROI',
    'AI email sequence builders',
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
