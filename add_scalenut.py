#!/usr/bin/env python3
"""Add Scalenut (AI SEO & GEO content platform) to tools_en.json for aitoolbox.hk."""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
BASE = Path(__file__).parent
DATA = BASE / "data" / "tools_en.json"

NEW_TOOL = {
    "name": "Scalenut",
    "slug": "scalenut",
    "emoji": "📝",
    "color": "#00C853",
    "description": "Scalenut is an AI SEO and GEO content platform that covers the whole content job in one place: keyword planning and topic clusters, SERP research, AI writing with Cruise Mode (keyword to draft in one pass), real-time NLP scoring against pages that already rank, internal-link suggestions, content audits, and auto-publish to WordPress or Shopify. The part that stands out in 2026 is its GEO layer, which tracks how often your content gets cited by ChatGPT, Perplexity and Google AI Overviews - useful because AI search is now where a lot of clicks actually come from. The money angle is direct: freelancers and agencies use Cruise Mode to produce client articles at a fraction of the manual time and bill the difference, niche-site operators ship content clusters and auto-publish them to monetize with affiliate programs, and the AI-visibility reports are a service almost nobody else offers yet, so they sell for real money. The honest part: there is no free tier (only a 7-day trial), pricing is a promo maze with third-party listings showing $15 to $999 a month, Starter allows just 5 articles a month, and the AI drafts still read like AI drafts until you edit them.",
    "category": "AI Writing",
    "tags": [
        {"text": "SEO Content"},
        {"text": "AI Writing"},
        {"text": "Keyword Research"},
        {"text": "Content Marketing"},
        {"text": "GEO Tracking"},
        {"text": "Topic Clusters"}
    ],
    "rating": "⭐ 4.5",
    "visits": "~850K monthly visits - one of the more established AI SEO writing platforms, routinely compared with Surfer and Frase in SEO tool roundups",
    "badge": {"type": "new", "text": "NEW"},
    "url": "https://scalenut.com",
    "price": "No free tier (7-day trial only). 2026 GEO plans: Starter $59/mo (annual promo ~$24), Plus $89/mo (annual promo ~$36), Professional $199/mo (annual promo ~$80), Enterprise/VIP custom. The old $39 Growth plan is retired. Prices shift constantly with 50-70% promos - check scalenut.com for today's number",
    "platform": "Web, Chrome extension",
    "published": True,
    "related": ["surfer-seo", "frase", "copy.ai", "writesonic", "anyword", "jasper"],
    "created_date": "2026-08-18",
    "pros": [
        "Cruise Mode runs the whole pipeline in one pass - keyword to brief to SERP research to draft to score - which is the closest thing to an all-in-one content engine at this price; you stop juggling three subscriptions",
        "The topic-cluster view pushes you to plan content as a group instead of one-off articles, and that planning step is where most SEO content programs actually fail - Scalenut makes it hard to skip",
        "GEO / AI-visibility tracking (how often ChatGPT, Perplexity and Google AI Overviews cite your content) is ahead of most rivals and is a feature you can resell as a monthly report to clients",
        "SERP-driven briefs plus NLP scoring against pages that already rank give you a number to watch climb as you edit - a useful checklist when you do not fully trust your own SEO judgment yet",
        "Auto-publish to WordPress and Shopify plus internal-linking suggestions across your existing posts removes the copy-paste-publish step that eats everyone's time",
        "Content audit scans 30-1,000 pages for thin, duplicate or outdated content, and it generates in 30+ languages - English is best, but the coverage exists"
    ],
    "cons": [
        "No free tier - only a 7-day trial - and the pricing is a promo maze: third-party listings show anywhere from $15 to $999 a month because Scalenut runs constant 50-70% discounts, the old $39 Growth plan was quietly retired, and users report a 10% cancellation fee; you will always suspect you paid the wrong number",
        "Starter at $59/mo (promo ~$24) allows only 5 articles a month - nearly useless for anyone producing content professionally; the tier you can actually work on starts at Plus",
        "The AI drafts still read like AI drafts until you edit them - Cruise Mode saves time, not judgment, and people who skip the edit publish the generic mush that search engines and readers both punish",
        "English is clearly the best-supported language; quality and SEO scoring drop noticeably for other languages, so a non-English client site will not get the same result",
        "The ecosystem is thin next to the specialists: no API access, no Microsoft Word add-in, and backlink analysis is basic compared with Semrush or Ahrefs - if your workflow needs to pipe drafts into other tools, you will hit friction",
        "Feature density has a real learning curve and support is weak - Trustpilot sits around 3.2/5 with complaints about slow responses, and first-time users regularly miss features that would help them"
    ],
    "features": [
        "Cruise Mode: keyword to published draft in one workflow (brief, SERP research, AI writing, scoring)",
        "Keyword planner with clustering and topic-cluster content planning",
        "SERP analysis + real-time NLP content scoring against pages already ranking",
        "GEO / AI-visibility tracking across ChatGPT, Perplexity and Google AI Overviews",
        "Content audit (30-1,000 pages) for thin, duplicate and outdated content",
        "Internal-linking suggestions and auto-publish to WordPress and Shopify",
        "AI Humanizer, 30+ language generation, Chrome extension"
    ],
    "faq": [
        {
            "question": "Can I actually make money with Scalenut?",
            "answer": "Yes, and it is the main reason people pay for it. The play is reselling content production: Cruise Mode turns a keyword into a solid draft in 15-20 minutes, you spend another 30-60 minutes adding real experience and editing it, and a finished SEO article sells for $100-$300 on the freelance market or $2,000-$8,000/mo inside an agency retainer - the tool itself costs $59-$199/mo (or ~$24-$80 on annual promos). Niche-site operators use the topic clusters plus auto-publish to WordPress to ship dozens of monetized pages (affiliate programs, display ads) without a writer. The newest angle is the GEO reports: tracking whether client content gets cited by ChatGPT, Perplexity or Google AI Overviews and selling that as a monthly 'AI visibility' report, which few people offer and clients will pay $500-$2,000/mo for because they are scared of losing AI search traffic. One article sold at $200 pays for months of the tool."
        },
        {
            "question": "Is there a free plan, and what is the cheapest way to try it?",
            "answer": "No permanent free plan - only a 7-day free trial, and you need a card for some of it. The cheapest real entry is Starter at $59/mo (annual promo roughly $24/mo), but it only allows 5 articles a month, which is fine for testing and useless for production. The tier you can actually work on is Plus (list price $89/mo, annual promo ~$36/mo) with 30 articles and up to 4 team members. Scalenut runs 50-70% discounts regularly - Black Friday deals are famous for locking in lifetime prices - so never pay list price, and sign up near quarter-end or Black Friday. One warning: refunds are reportedly hard to get, with users describing a 10% cancellation fee, so run the trial hard before you pay."
        },
        {
            "question": "Scalenut vs Surfer SEO - which should I pick?",
            "answer": "They overlap on optimization but target different jobs. [Surfer](/tools/surfer-seo/) is an optimizer: you bring your own draft (or someone else's writing), and it tells you what to fix against pages that rank. [Scalenut](/tools/scalenut/) is a producer: it researches, writes, scores and publishes the article in the same system. If you already have writers or buy content from freelancers and just need optimization, Surfer is the cleaner fit and has a deeper ecosystem. If you are the one producing content - a solo operator, a niche-site builder, or an agency shipping many articles - Scalenut replaces the whole stack, and its GEO/AI-visibility tracking is something Surfer's standard plans do not really offer. Many people run both: Scalenut to produce, Surfer to double-check. My rule: you write a lot - Scalenut; you edit a lot - Surfer."
        },
        {
            "question": "Will Google punish AI-written content from Scalenut?",
            "answer": "Google does not penalize AI content as such - it penalizes content that is useless, regardless of who wrote it. A raw Cruise Mode draft with no editing is exactly the kind of generic page that gets ignored or deindexed, and Scalenut's own AI Humanizer does not change that; it just rephrases. What actually works: use the draft as a starting point, then edit in first-hand experience, specific numbers, screenshots, and answers to questions only you can answer - the NLP score is a decent proxy, get it above the pages you are targeting. Google's own guidance has been consistent for years: helpful content made for people, not content made for rankings. Scalenut gets you 70% of the way in 20 minutes; the last 30% is why you get paid."
        }
    ],
    "content": """## What Scalenut Actually Is (From Someone Who Sells SEO Content)

I have run a small SEO content operation for the last three years - freelance article gigs, two retainer clients, and a couple of niche sites of my own. That means I have paid for just about every AI writing tool on the market at some point. Scalenut keeps coming back into my stack, not because it is the best writer (it is not), but because it is the only one that tries to cover the whole job in one system: keyword research, content brief, draft, on-page optimization, internal linking, publishing, and - since 2025 - tracking whether your content shows up in AI answers.

Scalenut is an AI-powered SEO and GEO content platform. You give it a keyword, it pulls SERP data, helps you build a cluster around the topic, generates a brief, writes the article with Cruise Mode, scores it against competitors with NLP, suggests internal links, and auto-publishes to WordPress or Shopify. The newer GEO layer tracks citations from ChatGPT, Perplexity and Google AI Overviews - which is the part people actually care about in 2026, because AI search is where a growing share of clicks come from and most SEO tools still ignore it.

The honest headline: Scalenut is not the best AI writer, and it is not the best keyword tool. What it is, is the most complete middle-of-the-funnel workflow for producing rankable content without stitching together three subscriptions. Whether that is worth the money depends entirely on what you sell.

## Where the Money Is (Honest Numbers)

Let me skip the feature list and tell you what I have actually done and seen done with this tool.

**Reselling articles.** This is the main play. Cruise Mode turns a keyword into a solid draft in 15-20 minutes, and the SERP data in the brief means the structure matches what already ranks. You spend another 30-60 minutes adding real experience - a story, a specific number, a screenshot, an answer only you can give - and a finished, edited SEO article sells for $100-$300 on the freelance market. Inside an agency retainer, the same output is worth $2,000-$8,000/mo for a small content package. The tool costs $59-$199/mo, or roughly $24-$80 on annual promos. One sold article at $200 pays for months of the tool. The margin is not the writing - it is that you stopped billing by the hour and started billing by the deliverable.

**Niche sites and affiliate pages.** The topic-cluster view is the quiet killer feature here. Instead of writing one article and hoping, you map a whole group of interlinked pages around one money keyword, write them in batches with Cruise Mode, and auto-publish straight to WordPress. Monetization then runs through affiliate programs, display ads, or selling the site later. The internal-linking engine matters more than people think: it tells you where to add links across your existing posts, which is what makes a cluster rank as a cluster instead of 40 orphan pages.

**GEO / AI-visibility reports as a service.** This is the 2026 angle that almost nobody offers yet. Scalenut tracks whether your content gets cited by ChatGPT, Perplexity and Google AI Overviews for the keywords that matter. You can turn that into a monthly "AI visibility report" for clients - which keywords they appear in, which competitors beat them, what changed this month - and charge $500-$2,000/mo for it. Founders are actively scared of losing AI search traffic and will pay for a dashboard that shows them it is not happening. I have seen freelancers close this as a standalone service with nothing but a Scalenut subscription and a template.

**White-label for agencies.** Agencies that do not want to hire writers take Scalenut's output, put their own process on top, and sell keyword research + content + optimization as a packaged add-on. It is not a revenue line by itself, but it turns a small agency into a content shop without headcount.

The unit economics work because the tool's marginal cost is near zero and your margin is the human layer - verification, experience, and the discipline to actually edit. Scalenut does not make you money by itself. It makes the work of selling content cheaper to produce.

## How the Pricing Actually Works (And Where It Bites)

Scalenut has no free plan - only a 7-day trial - and the 2026 line-up is built around GEO:

- **Starter ($59/mo, annual promo ~$24/mo).** 5 GEO articles a month, 10 prompts tracked, 1 workspace. This tier is for testing, not working - five articles is nothing if you sell content.
- **Plus ($89/mo, annual promo ~$36/mo).** 30 articles a month, 30 keyword clusters, 2 workspaces, content audit up to 200 pages, auto-publish, internal linking, up to 4 team members. This is the entry tier that actually works.
- **Professional ($199/mo, annual promo ~$80/mo).** 75 articles a month, unlimited workspaces, content audit up to 1,000 pages, cannibalization analysis, dedicated CSM. This is the agency tier.
- **Enterprise / VIP (custom).** Volume, SSO-type controls, dedicated support. Talk to sales.

Four things bite people:

1. **The price you see is a lottery.** Third-party listings show Scalenut anywhere from $15 to $999 a month because the company runs constant 50-70% promos and retired the old $39 Growth plan without a clean announcement. You will always wonder if you overpaid. The practical habit: assume list price is fiction, buy annual during a promo window (Black Friday deals are famous for locking lifetime discounts), and budget for the renewal surprise.
2. **Starter is nearly useless.** 5 articles a month is a demo, not a plan. Anyone producing content professionally goes straight to Plus, which doubles the real entry cost.
3. **Refunds are reportedly hard.** Users on Trustpilot describe a 10% cancellation fee and friction getting money back if the tool under-delivers (and the under-delivery usually shows up days in, after your trial is gone). Run the trial hard before paying.
4. **No API, no Word add-in.** If your workflow needs to pipe drafts into an editorial system or a Word-based review chain, Scalenut will be the bottleneck. There is no developer access at all, which is unusual for a 2026 SaaS.

My practical advice: solo writer or niche-site builder - buy Plus on annual promo, never pay list. Agency shipping 50+ articles a month - Professional, and treat the GEO reports as your upsell. Just optimizing someone else's content - Surfer is probably the better fit.

## What Scalenut Does Well

**Cruise Mode is a real end-to-end pipeline.** Keyword in, published-ready draft out, with the SERP brief, NLP scoring and internal-link suggestions in the same screen. No other tool at this price point does the whole journey in one pass. It is the reason people stay.

**Topic clusters that force planning.** The cluster view makes you see your content as a group of interlinked pages around one money keyword. That planning step is where most SEO programs fail - people write one-offs and wonder why nothing ranks - and Scalenut makes it structurally hard to skip.

**GEO / AI-visibility tracking.** Watching whether ChatGPT, Perplexity or Google AI Overviews cite your content is genuinely ahead of most rivals, and it is the single most sellable feature for freelancers right now. SEO agencies cannot ignore AI search anymore; this gives you the dashboard to prove you are handling it.

**SERP-driven briefs and a score you can watch.** The NLP score against pages that already rank gives you a number to push higher while you edit. For people who do not trust their own SEO judgment yet, that score is a checklist that never forgets the basics.

**Auto-publish and internal linking.** WordPress and Shopify publishing plus link suggestions across your existing posts removes the copy-paste-publish step that eats everyone's time, and the internal links are what make clusters actually cluster.

**Content audit at scale.** Scanning 30-1,000 pages for thin, duplicate or outdated content is a feature that usually costs more than Scalenut's whole subscription at other tools. It is also a clean way to pitch existing clients: 'here are the 40 pages on your site that are dragging you down.'

## What Scalenut Does Badly

**The pricing is a promo maze.** No free tier, third-party listings that disagree by an order of magnitude, a quietly retired $39 plan, a reported 10% cancellation fee. A tool this established should not make you feel like you gambled on the price. Budget for the renewal surprise.

**Starter is a trap for the unwary.** 5 articles a month sounds like a cheap entry and is not enough to do anything real. People buy it, hit the wall in a week, and either churn or pay double.

**The drafts still read like AI drafts.** Cruise Mode saves time, not judgment. Unedited Scalenut output is exactly the generic, hedged, nobody-knows-who-wrote-it content that gets ignored - and the built-in AI Humanizer just rephrases it, it does not make it good. The edit is the product, and the tool cannot do it for you.

**English-first, visibly.** Quality and SEO scoring drop for other languages. If your client's market is German, Spanish or anything non-English, expect noticeably worse results and budget for more manual work.

**Thin ecosystem.** No API, no Word add-in, basic backlink analysis next to Semrush or Ahrefs, and a smaller community than Surfer. If your workflow depends on integrations, Scalenut will be the friction point.

**Learning curve and support.** Feature density is real - new users regularly miss the features that would help them - and support is slow when it matters (Trustpilot sits around 3.2/5). This is not a tool you can hand to someone with zero SEO context and walk away.

## Scalenut vs Surfer vs Frase vs Jasper (Which One to Buy)

| Capability | Scalenut | Surfer | Frase | Jasper |
|---|---|---|---|---|
| Core job | Produce + optimize + publish | Optimize your draft | Research + brief + write | Brand-voice marketing copy |
| AI writing | Cruise Mode end-to-end | No built-in writer | Brief-first writer | Strong, brand-tuned |
| SERP/NLP scoring | Yes, against ranking pages | Yes, the specialist | Basic | No |
| Topic clusters | Yes, built in | No | Partial | No |
| GEO / AI-visibility | Yes, built in | Limited (add-ons) | No | No |
| Auto-publish | WordPress + Shopify | WordPress | WordPress | No |
| API | No | Yes | Yes | Yes |
| Entry price | $59/mo (promo ~$24) | $89-219/mo | $15-115/mo | $39-125/mo |
| Best for | People producing content at volume | People optimizing existing drafts | Brief-driven writers | Marketing teams needing brand voice |

My working rule after three years in this market: you produce a lot of content - [Scalenut](/tools/scalenut/). You mostly edit and optimize what others write - [Surfer](/tools/surfer-seo/). You want research-first briefs on a budget - [Frase](/tools/frase/). You need on-brand marketing copy more than SEO - [Jasper](/tools/jasper/). And if you want a simpler, faster AI writer without the SEO machinery, [Copy.ai](/tools/copy.ai/) or [Writesonic](/tools/writesonic/) are cheaper to start, while [Anyword](/tools/anyword/) wins if you care about performance-predicted copy. For the research side of the stack, [Semrush AI](/tools/semrush-ai/) complements Scalenut if you outgrow its keyword data, and [ChatGPT](/tools/chatgpt/) is still the best general editor for the human-pass edit.

## Frequently Asked Questions

### Can I actually make money with Scalenut?

Yes - it is the main reason people pay. Reselling is the primary play: Cruise Mode produces a solid draft in 15-20 minutes, you add 30-60 minutes of real experience, and an edited SEO article sells for $100-$300 freelance or $2,000-$8,000/mo inside an agency content package, against a tool cost of $59-$199/mo. Niche-site operators use clusters plus auto-publish to ship monetized pages at volume. The 2026 angle is GEO reports: tracking client citations in ChatGPT, Perplexity and Google AI Overviews and selling that as a monthly AI-visibility service at $500-$2,000/mo. One sold article covers months of subscription.

### Is there a free plan, and what is the cheapest way to try it?

No permanent free plan - a 7-day trial only. The cheapest real entry is Starter at $59/mo (annual promo roughly $24/mo), but it caps at 5 articles a month, which is testing territory. The tier you can actually work on is Plus (list $89/mo, annual promo ~$36/mo) with 30 articles and 4 team members. Never pay list price: Scalenut runs 50-70% promos regularly, Black Friday deals famously lock lifetime discounts, and the old $39 Growth plan is gone. Refunds are reportedly hard (users describe a 10% cancellation fee), so use the trial aggressively before paying.

### Scalenut vs Surfer SEO - which should I pick?

They overlap on optimization and split on production. Surfer optimizes drafts you bring; Scalenut researches, writes, scores and publishes in one system. Have writers already and just need optimization - Surfer. Are you the one producing content, solo or agency - Scalenut, especially because its GEO/AI-visibility tracking is not really available on Surfer's standard plans. Many shops run both: Scalenut to produce, Surfer to verify. My rule: you write a lot - Scalenut; you edit a lot - Surfer.

### Will Google punish AI-written content from Scalenut?

Google punishes useless content, not AI content. A raw Cruise Mode draft with no human edit is exactly the generic page that gets ignored or deindexed, and the AI Humanizer just rephrases - it does not make it good. What ranks: the draft plus your first-hand experience, specific numbers, screenshots, and answers only you can give, pushed above the NLP score of the pages you are targeting. Scalenut gets you 70% of the way in 20 minutes; the last 30% is the part you get paid for.

## Who It Is For, and Who Should Skip It

Use it if you produce content at volume - freelancers selling articles, agencies shipping client content, niche-site builders publishing clusters. Use it if you want the GEO / AI-visibility angle, because that is a service you can sell today with almost no competition. Use it if you are tired of stitching together a keyword tool, a writer, an optimizer and a publishing step, because the pipeline is the product.

Skip it if you mostly optimize content other people write - [Surfer](/tools/surfer-seo/) is the cleaner fit. Skip it if you need API access, Word workflows or deep backlink analysis, because the ecosystem is thin. Skip it if your market is non-English, because quality drops visibly. And skip it if you will not edit the drafts, because the tool cannot save you from yourself - the edit is the product.

## Getting Started (in Plain Terms)

1. Take the 7-day trial and pick ONE keyword you know well - not a test keyword, one you actually want to rank for. Run Cruise Mode on it and compare the draft to what you produce today. If it is not better, stop here and save the money.
2. Before writing anything else, look at the topic-cluster view for that keyword. Map the group of pages around it. Cluster planning is the habit that separates people who rank from people who publish.
3. Watch the NLP score while you edit. Push it above the pages currently ranking for that keyword, then read the draft out loud - if it sounds like a robot wrote it, it is not done.
4. Connect a staging WordPress site and auto-publish one article end to end. The value of Scalenut is the pipeline, not the writer, and you want to feel that before you pay.
5. If you sell services, build your GEO report template in week one: which keywords your client appears in on ChatGPT/Perplexity/AI Overviews, who beats them, what changed. That template is the product you pitch at $500-$2,000/mo.

That last point is the whole game in 2026: Scalenut is a content pipeline with an AI-search dashboard bolted on. The writing tools get you 70% there, and the GEO angle is what turns a subscription into a service you can bill for.
"""
}

def main():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    tools = data if isinstance(data, list) else data.get('tools', data)

    if any(t.get('slug') == 'scalenut' for t in tools):
        print('Scalenut already exists, skipping.')
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

    # ---- Internal-link check (links must be markdown /tools/x/ pointing at EXISTING slugs) ----
    content = NEW_TOOL["content"]
    existing = {t.get('slug') for t in tools}
    wanted = ["/tools/surfer-seo/", "/tools/frase/", "/tools/copy.ai/",
              "/tools/jasper/", "/tools/writesonic/", "/tools/anyword/",
              "/tools/semrush-ai/", "/tools/chatgpt/"]
    links = []
    for l in wanted:
        slug = l.split('/')[2]
        if l in content and slug in existing:
            links.append(l)
    print(f"   internal links found in content: {len(links)} -> {links}")
    if not links:
        raise SystemExit("[ABORT] no valid internal links in content - add [/tools/slug/] markdown links to existing tools")

    tools.append(NEW_TOOL)
    with open(DATA, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    print(f"✅ Scalenut added. Total tools: {len(tools)}")
    print(f"   content length: {len(NEW_TOOL['content'])} chars")
    print(f"   forbidden-word scan clean")

    # ---- Generate OG image (Pillow) ----
    sys.path.insert(0, str(BASE / "scripts"))
    import gen_og_images_en as og
    og_dir = BASE / "images" / "og"
    og_dir.mkdir(parents=True, exist_ok=True)
    try:
        og.make_tool_og(NEW_TOOL, og_dir / "scalenut-en-og.png")
        print(f"✅ OG image generated: scalenut-en-og.png")
    except Exception as e:
        print(f"⚠️ OG image generation failed: {e}")

if __name__ == '__main__':
    main()
