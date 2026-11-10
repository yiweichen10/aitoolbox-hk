# -*- coding: utf-8 -*-
"""Self-check for article #218 against SEO/GEO/quality rules."""
import re
import importlib.util

spec = importlib.util.spec_from_file_location("art", "_append_article_218.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
A = mod.ARTICLE
content = A["content"]

fails = []

# 1. Primary keyword exactly 4x (case-insensitive)
pk = "managed kubernetes"
pk_count = len(re.findall(re.escape(pk), content, re.I))
print(f"[PK] '{pk}' occurrences in content: {pk_count} (must be exactly 4)")
if pk_count != 4:
    fails.append(f"PK count = {pk_count}, expected 4")

# 2. Banned words
banned = ["leverage", "utilize", "utilisation", "utilization", "seamlessly", "seamless",
          "game-changing", "game changer", "empower", "streamline", "delve",
          "transformative", "comprehensive", "revolutionize", "cutting-edge",
          "as an AI", "in conclusion"]
low = content.lower()
for w in banned:
    if w.lower() in low:
        ctx = low[max(0, low.find(w.lower()) - 40): low.find(w.lower()) + 60]
        fails.append(f"BANNED WORD found: '{w}' ...{ctx}...")
print(f"[BANNED] scanned {len(banned)} terms -> {'CLEAN' if not any('BANNED' in f for f in fails) else 'VIOLATION'}")

# 3. Word count (split method)
wc = len(content.split())
print(f"[WORDS] {wc} (must be 2200-2800)")
if not (2200 <= wc <= 2800):
    fails.append(f"word count {wc} out of range")

# 4. Internal links to aitoolbox articles/tools
links = re.findall(r"\]\((/articles/[^)]+|/tools/[^)]+)\)", content)
print(f"[LINKS] internal links: {len(links)}")
for l in links:
    print("   ", l)
if len(links) < 2:
    fails.append(f"only {len(links)} internal links")

# 5. FAQ H3 headings
h3s = re.findall(r"^### (.+)$", content, re.M)
print(f"[FAQ] H3 headings: {len(h3s)}")
for h in h3s:
    print("   ", h)
if len(h3s) < 3:
    fails.append("FAQ needs >=3 H3")

# 6. Tables: >=1 table with >=4 rows and >=4 cols
blocks = re.findall(r"((?:^\|.+\|\s*\n)+)", content, re.M)
tables = []
for b in blocks:
    rows = [r for r in b.strip().split("\n") if not re.match(r"^\|[\s\-|]+\|$", r)]
    cols = rows[0].count("|") - 1
    tables.append((len(rows), cols))
print(f"[TABLES] {len(tables)} tables -> " + ", ".join(f"{r}rows x {c}cols" for r, c in tables))
if not any(r >= 4 and c >= 4 for r, c in tables):
    fails.append("no table with >=4 rows and >=4 cols")

# 7. Long-tail keyword spot check
longtails = ["amazon eks pricing", "gke pricing", "aks pricing", "doks pricing", "eks vs gke",
             "kubernetes control plane cost", "cheapest kubernetes hosting",
             "gke autopilot pricing", "extended support fee"]
present = [t for t in longtails if t in low]
print(f"[LONGTAILS] {len(present)}/{len(longtails)}: {present}")
if len(present) < 5:
    fails.append(f"only {len(present)} long-tails present")

# 8. Data-backed opening (first 200 chars contain a stat with % or $)
head = content[:300]
ok = ("90%" in head) and ("$" in head)
print(f"[GEO OPENING] data-backed stat in first 300 chars: {ok}")
if not ok:
    fails.append("opening lacks data-backed stat")

print("\n" + ("=" * 50))
if fails:
    print("FAILED CHECKS:")
    for f in fails:
        print("  -", f)
    raise SystemExit(1)
print("ALL CHECKS PASSED")
