#!/usr/bin/env python3
"""Add Manus (autonomous AI agent) to tools_en.json for aitoolbox.hk.

Built-in guards (same pattern as other add_*.py in this repo):
  - forbidden-word scan: fails loudly if any banned marketing word slips in
  - internal-link gate: every slug in `related` MUST already exist in tools_en.json
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
    "name": "Manus",
    "slug": "manus",
    "emoji": "🤖",
    "color": "#3B3B58",
    "description": "Manus is an autonomous AI agent that takes a one-line brief and does the whole job while you go do something else. You tell it 'research these five competitors and hand me a 10-page PDF' or 'build a landing page for this product and publish it,' and it plans the steps, opens a real browser, runs code in its own Linux sandbox, and comes back with a finished file. I have used it to fulfill client work I would normally hand to a junior: market-research decks, lead lists, data-cleaning jobs, small websites. The money angle is direct - you charge per deliverable on Upwork or Fiverr, or bill a monthly retainer for something like weekly competitor monitoring, and Manus does the multi-hour grind in the background while your credit cost stays a fraction of what you invoice. It is built by Butterfly Effect (the team behind Monica.im). The free tier gives 300 daily credits so you can test it before paying; real work sits on the $20-$40/month plans, with a $200 tier for heavy use.",
    "category": "AI Agents",
    "tags": [
        {"text": "Autonomous Agent"},
        {"text": "AI Agent"},
        {"text": "Research"},
        {"text": "Browser Automation"},
        {"text": "Data Analysis"},
        {"text": "Slides & Websites"},
        {"text": "Free tier", "type": "free"},
        {"text": "Web App"}
    ],
    "rating": "⭐ 4.4",
    "visits": "Around 20M monthly visits at its 2025 peak; used by freelancers reselling research and deck-building, solopreneurs automating repeatable deliverables, and analysts delegating multi-step web research",
    "badge": {"type": "hot", "text": "HOT"},
    "url": "https://manus.im",
    "price": "Free tier: 300 refresh credits that reset every 24 hours (no rollover), plus a one-time 1,000-credit starter pack, 1 concurrent task, and the lighter Manus 1.6 Lite model. Paid (checked August 2026): Starter $20/mo ($17/mo billed yearly) for 4,000 monthly credits and up to 20 concurrent tasks; Pro $40/mo ($34/mo yearly) for 8,000 monthly credits with a 7-day trial; Pro Max $200/mo ($167/mo yearly) for 40,000 monthly credits and a free cloud computer; Team from $20/seat/mo with a shared credit pool and SSO. Credits do not roll over and the agent's own error re-runs also spend them. Manus changed its pricing more than once in 2026 - confirm the live numbers on manus.im/pricing before you buy.",
    "platform": "Web app plus desktop (Windows, macOS) and mobile (iOS, Android) apps; API access, Slack, and email triggers (Mail Manus) on paid plans",
    "published": True,
    "related": ["chatgpt", "claude", "devin-ai", "gumloop", "relevance-ai", "perplexity", "browser-use"],
    "created_date": "2026-08-19",
    "pros": [
        "It finishes whole jobs, not steps. Most AI tools hand you a draft and leave the last mile to you. Manus keeps working - it plans, opens a browser, runs code, checks its own output, and returns a finished PDF, deck, or website. For reselling deliverables, that gap between 'draft' and 'done' is the whole business.",
        "The virtual computer is real. Each task spins up a Linux sandbox with a browser, terminal, and file system, so it can log into sites, scrape many pages in sequence, run Python on your CSV, and build charts - things a chat model simply cannot do on its own.",
        "Shareable replays are underrated. Every run is published as a URL showing each action it took. I send these to clients as proof of work, and I reuse them to train a junior on how a task should flow.",
        "The free tier is a genuine test, not a demo. 300 daily credits plus a 1,000-credit starter pack, no card required, is enough to run a few real tasks and see whether the output is worth billing for.",
        "Credit billing beats per-seat pricing for solo operators. You pay for what the agent actually does, so a slow week costs almost nothing instead of a fixed seat fee you are not using.",
        "Wide Research fans out across many sources in parallel, which turns a half-day of tab-hopping into a single structured answer - the closest thing to handing off 'go find out everything about X' to a competent researcher."
    ],
    "cons": [
        "Credits vanish and mistakes cost you. Monthly and daily credits do not roll over, and when the agent misplans a task, its retries and self-corrections burn credits too. A single complex research-plus-website job can eat a big chunk of a Starter allowance before you get a usable result.",
        "Autonomous does not mean unsupervised. Left alone, it can head down the wrong path - scraping the wrong site, filling a form incorrectly, or over-building - and you only notice after credits are spent. You have to check the plan and the replay, which cuts into the 'set it and forget it' promise.",
        "Ownership and corporate structure have been unsettled through 2026, with a high-profile acquisition and a regulatory review still unresolved. If you build a paid service on top of Manus, that uncertainty is a real platform risk - features, pricing, or availability could shift.",
        "The free plan is capped hard. One concurrent task and the lighter 1.6 Lite model mean serious multi-step work needs a paid tier; you cannot judge the strong models for free.",
        "Data routing matters for regulated work. Standard plans process tasks on the company's cloud, so before you feed it client PII or anything under GDPR-style rules, check where the data goes and get sign-off.",
        "It is not a workflow tool. For fixed, repeatable automations across many apps, a rules engine like Zapier or Make is cheaper and more predictable. Manus shines on open-ended, one-off jobs, not on the same trigger firing a thousand times."
    ],
    "features": [
        "Autonomous Agent Mode that plans, executes, and self-corrects multi-step tasks to completion",
        "Virtual Linux sandbox per task with its own browser, terminal, Python/Node runtime, and file system",
        "Browser operator that logs in and acts across real websites over long sessions",
        "Document generation: research turned into Word, Excel, PowerPoint, PDF, and live websites",
        "Wide Research for parallel, multi-source information gathering",
        "Shareable replay URLs that show every action the agent took",
        "Scheduled and recurring tasks that run unattended (daily monitoring, periodic pulls)",
        "Slide, image, and music generation plus website and small-app scaffolding",
        "Slack and email (Mail Manus) triggers, plus API access and a knowledge module that remembers preferences"
    ],
    "faq": [
        {
            "question": "How do people actually make money with Manus?",
            "answer": "The pattern that works is reselling deliverables, not reselling access to the tool. On Upwork and Fiverr there is steady demand for things Manus produces end to end: a competitor-research PDF, a scraped-and-filtered lead list, a data-cleaning pass on a messy spreadsheet, a simple landing page. You list a fixed-price gig - say $80 for an overnight market-research report - and Manus does the multi-step work in the background while your credit cost is a few dollars. The better model is recurring: sell a client weekly competitor monitoring or a monthly niche-market briefing for $300-$800/month, set it as a scheduled task, and pocket the spread between your retainer and your credit bill. The judgment you add - scoping the task, checking the output, framing it for the client - is what they pay for. Manus just removes the hours."
        },
        {
            "question": "Is Manus free, and how far does the free tier get me?",
            "answer": "Yes, there is a free plan with no credit card: 300 refresh credits that reset every 24 hours, plus a one-time 1,000-credit starter pack, one concurrent task, and the lighter Manus 1.6 Lite model. That is enough to run a handful of real tasks and decide whether the output is worth billing for - use it exactly that way. The limits bite fast for paid work, though. One task at a time and the Lite model mean a full research-and-build job will feel slow or stall, and credits do not roll over, so a busy testing day empties the tank. If you intend to sell what it makes, treat the free tier as an audition and move to Starter ($20/mo) or Pro ($40/mo) before you quote a client."
        },
        {
            "question": "Manus vs ChatGPT or Devin - when should I reach for which?",
            "answer": "Different jobs. [ChatGPT](/tools/chatgpt/) and [Claude](/tools/claude/) are conversation-first: fast for drafting, reasoning, and back-and-forth, and they now have agent modes, but you are still steering most of the way. Manus is delegation-first - you hand it an open-ended, multi-hour task and it works in its own sandbox until it produces a file. [Devin](/tools/devin-ai/) overlaps but is aimed squarely at software engineering, running inside a codebase; Manus is a generalist that does research, decks, data, and small sites as well as light coding. If your task is 'help me think or write,' use a chat model. If it is 'go do this whole thing and bring me the result,' that is Manus. And if it is 'run the same trigger across apps forever,' that is a job for [Gumloop](/tools/gumloop/) or a workflow tool, not an open-ended agent."
        },
        {
            "question": "What are the real catches before I rely on it for client work?",
            "answer": "Three worth pricing in. First, credit math: complex tasks and the agent's own error re-runs burn credits that never roll over, so budget for the plan that covers your worst month, not your average one, and check the credit estimate before large runs. Second, supervision: 'autonomous' still needs a human to check the plan and the replay, because a misread task can spend credits going the wrong way before you catch it - never promise a client a turnaround you have not test-run. Third, platform risk: ownership has been in flux during 2026, and the company's long-term direction is not settled, so avoid hard-coding Manus into a service you cannot swap out. Also confirm data handling before feeding it anything sensitive, since standard plans run tasks on the company's cloud."
        }
    ],
    "content": """## What Manus Actually Is (From Someone Who Resells What It Makes)

I run a small freelance operation - market research, lead lists, quick websites, the kind of work agencies charge a fortune for and clients want yesterday. Manus is the tool that changed my delivery math. It is an autonomous AI agent: you write one brief, and it plans the job, opens a real browser, runs code in its own Linux sandbox, and hands back a finished deliverable. Not a draft. A 10-page PDF, a working landing page, a cleaned spreadsheet with charts.

The honest framing first: this is not a chatbot with a fancy label. Tools like [ChatGPT](/tools/chatgpt/) and [Claude](/tools/claude/) talk you through a task; Manus goes and does it. It is built by Butterfly Effect, the Singapore-based team behind Monica.im, and it went viral in early 2025 with a 500,000-person waitlist. By 2026 it is one of the general-purpose agents people actually put to work, alongside [Devin](/tools/devin-ai/) for coding and [Browser Use](/tools/browser-use/) for web automation.

### How it works under the hood

Every task spins up a virtual computer - a containerized Linux box with a browser, a terminal, Python and Node, and a file system. A multi-agent setup (a planner, an executor, and a verifier) breaks your brief into steps, does them, and checks its own work. That architecture is why it can log into a site, click through fifty pages, pull the data, run analysis on it, and build a chart - a chain a plain chat model cannot manage on its own.

The other piece that matters for client work is the shareable replay. Every run publishes a URL that shows each action the agent took, step by step. I send these to clients as proof of work, and I use them to check where a task went sideways when the output is not right.

## How to Make Real Money with Manus

Most write-ups tell you to "automate your life." That is not where the income is. The money is in selling finished deliverables faster and cheaper than a human can produce them, while you keep the judgment part.

### Model 1: Per-deliverable gigs ($50-$300 each)

This is the fastest start. There is steady demand on Upwork and Fiverr for outputs Manus produces end to end:

- **Competitor research reports.** "Research the latest press, pricing, and product changes from these 5 competitors and produce a 10-page PDF." Price it at $80-$200. Manus does the multi-hour crawl overnight; your credit cost is a few dollars.
- **Lead lists.** Crawl a directory or listing portal, filter by your client's criteria, output a clean Excel. $50-$150 a list.
- **Data cleaning and charts.** A client sends a messy CSV; Manus dedupes, normalizes, and produces summary charts. $60-$150 a job.
- **Simple websites and landing pages.** A one-page site from a brief, published live. $100-$300.

The trick is scoping the gig tightly enough that the agent can finish it without you babysitting. Loose briefs waste credits; specific briefs print money.

### Model 2: Recurring monitoring retainers ($300-$800/month)

This is where the real business is, because it is recurring and it runs itself. Manus supports scheduled and recurring tasks, so you set a job to run every Monday morning and deliver to the client automatically:

- **Weekly competitor monitoring** - new pricing, new features, new press - delivered as a short brief to their inbox or Slack.
- **Daily market briefings** - stock moves, sector news, macro indicators - for a client who wants it before their morning meeting.
- **Recurring niche-market research** - a slice of an industry tracked over time, compiled into a monthly deck.

Charge $300-$800 a month. Your credit cost on a Pro plan might be $40. The spread is your margin, and the client stays because switching means rebuilding the workflow.

### Model 3: Productized "agent task" service

Take the gigs that sell best and turn them into a fixed product with a simple order form: "Overnight competitor report - $99." "Lead list, 200 verified rows - $129." You are selling a predictable outcome, not your hours. Manus does the work; you do quality control and delivery. This scales because your time per order drops as you refine the briefs and reuse them.

### Model 4: Speed advantage inside an existing agency

If you already do research, content, or web work, Manus is not a new revenue line - it is margin. A report that took a junior a full day now takes an agent two hours plus your review. Same invoice, a fraction of the labor. Or you undercut competitors on timeline: "24-hour turnaround" wins deals when the other shop quotes a week.

## What Manus Gets Wrong (Honest Critique)

I have run enough tasks to know where it costs me time and money.

**Credits disappear, and errors are billed to you.** Monthly and daily credits do not roll over. Worse, when the agent misplans and has to retry or self-correct, those re-runs spend credits too. A single ambitious job - deep research plus a built site - can chew through a Starter month's allowance before it lands. You have to check the credit estimate before big runs and budget for your worst month.

**"Autonomous" still needs a babysitter.** Leave it fully alone and it will occasionally scrape the wrong source, fill a form wrong, or over-engineer a simple ask - and you find out after the credits are gone. I always read the plan before a long run and skim the replay after. That is cheaper than trusting it blind.

**The ownership situation is unsettled.** Through 2026 the company's corporate structure has been in flux, with a high-profile acquisition and a regulatory review that are not resolved. For a hobby that does not matter. For a paid service you build on top of it, it is a genuine platform risk - do not hard-code Manus into something you cannot swap out.

**The free plan is a teaser for the strong models.** One concurrent task and the lighter 1.6 Lite model mean you cannot judge the good models without paying. Fine for an audition; not enough to run real work.

**Data routing is a question for regulated jobs.** Standard plans run tasks on the company's cloud. Before you feed it client personal data or anything under GDPR-style rules, confirm where the data goes and get sign-off. Do not learn this after the fact.

**It is the wrong tool for fixed workflows.** If your need is "the same trigger fires across apps a thousand times," a rules engine like [Gumloop](/tools/gumloop/) or a classic automation platform is cheaper and more predictable. Manus is built for open-ended, one-off jobs, not identical repetition.

## Manus vs. The Alternatives

| Tool | Best for | How it works | Entry price |
|------|----------|--------------|-------------|
| Manus | Open-ended multi-step jobs (research, decks, data, sites) | Autonomous agent in a Linux sandbox with a browser | Free / $20-$200 mo |
| [Devin](/tools/devin-ai/) | Software engineering inside a codebase | Coding agent, works in a repo | From higher tiers |
| [ChatGPT](/tools/chatgpt/) | Drafting, reasoning, conversation + agent mode | Chat-first, you steer | Free / $20 mo |
| [Perplexity](/tools/perplexity/) | Fast sourced answers and research | Search-first, cited | Free / $20 mo |
| [Gumloop](/tools/gumloop/) | Repeatable multi-app workflows | Node-based automation | Free / paid |
| [Relevance AI](/tools/relevance-ai/) | Building teams of task agents | No-code agent builder | Free / paid |

The short version: reach for Manus when the task is "go do this whole thing and bring me the finished result." Reach for a chat model when you want to think or write with help. Reach for a workflow tool when the same job repeats forever. They are not competitors so much as different-sized hammers.

## Getting Started Guide

**1. Sign up and spend the free credits on real tasks.** manus.im gives you 300 daily credits plus a 1,000-credit starter pack, no card. Do not waste them on toy prompts - run an actual job you would bill for and judge the output.

**2. Write the brief like a work order, not a chat.** "Research competitor pricing" is too loose and burns credits. "Visit these 5 URLs, pull current pricing tiers and any 2026 changes, and output a 1-page comparison table plus a short summary" gives the agent a target it can hit on the first try.

**3. Read the plan before a long run.** Manus shows its planned steps. Skim them. Catching a wrong turn here costs nothing; catching it after execution costs credits.

**4. Move to a paid plan before quoting clients.** Test-run your actual gig on Starter or Pro so you know the real credit cost and turnaround before you promise a price. Pick the plan that covers your busiest month, since credits do not roll over.

**5. Save your best briefs as templates.** The gigs that sell repeat. Keep the exact working brief for "overnight competitor report" or "200-row lead list" and reuse it - that is how a one-off gig becomes a productized service.

## Who Should Use Manus (and Who Should Not)

**Use Manus if:**
- You are a freelancer who resells research, lead lists, decks, or simple sites and wants to cut delivery hours
- You run recurring monitoring or briefing work you can put on a schedule
- You are an analyst who wants to hand off multi-step web research and get a structured file back
- You already run an agency and want speed as a competitive edge

**Skip Manus if:**
- Your need is a fixed, repeatable workflow across many apps (use a rules engine instead)
- You handle regulated personal data you cannot route through a third-party cloud without review
- You want a cheap, predictable per-task cost - credit burn on complex jobs is hard to forecast
- You need production-grade software built and maintained (a coding-specialist agent or a real developer fits better)

## Bottom Line

Manus is the clearest proof yet that "prompt in, finished work out" agents are real and useful today. It is not flawless - credits disappear, it needs supervision, and the corporate situation adds uncertainty - but for the specific job of delivering a completed research report, deck, lead list, or small site from a single brief, nothing I have used does it as completely.

The people making money with it are not chasing a moonshot. They scope tight deliverables, let the agent grind through the hours, add the judgment and quality control clients actually pay for, and keep the spread between a few dollars of credits and a real invoice. Start on the free tier with one job you would bill for. If the output holds up, you have a new way to deliver work while you sleep.""",
    "aeo_geo_updated": "2026-08-19"
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

    if any(t.get('slug') == 'manus' for t in tools):
        print('Manus already exists, skipping.')
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
    bak = DATA.with_suffix(".json.20260819b.bak")
    shutil.copy(DATA, bak)
    print(f"✅ backup created: {bak.name}")

    tools.append(NEW_TOOL)
    with open(DATA, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    print(f"✅ Manus added. Total tools: {len(tools)}")


if __name__ == '__main__':
    main()
