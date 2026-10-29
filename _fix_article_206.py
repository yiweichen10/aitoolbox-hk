#!/usr/bin/env python3
"""Third trim pass for article #206 (get under 2,800 words)."""
import json, re

PATH = 'data/articles_en.json'
SLUG = 'best-privacy-first-analytics-tools-2026-plausible-vs-fathom-vs-matomo-vs-ga4'

reps = [
    ("and EasyPrivacy filter lists have been deleting the same requests inside ad blockers for a decade. A meaningful share of your real traffic never reaches Google's servers, and no report will tell you which share.",
     "and EasyPrivacy filter lists have been deleting the same requests in ad blockers for a decade — a meaningful share of your real traffic never reaches Google's servers, and no report will tell you which share."),
    ("I have run real traffic through all four across client sites and my own properties: Plausible on content sites since 2021,",
     "I have run real traffic through all four: Plausible on content sites since 2021,"),
    ("The 2026 tier structure splits into three plans, each priced per traffic band, with annual billing costing 10x the monthly price (two months free):",
     "The 2026 tiers split into three plans, priced per traffic band, with annual billing costing 10x the monthly price (two months free):"),
    ("because Fathom's bet is that you should never study a pricing matrix to decide which features you need.",
     "because Fathom's bet is that you should never study a pricing matrix to pick features."),
    ("and the free Fathom Lite repo is a basic pageview counter without team features, not a real alternative to its own cloud.",
     "and the free Fathom Lite repo is a basic pageview counter, not a real alternative to its own cloud."),
]

with open(PATH, encoding='utf-8') as f:
    data = json.load(f)

idx = next(i for i, a in enumerate(data) if a['slug'] == SLUG)
c = data[idx]['content']
for old, new in reps:
    if old not in c:
        raise SystemExit(f"NOT FOUND: {old[:60]}...")
    c = c.replace(old, new)
data[idx]['content'] = c

with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("WORDS now:", len(re.findall(r'\S+', c)))
print("PK count:", c.count('web analytics tools'))
