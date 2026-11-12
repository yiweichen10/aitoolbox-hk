# -*- coding: utf-8 -*-
"""Append article #219: Best Managed Kafka Hosting 2026."""
import json, shutil, sys

SRC = r"C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data\articles_en.json"
BAK = r"C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data\articles_en.json.20261112.bak"

shutil.copyfile(SRC, BAK)
print("backup ->", BAK)

content = """The same 1 MB/s streaming pipeline — roughly 2.6 TB in and 7.9 TB out per month — bills about $530 on one managed Kafka service and about $1,243 on another. That is a 2.3x spread for identical work, and almost all of it comes down to how each vendor meters reads, writes, and idle time. Amazon MSK is the worst offender: an idle MSK Serverless cluster accrues $547.50 a month before a single message flows, because the $0.75 cluster-hour fee runs around the clock and the MSK API has no stop action — only delete. This guide compares Confluent Cloud, Amazon MSK, Redpanda Serverless, and Aiven for Apache Kafka on list prices pulled from each vendor's pricing pages in November 2026: unit rates, free tiers, minimum bills, and worked costs for the same pipeline. On managed Kafka hosting, the short version: Confluent's Basic tier keeps small workloads cheapest with a free first eCKU, Redpanda posts the lowest per-GB rates behind a $73 cluster floor, Aiven ships the most usable free tier plus a $35 flat developer plan, and MSK costs the most at every volume below tens of terabytes.

## Managed Kafka Hosting Prices at a Glance

Any Kafka hosting comparison has to start with structure, because these four services price three different things. Confluent and Redpanda sell usage; Aiven sells time; MSK sells brokers or a stack of usage meters. One provider also left the market: Upstash deprecated its Kafka product in 2026, its pricing page now returns a 404, and independent reviews list the product as deprecated — a reminder that cheap serverless entry tiers carry vendor risk.

| Vendor | Entry tier | Production model | Free tier |
| --- | --- | --- | --- |
| Confluent Cloud | Basic: first eCKU free, then $0.14/eCKU-hr | Serverless eCKUs + $0.05/GB data + $0.08/GB-mo storage | Free first eCKU; data and storage still billed |
| Amazon MSK | Provisioned kafka.m7g.large $0.204/broker-hr | Broker-hours, or Serverless meters ($0.75/cluster-hr + $0.10/GB in + $0.05/GB out) | None |
| Redpanda Serverless | $0.10/cluster-hr + per-GB usage | Usage meters: $0.045/GB written, $0.04/GB read, $0.09/GB-mo storage | $100 credits for 30 days, no card |
| Aiven for Apache Kafka | Free: 250 KiB/s, 5 topics, 3-day retention | Consumption hourly rates, or classic plans from $290/mo | Yes — full service, not a sandbox |

The 2026 packaging shift is worth noting: Confluent rebuilt its cluster tiers around Elastic Confluent Units with Basic as the free-start tier, and Aiven rebuilt its Kafka ladder around a real free tier and consumption billing. Both moves target the same audience MSK Serverless pricing quietly punishes — small and bursty pipelines.

## Confluent Cloud Pricing: The eCKU Model, Explained

Confluent Cloud pricing now runs on Elastic Confluent Units (eCKUs) that autoscale with demand and scale to zero when nothing is in use. The Basic tier includes the first eCKU free and bills additional compute at $0.14/eCKU-hour, with data in/out at $0.05/GB and storage at $0.08/GB-month. Limits: 1,500 partitions, 5 TB of storage, a 99.5% SLA, and public endpoints only. The catch is that the free compute allowance does not waive the data or storage meters: a month with 100 GB in and 200 GB out still costs $15 at the data rate alone, plus storage.

Standard, estimated at roughly $385/month at 70% utilization, moves compute to $0.75/eCKU-hour, drops data to $0.035–$0.050/GB, adds infinite storage, 2,500 partitions, and a 99.9% SLA that becomes 99.99% at two or more eCKUs. Enterprise (from ~$895/month) requires private networking, lifts partitions to 96,000, and prices data at $0.020–$0.050/GB. Freight is the specialty tier for logging and observability: $2.25/eCKU-hour with a two-eCKU minimum (estimated ~$2,300/month), storage at $0.03/GB-month, data at $0.014–$0.030/GB, and relaxed 1–2 second latency in exchange for the highest throughput ceiling in the lineup.

Volume discounts apply on committed annual deals: the per-GB data rate steps down to $0.014 at 7,500+ TB of monthly throughput. Billing is hourly with partial hours billed as full hours, invoiced monthly in arrears, and new accounts get $400 in signup credits. For a startup running one or two pipelines under ~1 MB/s, Basic is the closest thing to pay-per-message Kafka as a service — the free eCKU absorbs the compute line entirely.

## Amazon MSK Pricing: Brokers, Express Brokers, and the $547 Floor

Amazon MSK pricing has two shapes. Provisioned clusters bill broker-hours: kafka.m7g.large runs $0.204/hour (~$149/month per broker, with AWS recommending about 1,000 partitions per broker), m5.large runs $0.21/hour, and Standard brokers charge no per-GB fee for data in or out. Storage bills $0.10/GB-month on broker disks — with the default replication factor of three, that means three copies of every retained byte on your invoice — and tiered storage extends retention at $0.06/GB-month plus $0.0015/GB retrieval. Three m7g.large brokers cost about $447/month before storage. Express brokers cost exactly double ($0.408/hour for m7g.large) plus $0.01/GB ingested, and pay off only if their claimed 3x throughput lets you buy half as many.

MSK Serverless stacks five meters: $0.75/cluster-hour, $0.0015/partition-hour, $0.10/GB written, $0.05/GB read, and $0.10/GB-month stored. AWS's own pricing-page example — 100 partitions, 100 GB/day written, 200 GB/day read — totals $1,299.60 for a month, of which $547.50 is cluster hours. That cluster-hour fee accrues while the cluster exists, idle or not: a forgotten development cluster costs $547.50/month forever, and there is no stop button. The floor shapes every recommendation: MSK Serverless makes sense for spiky workloads whose average bill clears the $548 base comfortably, and provisioned Standard brokers beat it for steady 24/7 throughput because ingress and egress are unmetered.

Add-ons move real money at scale: MSK Connect bills $0.11/MCU-hour (one MCU is 1 vCPU plus 4 GB), the Replicator bills $0.30/hour plus $0.08/GB, and multi-VPC private connectivity adds $0.0225/hour plus $0.006/GB. Traffic in and out of the cluster follows standard AWS data-transfer rates.

## Redpanda Serverless Pricing: Lowest Per-GB Rates, With a $73 Floor

Redpanda Serverless pricing is the most aggressive per-GB in the group, published on the vendor's own price estimator: $0.10/cluster-hour, $0.0015/partition-hour, $0.045/GB written, $0.04/GB read, and $0.09/GB-month of retention. The estimator's default scenario — 0.1 MB/s average write, roughly 0.2 MB/s read, 7-day retention, 30 partitions — totals $144.14/month, of which $73.00 is cluster hours and $32.85 is partition hours. Read that as a de facto floor: before meaningful data moves, a Serverless cluster already carries about $106/month of time-and-partition charges.

The trial terms are strict. New accounts get $100 in credits for 30 days with no card; when credits or days run out, clusters suspend and data becomes inaccessible, with a seven-day grace period before deletion. Ceiling specs: 100 MB/s write and 300 MB/s read, 5,000 partitions, 99.9% SLA, multi-tenant AWS and GCP (beta) regions. The Kafka API itself is real — Redpanda is a C++ reimplementation that speaks the protocol, so standard clients, transactions, and ACLs work unchanged — but the Serverless tier omits RBAC, multi-AZ, Kafka Connect, and configurable maintenance windows, all of which require Dedicated or BYOC tiers sold on annual commitments. Against Confluent Basic, Redpanda charges less per GB in both directions ($0.045/$0.04 versus $0.05/$0.05); which service wins a bill comes down to whether the free eCKU or the $73 floor absorbs more of your idle time.

## Aiven Kafka Pricing: A Real Free Tier, $35 Developer, Consumption Professional

Aiven for Apache Kafka rebuilt its ladder in 2026. The Free tier runs $0 with up to 250 KiB/s throughput, 3-day retention, five topics of two partitions each, and Schema Registry plus REST proxy included — and it is the production service, not a sandbox. Developer costs $35/month flat ($0.04/hour) for up to 1 MB/s, 20 topics capped at 100 partitions, and a 99% SLA; for prototyping and staging it undercuts everything in this comparison until traffic approaches 1 MB/s.

Aiven Kafka pricing for production runs through the diskless Professional plan, billed hourly by workload size with a 99.99% SLA. Aiven's own table: 0.1 MB/s ingress, ~25 GB storage, ~1 TB network estimates $0.38/hour ≈ $276/month; 1 MB/s, ~253 GB, ~10 TB estimates $0.85/hour ≈ $622/month; 3 MB/s ≈ $1.91/hour ≈ $1,391/month; 10 MB/s ≈ $5.79/hour ≈ $4,226/month. Treat those as the vendor's ballparks, not quotes — the storage and network assumptions are Aiven's. Classic fixed plans persist alongside: Startup from $290/month ($0.40/hour, three dedicated VMs, 90 GB cluster storage), Business from $725/month, Premium from $2,800/month. Networking is metered on consumption plans and included under fair-use on classic ones.

## The Same Pipeline, Four Bills

Here is the managed Kafka hosting race with actual arithmetic. Assumptions: 1 MB/s average ingress (2,628 GB/month), 3 MB/s average reads from three consumer groups (7,884 GB/month), 7-day retention (about 60.5 GB held), 30 partitions, a 730-hour month. Confluent's bill assumes the cluster autoscales within the one free eCKU.

| Service | Monthly bill | Biggest line item | The catch |
| --- | --- | --- | --- |
| Confluent Cloud Basic | ~$530 | Data in/out: 10,512 GB × $0.05 = $525.60 | Free compute only covers one eCKU; data and storage always bill |
| Redpanda Serverless | ~$545 | Reads: 7,884 GB × $0.04 = $315.36 | $73 cluster + $33 partition charges accrue before much data moves |
| Aiven Professional | ~$622 | Vendor estimate at 1 MB/s ingress | Ballpark, not itemized; assumes Aiven's retention and network profile |
| Amazon MSK Serverless | ~$1,243 | Cluster hours: $547.50 | Idle costs $547.50; reads cost 2x Confluent per GB, writes 2x Redpanda |

The order flips with workload shape. At a 1:1 read-to-write ratio, Redpanda pulls ahead of Confluent because its read rate undercuts the flat $0.05. Heavy fan-out hurts every service equally per GB — except MSK, where reads already cost double. Tiny volumes favor Confluent Basic or the Aiven Developer plan, which have no meaningful floor. And for steady, read-heavy 24/7 pipelines, provisioned MSK Standard re-enters the race: three m7g.large brokers at $447/month carry unmetered ingress and egress, which beats every serverless bill once monthly data volume passes roughly 9–10 TB combined. Like-for-like comparisons also need a replication asterisk: Confluent, Redpanda Serverless, and Aiven price storage pre-replication, while provisioned MSK bills every replica on disk.

## Hidden Costs: Reads, Partitions, Retention, Networking

Managed Kafka cost per GB is the headline, but three quieter meters do the damage in production:

- **Consumer groups are a billing decision.** Egress is billed per GB out at $0.05 (Confluent) or $0.05 (MSK Serverless). Serving the same stream to five consumers multiplies the data bill by five; one compactor topic feeding a downstream store can cut it. Design consumption before you price it.
- **Partition-hours punish over-provisioning.** $0.0015/partition-hour sounds trivial until 1,000 partitions of headroom bill $1,095/month on both MSK Serverless and Redpanda — more than the entire Confluent data line at 1 MB/s. Size partitions for today and repartition later.
- **Retention multiplies through replication.** Seven days at 1 MB/s holds 60.5 GB pre-replication; on provisioned MSK with RF=3 that is 181.5 GB of billed disk, and 30-day retention turns it into $54/month of storage on a $447 broker bill. Serverless services price pre-replication, which quietly flatters their storage lines against MSK's.
- **Networking and add-ons sit outside the headline rates.** MSK traffic follows standard AWS transfer rates and PrivateLink bills separately; Redpanda's PrivateLink "incurs additional charges"; Aiven meters network on consumption plans; Confluent Basic is public-endpoint-only. Marketplace credits soften year one — $300 for Redpanda via AWS Marketplace, $400 from Confluent at signup.

## Frequently Asked Questions

### What is the cheapest way to run Kafka as a service in 2026?

For near-zero volume, Aiven's Free tier (250 KiB/s, five topics) and Confluent Basic (free first eCKU; a 10 GB/month feed bills under $1 of data) both run indefinitely at nothing. For a small but steady pipeline, Aiven Developer at $35/month flat is the cheapest managed Kafka until sustained traffic approaches 1 MB/s. Past that, Confluent Basic and Redpanda Serverless finish within about $15 of each other at the reference workload, and the winner depends on your read ratio.

### Why is MSK Serverless so expensive at low volume?

Three stacked meters: the $0.75/cluster-hour base runs 24/7 regardless of traffic ($547.50/month before a message), reads bill at $0.05/GB — double Confluent's flat rate and 25% above Redpanda — and partition-hours add $0.0015 per partition per hour. MSK Serverless only wins when traffic is genuinely spiky and the average bill clears the $548 base, or when avoiding broker sizing matters more than cost.

### Is Redpanda Serverless compatible with real Apache Kafka?

The Kafka API, yes: standard clients, transactions, offsets, and ACLs work against Redpanda's C++ implementation without code changes. What the Serverless tier lacks is ecosystem surface — RBAC, multi-AZ resilience, Kafka Connect, and configurable maintenance windows live in the Dedicated and BYOC tiers, which require annual commitments. Pipeline code portability is high; enterprise control-plane portability is not.

### What happened to Upstash Kafka?

Upstash deprecated it. The Kafka pricing page returns a 404 as of November 2026, and independent reviews list the product as deprecated and advise against new pipelines. Existing tenants face migration work, but Kafka workloads move cleanly: no service in this comparison locks clients to proprietary APIs, so the producer and consumer code ports as-is to Confluent, MSK, Redpanda, or Aiven.

### Confluent vs MSK: which one should a startup pick?

Confluent, for most startups under a few terabytes a month: the free eCKU, flat $0.05 data rate, managed connectors, Flink, and Schema Registry beat MSK Serverless on both floor and per-GB rates, and the same organization sells the governance tooling a data team eventually needs. MSK earns its keep when the workload is steady and heavy — Standard brokers leave ingress and egress unmetered, which beats every usage-priced rival above roughly 9–10 TB of combined monthly data — or when AWS Marketplace spend and single-vendor networking dominate the decision.

---

**Bottom line:** managed Kafka hosting in 2026 is priced by meter, and the meter decides the winner. Confluent Basic is the default pick for small and bursty pipelines because the free first eCKU erases idle costs that MSK Serverless bills at $547.50 a month; Redpanda wins the per-GB race and suits teams that will outgrow a single pipeline's data volume; Aiven offers the friendliest entry ramp and a 99.99% SLA consumption tier without per-GB surprises; provisioned MSK Standard is the steady-state heavyweight with unmetered data. Audit your read ratio and partition count before committing — they move the bill more than the vendor logo does. And if the workload behind the pipeline is a database, the same metered-vs-floor logic applies to storage: the [serverless Postgres comparison](/articles/best-serverless-postgres-hosting-2026-neon-vs-supabase-vs-planetscale-vs-amazon-rds) and the [managed Redis comparison](/articles/best-managed-redis-hosting-2026-upstash-vs-redis-cloud-vs-dragonfly-vs-elasticache) apply it to Postgres and Redis, while the [managed Kubernetes comparison](/articles/best-managed-kubernetes-2026-eks-vs-gke-vs-aks-vs-doks-pricing-compared) covers the control plane your brokers may eventually run beside."""

article = {
    "title": "Best Managed Kafka Hosting in 2026: Confluent vs Amazon MSK vs Redpanda vs Aiven Pricing Compared",
    "slug": "best-managed-kafka-hosting-2026-confluent-vs-msk-vs-redpanda-vs-aiven-pricing-compared",
    "date": "2026-11-12",
    "dateFull": "November 12, 2026",
    "category": "AI Infrastructure",
    "description": "Confluent vs MSK vs Redpanda vs Aiven at November 2026 list prices: the $547.50 idle MSK Serverless floor, Confluent's free eCKU, Redpanda's $73 floor, and worked bills for one pipeline.",
    "keywords": [
        "managed Kafka hosting",
        "Confluent Cloud pricing",
        "Amazon MSK pricing",
        "MSK Serverless pricing",
        "Redpanda Serverless pricing",
        "Aiven Kafka pricing",
        "Confluent vs MSK",
        "Kafka as a service",
        "cheapest managed Kafka",
        "Kafka hosting comparison",
        "managed Kafka cost per GB",
        "Upstash Kafka deprecated"
    ],
    "content": content,
}

with open(SRC, encoding="utf-8") as f:
    arts = json.load(f)

slugs = [a["slug"] for a in arts]
if article["slug"] in slugs:
    print("ERROR: slug already exists:", article["slug"])
    sys.exit(1)

arts.append(article)
with open(SRC, "w", encoding="utf-8") as f:
    json.dump(arts, f, ensure_ascii=False, indent=2)

print("appended article:", article["slug"], "| total articles:", len(arts))
