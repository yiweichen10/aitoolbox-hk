#!/usr/bin/env python3
"""fix_price_labels.py — 把超长 price 字段重塑为短标签 + 长描述入 pricing_details

规则（用户 2026-08-05 指令：禁止治标，必须治本）：
- price 字段 = 卡片/徽章用短价格标签（<=50 字符），语义化，非机械截断
- 原长 price 文本整体移入 pricing_details 字段保留（正文已覆盖价格，该字段为结构化备份）

历史：
- 2026-08-05 首轮修复 23 条（SHORT_MAP v1）
- 2026-09-07 二轮修复 20 条复发（SHORT_MAP v2，根因=生产线无闸门，见 seo-data-field-governance 类型 G）
  本脚本保留可复用：新增条目直接往 SHORT_MAP 加 slug->短标签 再跑。
"""
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_FILE = os.path.join(BASE_DIR, "data", "tools_en.json")

# 语义化短标签（AI 基于完整价格文本提炼，<=50 字符）
# v2 — 2026-09-07 复发批次（20 条）
SHORT_MAP = {
    "anythingllm":  "Free desktop + Cloud from $50/mo",
    "jenni-ai":     "Free + Plus from $12/mo",
    "aiprm":        "Free + Plus from ~$10/mo",
    "retool-ai":    "Free + Team $10/builder/mo",
    "wix-ai":       "Free + Light from $17/mo",
    "magnific-ai":  "From $39/mo (no free tier)",
    "gptzero":      "Free + Essential from $14.99/mo",
    "kaiber":       "Free + paid from ~$15/mo",
    "vidu-ai":      "Free + Standard from ~$8/mo",
    "seedance":     "Free daily credits + Basic ~$18/mo",
    "fireflies-ai": "Free + Pro from $10/seat/mo",
    "scalenut":     "From $59/mo (trial only, no free)",
    "lets-enhance": "10 free credits + Starter $9/mo",
    "manus":        "Free credits + Starter from $20/mo",
    "goldfish":     "Free during alpha (2026-08)",
    "genspark":     "Free daily credits + Plus ~$24/mo",
    "krea-2":       "Free + Basic from $9/mo",
    "durable":      "Free + Launch from $25/mo",
    "buffer":       "Free (3 channels) + ~$6/channel",
    "stan-store":   "From $29/mo (14-day trial)",
}


def main():
    tools = json.load(open(TOOLS_FILE, encoding="utf-8"))
    fixed = 0
    for t in tools:
        slug = t.get("slug", "")
        if slug in SHORT_MAP:
            old = t.get("price", "")
            # 原长文整体保留到 pricing_details（仅当尚未存在，避免覆盖）
            if "pricing_details" not in t and len(old) > len(SHORT_MAP[slug]):
                t["pricing_details"] = old
            if old != SHORT_MAP[slug]:
                t["price"] = SHORT_MAP[slug]
                fixed += 1
                print(f"  [OK] {slug}: {len(old)} -> {len(SHORT_MAP[slug])} chars | {SHORT_MAP[slug]}")
    json.dump(tools, open(TOOLS_FILE, "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"\nSaved. Fixed {fixed} tools.")

    # 校验：不应再有超长 price
    over = [(t['slug'], len(t['price'])) for t in tools if len(t.get('price', '')) > 80]
    if over:
        print(f"WARNING: {len(over)} tools still have price > 80 chars: {over}")
    else:
        print("VALIDATION PASS: no price field exceeds 80 chars.")


if __name__ == "__main__":
    main()
