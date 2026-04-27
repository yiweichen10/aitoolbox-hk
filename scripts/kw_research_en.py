#!/usr/bin/env python3
"""
kw_research.py — Serper.dev-powered keyword research for aitoolbox.hk

Serper gives us real Google SERP data: related searches, People Also Ask,
autocomplete suggestions, and organic results — all we need for data-driven
keyword planning without expensive API subscriptions.

Usage:
  python scripts/kw_research.py page <slug>        # full KW plan for a tool page
  python scripts/kw_research.py article <slug>     # full KW plan for an article
  python scripts/kw_research.py seed "<query>"     # raw SERP + related for a query

Output saved to data/_kw/<slug>.json (gitignored — never committed)
"""
import requests, os, json, sys, time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
BASE    = Path(__file__).parent.parent
KW_DIR  = BASE / "data" / "_kw"
KW_DIR.mkdir(parents=True, exist_ok=True)

API_KEY = os.getenv("SERPER_API_KEY")
HEADERS = {"X-API-KEY": API_KEY, "Content-Type": "application/json"}


def serp(query, gl="us", hl="en", num=10):
    """Fetch Google SERP for a query."""
    r = requests.post("https://google.serper.dev/search",
                      headers=HEADERS,
                      json={"q": query, "gl": gl, "hl": hl, "num": num},
                      timeout=15)
    r.raise_for_status()
    return r.json()


def autocomplete(query):
    """Google autocomplete suggestions via Serper."""
    r = requests.post("https://google.serper.dev/autocomplete",
                      headers=HEADERS,
                      json={"q": query},
                      timeout=15)
    r.raise_for_status()
    return [s.get("value", "") for s in r.json().get("suggestions", [])]


def extract_kw_signals(serp_data):
    """Pull related searches, PAA, and organic titles from a SERP result."""
    related  = [r["query"] for r in serp_data.get("relatedSearches", [])]
    paa      = [p["question"] for p in serp_data.get("peopleAlsoAsk", [])]
    organics = [{"rank": i+1, "title": o.get("title",""), "url": o.get("link","")}
                for i, o in enumerate(serp_data.get("organic", [])[:10])]
    return related, paa, organics


def page_kw_plan(slug, kind="tool"):
    """Build a full keyword plan for a tool or article slug."""
    if kind == "tool":
        data  = json.loads((BASE / "data/tools_en.json").read_text(encoding="utf-8"))
        item  = next((t for t in data if t["slug"] == slug), None)
        name  = item["name"] if item else slug
        cat   = item.get("category", "AI tool") if item else "AI tool"
        seeds = [
            f"{name} review",
            f"{name} alternative",
            f"best {cat.lower()} 2026",
            f"{name} vs",
            f"how to use {name}",
        ]
    else:
        data  = json.loads((BASE / "data/articles_en.json").read_text(encoding="utf-8"))
        item  = next((a for a in data if a["slug"] == slug), None)
        title = item["title"] if item else slug
        kws   = item.get("keywords", "") if item else ""
        seeds = [kws.split(",")[0].strip()] if kws else [title[:60]]
        seeds += [f"{seeds[0]} 2026", f"best {seeds[0]}"]

    print(f"[{slug}] querying: {seeds[:3]}")

    all_related, all_paa, all_organics, all_suggest = [], [], [], []

    for seed in seeds[:3]:
        d = serp(seed)
        related, paa, organics = extract_kw_signals(d)
        all_related  += related
        all_paa      += paa
        all_organics += organics

        suggest = autocomplete(seed)
        all_suggest += suggest
        time.sleep(0.3)

    # Dedupe
    all_related  = list(dict.fromkeys(all_related))
    all_paa      = list(dict.fromkeys(all_paa))
    all_suggest  = list(dict.fromkeys(all_suggest))

    # Filter noise: drop keywords where intent is "use AI to do X" not "find AI tool"
    NOISE_PATTERNS = [
        "how to use chatgpt to", "use chatgpt to", "chatgpt to write",
        "chatgpt to review", "chatgpt review paper", "chatgpt review writing",
        "chatgpt review document", "chatgpt review email", "chatgpt reviewer prompt",
        "review using", "using ai to", "prompt for",
    ]
    def is_noise(kw):
        kl = kw.lower()
        return any(p in kl for p in NOISE_PATTERNS)

    all_suggest = [k for k in all_suggest if not is_noise(k)]
    all_related = [k for k in all_related if not is_noise(k)]

    # Build KW candidates: seed[0] is primary, rest are longtail
    primary_kw  = seeds[0]
    longtail_kw = list(dict.fromkeys(all_suggest + all_related))[:30]

    plan = {
        "slug":        slug,
        "kind":        kind,
        "primary_kw":  primary_kw,
        "longtail_kw": longtail_kw,
        "paa":         all_paa[:10],
        "serp_top10":  all_organics[:10],
        "seeds_used":  seeds[:3],
    }

    out = KW_DIR / f"{slug}.json"
    out.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")

    # Print summary
    print(f"\nPRIMARY KW:  {primary_kw}")
    print(f"LONGTAIL ({len(longtail_kw)}):")
    for k in longtail_kw[:15]: print(f"  {k}")
    print(f"PAA ({len(all_paa)}):")
    for q in all_paa[:5]: print(f"  {q}")
    print(f"SERP TOP5:")
    for o in all_organics[:5]: print(f"  #{o['rank']} {o['url'][:65]}")
    print(f"\nSaved: {out}")
    return plan


if __name__ == "__main__":
    cmd  = sys.argv[1] if len(sys.argv) > 1 else ""
    args = sys.argv[2:]

    if cmd == "page":
        page_kw_plan(args[0], kind="tool")
    elif cmd == "article":
        page_kw_plan(args[0], kind="article")
    elif cmd == "seed":
        d = serp(" ".join(args))
        related, paa, organics = extract_kw_signals(d)
        suggest = autocomplete(" ".join(args))
        print("SUGGEST:", suggest[:10])
        print("RELATED:", related)
        print("PAA:", paa)
        print("TOP5:", [o["url"] for o in organics[:5]])
    else:
        print(__doc__)
