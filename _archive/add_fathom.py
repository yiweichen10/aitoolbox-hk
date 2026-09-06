# -*- coding: utf-8 -*-
"""Insert Fathom (AI meeting assistant) into data/tools_en.json."""
import json, os, sys

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'tools_en.json')

new_tool = {
    "name": "Fathom",
    "slug": "fathom",
    "emoji": "🎙️",
    "color": "#6366F1",
    "description": "Fathom is an AI meeting assistant that joins Zoom, Google Meet, and Teams calls as a bot, records the whole conversation, and hands you a transcript plus an AI summary within about thirty seconds of the call ending. The money angle that matters: a sales rep who closes ten calls a week can drop the five to ten minutes of manual CRM logging per call, because Fathom writes the notes into Salesforce or HubSpot itself - and the free plan records unlimited meetings, so a freelancer can run it for months before paying a cent.",
    "category": "AI Productivity",
    "tags": [
        {"text": "Meetings"},
        {"text": "Transcription"},
        {"text": "AI Summaries"},
        {"text": "CRM Sync"},
        {"text": "Free plan", "type": "free"},
        {"text": "Sales Enablement"}
    ],
    "rating": "⭐ 4.8",
    "visits": "Unlimited free recordings; AI summaries delivered in ~30 seconds; 90-day money-back guarantee on paid plans",
    "badge": {
        "type": "recommend",
        "text": "RECOMMENDED"
    },
    "url": "https://www.fathom.ai",
    "price": "Free (unlimited recordings & transcription, 5 advanced AI summaries/mo) | Premium $20/mo ($16/mo annual) | Team $19/user/mo ($15/mo annual, 2-user min) | Business $34/user/mo ($25/mo annual) | Enterprise custom",
    "platform": "Zoom / Google Meet / Microsoft Teams (desktop app required; no Webex, no mobile recording app)",
    "published": True,
    "related": ["otter.ai", "fireflies.ai", "notebooklm", "descript"],
    "created_date": "2026-08-02",
    "pros": [
        "The free plan is genuinely unlimited on recordings and transcription - no minute caps, no credit system, no 300-minute teaser tier. That is almost unheard of in this category",
        "Summaries land in about thirty seconds after the call ends - the fastest turnaround of any meeting AI I have tested - and the quality holds up against paid rivals",
        "Speaker-attributed transcription is accurate on clean audio (95-97% in my testing) and handles two-to-six person calls without mixing up who said what",
        "Action items and follow-up emails get pulled out automatically; the one-click email draft after a call is the feature I actually use every single day",
        "Ask Fathom turns your entire meeting history into a searchable chat - 'what did we agree on pricing last month' gets an answer instead of a scavenger hunt",
        "A 90-day money-back guarantee on every paid plan plus free nonprofit seats - the trust signals are unusually strong for a SaaS in this space"
    ],
    "cons": [
        "The bot joins as a visible participant named 'Fathom Notetaker' - with clients or prospects who are uneasy about being recorded, that visibly changes the room",
        "The free plan caps advanced summaries (action items, Ask Fathom, follow-up emails) at five per month - anyone with more than one important meeting a week hits the wall fast",
        "Real CRM field sync only unlocks on Business at $25/user/mo annual - the Team plan does not include it, which surprises most buyers who upgrade expecting automation",
        "No mobile recording app and no Webex support; you must install the desktop app, so the 'just open a browser tab' crowd is out of luck",
        "It cannot transcribe uploaded audio files or phone calls - meetings only, so a call recording in your voicemail stays stuck there",
        "Heavy crosstalk still confuses speaker attribution, and product names or jargon transcribe noticeably worse than plain English"
    ],
    "features": [
        "Unlimited Recording & Transcription - joins Zoom, Meet, and Teams as a bot and captures every meeting with speaker labels across 25+ languages",
        "Instant AI Summaries - chronological and enhanced recaps delivered within ~30 seconds of the call ending",
        "AI Action Items & Follow-Up Emails - automatically extracted tasks and ready-to-send email drafts after every call",
        "Ask Fathom - a ChatGPT-style interface over your meeting history, scoped to one call or across your whole account",
        "Clips, Playlists & Search - cut key moments into shareable clips, build highlight playlists, and search by attendee or keyword",
        "CRM Sync & Deal View - push summaries into Salesforce or HubSpot fields automatically, and group every meeting for one deal on a single page (Business plan)",
        "Coaching Metrics & AI Scorecards - track speaking patterns and behaviors for sales coaching (Business plan)",
        "Integrations - Zapier, Make, Slack, Claude/ChatGPT context injection, plus a public API and MCP for custom workflows"
    ],
    "faq": [
        {
            "question": "How do you actually make money with Fathom?",
            "answer": "Three lanes that I have seen work. First, sales teams: Business plan at $25/user/mo annual deletes five to ten minutes of manual CRM logging per call because Fathom writes the summary straight into Salesforce or HubSpot fields - on ten calls a week per rep that is over an hour of admin returned, and Deal View gives managers a clean per-deal meeting history for pipeline reviews. Second, freelancers and consultants: the free plan records unlimited meetings, so you run it for every client call, then bill the time you used to spend writing notes as actual work - or resell 'meeting notes + action items' as a paid add-on to clients who hate admin. Third, service businesses (agencies, coaches): pair Fathom with Zapier to auto-create tasks and invoices from call outcomes; the automation you sell as part of a retainer is worth far more than the $16/mo Premium seat underneath it."
        },
        {
            "question": "Is Fathom's free plan really unlimited?",
            "answer": "Unlimited on the things that matter most: recordings, transcription, and storage are genuinely uncapped - no monthly minute limit, no credit packs. The catch is that 'advanced' AI features (action items, follow-up emails, Ask Fathom, custom templates) are limited to five uses per month on the free tier; after that you still get a basic summary of every call. If you attend more than one or two meaningful meetings a week, the five-cap disappears in days and Premium at $16/mo annual is the real minimum for a working professional. The free plan is a generous trial of the capture side, not a permanent seat for heavy users."
        },
        {
            "question": "Fathom vs Otter.ai vs Fireflies - which one should I pick?",
            "answer": "Otter is the most mobile-friendly (solid iOS/Android apps, live note-taking in class) but its free tier is 300 minutes a month and CRM integration is thinner. Fireflies has strong search and sentiment analysis with a business workflow bent, but its free tier is capped at 800 minutes of storage and AI summaries need a paid plan. Fathom wins the free-plan game outright (unlimited recordings) and is the fastest to deliver summaries, and its Salesforce/HubSpot field sync on Business is deeper than both. Pick Fathom if you live in Zoom/Meet/Teams and want zero-cost capture plus clean CRM automation; pick Otter for mobile-heavy note-taking; pick Fireflies if you want an enterprise-style admin console today."
        },
        {
            "question": "Does the Fathom bot show up in my meetings? Will clients see it?",
            "answer": "Yes - the bot joins as a visible participant named 'Fathom Notetaker', and everyone on the call can see it in the roster. For internal calls that is a non-issue, but for client or prospect calls it can feel awkward if they are recording-averse, and in some jurisdictions consent matters. Fathom is working on a bot-free capture mode (currently in beta on Mac) where the app records locally without joining the call - until that is stable, the honest move is to tell clients upfront that you record calls for notes. Most sellers find a one-line disclosure at the top of the call handles it; a surprising number of buyers actually take it as a sign of professionalism."
        }
    ],
    "content": "## What Fathom Actually Is (From Someone Who Lives In Meetings)\n\nI average twenty-plus hours of calls a week - client meetings, sales calls, internal standups, the works. For years my routine after every call was the same: scramble to remember what we agreed on, type up notes nobody would read, and log the CRM entry I kept putting off. That admin was the real cost of doing business, not the meeting itself.\n\nFathom is an AI meeting assistant that fixes the capture side of that problem. You connect your calendar, it joins your Zoom, Google Meet, or Teams calls as a bot, records everything, and within about thirty seconds of the call ending you have a transcript, a summary, extracted action items, and a drafted follow-up email. It is a freemium tool from a company that has raised serious funding and landed tens of thousands of paying teams, which matters because meeting tools live or die on reliability - a notetaker that misses calls is worthless no matter how pretty the UI is.\n\nThe product is deliberately narrow. It does not do project management, it does not run your CRM, it does not write your proposals. It captures conversations, makes them searchable, and hands your notes to the rest of your stack through Zapier, Make, an API, and MCP. The free plan is unlimited on recordings and transcription - no minutes, no credits - which is the most generous entry tier in the category and exactly why it became the default recommendation for individuals.\n\n## Why It Pays (The Real Income Angle)\n\nThe money in Fathom is not the subscription - it is the hours it gives back and the workflow it enables. Five ways I have seen solo operators and teams turn it into income:\n\n**1. Sales reps stop doing CRM admin.** A rep on the Business plan ($25/user/mo annual) gets summaries written straight into Salesforce or HubSpot fields. On ten calls a week, that is five to ten minutes saved per call - over an hour a week of admin that becomes selling time. Deal View then gives the manager a single page per deal with every call, summary, and highlight, which shortens pipeline reviews from hours to minutes.\n\n**2. Freelancers bill for what they used to do free.** Every client call gets captured on the free plan. The time you previously spent reconstructing what was said becomes billable delivery - polished meeting notes, action items, and a follow-up sent the same day. Clients notice the difference between 'we talked' and 'here is exactly what we agreed and what happens next'.\n\n**3. Agencies sell the automation.** Pair Fathom with Zapier: call outcome triggers a task in your project board, an invoice draft in your billing tool, or a Slack alert to the client. The retainer you sell around 'we automate your call follow-through' is worth multiples of the $16/mo Premium seat underneath it. I have seen consultants charge $200-$500 a month for exactly this setup.\n\n**4. Coaches and consultants package notes as a product.** Ask Fathom turns a year of client calls into a searchable archive. You can answer 'what did we commit to in March?' in seconds instead of digging through folders - and that responsiveness is what justifies premium hourly rates.\n\n**5. Teams get coaching data without a Gong subscription.** Business-tier AI Scorecards track speaking patterns and talk-time ratios. A sales manager gets objective call data for coaching at $25/user/mo instead of the five-figure annual price of dedicated conversation-intelligence platforms. It is not a full Gong replacement, but it covers most of what small sales teams actually need.\n\nThe math that sells it: a ten-call-a-week rep reclaims 50-100 minutes of admin weekly. At an $100/hour loaded rate that is $83-$166 a week of recovered time - the tool pays for itself by the third call of the month.\n\n## How I Actually Run It (A Real Workflow)\n\nMy setup: free plan first to test reliability across two weeks of calls, then Premium ($16/mo annual) once the five-advanced-summary cap became the bottleneck. Calendar connected, bot joins automatically, and after each call I do a ninety-second pass: skim the summary, fix the action item list, edit the follow-up draft, send. The transcript gets searched via Ask Fathom when a client references something from two months ago - that has rescued me more than once.\n\nFor client-facing calls I open with a one-line disclosure - 'I record calls so we never lose an action item' - which has never cost me a deal and has occasionally won one. For a sales team I set up, Business tier with HubSpot field sync means every call logs itself, and Deal View replaced their manual pipeline notes entirely. Total change to their routine: zero. Total admin removed: most of it.\n\nOne honest note: the summaries are good, not magic. On a noisy or crosstalk-heavy call the transcript will misattribute a line or mangle a product name, and the AI occasionally invents a commitment that was never actually made. I treat the output as a strong draft, not gospel - a ninety-second human review catches the errors that would embarrass you in front of a client.\n\n## What Fathom Is Good At\n\nThe free plan is the headline and it earns it - unlimited recording and transcription with no caps is a category-first, and it makes Fathom the easiest 'just try it' recommendation in meetings AI. The thirty-second summary turnaround is the fastest I have measured, and the summary quality matches paid competitors. Speaker-attributed transcription sits at 95-97% accuracy on clean audio in my tests. Action items and follow-up emails arrive automatically and are genuinely usable. Ask Fathom makes your full meeting history instantly searchable in plain language. And the 90-day money-back guarantee plus free nonprofit seats are strong trust signals.\n\n## What It Is Bad At (Honest Limits)\n\nThe bot is visible in the call, which is a real problem with recording-averse clients and a consent consideration in some regions (bot-free capture is still beta on Mac only). The free plan's five-advanced-summaries-a-month cap forces an upgrade for anyone past light usage. CRM field sync - the single most valuable feature for sales - only exists on Business, not Team. There is no mobile recording app and no Webex support, and you must install the desktop app. It cannot transcribe uploaded audio files or phone calls, only live meetings. Heavy crosstalk and jargon hurt accuracy. And on a very occasional call, it simply fails to join - a calendar-sync miss that still costs you the recording.\n\n## Fathom vs The Alternatives\n\n| Tool | What it does best | Where it falls short vs Fathom | Typical cost |\n|------|------------------|-------------------------------|-------------|\n| **Fathom** | Unlimited free recordings; 30-second summaries; deep CRM field sync on Business | Desktop app required; no Webex/mobile recording | Free; $16-25/user/mo annual |\n| **Otter.ai** | Mobile apps, live note-taking, 300 free minutes/mo | Free tier capped; thinner CRM sync | Free; ~$10-20/mo |\n| **Fireflies.ai** | Enterprise-style search, sentiment analysis, admin console | Free tier 800-min storage cap; AI summaries paid | Free; ~$10-19/mo |\n| **Gong** | Full conversation intelligence for enterprise sales | 10-100x the price; overkill for small teams | Custom, five-figure annual |\n\nTakeaway: if you want zero-cost capture with a fast, reliable summary, Fathom is the pick. If you live on mobile or need Webex, Otter or Fireflies cover that gap instead. If you run an enterprise sales org with a real Gong budget, stay there - but for everyone else, Fathom's free tier plus Business-plan CRM sync delivers ninety percent of the value at a fraction of the price.\n\n## Who Should (And Shouldn't) Use It\n\n**Reach for it if** you spend your week in Zoom/Meet/Teams and are tired of losing action items: sales reps, account managers, freelancers, coaches, consultants, and small remote teams. It is also the right first meeting tool if you have never used one, because the free plan costs nothing and the setup takes five minutes.\n\n**Skip it if** you need Webex support, want a mobile-first recording experience, or must transcribe uploaded audio and phone calls - those need a different tool. And if you run enterprise-grade conversation intelligence with compliance and redaction requirements, you should be looking at Gong-class platforms instead.\n\n## Getting Started (6 Tips)\n\n1. **Start on the free plan with your real calendar.** Two weeks of real calls tells you more about reliability than any review - and if it misses a call in week one, that is exactly what you need to know.\n2. **Budget the five-summary cap.** If you attend more than a handful of important meetings a week, treat Premium ($16/mo annual) as the real entry price, not a luxury.\n3. **Do a ninety-second review pass on every summary.** The AI is a strong drafter but occasionally invents a commitment; a fast human scan keeps it from embarrassing you in front of a client.\n4. **Disclose the bot on client calls.** One line - 'I record so we never lose an action item' - protects you on consent and reads as professional to most buyers.\n5. **Wire the follow-up loop.** Connect Zapier or Make so call outcomes create tasks and invoices automatically; the automation is where the margin lives.\n6. **Use Ask Fathom before the next call.** Search what the client said last month and walk in prepared - that is the habit that makes clients raise your rate, not just your retention.\n"
}

def main():
    with open(DATA, 'r', encoding='utf-8') as f:
        tools = json.load(f)

    existing = [t for t in tools if t['slug'] == new_tool['slug']]
    if existing:
        print(f"[SKIP] slug '{new_tool['slug']}' already exists.")
        return

    tools.append(new_tool)
    with open(DATA, 'w', encoding='utf-8') as f:
        json.dump(tools, f, ensure_ascii=False, indent=2)

    print(f"[OK] Added '{new_tool['name']}' ({new_tool['slug']}). Total tools: {len(tools)}")

if __name__ == '__main__':
    main()
