# -*- coding: utf-8 -*-
"""
Export EN site content (tools + articles) from JSON to readable Markdown files.

Usage:
  python scripts/export_content_en.py                    # 导出全部（工具+文章）
  python scripts/export_content_en.py --type tools       # 只导工具
  python scripts/export_content_en.py --type articles    # 只导文章
  python scripts/export_content_en.py --slug fathom      # 只导单个工具/文章
  python scripts/export_content_en.py --out exports      # 指定输出目录
  python scripts/export_content_en.py --format txt       # 输出纯文本（默认 md）

Output: exports/tools_all.md, exports/articles_all.md (or exports/<slug>.md)
"""
import argparse
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, 'data')


def load_json(name):
    with open(os.path.join(DATA, name), 'r', encoding='utf-8') as f:
        return json.load(f)


def tool_to_md(t):
    lines = []
    lines.append(f"# {t.get('name', '')}")
    lines.append("")
    meta = f"- **Category**: {t.get('category','')}"
    if t.get('rating'): meta += f" | **Rating**: {t['rating']}"
    if t.get('price'): meta += f" | **Price**: {t['price']}"
    if t.get('platform'): meta += f" | **Platform**: {t['platform']}"
    lines.append(meta)
    if t.get('url'): lines.append(f"- **URL**: {t['url']}")
    lines.append("")
    lines.append("## Description")
    lines.append("")
    lines.append(t.get('description', ''))
    lines.append("")
    if t.get('pros'):
        lines.append("## Pros")
        lines.append("")
        for p in t['pros']:
            lines.append(f"- {p}")
        lines.append("")
    if t.get('cons'):
        lines.append("## Cons")
        lines.append("")
        for c in t['cons']:
            lines.append(f"- {c}")
        lines.append("")
    if t.get('features'):
        lines.append("## Features")
        lines.append("")
        for ft in t['features']:
            lines.append(f"- {ft}")
        lines.append("")
    if t.get('faq'):
        lines.append("## FAQ")
        lines.append("")
        for q in t['faq']:
            qq = q.get('question') or q.get('q') or ''
            aa = q.get('answer') or q.get('a') or ''
            lines.append(f"### Q: {qq}")
            lines.append("")
            lines.append(aa)
            lines.append("")
    if t.get('content'):
        lines.append("## Full Review")
        lines.append("")
        lines.append(t['content'])
        lines.append("")
    return "\n".join(lines)


def article_to_md(a):
    lines = []
    lines.append(f"# {a.get('title', '')}")
    lines.append("")
    meta = []
    if a.get('date'): meta.append(f"**Date**: {a['date']}")
    if a.get('dateFull'): meta.append(f"**DateFull**: {a['dateFull']}")
    if a.get('category'): meta.append(f"**Category**: {a['category']}")
    lines.append(" | ".join(meta))
    lines.append("")
    if a.get('description'):
        lines.append("## Description")
        lines.append("")
        lines.append(a['description'])
        lines.append("")
    if a.get('keywords'):
        lines.append(f"**Keywords**: {a['keywords']}")
        lines.append("")
    if a.get('content'):
        lines.append("## Full Article")
        lines.append("")
        lines.append(a['content'])
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description='Export EN site content to Markdown')
    ap.add_argument('--type', choices=['tools', 'articles', 'both'], default='both')
    ap.add_argument('--slug', help='Export only one tool/article by slug')
    ap.add_argument('--out', default=os.path.join(BASE, 'exports'))
    ap.add_argument('--format', choices=['md', 'txt'], default='md')
    args = ap.parse_args()

    tools = load_json('tools_en.json')
    arts = load_json('articles_en.json')
    os.makedirs(args.out, exist_ok=True)

    # 单个 slug
    if args.slug:
        for t in tools:
            if t['slug'] == args.slug:
                fn = os.path.join(args.out, f"tool-{args.slug}.{args.format}")
                with open(fn, 'w', encoding='utf-8') as f:
                    f.write(tool_to_md(t))
                print(f"[OK] {fn} ({len(tool_to_md(t))} chars)")
                return
        for a in arts:
            if a['slug'] == args.slug:
                fn = os.path.join(args.out, f"article-{args.slug}.{args.format}")
                with open(fn, 'w', encoding='utf-8') as f:
                    f.write(article_to_md(a))
                print(f"[OK] {fn} ({len(article_to_md(a))} chars)")
                return
        print(f"[ERR] slug '{args.slug}' not found in tools or articles.")
        return

    # 批量
    if args.type in ('tools', 'both'):
        parts = [tool_to_md(t) + "\n\n---\n\n" for t in tools]
        fn = os.path.join(args.out, f"tools_all.{args.format}")
        with open(fn, 'w', encoding='utf-8') as f:
            f.write("".join(parts))
        total = sum(len(p) for p in parts)
        print(f"[OK] {fn} — {len(tools)} tools, {total} chars")

    if args.type in ('articles', 'both'):
        parts = [article_to_md(a) + "\n\n---\n\n" for a in arts]
        fn = os.path.join(args.out, f"articles_all.{args.format}")
        with open(fn, 'w', encoding='utf-8') as f:
            f.write("".join(parts))
        total = sum(len(p) for p in parts)
        print(f"[OK] {fn} — {len(arts)} articles, {total} chars")

    print(f"Output dir: {args.out}")


if __name__ == '__main__':
    main()
