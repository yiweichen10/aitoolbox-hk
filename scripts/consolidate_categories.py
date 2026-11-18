#!/usr/bin/env python3
"""Consolidate duplicate tool categories into canonical 'AI X' names.

History: tools entered over months used near-duplicate labels —
'Video AI' vs 'AI Video', 'Image'/'AI Images' vs 'AI Image',
'AI Dev' vs 'AI Development', bare 'Marketing'/'Writing'/'SEO'/'Productivity'
vs their 'AI ' prefixed twins. Each duplicate label built its own /category/
page, splitting link equity and confusing navigation (32 labels -> ~10 dupes).

Mapping policy: canonical keeps the 'AI ' prefix; Webflow AI joins
AI Website Builder (it is a site platform, not a design asset tool).
AI Research (papers/科学) and Market Research (市场调研) are semantically
DIFFERENT and intentionally NOT merged.

Usage:
  python scripts/consolidate_categories.py --dry-run
  python scripts/consolidate_categories.py
"""
import json
import sys

TOOLS = "data/tools_en.json"

CANONICAL_MAP = {
    "Video AI":      "AI Video",
    "AI Images":     "AI Image",
    "Image":         "AI Image",
    "AI Dev":        "AI Development",
    "Marketing":     "AI Marketing",
    "Productivity":  "AI Productivity",
    "Writing":       "AI Writing",
    "SEO":           "AI SEO",
    "Automation":    "AI Automation",
    "AI Web Design": "AI Website Builder",
}


def main():
    dry = "--dry-run" in sys.argv
    tools = json.load(open(TOOLS, encoding="utf-8"))
    changes = {}
    for t in tools:
        old = t.get("category", "")
        new = CANONICAL_MAP.get(old)
        if new:
            changes.setdefault((old, new), []).append(t["slug"])
            t["category"] = new
    print("=== DRY RUN ===" if dry else "=== APPLY ===")
    for (old, new), slugs in sorted(changes.items()):
        print(f"  {len(slugs):3d}  {old!r} -> {new!r}   e.g. {slugs[:4]}")
    cats = sorted({t.get('category') for t in tools})
    print(f"分类数: 32 -> {len(cats)}")
    print("收敛后分类:", cats)
    if not dry:
        json.dump(tools, open(TOOLS, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("[OK] written", TOOLS)


if __name__ == "__main__":
    main()
