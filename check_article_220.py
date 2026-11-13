# -*- coding: utf-8 -*-
"""Self-check for article #220 (CDN pricing)."""
import json
import re
import sys

SLUG = "best-cdn-pricing-2026-bunny-vs-cloudflare-vs-fastly-vs-cloudfront-compared"
PK = "cdn pricing"
BANNED = ["leverage", "utilize", "seamlessly", "game-changing", "empower",
          "streamline", "delve into", "transformative", "comprehensive",
          "revolutionize", "cutting-edge", "as an ai", "in conclusion"]
LONGTAILS = ["bunny cdn vs cloudflare", "cloudfront pricing", "fastly pricing",
             "cheapest cdn", "cdn for video streaming", "cloudfront flat-rate plans",
             "fastly alternatives", "cdn price comparison"]

arts = json.load(open("data/articles_en.json", encoding="utf-8"))
a = next(x for x in arts if x["slug"] == SLUG)
content = a["content"]
errors, warns = [], []

# 1. Primary keyword density (content only, case-insensitive, substring)
pk_count = content.lower().count(PK)
print(f"PK '{PK}' in content: {pk_count}x", "OK" if pk_count == 4 else "FAIL")
if pk_count != 4:
    errors.append(f"PK count {pk_count} != 4")

# 2. Banned words (whole-article, word-ish boundaries)
low = content.lower()
for w in BANNED:
    if w in low:
        errors.append(f"BANNED WORD: {w}")
print("Banned words:", "OK (0)" if not any("BANNED" in e for e in errors) else errors)

# 3. Word count (split method)
wc = len(content.split())
print(f"Word count (split): {wc}", "OK" if 2200 <= wc <= 2800 else "FAIL")
if not 2200 <= wc <= 2800:
    warns.append(f"Word count {wc} out of range")

# 4. Internal links exist
links = re.findall(r"\]\((/articles/[^)]+)\)", content)
all_slugs = {x["slug"] for x in arts}
print(f"Internal article links: {len(links)}")
for l in links:
    slug = l.rsplit("/", 1)[-1]
    ok = slug in all_slugs
    print("  ", l, "OK" if ok else "MISSING")
    if not ok:
        errors.append(f"Missing link target: {l}")
if len(links) < 2:
    errors.append("Fewer than 2 internal links")

# 5. FAQ structure
h2s = re.findall(r"^## (.+)$", content, re.M)
h3s = re.findall(r"^### (.+)$", content, re.M)
faq_ok = any("Frequently Asked Questions" in h for h in h2s)
print(f"H2s: {len(h2s)}, H3 FAQs: {len(h3s)}", "OK" if faq_ok and len(h3s) >= 3 else "FAIL")
if not (faq_ok and len(h3s) >= 3):
    errors.append("FAQ structure incomplete")

# 6. Tables >= 4 rows x 4 cols
tables = []
cur = []
for line in content.splitlines():
    if line.strip().startswith("|"):
        cur.append(line)
    else:
        if len(cur) >= 3:
            tables.append(cur)
        cur = []
if len(cur) >= 3:
    tables.append(cur)
print(f"Tables found: {len(tables)}")
for i, t in enumerate(tables, 1):
    rows = len(t) - 1  # minus header
    cols = max(row.count("|") - 1 for row in t)
    ok = rows >= 4 and cols >= 4
    print(f"  Table {i}: {rows} rows x {cols} cols", "OK" if ok else "FAIL")
    if not ok:
        errors.append(f"Table {i} too small: {rows}x{cols}")

# 7. Long-tail counts
for lt in LONGTAILS:
    n = low.count(lt)
    print(f"Long-tail '{lt}': {n}x")

# 8. Duplicate slug check
slugs = [x["slug"] for x in arts]
if slugs.count(SLUG) != 1:
    errors.append("Slug duplicated")

print("\n" + ("ALL CHECKS PASSED" if not errors else "ERRORS: " + "; ".join(errors)))
if warns:
    print("Warnings:", "; ".join(warns))
sys.exit(1 if errors else 0)
