#!/usr/bin/env python3
"""Emit _tool_semrush.json for the English site (temp emitter, deleted after commit)."""
import json

tool = {
    "name": "Semrush",
    "slug": "semrush",
    "emoji": "📊",
    "color": "#FF642D",
    "description": "The heavyweight SEO suite that bolted AI-search tracking onto every plan in 2026. The money angle is direct: one client retainer pays for the subscription, competitor-gap audits are a repeatable product, and AI-visibility audits are the newest billable service in SEO.",
    "category": "AI SEO",
    "rating": "⭐ 4.5",
    "visits": "One of the most established names in SEO software, used by millions of marketers and a large share of agencies worldwide. Its keyword and backlink databases go back over a decade, which is why competitor research remains its strongest draw even as the market shifts toward AI answers.",
    "badge": {"type": "recommend", "text": "RECOMMENDED"},
    "url": "https://www.semrush.com/",
    "price": "Free plan · Paid from $139/mo",
    "pricing_details": "Verified from semrush.com/pricing (Nov 2026). Free: $0, 1 demo project, 10 reports/day, basic AI Visibility features. SEO plan: $139/mo monthly or $117.33/mo billed annually - 5 websites, 500 keywords tracked daily, Site Audit, Position Tracking, plus AI-search performance tracking and AI visibility reports. Starter (SEO + AI Search): $199/mo or $165.17/mo annual - adds MCP access, 50 AI prompts tracked daily, 1 domain for AI brand performance, 300 AI visibility reports/day. Pro+: $299/mo or $248.17/mo annual - 15 websites, 1,500 keywords, 100 prompts/day, historical data and content optimization. Advanced: custom pricing. Add-ons stack on top: extra users from $45/mo, agency lead-generation profile $90/mo, branded PDF reports $10-20/mo. Annual billing saves about 17%. Watch the per-project limits: the entry plan caps you at 5 websites, so an agency with 8 clients needs Pro+ immediately.",
    "pros": [
        "The competitor research is still the best reason to buy: keyword gap, backlink gap and traffic analytics across a database built over more than a decade. Finding the ten keywords a competitor ranks for and you do not is a twenty-minute job that produces a billable deliverable",
        "AI visibility tracking is now baked into every plan including the free tier - you can watch how a domain shows up in ChatGPT, Perplexity and Gemini answers without buying a separate AEO tool. Most rivals still sell this as an upsell or a separate product",
        "The free plan is genuinely usable for one site: 10 reports per day, 1 project, keyword and backlink lookups. Enough to run a real audit for a first client before you spend anything",
        "Breadth saves tool subscriptions: keyword research, site audit, rank tracking, backlinks, ad research, social scheduling and AI visibility in one login. Replacing the stack means three or four separate bills",
        "MCP access on Starter and above lets you plug Semrush data into AI agents and custom scripts - useful if you build client dashboards or automate reporting instead of assembling spreadsheets by hand"
    ],
    "cons": [
        "The price climbed hard: the entry paid plan used to be $99.95/mo and the lineup now starts at $139/mo with the old mid-tier names reshuffled. Existing subscribers got moved rather than protected",
        "The 2026 plan restructure is confusing - SEO, Starter, Pro+ and Advanced here, but separate product lines (AI Visibility, Traffic & Market, Content, Social, Local) each carry their own pricing pages. Expect to spend real time figuring out which plan you actually need",
        "AI visibility features tell you where you stand, not how to fix it. The dashboard shows your brand losing a prompt to a competitor; the actual work of earning the citation is still manual SEO and content. Vendors blur this, and you should not",
        "Usage limits bite agencies: 5 websites and 500 keywords on the entry plan, 50 tracked AI prompts a day on Starter. Tracking 8 clients across 3 AI engines blows through that fast, and the add-on pricing ($45 per extra user, $90 for the lead-gen profile) adds up quietly",
        "Non-English markets get thinner data. Keyword volumes and backlink coverage for smaller languages are noticeably weaker than for US/UK English, which matters if your clients are regional"
    ],
    "faq": [
        {
            "question": "Is Semrush worth $139/month for a beginner?",
            "answer": "For a hobby site, no - the free plan (10 reports/day) plus Google Search Console covers most of what a beginner needs, and paying $139 before you have an income from SEO is backwards. It becomes worth it the moment you have one paying client: a $500/month retainer covers the subscription four times over, and the competitor-gap and site-audit reports are what justify that retainer. The pragmatic path: take the free plan, run an audit on your own site to build a case study, land one client, then subscribe monthly (cancel between projects if work is irregular - no long lock-in on monthly billing)."
        },
        {
            "question": "Semrush vs Ahrefs in 2026 - which one should I pay for?",
            "answer": "They overlap about 80%, so pick by what you sell. If you sell content-led SEO and want the broadest toolkit (ads research, social, AI visibility tracking bundled in), Semrush wins - its AI-search features are further along and included across plans. If you mostly do backlink-driven work and value a cleaner, faster interface, Ahrefs is the better fit and many freelancers find its keyword data easier to trust. Running both is the classic agency move but hard to justify under $300/month of combined spend. My honest take: start with Semrush on monthly billing for the AI-visibility angle alone, and switch only if you find its backlink index insufficient for your niche."
        },
        {
            "question": "Can I actually track how my brand appears in ChatGPT with Semrush?",
            "answer": "Yes - every plan, including free, includes basic AI Visibility features, and paid plans track custom prompts across ChatGPT, Perplexity, Gemini and Google AI Overviews daily (50 prompts/day on Starter, 100 on Pro+). The honest caveat: it measures and alerts, it does not optimize. You still have to earn the citations through content, digital PR and structured data. Treat it as the reporting layer you show clients - 'here is where we appear in AI answers this month versus last' - which is precisely what makes AI-visibility retainers easy to sell right now."
        }
    ],
    "features": [
        "Keyword research with a 10+ year database: volumes, difficulty, intent, SERP features and keyword-gap analysis against any competitor",
        "AI visibility tracking across ChatGPT, Perplexity and Gemini: custom prompt monitoring, brand sentiment, and share-of-voice in AI answers",
        "Site Audit with AI-readiness checks: crawl up to 100k pages, thematic reports, and fix recommendations ranked by impact",
        "Position Tracking: daily rank tracking for 500 keywords on the entry plan, across devices and locations",
        "Backlink analytics: 40+ trillion links, toxic-link flags, and gap analysis against competitor link profiles",
        "SEO Writing Assistant: real-time content scoring against top-ranking pages, tone and readability checks",
        "MCP server access (Starter and above): pipe Semrush data into AI agents, Claude or custom scripts for automated reporting",
        "White-label and scheduled PDF reports ($10-20/mo add-on) for client deliverables",
        "Ad research and PPC keyword data: competitor ad copy history and spend estimates"
    ],
    "tags": [
        {"text": "SEO Toolkit"},
        {"text": "AI Visibility"},
        {"text": "Keyword Research"},
        {"text": "Agency Reporting"}
    ],
    "related": ["ahrefs", "vryse-ai", "peec-ai"],
    "platform": "Web app (browser, no install). MCP server access on Starter and above for piping data into AI agents and scripts. Mobile apps for rank tracking and reporting; Google Docs and WordPress add-ons for the Writing Assistant; API access on higher tiers.",
    "published": True,
    "created_date": "2026-11-03",
    "content": (
        "Semrush has been one of the two or three default answers to 'which SEO tool should I buy' for over a decade, and in 2026 it made the pivot that defines this market: every plan now ships with AI-search tracking. Not a separate AEO product, not an enterprise upsell - the entry plan watches how your domain shows up in ChatGPT, Perplexity and Gemini answers, tracks custom prompts daily, and reports brand sentiment. That matters because the question clients ask has changed. It used to be 'why am I not ranking for X'. Now it is increasingly 'why does ChatGPT recommend my competitor instead of me'.\n\n"
        "The core is unchanged and still the strongest part: a keyword database built over more than a decade, backlink analytics on a truly large index, site audits, rank tracking and competitor-gap reports. If you have never used it, the classic workflow is exactly as advertised - drop a competitor's domain in, pull the keywords they rank for that you do not, sort by gap and difficulty, and you have the outline of a content plan in an afternoon. That single report is the foundation of more paid SEO proposals than anything else in the industry.\n\n"
        "## Pricing: the real math\n\n"
        "The lineup was restructured in 2026 and it is worth reading carefully, because the names moved. Verified from semrush.com/pricing (Nov 2026): Free ($0, 1 demo project, 10 reports/day - genuinely usable for a first audit), SEO ($139/mo, $117.33/mo annual - 5 websites, 500 keywords, AI visibility reports included), Starter ($199/mo, $165.17/mo annual - adds MCP access, 50 tracked AI prompts/day, 300 AI visibility reports/day), Pro+ ($299/mo, $248.17/mo annual - 15 websites, 1,500 keywords, 100 prompts/day), and a custom Advanced tier. Add-ons stack: extra users from $45/mo, the agency lead-gen profile $90/mo, white-label reports $10-20/mo. Annual billing saves about 17%.\n\n"
        "The number that actually decides your plan is websites, not keywords. Five projects on the entry plan is fine for three own sites plus two clients; it is immediately too small for an agency, and the jump to Pro+ is nearly double. If you run client work, price your retainers so the subscription is a line item the client absorbs - standard practice, and clients accept it without blinking.\n\n"
        "For context on the hike: the entry plan sat at $99.95/mo for years. It is now $139. Nobody cancelled en masse, which tells you where pricing power in this market sits. But go in expecting a serious software bill, not a startup toy.\n\n"
        "## The AI part, honestly\n\n"
        "What works: the tracking. Seeing which prompts surface your brand, which surface competitors, and how that moved month over month is real, reportable data, and Semrush is further along here than most dedicated AEO startups in terms of coverage and reliability. The AI-readiness checks in Site Audit (crawlability by AI agents, structured data, llms.txt) are sensible and action-oriented.\n\n"
        "What does not work: the implication that the tool fixes what it measures. A dashboard that shows you losing the prompt 'best crm for solo consultants' to a competitor does not earn that citation back for you. The work is still content, digital PR, reviews and structured data - things a person does. Agencies that sell 'AI visibility optimization' by showing Semrush dashboards and then doing normal SEO under the hood are, bluntly, doing fine with this, but you should understand what you are buying: a measurement layer, not an autopilot.\n\n"
        "Also know the limits: 50 tracked prompts a day on Starter sounds like a lot until you manage four clients across three engines. The SEO Writing Assistant is serviceable but weaker than dedicated content-optimization tools at guiding a rewrite.\n\n"
        "## Where it hurts\n\n"
        "Price first: $139 to start, and the features most agencies actually want (MCP access, meaningful prompt tracking, historical data) start at $165-250/mo. Second, the plan maze: this pricing page sits next to separate product lines - AI Visibility, Traffic & Market, Content, Social, Local - each with its own pricing. Budget an hour to figure out your actual configuration, or you will overbuy. Third, the per-project limits and per-user add-ons nickel-and-dime growing teams in a way flat-per-seat SaaS does not. Fourth, data depth outside English-speaking markets is noticeably thinner - fine for US clients, frustrating for regional ones. Fifth, the learning curve is real; the interface has improved but a newcomer should expect a solid week before they stop clicking around aimlessly.\n\n"
        "## How people actually make money with it\n\n"
        "The retainer model is the obvious one and it still works: an SEO retainer runs $500-2,000/month for small business clients, and Semrush produces most of the deliverables - the audit, the keyword map, the rank report, the competitor gap. One client covers the subscription; three or four make it a rounding error.\n\n"
        "The productized angle: competitor-gap audits sold as fixed-price one-offs ($300-1,000) built almost entirely from Semrush exports. Fast to deliver, easy to systematize, and a proven foot in the door for retainer upsells.\n\n"
        "The new line worth watching: AI-visibility audits. Businesses are genuinely anxious about how they show up in ChatGPT answers, almost none of them can measure it, and Semrush hands you the measurement on day one. An 'AI search readiness audit' priced at $500-1,500 with a monthly monitoring retainer attached is one of the most sellable new services in SEO right now, and the tool's free tier is enough to build your first demo.\n\n"
        "Finally, the affiliate program pays around $200 per referred sale - if you publish SEO content, a review or comparison article that converts even a few readers a month is meaningful passive income.\n\n"
        "## Verdict\n\n"
        "Semrush in 2026 is still the safest serious choice for anyone doing SEO for money: the data moat is real, the breadth replaces three or four subscriptions, and the AI-visibility layer - while a measurement tool rather than a magic fix - is included at a price point where rivals still charge extra. The costs are honest ones: a higher entry price than two years ago, a plan structure that needs decoding, limits that agencies outgrow quickly. If you have one paying client or intend to find one, buy it monthly and bill it through. If you are a solo site owner with no client ambitions, the free plan plus patience will serve you until that changes."
    ),
}

# ---- self checks ----
BANNED = ["leverage", "utilize", "seamless", "game-changer", "revolutionize",
          "cutting-edge", "supercharge", "unleash", "elevate", "delve",
          "robust", "harness", "in today's digital", "take to the next level"]
blob = json.dumps(tool).lower()
hits = [w for w in BANNED if w in blob]
assert not hits, f"banned words present: {hits}"
assert len(tool["price"]) <= 50, f"price too long: {len(tool['price'])}"
assert len(tool["faq"]) >= 2
required = ("name", "slug", "url", "category", "description")
for f in required:
    assert tool.get(f), f"missing {f}"
assert len(tool["description"]) >= 40

with open("_tool_semrush.json", "w", encoding="utf-8") as fh:
    json.dump(tool, fh, ensure_ascii=False, indent=2)
print("OK _tool_semrush.json written, price =", repr(tool["price"]), len(tool["price"]), "chars")
print("content length:", len(tool["content"]))
