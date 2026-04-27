#!/usr/bin/env python3
"""
Compare MiniMax-M2.5 (SiliconFlow) vs MiniMax-M2.7 (MiniMax API) on same slug.
Usage: python scripts/compare_models_en.py <slug>
Example: python scripts/compare_models_en.py gemini
"""
import sys, json, re, os, time, requests
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
BASE      = Path("C:/Users/27040/WorkBuddy/20260321092139/seo-site-en")
KW_DIR    = BASE / "data/_kw"
DRAFT_DIR = BASE / "data/_drafts_en"
TOOLS_DB  = BASE / "data/tools_en.json"

SF_KEY    = os.getenv("SILICONFLOW_API_KEY")
SF_URL    = "https://api.siliconflow.cn/v1/chat/completions"
SF_MODEL  = "Pro/MiniMaxAI/MiniMax-M2.5"

MM_KEY    = os.getenv("MINIMAX_API_KEY")
MM_URL    = "https://api.minimaxi.com/v1/text/chatcompletion_v2"
MM_MODEL  = "MiniMax-M2.7"

AI_SMELL  = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
             'delve into','dive into','transformative','comprehensive',
             'it is worth noting','in conclusion','as an ai','in today']

NOISE_WORDS = ['crypto','reddit','github','crossword','air purifier','netflix',
               'rotten tomatoes','guardian','glassdoor','lipstick','nikke',
               'engines','trustpilot','audiio','tea review','stuck']

def load_tools():
    return json.loads(TOOLS_DB.read_text(encoding='utf-8'))

def filter_longtail(lt_list, tool_name):
    kept = []
    for kw in lt_list:
        kl = kw.lower()
        if any(n in kl for n in NOISE_WORDS):
            continue
        if tool_name.lower() not in kl and 'ai' not in kl and 'alternative' not in kl:
            if not any(w in kl for w in ['review','best','free','vs','price','cost','how']):
                continue
        kept.append(kw)
        if len(kept) >= 4:
            break
    return kept

def build_prompt(slug, tool, kw):
    tool_name  = tool.get('name', slug.title())
    primary_kw = kw.get('primary_kw', f'{tool_name} review')
    longtail   = filter_longtail(kw.get('longtail_kw', []), tool_name)
    paa        = kw.get('paa', [])[:4]
    price      = tool.get('price', 'Free + Paid')
    pros_str   = ' | '.join(tool.get('pros', [])[:4]) or 'N/A'
    cons_str   = ' | '.join(tool.get('cons', [])[:4]) or 'N/A'
    feat_str   = ' | '.join(tool.get('features', [])[:5]) or 'N/A'
    lt_str     = ', '.join([f'"{k}"' for k in longtail]) or f'"{tool_name} alternative"'
    paa_str    = '\n'.join([f'- "{q}"' for q in paa]) or f'- "Is {tool_name} worth it?"'

    system = (
        "You are a senior tech journalist with 10 years covering AI tools. "
        "You write for skeptical, time-poor professionals who can smell marketing copy instantly. "
        "Your reviews are known for being honest, specific, and opinionated — you always take a clear stance. "
        "Writing style: mix short punchy sentences with longer analytical ones. "
        "Use contractions naturally (it's, you'll, that's, there's). First person where it fits. "
        "Every claim must be backed by a specific detail — a price, a feature name, a real limitation. "
        "Absolutely forbidden words and phrases (violation = rewrite): "
        "leverage, utilize, seamlessly, game-changing, empower, streamline, delve into, dive into, "
        "transformative, comprehensive, revolutionize, cutting-edge, robust, innovative, "
        "it is worth noting, in conclusion, to summarize, as an AI, in today's world, "
        "the world of, it's important to note, a testament to."
    )
    user = f"""Write a detailed review article for {tool_name}. Target: 1400-1600 words. No H1 heading. Markdown only.

--- KEYWORD STRATEGY (SEO-driven, natural placement only) ---
Primary keyword "{primary_kw}" — place exactly 4 times:
  [1] Within the first 80 words of the intro
  [2] Inside one H2 section heading
  [3] Naturally within a body paragraph (not forced)
  [4] In the final recommendation paragraph

Longtail keywords — each used once, woven in naturally (never bolded or highlighted):
{lt_str}

FAQ section — use these exact phrases as H3 headings, word for word:
{paa_str}

--- TOOL FACTS (use these, do not invent numbers) ---
Price: {price}
Strengths: {pros_str}
Weaknesses: {cons_str}
Key features: {feat_str}

--- REQUIRED STRUCTURE (7 sections, follow precisely) ---

[1] INTRO — ~150 words, 2 paragraphs
  - First sentence: state what {tool_name} is and drop the primary keyword "{primary_kw}" immediately — do not bury it in a story opener
  - Second sentence onward: paint a specific real-world scenario where someone reaches for {tool_name}
  - Second paragraph: what this review covers and the stance you're taking
  - Primary keyword MUST appear within the first 80 words — no exceptions

[2] ## What {tool_name} Does Well — ~250 words
  - Cover exactly 3-4 strengths
  - Each strength: one sentence stating it, 2-3 sentences with a concrete example or specific feature detail
  - No generic praise — if you can't give a specific example, cut the strength

[3] ## {primary_kw.title()}: Pricing and Plans — ~200 words
  - List every pricing tier with exact cost
  - For each tier: who it's designed for, what's included, what's missing vs the tier above
  - End with a clear verdict on which tier offers best value

[4] ## Limitations Worth Knowing — ~200 words
  - Cover exactly 3-4 real weaknesses
  - Be direct — name the limitation, explain why it matters, say who it affects most
  - No softening language like "some users may find" — state it plainly

[5] ## {tool_name} vs Alternatives — ~250 words
  - Start with a comparison table (minimum 4 rows): Price / Best for / Free tier / [one key differentiating feature]
  - Name at least 3 real competing tools by their actual product name
  - After the table: 2-3 sentences on each competitor — where {tool_name} wins, where it loses
  - Be specific about the tradeoffs, not just "it depends"

[6] FAQ — ~200 words
  - Use EXACTLY these H3 headings, word for word:
{paa_str}
  - Each answer: 3-4 sentences, direct and specific, no hedging

[7] FINAL RECOMMENDATION — ~100 words, no heading
  - One clear sentence on who should use {tool_name} and why
  - One clear sentence on who should not use it and what they should use instead
  - Primary keyword must appear here
  - End with a single actionable sentence (e.g. start with free tier, compare X before paying)
"""
    return system, user, primary_kw, longtail

def call_siliconflow(system, user):
    r = requests.post(
        SF_URL,
        headers={"Authorization": f"Bearer {SF_KEY}", "Content-Type": "application/json"},
        json={
            "model": SF_MODEL,
            "messages": [{"role":"system","content":system},{"role":"user","content":user}],
            "max_tokens": 3000,
            "temperature": 0.72,
        },
        timeout=120
    )
    if r.status_code == 200:
        d = r.json()
        content = d["choices"][0]["message"]["content"]
        usage   = d.get("usage", {})
        return content, usage
    else:
        print(f"  [SF ERROR {r.status_code}] {r.text[:300]}")
        return None, {}

def call_minimax(system, user):
    r = requests.post(
        MM_URL,
        headers={"Authorization": f"Bearer {MM_KEY}", "Content-Type": "application/json"},
        json={
            "model": MM_MODEL,
            "messages": [{"role":"system","content":system},{"role":"user","content":user}],
            "max_tokens": 3000,
            "temperature": 0.72,
        },
        timeout=120
    )
    if r.status_code == 200:
        d = r.json()
        content = d["choices"][0]["message"]["content"]
        usage   = d.get("usage", {})
        return content, usage
    else:
        print(f"  [MM ERROR {r.status_code}] {r.text[:300]}")
        return None, {}

def qa_score(text, primary_kw):
    """Return dict of QA metrics."""
    if not text:
        return {}
    cl       = text.lower()
    pk       = primary_kw.lower()
    words    = len(text.split())
    smell    = [w for w in AI_SMELL if cl.count(w) > 0]
    pk_cnt   = cl.count(pk)
    first100 = ' '.join(text.split()[:100]).lower()
    h2s      = re.findall(r'^## .+', text, re.MULTILINE)
    h3q      = [h for h in re.findall(r'^### .+', text, re.MULTILINE) if '?' in h]
    table    = bool(re.search(r'^\|.+\|', text, re.MULTILINE))
    paras    = [p for p in text.strip().split('\n\n') if p.strip() and not p.strip().startswith('#')]
    last_pk  = pk in paras[-1].lower() if paras else False
    pk_h2    = any(pk in h.lower() for h in h2s)

    # Score: 1pt per criterion
    score = 0
    score += 1 if not smell else 0         # no AI smell
    score += 1 if pk_cnt >= 3 else 0       # PK density
    score += 1 if pk in first100 else 0    # PK in intro
    score += 1 if pk_h2 else 0             # PK in H2
    score += 1 if last_pk else 0           # PK in final para
    score += 1 if len(h3q) >= 2 else 0     # FAQ
    score += 1 if table else 0             # table
    score += 1 if words >= 1200 else 0     # length

    return {
        "words":    words,
        "pk_cnt":   pk_cnt,
        "pk_first100": pk in first100,
        "pk_h2":    pk_h2,
        "pk_last":  last_pk,
        "smell":    smell,
        "faq":      len(h3q),
        "table":    table,
        "score":    score,
        "max":      8,
    }

def print_qa(label, metrics, usage):
    if not metrics:
        print(f"\n  [{label}] FAILED (no content)")
        return
    smell_str = "CLEAN" if not metrics['smell'] else str(metrics['smell'])
    tok_in  = usage.get('prompt_tokens', usage.get('input_tokens', '?'))
    tok_out = usage.get('completion_tokens', usage.get('output_tokens', '?'))
    print(f"\n  [{label}]  score={metrics['score']}/{metrics['max']}  words={metrics['words']}")
    print(f"    smell    : {smell_str}")
    print(f"    PK x{metrics['pk_cnt']}   : first100={metrics['pk_first100']} | h2={metrics['pk_h2']} | last={metrics['pk_last']}")
    print(f"    FAQ      : {metrics['faq']}  table={metrics['table']}")
    print(f"    tokens   : in={tok_in} out={tok_out}")

def main():
    slug = sys.argv[1] if len(sys.argv) > 1 else "gemini"
    kw_path = KW_DIR / f"{slug}.json"
    if not kw_path.exists():
        print(f"No KW data for '{slug}'"); sys.exit(1)

    tools = load_tools()
    tmap  = {t['slug']: t for t in tools}
    tool  = tmap.get(slug, {})
    if not tool:
        print(f"Slug '{slug}' not in tools_en.json"); sys.exit(1)

    kw = json.loads(kw_path.read_text(encoding='utf-8'))
    system, user, primary_kw, longtail = build_prompt(slug, tool, kw)

    print(f"=== MODEL COMPARISON: {slug} ===")
    print(f"Primary KW : '{primary_kw}'")
    print(f"Longtail   : {longtail}")
    print(f"Prompt len : {len(user.split())} words\n")

    # ── M2.5 via SiliconFlow ──
    print("Calling M2.5 (SiliconFlow)...")
    t0 = time.time()
    content_25, usage_25 = call_siliconflow(system, user)
    t_25 = round(time.time() - t0, 1)
    if content_25:
        (DRAFT_DIR / f"{slug}-m25.md").write_text(content_25, encoding='utf-8')
        print(f"  Done in {t_25}s → {slug}-m25.md")
    metrics_25 = qa_score(content_25, primary_kw)

    # small gap
    time.sleep(3)

    # ── M2.7 via MiniMax ──
    print("Calling M2.7 (MiniMax)...")
    t0 = time.time()
    content_27, usage_27 = call_minimax(system, user)
    t_27 = round(time.time() - t0, 1)
    if content_27:
        (DRAFT_DIR / f"{slug}-m27.md").write_text(content_27, encoding='utf-8')
        print(f"  Done in {t_27}s → {slug}-m27.md")
    metrics_27 = qa_score(content_27, primary_kw)

    # ── print comparison ──
    print(f"\n{'='*55}")
    print(f"QA RESULTS — {slug}")
    print_qa(f"M2.5 SiliconFlow {t_25}s", metrics_25, usage_25)
    print_qa(f"M2.7 MiniMax     {t_27}s", metrics_27, usage_27)

    # ── Accio version (from DB for reference) ──
    existing = tool.get('content', '')
    if existing:
        metrics_ac = qa_score(existing, primary_kw)
        print(f"\n  [Accio/DB current]  score={metrics_ac['score']}/{metrics_ac['max']}  words={metrics_ac['words']}")
        smell_str = "CLEAN" if not metrics_ac['smell'] else str(metrics_ac['smell'])
        print(f"    smell    : {smell_str}")
        print(f"    PK x{metrics_ac['pk_cnt']}   : first100={metrics_ac['pk_first100']} | h2={metrics_ac['pk_h2']} | last={metrics_ac['pk_last']}")
        print(f"    FAQ      : {metrics_ac['faq']}  table={metrics_ac['table']}")

    print(f"\n{'='*55}")
    print(f"Winner: M2.5={metrics_25.get('score','?')}/8  M2.7={metrics_27.get('score','?')}/8  Accio={metrics_ac.get('score','?') if existing else '?'}/8")
    print(f"Drafts saved to data/_drafts_en/{slug}-m25.md and {slug}-m27.md")

if __name__ == "__main__":
    main()
