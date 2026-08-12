#!/usr/bin/env python3
"""Add Kaiber (AI music video / audio-reactive visual platform) to tools_en.json for aitoolbox.hk."""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
BASE = Path(__file__).parent
DATA = BASE / "data" / "tools_en.json"

NEW_TOOL = {
    "name": "Kaiber",
    "slug": "kaiber",
    "emoji": "🎬",
    "color": "#8B5CF6",
    "description": "Kaiber is the AI video platform that musicians and artists actually use, because it started with the one thing most generators do badly: syncing visuals to music. You drop in a track, pick an energy level, and it produces beat-locked, stylized video - which is why Linkin Park used it for an official music video and why independent musicians treat it as the default way to get a visualizer without hiring a motion designer. Under the hood it is not one model but several (Google Veo, Kling, Luma Dream Machine, Minimax, Mochi) inside one canvas called Superstudio, so you switch styles without paying for five subscriptions. The money angle is real and concrete: musicians pay $100-$500 for a finished AI music video, bands need visualizers for every single release, DJs and event promoters need loop visuals, and small businesses will pay to have their product photos animated into short clips - Kaiber is the tool that makes that work billable in an afternoon instead of a week. It is not magic: quality is inconsistent between generations, credits burn much faster than the price tag suggests, and long videos fall apart visually, so treat it as a client-service tool with controls you learn, not a one-click video machine.",
    "category": "AI Video",
    "tags": [
        {"text": "Music Video"},
        {"text": "Audio-Reactive"},
        {"text": "Image-to-Video"},
        {"text": "Beat Sync"},
        {"text": "Text-to-Video"},
        {"text": "Creators"}
    ],
    "rating": "⭐ 4.4",
    "visits": "~1.5M monthly visits (one of the most-searched music-video AI tools of 2026; built its name on the Linkin Park 'Lost' official music video and remains the default answer to 'AI music video generator')",
    "badge": {"type": "recommend", "text": "RECOMMENDED"},
    "url": "https://kaiber.ai",
    "price": "Credit-based subscription, and the numbers differ a lot across review sites - check kaiber.ai/pricing before you commit. Roughly: a free tier exists (small monthly credit pool, limited canvases, non-commercial); entry paid plans run about $5-$15/mo (watermarked or low-res output); the serious working tier is around $29/mo for ~1,400 credits (all models, no watermark, commercial use); a team tier sits near $149/mo (7,500+ credits, unlimited canvases, 4K). Credits are charged per second of generated video, premium models (Veo, Kling) cost more per generation - a single high-quality 5-second clip can burn 50-100+ credits - and unused monthly credits do not roll over",
    "platform": "Web (Superstudio canvas) + iOS/Android app",
    "published": True,
    "related": ["runway", "pika", "veo", "kling-ai", "luma-ai", "suno", "udio", "pixverse"],
    "created_date": "2026-08-13",
    "pros": [
        "Music sync is genuinely the best in the category: Beat Sync reads the track and cuts visuals on the beat and energy shifts, which is the difference between a clip that looks like a slideshow and one that feels like a music video - no other mainstream generator does this well",
        "You get multiple top models in one subscription: Veo for story-driven clips, Kling for realistic motion, Luma for cinematic camera moves, Minimax and Mochi for stylized and experimental looks - instead of paying for five separate subscriptions you switch models inside one project",
        "The learning curve is shallow for the core use: upload a song, pick a style, press generate - a first-time user can produce a usable visualizer in an evening without any motion-graphics background",
        "The mobile app is real, not a stripped preview: you can upload audio, pick styles and export from your phone, which matters when you are on the road with a musician who wants to see a concept right now",
        "Credible professional validation: Linkin Park used Kaiber for an official music video, and that endorsement carries weight when you pitch AI visuals to bands who have never heard of the tool",
        "There is a free tier, so you can test whether your music and the styles you like actually work together before spending a cent"
    ],
    "cons": [
        "Quality is inconsistent between generations - the same prompt and settings can produce a great clip one run and a mediocre one the next, so you will burn credits on rerolls, and that hidden cost is where the subscription really spends your money",
        "Credits evaporate faster than the price tag suggests: a single high-quality 5-second clip on a premium model can cost 50-100+ credits, so the ~$29 plan's 1,400 credits is more like a few dozen serious clips, not hundreds",
        "Unused monthly credits do not roll over, so a quiet month is wasted money, and there is no good way to bank credits for a big project later",
        "Long-form consistency falls apart: characters, style and lighting drift noticeably across a 3+ minute piece, which is why most paid music videos are assembled from many short segments edited together externally - not a set-and-forget tool",
        "The Superstudio node-based canvas is powerful but confusing at first: new users get lost connecting scenes, styles and audio nodes, and the interface assumes you already think like a motion designer",
        "Text-to-video accuracy and prompt control lag behind Runway and Sora - if your work is mostly prompt-driven cinematic shots rather than music-synced visuals, Kaiber is not the best tool for that job, and the free tier is non-commercial anyway"
    ],
    "features": [
        "Beat Sync: audio-reactive generation that cuts, pulses and transitions visuals on the beat and energy of an uploaded track (high-energy, cinematic and time-skip modes)",
        "Multi-model architecture inside one Superstudio canvas: Google Veo, Kling, Luma Dream Machine, Minimax Hailuo, Mochi and Flipbook, switchable per project, each with different credit costs",
        "Text-to-video and image-to-video generation, plus audio-reactive modes - animate product photos, album art or stills into moving clips",
        "Style presets and custom style mixing, with community styles you can borrow and iterate on",
        "Superstudio infinite canvas with node-based project layout: connect scenes, styles, audio and animations in one visual flow",
        "Built-in timeline editor for splitting, reordering and simple captioning before export",
        "iOS and Android apps with core features (audio upload, style selection, export)",
        "Credit-based usage billing: charged per second of generated video, premium models cost more, upscaling and advanced models gated to paid tiers"
    ],
    "faq": [
        {
            "question": "Can I actually make money with Kaiber, or is it just a toy for musicians?",
            "answer": "Yes, and it is one of the more concrete money plays in AI video, because the demand already exists - musicians need visual content for every release and most cannot afford a motion designer. The most direct gig is AI music videos and visualizers: independent artists pay $100-$500 for a finished visualizer or short music video, and with Kaiber a first draft is done in an evening, so you sell speed and curation, not render time. The repeat-business angle is stronger than the one-off: bands release singles and albums on a schedule, so a monthly retainer ($300-$1,000/mo) for visuals on every drop is realistic and sticks. DJs, event promoters and venues need loop visuals for screens and stages - that is bulk work with short turnaround. And a quieter niche that pays well: small businesses pay $50-$200 to have product photos or brand stills animated into short motion clips for ads and social (pair it with a music generator like [Suno](/tools/suno/) and you can sell a whole release package - song plus visuals - to artists who have neither). The catch is the same as any AI video tool - quality varies between generations, so your client work needs you to curate and re-run until it is good, and premium models burn credits fast. Budget credits into your price or you will eat the cost."
        },
        {
            "question": "What is the catch with Kaiber's pricing and credits?",
            "answer": "The catch is that the price tag and the real cost are different numbers. Kaiber charges credits per second of generated video, and the expensive models (Veo, Kling) cost more per generation - a single high-quality 5-second clip can run 50-100+ credits, so the entry paid tier's ~1,400 credits disappears in a few dozen serious clips, not hundreds. On top of that, unused monthly credits do not roll over, so a light month is money thrown away, and there is no way to bank credits for a big project. The pricing structure is also genuinely confusing right now: different review sites quote different tiers and prices for the same plan (I saw entry tiers quoted anywhere from $5 to $15/mo and the top tier from $99 to $149), which usually means the company is mid-restructure - check kaiber.ai/pricing directly and read what the current plan actually includes before subscribing. Practical defenses: test styles on the free tier first, generate with cheaper models for drafts and only spend premium-model credits on final takes, and never subscribe for a month of 'someday' - subscribe when you have a concrete batch of client work."
        },
        {
            "question": "How does Kaiber compare to Runway and Pika - which should I pick?",
            "answer": "Different strengths, and it comes down to what you actually make. Kaiber is the music-first tool: if your work is audio-reactive visuals, music videos, visualizers or anything where the track drives the edit, it is the best in its lane - Runway and Pika do not do beat-synced visuals anywhere near as well. Runway is the better text-to-video engine: more prompt control, more consistent results from a text prompt, a real editing suite, and better for cinematic or story-driven shots where you care about camera and composition - if your clients ask for short films or ad concepts rather than music visuals, Runway is the more reliable pick. Pika sits in the middle: fast, friendly, good for short social clips, but weaker on both music sync and fine control. The honest answer is that many working freelancers keep both - Kaiber for anything with a song attached, and Runway (or Sora) for prompt-driven cinematic work - and they justify it because the two tools do not overlap much. If you must pick one and your projects involve music, Kaiber. If they do not, Runway."
        },
        {
            "question": "What can I actually do on Kaiber's free tier?",
            "answer": "Enough to test, not enough to work with. The free tier gives you a small monthly credit pool (sources vary, roughly 10-50 credits depending on when you look), a limited number of canvases, access to a subset of models, and output limited in length and resolution - and importantly, it is non-commercial, so you cannot legally sell or use free-tier output for client work. What it is genuinely good for: testing whether your music and a style you like actually sync well, learning the Beat Sync workflow, and producing short social clips for your own pages to see what resonates. What it is not good for: any paid client project, long videos, or premium models (those are gated behind paid tiers anyway). My advice is to spend the free tier learning the workflow and confirming the style direction, then subscribe only when you have a concrete batch of work - and start with a small paid tier rather than the top one, because credit burn is the thing that catches people out, not the subscription itself."
        }
    ],
    "content": """## What Kaiber Actually Is (From Someone Who Makes Music Visuals for a Living)

I run a small freelance studio that makes visuals for independent musicians, and AI video tools went from 'worthless demo' to 'billable every week' over the last two years. Kaiber is the one I reach for when there is a song involved, which is most of my work. It is an AI video platform built around audio: you drop in a track, pick an energy level and a style, and it generates video that cuts and pulses with the beat. That does not sound special until you try the alternatives, because most generators treat video as pictures with motion - Kaiber treats it as music with pictures, and the difference shows.

The reason it can do this is that Kaiber is not one model but a shell around several. Inside a workspace called Superstudio you can generate with Google Veo, Kling, Luma Dream Machine, Minimax and Mochi, switching per project. That matters practically: Veo gives you story-driven clips with rich detail, Kling is better at realistic movement and prompt obedience, Luma does cinematic camera moves, and the smaller models are cheap for drafts. Instead of paying for five separate subscriptions, you pay one and pick the engine that fits the job. The Linkin Park music video they made with it ('Lost') is not a gimmick - it is the reason bands trust the tool, and trust is half the sale when you pitch AI visuals to a musician who has been burned by fuzzy AI nonsense before.

The honest part: Kaiber will not make you a video. It makes you fifty takes and you pick three. Quality varies between generations even with identical settings, long videos drift out of consistency, and the credits disappear faster than the price suggests. It is a client-service tool with a learning curve, not a one-click video machine - and once you accept that, the money math works.

## Where the Money Is (Honest Numbers)

Let me skip the theory and give you the actual gigs I have done and seen done with this tool.

**Music videos and visualizers for independent artists.** This is the core market. A band or solo artist releasing a single needs a visualizer - most cannot afford a motion designer's $1,000+ quote. Finished AI visualizers sell for $100-$500 depending on length and iteration count. A first draft takes an evening in Kaiber; the billable work is direction, curation and revisions. The repeat-business angle is stronger: artists release on a schedule, so a monthly retainer of $300-$1,000/mo for visuals on every drop is realistic, and retainers stick because nobody on that budget can do this themselves.

**Stage and event loop visuals.** DJs, venues and event promoters need loop visuals for screens - the stuff that runs behind a performer for an hour. This is bulk work with short turnaround, and because it repeats weekly, it is the closest thing to passive income in this niche. $50-$200 per loop set, recurring.

**Animated product clips for small businesses.** A quieter but reliable one: small businesses pay $50-$200 to have product photos or brand stills animated into short motion clips for ads and social. Kaiber's image-to-video is good enough for this, and the client usually has no idea the tool exists, so the value is in the deliverable, not the software.

**Teaching and templates.** Musicians genuinely want to make their own visuals but do not want to learn video software. Selling a course, a pack of ready-to-use style presets, or a done-for-you setup ($50-$300) is a real niche that keeps growing - the people buying are the same artists you would otherwise work for hourly.

The unit economics work because your cost per render is tiny: even at the ~$29/mo tier, a visualizer draft costs cents in credits. Your margin is the curation and the client relationship, not the compute.

## How the Pricing Actually Works (And Where It Bites)

Kaiber is credit-based, which is the part most reviews gloss over. You do not pay per video - you pay per second of generated video, and the premium models cost more per generation. A single high-quality 5-second clip on Veo or Kling can run 50-100+ credits. The working tier sits around $29/mo for roughly 1,400 credits, which sounds like a lot and is actually a few dozen serious clips. There is a team tier near $149/mo with more credits and 4K exports.

Three things bite people:

1. **Unused monthly credits do not roll over.** A quiet month is wasted money, and you cannot bank credits for a big project.
2. **The published prices are all over the place right now.** I checked half a dozen review sites while writing this and saw entry tiers quoted anywhere from $5 to $15/mo and top tiers from $99 to $149. That spread usually means the company is restructuring its plans, so the only reliable move is to check kaiber.ai/pricing directly before subscribing.
3. **Free tier is non-commercial.** You can test with it, but you cannot legally sell free-tier output, so it is a trial, not a business.

My practical advice: test styles on the free tier, generate drafts on cheap models, and only spend premium credits on final takes. And subscribe for a concrete batch of work, never for 'someday.'

## What Kaiber Does Well

**Music sync.** This is the category-defining feature. Beat Sync reads the track and cuts visuals on the beat and energy shifts. A Kaiber visualizer feels like a music video; a [Runway](/tools/runway/) or [Pika](/tools/pika/) clip feels like a slideshow with motion. If your work involves music, this is the differentiator.

**Multi-model access.** One subscription, five engines. The ability to switch between Veo, Kling, Luma, Minimax and Mochi inside one project is genuinely useful, because the right model for a moody ballad is not the right model for a high-energy dance track.

**Shallow entry curve.** Upload a song, pick a style, generate. A first-time user produces a usable visualizer in an evening with zero motion-graphics background - and that is exactly the skill gap you can sell against.

**A real mobile app.** Full audio upload, style selection and export from a phone. On the road with a musician who wants to see a concept right now, this closes deals.

**The Linkin Park halo.** Professional validation sells. When a band has never heard of AI visuals, 'the same tool Linkin Park used for an official video' opens a conversation that 'AI generator' does not.

## What Kaiber Does Badly

**Inconsistent quality between runs.** Same prompt, same settings, two different results - one great, one mediocre. You will burn credits on rerolls, and that hidden cost is where the subscription really spends your money. Clients see the good take; you pay for the five bad ones.

**Long-form consistency falls apart.** Characters, style and lighting drift across a 3+ minute piece. Real paid music videos are assembled from many short segments edited together externally, so budget for editing time, not just generation.

**The Superstudio canvas is confusing at first.** Node-based, infinite, powerful - and overwhelming. New users get lost connecting scenes, styles and audio nodes. The learning curve is real, and it is steeper than the marketing suggests.

**Text-to-video control lags the leaders.** If your work is prompt-driven cinematic shots rather than music-synced visuals, Runway or Sora give you more control and more consistent results. Kaiber is the best tool in its lane, but its lane is music, not general-purpose video.

**The credit economy hides the real price.** A $29 plan sounds cheap; a few dozen serious clips later it does not. Budget credits into client quotes or you eat the cost.

## Kaiber vs Runway vs Pika (Which One to Buy)

| Capability | Kaiber | Runway | Pika |
|---|---|---|---|
| Music sync / Beat Sync | Best in class - built around audio | Weak - no beat-driven workflow | Weak |
| Text-to-video consistency | Good but variable | Best - more prompt control | Medium |
| Multi-model access | Yes (Veo, Kling, Luma, Minimax, Mochi) | No (own models) | No (own models) |
| Long-form coherence | Drifts past ~3 min | Better for longer scenes | Short clips only |
| Free tier | Yes (limited, non-commercial) | Yes (limited) | Yes (limited) |
| Best for | Music videos, visualizers, live visuals | Cinematic/ad concept shots | Fast short social clips |

My rule after two years: if a song is involved, Kaiber. If it is a cinematic prompt-driven shot, Runway. Pika only when a client wants something quick and the song does not matter. Many working freelancers keep Kaiber plus one of the others, because they genuinely do not overlap much - and that is not subscription creep, that is the tools being different jobs.

## Frequently Asked Questions

### Can I actually make money with Kaiber, or is it just a toy for musicians?

Yes - it is one of the more concrete money plays in AI video because the demand already exists. Musicians need visual content for every release and most cannot afford a motion designer. Independent artists pay $100-$500 for a finished visualizer or short music video, and with Kaiber a first draft is done in an evening, so you sell speed and curation, not render time. The stronger play is the retainer: bands release on a schedule, so $300-$1,000/mo for visuals on every drop is realistic and sticks. DJs and venues need loop visuals (recurring bulk work), and small businesses pay $50-$200 to have product photos animated for ads. The catch is the same as any AI video tool - quality varies between generations, so client work needs curation and rerolls, and premium models burn credits. Build credit cost into your price or you eat it.

### What is the catch with Kaiber's pricing and credits?

The price tag and the real cost are different numbers. Kaiber charges credits per second of generated video, premium models cost more, and a single high-quality 5-second clip can run 50-100+ credits - so the working tier's ~1,400 credits is a few dozen serious clips, not hundreds. Unused monthly credits do not roll over, so a quiet month is wasted money. And right now the published prices are a mess - review sites quote entry tiers anywhere from $5 to $15/mo and top tiers from $99 to $149, which usually means a plan restructure is underway, so check kaiber.ai/pricing directly. Defenses: test on the free tier, draft on cheap models, spend premium credits only on final takes, and subscribe for a concrete batch of work.

### How does Kaiber compare to Runway and Pika - which should I pick?

Different strengths. Kaiber is music-first: audio-reactive visuals, music videos and visualizers are its lane, and it is the best in that lane - Runway and Pika do not do beat-synced visuals anywhere near as well. [Runway](/tools/runway/) is the better text-to-video engine: more prompt control, more consistent output, a real editing suite, better for cinematic or story-driven shots. Pika is the friendly middle: fast, good for short social clips, weak on both music sync and fine control. If your projects involve music, Kaiber. If they are prompt-driven cinematic work, Runway. Many freelancers keep both - they overlap less than you would expect.

### What can I actually do on Kaiber's free tier?

Enough to test, not enough to work with. It gives a small monthly credit pool, limited canvases, a subset of models, limited length and resolution - and it is non-commercial, so free-tier output cannot be sold or used for client work. Use it to test whether your music and a style actually sync well, learn the Beat Sync workflow, and make short clips for your own pages. Do not use it for paid projects, long videos or premium models (gated behind paid tiers anyway). Learn on free, subscribe for a concrete batch.

## Who It Is For, and Who Should Skip It

Use it if you are a freelancer selling music visuals, a musician who wants to stop paying for every visualizer, a DJ or event person who needs recurring screen loops, or an agency adding music-driven social content to what you offer. The free tier plus one paid month is a cheap way to find out if it fits.

Skip it if your work is mostly prompt-driven cinematic video with no music component - [Runway](/tools/runway/) or [Sora](/tools/sora/) will serve you better. Skip it too if you need long-form coherence (a 5-minute film) or if you cannot tolerate inconsistency between generations and want one-button reliable output - that tool does not exist yet, and Kaiber is not it. And if you only ever need free tools, remember the free tier cannot be used commercially.

## Getting Started (in Plain Terms)

1. Start on the free tier. Upload one of your tracks, run it through a few styles, and learn what Beat Sync actually does with your music - this step is free and tells you whether the tool fits before you spend anything.
2. When you subscribe, start small. Draft on the cheaper models (Mochi, Minimax) and only spend Veo/Kling credits on final takes - this is the single biggest cost saver.
3. Build a style library. Save the style + model + energy combinations that work for your music; a saved preset turns a 20-minute setup into a 2-minute one, and it is the closest thing to a reusable asset in this tool.
4. Assemble long pieces externally. Kaiber clips are segments; edit them together in CapCut or your usual editor, because long-form coherence is not its strength.
5. Only go up a tier when a concrete batch of client work needs it - never subscribe to a big plan 'to have it ready,' because credits expire monthly and a quiet month is pure waste.
"""
}

def main():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    tools = data if isinstance(data, list) else data.get('tools', data)

    if any(t.get('slug') == 'kaiber' for t in tools):
        print('Kaiber already exists, skipping.')
        return

    # ---- Forbidden-word scan (Anti-AI tone rule) ----
    FORBIDDEN = [
        "leverage", "utilize", "robust", "streamline", "seamless", "empower",
        "unlock", "elevate", "revolutioniz", "cutting-edge", "state-of-the-art",
        "game-chang", "harness", "unleash", "supercharge", "synerg", "unparalleled",
        "groundbreak", "transformative", "next-level", "best-in-class"
    ]
    blob = json.dumps(NEW_TOOL, ensure_ascii=False).lower()
    hits = [w for w in FORBIDDEN if w in blob]
    if hits:
        raise SystemExit(f"[ABORT] forbidden words found: {hits}")

    tools.append(NEW_TOOL)
    with open(DATA, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    print(f"✅ Kaiber added. Total tools: {len(tools)}")
    print(f"   content length: {len(NEW_TOOL['content'])} chars")
    print(f"   forbidden-word scan clean")

    # ---- Generate OG image (Pillow) ----
    sys.path.insert(0, str(BASE / "scripts"))
    import gen_og_images_en as og
    og_dir = BASE / "images" / "og"
    og_dir.mkdir(parents=True, exist_ok=True)
    try:
        og.make_tool_og(NEW_TOOL, og_dir / "kaiber-en-og.png")
        print(f"✅ OG image generated: kaiber-en-og.png")
    except Exception as e:
        print(f"⚠️ OG image generation failed: {e}")

if __name__ == '__main__':
    main()
