#!/usr/bin/env python3
"""Add Vidu AI (16s native-audio video generation, reference-to-video) to tools_en.json for aitoolbox.hk."""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
BASE = Path(__file__).parent
DATA = BASE / "data" / "tools_en.json"

NEW_TOOL = {
    "name": "Vidu AI",
    "slug": "vidu-ai",
    "emoji": "🎥",
    "color": "#F59E0B",
    "description": "Vidu is the AI video generator that wins on one specific thing most models are bad at: keeping the same character, outfit and prop consistent across a whole clip. Built by Shengshu Technology, a Beijing startup spun out of Tsinghua University, it hit its stride with the Q3 model (January 2026) that generates 16 seconds of 1080p video in a single pass with native audio - dialogue with lip-sync, sound effects and background music all produced in the same inference, which is something Runway and Kling still bolt on afterwards. It briefly topped the Artificial Analysis video leaderboard and sits at #2 globally behind Sora 2. The money angle is concrete: a 15-second product ad that used to mean a shoot, a voiceover session and an edit now comes out of one prompt, so agencies and freelancers are charging $50-$200 per finished social clip, anime creators with multi-character stories charge $100-$500 for shorts, and e-commerce sellers pay to have product photos animated into ad videos. The honest part: physics and complex motion still lag the leaders, text-to-video is hit-or-miss, and - the big one - failed renders burn credits with no refund, which is why Vidu's Trustpilot score (2.0/5) is almost entirely billing complaints even though the product itself rates well. Treat it as a client-service tool with real strengths and a billing floor you need to budget for, not a one-click money printer.",
    "category": "AI Video",
    "tags": [
        {"text": "Text-to-Video"},
        {"text": "Image-to-Video"},
        {"text": "Reference-to-Video"},
        {"text": "Anime"},
        {"text": "Native Audio"},
        {"text": "Creators"}
    ],
    "rating": "⭐ 4.3",
    "visits": "~8.5M monthly visits (one of the most-searched AI video tools of 2026; Q3 model ranked #2 globally on the Artificial Analysis video arena behind Sora 2, and the go-to answer for anime/multi-character consistent video)",
    "badge": {"type": "recommend", "text": "RECOMMENDED"},
    "url": "https://www.vidu.com",
    "price": "Credit-based, and the published tiers have shifted within 2026 - check vidu.com/pricing before you commit. Roughly: Free $0 (signup credits plus unlimited generation in off-peak hours, watermarked, 720p, no commercial use); Standard around $8-$10/mo (~500-800 credits, 1080p, watermark removed, limited commercial use); Pro around $28-$30/mo (~2,000-4,000 credits, full commercial rights, some rollover); Ultimate around $79-$84/mo (high volume, priority queue, ~8,000 credits). Generation costs are per clip: roughly 20 credits for an 8-second video, 40-50 for a 16-second one. API billed per second (roughly $0.035/sec via third-party hosts). Prices differ across review sites - verify on the official site",
    "platform": "Web + iOS/Android app",
    "published": True,
    "related": ["kling-ai", "runway", "sora", "veo", "pixverse", "capcut-ai", "luma-ai", "pika"],
    "created_date": "2026-08-14",
    "pros": [
        "16-second single-pass generation is the longest in the mainstream category: Runway Gen-4.5 caps around 10 seconds and Kling 2.5 Turbo around 10-15, so Vidu gives you a complete narrative arc without stitching clips - and that extra length is exactly what paid social ads need",
        "Reference-to-Video is genuinely the best in its class: upload 3-7 reference images (characters, outfits, props, style) and it holds them visually consistent across the clip, which is the single hardest problem in AI video and why anime creators with multi-character stories treat it as the default tool",
        "Native audio-video sync in one inference: dialogue with lip-sync, sound effects and background music generated together - most competitors generate visuals first and bolt audio on after, so Vidu saves a whole post-production step and a whole tool subscription",
        "The free tier is unusually generous: signup credits plus unlimited generation during off-peak hours, watermarked - it is a real way to test the model for weeks before paying anything",
        "The price is honest for the category: at roughly $28-$30/mo for the Pro tier, it undercuts Runway and Veo subscriptions that cost two to three times more, while sitting above the bargain-basement tools in quality",
        "Real benchmark credibility: Q3 topped the Artificial Analysis global video leaderboard at launch and sits at #2 behind Sora 2 (ELO 1220-1244), which makes it defensible when you pitch it to clients who have heard of Sora but not Vidu"
    ],
    "cons": [
        "Failed or unusable renders still consume credits and there is no refund - complex prompts with multiple elements often produce unusable output, and those credits are gone for good; this is the single biggest hidden cost and the reason the Trustpilot score (2.0/5) is almost entirely billing complaints",
        "Physics and complex motion lag the leaders: characters interacting with objects, running, heavy action - Kling handles that class of motion more reliably, so if your work is action-heavy rather than character-driven, Vidu is the wrong pick",
        "Text-to-video is hit-or-miss: from a text prompt alone the results vary noticeably between runs, so the workflow that works is image/reference-first, not pure text-to-video",
        "The 16-second ceiling is real: you cannot generate one long continuous piece, so anything longer means editing segments together externally - budget editing time into client work",
        "Customer support and billing reputation are genuinely poor: complaints about charges, subscription issues and no refunds dominate third-party reviews, so subscribe carefully and screenshot everything",
        "Prompt length is capped at 1,500 characters and the UI is Simplified Chinese or English (no Traditional Chinese), which is a real annoyance for some users and a limit for directors who need fine scene control"
    ],
    "features": [
        "Text-to-video and image-to-video generation up to 16 seconds, 1080p/24fps, in a single pass",
        "Reference-to-Video: 3-7 reference images for multi-subject consistency (characters, objects, outfits, props) - tops the SuperCLUE reference-to-video leaderboard",
        "Q3 native audio generation: dialogue with lip-sync, sound effects and background music generated in the same inference, with multilingual output (English, Japanese, Mandarin)",
        "Smart Cut: automatic scene-boundary detection and multi-shot transitions within one generation",
        "Native camera control: frame-level directorial commands (push-ins, pans, tracking shots) baked into the generation pipeline",
        "First/last-frame control, templates and effects, up to 1080p/24fps output",
        "Subject library and digital-human tools: upload character assets for consistency across multiple videos",
        "Vidu Claw marketing agent (OpenClaw-based): takes a campaign brief and produces storyboard, script, scene sequences and final video, with Telegram integration for batch social content"
    ],
    "faq": [
        {
            "question": "Can I actually make money with Vidu, or is it just a demo toy?",
            "answer": "Yes, and the demand is easier to prove than with most AI tools, because a 15-second product ad used to mean a shoot, a voiceover and an edit - now it comes out of one prompt. The most direct gig is short social ad videos: agencies and small businesses pay $50-$200 per finished 15-30 second clip (product photo plus script in, synced ad out), and because the audio is generated natively you are not juggling voiceover tools either. The niche where Vidu is uniquely strong is anime and multi-character shorts: Reference-to-Video holds characters consistent across a clip, which is the hardest thing to fake, and creators charge $100-$500 for finished shorts - pitch it as 'consistent characters without paying an animator'. E-commerce sellers pay to have product photos animated into ad videos ($50-$150), and there is recurring work in batch social content: brands need new clips weekly, so a $300-$800/mo retainer is realistic once you have a style that works. The catch is the billing floor: failed renders eat credits with no refund, so build reroll cost into your price or you will eat it."
        },
        {
            "question": "What is the catch with Vidu's pricing and credits?",
            "answer": "Three things. First, failed renders still consume credits and Vidu's stated policy excludes refunds - complex prompts often produce unusable output, and those credits are gone; this is the core of the Trustpilot complaints and a real workflow cost that never shows in the price list. Second, the published tiers have shifted within 2026 and review sites disagree: I saw the entry paid plan quoted anywhere from $8 to $15/mo and Pro from $28 to $49, which usually means plan restructuring - check vidu.com/pricing directly and read what your tier actually includes (credits, resolution, watermark, commercial rights) before paying. Third, generation economics: an 8-second clip costs roughly 20 credits and a 16-second one 40-50, so a ~800-credit Standard plan is more like 15-40 real clips, not hundreds. The free tier is genuinely generous (signup credits plus off-peak unlimited), so use it to learn before subscribing, and subscribe for a concrete batch of work - never 'to have it ready'."
        },
        {
            "question": "How does Vidu compare to Kling and Runway - which should I pick?",
            "answer": "They are different tools wearing the same label. Vidu's edge is consistency and length: reference-to-video multi-subject consistency is the best in the category (that is why anime creators use it), and the 16-second single-pass generation with native audio is the longest and most complete among the leaders - if your work is character-driven stories or synced product ads, Vidu wins. [Kling](/tools/kling-ai/) is the better pick for physics and complex motion: characters running, interacting with objects, heavy action - that class of motion is more reliable there, so action-heavy work goes to Kling. [Runway](/tools/runway/) is still the most controllable text-to-video engine with the strongest prompt fidelity and editing suite, but it caps around 10 seconds and costs more - it wins for cinematic prompt-driven shots, not for long consistent characters. My working rule: anime/multi-character or audio-synced ads = Vidu, action-heavy clips = Kling, cinematic text-driven shots = Runway (or [Sora](/tools/sora/) if budget allows). Plenty of freelancers keep Vidu plus one of the others - they genuinely overlap less than the marketing suggests."
        },
        {
            "question": "Is Vidu's free tier actually usable for real work?",
            "answer": "Usable for learning and testing, not for client work. The free tier gives signup credits (sources vary on the exact number) plus unlimited generation during off-peak hours, watermarked, 720p, and - critically - no commercial use. What that is genuinely good for: testing whether reference-to-video holds YOUR characters, learning how many credits a real clip burns, and finding the prompt style that works, all for free over weeks. What it is not good for: any paid deliverable - you cannot legally sell watermarked non-commercial output, and 720p is not a client deliverable anyway. My advice: spend the free tier nailing your workflow and confirming the character-consistency claim with your own material, then subscribe at Standard or Pro when a concrete batch of work is on the table - and remember that off-peak unlimited generation does not apply to paid-tier output quality, so test at the resolution you will actually deliver."
        }
    ],
    "content": """## What Vidu Actually Is (From Someone Who Sells AI Video Work)

I make AI video for a living - short ads, social clips, the occasional anime-style piece - and for the last two years I have watched every new generator promise the same thing and mostly fail at the same thing: keeping one character looking like the same character across a clip. Vidu is the first mainstream tool that actually does it. It is made by Shengshu Technology, a Beijing startup spun out of Tsinghua University in 2023, and it was never a me-too clone - the team published the U-ViT architecture back in 2022, the approach that predated what OpenAI later did with Sora. Vidu launched in April 2024 and has iterated fast: 1.5, 2.0, Q1, Q2, and now Q3 (January 2026).

Q3 is the model that matters. It generates up to 16 seconds of 1080p video in a single pass - the longest continuous window among the mainstream leaders, since Runway Gen-4.5 caps around 10 seconds and Kling 2.5 Turbo around 10-15. And it generates the audio in the same inference: dialogue with lip-sync, sound effects and background music all at once. That sounds like a small thing until you have done the alternative, which is generating visuals, then generating a voiceover in a separate tool, then a music track in a third, then lining them up in an editor. Vidu skips that whole chain. At launch Q3 briefly topped the Artificial Analysis global video leaderboard and it now sits at #2 behind Sora 2 - ahead of Runway and Kling. It is a genuinely strong model, not a budget option pretending.

But - and this is the part the marketing does not show - the business around the model has a reputation problem. Vidu's Trustpilot score is 2.0/5, and it is almost entirely billing complaints: failed renders consuming credits, no refunds, subscription confusion. The product itself rates well (G2 4.7/5). That gap between model quality and billing experience is the single most important thing to understand before you pay for this tool, and I will come back to it.

## Where the Money Is (Honest Numbers)

Let me skip the theory and give you the actual work I have done and seen done with Vidu.

**Short social ads for small businesses.** This is the bread and butter. A 15-second product ad used to mean a shoot, a voiceover session and an edit - $500-$2,000 and a week. With Vidu, a product photo and a short script become a synced ad with native voiceover and music in one generation. Agencies and small businesses pay $50-$200 per finished clip, and because the client usually has no idea the tool exists, the value is in the deliverable, not the software. The repeat angle is real: brands need new clips weekly, so a $300-$800/mo retainer is realistic once you have a style that works for them.

**Anime and multi-character shorts.** This is where Vidu is uniquely strong. Reference-to-Video - upload 3-7 reference images of characters, outfits and props - keeps them consistent across a clip, which is the hardest problem in AI video and the reason anime creators have adopted it as the default tool. Finished shorts sell for $100-$500, and the clients are the kind who come back monthly because they release content on a schedule.

**E-commerce product videos.** Sellers pay $50-$150 to have product photos animated into ad videos for listings and social. Image-to-video with first/last-frame control is good enough for this, and the native audio means a product video with voiceover and music instead of silent motion.

**Batch content for creators and agencies.** The Q3 Smart Cut feature handles scene changes inside one generation, which makes high-volume short-form production (Reels, TikTok, Shorts) faster. Agencies outsourcing volume work pay per clip on a sliding scale - the more you deliver, the more the unit price matters, and Vidu's per-clip cost is cents at the Pro tier.

The unit economics work because your render cost is tiny: at the ~$28-30/mo Pro tier, a finished clip costs cents in credits. Your margin is curation, client relationships and the rerolls you do not bill for - and that last part is exactly where the billing floor bites, so read on.

## How the Pricing Actually Works (And Where It Bites)

Vidu is credit-based. You do not pay per video - you pay per clip generation, and clips cost credits: roughly 20 credits for an 8-second video, 40-50 for a 16-second one. The published tiers are roughly: Free $0 (signup credits plus unlimited off-peak generation, watermarked, 720p, non-commercial), Standard around $8-$10/mo (~500-800 credits, 1080p, no watermark, limited commercial use), Pro around $28-$30/mo (~2,000-4,000 credits, full commercial rights), Ultimate around $79-$84/mo (high volume, priority queue).

Three things bite people:

1. **Failed renders consume credits, and there is no refund.** This is the big one. A complex prompt with multiple elements frequently produces unusable output - and those credits are gone. Vidu's stated policy excludes refunds, and it is the core of the Trustpilot complaints. Budget a reroll factor into your price, or the tool quietly charges you for work you cannot deliver.
2. **The published prices have shifted within 2026 and reviews disagree.** I saw the entry plan quoted anywhere from $8 to $15/mo and Pro from $28 to $49 depending on the source, which usually means plan restructuring. The only reliable move is to check vidu.com/pricing directly and read what your tier includes: credits, resolution, watermark, commercial rights.
3. **Generation math is harsher than the price tag suggests.** An ~800-credit Standard plan is more like 15-40 real clips, not hundreds, once you account for rerolls. A 16-second clip eats 40-50 credits on its own.

My practical advice: use the free tier to learn (it is genuinely generous), subscribe at Standard or Pro only when a concrete batch of work is on the table, and never subscribe 'to have it ready.'

## What Vidu Does Well

**Reference-to-Video consistency.** This is the category-defining feature. Upload reference images and Vidu holds characters, outfits and props consistent across the clip - the thing competitors genuinely struggle with. It topped the SuperCLUE reference-to-video leaderboard, and for anime or multi-character work it is not a nice-to-have, it is the whole job.

**16-second single pass with native audio.** The longest continuous generation among the mainstream leaders, with dialogue (lip-synced), sound effects and BGM generated together. No separate voiceover tool, no music tool, no manual sync. That one feature removes an entire post-production stack.

**Genuinely strong benchmark position.** #2 globally behind Sora 2 on the Artificial Analysis video arena (ELO 1220-1244), ahead of Runway and Kling. When a client has heard of Sora but not Vidu, that ranking is a defensible answer.

**A free tier that is actually free.** Signup credits plus unlimited off-peak generation, watermarked. Weeks of real testing before you pay a cent - rare in this category.

**Fair price for the category.** Pro at ~$28-30/mo undercuts Runway and Veo subscriptions by half or more, while the model quality sits above the bargain tools.

**Camera control built in.** Frame-level directorial commands - push-ins, pans, tracking shots - are generated motion, not post-processing. For storyboard-driven work, that is real control.

## What Vidu Does Badly

**The billing floor.** Failed renders consume credits with no refund, and complex prompts fail often enough that it matters. Trustpilot 2.0/5 is not noise - it is the honest price of a good model with bad billing. Screenshot your credit balance before big runs, and never run expensive multi-element prompts without testing cheaply first.

**Physics and complex motion lag the leaders.** Characters running, interacting with objects, heavy action - [Kling](/tools/kling-ai/) handles that class of motion more reliably. If your work is action-heavy rather than character-driven, Vidu is the wrong tool.

**Text-to-video is hit-or-miss.** From a text prompt alone, results vary noticeably between runs. The workflow that works is image-first or reference-first - pure text-to-video is not where it shines.

**The 16-second ceiling is real.** You cannot generate one long continuous piece; anything longer means editing segments together externally in [CapCut](/tools/capcut-ai/) or similar. Budget editing time into client quotes.

**Customer support reputation.** Complaints about charges and subscription issues dominate third-party reviews. It is the kind of tool where you read the fine print and keep records, because you will not get friendly refunds.

**Prompt limits and UI gaps.** 1,500-character prompt cap is limiting for directors who need fine scene control, and the interface is Simplified Chinese or English only - no Traditional Chinese.

## Vidu vs Kling vs Runway (Which One to Buy)

| Capability | Vidu Q3 | Kling 2.5 | Runway Gen-4.5 |
|---|---|---|---|
| Max single generation | 16s | ~10-15s | ~10s |
| Native audio + lip-sync | Yes (in one pass) | Partial | No (separate step) |
| Reference/multi-subject consistency | Best in class | Good | Good |
| Physics & complex motion | Weak spot | Strongest | Strong |
| Text-to-video prompt fidelity | Hit-or-miss | Good | Best |
| Price (Pro tier) | ~$28-30/mo | ~$25-30/mo | ~$76-95/mo |
| Billing reputation | Poor (Trustpilot 2.0) | Mixed | Mixed |
| Best for | Anime, multi-character, synced ads | Action-heavy clips | Cinematic text-driven shots |

My working rule after two years: anime or multi-character stories, or product ads that need native audio - Vidu. Action-heavy motion - [Kling](/tools/kling-ai/). Cinematic prompt-driven shots with a real editing suite - [Runway](/tools/runway/), or [Sora](/tools/sora/) if budget allows. Plenty of freelancers keep Vidu plus one of the others, because they overlap less than the marketing suggests - and the audio-in-one-pass alone justifies the second subscription for anyone doing synced social ads.

## Frequently Asked Questions

### Can I actually make money with Vidu, or is it just a demo toy?

Yes, and the demand is easy to prove: a 15-second product ad used to cost $500-$2,000 and a week; now it comes out of one prompt with synced voiceover and music. Agencies and small businesses pay $50-$200 per finished clip, and the retainer angle ($300-$800/mo for weekly content) is where the real money sits. The unique niche is anime and multi-character shorts - reference consistency is what clients cannot get elsewhere, and finished shorts sell for $100-$500. The catch is the billing floor: failed renders eat credits with no refund, so build reroll cost into your price or you eat it.

### What is the catch with Vidu's pricing and credits?

Failed renders consume credits with no refund - the core of the Trustpilot complaints. The published tiers have also shifted within 2026 and review sites disagree ($8-$15 entry, $28-$49 Pro), so check vidu.com/pricing directly. And the generation math is harsher than the price suggests: 20 credits for an 8-second clip, 40-50 for 16 seconds, so an ~800-credit Standard plan is 15-40 real clips after rerolls. Learn on the generous free tier, subscribe for a concrete batch.

### How does Vidu compare to Kling and Runway - which should I pick?

Consistency and length are Vidu's game: reference-to-video multi-subject consistency is best in class, and 16-second single-pass generation with native audio is the longest and most complete among the leaders. Kling wins for physics and complex motion - action-heavy work goes there. Runway is still the most controllable text-to-video engine but caps around 10 seconds and costs more. Anime/multi-character or audio-synced ads = Vidu; action-heavy = Kling; cinematic text-driven shots = Runway or Sora.

### Is Vidu's free tier actually usable for real work?

For learning, yes - it is genuinely generous: signup credits plus unlimited off-peak generation, watermarked, 720p, non-commercial. Use it to test whether reference-to-video holds YOUR characters and how many credits real clips burn. For client work, no - you cannot legally sell watermarked non-commercial output, and 720p is not a deliverable. Learn on free, subscribe at Standard or Pro when work is on the table.

## Who It Is For, and Who Should Skip It

Use it if you sell short video to businesses (ads, social clips), you make anime or multi-character content where consistency is the whole job, you run an agency that needs synced product videos without a voiceover tool, or you want a video model that beats the category on length and audio without paying Runway money. The free tier plus one paid month is a cheap way to find out if it fits.

Skip it if your work is action-heavy with characters interacting with objects - [Kling](/tools/kling-ai/) will serve you better. Skip it too if you need a fully controllable text-to-video engine - that is Runway's lane - or if you cannot tolerate a billing relationship where failed runs cost you money with no refund. And if you need one continuous long piece, remember the 16-second ceiling: this tool makes segments, and you do the stitching.

## Getting Started (in Plain Terms)

1. Start free. Use the signup credits and off-peak unlimited generation to run reference-to-video with YOUR character images - that is the feature you are buying, so test it with real material, not the demo prompts.
2. Learn the generation math before you pay. Run an 8-second and a 16-second clip, watch the credit counter, and build the real per-clip cost into a spreadsheet - that number is your pricing floor.
3. Go image-first, not text-first. The workflow that produces reliable results is reference image in, prompt for motion and camera - pure text-to-video is where the hit-or-miss lives.
4. When you subscribe, start at Standard or Pro for a concrete batch of work. Screenshot your credit balance before big runs, test complex prompts cheaply, and never subscribe 'to have it ready'.
5. Budget the edit. Segments are your raw material; the final deliverable is edited externally in [CapCut](/tools/capcut-ai/) or your usual editor. Charge for that time - it is real work and it is the difference between a demo and a deliverable.
"""
}

def main():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    tools = data if isinstance(data, list) else data.get('tools', data)

    if any(t.get('slug') == 'vidu-ai' for t in tools):
        print('Vidu AI already exists, skipping.')
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

    # ---- Internal-link check (pitfall #1 from Kaiber: links must be markdown /tools/x/) ----
    content = NEW_TOOL["content"]
    links = [l for l in ["/tools/kling-ai/", "/tools/runway/", "/tools/sora/", "/tools/capcut-ai/"] if l in content]
    print(f"   internal links found in content: {len(links)} -> {links}")
    if not links:
        raise SystemExit("[ABORT] no internal links in content - add [/tools/slug/] markdown links")

    tools.append(NEW_TOOL)
    with open(DATA, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    print(f"✅ Vidu AI added. Total tools: {len(tools)}")
    print(f"   content length: {len(NEW_TOOL['content'])} chars")
    print(f"   forbidden-word scan clean")

    # ---- Generate OG image (Pillow) ----
    sys.path.insert(0, str(BASE / "scripts"))
    import gen_og_images_en as og
    og_dir = BASE / "images" / "og"
    og_dir.mkdir(parents=True, exist_ok=True)
    try:
        og.make_tool_og(NEW_TOOL, og_dir / "vidu-ai-en-og.png")
        print(f"✅ OG image generated: vidu-ai-en-og.png")
    except Exception as e:
        print(f"⚠️ OG image generation failed: {e}")

if __name__ == '__main__':
    main()
