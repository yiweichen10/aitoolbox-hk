#!/usr/bin/env python3
"""Unified internal-link validator — the single source of truth for link rules.

Closes the loop that let bare-slug links (/chatgpt/) accumulate into 972 404s:
the old validate_internal_links.py only checked /articles/ links, so daily builds
passed while broken links piled up.

Link rules (target existence is checked against CURRENT catalog + built pages):
  - /tools/<slug>/      -> slug must exist in tools_en.json AND have a built page
  - /articles/<slug>/   -> slug must exist in articles_en.json AND have a built page
  - /category/<slug>/   -> slug must have a built category page
  - /<bare-slug>/       -> BARE SLUG (bug): must be rewritten to /tools/<slug>/
                           (or /articles/); if target does not exist, strip link
  - /<section>/ paths (css/js/images/assets/etc.) -> ignored

Usages:
  # validate one text (called by write scripts before persisting)
  from check_internal_links_en import validate_text
  errors = validate_text(content)

  # validate whole catalog (called by build + cron audit)
  python scripts/check_internal_links.py            # audit, exit 1 if broken
  python scripts/check_internal_links.py --report   # detailed, auto-fixable list
"""
import json
import os
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA = BASE_DIR / "data"
TOOLS_FILE = DATA / "tools_en.json"
ARTICLES_FILE = DATA / "articles_en.json"

SECTIONS = {"tools", "articles", "category", "vs", "alternatives", "search", "author",
            "rankings",
            "css", "js", "images", "assets", "images", "favicon.ico"}

# matches [text](/path/) markdown links
MD_RE = re.compile(r"\[([^\]]+)\]\((/[^)]+)\)")
# matches href="/path/"
HTML_RE = re.compile(r'href="(/[^"]+)"')


def _load_slugs():
    tools = json.load(open(TOOLS_FILE, encoding="utf-8"))
    arts = json.load(open(ARTICLES_FILE, encoding="utf-8"))
    tool_slugs = {t["slug"] for t in tools}
    art_slugs = {a["slug"] for a in arts}
    return tool_slugs, art_slugs


# 2026-11-18 治本：链接不只在 content 里，还藏在结构化字段（faq[].answer、
# pros/cons/features 列表、pricing_details）——pika 的 2 处裸 slug 就在 faq 里，
# 旧校验只查 content，漏网。这里定义哪些字段承载正文文本、需要校验。
TOOL_TEXT_FIELDS = ("content", "pricing_details")
ARTICLE_TEXT_FIELDS = ("content", "description")
# 递归跳过的纯值字段（永不包含链接）
SKIP_KEYS = {"url", "slug", "name", "color", "visits", "badge", "price",
             "date", "dateFull", "keywords", "aeo_geo_updated", "verified_price",
             "last_verified", "platform", "category", "title"}


def _page_exists(kind, slug):
    """Check the built page exists on disk (stronger than slug-in-json)."""
    p = BASE_DIR / kind / slug / "index.html"
    return p.is_file()


def validate_text(text, tool_slugs=None, art_slugs=None):
    """Return list of error dicts for internal links in one text blob.

    Each error: {'kind': 'bare'|'missing'|'category', 'href':..., 'label':..., 'reason':...}
    """
    if tool_slugs is None or art_slugs is None:
        tool_slugs, art_slugs = _load_slugs()
    errs = []
    for m in MD_RE.finditer(text or ""):
        label, href = m.group(1), m.group(2)
        path = href.split("?")[0].split("#")[0]
        parts = [p for p in path.split("/") if p]
        if not parts:
            continue
        first = parts[0]
        if first in SECTIONS:
            # 内部栏目链接强制尾斜杠（CF Pages 会 308，但统一格式利于一致性抓取）
            if first in ("tools", "articles", "category") and not href.endswith("/"):
                errs.append({"kind": "format", "href": href, "label": label,
                             "reason": "internal link missing trailing slash"})
            # known section: validate target for tools/articles/category
            if first == "tools" and len(parts) >= 2:
                slug = parts[1]
                if slug not in tool_slugs or not _page_exists("tools", slug):
                    errs.append({"kind": "missing", "href": href, "label": label,
                                 "reason": "tool page not found: " + slug})
            elif first == "articles" and len(parts) >= 2:
                slug = parts[1]
                if slug not in art_slugs or not _page_exists("articles", slug):
                    errs.append({"kind": "missing", "href": href, "label": label,
                                 "reason": "article page not found: " + slug})
            elif first == "category" and len(parts) >= 2:
                slug = parts[1]
                if not (BASE_DIR / "category" / slug / "index.html").is_file():
                    errs.append({"kind": "category", "href": href, "label": label,
                                 "reason": "category page not found: " + slug})
            elif first == "rankings" and len(parts) >= 2:
                slug = parts[1]
                if not (BASE_DIR / "rankings" / slug / "index.html").is_file():
                    errs.append({"kind": "rankings", "href": href, "label": label,
                                 "reason": "rankings page not found: " + slug})
            continue
        # bare slug (no known section prefix)
        slug = first
        if slug in tool_slugs and _page_exists("tools", slug):
            errs.append({"kind": "bare", "href": href, "label": label,
                         "reason": "bare tool slug, must be /tools/" + slug + "/"})
        elif slug in art_slugs and _page_exists("articles", slug):
            errs.append({"kind": "bare", "href": href, "label": label,
                         "reason": "bare article slug, must be /articles/" + slug + "/"})
        else:
            errs.append({"kind": "missing", "href": href, "label": label,
                         "reason": "link target not in catalog: " + slug})
    # HTML hrefs: check tools/articles/category targets only
    for m in HTML_RE.finditer(text or ""):
        href = m.group(1)
        path = href.split("?")[0].split("#")[0]
        parts = [p for p in path.split("/") if p]
        if not parts or parts[0] not in ("tools", "articles", "category") or len(parts) < 2:
            continue
        slug = parts[1]
        if parts[0] == "tools" and (slug not in tool_slugs or not _page_exists("tools", slug)):
            errs.append({"kind": "missing", "href": href, "label": "html",
                         "reason": "tool page not found: " + slug})
        elif parts[0] == "articles" and (slug not in art_slugs or not _page_exists("articles", slug)):
            errs.append({"kind": "missing", "href": href, "label": "html",
                         "reason": "article page not found: " + slug})
        elif parts[0] == "category" and not (BASE_DIR / "category" / slug / "index.html").is_file():
            errs.append({"kind": "category", "href": href, "label": "html",
                         "reason": "category page not found: " + slug})
    return errs


def _iter_text_fields(obj, path="", skip_top=None):
    """Yield (path, text) for every string that may carry prose links."""
    if skip_top and path == "":
        for k in skip_top:
            if k in obj:
                obj = {key: v for key, v in obj.items() if key != k}
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _iter_text_fields(v, f"{path}[{i}]")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k in SKIP_KEYS:
                continue
            yield from _iter_text_fields(v, f"{path}.{k}" if path else k)


def validate_all(tool_slugs=None, art_slugs=None):
    """Validate the WHOLE catalog: content + every structured text field.

    2026-11-18: 递归覆盖 faq/pros/cons/features/pricing_details 等所有可能
    携带正文的字段（pika faq 裸 slug 教训），并强制内部链接带尾斜杠。
    Returns (error_count, [(owner, err), ...]).
    """
    if tool_slugs is None or art_slugs is None:
        tool_slugs, art_slugs = _load_slugs()
    all_errs = []
    tools = json.load(open(TOOLS_FILE, encoding="utf-8"))
    arts = json.load(open(ARTICLES_FILE, encoding="utf-8"))
    for t in tools:
        for path, text in _iter_text_fields(t):
            for e in validate_text(text, tool_slugs, art_slugs):
                e = dict(e)
                e["field"] = path
                all_errs.append(("tool:" + t["slug"], e))
    for a in arts:
        for path, text in _iter_text_fields(a):
            for e in validate_text(text, tool_slugs, art_slugs):
                e = dict(e)
                e["field"] = path
                all_errs.append(("article:" + a["slug"], e))
    return len(all_errs), all_errs


def main():
    report = "--report" in sys.argv
    tool_slugs, art_slugs = _load_slugs()
    n, errs = validate_all(tool_slugs, art_slugs)
    by_kind = {}
    for owner, e in errs:
        by_kind[e["kind"]] = by_kind.get(e["kind"], 0) + 1
    print(f"[LINK AUDIT] tools={len(tool_slugs)} articles={len(art_slugs)}")
    print(f"[LINK AUDIT] broken links: {n}  {by_kind}")
    if report or n:
        for owner, e in errs[:40]:
            print(f"  {owner}: {e['kind']:8} {e['href']}  ({e['reason']})")
        if n > 40:
            print(f"  ... and {n-40} more")
    if n:
        print("[LINK AUDIT] FAIL — fix before build/deploy.")
        sys.exit(1)
    print("[LINK AUDIT] OK — all internal links resolve.")
    sys.exit(0)


if __name__ == "__main__":
    main()
