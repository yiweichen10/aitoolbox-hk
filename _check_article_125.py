# -*- coding: utf-8 -*-
"""自检脚本 for article #125 (must be run as standalone .py file)"""
import re, sys, json

DRAFT = r"C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\_article_125_draft.txt"
TOOLS = r"C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data\tools_en.json"
ARTICLES = r"C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data\articles_en.json"

with open(DRAFT, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. 词数
words = len(re.findall(r"\S+", text))
print(f"[1] Word count: {words}  (target 2200-2800) {'PASS' if 2200 <= words <= 2800 else 'FAIL'}")

# 2. PK 精确计数（小写）
pk = "ai subtitle generators 2026"
pk_count = len(re.findall(re.escape(pk), text.lower()))
print(f"[2] PK '{pk}' count: {pk_count} (target exactly 4) {'PASS' if pk_count == 4 else 'FAIL'}")

# 3. H2 里的 PK 必须小写
h2_lines = [l for l in text.split('\n') if l.startswith('## ')]
pk_in_h2 = [l for l in h2_lines if pk in l.lower()]
print(f"[3] H2 lines containing PK (must be lowercase): {pk_in_h2 if pk_in_h2 else 'NONE'} {'PASS' if pk_in_h2 else 'FAIL'}")

# 4. 长尾词
longtails = [
    "auto captions for TikTok",
    "AI video captions for YouTube",
    "Opus Clip vs Submagic",
    "free AI subtitle generator",
    "AI subtitles for social media",
    "CapCut auto captions",
    "video captioning tool",
    "Submagic alternatives",
    "subtitle generator pricing",
    "faceless YouTube channels",
]
lt_low = text.lower()
fails = []
for lt in longtails:
    c = lt_low.count(lt.lower())
    status = 'OK' if c >= 1 else 'MISSING'
    if c < 1:
        fails.append(lt)
    print(f"    longtail '{lt}': {c}x {status}")
print(f"[4] Long-tails: {'PASS (all present)' if not fails else 'FAIL: ' + str(fails)}")

# 5. 禁词
banned = ["leverage", "utilize", "seamlessly", "game-changing", "empower", "streamline",
          "delve into", "transformative", "comprehensive", "revolutionize", "cutting-edge",
          "as an AI", "in conclusion"]
hits = [b for b in banned if b.lower() in lt_low]
print(f"[5] Banned words: {hits if hits else 'NONE'} {'FAIL: ' + str(hits) if hits else 'PASS'}")

# 6. 内链（真实写入 markdown）
links = re.findall(r"\[([^\]]+)\]\((/tools/[^)]+|/articles/[^)]+)\)", text)
print(f"[6] Internal links found: {len(links)}")
for name, url in links:
    print(f"    - [{name}]({url})")
tool_slugs = set()
art_slugs = set()
try:
    with open(TOOLS, 'r', encoding='utf-8') as f:
        tool_slugs = {t.get('slug') for t in json.load(f)}
    with open(ARTICLES, 'r', encoding='utf-8') as f:
        art_slugs = {a.get('slug') for a in json.load(f)}
except Exception as e:
    print(f"    WARN: could not load slug sets: {e}")
valid = 0
for name, url in links:
    slug = url.strip('/').split('/')[-1]
    if '/tools/' in url and slug in tool_slugs:
        valid += 1
    elif '/articles/' in url and slug in art_slugs:
        valid += 1
    else:
        print(f"    INVALID LINK: {url} (slug '{slug}' not found)")
print(f"    Valid links: {valid}/{len(links)} {'PASS' if valid >= 2 and len(links) >= 2 else 'FAIL'}")

# 7. 对比表格（>=4行4列）
table_blocks = re.findall(r"\|.+\|(?:\n\|.+\|)+", text)
print(f"[7] Table blocks found: {len(table_blocks)}")
tbl_ok = False
for tb in table_blocks:
    rows = [r for r in tb.split('\n') if r.strip().startswith('|')]
    # 去掉分隔行
    data_rows = [r for r in rows if not re.match(r"^\|[\s\-:|]+\|$", r)]
    ncols = len([c for c in data_rows[0].split('|')[1:-1]]) if data_rows else 0
    print(f"    rows={len(data_rows)} cols={ncols}")
    if len(data_rows) >= 4 and ncols >= 4:
        tbl_ok = True
print(f"    Table requirement (>=4 rows, >=4 cols): {'PASS' if tbl_ok else 'FAIL'}")

# 8. FAQ
faq_h3 = re.findall(r"### .+", text)
faq_under = [h for h in faq_h3]
print(f"[8] FAQ H3 questions: {len(faq_under)} (need >=3) {'PASS' if len(faq_under) >= 3 else 'FAIL'}")
for h in faq_under:
    print(f"    - {h}")

print()
all_pass = (
    2200 <= words <= 2800 and pk_count == 4 and not fails and not hits
    and valid >= 2 and tbl_ok and len(faq_under) >= 3
)
print("=== OVERALL: " + ("ALL PASS ✅" if all_pass else "HAS FAILURES ❌") + " ===")
sys.exit(0 if all_pass else 1)
