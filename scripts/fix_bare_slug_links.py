#!/usr/bin/env python3
"""Fix bare-slug internal links in tool/article content (data-layer root fix).

Problem: content fields contain links like [ChatGPT](/chatgpt/) which render to
/comgpt/ -> 404. Correct path is /tools/chatgpt/.

Rules (conservative, following the "only link if counterpart exists" principle):
  1. bare slug in tool slugs     -> /tools/<slug>/
  2. bare slug in article slugs  -> /articles/<slug>/
  3. bare slug in explicit ALIAS map -> corrected /tools/<canonical>/
  4. bare slug unknown / semantically different -> link stripped, text kept
  5. real section paths (/tools/ /articles/ /category/ ...) are left untouched

Usage:
  python scripts/fix_bare_slug_links.py --dry-run   # audit only
  python scripts/fix_bare_slug_links.py             # apply
"""
import json
import re
import sys
from collections import Counter

TOOLS = "data/tools_en.json"
ARTICLES = "data/articles_en.json"
SECTIONS = {"tools", "articles", "category", "vs", "alternatives", "search", "author"}

# Only aliases that are DEFINITELY the same product (name variant / punctuation).
# Deliberately EXCLUDES semantically different items: llama->ollama,
# llama-3->ollama, claude-3-5-sonnet, magicschool-ai, diffit, etc.
ALIAS = {
    "canva": "canva-ai",
    "capcut": "capcut-ai",
    "zapier": "zapier-ai",
    "you-com": "you.com",
    "replit": "replit-ai",
    "remove-bg": "remove.bg",
    "copy-ai": "copy.ai",
    "bolt-new": "bolt.new",
    "webflow": "webflow-ai",
    "adobe-flyfly": "adobe-firefly",
    "adobe-fly": "adobe-firefly",
}

# matches [text](/slug/) and <a ... href="/slug/" ...>text</a>.
# Anchor text is captured so a stripped link keeps its words cleanly.
MD_RE = re.compile(r"\[([^\]]+)\]\((/[a-z0-9.\-]+/)\)")
HTML_RE = re.compile(r"(href=\")(/[a-z0-9.\-]+/)(\")")


def main():
    dry = "--dry-run" in sys.argv
    tools = json.load(open(TOOLS, encoding="utf-8"))
    arts = json.load(open(ARTICLES, encoding="utf-8"))
    tool_slugs = {t["slug"] for t in tools}
    art_slugs = {a["slug"] for a in arts}

    stats = Counter()
    examples = []

    def resolve(slug, owner):
        """Return corrected href, or None to strip the link (keep anchor text)."""
        if slug in SECTIONS:
            stats["untouched_section"] += 1
            return "__KEEP__"
        if slug in tool_slugs:
            stats["to_tool"] += 1
            return "/tools/" + slug + "/"
        if slug in art_slugs:
            stats["to_article"] += 1
            return "/articles/" + slug + "/"
        if slug in ALIAS and ALIAS[slug] in tool_slugs:
            stats["alias"] += 1
            return "/tools/" + ALIAS[slug] + "/"
        stats["stripped"] += 1
        if len(examples) < 12:
            examples.append(f"STRIP {owner}: {slug}")
        return None

    def fix_content(text, owner):
        def md_repl(m):
            label, href = m.group(1), m.group(2)
            new = resolve(href.strip("/"), owner)
            if new == "__KEEP__":
                return m.group(0)
            if new is None:
                return label
            return f"[{label}]({new})"

        def html_repl(m):
            new = resolve(m.group(2).strip("/"), owner)
            if new == "__KEEP__":
                return m.group(0)
            if new is None:
                return m.group(1) + m.group(2) + m.group(3)  # keep href but no link target change
            return m.group(1) + new + m.group(3)

        text = MD_RE.sub(md_repl, text)
        text = HTML_RE.sub(html_repl, text)
        return text

    changed_t = changed_a = 0
    for t in tools:
        old = t.get("content", "")
        new = fix_content(old, "tool:" + t["slug"])
        if new != old:
            t["content"] = new
            changed_t += 1
    for a in arts:
        old = a.get("content", "")
        new = fix_content(old, "article:" + a["slug"])
        if new != old:
            a["content"] = new
            changed_a += 1

    print("=== DRY RUN ===" if dry else "=== APPLY ===")
    print("changed tools:", changed_t, "| changed articles:", changed_a)
    for k, v in stats.most_common():
        print(f"  {v:5d}  {k}")
    print("strip examples:")
    for e in examples:
        print("  ", e)

    if not dry:
        with open(TOOLS, "w", encoding="utf-8") as f:
            json.dump(tools, f, ensure_ascii=False, indent=2)
        with open(ARTICLES, "w", encoding="utf-8") as f:
            json.dump(arts, f, ensure_ascii=False, indent=2)
        print("[OK] written", TOOLS, ARTICLES)


if __name__ == "__main__":
    main()
