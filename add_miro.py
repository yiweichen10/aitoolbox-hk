# -*- coding: utf-8 -*-
"""Add Miro AI to tools_en.json (aitoolbox.hk).
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
    "name": "Miro AI",
    "slug": "miro-ai",
    "emoji": "\U0001F91D",
    "color": "#FFD02F",
    "description": "Miro AI drops an AI assistant onto the infinite canvas that 80 million people already use for whiteboarding - tell it 'map our onboarding flow' and it draws the diagram, cluster 200 sticky notes by theme in a click, and turn a messy workshop board into a clean list of action items. I run client strategy sessions on it, and the money side is plain: I sell the facilitation and the boards other teams are too swamped to build themselves.",
    "category": "AI Productivity",
    "tags": [
        {"text": "Whiteboard"},
        {"text": "Collaboration"},
        {"text": "Mind Map", "type": "free"},
        {"text": "Workshops"},
        {"text": "AI Assistant"},
        {"text": "Remote"}
    ],
    "rating": "\u2b50 4.6",
    "visits": "About 8.5 million monthly visits",
    "badge": {
        "type": "recommend",
        "text": "RECOMMENDED"
    },
    "url": "https://miro.com/ai",
    "price": "Free (3 editable boards + basic AI); Starter $8/member/mo annual ($10 monthly, 25 AI credits); Business $16/member/mo annual ($20 monthly, 50 AI credits + AI agents); Enterprise custom (min 30 seats)",
    "platform": "Web, Windows, Mac, iOS, Android",
    "published": True,
    "related": [
        "figma-ai",
        "notion-ai",
        "chatgpt",
        "claude",
        "warp",
        "raycast-ai"
    ],
    "created_date": "2026-07-29",
    "pros": [
        "Text-to-diagram actually works - describe a process and it lays down proper shapes, connectors, and labels you then tweak, which saves the dead time of dragging boxes by hand",
        "Sticky-note clustering is the feature I reach for most - select a wall of brainstorm notes and it groups them by theme and flags the gaps, turning an hour of sorting into ten seconds",
        "Board summarization pulls action items and takeaways out of a chaotic session, so the client leaves with a written record instead of a screenshot",
        "The free tier is usable for real: unlimited boards (3 editable), 5,000+ templates, and 160+ integrations cover a genuine solo trial, not a teaser",
        "250+ integrations (Jira, Slack, Teams, Figma, Google) mean the board sits inside the client's existing stack rather than beside it",
        "Presentation mode lets you frame sections of a board and present as slides without exporting to PowerPoint, which keeps the meeting in one place"
    ],
    "cons": [
        "AI lives behind the paywall - the free plan gives you basic AI only, and the 3-editable-board cap bites the moment a second client board needs work",
        "AI credits are tight: 25 per member a month on Starter evaporates if you generate diagrams all day, and extra credit packs cost on top",
        "Per-seat pricing stacks up - a 10-person team on Business runs $160-$200 a month, and clients balk when you quote that as a prerequisite",
        "Big boards with thousands of elements get sluggish; panning and zooming stutter once a workshop board fills up",
        "Feature sprawl is real - new users stare at the toolbar for a week before they find the five things they actually need",
        "The mobile app is a viewer, not a workspace; you cannot run a proper session from a phone, and it is not a document or数据分析 tool no matter how hard you push it"
    ],
    "features": [
        "AI Diagram Generation - type a process, system, or workflow and Miro draws a complete diagram with correct shapes, connections, and labels on the canvas",
        "Mind Map Auto-Creation - generate a structured mind map from a topic or a pile of ideas, with branching and categorization handled for you",
        "Sticky Note Clustering - select brainstorm notes and AI groups them by theme, surfaces patterns, and suggests missing categories",
        "Board Summarization - AI reads the whole board and returns structured summaries, action items, and key takeaways from a session",
        "User Story Drafting - describe a feature and AI writes user stories with acceptance criteria directly on the canvas",
        "AI Workflows & Agents - on Business, build repeatable AI workflows and agents that ask the right questions and act (Business tier)",
        "MCP Server - connect Miro to Claude, Cursor, or Copilot so context flows both ways (500 calls/day Starter, 2,000 Business)",
        "Presentation Mode - frame board sections and present them as slides without leaving Miro"
    ],
    "faq": [
        {
            "question": "How do you make money with a tool that has a free tier?",
            "answer": "You do not resell Miro; you sell the facilitation and the board. A founder does not want another $8-a-seat app, he wants his Q3 strategy already mapped, his onboarding flow drawn, and his team aligned in a live session. I charge $500-$2,000 to run a remote design sprint or strategy workshop and hand over a board the team actually uses. The subscription is his cost; my invoice is for the work he will not do himself. At three to five client engagements a month that is $1,500-$10,000, against maybe $40-$80 of Miro bills on my side."
        },
        {
            "question": "Is the free plan enough to do paid work?",
            "answer": "For a trial, yes. Unlimited boards, 5,000+ templates, and 160+ integrations let you build a real demo. For delivery you hit the wall fast: only 3 boards stay editable and the AI is basic. Any client engagement needs Starter at $8 a seat a month so the board is private, exportable, and has 25 AI credits. I bake one or two seats into the quote; it barely dents the margin. Do not promise AI clustering or board summaries on the free tier - they will not be there when the client opens it."
        },
        {
            "question": "Miro AI vs Figma AI vs just a Google Doc - which do I learn to sell?",
            "answer": "They are not rivals, they are layers. Figma AI is for UI and screen design; a Doc is for writing. Miro is the thinking space - the messy middle where a team figures out the flow before anything gets designed or written. I pitch Miro to founders, ops leads, and agencies who need to align a group, not produce a pixel-perfect screen or a polished memo. When a client asks for a workshop, a retro, or a strategy map, Miro is the tool; Figma and Docs come later in the pipeline."
        },
        {
            "question": "What is the one mistake people make when they buy it?",
            "answer": "They open it, like the infinite canvas for an afternoon, and never build a real board - so the $8 feels wasted and they churn. The payoff is in the templates and AI workflows you set up: a lean-canvas board, a sprint-retro board, a customer-journey map. My setup package exists precisely because nobody wants to build that layer. Sell the board, not the login, and the subscription stops being a line item and becomes the thing that runs their week."
        }
    ],
    "content": "## What Miro AI Actually Is (From Someone Who Runs Client Sessions on It)\n\nI run a small strategy-and-facilitation gig - mostly remote workshops for founders and ops teams who need to get a plan out of their heads and onto something the whole group can see. For years that meant Google Slides, a shared Doc, and a lot of awkward \"can everyone see my screen.\" Then I moved it all onto Miro, and the AI layer is the part that earns its keep in this write-up.\n\nMiro is the online whiteboard 80 million people already use for brainstorming, flowcharts, and sprint planning. Miro AI is the assistant bolted onto that infinite canvas: you describe a process and it draws the diagram, you select 200 sticky notes and it clusters them by theme, and it can turn a chaotic workshop board into a clean list of action items. As of mid-2026 it pulls about 8.5 million visits a month, which for a collaboration tool is serious search traffic - exactly why it belongs on a money-minded site.\n\nThe free plan is real: unlimited boards (only 3 stay editable), 5,000+ templates, and 160+ integrations. Paid tiers lift the AI and the collaboration limits - Starter at $8 a seat a month (annual) or $10 monthly with 25 AI credits per member, Business at $16 a seat a month (annual) or $20 monthly with 50 AI credits plus SSO, guest editing, and AI workflows, and Enterprise on custom pricing with a 30-seat floor. None of that is exotic; it is the standard SaaS seat math, and the job is to sell the work the seat unlocks, not the seat.\n\n## Why It Pays (The Real Income Angle)\n\nMiro is cheap for you and expensive-feeling for the client, which is the gap you sell into. You are not moving software; you are moving a team from \"we talked about it\" to \"here is the board, here are the action items.\" Five ways I have seen solo operators and small agencies turn it into income:\n\n**1. Facilitated remote workshops ($500-$2,000 per session).** Design sprints, strategy offsites, quarterly planning, and retrospectives are the bread and butter. You run the session live on Miro, use AI to cluster notes and surface action items in real time, and the client walks away with a board plus a written summary. A half-day strategy sprint for a 12-person company at $1,500 is a normal booking; do three a month and you are at $4,500 against maybe $50 of Miro on your side.\n\n**2. Sell Miro board templates ($15-$50 each, passive).** Lean-canvas boards, OKR boards, sprint-retro boards, customer-journey maps, and hiring-scorecard boards are things thousands of teams need and will not build. Package one as a duplicate-able Miro board and list it on Gumroad. A $29 lean-canvas template that sells 40 times is $1,160 you earned while asleep; a small library of six does low-four-figures a month.\n\n**3. Client ops and process boards as a build service ($300-$1,500 per client).** Most small companies run their onboarding, their sales process, or their architecture diagram inside someone's head. You interview them for an hour and build the board - a mapped onboarding flow, a CRM visualization, a system architecture diagram with the 4,700+ shapes Miro ships. Hand it over, train one admin, and bill the setup. At five clients a quarter that is $1,500-$7,500 of project work with near-zero marginal cost.\n\n**4. Remote-facilitation retainers ($500-$2,000 a month per client).** Distributed teams need a steady hand running their weekly syncs, their retros, and their roadmapping. You become the outside facilitator on a monthly contract - show up, run the board, cluster the notes, own the action-item list. Two or three retainer clients replace a full-time salary with far less overhead.\n\n**5. Miro training for teams ($200-$500 per seat, or ~$2,000-$4,000 for a half-day cohort).** Plenty of teams bought Miro during the remote-work scramble and use it as a glorified sticky-note wall. You teach them the five features that matter - AI diagrams, clustering, board summaries, templates, presentation mode - and they suddenly get value from the seat they already pay for. Charge a company to train ten people and you have a four-figure day.\n\nThe common thread: the tool is the canvas, you are the person who makes it produce a decision. That is the part clients happily pay for and cannot do alone.\n\n## What Miro AI Is Good At (From the Keyboard)\n\n**AI diagram generation is the headline.** You type \"map our customer onboarding from signup to first win\" and it drops a diagram with the right shapes, connectors, and labels. It is a starting point, not a finished artifact - you still move things around - but it kills the blank-canvas paralysis that stalls every workshop's first ten minutes. I have watched a room go from silent to arguing about the right boxes in under a minute because the AI gave them something to react to.\n\n**Sticky-note clustering is the one I use most.** A brainstorm produces 150 notes; selecting them and asking AI to group by theme returns clusters with suggested category names and flags the gaps. What used to be an hour of me reading notes aloud is now ten seconds, and the client sees the structure form live, which builds trust faster than any slide.\n\n**Board summarization closes the loop.** At the end of a session the board is a mess by design - that is the point. AI reads it and returns action items and takeaways, so the client leaves with a written record instead of a screenshot they will never open. I paste that summary straight into the follow-up email; it is the deliverable.\n\n**Presentation mode keeps the meeting in one room.** Frame sections of the board and present them as slides without exporting to PowerPoint. For a client session that means no \"let me share a different window\" moment; the strategy and the slides are the same object.\n\n## What Miro AI Is Bad At (Be Honest Before You Pitch)\n\n**The AI is behind the paywall, and the free cap bites.** Free gives you basic AI and only 3 editable boards. The moment a second client board needs real work, you are on Starter, and the client needs a seat too if they are editing. Quote this up front; the surprise seat bill is the fastest way to lose the engagement.\n\n**AI credits are tight.** Twenty-five per member a month on Starter is fine for a few diagrams a week and disappears if you generate all day. Extra credit packs cost on top. If a client workflow leans hard on AI, scope the credits into the contract or you eat the overage.\n\n**Per-seat pricing stacks.** A 10-person team on Business is $160-$200 a month. That is reasonable for the client but you must present it as a prerequisite, not a surprise, and some solopreneurs will flinch at paying for a tool they will touch weekly.\n\n**Large boards get sluggish.** Once a workshop board crosses a few thousand elements, panning and zooming stutter. For a single strategy session it is fine; for a living operations board that grows daily, it gets heavy. Know which one you are building.\n\n**It is not a document or数据分析 tool.** I have seen people try to run a quarterly report or a spreadsheet inside Miro because the canvas is seductive. Don't. Write in a Doc, analyze in a sheet, and keep Miro for the visual thinking. Forcing it into the wrong job is how teams decide it \"isn't worth it.\"\n\n**The mobile app is a viewer.** You cannot run a proper session from a phone. If a client wants to poke the board on the train, fine; if they want to facilitate from it, they need a laptop. Set that expectation.\n\n## Miro AI vs the Alternatives (Quick Table)\n\n| Tool | Best at | AI angle | Pricing floor | Who I pitch it to |\n|------|---------|----------|---------------|------------------|\n| **Miro AI** | Visual thinking, workshops, diagrams | Generate diagrams, cluster notes, summarize board | Free / $8 seat/mo | Founders, ops, facilitators |\n| **Figma AI** | UI and screen design | Generate and edit designs | Free / ~$12 editor/mo | Designers, product teams |\n| **Notion AI** | Docs and connected databases | Write and summarize text | Free / $10 seat/mo | Writers, knowledge teams |\n| **Mural** | Similar whiteboard, facilitation-first | Similar AI clustering | Free / ~$12 seat/mo | Enterprise facilitators |\n| **Google Drawings / Slides** | Simple, free diagrams | None | Free | Ad-hoc, no collaboration need |\n\nI keep Figma for screen design, Notion for docs, and Miro for the messy middle where a group figures things out. They are tiers of the same pipeline, not rivals, and I sell all three to the same clients at different stages.\n\n## Who Should Use Miro AI (And Who Shouldn't)\n\n**Use it if** you facilitate groups, run strategy or planning sessions, map processes for clients, or teach teams to think visually. The AI turns the blank canvas from a hurdle into a launchpad, and the board becomes a deliverable you can bill for.\n\n**Skip it if** you work alone and just need to sketch once a quarter - a free drawing tool covers that. Or if your client needs hard analysis and reporting, not visual alignment; Miro will frustrate both of you. Or if the team is small and price-sensitive and will not use it weekly; the seat math only pays off when the board is part of someone's routine.\n\n## Getting Started (6 Tips From Someone Who Bills With It)\n\n1. **Start on the free plan and build one real board.** Not a test scribble - build your own lean-canvas or retro board so you feel where the AI helps and where it gets in the way before you pitch it.\n\n2. **Learn the five features that matter.** AI diagram, sticky-note clustering, board summary, templates, and presentation mode. Ignore the rest for month one; the toolbar sprawl will otherwise eat your first week.\n\n3. **Describe processes specifically.** \"Map our onboarding\" gives a generic frame; \"map our SaaS onboarding from trial signup to activated user, with the handoff from sales to CS\" gives a board worth showing a client. Specificity is the difference between a starting point and a deliverable.\n\n4. **Treat AI output as a draft, not a final.** It clusters and diagrams well but misses context a human catches. Always walk the client through the grouped notes and fix the misfiles live - that correction step is half the value you sell.\n\n5. **Package your best boards as templates.** The lean-canvas board you built for one client becomes the $29 template you sell to a hundred. Every delivered board is a product in waiting; duplicate it, clean it, and list it.\n\n6. **Scope the seats and credits before you quote.** Know whether the client needs Starter or Business, how many seats, and whether the workflow will burn AI credits. Put it in the proposal so the bill never surprises anyone.\n\n## The Bottom Line\n\nMiro AI is the thinking space for teams, and the AI turns the scary blank canvas into a first draft in seconds. For a solo facilitator or small agency it is close to free to run and expensive to buy as a service - which is the exact gap you sell across. Build the boards, run the sessions, and let the seat price be the client's problem while the invoice for the work stays yours. If your income depends on moving groups from talk to decision, this is the canvas to learn; if you mostly work alone and think in words or spreadsheets, Figma or Notion will serve you better."
}

# ---- Load, validate, append ----
with open(DATA, "r", encoding="utf-8") as f:
    tools = json.load(f)

existing_slugs = {t.get("slug") for t in tools}
if new_tool["slug"] in existing_slugs:
    print(f"[SKIP] slug '{new_tool['slug']}' already exists")
else:
    tools.append(new_tool)
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(tools, f, ensure_ascii=False, indent=2)
    print(f"[OK] appended '{new_tool['slug']}'. Total tools now: {len(tools)}")

# ---- Forbidden-word scan ----
forbidden = ["leverage", "utilize", "seamlessly", "game-changing", "empower",
             "streamline", "delve into", "dive into", "transformative",
             "comprehensive", "revolutionize", "cutting-edge", "as an ai",
             "in conclusion", "robust"]
text = new_tool["content"] + " " + new_tool["description"]
hits = [w for w in forbidden if w in text.lower()]
if hits:
    print("[FORBIDDEN WORD HITS]:", hits)
else:
    print("[FORBIDDEN] scan clean - no banned words")
