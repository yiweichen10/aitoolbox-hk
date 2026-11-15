# -*- coding: utf-8 -*-
"""Append article #222 (Static Hosting Pricing 2026) to data/articles_en.json.
Runs validation first; aborts (exit 1) without writing if any check fails.
"""
import json, re, sys

SLUG = "best-static-hosting-pricing-2026-netlify-vs-vercel-vs-cloudflare-pages-vs-github-pages"

ARTICLE = {
    "title": "Static Hosting Pricing in 2026: Netlify vs Vercel vs Cloudflare Pages vs GitHub Pages",
    "slug": SLUG,
    "date": "2026-11-15",
    "dateFull": "November 15, 2026",
    "category": "AI Infrastructure",
    "description": "Static hosting pricing compared for 2026: Netlify credit plans, Vercel Flat Rate CDN tiers, Cloudflare Pages' unlimited static delivery, and GitHub Pages limits. Worked bills from 20 GB to 5 TB.",
    "keywords": [
        "static hosting pricing",
        "netlify vs vercel pricing",
        "vercel flat rate cdn",
        "vercel bandwidth pricing",
        "netlify credits",
        "cloudflare pages pricing",
        "github pages limits",
        "cheapest static hosting",
        "static site hosting",
        "vercel hobby commercial use"
    ],
    "content": """The same static site pushing one terabyte of traffic a month bills at $5 on Cloudflare, $20 on Vercel under its Flat Rate CDN, about $199 on Netlify's credit-based Personal plan, and $0 on GitHub Pages — if you are willing to violate GitHub's commercial-use policy to get it. That is a 40x spread on identical traffic, and it means the platform you pick without reading the rate card can cost 10x more than the one your competitor picked. Two of the four vendors rewrote their pricing inside the last 14 months: Netlify moved every new account onto a credit system on September 4, 2025, and Vercel replaced per-gigabyte overage math with Flat Rate CDN capacity tiers. Cloudflare quietly folded Pages billing into Workers. Anyone comparing static hosting pricing on a two-year-old blog post is comparing rate cards that no longer exist.

This guide rebuilds the comparison from the current official pricing pages (all checked November 15, 2026), runs four traffic scenarios through real bills, and flags the terms-of-service clauses — Netlify's one-way migration, Vercel's Hobby commercial ban, GitHub Pages' outright prohibition on business sites — that decide whether a plan is actually usable.

## Static Hosting Pricing at a Glance

Four platforms, four billing philosophies. Netlify meters everything through credits. Vercel meters bandwidth unless you opt into flat tiers. Cloudflare meters Worker compute and gives static asset delivery away. GitHub meters nothing and polices usage with a policy document instead.

| Platform | Free tier | Paid entry | Bandwidth overage | Overage protection | Commercial use on free tier |
|---|---|---|---|---|---|
| Netlify | 300 credits/mo (~15 GB or 1.5M requests) | Personal $9/mo | 20 credits/GB (~$0.20) | Auto recharge, opt-in | Allowed |
| Vercel | 100 GB + 1M CDN requests | Pro $20/seat/mo | $0.15/GB on-demand | Flat Rate CDN tiers | No — Hobby is non-commercial only |
| Cloudflare Pages | Unlimited static asset requests | Workers Paid $5/mo | $0 — no egress fee | No meter to exceed | Allowed |
| GitHub Pages | 100 GB/mo soft cap | GitHub Pro $4/mo | None — no billing at all | None — overuse means throttling | Banned |

Three things stand out. First, the free tiers are no longer comparable: Vercel still hands Hobby users 100 GB a month, Netlify's credit conversion cuts that to roughly 15 GB for new accounts, and Cloudflare does not count static traffic at all. Second, only Cloudflare's bandwidth price is $0 in writing; GitHub's is $0 by absence of a billing system, enforced by a soft cap GitHub can revoke. Third, the paid floors span $4 to $20 a month before a single overage, and that $16 gap buys very different things — Vercel's floor includes a 1 TB Flat Rate CDN tier, Netlify's includes unlimited team seats.

## Netlify Credits Explained: What 300 Free Credits Actually Buys

Since September 4, 2025, every new Netlify account runs on credits. One credit is worth about a cent: auto-recharge packs sell 500 credits for $5 on Personal and 1,500 for $10 on Pro. The official meter rates stack up like this:

- **Web bandwidth: 20 credits per GB** — about $0.20 at Personal recharge rates, roughly $0.13 at Pro's pack rate
- **Web requests: 2 credits per 10,000** — about $1 per million requests
- **Production deploys: 15 credits each**
- **Function compute: 10 credits per GB-hour**

The 300-credit Free allowance converts to about 15 GB of bandwidth, or 1.5 million requests, or 20 production deploys — if you spend every credit on one resource. Sites that mix deploys and traffic hit the hard limit sooner, and Free has no auto recharge: when credits run out, serving stops. The $9 Personal tier exists for that moment: 1,000 credits (50 GB), with opt-in recharges in $5 blocks.

Pro starts at $20 a month with 3,000 credits (150 GB), scales to 20,000 credits, adds unlimited team members — the only plan here where seats cost nothing extra — and rolls unused credits into the next cycle on tiers of 5,000 or more.

One more thing worth knowing before you migrate in: accounts created before September 4, 2025 keep the legacy plans, with 100 GB of included bandwidth and $55-per-100-GB overage blocks. You cannot move back to a legacy plan after switching to credits. Netlify's own docs call the change permanent.

## Vercel Flat Rate CDN Changed the Math

Vercel bandwidth pricing runs on-demand at $0.15 per GB of Fast Data Transfer and $2.00 per million CDN requests. The Hobby plan includes 100 GB and 1 million requests free — still the largest raw bandwidth number among the metered platforms — but Hobby carries a restriction that matters more than the quota. Vercel's fair use policy restricts Hobby to "non-commercial personal use only": running ads, affiliate links as the site's primary purpose, or charging for anything all count as commercial. Asking for donations, notably, does not. Any commercial deployment "requires either a Pro or Enterprise plan."

Pro costs $20 per developer seat per month (viewer seats are free) and includes $20 of usage credit. The genuinely new part is Flat Rate CDN, which swaps per-unit billing for capacity tiers:

| Tier | CDN requests | Data transfer | Monthly price |
|---|---|---|---|
| Tier 1 — included with Pro | 1M | 1 TB | $20 |
| Tier 2 | 10M | 50 TB | $100 |
| Tier 3 | 50M | 50 TB | $300 |
| Tier 4 | 150M | 50 TB | Higher — on-demand above it |

The mechanics favor predictability: Vercel sizes your tier on typical monthly usage, and a one-day spike does not trigger an upgrade — the tier only moves at the start of the next billing cycle. Exceed the top tier and you fall back to on-demand rates. Compared with on-demand pricing, the included 1 TB tier breaks even at about 133 GB of monthly transfer ($20 divided by $0.15); past that point every gigabyte is effectively $0.02 instead of $0.15.

The catch is scope. Flat Rate CDN excludes bulk file distribution, media delivery where files are the majority of bandwidth, and storage-style hosting — Vercel can move violating projects onto its throttled Flex network. The 50 TB tier is for web apps, not for serving your users' uploads. Heavy file delivery belongs on object storage or a [CDN that prices video honestly](/articles/best-cdn-pricing-2026-bunny-vs-cloudflare-vs-fastly-vs-cloudfront-compared).

## Cloudflare Pages Pricing Is Now Workers Pricing

Search for a Cloudflare Pages pricing page in 2026 and you land on a 404 — Pages billing now lives inside the Workers pricing docs, and Pages Functions are billed as Workers. The facts that matter for static site hosting:

Static asset requests are free and unlimited, in writing, on both plans. The Free plan also includes 100,000 Worker requests per day for anything dynamic. Workers Paid carries a $5 monthly minimum and includes 10 million Worker requests and 30 million CPU milliseconds; beyond that, requests cost $0.30 per million and CPU time $0.02 per million. There is no data transfer charge at all — Cloudflare's pricing page states plainly that "there are no additional charges for data transfer (egress) or throughput (bandwidth)."

Cloudflare's own worked example makes the point: a project serving 15 million requests a month where 80% hit static assets costs $5.00 total — the subscription fee, nothing else. The same traffic profile billed through Netlify's credit meter works out to roughly $120–$180 a month depending on which recharge pack applies. For pure static delivery with real traffic, Cloudflare Pages pricing is the floor every other vendor prices against.

One date to watch: Workers Logs switches to Cloudflare's Observability pricing on December 1, 2026, so heavy logging under the $5 plan gets more expensive from December onward. Static delivery itself is untouched.

## GitHub Pages Limits and the Commercial-Use Ban

GitHub Pages remains the only option here with no billing system at all, which is both its appeal and its trap. The published limits: a soft bandwidth cap of 100 GB per month, a soft limit of 10 builds per hour (waived when you publish through a custom GitHub Actions workflow), a 1 GB ceiling on the published site, and deploys that time out at 10 minutes.

Then there is the clause that disqualifies half the use cases outright. GitHub's docs state that Pages "is not intended for or allowed to be used as a free web-hosting service to run your online business, e-commerce site, or any other website that is primarily directed at either facilitating commercial transactions or providing commercial software as a service (SaaS)." Exceed the soft caps and the consequence is not an invoice — it is an email from GitHub Support suggesting a CDN or another host, or the site simply not being served.

For what it is built for — documentation, portfolios, open-source project sites — Pages is genuinely free, and private-repo Pages only needs GitHub Pro at $4 a month or Team at $4 per user. For anything that earns money, it is a terms-of-service violation with a shutdown date attached.

## Worked Bills: Four Traffic Levels, Four Platforms

Rates only matter when they hit a bill, so here is static hosting pricing run through four common traffic profiles, using each platform's current rate card and fixed assumptions: solo operator, 50 KB pages, 20 deploys a month, monthly billing.

| Scenario | Netlify | Vercel | Cloudflare Pages | GitHub Pages |
|---|---|---|---|---|
| Hobby blog — 20 GB/mo, non-commercial | $0 (300 credits) | $0 (Hobby) | $0 (Free) | $0 |
| Portfolio — 60 GB/mo, runs ads | $39 ($9 + 150 GB x $0.20) | $20 Pro (1 TB Flat Rate tier) | $0 (Free) | Not allowed |
| Product site — 1 TB/mo | $199 ($9 + 950 GB x $0.20) | $20 (Flat Rate Tier 1) | $5 (Workers Paid) | 100 GB cap — will throttle |
| App delivery — 5 TB/mo | $999 ($9 + 4,950 GB x $0.20) | $100 (Flat Rate Tier 2) | $5 (Workers Paid) | Cap exceeded — throttle or migrate |

The 1 TB row is the headline. Netlify's meter charges $0.20 per gigabyte at Personal recharge rates, so 950 GB of overage lands the bill near $199. Vercel's Flat Rate CDN includes the full terabyte inside the $20 Pro subscription. Cloudflare charges nothing for static delivery, so the bill is the $5 subscription floor. Same traffic, 40x difference — and the ordering stays stable at 5 TB, where Netlify crosses four figures and Vercel's $100 tier covers fifty.

The portfolio row exposes the free-tier traps. A portfolio running ads is commercial under both Vercel's and GitHub's definitions, which leaves Netlify's $9 Personal tier (1,000 credits cover 50 GB) and Cloudflare's genuinely free unlimited tier. GitHub Pages is the only column with "not allowed" written into it, and Vercel Hobby's $0 carries the same asterisk. If the site needs real backend compute — cron jobs, queues, long-running processes — static hosts are the wrong category entirely; the [PaaS alternatives comparison](/articles/heroku-alternatives-2026-railway-vs-render-vs-flyio-pricing-compared) covers where that spend belongs.

| Your situation | Pick | Why | Likely bill |
|---|---|---|---|
| Docs or open-source project site | GitHub Pages | Free within policy, Actions deploys | $0 |
| Static site with real traffic, no server code | Cloudflare Pages | Unlimited static requests, $5 floor | $0–$5 |
| Next.js app, mixed static and functions | Vercel Pro | Flat Rate CDN plus function compute on one bill | $20–$100 |
| Team of 3+, frequent deploys, previews | Netlify Pro | Unlimited seats, free deploy previews, credit rollover at 5K | $20+ |

## Netlify vs Vercel Pricing: The Head-to-Head

The two metered incumbents now diverge on every axis worth measuring, and the netlify vs vercel pricing question has different answers depending on which meter dominates your bill. At 1 TB of traffic it is roughly $199 against $20, an order of magnitude. At the request meter, Netlify charges about $1 per million requests against Vercel's $2.00 — half the rate. On seats, the polarity flips: Netlify Pro includes unlimited team members while Vercel charges $20 per developer seat, so a five-developer team pays $100 a month on Vercel against $20 on Netlify before any traffic.

Both carry migration locks worth reading twice. Netlify's credit switch is permanent — legacy accounts that move cannot move back. Vercel's Flat Rate CDN comes with fair-use exclusions that let the company re-tier throttled projects. Neither trap fires on ordinary web apps, but both reward re-checking the current terms before an annual commitment, because this category re-prices itself every year.

## Frequently Asked Questions

### Is Cloudflare Pages really free for unlimited bandwidth?
Yes for static assets. Cloudflare's pricing docs state that requests to static assets are free and unlimited on both the Free and Workers Paid plans, and there is no egress or bandwidth fee. You pay only when code runs — Workers, Pages Functions, D1, KV — and the Workers Paid plan has a $5 monthly minimum. A purely static site that never invokes a Worker can run on the Free plan at $0 indefinitely.

### What is Vercel Flat Rate CDN and is it worth it?
It is Vercel's capacity-tier billing for content delivery: $20 a month covers 1 million CDN requests and 1 TB of transfer, $100 covers 10 million requests and 50 TB, and $300 covers 50 million requests at the same 50 TB. Against on-demand rates of $0.15 per GB, the included 1 TB tier breaks even at about 133 GB of monthly transfer. It only covers standard web delivery — bulk file distribution and media-heavy projects are excluded by fair use guidelines and can be moved to a throttled network.

### Can I run my business site on GitHub Pages?
No. GitHub's documentation explicitly disallows using Pages for an online business, e-commerce, or SaaS, and exceeding the 100 GB soft bandwidth cap risks throttling or an email suggesting you move to another host. Pages is fine for docs and non-commercial projects. For anything commercial, Cloudflare Pages' unlimited static delivery or a $5 Workers plan is the compliant route.

### What happened to Netlify's free 100 GB bandwidth?
New accounts since September 4, 2025 get 300 credits a month instead — worth roughly 15 GB of bandwidth at 20 credits per GB. Accounts created before that date keep the legacy plans, with 100 GB included and $55 per additional 100 GB, and cannot switch back after moving to credits. If you are on a legacy plan with real traffic, staying put is currently the cheaper deal.

### Which is the cheapest static hosting for a personal portfolio?
Cloudflare Pages is $0 with unlimited static requests and no commercial-use asterisk, which makes it the cheapest static hosting choice for a portfolio that might earn money someday. GitHub Pages is also $0 if the portfolio carries no ads or paid engagements. Vercel's Hobby tier is $0 but the Vercel Hobby commercial use rule restricts it to non-commercial personal projects, and Netlify's Free plan works only under roughly 15 GB of monthly traffic given its 300-credit hard limit.

## Bottom Line

Static hosting pricing in 2026 splits cleanly by traffic volume rather than by brand loyalty. Under 15 GB a month, every platform here is $0 and the decision is workflow, not cost. Between 50 GB and a terabyte, Cloudflare Pages is the price anchor — $0 to $5 against $20-plus on the metered platforms — and Vercel's Flat Rate CDN is the only metered option that makes bandwidth math stop mattering. Past a terabyte of app delivery, Vercel's $100 tier covers 50 TB while Netlify's credit meter crosses $999 at 5 TB. GitHub Pages stays free for docs and portfolios and off-limits for business.

Two warnings to carry forward. First, rate cards in this category now expire: Netlify's credit system is one-way for accounts that switch, and Vercel has already restructured CDN billing once. Re-check the official pages before any annual commitment. Second, the free tiers carry terms, not just quotas — Vercel and GitHub both ban commercial use on their $0 plans, and "free" that ends in a takedown notice is not free. If heavy downloads are part of the plan, pair the static site with storage priced for it; the [object storage comparison](/articles/best-object-storage-pricing-2026-aws-s3-vs-cloudflare-r2-vs-backblaze-b2-vs-wasabi) covers the zero-egress options that pair naturally with Pages. The cheapest platform is the one whose bill and terms you have actually read."""
}

PK = "static hosting pricing"
BANNED = ["leverage", "utilize", "seamlessly", "game-changing", "empower", "streamline",
          "delve into", "transformative", "comprehensive", "revolutionize", "cutting-edge",
          "as an AI", "in conclusion"]
INTERNAL_LINKS = [
    "/articles/best-cdn-pricing-2026-bunny-vs-cloudflare-vs-fastly-vs-cloudfront-compared",
    "/articles/heroku-alternatives-2026-railway-vs-render-vs-flyio-pricing-compared",
    "/articles/best-object-storage-pricing-2026-aws-s3-vs-cloudflare-r2-vs-backblaze-b2-vs-wasabi",
]

def main():
    content = ARTICLE["content"]
    errors = []

    # 1. word count (split convention)
    wc = len(content.split())
    print(f"[CHECK] word count (split): {wc}")
    if not (2200 <= wc <= 2800):
        errors.append(f"word count {wc} out of range 2200-2800")

    # 2. PK count, case-insensitive, content only
    pk_count = len(re.findall(re.escape(PK), content, re.IGNORECASE))
    print(f"[CHECK] PK '{PK}' count: {pk_count}")
    if pk_count != 4:
        errors.append(f"PK count {pk_count} != 4")

    # 3. banned words
    low = content.lower()
    for w in BANNED:
        if w in low:
            errors.append(f"banned word present: {w}")
    print(f"[CHECK] banned words: {'CLEAN' if not any(w in low for w in BANNED) else 'FOUND'}")

    # 4. long-tail keywords present in content
    for kw in ARTICLE["keywords"]:
        n = len(re.findall(re.escape(kw.lower()), low))
        flag = "OK" if n > 0 else "MISSING"
        print(f"[CHECK] long-tail '{kw}': {n}x {flag}")
        if n == 0:
            errors.append(f"long-tail missing from body: {kw}")

    # 5. internal links
    found = [u for u in INTERNAL_LINKS if f"]({u})" in content]
    print(f"[CHECK] internal links found: {len(found)}/{len(INTERNAL_LINKS)}")
    if len(found) < 2:
        errors.append("fewer than 2 internal links")

    # 6. FAQ H3 count
    h3 = re.findall(r"^### (.+)$", content, re.M)
    faq = len(h3)
    print(f"[CHECK] H3 headings: {faq} ({[h[:40] for h in h3]})")
    if faq < 3:
        errors.append("fewer than 3 H3 headings")

    # 7. markdown tables: rows >= 4 (data rows), cols >= 4
    tables = []
    cur = []
    for line in content.splitlines():
        if line.strip().startswith("|"):
            cur.append(line.strip())
        else:
            if cur:
                tables.append(cur)
                cur = []
    if cur:
        tables.append(cur)
    print(f"[CHECK] tables detected: {len(tables)}")
    big = 0
    for t in tables:
        ncols = t[0].count("|") - 1
        nrows = len(t) - 2  # minus header + separator
        print(f"        table: {nrows} rows x {ncols} cols")
        if nrows >= 4 and ncols >= 4:
            big += 1
    if big < 1:
        errors.append("no comparison table with >=4 rows and >=4 cols")

    if errors:
        print("\n[FAIL] validation errors:")
        for e in errors:
            print("  -", e)
        sys.exit(1)

    # append
    path = "data/articles_en.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if any(a["slug"] == SLUG for a in data):
        print("[ABORT] slug already exists:", SLUG)
        sys.exit(1)
    data.append(ARTICLE)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n[OK] appended article #{len(data)} -> {path} (total {len(data)} articles)")

if __name__ == "__main__":
    main()
