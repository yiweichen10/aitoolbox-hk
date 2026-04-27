#!/usr/bin/env python3
"""Batch keyword research for all tool pages. Skips already-done slugs."""
import json, sys, time
from pathlib import Path
from kw_research import page_kw_plan

BASE   = Path(__file__).parent.parent
KW_DIR = BASE / "data" / "_kw"

tools  = json.loads((BASE / "data/tools_en.json").read_text(encoding="utf-8"))
slugs  = [t["slug"] for t in tools if t.get("published")]

done   = {p.stem for p in KW_DIR.glob("*.json")}
todo   = [s for s in slugs if s not in done]

limit  = int(sys.argv[1]) if len(sys.argv) > 1 else len(todo)
todo   = todo[:limit]

print(f"Already done: {len(done)} | To process: {len(todo)}")

for i, slug in enumerate(todo, 1):
    print(f"\n[{i}/{len(todo)}] {slug}")
    try:
        page_kw_plan(slug, kind="tool")
        time.sleep(1)
    except Exception as e:
        print(f"  ERROR: {e}")
        if "429" in str(e) or "rate" in str(e).lower():
            print("Rate limit hit — stopping.")
            break

print(f"\nDone. {KW_DIR}")
