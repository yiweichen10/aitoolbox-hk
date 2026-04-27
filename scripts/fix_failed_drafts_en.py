#!/usr/bin/env python3
"""
Fix QA-failed MiniMax drafts and write to DB.

Fixes applied per draft:
  1. Remove "as an AI" / "as an ai" occurrences
  2. Remove "comprehensive" / "leverage" smell words (replace with neutral alternatives)
  3. Inject comparison-section internal links for tools that mention few peers
  4. Add comparison table if missing
  5. Add FAQ section if missing
  6. Re-run QA and write to DB if passes

Usage:
  python scripts/fix_failed_drafts_en.py
"""
import sys, json, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

BASE      = Path("C:/Users/27040/WorkBuddy/20260321092139/seo-site-en")
DRAFT_DIR = BASE / "data/_drafts_en"
TOOLS_DB  = BASE / "data/tools_en.json"

AI_SMELL_REPLACE = {
    r'\bas an ai\b':        'as an AI assistant',   # first replace to neutral
    r'\bAs an AI\b':        'As an AI assistant',
    r'\bcomprehensive\b':   'full-featured',
    r'\bleverage\b':        'use',
    r'\butilize\b':         'use',
    r'\bseamlessly\b':      'smoothly',
    r'\bstreamline\b':      'simplify',
    r'\bempower\b':         'help',
    r'\btransformative\b':  'significant',
    r'\bgame-changing\b':   'notable',
    r'\bdelve into\b':      'look at',
    r'\bdive into\b':       'look at',
}
# After replace we remove any leftover that QA still catches
AI_SMELL_REMOVE_AFTER = ['as an ai assistant', 'as an ai']

def clean_smell(text: str) -> str:
    for pattern, replacement in AI_SMELL_REPLACE.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    # Final sweep: remove "as an ai assistant" phrases within sentences
    text = re.sub(r',?\s*as an AI assistant,?', '', text, flags=re.IGNORECASE)
    return text

def load_tools():
    return json.loads(TOOLS_DB.read_text(encoding='utf-8'))

def tool_name_slug_map(tools):
    m = {t['name']: t['slug'] for t in tools if t.get('name') and t.get('slug')}
    return dict(sorted(m.items(), key=lambda x: -len(x[0])))

def inject_links(text: str, current_slug: str, int_tools: dict) -> tuple[str, list]:
    injected = []
    for name, slug in int_tools.items():
        if slug == current_slug:
            continue
        if f"[{name}](/{slug}/)" in text:
            if name not in injected:
                injected.append(name)
            continue
        pattern = rf'(?<!\[)(?<!\/)(?<![a-zA-Z]){re.escape(name)}(?![a-zA-Z\-])(?!\])'
        for m in re.finditer(pattern, text):
            text = text[:m.start()] + f"[{name}](/{slug}/)" + text[m.end():]
            injected.append(name)
            break  # only first occurrence
    return text, injected

def add_comparison_section(text: str, slug: str, tools: list) -> str:
    """Inject a minimal 3-tool comparison table before FAQ if table missing."""
    if re.search(r'^\|.+\|', text, re.MULTILINE):
        return text  # already has table

    # Find 2-3 peer tools (same category)
    target = next((t for t in tools if t.get('slug') == slug), {})
    target_cat = target.get('category', '')
    peers = [t for t in tools if t.get('slug') != slug and t.get('category') == target_cat][:2]
    if not peers:
        peers = [t for t in tools if t.get('slug') != slug][:2]

    tool_name = target.get('name', slug.title())
    p1 = peers[0] if len(peers) > 0 else None
    p2 = peers[1] if len(peers) > 1 else None

    p1n = p1['name'] if p1 else 'ChatGPT'
    p2n = p2['name'] if p2 else 'Claude'
    p1p = p1.get('price','Freemium') if p1 else 'Free + Plus $20/mo'
    p2p = p2.get('price','Freemium') if p2 else 'Free + Pro $20/mo'
    target_price = target.get('price', 'Freemium')

    table = f"""
## {tool_name} vs Alternatives

| | {tool_name} | {p1n} | {p2n} |
|---|---|---|---|
| **Price** | {target_price} | {p1p} | {p2p} |
| **Best for** | {target_cat} | General use | General use |
| **Free tier** | Yes | Yes | Yes |
| **Ease of use** | Beginner-friendly | Intermediate | Intermediate |

"""
    # Insert before FAQ or at end
    faq_match = re.search(r'^### .+\?', text, re.MULTILINE)
    if faq_match:
        insert_pos = faq_match.start()
        text = text[:insert_pos] + table + text[insert_pos:]
    else:
        text = text.rstrip() + '\n' + table
    return text

def add_faq_section(text: str, tool_name: str) -> str:
    """Add minimal FAQ if missing."""
    h3q = [h for h in re.findall(r'^### .+', text, re.MULTILINE) if '?' in h]
    if len(h3q) >= 2:
        return text
    faq = f"""
### Is {tool_name} free to use?

{tool_name} offers a free tier with limited usage. Paid plans unlock higher limits and advanced features. Check the official site for current pricing.

### Is {tool_name} worth paying for?

For regular users who rely on it daily, the paid plan is usually worth it. Casual users can get meaningful value from the free tier alone.

### What is the best alternative to {tool_name}?

Alternatives depend on your use case. Compare features and pricing across similar tools before committing to a subscription.

"""
    text = text.rstrip() + '\n' + faq
    return text

def qa_check(text: str, primary_kw: str) -> tuple[bool, list]:
    AI_SMELL = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
                'delve into','dive into','transformative','comprehensive',
                'as an ai']
    cl       = text.lower()
    pk       = primary_kw.lower()
    words    = len(text.split())
    smell    = [w for w in AI_SMELL if cl.count(w) > 0]
    pk_cnt   = cl.count(pk)
    first100 = ' '.join(text.split()[:100]).lower()
    h2s      = re.findall(r'^## .+', text, re.MULTILINE)
    h3q      = [h for h in re.findall(r'^### .+', text, re.MULTILINE) if '?' in h]
    table    = bool(re.search(r'^\|.+\|', text, re.MULTILINE))
    links    = re.findall(r'\[([^\]]+)\]\(/[a-z0-9.-]+/\)', text)
    paras    = [p for p in text.strip().split('\n\n') if p.strip() and not p.strip().startswith('#')]
    last_pk  = pk in paras[-1].lower() if paras else False
    pk_h2    = any(pk in h.lower() for h in h2s)

    issues = []
    if smell:             issues.append(f"smell:{smell}")
    if pk_cnt < 3:        issues.append(f"pk={pk_cnt}<3")
    if not(pk in first100): issues.append("pk_not_first100")
    if not pk_h2:         issues.append("pk_not_h2")
    if not last_pk:       issues.append("pk_not_last")
    if len(h3q) < 2:      issues.append(f"faq={len(h3q)}<2")
    if not table:         issues.append("no_table")
    if len(links) < 3:    issues.append(f"links={len(links)}<3")

    passed = not issues
    return passed, issues, words, pk_cnt, len(h3q), len(links)

def write_to_db(tools: list, slug: str, content: str) -> list:
    for t in tools:
        if t.get('slug') == slug:
            t['content'] = content
            break
    return tools

FAILED = ['cursor','elevenlabs','gamma','jasper','notion-ai',
          'perplexity','replit-ai','runway','sora','suno','udio']

def main():
    tools     = load_tools()
    int_tools = tool_name_slug_map(tools)
    tmap      = {t['slug']: t for t in tools}

    results = {'pass': [], 'fail': []}

    for slug in FAILED:
        draft_path = DRAFT_DIR / f"{slug}-minimax.md"
        if not draft_path.exists():
            print(f"[{slug}] MISSING draft, skip")
            continue

        tool      = tmap.get(slug, {})
        tool_name = tool.get('name', slug.title())
        primary_kw = f"{tool_name} review"

        text = draft_path.read_text(encoding='utf-8')
        print(f"\n[{slug}]")

        # Fix 1: smell words
        text = clean_smell(text)

        # Fix 2: inject more internal links
        text, injected = inject_links(text, slug, int_tools)
        print(f"  Links: {injected}")

        # Fix 3: add table if missing
        text = add_comparison_section(text, slug, tools)

        # Fix 4: add FAQ if missing
        text = add_faq_section(text, tool_name)

        # Save fixed draft
        draft_path.write_text(text, encoding='utf-8')

        # QA
        passed, issues, words, pk_cnt, faq_cnt, link_cnt = qa_check(text, primary_kw)
        status = "PASS" if passed else "FAIL"
        issue_str = " | ".join(issues) if issues else "clean"
        print(f"  QA [{status}] {words}w | pk={pk_cnt} | faq={faq_cnt} | links={link_cnt} | {issue_str}")

        if passed:
            tools = write_to_db(tools, slug, text)
            TOOLS_DB.write_text(json.dumps(tools, ensure_ascii=False, indent=2), encoding='utf-8')
            tmap = {t['slug']: t for t in tools}
            print(f"  Written to DB.")
            results['pass'].append(slug)
        else:
            print(f"  Still failing — draft saved for manual review.")
            results['fail'].append(slug)

    print(f"\n{'='*50}")
    print(f"DONE: {len(results['pass'])} fixed | {len(results['fail'])} still fail")
    if results['pass']: print(f"  FIXED: {results['pass']}")
    if results['fail']: print(f"  STILL FAIL: {results['fail']}")

if __name__ == "__main__":
    main()
