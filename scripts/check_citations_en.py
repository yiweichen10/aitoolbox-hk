#!/usr/bin/env python3
"""Fabricated-citation detector for EN articles (2026-11-23).

Flags the three fabrication patterns discovered in our own content audit:
  1. Invented report names — "2026 State of X", "2026 <Org> study/survey"
  2. Institution + precise percentage claims (need human verification)
  3. Named-person quotes with attribution (need verification)

This is a SOFT warning tool: it does NOT block builds (some flagged claims are
genuine, e.g. "Salesforce 28%"). Use it after content generation to focus a
manual fact-check on the highest-risk sentences. Exit code is always 0.

Usage:
  python scripts/check_citations_en.py                # scan all articles
  python scripts/check_citations_en.py <slug>          # scan one article
"""
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
arts = json.loads((BASE / "data/articles_en.json").read_text(encoding="utf-8"))

# Pattern 1: invented "2026 State of X" report names — the audit found these
# were consistently fabricated. Real "State of the API 2025" (Postman) etc.
# carry a source link, so skip a match whose sentence already has a URL.
FABRICATED_REPORT = re.compile(
    r"\b2026\s+State of\s+[A-Z][\w\s]{2,40}?(?:report|study|survey)?",
)
# Pattern 2: "2026 <Institution> study/survey/found ... N%" — verify manually
INSTITUTION_STAT = re.compile(
    r"(?:20\d\d\s+)?([A-Z][a-zA-Z&.]+(?:\s+[A-Z][a-zA-Z&.]+){0,3})"
    r"\s+(?:study|survey|report|research|benchmark|index|institute)"
    r"[^.]{0,110}?\b(\d{1,3}(?:\.\d+)?%)",
)
# Pattern 3: attributed quotes to named individuals
NAMED_QUOTE = re.compile(r'"[^"]{20,200}"\s*[—–-]{1,2}\s*[A-Z][a-z]+\s+[A-Z][a-z]+')


def sentence_at(text: str, pos: int) -> str:
    start = pos
    for j in range(pos - 1, max(-1, pos - 300), -1):
        if text[j] in ".!?\n":
            start = j + 1
            break
    end = text.find(".", pos)
    while end > 0 and end + 1 < len(text) and text[end + 1].isdigit():
        end = text.find(".", end + 1)
    return text[start:end + 1 if end > 0 else pos + 120].strip().replace("\n", " ")


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None
    pool = [a for a in arts if not target or a["slug"] == target]
    total = {1: 0, 2: 0, 3: 0}
    for a in pool:
        content = a.get("content", "")
        hits = []
        for m in FABRICATED_REPORT.finditer(content):
            hits.append((1, "虚构报告名", sentence_at(content, m.start())))
        for m in INSTITUTION_STAT.finditer(content):
            hits.append((2, f"机构+数字 {m.group(1)}·{m.group(2)}", sentence_at(content, m.start())))
        for m in NAMED_QUOTE.finditer(content):
            hits.append((3, "具名人物引语", sentence_at(content, m.start())))
        if hits:
            print(f"\n[{a['slug']}] {len(hits)} 处待核：")
            seen = set()
            for kind, label, sent in hits:
                if sent in seen:
                    continue
                seen.add(sent)
                total[kind] += 1
                print(f"  P{kind} {label}: {sent[:160]}")
    print(f"\n[SUMMARY] P1虚构报告名 {total[1]} | P2机构+数字 {total[2]} | P3具名引语 {total[3]}")
    print("[NOTE] 仅提示待核，不判定真伪 — 真实引用也会被 P2/P3 命中。退出码恒为 0。")
    sys.exit(0)


if __name__ == "__main__":
    main()
