#!/usr/bin/env python3
"""Append article #151 (AI data labeling tools) to data/articles_en.json."""
import json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(BASE, 'data', 'articles_en.json')

with open(path, 'r', encoding='utf-8') as f:
    articles = json.load(f)

PK = 'ai data labeling tool'

with open(os.path.join(BASE, '_article_151_draft.txt'), 'r', encoding='utf-8') as f:
    raw = f.read()

lines = raw.strip().split('\n')
title = lines[0].strip()
if title.startswith('## '):
    title = title[3:].strip()
content = '\n'.join(lines[1:]).strip()

article = {
    "title": title,
    "slug": "best-ai-data-labeling-tools-2026-labelbox-vs-scale-ai-vs-encord-vs-v7",
    "date": "2026-09-04",
    "dateFull": "2026-09-04T06:50:00+08:00",
    "category": "AI Data",
    "description": "The AI data labeling market hits $6.69B in 2026 (26.5% CAGR). We tested Labelbox, Scale AI, Encord, and V7 on the same jobs to find the tool that actually ships clean training data.",
    "keywords": [
        "ai data labeling tool",
        "labelbox vs scale ai",
        "scale ai alternative",
        "data labeling pricing 2026",
        "encord vs labelbox",
        "best image annotation platform",
        "ai assisted annotation tools"
    ],
    "content": content
}

# ── Pre-flight checks ─────────────────────────────────────────────────────────
BANNED = ["leverage", "utilize", "seamlessly", "game-changing", "empower", "streamline",
          "delve into", "transformative", "comprehensive", "revolutionize", "cutting-edge",
          "as an ai", "in conclusion"]
low = content.lower()
banned_hits = [w for w in BANNED if w in low]
pk_count = low.count(PK)
word_count = len(content.split())
internal_links = re.findall(r'\]\((/articles/[^)]+)\)', content)

print("PK count:", pk_count)
print("Word count:", word_count)
print("Banned hits:", banned_hits)
print("Internal links:", internal_links)
assert pk_count == 4, f"PK must be exactly 4, got {pk_count}"
assert not banned_hits, f"Banned words found: {banned_hits}"
assert 2200 <= word_count <= 2800, f"Word count out of range: {word_count}"
assert len(internal_links) >= 2, f"Need >=2 internal links, got {len(internal_links)}"

articles.append(article)
with open(path, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)
print("Appended. Total articles:", len(articles))
