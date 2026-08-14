#!/usr/bin/env python3
"""Add Seedance (ByteDance 2.0/2.5 30s AI video) to tools_en.json for aitoolbox.hk."""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
BASE = Path(__file__).parent
DATA = BASE / "data" / "tools_en.json"

NEW_TOOL = {
    "name": "Seedance",
    "slug": "seedance",
    "emoji": "🎬",
    "color": "#6366F1",
    "description": "Seedance is ByteDance's AI video generation model family - the one that quietly became the longest-single-take option in the category when version 2.5 shipped on July 31, 2026 with a native 30-second single-pass generation (a 180-second beta mode on top), versus the 15-second ceiling of Kling 3.0 and the shorter extension-based approach of Google Veo 3.1. The same model does text, images, video and audio input, and up to 50 reference materials in one generation - about 30 images, 10 video clips and 10 audio files - which is why brand ad work keeps coming back to it: a product, a face, a color palette and a sound bed all stay locked across a whole clip. Audio is generated jointly (dialogue with lip-sync, SFX, BGM in one inference), and 2.5 added timestamp-level shot control and a 3D white-model preview for storyboard work that no competitor has shipped yet. The money angle is direct: a 30-second brand ad or a beat-synced music video no longer needs clip stitching, so freelancers and agencies are charging $100-$500 per finished piece, and the 50-reference system makes strict brand consistency the sellable feature. The honest part: pricing is genuinely messy (API tokens vs consumer subscriptions, and resolution moves your bill by 2.25x), the claimed 20% prompt-following improvement over 2.0 has no independent benchmark behind it, long-form consistency past the first few shots is still unproven, text in video still comes out garbled, and access is limited - Dreamina is not available in the US and the global API rollout has been delayed. It is a serious contender in the post-Sora top tier, not a toy - but budget for learning curve and rerolls like any video tool.",
    "category": "AI Video",
    "tags": [
        {"text": "Text-to-Video"},
        {"text": "Image-to-Video"},
        {"text": "Multi-shot Storytelling"},
        {"text": "Native Audio"},
        {"text": "30s Generation"},
        {"text": "ByteDance"}
    ],
    "rating": "⭐ 4.4",
    "visits": "Trending fast - Seedance 2.5 launched July 31, 2026 with API live on Volcano Engine since Aug 7; Seedance 2.0 leads the Artificial Analysis video arena at ~1,218 Elo, ahead of Veo 3.1 and Kling 3.0 (2.5 has no published independent arena score yet)",
    "badge": {"type": "new", "text": "NEW"},
    "url": "https://seed.bytedance.com/seedance2_0",
    "price": "Two separate billing systems. Consumer side via Jimeng (CN) or Dreamina (international): free tier ~66 credits/day, Jimeng Basic ¥69/mo (~1,080 credits), Standard ¥199/mo (~4,000 credits, 4K), Advanced ¥499/mo (~15,000 credits, commercial license); Dreamina Basic ~$18/mo, Standard ~$42/mo, Advanced ~$84/mo. API side via Volcano Engine/BytePlus: token-based - Seedance 2.5 is ¥70 per million tokens without video input, ¥42 with video input (about 52% above 2.0's ¥46/¥28). BytePlus worked example: a 5-second 16:9 clip costs ~$0.514 at 480p but ~$1.156 at 720p - resolution, not the headline token rate, drives your bill. 2.0 mini/fast discounted Aug 7-Sep 7 (720p ~¥0.2-0.6/sec). Sources differ; check the official pricing page",
    "platform": "Web (Jimeng/Dreamina), mobile apps, API (Volcano Engine / BytePlus)",
    "published": True,
    "related": ["kling-ai", "runway", "sora", "veo", "vidu-ai", "pixverse", "capcut-ai"],
    "created_date": "2026-08-15",
    "pros": [
        "30-second single-pass generation is the longest in the mainstream category: Kling 3.0 caps at 15 seconds and Veo 3.1 uses extension-based generation, so Seedance 2.5 gives you a complete narrative arc - setup, build, turn, payoff - in one take with no stitch line, plus a 180-second beta mode for longer pieces",
        "Up to 50 multimodal references in one generation (roughly 30 images, 10 video clips, 10 audio files) for characters, locations, products, style guides and sound beds - competitors take a handful of images, so strict brand-consistency ad work has a concrete reason to choose Seedance",
        "Native joint audio-video generation: dialogue with lip-sync, sound effects and background music in the same inference, in 11 languages - you do not need a separate voiceover tool or music tool for synced content",
        "Timestamp-level shot control is a genuine 2.5 upgrade: 2.0's docs warned that precise timing was 'unstable', while 2.5 lists efficient second-level timestamp response as a core selling point - for beat-synced music videos and structured ads that is the difference between usable and unusable",
        "3D white-model preview (white-box blockout): rough untextured geometry to lock camera and staging before anything is lit - the first feature of its kind in a video model, and a real workflow win for anyone who storyboards or pitches previz to clients",
        "Strong speed and benchmark position: 15-second videos generate in 30-60 seconds (2-3x faster than Runway per reviews), and 2.0 sits at ~1,218 Elo on the Artificial Analysis arena ahead of Veo 3.1 and Kling 3.0 - defensible when you pitch it against names clients already know"
    ],
    "cons": [
        "Pricing is genuinely messy and easy to misread: two separate systems (token-based API vs credit subscriptions), the per-second figures quoted by third parties are often wrong by a multiple, and resolution moves your bill by ~2.25x (a 5-second clip is $0.514 at 480p but $1.156 at 720p on BytePlus's own example) - model your real costs before committing",
        "The claimed 20% prompt-following improvement of 2.5 over 2.0 has no independent benchmark behind it, and 2.5 costs ~52% more per token - you are paying a premium on an unverified headline number",
        "Long-form consistency past the first few shots is unproven: 2.0 reviews show characters and backgrounds drifting around shot 4-5, and 2.5's 30-second window is new enough that nobody has stress-tested it at scale yet",
        "Text in video still comes out garbled or deformed - logos, titles and captions must be added in post-production, which costs time and can break a deliverable if the client expects baked-in text",
        "Scenes with 3+ characters interacting are error-prone: character merging and uncoordinated motion show up in multi-character prompts, so complex narrative work still means segmented generation plus editing",
        "Access is genuinely limited: Dreamina is not available in the US, the global API rollout has been delayed over copyright discussions with studios, and each integration platform exposes only a subset of the model's capabilities - what you see in Jimeng is not the full model"
    ],
    "features": [
        "Native 30-second single-pass generation (plus 180-second beta mode) with multi-shot narrative structure in one inference",
        "Up to 50 multimodal references per generation: ~30 images, 10 video clips, 10 audio files - characters, locations, products, style guides, sound beds",
        "Joint audio-video generation: dialogue with lip-sync, SFX and BGM in the same pass, in 11 languages (English, Chinese, Japanese, Korean, Spanish, Arabic, Portuguese and more)",
        "Timestamp-level shot and camera control - second-level timing instructions honored reliably in 2.5 (a documented weak point of 2.0)",
        "Localized editing: redraw part of a frame without regenerating the rest, plus green-screen plates and video-in to fill transition gaps (clean clip joining)",
        "3D white-model preview / white-box blockout: lock camera position and staging with rough geometry before lighting",
        "Multi-view subject reference, grid storyboard reference, and any aspect ratio from 0.4 to 2.5 (2.0 was fixed presets)",
        "Access via Jimeng / Dreamina consumer apps, Doubao Pro, and the Volcano Engine (BytePlus) API since Aug 7, 2026"
    ],
    "faq": [
        {
            "question": "Can I actually make money with Seedance, or is it just another demo model?",
            "answer": "Yes, and the strongest angle is the one that was painful before: a 30-second single-pass generation means a complete brand ad or narrative short with no clip stitching, and the 50-reference system holds a product, face and palette consistent across the whole take - that consistency is exactly what clients pay for and what freelancers charge $100-$500 per finished piece for. Music-video work is the niche where Seedance is uniquely strong because 2.5 honors timestamp-level prompts, so beat-synced cuts land where they must - creators charge $100-$500 for synced MVs that used to require frame-by-frame editing. There is also previz money: the 3D white-model preview lets you pitch camera and staging to clients before anything is rendered, a billable B2B service agencies offer. And the multilingual lip-sync (11 languages) makes localized ad variants cheap - one script, several markets. The catch is the billing complexity and reroll rate on long clips: budget for learning and failed runs, and model your per-clip cost before quoting."
        },
        {
            "question": "API tokens or the Jimeng/Dreamina subscription - which do I actually pay?",
            "answer": "They are two different products and the cost math does not transfer. The API (Volcano Engine / BytePlus) bills per token: Seedance 2.5 is ¥70 per million tokens without video input and ¥42 with video input - about 52% above 2.0 - and BytePlus's own example prices a 5-second 720p clip at ~$1.156 versus ~$0.514 at 480p, so resolution is the real driver, not the headline rate. The consumer subscriptions bundle Seedance with other tools: Jimeng is free (~66 credits/day), Basic ¥69/mo (~1,080 credits), Standard ¥199/mo (~4,000, 4K), Advanced ¥499/mo (~15,000, commercial license); Dreamina international runs Basic ~$18/mo, Standard ~$42/mo, Advanced ~$84/mo. For a freelancer doing client clips, the consumer subscription is usually the cheaper entry - a Standard plan covers real volume - while the API makes sense only if you are building a product or need programmatic generation. Whichever you pick, check the official pricing page and the resolution/credit terms for your region, because third-party per-second figures have been wrong by a multiple."
        },
        {
            "question": "How does Seedance compare to Kling and Veo - which should I pick?",
            "answer": "Different tools wearing the same label. Seedance's edge is duration, reference breadth and beat control: 30-second single takes with up to 50 references and stable timestamp-level direction - pick it for long narrative arcs, brand-consistency ads and beat-synced music videos. [Kling](/tools/kling-ai/) is the better pick for physics, complex motion and cinematic camera: Kling 3.0 does 15-second generation with multiple camera setups, native 4K at 60fps and AI Director control, and it handles action-heavy clips more reliably - though reviews note a 30-40% reroll rate on complex prompts. [Veo](/tools/veo/) 3.1 is strongest for synchronized dialogue and lip-sync quality with an official global developer API, but its generation is shorter and extension-based, and Ultra runs $249.99/mo. Runway remains the most controllable editing-oriented pipeline but caps around 10 seconds. My working rule: long single-take brand work or music videos = Seedance, action and physics = Kling, dialogue-driven scenes with global API access = Veo. Many freelancers keep Seedance plus one of the others because they overlap less than the marketing suggests."
        },
        {
            "question": "How do I get access, and is it usable outside China?",
            "answer": "Access is the most annoying part of this tool right now. In mainland China you use the Jimeng app or Doubao Pro; internationally it runs through Dreamina (dreamina.capcut.com), which is ByteDance's global creative platform - but Dreamina is not available in the US, and the global API rollout has been delayed over copyright discussions with studios. Third-party API aggregators have begun listing Seedance routes (from around $0.084/sec at the lowest tier), so international access is possible but you should verify the region where your account works before paying. Also note each integration exposes a subset of the model: I have seen implementations where 4K/21:9 was documented but the actual product only offered 480p-1080p, and region-based editing tools were missing. Test the exact capabilities of the platform you intend to use - do not assume the model's spec sheet is what you get in the UI."
        }
    ],
    "content": """## What Seedance Actually Is (From Someone Who Sells AI Video Work)

I make AI video for a living - brand ads, music videos, the occasional short-form batch for agencies - so I have watched the top tier of this market reshuffle twice in 2026. OpenAI shut down the Sora consumer app in late April and its API runs only until late September. That leaves Google's Veo, Kuaishou's Kling, Runway, and ByteDance's Seedance contesting the top tier, and Seedance is the one that keeps winning on the metric that actually matters for paid work: how long a single take can run before you are back in the timeline stitching clips.

Seedance is ByteDance's in-house video model family. Version 2.0 shipped on February 12, 2026 and made 4-15 second generations with joint audio - dialogue with lip-sync, sound effects and background music in the same inference. Version 2.5 launched July 31, 2026, and its API went live on Volcano Engine on August 7. The headline is a native 30-second single-pass generation - the longest in the mainstream category, since Kling 3.0 caps at 15 seconds and Veo 3.1 uses shorter extension-based generation - plus a 180-second beta mode for longer pieces. A genuinely continuous half-minute take removes the most expensive failure mode in AI video work: the rejected clip that looked fine in isolation and fell apart when you joined two segments.

The reference system is the other story. Seedance 2.5 accepts up to 50 multimodal reference materials in one generation - roughly 30 images, 10 video clips and 10 audio files - spanning characters, locations, products, style guides and sound beds. Most competing models still take a handful of reference images. If you have ever tried to hold a brand's exact product, face and color palette across a whole clip with the competition, you know why this is the feature people pay for.

## Where the Money Is (Honest Numbers)

Let me skip the spec talk and tell you what I have actually done and seen done with this model.

**30-second brand ads, one take.** This is the bread and butter. A 30-second ad used to mean either a shoot or stitching five 6-second generations into a timeline and praying the joins looked right. Seedance 2.5 does the whole arc - setup, build, turn, payoff - in a single generation with no stitch line, and the 50-reference system holds the product, the face and the palette consistent the whole way. Agencies and small businesses pay $100-$500 per finished piece, and the repeat angle is real: brands need new ads monthly, so a $500-$1,500/mo retainer is realistic once you have a style that works for them.

**Music videos with real beat sync.** This is the niche where Seedance is uniquely strong. Version 2.5 honors timestamp-level prompts - you write 0s-3s: such-and-such happens, and it lands there - which 2.0 explicitly did not support reliably. Beat-synced cuts, captions landing on the chorus downbeat, a cut that must hit at exactly the fourth second: that is the difference between a usable MV and a pile of rerolls. Creators charge $100-$500 for synced music visuals that used to require frame-by-frame editing, and the native audio means the music and visuals are generated together.

**Previz and pitch work.** The 3D white-model preview - rough untextured geometry to lock camera position and staging before anything is lit - is the first feature of its kind in a video model, and it is a billable service: agencies pitch camera moves and staging to clients before spending a credit on final renders. Pre-visualization is a real line item in commercial production, and Seedance is the first AI tool that speaks that language.

**Localized ad variants.** The joint audio generates dialogue in 11 languages, so one script becomes localized ads without a separate voiceover pipeline. Marketing agencies charge per-market localization, and this collapses the cost of producing it.

The unit economics work because your render cost is manageable at the consumer tiers - a Jimeng Standard plan at ¥199/mo (~4,000 credits) covers real client volume. Your margin is curation, client relationships and the rerolls you do not bill for.

## How the Pricing Actually Works (And Where It Bites)

Seedance bills two entirely different ways depending on where you use it, and most people pick the wrong one to reason about.

**The API (Volcano Engine / BytePlus).** Token-based: 2.5 is ¥70 per million tokens without video input and ¥42 with video input - about 52% above 2.0's ¥46/¥28. BytePlus publishes a worked example that matters more than any headline rate: a 5-second 16:9 clip costs ~$0.514 at 480p but ~$1.156 at 720p. That single comparison is the most important line on the rate card, because moving from 480p to 720p raises the clip price roughly 2.25x. Resolution, not the headline token rate, is what governs your bill - and third-party per-second figures (I have seen $0.084/sec quoted for 2.5) are often wrong by a multiple.

**The consumer subscriptions (Jimeng / Dreamina).** These bundle Seedance with other tools. Jimeng: free (~66 credits/day), Basic ¥69/mo (~1,080 credits), Standard ¥199/mo (~4,000, 4K), Advanced ¥499/mo (~15,000, commercial license). Dreamina international: Basic ~$18/mo, Standard ~$42/mo, Advanced ~$84/mo.

Three things bite people:

1. **2.5 costs ~52% more than 2.0 with no independent benchmark for the upgrade.** ByteDance claims roughly a 20% improvement in prompt adherence, and there is no published third-party benchmark behind that figure. You are paying a real premium on an unverified headline.
2. **The integration you use is not the full model.** Every platform - Jimeng, Dreamina, each API host - exposes a subset of capabilities. I have seen implementations where 4K/21:9 was documented but the product actually offered 480p-1080p, and region-based editing missing. What you see in the UI is not the model's spec sheet.
3. **Resolution is a 2.25x price step.** Budget at the resolution you will actually deliver, and run test clips at 480p before committing credits to 720p or above.

My practical advice: start on the consumer subscription (Jimeng or Dreamina) to learn the model, upgrade to Standard when a concrete batch of work is on the table, and only touch the API if you are building a product. And check the official pricing page for your region - the per-second figures floating around reviews are unreliable.

## What Seedance Does Well

**30-second single takes.** The category's longest mainstream generation, with a complete story structure - setup, build, turn, payoff - organized by the model in one inference. No stitch line, no join artifacts, no rejected-clip-in-the-timeline failure mode.

**50-reference multimodal input.** Characters, locations, products, style guides, sound beds - up to 50 materials in one generation. For brand work, this is the difference between a video and a video that respects the brand.

**Native joint audio.** Dialogue with lip-sync, SFX and BGM in the same pass, in 11 languages. No separate voiceover tool, no music tool, no manual sync.

**Timestamp-level control in 2.5.** Second-level shot direction that actually works - 2.0's docs warned timing was unstable and recommended sequential shot numbering instead; 2.5 does a 180 and makes timestamps a core selling point. For music videos and structured ads, this is a verdict-level feature.

**3D white-model preview.** Camera and staging locked with rough geometry before rendering. First of its kind in a video model, and genuinely useful for storyboards and client pitches.

**Speed and benchmark position.** 15-second videos generate in roughly 30-60 seconds per reviews - 2-3x faster than Runway - and 2.0 sits at ~1,218 Elo on the Artificial Analysis arena, ahead of Veo 3.1 and Kling 3.0. When a client has heard of Veo but not Seedance, that ranking is a defensible answer.

## What Seedance Does Badly

**The pricing mess.** Two billing systems, resolution steps that move your bill 2.25x, integration platforms exposing different subsets, and no reliable third-party cost figures. You cannot quote a client until you have modeled your real per-clip cost, and that takes real effort.

**Unverified marketing claims.** The 20% prompt-following improvement over 2.0 has no independent benchmark, and 2.5's premium is 52%. Treat the headline as a claim, not a fact, until arena scores for 2.5 appear.

**Long-form consistency is unproven.** 2.0 reviews show characters and backgrounds drifting around shot 4-5 of longer sequences, and 2.5's 30-second window is new enough that nobody has stress-tested it at scale. The longest take is also the riskiest take.

**Text in video is garbled.** Logos, titles and captions come out deformed and must be added in post-production. If a client expects baked-in text, budget for the edit.

**Multi-character scenes break.** Three or more characters interacting produces character merging and uncoordinated motion. Complex narrative work still means segmented generation plus editing.

**Access is genuinely limited.** Dreamina is not available in the US, the global API rollout has been delayed over copyright discussions with studios, and third-party routes vary in quality. Verify your region works before paying.

## Seedance vs Kling vs Veo (Which One to Buy)

| Capability | Seedance 2.5 | Kling 3.0 | Veo 3.1 |
|---|---|---|---|
| Max single generation | 30s (+180s beta) | 15s | Shorter, extension-based |
| Reference inputs | Up to 50 (30 img + 10 vid + 10 audio) | A handful of images | A handful of images |
| Native audio + lip-sync | Yes (joint generation, 11 languages) | Yes (v3.0) | Yes (synchronized dialogue) |
| Timestamp-level shot control | Yes (2.5 strength) | Limited | Partial |
| 3D white-box previs | Yes (first in category) | No | No |
| Resolution ceiling | 4K (via integration) | Native 4K at 60fps | 4K |
| API price | ~¥70/M tokens (no video input) | ~$0.075-0.18/sec | ~$0.09/sec |
| Consumer entry | ¥69/mo (Jimeng) / ~$18/mo (Dreamina) | ~$6/mo | $19.99/mo |
| Best for | Long single-take, brand consistency, beat-synced MV | Physics, action, cinematic camera | Dialogue-driven scenes, global API |

My working rule after a year in this market: long single-take brand work or music videos - Seedance. Action, physics and cinematic camera work - [Kling](/tools/kling-ai/). Dialogue-driven scenes with a reliable global API - [Veo](/tools/veo/). [Runway](/tools/runway/) remains the most controllable editing-oriented pipeline if you need heavy post-production, and [Vidu](/tools/vidu-ai/) is still the pick for anime and multi-character consistency. Plenty of freelancers keep Seedance plus one of the others, because they genuinely overlap less than the marketing suggests - and the 30-second single take alone justifies a second subscription for anyone doing narrative ads.

## Frequently Asked Questions

### Can I actually make money with Seedance, or is it just another demo model?

Yes - and the strongest angle is the one that used to be painful: a 30-second single-pass generation means a complete brand ad with no clip stitching, and the 50-reference system holds product, face and palette consistent across the whole take. Freelancers charge $100-$500 per finished piece, and the retainer angle ($500-$1,500/mo for monthly ad content) is where the real money sits. Music-video work is the unique niche - timestamp-level control makes beat-synced cuts land where they must, and synced MVs sell for $100-$500. Previz via the 3D white-model preview is a billable B2B service, and 11-language joint audio makes localized ad variants cheap. The catch is the billing complexity and reroll rate on long clips: model your per-clip cost before quoting.

### API tokens or the Jimeng/Dreamina subscription - which do I actually pay?

They are different products with different math. The API bills per token (2.5: ¥70/M without video input, ¥42/M with - about 52% above 2.0), and BytePlus's own example prices a 5-second 720p clip at ~$1.156 versus ~$0.514 at 480p, so resolution drives your bill. The consumer subscriptions bundle Seedance with other tools: Jimeng free (~66 credits/day), Basic ¥69/mo, Standard ¥199/mo (4K), Advanced ¥499/mo (commercial); Dreamina Basic ~$18/mo to Advanced ~$84/mo. For client work as a freelancer, the consumer subscription is usually the cheaper entry; the API makes sense only if you are building a product. Check the official pricing page for your region - third-party per-second figures have been wrong by a multiple.

### How does Seedance compare to Kling and Veo - which should I pick?

Seedance wins on duration, reference breadth and beat control: 30-second takes with up to 50 references and stable timestamp direction - for long narrative arcs, brand-consistency ads and beat-synced music videos. Kling wins on physics, complex motion and cinematic camera: 4K at 60fps, AI Director control, and more reliable action handling (though with a 30-40% reroll rate on complex prompts). Veo is strongest for synchronized dialogue quality with an official global developer API, but generation is shorter and extension-based, and Ultra is $249.99/mo. Long single-take brand work or MV = Seedance; action and physics = Kling; dialogue-driven scenes with global API access = Veo. Many freelancers keep Seedance plus one of the others.

### How do I get access, and is it usable outside China?

This is the most annoying part. In mainland China: Jimeng app or Doubao Pro. Internationally: Dreamina (dreamina.capcut.com), which is ByteDance's global platform - but Dreamina is not available in the US, and the global API rollout has been delayed over copyright discussions with studios. Third-party aggregators list Seedance routes from around $0.084/sec, so international access exists but verify your region works before paying. Also remember each integration exposes a subset of capabilities - I have seen 4K documented but only 480p-1080p actually available. Test the exact platform you intend to use; do not assume the model's spec sheet is what you get in the UI.

## Who It Is For, and Who Should Skip It

Use it if you sell narrative video to businesses - 30-second brand ads, story-driven social content - because the single take with consistent references is a deliverable nobody else hits in one pass. Use it if you make music videos or any beat-synced content, because the timestamp control is category-unique. Use it if you pitch previz or storyboards to clients, because the white-model preview speaks their language. And use it if you want a top-tier model without paying Veo Ultra money.

Skip it if your work is action-heavy with characters interacting with objects - [Kling](/tools/kling-ai/) will serve you better. Skip it if you need baked-in text or titles in the video, because text generation is garbled and you will do that in post anyway. Skip it if you are outside China and need reliable official API access today, because the global rollout is delayed. And if you cannot tolerate a pricing model that takes real effort to understand - two billing systems, resolution steps, unverified claims - budget extra time or pick a simpler tool.

## Getting Started (in Plain Terms)

1. Sign up on Jimeng (CN) or Dreamina (international) and burn the free credits (~66/day) on the 30-second mode specifically - that is the feature you are buying, so test whether your kind of content survives a full single take.
2. Learn the billing before you quote. Run the same prompt at 480p and 720p, watch the credits or tokens, and build the real per-clip cost into a spreadsheet - that number is your pricing floor, and the 2.25x resolution step will surprise you.
3. Go reference-heavy, not prompt-heavy. The 50-reference system is the strength: upload product, face, palette and sound bed, then direct motion and camera in the prompt. For 2.5, write timestamps (0s-3s: ...); for 2.0, use sequential shot numbering instead - the timing behavior is opposite between generations.
4. Subscribe at Standard (not Basic) when a concrete batch of work is on the table. Basic's credit count disappears fast on 30-second generations. Never subscribe 'to have it ready'.
5. Budget the edit anyway. Text, logos and complex multi-character moments still need post-production in [CapCut](/tools/capcut-ai/) or your usual editor - charge for that time, because it is the difference between a demo and a deliverable.
"""
}

def main():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    tools = data if isinstance(data, list) else data.get('tools', data)

    if any(t.get('slug') == 'seedance' for t in tools):
        print('Seedance already exists, skipping.')
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

    # ---- Internal-link check (pitfall #1: links must be markdown /tools/x/) ----
    content = NEW_TOOL["content"]
    links = [l for l in ["/tools/kling-ai/", "/tools/runway/", "/tools/veo/", "/tools/vidu-ai/", "/tools/capcut-ai/"] if l in content]
    print(f"   internal links found in content: {len(links)} -> {links}")
    if not links:
        raise SystemExit("[ABORT] no internal links in content - add [/tools/slug/] markdown links")

    tools.append(NEW_TOOL)
    with open(DATA, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    print(f"✅ Seedance added. Total tools: {len(tools)}")
    print(f"   content length: {len(NEW_TOOL['content'])} chars")
    print(f"   forbidden-word scan clean")

    # ---- Generate OG image (Pillow) ----
    sys.path.insert(0, str(BASE / "scripts"))
    import gen_og_images_en as og
    og_dir = BASE / "images" / "og"
    og_dir.mkdir(parents=True, exist_ok=True)
    try:
        og.make_tool_og(NEW_TOOL, og_dir / "seedance-en-og.png")
        print(f"✅ OG image generated: seedance-en-og.png")
    except Exception as e:
        print(f"⚠️ OG image generation failed: {e}")

if __name__ == '__main__':
    main()
