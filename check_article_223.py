# -*- coding: utf-8 -*-
"""Self-check for article #223: SEO/GEO compliance."""
import json, re, os

ARTICLE_SLUG = "best-serverless-functions-pricing-2026-aws-lambda-vs-cloudflare-workers-vs-vercel-vs-deno-deploy"
PK = "serverless functions pricing"
LONGTAILS = ["aws lambda pricing", "lambda cost per million requests", "aws lambda free tier",
             "cloudflare workers pricing", "cloudflare workers free tier", "vercel functions pricing",
             "deno deploy pricing", "cheapest serverless functions", "lambda vs cloudflare workers",
             "serverless cost per million requests"]
BANNED = ["leverage", "utilize", "seamlessly", "game-changing", "empower",
          "streamline", "delve into", "transformative", "comprehensive",
          "revolutionize", "cutting-edge", "as an AI", "in conclusion"]

with open("data/articles_en.json", encoding="utf-8") as f:
    data = json.load(f)
arts = data if isinstance(data, list) else data["articles"]
art = next(a for a in arts if a["slug"] == ARTICLE_SLUG)
c = art["content"]

errors, warns = [], []

# 1. Primary keyword count (case-insensitive)
pk_count = len(re.findall(re.escape(PK), c, re.I))
if pk_count != 4:
    errors.append(f"PK '{PK}' count = {pk_count}, expected exactly 4")

# 2. Banned words (word-boundary, case-insensitive)
low = c.lower()
for w in BANNED:
    if re.search(r"\b" + re.escape(w) + r"\b", low):
        errors.append("banned word found: " + w)

# 3. Word count (split)
wc = len(c.split())
if not (2200 <= wc <= 2800):
    errors.append(f"word count {wc} outside 2200-2800")

# 4. Internal links
links = re.findall(r"\]\((/[^)]+)\)", c)
if len(links) < 2:
    errors.append(f"internal links = {len(links)}, need >= 2")

# 5. FAQ section with >= 3 H3
m = re.search(r"^## Frequently Asked Questions$(.*)^## ", c, re.M | re.S)
faq = m.group(1) if m else ""
h3s = re.findall(r"^### .+$", faq, re.M)
if len(h3s) < 3:
    errors.append(f"FAQ H3 count = {len(h3s)}")

# 6. Markdown tables >= 4 rows x 4 cols
tables = []
cur = []
for line in c.split("\n"):
    if line.strip().startswith("|"):
        cur.append(line.strip())
    else:
        if len(cur) >= 4:
            tables.append(cur)
        cur = []
if len(cur) >= 4:
    tables.append(cur)
big = 0
for t in tables:
    cols = t[0].count("|") - 1
    if len(t) - 2 >= 4 and cols >= 4:
        big += 1
if big < 1:
    errors.append("no comparison table with >=4 data rows and >=4 columns")
print(f"tables found: {len(tables)}, big tables (>=4x4): {big}")

# 7. Data-backed opening
first = c.split(". ")[0]
if "$" not in first:
    warns.append("opening sentence lacks a $ figure")

# 8. Link targets exist on disk
for l in links:
    p = l.lstrip("/").rstrip("/")
    if not (os.path.isdir(p) or os.path.exists(p + ".html") or os.path.exists(p)):
        errors.append("broken internal link path: " + l)

# 9. Long-tail body placement
for lt in LONGTAILS:
    n = len(re.findall(re.escape(lt), c, re.I))
    print(f"longtail [{lt}]: {n}")
    if n == 0:
        errors.append(f"longtail missing from body: {lt}")

# 10. PK substring-trap guard: body must NOT contain 'vercel serverless functions pricing'
if re.search(re.escape("vercel " + PK), c, re.I):
    errors.append("substring trap: 'vercel serverless functions pricing' in body inflates PK count")

print("word count (split):", wc)
print("PK count:", pk_count)
print("internal links:", len(links))
print("FAQ H3s:", len(h3s))
if warns:
    print("WARNINGS:", warns)
if errors:
    print("FAILURES:")
    for e in errors:
        print(" -", e)
    raise SystemExit(1)
print("ALL CHECKS PASSED")
