#!/usr/bin/env python3
"""Staleness audit for EN articles — READ-ONLY, prints a refresh candidate list.

Never edits content automatically: tutorials/guides are editorial pieces and an
AI rewrite would degrade them. This script only ranks candidates so a human (or
a supervised run) decides what to refresh.

Rules:
  - article age = today - article.date; >180 days => stale candidate
  - ranked by (age desc, word count asc) so the oldest, thinnest pieces surface
  - also reports tools missing pricing_details (E-E-A-T gap flagged earlier)

Usage: python scripts/article_staleness_check.py [--days N]
Exit 0 always (audit only — not a build gate).
"""
import json
import sys
from datetime import date, datetime

ARTICLES = "data/articles_en.json"
TOOLS = "data/tools_en.json"


def age_days(d: str) -> int:
    try:
        return (date.today() - datetime.strptime(d[:10], "%Y-%m-%d").date()).days
    except Exception:
        return -1


def main():
    threshold = 180
    if "--days" in sys.argv:
        threshold = int(sys.argv[sys.argv.index("--days") + 1])
    arts = json.load(open(ARTICLES, encoding="utf-8"))
    tools = json.load(open(TOOLS, encoding="utf-8"))
    today = date.today().isoformat()

    stale = []
    for a in arts:
        age = age_days(a.get("date", ""))
        if age < 0 or age <= threshold:
            continue
        words = len(a.get("content", "").split())
        stale.append((age, words, a["title"][:64], a["slug"], a.get("date", "")))
    stale.sort(reverse=True)

    no_pd = [t["slug"] for t in tools if not (t.get("pricing_details") or "").strip()]

    print(f"[STALENESS AUDIT] {today} | threshold: >{threshold} days")
    print(f"articles: {len(arts)} total | stale candidates: {len(stale)}")
    for age, words, title, slug, d in stale[:20]:
        print(f"  {age:4d}d {words:5d}w  {d}  {title}")
        print(f"        /articles/{slug}/")
    if len(stale) > 20:
        print(f"  ... and {len(stale) - 20} more")
    print(f"tools missing pricing_details: {len(no_pd)}/{len(tools)}")
    print("[NOTE] read-only audit — refresh decisions are human-owned.")
    sys.exit(0)


if __name__ == "__main__":
    main()
