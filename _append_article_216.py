# -*- coding: utf-8 -*-
"""Append Article #216: Best Managed Redis Hosting 2026. Self-checks run BEFORE writing."""
import json, re, os, sys

ART = "data/articles_en.json"
SLUG = "best-managed-redis-hosting-2026-upstash-vs-redis-cloud-vs-dragonfly-vs-elasticache"

TITLE = "Best Managed Redis Hosting in 2026: Upstash vs Redis Cloud vs Dragonfly vs ElastiCache"
DESC = ("Upstash vs Redis Cloud vs Dragonfly Cloud vs ElastiCache on November 2026 pricing: "
        "per-command billing, the $91 idle floor, HA memory doubling, and four worked workloads.")
KEYWORDS = ["managed Redis hosting", "Upstash vs Redis Cloud", "Redis Cloud pricing", "Upstash pricing",
            "ElastiCache pricing", "Dragonfly vs Redis", "serverless Redis", "cheapest managed Redis",
            "ElastiCache vs Redis Cloud", "Valkey vs Redis"]

CONTENT = """An idle 1 GB cache costs $0 on Upstash, about $18 on Redis Cloud Essentials, and $91.25 on ElastiCache Serverless for Redis OSS — the same data, on the same wire protocol, doing absolutely nothing. That spread is the most important fact in managed Redis hosting right now, because the four viable providers stopped selling the same product. Upstash sells commands. Redis Cloud sells provisioned memory. Dragonfly sells RAM with an SSD escape hatch. AWS sells node-hours plus a metered serverless mode it introduced in late 2024.

The market fractured before the prices did. In March 2024, Redis Ltd. moved its core database under the RSALv2 and SSPL licenses; a Linux Foundation fork named Valkey appeared within days, and AWS, Google Cloud, DigitalOcean, and Aiven all standardized on it. Redis answered a year later by returning the core to open source under AGPLv3 with Redis 8 — but the fork economics stuck. On AWS in November 2026, Valkey nodes run about 20% cheaper than equivalent Redis OSS nodes, and Valkey Serverless undercuts Redis OSS by roughly 33% on storage and processing units. Engine choice moves your bill by a third before you compare vendors at all.

This guide prices the four realistic options — Upstash, Redis Cloud, Dragonfly Cloud, and Amazon ElastiCache — on November 2026 public rates, then runs four real workloads through each bill. The winner changes per workload, and the crossover points are sharper than most vendor pages admit. Caches rarely sit alone: if yours backs a Postgres database, the [serverless Postgres hosting comparison](/articles/best-serverless-postgres-hosting-2026-neon-vs-supabase-vs-planetscale-vs-amazon-rds) covers the other half of that stack.

## Four Billing Models, One Protocol

Every provider here speaks the RESP protocol, so switching is a client-library change, not a rewrite. What differs is what the meter counts.

Upstash pricing has three shapes. The free tier covers 256 MB and 500K commands a month. Pay-as-you-go bills $0.20 per 100K commands plus $0.25 per GB-month of storage after the first free gigabyte, bandwidth free to 200 GB/month then $0.03/GB — and an idle database costs $0. Fixed plans replace the command meter with flat monthly pricing and a throughput cap. A REST API is why serverless Redis works from Cloudflare Workers and Vercel functions that cannot hold a TCP connection; Supabase routes Edge Functions caching through it and Zapier runs global rate limiting on it, per write-ups hosted on Upstash's own site.

Redis Cloud bills provisioned memory and never meters requests. The free tier is one 30 MB database at 100 operations per second. Essentials starts at $0.007/hour — about $5/month for 250 MB — and Pro bills hourly with a $200/month minimum for dedicated infrastructure, multiple databases per subscription, and a 99.999% uptime SLA. It is also the only place you get the first-party Redis 8 module stack: Search, JSON, TimeSeries, and Bloom, maintained by Redis itself.

Dragonfly Cloud sells RAM on flat plans: Flex starts at $36/month on AWS, GCP, or Azure — roughly $11 per GB-month at scale — and Business plans from $2,000/month add bring-your-own-cloud, SSO, and custom SLAs. The hook is SSD tiering: pay 1.5 times the RAM rate and get eight times the capacity, hot values in memory and cold values on local NVMe.

ElastiCache prices two ways: classic node-hours from $0.0128/hour (cache.t4g.micro on Valkey, about $9.34/month), or Serverless at $0.084 per GB-hour plus $0.0023 per million ECPUs on Valkey. There is no scale-to-zero — billing starts when the cache becomes Available and stops only when you delete it. ElastiCache and most cloud platforms now default to Valkey, protocol-compatible with Redis clients; Dragonfly is a separate multi-threaded engine that also speaks the Redis, Valkey, and Memcached APIs. Only Redis Cloud runs the first-party module set, so if a workload depends on TimeSeries or Bloom, capability beats price.

## Managed Redis Hosting Pricing, Side by Side

| Platform | Engine | Billing model | Entry paid price | Free tier | High availability |
|---|---|---|---|---|---|
| Upstash | Redis-compatible protocol | Per command, or fixed plans | $0 PAYG; $10/mo (250 MB) | 256 MB + 500K commands/mo | Prod Pack: +$200/mo per database |
| Redis Cloud | Redis 8 (first-party) | Per provisioned GB | ~$5/mo (250 MB) | 30 MB at 100 ops/sec | HA doubles billed memory; Active-Active doubles it again |
| Dragonfly Cloud | Dragonfly (Redis/Valkey/Memcached APIs) | Flat plans, per GB RAM | $36/mo (Flex) | Trial only; self-hosted CE is free | Included on Flex and up |
| ElastiCache | Valkey / Redis OSS / Memcached | Node-hour, or serverless GB-hr + ECPU | ~$9.34/mo (t4g.micro) | $100 credits (new accounts) | Second node at full cost |

Upstash fixed plans run $10 (250 MB), $20 (1 GB), $100 (5 GB), $200 (10 GB), $400 (50 GB), $800 (100 GB), and $1,500 (500 GB), each with unlimited commands under a throughput cap — 10,000 commands/second through the 10 GB plan, 16,000 on the top two. The Prod Pack adds an uptime SLA and multi-zone redundancy for a flat $200/month per database, and a read replica in another region costs roughly half the base plan.

Redis Cloud Essentials steps from $5 (250 MB) through about $18 (1 GB, per Redis's own calculator) on shared infrastructure, and Redis's calculator quoted a 10 GB high-availability production cache at $549/month on Pro. The multiplier to watch is availability: replication doubles billed memory, and Active-Active in a second region doubles it again — a 10 GB dataset can bill as 40 GB. ElastiCache vs Redis Cloud is mostly the availability-multiplier question plus AWS integration: Redis Cloud folds failover into that doubled memory line, while ElastiCache charges for a second full node.

Dragonfly prices RAM at $11/GB-month on Flex, with the tiered option at $16.50/GB-month for eight times the capacity. ElastiCache node rates in us-east-1: cache.t4g.micro $0.0128/hour (~$9.34/month), cache.t4g.medium $0.052/hour (~$38/month), cache.r7g.large $0.1752/hour on Valkey versus $0.219 on Redis OSS (~$128 versus ~$160/month), and cache.r7g.xlarge $0.3496/hour (~$255/month). High availability means a second node — every node price doubles. Cross-AZ traffic between your app and the cache costs $0.01/GB each way, a line item that doesn't exist on the other three unless you replicate across regions. Reserved nodes cut up to 55%, and Database Savings Plans trim Serverless up to 30% on a one-year commitment.

## Four Workloads, Three Different Winners

The arithmetic of managed Redis hosting never resolves into a single winner; it resolves per workload. Four worked examples at us-east-1 rates, November 2026:

| Workload | Upstash | Redis Cloud | Dragonfly Cloud | ElastiCache (Valkey) |
|---|---|---|---|---|
| Hobby rate limiter: 400K commands/mo, 50 MB | $0 (free tier) | $5 (250 MB Essentials) | $36 (Flex) | ~$6 (serverless floor) |
| Steady small app: 12M commands/mo, 1 GB | $20 (fixed 1 GB) | $18 (Essentials) | $36 (Flex) | ~$61 (serverless) |
| Production cache: 8 GB at 2,500 req/s | $200 (fixed 10 GB) | ~$150–$300 (HA doubles) | $88 (8 × $11) | ~$505 (serverless) |
| Memory-bound: 400 GB, 50 GB hot | $1,500 (fixed 500 GB) | Custom quote (Pro) | $825 (tiered) | ~$24,500 (serverless) |

The hobby workload is the cleanest win. Four hundred thousand commands a month is roughly 16K/day, inside Upstash's free ceiling, so the bill is $0. Redis Cloud's free tier caps at 30 MB, so the same app pays $5. ElastiCache Serverless for Valkey meters a 100 MB storage minimum — about $6.13/month — while the Redis OSS engine's 1 GB minimum makes the identical idle dev cache $91.25. Pick Valkey, not Redis OSS, on AWS dev environments, or run Dragonfly's free Community Edition on a $5 VPS for zero managed cost.

The steady small app flips it. Twelve million commands a month on Upstash pay-as-you-go computes to $24 (120 × $0.20), so the $20 fixed plan wins on the same vendor — but Redis Cloud Essentials at 1 GB is $18 flat, Dragonfly's Flex floor is $36, and ElastiCache Serverless Valkey lands near $61 ($61.32 of storage plus about $0.03 of ECPUs). Memory-priced plans beat command-priced plans when the GB is always on and command volume is modest.

The production cache is where models collide. An 8 GB working set at a steady 2,500 req/s: Upstash's 10 GB fixed plan is $200 flat; Redis Cloud's 8 GB Essentials interpolates to roughly $150 and doubles to about $300 with replication; Dragonfly is $88 (8 × $11); ElastiCache Serverless Valkey is the expensive one at roughly $505 — $490 of storage plus $15 of ECPUs. A t4g.medium node pair at ~$76 is cheaper if you accept manual failover configuration, and that single-point-of-failure tradeoff is the real AWS tax at small scale.

The memory-bound case is Dragonfly's pitch, from its own published example: 400 GB with 50 GB hot provisions 50 GB of RAM plus 350 GB of SSD at $16.50/GB-month, or $825/month — versus $4,400 all-RAM, an 81% cut. Upstash's fixed 500 GB plan is $1,500. ElastiCache Serverless is roughly $24,500 at 400 GB, but its r6gd nodes tier to SSD for what AWS claims is over 60% savings at maximum use, so node tiering is the AWS answer here. Redis Cloud quotes this scale custom through Pro.

## Where Each Vendor Breaks

### Upstash: the command meter cuts both ways

The free tier's real ceiling is command count, not storage. A logged-in page view that checks a session, enforces a rate limit, and reads a cached fragment already fires four to six commands — the popular sliding-window rate limiter alone sends three to five per check. Past roughly 5M commands/month, a fixed plan beats pay-as-you-go on Upstash's own math, and the failure mode is a steady chatty app: 100M commands/month is $200 on the meter and $20 on the 1 GB fixed plan — same vendor, ten times apart. Throughput ceilings matter too: fixed plans cap at 10,000 commands/second until you reach the 100 GB tier.

### Redis Cloud pricing: what actually doubles the bill

Three multipliers do the damage. Replication doubles billed memory on Essentials and Pro. Active-Active geo-replication doubles it again, so a two-region 10 GB deployment bills as 40 GB. And the Pro tier's $200/month minimum is a floor, not a starting point — Redis's calculator landed a 10 GB HA build at $549/month. In exchange you get dedicated infrastructure, a 99.999% SLA, and the only first-party implementation of Search, JSON, TimeSeries, and Bloom. ToolRadar's October 2026 read of the pricing page also lists a Flex tier — RAM backed by SSD for 1–100 GB from $5/month — worth checking for cold-heavy datasets if it is live in your region.

### Dragonfly vs Redis: a bet on threads and SSDs

The "25x faster than Redis" claim is Dragonfly's marketing; the verifiable part is architectural — a multi-threaded, shared-nothing engine that holds more data per GB in the vendor's benchmarks, priced at $11/GB-month against Redis Cloud's small-scale effective rates and ElastiCache Serverless's ~$61/GB-month storage math. What you can check without benchmarks: it speaks the Memcached API too, so it is the only vendor here that can absorb a legacy Memcached fleet without a client rewrite. The risk is ecosystem age — fewer years of production scars than the 2009-vintage original. If the cold tail of your dataset belongs on cheap object storage instead, the [object storage pricing comparison](/articles/best-object-storage-pricing-2026-aws-s3-vs-cloudflare-r2-vs-backblaze-b2-vs-wasabi) prices that layer separately.

### ElastiCache pricing: floors, reservations, and the Valkey decision

AWS-native means VPC-only networking — there is no public endpoint, so ElastiCache cannot serve an edge application — plus IAM and a per-region operations burden. The Valkey vs Redis OSS decision mostly answers itself: protocol-identical clients, 20% cheaper nodes, 33% cheaper Serverless. Reserved nodes (up to 55% off) fit steady throughput, and the one-year Database Savings Plan (up to 30%) is the only Serverless discount. The structural trap is the floor: an idle Redis OSS Serverless cache bills $91.25/month before serving a single request, and no ElastiCache configuration scales to zero — you delete the cache to stop the meter.

## Frequently Asked Questions

### Is Upstash cheaper than Redis Cloud?

Below roughly 12M commands/month, yes — a bursty 400K-command app is free on Upstash and $5 on Redis Cloud, and an idle one is $0 versus $5. The Upstash vs Redis Cloud crossover lands near 12M commands/month on a small always-on dataset: Redis Cloud Essentials takes over at $18 for 1 GB against $24 metered (or $20 fixed) on Upstash. At heavy steady throughput the comparison shifts to ceilings per dollar — Upstash's fixed 1 GB plan allows 10,000 commands/second while Redis Cloud's $18 1 GB Essentials tier allows about 2,000 ops/second.

### How much does Amazon ElastiCache cost per month?

The floors first: Serverless Valkey idles at about $6.13/month (100 MB minimum), Serverless Redis OSS at $91.25 (1 GB minimum), and the cheapest node is $9.34/month (cache.t4g.micro, Valkey). A production t4g.medium with a replica runs about $76/month. An 8 GB steady cache on Serverless Valkey computes to roughly $505/month. New AWS accounts get $100 in credits, reserved nodes cut up to 55%, and Database Savings Plans trim Serverless up to 30%.

### Which is the cheapest managed Redis service?

By entry price: Upstash ($0 pay-as-you-go with no floor), then Redis Cloud ($5), ElastiCache Serverless Valkey (~$6 idle floor), and Dragonfly Cloud ($36). By free-tier generosity, Upstash wins outright — 500K commands plus 256 MB versus Redis Cloud's 30 MB. By cost per GB at scale, Dragonfly's $11 RAM rate and $16.50 tiered rate undercut everyone's memory pricing.

### Is Dragonfly a real drop-in Redis replacement?

At the protocol level, yes — it speaks the Redis, Valkey, and Memcached APIs, so client libraries don't change. What deserves testing before migration: your exact command surface, plus any dependency on Redis's first-party modules. Dragonfly covers search, JSON, and vectors, but TimeSeries and Bloom equivalents are gaps to verify with your own workload, not a vendor checklist.

### What's the deal with Valkey — is it just cheap Redis?

It is the same wire protocol under different governance — the reason Redis alternatives like Valkey and Dragonfly exist at all. Valkey forked from Redis 7.x days after the March 2024 license change and lives under the Linux Foundation, with AWS and Google Cloud running it in production. Redis 8 returned to open source under AGPLv3 in May 2025 and added features Valkey has not matched yet, including vector sets. On AWS the price delta is 20–33% in Valkey's favor, so the practical question is whether you need Redis-specific features — not whether Valkey clients work, because they do.

## The Bottom Line

Managed Redis hosting in 2026 is a billing-model decision before it is a vendor decision. Spiky, low-volume, or edge-deployed traffic belongs on Upstash, because $0 idle and HTTP access match serverless economics — just move to a fixed plan past 5M commands/month. Steady mid-size caches that need first-party Search, JSON, TimeSeries, or Bloom belong on Redis Cloud, budgeting for replication to double the memory line. Very large, mostly-cold datasets belong on Dragonfly's tiered memory ($825 versus $4,400 on a 400 GB set) or ElastiCache r6gd nodes if you are AWS-committed. High sustained throughput inside a VPC belongs on ElastiCache for Valkey with reserved nodes — and never on Redis OSS Serverless unless you enjoy a $91 monthly floor on an empty cache.

Your app platform decision interacts with all of this: Railway, Render, and Fly.io price bandwidth and add-ons differently, and the [PaaS pricing comparison](/articles/heroku-alternatives-2026-railway-vs-render-vs-flyio-pricing-compared) covers where self-deployed Redis fits that picture. Price the cache model first, then the stack around it."""

# ---------------- Self-checks ----------------
errors, warnings = [], []
low = CONTENT.lower()

wc = len(CONTENT.split())
if not (2200 <= wc <= 2800):
    errors.append(f"word count {wc} outside 2200-2800")

pk = low.count("managed redis hosting")
if pk != 4:
    errors.append(f"PK 'managed redis hosting' count = {pk}, expected 4")

BANNED = ["leverage", "utilize", "seamlessly", "game-changing", "empower", "streamline",
          "delve", "transformative", "comprehensive", "revolutionize", "cutting-edge",
          "as an ai", "in conclusion"]
for b in BANNED:
    if b in low:
        errors.append(f"banned word present: {b}")

LONGTAILS = ["upstash vs redis cloud", "redis cloud pricing", "upstash pricing",
             "elasticache pricing", "dragonfly vs redis", "serverless redis",
             "cheapest managed redis", "elasticache vs redis cloud", "valkey vs redis",
             "redis alternatives"]
missing = [t for t in LONGTAILS if t not in low]
if missing:
    errors.append(f"missing long-tails: {missing}")

h3 = len(re.findall(r"^### ", CONTENT, re.M))
if h3 < 3:
    errors.append(f"FAQ H3 count = {h3}, need >=3")

tables = re.findall(r"((?:^\|.+\|\s*$\n?)+)", CONTENT, re.M)
table_reports = []
for i, t in enumerate(tables):
    rows = [r for r in t.strip().split("\n") if r.strip()]
    cols = rows[0].count("|") - 1
    table_reports.append(f"table{i+1}: {len(rows)} rows x {cols} cols")
    if len(rows) < 5 or cols < 4:
        errors.append(f"table{i+1} too small: {len(rows)}x{cols}")

links = re.findall(r"\]\((/articles/[^)]+)\)", CONTENT)
if len(links) < 2:
    errors.append(f"internal links = {len(links)}, need >=2")

data = json.load(open(ART, encoding="utf-8"))
slugs = {a["slug"] for a in data}
if SLUG in slugs:
    errors.append("slug already exists")
for L in links:
    if L.replace("/articles/", "") not in slugs:
        errors.append(f"link target missing: {L}")

print(f"word count: {wc}")
print(f"PK count: {pk}")
print(f"H3 count: {h3}")
for r in table_reports:
    print(r)
print(f"internal links: {len(links)} -> {links}")

if errors:
    print("\nFAIL:")
    for e in errors:
        print(" -", e)
    sys.exit(1)

# ---------------- Write ----------------
bak = ART + ".20261109.bak"
if not os.path.exists(bak):
    import shutil
    shutil.copy2(ART, bak)
    print("backup ->", bak)

entry = {"title": TITLE, "slug": SLUG, "date": "2026-11-09", "dateFull": "November 9, 2026",
         "category": "AI Infrastructure", "description": DESC, "keywords": KEYWORDS, "content": CONTENT}
data.append(entry)
with open(ART, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("appended. total articles:", len(data))
