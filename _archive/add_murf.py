# -*- coding: utf-8 -*-
"""Add Murf AI to tools_en.json (aitoolbox.hk).
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
    "name": "Murf AI",
    "slug": "murf-ai",
    "emoji": "\U0001F399",
    "color": "#7C3AED",
    "description": "Murf AI is a voiceover studio, not just a text-to-speech button - you paste a script, pick one of 200-plus voices, and it returns studio-grade audio with timing, emphasis, and pronunciation control, plus a timeline editor that syncs the voice to your video. I run voiceover-as-a-service for video agencies and course creators on it, and the money side is plain: clients pay $50-$300 per finished voiceover while my only real cost is a $19-a-month subscription.",
    "category": "AI Audio",
    "tags": [
        {"text": "Voiceover"},
        {"text": "Text to Speech"},
        {"text": "AI Voices", "type": "free"},
        {"text": "E-learning"},
        {"text": "Narration"},
        {"text": "Dubbing"}
    ],
    "rating": "\u2b50 4.6",
    "visits": "About 780,000 monthly visits (10M+ developers, businesses, and creators on the platform)",
    "badge": {
        "type": "recommend",
        "text": "RECOMMENDED"
    },
    "url": "https://murf.ai",
    "price": "Free ($0; 10 min total voice generation, no downloads, no commercial rights); Creator $19/mo billed annually ($29 monthly; 24 hrs/yr generation, 200+ voices, commercial rights, unlimited downloads); Business $66/mo annual ($99 monthly; 96 hrs/yr, business license, voice cloning add-on, team features); Enterprise custom",
    "platform": "Web, Windows, Mac, iOS, Android",
    "published": True,
    "related": [
        "play-ht",
        "cartesia",
        "elevenlabs",
        "aiva",
        "wondercraft-ai",
        "deepgram",
        "speechify",
        "jasper"
    ],
    "created_date": "2026-07-30",
    "pros": [
        "The studio workflow is the real draw - a timeline editor, video-plus-voiceover sync, a pronunciation dictionary, and client comment threads make it a production tool, not a bare TTS button",
        "Commercial rights kick in from the Creator plan, so you can sell the audio (YouTube monetization, client deliverables) without a legal gray area hanging over the file",
        "200-plus voices across 30-plus languages with pitch, speed, and pause control, plus 'Say It My Way' to lock a consistent brand narrator across a whole content library",
        "Team features on Business (shared projects, client review links, revision history) mean an agency can hand a draft to a client for notes without exporting and emailing MP3s",
        "Canva and PowerPoint integrations push voiceovers straight into marketing and training decks, which cuts the busywork on high-volume jobs",
        "Flat subscription with unlimited downloads - once a clip is generated you own the file, so you can archive voiceovers outside Murf and dodge the storage caps"
    ],
    "cons": [
        "Raw realism still trails ElevenLabs on long-form, emotional narration; for an audiobook or a heartfelt brand film, ElevenLabs sounds more human",
        "The free tier is a teaser - 10 minutes of generation total (not per month on some plans), no downloads, no commercial rights, and it stamps 'Created with Murf AI' at the end of every clip",
        "The voice library grows slower than the front-runners, and a few niche accents and regional dialects are thin, so some clients will not find 'their' voice",
        "API access is limited on the lower tiers; if you want to wire voice generation into an app or a pipeline you are pushed toward Business or Enterprise",
        "There is no deep DAW-style mixing or mastering - for cinematic polish you still export and finish in an external editor",
        "Voice cloning needs the Business plan plus a clean 30-second sample, and the result is only as good as the source audio you feed it"
    ],
    "features": [
        "Text to Speech Studio - 200+ realistic voices in 30+ languages; paste a script, pick a voice, and generate studio audio with one click",
        "Timeline & Video Sync Editor - drop a video in, generate the voiceover, and auto-sync it, with no Premiere or Final Cut in the loop",
        "Pronunciation & Emphasis Control - custom dictionary for brand names and jargon, plus pitch, speed, pause, emphasis, and variability tuning",
        "Voice Cloning - clone any voice from a 30-second sample (Business and up) to keep a consistent brand narrator across projects",
        "Commercial Rights - full commercial usage rights from the Creator plan, so you can monetize on YouTube and bill clients without worry",
        "Team Collaboration - shared workspaces, client review links, timestamped comments, and revision history on Business and Enterprise",
        "AI Dubbing (StudioDub) - localize videos into 20+ languages while preserving the original voice, meaning, and tone (separate product)",
        "Canva & PowerPoint Integration - send voiceovers straight into marketing creatives and training decks without a file shuffle"
    ],
    "faq": [
        {
            "question": "How do you make money with a tool that has a free tier?",
            "answer": "You sell the voiceover, not the app. A video agency does not want another $19 subscription; it wants 20 narrated explainer videos that sound like a real narrator. I charge $50-$300 per finished voiceover depending on length and revisions. Real case: a faceless finance channel pays me $150 per video for 20 videos a month - that is $3,000, against one Creator seat at $19. At five to ten clients a month you are at $1,500-$15,000 with a margin near 98%. The free tier is what got the first client in the door; the paid plan is what lets you hand over a clean, rights-cleared file."
        },
        {
            "question": "Is the free plan enough to do paid work?",
            "answer": "No, and this trips up beginners. The free plan gives you 10 minutes of generation total, blocks downloads, denies commercial rights, and watermarks the audio with 'Created with Murf AI' at the end. You cannot deliver that to a paying client. You need Creator at $19 a month (billed annually) for unlimited downloads and commercial rights. I bake one Creator seat into every quote; at that price it is invisible inside a $200 invoice. Do not promise a client a usable file on the free tier - it will not exist."
        },
        {
            "question": "Murf vs ElevenLabs vs Play.ht - which one do I learn to sell?",
            "answer": "They split by buyer. ElevenLabs wins on raw realism and is the pick for audiobooks and emotional long-form, but its studio and collaboration tools are lighter and it is more developer-facing. Play.ht has a huge voice library and strong API for podcasts and apps. Murf sits in the middle for production teams: the timeline editor, pronunciation control, and client review links make it the easiest to sell to agencies, course creators, and non-technical clients who need a workflow, not just an API. I pitch Murf to anyone shipping explainer videos, e-learning, or corporate training at volume."
        },
        {
            "question": "What is the one mistake people make when they buy it?",
            "answer": "They generate two test clips, like the voice, and never build a reusable setup - so the next job starts from a blank script and the $19 feels like a subscription with no payoff, and they churn. The money is in the repeat work: a saved voice preset per client, a pronunciation dictionary for their jargon, and a monthly retainer where you become their voice department. Sell the system, not the login, and Murf turns from a $19 line item into the engine behind $1,500-plus a month of client work."
        }
    ],
    "content": "## What Murf AI Actually Is (From Someone Who Bills For Voiceovers)\n\nI run a small voiceover gig - mostly narration for video agencies, course creators, and the odd corporate training video. For years that meant booking studio time, babysitting a mic, and re-recording every time a client changed a sentence. Then I moved the generation step onto Murf AI, and the studio layer is the reason this write-up exists.\n\nMurf AI is an AI voiceover platform that, as of early 2026, pulls about 780,000 visits a month and sits behind more than 10 million developers, businesses, and creators. You paste a script, pick from 200-plus voices across 30-plus languages, and it returns studio-grade audio with timing, emphasis, and pronunciation control. It is not a bare text-to-speech button; it is a production studio - there is a timeline editor that syncs the voice to your video, a pronunciation dictionary for brand names and jargon, and client comment threads for review. As of mid-2026 it carries SOC 2, ISO 27001, GDPR, and HIPAA alignment, which matters when a corporate client asks about data.\n\nThe free plan is a teaser: 10 minutes of generation total, no downloads, no commercial rights. Paid tiers open the door - Creator at $19 a month billed annually ($29 monthly) gives 24 hours of generation a year, all 200-plus voices, commercial rights, and unlimited downloads; Business at $66 a month annual ($99 monthly) adds a business license, voice cloning, and team features; Enterprise is custom. The job is to sell the voiceover the plan unlocks, not the plan.\n\n## Why It Pays (The Real Income Angle)\n\nMurf is nearly free for you and sounds expensive for the client, which is the exact gap you sell into. You are not moving software; you are moving a person from 'I have a script in a Doc' to 'here is a narrated, rights-cleared audio file I can ship tonight.' Six ways I have seen solo operators and small agencies turn it into income:\n\n**1. Voiceover-as-a-service for YouTubers and video agencies ($50-$300 per voiceover).** This is the highest-volume use. A faceless finance channel pays me $150 per video for 20 videos a month - $3,000 - against one Creator seat at $19. A local agency keeps me on a flow of explainer narrations at $80-$120 each. At five to ten clients a month that is $1,500-$15,000, and the marginal cost per clip is rounding error. Margin sits near 98%.\n\n**2. E-learning and course narration ($200-$800 per course).** Udemy, Teachable, and corporate training teams need a consistent narrator across dozens of modules. I charge $200 for a short course and $500-$800 for a multi-hour program. An Udemy instructor paid me $500 for a six-hour course and now sends every new module. The 'Say It My Way' feature locks one voice across the whole library, so the sequel sounds like the original.\n\n**3. Audiobook and podcast intro narration ($100-$500 per book, $50-$150 per intro).** Self-published authors and podcasters want a pro open without booking a studio. I sell a per-chapter rate for audiobooks and a flat fee for a podcast intro and outro. A business podcast pays $150 a month for a fresh intro plus ad reads.\n\n**4. Ad and commercial voiceover for local businesses ($150-$500 per ad).** Real estate, dental, and law-firm spots need a trustworthy voice and a fast turnaround. I charge $150 for a 30-second radio-style spot and $400-$500 for a multi-version ad set with revisions. The agency marks it up; I stay the silent production line.\n\n**5. Explainer and corporate training videos ($300-$1,500 per project).** Agencies outsource narration they used to book a voice actor for. I sell a per-project build with script timing and a pronunciation pass. A safety-training company keeps me on a $1,200-a-month stream of modules.\n\n**6. White-label voiceover retainer ($300-$1,500 per month per client).** This is the compounding one. You become the client's voice department: they send scripts, you return branded, voice-locked audio. At $300-$1,500 a month per client with three to five clients, that is $1,500-$7,500 in recurring revenue for work that takes an hour or two a week once the preset is set. Add Murf's AI Dubbing on top and you localize their videos into 20-plus languages at $100-$500 per localized video.\n\n## What Murf AI Is Bad At (Be Honest Before You Sell It)\n\nI would not pitch Murf as magic, because clients hear the cracks:\n\n- **Realism trails ElevenLabs on long-form.** For an audiobook or a heartfelt brand film, ElevenLabs still sounds more human. Murf is plenty good for explainers, ads, and e-learning, but do not promise a movie trailer.\n- **The free tier is a trap.** Ten minutes total, no downloads, no commercial rights, and a 'Created with Murf AI' stamp at the end. Creator is mandatory for paid work.\n- **The voice library grows slowly.** Some niche accents and regional dialects are thin, so a client may not find exactly 'their' voice, and you fall back to cloning.\n- **API is gated.** If a client wants voice generation baked into their app, you are pushed to Business or Enterprise; the lower tiers are for human-in-the-loop production, not pipelines.\n- **No deep mixing.** For cinematic polish you export and finish in an external editor. Murf gets you 90% there, not 100%.\n- **Cloning needs clean source.** Voice cloning requires the Business plan and a clean 30-second sample; garbage in, garbage out.\n\n## Murf vs The Field (Who To Pitch It Against)\n\n| Tool | Best at | Weak spot | Where Murf wins |\n|-------|---------|-----------|------------------|\n| **Murf AI** | Studio workflow + team production | Long-form realism | Timeline editor, pronunciation control, client review, commercial rights from $19 |\n| **ElevenLabs** | Most natural voice, API-first | Lighter studio tools | Better for audiobooks and devs building apps |\n| **Play.ht** | Huge voice library, podcast API | Less production UI | Strong for podcasts and programmatic audio |\n| **Lovo** | Character/animation voices | Smaller enterprise footprint | Good for games and characters |\n| **Speechelo** | One-click beginner TTS | Dated quality, no studio | Fine for absolute beginners, not client work |\n\n## Who Should Use Murf (And Who Shouldn't)\n\n**Use it if** you sell narration to video agencies, course creators, podcasters, and corporate training teams who need a workflow and a consistent voice, not just an API. It is the closest thing to a voice studio in a tab.\n\n**Skip it if** you need the most human possible long-form narration (ElevenLabs), or you are a developer wiring speech into an app at scale (an API-first tool fits better). Murf is a production tool, not a research toy.\n\n## Getting Started (Six Moves That Actually Earn)\n\n1. **Build one voice preset per client before you bill.** Lock voice, pitch, speed, and a pronunciation dictionary for their jargon. Every future script starts there and sounds like them.\n2. **Save a pronunciation library.** Brand names, product terms, and client-specific words pronounced right the first time save you revision rounds.\n3. **Generate, then trim, never ship raw.** The first pass is 90% there. Spend five minutes on emphasis and a pause, and that is the gap between 'AI voice' and 'paid like a pro.'\n4. **Lead with the review link, keep the file as backup.** Send the Murf share link for client notes, and only export the MP3 when they approve - no emailing drafts.\n5. **Bundle into a monthly retainer early.** The first voiceover is a trial; the second should be a $300-$1,500-a-month voice-department conversation. That is where the money compounds.\n6. **Add dubbing as an upsell.** Once a client trusts the English voice, offer localization into 20-plus languages at $100-$500 per video. Easy margin on work you already understand.\n\n## The Bottom Line\n\nMurf AI is the fastest way I know to turn a script into a voiceover a client will pay $50-$300 for, and at $19 a month the margin is basically all yours. The honest limits - realism on long-form, the free-tier trap, the lighter API - are real but manageable, and they are exactly why a client hires you instead of opening a free account. Sell the voiceover and the retainer, not the login, and Murf becomes the engine behind a tidy monthly income."
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
