# -*- coding: utf-8 -*-
"""Append article #225 (Speech-to-Text API Pricing) to data/articles_en.json with self-checks.
Pricing verified from official pages on 2026-11-18:
- Deepgram pricing page (promo table + FAQ + Growth terms)
- AssemblyAI pricing page (STT-3.7 / Universal-2) + official docs model table (streaming) + Nov 4 2026 cost guide
- OpenAI developers pricing page (transcription section)
- ElevenLabs speech-to-text product page (API $0.20/hr, credits 30k=1h31m etc.) + docs + third-party trackers
"""
import json, re, sys

ART = {
    "title": "Speech-to-Text API Pricing in 2026: Deepgram vs AssemblyAI vs OpenAI vs ElevenLabs Compared",
    "slug": "best-speech-to-text-api-pricing-2026-deepgram-vs-assemblyai-vs-openai-vs-elevenlabs",
    "date": "2026-11-18",
    "category": "AI Infrastructure",
    "description": "Deepgram, AssemblyAI, OpenAI and ElevenLabs rate cards, worked bills from 10 to 10,000 hours, and the session-time and credit traps behind the real bill.",
    "keywords": "speech-to-text api pricing,deepgram pricing,deepgram nova-3 pricing,assemblyai pricing,openai whisper api pricing,elevenlabs scribe pricing,cheapest speech-to-text api,real-time transcription pricing,speech-to-text api free tier,speech-to-text api cost per hour,gpt-4o-transcribe pricing",
    "content": """Transcribing 1,000 hours of recorded audio this month costs $150 on AssemblyAI, $180 on OpenAI's cheapest transcriber, $200 on ElevenLabs Scribe v3, and $252 on Deepgram Nova-3 — a spread of barely 1.7x between four flagship models. The 600x spread between LLM inference platforms makes this market look like what it has become: a commodity. Speech-to-text API pricing has collapsed toward commodity rates, which means the rate card is no longer where the money goes. The real bill now hides in four places: streaming sessions that bill dead air, add-ons priced per minute, multichannel audio billed per channel, and a credit system at ElevenLabs that works out to roughly 18 times the API rate for the same transcription. This piece walks through each rate card as published on November 18, 2026, runs identical workloads through all four meters, and marks where each vendor wins.

## Speech-to-Text API Pricing at a Glance

One warning: these vendors meter different things — per second of audio, per minute of connection, per hour of WebSocket session, per credit — so every figure below is converted to dollars per hour of audio. Speech-to-text API cost per hour is the number your invoice converges on, whatever the rate card says.

| Provider and model | Pre-recorded | Streaming | What the meter runs on | Free tier |
|---|---|---|---|---|
| AssemblyAI Universal-2 | $0.15/hr | $0.15/hr (Universal-Streaming) | seconds of audio (batch) / session duration (streaming) | 185 hrs batch + 333 hrs streaming |
| AssemblyAI STT-3.7 | $0.21/hr | $0.30/hr ($0.45 agent tier) | audio duration / session duration | same pool |
| Deepgram Nova-3 (promo rates) | $0.252/hr | $0.288/hr | every second, no block rounding | $200 credit, no expiry |
| OpenAI gpt-4o-mini-transcribe | $0.18/hr | $1.02/hr (live models) | per-minute estimate on token billing | none for transcription |
| OpenAI gpt-4o-transcribe-diarize | $0.36/hr | — | per-minute estimate | none |
| ElevenLabs Scribe v3 / v3 Live | $0.20/hr | $0.22/hr | every second of audio sent, silence included | ~12 min/mo on the Free plan |

If you want the consumer side of this market — meeting note-takers with apps and per-seat pricing — that is a different product with a different price curve, covered in the [transcription tools roundup](/articles/best-ai-transcription-tools-2026-fireflies-vs-otter-vs-krisp-vs-fathom-vs-tldv). Everything below is the raw developer API.

## Deepgram Pricing: Per-Second Meters and a $200 Head Start

Deepgram's card, as published on November 18, 2026, runs promo rates: Nova-3 monolingual transcribes pre-recorded audio at $0.0042 per minute (marked "was $0.0065") and streams at $0.0048 per minute (was $0.0077). Multilingual Nova-3 sits at $0.0050 pre-recorded and $0.0058 streaming. Flux, the streaming model built for voice agents, runs $0.0065 per minute in English and $0.0078 multilingual. Converted to hours: $0.252 pre-recorded, $0.288 streaming, $0.39 on Flux.

Deepgram Nova-3 pricing therefore lands between OpenAI's two mid-tier transcribers — cheaper per hour than gpt-transcribe ($0.27), dearer than gpt-4o-mini-transcribe ($0.18) — with two things no rival matches. First, billing runs per second with no block rounding, so a 14-second clip bills as 14 seconds. Second, the free tier is a $200 credit with no expiry and no card required; Deepgram's own FAQ estimates that at roughly 43,000 minutes, over 700 hours, of Nova-3 transcription. That is the largest dollar-value free tier of the four. The [Deepgram tool page](/tools/deepgram) carries the snapshot.

Note: Deepgram's FAQ page still states that monolingual streaming costs "$0.46 an hour" — which matches the pre-promo $0.0077/min rate, not the $0.288 the rate table shows. Assume the table; if the promo expires, legacy rates return.

Scale pricing: the Growth plan starts at $4,000 per year in prepaid credits for up to 20% off and higher concurrency (225 streaming connections against 150 on pay-as-you-go). Watch the overage clause — usage beyond your credits bills at the Growth rate plus 10%, charged weekly. Add-ons bill per minute on top: diarization +$0.0020/min (about $0.12/hr), redaction +$0.0020/min, entity detection +$0.0017/min, keyterm prompting +$0.0013/min, smart formatting included. Multichannel audio bills by total duration across channels: a ten-minute stereo file bills as twenty minutes.

## AssemblyAI Pricing: The Lowest Base Rate, With a Session-Time Catch

AssemblyAI's card is the simplest of the four: AssemblyAI-STT-3.7, the new flagship, transcribes pre-recorded audio at $0.21 per hour across 32 languages; Universal-2 does the same job across 99 languages at $0.15 per hour. That $0.15 figure is the lowest published base rate on this page, with no minimums and no contract.

Streaming is where the bill bends. The realtime models bill session duration — AssemblyAI's docs define it as "the total time your WebSocket connection stays open," not audio sent. Silence, the pause while your agent decides what to say, and hold time all meter. A session your code forgets to close auto-closes at three hours, billed in full. Current rates: AssemblyAI-STT-3.7-Realtime at $0.30/hr, the agent-tuned STT-3.7-Realtime-Agent at $0.45/hr, and the previous flagship Universal-3.6 Pro Realtime at $0.45/hr. The company's November 4, 2026 cost guide also lists a value streaming tier, Universal-Streaming, at $0.15 per session hour.

The free tier is the most generous in streaming hours: up to 185 hours of pre-recorded and up to 333 hours of streaming transcription, no credit card. Add-ons stack on both surfaces — diarization at +$0.02/hr async and +$0.12/hr streaming, prompting at +$0.05/hr, Voice Focus noise cancellation at +$0.10/hr streaming, PII redaction at +$0.08/hr async. Keyterm prompting is included on Universal-2 and the realtime flagship, +$0.05/hr on the premium batch model. Multichannel audio bills per channel: a one-hour stereo file is two billable hours.

On accuracy, treat vendor claims as marketing until tested on your own audio. AssemblyAI's code-switching benchmark scores its Universal-3.5 Pro at 7.69 WER against Scribe v2's 8.77, Deepgram Nova-3's 12.22, and GPT-4o Transcribe's 44.58; the independent Artificial Analysis leaderboard puts Scribe v3 in first place instead. Both can be true on different audio — the free hours exist so you can find out which one describes yours.

One more line item: AssemblyAI sells a single-meter Voice Agent API at a flat $4.50/hr that replaces the STT + LLM + TTS stack with one WebSocket — a premium over the parts, sold as simplicity.

## OpenAI Transcription Pricing: Per-Minute Flat Rates and a Built-In Diarizer

OpenAI's card has quietly become competitive on batch. gpt-4o-mini-transcribe runs $0.003 per minute ($0.18/hr) — cheaper than ElevenLabs and Deepgram. The newer gpt-transcribe runs $0.0045/min ($0.27/hr). gpt-4o-transcribe stays at $0.006/min ($0.36/hr), billed underneath as $2.50 per million audio input tokens and $10 per million text output tokens, with the per-minute figure being OpenAI's published estimate.

The sleeper pick is gpt-4o-transcribe-diarize: same $0.006/min, with speaker labels included rather than upsold. At $0.36 all-in per hour it undercuts Deepgram's diarized bill ($0.252 + $0.12 = $0.372) and matches the "included" posture of ElevenLabs. OpenAI Whisper API pricing, meanwhile, has not moved since its 2023 launch — $0.006/min, $0.36/hr — and at today's rates that makes Whisper the worst deal on OpenAI's own card, kept alive by habit and the prompt parameter.

gpt-4o-transcribe pricing gets less competitive on the live side: gpt-live-transcribe and gpt-realtime-whisper bill $0.017 per minute ($1.02/hr), and live translation runs $0.034/min. That is 3.4x to 5.7x the native streaming specialists — OpenAI's live transcription is priced for Realtime-API voice sessions, not for captioning at scale.

Two structural notes: no meaningful free tier for transcription, and no published volume discounts — usage draws down a prepaid balance at list price.

## ElevenLabs Scribe Pricing: $0.20 an Hour, Unless You Pay in Credits

Scribe v3, released November 10, 2026, kept v2's API price — $0.003333 per audio minute, $0.20 per hour — while cutting errors: 27% fewer word errors than Scribe v2 by ElevenLabs' count, and first place on Artificial Analysis' independent AA-WER benchmark at 1.95%, ahead of Microsoft's MAI-Transcribe-2 (2.04%) and Scribe v2 (2.18%). Speaker diarization for up to 32 speakers is included, across 90+ languages. The realtime model, Scribe v3 Live, costs $0.22 per hour and ranks second among streaming APIs on Coval's voice-agent benchmark at 2.3% WER.

Add-ons: keyterm prompting costs +$0.05/hr, transcript editing +$0.07/hr. Silence is not discounted — the docs state billing covers "every second of audio you send, including pauses and silent stretches."

The trap is the credit system. Inside the ElevenLabs app, speech-to-text consumes 330 credits per minute — about 19,800 per hour — drawn from the same pool as voices, music, and dubbing. The plan table confirms the arithmetic: Starter's 30k credits buy 1 hour 31 minutes of transcription, Creator's 121k buy 6 hours 7 minutes, Pro's 600k buy 30 hours 18 minutes. Per hour, Creator works out to roughly $3.60, Pro to $3.27 — 16 to 18 times the API rate. ElevenLabs Scribe pricing through the API meter is a sharp deal; through the credit pool it is the most expensive transcription on this page. The [ElevenLabs tool page](/tools/elevenlabs) links both surfaces.

The Free plan includes 10k credits, which the plan table meters as about 12 minutes of transcription a month — enough to test accuracy, not to ship on. Enterprise contracts add EU, India, and Singapore data residency and a HIPAA BAA.

## Worked Bills: The Same Audio on Four Meters

The cleanest way to compare speech-to-text API pricing is to run identical workloads through all four meters. First, pre-recorded batch, no add-ons, at pay-as-you-go list rates:

| Monthly volume | AssemblyAI Universal-2 | OpenAI gpt-4o-mini-transcribe | ElevenLabs Scribe v3 | Deepgram Nova-3 |
|---|---|---|---|---|
| 10 hours | $1.50 | $1.80 | $2.00 | $2.52 |
| 100 hours | $15.00 | $18.00 | $20.00 | $25.20 |
| 1,000 hours | $150 | $180 | $200 | $252 |
| 10,000 hours | $1,500 | $1,800 | $2,000 | $2,520 |

Those figures scale linearly because none of the four publishes self-serve volume tiers — Deepgram's ~20% Growth discount and AssemblyAI's negotiated volume rates sit behind commitments. Now the same 1,000 hours with speaker labels, where the rankings reorder:

| Vendor (1,000 diarized hours) | Base rate | Diarization | Total bill |
|---|---|---|---|
| AssemblyAI Universal-2 | $0.15/hr | +$0.02/hr add-on | $170 |
| ElevenLabs Scribe v3 | $0.20/hr | included | $200 |
| OpenAI gpt-4o-transcribe-diarize | $0.36/hr | included | $360 |
| Deepgram Nova-3 | $0.252/hr | +$0.12/hr add-on | $372 |

Streaming, 1,000 hours of live audio: Scribe v3 Live $220, Deepgram Nova-3 streaming $288, AssemblyAI STT-3.7-Realtime $300, OpenAI gpt-live-transcribe $1,020. Those are floor numbers on AssemblyAI and Deepgram, because their streaming meters run on connection or session time — the next section covers what that does to the bill.

## Streaming Is Where the Bill Doubles

Real-time transcription pricing differs from batch in one structural way that matters more than any rate card: what gets metered. AssemblyAI bills session duration — the WebSocket's open time. Deepgram bills per minute of connection time. ElevenLabs and OpenAI bill the audio you stream, which for a live session amounts to the same wall clock. The difference shows up in the gaps: a voice agent whose callers speak 60% of the time, then wait while the LLM answers, meters 1,000 hours of session per 600 hours of speech on the session-billing vendors. Silence is not free on any of them.

Add-ons stack harder in streaming, too. A realistic AssemblyAI voice-agent configuration — STT-3.7-Realtime with diarization (+$0.12) and Voice Focus (+$0.10) — lands at $0.52 per session hour, 73% above its own $0.30 base and two and a half times the batch flagship rate. Deepgram's diarization adds the same +$0.12/hr on its streaming surface.

There is a third path: single-meter voice stacks. AssemblyAI's Voice Agent API bills a flat $4.50/hr for STT, a managed LLM, and TTS in one WebSocket; Deepgram sells the same bundle per minute of connection, cheaper if you bring your own model or voice. Whether the bundle beats wiring three vendors yourself depends on how much of the session the model and the voice spend talking — the LLM half of that stack is priced in the [LLM inference pricing breakdown](/articles/best-llm-inference-pricing-2026-groq-vs-together-vs-fireworks-vs-replicate), and the platform-level tradeoffs are compared in the [voice agent platforms roundup](/articles/best-ai-voice-agents-2026-vapi-vs-retell-vs-bland-vs-twilio). At $4.50/hr you are paying a visible premium for one meter instead of three; for many teams that is still the right call.

## Free Tiers and the Cheapest Start

Four free tiers, four different shapes:

- **Deepgram**: $200 in credits, no expiry, no card — roughly 700-plus hours of Nova-3 at promo rates. The largest speech-to-text API free tier in dollar terms.
- **AssemblyAI**: up to 185 hours batch and 333 hours streaming, no card. The largest in streaming hours, and the only one that tests a realtime surface properly.
- **ElevenLabs**: the Free plan's 10k credits meter as roughly 12 minutes a month inside the app; the $0.20/hr API rate is pay-as-you-go on top.
- **OpenAI**: nothing specific to transcription — you fund an account balance and spend it at list price.

Below the majors, independent trackers list Soniox at $0.12 per hour and Microsoft's MAI-Transcribe-2 around $0.10 per hour — both undercut every rate on this page, with thinner ecosystems to show for it. And the vendors' own benchmarks disagree wildly: AssemblyAI's test scores GPT-4o Transcribe at 44.58 WER; independent leaderboards score Scribe-class models around 2%. The only number that matters is the one your audio produces, and every free tier here exists so you can produce it before spending.

## Frequently Asked Questions

### How much does Deepgram cost per hour?

At the promo rates published November 18, 2026: $0.252/hr pre-recorded and $0.288/hr streaming on Nova-3 monolingual ($0.0042 and $0.0048 per minute), $0.30 and $0.348 multilingual, $0.39 on Flux streaming. Speaker diarization adds about $0.12/hr. The Growth plan cuts up to 20% against a $4,000/year commitment, with a +10% weekly-billed overage premium once credits run out. Deepgram's own FAQ still quotes "$0.46 an hour" for streaming — the pre-promo card, not the current table.

### What is the cheapest speech-to-text API in 2026?

For pre-recorded audio, AssemblyAI Universal-2 at $0.15/hr is the lowest published rate among the four majors. For streaming, AssemblyAI's Universal-Streaming lists at $0.15 per session hour and ElevenLabs Scribe v3 Live at $0.22/hr. Independent trackers place Soniox ($0.12/hr) and Microsoft's MAI-Transcribe-2 (about $0.10/hr) below all four — worth testing, less proven in production. The cheapest option that fails your audio is the most expensive one, so run the free tier first.

### Does AssemblyAI charge for silence in streaming?

Yes. Streaming bills session duration — the total time the WebSocket stays open — not the audio sent. Silence, agent thinking time, and hold time all meter, and a session your code never closes auto-terminates after three hours, billed in full. Close sessions the moment a call ends, and use batch for anything pre-recorded — only audio duration bills there.

### Why does ElevenLabs transcription cost more inside the app?

Credits. In-app speech-to-text consumes 330 credits per minute from the same pool as TTS, music, and dubbing — about 19,800 credits per hour. On the $22 Creator plan that works out to roughly $3.60 per transcribed hour, about 18 times the $0.20 API rate. The subscription is priced for creators mixing modalities. If transcription dominates your usage, buy through the API meter.

### Is it cheaper to self-host Whisper than to pay for an API?

Almost never, if the count is honest. AssemblyAI's published total-cost model — with assumptions it describes as generous to self-hosting — puts production-grade deployment at two on-demand GPUs (about $2,920/month) plus a quarter of a loaded engineer (about $4,167/month): roughly $7,000/month fixed before the first hour. Against a $0.15-$0.21/hr API rate, break-even sits north of 30,000 audio-hours a month. Data sovereignty, latency, and compliance are the honest reasons to self-host; unit price is not.

## Bottom Line

Speech-to-text API pricing is a solved problem at the rate-card level — every vendor here transcribes an hour for $0.15 to $0.36, and none of them will decide your margin. The meters will. Pick by meter shape, not by headline:

- **Batch volume on a budget**: AssemblyAI Universal-2 at $0.15/hr, with 185 free hours to validate accuracy on your own audio first.
- **Accuracy-critical batch with speakers**: ElevenLabs Scribe v3 at $0.20/hr, diarization included, best independent WER score on the board.
- **Already building on OpenAI**: gpt-4o-mini-transcribe at $0.003/min; add speaker labels via gpt-4o-transcribe-diarize at $0.36/hr all-in.
- **Realtime voice agents**: Deepgram's promo streaming rates plus a $200 no-expiry credit to start, or Scribe v3 Live at $0.22/hr; take the $4.50/hr single-meter bundles when you would rather wire one WebSocket than three vendors.

Every vendor here has already won the price war. What separates the $150 invoice from the $1,500 one is which meter your workload trips — session time, channels, add-ons, or credits. Count those before you count the rate card."""
}

def main():
    path = "data/articles_en.json"
    with open(path, encoding="utf-8") as f:
        arts = json.load(f)

    # Duplicate guard (exact slug or rename-detected prefix)
    for a in arts:
        if a["slug"] == ART["slug"]:
            print("ABORT: slug already exists:", ART["slug"]); sys.exit(1)
    prefix = ART["slug"].split("-2026-")[0]
    hits = [a["slug"] for a in arts if a["slug"].startswith(prefix)]
    if hits:
        print("ABORT: similar slugs exist:", hits); sys.exit(1)

    c = ART["content"]

    # ---- self checks ----
    errors = []

    # 1. word count (split convention)
    wc = len(c.split())
    if not (2200 <= wc <= 2800):
        errors.append(f"word count {wc} out of range 2200-2800")

    # 2. PK exact 4x in content (case-insensitive)
    pk = "speech-to-text api pricing"
    pk_count = c.lower().count(pk)
    if pk_count != 4:
        errors.append(f"PK '{pk}' count = {pk_count}, expected 4")

    # 3. long-tails present
    longtails = [
        "deepgram pricing", "deepgram nova-3 pricing", "assemblyai pricing",
        "openai whisper api pricing", "elevenlabs scribe pricing",
        "cheapest speech-to-text api", "real-time transcription pricing",
        "speech-to-text api free tier", "speech-to-text api cost per hour",
        "gpt-4o-transcribe pricing",
    ]
    low = c.lower()
    missing = [lt for lt in longtails if lt not in low]
    if missing:
        errors.append("missing long-tails: " + ", ".join(missing))

    # 4. banned words
    banned = ["leverage", "utilize", "seamlessly", "game-changing", "empower",
              "streamline", "delve", "transformative", "comprehensive",
              "revolutionize", "cutting-edge", "as an ai", "in conclusion"]
    found = [b for b in banned if b in low]
    if found:
        errors.append("banned words found: " + ", ".join(found))

    # 5. tables: >=1 table with >=4 data rows and >=4 cols
    tables = []
    cur = []
    for line in c.split("\n"):
        if line.strip().startswith("|"):
            cur.append(line)
        else:
            if cur:
                tables.append(cur); cur = []
    if cur:
        tables.append(cur)
    good_tables = 0
    for t in tables:
        cols = len([x for x in t[0].strip().strip("|").split("|")])
        data_rows = len(t) - 2  # minus header + separator
        if cols >= 4 and data_rows >= 4:
            good_tables += 1
    if good_tables < 1:
        errors.append(f"no table with >=4 rows and >=4 cols (tables found: {len(tables)})")

    # 6. internal links >=2 and targets exist
    links = re.findall(r"\]\((/articles/[^)]+|/tools/[^)]+)\)", c)
    if len(links) < 2:
        errors.append(f"internal links = {len(links)}, expected >=2")
    with open("data/tools_en.json", encoding="utf-8") as f:
        tool_slugs = {t["slug"] for t in json.load(f)}
    art_slugs = {a["slug"] for a in arts}
    for ln in links:
        if ln.startswith("/articles/"):
            s = ln[len("/articles/"):].rstrip("/")
            if s not in art_slugs:
                errors.append("broken article link: " + ln)
        else:
            s = ln[len("/tools/"):].rstrip("/")
            if s not in tool_slugs:
                errors.append("broken tool link: " + ln)

    # 7. FAQ H3 count >= 3
    faq_part = c.split("## Frequently Asked Questions", 1)[1]
    h3 = [l for l in faq_part.split("\n") if l.startswith("### ")]
    if len(h3) < 3:
        errors.append(f"FAQ H3 count = {len(h3)}, expected >=3")

    if errors:
        print("SELF-CHECK FAILED:")
        for e in errors:
            print(" -", e)
        sys.exit(1)

    arts.append(ART)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(arts, f, ensure_ascii=False, indent=2)

    print(f"OK: appended article #{len(arts)}")
    print(f"slug: {ART['slug']}")
    print(f"word count: {wc}")
    print(f"PK count: {pk_count}")
    print(f"long-tails: {len(longtails) - len(missing)}/{len(longtails)}")
    print(f"tables: {len(tables)} total, {good_tables} qualify (>=4x4)")
    print(f"internal links: {len(links)} -> {links}")

if __name__ == "__main__":
    main()
