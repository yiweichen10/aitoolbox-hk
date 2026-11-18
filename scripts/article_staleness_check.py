#!/usr/bin/env python3
"""Staleness audit for EN articles — READ-ONLY, prints a refresh candidate list.

Never edits content automatically: tutorials/guides are editorial pieces and an
AI rewrite would degrade them. This script only ranks candidates so a human (or
a supervised run) decides what to refresh.

Rules:
  - article age = today - article.date; >180 days => stale candidate
  - ranked by (age desc, word count asc) so the oldest, thinnest pieces surface
  - also reports tools missing pricing_details (E-E-A-T gap flagged earlier)
  - 2026-11-18: AI crawler whitelist freshness check — flags known AI bots
    missing from robots.txt so the whitelist is reviewed monthly, not yearly

Usage: python scripts/article_staleness_check.py [--days N]
Exit 0 always (audit only — not a build gate).
"""
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

ARTICLES = "data/articles_en.json"
TOOLS = "data/tools_en.json"
ROBOTS = "robots.txt"

# Reference list of known AI engine crawlers (2026-11). Any bot below that is
# NOT explicitly allowed in robots.txt is flagged for manual review against
# vendor docs (OpenAI / Anthropic / Google / Meta / Mistral / Perplexity).
KNOWN_AI_BOTS = [
    # OpenAI
    "GPTBot", "ChatGPT-User", "OAI-SearchBot",
    # Anthropic
    "ClaudeBot", "Claude-SearchBot", "Claude-User", "Claude-Runner",
    "Claude-Web", "anthropic-ai",
    # Perplexity
    "PerplexityBot", "Perplexity-User",
    # Google / Apple / Amazon
    "Google-Extended", "Applebot-Extended", "Amazonbot",
    # Meta / Mistral / Common Crawl / ByteDance
    "meta-externalagent", "meta-externalfetcher", "FacebookBot",
    "MistralAI-User", "CCBot", "Bytespider",
]


def check_robots_crawlers() -> list:
    """Return known AI bots not explicitly listed in robots.txt."""
    try:
        text = Path(ROBOTS).read_text(encoding="utf-8")
    except OSError:
        return KNOWN_AI_BOTS[:]
    listed = {ua.strip().lower() for ua in re.findall(r"(?im)^user-agent:\s*(\S+)", text)}
    return [b for b in KNOWN_AI_BOTS if b.lower() not in listed]


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

    missing_bots = check_robots_crawlers()
    if missing_bots:
        print(f"robots.txt AI crawler whitelist: {len(missing_bots)} known bot(s) NOT explicitly listed:")
        for b in missing_bots:
            print(f"  - {b}  (check vendor docs; default User-agent:* Allow covers it, but whitelist explicitly)")
    else:
        print("robots.txt AI crawler whitelist: all known AI bots explicitly listed")

    print("[NOTE] read-only audit — refresh decisions are human-owned.")
    sys.exit(0)


if __name__ == "__main__":
    main()
