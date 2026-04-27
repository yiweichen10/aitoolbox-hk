import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open("data/tools_en.json", "r", encoding="utf-8") as f:
    tools = json.load(f)

for t in tools:
    if t.get("slug") in ["tensor.art", "brandmark", "make"]:
        content = t.get("content", "")
        h3q = re.findall(r"^### .+", content, re.MULTILINE)
        has_q = [h for h in h3q if "?" in h]
        tbl = re.search(r"^\|.+\|", content, re.MULTILINE)
        print(f"{t['slug']}: H3={len(h3q)} Q?={len(has_q)} tbl={bool(tbl)}")
        if h3q:
            print("  h3 samples:", h3q[:2])
        else:
            raw = [l for l in content.split("\n") if "###" in l]
            print("  raw ### lines:", raw[:2])
        if not tbl:
            pipe_lines = [l for l in content.split("\n") if "|" in l]
            print("  pipe lines:", pipe_lines[:2])
        print()
