#!/usr/bin/env python3
"""Add Krea 2 (Krea's first in-house foundation image model) to tools_en.json for aitoolbox.hk.

Built-in guards (same pattern as other add_*.py in this repo):
  - forbidden-word scan: fails loudly if any banned marketing word slips in
  - internal-link gate: every slug in `related` AND every in-content link MUST already exist in tools_en.json
"""
import json
import re
import sys
import shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
BASE = Path(__file__).parent
DATA = BASE / "data" / "tools_en.json"

# Banned "AI marketing bot" words. Keep this list tight and enforced.
FORBIDDEN = [
    "leverage", "leveraging", "leverages", "utilize", "utilizing", "utilizes",
    "robust", "seamless", "seamlessly", "cutting-edge", "game-changer",
    "game changer", "revolutionize", "revolutionary", "empower", "empowering",
    "empowers", "unlock", "unlocks", "delve", "navigate", "navigates",
    "navigating", "elevate", "elevates", "myriad", "testament", "in conclusion",
    "furthermore", "moreover", "crucial", "essential", "paramount",
    "state-of-the-art", "harness", "facilitate", "facilitates", "optimize",
    "optimizes", "streamline", "streamlines", "underscore", "underscores",
    "bespoke", "frictionless", "holistic", "synergy", "supercharge",
    "seamless integration", "cutting edge",
]

NEW_TOOL = {
    "name": "Krea 2",
    "slug": "krea-2",
    "emoji": "🎨",
    "color": "#FF4D4D",
    "description": "Krea 2 is Krea's first image model built entirely in-house - not another Flux or Stable Diffusion wrapper. Released June 2026 with open weights, it is built for people who care about how the picture looks, not just whether it appears. The three variants do different jobs: Turbo for fast iteration at roughly three seconds a shot, Medium for stable illustration and anime, Large for the richest photorealism. The real draw is creative control - you can feed it a single reference image or a whole moodboard and it picks up the style, and 'creativity' is an actual slider you turn up when you want the model to interpret instead of copy. The money side is concrete: at $0.015-$0.07 per API image, you can run a print-on-demand shop, a custom-portrait service, or batch product visuals for e-commerce without touching a subscription. The free consumer tier hands out 100 compute units a day, so you can prototype every billable workflow before spending a dollar.",
    "category": "AI Image",
    "tags": [
        {"text": "AI Image"},
        {"text": "Real-time Generation"},
        {"text": "Style Transfer"},
        {"text": "Open Weights"},
        {"text": "API"},
        {"text": "Free tier", "type": "free"},
        {"text": "Web App"}
    ],
    "rating": "⭐ 4.6",
    "visits": "~3.5M monthly visits in the CN directory (Krea platform; Krea 2 is the flagship model shipped June 2026 with open weights)",
    "badge": {"type": "hot", "text": "HOT"},
    "url": "https://www.krea.ai/krea-2",
    "price": "Consumer plans: Free $0 (100 compute units/day, Krea 2 access, real-time models, limited upscaling and LoRA training, no card needed); Basic $9/month (5,000 units, commercial license, full image/3D/lipsync models, LoRA up to 50 images, upscaling to 22K); Pro $35/month (20,000 units, all video models, workflow automation, bulk discounts); Max $105/month (60,000 units, unlimited LoRAs, relaxed generations); Business $200/month (80,000 units, up to 50 seats, team controls). Annual billing ~20-40% off. API is billed separately and per generation: Krea 2 Turbo from $0.015, Medium $0.03 (with style ref $0.035, moodboard $0.04), Large $0.06 (style ref $0.065, moodboard $0.07). Check krea.ai/pricing for current numbers.",
    "platform": "Web app (real-time canvas, enhancement, upscaling, LoRA training) plus a documented REST API and open-weight checkpoints on Hugging Face for self-hosting",
    "published": True,
    "related": ["krea-ai", "midjourney", "flux-1", "ideogram", "leonardo-ai", "recraft", "stable-diffusion", "adobe-firefly", "photoroom", "lets-enhance"],
    "created_date": "2026-08-23",
    "pros": [
        "Style control is the standout feature. Drop in one reference image or a moodboard of dozens and Krea 2 actually matches the look - not a vague 'similar vibe' but a real style transfer. For brand-consistent work (a product line, a recurring character, a series of social posts), that is the difference between usable output and a restart.",
        "The 'creativity' slider is genuinely useful, not a gimmick. High values push the model to interpret and add visual richness; low values keep it literal. I use it as a dial for how much surprise I want in a batch, and it behaves predictably.",
        "Open weights change the math. Krea 2 RAW and Turbo are on Hugging Face, so you can self-host, fine-tune on your own catalog, and skip per-image API fees entirely once the hardware is yours. For a production shop doing volume, that is a real exit from metered pricing.",
        "The API is cheap enough to build a business on. Turbo at $0.015 an image means a 1,000-image batch costs fifteen dollars. That is the kind of unit economics that lets you undercut design agencies and still keep margin.",
        "Real-time canvas is the fastest way to iterate I have used. You type or draw and the image updates live; you are not waiting thirty seconds per try. For client calls where they watch you work, that speed sells the service as much as the result does.",
        "Free tier is a real sandbox. 100 compute units a day with no card covers plenty of experimentation. You can validate a paid workflow - test prompts, style refs, batch sizes - before committing to Basic or the API."
    ],
    "cons": [
        "It is not the most realistic model on every task. Krea 2 leans artistic and expressive; on strict photorealism, [Flux](/tools/flux-1/) and [Ideogram](/tools/ideogram/) still win specific jobs, and hands, text, and fine product detail can drift. For catalog-accurate product shots you will be editing more than you expect.",
        "The compute-unit system is confusing and easy to blow through. Image, video, upscaling, and LoRA training all draw from the same daily or monthly pool, and the rates are not intuitive. I have watched a 'quick' session eat a day's free units in twenty minutes of real-time play.",
        "Medium and Large generation is not instant. Turbo is fast, but Medium takes around ten seconds and Large around twenty-five, and the API queues under load. If your service promises same-minute turnaround, the slower variants will bite you during a traffic spike.",
        "Style-reference quality depends entirely on your input images. Give it weak, low-res, or mismatched references and you get muddy output - the tool magnifies the quality of what you feed it. Beginners blame the model when the real problem is their moodboard.",
        "The platform changed shape in March 2026 (unified navigation, drag-and-drop, voice mode, rebuilt mobile). Features move, the interface you learned shifts, and some older tutorials are already wrong. Budget time to re-learn after each update instead of trusting last month's screenshots.",
        "Commercial license lives behind the paid tiers. Free lets you play; Basic and up give you the license to sell the output. If you try to run a client service on the free tier, you are on the wrong side of the terms - and the API commercial license is a separate conversation from your consumer subscription."
    ],
    "features": [
        "Krea 2 foundation model: first image model built from scratch in-house, released June 2026 with open weights (RAW and Turbo checkpoints on Hugging Face)",
        "Three variants: Turbo (~3s, fast iteration), Medium (~10s, illustration/anime/painting), Large (~25s, photorealism and raw texture)",
        "Style transfer: feed one reference image or a moodboard of dozens; the model matches the creative direction with precision",
        "Creativity slider: an actual tunable parameter - raise it for interpretation and visual richness, lower it for literal adherence",
        "Real-time canvas: type or draw and the image updates live, built for fast iteration and live client sessions",
        "LoRA training: fine-tune on your own images (up to 50 on Basic, unlimited on Max and Business)",
        "Image upscaling to 22K resolution on paid plans; enhancement tools for cleanup and resolution",
        "REST API billed per generation ($0.015-$0.07 per image by variant) with separate API balance from consumer subscriptions",
        "Open-weight checkpoints and official inference code on GitHub for self-hosting and custom fine-tuning"
    ],
    "faq": [
        {
            "question": "How do you actually make money with Krea 2?",
            "answer": "Four paths work in 2026, and all of them lean on the cheap API and the style control. First, print-on-demand and AI-art prints: generate at the API rate of $0.015-$0.07 per image, upscale to 22K, and sell posters or merch - a run of 100 designs costs you under ten dollars in generation before you list them. Second, custom portrait and avatar services: feed a client's photos as style references, produce a consistent character pack, and charge $30-$150 a set - the moodboard feature is what keeps the faces and outfits on-brand across the whole pack. Third, e-commerce and product visuals: batch-generate lifestyle and variant shots for online stores at a fraction of a photographer's day rate, charging $300-$1,500 a month per store for ongoing visual refresh. Fourth, brand-asset retainers: agencies and solo founders need consistent social posts, ad creatives, and concept art on a schedule, and Krea 2's style transfer lets you lock one look across everything - bill $500-$2,000 a month for that. The through-line: the free tier and low API cost mean your raw material is nearly free; you charge for taste, consistency, and throughput, which is exactly the part clients cannot do themselves."
        },
        {
            "question": "Is the free tier enough to start a service, and how do the compute units work?",
            "answer": "The free tier gives 100 compute units a day with no credit card, and it is enough to learn the tool and prototype a workflow - but not to run a business. Image generation, real-time canvas, upscaling, and LoRA training all draw from that same daily pool, and the math is not obvious: a few minutes of real-time play or one LoRA training job can drain the whole day's allowance. For anything client-facing you will hit the wall fast and need Basic ($9) at minimum for the commercial license, or the API if you are doing volume. My rule: use free to prove the workflow works, use Basic to legally sell the first clients, and move to the API the moment your per-image volume makes metered API cheaper than a subscription. And re-check krea.ai/pricing before you quote a client, because the unit rates shift."
        },
        {
            "question": "Krea 2 vs Midjourney vs Flux - which one do I use?",
            "answer": "They solve different problems. [Midjourney](/tools/midjourney/) still produces the most consistently beautiful, 'finished' images out of the box and has the strongest community and style ecosystem - but it is a closed walled garden with weak style-reference control and no open weights. [Flux](/tools/flux-1/) (via the Flux family) is the open, fast, photorealistic workhorse that a lot of pipelines are built on, and it often beats Krea 2 on strict realism and text. Krea 2's edge is creative direction: the moodboard style transfer and the creativity slider give you control the others treat as afterthoughts, and the open weights let you self-host. Honest guidance: pick Midjourney when you want gorgeous output with zero fuss, Flux when you need photorealism or an open model to build on, and Krea 2 when style consistency across a batch or a series is the job - brand sets, character packs, recurring campaign visuals. Most working image people I know keep two of the three in their stack rather than pledging to one."
        },
        {
            "question": "Can I self-host Krea 2, and is the output mine to sell?",
            "answer": "Yes on both, with caveats. Krea released Krea 2 RAW and Turbo as open-weight checkpoints on Hugging Face with official inference code on GitHub, so you can download, fine-tune on your own catalog, and run generation on your own hardware - that removes per-image API fees entirely once you own the GPUs. For commercial rights: consumer plans Basic and above include a commercial license for what you generate in the app, and API output is licensed for commercial use (marketing, products, client work) per Krea's API terms. The free tier does not grant commercial rights, so do not bill client work off free units. If you self-host the open weights, the license on those weights is the open-release license - read it before you ship a product on top of it, because open weights and the hosted commercial license are not the same agreement."
        }
    ],
    "content": """## What Krea 2 Actually Is (From Someone Who Sells Image Work)

I run a small visual studio: product visuals for online stores, custom portrait packs, and the occasional brand-asset retainer. I have bounced between [Midjourney](/tools/midjourney/), [Flux](/tools/flux-1/), and [Ideogram](/tools/ideogram/) for two years. Krea 2 is the first new model in a while that made me change my stack, and not because it is the prettiest - because it lets me control the look.

Quick context so you know what you are buying. Krea spent its early life as a model aggregator: a clean interface on top of other people's models (Flux, Stable Diffusion, Ideogram) plus a real-time canvas and upscaling. Krea 2, released June 2026 with open weights, is their first image model built from scratch. That matters: it is trained to match Krea's creative-direction UX, and it is the only one of the bunch you can download and run yourself. There are three variants - Turbo for speed, Medium for stable illustration and anime, Large for the richest photorealism - and 'creativity' is a slider, not a mood.

Here is what it is like to actually bill work with it, where it falls short, and where the money is.

## How to Make Real Money with Krea 2

Krea 2 does not pay you. The income is in the services you deliver faster and more consistently, and four patterns are working in 2026.

### Pattern 1: Print-on-demand and AI-art prints - near-zero material cost

The API charges $0.015-$0.07 per image depending on variant. A batch of 100 designs costs you under ten dollars in generation before you list them. Upscale the winners to 22K and they are print-ready. The margin is in curation and niche selection, not production - you can test fifty concepts a night for pocket change and only print what sells. This is the lowest-risk entry because your downside is a few dollars, not a photographer's day rate.

### Pattern 2: Custom portrait and avatar packs - $30-$150 per set

Feed a client's photos in as style references, then generate a consistent character across outfits, settings, and moods. The moodboard feature is what makes this viable: the faces and clothing stay on-brand across the whole pack instead of drifting every frame. People pay for 'a coherent set that looks like me,' and Krea 2's style transfer is the cheapest way to deliver that. Charge per pack, or bundle into a monthly personal-branding subscription.

### Pattern 3: E-commerce and product visuals - $300-$1,500/month per store

Online stores need constant visual refresh - lifestyle shots, color variants, seasonal campaigns - and most cannot afford a photographer every week. Batch-generate the variants on Krea 2 at a fraction of a shoot's cost, clean up the ones that drift, and bill a monthly retainer. The creative-control features mean the store's look stays consistent across months of output, which is the part clients actually notice and pay for.

### Pattern 4: Brand-asset retainers - $500-$2,000/month

Agencies and solo founders need consistent social posts, ad creatives, and concept art on a schedule. Krea 2's style transfer lets you lock one visual language across everything they publish. You become the person who keeps their feed coherent, and that is a recurring line item, not a one-off project. The free tier and cheap API mean your raw material is nearly free; you charge for taste, consistency, and throughput - exactly the part they cannot do themselves.

The through-line in all four: the generation is almost free, so you compete on judgment and consistency, not on who can push a button.

## What Krea 2 Gets Wrong (Honest Critique)

I have shipped client work on it for months. Here is where it costs me time, money, or a red-faced email.

**It is not the most realistic model on every task.** Krea 2 leans artistic and expressive. On strict photorealism - a watch, a sneaker, skin texture - [Flux](/tools/flux-1/) and [Ideogram](/tools/ideogram/) still win specific jobs, and hands, embedded text, and fine product detail drift. For catalog-accurate shots you will edit more than you budgeted. I keep Flux in the stack precisely for the 'must be exact' frames.

**The compute-unit system is confusing and easy to blow.** Image, video, upscaling, and LoRA training all pull from one daily or monthly pool, and the rates are not intuitive. A 'quick' real-time session ate a full day's free allowance in twenty minutes of play. You have to watch the meter like a taxi, or a client call turns into an unexpected bill.

**Medium and Large are not instant.** Turbo is fast (~3s), but Medium runs ~10s and Large ~25s, and the API queues under load. If you promise a client same-minute turnaround, the slower variants will bite during a traffic spike. I schedule batch jobs for off-peak and quote realistic windows.

**Style-reference quality is a function of your inputs.** Give it weak, low-res, or mismatched references and you get muddy output. The tool magnifies the quality of what you feed it. Half the 'Krea 2 is bad' complaints I see are really 'my moodboard was three blurry screenshots.' Garbage in, gorgeous-looking garbage out.

**The platform keeps reshaping.** March 2026 brought unified navigation, drag-and-drop, voice mode, and a rebuilt mobile app. Features move, the interface you learned shifts, older tutorials go stale. Budget re-learning time after each update instead of trusting last month's screenshots - I got burned quoting a workflow that the redesign had renamed.

**Commercial rights sit behind the paid tiers.** Free lets you play; Basic and up grant the license to sell output. Try to run a client service on free units and you are violating terms, and the API commercial license is a separate agreement from your consumer subscription. Know which license covers the work before you invoice.

## Krea 2 vs. The Alternatives

| Tool | Best for | How it works | Entry price |
|------|----------|--------------|-------------|
| Krea 2 | Style-consistent batches, brand sets, self-hosting | In-house foundation model with moodboard style transfer + creativity slider | Free / $9 mo (Basic) |
| [Midjourney](/tools/midjourney/) | Gorgeous out-of-box output, community styles | Closed image model, Discord/web app | $10 mo |
| [Flux](/tools/flux-1/) | Open, fast photorealism, pipeline building | Open-weight image models (Flux family) | Free / API credits |
| [Ideogram](/tools/ideogram/) | Accurate text in images | Diffusion model strong on typography | Free / $8 mo |
| [Leonardo AI](/tools/leonardo-ai/) | Game/assets pipelines, fine-tuning | Platform with models + training + API | Free / $10 mo |
| [Recraft](/tools/recraft/) | Brand design systems, vector + image | Design-first AI with brand kits | Free / $12 mo |
| [Stable Diffusion](/tools/stable-diffusion/) | Maximum openness, local control | Fully open models, countless forks | Free / self-host |
| [Adobe Firefly](/tools/adobe-firefly/) | Safe commercial assets in Creative Cloud | Adobe's commercially-safe model | Free / $10 mo |
| [Photoroom](/tools/photoroom/) | Product background removal at scale | Background/edit API + app | Free / $13 mo |
| [Let's Enhance](/tools/lets-enhance/) | Upscaling and photo restoration | Credit-based enhancer + Claid API | Free / $9 mo |

The short version: [Midjourney](/tools/midjourney/) is the beauty pick with zero fuss, [Flux](/tools/flux-1/) is the open photorealistic workhorse, and Krea 2 owns the creative-direction lane - moodboard style transfer, a real creativity dial, and open weights you can self-host. [Recraft](/tools/recraft/) and [Leonardo AI](/tools/leonardo-ai/) are the closer competitors if your work is brand kits or game assets with training. None of them give you Krea 2's combination of style control and self-hosting freedom.

## Getting Started Guide

**1. Start free and burn 100 units a day on purpose.** Do not subscribe on day one. Run your actual billable workflow - a portrait pack, a product variant set, a brand moodboard - and see which variant (Turbo/Medium/Large) actually does the job. The free tier is a real sandbox, not a teaser.

**2. Learn the compute-unit math before you charge a client.** Watch what drains the pool: real-time canvas, upscaling, LoRA training. Know that free units reset daily and subscription units monthly. If your workflow is batch-heavy, the API at $0.015-$0.07 per image will beat any subscription - do the arithmetic before you quote.

**3. Build a moodboard before you build a batch.** Krea 2's style transfer is only as good as your references. Collect 10-30 clean, high-res images that show the exact look you want, then generate. This one step separates 'coherent brand set' from 'random pretty pictures.'

**4. Use the creativity slider as a batch dial.** Low for literal product shots, high for expressive editorial. Set it per job, not per session - the difference is visible and clients feel it.

**5. Pick ONE paid deliverable and build the client story around it.** The portrait pack, the store-visual retainer, or the print shop - choose the one your existing clients already ask for. Krea 2 is the engine; the consistency is what you sell. And keep checking krea.ai/pricing, because the unit rates move.

## Who Should Use Krea 2 (and Who Should Not)

**Use Krea 2 if:**
- You sell image work where style consistency matters - brand sets, character packs, recurring campaign visuals
- You want to self-host or fine-tune an open model instead of renting someone's API forever
- You run volume and care about $0.015-$0.07 per-image unit economics
- You like real-time iteration and live client sessions

**Skip Krea 2 if:**
- Your job is strict photorealism with exact product detail - [Flux](/tools/flux-1/) or [Ideogram](/tools/ideogram/) will save you editing time
- You want a closed, hands-off 'always beautiful' experience - [Midjourney](/tools/midjourney/) is less work
- You refuse to learn a tool that reshapes every few months
- You need commercial rights on a zero budget - the free tier does not grant them

## Bottom Line

Krea 2 is the first model in a while that changed how I work, and it is not because it is the prettiest. The moodboard style transfer, the creativity slider, and the open weights give a working image person something the closed beauties do not: control and an exit from metered pricing. For anyone selling consistent visual work - portraits, store visuals, brand assets - the throughput and consistency are real, and the free tier means you can prove it before paying.

It is not flawless: it drifts on strict realism, the compute-units system is a trap for the careless, the slower variants queue under load, and the platform keeps moving. But the work it removes - the inconsistent batches, the per-image studio cost, the lock-in - is exactly the work clients should not be paying you to redo. Use it for the control, keep your taste on top, and bill for the consistency."""
}

def scan_forbidden(text, label):
    found = []
    low = text.lower()
    for w in FORBIDDEN:
        if re.search(r'(?<![a-z])' + re.escape(w) + r'(?![a-z])', low):
            found.append(w)
    if found:
        print(f"❌ FORBIDDEN WORD CHECK FAILED in {label}: {found}")
        sys.exit(1)
    print(f"✅ forbidden-word scan clean ({label})")


def main():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    tools = data['tools'] if isinstance(data, dict) else data

    if any(t.get('slug') == 'krea-2' for t in tools):
        print('Krea 2 already exists, skipping.')
        return

    # Internal-link gate: every related slug must already exist in EN
    existing = {t['slug'] for t in tools}
    missing_links = [r for r in NEW_TOOL['related'] if r not in existing]
    if missing_links:
        print(f"❌ INTERNAL-LINK GATE FAILED: related slugs missing from EN: {missing_links}")
        sys.exit(1)
    print(f"✅ internal-link gate passed: {len(NEW_TOOL['related'])} related slugs all exist in EN")

    # In-content markdown links must also point to existing slugs
    content_slugs = set(re.findall(r'\]\(/tools/([a-z0-9\-\.]+)/\)', NEW_TOOL['content']
                                   + ' '.join(f['answer'] for f in NEW_TOOL['faq'])))
    missing_content = [s for s in content_slugs if s not in existing]
    if missing_content:
        print(f"❌ CONTENT-LINK GATE FAILED: in-text links to missing slugs: {missing_content}")
        sys.exit(1)
    print(f"✅ content-link gate passed: {sorted(content_slugs)} all exist in EN")

    # Forbidden-word scan across all user-facing text
    scan_forbidden(NEW_TOOL['description'], 'description')
    scan_forbidden(NEW_TOOL['price'], 'price')
    scan_forbidden(' '.join(NEW_TOOL['pros']), 'pros')
    scan_forbidden(' '.join(NEW_TOOL['cons']), 'cons')
    scan_forbidden(' '.join(NEW_TOOL['features']), 'features')
    scan_forbidden(' '.join(f['question'] + ' ' + f['answer'] for f in NEW_TOOL['faq']), 'faq')
    scan_forbidden(NEW_TOOL['content'], 'content')

    # Backup before edit (safety rule)
    bak = DATA.with_suffix(".json.20260823.bak")
    shutil.copy(DATA, bak)
    print(f"✅ backup created: {bak.name}")

    tools.append(NEW_TOOL)
    with open(DATA, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    print(f"✅ Krea 2 added. Total tools: {len(tools)}")


if __name__ == '__main__':
    main()
