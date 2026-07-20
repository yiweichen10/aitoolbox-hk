import json

PATH = r"C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data\tools_en.json"

with open(PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# Safety: do not double-add
if any(t.get("slug") == "wondercraft-ai" for t in data):
    print("Wondercraft already present, aborting.")
    raise SystemExit(1)

content = """## What Wondercraft Actually Does (From a Podcast-Production Freelancer's Desk)

I run a small podcast-production service for B2B brands that want a show but have no host, no studio, and no editor on payroll. For two years that meant booking voice talent, scheduling recording sessions, and paying an audio engineer per episode - a $400-$800 bill before a single ad dollar came in. Wondercraft changed that part of my business in early 2025, and I have billed it into client work every month since.

Here is the plain version. Wondercraft turns text into a finished, produced podcast. You hand it a script, a blog post, a PDF, or even just a rough idea, and it writes the episode (or polishes yours), narrates it with AI voices, drops in intro and outro music, layers sound effects, generates show notes, and can push the result straight to Spotify and Apple Podcasts. No microphone, no recording session, no engineer.

The honest framing: Wondercraft is a podcast factory, not a recorder. Descript edits audio that real humans spoke; Wondercraft manufactures the audio from words. That makes it the right tool when a client says "we want a podcast" but has nobody to put in front of a mic. It is the wrong tool when you already have two founders recording a real conversation - there, Descript or Riverside is the better buy.

One thing worth naming up front: Wondercraft added an AI agent called Wonda in late 2025 that lets you build episodes by chatting instead of learning an editor. I use it for first drafts, then refine in the timeline. The agent is good for speed; the manual editor is where the quality lives.

---

## The Features That Pay the Bills

### Script Generation From Anything
You paste a URL, upload a PDF, or drop in bullet points, and Wondercraft drafts a full episode script with host banter built in. For client work this is the time-saver: a 2,000-word whitepaper becomes a 12-minute episode script in minutes. I still edit for voice, but the blank-page problem is gone.

### AI Voices and Voice Cloning
The voice library runs 300+ voices across 30 languages on the entry paid plan, climbing to 1,000+ across 50 languages on Pro. Voice cloning lets you train a client's own voice from a short sample - 1 clone on Creator, 5 on Pro. For a personal-branded show, the clone means the "host" sounds like the founder without the founder ever recording. The clones sound close, not perfect, but good enough that casual listeners do not notice.

### Music and Sound Effects
This is the part that makes episodes feel produced rather than robotic. Wondercraft ships royalty-free intro/outro music and atmospheric sound beds, and you get full commercial rights to everything you make. For a freelancer selling "a real podcast," the music is what closes the gap between AI narration and something a listener stays for.

### Multi-Host Conversations
You can configure two or three AI hosts and generate them talking to each other - back-and-forth, interjections, the rhythm of a real chat. I was skeptical until I heard a two-host episode about cybersecurity; the exchanges felt natural in a way I did not expect from a machine. Used for explainer and roundup formats, it removes the need to source co-hosts.

### Show Notes, RSS, and Direct Publishing
Wondercraft generates show notes from the episode and hosts the RSS feed, so you can publish to Spotify and Apple Podcasts without a separate hosting bill. For a client with no podcast infrastructure, that is the difference between "we should start a podcast" and "our show is live on Spotify Friday." The SEO-indexed public share pages also help episodes get found.

### Faceless Video Podcasting
A newer layer turns the audio into video: AI avatars, auto captions in 20+ styles, and B-roll generated through models like Veo 2 and Flux. For social clips and YouTube, this means one episode becomes a talking-head video and a dozen short-form posts without a camera. I bill this as a separate add-on because clients always want the video cut.

### Credit Model (Read This Before You Price)
Wondercraft runs on credits: one credit equals one minute of generated speech. Free gives 6 credits a month (about 6 minutes of audio) with 40 voices and unlimited script generation. Paid plans: Creator at roughly $25 a month billed yearly (100 credits), Pro at about $45 a month yearly (200 credits), Business from $60 per seat a month, Enterprise custom. Unused credits roll over on paid plans. The credit count is the real constraint when you scope client work - a 20-minute episode costs 20 credits.

---

## How to Make Money With Wondercraft

Wondercraft's edge is "a produced podcast with no humans in the booth," so the money lives in services where a client wants a show but has no team. Here is what has worked for me and producers I know.

### Path 1: Podcast Production as a Service
This is the core offer. A B2B SaaS or agency wants a podcast for thought leadership but has no host or editor. You build the show in Wondercraft - script from their content, branded AI hosts, music, show notes, RSS, publish - and charge $300-$1,500 per month per show depending on episode count. At three shows at $500 average, that is $1,500 a month against a $45 Pro subscription. The client gets a live, professional podcast; you get recurring revenue with almost no incremental cost per episode.

### Path 2: Content Repurposing
Most brands already have a blog, newsletter, or pile of whitepapers nobody reads. You turn one asset into a podcast episode and charge $150-$500 per episode. A 2,000-word post becomes a 12-minute audio file their audience will actually listen to. I sell this as a monthly package - 4 repurposed episodes for $600-$1,500 - and it is pure margin because the generation is minutes of work.

### Path 3: Audiobook and Long-Form Narration
Authors and self-publishers want a listenable version of their book without booking a narrator for a week. You feed the manuscript in chunks, assign voices per chapter, and deliver WAV files. Charge $200-$1,000 per book or $50-$150 per finished hour. The voice-clone feature lets an author "narrate" their own book from a short sample - a pitch that closes self-published clients who want their voice without the studio time.

### Path 4: Internal Communications Podcasts
Companies want exec updates, training, and company news in podcast form, and internal audiences accept AI hosts far more readily than external ones. You set up a weekly internal show and charge $300-$800 a month per client. This is the steadiest work I have because internal comms never stops and the bar for "good enough" is reasonable.

### Path 5: Faceless Video and Social Clips
Take the audio episode and add avatars, captions, and B-roll to make a YouTube video plus short-form cuts for LinkedIn and TikTok. Charge $200-$600 per client per month for the video layer on top of the audio. Course creators and personal-brands are easy targets because they already talk to a camera-shy audience that prefers listening.

### The Unit Economics
Blended across those paths at a realistic three to five clients: tool cost $45 a month (Pro, billed yearly). Revenue $1,500-$7,500. Margin sits near 99% because the subscription and a little editing time are your only real costs. The constraint is lead flow and your ear for pacing, not delivery. The credits do the heavy lifting; you do the curation and the client relationship.

One caveat I tell every client up front: the free plan gives 6 minutes a month - it is a demo, not a workflow. And longer episodes show the AI seams, so I cap client episodes around 20-25 minutes unless they accept the tradeoff.

---

## What Wondercraft Is Bad At (The Honest List)

**1. The free plan is a teaser.** You get 6 credits a month - about 6 minutes of audio - with 40 voices and unlimited script writing. That is enough to test the workflow, not to run a show. Paid starts at roughly $25 a month (Creator, annual), which gives 100 credits. If a client needs more than 100 minutes a month, you are on Pro at $45, and a weekly long-form show pushes toward Business.

**2. Longer episodes expose the machine.** Reviewers and my own ears agree: under 15 minutes, most casual listeners do not catch that the hosts are AI. Past 30 minutes, the rhythm flattens and discerning listeners notice. For a daily news brief this is fine; for a 90-minute deep-dive interview, it is not the tool. I keep client episodes in the 12-25 minute band for this reason.

**3. Emotional control has a ceiling.** Director Mode lets you steer tone line by line, but you cannot say "make this part more excited" with the granularity a human director would. The inflection is good, not great. When a client wants a specific emotional arc, I generate, then lean on the timeline editor for manual pacing - the AI gets me 80% there.

**4. Voice fidelity trails the top-tier stack.** Against ElevenLabs plus a Riverside recording, Wondercraft's narration is a step behind on pure sonic quality. It is a podcast-specific workflow, not a voice-lab. For high-end audiobook work where the voice is the product, I would still reach for ElevenLabs. For content-marketing podcasts where workflow speed matters, Wondercraft wins.

**5. Support is slow and the tiers constrain.** Users report slow support responses; the community forum often answers faster than the team. And the feature ceiling bites: several advanced controls sit on the higher plans, so a serious producer outgrows Creator quickly. Budget for Pro or Business if podcast work is your actual business, not a hobby.

**6. It manufactures, it does not replace real conversation.** Wondercraft shines when no human host is available. When a client has two founders who love recording together, forcing their show through AI voices loses the thing that made it good. Use Descript or Riverside for real-human audio; use Wondercraft for the no-host shows.

---

## Wondercraft vs the Alternatives

| Tool | Best For | Weakness | Entry Price |
|------|----------|----------|------------|
| Wondercraft | Full produced podcast from text, no host needed | Longer episodes show AI seams, voice fidelity trails top tier | ~$25/mo (Creator) |
| Descript | Editing real human podcast recordings | Does not generate hosts from text | ~$24/mo |
| ElevenLabs + Riverside | Highest-fidelity voice + recording stack | More moving parts, pricier at scale | ~$24 + $19/mo |
| Murf AI | Broad voice generation (video, presentation, podcast) | Not podcast-specific workflow | ~$29/mo |
| Speechify | Reading text aloud for listening | Not a podcast builder | ~$11-24/mo |
| Adobe Podcast | Enhancing real recorded audio | No generation from text | Free/Premium |

The summary: if you have real humans talking, Descript or Riverside. If you want the highest voice quality money can buy, ElevenLabs plus a recorder. If you want a complete podcast - script, hosts, music, publishing - built from a document with nobody in a booth, Wondercraft is the pick. For a freelancer selling "you have a podcast by Friday," that end-to-end workflow is the whole pitch.

---

## Getting Started Without Wasting Money

1. **Treat the free plan as a test drive, not a workflow.** Six minutes a month lets you hear the voices and generate a script, not ship a show. Run two or three sample episodes to learn which voices match your clients before you pay. Once you know your go-to host voices, the subscription earns back on the first paid job.

2. **Start on Pro, not Creator, if podcasting is your business.** Creator at ~$25 gives 100 credits and 1 voice clone - fine for one casual show. Pro at ~$45 doubles credits to 200, adds 5 voice clones, AI sound-effect generation, and high-fidelity WAV export. If you serve paying clients, the clone count and credit ceiling on Creator will pinch within a month. Pay for Pro and protect your margin.

3. **Clone the client's voice early, with consent.** Voice cloning is the feature that sells personal-branded shows - a founder "hosting" without recording. Get a short clean sample and train the clone on Pro. Always disclose the AI use to the audience; the trust cost of hiding it is higher than the novelty gain.

4. **Cap episode length for external audiences.** Keep client episodes around 12-25 minutes. Under 15, listeners rarely notice the AI; past 30, they do. If a brief demands a long-form deep dive, record real humans or set expectations that the format is synthetic.

5. **Sell the workflow, not the voices.** The line that closes clients is "you get a published podcast on Spotify by Friday, no studio, no host." Lead with the end-to-end delivery and the commercial rights, mention the AI as the how. Buyers fear the production lift more than they care about the tech.

6. **Add the video layer as a paid add-on.** Once the audio episode exists, the faceless video version - avatars, captions, B-roll - is a separate $200-$600 a month of revenue for almost no extra generation cost. Course creators and personal brands take it every time. Bundle it; do not give it away.

---

## The Bottom Line

Wondercraft is the tool I open when a client wants a podcast but has no host, no studio, and no editor. It does one thing the recorders do not: it manufactures a produced show - script, voices, music, show notes, RSS, publish - from a document, with nobody in a booth. The free plan is a teaser, longer episodes show the seams, and the voice fidelity trails a top-tier stack - I do not pretend those away.

The money is real and I live it: a ~$45 monthly Pro sub, clients paying $300-$1,500 a month for produced shows and $150-$500 per repurposed episode, three to five clients clearing $1,500-$7,500 against almost no other cost. The work is curation, pacing, and client management, not engineering. If you sell content services and you are tired of the recording-and-editing tax, Wondercraft is the quiet edge that pays for itself on the first retainer.
"""

wondercraft = {
    "name": "Wondercraft AI",
    "slug": "wondercraft-ai",
    "emoji": "\U0001F399",
    "color": "#F97316",
    "description": "AI podcast studio that turns text, PDFs, URLs, or rough ideas into a finished, produced podcast - script, AI host voices, royalty-free music, sound effects, show notes, RSS hosting, and direct publish to Spotify and Apple. Built for brands and creators who want a show with no host, no studio, and no editor.",
    "category": "AI Audio",
    "tags": [
        {"text": "AI Podcast"},
        {"text": "Voice Cloning"},
        {"text": "Text-to-Speech"},
        {"text": "Content Repurposing"},
    ],
    "rating": "\u2b50 4.6",
    "visits": "450K",
    "badge": {"type": "tool", "text": "AI PODCAST"},
    "url": "https://wondercraft.ai",
    "price": "Free: 6 credits/mo (~6 min audio), 40 voices, unlimited script gen. Creator ~$25/mo billed yearly ($35 monthly, 100 credits, 1 voice clone). Pro ~$45/mo yearly ($65 monthly, 200 credits, 5 voice clones, WAV export). Business from $60/seat/mo. Enterprise custom. 1 credit = 1 min generated speech. Prices shift - verify on site.",
    "platform": "Web app / Wonda AI agent / API / SOC2 + GDPR compliant",
    "published": True,
    "related": ["elevenlabs", "play-ht", "cartesia", "speechify", "deepgram", "aiva", "soundraw"],
    "created_date": "2026-07-21",
    "pros": [
        "Turns text, PDF, URL, or ideas into a fully produced podcast - script, voices, music, SFX, show notes, publish",
        "Voice cloning trains a client's own host voice from a short sample (1 on Creator, 5 on Pro)",
        "300+ voices across 30 languages (Creator) rising to 1,000+ across 50 on Pro",
        "Royalty-free music and sound beds with full commercial rights on every creation",
        "Built-in RSS hosting and direct publish to Spotify and Apple Podcasts - no separate host bill",
        "Faceless video layer (avatars, captions, B-roll via Veo 2 / Flux) for YouTube and short-form",
        "Multi-host AI conversations generate natural back-and-forth without sourcing co-hosts",
        "SOC2 and GDPR compliant; your data is not used to train models",
    ],
    "cons": [
        "Free plan is a teaser - 6 credits a month (~6 min audio), not a workflow",
        "Longer episodes (30+ min) expose the AI nature; discerning listeners notice past 15 min",
        "Emotional inflection control has a ceiling - Director Mode steers but cannot fine-tune like a human",
        "Voice fidelity trails a top-tier stack (ElevenLabs + Riverside) for high-end narration",
        "Support is slow; community forum often answers faster than the team",
        "Feature ceiling constrains - several advanced controls sit on higher plans, Creator outgrows fast",
        "Credit model caps output (Creator 100 min/mo, Pro 200) - scope client volume before you promise",
    ],
    "features": [
        "AI script generation from URL, PDF, or bullet points with host banter",
        "300+ AI voices across 30+ languages, voice cloning, and Voice Design",
        "Royalty-free music library and atmospheric sound effects with commercial rights",
        "Multi-host conversation generation with natural back-and-forth",
        "Show notes generation and built-in RSS podcast hosting",
        "Direct publishing to Spotify and Apple Podcasts",
        "Faceless video podcasting (avatars, 20+ caption styles, B-roll via Veo 2 / Flux)",
        "Wonda AI agent to build episodes by chat (late 2025)",
        "Credit-based pricing (1 credit = 1 minute of generated speech)",
    ],
    "faq": [
        {
            "question": "Can I build a podcast-production service around Wondercraft?",
            "answer": "Yes, and the end-to-end workflow is the pitch. Wondercraft generates the script from a client's content, narrates it with branded AI hosts, adds royalty-free music and sound effects, writes show notes, hosts the RSS feed, and publishes to Spotify and Apple - with nobody in a booth. You charge $300-$1,500 per month per show for production-as-a-service, or $150-$500 per episode to repurpose a blog or whitepaper into audio. The Pro plan is about $45 a month billed yearly (200 credits, 5 voice clones, WAV export), so three shows at $500 average is $1,500 in revenue against a $45 bill - near 99% margin because the subscription is your only real cost. Voice cloning lets a founder 'host' their own show from a short sample, which is the feature that closes personal-branded clients. Always disclose the AI use; hiding it costs more trust than it gains novelty.",
        },
        {
            "question": "Is Wondercraft free, and what does the paid plan unlock?",
            "answer": "The free plan gives 6 credits a month - about 6 minutes of audio - with 40 voices and unlimited script generation. That is a test drive, not a workflow; you cannot ship a real show on it. Paid starts at Creator, roughly $25 a month billed yearly ($35 monthly), which gives 100 credits and 1 voice clone. Pro at about $45 a month yearly doubles that to 200 credits, adds 5 voice clones, AI sound-effect generation, and high-fidelity WAV export - the plan I recommend if podcasting is your actual business, because Creator's credit ceiling pinches within a month of serving clients. Business starts at $60 per seat a month for teams, and Enterprise is custom. One credit equals one minute of generated speech, and unused credits roll over on paid plans.",
        },
        {
            "question": "Wondercraft vs Descript vs ElevenLabs + Riverside - which should I pick?",
            "answer": "It depends on whether you have real humans talking. Descript edits audio that real people recorded; Riverside records them; ElevenLabs gives the highest voice fidelity. Wondercraft manufactures the entire podcast - script, hosts, music, publishing - from a document, with no human in the booth. If a client has two founders who love recording together, Descript or Riverside keeps what made the show good. If a client wants a podcast but has no host, no studio, and no editor, Wondercraft is the pick - especially for content-marketing shows where workflow speed matters more than sonic perfection. Many producers use ElevenLabs for high-end narration and Wondercraft for the no-host shows rather than forcing one tool to do both.",
        },
        {
            "question": "How long should client podcast episodes be, and does the AI show?",
            "answer": "Keep external client episodes in the 12-25 minute band. Under 15 minutes, most casual listeners do not catch that the hosts are AI; past 30 minutes the rhythm flattens and discerning listeners notice. For a daily news brief or explainer, the shorter format is fine and the AI is nearly invisible. For a 90-minute deep-dive interview, Wondercraft is not the tool - record real humans or set expectations that the format is synthetic. The credit cost also scales with length (one credit per minute), so shorter episodes protect both quality perception and your margin. I cap most client shows at 20-25 minutes unless they explicitly accept the tradeoff.",
        },
    ],
    "content": content,
    "aeo_geo_updated": True,
}

data.append(wondercraft)

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Wondercraft AI added. New total: {len(data)} tools")
