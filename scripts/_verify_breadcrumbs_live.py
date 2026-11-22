#!/usr/bin/env python3
"""Verify all fixed article pages live: breadcrumb JSON-LD must have no name-only non-last items."""
import json
import re
import sys
import urllib.request

BASE = "https://www.aitoolbox.hk/articles/"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"}


def check(slug: str) -> str:
    url = BASE + slug + "/"
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=25) as r:
            html = r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return f"FETCH_FAIL {slug} ({e})"
    bad = False
    has_breadcrumb = False
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        raw = m.group(1)
        if "BreadcrumbList" not in raw:
            continue
        has_breadcrumb = True
        try:
            data = json.loads(raw)
        except Exception:
            return f"JSON_ERROR {slug}"
        els = data.get("itemListElement", [])
        for li in els[:-1]:
            if "item" not in li:
                bad = True
    if not has_breadcrumb:
        return f"NO_SCHEMA {slug}"
    return f"BAD {slug}" if bad else "OK"


def main() -> None:
    slugs = [s.strip() for s in open(sys.argv[1], encoding="utf-8") if s.strip()]
    ok = bad = fail = 0
    fails = []
    for i, slug in enumerate(slugs, 1):
        r = check(slug)
        if r == "OK":
            ok += 1
        elif r.startswith("FETCH_FAIL"):
            fail += 1
            fails.append(r)
        else:
            bad += 1
            print(r)
        if i % 20 == 0:
            print(f"... {i}/{len(slugs)} checked", flush=True)
    print(f"== RESULT: ok={ok} bad={bad} fetch_fail={fail} / {len(slugs)} ==")
    for f in fails:
        print(f)


if __name__ == "__main__":
    main()
