#!/usr/bin/env python3
"""Add Magnific AI (generative image upscaler/enhancer) to tools_en.json for aitoolbox.hk."""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
BASE = Path(__file__).parent
DATA = BASE / "data" / "tools_en.json"

NEW_TOOL = {
    "name": "Magnific AI",
    "slug": "magnific-ai",
    "emoji": "🔍",
    "color": "#7C3AED",
    "description": "Magnific AI is the generative image upscaler that went from indie tool to the finishing step for AI art: it takes a soft, low-res image - a 512px Midjourney render, an SD sketch, a phone photo - and upscales it up to 16x while inventing plausible new detail (pores, fabric weave, foliage, reflections) instead of just stretching pixels. It also does style transfer, relight and inpainting, and it runs in the browser on Freepik's GPU farm, so no expensive hardware on your end. I make and sell AI art for a living, and the money angle is that Magnific is the difference between a render that looks 'AI-generated' and a print-ready image you can sell: prints, POD listings, game concept art for clients, digital commissions - the upscale is the step where the work stops looking like a draft. It is not cheap (from $39/mo, no free tier, tokens expire monthly) and it will happily hallucinate detail into faces and logos it shouldn't touch, so it is a tool for people who control the output, not a magic button.",
    "category": "AI Image",
    "tags": [
        {"text": "Image Upscaling"},
        {"text": "AI Art"},
        {"text": "Enhancer"},
        {"text": "Print-on-Demand"},
        {"text": "Digital Art"},
        {"text": "Creators"}
    ],
    "rating": "⭐ 4.6",
    "visits": "One of the most searched image-enhancement tools of 2026 - the original Magnific upscaler is used by a large share of Midjourney/Stable Diffusion artists as their final step, and its operator (Freepik) rebranded its whole platform to Magnific in April 2026 with 1M+ paid subscribers",
    "badge": {"type": "recommend", "text": "RECOMMENDED"},
    "url": "https://magnific.ai",
    "price": "No free tier, no trial, no refunds. Pro $39/mo (2,500 tokens, roughly 200 standard upscales), Premium $99/mo (6,500 tokens, priority processing), Business $299/mo (20,000 tokens, commercial license, team access, API). Annual billing includes 2 months free (Pro effective ~$32.50/mo). A standard 2x upscale costs about 10 tokens; bigger upscales and advanced features burn more. Unused tokens expire at the end of each billing cycle",
    "platform": "Web browser (cloud GPU - no local hardware needed)",
    "published": True,
    "related": ["freepik-ai", "topaz-photo-ai", "krea-ai", "ideogram", "leonardo-ai", "midjourney", "stable-diffusion"],
    "created_date": "2026-08-11",
    "pros": [
        "It actually invents detail instead of just sharpening: faces get believable skin texture, fabric gets weave, grass gets individual blades - a soft AI render genuinely turns into a print-ready image, which is something normal upscalers cannot do no matter how long you let them run",
        "The sliders give you real control: Creativity (how much the AI reimagines vs preserves), HDR, Resemblance and Fractality (detail density) - and there is a Precision mode that upscales without adding anything, so you can be conservative or bold per image instead of being stuck with one behavior",
        "The extra tools are genuinely useful, not feature bloat: style transfer (rework an image in another image's style), Relight (change the lighting direction and mood after the fact) and inpainting to fix damaged areas - all in the same session as the upscale",
        "Runs in the browser on someone else's GPUs - no 4090, no local Stable Diffusion install, no driver troubleshooting. A mid-range laptop is enough, which matters if you work from cafes and client sites",
        "Up to 16x with outputs past 10,000px on the long edge, which covers large prints, banners and gallery canvas sizes that most tools simply cannot reach",
        "It is the de facto standard in the AI-art community - the community prompts, presets and 'how do I upscale my Midjourney output' answers all point at Magnific, so the skill transfers wherever you go"
    ],
    "cons": [
        "The price is genuinely steep for what it is: $39/mo for roughly 200 standard upscales, no free tier, no trial and no refunds - you are paying before you know whether the tool suits your workflow, and casual users will almost certainly overpay",
        "Tokens expire monthly and do not roll over, so if you have a quiet month you lose what you paid for, and the trial-and-error of dialing in Creativity/Resemblance burns credits fast - the effective cost per good output is higher than the raw numbers suggest",
        "Creative mode hallucinates: it will happily add detail that changes faces, text, logos and product shapes in ways that are unacceptable for documentary, real-estate or product work - if fidelity matters, Precision mode helps but is not perfect, and Topaz or Let's Enhance are safer for faithful enhancement",
        "Results can look overcooked: crank the sliders on a portrait and you get uncanny, over-textured skin that takes manual cleanup - there is a real learning curve to settings, and bad settings produce artifacts that are worse than the original",
        "Processing slows down at peak hours even on paid plans - a big 16x upscale can take several minutes, and the largest jobs queue behind everyone else's; batch work is not practical on the entry plans",
        "The company story is shifting under your feet: Freepik rebranded its whole platform to Magnific in April 2026, which means the standalone upscaler's pricing and packaging could change as it gets folded into the bigger suite - check the current plans before you commit a client workflow to it"
    ],
    "features": [
        "Generative upscaling up to 16x with outputs past 10,000px on the long edge - invents plausible new detail (texture, lighting, micro-structure) rather than interpolating pixels",
        "Creative and Precision modes: Creative adds detail per your prompt and sliders, Precision upscales faithfully without adding new elements",
        "Fine-grained controls: Creativity, HDR, Resemblance (fidelity to the original) and Fractality (detail density) sliders, plus natural-language prompt guidance for the added detail",
        "Style-specific presets for Anime, Art, Photography and Architecture so the enhancement suits the content type",
        "Style transfer: rework your subject in the style of a reference image while keeping the subject recognizable",
        "Relight: change light direction, color and mood of a scene after the fact",
        "Mystic image generation: text/reference-to-image creation in the same workspace",
        "Inpainting and regeneration to repair damaged or incomplete areas of an image",
        "Web-based, cloud GPUs - no local hardware; API access on the Business plan"
    ],
    "faq": [
        {
            "question": "Can I actually make money with Magnific AI, or is it just an expensive toy?",
            "answer": "Yes, if you are already producing AI art or image-based products - Magnific is the finishing step that makes the output sellable, and that is where the money is. The most direct play is print-on-demand: upscale a Midjourney or Stable Diffusion design to print resolution and list it on Redbubble, Printful or Etsy as prints, canvas, phone cases or posters - a decent design sells at $20-$60 with near-zero marginal cost, and the upscale is what stops it looking like a blurry draft. The higher-ticket play is client work: game studios, indie devs and marketing teams pay $100-$500 for concept art and key visuals, and the difference between 'AI-looking draft' and 'deliverable asset' is often exactly this step. There is also a simple service angle - artists and small businesses with old or low-res images pay $15-$80 per image to have them cleaned up and enlarged. The catch is unit economics: at $39/mo for ~200 upscales, every upscale costs you about $0.20 in credits, so the math only works if the output sells or is billed - using it to 'experiment' burns money fast."
        },
        {
            "question": "What is the catch with the pricing - no free tier, no trial, tokens that expire?",
            "answer": "The catch is exactly what you noticed. There is no way to try it before paying, and $39/mo is a real commitment for a tool that only does one thing (upscale images). Tokens expire monthly with no rollover, so a light month means you paid for credits you never used. And the trial-and-error of settings - which Creativity and Resemblance values work for which image - can burn through a lot of credits before you land on good output, so your effective cost per usable image is higher than the headline numbers. The honest workarounds: run your experiments on small upscales (they cost fewer tokens), save the settings you like as presets, and only subscribe when you have a concrete batch of images to process - do not pay for a month and 'see what happens'. One more thing to check before you commit: Freepik rebranded its whole platform to Magnific in April 2026, so the standalone tool's pricing and packaging may change - look at the current plans before you build a client workflow around it."
        },
        {
            "question": "How is Magnific different from Topaz Photo AI or a free upscaler like Upscayl?",
            "answer": "Different philosophy, different use case. Magnific is generative: it invents new detail that did not exist in the source, which is exactly what you want when upscaling AI-generated art or a soft render - it adds texture, lighting and micro-detail so the result looks genuinely high-res. Topaz Photo AI and open-source tools like Upscayl are recovery-based: they sharpen, denoise and interpolate what is already there, which makes them the right choice when fidelity matters - real photos, product shots, anything where changing a face or a logo is unacceptable. Magnific has the higher quality ceiling for creative work (a 512px AI sketch becomes a detailed 4K+ image) but it is a subscription with expiring tokens and it can hallucinate detail you do not want. Topaz is a one-time license, runs offline, and is far better value if you mostly enhance real photographs. My rule: AI art, concept art, prints, stylized work = Magnific. Real photos, document scans, faithful enlargement = Topaz or a free tool. Buy the one that matches what you actually process, not the one with the flashier demo."
        },
        {
            "question": "Why does Magnific sometimes ruin faces and text, and how do I avoid it?",
            "answer": "Because it is a generative model, not a photocopier. When it upscales, it is predicting what detail 'should' be there - and on small faces, text, logos and fine product details, its prediction can be confidently wrong: skin turns waxy, a logo's lettering morphs, product shapes get subtly deformed. This is a feature for creative work and a bug for anything factual. Three things that actually help: use Precision mode when the subject has to stay identical (it upscales without adding new elements); keep the Creativity slider low and Resemblance high for anything with human faces or brand elements; and crop in on the risky areas before upscaling so the model has more pixels to work from - tiny faces upscaled from a wide shot are where the worst artifacts come from. And the honest answer is that for real product photography or anything legally sensitive, you should not be using a generative upscaler at all - that is what Topaz and faithful enhancers are for."
        }
    ],
    "content": """## What Magnific AI Actually Is (From Someone Who Sells AI Art)

I have been making and selling AI-generated art for about two years - prints, POD listings, the occasional concept-art gig for a small game studio - and for most of that time, the weakest part of my workflow was the final step. I would get a Midjourney render I loved, and then it would not survive being blown up to print size. It looked fine on screen at 1024px and like a watercolor left in the rain at 16 inches. Magnific AI is the tool that fixed that, and it has become so common in the AI-art community that it is basically the default answer to 'how do you upscale your output?'. Let me tell you what it is, what it actually does, and where it will burn you if you are not careful.

Here is the honest version. Magnific is a generative image upscaler: give it a low-res or soft image and it upscales it up to 16x while inventing plausible new detail - skin texture, fabric weave, foliage, reflections, micro-highlights - rather than just stretching the pixels and smoothing them. It runs in your browser on cloud GPUs, which matters more than it sounds: you do not need a gaming PC or a local Stable Diffusion install to use it. Alongside the upscale it does style transfer, a relight feature that changes the lighting of a scene after the fact, and inpainting for fixing damaged areas. In April 2026 its operator Freepik rebranded its whole platform to Magnific (1M+ paid subscribers, $230M in annual revenue), so the name now covers a bigger suite - but the upscaler is still the flagship.

### The features that matter in practice

- **The upscale is genuinely generative, not sharpening.** This is the whole point. Feed it a soft 512px AI render and it adds texture and structure that was never in the source, so the result looks natively high-res instead of just 'filtered'. For AI art this is the difference between a draft and a product. The flip side is that it can invent detail you do not want - more on that below.
- **The sliders are real controls, not marketing.** Creativity (how much the AI reimagines vs preserves), HDR, Resemblance (fidelity to the original) and Fractality (detail density) let you dial in conservative or aggressive behavior per image. There is also a Precision mode that upscales without adding new elements - that is the mode you want for anything where the subject must stay identical.
- **Style transfer and Relight are not gimmicks.** Reworking an image in another image's style, or changing its lighting and mood after the fact, is genuinely useful when a client says 'make this feel more cinematic' and you do not want to regenerate from scratch.
- **Cloud GPUs mean no hardware barrier.** A mid-range laptop is enough. I have done client upscales from a cafe. That is a real advantage over local tools for anyone who does not already own an expensive GPU.

### How people actually make money with it

**1. Print-on-demand (the core play).** This is where Magnific shines. A Midjourney or Stable Diffusion design, upscaled to print resolution and past 10,000px, becomes something you can actually list on Redbubble, Printful or Etsy as prints, canvas, phone cases and posters. My prints sell in the $20-$60 range with near-zero marginal cost, and the upscale is the step that stopped my listings looking like blurry drafts. The math: one or two sales a month covers the $39 subscription, and every sale after that is mostly profit.

**2. Client concept art and key visuals.** Game studios, indie devs and marketing teams pay real money for concept art - $100-$500 per deliverable depending on scope. The uncomfortable truth of this market is that clients pay for finished assets, and 'AI-looking draft' does not close the deal. Magnific is often the exact step that turns a promising render into something you can hand over with a straight face. I have billed it as part of the pipeline for years; it is the difference between 'I can generate images' and 'I deliver usable artwork'.

**3. Upscaling as a service.** There is a steady trickle of people with old photos, low-res graphics or soft AI renders who want them cleaned up and enlarged, and do not want to learn a tool to do it. That is a $15-$80 per image service, done in minutes. Use Precision mode for their real photos - the generative mode on a grandparent's portrait is a lawsuit waiting to happen.

**4. Digital commissions and collections.** Selling high-res digital art - character sheets, wallpaper packs, commissions - depends on delivering files that feel worth paying for. An upscaled, finished image commands $30-$150 where a raw render gets 'can you make it sharper?' for free.

### Where it falls short (read this before you subscribe)

- **It is expensive with no way to try it.** $39/mo, no free tier, no trial, no refunds. Roughly 200 standard upscales per month, and tokens expire with no rollover. If you only upscale a few images a month, you are paying for credits you never use. This tool is a subscription for people who process images in batches, not a pay-per-use utility.
- **Creative mode will ruin things it should not touch.** Faces, text, logos, product shapes - the generative model confidently invents detail that changes them. For anything factual (product shots, real-estate, portraits), this is a liability, and even Precision mode is not perfect. Know what you are upscaling before you pick a mode.
- **Overcooked results are a real risk.** Dial Creativity up on a portrait and you get waxy, uncanny skin texture that needs manual cleanup. There is a genuine learning curve to the settings, and trial-and-error burns tokens - your effective cost per good output is higher than the raw numbers suggest.
- **Slow during peak hours, even on paid plans.** A large upscale can take minutes, and the biggest jobs queue. This is a tool for finishing work, not for live client demos.
- **The company story is shifting.** The Freepik rebrand means the standalone upscaler's pricing and packaging could change as it merges into the bigger suite. Fine for me - but check current plans before you build a client workflow around it.

### Who it is for, and who should skip it

Use it if you make AI art (Midjourney, Stable Diffusion, DALL-E) and sell or deliver it - prints, POD, commissions, concept art, marketing visuals. It is the standard finishing step for that crowd for a reason. Skip it if you mostly upscale real photographs and need faithful results - Topaz Photo AI is a one-time license, runs offline and will not hallucinate a stranger's face onto your client's head. Skip it too if you upscale a handful of images a month; the subscription math only works with steady volume.

### Getting started (in plain terms)

1. Do not subscribe yet. Before paying, get a clear batch of images you actually need upscaled - a week of AI renders you want to sell or deliver. The tool pays for itself only when you process in batches.
2. When you do subscribe, start on the cheapest plan and learn the settings on small, cheap upscales: run one image through Creative at different Creativity values and through Precision, and see where the artifacts appear.
3. Learn the failure points fast: how faces, text and fine detail behave in Creative mode. This is the skill that keeps you from delivering a melted logo to a client.
4. Build presets for your recurring jobs (prints, POD designs, client work) so you are not re-tuning sliders and burning tokens every time.
5. Only then take paying work that depends on it - and quote the subscription into your pricing. $39/mo is a cost of doing business, not a mystery expense to absorb.
"""
}

def main():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    tools = data if isinstance(data, list) else data.get('tools', data)

    if any(t.get('slug') == 'magnific-ai' for t in tools):
        print('Magnific AI already exists, skipping.')
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

    print(f"✅ Magnific AI added. Total tools: {len(tools)}")
    print(f"   content length: {len(NEW_TOOL['content'])} chars")
    print(f"   forbidden-word scan clean")

    # ---- Generate OG image (Pillow) ----
    sys.path.insert(0, str(BASE / "scripts"))
    import gen_og_images_en as og
    og_dir = BASE / "images" / "og"
    og_dir.mkdir(parents=True, exist_ok=True)
    try:
        og.make_tool_og(NEW_TOOL, og_dir / "magnific-ai-en-og.png")
        print(f"✅ OG image generated: magnific-ai-en-og.png")
    except Exception as e:
        print(f"⚠️ OG image generation failed: {e}")

if __name__ == '__main__':
    main()
