import re, sys

PK = "ai ad spy tools 2026"
LONGTAIL = [
    "bigspy pricing", "adspy vs bigspy", "poweradspy pricing", "anstrex native ads",
    "best ad spy tool for facebook", "tiktok ad spy tool", "ad spy free",
    "competitor ad intelligence", "facebook ad library alternative", "ad spy tool for dropshipping",
]
BANNED = ["leverage", "utilize", "seamlessly", "game-changing", "empower", "streamline",
          "delve into", "transformative", "comprehensive", "revolutionize", "cutting-edge",
          "as an ai", "in conclusion"]

raw = open("_article_145_draft.txt", encoding="utf-8").read()
content = raw.split("\n---\n", 1)[1].strip()

words = len(content.split())
pk_count = content.lower().count(PK)
banned_hits = [b for b in BANNED if re.search(r"\b"+re.escape(b)+r"\b", content.lower())]
longtail_hits = {lt: content.lower().count(lt) for lt in LONGTAIL}
internal = re.findall(r"\[[^\]]+\]\((/(?:articles|tools)/[^)]+)\)", content)

# table check
lines = content.split("\n")
table_rows = [l for l in lines if l.strip().startswith("|") and "---" not in l]
data_rows = [l for l in table_rows if not set(l.strip()) <= set("|- ")]
cols = [len([c for c in l.strip().strip("|").split("|")]) for l in data_rows]
table_ok = len(data_rows) >= 4 and min(cols) >= 4

# FAQ check
h2 = re.findall(r"^## (.+)$", content, re.M)
h3 = re.findall(r"^### (.+)$", content, re.M)
faq_h2 = any("frequently asked questions" in x.lower() for x in h2)
faq_h3 = [x for x in h3 if any(f in content[content.lower().find("frequently asked questions"):].lower() for f in [x.lower()])]

print("WORD COUNT:", words, "OK" if 2200 <= words <= 2800 else "FAIL")
print("PK COUNT:", pk_count, "OK" if pk_count == 4 else "FAIL")
print("BANNED:", banned_hits if banned_hits else "NONE OK")
print("LONGTAIL MISSING:", [lt for lt,c in longtail_hits.items() if c == 0] or "ALL OK")
print("INTERNAL LINKS:", len(internal), internal)
print("TABLE rows/cols:", len(data_rows), cols, "OK" if table_ok else "FAIL")
print("FAQ H2:", faq_h2, "| H3 count in FAQ:", len([x for x in h3]))
print("H2 list:", h2)

ok = (2200 <= words <= 2800 and pk_count == 4 and not banned_hits
      and all(c>0 for c in longtail_hits.values()) and len(internal) >= 2
      and table_ok and faq_h2 and len(h3) >= 3)
print("\nRESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
