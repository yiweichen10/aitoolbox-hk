#!/usr/bin/env python3
"""Add AIPRM (ChatGPT/Claude prompt library) to tools_en.json for aitoolbox.hk."""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
BASE = Path(__file__).parent
DATA = BASE / "data" / "tools_en.json"

NEW_TOOL = {
    "name": "AIPRM",
    "slug": "aiprm",
    "emoji": "💬",
    "color": "#8B5CF6",
    "description": "AIPRM is a browser extension that drops 5,400+ community-built prompts straight into the ChatGPT and Claude sidebars, so you stop writing prompts from scratch and start picking from templates that already work. I use it daily for client work - SEO articles, ad copy, product descriptions, email sequences - and the honest take is that it does not make the AI smarter, it makes the person driving the AI faster and more consistent. Free tier is permanent and includes the whole public library; paid plans add private prompts, custom lists, tone control, team sharing and live web crawling. The money angle is simple: a freelancer or agency that bills by the deliverable can turn around the same volume of content in a third of the time, and the private prompt library becomes a real asset you keep and reuse across clients.",
    "category": "AI Writing",
    "tags": [
        {"text": "Prompt Library"},
        {"text": "ChatGPT"},
        {"text": "Claude"},
        {"text": "Chrome Extension"},
        {"text": "Content Creation"},
        {"text": "SEO"},
        {"text": "Copywriting"},
        {"text": "Team Collaboration"}
    ],
    "rating": "⭐ 4.4",
    "visits": "2,000,000+ users and 5,400+ public prompts; used by solo freelancers, SEO agencies, e-commerce sellers and in-house marketing teams who want consistent AI output without re-teaching the model every session",
    "badge": {"type": "recommend", "text": "RECOMMENDED"},
    "url": "https://www.aiprm.com/",
    "price": "Free plan is permanent and includes the full public prompt library (with ads and a small private-prompt cap). Paid plans: Plus ~$10/month, Pro ~$33-39/month, Elite ~$79-99/month, Titan ~$999/month, Team ~$199/month (5 seats), Business ~$499/month (15 seats). Annual billing adds two free months. No refunds, no discount codes - what you see on the pricing page is what you get. Your ChatGPT/Claude subscription is separate; AIPRM only organizes the prompts you feed them",
    "platform": "Chrome, Edge and Firefox extension; works inside ChatGPT, Claude and compatible AI chat UIs (Midjourney, DALL-E, Leonardo via model-specific templates)",
    "published": True,
    "related": ["jasper", "copy.ai", "frase", "wordtune", "anyword", "semrush-ai"],
    "created_date": "2026-08-08",
    "pros": [
        "The 5,400+ prompt library is genuinely useful out of the box - SEO articles, ad copy, product descriptions, cold emails, buyer personas - and most of them beat what you will type yourself on the first try",
        "Free tier is not a 7-day trap: it stays free forever with the whole public library, which is rare for a tool in this niche",
        "Private prompts and custom lists are where the real value sits for working professionals - you build your own library once, then reuse it on every client without retyping anything",
        "Team plans standardize output: when five writers share the same private prompts, the agency voice stops drifting from person to person",
        "Power Continue and tone/writing-style selectors remove the most annoying part of ChatGPT work - the 'now make it shorter / now make it sound more formal' back-and-forth",
        "Live web crawling lets you paste a URL into a prompt and have the AI read the actual page - huge for competitor analysis and content briefs"
    ],
    "cons": [
        "It does not make the model smarter. Feed a weak prompt base a weak idea and you still get generic fluff - the library raises the floor, not the ceiling",
        "Free tier shows ads and caps private prompts, and some of the best community prompts are locked behind paid tiers - annoying when a template you rely on suddenly needs Plus",
        "Pricing tiers multiply confusingly: Plus/Pro/Elite/Titan/Team/Business with overlapping limits, and no refunds if you pick wrong - read the limit table before paying",
        "It lives only inside ChatGPT/Claude UIs - it is not a standalone writing app, so your workflow is tied to the chat interface and the extension's sidebar",
        "Community prompts are uneven: anyone can publish and vote, so quality varies wildly and some templates inject the author's own brand or pitch into the output",
        "The extension adds visible clutter to the chat sidebar - power users who already have a prompt workflow may find it more noise than help"
    ],
    "features": [
        "5,400+ community prompts in the public library, searchable by category, popularity and author",
        "Private prompt templates with favorites list, hidden list and custom lists for organizing work",
        "Team collaboration: shared private lists, co-authors and multi-seat admin controls",
        "AIPRM Verified Prompts - engineered and maintained by the AIPRM team, with no ad links in output",
        "Power Continue: expand, simplify or shorten the previous AI output with one click",
        "Tone & writing style selector with customizable profiles on paid tiers",
        "Live web crawling: pull a URL's text or HTML directly into a prompt",
        "Custom GPT integration and model-specific templates for ChatGPT, Claude, Midjourney, DALL-E and Leonardo"
    ],
    "faq": [
        {
            "question": "Can you actually make money with AIPRM when the prompts are free?",
            "answer": "Yes, and that is the main reason I still use it. The prompts are free, but your time is not. A freelancer billing $50-$200 per SEO article or ad copy deliverable can finish the same brief in a third of the time using a proven template, which means more billable projects per week. The bigger play is the private prompt library: spend a weekend writing prompts for one niche - say e-commerce product descriptions or real estate listings - and you now own a repeatable asset. Agencies charge $500-$2,000 to set up a custom prompt system for a client who keeps forgetting how to talk to ChatGPT, and AIPRM is the delivery vehicle: shared team lists, standardized voice, and a handover document that is actually usable. The tool is the shovel; the system you build with it is what clients pay for."
        },
        {
            "question": "Is the free version enough, or do I need a paid plan?",
            "answer": "For a solo user, the free plan is genuinely workable for a long time: you get the entire 5,400+ public library forever. The limits hit you in three places: private prompt templates (the free cap is small), custom lists, and ads. The moment you start building your own library and organizing it by project - which is when AIPRM stops being a template dump and becomes a workflow - you will want Plus or Pro. My advice: start free, and upgrade only when you hit the private-prompt ceiling, not before. Do not buy Elite or Titan on day one; most people never need those limits."
        },
        {
            "question": "How is AIPRM different from just asking ChatGPT to write my copy?",
            "answer": "Two differences that matter in practice. First, consistency: a tested template produces the same structure, tone and format every time, so you are not rolling the dice on a fresh prompt each session. Second, it saves the tuning loop - the 'make it shorter, more formal, add a CTA' back-and-forth gets compressed into built-in controls like Power Continue and the tone selector. The honest caveat: for one-off creative writing, a well-written custom prompt beats any generic template. AIPRM wins on volume and repeatability, which is exactly what client work is."
        },
        {
            "question": "Does AIPRM work with Claude, or is it ChatGPT-only?",
            "answer": "It works with both. The extension supports ChatGPT and Claude side by side, and there are model-specific template sets - the same library is offered for Claude with prompts tuned to how Claude behaves. There are also templates for image models like Midjourney, DALL-E and Leonardo. One catch worth knowing: the extension injects its sidebar into the chat UI, so if the model's interface changes (which happens often), prompts can briefly break until the AIPRM team ships an update - a minor annoyance, not a blocker."
        }
    ],
    "content": """## What AIPRM Actually Is (From Someone Who Bills by the Deliverable)

I write content for clients who pay per article and per ad set, so my whole business runs on one question: how fast can I turn a brief into something that does not need a rewrite? AIPRM is the tool I keep going back to for that exact problem. It is a browser extension that adds a sidebar of 5,400+ pre-built prompts to ChatGPT and Claude. You pick a template - 'SEO blog article', 'Facebook ad copy', 'product description', 'cold email' - it fills the chat with a structured prompt, and you run it. That is the whole trick. No prompt engineering course required.

The catch, and it is a real one: AIPRM does not make the AI smarter. If you feed it a thin brief, you get thin output, same as always. What it does is remove the two biggest time sinks in client work - writing a good prompt from scratch and then tuning the output for ten minutes. A proven template gets you 80% of the way on the first run, and Power Continue plus the tone selector handle most of the remaining 20%.

### The core features that matter

- **The 5,400+ public library**: prompts for SEO, copywriting, marketing, sales, coding, customer service, research. Searchable by category and popularity, so the heavily-used prompts rise to the top. Quality is uneven - community prompts are user-published - but the 'AIPRM Verified' ones are maintained by their team and free of ad links.
- **Private prompts and custom lists**: this is the feature that turns AIPRM from a template dump into a workflow. You save your own prompts, organize them into lists (Copywriting, Legal, Web Dev - whatever your clients need), and reuse them forever. This is also where the upgrade pressure comes from, since free accounts cap private prompts.
- **Team sharing**: private lists can be shared with co-authors, and multi-seat plans give an admin control over what the whole team uses. If you run an agency, this is how five writers end up producing the same voice.
- **Power Continue and tone selector**: instead of typing 'make it shorter' over and over, you pick the action. Small thing, but it saves real minutes per deliverable.
- **Live web crawling**: paste a competitor's URL into a prompt and the AI reads the actual page. I use this constantly for content briefs and competitor teardowns.

### How people actually make money with it

The honest answer is that nobody pays for AIPRM itself and gets rich - the prompts are free. Money comes from what the prompts let you ship faster:

**1. Freelance content and copywriting.** The most direct path. You bill per deliverable - a $60 SEO article, a $40 Facebook ad set, a $150 landing page - and AIPRM cuts your turnaround time. More deliverables per week at the same quality is a straight income increase. The templates also catch genres you are weaker at; I would not say my cold emails improved, but I stopped staring at a blank cursor.

**2. Agency standardization.** When you have writers, designers and VA staff all touching ChatGPT, output drifts. Build one private library in the agency voice, share it with the team, and client deliverables stop needing the 'who wrote this?' pass. Agencies bill this as part of their retainer - the prompt system is an internal asset, not a subscription line item.

**3. E-commerce and dropshipping.** Product descriptions, listing optimization and ad variants are pure template territory. A seller processing 200 SKUs can generate first-draft descriptions in an afternoon instead of a week, and the tone selector keeps them consistent with the brand.

**4. Selling the system, not the tool.** The higher-margin play: small businesses know they 'should use AI' but have no idea how. A freelancer or consultant charges $500-$2,000 to set up their prompt library - research their niche, write 20-30 prompts, install the extension, train the owner - and leaves them with something they actually use. AIPRM is the delivery vehicle because the client can see and touch the prompts.

**5. Content pipelines for SEO agencies.** If you run a programmatic or link-building content operation, the prompt library standardizes briefs across writers and reduces the editing pass. That is money saved on the editing line.

### Where it falls short

- **Community prompts are a lottery.** Anyone can publish, and some templates are padded with the author's own product pitch or generic filler. Check the upvote count and the 'Verified' tag before relying on one.
- **The free tier is a teaser.** It works forever, but ads and the private-prompt cap push serious users toward Plus or Pro. The limit table across Plus/Pro/Elite/Titan/Team/Business is genuinely confusing, and there are no refunds - read it carefully before paying.
- **It is married to the chat UI.** AIPRM is a sidebar inside ChatGPT/Claude, not a standalone app. When the model's interface changes, prompts can glitch until the extension updates.
- **It does not fix bad input.** A generic template applied to a vague brief still produces generic content. The tool raises the floor, not the ceiling.

### Who it is for, and who should skip it

Buy it (or at least install the free version) if you produce content in volume - freelancers, agencies, e-commerce sellers, marketers. Skip it if you mostly write one-off creative pieces, already have a personal prompt system that works, or hate extra UI cluttering your chat. If you are a power user who writes excellent prompts from scratch, the library will feel like noise and the sidebar like clutter - you are not the target.

### Getting started (in plain terms)

1. Install the extension for Chrome, Edge or Firefox.
2. Open ChatGPT or Claude and look for the AIPRM sidebar.
3. Search the library for your niche - 'SEO', 'product description', whatever you do daily.
4. Run a top-voted template on a real task and judge the output yourself.
5. Start saving your own prompts early. The private library is the asset that compounds; the public one is just the free sample.
"""
}

def main():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    tools = data if isinstance(data, list) else data.get('tools', data)

    if any(t.get('slug') == 'aiprm' for t in tools):
        print('AIPRM already exists, skipping.')
        return

    tools.append(NEW_TOOL)
    with open(DATA, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    print(f"✅ AIPRM added. Total tools: {len(tools)}")

if __name__ == '__main__':
    main()
