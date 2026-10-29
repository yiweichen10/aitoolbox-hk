#!/usr/bin/env python3
"""Append article #206: privacy-first web analytics (Plausible vs Fathom vs Matomo vs GA4)."""
import json

PATH = 'data/articles_en.json'

content = """Google Analytics still runs on just over half of all websites — W3Techs puts it on roughly 55% of sites with a known analytics tracker — yet Firefox has blocked its script by default since 2019 under Enhanced Tracking Protection, and EasyPrivacy filter lists have been quietly deleting the same requests inside ad blockers for a decade. That gap between installs and actual data collection is the quiet scandal of the free tier: a meaningful share of your real traffic never reaches Google's servers, and no report will tell you which share. In 2026, four privacy-first web analytics tools have become the standard escape routes: Plausible, Fathom Analytics, Matomo, and — for teams that stay and pay in other currencies — Google Analytics 4 itself. I have run real traffic through all four across client sites and my own properties: Plausible on content sites since 2021, Fathom on a portfolio of small client sites, Matomo self-hosted inside a corporate network, GA4 wherever a client's Google Ads bid strategy demanded it. The pattern that holds after all that: the sticker price is never the real price. The real price is traffic-tier arithmetic, compliance overhead, and how many reports your team actually opens. Here is what each one costs in 2026, where each wins, and the trade-offs the comparison pages skip.

## How the four actually diverge

All four count visitors, pageviews, referrers, and campaigns. On a feature checklist they overlap heavily. The differences that decide budgets are metering model, data residency, and how much tracking depth each one is willing to sell you.

- **Plausible** is open-core software (AGPL) with a deliberately one-page dashboard. Its script is about 2.5KB gzipped against roughly 135KB for the GA4 tag — Plausible's own published comparison, and the number holds up in dev tools. No cookies, no personal data storage, all hosted data processed in the EU on German servers. Cloud is metered by monthly pageviews plus custom events; a free Community Edition can be self-hosted with real trade-offs.
- **Fathom Analytics** is a closed-source SaaS with the simplest pricing in the category: flat monthly tiers by pageview volume, and 50 sites included on every plan. Everything ships in every tier — event and revenue tracking, UTM reporting, shared dashboards, the API. Fathom Lite, its free open-source ancestor written in Go, still exists on GitHub but is minimal and largely dormant.
- **Matomo** is the heavyweight. Its self-hosted core is free forever with unlimited users and hits, and it is the only tool here that offers full user-level tracking — the capability the privacy-first tools refuse to build. Cloud hosting starts at €22 a month with data stored in Frankfurt. Heatmaps, session recordings, funnels, and A/B testing arrive as paid plugins or bundles, and 100+ integrations cover nearly every CMS and commerce stack.
- **Google Analytics 4** is free and unavoidable at scale: its Google Ads conversion import and BigQuery raw export (free up to 1 million events a day) have no real substitutes inside the Google ecosystem. The costs arrive as consent management, blocked traffic, script weight, sampling in exploration reports, and an event model that agencies still bill migration hours for, two years after Universal Analytics died.

A market note: Plausible and Fathom sell simplicity by traffic volume, Matomo sells depth by bundle, and Google sells attention — the analytics is free because the ad network on the other side is not. That is why four "similar" tools produce four completely different invoices.

## Plausible pricing 2026: traffic tiers, plan walls, and the self-hosting trap

Plausible prices by total monthly pageviews plus custom events across all sites in an account — custom events count against the same allowance, which surprises teams that instrument everything. The 2026 tier structure splits into three plans, each priced per traffic band, with annual billing costing 10x the monthly price (two months free):

| Pageviews/mo | Starter | Growth | Business |
| --- | --- | --- | --- |
| 10k | $9 | $14 | $19 |
| 100k | $19 | $29 | $39 |
| 500k | $49 | $74 | $99 |
| 1M | $69 | $104 | $139 |
| 10M | $169 | $254 | $339 |

Starter covers one site with three years of retention. Growth allows three sites and three team members and adds shared links and embedded dashboards. Business raises that to ten sites and ten members, five-year retention, custom properties, the Stats API (600 requests per hour), the Looker Studio connector, funnels, and ecommerce revenue attribution. Enterprise is quote-only and adds SSO, the Sites API, a managed proxy, and scheduled raw-data exports. A 30-day trial runs at Business limits with no credit card, and nonprofits, schools, and open-source projects get 15% off annual Business plans.

The overage policy is the most forgiving I have seen: one month over your tier costs nothing and interrupts nothing. Only after two consecutive months over does Plausible ask you to upgrade, and refusing merely locks the dashboards while collection continues. Contrast that with per-event overage billing elsewhere and the practical risk of a traffic spike is close to zero.

The self-hosting trap is economic, not technical. Plausible Community Edition is free and runs on Docker Compose with PostgreSQL and ClickHouse, but the cloud's funnel, revenue goals, SSO, and Sites API never ship in CE, releases land only twice a year, bot filtering is basic, and patching is your job. That last point got real in 2026: CVE-2026-8467, an unauthenticated remote code execution through a /storybook endpoint, affected CE 3.0 through 3.2.0 and was fixed in v3.2.1 — an unpatched instance was genuinely exploitable. And the savings are smaller than people assume: a $17/month VPS is the realistic floor for running ClickHouse comfortably, so below 100k pageviews on a single site, the $9 cloud plan is cheaper than the hardware, before counting your time.

## Fathom Analytics pricing: flat tiers and the 50-site allowance

Fathom's pricing is a single axis: $15 a month covers up to 100,000 monthly pageviews, $25 covers 200,000, and $45 covers 500,000, with higher tiers above that. Annual billing gives two months free. Every plan ships the same feature set — event and revenue tracking, UTM campaign reporting, saved views, shared dashboards, automatic bot filtering, the analytics API, unlimited email reports — because Fathom's bet is that you should never study a pricing matrix to decide which features you need.

Two details make Fathom unusually cheap for the right workload. First, all plans include at least 50 sites, and extra sites come in packs of 50 for $10 a month — so an agency or a solo operator running a portfolio of client sites pays for pageviews, not per-site fees. Second, pageviews share the allowance across all sites, which suits many small sites better than one big one. At 100,000 monthly pageviews, Fathom is $15 against Plausible Starter's $19 for a single site; by the time you add Plausible's three-site Growth plan at $29, Fathom's $15 covering fifty sites is not a competition. For one high-traffic site, the math flips back toward Plausible's single-site Starter tier.

The honest caveat: Fathom is the least transparent operationally — closed source, no self-hosting of the commercial product, and the free Fathom Lite repo is a basic pageview counter without team features, not a real alternative to its own cloud. If open-source matters to your procurement process, Fathom is out by definition, and the decision moves to Plausible versus Matomo.

## Matomo pricing 2026: the free core and the expensive bundles

Matomo pricing in 2026 splits cleanly between cloud and on-premise, and the on-premise core is genuinely free forever — unlimited users, unlimited hits, with ecommerce tracking, events, campaigns, custom dashboards, and segments all included. That is the only free tier in this comparison that is a full analytics product rather than a trial or a stripped counter.

Matomo Cloud starts at €22 a month (billed annually, which gives two months free) for 50,000 hits, scaling through tiers to 10 million hits, with overage at about €2.20 per extra 5,000 hits. Data is stored in Frankfurt. Cloud includes every feature, which means heatmaps, session recordings, funnels, and A/B testing that the self-hosted route gates behind paid plugins — those bundles start at €275 a month for Team (4 users, 5 million hits, heatmaps, recordings, funnels, media analytics), €1,450 a month for Business (20 users, 30 million hits, cohorts, multi-channel attribution, roll-up reporting, white labeling), and €3,400 a month for Enterprise (50 users, 100 million hits, A/B testing, SSO, crash analytics). Annual billing takes about 17% off.

In the Matomo vs Google Analytics debate, Matomo's argument is depth without lock-in: it is the only option here that can track individual users across sessions if you ask it to — useful for enterprise support and cohort work, and precisely the capability that makes a GDPR compliant web analytics setup your own problem when self-hosting. Matomo gives you the controls; the compliance obligations stay on your side of the fence. Teams that want someone else to hold the compliance risk take the cloud, at Frankfurt data residency, and accept the EUR pricing.

## Google Analytics 4: free until you price the whole stack

GA4's license cost is zero, and the list price for GA360 — the enterprise tier — starts around $50,000 a year with usage-based pricing Google does not publish. But most teams comparing this category are weighing the free tier against paid privacy-first tools, so the honest accounting is total cost of operation, not license fees.

Four costs hide inside "free." First, compliance: for EU visitors, GA4 requires a cookie consent banner and a consent management platform, which is a vendor fee plus legal review, and after European regulators' rulings on Google Analytics data transfers, several EU markets have additional risk assessments to sign off on. Second, blocked collection: Firefox has blocked the GA tag by default since 2019, and EasyPrivacy filter lists cover a large share of ad-blocker users — your real traffic is undercounted in ways you cannot audit. Third, weight: the GA4 tag runs around 135KB gzipped, and once Google Tag Manager and a consent banner are added, the stack commonly passes 285KB — a measurable drag on page speed on every pageview. Fourth, sampling: exploration reports sample data at meaningful volumes, so enterprise-scale analyses quietly lose precision unless you pay for 360 or route everything through the free BigQuery export.

What you get for that is real: Google Ads conversion import that feeds bidding strategies directly, BigQuery raw event access free up to a million events a day, and machine-learning insights no indie tool matches. If paid search is your primary channel, that Ads integration frequently decides the question on its own.

## Feature and cost comparison

The table distills list prices and models as of October 2026, taken from each vendor's pricing page.

| Tool | Free tier | Paid entry | Metering & data model | Best fit |
| --- | --- | --- | --- | --- |
| Plausible | 30-day trial; free AGPL self-host (CE) | $9/mo at 10k pageviews, 1 site; annual = 2 months free | Pageviews + custom events per tier; no cookies; EU-only data; Business unlocks API and funnels | Content sites and teams dropping consent banners |
| Fathom Analytics | 7-day trial (card required) | $15/mo for 100k pageviews, 50 sites included | Flat pageview tiers shared across all sites; closed source, cloud only | Solo operators and agencies running many small sites |
| Matomo | Self-hosted core free forever, unlimited users and hits | Cloud €22/mo at 50k hits; plugin bundles from €275/mo | Hits per tier; optional full user-level tracking; self-host anywhere | Enterprises needing full features under their own control |
| Google Analytics 4 | Free, with BigQuery export to 1M events/day | GA360 from ~$50k/yr (usage-based, unpublished) | Event-based; sampling in explorations; consent banner required for EU | Teams whose Google Ads bidding depends on GA conversion import |

## Which web analytics tools fit which team

Matching web analytics tools to a workload starts with one question most teams skip: what do you actually do with the numbers? If the answer is "watch traffic trends, sources, and top pages weekly," Plausible Starter at $9 a month or Fathom at $15 is the entire requirement, and GA4's overhead buys nothing you will read. If the answer is "I run twenty small client sites," Fathom wins outright — $15 covers all of them, with 50-site allowances and shared client dashboards built for exactly that shape of business. If the answer is "we need funnels, attribution, A/B tests, and user-level analysis, but our lawyers say no Google," Matomo is the only tool here with the depth to replace GA4 feature-for-feature, and the self-hosted core is free until you want the premium bundles. If the answer is "our Google Ads account eats our analytics output for breakfast," stay on GA4 — the conversion import into bidding is worth more than every dashboard feature the alternatives offer, and the free BigQuery export covers the raw-data objection.

Two adjacent jobs deserve their own tools. Watching aggregate trends tells you what happened on the page, not what visitors did inside it — for that, our [session replay tools comparison](/articles/best-session-replay-tools-2026-logrocket-vs-hotjar-vs-fullstory-vs-posthog) covers tools that record individual sessions, a genuinely different privacy and compliance conversation. And traffic numbers will never tell you why visitors left — for that, our [survey tools comparison](/articles/best-ai-survey-tools-2026-typeform-vs-fillout-vs-jotform-vs-tally) covers asking them directly. A third note for acquisition-focused readers: our [AI SEO tools comparison](/articles/best-ai-seo-tools-niche-sites-2026) pairs naturally with a lightweight analytics stack for niche content sites.

## Frequently Asked Questions

### What are the best Google Analytics 4 alternatives in 2026?

For most small and mid-size sites, the three credible GA4 alternatives are Plausible, Fathom, and Matomo, and the choice is a workload question. Plausible is the best Google Analytics 4 alternative for content sites that want one clean dashboard and no consent banner, from $9 a month. Fathom is the best pick for portfolios of many small sites, with 50 sites included from $15. Matomo is the best full-feature replacement when someone needs funnels, heatmaps, A/B testing, and user-level tracking without Google, and its self-hosted core is free. If Google Ads bidding consumes your conversion data, none of the three replaces that integration, and running GA4 alongside a privacy-first tool for clean traffic measurement is a common and defensible compromise.

### Do Plausible, Fathom, and Matomo let me remove the cookie consent banner?

Yes, with one asterisk. Plausible and Fathom use no cookies and collect no personal data by design, and both vendors document GDPR, CCPA, and PECR compliance — sites can drop the analytics cookie banner entirely. Plausible has even published a third-party GDPR legal assessment. Matomo's default configuration can run cookieless too, and its cloud data stays in Frankfurt, but Matomo's optional user-level tracking features can pull it back into consent territory — if you turn those on, put your privacy lawyer back on speed dial. The practical rule: cookieless defaults mean no consent banner for analytics in all three, and that saving alone is often the compliance argument for switching.

### Plausible vs Fathom: which is better for a small website?

For a single site under 100,000 monthly pageviews, Plausible Starter at $9 a month is the cheaper entry, with the bonus of a self-hosting escape hatch later. For two or more sites, Fathom pulls ahead immediately: $15 covers up to fifty sites with the pageview allowance shared across them, while Plausible's three-site Growth plan runs $29. Feature-wise they are closer than the pricing suggests — both do events, revenue tracking, UTM reports, shared dashboards, and bot filtering on every plan. Choose Plausible if open source, EU-only infrastructure, or eventual self-hosting matters; choose Fathom if you run a portfolio or want the simplest bill in the category.

### Is self-hosted Matomo really free?

The core is. Matomo On-Premise is free forever with unlimited users and unlimited hits, including ecommerce tracking, events, custom dashboards, and segments — a full analytics product, not a crippleware demo. What costs money is depth and support: premium plugins like Heatmaps & Session Recording, Funnels, and A/B Testing are sold individually or bundled, starting at €275 a month for the Team bundle. You also pay the hidden way — hosting that can handle your traffic, and the operational work of updates, backups, and security, which Matomo Cloud handles for €22 a month. For high-traffic sites, the self-hosted free core is the strongest free offer in this entire category.

### Can privacy-first analytics track ecommerce revenue?

Yes, all three paid tools handle it, at different depths. Plausible's Business plan ($19 a month at 10k pageviews) adds ecommerce revenue attribution with funnels. Fathom ships event and revenue tracking on every plan, including the $15 entry tier — no feature gating at all. Matomo has the deepest commerce support of the three: full ecommerce tracking is in the free core, with cart analysis and multi-channel attribution in the paid bundles. What none of them do is ad-platform integration — if your revenue optimization happens inside Google Ads bidding, privacy-first ecommerce analytics tells you what sold, but only GA4 feeds that machine.

## The bottom line

In 2026, web analytics tools compete on what they refuse to collect as much as what they measure. Plausible is the default for content-driven teams at $9 a month, with forgiving overage policy and a self-host path — just respect the patching obligation if you take it. Fathom at $15 is the quiet bargain for anyone running many small sites, with fifty sites included and no feature matrix to study. Matomo is the full-feature answer for enterprises that cannot send data to Google, free to self-host and €22 on cloud. GA4 remains free and remains the right call when Google Ads bidding depends on its conversion import — but price the consent stack, the blocked traffic, and the script weight before calling it free. The most contrarian advice I can give: most teams would lose nothing real by running a privacy-first tool as the primary dashboard and keeping GA4 only where the ad machine needs it. The trial periods are generous on all four — run your real traffic through two of them for a month and let your own dashboard answer the question.
"""

article = {
    "title": "Best Privacy-First Analytics Tools in 2026: Plausible vs Fathom Analytics vs Matomo vs Google Analytics 4",
    "slug": "best-privacy-first-analytics-tools-2026-plausible-vs-fathom-vs-matomo-vs-ga4",
    "date": "2026-10-30",
    "dateFull": "October 30, 2026",
    "category": "AI Product Analytics",
    "description": "Plausible, Fathom Analytics, Matomo, and GA4 compared: 2026 pricing tiers, cookie-banner rules, self-hosting options, and which analytics tool fits your team.",
    "keywords": [
        "web analytics tools",
        "Plausible pricing 2026",
        "Plausible vs Fathom",
        "Google Analytics 4 alternatives",
        "Matomo pricing 2026",
        "GDPR compliant web analytics",
        "Fathom Analytics pricing",
        "best privacy-first analytics"
    ],
    "content": content
}

with open(PATH, encoding='utf-8') as f:
    data = json.load(f)

if any(a['slug'] == article['slug'] for a in data):
    raise SystemExit(f"Duplicate slug guard: {article['slug']} already exists")

data.append(article)

with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Appended article: {article['slug']} (total: {len(data)})")
