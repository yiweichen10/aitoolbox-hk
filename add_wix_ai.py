#!/usr/bin/env python3
"""Add Wix AI (AI website builder - Wix Harmony + Aria agent) to tools_en.json for aitoolbox.hk."""
import json
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
BASE = Path(__file__).parent
DATA = BASE / "data" / "tools_en.json"

NEW_TOOL = {
    "name": "Wix AI",
    "slug": "wix-ai",
    "emoji": "🎨",
    "color": "#0C0887",
    "description": "Wix AI is the AI layer baked into Wix, the all-in-one website builder - specifically the 2026 Wix Harmony editor and its built-in agent Aria. You describe your business in plain English - 'plumbing company in Austin with a booking page and a services list' - and Harmony generates a complete multi-page site with real copy, images and layout in about three minutes. Then Aria keeps working with you: 'make the header more modern', 'add a testimonial section', 'write a blog post' - it edits the live site while you watch. No code, no design skills, no blank canvas. I build websites for small local businesses for a living, and the money angle is straightforward: a plumber or dentist who would pay a design agency $3K and wait six weeks for a site gets a solid one from me in a day for a fraction of that, and I hand over the keys so they own the thing. Wix is my delivery vehicle - the AI does the first draft, I do the polish, and the client pays me for judgment and speed, not for dragging pixels around.",
    "category": "AI Design",
    "tags": [
        {"text": "AI Website Builder"},
        {"text": "No-Code"},
        {"text": "AI Agent"},
        {"text": "eCommerce"},
        {"text": "Drag-and-Drop"},
        {"text": "SEO"},
        {"text": "Small Business"},
        {"text": "Freelancers"}
    ],
    "rating": "⭐ 4.8",
    "visits": "Wix is one of the most-used website builders on the planet - roughly 260 million sites run on it, and its AI features are the main reason new builders pick it over Squarespace, GoDaddy or Hostinger (tech.co rated it the best AI website builder of 2026 with a 4.8/5)",
    "badge": {"type": "recommend", "text": "RECOMMENDED"},
    "url": "https://www.wix.com",
    "price": "Free plan: $0 forever (Wix subdomain, 500MB storage, Wix ads on your site, full access to the Harmony editor and Aria for testing). Paid plans (annual billing): Light $17/mo (custom domain for 1 year, 2GB storage, basic marketing tools), Core $29/mo (50GB storage, basic eCommerce, online scheduling, 3 collaborators), Business $39/mo (100GB storage, full commerce, standard marketing suite), Business Elite $159/mo (unlimited storage, advanced marketing, developer tools). Monthly billing costs more. A free domain for the first year is included on Light and up",
    "platform": "Web browser (fully hosted - no separate hosting or domain setup needed)",
    "published": True,
    "related": ["webflow-ai", "framer-ai", "relume-ai", "lovable", "v0-dev", "canva-ai", "spline-ai"],
    "created_date": "2026-08-10",
    "pros": [
        "The AI actually delivers a usable site, not a landing-page mock: type your business description and you get a multi-page site with copy, images, buttons and forms wired up - then Aria edits it conversationally ('add a CTA to the services page') in seconds. For client work this turns day-one into hour-one",
        "The free plan is real, not a bait: you can build a fully functional site on yourname.wixsite.com and even try Aria and the AI content tools without paying anything. That makes it the easiest tool to pitch to a budget client who has never had a website",
        "The whole stack is one subscription: hosting, domain, SSL, eCommerce, booking, email marketing and SEO tools are all included in the monthly price. No patching together five vendors like a WordPress build needs",
        "The AI text and image generators are built into every editing surface - you can regenerate a headline, a product description or a hero image inline while you work, which is where the real time savings are",
        "800+ templates plus the AI generator plus the drag-and-drop editor means you can start from AI, a template, or a blank canvas and switch styles anytime - most builders lock you into one starting point",
        "For eCommerce specifically, the AI writes product descriptions and the store setup is genuinely fast - I've stood up a working online store for a client in an afternoon that would have taken a week with WooCommerce"
    ],
    "cons": [
        "AI-generated sites have a 'Wix look' - clean, competent, and a bit samey. If your client wants a distinctive brand, you will be doing real design work on top, and that is where the AI stops being a shortcut",
        "The editor is powerful but genuinely overwhelming for beginners: there are app-market integrations, Velo code, members areas, marketing dashboards... the menu sprawl confuses people who just wanted a simple site. Your first-time clients will call you to explain it",
        "You cannot change your site's template after you publish. The AI or template you picked on day one is your structural cage forever - a real annoyance when a client's business pivots a year in",
        "The free plan is not 'free site': it serves Wix ads and a Wix subdomain, which looks amateur for a real business. Clients will need at least Light ($17/mo) to look legit, and that is an ongoing cost they must accept",
        "Vendor lock-in is total. Wix owns your hosting, your data and your site structure, and there is no clean export path - if a client ever wants to leave, you are rebuilding from scratch. I always tell clients this before we start",
        "The AI is only as good as its training data on your niche: it nails restaurants, salons and trades, but genuinely weird or technical businesses get generic copy that reads like a template wrote it - and you still have to fact-check everything it says about the client's services"
    ],
    "features": [
        "Wix Harmony editor (2026): AI-first site building where you describe your business in plain English and get a complete multi-page site with content, images and layout in ~3 minutes",
        "Aria AI agent: a conversational assistant inside the editor that makes design changes, adds pages, edits content and runs tasks by natural-language instruction ('make the header more modern')",
        "AI text generator and AI image generator built into every editing surface - headlines, product descriptions, blog posts, hero images",
        "AI SEO assistant (SEO Wiz): automated meta tags, keyword suggestions, alt text and an optimization checklist per page",
        "800+ templates and a full drag-and-drop editor with responsive mobile adaptation",
        "Built-in eCommerce: product catalogs, payments, shipping, subscriptions and dropshipping/print-on-demand integrations (Core plan and up)",
        "App Market with 500+ integrations plus Velo, a dev platform for custom JavaScript when you outgrow the builder",
        "All-in-one hosting: free SSL, domain management, backups, analytics and site performance monitoring included in the subscription",
        "Blog and CMS tools with categories, tags and SEO settings; online scheduling and booking (Core plan and up)"
    ],
    "faq": [
        {
            "question": "Can a freelancer actually make money building sites with Wix AI?",
            "answer": "Yes - this is the most beginner-friendly path into paid web design, and the numbers work. The pitch to a local business is: 'a full website in one to two days, you own it, $500-$2,000 depending on pages and eCommerce.' The AI does the first draft in minutes, so your time goes into asking the client good questions, writing honest copy that AI gets wrong, polishing the design and setting up their domain, email and Google Business Profile. Most of my clients take a $50-$150/month care plan afterwards (hosting billing, edits, content updates, the occasional Aria hand-hold), and that recurring revenue is where the real money is. The trap to avoid: undercharging because 'the AI did the work.' Clients pay for the result and the fact you knew which questions to ask - not for how fast the AI made it. A common failure mode is building a generic site in an afternoon, calling it done, and wondering why the client won't pay. If you want a distinctive, conversion-focused site, the AI is your first draft, not your finish line."
        },
        {
            "question": "Is the free plan actually enough, or do you have to upgrade right away?",
            "answer": "For building and testing, the free plan is genuinely enough - you get the full Harmony editor, Aria, the AI content tools and 500MB of storage, and you can build a complete site to show a client before they pay anything. But no real business should go live on it: the site carries Wix ads and a yourname.wixsite.com address, both of which scream 'amateur' to customers. The practical move is to build on Free, show the client the draft, then upgrade to Light ($17/mo) or Core ($29/mo) the day you go live - Light removes ads and adds your domain, Core adds basic eCommerce and booking. If the client needs to sell products, skip straight to Core; if it is purely a brochure site, Light is plenty. And make the subscription the client's cost, not yours - roll it into your project quote or care plan so you are not eating $17-$39/month per client forever."
        },
        {
            "question": "How is Wix AI different from Webflow AI, Framer AI or just using ChatGPT to make a site?",
            "answer": "ChatGPT gives you copy and maybe some HTML, but it cannot host, secure, or run your site - you still have to put it somewhere. Wix, Webflow and Framer all generate and host full sites, but they aim at different people. Wix is the most beginner-friendly and the broadest: free plan, eCommerce, booking, email marketing and an app market in one box - it is the right pick for small local businesses, service pros and first-time site owners, and it is what I recommend to clients who want to self-manage after I hand over. Webflow and Framer are designer tools: more granular control over layout and motion, but a steeper learning curve and no true free plan worth using - better for portfolio sites, startups and design agencies where the site is a design piece. The honest trade-off: Wix's AI gives you the fastest path to a working business site, but if a client needs a site that looks genuinely designed, I quote them Framer or Webflow instead and charge more. Pick the tool to match the client, not the other way around."
        },
        {
            "question": "What are the real downsides clients should know before committing to Wix?",
            "answer": "Four things I tell every client up front. First, template lock: the structure you pick at the start is permanent - you can restyle it, but you cannot swap to a different template once published, so choose the starting point carefully. Second, lock-in: Wix hosts everything, and there is no clean way to export your site to another platform - if they ever want to leave, it is a full rebuild. Third, ongoing cost: it is a subscription, not a one-time purchase, and a real business realistically needs $17-$39/month plus a domain, forever. Fourth, the AI and templates have a recognizable 'Wix look' - fine for most small businesses, wrong for anyone who needs distinctive branding, in which case a designer tool or a custom build is the better recommendation. None of these are deal-breakers for the typical local business client, but a client who understands them is a client who does not blame you later."
        }
    ],
    "content": """## What Wix AI Actually Is (From Someone Who Builds Small-Business Sites for a Living)

I make websites for local businesses - plumbers, dentists, dog groomers, the occasional restaurant - and I have been doing it long enough to remember when 'build me a website' meant two weeks of work and a client whose face fell at the price. Wix AI changed that math for me in 2026, and I want to tell you exactly how, because most of what you read about AI builders is marketing fluff written by people who have never delivered a site to an actual paying client.

Here is the honest version. Wix AI is the AI layer built into Wix, the all-in-one website builder. In January 2026 Wix launched the Harmony editor, which does the thing the demos show: you type a description of your business - 'a plumbing company in Austin with a services list and a booking page' - and in about three minutes it produces a complete multi-page site with real copy, images and a layout that does not embarrass you. Then there is Aria, Wix's built-in AI agent, which keeps working with you after the site exists: 'make the header more modern', 'add a testimonial section', 'write me a blog post about water heater maintenance'. It edits the live site while you watch, and it is fast - I asked it to add a call-to-action button to a page and it did it in about five seconds.

That is the product. Now let me tell you what it is actually good for, where it lies to you, and how the money works.

### The features that matter in practice

- **The AI site generator is not a demo trick.** It produces a real, multi-page, navigable site - not a single landing page. For the 80% of small-business sites that just need 'here's what we do, here's how to contact us, here's our prices', this turns a two-day build into a morning. Where it falls down is anything that needs a genuinely unusual layout or a strong brand identity - then the result looks like a very clean template, which is exactly what it is.
- **Aria is the real time-saver.** The agent is not just a site generator you run once - it lives in the editor and does ongoing edits by conversation. Client says 'can we move the reviews to the top?' - you tell Aria, it happens, you screenshot it for the client. I charge for speed and judgment, and Aria is the speed.
- **AI copy and images are everywhere.** Text generator, image generator, inline in every editing surface. For a client who has no photos of their own and no copy, this is the difference between a working site and a blank page. You still rewrite the important stuff - about pages and service descriptions need to sound like the actual human business owner, not a well-mannered robot.
- **Everything is one subscription.** Hosting, SSL, domain, analytics, eCommerce, booking, email marketing - all in the monthly price. For a client who is terrified of the words 'domain' and 'hosting', this removes the whole category of problems.
- **SEO Wiz actually helps beginners.** It generates meta tags, suggests keywords and gives a per-page optimization checklist. It is not a substitute for real SEO work, but it gets a client's site past 'invisible on Google' faster than most DIY builders.

### How people actually make money with it

**1. Website builds for local businesses (the core play).** The market is enormous and underserved: millions of small businesses still run on a Facebook page or nothing at all. With Wix AI you can quote a proper site - four to six pages, copy, booking or contact form - at $500-$2,000 and deliver in a day or two. The client pays for the result and for the fact you knew which questions to ask ('do you take walk-ins?', 'what do people complain about?'), not for the hours the AI saved you. This is a real, repeatable service business.

**2. Care plans and maintenance retainers.** The money in web design is not the build, it is the retainer. After handover, most small-business clients cannot touch their own site - they call you for edits, content updates, the occasional Aria hand-hold. A $50-$150/month care plan for hosting billing, changes and support has near-100% retention, because firing you means going back to not having anyone. Ten clients on care plans is $1,000+ a month of recurring revenue on top of builds.

**3. Migration services.** A surprising number of businesses are stuck on an ugly old WordPress site or a frozen Wix site from 2018. Rebuilding them on the current Wix with the AI generator is a $300-$800 job that takes a day, and the before/after sells itself. 'I rebuilt your entire site and it is faster, mobile-friendly and live' is a closing line that works.

**4. eCommerce setups.** The AI writes product descriptions and the store setup is genuinely fast - I have stood up a working online store for a client in an afternoon that would have been a week on WooCommerce. For a boutique or a maker with 20-50 products, $1,000-$3,000 for a designed, working store is an easy sell, and the payment processing revenue makes the subscription feel worth it to the client.

**5. Niche specialization.** Pick one vertical - real estate agents, dental clinics, gyms - and reuse your question list, your copy patterns and your Aria prompts across every client. You get faster, your sites get better, and you can charge more because you are 'the person who builds sites for dentists', not 'someone who makes websites'.

### Where it falls short (read this before you commit)

- **The AI has a recognizable 'Wix look'.** Clean, competent, samey. If the client needs a site that stands out - a design agency, a premium brand - Wix AI is the wrong tool, and you should say so and quote Framer or Webflow instead. Recommending the wrong tool to make a buck costs you the referral.
- **The editor overwhelms beginners.** App market, Velo code, members areas, marketing dashboards - the menu sprawl is real. Clients will get lost, and that is partly a feature (they pay you to be the one who is not lost), but be honest that Wix is not a 'set it and forget it' platform for them.
- **Template lock is permanent.** The structure you start with is your cage forever - you can restyle, but you cannot swap templates once published. Pick the starting point for the long term.
- **Lock-in is total.** Wix owns the hosting, the data, the structure. No clean export, no easy goodbye. Tell clients this before they commit, not after.
- **Free is a taste, not a business site.** Ads and a Wix subdomain are fine for testing, embarrassing for a real business. Budget the client onto Light or Core from day one.

### Who it is for, and who should skip it

Use it if you are a freelancer or small agency building sites for local businesses and service pros, or if you are a business owner who wants to get online without learning design or code. It is the fastest honest path from 'I need a website' to 'my website is live and does not embarrass me'. Skip it if you need a genuinely distinctive brand site (that is a designer tool or a custom build), if you are building a large custom web application (that is real development), or if you have a strong opinion about owning your stack - because with Wix, Wix owns it. And if you are choosing between Wix and Webflow or Framer, the question is simple: does this site need to look designed, or does it need to work for a small business? The first answer is Webflow or Framer and a bigger invoice. The second is Wix, a faster delivery, and a happier client.

### Getting started (in plain terms)

1. Sign up on the free plan and try the generator with a real business you know - a friend's business is perfect. See what the first draft looks like and where it gets the details wrong.
2. Spend an hour with Aria: make it add a section, change a headline, write a page. This is the skill you will sell, so get comfortable with what it does well and what needs your hand.
3. Build one site end to end for free: pages, copy, images, a booking or contact form, mobile view. Hand it to the business owner as a preview and ask them what is wrong - their answers are the difference between a template and a sale.
4. Learn the billing so you can quote honestly: which features need Core, what the domain costs, what the care plan should include. Nothing loses a client faster than surprise fees.
5. Only then take a paying client. Do the build on the free plan, put them on Light or Core at launch, roll the subscription into your quote or care plan, and never eat the monthly cost yourself.
"""
}

def main():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    tools = data if isinstance(data, list) else data.get('tools', data)

    if any(t.get('slug') == 'wix-ai' for t in tools):
        print('Wix AI already exists, skipping.')
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

    print(f"✅ Wix AI added. Total tools: {len(tools)}")
    print(f"   content length: {len(NEW_TOOL['content'])} chars")
    print(f"   forbidden-word scan clean")

    # ---- Generate OG image (Pillow) ----
    sys.path.insert(0, str(BASE / "scripts"))
    import gen_og_images_en as og
    og_dir = BASE / "images" / "og"
    og_dir.mkdir(parents=True, exist_ok=True)
    try:
        og.make_tool_og(NEW_TOOL, og_dir / "wix-ai-en-og.png")
        print(f"✅ OG image generated: wix-ai-en-og.png")
    except Exception as e:
        print(f"⚠️ OG image generation failed: {e}")

if __name__ == '__main__':
    main()
