#!/usr/bin/env python3
"""gen_kw_base_en.py — zero-cost keyword baseline for every tool & article.

Creates data/_kw/<slug>.json for slugs that DON'T have a file yet (never
overwrites real Serper-researched files). Baselines are template-driven:
  primary = "{name} review" (tools) / first keyword (articles)
  longtail = deterministic intent templates + the tool's real FAQ questions
              (FAQs double as PAA-style queries we can already answer)
Files carry "source": "template". When a SERPER_API_KEY becomes available,
kw_research_en.py page <slug> replaces these with SERP-validated data.

Usage: python scripts/gen_kw_base_en.py [--dry-run]
"""
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KW_DIR = os.path.join(BASE_DIR, 'data', '_kw')

TOOLS_FILE = os.path.join(BASE_DIR, 'data', 'tools_en.json')
ARTICLES_FILE = os.path.join(BASE_DIR, 'data', 'articles_en.json')

TOOL_TEMPLATES = [
    '{name} review',
    '{name} alternatives',
    '{name} pricing',
    '{name} free',
    'is {name} worth it',
    '{name} vs chatgpt',
    'how does {name} work',
    '{name} discount',
    'best {cat} tools 2026',
    '{name} tutorial',
]
ARTICLE_TEMPLATES = [
    '{kw} 2026',
    'best {kw}',
    '{kw} comparison',
    '{kw} pricing',
    '{kw} alternatives',
]


def main():
    dry = '--dry-run' in sys.argv
    tools = json.load(open(TOOLS_FILE, encoding='utf-8'))
    articles = json.load(open(ARTICLES_FILE, encoding='utf-8'))
    existing = set()
    if os.path.isdir(KW_DIR):
        existing = {f[:-5] for f in os.listdir(KW_DIR) if f.endswith('.json')}

    written = skipped = 0
    for t in tools:
        slug = t.get('slug', '')
        name = t.get('name', slug)
        cat = (t.get('category') or 'AI tool').replace('AI ', '').lower()
        if not slug or slug in existing:
            skipped += 1
            continue
        longtail = [tpl.format(name=name, cat=cat) for tpl in TOOL_TEMPLATES]
        faqs = [f['question'] for f in (t.get('faq') or []) if isinstance(f, dict) and f.get('question')]
        plan = {
            'slug': slug,
            'kind': 'tool',
            'primary_kw': f'{name} review',
            'longtail_kw': longtail + faqs,
            'paa': [],
            'serp_top10': [],
            'seeds_used': [],
            'source': 'template',
        }
        if not dry:
            with open(os.path.join(KW_DIR, f'{slug}.json'), 'w', encoding='utf-8') as f:
                json.dump(plan, f, ensure_ascii=False, indent=1)
        written += 1

    for a in articles:
        slug = a.get('slug', '')
        if not slug or slug in existing:
            skipped += 1
            continue
        kws = a.get('keywords') or ''
        if isinstance(kws, list):
            kws = ', '.join(str(k) for k in kws)
        kw0 = kws.split(',')[0].strip() if kws else (a.get('title') or slug)[:60]
        longtail = [tpl.format(kw=kw0) for tpl in ARTICLE_TEMPLATES]
        faqs = [f['question'] for f in (a.get('faq') or []) if isinstance(f, dict) and f.get('question')]
        plan = {
            'slug': slug,
            'kind': 'article',
            'primary_kw': kw0,
            'longtail_kw': longtail + faqs,
            'paa': [],
            'serp_top10': [],
            'seeds_used': [],
            'source': 'template',
        }
        if not dry:
            with open(os.path.join(KW_DIR, f'{slug}.json'), 'w', encoding='utf-8') as f:
                json.dump(plan, f, ensure_ascii=False, indent=1)
        written += 1

    total = len(tools) + len(articles)
    mode = 'DRY-RUN' if dry else 'WRITTEN'
    print(f'[{mode}] baseline kw files: {written} new, {skipped} skipped (already have data) / {total} total pages')
    if not dry and written:
        print('Note: files carry "source":"template". Run kw_research_en.py page <slug> with a SERPER_API_KEY to replace with SERP-validated data.')


if __name__ == '__main__':
    main()
