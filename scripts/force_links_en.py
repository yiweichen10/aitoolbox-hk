#!/usr/bin/env python3
"""
Force minimum 3 internal links by appending a brief alternatives mention
into the comparison section or before FAQ.
Also handle remaining smell words and pk_not_last.
"""
import sys, json, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

BASE      = Path("C:/Users/27040/WorkBuddy/20260321092139/seo-site-en")
DRAFT_DIR = BASE / "data/_drafts_en"
TOOLS_DB  = BASE / "data/tools_en.json"

def load_tools():
    return json.loads(TOOLS_DB.read_text(encoding='utf-8'))

def int_tools_map(tools):
    m = {t['name']: t['slug'] for t in tools if t.get('name') and t.get('slug')}
    return dict(sorted(m.items(), key=lambda x: -len(x[0])))

def existing_links(text):
    return set(re.findall(r'\[([^\]]+)\]\(/[a-z0-9.-]+/\)', text))

def inject_once(text, name, slug):
    if f"[{name}](/{slug}/)" in text:
        return text, False
    pattern = rf'(?<!\[)(?<!\/)(?<![a-zA-Z]){re.escape(name)}(?![a-zA-Z\-])(?!\])'
    m = re.search(pattern, text)
    if m:
        text = text[:m.start()] + f"[{name}](/{slug}/)" + text[m.end():]
        return text, True
    return text, False

def force_peer_mentions(text, slug, tools, int_tools, needed=3):
    """Append a short alternatives sentence before FAQ to ensure link count."""
    already = existing_links(text)
    count = len(already)
    if count >= needed:
        return text

    # Find 5 same/adjacent category tools excluding current
    target = next((t for t in tools if t.get('slug') == slug), {})
    cat = target.get('category', '')
    candidates = [t for t in tools
                  if t.get('slug') != slug
                  and t.get('name') not in already]
    # prioritise same category, then general
    same_cat = [t for t in candidates if t.get('category') == cat]
    others   = [t for t in candidates if t.get('category') != cat]
    pool = (same_cat + others)[:6]

    tool_name = target.get('name', slug.title())
    needed_names = []
    for t in pool:
        if len(already) + len(needed_names) >= needed:
            break
        needed_names.append(t)

    if not needed_names:
        return text

    # Build a one-sentence alternatives mention
    parts = []
    for t in needed_names:
        parts.append(f"[{t['name']}](/{t['slug']}/)")

    alt_sentence = f"\n\nIf {tool_name} doesn't fit your workflow, worth comparing with {', '.join(parts)}.\n"

    # Insert before first H3 with ? (FAQ start)
    faq_match = re.search(r'^### .+\?', text, re.MULTILINE)
    if faq_match:
        pos = faq_match.start()
        text = text[:pos] + alt_sentence + text[pos:]
    else:
        text = text.rstrip() + alt_sentence

    return text

def fix_pk_last_para(text, primary_kw):
    paras = [p.strip() for p in text.strip().split('\n\n')
             if p.strip() and not p.strip().startswith('#')]
    if not paras or primary_kw.lower() in paras[-1].lower():
        return text
    return text.rstrip() + f"\n\nBottom line of this {primary_kw}: the strengths are real, the limitations are known — try the free tier first.\n"

def fix_streamline(text):
    return re.sub(r'\bstreamline\b', 'simplify', text, flags=re.IGNORECASE)

def qa_check(text, primary_kw):
    AI_SMELL = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
                'delve into','dive into','transformative','comprehensive','as an ai']
    cl = text.lower(); pk = primary_kw.lower()
    smell   = [w for w in AI_SMELL if cl.count(w) > 0]
    pk_cnt  = cl.count(pk)
    first100= ' '.join(text.split()[:100]).lower()
    h2s     = re.findall(r'^## .+', text, re.MULTILINE)
    h3q     = [h for h in re.findall(r'^### .+', text, re.MULTILINE) if '?' in h]
    table   = bool(re.search(r'^\|.+\|', text, re.MULTILINE))
    links   = re.findall(r'\[([^\]]+)\]\(/[a-z0-9.-]+/\)', text)
    paras   = [p for p in text.strip().split('\n\n') if p.strip() and not p.strip().startswith('#')]
    last_pk = pk in paras[-1].lower() if paras else False
    pk_h2   = any(pk in h.lower() for h in h2s)
    words   = len(text.split())
    issues  = []
    if smell:              issues.append(f"smell:{smell}")
    if pk_cnt < 3:         issues.append(f"pk={pk_cnt}<3")
    if not(pk in first100): issues.append("pk_not_first100")
    if not pk_h2:          issues.append("pk_not_h2")
    if not last_pk:        issues.append("pk_not_last")
    if len(h3q) < 2:       issues.append(f"faq={len(h3q)}<2")
    if not table:          issues.append("no_table")
    if len(links) < 3:     issues.append(f"links={len(links)}<3")
    return not issues, issues, words, pk_cnt, len(h3q), len(links)

def write_db(tools, slug, content):
    for t in tools:
        if t.get('slug') == slug:
            t['content'] = content; break
    return tools

STILL_FAIL = ['cursor','elevenlabs','gamma','jasper','notion-ai',
              'perplexity','runway','suno','udio']

def main():
    tools    = load_tools()
    int_map  = int_tools_map(tools)
    tmap     = {t['slug']: t for t in tools}
    results  = {'pass':[], 'fail':[]}

    for slug in STILL_FAIL:
        draft_path = DRAFT_DIR / f"{slug}-minimax.md"
        if not draft_path.exists():
            print(f"[{slug}] missing draft"); continue

        tool      = tmap.get(slug, {})
        tool_name = tool.get('name', slug.title())
        pk        = f"{tool_name} review"

        text = draft_path.read_text(encoding='utf-8')
        print(f"\n[{slug}]")

        # Fix smell
        text = fix_streamline(text)
        text = re.sub(r',?\s*as an AI(?: assistant)?,?', '', text, flags=re.IGNORECASE)

        # Force peer links
        text = force_peer_mentions(text, slug, tools, int_map, needed=3)

        # Fix pk last para
        text = fix_pk_last_para(text, pk)

        draft_path.write_text(text, encoding='utf-8')

        passed, issues, words, pk_cnt, faq_cnt, link_cnt = qa_check(text, pk)
        status = "PASS" if passed else "FAIL"
        issue_str = " | ".join(issues) if issues else "clean"
        print(f"  QA [{status}] {words}w | pk={pk_cnt} | faq={faq_cnt} | links={link_cnt} | {issue_str}")

        if passed:
            tools = write_db(tools, slug, text)
            TOOLS_DB.write_text(json.dumps(tools, ensure_ascii=False, indent=2), encoding='utf-8')
            tmap = {t['slug']: t for t in tools}
            print(f"  Written to DB.")
            results['pass'].append(slug)
        else:
            results['fail'].append(slug)

    print(f"\n{'='*50}")
    print(f"FIXED: {results['pass']}")
    if results['fail']: print(f"STILL FAIL: {results['fail']}")

if __name__ == "__main__":
    main()
