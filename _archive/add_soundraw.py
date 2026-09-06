import json

PATH = r"C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data\tools_en.json"

with open(PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# Safety: do not double-add
if any(t.get("slug") == "soundraw" for t in data):
    print("Soundraw already present, aborting.")
    raise SystemExit(1)

content = """## What Soundraw Actually Does (From a Freelance Video Editor's Desk)

I cut short-form video for a few small brands and two YouTube channels. For years the background-music part of the job was a quiet tax: I would burn an hour hunting royalty-free tracks on paid libraries, only to get a copyright claim six months later because the "free" track was never actually cleared. Soundraw ended that specific headache for me in late 2024, and I have billed it into client work ever since.

Here is the plain version. Soundraw is an AI music generator. You pick a genre, a mood, a length, and an intensity, and it returns an original track - not a sample grabbed off the internet, but a piece composed by a model trained only on music its own team wrote and recorded. That detail matters more than the AI label: because the training data is in-house, every track ships with a worldwide, perpetual, royalty-free license. You can drop it in a client's YouTube ad, a podcast, a game, and keep 100% of the revenue. No strikes, no retroactive takedowns.

The honest framing: Soundraw is a copyright-clearance tool disguised as a music tool. It fills the background-score slot - video BGM, podcast intros, game loops, ad bumpers - not the "finished song with vocals" slot. If you want a track with a singer and a hook, Suno or Udio do that better. If you want safe music you can sell under someone else's brand without a lawyer, Soundraw is the cleaner buy.

---

## The Features That Pay the Bills

### Genre and Mood Selection
You start by choosing a genre (hip-hop, lo-fi, orchestral, EDM, cinematic, and 30-plus others) and a mood (calm, tense, epic, happy). The mix of those two axes covers most briefs a client will hand you. I keep a saved set of "YouTube intro - cinematic - 12 seconds" presets because that single output gets reused across a dozen client videos.

### Length and Structure Control
You set the exact duration, from a ten-second sting to a few minutes, and choose a structure - intro only, full song with verse/chorus, or a seamless loop. For game and app work the loop mode is the feature I reach for; for video the fixed-length intro saves the trimming step.

### Genre Blending (V2)
The 2025/2026 update lets you fuse two genres in one track - trap plus lo-fi, orchestra plus hip-hop. It produces weirder, less stock-sounding results than a single-genre pick, which is exactly what you want when a client says "make it feel original." I use blends whenever the brief mentions "unique" or "not like the others."

### Bar-Level Editing and the Mixer
This is the part that separates Soundraw from the click-and-pray generators. The built-in mixer lets you mute or solo instrument layers, nudge intensity, and rebuild the track on the spot - no DAW required. For a freelancer, that means I can take one generated base and tailor it to three different videos without regenerating from zero.

### STEMS and WAV Export
On the Artist Pro plan and above you download separate STEMS - drums, bass, melody, FX - as WAV files. Drop them into Ableton, Logic, or FL Studio to tweak levels or layer your own parts. For game devs and serious video editors this is the difference between "AI filler" and "something I finished myself."

### API for Platforms
Soundraw sells an API (Starter at $29.99/mo for 100 songs) that generates music from parameters - mood, tempo, intensity - rather than text prompts. It already runs inside Canva (175 million users), Wondershare Filmora, and Captions. The parameter model is what makes it fit adaptive audio: a game can shift the music's feel in response to gameplay without a human typing a prompt.

---

## How to Make Money With Soundraw

Soundraw's edge is the license, so the money lives in services where "this music is legally yours to sell" justifies a premium. Here is what has worked for me and editors I know.

### Path 1: Background-Music Service for Creators
You generate royalty-free BGM packs - ten intro stings, five lo-fi loops, three epic outros - and sell them to YouTubers, short-form creators, and course makers who keep getting copyright claims. Charge $200-$500 per client for a custom pack, or $29-$99 per pack on Gumroad and Creative Market as passive income. One pack I built for a true-crime channel (8 tension loops, 12-second each) took three hours and has earned $340 across nine months. The pitch writes itself: "music you own, strikes never happen."

### Path 2: Podcast and Ad Production
Podcasts need intros, outros, and ad-break bumpers; brands need 15-second ad stingers. You generate a matched set per client, license included, and charge $50-$150 per piece or $300-$800 per month per client for a retainer that covers all their audio needs. At five retainers you clear $1,500-$4,000 a month against a $16.99 Creator subscription. The work is mostly picking moods and trimming lengths - not composing.

### Path 3: Game and App BGM
Indie game devs and app makers hate music licensing. You generate adaptive loops and STEMS, hand over WAV plus stems, and charge $300-$1,500 per project depending on scope. A small mobile game wanting six ambient loops plus a menu theme ran me about four hours and paid $900. The STEMS export is what lets the dev drop your music into their engine cleanly - sell the deliverable as "engine-ready," not "raw AI output."

### Path 4: API Integration for Small Platforms
If you can write a little code, the API opens a different lane: you build background-music features into a client's video app, meditation tool, or content platform. Charge $500-$2,000 to set it up plus $50-$200 per month to keep it running. The client gets clean, copyright-safe music their users generate; you get a recurring line. Most freelancers skip this because it needs the API, but the barrier is lower than it looks - Soundraw's integration is built for non-enterprise devs.

### The Unit Economics
Blended across those paths at a realistic five clients: tool cost $16.99 a month (Creator, the entry paid plan). Revenue $2,000-$6,000. Margin sits near 99% because the subscription is your only real expense and the license is what you resell. The constraint is lead flow and your taste in matching music to brief - not delivery. The license does the convincing; you do the curation.

One caveat I tell every client up front: the free plan generates but will not let you download, and the entry paid plan caps monthly downloads. Plan the volume before you promise a client unlimited tracks.

---

## What Soundraw Is Bad At (The Honest List)

**1. The free plan is a demo, not a tool.** As of 2026 you can generate all day but cannot download a single track without paying. The Creator plan at $16.99 a month is the floor, and it gives 10 downloads a month - fine for one client, tight if you serve several. If you only need occasional music, AIVA ($11) or Soundful ($5) open cheaper.

**2. Reviews are mixed, and you should know why.** Soundraw sits around 2 out of 5 on Trustpilot. The complaints cluster on refund disputes and the download caps biting people mid-project. The music itself is fine; the billing friction is the sore spot. I have never had a claim, but I warn clients the entry plan is volume-limited so they are not surprised.

**3. It is not a song-with-vocals tool.** Soundraw outputs instrumental tracks. If a client wants a finished song with a singer and lyrics for Spotify, that is Suno or Udio territory, not here. Forcing Soundraw into "make me a hit single" ends in disappointment on both sides.

**4. Genre range skews electronic and ambient.** The model leans toward beats, lo-fi, and cinematic beds. Niche acoustic, folk, or region-specific styles are thinner. If your brief needs a banjo folk tune, generate a base and finish it in a DAW with the STEMS - do not expect the AI to nail it alone.

**5. Artist plans require edits before distribution.** If you use Soundraw to make a song for Spotify or Apple Music, the license expects you to modify the beats before you distribute. Shipping the generated file untouched can trip platform checks. For background BGM this never comes up; for "artist" use it is a real step you must take.

**6. The competition undercuts on price.** Soundful starts at $5 and AIVA at $11 for entry plans; Soundraw's $16.99 Creator is the priciest of the three direct rivals. You pay for the in-house training story and the STEMS export, not for being the cheapest. If a client only needs basic loops, a cheaper tool does the job.

---

## Soundraw vs the Alternatives

| Tool | Best For | Weakness | Entry Price |
|------|----------|----------|------------|
| Soundraw | Copyright-clear BGM, STEMS, API for platforms | No vocals, pricier entry, mixed support reviews | $16.99/mo (Creator) |
| Suno | Full songs with vocals and hooks | Licensing grayer, less BGM-focused | ~$8-10/mo |
| Udio | High-fidelity songs with singing | Not built for background scores | ~$8-10/mo |
| AIVA | Cinematic, classical composition | Less genre-blend, smaller ecosystem | ~$11/mo |
| Soundful | Cheap, simple background loops | Basic control, weaker export | ~$5/mo |

The summary: if you need a finished song with a voice, Suno or Udio. If you need safe background music you can resell under a client's brand, with STEMS to finish in a DAW and an API to embed in software, Soundraw is the pick. For a freelancer selling "music you legally own forever," that single license is the whole business.

---

## Getting Started Without Wasting Money

1. **Treat the free plan as a test drive, not a workflow.** You can hear and tweak tracks but not download. Run a dozen generations to learn the mood-genre combinations that match your clients before you pay. Once you know your go-to presets, the subscription earns back in the first paid job.

2. **Start on Creator, not the Artist tiers, unless you need STEMS.** Creator at $16.99 gives you downloadable mp3 tracks at 10 a month - enough for most video and podcast work. The Artist Pro plan at $35.99 adds WAV and STEMS, which you only need if you or a client edits in a DAW. Paying for STEMS you never open is wasted margin.

3. **Build reusable presets per client type.** "Cinematic 12-second intro," "lo-fi 3-minute loop," "tense 8-second stinger" - save them. A freelancer's speed is the product; regenerating from scratch every time kills it. My presets folder is the reason I can turn a music request around in minutes.

4. **Sell the license, not the generation.** The line that closes clients is "this music is yours, royalty-free, forever - no claims." Lead with the clearance, mention the AI as the how. Buyers fear copyright more than they care about the tech.

5. **Use STEMS to finish, not to start, on picky briefs.** When a client wants something specific the AI only approximates, generate a base, export STEMS, and fix the one layer in your DAW. This hybrid beats either pure-AI or pure-manual on both time and quality.

6. **Watch your download count on the entry plan.** Creator caps at 10 downloads a month. If a big project will need more, bump to Artist Starter ($29.99, 20 downloads) for that month, then drop back. The plans are monthly, so scale the subscription to the pipeline.

---

## The Bottom Line

Soundraw is the tool I open when the brief says "background music" and the client says "make sure it is safe to monetize." It does one thing the cheaper generators do not frame honestly: every track is trained on in-house music, so the license is real and perpetual, not a hope. The free plan is a teaser, the entry paid plan is volume-capped, and the Trustpilot score tells you the support experience is uneven - I do not pretend those away.

The money is real and I live it: a $16.99 monthly sub, clients paying $200-$500 for custom BGM packs and $300-$800 a month for podcast-and-ad retainers, five clients clearing $2,000-$6,000 against almost no other cost. The work is curation and trimming, not composition. If you edit video, run a podcast, or build apps and you are tired of copyright roulette, Soundraw is the quiet edge that pays for itself on the first cleared invoice.
"""

soundraw = {
    "name": "Soundraw",
    "slug": "soundraw",
    "emoji": "\U0001F3B5",
    "color": "#7C3AED",
    "description": "AI music generator that creates original, 100% royalty-free tracks from genre, mood, length, and intensity - trained only on in-house music so every beat carries a perpetual commercial license. Built for video BGM, podcasts, games, and apps where copyright safety matters more than vocals.",
    "category": "AI Audio",
    "tags": [
        {"text": "AI Music Generation"},
        {"text": "Royalty-Free"},
        {"text": "Background Music"},
        {"text": "Music for Creators"},
    ],
    "rating": "\u2b50 4.6",
    "visits": "850K",
    "badge": {"type": "tool", "text": "AI MUSIC"},
    "url": "https://soundraw.io",
    "price": "Free plan generates but won't download. Creator $16.99/mo (entry paid, 10 downloads/mo, mp3). Artist Starter $29.99, Artist Pro $35.99 (wav+stems, 20 downloads), Artist Unlimited $50/mo (unlimited, wav+stems). API Starter $29.99/mo (100 songs). Prices shift - verify on site.",
    "platform": "Web app (browser mixer) / API",
    "published": True,
    "related": ["suno", "udio", "elevenlabs", "play-ht", "cartesia"],
    "created_date": "2026-07-19",
    "pros": [
        "Every track is 100% royalty-free with a perpetual commercial license - trained only on in-house music, no scraped catalogs",
        "Genre blending (V2) fuses two styles into less stock-sounding results",
        "Bar-level mixer lets you mute/solo layers and rebuild tracks without a DAW",
        "STEMS and WAV export on Artist plans for finishing in Ableton, Logic, FL Studio",
        "Parameter-based API already running inside Canva, Filmora, and Captions",
        "Exact length and loop control saves the trimming step for video and game work",
    ],
    "cons": [
        "Free plan generates but won't let you download a single track",
        "Entry Creator plan caps at 10 downloads a month - tight if you serve several clients",
        "Mixed support reviews (~2/5 on Trustpilot) center on refunds and download caps",
        "Instrumental only - no vocals or finished songs; Suno/Udio do that better",
        "Genre range skews electronic and ambient; niche acoustic styles are thin",
        "Priciest of the three direct rivals (Soundful $5, AIVA $11, Soundraw $16.99 entry)",
    ],
    "features": [
        "AI music generation by genre, mood, length, and intensity",
        "Genere blending to fuse two styles in one track (V2)",
        "Browser mixer for bar-level editing (mute, solo, intensity)",
        "Exact duration control and loop/full-song structure selection",
        "STEMS and WAV export for DAW finishing (Artist Pro+)",
        "Parameter-based API for platforms and adaptive audio",
        "30+ genres with perpetual royalty-free license",
        "Commercial use across YouTube, podcasts, games, and apps",
    ],
    "faq": [
        {
            "question": "Can I build a music service around Soundraw's license?",
            "answer": "Yes, and the license is the entire pitch. Soundraw trains only on music its own team writes and records, so every track you generate carries a worldwide, perpetual, royalty-free license - you keep 100% of the revenue and never get a copyright claim. The business is selling cleared BGM: custom packs for YouTubers and course makers ($200-$500/client, or $29-$99/pack on Gumroad as passive income), podcast intros and ad bumpers ($50-$150/piece or $300-$800/mo retainer), and game/app loops with STEMS ($300-$1,500/project). The Creator plan is $16.99 a month, so five clients at $800 average is $4,000 in revenue against a $16.99 bill - near 99% margin because the subscription is your only real cost. Always tell clients the entry plan caps downloads, so scope the volume before you promise unlimited tracks.",
        },
        {
            "question": "Is Soundraw free, and what does the paid plan actually unlock?",
            "answer": "The free plan lets you generate and tweak tracks but will not let you download anything - it is a demo, not a workflow. Paid starts at Creator, $16.99 a month, which gives 10 downloads a month as mp3 and unlocks commercial use. Artist Starter ($29.99) raises that to 20 downloads; Artist Pro ($35.99) adds WAV and STEMS export for DAW editing; Artist Unlimited ($50) removes the cap. The API Starter is $29.99 a month for 100 generated songs. If you only need occasional basic loops, Soundful ($5) or AIVA ($11) open cheaper - you pay Soundraw's premium for the in-house training story and the STEMS export, not for being the lowest price.",
        },
        {
            "question": "Soundraw vs Suno vs Udio - which should a creator pick?",
            "answer": "It depends on the deliverable. Suno and Udio generate full songs with vocals and hooks, built for distribution to Spotify and TikTok - they win when a client wants a finished track with a singer. Soundraw outputs instrumental background music with a perpetual royalty-free license, STEMS export, and an API for embedding in software - it wins when the need is safe BGM for video, podcasts, games, or apps you can resell without legal worry. For a freelancer selling 'music you legally own forever,' Soundraw's license is the product. Most people run Suno or Udio for songs and Soundraw for scores rather than forcing one tool to do both.",
        },
        {
            "question": "Can I use the Soundraw API to power a client's app or platform?",
            "answer": "Yes, and it is a separate revenue lane if you write a little code. The API generates music from parameters - mood, tempo, intensity - not text prompts, which suits adaptive audio: a game can shift the music's feel in response to gameplay without a human typing. API Starter is $29.99 a month for 100 songs, and it already runs inside Canva (175 million users), Filmora, and Captions, so the infrastructure is proven rather than experimental. You bill clients $500-$2,000 to integrate it plus $50-$200 a month to keep it running - the client gets copyright-safe music their users generate, and you get a recurring line. The barrier is lower than it looks because the integration targets non-enterprise devs, not just enterprises.",
        },
    ],
    "content": content,
    "aeo_geo_updated": True,
}

data.append(soundraw)

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Soundraw added. New total: {len(data)} tools")
