#!/usr/bin/env python3
"""Fill missing pricing_details for tools — DERIVED from existing on-site data only.

Source material per tool (in priority order):
  1. `price` short label (build-gate enforced <=80 chars, e.g. 'Free + Plus $20/mo')
  2. FAQ answers that mention pricing ($, /mo, free tier, cost...)
Composition: '<price label>. <up to 2 pricing-relevant FAQ sentences>'.

ZERO-FABRICATION POLICY: this script never invents numbers. Tools whose
existing data yields no concrete pricing beyond the label are NOT padded —
they are reported to stdout for a human/web-research pass.

Usage: python scripts/enrich_pricing_details.py [--dry-run]
Backup: data/tools_en.json.bak-pricing (written once per run, before patch).
"""
import json
import re
import shutil
import sys
from pathlib import Path

TOOLS = Path("data/tools_en.json")
BACKUP = Path("data/tools_en.json.bak-pricing")

PRICE_Q = re.compile(r"(free|cost|price|pricing|much|plan|tier|pay|subscription|upgrade|billing)", re.I)
MONEY = re.compile(r"(\$\s?\d|\bfree\b|/mo\b|per month|per year|/year\b)", re.I)
_SENT = re.compile(r"(?<=[.!?])\s+")


def pricing_faq_sentences(faq) -> list:
    """Pricing-relevant sentences from FAQ answers, best (most numeric) first."""
    sents = []
    for item in (faq or []):
        if not isinstance(item, dict):
            continue
        ans = str(item.get("answer", "")).strip()
        if not ans:
            continue
        if not (PRICE_Q.search(str(item.get("question", ""))) or MONEY.search(ans)):
            continue
        for s in _SENT.split(ans):
            s = re.sub(r"^(yes|no)[,.]\s+", "", s.strip(), flags=re.I).strip()
            if MONEY.search(s):
                sents.append(s)
    # most informative first: sentences with $ figures outrank bare "free"
    sents.sort(key=lambda s: (0 if "$" in s else 1, -len(s)))
    return sents


def compose(tool) -> tuple[str, bool]:
    """Return (pricing_details, has_concrete_numbers)."""
    price = str(tool.get("price", "")).strip()
    parts = []
    if price:
        parts.append(price if price.endswith(".") else price + ".")
    sents = pricing_faq_sentences(tool.get("faq"))
    budget = 220 - len(" ".join(parts))
    taken = []
    for s in sents:
        if len(" ".join(taken + [s])) > budget:
            break
        taken.append(s)
        if len(taken) >= 2:
            break
    parts.extend(taken)
    detail = " ".join(parts).strip()
    if len(detail) > 260:  # hard cap, word boundary
        detail = detail[:260].rsplit(" ", 1)[0].rstrip(",;") + "…"
    concrete = bool(re.search(r"\$\s?\d", detail)) or bool(re.search(r"from \$|\d+/mo|\d+ per month", detail, re.I))
    return detail, concrete


def main():
    dry = "--dry-run" in sys.argv
    tools = json.loads(TOOLS.read_text(encoding="utf-8"))
    missing = [t for t in tools if not (t.get("pricing_details") or "").strip()]
    print(f"[ENRICH] {len(missing)}/{len(tools)} tools missing pricing_details")

    patched, need_research = [], []
    for t in missing:
        detail, concrete = compose(t)
        if not detail:
            need_research.append((t["slug"], t.get("price", ""), "no usable data at all"))
            continue
        patched.append((t["slug"], detail, concrete))
        if not concrete:
            need_research.append((t["slug"], t.get("price", ""), "no concrete numbers, label only"))

    if not dry:
        if not BACKUP.exists():
            shutil.copy2(TOOLS, BACKUP)
            print(f"[BACKUP] {BACKUP}")
        by_slug = {t["slug"]: t for t in tools}
        for slug, detail, _ in patched:
            by_slug[slug]["pricing_details"] = detail
        TOOLS.write_text(json.dumps(tools, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[PATCHED] {len(patched)} tools "
          f"(concrete numbers: {sum(1 for _, _, c in patched if c)}, label-only: {sum(1 for _, _, c in patched if not c)})")
    print("\n--- sample (first 6) ---")
    for slug, detail, concrete in patched[:6]:
        print(f"  [{slug}] {'OK ' if concrete else 'weak'} {detail[:150]}")
    if need_research:
        print(f"\n--- NEEDS WEB RESEARCH ({len(need_research)}) ---")
        for slug, price, why in need_research:
            print(f"  - {slug}  (price: {price!r}; {why})")
    print("\n[DONE]" + (" (dry-run, nothing written)" if dry else ""))


if __name__ == "__main__":
    main()
