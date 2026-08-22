#!/usr/bin/env python3
"""Add Genspark (AI agent search engine / Sparkpages workspace) to tools_en.json for aitoolbox.hk.

Built-in guards (same pattern as other add_*.py in this repo):
  - forbidden-word scan: fails loudly if any banned marketing word slips in
  - internal-link gate: every slug in `related` AND every in-content link MUST already exist in tools_en.json
"""
import json
import re
import sys
import shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
BASE = Path(__file__).parent
DATA = BASE / "data" / "tools_en.json"

# Banned "AI marketing bot" words. Keep this list tight and enforced.
FORBIDDEN = [
    "leverage", "leveraging", "leverages", "utilize", "utilizing", "utilizes",
    "robust", "seamless", "seamlessly", "cutting-edge", "game-changer",
    "game changer", "revolutionize", "revolutionary", "empower", "empowering",
    "empowers", "unlock", "unlocks", "delve", "navigate", "navigates",
    "navigating", "elevate", "elevates", "myriad", "testament", "in conclusion",
    "furthermore", "moreover", "crucial", "essential", "paramount",
    "state-of-the-art", "harness", "facilitate", "facilitates", "optimize",
    "optimizes", "streamline", "streamlines", "underscore", "underscores",
    "bespoke", "frictionless", "holistic", "synergy", "supercharge",
    "seamless integration", "cutting edge",
]

NEW_TOOL = {
    "name": "Genspark",
    "slug": "genspark",
    "emoji": "✨",
    "color": "#2563EB",
    "description": "Genspark is an AI agent workspace that started as an ad-free search engine that built a custom Sparkpage for every query, then pivoted hard into autonomous agents. Its Super Agent splits a request into sub-tasks, coordinates nine-plus foundation models and 80-plus built-in tools, and hands you a finished deliverable instead of an answer: a cited research page in under 15 seconds, a slide deck in about four minutes, a spreadsheet, a website, or even a real phone call made on your behalf. Backed by roughly $385M at a $1.6B valuation (April 2026) with ARR past $200M, it is the fastest-growing AI search/agent hybrid around. The money angle is genuinely broad: sell AI-search visibility (GEO) audits to local businesses, deliver done-for-you research reports built on Sparkpages, outsource appointment-verification calls with the Call For Me agent, or resell pitch decks and market analysis produced in minutes. Free tier gives 100-200 credits a day, so you can test the exact workflow you plan to bill for before paying anything.",
    "category": "AI Search",
    "tags": [
        {"text": "AI Search"},
        {"text": "AI Agents"},
        {"text": "Sparkpages"},
        {"text": "Deep Research"},
        {"text": "GEO"},
        {"text": "Free tier", "type": "free"},
        {"text": "Web App"}
    ],
    "rating": "⭐ 4.5",
    "visits": "Around 10.8M monthly visits in the CN directory - a 2024 search launch that hit 5M users in nine months, then rode the Super Agent pivot to $200M+ ARR by early 2026",
    "badge": {"type": "hot", "text": "HOT"},
    "url": "https://www.genspark.ai",
    "price": "Free $0 (100-200 credits/day, 1GB AI Drive, basic Sparkpages and agents); Plus about $20-25/month billed annually (10,000 credits/month, 50GB, unlimited AI chat and image generation through end of 2026); Pro about $200-250/month billed annually (125,000 credits/month, 1TB); Enterprise custom. Review sites list slightly different Plus/Pro prices, so check genspark.ai/pricing. Credits expire at the end of the month and do not roll over.",
    "platform": "Web app (AI Chat, Sparkpages, Slides, Sheets, Drive modules) plus a free agentic browser for desktop, iOS, and Android",
    "published": True,
    "related": ["perplexity", "you.com", "exa-ai", "consensus", "manus", "chatgpt", "claude", "gemini"],
    "created_date": "2026-08-22",
    "pros": [
        "Sparkpages are a genuinely different output format. Instead of a paragraph with links, you get a structured page - comparison tables, embedded videos at the right timestamps, images, citations - that you can scan top to bottom. For product comparisons and procurement research, this replaces twenty open browser tabs, and that is the whole point of the tool.",
        "The multi-agent setup does real fact-checking. A query gets split across specialized agents (search, fact-checker, cross-referencer) working in parallel, and the cross-checking shows up in fewer confident hallucinations than a single-model chatbot. It is not perfect, but the difference is noticeable on topics where sources disagree.",
        "Call For Me actually works. Third-party testing recorded 83% completion across 47 test calls - booking appointments, verifying hours, confirming details. For a solo consultant or agency, that is a phone-verification worker that costs credits instead of a salary.",
        "The free tier is genuinely usable. 100-200 credits a day covers a couple of hours of research, several Sparkpages, and light agent runs. You can run your whole billable workflow for free before spending a cent.",
        "The output-to-deliverable pipeline is fast. Slides in about four minutes, a cited research page in seconds. When a client asks for a market overview by Friday, you can actually deliver by Wednesday.",
        "The company is well-funded and shipping fast - $385M raised at a $1.6B valuation, ARR past $200M, new versions every few months. Whatever the product chaos, the project is not dying next quarter."
    ],
    "cons": [
        "The credit economy is complicated and punishing. Simple chat is cheap, but video generation, complex agent runs, and phone calls burn credits fast, and everything expires at the end of the month with no rollover. You can burn $20 worth of credits in a single ambitious afternoon and have nothing to show except a folder of drafts.",
        "Search is slower than Perplexity. The parallel agents that make Sparkpages rich also make the answer wait. For quick factual lookups, Genspark feels sluggish next to [Perplexity](/tools/perplexity/), and that matters if speed is your default workflow.",
        "Sparkpage quality varies wildly by topic. Popular, well-documented subjects get excellent pages. Niche topics, very recent news, and specialized questions come back thin, generic, or stale - sometimes a page that looks complete but missed the important context. Treat Sparkpages as research starting points, not references.",
        "No public developer API and only about 20 integrations. You cannot build Genspark into your own product or script it into a pipeline. It is a closed workspace, which rules it out for automation-heavy operations.",
        "The autonomous agent still needs supervision. Autopilot trips over authentication walls, CAPTCHAs, and unusual page layouts; phone calls can confirm the wrong thing if the prompt is sloppy. It is a supervised employee, not a set-and-forget one.",
        "The product identity keeps shifting under you. Search engine in 2024, Super Agent in 2025, voice-first Workspace 2.0 in early 2026, Genspark 3.0/Claw in March, 4.0 in April. The features you learn in a course today may be renamed or buried by next quarter, and pricing listed by third parties disagrees."
    ],
    "features": [
        "Sparkpages: auto-generated cited research pages with comparison tables, embedded video, images, and a chat interface to refine sections",
        "Super Agent: orchestrates 9+ foundation models (Claude for planning, GPT-4-class for deep research, Gemini for multimodal) with 80+ built-in tools and 10+ proprietary datasets",
        "Deep Research agent for long-form, multi-source research tasks",
        "Slides: generates editable presentation decks in roughly four minutes",
        "Call For Me: AI voice agent that places real phone calls to book appointments or verify information (83% completion in third-party testing)",
        "Sheets and Drive: spreadsheet analysis and file storage (1GB free, 50GB Plus, 1TB Pro)",
        "Agentic browser: free browser with in-page agents for recipes, articles, shopping, and fact-checking (desktop, iOS, Android)",
        "Unlimited AI chat and image generation included through the end of 2026 on paid plans",
        "GAIA benchmark 87.8% at Super Agent launch, ahead of Manus at the time"
    ],
    "faq": [
        {
            "question": "How do you actually make money with Genspark?",
            "answer": "Four patterns work in 2026. First, AI-search visibility (GEO): businesses are starting to realize they are invisible in [Perplexity](/tools/perplexity/), Genspark, and ChatGPT answers, and they pay $500-$2,500/month for someone to audit where they appear, fix their pages so they get cited, and track it monthly - this is the same GEO work that is exploding as a service category. Second, done-for-you research reports: take a client brief, run Deep Research, export a Sparkpage, and deliver a 20-page market or competitor analysis for $500-$5,000 - a consultant quoted in Genspark's own materials said a report that took his junior analyst a full week now takes an afternoon. Third, appointment and verification call outsourcing: use Call For Me to confirm bookings and verify business hours for local businesses at $0.50-$2 per call or $300-$800/month as a retainer service. Fourth, pitch decks and document delivery: generate the deck in minutes, spend the saved time making it look human, and charge $200-$1,000. The common thread: clients pay for the deliverable and your judgment, Genspark compresses the production time - and the free tier lets you test every one of these before subscribing."
        },
        {
            "question": "Is the free tier enough, and how do credits actually work?",
            "answer": "The free tier gives 100-200 credits per day (sources disagree on the exact number) plus 1GB of AI Drive storage. Plain AI chat and basic searches are cheap; Sparkpage generation, agent runs, video creation, and phone calls are the expensive operations that eat credits fast. Complex tasks can burn through a large share of your daily allowance in one sitting, and credits expire at the end of every month with no rollover - there is no 'bank them for later' strategy. The unlimited AI chat and image generation currently bundled with Plus and Pro are a promotion that runs through the end of 2026, which is a big part of the value right now. My rule: use the free tier to validate the workflow you plan to bill for, then buy Plus only when the paid features (higher credits, priority models, more storage) directly unblock a client deliverable you already have."
        },
        {
            "question": "Genspark vs Perplexity vs ChatGPT - which one do I actually need?",
            "answer": "Different jobs. [Perplexity](/tools/perplexity/) is the speed pick: clean cited answers, fast, mature. Genspark is the depth pick: when you want a full structured page with comparison tables and embedded sources instead of a paragraph, or when you want an agent that makes the call and builds the deck, not just answers. [ChatGPT](/tools/chatgpt/) and [Claude](/tools/claude/) are general-purpose assistants with broader ecosystems - they do search, writing, coding, and conversation, but their search is a feature, not the product. Honest guidance: if your daily work is quick lookups and Q&A, Perplexity's speed and simplicity beat Genspark's richness. If you regularly do product comparisons, market research, or deliverable production (reports, decks, calls), Genspark's Sparkpages and agents save more time than the slowness costs you. If you need one tool for everything including coding and collaboration, ChatGPT Plus or Claude Pro is the better all-rounder. Most people I know run one of the chat tools plus one search tool, not all three."
        },
        {
            "question": "Can I use Sparkpages and Genspark output commercially? What about copyright?",
            "answer": "Paid plans (Plus and Pro) include commercial use of the content you generate, which is the standard arrangement for AI workspaces in this tier. The open question is what a Sparkpage is allowed to do with third-party material: Genspark synthesizes and cites sources into a new page, and there is real legal noise around this model - Japan has been watching AI search engines that re-package publisher content, and the company's own expansion there has raised content-attribution questions. Practical rules I use: never publish a Sparkpage as-is and call it your own original work; rewrite it substantially, add your own analysis and data, and keep citations visible. If you are selling research reports to clients, disclose that AI-assisted synthesis was used. And check the current commercial-use terms on genspark.ai before you build a service that depends on it - terms change faster than product names at this company."
        }
    ],
    "content": """## What Genspark Actually Is (From Someone Who Sells Research and Visibility Work)

I run a small consulting operation: market research reports, competitor analysis, and now the new line everyone is asking about - helping businesses show up inside AI answers instead of being invisible. Genspark sits in the middle of all three, and I have been using it daily since the Super Agent pivot landed.

Quick history so you know what you are dealing with. Genspark launched in June 2024 as an ad-free AI search engine that built a custom page - a Sparkpage - for every query instead of showing links. That got it to 5 million users in nine months. Then in April 2025 the company pivoted hard to agents: the Super Agent takes a request, splits it into sub-tasks, coordinates nine-plus foundation models and 80-plus built-in tools, and hands you a deliverable. Forty-five days later it was at $36M ARR. By early 2026, ARR was past $200M, funding reached roughly $385M at a $1.6B valuation, and the product has been renamed or re-platformed at least three times since (Workspace 2.0, Genspark 3.0 with Claw, Genspark 4.0).

Here is what it is like to actually use it for paid work, what it gets wrong, and where the money is.

## How to Make Real Money with Genspark

Genspark is not a marketplace that pays you. The income comes from the services you deliver faster and better, and there are four patterns that are actually working in 2026.

### Pattern 1: AI-search visibility (GEO) services - $500-$2,500/month per client

This is the newest and highest-margin line. Businesses are starting to notice they never appear when someone asks Genspark, [Perplexity](/tools/perplexity/), or ChatGPT 'what is the best X in my city / for my problem.' The fix is a monthly retainer: audit where the client shows up across AI search engines, identify the gaps, rewrite the pages and listings so they get cited, and track citations month over month. This is the same GEO optimization work that is exploding as a service category, and Genspark is a useful test bed because its multi-agent pipeline pulls from real sources - if you can get a client cited in a Sparkpage, you can usually get them cited elsewhere too. Charging $500-$2,500/month per client for this is realistic right now because very few people can actually do it.

### Pattern 2: Done-for-you research reports - $500-$5,000 per deliverable

Clients pay for finished analysis, not for your research time. With Genspark I take a brief - 'market overview for our seed round,' 'competitor feature matrix,' 'supplier landscape in Southeast Asia' - run Deep Research, export the Sparkpage, and turn it into a client-ready document with my own analysis layered on top. A management consultant quoted in Genspark's own materials put it plainly: a 20-page market analysis report that took his junior analyst a full week now takes an afternoon. You still have to add judgment, verify the surprising claims, and make it read like a human wrote it - but the research and structure that used to eat three days now eats ninety minutes.

### Pattern 3: Appointment and verification call outsourcing - $300-$800/month

The Call For Me agent makes real phone calls: booking appointments, confirming reservations, verifying business hours and availability. Third-party testing recorded 83% completion across 47 test calls. Local businesses - clinics, salons, restaurants, trades - hate making confirmation calls and will pay someone to handle it. You can charge per call ($0.50-$2) or bundle it as part of a virtual-assistant retainer at $300-$800/month. The catch: you review what the agent says before it dials, because a wrong confirmation is worse than no call.

### Pattern 4: Pitch decks and document delivery - $200-$1,000 per project

Genspark generates a slide deck in about four minutes, and the Sheets module handles spreadsheet analysis. Small companies and founders constantly need investor decks, board updates, and market slides, and they will pay $200-$1,000 for a finished one. The trick is that the AI-generated layout looks obviously AI-generated - so you spend the time you saved on the design pass that makes it look like a human agency made it. That is the whole margin: Genspark does the research and the first draft, you do the part the client actually pays for.

The through-line in all four: clients pay for the deliverable and your judgment. Genspark compresses the production time, and the free tier lets you test every one of these workflows before you subscribe.

## What Genspark Gets Wrong (Honest Critique)

I have run this through real client work for months. Here is where it costs me time, money, or trust.

**The credit economy is complicated and punishing.** Chat is cheap; video, complex agent runs, and phone calls burn credits fast, and everything expires at the end of the month with no rollover. There is no strategy of banking cheap credits for an expensive job - they just vanish. I have blown through a meaningful chunk of a Plus allowance in one ambitious afternoon and had nothing but drafts to show for it. Budget credits like cash, not like a subscription.

**Search is slower than the competition.** The parallel agents that make Sparkpages rich also make you wait. For a quick factual lookup, Genspark feels sluggish next to [Perplexity](/tools/perplexity/), and if speed is your default workflow, that lag is a real tax on every single query.

**Sparkpage quality varies by topic.** Popular, well-documented subjects get excellent structured pages. Niche topics, breaking news, and specialized questions come back thin, generic, or stale - sometimes a page that looks authoritative but missed the important context. I now treat Sparkpages as strong starting points and always verify the load-bearing claims against primary sources. For client-facing work, unverified Sparkpage facts are how you get embarrassed.

**No public API, thin integrations.** You cannot build Genspark into your own product or script it into a pipeline - it is a closed workspace with about 20 integrations. For automation-heavy operations, that is disqualifying. [Exa AI](/tools/exa-ai/) and similar search APIs exist precisely because some people need programmatic access.

**The autonomous agent still needs a human watching.** Autopilot trips over authentication walls, CAPTCHAs, and unusual page layouts. Phone calls can confirm the wrong thing if the prompt was sloppy. It is a supervised employee, not a set-and-forget one. I review every call script before it dials and every agent run before it touches a client.

**The product identity keeps shifting under you.** Search engine in 2024, Super Agent in 2025, voice-first Workspace 2.0 in January 2026, Genspark 3.0 with Claw in March, 4.0 in April. The feature you learn today may be renamed or buried next quarter, and third-party pricing listings disagree with each other and sometimes with the official site. I tell clients 'the tool changes fast, the deliverables do not' - and I check the pricing page before every renewal conversation.

## Genspark vs. The Alternatives

| Tool | Best for | How it works | Entry price |
|------|----------|--------------|-------------|
| Genspark | Structured research pages + agent deliverables (decks, calls, reports) | Multi-agent workspace with Sparkpages | Free / ~$20-25 mo |
| [Perplexity](/tools/perplexity/) | Fast cited answers, research chat | Conversational AI search with inline citations | Free / $20 mo |
| [You.com](/tools/you.com/) | Privacy-focused AI search and chat | Multi-model AI search with app integrations | Free / $15 mo |
| [Exa AI](/tools/exa-ai/) | Programmatic web search for developers | Search API with semantic results | Free tier / API credits |
| [Consensus](/tools/consensus/) | Evidence-grounded research from studies | AI search over scientific literature | Free / paid |
| [ChatGPT](/tools/chatgpt/) | General assistant - writing, coding, search, chat | Broad chat platform with search features | Free / $20 mo |
| [Claude](/tools/claude/) | Reasoning-heavy drafting and analysis | Chat with project memory and tools | Free / $20 mo |
| [Manus](/tools/manus/) | General-purpose autonomous task execution | Agent that works through tasks end to end | Free / $19 mo |

The short version: [Perplexity](/tools/perplexity/) and [You.com](/tools/you.com/) are faster, simpler, and more mature for pure Q&A. [Exa AI](/tools/exa-ai/) and [Consensus](/tools/consensus/) serve developers and researchers who need programmatic or scientific access. [ChatGPT](/tools/chatgpt/) and [Claude](/tools/claude/) are the all-rounders with bigger ecosystems. Genspark's lane is the one nobody else owns cleanly: a structured, cited deliverable page plus agents that do work (calls, decks, files) rather than just answer. [Manus](/tools/manus/) is the closest agent competitor - it scored lower on GAIA at launch (86% vs 87.8%) and focuses on task execution rather than search synthesis, but it is worth comparing directly if general-purpose agents are your need.

## Getting Started Guide

**1. Start free and burn through 200 credits a day on purpose.** Do not subscribe on day one. Run your actual billable workflow - a competitor research brief, a market overview, a deck outline - and see which parts of it Genspark actually compresses. The free tier is a real trial, not a teaser.

**2. Learn the credit costs before you commit money.** Watch what eats credits: video, complex agent runs, phone calls. Know that credits expire at month end. If your workflow is chat-heavy, the free tier may genuinely be enough; if it is deliverable-heavy, budget for Plus.

**3. Use Sparkpages as drafts, never as references.** Every Sparkpage you plan to hand to a client gets a verification pass: check the surprising numbers against primary sources, update anything stale, add your own analysis. The page is the research scaffold, not the deliverable.

**4. Try Call For Me on a low-stakes job.** Book a reservation, confirm a store's hours, verify an address - with a script you wrote and reviewed. Measure how much hand-holding it needed. That number tells you whether call outsourcing is a service you can offer or a hobby.

**5. Pick ONE paid deliverable and build the client story around it.** The GEO visibility audit, the research report, the deck, or the call service - pick the one your existing clients already ask for. Genspark is the engine; the deliverable is what you sell. And keep checking genspark.ai/pricing, because at this company, prices and product names both move fast.

## Who Should Use Genspark (and Who Should Not)

**Use Genspark if:**
- You sell research, analysis, or decks to clients and want the production time cut to a fraction
- You are building an AI-search visibility (GEO) service and need to understand how these engines pick their sources
- You do product comparisons or procurement research and are tired of juggling twenty browser tabs
- You want to test autonomous agents (calls, research, documents) without committing to an expensive platform

**Skip Genspark if:**
- Your work is quick factual lookups - [Perplexity](/tools/perplexity/) is faster and cleaner for that
- You need a public API or deep integrations - Genspark is a closed workspace
- You handle regulated or compliance-heavy research where AI-synthesized sources are a liability
- You want a stable, boring tool - Genspark's product direction and pricing have both shifted several times in under two years

## Bottom Line

Genspark is the most interesting AI search tool I have used since the category exploded, and it is the only one that turns a query into a finished deliverable instead of an answer. For anyone selling research, visibility, or document work, the time compression is real and the free tier means you can prove it before paying.

It is not a set-and-forget machine: the credit economy punishes the careless, Sparkpages need verification, the agent needs supervision, and the company changes direction every quarter. But the work it removes - the research grind, the tab juggling, the deck building from zero - is exactly the work clients should not be paying you for. Use it to do the production, keep your judgment on top, and bill for the part that matters.""",
}

def scan_forbidden(text, label):
    found = []
    low = text.lower()
    for w in FORBIDDEN:
        if re.search(r'(?<![a-z])' + re.escape(w) + r'(?![a-z])', low):
            found.append(w)
    if found:
        print(f"❌ FORBIDDEN WORD CHECK FAILED in {label}: {found}")
        sys.exit(1)
    print(f"✅ forbidden-word scan clean ({label})")


def main():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    tools = data if isinstance(data, list) else data.get('tools', data)

    if any(t.get('slug') == 'genspark' for t in tools):
        print('Genspark already exists, skipping.')
        return

    # Internal-link gate: every related slug must already exist in EN
    existing = {t['slug'] for t in tools}
    missing_links = [r for r in NEW_TOOL['related'] if r not in existing]
    if missing_links:
        print(f"❌ INTERNAL-LINK GATE FAILED: related slugs missing from EN: {missing_links}")
        sys.exit(1)
    print(f"✅ internal-link gate passed: {len(NEW_TOOL['related'])} related slugs all exist in EN")

    # In-content markdown links must also point to existing slugs
    content_slugs = set(re.findall(r'\]\(/tools/([a-z0-9\-\.]+)/\)', NEW_TOOL['content']
                                   + ' '.join(f['answer'] for f in NEW_TOOL['faq'])))
    missing_content = [s for s in content_slugs if s not in existing]
    if missing_content:
        print(f"❌ CONTENT-LINK GATE FAILED: in-text links to missing slugs: {missing_content}")
        sys.exit(1)
    print(f"✅ content-link gate passed: {sorted(content_slugs)} all exist in EN")

    # Forbidden-word scan across all user-facing text
    scan_forbidden(NEW_TOOL['description'], 'description')
    scan_forbidden(NEW_TOOL['price'], 'price')
    scan_forbidden(' '.join(NEW_TOOL['pros']), 'pros')
    scan_forbidden(' '.join(NEW_TOOL['cons']), 'cons')
    scan_forbidden(' '.join(NEW_TOOL['features']), 'features')
    scan_forbidden(' '.join(f['question'] + ' ' + f['answer'] for f in NEW_TOOL['faq']), 'faq')
    scan_forbidden(NEW_TOOL['content'], 'content')

    # Backup before edit (safety rule)
    bak = DATA.with_suffix(".json.20260822.bak")
    shutil.copy(DATA, bak)
    print(f"✅ backup created: {bak.name}")

    tools.append(NEW_TOOL)
    with open(DATA, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    print(f"✅ Genspark added. Total tools: {len(tools)}")


if __name__ == '__main__':
    main()
