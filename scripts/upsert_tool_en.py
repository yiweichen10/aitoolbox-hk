#!/usr/bin/env python3
"""upsert_tool_en.py — 英文站工具入库统一入口（所有写入必须走这里，禁止裸 json.dump）

用法：
  python scripts/upsert_tool_en.py tool.json          # 单个工具对象
  python scripts/upsert_tool_en.py tools.json         # 工具数组
  cat tool.json | python scripts/upsert_tool_en.py -  # stdin

规则（2026-09-07 治理，防价格污染复发，见技能 seo-data-field-governance 类型 G）：
- price 字段必须是短价格标签（<=50 建议、>80 拒绝入库），如 "Free + Pro from $19/mo"
- 长价格说明放 pricing_details 字段
- 按 slug upsert：已存在则合并更新，不存在则追加
- 自动备份 data/tools_en.json -> data/tools_en.json.upsert.bak
"""
import json
import os
import shutil
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_FILE = os.path.join(BASE_DIR, "data", "tools_en.json")

REQUIRED_FIELDS = ("name", "slug", "url", "category", "description")
PRICE_HARD_LIMIT = 80   # 超过直接拒绝
PRICE_SOFT_LIMIT = 50   # 超过打印建议


def validate(tool: dict) -> list:
    errs = []
    slug = tool.get("slug", "?")
    for f in REQUIRED_FIELDS:
        if not (tool.get(f) or "").strip() if isinstance(tool.get(f), str) else not tool.get(f):
            errs.append(f"{slug}: missing required field '{f}'")
    price = tool.get("price", "") or ""
    if len(price) > PRICE_HARD_LIMIT:
        errs.append(
            f"{slug}: price is {len(price)} chars (>{PRICE_HARD_LIMIT}). "
            f"price MUST be a short card label like 'Free + Pro from $19/mo'. "
            f"Move full pricing text into 'pricing_details'."
        )
    elif len(price) > PRICE_SOFT_LIMIT:
        print(f"  [hint] {slug}: price {len(price)} chars (>50). Consider a shorter label.")
    if len(tool.get("description", "") or "") < 40:
        errs.append(f"{slug}: description too short (<40 chars)")
    return errs


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    arg = sys.argv[1]
    raw = sys.stdin.read() if arg == "-" else open(arg, encoding="utf-8").read()
    data = json.loads(raw)
    tools_in = data if isinstance(data, list) else [data]

    all_errs = [e for t in tools_in for e in validate(t)]
    if all_errs:
        print("REJECTED — fix before writing:")
        for e in all_errs:
            print(f"  ✗ {e}")
        sys.exit(1)

    existing = json.load(open(TOOLS_FILE, encoding="utf-8"))
    shutil.copy2(TOOLS_FILE, TOOLS_FILE.replace(".json", ".upsert.bak"))
    index = {t["slug"]: i for i, t in enumerate(existing)}
    added = updated = 0
    for t in tools_in:
        if t["slug"] in index:
            existing[index[t["slug"]]].update(t)
            updated += 1
        else:
            t.setdefault("published", True)
            existing.append(t)
            index[t["slug"]] = len(existing) - 1
            added += 1
    json.dump(existing, open(TOOLS_FILE, "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"OK: {added} added, {updated} updated. total={len(existing)} tools.")


if __name__ == "__main__":
    main()
