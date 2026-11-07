"""Self-check for article #215 before appending to articles_en.json."""
import os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
md_path = os.path.join(BASE, "scripts", "_tmp_article_215.md")
with open(md_path, "r", encoding="utf-8") as f:
    content = f.read()

errors, warnings = [], []

# 1. PK count: exactly 4
PK = "Heroku alternatives"
pk_count = content.count(PK)
print(f"[PK] '{PK}' occurrences: {pk_count} {'OK' if pk_count == 4 else 'FAIL (need exactly 4)'}")
if pk_count != 4:
    errors.append("PK count != 4")

# PK placement: intro (before first H2), H2, body, conclusion (last paragraph)
first_h2 = content.find("\n## ")
intro = content[:first_h2]
h2s = re.findall(r"^## .+$", content, re.M)
last_para_start = content.rfind("\n")
bottom_line_zone = content[content.rfind("Bottom line:"):]
print(f"[PK] in intro: {PK in intro}")
print(f"[PK] in an H2: {any(PK in h for h in h2s)}")
print(f"[PK] in bottom line: {PK in bottom_line_zone}")
if PK not in intro: errors.append("PK missing in intro")
if not any(PK in h for h in h2s): errors.append("PK missing in H2")
if PK not in bottom_line_zone: errors.append("PK missing in bottom line")

# 2. Banned words
BANNED = ["leverage", "utilize", "seamlessly", "game-changing", "empower", "streamline",
          "delve into", "transformative", "comprehensive", "revolutionize", "cutting-edge",
          "as an AI", "in conclusion", "In conclusion"]
low = content.lower()
hits = [w for w in BANNED if w.lower() in low]
print(f"[BANNED] hits: {hits if hits else 'none (OK)'}")
if hits: errors.append(f"Banned words found: {hits}")

# 3. Word count
words = len(content.split())
print(f"[WORDS] {words} {'OK' if 2200 <= words <= 2800 else 'FAIL (2200-2800)'}")
if not (2200 <= words <= 2800): errors.append(f"word count {words} out of range")

# 4. FAQ section with >= 3 H3
faq_pos = content.lower().find("## frequently asked questions")
h3s_after = re.findall(r"^### .+$", content[faq_pos:], re.M) if faq_pos >= 0 else []
print(f"[FAQ] section exists: {faq_pos >= 0}, H3 count after FAQ H2: {len(h3s_after)}")
if faq_pos < 0: errors.append("missing FAQ H2")
if len(h3s_after) < 3: errors.append("FAQ H3 < 3")

# 5. Tables: at least one with >=4 rows and >=4 cols
tables = re.findall(r"(?:^\|.*\|\s*$\n?)+", content, re.M)
best = 0
for t in tables:
    rows = [r for r in t.strip().split("\n")]
    data_rows = [r for r in rows if not re.match(r"^\|[\s\-|:]+\|$", r)]
    cols = data_rows[0].strip().strip("|").count("|") + 1 if data_rows else 0
    best = max(best, len(data_rows) * 100 + cols)
    print(f"[TABLE] {len(data_rows)} data rows x {cols} cols")
if best < 4 * 100 + 4:
    errors.append("no table with >=4 rows and >=4 cols")

# 6. Internal links: >=2, targets exist
links = re.findall(r"\]\((/articles/[^)]+|/tools/[^)]+)\)", content)
print(f"[LINKS] internal links: {len(links)}")
for l in links:
    if l.startswith("/articles/"):
        p = os.path.join(BASE, "articles", l[len("/articles/"):].strip("/"))
        ok = os.path.isdir(p)
        print(f"   {l} -> exists: {ok}")
        if not ok: errors.append(f"broken article link: {l}")
    else:
        p = os.path.join(BASE, "tools", l[len("/tools/"):].strip("/"))
        ok = os.path.isdir(p)
        print(f"   {l} -> exists: {ok}")
        if not ok: errors.append(f"broken tool link: {l}")
if len(links) < 2: errors.append("internal links < 2")

# 7. Long-tail keyword presence (case-insensitive)
LONGTAILS = ["railway vs render", "railway pricing", "render pricing", "fly.io pricing",
             "heroku pricing", "cheapest heroku alternative", "usage-based pricing",
             "eco dyno", "render vs railway", "fly.io vs railway"]
for lt in LONGTAILS:
    n = low.count(lt)
    print(f"[LT] '{lt}': {n} {'OK' if n >= 1 else 'MISSING'}")
    if n == 0: warnings.append(f"long-tail missing: {lt}")

# 8. Duplicate heading check (build_en may reject or SEO prefers unique)
h2_all = [h.lower() for h in h2s]
if len(h2_all) != len(set(h2_all)):
    errors.append("duplicate H2 headings")

print("\n=== RESULT ===")
if errors:
    print("ERRORS:")
    for e in errors: print(" -", e)
    sys.exit(1)
print("ALL CHECKS PASSED" + (f" | warnings: {warnings}" if warnings else ""))
