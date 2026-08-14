# -*- coding: utf-8 -*-
"""Append article #130 to articles_en.json"""
import json, re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DATA = 'data/articles_en.json'
DRAFT = '_article_130_draft.txt'

with open(DRAFT, 'r', encoding='utf-8') as f:
    raw = f.read().strip()
    # 坑#4/#8：草稿含 meta 头，必须用 split('\n---\n', 1) 只取正文
    content = raw.split('\n---\n', 1)[1].strip()

article = {
    "title": "Best AI Chatbot Builders 2026: Chatbase vs Voiceflow vs Botpress vs Coze — The Real Cost of Hiring a Developer to Build a Bot",
    "slug": "best-ai-chatbot-builders-2026-chatbase-vs-voiceflow-vs-botpress-vs-coze",
    "date": "2026-08-15",
    "dateFull": "2026-08-15",
    "category": "AI Chatbot Builders",
    "description": "Around $11-13 billion will move through the chatbot market this year, and roughly 30% of customer service cases are already resolved by software. A custom-built bot runs $20,000-80,000 plus 15-20% annual maintenance; Chatbase, Voiceflow, Botpress, and Coze ship the same outcome for $0-150 a month. This comparison covers real pricing, billing-model traps, ROI math, and who should buy what.",
    "keywords": [
        "AI chatbot builders 2026",
        "Chatbase vs Voiceflow",
        "Voiceflow vs Botpress",
        "no-code chatbot builder",
        "custom chatbot development cost",
        "chatbot platform pricing comparison",
        "best chatbot builder for small business",
        "Botpress self-hosted",
        "Coze free plan",
        "AI chatbot for website",
        "chatbot ROI"
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

pk = 'AI chatbot builders 2026'
print('Primary keyword exact count:', text.count(pk))

longtail = [
    'Chatbase vs Voiceflow',
    'Voiceflow vs Botpress',
    'no-code chatbot builder',
    'custom chatbot development cost',
    'chatbot platform pricing comparison',
    'best chatbot builder for small business',
    'Botpress self-hosted',
    'Coze free plan',
    'AI chatbot for website',
    'chatbot ROI',
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
links = re.findall(r'\[([^\]]+)\]\((/[^)]+)\)', text)
for l in links:
    slug = l[1].strip('/').split('/')[-1]
    if l[1].startswith('/articles/'):
        valid = any(slug == a['slug'] for a in arts)
    else:
        tools = json.load(open('data/tools_en.json', encoding='utf-8'))
        valid = any(slug == t.get('slug') for t in tools)
    print(f'  {l[0]} -> {slug} | valid: {valid}')

# count H2/H3
h2 = len(re.findall(r'^## ', text, re.M))
h3 = len(re.findall(r'^### ', text, re.M))
print('\nH2 count:', h2, '| H3 count:', h3)

print('FAQ section present:', 'Frequently Asked Questions' in text)
print('\nTables present (| count):', text.count('|'))
