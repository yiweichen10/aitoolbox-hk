#!/usr/bin/env python3
"""Analyze tools_en.json price labels for the AI Tool Pricing Index.

Extraction rules (conservative, no invented numbers):
- free tier: the label advertises 'free' in some form (incl. limited/open-source/free-trial).
- entry monthly price: the LOWEST explicitly published USD per-month number ($N/mo),
  taken only from labels that state a USD monthly figure. Excludes per-token,
  per-sale, percentage fees, one-time/lifetime, and non-USD (EUR/GBP) figures.
- unpriced: no extractable USD monthly figure (API/contact/usage-based/one-time/free-only).
Prints a full audit table plus aggregate stats by category.
"""
import json
import os
import re
import statistics
from collections import defaultdict
from datetime import date

DATA = "data/tools_en.json"
SNAPSHOT = "data/_pricing_index_snapshot.json"
HISTORY = "data/_pricing_index_history.json"

# $20/mo, $19.99/mo, $9.95 /mo -> collect all explicit USD monthly figures
RE_MONTHLY = re.compile(r"\$\s*(\d+(?:\.\d+)?)\s*/\s*mo\b", re.I)
# price RANGE for a monthly plan: $29 - $249/mo, $0-$330/mo -> take the LOWER bound
RE_RANGE = re.compile(r"\$\s*(\d+(?:\.\d+)?)\s*[-–]\s*\$\s*\d+(?:\.\d+)?\s*/\s*mo\b", re.I)
# annual-billing equivalent in parentheses: "(annual $4.17/mo)", "billed yearly: $15/mo"
RE_ANNUAL = re.compile(r"\((?:annual|billed yearly)[^)]*\)|billed yearly:\s*\$\d+(?:\.\d+)?/mo", re.I)
RE_TOKEN = re.compile(r"per\s*(?:1k|m\b|million|token)|\$\s*\d+(?:\.\d+)?\s*/\s*(?:m\b|million|1k)\b", re.I)
RE_FREE = re.compile(r"\bfree\b", re.I)
RE_ONETIME = re.compile(r"one.?time|lifetime", re.I)
RE_NONUSD = re.compile(r"\b(?:EUR|GBP|€|£)\s*\d|\d+\s*(?:EUR|GBP)", re.I)


def extract(t):
    price = t.get("price", "") or ""
    has_free = bool(RE_FREE.search(price))
    # remove annual-equivalent figures so they are not mistaken for the monthly entry price
    cleaned = RE_ANNUAL.sub("", price)
    nums = []
    # handle price ranges FIRST, then strip them so the upper bound is not
    # re-captured as a single-point price by RE_MONTHLY.
    # "$29-$249/mo" -> lower bound 29 is the entry price;
    # "$0-$330/mo"  -> starts at free, no explicit paid entry -> contributes nothing.
    for m in list(RE_RANGE.finditer(cleaned)):
        low = float(m.group(1))
        if low >= 1:
            nums.append(low)
    cleaned = RE_RANGE.sub(" ", cleaned)
    # single-point monthly prices; drop per-seat / per-user / per-builder figures
    for m in RE_MONTHLY.finditer(cleaned):
        tail = cleaned[m.end():m.end()+18]
        if re.match(r"\s*/\s*(?:seat|user|builder)\b", tail, re.I):
            continue
        nums.append(float(m.group(1)))
    nums = [n for n in nums if 1 <= n <= 1000]
    entry = min(nums) if nums else None
    return {
        "name": t["name"],
        "slug": t["slug"],
        "category": t.get("category", "Other"),
        "price": price,
        "free": has_free,
        "entry": entry,
        "onetime": bool(RE_ONETIME.search(price)),
        "nonusd": bool(RE_NONUSD.search(price)),
        "token": bool(RE_TOKEN.search(price)),
    }


def main():
    tools = json.load(open(DATA, encoding="utf-8"))
    rows = [extract(t) for t in tools]

    priced = [r for r in rows if r["entry"] is not None]
    free = [r for r in rows if r["free"]]
    prices = [r["entry"] for r in priced]

    print("=" * 60)
    print(f"TOOLS: {len(rows)}")
    print(f"FREE-TIER advertised: {len(free)} ({len(free)/len(rows)*100:.1f}%)")
    print(f"PUBLISHED USD MONTHLY price: {len(priced)} ({len(priced)/len(rows)*100:.1f}%)")
    print(f"NO USD MONTHLY price: {len(rows)-len(priced)}")
    if prices:
        print(f"Mean entry price: ${statistics.mean(prices):.2f}")
        print(f"Median entry price: ${statistics.median(prices):.2f}")
        print(f"Min / Max: ${min(prices):.0f} / ${max(prices):.0f}")
    print("=" * 60)

    print("\n### FULL AUDIT TABLE (name | free | entry | price label)")
    for r in rows:
        print(f"{r['name'][:28]:28} | {'Y' if r['free'] else '-'} | "
              f"{('$'+format(r['entry'],'g')) if r['entry'] is not None else '  --  ':>8} | {r['price']}")

    print("\n### BY CATEGORY (>=3 priced tools, sorted by median)")
    bycat = defaultdict(list)
    for r in rows:
        bycat[r["category"]].append(r)
    cat_stats = []
    for cat, rs in bycat.items():
        ps = [r["entry"] for r in rs if r["entry"] is not None]
        if len(ps) >= 3:
            cat_stats.append((cat, len(rs), len(ps), statistics.median(ps), statistics.mean(ps)))
    for cat, total, n, med, avg in sorted(cat_stats, key=lambda x: -x[3]):
        print(f"{cat:24} tools={total:3} priced={n:3} median=${med:6.2f} mean=${avg:6.2f}")

    # export machine-readable snapshot for article generation
    out = {
        "generated_date": date.today().isoformat(),
        "generated_from": DATA,
        "total_tools": len(rows),
        "free_tier_count": len(free),
        "priced_count": len(priced),
        "mean_entry": round(statistics.mean(prices), 2) if prices else None,
        "median_entry": round(statistics.median(prices), 2) if prices else None,
        "by_category": [
            {"category": c, "tools": t, "priced": n, "median": round(m, 2), "mean": round(a, 2)}
            for c, t, n, m, a in sorted(cat_stats, key=lambda x: -x[3])
        ],
        "rows": rows,
    }

    # Archive the PREVIOUS snapshot's headline figures before overwriting.
    # This is the only durable record for month-over-month comparison.
    hist = []
    if os.path.exists(HISTORY):
        try:
            hist = json.load(open(HISTORY, encoding="utf-8"))
        except Exception:
            hist = []
    if os.path.exists(SNAPSHOT):
        try:
            prev = json.load(open(SNAPSHOT, encoding="utf-8"))
            prev_date = prev.get("generated_date")
            if prev_date and not any(h.get("date") == prev_date for h in hist):
                hist.append({
                    "date": prev_date,
                    "total_tools": prev["total_tools"],
                    "free_tier_count": prev["free_tier_count"],
                    "priced_count": prev["priced_count"],
                    "mean_entry": prev["mean_entry"],
                    "median_entry": prev["median_entry"],
                })
        except Exception:
            pass
    hist = sorted(hist, key=lambda h: h["date"])[-24:]  # keep up to 2 years
    with open(HISTORY, "w", encoding="utf-8") as f:
        json.dump(hist, f, ensure_ascii=False, indent=2)
    print(f"[OK] history -> {HISTORY} ({len(hist)} snapshots)")

    with open(SNAPSHOT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"[OK] snapshot -> {SNAPSHOT}")


if __name__ == "__main__":
    main()
