# -*- coding: utf-8 -*-
"""Append article #223: Serverless Functions Pricing 2026 (Lambda vs Workers vs Vercel vs Deno Deploy).
All prices verified from official rate cards on 2026-11-16.
"""
import json

SLUG = "best-serverless-functions-pricing-2026-aws-lambda-vs-cloudflare-workers-vs-vercel-vs-deno-deploy"

ARTICLE = {
    "title": "Serverless Functions Pricing in 2026: AWS Lambda vs Cloudflare Workers vs Vercel vs Deno Deploy",
    "slug": SLUG,
    "date": "2026-11-16",
    "dateFull": "November 16, 2026",
    "category": "AI Infrastructure",
    "description": "Serverless functions pricing compared across AWS Lambda, Cloudflare Workers, Vercel, and Deno Deploy: wall-clock vs active-CPU billing, free tier limits, and worked bills from 10M to 100M requests.",
    "keywords": [
        "serverless functions pricing",
        "aws lambda pricing",
        "lambda cost per million requests",
        "aws lambda free tier",
        "cloudflare workers pricing",
        "cloudflare workers free tier",
        "vercel serverless functions pricing",
        "vercel functions pricing",
        "deno deploy pricing",
        "cheapest serverless functions",
        "lambda vs cloudflare workers",
        "serverless cost per million requests",
    ],
    "content": """The same API serving ten million requests in a month bills at $5.80 on Cloudflare Workers, $7.00 on AWS Lambda, about $10 on Vercel before credits, and $30.06 on Deno Deploy. That is a 5x spread for code doing the identical job on identical traffic. Make that API wait on a database for a fifth of every request and the ranking inverts: Lambda climbs to $18.67 while Workers stays at $8.40. Each platform bills a different quantity — wall-clock duration, active CPU time, provisioned memory, or raw request counts — so the sticker rate on the homepage tells you almost nothing. Serverless functions pricing in 2026 is a billing-model question before it is a rate question. This piece reads all four official rate cards as published in November 2026, pushes the same three workloads through each meter, and reduces the choice to one ratio from your own traces.

## Serverless Functions Pricing at a Glance

None of the four vendors meters compute the same way; the table below is the argument in one screen.

| Platform | Entry paid plan | Included requests | Included compute | Overage rates |
| --- | --- | --- | --- | --- |
| AWS Lambda | none — pure pay-as-you-go | 1M/mo (always-free tier) | 400K GB-seconds/mo | $0.20/M requests + $0.0000166667/GB-s |
| Cloudflare Workers | $5/mo | 10M/mo | 30M CPU-ms | $0.30/M requests + $0.02/M CPU-ms |
| Vercel (Pro) | $20/seat | none — billed on demand | none — $20 monthly usage credit | $0.60/M invocations + $0.128/CPU-hr + $0.0106/GB-hr (US east) |
| Deno Deploy (Pro) | $20/mo | 5M/mo | 50 CPU-hr + 750 GiB-hr | $2/M requests + $0.10/CPU-hr + $0.025/GiB-hr |

## AWS Lambda Pricing: The Wall-Clock Meter

AWS Lambda pricing starts from two numbers: $0.20 per million requests and $0.0000166667 per GB-second of duration in us-east-1, with duration rounded up to the nearest millisecond. The GB-second rate is the trap. Lambda bills the entire window between code start and return, and the current rate card states that billed duration includes initialization code outside the handler — so I/O waits, connection pools, and cold-start module loads all cost compute money. Memory scales from 128 MB to 10,240 MB in 1 MB steps, and CPU allotment scales with it — which is why 512 MB remains the sensible default for I/O-shaped APIs.

The aws lambda free tier knocks out the first million requests and 400,000 GB-seconds every month, permanently. At 512 MB, that allowance covers roughly 800,000 wall-clock seconds of runtime — enough to hold a genuine side project at $0. Graviton (arm64) runs about 20% cheaper per GB-second, so build for arm unless an x86-only dependency stops you.

Two costs sit outside the headline pair. Responses to the internet bill at EC2 data-transfer rates — a line most estimates forget until the first invoice. Second, AWS spent the last year bolting on new product lines with their own meters: Lambda Managed Instances (EC2 capacity plus a 15% management fee for steady workloads that outgrew per-request billing), Durable Functions ($8.00 per million workflow operations plus $0.25/GB written), and Web Functions — $0.30 per million requests billed on active CPU, which is AWS quietly shipping the same meter Cloudflare and Vercel already use. The rate card grows more entries every year; the classic Event Functions column still runs most bills.

## Cloudflare Workers Pricing: Billed for CPU, Not for Waiting

Cloudflare Workers pricing collapses the bill into two variables: requests and CPU time. The $5 monthly plan includes ten million requests and 30 million CPU milliseconds; past that, $0.30 per additional million requests and $0.02 per additional million CPU milliseconds. Wall-clock duration carries no charge beyond a 5-minute CPU ceiling per invocation. Waiting on a database is free. So is egress — Cloudflare charges nothing for outbound data transfer — and static-asset requests are free and unlimited, the same zero-egress logic behind our [static hosting comparison](/articles/best-static-hosting-pricing-2026-netlify-vs-vercel-vs-cloudflare-pages-vs-github-pages) and [CDN pricing breakdown](/articles/best-cdn-pricing-2026-bunny-vs-cloudflare-vs-fastly-vs-cloudfront-compared).

Cloudflare's own worked example doubles as this article's benchmark: 15 million requests at 7 ms of average CPU lands at $8.00 per month, and the same shape at 100 million lands at $45.40. Both numbers reappear in the table below.

The free plan is the most generous here on volume: 100,000 requests per day — about three million a month — against Lambda's one million and Deno's one million. The ceiling is 10 ms of CPU per invocation on 128 MB of memory — excludes image work and heavy JSON munging, covers most API handlers. One dated line item: Workers Logs moves to Cloudflare's Observability pricing on December 1, 2026, so log-heavy Workers should re-check their bill that month.

## Vercel Functions Pricing: Three Meters and a $20 Credit

Vercel functions pricing under Fluid compute runs three meters at once, priced per region. Active CPU bills only while your code executes — $0.128 per CPU-hour in the cheapest US regions (iad1, pdx1, cle1) — and pauses while the function waits on an API call or a query. Provisioned memory bills the whole instance lifetime whether or not the CPU is busy: $0.0106 per GB-hour in those same regions. Invocations add $0.60 per million on Pro. A request that burns 7 ms of CPU inside a 60 ms wall on a 1 GB instance costs roughly $0.0009 — cheap per call, but the three-line math stacks up faster than Workers' two-line math.

Hobby includes 1 million invocations, 4 hours of active CPU, and 360 GB-hours of memory per month — a personal, non-commercial plan. Exceeding its limits pauses your deployment with a 503 that does not clear itself for 30 days. Pro flips the model: nothing is included, everything bills on demand, and the plan's $20 monthly usage credit absorbs the first $20 of it. For a Next.js shop already deployed on Vercel, functions ride the same deploy pipeline and the same credit — that convenience is the product, and the per-unit rates are the price of it.

## Deno Deploy Pricing: Simple Cards, Pricey Requests

Deno Deploy pricing is the easiest card to read and the hardest to outgrow. Free covers 1 million requests, 10 hours of active CPU, 150 GiB-hours of memory time (at a fixed 768 MB), and 20 GiB of egress; idle apps shut down after 20-30 seconds, so memory stops billing at scale-to-zero. Pro, at $20, lifts that to 5 million requests, 50 CPU-hours, and 750 GiB-hours — then bills $2 per additional million requests, $0.10 per CPU-hour, and $0.025 per GiB-hour.

That request rate is the problem. $2 per million is 6.7x Cloudflare's request overage, and at 100 million requests the overage alone is $190 — on top of the $20 base, and worse on the $200 Builder plan (25 million included, then the same $2/M, which works out to $350 at that volume). Deno's counters are honest and the developer experience is clean — TypeScript first, KV built in, no cold-config — but the economics only hold under five million requests a month. A reliability SLA exists only on Enterprise.

## Worked Bills: The Same Code on Four Meters

The numbers below are what serverless functions pricing actually costs once the meters start running. Fix three workloads, hold them constant, price everything in US regions. API A is the common case: 7 ms of CPU and 60 ms of wall time per request — I/O waiting on a cache or a quick query — on 512 MB of Lambda memory and 1 GB of Vercel instances. API B is the database-heavy case: 20 ms of CPU inside a 200 ms wall. Serial concurrency is assumed for memory billing on Vercel and Deno; their concurrency optimizations only shrink those numbers. Internet egress is excluded everywhere, because each platform meters it differently.

| Platform | API A: 10M requests | API A: 100M requests | API B (I/O-heavy): 10M requests | What moves the number |
| --- | --- | --- | --- | --- |
| AWS Lambda (512 MB) | $7.00 | $70.00 + egress | $18.67 | wall-clock duration bills every I/O wait |
| Cloudflare Workers ($5 plan) | $5.80 | $45.40 | $8.40 | requests + CPU-ms only; duration and egress free |
| Vercel Pro (US east) | ~$10.26 → $0 with credit | ~$102.56 → ~$83 with credit | ~$19.00 → $0 with credit | memory bills through I/O waits; credit offsets small bills |
| Deno Deploy Pro | $30.06 | $210.00 | $30.56 | $2/M request overage dominates above 5M |

Lambda at ten million API-A requests: $2.00 of requests plus 300,000 GB-seconds of duration — $5.00 — for $7.00 all-in. At one hundred million: $20 plus $50, or $70 before a cent of egress. Workers: the $5 plan covers all ten million requests and 30M of the 70M CPU-ms, so $5.80; at 100 million it is exactly Cloudflare's published $45.40. Vercel at ten million: $2.49 of active CPU (19.4 CPU-hours), $6.00 of invocations, and $1.77 of memory — $10.26, zeroed out by the Pro credit. Deno: $20 base plus $10 of request overage, $30.06 all-in. Serverless cost per million requests is not one number; it is a function of how much of each request your meter is watching.

Now the inversion. API B's 200 ms walls push Lambda's duration bill to $18.67, while Workers — which stops billing at the 20 ms CPU boundary — lands at $8.40. Flip the shape the other way, to 8 ms of wall against 7 ms of CPU, and Lambda wins outright: $2.67 for ten million requests against Workers' $5.80, because a GB-second of x86 at 512 MB is a tighter unit than Workers' request-plus-CPU pair. The ranking you get depends entirely on where the wall clock and the CPU clock diverge.

## Lambda vs Cloudflare Workers: Compute the Ratio, Then Choose

Lambda vs cloudflare workers reduces to one ratio: wall time divided by CPU time, taken from your own traces. Above roughly 5-to-1 — genuinely I/O-bound APIs — Workers' CPU-only meter wins, and the gap widens with scale. Below 2-to-1 — image resizing, PDF rendering, encryption, anything where the process is actually running — Lambda's per-GB-second rate wins, and x86 or Graviton binaries run unmodified. In between, price them out; the worked bills above show a band where either could win.

The second difference is runtime, not money. Lambda runs full Node, Python, Java, .NET, or Go in up to 10 GB of memory with no API changes. Workers runs V8 isolates on a Web-standard API surface — Node compatibility has improved sharply, but npm modules that touch the filesystem, spawn processes, or load native bindings still need rework. That portability cost is real money the rate card never shows. If the rewrite costs an engineer-week, Workers' $45 versus Lambda's $70 at 100 million requests pays back inside a month; at 10 million requests the $1.20 monthly difference never will. And if the workload is really a queue consumer or a long-running state machine, it belongs on one of the [background job schedulers](/articles/best-background-job-schedulers-2026-inngest-vs-triggerdev-vs-temporal-vs-hatchet) we compared, not on either function meter.

Vercel and Deno fit narrower slots. Vercel wins when the frontend already lives there and the $20 credit covers a small API; its fluid model is the most graceful of the active-CPU meters about I/O, but memory billing through waits and $0.60/M invocations add up at volume. Deno wins on TypeScript ergonomics and a genuinely usable free tier, with a request-rate cliff past 5 million as the tax.

## The Free Tiers, and the Cheapest Serverless Functions to Start

Every platform here has a real free tier — the differences are ceilings, not marketing. The cloudflare workers free tier allows 100,000 requests a day with a 10 ms CPU cap per call, the highest request volume on this list. Lambda's always-free allowance covers 1 million requests and 400,000 GB-seconds monthly — the deepest compute allowance here, and it never expires. Deno's free plan includes 10 hours of CPU on real requests with automatic scale-to-zero. Vercel Hobby includes 1 million invocations but forbids commercial use, which quietly disqualifies anything with a revenue link on it.

| Platform | Free requests | Free compute | Memory | Commercial use |
| --- | --- | --- | --- | --- |
| AWS Lambda | 1M per month | 400K GB-seconds per month | pay-as-you-go from 128 MB | allowed |
| Cloudflare Workers | 100K per day (~3M per month) | 10 ms CPU per invocation | 128 MB per isolate | allowed |
| Vercel Hobby | 1M invocations per month | 4 CPU-hours per month | 360 GB-hours included | not allowed |
| Deno Deploy Free | 1M per month | 10 CPU-hours per month | 150 GiB-hours (768 MB fixed) | personal projects |

The cheapest serverless functions for a side project, in order: Workers if daily traffic stays under 100,000 and handlers stay light; Lambda if traffic is bursty and compute-heavy, because the GB-second allowance absorbs long-running jobs; Deno if you want TypeScript without configuration; Vercel Hobby only for portfolios and prototypes.

## Frequently Asked Questions

### How much does AWS Lambda cost per million requests?

The request line is $0.20 per million, always. The compute line depends on shape: lambda cost per million requests at 512 MB and 100 ms of wall time works out to $0.83 of GB-seconds (50,000 GB-seconds at $0.0000166667) plus $0.20 of requests — about $1.03 per million all-in. Halve the memory and you halve the compute line; double the wall time and you double it. Internet egress is the line item that can exceed both.

### Is Cloudflare Workers cheaper than AWS Lambda?

For I/O-bound code, yes, and the gap widens with scale: $45.40 versus $70.00 at 100 million requests of the API-A shape above. For compute-bound code, no: the same comparison at 8 ms walls gives Lambda $2.67 against Workers' $5.80 for ten million requests. The lambda vs cloudflare workers decision is the wall-to-CPU ratio, plus one practical check — whether your Node code actually runs inside a Workers isolate without rewrites.

### How does Vercel bill serverless functions in 2026?

Three meters on Fluid compute: active CPU at $0.128 per hour in the cheapest US regions, provisioned memory at $0.0106 per GB-hour for the entire instance lifetime including I/O waits, and $0.60 per million invocations on Pro. Hobby includes 4 CPU-hours, 360 GB-hours, and 1 million invocations monthly but pauses your site with a 503 if you cross the line — and it stays paused until you act. Pro includes nothing; the $20 monthly usage credit is the only buffer.

### What is the cheapest serverless hosting for a small side project?

Free, in this order: Cloudflare Workers gives the most requests — about three million monthly at 100K/day — if every handler stays under 10 ms of CPU. Lambda's free tier gives the most compute, 400K GB-seconds, for bursty or long-running jobs. Deno Deploy's free plan is the smoothest TypeScript experience with 10 CPU-hours included. The cheapest paid option is Workers at $5 flat, which includes more requests and CPU than any other entry plan here. If those functions need a database behind them, pair the free tiers with our [serverless Postgres comparison](/articles/best-serverless-postgres-hosting-2026-neon-vs-supabase-vs-planetscale-vs-amazon-rds) — Neon's free branch and Supabase's free tier are the current defaults.

### Do Lambda cold starts cost money?

On the current rate card, billed duration starts when code begins executing and includes initialization outside the handler, so a cold start bills like runtime — small money, real latency. AWS's answer is SnapStart: free on supported Java managed runtimes, a caching-and-restore fee on the others, which cuts initialization from seconds to hundreds of milliseconds. Provisioned Concurrency pays a standing per-GB-second charge to keep instances warm — the expensive fix, worth it only when cold starts break user-facing SLAs.

## Bottom Line

Serverless functions pricing in 2026 rewards whoever reads the meter before the homepage. Four verdicts. Default choice: Cloudflare Workers — $5 covers what most solo projects and small products actually serve, duration and egress are free, and the 100K/day free plan means many pay nothing at all. Compute-heavy or runtime-constrained code: AWS Lambda, where full Node and Python run without isolate limits, the always-free tier is the deepest here, and Graviton trims the GB-second rate. Next.js shops: stay on Vercel and let the $20 credit absorb a small API — but watch memory hours, and know that Hobby pauses. Deno Deploy: a clean five-million-request ceiling, beyond which the $2/M request rate quietly funds the other three vendors' marketing. Compute the wall-to-CPU ratio from your own traces first; every dollar after that follows from it."""
}

with open("data/articles_en.json", "r", encoding="utf-8") as f:
    arts = json.load(f)

slugs = [a["slug"] for a in arts]
assert SLUG not in slugs, "slug already exists!"
arts.append(ARTICLE)

with open("data/articles_en.json", "w", encoding="utf-8") as f:
    json.dump(arts, f, ensure_ascii=False, indent=2)

print("appended", SLUG, "| total articles:", len(arts))
