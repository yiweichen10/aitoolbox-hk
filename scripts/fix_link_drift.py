#!/usr/bin/env python3
"""Fix remaining internal-link format drift (2nd pass, after fix_bare_slug_links.py).

Patterns found in AI-generated article content:
  - /en/tools/<slug>/   -> /tools/<slug>/     (stray /en/ prefix)
  - /en/articles/<slug>/ -> /articles/<slug>/
  - /tool/<slug>/       -> /tools/<slug>/     (singular typo)
  - bare article slug   -> /articles/<slug>/
  - alias variants      -> canonical slug (invideo->invideo-ai, bolt-new->bolt.new)

Targets are verified against the current catalog + built pages; links whose
target does not exist are stripped to plain text (anchor kept).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from check_internal_links_en import _load_slugs, _page_exists, MD_RE, HTML_RE

ROOT = Path(__file__).resolve().parent.parent
TOOLS_FILE = ROOT / "data" / "tools_en.json"
ARTICLES_FILE = ROOT / "data" / "articles_en.json"

ALIAS_TOOL = {"invideo": "invideo-ai", "bolt-new": "bolt.new"}
SECTIONS = {"tools", "articles", "category", "vs", "alternatives", "search", "author",
            "css", "js", "images", "assets"}


def main():
    dry = "--dry-run" in sys.argv
    tools = json.load(open(TOOLS_FILE, encoding="utf-8"))
    arts = json.load(open(ARTICLES_FILE, encoding="utf-8"))
    tslugs, aslugs = _load_slugs()
    stats = {}

    def resolve(path):
        """Return corrected href, '__KEEP__', or None to strip."""
        parts = [p for p in path.split("?")[0].split("#")[0].split("/") if p]
        if not parts:
            return "__KEEP__"
        # stray /en/ prefix
        if parts[0] == "en" and len(parts) > 1:
            parts = parts[1:]
        # singular /tool/
        if parts[0] == "tool" and len(parts) > 1:
            parts[0] = "tools"
        if parts[0] not in SECTIONS:
            # bare slug: guess tools first, then articles
            slug = parts[0]
            if slug in ALIAS_TOOL:
                slug = ALIAS_TOOL[slug]
            if slug in tslugs and _page_exists("tools", slug):
                stats["bare_to_tool"] = stats.get("bare_to_tool", 0) + 1
                return "/tools/" + slug + "/"
            if slug in aslugs and _page_exists("articles", slug):
                stats["bare_to_article"] = stats.get("bare_to_article", 0) + 1
                return "/articles/" + slug + "/"
            stats["stripped"] = stats.get("stripped", 0) + 1
            return None
        kind = parts[0]
        if len(parts) < 2:
            return "__KEEP__"
        slug = parts[1]
        if slug in ALIAS_TOOL and kind == "tools":
            slug = ALIAS_TOOL[slug]
        ok = ((kind == "tools" and slug in tslugs and _page_exists("tools", slug)) or
              (kind == "articles" and slug in aslugs and _page_exists("articles", slug)) or
              (kind == "category" and (ROOT / "category" / slug / "index.html").is_file()))
        if ok:
            stats["prefix_fixed"] = stats.get("prefix_fixed", 0) + 1
            return f"/{kind}/{slug}/"
        stats["stripped"] = stats.get("stripped", 0) + 1
        return None

    def fix(text):
        def md(m):
            label, href = m.group(1), m.group(2)
            new = resolve(href)
            if new == "__KEEP__":
                return m.group(0)
            if new is None:
                return label
            return f"[{label}]({new})"

        def html(m):
            new = resolve(m.group(1))
            return m.group(0) if new == "__KEEP__" else (m.group(0) if new is None else f'href="{new}"')

        return HTML_RE.sub(html, MD_RE.sub(md, text or ""))

    ct = ca = 0
    for t in tools:
        old = t.get("content", "")
        new = fix(old)
        if new != old:
            t["content"] = new
            ct += 1
    for a in arts:
        old = a.get("content", "")
        new = fix(old)
        if new != old:
            a["content"] = new
            ca += 1

    print("=== DRY RUN ===" if dry else "=== APPLY ===")
    print("changed tools:", ct, "changed articles:", ca)
    for k, v in sorted(stats.items()):
        print(f"  {v:4d}  {k}")
    if not dry:
        json.dump(tools, open(TOOLS_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        json.dump(arts, open(ARTICLES_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("[OK] written")


if __name__ == "__main__":
    main()
