# -*- coding: utf-8 -*-
"""Append article #131 to articles_en.json (with compliance checks)."""
import json, re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DATA = 'data/articles_en.json'
DRAFT = '_article_131_draft.txt'

with open(DRAFT, 'r', encoding='utf-8') as f:
    raw = f.read().strip()
    # 坑#4/#8：草稿含 meta 头，必须用 split('\n---\n', 1) 只取正文
    content = raw.split('\n---\n', 1)[1].strip()

# 坑#8 后置检查：正文不得以 meta 头开头
assert not content.startswith('TITLE:'), 'meta leak: content starts with TITLE:'
assert 'SLUG:' not in content[:200], 'meta leak: SLUG: in content head'

article = {
    "title": "Best AI Photo Enhancers in 2026: Topaz Photo AI vs Remini vs Gigapixel vs Upscayl — The Real Cost of Restoring Old Photos",
    "slug": "best-ai-photo-enhancers-2026-topaz-vs-remini-vs-gigapixel-vs-upscayl",
    "date": "2026-08-16",
    "dateFull": "2026-08-16",
    "category": "AI Photo",
    "description": "Professional photo restoration labs charge $50-150 per image for standard work and $200-500+ for heavy damage. AI photo enhancers 2026 cut that to a one-time software license or a free open-source app. This comparison covers Topaz Photo AI, Remini, Gigapixel AI, and Upscayl — real pricing, billing traps, hardware requirements, and the ROI math for restoring a 200-photo family album.",
    "keywords": [
        "AI photo enhancers 2026",
        "restore old photos with AI",
        "Topaz Photo AI vs Remini",
        "AI photo restoration cost",
        "free AI photo enhancer",
        "upscale old photos for printing",
        "Remini subscription cost",
        "enhance blurry photos",
        "AI photo enhancer for Mac",
        "AI face enhancement"
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
print('Word count:', len(text.split()))
pk = 'AI photo enhancers 2026'
print('Primary keyword exact count:', text.count(pk))
banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline','delve into',
          'transformative','comprehensive','revolutionize','cutting-edge','as an AI','in conclusion']
found = [b for b in banned if b.lower() in text.lower()]
print('Banned words:', found if found else 'NONE - clean')
for kw in article['keywords'][1:]:
    print(f"  {text.lower().count(kw.lower())}x  {kw}")
print('Internal links:', len(re.findall(r'\[[^\]]+\]\((/[^)]+)\)', text)))
print('content starts with TITLE:', content.strip().startswith('TITLE:'))
