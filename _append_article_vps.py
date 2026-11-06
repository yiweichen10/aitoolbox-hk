# -*- coding: utf-8 -*-
"""Append VPS hosting article to articles_en.json with full self-check (check BEFORE save)."""
import json, re, sys

BASE = r"C:\Users\27040\WorkBuddy\20260321092139\seo-site-en"
SRC = BASE + r"\_tmp_vps_article.md"
DST = BASE + r"\data\articles_en.json"

SLUG = "best-vps-hosting-2026-hetzner-vs-digitalocean-vs-vultr-vs-linode"

entry = {
    "title": "Best VPS Hosting in 2026: Hetzner vs DigitalOcean vs Vultr vs Linode",
    "slug": SLUG,
    "date": "2026-11-06",
    "dateFull": "November 6, 2026",
    "category": "AI Infrastructure",
    "description": ("Hetzner vs DigitalOcean vs Vultr vs Linode on real 2026 pricing: entry-tier specs, "
                    "egress overage math, managed ecosystem trade-offs, and which cheap VPS fits side "
                    "projects, EU-first products, and global traffic-heavy apps."),
    "keywords": [
        "VPS hosting",
        "Hetzner vs DigitalOcean",
        "Hetzner pricing",
        "DigitalOcean pricing",
        "Vultr vs Hetzner",
        "Linode pricing",
        "cheapest VPS hosting",
        "best VPS for developers",
        "DigitalOcean alternative",
    ],
}

with open(SRC, encoding="utf-8") as f:
    content = f.read().strip()

entry["content"] = content

errors = []

# 1. PK count (case-insensitive) must be exactly 4 in content
pk = "VPS hosting"
n_pk = len(re.findall(re.escape(pk), content, flags=re.IGNORECASE))
if n_pk != 4:
    errors.append(f"PK '{pk}' count = {n_pk}, expected exactly 4")

# 2. Banned words
banned = ["leverage", "utilize", "seamlessly", "game-changing", "game changing", "empower",
          "streamline", "delve", "transformative", "comprehensive", "revolutionize",
          "cutting-edge", "cutting edge", "as an AI", "in conclusion", "unleash", "robust"]
low = content.lower()
for w in banned:
    if w in low:
        errors.append(f"BANNED WORD found: '{w}'")

# 3. Word count 2200-2800
wc = len(content.split())
if not (2200 <= wc <= 2800):
    errors.append(f"Word count = {wc}, expected 2200-2800")

# 4. Internal links >= 2, all targets exist
links = re.findall(r"\]\(/articles/([a-z0-9\-]+)\)", content)
if len(links) < 2:
    errors.append(f"Internal links = {len(links)}, expected >= 2")
with open(DST, encoding="utf-8") as f:
    arts = json.load(f)
existing_slugs = {a["slug"] for a in arts}
for l in links:
    if l not in existing_slugs:
        errors.append(f"Internal link target NOT FOUND: {l}")

# 5. FAQ: H2 'Frequently Asked Questions' + >= 3 H3
if "## Frequently Asked Questions" not in content:
    errors.append("Missing H2 'Frequently Asked Questions'")
h3s = re.findall(r"^### (.+)$", content, flags=re.M)
if len(h3s) < 3:
    errors.append(f"H3 count = {len(h3s)}, expected >= 3")

# 6. At least one markdown table with >= 4 rows and >= 4 columns
tables = []
cur = []
for line in content.splitlines():
    if line.strip().startswith("|"):
        cur.append(line)
    else:
        if len(cur) >= 5:  # header + sep + >=3 data rows
            tables.append(cur)
        cur = []
if len(cur) >= 5:
    tables.append(cur)
ok_table = False
for t in tables:
    ncols = t[0].count("|") - 1
    nrows = len(t) - 2  # minus header & separator
    if ncols >= 4 and nrows >= 4:
        ok_table = True
        break
if not ok_table:
    errors.append("No markdown table with >= 4 data rows and >= 4 columns")

# 7. Slug uniqueness
if SLUG in existing_slugs:
    errors.append(f"Slug already exists: {SLUG}")

if errors:
    print("SELF-CHECK FAILED:")
    for e in errors:
        print("  -", e)
    sys.exit(1)

arts.append(entry)
with open(DST, "w", encoding="utf-8") as f:
    json.dump(arts, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"SELF-CHECK PASSED: PK={n_pk}, words={wc}, links={len(links)} (all exist), H3={len(h3s)}, tables={len(tables)}")
print(f"Article #{len(arts)} appended -> {DST}")
