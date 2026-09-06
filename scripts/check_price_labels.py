#!/usr/bin/env python3
"""check_price_labels.py — 复查命令（G4 固化）：1 条命令确认 price 字段治理未复发

退出码 0 = 干净；1 = 有污染（可直接挂进自动化收尾检查）。
"""
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_FILE = os.path.join(BASE_DIR, "data", "tools_en.json")

tools = json.load(open(TOOLS_FILE, encoding="utf-8"))
bad = [(t["slug"], len(t.get("price", ""))) for t in tools if len(t.get("price", "") or "") > 80]
if bad:
    print(f"FAIL: {len(bad)} tools with price > 80 chars:")
    for s, l in sorted(bad, key=lambda x: -x[1]):
        print(f"  - {s} ({l})")
    sys.exit(1)
longish = [(t["slug"], len(t["price"])) for t in tools if 50 < len(t.get("price", "") or "") <= 80]
print(f"PASS: {len(tools)} tools, 0 polluted." + (f" ({len(longish)} in 50-80 gray zone)" if longish else ""))
