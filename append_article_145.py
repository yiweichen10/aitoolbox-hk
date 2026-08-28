import json, sys

DRAFT = "_article_145_draft.txt"
DATA = "data/articles_en.json"
PK = "ai ad spy tools 2026"

raw = open(DRAFT, encoding="utf-8").read()
head, _, body = raw.partition("\n---\n")
body = body.strip()

meta = {}
for line in head.strip().split("\n"):
    if ":" in line:
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip()

required = ["TITLE", "SLUG", "CATEGORY", "DATE", "DESCRIPTION", "KEYWORDS"]
for r in required:
    if r not in meta:
        print("MISSING META:", r); sys.exit(1)

content = body
if content.startswith("TITLE:"):
    print("META LEAK: content starts with TITLE:"); sys.exit(1)

d = json.load(open(DATA, encoding="utf-8"))
slugs = [a["slug"] for a in d]
if meta["SLUG"] in slugs:
    print("SLUG COLLISION:", meta["SLUG"]); sys.exit(1)

article = {
    "title": meta["TITLE"],
    "slug": meta["SLUG"],
    "date": meta["DATE"],
    "dateFull": meta["DATE"],
    "category": meta["CATEGORY"],
    "description": meta["DESCRIPTION"],
    "keywords": meta["KEYWORDS"],
    "content": content,
}
d.append(article)
json.dump(d, open(DATA, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("APPENDED. total articles:", len(d))
print("PK in content count:", content.lower().count(PK))
print("content starts with:", content[:40].replace("\n", " "))
