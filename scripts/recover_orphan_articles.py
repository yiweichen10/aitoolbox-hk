# -*- coding: utf-8 -*-
"""P0-2: 将两个孤儿文章补录进 articles_en.json(回收进自动化管理体系)。
孤儿文章(已生成HTML,有真实内容,但不在 data 源):
  - ai-tools-that-make-money-2026 (date 2026-04-08, cat AI Income)
  - best-free-ai-tools-2026 (date 2026-04-07, cat AI Tools)
从 HTML 提取正文 → 构造 dict → 追加。不删页,只补录。
"""
import re, json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, 'data', 'articles_en.json')

ORPHANS = {
    'ai-tools-that-make-money-2026': {
        'title': '5 AI Tools That Actually Make Money in 2026 (Tested)',
        'slug': 'ai-tools-that-make-money-2026',
        'date': '2026-04-08',
        'dateFull': '2026-04-08T06:50:00+08:00',
        'category': 'AI Income',
        'description': "We tested 20+ AI tools for real income potential. These 5 consistently generated revenue for solo creators and freelancers with zero upfront investment.",
        'keywords': [
            'AI tools that make money 2026',
            'AI income tools tested',
            'best AI tools for freelancers',
            'AI side hustle tools',
            'AI tools to earn money online',
            'passive income AI tools',
            'AI tools for solo creators',
            'real income AI tools review',
        ],
    },
    'best-free-ai-tools-2026': {
        'title': 'Best Free AI Tools in 2026: No Credit Card Required',
        'slug': 'best-free-ai-tools-2026',
        'date': '2026-04-07',
        'dateFull': '2026-04-07T06:50:00+08:00',
        'category': 'AI Tools',
        'description': "The complete guide to the best AI tools you can use for free in 2026. No credit card, no trial period — just sign up and start using.",
        'keywords': [
            'best free AI tools 2026',
            'free AI tools no credit card',
            'free AI tools no sign up',
            'completely free AI tools',
            'free AI writing tools',
            'free AI image generators',
            'free ChatGPT alternatives',
            'free AI tools list 2026',
        ],
    },
}


def extract_content(slug):
    path = os.path.join(BASE, 'articles', slug, 'index.html')
    h = open(path, encoding='utf-8', errors='ignore').read()
    art = re.search(r'<article[^>]*>(.*?)</article>', h, re.S)
    if not art:
        return ''
    body = art.group(1)
    body = re.sub(r'</(p|h2|h3|h4|li|blockquote)>', '\n', body)
    body = re.sub(r'<[^>]+>', '', body)
    lines = [l.strip() for l in body.split('\n')]
    # 清理开头的 "标题 / 日期 · 分类" 噪音行
    cleaned = []
    skip_prefixes = ('April ', 'Best Free AI Tools in 2026:', '5 AI Tools That Actually Make Money in 2026 (Tested)')
    started = False
    for l in lines:
        if not l:
            continue
        if not started:
            if l.startswith(skip_prefixes) or '·' in l and ('2026' in l or 'AI' in l):
                continue
            started = True
        cleaned.append(l)
    return '\n'.join(cleaned).strip()


def main():
    a = json.load(open(DATA, encoding='utf-8'))
    existing = {x['slug'] for x in a}
    added = []
    for slug, meta in ORPHANS.items():
        if slug in existing:
            print(f'SKIP {slug} (already in data)')
            continue
        content = extract_content(slug)
        if not content:
            print(f'WARN {slug}: content empty, skip')
            continue
        entry = dict(meta)
        entry['content'] = content
        a.append(entry)
        added.append(slug)
        print(f'ADDED {slug} (content {len(content)} chars)')
    if added:
        json.dump(a, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        print(f'\nSaved. Total articles: {len(a)} (+{len(added)})')
    else:
        print('Nothing added.')


if __name__ == '__main__':
    main()
