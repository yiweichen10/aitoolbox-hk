#!/usr/bin/env python3
"""Compute the transparent 4-factor editorial score for every tool.

Why: the displayed star "EDITOR SCORE" used to be an opinion assigned when a
tool was added — dozens of tools crowded at 4.4-4.8 with unearned 5.0s. Since
2026-11-20 the star score is DERIVED from the published rubric below, and the
same rubric drives every ranking on the site ("ranked by score" is literal).

Rubric (each factor 0-10, weighted, total 0-100):

  1. Depth          35%  review body length, log-normalized
                          (1,800 chars = 1.0, 18,000 chars = 10.0)
  2. Completeness   25%  pros/cons specificity, features, FAQ, pricing research
  3. Popularity     25%  visits signal, log-normalized (42K=1.0, 4M=10.0),
                          plus a small log-scaled bonus from verified user
                          likes (fetched from the live /api/likes endpoint;
                          capped at +2.0 so it informs but cannot dominate)
  4. Freshness      15%  best available date (last_verified > aeo_geo_updated >
                          created_date). Missing date = neutral 5.0, never a
                          silent penalty for missing metadata.

Displayed star: rating = round(1 + total/100 * 4, 1)  ->  1.0..5.0
  (total 90 -> 4.6, total 68 -> 3.7, total 44 -> 2.8)
The rating is written back into tools_en.json so every consumer (cards,
schema, alternatives, vs pages) stays consistent. Editor opinion is expressed
through badges (Editor's Choice / Pick), not through inflated stars.

Output: data/scores_en.json
  {"generated_at", "rubric", "likes_source", "scores": {slug: {...}}}

Pipeline order: score_tools_en.py -> build_en.py -> deploy_cf_en.py.
"""
from __future__ import annotations

import json
import math
import os
import re
import shutil
import urllib.request
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_PATH = os.path.join(BASE_DIR, 'data', 'tools_en.json')
SCORES_PATH = os.path.join(BASE_DIR, 'data', 'scores_en.json')

SITE = 'https://www.aitoolbox.hk'
LIKES_URL = SITE + '/api/likes'

WEIGHTS = {
    'depth': 0.35,
    'completeness': 0.25,
    'popularity': 0.25,
    'freshness': 0.15,
}

# (chars at score 1.0, chars at score 10.0) — log scale
DEPTH_RANGE = (1800, 18000)
# (visits at score 1.0, visits at score 10.0) — log scale, parsed from "42K"/"1.2M"
POPULARITY_RANGE = (42_000, 4_000_000)
# likes bonus: min(2.0, log10(1+likes) * 2) — 10 likes ≈ +2.0 is the cap
LIKES_BONUS_CAP = 2.0

DATE_RE = re.compile(r'^(20\d{2}-\d{2}-\d{2})')


def _log_norm(value: float, lo: float, hi: float) -> float:
    """Map value onto 1.0..10.0 on a log scale, clamped."""
    value = max(value, 1)
    lo = max(lo, 1)
    hi = max(hi, lo * 2)
    t = (math.log(value) - math.log(lo)) / (math.log(hi) - math.log(lo))
    return round(1.0 + 9.0 * min(max(t, 0.0), 1.0), 2)


def parse_visits_num(visits_str) -> float:
    s = str(visits_str or '').upper()
    m = re.search(r'(\d+(?:\.\d+)?)\s*([KM]?)', s)
    if not m:
        return 0.0
    num = float(m.group(1))
    mult = {'K': 1_000, 'M': 1_000_000}.get(m.group(2), 1)
    return num * mult


def _best_date(tool: dict) -> str | None:
    for key in ('last_verified', 'aeo_geo_updated', 'created_date'):
        v = tool.get(key)
        if isinstance(v, str):
            m = DATE_RE.match(v.strip())
            if m:
                return m.group(1)
    return None


def fetch_likes() -> dict:
    """Pull verified like counts from the live site. Best-effort: on any
    failure (first deploy, network) return {} and score without the bonus."""
    try:
        # CF bot protection rejects the default Python UA with 403.
        req = urllib.request.Request(LIKES_URL, headers={
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (compatible; aitoolbox-pipeline/1.0)',
        })
        with urllib.request.urlopen(req, timeout=8) as r:
            d = json.loads(r.read().decode('utf-8'))
        likes = d.get('likes') if isinstance(d, dict) else None
        return likes if isinstance(likes, dict) else {}
    except Exception:
        return {}


def score_depth(tool: dict) -> float:
    return _log_norm(len(str(tool.get('content', '') or '')), *DEPTH_RANGE)


def score_completeness(tool: dict) -> float:
    pts = 0.0
    pros = tool.get('pros') or []
    cons = tool.get('cons') or []
    pts += min(len(pros), 5) / 5 * 3.0
    pts += min(len(cons), 5) / 5 * 3.0
    pts += min(len(tool.get('features') or []), 8) / 8 * 1.5
    pts += min(len(tool.get('faq') or []), 4) / 4 * 1.5
    pts += min(len(str(tool.get('pricing_details') or '')) / 400, 1.0) * 1.0
    return round(min(pts, 10.0), 2)


def score_popularity(tool: dict, likes: int) -> float:
    v = parse_visits_num(tool.get('visits'))
    base = _log_norm(v, *POPULARITY_RANGE) if v > 0 else 1.0
    bonus = min(LIKES_BONUS_CAP, math.log10(1 + max(int(likes), 0)) * 2.0)
    return round(min(base + bonus, 10.0), 2)


def score_freshness(tool: dict, today: datetime) -> float:
    date_str = _best_date(tool)
    if not date_str:
        return 5.0  # neutral — do not punish missing metadata
    try:
        days = (today - datetime.strptime(date_str, '%Y-%m-%d')).days
    except ValueError:
        return 5.0
    if days <= 14:
        return 10.0
    if days >= 365:
        return 1.0
    # linear decay 10 -> 1 between 14 and 365 days
    return round(10.0 - 9.0 * (days - 14) / (365 - 14), 2)


def star_from_total(total: float) -> str:
    return f"{round(1.0 + total / 100.0 * 4.0, 1):.1f}"


def main() -> None:
    with open(TOOLS_PATH, encoding='utf-8') as f:
        tools = json.load(f)
    today = datetime.now()
    today_iso = today.strftime('%Y-%m-%d')

    likes_map = fetch_likes()
    if likes_map:
        n_likes = sum(int(v) for v in likes_map.values() if str(v).isdigit())
        print(f"[OK] likes fetched: {len(likes_map)} tools, {n_likes} total")
    else:
        print("[WARN] no likes available (first deploy or network) — scoring without like bonus")

    scores = {}
    rating_updates = {}
    for t in tools:
        slug = t.get('slug', '')
        if not slug:
            continue
        likes = int(likes_map.get(slug, 0) or 0)
        f_depth = score_depth(t)
        f_compl = score_completeness(t)
        f_pop = score_popularity(t, likes)
        f_fresh = score_freshness(t, today)
        total = round(10 * (
            f_depth * WEIGHTS['depth']
            + f_compl * WEIGHTS['completeness']
            + f_pop * WEIGHTS['popularity']
            + f_fresh * WEIGHTS['freshness']
        ), 1)
        scores[slug] = {
            'depth': f_depth,
            'completeness': f_compl,
            'popularity': f_pop,
            'likes': likes,
            'freshness': f_fresh,
            'total': total,
        }
        rating_updates[slug] = star_from_total(total)

    # Write derived stars back so cards/schema/vs/alternatives stay consistent.
    changed = 0
    for t in tools:
        slug = t.get('slug', '')
        new_star = rating_updates.get(slug)
        if new_star and str(t.get('rating', '')).strip() != new_star:
            t['rating'] = new_star
            changed += 1
    if changed:
        shutil.copy2(TOOLS_PATH, TOOLS_PATH + '.prescore.bak')
        with open(TOOLS_PATH, 'w', encoding='utf-8') as f:
            json.dump(tools, f, ensure_ascii=False, indent=1)
        print(f"[OK] star ratings rewritten from rubric: {changed}/{len(tools)} tools updated")
    else:
        print('[OK] star ratings already in sync with rubric')

    out = {
        'generated_at': today_iso,
        'rubric': {
            'description': 'Transparent 4-factor editorial ranking score (0-100); displayed star = 1 + total/100*4',
            'weights': WEIGHTS,
            'depth_range_chars': DEPTH_RANGE,
            'popularity_range_visits': POPULARITY_RANGE,
            'likes_bonus': f'min({LIKES_BONUS_CAP}, log10(1+likes)*2) from verified /api/likes',
            'freshness_rule': '14d=10.0, linear to 1.0 at 365d; missing date = neutral 5.0',
        },
        'likes_source': LIKES_URL if likes_map else 'unavailable',
        'scores': scores,
    }
    with open(SCORES_PATH, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    ranked = sorted(scores.items(), key=lambda kv: kv[1]['total'], reverse=True)
    print(f'[OK] scored {len(scores)} tools -> data/scores_en.json')
    print('Top 5:')
    for slug, s in ranked[:5]:
        print(f"  {s['total']:5.1f}  {star_from_total(s['total'])}/5  {slug}")
    lows = sorted(scores.items(), key=lambda kv: kv[1]['total'])[:3]
    print('Bottom 3:')
    for slug, s in lows:
        print(f"  {s['total']:5.1f}  {star_from_total(s['total'])}/5  {slug}")


if __name__ == '__main__':
    main()
