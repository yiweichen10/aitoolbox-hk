#!/usr/bin/env python3
"""fix_price_labels.py — 治本：把超长 price 字段重塑为短标签 + 长描述入 pricing_details

规则（用户 2026-08-05 指令：禁止治标，必须治本）：
- price 字段 = 卡片/徽章用短价格标签（<=50 字符），语义化，非机械截断
- 原长 price 文本整体移入 pricing_details 字段保留（正文已覆盖价格，该字段为结构化备份）
"""
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_FILE = os.path.join(BASE_DIR, "data", "tools_en.json")

# 语义化短标签（由 AI 基于完整价格文本提炼，<=50 字符）
SHORT_MAP = {
    "semrush-ai": "Free + Pro from $139.95/mo",
    "relevance-ai": "Free + Pro from $49/mo",
    "cartesia": "Free + Pro from $19/mo",
    "milvus": "Free (open source) + Cloud $0.80/hr",
    "webflow-ai": "Free + Core from $29/mo",
    "weaviate": "Free (self-host) + Cloud $25/mo",
    "looka": "From $20 (pay per download)",
    "wordtune": "Free + Plus from $9.99/mo",
    "anyword": "From $39/mo (no free plan)",
    "kapwing": "Free + Pro from $16/mo",
    "soundraw": "Free + Creator from $16.99/mo",
    "aiva": "Free + Pro from EUR33/mo",
    "wondercraft-ai": "Free + Creator from $25/mo",
    "topaz-photo-ai": "From $199 one-time",
    "raycast-ai": "Free + Pro from $8/mo",
    "miro-ai": "Free + Starter $8/seat/mo",
    "murf-ai": "Free + Creator from $19/mo",
    "cleanvoice": "Free trial + from $2.20/hr",
    "voiceflow": "Free + Pro from $60/mo",
    "fathom": "Free + Premium from $20/mo",
    "languagetool": "Free + Premium from $24.90/mo",
    "exa-ai": "Pay-as-you-go from $7/1K req",
    "elicit": "Free + Pro from $49/user/mo",
}


def main():
    tools = json.load(open(TOOLS_FILE, encoding="utf-8"))
    fixed = 0
    for t in tools:
        slug = t.get("slug", "")
        if slug in SHORT_MAP:
            old = t.get("price", "")
            # 原长文整体保留到 pricing_details（仅当尚未存在，避免覆盖）
            if "pricing_details" not in t and old != SHORT_MAP[slug]:
                t["pricing_details"] = old
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
