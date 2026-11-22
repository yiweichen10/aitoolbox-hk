#!/usr/bin/env python3
"""enrich_new_tools_en.py — deepen thin tool-review content via DeepSeek.

Target slugs: the 2026-11-21 AI-detector batch (originality-ai, zerogpt,
copyleaks, nano-banana, hailuo-ai). Their reviews are ~3k chars vs the 9k
site veterans, so Depth factor drags scores to 2.5-2.7.

Facts are LOCKED: the prompt carries the tool's existing JSON (content, faq,
features, pros/cons, pricing_details) as the only permitted factual source.
The model may restructure, deepen workflows/decision-guides and comparisons
in general terms, but MUST NOT invent prices, dates, version numbers or new
features. Output is validated (no new '$'+digit figures) before saving.

Writes data/_drafts_en/<slug>.content.md, then assembles upsert JSON
(_enrich_upsert_<slug>.json) for upsert_tool_en.py. Nothing writes
tools_en.json directly (governance rule).
"""
import json
import os
import re
import urllib.request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CN_ENV = os.path.join(os.path.dirname(BASE_DIR), 'seo-site', '.env')
TOOLS_FILE = os.path.join(BASE_DIR, 'data', 'tools_en.json')
DRAFT_DIR = os.path.join(BASE_DIR, 'data', '_drafts_en')

TARGET_SLUGS = ['originality-ai', 'zerogpt', 'copyleaks', 'nano-banana', 'hailuo-ai']
TARGET_CHARS = 6500


def load_env(path):
    cfg = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                cfg[k.strip()] = v.strip()
    return cfg


def call_deepseek(cfg, prompt):
    body = json.dumps({
        'model': cfg.get('DEEPSEEK_MODEL', 'deepseek-chat'),
        'messages': [
            {'role': 'system', 'content': 'You are the lead editor of an independent AI tool review site. Write in a first-person, hands-on, no-fluff editorial voice. Markdown with ## section headings. Never invent facts, prices, dates or features that are not in the provided source material.'},
            {'role': 'user', 'content': prompt},
        ],
        'temperature': 0.6,
        'max_tokens': 8000,
    }).encode('utf-8')
    req = urllib.request.Request(
        cfg.get('DEEPSEEK_BASE_URL', 'https://api.deepseek.com/v1') + '/chat/completions',
        data=body,
        headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + cfg['DEEPSEEK_API_KEY']},
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        d = json.loads(r.read().decode('utf-8'))
    return d['choices'][0]['message']['content']


def validate(out_text, src_facts):
    """Reject output that introduces $ figures not present in source facts."""
    allowed = set(re.findall(r'\$[\d.,]+', src_facts))
    new_money = [m for m in re.findall(r'\$[\d.,]+', out_text) if m not in allowed]
    return new_money


def build_prompt(t):
    src = json.dumps({
        'name': t.get('name'),
        'existing_review_markdown': t.get('content', ''),
        'features': t.get('features'),
        'pros': t.get('pros'),
        'cons': t.get('cons'),
        'faq': t.get('faq'),
        'pricing_details': t.get('pricing_details'),
        'price_label': t.get('price'),
        'category': t.get('category'),
        'related_tools': t.get('related'),
    }, ensure_ascii=False, indent=1)
    return f"""Expand the review below to approximately {TARGET_CHARS} characters (currently too thin).

STRICT RULES:
1. FACTS ARE LOCKED. Use ONLY the facts in the source JSON. Do NOT invent prices, dollar figures, dates, version numbers, benchmark scores, or new features. You may elaborate on existing facts and discuss category-level realities in general terms.
2. Keep the existing first-person editorial voice and all existing section ideas; deepen them. Add these sections: a realistic hands-on workflow walkthrough, "Who should use this / who shouldn't", a practical decision guide versus the related tools (by positioning, not by invented specs), and a "mistakes people make" section.
3. Keep every existing internal link exactly as-is (format /tools/<slug>/). You may reuse only links that already appear in the source.
4. Output ONLY the markdown review body, no preamble, no code fences.
5. Do not introduce any '$' figure that is not already in the source.

SOURCE JSON:
{src}"""


def main():
    cfg = load_env(CN_ENV)
    assert cfg.get('DEEPSEEK_API_KEY'), 'DEEPSEEK_API_KEY missing in CN .env'
    os.makedirs(DRAFT_DIR, exist_ok=True)

    tools = json.load(open(TOOLS_FILE, encoding='utf-8'))
    by_slug = {t['slug']: t for t in tools}

    for slug in TARGET_SLUGS:
        t = by_slug[slug]
        out_path = os.path.join(DRAFT_DIR, f'{slug}.content.md')
        if os.path.exists(out_path) and os.path.getsize(out_path) > TARGET_CHARS * 0.8:
            print(f'[skip] {slug} — draft already exists ({os.path.getsize(out_path)} chars)')
            continue
        print(f'[call] {slug} ...')
        try:
            text = call_deepseek(cfg, build_prompt(t))
        except Exception as e:
            print(f'  [FAIL] {slug}: {e}')
            continue
        text = text.strip()
        if text.startswith('```'):
            text = re.sub(r'^```(?:markdown)?\n?', '', text).rstrip('```').strip()
        bad_money = validate(text, json.dumps(t, ensure_ascii=False))
        if bad_money:
            print(f'  [REJECT] {slug}: invented dollar figures {bad_money[:5]} — not saved')
            continue
        if len(text) < TARGET_CHARS * 0.6:
            print(f'  [WARN] {slug}: only {len(text)} chars, saving anyway')
        with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
        # assemble upsert payload (content only — everything else unchanged)
        upsert = {'slug': slug, 'content': text}
        up_path = os.path.join(DRAFT_DIR, f'_enrich_upsert_{slug}.json')
        with open(up_path, 'w', encoding='utf-8') as f:
            json.dump(upsert, f, ensure_ascii=False, indent=1)
        print(f'  [OK] {slug}: {len(text)} chars -> {up_path}')


if __name__ == '__main__':
    main()
