# -*- coding: utf-8 -*-
"""生成 aitoolbox.hk 意图词候选表(不依赖 GSC/外部流量,纯站点资产驱动)。
输出: keyword_opportunities.csv + .md
三类词:
  1) 对比词: 同类工具互比 (category 内 top 工具组合)
  2) 品牌词: 153 工具 -> X review / X alternatives / X vs [竞品]
  3) 长尾词: 分类 x 场景/职业 模板
标注: 现有文章是否已覆盖 (gap 分析)
"""
import json, csv, os, re
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, 'data')
OUT = os.path.join(BASE, 'exports')

tools = json.load(open(os.path.join(DATA, 'tools_en.json'), encoding='utf-8'))
articles = json.load(open(os.path.join(DATA, 'articles_en.json'), encoding='utf-8'))

# 现有文章覆盖的工具名集合(从标题/url 抽)
existing_slugs = {a['slug'] for a in articles}
existing_titles = ' '.join(a.get('title', '').lower() for a in articles)
existing_urls = ' '.join(a.get('slug', '').lower() for a in articles)

# 分类聚类
cat_tools = defaultdict(list)
for t in tools:
    cat_tools[t.get('category', '?')].append(t)

# 真人场景/职业长尾模板(用于长尾词生成)
SCENARIOS = {
    'AI Video': ['youtube', 'tiktok', 'short films', 'product demos', 'faceless youtube'],
    'AI Image': ['social media', 'ecommerce product', 'profile picture', 'logo', 'wallpaper'],
    'AI Coding': ['beginners', 'freelancers', 'startups', 'students', 'non-technical'],
    'AI Audio': ['podcasters', 'youtube videos', 'audiobooks', 'tiktok voiceover'],
    'AI Development': ['indie hackers', 'startups', 'prototyping', 'backend'],
    'AI Chat': ['writing', 'coding help', 'customer support', 'study'],
    'AI Design': ['non-designers', 'small business', 'social media', 'ui mockups'],
    'AI Writing': ['bloggers', 'students', 'copywriters', 'non-native english'],
    'AI Automation': ['small business', 'solopreneurs', 'marketers', 'no-code'],
    'AI Search': ['researchers', 'students', 'developers', 'fact-checking'],
    'AI Agents': ['business workflow', 'customer service', 'sales', 'personal assistant'],
    'AI Marketing': ['small business', 'saas', 'ecommerce', 'agencies'],
    'AI Productivity': ['remote teams', 'students', 'freelancers', 'executives'],
    'AI SEO': ['bloggers', 'saas', 'ecommerce', 'agencies'],
    'AI Translation': ['business', 'travel', 'documents', 'video subtitles'],
    'AI E-commerce': ['shopify', 'small business', 'dropshipping', 'product photos'],
    'AI Web Design': ['non-technical', 'small business', 'landing pages', 'portfolios'],
    'AI Research': ['students', 'academics', 'market analysts', 'phd'],
    'AI Office': ['remote teams', 'executives', 'administrative', 'students'],
    'Market Research': ['startups', 'product managers', 'vc', 'competitor analysis'],
}

def has_cover(text):
    """粗略判断现有文章是否覆盖某工具/词"""
    t = text.lower()
    return t in existing_urls or t in existing_titles

rows = []

# ---- 1) 对比词: 同类内 top 4 组合 ----
for cat, ts in cat_tools.items():
    # 过滤过小分类(>=3 才值得比)
    if len(ts) < 3:
        continue
    top = ts[:5]
    # 去重同名(如 jasper / jasper-chat 同分类)避免组合里重复
    seen = set(); dedup_top = []
    for t in top:
        if t['name'].lower() in seen:
            continue
        seen.add(t['name'].lower()); dedup_top.append(t)
    top = dedup_top[:4] if dedup_top else top[:4]
    names = [t['name'] for t in top]
    # 生成 "A vs B vs C vs D" 主对比词
    combo = ' vs '.join(names[:4])
    slug_tail = '-vs-'.join(t['slug'] for t in top[:4])
    # 分类名若已含 "ai" 则不重复拼
    cat_lc = cat.lower()
    cat_label = cat_lc if 'ai' in cat_lc else f'ai {cat_lc}'
    kw = f"best {cat_label} tools in 2026: {combo}"
    covered = any(has_cover(t['slug']) for t in top[:4])
    rows.append({
        'keyword': kw, 'type': 'Comparison', 'category': cat,
        'tools': ', '.join(names[:4]),
        'covered': 'YES' if covered else 'GAP',
        'priority': 'P1' if not covered else 'P2'
    })
    # 两两对比(高意图,商业价值强) — 跳过同名/同slug互比
    for i in range(min(4, len(top))):
        for j in range(i+1, min(4, len(top))):
            if top[i]['slug'] == top[j]['slug'] or top[i]['name'].lower() == top[j]['name'].lower():
                continue
            pair = f"{top[i]['name']} vs {top[j]['name']}"
            pk = f"{top[i]['slug']}-vs-{top[j]['slug']}"
            cov = has_cover(top[i]['slug']) and has_cover(top[j]['slug'])
            rows.append({
                'keyword': pair, 'type': 'Comparison', 'category': cat,
                'tools': f"{top[i]['name']}, {top[j]['name']}",
                'covered': 'YES' if cov else 'GAP',
                'priority': 'P1' if not cov else 'P2'
            })

# ---- 2) 品牌词: 153 工具 -> review / alternatives / vs竞品 ----
# 选每个工具的一个同分类竞品做 "X vs Y"
cat_by_name = {t['slug']: t for t in tools}
for t in tools:
    slug, name, cat = t['slug'], t['name'], t.get('category', '?')
    # review
    rows.append({'keyword': f"{name} review 2026", 'type': 'Brand', 'category': cat,
                 'tools': name, 'covered': 'YES' if has_cover(slug) else 'GAP',
                 'priority': 'P2' if has_cover(slug) else 'P1'})
    # alternatives
    rows.append({'keyword': f"{name} alternatives", 'type': 'Brand', 'category': cat,
                 'tools': name, 'covered': 'GAP', 'priority': 'P3'})
    # vs 一个同分类竞品 (跳过同名/同slug自比)
    peers = [x for x in cat_tools[cat] if x['slug'] != slug and x['name'].lower() != name.lower()]
    if peers:
        p = peers[0]
        rows.append({'keyword': f"{name} vs {p['name']}", 'type': 'Brand', 'category': cat,
                     'tools': f"{name}, {p['name']}",
                     'covered': 'YES' if (has_cover(slug) and has_cover(p['slug'])) else 'GAP',
                     'priority': 'P2'})

# ---- 3) 长尾词: 分类 x 场景 ----
for cat, scen in SCENARIOS.items():
    if cat not in cat_tools:
        continue
    cat_lc = cat.lower()
    cat_label = cat_lc if 'ai' in cat_lc else f'ai {cat_lc}'
    for s in scen:
        kw = f"best {cat_label} tool for {s} 2026"
        # 长尾词覆盖判定: 分类相关文章已存在则算部分覆盖
        cat_cov = any(cat.lower() in u for u in existing_urls.split())
        rows.append({'keyword': kw, 'type': 'Long-tail', 'category': cat,
                     'tools': f"[category: {cat}]", 'covered': 'YES' if cat_cov else 'GAP',
                     'priority': 'P1' if not cat_cov else 'P2'})

# ---- 统计 + 输出 ----
os.makedirs(OUT, exist_ok=True)
csv_path = os.path.join(OUT, 'keyword_opportunities.csv')
md_path = os.path.join(OUT, 'keyword_opportunities.md')

with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['keyword','type','category','tools','covered','priority'])
    w.writeheader()
    w.writerows(rows)

# 统计
from collections import Counter
type_cnt = Counter(r['type'] for r in rows)
gap_cnt = sum(1 for r in rows if r['covered'] == 'GAP')
p1_gap = [r for r in rows if r['priority']=='P1' and r['covered']=='GAP']

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(f"# aitoolbox.hk 意图词候选表 (生成于站点资产, 不依赖 GSC)\n\n")
    f.write(f"- 总词数: **{len(rows)}**\n")
    f.write(f"- 类型分布: {dict(type_cnt)}\n")
    f.write(f"- 未覆盖(GAP): **{gap_cnt}** 条\n")
    f.write(f"- P1 优先级未覆盖(最该先做): **{len(p1_gap)}** 条\n\n")
    f.write("## P1 未覆盖词 (行动清单)\n\n")
    for r in p1_gap[:60]:
        f.write(f"- [{r['type']}] `{r['keyword']}` — cat: {r['category']}\n")
    f.write("\n## 全量词表 (CSV 见 keyword_opportunities.csv)\n\n")
    for r in rows[:200]:
        f.write(f"- {r['covered']:4s} | {r['priority']} | {r['type']:10s} | {r['keyword']}\n")

print(f"总词数: {len(rows)}")
print(f"类型分布: {dict(type_cnt)}")
print(f"GAP 未覆盖: {gap_cnt}")
print(f"P1 GAP: {len(p1_gap)}")
print(f"输出: {csv_path}")
print(f"输出: {md_path}")
