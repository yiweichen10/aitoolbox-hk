#!/usr/bin/env python3
"""
Reusable article appender for aitoolbox.hk articles_en.json.

Usage:
    python scripts/append_article.py <content_file.txt> --slug "my-slug" --category "Category Name"

Example:
    python scripts/append_article.py article_89_content.txt \
        --slug "best-ai-healthcare-tools-2026" \
        --category "AI Healthcare"

The content file must have title on first line, body on subsequent lines.
Field naming convention: always use "content" (NOT "body") — this matches what build_en.py reads.
Articles are prepended (newest first) to match existing convention.
"""
import json
import os
import sys
import argparse
from datetime import datetime

# === CONFIG ===
# Path to articles_en.json (relative to project root, resolved from this script's location)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
ARTICLES_PATH = os.path.join(PROJECT_ROOT, "data", "articles_en.json")

# === THE ONLY VALID FIELD NAME ===
# build_en.py line ~727 reads: article.get('content')
# DO NOT use "body" — it will produce empty pages.
CONTENT_FIELD = "content"


def append_article(content_file: str, slug: str, category: str, date: str = None,
                   keywords: list = None, description: str = None) -> dict:
    """
    Read content from file, build article dict with correct fields, append to articles_en.json.

    Returns the article dict that was appended.
    """
    if not os.path.exists(content_file):
        raise FileNotFoundError(f"Content file not found: {content_file}")

    with open(content_file, "r", encoding="utf-8") as f:
        raw = f.read()

    lines = raw.strip().split("\n")
    title = lines[0].strip()
    # Remove leading "## " if present (some content files have markdown title prefix)
    if title.startswith("## "):
        title = title[3:].strip()
    body = "\n".join(lines[1:]).strip()

    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    # Auto-extract description from first ~160 chars of body
    if description is None:
        first_para = body.split("\n\n")[0].strip()
        if len(first_para) > 160:
            description = first_para[:157] + "..."
        else:
            description = first_para

    article = {
        "title": title,
        "slug": slug,
        "date": date,
        "category": category,
        "description": description,
        "keywords": ", ".join(keywords) if keywords else "",
        CONTENT_FIELD: body,  # <-- THE ONLY VALID FIELD NAME
    }

    # Read existing articles
    with open(ARTICLES_PATH, "r", encoding="utf-8") as f:
        articles = json.load(f)

    # Prepend (newest first — convention used by all previous append scripts)
    articles.insert(0, article)

    # Write back
    with open(ARTICLES_PATH, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"✓ Appended article #{len(articles)}: {title[:80]}")
    print(f"  Slug: {slug}")
    print(f"  Category: {category}")
    print(f"  Date: {date}")
    print(f"  Body length: {len(body)} chars")
    return article


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Append a new article to articles_en.json")
    parser.add_argument("content_file", help="Path to .txt file with article content")
    parser.add_argument("--slug", required=True, help="URL slug (e.g. best-ai-foo-tools-2026)")
    parser.add_argument("--category", required=True, help="Category name (e.g. 'AI Video')")
    parser.add_argument("--date", help="Publication date (default: today)")
    parser.add_argument("--keywords", nargs="*", help="Space-separated keywords")
    args = parser.parse_args()

    append_article(
        content_file=args.content_file,
        slug=args.slug,
        category=args.category,
        date=args.date,
        keywords=args.keywords,
    )
