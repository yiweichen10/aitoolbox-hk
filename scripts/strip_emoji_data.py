# -*- coding: utf-8 -*-
"""strip_emoji_data.py — one-off data migration (2026-11-17).

Removes decorative emojis from the content fields of tools_en.json and
articles_en.json. Rules:

  - KEEP U+2B50 (⭐): star-rating tables inside review content are editorial
    scoring notation ("Text rendering | ⭐⭐⭐⭐⭐"), stripping them would
    destroy the tables. Only the rating FIELD's "⭐ " prefix is normalised.
  - STRIP everything else in the emoji ranges (decorative), replaced by a
    space, then whitespace collapsed so words never glue together.
  - DELETE the legacy per-tool `emoji` field (dead data; renderer has zero
    references since the v2 redesign).
  - A timestamped backup of both files is written before any mutation.
"""
import json
import re
import shutil
from datetime import datetime

TOOLS = 'data/tools_en.json'
ARTICLES = 'data/articles_en.json'
STAMP = datetime.now().strftime('%Y%m%d_%H%M%S')

# emoji ranges, EXCLUDING U+2B50 (kept: star-rating notation in content)
EMOJI = re.compile(
    '[\U0001F000-\U0001FAFF]'
    '|[\u2600-\u27BF]'
    '|[\u2B00-\u2B4F]'
    '|[\uFE0F\u200D\u20E3]'
)


def clean_text(s: str) -> str:
    s2 = EMOJI.sub(' ', s)
    s2 = re.sub(r'[ \t]{2,}', ' ', s2)
    s2 = re.sub(r' +\n', '\n', s2)
    return s2


def clean_str(s):
    if not isinstance(s, str):
        return s, 0
    n = len(EMOJI.findall(s))
    if not n:
        return s, 0
    return clean_text(s), n


def clean_tool(t, report):
    moved = 0
    # dead legacy field
    if 'emoji' in t:
        moved += len(str(t['emoji']))
        del t['emoji']
    # rating normalisation: "⭐ 4.9" -> "4.9"
    r = t.get('rating')
    if isinstance(r, str) and '⭐' in r:
        t['rating'] = r.replace('⭐', '').replace('/ 5', '').strip()
        moved += 1
    for field in ('description', 'content', 'pricing_details', 'platform'):
        v, n = clean_str(t.get(field))
        if n:
            t[field] = v
            report[field] = report.get(field, 0) + n
            moved += n
    for field in ('pros', 'cons', 'features'):
        v = t.get(field)
        if isinstance(v, list):
            for i, item in enumerate(v):
                v2, n = clean_str(item)
                if n:
                    v[i] = v2
                    report[field] = report.get(field, 0) + n
                    moved += n
        elif isinstance(v, str):
            v2, n = clean_str(v)
            if n:
                t[field] = v2
                report[field] = report.get(field, 0) + n
                moved += n
    for f in t.get('faq') or []:
        for k in ('question', 'answer'):
            v2, n = clean_str(f.get(k))
            if n:
                f[k] = v2
                report[field] = report.get(field, 0) + n
                moved += n
    return moved


def clean_article(a, report):
    moved = 0
    for field in ('title', 'description', 'content'):
        v, n = clean_str(a.get(field))
        if n:
            a[field] = v
            report['art_' + field] = report.get('art_' + field, 0) + n
            moved += n
    return moved


def main():
    for src in (TOOLS, ARTICLES):
        shutil.copy(src, src.replace('.json', f'.bak_{STAMP}.json'))
    print('backups written: *.bak_%s.json' % STAMP)

    tools = json.load(open(TOOLS, encoding='utf-8'))
    report_t = {}
    n_t = sum(clean_tool(t, report_t) for t in tools)

    articles = json.load(open(ARTICLES, encoding='utf-8'))
    report_a = {}
    n_a = sum(clean_article(a, report_a) for a in articles)

    json.dump(tools, open(TOOLS, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    json.dump(articles, open(ARTICLES, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    print(f'tools: {n_t} emojis/dead-fields cleaned across {len(tools)} tools -> {report_t}')
    print(f'articles: {n_a} emojis cleaned across {len(articles)} articles -> {report_a}')
    print('kept: U+2B50 star-rating notation inside content (editorial scoring tables)')


if __name__ == '__main__':
    main()
