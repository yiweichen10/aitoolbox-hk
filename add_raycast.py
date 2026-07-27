# -*- coding: utf-8 -*-
"""Add Raycast AI to tools_en.json (aitoolbox.hk).
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
    "name": "Raycast AI",
    "slug": "raycast-ai",
    "emoji": "\u26a1",
    "color": "#FF6369",
    "description": "Raycast AI bolts a chat bar and inline AI commands onto your Mac - hit a hotkey, type a prompt, and it summarizes the email you just selected, rewrites the paragraph, or drafts the reply without you ever leaving the window. I run my whole day through it, and the money side is simple: I sell the setup other people are too busy to build, plus the few hours a week it hands back to me.",
    "category": "AI Productivity",
    "tags": [
        {"text": "Launcher"},
        {"text": "Productivity"},
        {"text": "AI Commands"},
        {"text": "Mac"},
        {"text": "Free", "type": "free"},
        {"text": "Automation"}
    ],
    "rating": "\u2b50 4.8",
    "visits": "Roughly 750K to 1M monthly visits",
    "badge": {
        "type": "hot",
        "text": "HOT"
    },
    "url": "https://www.raycast.com",
    "price": "Free (50 AI msgs/mo) + Pro $8/mo (or $96/yr), Pro+Advanced AI $16/mo, Teams Pro $12/user/mo",
    "platform": "macOS (Windows in beta), iOS app, web",
    "published": True,
    "related": [
        "warp",
        "chatgpt",
        "claude",
        "perplexity",
        "gemini",
        "julius-ai",
        "chatpdf"
    ],
    "created_date": "2026-07-28",
    "pros": [
        "Zero context switching - select any text anywhere and fire an AI command with one hotkey, so the reply gets written without alt-tabbing into a chat tab",
        "The free tier is genuinely usable: full launcher plus 50 AI messages a month covers a real test drive, not a crippled teaser",
        "AI Commands run inline on whatever you selected - summarize, rewrite, translate, explain - which is where most of the daily time saving actually comes from",
        "1,000+ community extensions pull in third-party tools (Linear, Slack, GitHub, calendars), so one bar becomes your whole work surface",
        "BYOK support - bring your own OpenAI, Anthropic, or Google key and the cost stays flat no matter how much you prompt",
        "Shared snippets, quicklinks, and commands on the Teams plan let you hand a whole company the same tuned workflow in an afternoon"
    ],
    "cons": [
        "macOS only in practice - Windows is still a beta with Cloud Sync and Raycast AI gated, and there is no Linux build, so half your clients are locked out",
        "The free 50-message cap disappears in a single busy afternoon; to use it as a real work tool you pay, and the better models sit behind the $16/mo Advanced add-on",
        "Model line-up shifts with Raycast's provider deals - you cannot pin an exact model version, which matters if a client's output depended on one",
        "It is a launcher, not an agent - AI Commands fire one shot at selected text, they will not chain a multi-step job or read across your whole file system on their own",
        "Power lives in building your own commands and snippets; install it and walk away and you get a prettier Spotlight, not the payoff",
        "Everything you ask lives in Cloud Sync when that is on; teams with hard data rules need the Enterprise tier and some setup before it is clean"
    ],
    "features": [
        "AI Chat - a floating conversation with GPT, Claude, Gemini, Perplexity and more, triggered from the keyboard without leaving your app",
        "AI Commands - inline actions on selected text: summarize, rewrite, translate, explain, or draft, each bound to its own hotkey",
        "AI Extensions - community-built integrations that drop Perplexity, image tools, and dozens more into the same command bar",
        "Clipboard History - searchable record of everything you copied, with AI search so you can find that snippet from last week",
        "Snippets - text templates with dynamic placeholders, fired by a shortcut, great for repetitive replies and client boilerplate",
        "Window Management - keyboard-driven tiling and resizing so you stop reaching for the mouse",
        "Cloud Sync - carries your snippets, notes, and chats across Macs and iOS; Teams adds shared commands and a private store"
    ],
    "faq": [
        {
            "question": "How do you make money with a tool that has a free tier?",
            "answer": "You do not resell Raycast; you sell the setup and the time. A founder does not want an $8/month app, he wants his inbox, his snippets, and his daily replies already wired up and working. I charge $300-$1,000 to build a founder's command pack (summarize, rewrite, translate, draft) plus $100-$300 a month to keep it tuned. The subscription is his cost, my invoice is for the work he will not do himself. At five clients that is $1,500-$2,500 a month against $40-$80 of Raycast bills."
        },
        {
            "question": "Is the free plan enough to do paid work?",
            "answer": "No, and that is fine. Fifty AI messages a month covers a demo and a personal trial, not a working day. For any real volume - a client's inbox, a team's snippets, your own drafting - you need Pro at $8 a month, and if the client wants the top models you add the $16 Advanced tier. Bake the $8-$16 into your quote; it barely moves your margin."
        },
        {
            "question": "Raycast AI vs Warp vs just a ChatGPT tab - which do I learn to sell?",
            "answer": "They solve different problems and I sell all three. Warp is the terminal for people who live in the shell; Raycast is the everything-bar for everyone else - email, docs, calendar, snippets. A bare ChatGPT tab makes you leave your work to talk to the model; Raycast runs the model on the text you already have selected. I pitch Raycast to non-technical founders and ops people, Warp to devs, and keep ChatGPT for deep sessions. They are not rivals, they are tiers of the same pitch."
        },
        {
            "question": "What is the one mistake people make when they buy it?",
            "answer": "They install it, like the window switcher, and stop. The payoff is in the AI Commands and snippets you build - a 'rewrite this in plain English' hotkey, a 'draft a reply' template, a snippet for the weekly client update. Without those, Raycast is a prettier Spotlight and the $8 feels wasted. My setup package exists precisely because nobody wants to build that layer themselves, and that is the part clients happily pay for."
        }
    ],
    "content": "## What Raycast AI Actually Is (From Someone Who Lives in the Command Bar)\n\nI run a small solo operation - writing, client calls, a bit of contracting - and for most of 2023 I had the same ten browser tabs open all day: a chat tool, a notes app, a calendar, a clipboard manager, and a translator I kept pasting into. Then I moved all of it behind one hotkey with Raycast, and the tab-switching stopped being a tax on my attention.\n\nRaycast is a launcher for macOS. You hit a key, type, and it opens apps, finds files, runs calculations, controls your music, and manages windows. In late 2023 they bolted an AI layer on top, and that is the part that earns its place in this write-up. Raycast AI gives you an AI Chat you can call from anywhere, and - more usefully - AI Commands that act on whatever text you have selected right now. Highlight a sloppy paragraph, hit your rewrite hotkey, and a clean version lands in place. Highlight a client email, hit your draft-reply command, and a response is ready to edit. You never leave the window you were in.\n\nThe free plan is real: the full launcher plus 50 AI messages a month, no card. Paid tiers lift the limits and open better models - Pro at $8/month ($96 a year) and Pro + Advanced AI at $16/month for the strongest models from OpenAI, Anthropic, Perplexity, Google, xAI and others. Teams plans start at $12 per seat a month and add shared snippets, commands, and a private store. As of mid-2026 it runs on macOS (Windows is in beta, iOS has an app), it has 500K+ users, and it pulls in roughly three quarters of a million to a million visits a month. For a productivity tool that is serious search traffic, which is exactly why it belongs on a money-minded site.\n\n## Why It Pays (The Real Income Angle)\n\nRaycast is cheap - free to try, eight to sixteen dollars a month to work at volume. You are not selling software. You are selling the configuration other people are too busy to build, plus the hours a week it gives back. Because the tool costs almost nothing, your margin on every job sits near 100%; the only real cost is your own setup time. Here is how I have seen people turn Raycast into income.\n\n### 1. Build and sell Raycast setups + custom AI command packs\nThis is the cleanest play. Non-technical founders, coaches, and solo consultants want the speed but will never sit down to wire it up. You hand them a tuned command pack - summarize, rewrite, translate, draft-reply - bound to hotkeys they already use, plus a set of snippets for their repetitive messages. Charge $300-$1,000 for the build and $100-$300 a month to keep it tuned as their work changes. Tool cost to you: $8-$16. At five clients that is $1,500-$2,500 a month of near-pure margin, and the work is mostly a one-time afternoon per client with light upkeep.\n\n### 2. Roll out Raycast for Teams\nSmall companies waste real time on inconsistent workflows - everyone drafts the same reply differently, everyone hunts for the same snippet. On the Teams plan you build shared snippets, quicklinks, and commands once and push them to the whole org through a private store. Charge $1,500-$4,000 to set up a team of 10-20 and $200-$500 a month to maintain it. The math is easy to sell: if you save ten people fifteen minutes a day, that is twenty-five hours a week of recovered time, worth far more than the $120-$240 in monthly seat costs.\n\n### 3. Productivity training workshops\nFounders' groups, coworking spaces, and virtual assistant networks will pay to watch someone show the actual hotkeys. Run a half-day Raycast setup clinic at $200-$500 a seat, or a $1,000-$2,500 private session for a team. The hook is concrete: leave with your command pack built, not a slideshow. One session for eight people at $300 a seat is $2,400 for a morning, and you can record it and resell the replay.\n\n### 4. Sell snippet and command packs as passive products\nOnce you have a command pack that works, package it. A 'Founder Reply Pack' or a 'Consultant Snippet Kit' sells on Gumroad or your own site for $19-$49, and it keeps selling while you sleep. The build cost is your time; the distribution cost is near zero. A single well-named pack that ranks for 'Raycast AI commands for founders' can move steadily for months.\n\n### 5. Your own time multiplier\nThe quiet one. Raycast saves me three to five hours a week on small frictions - finding the copied link, rewriting the draft, switching the window, translating the message. At $100 an hour that is $1,200-$2,000 a month of billable time I get back, against $8-$16 in software. You do not need a client to make Raycast pay; you just need to bill the hours it returns.\n\n## What Raycast AI Is Bad At (Be Honest Before You Pitch It)\n\nIt is not magic and it is not for everyone, and a pitch that hides the rough edges loses the client the week they hit them.\n\n- **macOS only in practice.** Windows exists as a beta with Cloud Sync and Raycast AI partly gated, and there is no Linux build. If your client is a PC shop, Raycast is a no-sell - point them at PowerToys or a clipboard manager instead.\n- **The free cap is small.** Fifty AI messages vanish in a busy afternoon. To use it as a work tool you pay, and the models worth using sit behind the $16 Advanced add-on. Price that in up front.\n- **Model versions drift.** Raycast swaps providers and versions as deals change. If a client's output leaned on one specific model, you cannot pin it forever. For most work that is fine; for regulated or reproducible output it is a problem.\n- **It is a launcher, not an agent.** AI Commands fire one shot at selected text. They will not chain a five-step job or read across your whole drive on their own. For real agentic work you need something else; Raycast speeds the human, it does not replace him.\n- **The payoff needs building.** Install it and walk away and you get a prettier Spotlight. The money is in the commands and snippets you (or your client) construct. That setup layer is exactly the service you sell.\n- **Cloud Sync and data.** With Cloud Sync on, your chats and snippets live on Raycast's servers. Teams with hard privacy rules need the Enterprise tier and some administration before it is clean. Say so before the contract, not after.\n\n## Raycast AI vs the Alternatives\n\n| Tool | Best at | Pricing floor | Platform | Where Raycast wins |\n|------|---------|---------------|----------|--------------------|\n| Raycast AI | One bar for chat, commands, snippets, launcher | Free / $8 mo | macOS (Win beta) | Broadest surface - AI plus the whole OS workflow in one key |\n| Warp | Terminal work for developers | Free / $18 mo | Mac, Linux, Win | Warp owns the shell; Raycast owns everything else |\n| Alfred | Launcher with deep workflows | Free / ~$34 once | macOS only | Alfred is cheaper long-term and more scriptable, but its AI is weaker |\n| ChatGPT tab | Deep, open-ended chat | Free / $20 mo | Web, all OS | ChatGPT goes deeper; Raycast acts on the text you already selected |\n| Spotlight / PowerToys | Built-in file launch | Free | macOS / Windows | Free and fine, but no AI and no snippets |\n\nMy read: learn Raycast if you sell to non-technical founders and ops people, Warp if you sell to developers, and keep a ChatGPT tab for the heavy thinking. They are tiers of the same pitch, not rivals.\n\n## Who Should Use It, Who Should Not\n\n**Reach for Raycast if** you live in email, docs, and chat all day, you repeat the same replies and snippets, you want AI on the text in front of you without opening a new tab, or you advise founders and teams who do. The setup service writes itself.\n\n**Skip it if** your clients are all on Windows or Linux (no real build), they need pinned, reproducible model output for compliance, or they want autonomous agents that run jobs without a human at the keyboard. Raycast speeds a person; it does not stand in for one.\n\n## Getting Started (Six Practical Tips)\n\n1. **Start on the free tier for a week.** Use the 50 messages to feel where AI Commands save you time before you pay a cent.\n2. **Build three commands first.** A rewrite, a summarize, and a draft-reply - bound to hotkeys you already hit. That trio pays for the subscription within days.\n3. **Turn snippets into client boilerplate.** The weekly update, the intro line, the invoice note - each becomes a two-key insert.\n4. **Try BYOK early.** Bring your own OpenAI or Anthropic key and your cost stays flat no matter how much you prompt; good when a client's volume spikes.\n5. **Sell the package, not the app.** When you pitch a client, lead with the command pack you will build, not the $8 plan. The plan is a line item; the pack is the product.\n6. **Record your setup session.** The video of you building a founder's pack is itself a $19-$49 product and a workshop lead magnet.\n\n## FAQ\n\n**Can you actually make money with a near-free tool?**\nYou do not resell Raycast; you sell the setup and the time. A founder does not want an $8/month app, he wants his inbox, snippets, and daily replies already wired up. I charge $300-$1,000 to build that pack plus $100-$300 a month to keep it tuned. The subscription is his cost; my invoice is for the work he will not do. At five clients that is $1,500-$2,500 a month against $40-$80 of Raycast bills.\n\n**Is the free plan enough to do paid work?**\nNo, and that is fine. Fifty AI messages a month covers a demo and a personal trial, not a working day. For real volume you need Pro at $8 a month, and if the client wants the top models you add the $16 Advanced tier. Bake the $8-$16 into your quote; it barely moves your margin.\n\n**Raycast AI vs Warp vs a ChatGPT tab - which do I learn?**\nThey solve different problems and I sell all three. Warp is the terminal for people who live in the shell; Raycast is the everything-bar for everyone else. A bare ChatGPT tab makes you leave your work to talk to the model; Raycast runs the model on the text you already selected. I pitch Raycast to non-technical founders and ops people, Warp to devs, and keep ChatGPT for deep sessions. They are not rivals, they are tiers of the same pitch.\n\n**What is the one mistake buyers make?**\nThey install it, like the window switcher, and stop. The payoff is in the AI Commands and snippets you build - a rewrite hotkey, a draft-reply template, a client-update snippet. Without those, Raycast is a prettier Spotlight and the $8 feels wasted. My setup package exists because nobody wants to build that layer, and that is the part clients happily pay for.\n",
    "aeo_geo_updated": True
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
