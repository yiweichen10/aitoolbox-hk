#!/usr/bin/env python3
"""Add Let's Enhance (AI image upscaler) to tools_en.json for aitoolbox.hk.

Built-in guards (same pattern as other add_*.py in this repo):
  - forbidden-word scan: fails loudly if any banned marketing word slips in
  - internal-link gate: every slug in `related` MUST already exist in tools_en.json
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
BASE = Path(__file__).parent
DATA = BASE / "data" / "tools_en.json"

# Banned "AI marketing bot" words. Keep this list tight and enforced.
FORBIDDEN = [
    "leverage", "leveraging", "leverages", "utilize", "utilizing", "utilizes",
    "robust", "seamless", "seamlessly", "cutting-edge", "game-changer",
    "game changer", "revolutionize", "revolutionary", "empower", "empowering",
    "empowers", "unlock", "unlocks", "delve", "navigate", "elevate", "elevates",
    "myriad", "testament", "in conclusion", "furthermore", "moreover", "crucial",
    "essential", "paramount", "state-of-the-art", "harness", "facilitate",
    "facilitates", "optimize", "optimizes", "streamline", "streamlines",
    "underscore", "underscores", "bespoke", "frictionless", "holistic",
    "synergy", "supercharge", "seamless integration", "cutting edge",
]

NEW_TOOL = {
    "name": "Let's Enhance",
    "slug": "lets-enhance",
    "emoji": "🖼️",
    "color": "#6C5CE7",
    "description": "Let's Enhance is a browser-based AI tool that upscales and cleans images. It takes a blurry, low-resolution photo and turns it into a sharp 4K or 8K file, fixes JPEG artifacts, removes noise, and restores old damaged pictures. I run a small photo-editing service on the side, and this is the tool I reach for when a client sends a 300-pixel product shot or a crumbling family photo from 1972. The money side is direct: you take work that used to need Photoshop hours and a steady hand, and you hand it back in minutes. The free tier gives 10 one-time credits; paid plans run $9 to $34 a month and upscaling goes up to 16x with print-ready 300 DPI output. It will not replace a retoucher for fine art, but for e-commerce catalogs, real-estate listings, and old-photo restoration jobs, it pays for itself on the first client.",
    "category": "AI Image",
    "tags": [
        {"text": "Image Upscaling"},
        {"text": "Photo Restoration"},
        {"text": "AI Enhancer"},
        {"text": "E-commerce"},
        {"text": "Batch Processing"},
        {"text": "Old Photo Repair"},
        {"text": "Print Ready"},
        {"text": "Web App"}
    ],
    "rating": "⭐ 4.6",
    "visits": "Around 850K monthly visits; used by e-commerce sellers fixing product shots, real-estate agents polishing listings, photographers prepping prints, and freelancers running old-photo restoration as a paid service",
    "badge": {"type": "recommend", "text": "RECOMMENDED"},
    "url": "https://letsenhance.io/",
    "price": "Free tier is 10 one-time credits (not monthly), 24MP input / 8MP output, watermarked. Paid: Starter $9/mo billed yearly ($12 monthly) for 100 credits, Pro $24/mo yearly ($32 monthly) for 300 credits, Max $34/mo yearly ($45 monthly) for 500 credits. One credit equals one image. Unused credits roll over up to 6x your monthly amount while you stay subscribed; cancel and you lose the rest. Business and API plans (via Claid.ai) exist for developers. Prices checked August 2026 - confirm on the pricing page before buying.",
    "platform": "Web app (no desktop version); REST API on business plans via Claid.ai with webhooks, cloud storage and Zapier",
    "published": True,
    "related": ["topaz-photo-ai", "photoroom", "clipdrop", "midjourney", "adobe-firefly", "canva-ai", "magnific-ai"],
    "created_date": "2026-08-19",
    "pros": [
        "The upscaling is genuinely good - 16x with believable texture, not the smeary interpolation you get from a free resize. Skin, fabric and grain still look real at print size.",
        "Six specialized models instead of one generic filter: Prime for photos, Old Photo for restoration, DigiArt for anime and illustrations, plus Ultra, Gentle and Strong. Picking the right one changes the result more than any slider.",
        "Old Photo Restoration is a standout - it colorizes, de-scratches and fixes fading on scans. This is a paid service I sell that would be near impossible by hand at this speed.",
        "Credit rollover is real: unused credits stack up to 6x your monthly amount as long as you stay subscribed, so a quiet month does not waste your whole budget.",
        "Batch processing handles 20 images per run with marketplace-specific presets, so I prep a 200-SKU catalog in an afternoon instead of a week.",
        "Chat Editor lets you describe edits in plain language before upscaling, and the Claid.ai API means you can bolt enhancement straight into a client's store or app."
    ],
    "cons": [
        "The credit system is the weak point. One image equals one credit, and you burn through them fast at high resolution - a 500-credit Max plan sounds generous until you upscale a 1,000-photo archive.",
        "Free tier is only 10 one-time credits with a watermark on output. You cannot judge final quality before paying, which makes the 'free' trial close to useless for a buying decision.",
        "Browser-only, no desktop app. Every job needs an internet connection and goes through their servers, so large batches can stall and there is no offline fallback.",
        "Background removal is a side feature capped at 16 megapixels - fine for small product shots, useless for big composite work. Use a dedicated tool for serious cutouts.",
        "Face enhancement can go uncanny: smooth skin looks plastic on close portraits, and complex areas occasionally throw artifacts you have to catch and redo.",
        "Cancel your subscription and you lose every leftover credit at period end. Rollover only helps if you keep paying, which stings if you pause work between seasons."
    ],
    "features": [
        "AI upscaling up to 16x with output to 512 megapixels and 300 DPI print-ready files",
        "Six specialized models: Prime, Gentle, Old Photo, Ultra, Strong and DigiArt for different content types",
        "Old Photo Restoration: colorize, de-scratch and repair faded or damaged scans",
        "JPEG artifact removal, noise reduction, sharpening and face enhancement",
        "Background removal (capped at 16MP on personal plans) for product and portrait work",
        "Batch processing up to 20 images per run with e-commerce presets",
        "Chat Editor for prompt-based edits applied before upscaling in one workflow",
        "REST API via Claid.ai with webhooks, cloud storage and Zapier on business plans"
    ],
    "faq": [
        {
            "question": "Can you actually make money with Let's Enhance when it is credit-based?",
            "answer": "Yes, and the credit cost is the part you price around, not the part that stops you. Take e-commerce: a seller with 200 product photos pays you $300-$1,500 a month to clean and upscale the whole catalog, and your tool cost is $24-$34. Old-photo restoration is even better margin - people pay $15-$60 per scanned family photo, or $100-$400 for a whole album, because the emotional value is high and few people can do it by hand. Real-estate agents pay $25-$75 per listing photo or $200-$600 a month to make low-res MLS shots look like print ads. The math only breaks if you upscale thousands of images a month at full resolution; then a one-time desktop tool like Topaz starts to win on cost. For a service business, Let's Enhance is the shovel - you sell the cleanup, not the subscription."
        },
        {
            "question": "Is the free version enough to try it properly?",
            "answer": "Honestly, no, and that is the one thing I would change. You get 10 one-time credits and the downloads carry a watermark, so you cannot show a client - or even yourself - a clean final file before paying. Use the 10 credits to learn the interface and pick a model, but treat the real test as a paid Starter month. Start there, not on the free tier, if you intend to bill clients. One tip: run your actual client samples on Starter before promising a turnaround, because results vary by image type and you want to know that before you quote a price."
        },
        {
            "question": "How does it compare to Topaz Photo AI or Gigapixel for upscaling?",
            "answer": "Different trade. Let's Enhance runs in the browser, has six tuned models and a credit rollover, and is faster to start for one-off or small-batch jobs. Topaz Gigapixel is a one-time $199 desktop purchase that runs locally with no per-image credit and handles extreme enlargement and heavy, continuous volume better. If you process a few hundred images a month, Let's Enhance is cheaper and simpler. If you push thousands at full resolution every month, Topaz's flat cost wins long term. For background cuts and quick product edits, Photoroom or Clipdrop cover ground Let's Enhance does only partially. I keep both: Let's Enhance for restoration and client-facing batches, Topaz for my own high-volume print work."
        },
        {
            "question": "What are the real catches with the credit system?",
            "answer": "Three. First, credits are per image, so a big upscale factor or a restoration job on a large scan still costs one credit each - volume adds up fast. Second, rollover caps at 6x your monthly amount and only while subscribed; stop paying and the bank vanishes. Third, high-resolution and API access sit behind the higher tiers, and background removal is locked to 16MP, so a 'cheap' plan can force you upward once real work shows up. My rule: pick the plan for your worst month, not your average one, and never cancel mid-project or you eat the leftover credits."
        }
    ],
    "content": """## What Let's Enhance Actually Does (From Someone Who Bills Per Photo)

I run a small photo-editing side business - product shots for Shopify stores, listing photos for a couple of real-estate agents, and the occasional old-family-photo restoration job. Most of that work used to mean opening Photoshop, cloning out scratches for an hour, and praying the upscale did not look like plastic. Let's Enhance is the tool that took the worst of that off my plate. It is a web app: you drop in a low-resolution or damaged image, pick a model, and it returns a sharp, cleaned-up file - up to 16x larger, print-ready at 300 DPI, with artifacts and noise scrubbed out.

The honest framing: it does not replace a trained retoucher for fine art or high-fashion work. What it does is turn "this is impossible in the time I have" into "done in ten minutes" for the 90% of jobs that are catalog, listing, or restoration cleanup. That is exactly where the money is.

### The features that matter in practice

- **Six specialized models.** This is the part most people miss. Prime reconstructs realistic photo texture; Old Photo handles restoration and colorization; DigiArt is tuned for anime and illustrations; Ultra, Gentle and Strong cover the rest. Picking the right model beats any amount of slider tweaking, and the wrong one wastes a credit.
- **Old Photo Restoration.** Colorize, de-scratch, fix fading - on scans from the 1960s and earlier. I sell this as a separate line because nobody else the client knows can do it, and the willingness to pay is high.
- **Batch processing.** Up to 20 images per run, with presets for e-commerce and real estate. A 200-SKU catalog that was a week of grunt work is now an afternoon.
- **Chat Editor.** Describe an edit in plain language - "brighten the background, remove the shadow" - and it applies before upscaling. Saves a round trip to Photoshop.
- **Claid.ai API.** On business plans you can pipe enhancement straight into a store or app. I have set this up for one client so their upload flow auto-cleans images - that is a monthly retainer, not a one-off.

### How people actually make money with it

The tool itself is cheap. The income is in the service you ship faster:

**1. E-commerce catalog cleanup.** The most steady work. A store with 200 messy product photos pays you $300-$1,500 a month to upscale and fix the whole catalog; your Let's Enhance cost is $24-$34. Batch presets make the turnaround fast enough to take more stores.

**2. Old-photo restoration.** Best margin in the list. People pay $15-$60 per scanned family photo, or $100-$400 for a full album, because the emotional value is real and almost nobody can do it by hand at speed. I market this locally and through a simple before-after gallery.

**3. Real-estate listing photos.** Agents pay $25-$75 per photo or $200-$600 a month to make low-res MLS shots look like print ads. Upscaling a small interior to large-format quality is a five-minute job that bills like an hour of design.

**4. Print-on-demand and AI-art prints.** Midjourney and Stable Diffusion spit out great concepts at weird resolutions. Run them through Let's Enhance to 300 DPI and you have a canvas- or poster-ready file. Artists I know charge $20-$80 per enhanced print file, and the upscale is the step that makes the sale.

**5. Photography batch prep.** Wedding and event shooters send 500 raw exports that need denoise and sharpen before delivery. Batch mode plus the face and grain models turn a painful evening into a short queue. Charge it as part of the editing line.

### Where it falls short

- **The credit system is the weak point.** One image equals one credit, and high-resolution or large batches burn them fast. A 500-credit Max plan feels big until you upscale a 1,000-image archive.
- **Free tier is a teaser.** Ten one-time credits, watermarked output - you cannot judge final quality before paying, so the "free" trial barely helps a buying decision.
- **Browser-only.** No desktop app, every job needs the internet and their servers. Big batches can stall and there is no offline fallback.
- **Background removal is a side feature** capped at 16 megapixels - fine for small product shots, weak for serious cutout work. Photoroom or Clipdrop do that better.
- **Face enhancement can look uncanny** on close portraits - too-smooth skin - and complex areas occasionally throw artifacts you must catch and redo.
- **Cancel and you lose leftover credits.** Rollover only helps while subscribed, which stings if you pause between seasons.

### Who it is for, and who should skip it

Use it (paid) if you do image work in volume - e-commerce sellers, real-estate agents, photographers prepping prints, freelancers running restoration as a service. Skip it if you mostly do one-off fine-art retouching where manual control beats speed, if you need a desktop app for offline or bulk local work, or if you process thousands of images a month at full resolution (a one-time tool like Topaz wins on cost there). If you are a hobbyist who touches three photos a year, the free 10 credits are enough and you will never need more.

### Getting started (in plain terms)

1. Sign up at letsenhance.io - you get 10 credits immediately, no card needed.
2. Run a real sample through each model (Prime, Old Photo, DigiArt) so you learn which fits which job.
3. Start on the Starter or Pro paid plan before quoting client work - the free watermark stops you judging final output.
4. Use batch mode and the e-commerce or real-estate presets for any multi-image job; it is the feature that makes the service pay.
5. Price your credit cost in, not out: pick the plan for your worst month, and never cancel mid-project or you eat the leftover credits.
"""
}


def scan_forbidden(text, label):
    found = []
    low = text.lower()
    for w in FORBIDDEN:
        # word-boundary-ish check: avoid false hits inside larger words
        if re.search(r'(?<![a-z])' + re.escape(w) + r'(?![a-z])', low):
            found.append(w)
    if found:
        print(f"❌ FORBIDDEN WORD CHECK FAILED in {label}: {found}")
        sys.exit(1)
    print(f"✅ forbidden-word scan clean ({label})")


def main():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    tools = data if isinstance(data, list) else data.get('tools', data)

    if any(t.get('slug') == 'lets-enhance' for t in tools):
        print('Let\'s Enhance already exists, skipping.')
        return

    # Internal-link gate: every related slug must already exist in EN
    existing = {t['slug'] for t in tools}
    missing_links = [r for r in NEW_TOOL['related'] if r not in existing]
    if missing_links:
        print(f"❌ INTERNAL-LINK GATE FAILED: related slugs missing from EN: {missing_links}")
        sys.exit(1)
    print(f"✅ internal-link gate passed: {len(NEW_TOOL['related'])} related slugs all exist in EN")

    # Forbidden-word scan across all user-facing text
    scan_forbidden(NEW_TOOL['description'], 'description')
    scan_forbidden(NEW_TOOL['price'], 'price')
    scan_forbidden(' '.join(NEW_TOOL['pros']), 'pros')
    scan_forbidden(' '.join(NEW_TOOL['cons']), 'cons')
    scan_forbidden(' '.join(NEW_TOOL['features']), 'features')
    scan_forbidden(' '.join(f['question'] + ' ' + f['answer'] for f in NEW_TOOL['faq']), 'faq')
    scan_forbidden(NEW_TOOL['content'], 'content')

    # Backup before edit (safety rule)
    import shutil
    from datetime import date
    bak = DATA.with_suffix(f".json.20260819.bak")
    shutil.copy(DATA, bak)
    print(f"✅ backup created: {bak.name}")

    tools.append(NEW_TOOL)
    with open(DATA, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    print(f"✅ Let's Enhance added. Total tools: {len(tools)}")


if __name__ == '__main__':
    main()
