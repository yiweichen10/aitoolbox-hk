#!/usr/bin/env python3
"""
Batch rewrite tool pages using MiniMax API + post-process patch.

Flow per tool:
  1. Load KW data from data/_kw/<slug>.json
  2. Load tool metadata from data/tools_en.json
  3. Build prompt with real KW + tool data
  4. Call MiniMax API → save draft to data/_drafts_en/<slug>-minimax.md
  5. Post-process: fix H2 PK, inject internal links, fix final-para PK
  6. QA check → print result
  7. Write content into tools_en.json

Usage:
  python scripts/batch_rewrite_en.py                  # rewrite all 20 tools with KW data
  python scripts/batch_rewrite_en.py gemini suno       # specific slugs only
  python scripts/batch_rewrite_en.py --dry-run         # show plan, no API calls
"""

import sys, json, re, time, os, requests
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("MINIMAX_API_KEY")
BASE = Path("C:/Users/27040/WorkBuddy/20260321092139/seo-site-en")
KW_DIR    = BASE / "data/_kw"
DRAFT_DIR = BASE / "data/_drafts_en"
TOOLS_DB  = BASE / "data/tools_en.json"
DRAFT_DIR.mkdir(exist_ok=True)

AI_SMELL = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
            'delve into','dive into','transformative','comprehensive',
            'it is worth noting','in conclusion','as an ai','in today']

# ── noise longtail filter ──────────────────────────────────────────────────
NOISE_WORDS = ['crypto','reddit','github','crossword','center','pr review','maker',
               'prompt','cowork','codex','february','march','character','bot 2026',
               'air purifier','netflix','rotten tomatoes','guardian','glassdoor',
               'lipstick','nikke','engines','blue 11','trustpilot','audiio','audio review',
               'tea review','stuck','next file']

def filter_longtail(lt_list: list, tool_name: str) -> list:
    """Keep only relevant longtail KWs (max 4)."""
    name_lower = tool_name.lower()
    kept = []
    for kw in lt_list:
        kl = kw.lower()
        if any(n in kl for n in NOISE_WORDS):
            continue
        if name_lower not in kl and 'ai' not in kl and 'alternative' not in kl:
            # only keep generic phrases that are clearly about the tool context
            if not any(w in kl for w in ['review','best','free','vs','price','cost','how']):
                continue
        kept.append(kw)
        if len(kept) >= 4:
            break
    return kept

# ── load tool registry ─────────────────────────────────────────────────────
def load_tools():
    return json.loads(TOOLS_DB.read_text(encoding='utf-8'))

def tool_map(tools):
    return {t['slug']: t for t in tools}

def get_internal_tools(tools):
    """Return {name: slug} sorted by name length desc."""
    m = {t['name']: t['slug'] for t in tools if t.get('name') and t.get('slug')}
    return dict(sorted(m.items(), key=lambda x: -len(x[0])))

# ── build prompt ───────────────────────────────────────────────────────────
def build_prompt(slug: str, tool: dict, kw: dict) -> tuple[str, str, list]:
    tool_name  = tool.get('name', slug.title())
    primary_kw = kw.get('primary_kw', f'{tool_name} review')
    longtail   = filter_longtail(kw.get('longtail_kw', []), tool_name)
    paa        = kw.get('paa', [])[:4]

    # Tool metadata
    price    = tool.get('price', 'Free + Paid')
    pros     = tool.get('pros', [])
    cons     = tool.get('cons', [])
    features = tool.get('features', [])

    pros_str     = ' | '.join(pros[:4]) if pros else 'N/A'
    cons_str     = ' | '.join(cons[:4]) if cons else 'N/A'
    features_str = ' | '.join(features[:5]) if features else 'N/A'

    lt_str  = ', '.join([f'"{k}"' for k in longtail]) if longtail else f'"{tool_name} alternative", "{tool_name} free"'
    paa_str = '\n'.join([f'- "{q}"' for q in paa]) if paa else f'- "Is {tool_name} worth it?"'

    system = (
        "You are a senior tech journalist covering AI tools. "
        "Write honest, specific, opinionated reviews for a skeptical audience. "
        "Short punchy sentences mixed with longer ones. Contractions throughout. "
        "Real prices and real limitations. "
        "No corporate buzzwords: no leverage, seamlessly, game-changing, comprehensive, "
        "delve into, transformative, empower, streamline."
    )

    user = f"""Write a 1400-word review page for {tool_name}. Use these keywords naturally — weave in, do NOT stuff:
- Primary "{primary_kw}": 3-4x — must appear in first 100 words, one H2 title, and final paragraph
- Longtail (1x each): {lt_str}
- FAQ H3 questions verbatim (use exactly as written):
{paa_str}

Tool data:
- Price: {price}
- Pros: {pros_str}
- Cons: {cons_str}
- Key features: {features_str}

Structure (NO H1 heading):
Intro 1-2 paras (hook + context) →
4-5 H2 sections covering: what it does well / pricing breakdown / who it's best for / real limitations / vs top alternatives →
Comparison table ({tool_name} vs 2-3 competitors) →
FAQ using the H3 questions above →
Final recommendation paragraph (no "Conclusion" header)

Rules:
- Internal links: when mentioning other AI tools by name, write them as plain text (no markdown links — links will be added by post-processing)
- Raw Markdown only, no HTML
- No "In conclusion", "As an AI", "It's worth noting"
- Every claim must be specific: name the feature, the price, the limitation
"""
    return system, user, longtail

# ── call MiniMax ───────────────────────────────────────────────────────────
def call_minimax(system: str, user: str, slug: str) -> str | None:
    try:
        r = requests.post(
            "https://api.minimaxi.com/v1/text/chatcompletion_v2",
            headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
            json={
                "model": "MiniMax-M2.7",
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user",   "content": user},
                ],
                "max_tokens": 3000,
                "temperature": 0.72,
            },
            timeout=120
        )
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        else:
            print(f"  [API ERROR {r.status_code}] {r.text[:200]}")
            return None
    except Exception as e:
        print(f"  [EXCEPTION] {e}")
        return None

# ── post-process ───────────────────────────────────────────────────────────
def fix_pk_in_h2(text: str, tool_name: str, primary_kw: str) -> str:
    h2s = re.findall(r'^(## .+)$', text, re.MULTILINE)
    if not h2s:
        return text
    first_h2 = h2s[0]
    if primary_kw.lower() in first_h2.lower():
        return text
    old_title = first_h2[3:].strip()
    remainder = re.sub(rf'^what\s+{re.escape(tool_name)}\s*', '', old_title, flags=re.IGNORECASE).strip()
    new_h2 = f"## {tool_name} Review: {remainder}" if remainder else f"## {tool_name} Review: Features and Performance"
    return text.replace(first_h2, new_h2, 1)

def inject_internal_links(text: str, current_slug: str, int_tools: dict) -> tuple[str, list]:
    injected = []
    for name, slug in int_tools.items():
        if slug == current_slug:
            continue
        if f"[{name}](/{slug}/)" in text:
            continue
        pattern = rf'(?<!\[)(?<!\/)(?<![a-zA-Z]){re.escape(name)}(?![a-zA-Z])(?!\])'
        m = re.search(pattern, text)
        if m:
            text = text[:m.start()] + f"[{name}](/{slug}/)" + text[m.end():]
            injected.append(name)
    return text, injected

def fix_pk_in_final_para(text: str, primary_kw: str) -> str:
    paras = [p.strip() for p in text.strip().split('\n\n') if p.strip() and not p.strip().startswith('#')]
    if not paras or primary_kw.lower() in paras[-1].lower():
        return text
    return text.rstrip() + f"\n\nBottom line of this {primary_kw}: use the strengths it offers, know its limits, and try the free tier before paying."

def post_process(text: str, tool_name: str, primary_kw: str, current_slug: str, int_tools: dict) -> tuple[str, list]:
    text = fix_pk_in_h2(text, tool_name, primary_kw)
    text, injected = inject_internal_links(text, current_slug, int_tools)
    text = fix_pk_in_final_para(text, primary_kw)
    return text, injected

# ── QA ────────────────────────────────────────────────────────────────────
def qa_check(text: str, primary_kw: str, slug: str) -> bool:
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

    passed = (not smell and pk_cnt >= 3 and (pk in first100) and pk_h2 and last_pk
              and len(h3q) >= 2 and table and len(links) >= 3)

    status = "PASS" if passed else "FAIL"
    issues = []
    if smell:         issues.append(f"smell:{smell}")
    if pk_cnt < 3:    issues.append(f"pk_cnt={pk_cnt}<3")
    if not (pk in first100): issues.append("pk_not_first100")
    if not pk_h2:     issues.append("pk_not_in_h2")
    if not last_pk:   issues.append("pk_not_last_para")
    if len(h3q) < 2:  issues.append(f"faq={len(h3q)}<2")
    if not table:     issues.append("no_table")
    if len(links) < 3:issues.append(f"links={len(links)}<3")

    issue_str = " | ".join(issues) if issues else "clean"
    print(f"    QA [{status}] {words}w | pk={pk_cnt} | faq={len(h3q)} | links={len(links)} | {issue_str}")
    return passed

# ── write to DB ───────────────────────────────────────────────────────────
def write_to_db(tools: list, slug: str, content: str) -> list:
    for t in tools:
        if t.get('slug') == slug:
            t['content'] = content
            break
    return tools

# ── main ──────────────────────────────────────────────────────────────────
def main():
    args     = [a for a in sys.argv[1:] if not a.startswith('--')]
    dry_run  = '--dry-run' in sys.argv

    # All slugs with KW data
    all_kw_slugs = sorted([p.stem for p in KW_DIR.glob('*.json')])

    # Filter: skip chatgpt (already done with new process) and claude
    SKIP = {'chatgpt', 'claude'}
    target_slugs = [s for s in (args if args else all_kw_slugs) if s not in SKIP]

    tools    = load_tools()
    tmap     = tool_map(tools)
    int_tools = get_internal_tools(tools)

    print(f"Target: {len(target_slugs)} tools | dry_run={dry_run}")
    print(f"Slugs : {target_slugs}\n")

    if dry_run:
        for slug in target_slugs:
            kw   = json.loads((KW_DIR / f"{slug}.json").read_text(encoding='utf-8'))
            tool = tmap.get(slug, {})
            _, _, lt = build_prompt(slug, tool, kw)
            print(f"  {slug}: pk='{kw.get('primary_kw')}' | lt={lt}")
        return

    results = {'pass': [], 'fail': [], 'error': []}

    for i, slug in enumerate(target_slugs):
        print(f"\n[{i+1}/{len(target_slugs)}] {slug}")

        kw_path = KW_DIR / f"{slug}.json"
        if not kw_path.exists():
            print(f"  SKIP: no KW data")
            results['error'].append(slug)
            continue

        kw   = json.loads(kw_path.read_text(encoding='utf-8'))
        tool = tmap.get(slug, {})
        if not tool:
            print(f"  SKIP: slug not in tools_en.json")
            results['error'].append(slug)
            continue

        tool_name  = tool.get('name', slug.title())
        primary_kw = kw.get('primary_kw', f'{tool_name} review')

        system, user, lt = build_prompt(slug, tool, kw)
        print(f"  Generating... pk='{primary_kw}' | lt={lt}")

        content = call_minimax(system, user, slug)
        if not content:
            results['error'].append(slug)
            continue

        # Save raw draft
        draft_path = DRAFT_DIR / f"{slug}-minimax.md"
        draft_path.write_text(content, encoding='utf-8')
        print(f"  Raw: {len(content.split())}w → {draft_path.name}")

        # Post-process
        content, injected = post_process(content, tool_name, primary_kw, slug, int_tools)
        draft_path.write_text(content, encoding='utf-8')
        print(f"  Links injected: {injected}")

        # QA
        passed = qa_check(content, primary_kw, slug)

        if passed:
            tools = write_to_db(tools, slug, content)
            TOOLS_DB.write_text(json.dumps(tools, ensure_ascii=False, indent=2), encoding='utf-8')
            tmap = tool_map(tools)  # refresh
            print(f"  Written to DB.")
            results['pass'].append(slug)
        else:
            print(f"  Draft saved but NOT written to DB (QA fail). Manual review needed.")
            results['fail'].append(slug)

        # Rate limit buffer
        if i < len(target_slugs) - 1:
            time.sleep(2)

    print(f"\n{'='*50}")
    print(f"DONE: {len(results['pass'])} pass | {len(results['fail'])} fail | {len(results['error'])} error")
    if results['pass']:  print(f"  PASS : {results['pass']}")
    if results['fail']:  print(f"  FAIL : {results['fail']}")
    if results['error']: print(f"  ERROR: {results['error']}")

if __name__ == "__main__":
    main()
