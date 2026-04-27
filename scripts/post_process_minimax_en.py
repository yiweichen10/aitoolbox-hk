#!/usr/bin/env python3
"""
Post-process MiniMax-generated drafts to reach Accio-level quality.

Fixes:
  1. Primary KW in H2  — prepend "{Tool} Review: " to first H2 if PK missing
  2. Internal links    — replace first plain mention of each tool name with [Name](/slug/)
  3. Final-para PK     — ensure primary KW appears in last paragraph

Usage:
  python scripts/post_process_minimax.py <draft_path> <tool_slug>

Example:
  python scripts/post_process_minimax.py data/_drafts_en/chatgpt-minimax.md chatgpt
"""

import re, sys, json
from pathlib import Path

# ── load tool registry ──────────────────────────────────────────────────────
TOOLS_DB = Path("data/tools_en.json")

def load_tools():
    data = json.loads(TOOLS_DB.read_text(encoding="utf-8"))
    # {name: slug}, longest names first to avoid partial matches
    mapping = {t["name"]: t["slug"] for t in data if t.get("name") and t.get("slug")}
    return dict(sorted(mapping.items(), key=lambda x: -len(x[0])))

# ── fix 1: ensure primary KW in first H2 ───────────────────────────────────
def fix_pk_in_h2(text: str, tool_name: str, primary_kw: str) -> tuple[str, bool]:
    h2s = re.findall(r'^(## .+)$', text, re.MULTILINE)
    if not h2s:
        return text, False
    first_h2 = h2s[0]
    if primary_kw.lower() in first_h2.lower():
        return text, True  # already there
    # Rename: "## What X Does" → "## X Review: What It Does"
    old_title = first_h2[3:].strip()
    # strip leading "What {tool_name}" → keep remainder
    remainder = re.sub(rf'^what\s+{re.escape(tool_name)}\s*', '', old_title, flags=re.IGNORECASE).strip()
    if remainder:
        new_h2 = f"## {tool_name} Review: {remainder}"
    else:
        new_h2 = f"## {tool_name} Review: Features and Capabilities"
    text = text.replace(first_h2, new_h2, 1)
    return text, True

# ── fix 2: inject internal links ──────────────────────────────────────────
def inject_internal_links(text: str, current_slug: str, tools: dict) -> tuple[str, list]:
    injected = []
    for name, slug in tools.items():
        if slug == current_slug:
            continue  # don't link to self
        # already linked?
        if f"[{name}](/{slug}/)" in text:
            continue
        # find first plain occurrence (not inside [] or already in a link)
        # pattern: name not preceded by [ and not inside existing markdown link
        pattern = rf'(?<!\[)(?<!\/)(?<!\w){re.escape(name)}(?!\w)(?!\])'
        m = re.search(pattern, text)
        if m:
            # replace only first occurrence
            text = text[:m.start()] + f"[{name}](/{slug}/)" + text[m.end():]
            injected.append(name)
    return text, injected

# ── fix 3: ensure PK in final paragraph ────────────────────────────────────
def fix_pk_in_final_para(text: str, primary_kw: str) -> tuple[str, bool]:
    paras = [p.strip() for p in text.strip().split('\n\n') if p.strip() and not p.strip().startswith('#')]
    if not paras:
        return text, False
    last_para = paras[-1]
    if primary_kw.lower() in last_para.lower():
        return text, True
    # append a natural sentence
    sentences = last_para.rstrip('.').split('.')
    appended = text.rstrip() + f"\n\nBottom line of this {primary_kw}: honest strengths, real limitations — try the free tier first."
    return appended, True

# ── QA report ──────────────────────────────────────────────────────────────
def qa_report(text: str, primary_kw: str, tool_slug: str):
    cl = text.lower()
    AI_SMELL = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
                'delve into','dive into','transformative','comprehensive',
                'it is worth noting','in conclusion','as an ai','in today']
    smell   = [(w, cl.count(w)) for w in AI_SMELL if cl.count(w) > 0]
    pk      = primary_kw.lower()
    pk_cnt  = cl.count(pk)
    first100 = ' '.join(text.split()[:100]).lower()
    h2s     = re.findall(r'^## .+', text, re.MULTILINE)
    h3q     = [h for h in re.findall(r'^### .+', text, re.MULTILINE) if '?' in h]
    table   = bool(re.search(r'^\|.+\|', text, re.MULTILINE))
    links   = re.findall(r'\[([^\]]+)\]\(/[a-z0-9.-]+/\)', text)
    paras   = [p for p in text.strip().split('\n\n') if p.strip() and not p.strip().startswith('#')]
    last_pk = pk in paras[-1].lower() if paras else False
    pk_h2   = any(pk in h.lower() for h in h2s)
    words   = len(text.split())

    print(f"\n=== POST-PROCESS QA: {tool_slug} ({words}w) ===")
    print(f"  AI smell  : {'CLEAN' if not smell else smell}")
    print(f"  PK x{pk_cnt}    : first100={pk in first100} | h2={pk_h2} | last_para={last_pk}")
    print(f"  H2 ({len(h2s)})   : {[h[3:55] for h in h2s]}")
    print(f"  FAQ H3+?  : {len(h3q)}")
    print(f"  Table     : {table}")
    print(f"  Int links : {links}")
    pass_all = (
        not smell and
        pk_cnt >= 3 and
        (pk in first100) and pk_h2 and last_pk and
        len(h3q) >= 3 and
        table and
        len(links) >= 3
    )
    print(f"\n  RESULT: {'ALL PASS' if pass_all else 'NEEDS REVIEW'}")
    return pass_all

# ── main ───────────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 3:
        print("Usage: python post_process_minimax.py <draft_path> <tool_slug>")
        sys.exit(1)

    draft_path  = Path(sys.argv[1])
    tool_slug   = sys.argv[2]
    tools       = load_tools()

    if tool_slug not in tools.values():
        print(f"Warning: '{tool_slug}' not found in tools_en.json — proceeding anyway")

    # Derive tool_name and primary_kw from slug
    tool_name   = next((n for n, s in tools.items() if s == tool_slug), tool_slug.replace('-', ' ').title())
    primary_kw  = f"{tool_name} review"

    text = draft_path.read_text(encoding="utf-8")
    print(f"Input: {len(text.split())} words | PK: '{primary_kw}'")

    # Apply fixes
    text, h2_ok    = fix_pk_in_h2(text, tool_name, primary_kw)
    text, injected = inject_internal_links(text, tool_slug, tools)
    text, lp_ok    = fix_pk_in_final_para(text, primary_kw)

    print(f"Fix H2 PK  : {'OK' if h2_ok else 'SKIPPED'}")
    print(f"Int links  : +{len(injected)} → {injected}")
    print(f"Final para : {'OK' if lp_ok else 'SKIPPED'}")

    # Save in-place
    draft_path.write_text(text, encoding="utf-8")
    print(f"Saved → {draft_path}")

    # QA
    qa_report(text, primary_kw, tool_slug)

if __name__ == "__main__":
    main()
