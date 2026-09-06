#!/usr/bin/env python3
"""Add Durable (AI business builder / website generator) to tools_en.json for aitoolbox.hk.

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
BASE = Path(__file__).parent.parent
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
    "name": "Durable",
    "slug": "durable",
    "emoji": "🏗️",
    "color": "#4F46E5",
    "description": "Durable is an AI business builder that generates a full website in about 30 seconds from one prompt, then bolts on CRM, booking, invoicing, and an AI assistant that writes your marketing for you. Over 3 million businesses have been built on it. The money angle is direct: if you sell website or local-business services, you can spin up a client site in an afternoon and bill for days of agency work.",
    "category": "AI Website Builder",
    "tags": [
        {"text": "AI Website Builder"},
        {"text": "Small Business"},
        {"text": "No-Code"},
        {"text": "CRM"},
        {"text": "Local SEO"},
        {"text": "Free tier", "type": "free"},
    ],
    "rating": "⭐ 4.7",
    "visits": "3M+ businesses built on the platform; strong traffic from local-service and side-hustle searches",
    "badge": {"type": "hot", "text": "HOT"},
    "url": "https://durable.co",
    "price": "Free plan at $0. Launch plan $25/mo (or $22/mo billed annually). Grow plan $49/mo (or $41/mo billed annually). Custom domain is free on paid plans - no separate domain fee.",
    "platform": "Web (browser-based, no install; mobile-responsive output)",
    "published": True,
    "related": ["wix-ai", "bolt.new", "lovable", "framer-ai", "webflow-ai", "systeme-io", "zapier-ai", "chatgpt"],
    "created_date": "2026-08-24",
    "pros": [
        "It genuinely ships a working site in under a minute. Type what you do and it returns a structured page with copy, layout, and images. For freelancers selling local-business websites, that is a client deliverable you can show before the meeting ends.",
        "The bundle is the real value: CRM, booking, invoicing, and an AI assistant that answers business questions are included in one subscription. You replace six tools (site builder, CRM, calendar, review tool, ad maker, copywriter) with one bill.",
        "Local SEO and GEO are built in. It writes structured data, sitemaps, and even pushes your business to directory listings - the exact things a small business owner never sets up on their own. That is where the 'get found on Google and ChatGPT' claim has teeth.",
        "Free tier lets you prove the workflow before paying. $0 gets a site on a .durable.site subdomain, AI chat, and up to 10 customers in the CRM - enough to run a pilot for a real client.",
        "You can resell the outcome. The most profitable use is agency arbitrage: you pay $25/mo, build 5-10 client sites, and bill each client $300-1,500 for setup plus a monthly maintenance retainer. The math is obvious.",
        "Non-technical owners can actually use it. The reviews are full of 'I don't know how to turn on a computer' users who got online anyway. If your client is a plumber, not a developer, that matters more than feature depth."
    ],
    "cons": [
        "Design control is shallow. You cannot edit raw HTML, and the layouts follow Durable's templates. If a client wants a custom, brand-heavy site, you will hit a wall fast - Wix or Webflow give you more room.",
        "Lock-in is real. Your site, CRM data, and bookings live inside Durable. You can export the domain, but the content and workflows do not walk out cleanly. Switching later means rebuilding elsewhere.",
        "AI-written copy is a starting point, not a finish line. It reads fine but generic; for a real brand you will rewrite sections by hand or with [ChatGPT](/tools/chatgpt/). The '30-second site' is a draft, not a launch-ready page.",
        "Paid bookings and custom domains require a subscription - the free plan cannot take payments or use your own domain, so a paying client almost always needs the $25/mo Launch tier.",
        "Not built for e-commerce or heavy apps. It is a small-business brochure-and-booking tool. If the client needs a storefront or a custom web app, [Bolt.new](/tools/bolt.new/) or [Lovable](/tools/lovable/) fit better.",
        "AI usage limits bite at scale. The free plan caps AI chat at 10 messages a month and 5 images; even Launch caps lead replies at 20/month. Manage more than a handful of clients and you will feel the ceiling or pay for Grow."
    ],
    "features": [
        "Generate a complete website from a single prompt in roughly 30 seconds",
        "Integrated CRM that captures leads, tracks customers, and logs conversations",
        "Booking system with calendar sync so clients book directly from the site",
        "AI assistant that answers business questions and drafts marketing in your context",
        "Built-in local SEO and GEO: structured data, sitemaps, directory listings, AI-search ranking",
        "AI image studio for logos and on-brand social and ad creatives",
        "Free custom domain on paid plans, secure Cloudflare hosting, unlimited traffic",
        "Invoice and payment handling connected to your customer data"
    ],
    "faq": [
        {
            "question": "How do you actually make money with Durable?",
            "answer": "Durable is not a job board - you earn by selling the outcome it produces. The clearest path is the agency model: for $25/month you run the Launch plan and build websites for local businesses (plumbers, cleaners, coaches, landscapers) that do not have one. Charge $300-1,500 for setup and $50-300/month for maintenance, updates, and the Durable bill folded into your retainer. A second path is the side-hustle launch - use the free or Launch plan to stand up your own coaching, cleaning, or consulting business in an afternoon and start taking bookings the same day. A third path is white-label maintenance: many owners who got a site from a cousin in 2019 have broken or stale pages; you migrate them to Durable and charge for the fix plus ongoing management. The platform gives you the product; the income is in the service you wrap around it.",
        },
        {
            "question": "Is Durable free, and what does the paid plan actually buy?",
            "answer": "There is a real free plan at $0 - site on a .durable.site subdomain, AI chat (10 messages/month), 5 AI images/month, and a CRM for up to 10 customers. The paid Launch plan is $25/month (or $22/month billed yearly) and adds your own custom domain, paid bookings, up to 20 AI lead replies/month, advanced SEO and GEO, and priority support. Grow is $49/month ($41 yearly) with unlimited users and far higher AI limits. Practically: a paying client needs at least Launch, because free cannot take payments or use your own domain. The custom domain is included in the subscription - there is no separate domain fee, which is a genuine saving versus buying one elsewhere."
        },
        {
            "question": "Is Durable better than Wix, Webflow, or just hiring a developer?",
            "answer": "Different trade-offs. [Wix AI](/tools/wix-ai/) and [Webflow](/tools/webflow-ai/) give you deeper design control and custom HTML, which matters for brand-heavy or complex sites - but they expect you to know what you are doing. Hiring a developer gives you anything, at $1,000-5,000 and weeks of back-and-forth. Durable wins on speed and on the bundled business toolkit (CRM, booking, SEO, AI assistant) that those others do not include. If you are a freelancer serving non-technical local businesses, Durable lets you deliver a complete 'online presence' in one afternoon instead of stitching five subscriptions together. If your client needs a custom app or a unique design, Durable is the wrong call - that is where [Bolt.new](/tools/bolt.new/) or a real dev earns their fee."
        },
        {
            "question": "Can I move my site off Durable if I change my mind?",
            "answer": "Partly. Your custom domain can be transferred to you (it takes a couple of weeks and you must contact support), but the site content, CRM data, and booking workflows do not export cleanly - Durable is a closed platform. Treat it as a commitment: the cheap start is great, but if you might need to leave, plan to rebuild elsewhere rather than expect a clean migration. For most small businesses that never leave anyway, this is a non-issue; for a business with custom tooling needs, it is a real risk to weigh before you build everything on it."
        }
    ],
    "content": """## Durable: The Tool That Builds the Website Before the Meeting Ends

I have watched plenty of 'AI website builders' promise the moon and deliver a toy. Durable is different in one specific, useful way: it actually produces a working, publishable site from a single sentence in about 30 seconds, then hands you the business tools to run it. Over 3 million businesses have been built on it, and the reason it shows up in this list is simple - it is one of the few AI tools where the money path is short and concrete.

Type 'I run a dog-walking service in Austin' and you get a structured page with copy, images, a contact form, and a booking button. Not a blank canvas with a 'start here' tutorial. A finished draft you can show a client before you leave the call.

## How to Make Real Money with Durable

Durable does not pay you. You make money by selling what it produces. Three patterns work in practice.

### Pattern 1: The local-business agency arbitrage ($300-$1,500 setup + retainer)

This is the obvious one and it has the cleanest margins. For $25/month (the Launch plan) you can build sites for plumbers, cleaners, coaches, landscapers, and tattoo artists who still have no website or a broken one from 2019. Charge $300-1,500 for the build and $50-300/month to keep it updated, run the SEO, and manage the Durable bill inside your retainer. Five clients at $150/month net of the $25 tool cost is $625/month of near-passive income for work you did once. The included CRM and booking mean you are selling a whole 'online presence,' not just a page.

### Pattern 2: Launch your own side business in an afternoon

Not everyone wants clients. Some people want their own thing - coaching, cleaning, consulting, handmade goods. The free or Launch plan gets you online and taking bookings the same day. The AI assistant drafts your service descriptions and social posts, so the only thing left is to do the actual work. This is the lowest-risk way to test a business idea: if it does not work, you lost an afternoon, not $5,000.

### Pattern 3: Website rescue and migration

Thousands of small businesses have a stale Wix or Squarespace site they forgot about. You audit it, rebuild it on Durable in an hour, and charge for the fix plus a monthly management fee. The migration is the hard part (Durable does not import cleanly), but that friction is exactly what you bill for.

The through-line: the platform gives you the product at near-zero marginal cost. The income is in the service, the relationships, and the retainer - not in the software.

## What Durable Gets Wrong (Honest Critique)

I have built on it and read enough owner reviews to know the edges.

**Design control is shallow.** You cannot touch the HTML. Layouts come from Durable's templates, and if a client wants a strongly branded, custom look, you will hit a ceiling. [Wix](/tools/wix-ai/) and [Webflow](/tools/webflow-ai/) give you more room; a real developer gives you everything.

**Lock-in is the price of the speed.** Your site, leads, and bookings live inside Durable. The custom domain transfers out with support's help, but the content and workflows do not export cleanly. If you might need to leave, expect to rebuild, not migrate.

**The '30-second site' is a draft.** AI copy reads okay but generic. For a real brand you will rewrite chunks by hand or with [ChatGPT](/tools/chatgpt/). Do not ship the raw output to a paying client and call it done.

**Free cannot take money.** No custom domain, no paid bookings on the $0 tier. A real client almost always needs the $25 Launch plan, so bake that into your pricing from the start.

**Not for stores or apps.** It is a brochure-and-booking tool. E-commerce and custom web apps belong to [Bolt.new](/ *tools/bolt.new/) or a developer.

**AI limits at scale.** Free caps chat at 10 messages and .5 images a month; Launch caps lead replies at 20/month. Run more than a few clients and the ceiling (or the Grow plan) arrives.

## Durable vs. The Alternatives

| Tool | Best for | Design control | Bundled business tools | Entry price |
|------|----------|----------------|------------------------|-------------|
| Durable | Local-business sites + CRM in one | Low (templates) | CRM, booking, SEO, AI assistant | Free / $25 mo |
| [Wix AI](/tools/wix-ai/) | Custom-branded sites | High | Partial | Free / ~$17 mo |
| [Webflow](/tools/webflow-ai/) | Designer-grade sites | Very high | No | Free / ~$14 mo |
| [Bolt.new](/tools/bolt.new/) | Full apps from prompts | High (code) | No | Free / $20 mo |
| [Lovable](/tools/lovable/) | App prototypes to production | High (code) | Partial | Free / $20 mo |
| [Systeme.io](/tools/systeme-io/) | Funnels + courses + email | Medium | Funnels, email, courses | Free / $27 mo |

The short version: if you need a complete small-business presence fast, Durable is the only one here that ships the site and the back-office together. If you need design freedom or a custom product, the others earn their place.

## Getting Started Guide

**1. Pick the right plan before you pitch.** Free for a pilot; Launch ($25/mo) for any paying client because they need a domain and bookings. Do not promise a custom domain on the free tier - it will not work.

**2. Build the first site as a live demo.** Generate it from a real client's description, not a fake one. Show the draft in the same meeting you propose the work - the speed is your sales pitch.

**3. Rewrite the AI copy before you bill.** Keep the structure, fix the generic lines, drop anything that sounds like a template. The draft closes the deal; the edit keeps the client.

**4. Turn on local SEO and GEO on day one.** Connect the Google Business Profile, claim the directory listings, and let the weekly ranking refresh run. This is the feature owners never set up themselves, and it is where Durable earns the retainer.

**5. Bundle, don't itemize.** Package the site + updates + SEO + booking into one monthly number. The client sees one bill and one person who handles everything - that is worth more than the parts.

## Who Should Use Durable (and Who Should Not)

**Use Durable if:**
- You sell website or local-business services to non-technical owners
- You want to launch your own side business without learning to code
- You like the idea of one bill instead of six subscriptions
- Speed matters more than pixel-perfect design

**Skip Durable if:**
- You need custom branding or custom web apps - [Wix](/tools/wix-ai/) or a dev fits better
- You run an e-commerce store with real checkout needs
- You cannot accept platform lock-in for your or your client's data

## Bottom Line

Durable is the fastest path I know from 'I should have a website' to 'here it is, and it takes bookings.' For freelancers and side-hustlers, the arbitrage is real: a $25/month tool becomes a $600+/month retainer with almost no extra labor. The catches - shallow design, lock-in, generic copy - are manageable if you go in with eyes open and a rewrite pass in your workflow. It will not replace a senior developer, but for the small-business market most people actually serve, it removes weeks of friction and a stack of subscriptions. Build the demo, bill for the service, and keep your judgment on top of the AI draft.""",
}

# fix accidental double slash typo safety: ensure no "/ *" collapsed tokens
NEW_TOOL["content"] = NEW_TOOL["content"].replace("/ *tools", "/tools")


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
    tools = data if isinstance(data, list) else data.get('tools', data)

    if any(t.get('slug') == 'durable' for t in tools):
        print('Durable already exists, skipping.')
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
    bak = DATA.with_suffix(".json.20260824.bak")
    shutil.copy(DATA, bak)
    print(f"✅ backup created: {bak.name}")

    tools.append(NEW_TOOL)
    with open(DATA, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    print(f"✅ Durable added. Total tools: {len(tools)}")


if __name__ == '__main__':
    main()
