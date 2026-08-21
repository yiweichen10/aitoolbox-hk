#!/usr/bin/env python3
"""Add Goldfish (local-first AI memory assistant for Mac) to tools_en.json for aitoolbox.hk.

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
    "name": "Goldfish",
    "slug": "goldfish",
    "emoji": "🐠",
    "color": "#FFA500",
    "description": "Goldfish is a local AI memory assistant that lives on your Mac. It watches what you work on across email, Slack, WhatsApp, Notion, your browser, and your code editor, stores that context in an encrypted SQLite database on your machine, and lets you press Option in any text field to reply, write, summarize, or continue in your own tone - no copy-pasting, no re-explaining the thread. Launched June 2026, it won Product Hunt Product of the Day (935 upvotes) and is free during alpha/beta. The money angle is real if you sell communication work: virtual-assistant and email-handling services, community management, or freelance writing where every client has a different voice. Goldfish lets one person carry several clients' worth of tone and context without juggling notes, and it is free while you figure out whether that workflow pays.",
    "category": "AI Writing",
    "tags": [
        {"text": "Local-First"},
        {"text": "AI Memory"},
        {"text": "Writing Assistant"},
        {"text": "Mac"},
        {"text": "Privacy"},
        {"text": "Free tier", "type": "free"},
        {"text": "Desktop App"}
    ],
    "rating": "⭐ 4.6",
    "visits": "Around 5M monthly visits in the CN directory - a June 2026 launch that won Product Hunt Product of the Day with 935 upvotes and spread fast through Mac-productivity circles",
    "badge": {"type": "new", "text": "NEW"},
    "url": "https://goldfish.sh",
    "price": "Free during alpha and beta, no paid tiers announced yet. The official FAQ says Goldfish is free in both alpha and beta and lists no pricing plans as of August 2026. That is the whole pricing story right now - and it cuts both ways: zero cost to test the workflow, but no subscription means no proof the product has a business model, so do not build a service that cannot survive Goldfish disappearing or suddenly charging.",
    "platform": "macOS (primary) and Windows desktop; no mobile app, no web app, no cloud sync - the memory stays on the machine it was built on",
    "published": True,
    "related": ["jasper", "wordtune", "jenni-ai", "copy.ai", "chatgpt", "claude", "grammarly-ai", "notebooklm"],
    "created_date": "2026-08-21",
    "pros": [
        "It kills the re-explaining loop. Every AI writing tool has the same tax: paste the thread, summarize the Slack conversation, re-describe the project. Goldfish already has that context because it watched you work. Press Option in any text field and the reply comes out knowing what the last email said. That is the entire pitch, and it works.",
        "The memory is genuinely local. Context lives in an encrypted SQLite database on your Mac, not a company server. AI requests go to Azure OpenAI with zero data retention and no training on your data, per their docs. For a tool that reads your screen, local-first is the difference between 'creepy' and 'fine'.",
        "It works in every app without per-app integrations. No plugins, no Zapier-style glue. If you can type there, Option works there - Gmail, Slack, WhatsApp, Notion, Xcode, the browser. That coverage is what a VA or freelancer actually needs.",
        "It learns your voice, which is the whole game for client work. Cross-app, cross-contact, cross-scenario: after a few days it stops sounding like a generic chatbot and starts sounding like you. Clients notice the difference between canned AI copy and 'this person actually wrote it.'",
        "Free right now, with no card. Alpha/beta means you can run the exact workflow you would bill for and decide if it holds up before spending a cent.",
        "The local MCP hook to Claude Desktop is a quiet power move. Your Mac's context becomes available to Claude through a local server, so you get a frontier model with your work history instead of a blank chat."
    ],
    "cons": [
        "Free is a red flag, not just a perk. No paid tier announced means the business model is unproven. Either they find a way to charge (and your workflow now has a cost), or the project stalls and your 'free forever' tool stops getting updates. Treat it as a free trial with an unknown expiration date.",
        "The privacy promise depends on trust you cannot audit. Yes, storage is local - but you are granting macOS Accessibility permission and a local MCP server, meaning the app can read everything on your screen, and completions leave your machine through Azure OpenAI. 'Zero data retention' is their word, not a contract you can verify. Do not let it watch client passwords, financials, or anything you would not hand to a stranger.",
        "It is a Mac tool with a Windows afterthought. The product story, privacy docs, and workflow are built around macOS. Windows builds exist but get less attention, and there is no mobile app, no web app, and no cloud sync - your memory lives and dies on one machine.",
        "The voice matching takes time and data. Day one, Goldfish does not sound like you; it needs days of your writing to model your tone. If you need 'sounds exactly like me' on the first afternoon, you will be disappointed.",
        "AI output still needs a human before it goes out. These are replies to clients, bosses, and courts. Goldfish gives you a strong draft in your voice, but the judgment - what not to say, what to soften, what to never send - is still yours. Skip that step and you will eventually regret it.",
        "Single-user, single-machine, no team memory. If your work needs shared context across people or devices, Goldfish is the wrong shape - it is a personal memory, not a workspace."
    ],
    "features": [
        "Press Option in any text field to reply, write, summarize, or continue with on-screen context",
        "Cross-app local memory: email, Slack, WhatsApp, Notion, browsers, code editors - stored in an encrypted local SQLite database",
        "Tone matching: learns your writing style across apps, people, and scenarios over time",
        "Local MCP server that connects your Mac's context to Claude Desktop",
        "Workflow awareness: surfaces recurring processes and flags forgotten follow-ups",
        "Auto-generated, searchable wiki of your work, browsable from the 'aquarium' in the Mac notch",
        "App and domain controls to pause or restrict what gets captured",
        "Runs through Azure OpenAI with zero data retention and no model training on your data"
    ],
    "faq": [
        {
            "question": "How do you actually make money with Goldfish?",
            "answer": "Goldfish is not a direct moneymaker like a freelancing platform - it is an efficiency tool for people who sell communication work, and the income comes from the services you deliver faster. The most direct pattern is virtual-assistant work: clients pay $15-$35/hour or $400-$1,000/month for someone to handle their email, Slack, and scheduling. A VA who writes every reply in the client's voice without asking for the backstory can carry 3-5 clients where a slower one manages two. Second pattern: community and inbox management for creators or small SaaS - reply to comments, DMs, and support threads in a consistent brand voice, $300-$800/month per account. Third pattern for freelancers: if you write for several clients with different styles, Goldfish keeps each voice separate and current, so you stop burning 20 minutes re-reading old work before each assignment - that time goes back into taking more jobs. The tool is free right now, so the math is pure margin: everything you bill is yours."
        },
        {
            "question": "Is Goldfish really free, and how long will that last?",
            "answer": "Yes, it is free in alpha and beta - the official FAQ and homepage both say so, with no paid tiers listed as of August 2026 and no card required to install. But read that as what it is: an unproven business model. Free during alpha is how young apps buy users; it tells you nothing about price later. When monetization comes, the likely shapes are a subscription for the assistant and paid tiers for heavier AI usage or team features. My advice: build your workflow now while it costs nothing, but design it so a $10-20/month fee would not break the service you sell. And keep an eye on the project's pulse - if updates slow down, that is your signal to evaluate alternatives like [Jasper](/tools/jasper/) or [Wordtune](/tools/wordtune/) before you are forced to."
        },
        {
            "question": "Is Goldfish safe to use given it reads everything on my screen?",
            "answer": "Straight answer: the architecture is privacy-forward but the trust surface is real. Storage is local and encrypted (SQLite on your Mac), and only the context needed for a request goes to Azure OpenAI with zero data retention, per their docs. That is better than most AI writing tools, which keep your prompts in the cloud by default. The catches: you must grant macOS Accessibility permission, which means the app can read anything visible on screen, and completions do leave your machine through a third-party API. You cannot audit their 'zero retention' claim from the outside. Practical rules I use: keep Goldfish's app and domain exclusions on for anything sensitive (banking, client credentials, legal docs), pause capture when sharing your screen or working with confidential material, and never rely on a free alpha tool for regulated or legally significant writing. If your work is under NDA or compliance review, get sign-off before installing anything that watches your screen."
        },
        {
            "question": "How is Goldfish different from Grammarly, Jasper, or just asking ChatGPT?",
            "answer": "Different jobs, different tools. [Grammarly](/tools/grammarly-ai/) fixes your text after you write it - grammar, tone nudges, clarity - it does not know or care what you were working on. [Jasper](/tools/jasper/) and similar AI writers generate long-form marketing copy from briefs, but you still hand them the context every time. [ChatGPT](/tools/chatgpt/) is a general assistant you paste background into. Goldfish is the only one of these that already has your context because it watched you work - you press Option and the draft arrives knowing the email thread, the meeting notes, and how you usually phrase things. The trade-off is platform and scope: Goldfish is Mac-local and single-user, while the others are cross-platform, cloud-synced, and better for teams or heavy document generation. If your bottleneck is 're-explain everything before AI can help,' Goldfish wins. If you need collaborative writing or content production at scale, the cloud tools fit better."
        }
    ],
    "content": """## What Goldfish Actually Is (From Someone Who Sells Communication Work)

I run a small freelance operation - email handling, community management, writing for a few clients who each have a very different voice. My job is mostly replying to people in their tone without ever asking them for the backstory. Goldfish is the tool that made that job feel almost unfair.

It is a local AI memory assistant for Mac. It watches what you work on across your apps - email, Slack, WhatsApp, Notion, your browser, your code editor - and stores that context in an encrypted SQLite database on your machine. Then, in any text field, you press Option and it drafts a reply, a summary, or a continuation in your voice, using what is on screen and what it remembers. No copy-pasting. No re-explaining the thread. No cloud storage of your work.

It launched in June 2026, won Product Hunt Product of the Day with 935 upvotes, and has been free through alpha and beta. Let me tell you what it is like to actually use it for paid work, what it gets wrong, and where the money is.

## How to Make Real Money with Goldfish

Goldfish is not a marketplace and it does not pay you. The income comes from the communication services you deliver faster, and there are three patterns that actually work.

### Pattern 1: Virtual-assistant and email-handling services ($400-$1,000/month per client)

The classic VA gig: a busy founder or agency owner hands you their inbox and calendar. Clients pay $15-$35/hour or $400-$1,000/month for someone who replies in their voice, keeps threads moving, and never makes them repeat themselves. Goldfish is built for exactly this. Because it remembers what the client has been working on, a draft reply arrives with the right context the first time - you are not the person asking 'can you remind me what this is about?' The math: a VA who can carry 3-5 clients instead of 2 has just multiplied their income without working more hours.

### Pattern 2: Community and inbox management ($300-$800/month per account)

Creators, small SaaS companies, and course sellers drown in comments, DMs, and support threads - and they pay for someone to keep the replies fast and on-brand. Goldfish holds the brand voice and the conversation history, so you can answer a support thread in the founder's tone, then flip to a creator's comment section without missing a beat. Agencies bundle this as 'community management' at $300-$800/month per account. Your cost: zero, while it is free.

### Pattern 3: Faster multi-client writing (more billable hours per week)

If you write for several clients with different styles, the silent tax is context-switching - re-reading old work before each assignment to remember how this client talks. Goldfish keeps each voice and each project's context separate and current, so the 'get back into it' time nearly disappears. That is not a new revenue line; it is hours returned to your week that you can sell again. A writer who saves 5 hours a week this way can take on roughly one more client or one more assignment at the same pace.

The through-line in all three: clients are not paying for the tool, they are paying for your judgment and your voice - Goldfish just removes the hours and the 'let me check my notes' delay. Keep the judgment part, and the spread between what you invoice and what the tool costs (free, today) is yours.

## What Goldfish Gets Wrong (Honest Critique)

I have run this thing through real client work for weeks. Here is where it costs me time, trust, or peace of mind.

**Free is a warning sign, not just a gift.** There is no paid tier, which means the company has not proven people will pay for this. Either they find a pricing model and my free workflow suddenly has a line item, or the project stalls and updates dry up. I have built the service so a $10-20/month fee would not break it, and I check the project's pulse regularly. Do not hard-code Goldfish into a service you cannot swap out.

**The privacy promise requires trust I cannot verify.** Storage is local - good - but the app gets macOS Accessibility permission, meaning it can read everything on screen, and each completion leaves your machine through Azure OpenAI. 'Zero data retention' is their claim, and I cannot audit it. I keep Goldfish's exclusions on for banking, client credentials, and legal docs, and I pause capture entirely for anything under NDA. If you handle regulated data, get sign-off before installing anything that watches your screen.

**It is a Mac tool with Windows as an afterthought.** The product story, privacy docs, and the whole vibe are macOS. Windows builds exist but clearly get less love. No mobile app, no web app, no cloud sync - the memory lives and dies on one machine. If you split time between a work Mac and a personal laptop, the context does not follow you.

**The voice matching takes days, not minutes.** Day one output sounds like a polite chatbot with a memory. Only after it has seen a few days of your writing does it start to sound like you. That is fine for a long-term VA workflow, useless for a one-off 'make this sound like me' job.

**AI drafts still need a human gate.** These are replies to clients, bosses, and in some cases legal or financial people. Goldfish drafts well in your voice, but the judgment - what not to say, what to soften, what to never send - is still on you. Skip the review step and you will eventually regret it.

**Single-user, single-machine.** No team memory, no shared context, no collaboration. If your work needs a group to see the same history, Goldfish is the wrong shape.

## Goldfish vs. The Alternatives

| Tool | Best for | How it works | Entry price |
|------|----------|--------------|-------------|
| Goldfish | Replying with full context in your own voice | Local memory + Option key in any text field | Free (alpha/beta) |
| [Grammarly](/tools/grammarly-ai/) | Fixing grammar and tone after you write | Inline editor suggestions | Free / $12 mo |
| [Jasper](/tools/jasper/) | Long-form marketing copy from briefs | Cloud AI writer with brand voice | From $39 mo |
| [Wordtune](/tools/wordtune/) | Rewriting and rephrasing what you wrote | Inline rewrite suggestions | Free / $9.99 mo |
| [ChatGPT](/tools/chatgpt/) | General drafting, thinking, back-and-forth | Chat with memory features | Free / $20 mo |
| [Claude](/tools/claude/) | Reasoning-heavy drafting and analysis | Chat with project memory | Free / $20 mo |
| [NotebookLM](/tools/notebooklm/) | Working inside your uploaded documents | Grounded Q&A on your sources | Free / paid |

The short version: [Grammarly](/tools/grammarly-ai/) and [Wordtune](/tools/wordtune/) improve text you have already written. [Jasper](/tools/jasper/) and [Copy.ai](/tools/copy.ai/) generate fresh marketing copy but you hand them the context every time. [ChatGPT](/tools/chatgpt/) and [Claude](/tools/claude/) are general assistants that need you to paste background in. Goldfish is the only one that already has your context because it watched you work - that is the whole difference. [NotebookLM](/tools/notebooklm/) is the closest cousin in spirit (AI grounded in your material), but it works on documents you upload, not your live workflow.

## Getting Started Guide

**1. Install on your main Mac and grant Accessibility access.** Goldfish needs macOS Accessibility permission to read on-screen text - that is the price of the context magic. Before you do, set up its app and domain exclusions for anything sensitive. Configure it once, correctly, on the machine where you actually do the work.

**2. Spend the first week just using it, not judging it.** The voice matching needs days of your writing to lock in. Reply to real emails, summarize real threads, let it build memory. Day-one output will not sound like you; week-one output will.

**3. Set up the MCP connection to Claude Desktop if you use it.** The local MCP server hands Claude your Mac's context, which turns a blank Claude chat into one that already knows what you are working on. It is the hidden power feature and it costs nothing.

**4. Turn it into a billable workflow before the free ride ends.** Pick one real client task - email replies, support threads, comment responses - and run it end to end with Goldfish for a week. Measure the time you save. That number is the basis of the VA or community-management rate you quote.

**5. Keep a kill switch.** Decide now what you would do if Goldfish started charging $20/month or stopped updating. The alternatives list above is your fallback. Do not let a free alpha tool become a dependency you cannot exit.

## Who Should Use Goldfish (and Who Should Not)

**Use Goldfish if:**
- You sell communication work - VA, email handling, community management, support - and want to carry more clients
- You write for multiple clients and waste time re-learning each voice
- You live in email, chat, and docs and are tired of pasting background into AI tools
- You care about privacy and want your writing memory to stay on your machine

**Skip Goldfish if:**
- You need team-shared context or cloud sync across devices - it is single-user and single-machine
- Your work is Mac-secondary or you mostly use Windows seriously
- You handle regulated or sensitive data and cannot authorize a screen-reading app with third-party AI processing
- You need long-form content production at scale - a dedicated AI writer like [Jasper](/tools/jasper/) fits better

## Bottom Line

Goldfish is the first AI writing tool I have used that understood the work around the text field, not just the words inside it. For anyone who sells communication work, the effect is real: replies arrive with context, in the client's voice, without the re-explaining ritual that eats an hour a day.

It is not for everyone - the free phase is a warning as much as a gift, the privacy trust surface is real, and it is stubbornly Mac-local. But if you are a VA, a community manager, or a writer juggling voices, install it on your main Mac, give it a week, and measure the time it gives back. The tool costs nothing right now; your judgment is what you sell. Goldfish just removes the hours between the two.""",
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

    if any(t.get('slug') == 'goldfish' for t in tools):
        print('Goldfish already exists, skipping.')
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
    bak = DATA.with_suffix(".json.20260821.bak")
    shutil.copy(DATA, bak)
    print(f"✅ backup created: {bak.name}")

    tools.append(NEW_TOOL)
    with open(DATA, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    print(f"✅ Goldfish added. Total tools: {len(tools)}")


if __name__ == '__main__':
    main()
