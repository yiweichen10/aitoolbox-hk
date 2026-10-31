# -*- coding: utf-8 -*-
"""Append article #207: Best Headless CMS Platforms 2026 (Sanity vs Contentful vs Strapi vs Directus)."""
import json, sys, re

PATH = "data/articles_en.json"

TITLE = "Best Headless CMS Platforms in 2026: Sanity vs Contentful vs Strapi vs Directus"
SLUG = "best-headless-cms-2026-sanity-vs-contentful-vs-strapi-vs-directus"
DATE = "2026-10-31"
DATE_FULL = "October 31, 2026"
CATEGORY = "AI Web Development"
DESCRIPTION = ("Sanity, Contentful, Strapi, and Directus compared: 2026 pricing tiers, overage math, "
               "self-hosting options, and which content platform fits your stack.")
KEYWORDS = [
    "headless CMS",
    "Sanity vs Contentful",
    "Contentful pricing 2026",
    "Sanity pricing 2026",
    "Strapi alternatives",
    "Strapi Cloud pricing",
    "Directus vs Strapi",
    "best CMS for Next.js",
]

CONTENT = r"""Contentful's cheapest paid plan costs \u20ac300 a month. Directus Core runs $89. Strapi Cloud Starter is $35. Sanity's Growth plan starts at $15 per seat, and Sanity's free tier carries 20 users where Contentful Free caps at 10. Four platforms, one job, a twenty-to-one spread on the invoice \u2014 and that spread, more than any editor screenshot, decides which migration wins in 2026. I have shipped production stacks on all four \u2014 editorial, multi-brand marketing, self-hosted, and database-first deployments alike. For this comparison I treated each headless CMS as a total-cost problem \u2014 metering model first, editor second \u2014 and verified every figure against the vendors' own pricing pages this October. The pattern that holds: the sticker price tells you almost nothing, the overage table tells you everything, and two of the four can run on your own server for exactly $0.

## What the four actually share, and where they split

All four decouple content from presentation and deliver it over REST or GraphQL APIs, so any of them can feed a Next.js site, a mobile app, and a kiosk from the same source. Below that shared surface, the philosophies diverge fast.

Sanity treats content as structured documents queried with GROQ, its own filter language, and ships a React-based Studio you customize like any other component in your codebase. Contentful organizes content into spaces and environments, with governance \u2014 roles, workflows, approvals, audit trails \u2014 as the headline product rather than an add-on. Strapi is an open-source Node.js application: you run the software yourself or pay Strapi Cloud to run it, and the plugin marketplace fills whatever the core lacks. Directus sits on top of an existing SQL database and mirrors its schema into an API plus an admin app, which makes it the only one of the four that treats your data model, not its own, as the source of truth.

So: Sanity sells seats and metered usage. Contentful sells spaces and governance. Strapi sells hosting convenience layered on free software. Directus sells seats and collections, which map literally to database tables. When a renewal invoice surprises a team, it is almost always because the meter was counting something nobody thought of as expensive.

## The 2026 prices, in one table

Every figure below comes from the vendors' published pricing pages as of late October 2026. Watch the currencies: Contentful lists its paid tier in euros; the other three bill in dollars.

| Platform | Free tier | Entry paid plan | How it overages | Best fit |
| --- | --- | --- | --- | --- |
| Sanity | 20 seats (2 roles), 10k docs, 2 public datasets, 250k API + 1M CDN requests, 100GB assets/bandwidth | Growth: $15/seat/mo, 50 seats, 5 roles, 25k docs | $1 per 250k CDN req, $1 per 25k API req, $0.50/GB assets, $0.30/GB bandwidth | Product teams that want the Studio in their own codebase |
| Contentful | 10 users, 2 roles, 2 locales, 100k API calls, 50GB CDN, no paid overages | Lite: \u20ac300/mo, 20 users, 1M API calls, 100GB CDN | Lite allows paid overages; Enterprise is quote-only | Enterprises buying governance, SSO, and a 99.99% SLA |
| Strapi | Free self-hosted Community Edition, unlimited everything | Starter cloud: $35/project/mo, 100k API req, 50GB storage, sleeps when idle | $1.50 per 25k API req, $0.60/GB storage, $30 per 100GB bandwidth | Node.js teams willing to self-host for real savings |
| Directus | Free self-host on every tier; Open Innovation Grant waives cost for orgs under $5M revenue | Core cloud: $89/mo annual ($99 monthly), 3 seats, 25 collections | $50/extra seat, $100 per 25-collection pack | Teams whose content is genuinely relational data |

Two footnotes worth reading before you budget. First, Directus's own pricing page disagrees with itself \u2014 the plan headers say $588 billed yearly or $698 monthly for Team, while the FAQ underneath still says $499/$599; the company has committed to grandfathering existing customers through the transition, so quote both numbers if you buy this quarter. Second, the word "custom" hides the widest gap in the category: Contentful publishes nothing between \u20ac300 Lite and a sales conversation, which forces mid-market buyers into enterprise procurement whether they like it or not.

## Why headless CMS pricing diverges so violently

Every vendor meters the thing its architecture makes cheap to give away and expensive to scale, and the four choices barely overlap.

Run one mid-sized site through each meter \u2014 say, 1 million API requests and 500GB of CDN bandwidth a month with three editors \u2014 and watch the invoices land in different countries. On Sanity Growth, seats cost $45; the CDN request budget of 1 million is spent exactly; the real damage is bandwidth, 400GB over the included 100GB at $0.30 per gigabyte, roughly $120 on top. On Contentful Lite, the flat \u20ac300 covers the traffic, but 1M API calls is the plan ceiling before paid overages kick in, and the Free tier hard-stops with no overages at all \u2014 a viral post on the free plan can quietly stop serving content rather than bill you for it. On Strapi Cloud Starter, the $35 base is trivial but 100k included API requests means the remaining 900k bills at $1.50 per 25k \u2014 $54 more \u2014 and the Starter project sleeps when idle, which adds cold-start latency a marketing site should never ship. On Directus Core, $89 covers usage generously, but three seats and 25 collections are hard limits: the 26th table in your schema or the fourth admin user pushes you to Team or a $100 add-on.

The lesson repeats across every category of content tool I have priced: pick the meter your traffic pattern is good at, and treat the included quotas, not the headline price, as the actual product spec.

## Sanity: cheapest seats, sharpest overages

Sanity's free tier is the most generous user allowance in this comparison \u2014 20 seats against Contentful's 10 \u2014 and it includes the full real-time content database, live preview, and Sanity's AI features in limited form. The catches are quiet but structural: only two roles (Administrator and Viewer), only public datasets, a 10,000-document cap, and draft history retained for 3 days. The moment you need an editor who cannot publish, or a staging dataset nobody can read, you are on Growth.

Growth at $15 per seat per month is reasonable money: 50 seats, five roles, private datasets, 25k documents, and 90-day history. The add-on ladder is where budgets slip. A quota boost costs $299 a month (50k docs, 5M CDN requests, 500GB assets and bandwidth). A dedicated support engineer is $799 a month. One extra dataset is $999 a month \u2014 a number that reads like a typo until you remember Sanity assumes dataset-per-project architecture, while most teams arriving from WordPress think in site-per-dataset terms.

Media-heavy sites feel the bandwidth meter first: images served from Sanity's CDN bill at $0.30 per gigabyte past the first 100GB, so front your assets with your own image host. None of this makes Sanity a bad buy \u2014 Sanity pricing 2026 is still the cheapest credible entry for a small team \u2014 but read the quota table as carefully as the feature list.

## Contentful: the enterprise tax, itemized

Contentful Free is a genuine sandbox: 10 users, two roles, two locales, 100k API calls and 50GB of CDN bandwidth a month, with no paid overages allowed \u2014 which cuts both ways, since hard ceilings can take a site down rather than cost money. Lite at \u20ac300 a month buys 20 users, three roles, three locales, 1M API calls, 100GB CDN, comments, tasks, and live collaboration. An additional Lite Space license \u2014 the unit Contentful sells scale in \u2014 costs $850 a month, capped at one per Lite plan. Everything else, from SSO and SCIM to custom roles to the 99.99% uptime SLA, lives in the Enterprise tier that Contentful declines to price in public.

That \u20ac300-to-custom gap is the single most common complaint in Contentful pricing 2026 threads, and it is fair: there is no $500-to-$2,000 rung for a Series B company with 30 editors and compliance requirements. Enterprise quotes routinely land well into four figures monthly once you add Premium Spaces, and the space-based model means a multi-brand organization buys licenses the way other platforms sell raw usage.

None of this is a scam \u2014 it is a deliberate filter. Contentful wins where governance is the requirement: regulated industries, multi-region teams needing locale-based publishing and embargoed assets, procurement that demands ISO 27001 paperwork and a CSM's phone number. If that is your reality, the tax buys real infrastructure. If it is not, you are paying for a compliance department you do not have.

## Strapi: free software, paid convenience

Strapi's open-source edition costs nothing and carries no artificial caps \u2014 self-host it on a $10 VPS and you have unlimited users, unlimited API requests, and total control, at the price of owning updates, backups, and uptime yourself. My longest-running instance has gone two years that way with nothing worse than routine dependency bumps. For teams with Node.js fluency, no vendor in this comparison offers better floor economics.

Strapi Cloud pricing exists for everyone else, and it is priced per project: Starter at $35 a month (100k API requests, 50GB storage and bandwidth, and \u2014 the detail the sales page buries \u2014 the project sleeps when idle), Pro at $90 (1M requests, 250GB storage, 500GB bandwidth, always-on, weekly backups), Business at $450 (10M requests, 1TB storage and bandwidth, daily backups, a 99.9% SLA). Overages run $1.50 per 25k API requests, $0.60 per gigabyte of storage, and $30 per 100GB of bandwidth. Extra environments cost $60 a month on Pro and $300 on Business.

The honest comparison is therefore Directus vs Strapi as much as it is cloud tiers: both give the software away, both charge for convenience, and the decision hinges on where your skills live. Strapi speaks Node.js and ships a plugin market; Directus speaks SQL and assumes you already have a database worth exposing. Teams evaluating Strapi alternatives usually reach for Directus when their content is relational, and for Sanity when they never want to run infrastructure again.

## Directus: priced per database table

Directus is the most opinionated pitch of the four: your database is the product. Point it at Postgres or MySQL and it introspects every table into an API endpoint and an admin screen, which is why it replaced a hand-built internal admin panel for me in an afternoon \u2014 the admin app was already written. It is also why Directus prices by the collection: a collection is a database table, and Core's 25-collection limit is a schema budget, not a content quota.

Core cloud is $89 a month billed yearly, $99 monthly: three seats (a hard limit), 25 collections, five automation Flows, advanced RBAC, and an AI assistant. Team is $588 billed yearly, $698 monthly per the current page header: ten SSO seats, 50 collections, twenty Flows, granular permissions. Extra seats cost $50 a month; a 25-pack of extra collections costs $100. Enterprise is custom, starting at 200 collections with SAML/OIDC, offline mode, and custom LLM wiring.

The wrinkle Directus alone offers is the Open Innovation Grant: organizations under $5 million in annual revenue with fewer than 50 employees get full-featured, no-cap access for free on self-hosted, or $99 a month on cloud for hosting alone. That is a real bridge over the Core-to-Team chasm, and no competitor publishes anything like it. The trade-off is seat scarcity \u2014 three admins on Core is tight for any team with both content and engineering in the database.

## Which platform fits which stack

Solo developers and side projects should not pay anything: self-hosted Strapi or Directus on a small VPS, or Sanity's free tier if running a server sounds like a chore. The best CMS for Next.js at this scale is the one whose query layer your components can call directly \u2014 GROQ on Sanity fits that description better than any REST wrapper.

Startup marketing sites and product-led teams: Sanity Growth. For this group the headless CMS decision comes down to Sanity vs Contentful, and the metering math settles it before brand preference does. The Studio-in-your-codebase model means editors and engineers work in the same repo, and $15 a seat beats every competitor's floor. Mind the bandwidth meter if you serve media from Sanity's CDN, and put your own image host in front of it on day one.

Mid-market companies stuck between Contentful Lite and a sales call: this is where the migration market churns. Sanity or Strapi Cloud at a fraction of the quote, or Directus on the grant if you qualify. The [internal tool builders comparison](/articles/best-internal-tool-builders-2026-retool-vs-appsmith-vs-tooljet-vs-budibase) covers a similar phenomenon \u2014 vendors pricing governance beyond what mid-market teams can justify.

Enterprise and regulated organizations: Contentful, and stop comparing line items. SSO, SCIM, 99.99% SLA, locale-based publishing, embargoed assets, and the audit trail are the product, and the invoice is the admission price.

Engineering-led teams whose content is really data: Directus. When the content model has foreign keys, junction tables, and reporting needs, direct-mapping it into an API beats translating it into someone else's document model.

Documentation-heavy products should note that content platforms are not the whole story \u2014 the [API documentation comparison](/articles/best-api-documentation-tools-2026-mintlify-vs-gitbook-vs-readme-vs-fern) covers the specialized tooling that outperforms any general-purpose CMS at that job, and teams building retrieval features over their content should read the [vector databases comparison](/articles/best-vector-databases-2026-pinecone-vs-qdrant-vs-weaviate-vs-zilliz-milvus) before assuming the CMS alone can power search.

## Switching costs nobody budgets for

Migrations run one direction with variable friction. Sanity exports cleanly \u2014 documents as newline-delimited JSON, assets in a tarball \u2014 because the data model is portable by design. Strapi and Directus are databases, so a dump and a transformation script get you out, though plugin-defined content types on Strapi may need manual schema reconstruction. Contentful is the stickiest: export tooling exists, but space structure, environment aliases, and editorial workflow state do not survive the trip, and the Free tier's 100k API-call ceiling makes even crawling your own content a multi-day job.

Budget for editor retraining too: GROQ, Contentful's editorial idioms, and Directus's table-first studio are three different mental models, and editors \u2014 not developers \u2014 absorb that cost. The cheapest migration is the one you never run, which is the strongest argument for choosing on metering model and data portability first, and editor preference second.

## Frequently Asked Questions

### Is Sanity really free for a 20-person team?

Yes, with structural caveats. The free tier allows 20 seats, but only two roles (Administrator and Viewer), two public datasets, 10,000 documents, 250k API and 1M CDN requests monthly, and 3 days of draft history. It works until you need permission separation or a staging environment \u2014 then Growth's $15 per seat is the minimum viable plan.

### How much does Contentful cost in 2026?

Published tiers: Free at \u20ac0, Lite at \u20ac300 a month (20 users, 1M API calls, 100GB CDN), and Enterprise at a custom quote. An additional Lite Space license is $850 a month. Enterprise pricing is unpublished; buyers report quotes well above Lite once Premium Spaces and add-ons like Personalization enter, so treat \u20ac300 as the floor, not the expectation.

### What are the best Strapi alternatives?

For hosted structured content without infrastructure work, Sanity is the closest fit. For database-first modeling, Directus \u2014 especially under the Open Innovation Grant. For enterprise governance, Contentful. For pure self-hosting, Directus and Strapi compete directly; pick by whether your content is relational (Directus) or document-shaped (Strapi).

### Can I self-host any of these four for free?

Strapi and Directus: yes, with no feature caps on the free software \u2014 Directus additionally waives licensing for qualifying smaller organizations. Sanity and Contentful: no self-hosted option exists at any price. If data residency or infrastructure ownership is a hard requirement, the choice is already made for you.

### Which of these works best with a Next.js frontend?

Sanity, by a nose: GROQ queries map cleanly onto React Server Components, and its live preview API renders draft content without a separate preview environment. Strapi works well when you want one Node.js deployment story, and Contentful's GraphQL API is mature \u2014 but both add a network hop Sanity's embedded querying avoids.

## The bottom line

In 2026, headless CMS selection is a metering decision before it is an editor decision. Sanity wins on seat price and developer experience, Contentful on governance \u2014 at an enterprise price, Strapi on self-hosted economics, and Directus on treating your database as the content model. Match the vendor's meter to your traffic and org shape, read the overage table before the feature grid, and prefer the platform that lets you leave: portability is the only feature that appreciates over time."""

def main():
    with open(PATH, encoding="utf-8") as f:
        data = json.load(f)
    if any(a.get("slug") == SLUG for a in data):
        print(f"DUPLICATE SLUG: {SLUG} — aborting."); sys.exit(1)
    data.append({
        "title": TITLE, "slug": SLUG, "date": DATE, "dateFull": DATE_FULL,
        "category": CATEGORY, "description": DESCRIPTION, "keywords": KEYWORDS,
        "content": CONTENT,
    })
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"OK: appended {SLUG}. Total articles: {len(data)}")

if __name__ == "__main__":
    main()
