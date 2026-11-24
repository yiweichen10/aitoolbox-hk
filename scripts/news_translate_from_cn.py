#!/usr/bin/env python3
"""news_translate_from_cn.py — translate the CN site's daily news into EN.

Reads the CN site's data/news_YYYY-MM-DD.json files (already quality-gated by
the CN pipeline), translates title/summary/commentary via DeepSeek, and merges
into data/news_en.json keyed by CN item id.

Pipeline order (daily_growth_en.py): this script -> score -> build -> deploy.
Skips ids already present. Unlike the old SiliconFlow version, a missing key or
a failed translation is a hard error (exit 1): silently skipping used to leave
the EN news section stale without anybody noticing.

Usage:
  python scripts/news_translate_from_cn.py [days]   # default: latest 3 CN days
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


def _read_env(path: str) -> dict:
    env = {}
    if not os.path.isfile(path):
        return env
    for line in open(path, encoding='utf-8'):
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


# Config precedence: process env > EN .env > CN .env (shared data is allowed;
# the key lives only in the CN .env, which is the one site that has one).
_cfg = {}
for _p in (os.path.join(os.path.dirname(CN_DIR), '.env'),
           os.path.join(BASE_DIR, '.env')):
    _cfg.update(_read_env(_p))

API_KEY = os.getenv('DEEPSEEK_API_KEY') or _cfg.get('DEEPSEEK_API_KEY', '')
API_BASE = (os.getenv('DEEPSEEK_BASE_URL') or _cfg.get('DEEPSEEK_BASE_URL')
            or 'https://api.deepseek.com/v1').rstrip('/')
MODEL = os.getenv('DEEPSEEK_MODEL') or _cfg.get('DEEPSEEK_MODEL') or 'deepseek-v4-flash'
API_URL = API_BASE + '/chat/completions'

DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 3


def chat(prompt: str, user_msg: str) -> str:
    body = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_msg},
        ],
        "temperature": 0.3,
        "max_tokens": 1500,
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
    last = ''
    for attempt in range(2):
        try:
            raw = chat(sysmsg, user_msg)
            m = re.search(r'\{.*\}', raw, re.S)
            if m:
                return json.loads(m.group())
            last = 'no JSON object in response'
        except Exception as e:
            last = f'{type(e).__name__}: {e}'
        if attempt == 0:
            print(f"  retry {it.get('id', '?')}: {last[:160]}", flush=True)
    print(f"  ERROR translate {it.get('id', '?')}: {last[:300]}", flush=True)
    return None


def slugify(text: str, date_iso: str) -> str:
    s = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')[:60]
    return f"{date_iso}-{s}"


def main() -> int:
    if not API_KEY:
        print("[news][ERROR] DEEPSEEK_API_KEY not found in env / EN .env / CN .env "
              "— EN news sync aborted (refusing to silently serve stale news)")
        return 1

    try:
        en = json.load(open(OUT_PATH, encoding='utf-8'))
    except Exception:
        en = []
    have = {it['id'] for it in en}

    files = sorted(f for f in os.listdir(CN_DIR)
                   if re.match(r'news_\d{4}-\d{2}-\d{2}\.json$', f))
    days = files[-DAYS:]
    if not days:
        print("[news][ERROR] no CN news_YYYY-MM-DD.json files found")
        return 1

    added = 0
    errors = 0
    for fname in days:
        day = fname[5:15]
        cn = json.load(open(os.path.join(CN_DIR, fname), encoding='utf-8'))
        for it in cn:
            if it.get('id') in have:
                continue
            t = translate_item(it)
            if not t:
                errors += 1
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
            print(f"  + {it['id']} {t.get('title', '')[:60]}", flush=True)

    if errors:
        print(f"[news][ERROR] {errors} item(s) failed to translate — "
              "no partial data written; fix and rerun")
        return 1

    if added:
        en.sort(key=lambda x: x.get('published_at', ''), reverse=True)
        with open(OUT_PATH, 'w', encoding='utf-8') as f:
            json.dump(en, f, ensure_ascii=False, indent=1)
    print(f"[news] added {added} items -> data/news_en.json (total {len(en)}); "
          f"scanned CN days: {days[0]}..{days[-1]}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
