#!/usr/bin/env python3
"""news_translate_from_cn.py — translate the CN site's daily news into EN.

Reads the CN site's data/news_YYYY-MM-DD.json files (already quality-gated by
the CN pipeline), translates title/summary/commentary via SiliconFlow
(DeepSeek), and merges into data/news_en.json keyed by CN item id.

Pipeline order (daily_growth_en.py): this script -> score -> build -> deploy.
Skips ids already present. If SILICONFLOW_API_KEY is unset, exits 0 without
touching data (news section keeps serving the last synced items).
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CN_DIR = os.path.join(BASE_DIR, '..', 'seo-site', 'data')
OUT_PATH = os.path.join(BASE_DIR, 'data', 'news_en.json')

API_KEY = os.getenv("SILICONFLOW_API_KEY", "")
API_URL = "https://api.siliconflow.cn/v1/chat/completions"
MODEL = "deepseek-ai/DeepSeek-V4-Pro"

DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 1  # default: latest CN day


def chat(prompt: str, user_msg: str) -> str:
    body = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_msg},
        ],
        "temperature": 0.3,
    }).encode('utf-8')
    req = urllib.request.Request(API_URL, data=body, headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.loads(r.read().decode('utf-8'))
    return d['choices'][0]['message']['content'].strip()


def translate_item(it: dict) -> dict | None:
    sysmsg = (
        "You are a translator for an English AI-news site. Translate the given "
        "Chinese AI-news brief into natural English JSON. Keep every fact, number, "
        "company name and URL exactly as stated — never add or invent facts. "
        "Return ONLY a JSON object with keys: title, summary, commentary. "
        "summary <= 60 words; commentary <= 80 words."
    )
    user_msg = json.dumps({
        "title": it.get('title', ''),
        "summary": it.get('summary', ''),
        "commentary": it.get('commentary', ''),
    }, ensure_ascii=False)
    try:
        raw = chat(sysmsg, user_msg)
        m = re.search(r'\{.*\}', raw, re.S)
        return json.loads(m.group()) if m else None
    except Exception as e:
        print(f"  translate failed: {e}")
        return None


def slugify(text: str, date_iso: str) -> str:
    s = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')[:60]
    return f"{date_iso}-{s}"


def main() -> int:
    if not API_KEY:
        print("[news] SILICONFLOW_API_KEY not set — skipping (existing EN news kept)")
        return 0

    try:
        en = json.load(open(OUT_PATH, encoding='utf-8'))
    except Exception:
        en = []
    have = {it['id'] for it in en}

    days = sorted(f for f in os.listdir(CN_DIR) if re.match(r'news_\d{4}-\d{2}-\d{2}\.json$', f))[-DAYS:]
    added = 0
    for fname in days:
        day = fname[5:15]
        cn = json.load(open(os.path.join(CN_DIR, fname), encoding='utf-8'))
        for it in cn:
            if it.get('id') in have:
                continue
            t = translate_item(it)
            if not t:
                continue
            en.append({
                'id': it['id'],
                'slug': slugify(t.get('title', 'ai-news'), day),
                'title': t.get('title', ''),
                'summary': t.get('summary', ''),
                'category': it.get('category', 'products'),
                'source': it.get('source', ''),
                'source_url': it.get('source_url', ''),
                'published_at': it.get('published_at') or day,
                'commentary': t.get('commentary', ''),
            })
            have.add(it['id'])
            added += 1
            print(f"  + {it['id']} {t.get('title', '')[:60]}")

    if added:
        en.sort(key=lambda x: x.get('published_at', ''), reverse=True)
        json.dump(en, open(OUT_PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"[news] added {added} items -> data/news_en.json (total {len(en)})")
    return 0


if __name__ == '__main__':
    sys.exit(main())
