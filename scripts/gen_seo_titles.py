#!/usr/bin/env python3
"""Generate seo_title for every article whose title exceeds the SERP limit.

Strategy (keyword-preserving, not blind truncation):
  1. If the title has a "Main: subtitle" structure, use the main part.
  2. If still too long, cut at a word boundary (never mid-word).
  3. Target <= SEO_TITLE_MAX (55) so that " - AI Tool Lab" (~15 chars)
     keeps the full <title> within Google's ~580px display budget.

seo_title is ONLY used for <title>/og:title/twitter:title (SERP display).
The full title stays as H1, JSON-LD headline, cards and RSS.

Usage:
  python scripts/gen_seo_titles.py --dry-run   # audit + preview
  python scripts/gen_seo_titles.py             # write seo_title fields
"""
import json
import re
import sys

ARTICLES = "data/articles_en.json"
SEO_TITLE_MAX = 55


def cut_word_boundary(s: str, limit: int) -> str:
    if len(s) <= limit:
        return s
    cut = s[:limit].rsplit(" ", 1)[0].rstrip(" ,-–—:")
    return cut


def make_seo_title(title: str) -> str:
    # 1) main part before colon (keeps the primary keyword, drops the long
    #    "vs A vs B vs C — The Real Cost" tail that Google would cut anyway)
    if ":" in title:
        main = title.split(":", 1)[0].strip()
    else:
        main = title
    # 2) "in 2026" carries the freshness signal — keep it if present in main
    # 3) word-boundary cut to the budget
    short = cut_word_boundary(main, SEO_TITLE_MAX)
    # tidy: collapse spaces, strip dangling prepositions
    short = re.sub(r"\s+", " ", short).strip()
    short = re.sub(r"\b(for|with|and|of|to|in)$", "", short).strip()
    return short


def main():
    dry = "--dry-run" in sys.argv
    arts = json.load(open(ARTICLES, encoding="utf-8"))
    changed = 0
    previews = []
    # build 端规则：serp_title<=46 时拼 " - AI Tool Lab"，否则裸用——两者都 <=60。
    # 因此只有 title 本体 >55（且无冒号主标题可用）的才需要生成截断；
    # 已有合规 seo_title（<=55）的保留不动。
    for a in arts:
        t = a.get("title", "")
        st = a.get("seo_title", "")
        if st and len(st) <= SEO_TITLE_MAX:
            continue  # existing seo_title is compliant
        if len(t) <= SEO_TITLE_MAX:
            continue  # full title already fits (build will show it bare or with suffix)
        new = st if st else make_seo_title(t)
        if len(new) > SEO_TITLE_MAX:
            new = cut_word_boundary(new, SEO_TITLE_MAX)
        if new != t:
            a["seo_title"] = new
            changed += 1
            previews.append((len(t), t[:70], new))
    over = [(a["slug"], a.get("seo_title", "")) for a in arts
            if a.get("seo_title") and len(a["seo_title"]) > SEO_TITLE_MAX]
    print("=== DRY RUN ===" if dry else "=== APPLY ===")
    print("seo_title written:", changed)
    print("still over budget after cut:", len(over))
    for slug, s in over[:10]:
        print(f"  {len(s):3d}  {slug} -> {s}")
    print("samples (len_full | full | seo_title):")
    for lf, full, new in previews[:25]:
        print(f"  {lf:3d}  {full[:58]:58} => {new}")
    if not dry:
        json.dump(arts, open(ARTICLES, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("[OK] written", ARTICLES)


if __name__ == "__main__":
    main()
