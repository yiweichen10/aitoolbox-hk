# -*- coding: utf-8 -*-
"""Append article #220: Best CDN Pricing 2026 (Bunny vs Cloudflare vs Fastly vs CloudFront)."""
import json

ARTICLE = {
    "title": "Best CDN Pricing in 2026: Bunny CDN vs Cloudflare vs Fastly vs CloudFront Compared",
    "slug": "best-cdn-pricing-2026-bunny-vs-cloudflare-vs-fastly-vs-cloudfront-compared",
    "date": "2026-11-13",
    "dateFull": "November 13, 2026",
    "category": "AI Infrastructure",
    "description": "Bunny at $0.01/GB, CloudFront's $15 plan with 50TB, Cloudflare's unmetered-but-restricted CDN, Fastly's 2025 reprice — worked bills at real traffic levels.",
    "keywords": ["CDN pricing", "Bunny CDN vs Cloudflare", "cheapest CDN", "CloudFront pricing", "Fastly pricing", "Cloudflare CDN pricing", "Bunny CDN pricing", "CDN for video streaming", "CloudFront flat-rate plans", "Fastly alternatives"],
    "content": """The same 50 TB of monthly traffic costs $200 on Cloudflare's Business plan, $501 at Bunny CDN, $200 on Amazon CloudFront's new flat-rate Business tier, and roughly $4,400 at Fastly's published rates. That is a 22x spread for what is, functionally, the same commodity delivered to the same viewers. The spread got wider in late 2025, when two of these four vendors rebuilt their rate cards within a month of each other: AWS launched CloudFront flat-rate pricing plans on November 18, 2025 — including a $15/month tier that includes 50 TB of transfer, bytes that price out at just under $4,000 on the pay-as-you-go card — and Fastly deleted its $50 monthly account fee on November 4, 2025. Most comparison posts still quote the old cards. This guide compares Bunny, Cloudflare, Fastly, and CloudFront on list prices pulled from each vendor's pricing pages in November 2026: unit rates, free allowances, request fees, and worked bills at real traffic levels. On CDN pricing, the short version: Bunny posts the lowest honest per-gigabyte rates with no request fees, CloudFront's Pro plan is the cheapest published way to push big files under 50 TB, Cloudflare is free-to-cheap for actual web pages with one contract clause to respect, and Fastly sells purge speed and edge compute, not cheap bandwidth.

## What Changed in Late 2025: CloudFront Goes Flat, Fastly Drops Its Fee

Two repricing events reset this market, and both are still missing from most 2026 comparisons.

AWS introduced flat-rate CloudFront plans on November 18, 2025, then expanded the top tier in May 2026. A plan is one monthly price per distribution with no overage charges: Free at $0 (1M requests, 100 GB), Pro at $15 (10M requests, 50 TB), Business at $200 (125M requests, 50 TB), Premium at $1,000 (500M requests, 50 TB), configurable up to 600 TB and 6B requests for $10,000. Every plan bundles WAF, DDoS protection, Route 53 DNS, TLS, logging, edge compute, and monthly S3 storage credits. Exceed the allowance and AWS says it "may serve traffic from fewer or more distant edge locations" — degraded delivery instead of an overage bill. Blocked DDoS and WAF traffic never counts against the quota. Put the same 50 TB on the pay-as-you-go card — 1 TB free, 9 TB at $0.085/GB, 40 TB at $0.080 — and the data alone costs $3,965. Pro costs $15. That is not a discount; it is a different product philosophy: bytes become a quota with a performance caveat instead of a meter.

Fastly repriced on November 4, 2025. New accounts lost the $50/month account fee and gained 100 GB of bandwidth plus 1M requests free each month; requests moved to one global rate of $0.01 per 10,000. The independent analysis at UsagePricing calculates that the unified request rate costs roughly 33% more in North America and Europe than the legacy card, and 38% less in South Korea, India, and Africa. Accounts opened before that date keep the old card — two Fastly customers with identical traffic can receive different bills. The published bandwidth tiers also stop at 20 TB; beyond that you are in a sales conversation, with packages starting at $1,500/month (Basic, 100M requests) and $6,000/month (Starter, 500M requests).

## CDN Pricing at a Glance: Four Meters, Four Bills

Every model here meters two things — bytes and requests — and each vendor meters them differently. Bunny and Cloudflare ignore requests entirely; Fastly and CloudFront bill both. CloudFront's flat-rate plans convert bytes from a meter into a quota.

| Provider | Billing model | Free allowance | Request fees | Floor cost |
| --- | --- | --- | --- | --- |
| Bunny CDN | Per-GB by region; $0.005/GB volume tier | 14-day trial, nothing recurring | None | $1/month minimum |
| Cloudflare | Flat subscription, unmetered bandwidth | Free plan (web pages) | None | $0 |
| Amazon CloudFront | PAYG tiers + optional flat-rate plans | 1 TB + 10M requests/month always free (PAYG); 100 GB + 1M (flat Free) | $0.75–$1.00 per 1M HTTP/HTTPS | $0 |
| Fastly | Per-GB by region + per-request | 100 GB + 1M requests/month (new accounts) | $1.00 per 1M | $0 (new accounts) |

## Bunny: $0.01 a Gigabyte, No Request Fees, a $1 Floor

Bunny is the price anchor every other vendor's marketing has to argue with. The standard network — 119 points of presence — charges $0.01/GB in Europe and North America, $0.03 in Asia and Oceania, $0.045 in South America, and $0.06 in the Middle East and Africa. There are no request fees, a $1 monthly minimum, and an overcharge-protection spending cap you set yourself. Features other vendors paywall — WAF-style protection (Bunny Shield), image optimization, edge scripting — are included at every spend level.

High-volume customers drop to the volume network: 10 PoPs at $0.005/GB for the first 500 TB, $0.004 up to 1 PB, and $0.002 up to 2 PB. At petabyte scale that is $5 per terabyte, a number none of the other three will print on a public page.

Two honest caveats. First, performance: Bunny's own page cites a 24 ms worldwide median against CloudFront's 27 ms (CDNPerf data, March 2025) — vendor math, but consistent with the public CDNPerf ranking, and the gap users feel is measured in milliseconds. Second, Bunny's own 5 TB comparison chart lists CloudFront at "$425+" and Fastly at "$600+" — figures that match the published pay-as-you-go arithmetic exactly (5 TB x $0.085 = $425; 5 TB x $0.12 = $600), so the vendor table holds up against list prices even though it is, obviously, marketing.

What Bunny does not have: a China presence, deep African PoP coverage, or a free tier beyond the trial. For pure byte delivery at list price, nothing else in this comparison comes close.

## CloudFront's Flat-Rate Plans Rewrote the Big-File Mid-Market

The classic CloudFront pricing card still exists and is worth reading once: $0.085/GB for the first 10 TB in the US and Europe, $0.080 for the next 40 TB, $0.060 for the next 100 TB, falling to $0.020 above 5 PB, with HTTPS requests at $1.00 per million and a permanently free 1 TB/month allowance plus 10M requests. Fetching from AWS origins — S3, ALB, anything inside AWS — costs nothing, so the CDN hop often reduces total egress spend rather than adding to it.

Anyone searching CloudFront pricing in 2026, though, should start with the flat-rate decision instead of the per-GB tiers. The $15 Pro plan includes 50 TB that prices out at $3,965 on the usage card — a 99.6% reduction for steady traffic that fits the quota. The binding constraint is requests: Pro includes 10M. Fifty terabytes over 10M requests averages a 5 MB object, which describes video segments, software packages, and game patches — not web pages. A page-heavy site pushing 50 TB at a 100 KB average object runs 500M requests and lands on Business at $200, where the allowance is 125M requests.

Two structural details decide real deployments. The allowance is per distribution, so five sites means five plans (up to 100 per account, and AWS Free Tier accounts cannot subscribe at all). And the content-type restriction that shapes Cloudflare's terms simply does not exist here — video and large downloads are fine on every tier, which is why the Pro plan is the aggressive price point for video and software delivery under quota.

## Cloudflare: Unmetered Bandwidth, One Contract Clause

Cloudflare's pitch looks like a category error: a global CDN across 335+ cities with unmetered bandwidth, starting at $0. Pro costs $20/month billed annually ($25 monthly), Business $200 ($250 monthly), and every plan including Free carries unmetered DDoS mitigation. Add-ons stay flat too: Argo smart routing $5/month, load balancing $5/month, advanced certificate management $10/month. For web pages — HTML, CSS, JS, and the images embedded in them — this is the cheapest CDN on the internet, full stop.

The clause sits in the CDN service-specific terms: "Unless you are an Enterprise customer, Cloudflare offers specific Paid Services (e.g., the Developer Platform, Images, and Stream) that you must use in order to serve video and other large files via the CDN," with the right to "disable or limit your access" if you serve "video or a disproportionate percentage of pictures, audio files, or other large files" without them. That is not a dead letter. Cloudflare's H1 2025 transparency report describes actioning 54,000 abuse reports, terminating 21,000 accounts, and states plainly: "Every second of a typical video requires as much bandwidth as loading a full webpage... we've always restricted use of our free services to deliver streaming video."

Read it as a boundary, not a gotcha: images and scripts inside pages are fine at any volume; a file locker, a video library, or bulk downloads push you onto Stream, Images, or R2 — the zero-egress object storage that still undercuts most S3 bills, as our [object storage comparison](/articles/best-object-storage-pricing-2026-aws-s3-vs-cloudflare-r2-vs-backblaze-b2-vs-wasabi) shows — or onto an Enterprise contract. On those products the "unmetered" story becomes per-minute and per-operation meters, so quote them separately before migrating.

## Fastly: You Pay for Purge Speed and Edge Compute, Not Bandwidth

Fastly pricing makes no attempt to win per-gigabyte. New accounts get 100 GB and 1M requests free monthly, then pay $0.12/GB in North America and Europe for the first 10 TB — twelve times Bunny's rate — and $0.08 for the next 10 TB; the published card stops at 20 TB, then it is a quote. Requests run $1.00 per million after the free million, one global rate.

What the premium buys: a median global purge time under 150 ms, instant invalidation that e-commerce teams and newsrooms treat as revenue-critical, Wasm-based Compute at the edge, and 578 Tbps of capacity aimed at streaming workloads. Procurement bundles formalize it: Basic at $1,500/month for 100M requests, Starter at $6,000 for 500M.

The November 2025 repricing deserves one more sentence in any audit: grandfathering. Accounts opened before November 4, 2025 keep the $50 fee and the cheaper per-region request rates; accounts opened after get the free allowances. Anyone shopping Fastly alternatives on price alone has three cheaper options above; pick Fastly when instant purging or edge compute is the requirement, and budget the bandwidth premium accordingly.

## Four Worked Bills at Real Traffic Levels

The Bunny CDN vs Cloudflare debate usually collapses into "unmetered versus per-GB" without the two numbers that decide everything: content type and request count. The table below fixes traffic to EU/NA-weighted delivery at November 2026 list prices, with the video row shifted to Asia.

| Workload | Bunny CDN | Cloudflare | Amazon CloudFront | Fastly |
| --- | --- | --- | --- | --- |
| 1 TB + 5M requests (blog) | $11 | $0 Free | $0 on PAYG free tier | $108 |
| 10 TB + 10M requests (content site) | $101 | $20–25 Pro | $15 Pro flat ($765 on PAYG) | $1,197 |
| 50 TB + 50M requests (e-commerce) | $501 | $200–250 Business | $200 Business flat ($4,005 on PAYG) | ~$4,400 est. |
| 30 TB video, 5M requests (VOD) | $501 blended (20 TB EU + 10 TB Asia) | Stream/R2 or Enterprise required | $15 Pro flat | ~$3,000 est. |
| 500 TB + 100M requests (bulk delivery) | $2,501 volume tier | ToS risk self-serve; Enterprise quote | $10,000 Premium L6 flat | Quote beyond 20 TB |

Three patterns fall out of the CDN pricing math. First, byte-heavy workloads with modest request counts belong on CloudFront's Pro plan or Bunny — a quota with degraded delivery as the penalty, or a meter with a $1 floor. Second, request-heavy page delivery flips toward Bunny and Cloudflare, because per-request fees accumulate: at 500M requests, CloudFront's usage card adds roughly $500 and Fastly's about the same, while Bunny and Cloudflare add nothing. Third, Cloudflare only wins the rows where the content is actually pages.

| Provider | Request meter | Per 1M HTTPS | Added at 100M requests/mo |
| --- | --- | --- | --- |
| Bunny CDN | None | $0 | $0 |
| Cloudflare | None | $0 | $0 |
| Amazon CloudFront (PAYG) | $0.01 per 10K (US/EU) | $1.00 | ~$100 |
| Fastly | $0.01 per 10K after 1M free | $1.00 | ~$99 |

Fastly's 50 TB figure is a third-party estimate (LatencyCost pegs it near $4,400) because the published card stops at 20 TB; treat both Fastly estimates as sales-quote territory. CloudFront's PAYG figures use the always-free 1 TB plus the tiered rates above. The origin side of this stack carries its own bill — the [VPS pricing comparison](/articles/best-vps-hosting-2026-hetzner-vs-digitalocean-vs-vultr-vs-linode) covers where the bytes come from, and the [Heroku alternatives breakdown](/articles/heroku-alternatives-2026-railway-vs-render-vs-flyio-pricing-compared) shows how PaaS platforms meter the same egress at $0.02–$0.15 per GB.

## Frequently Asked Questions

### Is Bunny CDN cheaper than Cloudflare?

For byte delivery, yes, and it is not close: $10 per terabyte in EU/NA against Cloudflare's flat plans, with no request fees on either side of the ledger. The Bunny CDN vs Cloudflare comparison only reverses when traffic is actual web pages, where Cloudflare's Free and Pro plans serve HTML, CSS, and embedded images unmetered for $0–$25 total. When the content is video or bulk files, Cloudflare's terms require Stream, R2, or Enterprise, and Bunny's $0.01–$0.03/GB undercuts all of them at list price.

### What is the cheapest CDN for video streaming?

Under 50 TB per month with under 10M requests, CloudFront's $15 Pro plan — video is explicitly allowed on every CloudFront tier. Above the quota or with more requests, Bunny at $0.01/GB EU-NA and $0.03 in Asia with no request fees is the cheapest metered option. Cloudflare requires its paid video products or an Enterprise contract; Fastly's list rates run twelve times Bunny's in EU/NA. At petabyte scale, Bunny's volume network at $0.005/GB is the lowest published rate among the four.

### Does Cloudflare charge for bandwidth?

No. Bandwidth is unmetered on every plan from Free to Business, with unmetered DDoS protection included. The limit is contractual, not financial: the CDN service-specific terms require Cloudflare's paid products (Stream, Images, R2) or an Enterprise agreement for video and other large files, and the 2025 enforcement actions show the clause gets applied in practice.

### How much does Amazon CloudFront cost per GB?

On pay-as-you-go, $0.085/GB for the first 10 TB in the US and Europe, tiered down to $0.020 above 5 PB, with the first 1 TB per month permanently free and HTTPS requests at $1.00 per million. On flat-rate plans, $15/month includes 50 TB (10M requests), $200 includes 50 TB (125M requests), and $1,000 includes 50 TB (500M requests, configurable to 600 TB for $10,000). Exceeding an allowance degrades performance instead of billing an overage.

### What did Fastly change in its pricing?

On November 4, 2025, Fastly removed the $50 monthly account fee for new accounts and added 100 GB of bandwidth and 1M requests free per month, moving requests to a single global rate of $0.01 per 10,000 — about 33% higher in North America and Europe than the legacy card, about 38% lower in South Korea, India, and Africa. Accounts opened earlier keep the old card, so two customers with identical traffic can pay differently. The published bandwidth tiers stop at 20 TB; beyond that, pricing goes through sales.

## The Bottom Line

CDN pricing in 2026 splits by content type more than by vendor, and the four-week repricing wave of late 2025 made the old comparisons obsolete. Serve web pages: Cloudflare's Free or Pro plan is unbeatable, provided your media lives inside pages rather than beside them. Serve large files under 50 TB with fewer than 10M requests: CloudFront's $15 Pro plan is the most aggressive published offer this market has seen. Serve bytes on a meter with high request counts or many sites: Bunny's $0.01/GB, no request fees, and $1 floor make it the honest default. Need sub-150 ms purges and Wasm compute for streaming or publishing: that is Fastly's product, and the bandwidth premium is its price — anyone evaluating Fastly alternatives on cost alone should start with Bunny and CloudFront flat-rate instead.

One habit worth keeping: re-run this math annually. CloudFront's 50 TB allowance collapsed from $3,965 to $15 in a single announcement. Per-GB list prices are negotiation anchors, not truths, and the vendors have now proven twice in one month that they will move them."""
}

def main():
    path = "data/articles_en.json"
    with open(path, encoding="utf-8") as f:
        arts = json.load(f)
    if any(a["slug"] == ARTICLE["slug"] for a in arts):
        raise SystemExit("Slug already exists: " + ARTICLE["slug"])
    arts.append(ARTICLE)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(arts, f, ensure_ascii=False, indent=2)
    print("Appended. Total articles:", len(arts))

if __name__ == "__main__":
    main()
