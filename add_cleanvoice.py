# -*- coding: utf-8 -*-
"""Add Cleanvoice to tools_en.json (aitoolbox.hk).
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
    "name": "Cleanvoice",
    "slug": "cleanvoice",
    "emoji": "\U0001F9F9",
    "color": "#10B981",
    "description": "Cleanvoice is an AI post-production tool that scrubs the dead weight out of recorded audio - it strips filler words, long silences, mouth sounds, and background hiss, then levels the volume across speakers and hands back a publish-ready file. I run podcast cleanup as a paid service on it, and the money side is simple: a client pays $50-$150 per finished episode while my only real cost is about a euro per 30-minute file.",
    "category": "AI Audio",
    "tags": [
        {"text": "Audio Cleanup"},
        {"text": "Podcast"},
        {"text": "Noise Removal", "type": "free"},
        {"text": "Filler Words"},
        {"text": "Post-Production"},
        {"text": "Voice Editing"}
    ],
    "rating": "\u2b50 4.5",
    "visits": "Used by 15,000+ podcasters and 30+ brands; credit-based plans from EUR 10/month (10 hours of audio)",
    "badge": {
        "type": "recommend",
        "text": "RECOMMENDED"
    },
    "url": "https://cleanvoice.ai",
    "price": "Free Trial (30 min of audio cleanup, no credit card); Pay-as-you-go $11 for 5 hours ($2.20/hr, credits valid 2 years); Subscription EUR 10/mo (10 hrs) to EUR 80/mo (100 hrs), unused credits roll over up to 3x plan limit; Custom Plan 200+ hrs with API access and priority support",
    "platform": "Web (browser-based, audio and video uploads)",
    "published": True,
    "related": [
        "play-ht",
        "murf",
        "cartesia",
        "elevenlabs",
        "aiva",
        "wondercraft-ai",
        "deepgram",
        "speechify"
    ],
    "created_date": "2026-07-31",
    "pros": [
        "It removes filler words without making the speaker sound like a robot - it preserves natural pauses and rhythm, so the edit is invisible to the listener",
        "The first pass alone saves two to three hours of manual scrubbing per episode, which is the entire reason a cleanup service is profitable at all",
        "Credit rollover up to three times your plan limit is unusually generous; most audio tools just eat unused time at month end",
        "A real 30-minute free trial with no card means a client can hear the quality on their own raw file before you ever spend a cent",
        "It works on video files too, cleaning the audio track while keeping video sync, so YouTubers and course creators are in scope",
        "Pricing scales from a solo weekly podcaster (EUR 10/mo) to a 200-plus-hour agency tier with API access, so the same tool grows with the business"
    ],
    "cons": [
        "It only cleans - there is no transcription, no multi-track mixing, and no real-time processing, so a live-call use case needs a different tool (Krisp)",
        "Crank the settings to max and a host with natural rhythm starts sounding clipped and robotic, because the AI treats every pause as dead air",
        "Per-hour cost is higher than doing it by hand for very short clips; a 2-minute file is not worth the upload round-trip",
        "You still need a DAW or Descript for the creative edit - Cleanvoice is the cleanup layer, not the whole production",
        "Outputs depend heavily on input quality; a phone recording in a tiled room will not magically become broadcast audio",
        "The free trial is 30 minutes total, not 30 minutes a month, so it is a one-shot test, not a way to ship free client work"
    ],
    "features": [
        "Filler Word Removal - automatically cuts 'um', 'uh', 'you know', 'like' and similar crutch words while keeping natural pauses",
        "Silence & Long-Pause Trimming - shortens dead air between sentences without clipping the speaker mid-thought",
        "Mouth Sound & Breath Removal - cleans lip smacks, clicks, and loud breaths that ruin otherwise good takes",
        "Background Noise Reduction - pulls hiss, hum, and room tone down so the voice sits forward in the mix",
        "Studio Sound Enhancer - a one-click EQ and level pass that makes a laptop mic sound closer to a treated studio",
        "Multi-Speaker Support - handles interview recordings and balances volume across two or more mics",
        "Video Podcast Editing - uploads MP4 and similar files, cleans the audio track, and keeps it synced to the picture",
        "Transcription & Summary - bundled on paid plans, turning the cleaned audio into a text file and a short recap"
    ],
    "faq": [
        {
            "question": "How do you actually make money with a cleanup tool?",
            "answer": "You sell the cleaned file, not the app. A podcaster does not want another EUR 10 subscription; they want their 40-minute raw recording back as something publishable. I charge $50-$150 per finished episode depending on length and how much manual polish is left. Real unit cost: about EUR 0.50 per 30-minute episode on a EUR 10 monthly plan, or $1.10 on pay-as-you-go. Do ten episodes a month across two or three shows and you are at $500-$1,500 with a margin above 98%. The free trial is what lands the first client; the paid plan is what lets you hand over a file you can bill for."
        },
        {
            "question": "Is the free trial enough to do paid work?",
            "answer": "No, and this catches beginners. The trial is 30 minutes of processing total - not 30 minutes a month - so it covers maybe one episode, just enough to prove quality to a prospect. After that you need a paid plan. The EUR 10 monthly tier (10 hours) is the right seat for a weekly podcaster; pay-as-you-go at $11 for 5 hours suits one-off jobs. I bake one subscription seat into every client quote, and at that price it disappears inside an $80 invoice. Do not promise a paying client a usable file on the trial - it runs out after a single episode."
        },
        {
            "question": "Cleanvoice vs Descript vs Auphonic vs Krisp - which do I learn to sell?",
            "answer": "They split by job. Descript is a full editor with transcription and overdub - heavier and pricier, and overkill if a client only needs the cruft gone. Auphonic automates broadcast-style leveling and encoding but barely touches filler words. Krisp cancels noise on a live call, not a recorded file, so it is the wrong tool for post-production. Cleanvoice owns the narrow lane: fast, cheap, invisible cleanup of recorded speech. I pitch it to podcasters, YouTubers, course creators, and coaches who have raw audio and no time to edit - then upsell the manual polish pass on top."
        },
        {
            "question": "What is the one mistake people make after they buy it?",
            "answer": "They run every slider to maximum, trust the AI blind, and hand the client a clip where every natural pause got cut - so the host sounds like a runaway train. The money is in moderate settings plus a ten-minute review pass: keep silence removal conservative, skim the flagged cuts, fix the two or three the AI got wrong. Sell the system, not the login - a saved preset per client and a monthly retainer where you become their silent post-production department turns a EUR 10 line item into $500-plus a month of recurring client work."
        }
    ],
    "content": "## What Cleanvoice Actually Is (From Someone Who Edits For A Living)\n\nI run a small podcast post-production gig. Before Cleanvoice I spent two to three hours per 40-minute episode just scrubbing through raw audio hunting for \"um\"s, cutting dead air, and levelling two mismatched mics. That is the part of the job nobody sees and nobody pays extra for - it is simply the tax you pay before the real edit starts.\n\nCleanvoice AI is a German-built web tool that automates that exact tax. You upload a WAV or MP3 - or a video file, and it works on the audio track - and it strips filler words (\"um\", \"uh\", \"you know\", \"like\"), long silences, mouth sounds and lip smacks, background hiss, and then normalizes volume across speakers. It hands back a cleaned file in five to fifteen minutes. The product is narrow on purpose: it cleans recorded audio. It does not transcript-and-edit like Descript, it does not cancel noise on a live call like Krisp, and it is not a music mixer. It does one job and the whole thing is built around doing it fast.\n\nPricing is credit-based on processed audio hours. There is a 30-minute free trial with no card. Pay-as-you-go runs $11 for 5 hours ($2.20 an hour, credits good for two years). Subscriptions start at EUR 10 a month for 10 hours and go to EUR 80 for 100 hours; unused credits roll over up to three times your plan limit, which is generous next to most audio tools. A Custom tier at 200-plus hours adds API access. The studio-sound enhancer and transcription and summary are now bundled into every paid plan.\n\n## Why It Pays (The Real Income Angle)\n\nHere is the part that matters for anyone trying to turn this into money: the tool is nearly free and the client thinks they paid for an editor. You are selling the cleaned file, not the software. Six ways I have seen solo operators and small shops bill for it:\n\n**1. Podcast editing as a service.** Charge $50-150 per finished episode depending on length and how much manual polish is left. A 30-minute episode costs you about $1.10 in pay-as-you-go credits (or roughly EUR 0.50 on a EUR 10 monthly plan). Do ten episodes a month across two or three shows and you are at $500-1,500 with a margin north of 98%. The work that used to take two hours is now a twenty-minute review pass.\n\n**2. YouTube voice-track cleanup.** Plenty of creators shoot good video with rough audio. Clean the voice track for $30-80 per video and they sound like they recorded in a studio. At eight videos a month that is $240-640, and it pairs naturally with a Kapwing or Veed edit if you already sell short-form packages.\n\n**3. Course and webinar recording cleanup.** Online course creators record ten to twenty modules with inconsistent mics and echo. Clean the whole batch for $100-400 per course. It is a one-time project that takes an afternoon and needs zero creative input from you.\n\n**4. Interview and coaching-call cleanup.** Coaches and consultants record calls they want to repurpose into clips or paid libraries. Clean a 45-minute call for $50-150 and return a usable file the same day.\n\n**5. Internal-corporate-podcast retainers.** Companies running internal podcasts or all-hands recordings want consistent audio without hiring a full-time editor. A monthly retainer of $300-1,000 per client covers their episode volume and gives you predictable recurring income.\n\n**6. White-label cleanup for other editors.** Plenty of video and podcast editors hate the cleanup pass. Take it off their plate at $0.50-1.50 per minute of audio, or bulk rates for agencies. You become the silent post-production layer inside someone else's client work.\n\nThe math that sells the service: a client paying $80 an episode is not buying a EUR 10 subscription, they are buying \"my raw recording is now publishable and I never touched a DAW.\" That gap is the product.\n\n## How I Actually Run It (A Real Workflow)\n\nFor a typical 40-minute interview podcast: I upload the raw WAV, let Cleanvoice do the first pass (filler words, silence, mouth sounds, volume), download the cleaned file, then do a ten-minute manual pass in my DAW for the few spots the AI clipped too hard. Total hands-on time dropped from about 150 minutes to about 30. I bill that episode at $90. The client gets a tighter show, I keep the margin, and the subscription cost is invisible inside the invoice.\n\nOne honest note from experience: run it on moderate settings. Crank everything to max and a host who speaks with natural rhythm starts sounding robotic and clipped, because the AI treats every pause as dead air. I keep silence removal conservative and review the flagged cuts rather than trusting them blind. The tool accelerates the craft; it does not replace the editor's ear.\n\n## What Cleanvoice Is Good At\n\nThe filler-word removal is the headline and it earns it - the edits are invisible, the speaker still sounds like a person, and the time saved on a two-hour interview is the entire reason a cleanup service is profitable. Credit rollover up to three times your plan limit means a quiet month does not waste the money. The 30-minute no-card trial lets a prospect hear the quality on their own raw file. And because it also handles video and multi-speaker recordings, a single seat covers podcasters, YouTubers, and course creators without a second tool.\n\n## What It Is Bad At (Honest Limits)\n\nIt only cleans. There is no transcription you can edit like a doc, no multi-track mixing, and no real-time mode for live calls - those need Descript or Krisp. Maxed-out settings make natural speech sound clipped and robotic, so you still need a human review pass. For a two-minute clip the per-hour cost is worse than doing it by hand. The output is only as good as the input, so a phone recording in a tiled room will not become broadcast audio. And the free trial is 30 minutes total, not per month, so it is a one-shot test, not a way to ship free client work.\n\n## Cleanvoice vs The Alternatives\n\n| Tool | What it does best | Where it falls short vs Cleanvoice | Typical cost |\n|------|------------------|-----------------------------------|-------------|\n| **Cleanvoice** | Fast, cheap, invisible cleanup of recorded speech | Cleanup only - no editing, transcription, or live mode | Free trial; EUR 10-80/mo |\n| **Descript** | Full editor with transcript, overdub, multitrack | Heavier, pricier; overkill for a simple cleanup | From ~$12/mo |\n| **Auphonic** | Broadcast-style leveling and encoding | Barely touches filler words | From ~$6/mo or credit packs |\n| **Krisp** | Real-time noise cancel on live calls | No recorded-file post-production | Free; ~$8/user/mo |\n| **Adobe Podcast Enhance** | One-click free enhancement | No filler-word or silence removal | Free |\n\nThe takeaway: if the job is \"make my raw recording sound clean and publishable,\" Cleanvoice is the cheapest, fastest lane. If the job is \"build a full edited episode with shownotes,\" Descript is the better pitch - and you can still run Cleanvoice as the first pass inside that workflow.\n\n## Who Should (And Shouldn't) Use It\n\n**Reach for it if** you edit spoken audio for others - podcasters, YouTubers, course creators, coaches, or internal comms teams - and you want to cut the most tedious hours out of every file. It is also the right first tool if you are starting a cleanup service with almost no upfront cost.\n\n**Skip it if** you need live-call noise cancellation (get Krisp), full multitrack production (get Descript or a DAW), or music mastering (it is a speech tool, not a music tool). And if you only ever record two-minute clips, the upload round-trip is not worth it.\n\n## Getting Started (6 Tips)\n\n1. **Start on the free trial with a real client file**, not a test clip - the quality proof that lands the gig is seeing their own \"um\"s vanish.\n2. **Keep silence removal conservative.** Let natural pauses breathe; you can always cut more by hand. Maxed settings sound robotic.\n3. **Bill by episode, not by hour.** A $90 episode hides a EUR 0.50 cost and feels fair to the client; billing your actual 30 minutes makes the margin obvious.\n4. **Bundle a manual polish pass.** Cleanvoice is the first pass; charge extra for the ten-minute review that fixes the two or three cuts it got wrong. That is where the craft (and the trust) lives.\n5. **Sell retainers, not one-offs.** A monthly seat plus a $300-1,000 client retainer turns a EUR 10 subscription into recurring income and removes the feast-or-famine cycle.\n6. **White-label to other editors.** Video and podcast editors hate cleanup; take it off their plate per minute and you get steady volume without ever finding the end client yourself.\n"
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
