# -*- coding: utf-8 -*-
"""Append article #221: LLM API Pricing Compared 2026."""
import json

ART = {
    "title": "LLM API Pricing Compared in 2026: GPT-6 Astra vs Claude Opus 5.5 vs Gemini 4 vs DeepSeek",
    "slug": "best-llm-api-pricing-2026-openai-gpt-6-vs-claude-opus-5-5-vs-gemini-4-vs-deepseek-compared",
    "date": "2026-11-14",
    "dateFull": "November 14, 2026",
    "category": "AI Infrastructure",
    "description": "GPT-6 Astra bills $10/$50, Opus 5.5 $4/$20, Gemini 4 Carbon doubles to $4/$20 on December 1, DeepSeek V4-Pro runs $0.66-$1.32 input. Cache economics, surcharges, worked bills.",
    "keywords": [
        "LLM API pricing",
        "GPT-6 Astra pricing",
        "Claude Opus 5.5 pricing",
        "Gemini 4 API pricing",
        "DeepSeek API pricing",
        "cheapest LLM API",
        "GPT-5.6 Sol pricing",
        "LLM API price comparison",
        "prompt caching savings",
        "DeepSeek off-peak pricing",
    ],
    "content": r"""The same million input tokens and million output tokens cost $60 on OpenAI's GPT-6 Astra, $24 on Claude Opus 5.5, $12 on Gemini 4 Carbon through November 30, and $5.28 on DeepSeek V4-Pro at peak rates — an 11x spread between four frontier models that all advertise million-token context windows, and 23x if you catch DeepSeek's off-peak meter. November 2026 is the worst month in years to lock a rate card without checking the expiration dates. Three clocks are running at once: OpenAI's GPT-5.6 Sol promotional pricing holds "at least through November 21," Google doubles Gemini 4 Carbon and Argon from $2/$10 to $4/$20 on December 1, and the Gemini Flash line doubles on January 1, 2027. Anthropic spent 2026 pushing the other way — Opus 5.5 shipped at $4/$20, down from Opus 5's $5/$25, and a scheduled Sonnet increase was cancelled outright. This guide breaks down LLM API pricing across the four vendors on numbers pulled from their own pricing pages this week: list rates, cache economics, long-context surcharges, and worked bills at real volume.

## What Changed in 2026: Two Vendors Raised Prices While Two Cut Them

April 2026: OpenAI ships GPT-5.5 at $5 per million input and $30 per million output — roughly double GPT-5.4 — and positions it as the agent-and-coding flagship. By November the menu has moved again. The current OpenAI rate card runs four text models: GPT-6 Astra at $10/$50, GPT-5.6 Sol at $4/$20 (a promotional rate the pricing page says holds "at least through November 21"), GPT-5.6 Terra at $2/$12, and GPT-5.6 Luna at $0.20/$1.20. Every model carries a 1.05 million-token context window with 128K maximum output, and every published price is a short-context price: beyond 272,000 input tokens, OpenAI bills input at 2x, cached input at 2x, and output at 1.5x. Filling Astra's window is not a $10-per-million exercise; it is a $20 one.

Anthropic's 2026 went the opposite way. Claude Opus 5.5 landed at $4/$20 — a fifth cheaper on input than the $5/$25 Opus 5 it succeeded. The pricing docs carry an unusual footnote: Sonnet 5's $2/$10 was announced as introductory pricing through August 31, 2026, the planned rise to $3/$15 on September 1 never happened, and $2/$10 is now the standard rate. The budget tier got its own reset — Haiku 5.5 costs $0.10/$0.50 for prompts up to 100,000 tokens, one-fifth of Haiku 4.5's $1/$5, though prompts beyond that threshold jump to $0.50/$2.50.

Google's Gemini 4 family (Carbon, Argon, Hydrogen) launched on intro pricing that doubles in December: Carbon and Argon move from $2/$10 to $4/$20 on December 1, and cache reads rise from $0.10 to $0.20 the same day. The Flash line gets its own doubling on January 1, 2027 — 3.8 Flash goes from $0.75/$3.75 to $1.50/$7.50. Gemini 2.5 Pro is retired; requests route to 3.8 Flash at Flash rates from December 1.

DeepSeek restructured its meter instead of its levels. The V4 generation splits into deepseek-flash and deepseek-v4-pro, both with 1M context and up to 384K output, billed at peak and off-peak rates. Peak hours are 01:00–04:00 and 06:00–10:00 UTC on weekdays — seven hours a day, five days a week. Every other hour, including the whole weekend, bills at exactly half.

## LLM API Pricing at a Glance: Four Frontier Rate Cards

| Model | Input / 1M | Output / 1M | Cache read / 1M | The catch |
|---|---|---|---|---|
| OpenAI GPT-6 Astra | $10.00 | $50.00 | $1.00 | 2x input / 1.5x output beyond 272K tokens |
| Claude Opus 5.5 | $4.00 | $20.00 | $0.20 | Fable 5.2 ($8/$40) sits above it |
| Gemini 4 Carbon | $2.00, then $4.00 Dec 1 | $10.00, then $20.00 Dec 1 | $0.10, then $0.20 | Intro pricing expires; implicit caching only |
| DeepSeek V4-Pro | $1.32 peak / $0.66 off-peak | $3.96 / $1.98 | $0.044 / $0.022 | 500 concurrent-request cap |

Read the cache column as a multiple of list input and the gaps widen: Astra charges 10 percent of its input rate for a cache read, Opus 5.5 charges 5 percent, Carbon 5 percent until it doubles, and DeepSeek about 3 percent with no write premium. Batch halves everything on the first three — Astra's input drops to $5, Opus 5.5 to $2, Carbon to $1 — while DeepSeek's batch equivalent is simply the off-peak clock that covers roughly 79 percent of the week.

## The Frontier Tier: What $60, $24, $12, and $5.28 Buy

Price the same benchmark — 1M tokens in, 1M tokens out — and the frontier splits into three bands. Astra is alone at the top: $60 a blended million, a knowledge cutoff of April 30, 2026, and the only model here whose output cap (128K) is a fraction of its rivals' decode ranges. Sol, Opus 5.5, and Carbon-in-December cluster at $24, which is the number worth remembering: Google's intro price is a loan, and on December 1 Carbon lands exactly on the Sol/Opus line. V4-Pro undercuts all of it at $5.28 peak, $2.64 off-peak — with two strings attached. The concurrency cap is 500 requests, versus effectively pooled capacity at the hyperscalers, and DeepSeek's published web-tool add-ons ($0.75 per 1,000 searches or fetches, $0.225 per 1,000 pages parsed) are separate line items rather than bundled features.

Anthropic also sells a tier above Opus now: Claude Fable 5.2 at $8/$40, with the limited-availability Mythos 5.2 alongside. If your workload genuinely needs it, the price is real; most teams evaluating frontier models will never touch it.

## The Workhorse Tier: Where Real Volume Lives

Frontier flags get planted in demos; bills get written in the workhorse tier. Same four vendors, same structure:

| Model | Input / 1M | Output / 1M | Cache read / 1M | Watch for |
|---|---|---|---|---|
| GPT-5.6 Terra | $2.00 | $12.00 | $0.20 | 2x/1.5x surcharge beyond 272K input |
| Claude Sonnet 5.5 | $2.00 | $10.00 | $0.10 | $2/$10 made permanent; rise cancelled |
| Gemini 3.8 Flash | $0.75 | $3.75 | $0.075 | Doubles January 1, 2027 |
| deepseek-flash | $0.30 / $0.15 off-peak | $1.20 / $0.60 | $0.006 / $0.003 | 2,500-request concurrency cap |

The budget shelf below that tier is the deepest it has ever been. OpenAI's Luna prices output at $1.20 — the same number as deepseek-flash's peak rate — with cached input at $0.02. Haiku 5.5 undercuts everything at $0.10/$0.50 for sub-100K prompts. Gemini 3.5 Flash-Lite holds at $0.30/$2.50 with no announced increase. And GPT-5.1, the previous OpenAI workhorse at $1.25/$10, is still on sale; price trackers that snapshot daily have recorded no move since August. None of these numbers requires a negotiated contract, a reserved-commitment discount, or a sales call — they are the metered list prices any credit card can hit today.

## Prompt Caching Is the Third Price Column

Every vendor now prices a cached token differently from a fresh one, and the deltas are large enough to reorder a comparison. OpenAI's structure on the 5.6 generation mirrors Anthropic's: cache reads run at 10 percent of list input (Sol $0.40, Astra $1.00), but writes carry a premium — $5.00 per million for a 30-minute TTL and $10.00 for a 12-hour one on Sol. Anthropic charges 1.25x list input for a 5-minute write and 2x for an hour, then reads back at 5 percent on current models — $0.10 on Sonnet 5.5, $0.20 on Opus 5.5 — with break-even after a single read. Google only supports implicit caching on Gemini 4, which means you cannot pin a retrieval corpus the way explicit caching APIs let you — a real constraint for RAG stacks, which we compared in our vector database review — and several Flash models add a storage fee per million cached tokens per hour. DeepSeek remains the outlier: no write premium, and a V4-Pro cache hit at $0.044, about 3 percent of its peak input price.

Run the numbers on the support-chatbot shape — 20M input and 4M output a month, 75 percent of input served from cache, one-time write premiums excluded — and caching cuts Anthropic's bill from $160 to $103, Astra's from $400 to $265, and DeepSeek's peak bill from $42.24 to $23.10. The ordering does not change. The magnitude does: on agent loops that resend the same system prompt and file context all day, the cache column is routinely worth more than a list-price negotiation would be.

## Three Worked Bills at Real Volume

Every bill below applies list-price LLM API pricing with no caching, no batch discounts, and no negotiation — the worst case a brand-new account can hit.

| Monthly workload | GPT-6 Astra | Claude Opus 5.5 | Gemini 4 Carbon | DeepSeek V4-Pro |
|---|---|---|---|---|
| Benchmark: 1M in + 1M out | $60 | $24 | $12 ($24 Dec 1) | $5.28 ($2.64 off-peak) |
| Support chatbot: 20M in + 4M out | $400 | $160 | $80 ($160 Dec 1) | $42.24 ($21.12) |
| Coding agent: 540M in + 108M out | $10,800 | $4,320 | $2,160 ($4,320) | $1,140.48 ($570.24) |
| Batch pipeline: 100M in + 10M out, half rates | $750 | $300 | $150 ($300) | $85.80 off-peak |

The coding-agent row assumes 300 sessions a day at 60K input and 12K output each. It is also the row where the fine print bites hardest: push any single Astra session past 272K input tokens and that session's inputs bill at 2x and its outputs at 1.5x — a long-context agent can clear $15,000 on the same request count. The workhorse tier tells the opposite story. The identical agent load costs $2,376 on GPT-5.6 Terra, $810 on Gemini 3.8 Flash ($1,620 from January 1), and $291.60 on deepseek-flash at peak, $145.80 off-peak. The spread inside one vendor's menu is now wider than the spread between vendors — which is why model selection, not vendor selection, moves most bills.

## When DeepSeek Is the Rational Default — and When It Is Not

DeepSeek's off-peak window deserves a second look from US-based teams, because the peak hours are drawn in UTC: 01:00–04:00 and 06:00–10:00, which maps to 8:00–11:00 PM and 1:00–5:00 AM Eastern. American business hours are entirely off-peak. A US office running batch extraction, evaluation suites, or background summarization during the workday pays the half rate all day, every day — the full picture is on our DeepSeek V4 tool profile.

The honest caveats: 500 concurrent requests on V4-Pro and 2,500 on flash are hard caps that high-fanout agent fleets can hit, the API bills its web-search and file-parsing tools separately — the same unbundling we documented across search APIs — and the standard disclaimer applies with extra force here: a price sheet says nothing about whether the model is good enough for your task. Run both models on your own traffic before migrating anything; a 5x cheaper model that needs 3x the tokens to finish a job is not cheaper. Teams that end up running a mixed fleet — a cheap model for drafts, a frontier one for the hard turn — usually wrap the routing in a gateway rather than hardcoding endpoints; we compared the main options in our LLM gateway roundup.

## Frequently Asked Questions

### How much does the GPT-6 Astra API cost?

GPT-6 Astra costs $10.00 per million input tokens and $50.00 per million output tokens at standard rates, with cached input at $1.00 per million. Those prices apply up to 272,000 input tokens; beyond that, input bills at 2x ($20.00), cached input at 2x, and output at 1.5x ($75.00). Batch processing halves the short-context rates, and Fast mode — OpenAI's priority lane — runs at double.

### Is Claude Opus 5.5 cheaper than GPT-5.6 Sol?

On paper they are identical: $4.00 input and $20.00 output per million tokens. The differences sit underneath — Opus 5.5 reads cached input at $0.20 (5 percent of list) versus Sol's $0.40, and Anthropic publishes no long-context surcharge, while Sol inherits OpenAI's 2x/1.5x multipliers past 272K tokens. Sol's rate is also explicitly promotional through at least November 21, 2026, so the two may not stay matched. At blended list price, both cost $24 per million-in-plus-million-out — the same number Gemini 4 Carbon hits on December 1.

### What is the cheapest LLM API in 2026?

For usable quality at scale, deepseek-flash is the cheapest metered option in this comparison: $0.30/$1.20 at peak and $0.15/$0.60 off-peak, with cache hits at $0.006. Anthropic's Haiku 5.5 posts the cheapest single rate at $0.10/$0.50, but only for prompts under 100,000 tokens. OpenAI's Luna ($0.20/$1.20) and Gemini 3.5 Flash-Lite ($0.30/$2.50) bracket the sub-dollar tier. Anything promising frontier quality below these numbers is either an open-weight model on a third-party host or a loss leader — read the throughput and concurrency limits before you migrate.

### Why is Gemini 4 pricing increasing on December 1, 2026?

Google launched the Gemini 4 family (Carbon, Argon, Hydrogen) on introductory pricing — $2/$10 for the frontier models — with the increase published on its own pricing page from day one: $4/$20 beginning December 1, 2026, with cache reads doubling to $0.20 the same day. The Flash line follows on January 1, 2027, moving from $0.75/$3.75 to $1.50/$7.50. It is the intro-then-step-up pattern in its purest form, and it means any annual commitment signed in November on Gemini 4 rates should be modeled at the December numbers, not the current ones.

### How do DeepSeek's off-peak prices work?

DeepSeek bills deepseek-flash and V4-Pro at two rates. Peak hours are 01:00–04:00 and 06:00–10:00 UTC, Monday through Friday, excluding Chinese public holidays — 35 hours a week. Everything else, including the entire weekend, bills at exactly half: $0.66 input and $1.98 output on V4-Pro, $0.15/$0.60 on flash, with cache hits at $0.022 and $0.003 respectively. Off-peak is not a separate batch queue with worse latency; it is the same synchronous API on the same endpoints, which makes it usable for interactive traffic, not just overnight jobs.

## The Bottom Line

Four rate cards, four meters, and no single winner. If you need the highest ceiling regardless of cost, GPT-6 Astra is the tool — just model long-context sessions at the 2x/1.5x multipliers, because that is where its real bill lives. For coding agents and cache-heavy loops, Claude Opus 5.5 at $4/$20 with $0.20 cache reads and stackable 50 percent batch discounts is the most predictable frontier bill in the group. Gemini 4 Carbon is the market's cheapest frontier model for exactly sixteen more days; whatever you build on the $12 blended million, rebuild the budget at $24. And for high-volume, latency-tolerant work — extraction, evaluation, summarization, overnight pipelines — DeepSeek's off-peak meter remains untouchable at $2.64 a blended million. Prices moved in both directions at once this year, which means last quarter's LLM API pricing comparison is already a liability. Check the meters monthly, and route the fleet through a gateway so switching costs stay near zero.""",
}

def main():
    path = "data/articles_en.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    arts = data if isinstance(data, list) else data["articles"]
    slugs = [a["slug"] for a in arts]
    if ART["slug"] in slugs:
        raise SystemExit("slug already exists: " + ART["slug"])
    arts.append(ART)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("appended:", ART["slug"], "| total articles:", len(arts))

if __name__ == "__main__":
    main()
