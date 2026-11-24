#!/usr/bin/env python3
"""news_translate_from_cn.py — agent-driven EN news sync, no paid API.

The translation is done by the WorkBuddy agent itself (zero API cost). This
script only handles the deterministic parts:

  python scripts/news_translate_from_cn.py --prepare [days]
      Scan the CN site's data/news_YYYY-MM-DD.json files, skip ids already in
      data/news_en.json, and write data/_news_pending_en.json.

  (agent step, in the conversation)
      Read data/_news_pending_en.json, translate title/summary/commentary into
      natural English, and write data/_news_translated_en.json as a JSON array
      of {"id", "title", "summary", "commentary"} objects. Keep every fact,
      number, company name and URL exactly as stated; summary <= 60 words,
      commentary <= 80 words. Never invent facts.

  python scripts/news_translate_from_cn.py --merge
      Validate the agent output against the pending batch (exact id match,
      non-empty fields, length limits), then merge into data/news_en.json.
      Both work files are archived under data/_news_agent_archive/ on success.

  python scripts/news_translate_from_cn.py --check
      Exit 1 if a pending batch or a leftover translated file exists, i.e. the
      agent step has not been completed. Used by daily_growth_en.py so a stale
      news section can never pass unnoticed.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CN_DIR = os.path.join(BASE_DIR, '..', 'seo-site', 'data')
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUT_PATH = os.path.join(DATA_DIR, 'news_en.json')
PENDING_PATH = os.path.join(DATA_DIR, '_news_pending_en.json')
TRANSLATED_PATH = os.path.join(DATA_DIR, '_news_translated_en.json')
ARCHIVE_DIR = os.path.join(DATA_DIR, '_news_agent_archive')

MAX_SUMMARY_WORDS = 60
MAX_COMMENTARY_WORDS = 80


def _load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def _write_json(path, obj):
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def _cn_files(days: int):
    files = sorted(f for f in os.listdir(CN_DIR)
                   if re.match(r'news_\d{4}-\d{2}-\d{2}\.json$', f))
    return files[-days:] if days > 0 else []


def cmd_prepare(days: int) -> int:
    if os.path.exists(TRANSLATED_PATH):
        print(f"[news][ERROR] leftover {os.path.basename(TRANSLATED_PATH)} — "
              "merge it first (or remove it deliberately) before preparing a new batch")
        return 1

    en = _load_json(OUT_PATH) if os.path.exists(OUT_PATH) else []
    have = {it['id'] for it in en}
    files = _cn_files(days)
    if not files:
        print("[news][ERROR] no CN news_YYYY-MM-DD.json files found")
        return 1

    items = []
    for fname in files:
        day = fname[5:15]
        for it in _load_json(os.path.join(CN_DIR, fname)):
            if it.get('id') in have:
                continue
            items.append({
                'id': it['id'],
                'day': day,
                'title': it.get('title', ''),
                'summary': it.get('summary', ''),
                'commentary': it.get('commentary', ''),
                'category': it.get('category', 'products'),
                'source': it.get('source', ''),
                'source_url': it.get('source_url', ''),
                'published_at': it.get('published_at') or day,
            })

    if not items:
        if os.path.exists(PENDING_PATH):
            os.remove(PENDING_PATH)
        print(f"[news] no pending items (scanned {files[0][5:15]}..{files[-1][5:15]}); "
              f"EN news already has {len(en)} items")
        return 0

    _write_json(PENDING_PATH, {
        'generated_at': datetime.now().astimezone().isoformat(timespec='seconds'),
        'cn_days': [f[5:15] for f in files],
        'count': len(items),
        'items': items,
    })
    print(f"[news] PENDING {len(items)} item(s) -> {PENDING_PATH}")
    print("[news] NEXT: agent translates title/summary/commentary into English, "
          f"writes {TRANSLATED_PATH}, then runs --merge")
    for it in items:
        print(f"  - {it['id']} {it['title'][:56]}")
    return 0


def cmd_merge() -> int:
    if not os.path.exists(PENDING_PATH):
        print(f"[news][ERROR] no pending batch at {PENDING_PATH}; run --prepare first")
        return 1
    if not os.path.exists(TRANSLATED_PATH):
        print(f"[news][ERROR] no agent output at {TRANSLATED_PATH}; "
              "agent must translate the pending batch first")
        return 1

    batch = _load_json(PENDING_PATH)
    pending = batch['items']
    translated = _load_json(TRANSLATED_PATH)
    if not isinstance(translated, list):
        print("[news][ERROR] translated file must be a JSON array")
        return 1

    by_id = {}
    for i, t in enumerate(translated):
        if not isinstance(t, dict) or not t.get('id'):
            print(f"[news][ERROR] translated[{i}] missing id")
            return 1
        if t['id'] in by_id:
            print(f"[news][ERROR] duplicate translated id {t['id']}")
            return 1
        by_id[t['id']] = t

    expected = {it['id'] for it in pending}
    missing = sorted(expected - set(by_id))
    extra = sorted(set(by_id) - expected)
    if missing or extra:
        print(f"[news][ERROR] id mismatch — missing={missing} unexpected={extra}")
        return 1

    errors = []
    for it in pending:
        t = by_id[it['id']]
        for k in ('title', 'summary', 'commentary'):
            v = t.get(k)
            if not isinstance(v, str) or not v.strip():
                errors.append(f"{it['id']}: {k} is empty or not a string")
        for k, limit in (('summary', MAX_SUMMARY_WORDS),
                         ('commentary', MAX_COMMENTARY_WORDS)):
            v = t.get(k)
            if isinstance(v, str) and len(v.split()) > limit:
                errors.append(f"{it['id']}: {k} has {len(v.split())} words (limit {limit})")
    if errors:
        print("[news][ERROR] agent output failed validation:")
        for e in errors:
            print("  " + e)
        print("[news] fix the translated file and rerun --merge (nothing was written)")
        return 1

    en = _load_json(OUT_PATH) if os.path.exists(OUT_PATH) else []
    have = {it['id'] for it in en}
    added = 0
    for it in pending:
        if it['id'] in have:
            continue
        t = by_id[it['id']]
        title = t['title'].strip()
        s = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:60]
        en.append({
            'id': it['id'],
            'slug': f"{it['day']}-{s}",
            'title': title,
            'summary': t['summary'].strip(),
            'category': it['category'],
            'source': it['source'],
            'source_url': it['source_url'],
            'published_at': it['published_at'],
            'commentary': t['commentary'].strip(),
        })
        have.add(it['id'])
        added += 1
        print(f"  + {it['id']} {title[:60]}")

    en.sort(key=lambda x: x.get('published_at', ''), reverse=True)
    _write_json(OUT_PATH, en)

    stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    dest = os.path.join(ARCHIVE_DIR, stamp)
    os.makedirs(dest, exist_ok=True)
    shutil.move(PENDING_PATH, os.path.join(dest, os.path.basename(PENDING_PATH)))
    shutil.move(TRANSLATED_PATH, os.path.join(dest, os.path.basename(TRANSLATED_PATH)))

    print(f"[news] merged {added} item(s) -> data/news_en.json (total {len(en)}); "
          f"batch archived to {os.path.relpath(dest, BASE_DIR)}")
    return 0


def cmd_check() -> int:
    problems = []
    if os.path.exists(PENDING_PATH):
        n = _load_json(PENDING_PATH).get('count', '?')
        problems.append(f"pending batch not translated ({n} item(s))")
    if os.path.exists(TRANSLATED_PATH):
        problems.append("translated file not merged")
    if problems:
        print("[news][ERROR] " + "; ".join(problems))
        print("[news] agent translation must be finished before build/deploy")
        return 1
    print("[news] sync clean — no pending agent translation")
    return 0


def main() -> int:
    args = sys.argv[1:]
    # Back-compat: a bare number used to mean "days" (the API mode is gone).
    if args and args[0].isdigit():
        args = ['--prepare'] + args
    mode = args[0] if args else '--check'
    if mode == '--prepare':
        days = int(args[1]) if len(args) > 1 else 3
        return cmd_prepare(days)
    if mode == '--merge':
        return cmd_merge()
    if mode == '--check':
        return cmd_check()
    print(f"[news][ERROR] unknown mode {mode!r}; use --prepare [days] / --merge / --check")
    return 2


if __name__ == '__main__':
    sys.exit(main())
