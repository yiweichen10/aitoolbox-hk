#!/usr/bin/env python3
"""Generate the 'AI Tool Free Tier Report 2026' article — sister piece to the
Pricing Index. All figures injected from data/tools_en.json at run time.

Classification rules (conservative, label-driven — no invented terms):
  open-source : label or pricing_details mention open-source/self-hosting
  credits     : label mentions credits OR a numeric usage allowance (e.g. 'Free (1,000 ops/mo)')
  trial       : label mentions trial (and is not a Free+paid combo)
  freemium    : 'Free' combined with a paid tier ($X/mo or '(limited)')
  free-only   : label shows only Free, no paid tier mentioned
  (unspecified free labels are counted inside free-only with the caveat stated)

Slug stays fixed: ai-tool-free-tier-report-2026 (monthly refresh, same URL).
"""
import json
import re
from datetime import date

ARTICLES = "data/articles_en.json"
SLUG = "ai-tool-free-tier-report-2026"
DATE = date.today().isoformat()
CATEGORY = "AI Guide"


def classify(t):
    blob = (t.get('price', '') + ' ' + (t.get('pricing_details') or '')).lower()
    if 'open-source' in blob or 'open source' in blob or 'self-host' in blob:
        return 'open-source'
    if re.search(r'credit', blob):
        return 'credits'
    p = t.get('price', '').lower()
    if 'trial' in p and not re.search(r'free\s*[+&]', p):
        return 'trial'
    # numeric allowance inside the label: 'Free (1,000 ops/mo)'
    if re.search(r'free\s*\([^)]*\d', p):
        return 'credits'
    if 'free' in p and (re.search(r'\$\d', p) or '(limited)' in p):
        return 'freemium'
    if 'free' in p:
        return 'free-only'
    return None


def top_tools(tools, cat, n=6):
    pool = [t for t in tools if classify(t) == cat]
    pool.sort(key=lambda t: -float(re.sub(r'[^\d.]', '', str(t.get('rating', ''))) or 0))
    return [t['name'] for t in pool[:n]], len(pool)


def main():
    tools = json.load(open(ARTICLES.replace('articles_en', 'tools_en'), encoding='utf-8'))
    total = len(tools)
    counts = {'open-source': 0, 'credits': 0, 'trial': 0, 'freemium': 0, 'free-only': 0}
    reps = {}
    for t in tools:
        c = classify(t)
        if c:
            counts[c] += 1
    for c in counts:
        reps[c], _ = top_tools(tools, c)
    free_total = sum(counts.values())
    free_pct = free_total / total * 100

    def names(cat):
        return ', '.join(reps[cat][:4])

    def link(cat, n=3):
        pool = sorted([t for t in tools if classify(t) == cat],
                      key=lambda t: -float(re.sub(r'[^\d.]', '', str(t.get('rating', ''))) or 0))
        return ', '.join(f"[{t['name']}](https://www.aitoolbox.hk/tools/{t['slug']}/)"
                         for t in pool[:n])

    title = f"AI Tool Free Tier Report 2026: What Free Actually Gets You"
    content = f""""Free" is the most common word in AI tool pricing — and the least standardized. Across the {total} tools in our catalog, {free_total} ({free_pct:.0f}%) advertise some form of free access. But the label "free" covers five very different deals: software you can self-host forever, a monthly allowance of credits, a permanent-but-limited plan, a fully free product, and a countdown trial. This report breaks the {free_total} down by what "free" actually means, using the published price labels in our database on {DATE}.

## The five shapes of free

| Shape | Tools | Share of catalog | What it really is |
|---|---|---|---|
| Freemium | {counts['freemium']} | {counts['freemium']/total*100:.0f}% | A permanent free tier with hard limits, next to paid plans |
| Credits-based | {counts['credits']} | {counts['credits']/total*100:.0f}% | A monthly allowance that resets — heavy use burns it fast |
| Free-only | {counts['free-only']} | {counts['free-only']/total*100:.0f}% | No paid tier in the label at all |
| Open-source / self-host | {counts['open-source']} | {counts['open-source']/total*100:.0f}% | The code is free; you pay in setup time and compute |
| Time-boxed trial | {counts['trial']} | {counts['trial']/total*100:.0f}% | Full access on a countdown — then the paywall |

The median entry price among tools that publish one is covered in our [AI Tool Pricing Index](https://www.aitoolbox.hk/articles/ai-tool-pricing-index-2026/); this report is about the other side of the same question — what you get before you pay anything.

## Freemium: the permanent sample

{counts['freemium']} tools — {names('freemium')} among them — run the freemium model: a free tier that never expires but caps something that matters. The pattern to watch is *which* knob the free tier turns down. Chat assistants usually cap volume (messages per day); image and video generators cap generation counts and export quality; collaboration tools cap seats or history.

The honest read: a freemium tier is a product demo with usage attached. It is genuinely useful for evaluation and light personal work, and almost always annoying at production volume. That is by design — the free tier exists to prove the workflow fits before the upgrade conversation.

## Credits: renting, not owning

{counts['credits']} tools sell access through credit allowances — {link('credits', 4)} all work this way. Credits map cost to consumption, which sounds fair until you learn the per-credit price of the thing you actually want. Heavy users often end up paying more per output than a flat plan would cost; light users leave paid credits unused. Check the reset window before committing: a monthly reset you cannot bank is the difference between a real allowance and a marketing one.

## Free-only: read the business model

{counts['free-only']} tools publish only a free label. Some are genuinely free products backed by a larger business; some are open-core with a paid cloud; a few are free during a launch window. The label tells you there is no price tag on the page — it does not tell you the resource limits. For these, the limit lives in the docs, not the pricing card.

## Open-source: free, with a bill attached

{counts['open-source']} tools — {link('open-source', 3)} — are free in the strongest sense: self-host and there is no seat fee and no usage meter. The costs move to compute and maintenance. Running a local image model on your own GPU is free the way a garden is free: excellent value, real labor. For privacy-sensitive work this shape is often the only acceptable one.

## Trials: the countdown

{counts['trial']} tools gate everything behind a time-boxed trial — {names('trial')} among them. Trials are the least useful "free" for building a habit: you get the full product for days, not the limited product forever. If a tool only offers a trial, evaluate it with your real workload immediately, because the clock starts on signup.

## How we classified this

Each tool's published price label in our catalog was matched against five patterns on {DATE}, in priority order: open-source/self-host mentions first, then credit allowances, then trial-only labels, then Free-plus-paid combinations (freemium), then free-only labels. Labels are the vendors' own wording — we did not re-test each free tier's limits, and vendors change terms without notice. Verify the current terms on the vendor's page before relying on a free tier for production work.

## Frequently asked questions

**What percentage of AI tools are actually free?**
{free_total} of {total} tools ({free_pct:.0f}%) in our catalog advertise free access in some form. But only {counts['open-source']} are open-source (free without usage limits), and {counts['freemium']} are freemium (permanently free within limits). "Free" is not one thing — the five shapes above differ sharply in what you can do before paying.

**Which free tier is best for heavy use?**
Open-source tools, if you can self-host — there is no usage meter. Otherwise, freemium tools with generous permanent tiers beat credit-based tools for predictable workloads, because credits scale with consumption and heavy months cost more.

**Are free AI tools safe for work data?**
Treat free tiers like any cloud service: check the vendor's data-retention terms before pasting anything confidential. Open-source self-hosted tools are the exception — the data never leaves your machine. Many employers now publish an AI usage policy; read it first.

**Do free tiers expire?**
Freemium tiers and open-source licenses do not expire; trials do. Credit allowances usually reset monthly. The trap is vendors quietly narrowing a freemium tier over time — we refresh this report monthly, and the [Pricing Index](https://www.aitoolbox.hk/articles/ai-tool-pricing-index-2026/) tracks the paid side.

## Use this report

Quote it with attribution and note the {DATE} snapshot date. Each tool linked above goes to its full review, where the pricing card shows the current published label and the review covers what the free tier can and cannot do.
"""

    desc = (f"{free_total} of {total} AI tools advertise free access — but 'free' means five different "
            f"things. Freemium ({counts['freemium']}), credits ({counts['credits']}), open-source "
            f"({counts['open-source']}), free-only ({counts['free-only']}), trials ({counts['trial']}). "
            f"Original data, reproducible method.")
    keywords = ("AI tools free tier,free AI tools 2026,freemium AI tools,AI tool credits explained,"
                "open source AI tools,free vs paid AI tools,AI free tier limits")
    article = {
        "title": title,
        "seo_title": "AI Tool Free Tier Report 2026",
        "slug": SLUG,
        "date": DATE,
        "category": CATEGORY,
        "description": desc,
        "keywords": keywords,
        "content": content,
    }
    arts = json.load(open(ARTICLES, encoding="utf-8"))
    arts = [a for a in arts if a.get("slug") != SLUG]
    arts.append(article)
    with open(ARTICLES, "w", encoding="utf-8") as f:
        json.dump(arts, f, ensure_ascii=False, indent=2)
    print(f"[OK] '{SLUG}' written. free={free_total}/{total} "
          f"{dict(counts)} | articles total: {len(arts)}")


if __name__ == "__main__":
    main()
