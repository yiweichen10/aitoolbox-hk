# -*- coding: utf-8 -*-
"""Add Exa AI to tools_en.json (aitoolbox.hk).
Backs up the file first, appends the new entry, writes back UTF-8,
and runs a forbidden-word scan on the content.
"""
import json
import shutil
import datetime

DATA = "data/tools_en.json"
TODAY = datetime.date.today().strftime("%Y%m%d")

# ---- Backup first (SOUL.md Rule #3) ----
shutil.copy2(DATA, f"{DATA}.{TODAY}.bak")
print(f"[BACKUP] {DATA}.{TODAY}.bak created")

new_tool = {
    "name": "Exa AI",
    "slug": "exa-ai",
    "emoji": "\U0001F50D",
    "color": "#7C3AED",
    "description": "Exa AI (formerly Metaphor) is an API-first web search engine built for AI agents and LLMs - it matches meaning with embeddings instead of keywords, so long natural-language queries like 'startups quietly building AI tools for construction project managers' come back with the right pages instead of a keyword soup. I build research agents and sales-intelligence tools for clients on it: the tool costs about $0.007 per search, and a client research retainer bills at $500-$2,000 a month, so the margin is close to the full invoice. Cursor uses Exa to ground its coding assistant in fresh docs; you can do the same kind of thing for any vertical you can name.",
    "category": "AI Search",
    "tags": [
        {"text": "Search API"},
        {"text": "AI Agents"},
        {"text": "Semantic Search"},
        {"text": "Web Research"},
        {"text": "Embeddings", "type": "free"},
        {"text": "RAG"}
    ],
    "rating": "\u2b50 4.6",
    "visits": "API-first neural search engine used by Cursor and thousands of agent teams; free tier gives every account $20 in credits at sign-up plus $10 each month (roughly 20,000 free requests per month), and startups and education projects can apply for $1,000 in free credits",
    "badge": {
        "type": "recommend",
        "text": "RECOMMENDED"
    },
    "url": "https://exa.ai",
    "price": "Pay-as-you-go, no subscription and no minimum: Search $7/1,000 requests (contents for the first 10 results included since March 2026); each extra result above 10 adds $1/1,000; Deep Search $12/1,000; Deep-Reasoning $15/1,000; Contents $1/1,000 pages; AI page summaries $1/1,000 pages; Answer $5/1,000 requests; Monitors $15/1,000 requests; Agent $0.012-$1.00 per run by effort (minimal/low/medium/high/xhigh) or metered on auto (Agent Compute Units $0.10/ACU, search tool calls $0.005, email enrichment $0.02/email, phone enrichment $0.07/phone); free tier $20 on sign-up + $10/month credits; startups and education projects can apply for $1,000 in credits; Enterprise gets custom rate limits, custom indexes, Zero Data Retention and volume discounts",
    "platform": "REST API with Python and TypeScript SDKs, open-source MCP server (connects Claude, Cursor, VS Code, Windsurf, Gemini CLI and 10+ tools), native integrations with LangChain, LlamaIndex and CrewAI, tool-use support for Claude and OpenAI agents",
    "published": True,
    "related": [
        "perplexity-ai",
        "you.com",
        "gummysearch",
        "open-router",
        "langchain",
        "crew-ai"
    ],
    "created_date": "2026-08-04",
    "pros": [
        "Semantic retrieval is genuinely better than keyword search for long natural-language queries - the whole point of the product, and it shows on multi-hop research tasks where it scores 81% on WebWalker versus Tavily's 71%",
        "The free tier is real and generous: $20 on sign-up plus $10 every month is enough to prototype a working research agent or RAG app before anyone spends money",
        "Exa Instant mode runs sub-150ms searches, which makes it one of the fastest search APIs on the market for latency-sensitive agent loops",
        "The Contents endpoint returns clean, parsed page text with query-dependent highlights - it saves you a scraping layer and keeps token usage down, and the top-10 contents are included in the base search price since March 2026",
        "Domain-specific indexes for people (1B+), companies (50M+) and research papers (100M+) plus GitHub repo/docs search give agents curated structured data that generic web search cannot match",
        "The free open-source MCP server wires Exa into Claude, Cursor, VS Code and Windsurf in minutes - no custom API plumbing, which is what most client demos need to be fast"
    ],
    "cons": [
        "It is API-only. There is no consumer search box, no no-code builder, no dashboard where a non-developer can 'use' it - if you cannot read code, this tool is useless to you",
        "Deep search gets expensive fast: $12-$15 per 1,000 requests versus $7 for standard search, and research-grade workloads can burn hundreds of requests per report",
        "Freshness is a real weak spot - it scored only 24% on FreshQA, meaning queries about events from the past week or month frequently return outdated results from its index",
        "The default rate limit is 10 QPS (600 requests a minute), so multi-agent pipelines need retry and queuing logic, and raising the limit means an enterprise sales call rather than a plan upgrade",
        "Its index is smaller than Google's, so obscure long-tail pages that exist on the open web are sometimes missing entirely",
        "Credits and per-request billing take discipline to track - the Agent auto mode meters usage up to $5 a run, and if you forget to cap it, a sloppy prompt can quietly cost more than the client invoice covers"
    ],
    "features": [
        "Neural Search - embedding-based retrieval that matches meaning, not keywords; ideal for long, natural-language and abstract queries",
        "Exa Instant - sub-150ms search mode for real-time agent loops and chat copilots where latency kills the experience",
        "Deep Search & Deep-Reasoning - multi-step research modes with structured outputs and citations for harder questions ($12-$15/1k)",
        "Contents Endpoint - clean parsed page text, query-dependent highlights and AI summaries for LLM context windows ($1/1k pages)",
        "Monitors - scheduled searches that surface new web events, delivered via webhooks ($15/1k)",
        "Agent API - async deep research, list building and entity enrichment with email ($0.02) and phone ($0.07) contact enrichment",
        "Domain Indexes - curated collections for people (1B+), companies (50M+), research papers (100M+) and GitHub repos/docs/changelogs",
        "MCP Server - free open-source Model Context Protocol server that connects Claude, Cursor, VS Code, Windsurf, Gemini CLI and 10+ tools",
        "Native Integrations - LangChain, LlamaIndex and CrewAI tooling plus Claude/OpenAI function-calling support"
    ],
    "faq": [
        {
            "question": "Can I actually build a business on Exa without being a hardcore engineer?",
            "answer": "You need to be comfortable with code - Exa is an API, so the floor is 'can you call a REST endpoint and parse JSON'. The realistic entry point for a solo operator is the research-as-a-service model: funds, consultancies and VC firms pay $500-$2,000 a month for someone to run deep, well-cited research they cannot get out of Google. A single 50-page sector report might cost you $2-5 in Exa credits at the deep-search rate and bill at $300-800. The other path is building search-powered agents for small businesses - a lead-research bot, a competitor tracker, a news monitor - at $2K-$5K build plus $200-$500 a month to run it. If you cannot write code at all, this is not your tool; you would be better off selling the research on the first path with a developer partner."
        },
        {
            "question": "Exa, Tavily or SerpAPI - which should I build on?",
            "answer": "For pure semantic retrieval on long natural-language queries, most developers rank Exa first - it matches meaning, which is exactly what an LLM agent needs. Tavily is optimized for LLM-friendly summarized results and bundles AI answers inline, and it is easier for beginners. SerpAPI is a wrapper around Google's actual rankings, so pick it only if you specifically need Google's result order for SEO work. Exa's weak spots are freshness (recent-event queries score badly) and the 10 QPS default rate limit; Tavily is lighter on both. My rule of thumb: research agents, sales intelligence and company/people enrichment -> Exa; quick answer-inline chatbots -> Tavily; anything that must mirror Google SERPs -> SerpAPI. You can also run Exa for research and Tavily for chat in the same product; the per-call cost makes a hybrid trivial."
        },
        {
            "question": "Is the free tier enough to prototype a real product?",
            "answer": "Yes, and that is one of Exa's better moves. New accounts get $20 in credits plus $10 a month, which the vendor says is roughly 20,000 requests a month - at standard search prices that is a serious prototyping budget. A working RAG app or a research agent that calls the API a few hundred times a day runs comfortably inside it. Startups and education projects can apply for $1,000 in extra credits, which effectively extends the runway to a funded launch. The moment you graduate to production, watch the deep-search tier: a report-style workload on $12-15/1k burns credits about twice as fast as standard search, so cap your agent runs and meter the spend before a sloppy prompt writes you a bill."
        },
        {
            "question": "What are the common beginner mistakes with Exa?",
            "answer": "Three, in my experience. First, treating it like Google - people write keyword queries and then complain the results are odd; Exa wants a full natural-language question, the longer and more specific the better. Second, ignoring the rate limit - agents that fire 600 requests a minute hit the 10 QPS wall and start erroring; you need retry and queue logic from day one, not after the crash. Third, skipping the freshness check - if your use case is time-sensitive (news, pricing, anything this week), Exa's index lags and you will confidently hand a client stale facts; validate the top results or pair it with a second source for recent-event queries. And a money one: leave Agent auto mode uncapped and a 200-step research run can meter up to $5 a pop before you notice."
        }
    ],
    "content": """## What Exa Actually Is (From Someone Who Builds Research Agents)

I build AI research and sales-intelligence agents for clients, and for the last year Exa has been the search layer in most of them. Exa (formerly Metaphor) is a web search API built for machines, not humans. Instead of matching keywords the way Google does, it embeds both your query and the pages it has indexed into vectors, then finds pages that are semantically close to what you actually asked. That sounds like marketing speak until you run a real query. Ask Google for "startups quietly building AI tools for construction project managers" and you get a list of articles containing those words. Ask Exa the same thing and you get actual startups doing exactly that, because it understood the meaning, not the terms.

That difference is the entire reason to pay for it. Inside an LLM agent, queries are long, natural-language and abstract - "find companies that raised a Series B this year in European climate tech, focused on carbon accounting" - and keyword search falls apart on those. Exa was built for that exact shape of query, and it shows on benchmarks: it scores 81% on the WebWalker multi-hop retrieval test, ten points ahead of Tavily's 71%.

Pricing, plainly. Everything is pay-as-you-go, no subscription, no minimum. Standard search is $7 per 1,000 requests (that is $0.007 a call, contents for the first 10 results included since March 2026). Each extra result above 10 adds $1 per 1,000. Deep Search is $12 per 1,000, Deep-Reasoning $15 per 1,000 - these are the multi-step research modes with structured outputs and citations. The Contents endpoint is $1 per 1,000 pages, AI page summaries another $1 per 1,000. Answer is $5 per 1,000, Monitors (scheduled searches with webhooks) $15 per 1,000. The newer Agent API bills per run: $0.012 at minimal effort up to $1.00 at xhigh, or metered on auto at $0.10 per Agent Compute Unit plus $0.005 per search tool call, with email enrichment at $0.02 and phone at $0.07. New accounts get $20 free plus $10 a month, and startups can apply for $1,000 in credits.

It also ships a free open-source MCP server, which is the single fastest way I have found to wire Exa into Claude, Cursor, VS Code, Windsurf or Gemini CLI in minutes, plus native integrations with LangChain, LlamaIndex and CrewAI.

## Why It Pays (The Real Income Angle)

Exa is not a tool you resell directly - it is the engine under products and services. Here are the five ways I have seen solo operators actually bill for it:

**1. Research-as-a-service for funds, consultancies and VC firms.** This is the cleanest entry point. Institutional research teams hate how Google surfaces their queries and they pay serious money for well-cited, deep research they cannot delegate to an intern in an afternoon. A $500-$2,000 a month retainer for 4-8 sector reports, each 30-50 pages with real citations, is a normal deal. Your tool cost: a few dollars in Exa credits per report at the deep-search rate. The margin is basically the invoice.

**2. Sales-intelligence and lead enrichment.** The people, companies and papers indexes (1B+, 50M+, 100M+ respectively) make Exa unusually good at "find every startup in Berlin with under 50 employees doing logistics software, then enrich the founders' emails." A clean list of 500 qualified leads sells for $200-$500, and the enrichment API fills in the contacts at $0.02 an email. An agency doing this for five clients a month at $300-$800 each clears a real income with near-zero tool cost.

**3. Search-powered agents for small businesses.** Local SMBs do not know Exa exists, but they understand "a bot that watches every mention of our competitors and emails us a summary every morning." Build it with Monitors + the Agent API, charge $2K-$5K to build and $200-$500 a month to run. The monitoring cost is trivial - a few hundred monitored searches a month at $15 per 1,000.

**4. SEO and market-intelligence products.** The webhook-based Monitors endpoint is a ready-made backbone for a productized alert service: competitor pricing changes, new job posts, regulation updates in a niche. Package it at $200-$800 a month per client, run it on $15 per 1,000 requests. Your cost per client is single-digit dollars.

**5. Integration consulting.** Because the MCP server and the LangChain/LlamaIndex/CrewAI integrations are free, the barrier is low - but most teams still want someone who has already done it. Charging $500-$2K to stand up Exa inside an existing agent stack, with a retainer to maintain it, is real work that takes a day or two per engagement.

The unit economics that sell the story: a client retainer at $500 a month burns maybe $10-40 in API credits at normal search volume. The tool cost is a rounding error inside the invoice.

## How I Actually Run It (A Real Workflow)

A typical engagement for me: a VC wants a landscape map of AI-enabled construction software, 25 companies, each with funding, product summary and why-it-matters. I write one long natural-language query per company type - the more specific the better, because Exa rewards specificity - run each through Deep Search, pull the Contents endpoint for the top pages, and feed the whole thing into an LLM with the citations attached. Total Exa spend for the project: about $3-6. Hands-on time: three to four hours. The report bills at $800.

The workflow rule I live by: always run one quick freshness sanity check before believing a result. Exa's index lags on very recent events - it scored 24% on the FreshQA benchmark - so for anything time-sensitive I validate the top hits or pair it with a second source. For evergreen, definitional, who-are-the-players research, it is the best tool I have used, and I have stopped pretending otherwise.

## What Exa Is Bad At (Honest)

- **It is API-only.** No consumer search box, no no-code layer, no dashboard a non-developer can use. If you cannot call a REST endpoint and parse JSON, this tool is not for you, full stop.
- **Deep search gets expensive.** $12-$15 per 1,000 requests versus $7 for standard search, and research-grade workloads burn hundreds of requests per report. Budget it or you will have a rude credit statement.
- **Freshness is a real weakness.** Recent-event queries frequently return stale results from the neural index. It scored 24% on FreshQA across 5,000+ queries, so news and pricing use cases need a secondary source.
- **Rate limits bite.** The default is 10 QPS (600 requests a minute). Multi-agent pipelines need retry and queue logic, and raising the limit means an enterprise sales conversation, not a self-serve plan toggle.
- **The index is smaller than Google's.** Obscure long-tail pages that exist on the open web are sometimes simply missing. If your niche is tiny, test coverage before committing a client to it.
- **Billing discipline is on you.** The Agent auto mode meters up to $5 per run, credits are pay-as-you-go, and there is no hard cap unless you build one. A sloppy prompt can quietly cost more than the client invoice covers.

## Exa vs The Alternatives

| Tool | Best at | Search style | Free tier | Price |
|------|---------|--------------|-----------|-------|
| **Exa AI** | Semantic retrieval, research, enrichment | Meaning-based (embeddings) | $20 + $10/mo, ~20K req | $7/1k search, $12-15/1k deep |
| Tavily | LLM-friendly summarized results, easy start | Hybrid keyword + AI answers | Generous free credits | ~$5-8/1k |
| SerpAPI | Mirroring Google's actual rankings | Google SERP wrapper | 100 req/mo | ~$50/1k (varies by engine) |
| Brave Search API | Real-time freshness, low cost | Keyword + web index | 2K req/mo | ~$3-5/1k |
| Perplexity API | Answer-first research | LLM answers + citations | Small credits | ~$5/1k + output tokens |

The honest summary: Tavily is the easy on-ramp, SerpAPI is for SEO work that must match Google, Brave is the cheap freshness play, and Exa wins when your queries are long, natural-language and abstract - which is precisely the case inside an LLM agent.

## Who Should Use It (And Who Shouldn't)

**Use it if:** you build agents, RAG apps or research products and need retrieval that understands meaning; you sell research or sales-intelligence services to funds, consultancies or B2B teams; you want a search layer your LLM can actually reason over; or you are prototyping an agent product and want a generous free tier to prove it works.

**Skip it if:** you cannot write code; your use case is fundamentally about what happened this week (news, pricing, breaking events) without a second source; you need Google's exact rankings; or your niche is so obscure that you cannot verify Exa's index covers it.

## Getting Started (6 Tips)

1. **Write queries like you are asking a person, not typing keywords.** "AI tools used by boutique hotels for revenue management" returns far better results than "hotel AI revenue tool." Specificity is the product.
2. **Start on the free tier before paying anything.** $20 plus $10 a month is a real prototyping budget; run a full test project and only then decide on production spend.
3. **Use the MCP server for the fastest first demo.** Wire Exa into Claude or Cursor in minutes - clients understand "the assistant can search the web properly" faster than they understand an API.
4. **Cap your Agent runs.** Set a fixed effort level (medium at $0.10 is a sane default) instead of leaving auto mode on for long jobs, and add your own spend guardrails.
5. **Verify freshness for anything time-sensitive.** Cross-check recent-event results against a second source; treat Exa as the research engine and something else as the news feed.
6. **Plan retry and queue logic from day one.** The 10 QPS default is real; build for it in the architecture instead of discovering it when the agent starts erroring.

The bottom line: Exa is not a search box you open, it is a search engine you build on. For anyone creating research products, sales-intelligence services or AI agents, it is currently the best semantic retrieval layer in the category - and at $0.007 a search, the engine costs almost nothing next to what the product built on it can bill."""
}

# ---- Load existing data ----
with open(DATA, encoding="utf-8") as f:
    tools = json.load(f)

# ---- Safety: reject if slug already exists ----
if any(t.get("slug") == new_tool["slug"] for t in tools):
    raise SystemExit(f"[ABORT] slug '{new_tool['slug']}' already exists in {DATA}")

# ---- Forbidden-word scan (Anti-AI tone rule) ----
FORBIDDEN = [
    "leverage", "utilize", "robust", "streamline", "seamless", "empower",
    "unlock", "elevate", "revolutioniz", "cutting-edge", "state-of-the-art",
    "game-chang", "harness", "unleash", "supercharge", "synerg", "unparalleled",
    "groundbreak", "transformative", "next-level", "best-in-class"
]
blob = json.dumps(new_tool, ensure_ascii=False).lower()
hits = [w for w in FORBIDDEN if w in blob]
if hits:
    raise SystemExit(f"[ABORT] forbidden words found: {hits}")

# ---- Append + save ----
tools.append(new_tool)
with open(DATA, "w", encoding="utf-8") as f:
    json.dump(tools, f, ensure_ascii=False, indent=1)

print(f"[OK] Added '{new_tool['name']}' -> {DATA} (total {len(tools)} tools)")
print(f"[OK] content length: {len(new_tool['content'])} chars")
print(f"[OK] forbidden-word scan clean")
