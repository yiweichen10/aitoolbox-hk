Heroku ran the developer cloud everyone else spent a decade copying — Salesforce bought it for $212 million in 2010 — and its survey footprint keeps shrinking: Stack Overflow's 2026 survey put Heroku at 3.6% of the 10,889 developers who answered its cloud-platform question, down from 5.4% the year before, while Railway, its most-shopped successor, sits below the 1% threshold needed to print a row at all. (Sample bases shift between survey years; treat the trend as directional.) The catalyst is concrete, though: in February 2026, Salesforce confirmed Heroku was moving to "sustaining engineering" — bug fixes and security patches only — and stopped selling new Enterprise contracts, the contract type that gates the Kubernetes-native Fir generation behind a roughly $1,000-a-month Private Space floor. The hunt for Heroku alternatives is now routine procurement rather than a Hacker News pastime, and the three platforms that absorb most defectors — Railway, Render, and Fly.io — bill in three incompatible ways. This article prices all four the way an operator would: the same workloads, the same arithmetic, list prices pulled from each vendor's own pages in November 2026.

## Why developers hunt for Heroku alternatives in 2026

Three things changed in the last eighteen months.

First, the platform itself. Fir — the rebuilt, Kubernetes-backed generation — has been locked to Fir Private Spaces since it went generally available in April 2025, and Heroku's own documentation still lists the Common Runtime, where every cheap dyno actually runs, as "to be added" with no committed date. The price of admission is a Standard Space at about $1.39 an hour, capping near $1,000 a month before a single dyno boots.

Second, the compute ladder. Heroku's entry compute is a Standard-1X dyno at $25 a month: 512 MB of RAM, a shared CPU slice that bursts between 1x and 4x. That is roughly $50 per gigabyte of RAM per month. The same $25 on Render buys a dedicated 1 vCPU and 2 GB of RAM; on Fly.io it covers about three months of a 1 GB shared-CPU machine.

Third, the database economics. Heroku Postgres Essential plans — $5, $9, and $20 a month — cap connections at 20 or 40, ship with no rollback, no fork/follow, and tolerate up to four hours of downtime a month with unannounced maintenance. The first production-grade jump, the new Advanced tier, starts at $150 a month. Comparable managed Postgres on Render starts at $19.

None of this makes Heroku useless — unbilled egress, Salesforce integration, and a genuine Shield compliance tier remain real edges. But the market has repriced the question, and the rest of this article is the arithmetic.

## The metering models don't compare directly

Every platform here sells roughly the same thing — a container, a URL, a deploy pipeline — but the invoices are built in different units, and that is where cost surprises live.

**Railway** bills usage by the second and charges only for active CPU and memory: about $20.29 per vCPU-month for an always-on service, $10.14 per GB-month of memory, $0.05 per GB of egress. The Hobby plan carries a $5 monthly minimum that doubles as a $5 usage credit; Pro carries a $20 minimum and adds unlimited seats.

**Render** bills fixed instance rates plus a workspace fee: $0 Hobby (25 services), $25 Pro (autoscaling, unlimited seats, 25 GB of bandwidth). Instances have fixed prices regardless of how idle they sit.

**Fly.io** bills per-second machines with no platform fee and no free tier ($1 trial credit, 7 days). Machines cost the same whether traffic arrives or not; stopped machines still bill their disk.

**Heroku** bills flat per-dyno rates with add-ons priced à la carte.

A "$7 instance," a "$5 minimum," and a "$2.19 machine" are not comparable numbers. The worked-cost section below makes them comparable by holding the workload constant.

## Railway pricing: usage-based compute with a $5 floor

Railway's Free plan is the odd one out: after a 30-day trial with $5 of credits, it costs $1 a month — a free plan with an invoice, keeping 1 vCPU and 512 MB per service for experiments.

The Hobby plan's $5 minimum covers most side projects entirely — a 512 MB service running part-time bills well under it. Pro's $20 minimum is the real production entry point: unlimited seats, a 99.99% availability target, 30-day log retention, and services up to 1,000 vCPU and 1 TB of RAM.

The usage math is straightforward. An always-on 1 vCPU / 2 GB service accrues about $41 a month before egress ($20.29 of CPU, $20.28 of memory). A database deployed as a service — Railway lets you deploy any open-source database with one click — bills at the same rates, so a 1 vCPU / 1 GB Postgres box lands near $30 plus volume storage at $0.16 per GB-month.

Railway's strengths are transparency and seats: watch the CPU graph, set spend limits, add teammates without per-seat invoices; preview environments come standard. Its weak points: $0.05 per GB bandwidth (2.5 times Fly.io's rate) and no true scale-to-zero — a deployed service bills unless you delete it or zero its replicas.

## Render pricing: fixed instances plus a $25 workspace fee

Render's web instance ladder runs $7 (0.5 CPU, 512 MB) → $25 (1 CPU, 2 GB) → $85 (2/4) → $135 (2/8) → $175 (4/8) → $225 (4/16) → $450 (8/32) → $1,500 (12 CPU, 96 GB). Paid instances never sleep. That $25 instance is the quiet headline of this comparison: the same price as Heroku's Standard-1X, with four times the RAM and a dedicated CPU.

Render Postgres starts at $19 (0.5 CPU, 1 GB, 100 connections), scales to $100 for 2 CPU / 8 GB, and bills expandable storage at $0.30 per GB. Point-in-time recovery covers 3 days on the Hobby workspace and 7 on paid plans.

Two line items bite: bandwidth and the workspace fee. Hobby includes 5 GB of egress; beyond that, Render charges $0.15 per GB — the most expensive rate in this comparison. Pro's $25 fee is per workspace, and SAML SSO, HIPAA-eligible workspaces, and 1 TB of bandwidth live on the $499 Scale plan.

For teams that want a fixed, predictable bill with managed Postgres in the same console, Render pricing is the most legible of the three. Model your egress before committing.

## Fly.io pricing: the cheapest always-on machines

Fly.io runs your container in a Firecracker microVM across 30-plus regions, and its shared-CPU ladder is the cheapest always-on compute here: $2.19 a month for 256 MB, $3.69 for 512 MB, $6.70 for 1 GB, $12.70 for 2 GB. Dedicated vCPUs start at performance-1x — $33 a month for 1 vCPU and 2 GB — with extra RAM at $6 per GB-month.

Bandwidth is Fly's other edge: $0.02 per GB in North America and Europe, $0.04 in Asia-Pacific, inbound free. Fly's own worked examples put a 24/7 Discord bot at $2.21 a month and a small web app plus managed Postgres at $43.67.

Two costs deserve a warning label: volumes bill $0.15 per GB-month whether or not a machine is attached, and stopped machines still pay $0.15 per GB-month for their root filesystem. Managed Postgres starts at $38; self-managed Postgres on a $2 machine is possible if you own the backups.

A platform-risk footnote: in July 2026, Fly.io raised a $25 million Series D and installed former Docker CEO Scott Johnston, formalizing a pivot toward "computers for agents" — persistent compute for AI coding agents, with about 8,000 customers already building agent products. General app hosting is not going away, but the roadmap's center of gravity moved. The lowest prices in this article come with the newest strategy attached.

## Heroku pricing: the baseline everyone undercuts

The Cedar-generation dyno ladder: Eco at $5 flat for a 1,000-hour pool (dynos sleep), Basic at $7 (sleeps after 30 idle minutes), Standard-1X at $25 (512 MB, shared CPU), Standard-2X at $50 (1 GB), Performance-M at $250 (2.5 GB, dedicated compute), Performance-L at $500 (14 GB). Heroku dyno pricing has not moved in a decade — it is the fixed reference the challengers discount against.

The new Fir dynos are dedicated and Kubernetes-backed — dyno-1c-0.5gb at $25, dyno-1c-4gb at $80, dyno-8c-32gb at $640 — but they require a Fir Private Space, and that space caps out near $1,000 a month before any dyno runs. Heroku Postgres Essential plans are $5, $9, and $20 for 1, 10, and 32 GB; the Advanced tier starts at $150 for a 4 GB instance with 100 GB of storage included, high availability on by default, and $0.30 per GB beyond that. Egress remains unbilled in the common runtime — the single pricing edge Heroku keeps.

For a small app, Heroku means $7 (Basic) plus $9 (Essential-1 Postgres) — $16 a month for a platform that sleeps. For anything production-grade the stack compounds: two Standard-1X dynos, a Standard-0 database, and a logging add-on approach $110 a month.

## Railway vs Render vs Fly.io vs Heroku: three workloads, one arithmetic

Hold the workload constant and the platforms sort themselves out. Assumptions: a 730-hour month, always-on services billed at 100% active on the usage-based platforms, list prices from each vendor's own pages in November 2026.

| Platform | Metering model | Entry paid tier | Production instance | Platform fee |
| --- | --- | --- | --- | --- |
| Railway | Per-second usage, active CPU/RAM only | Hobby: $5/mo minimum (incl. $5 credit) | 1 vCPU + 2 GB ≈ $41/mo by usage | $0 — Pro $20/mo minimum adds seats, 99.99% target |
| Render | Fixed instance rates | Starter: $7/mo (0.5 CPU / 512 MB) | Standard: $25/mo (1 CPU / 2 GB) | $0 Hobby / $25 Pro per workspace |
| Fly.io | Per-second machines, no platform fee | shared-cpu-1x 512 MB: $3.69/mo | performance-1x: $33/mo (1 vCPU / 2 GB) | $0 — support from $29/mo optional |
| Heroku | Flat dyno rates + add-ons | Eco $5 flat (sleeps) / Basic $7 | Performance-M: $250/mo (2.5 GB dedicated) | $0 common runtime — Spaces ≈ $1,000/mo |

Now the same four platforms against the same four workloads:

| Workload (always-on, Nov 2026 list prices) | Railway | Render | Fly.io | Heroku |
| --- | --- | --- | --- | --- |
| Side project: 0.5 vCPU / 512 MB, 10 GB egress | ≈ $15.70 | ≈ $7.75 | ≈ $3.89 | $7 Basic (sleeps) / $25 Standard-1X |
| Production app: 1 vCPU / 2 GB, 50 GB egress | ≈ $43.10 | ≈ $31.75 | ≈ $34.00 ($13.70 shared CPU) | $25 for 0.5 GB; $250 for a real 2.5 GB dyno |
| Production app: 2 vCPU / 8 GB, 100 GB egress | ≈ $126.70 | ≈ $171.25 | ≈ $134.00 | $250 Performance-M (2.5 GB); no 8 GB dyno under $1,500 |
| Production database | ≈ $32 (self-managed 1 vCPU / 1 GB + volume) | $19–$40 managed | $38 managed (self-managed from ≈ $2) | $5–$20 Essential / $50 Standard-0 |
| 1 TB egress, app only | $50 | ≈ $146–$171 | $20 | $0 — not billed |

Read the table as three separate verdicts rather than one winner. The Render vs Railway question resolves on workload shape: Railway's per-second active billing wins when compute sits idle, Render's fixed $25 instance wins when the box runs hot around the clock — until egress pushes the bill back. Fly.io vs Railway on bandwidth is not close: $0.02 versus $0.05 per GB. Fly wins the side-project row outright; Heroku wins only egress and the paperwork.

Zoom out and RAM-per-dollar settles it: the Heroku alternatives undercut Heroku's entry tier four-to-seven on compute, Fly's shared machines thirteen-fold at 512 MB. Heroku keeps two edges — unbilled egress and a Salesforce-grade compliance stack — and both are niche.

## Which one to pick

**Solo builders and side projects: Fly.io.** A $3.69 machine that never sleeps beats a sleeping $7 dyno and a free tier that spins down after fifteen minutes. Pair it with proper managed Postgres — backups are the first thing you skip and the last thing you can afford to skip.

**Startups shipping a real product: Railway Pro or Render Pro.** Railway if traffic is spiky and the usage graph doubles as a budget tool; Render for fixed instance bills, autoscaling, and managed Postgres in one console. Run the math above with your own numbers — the gap between them is workload shape, not quality.

**Bandwidth-heavy apps — media, file delivery, websockets: Fly.io**, and it is not close. $0.02 per GB versus Render's $0.15 is a seven-fold spread that compounds every month, and Render's 1 TB included allowance only arrives on the $499 Scale workspace.

**Compliance-bound and Salesforce-adjacent teams: Heroku still.** Shield Spaces at roughly $3,000 a month buy HIPAA-grade paperwork that none of the challengers sell. You are paying for audit posture, not compute.

**And a fifth option: skip the PaaS tax.** A $6 VPS from the [Hetzner vs DigitalOcean VPS comparison](/articles/best-vps-hosting-2026-hetzner-vs-digitalocean-vs-vultr-vs-linode) runs most of the workloads here for a fraction of the price — if you accept owning the ops, the backups, and the 3 a.m. pages. Platform fees buy back your evenings; whether that trade is worth $40 a month is a budgeting question.

Whichever lane you take, keep the database off the app platform at any real scale — the [serverless Postgres hosting comparison](/articles/best-serverless-postgres-hosting-2026-neon-vs-supabase-vs-planetscale-vs-amazon-rds) covers the vendors that price better and survive an app-platform outage — and put [uptime monitoring](/articles/best-uptime-monitoring-tools-2026-better-stack-vs-uptimerobot-vs-checkly-vs-pingdom) in front of the deploy before your users become your alerting system.

## Frequently Asked Questions

### Is Railway cheaper than Render?

Workload shape decides. For idle-heavy or spiky apps, Railway — you pay only for active CPU and memory, and the $5 Hobby floor covers most side projects. For an always-on box running hot, Render's fixed $25 instance (1 CPU, 2 GB dedicated) bills less than the same machine on Railway's metering, which lands near $41. Render's $0.15 per GB egress and the $25 Pro workspace fee flip the math for traffic-heavy apps and teams. Idle → Railway; hot fixed-size boxes → Render; heavy egress → Fly.io.

### What is the cheapest Heroku alternative in 2026?

Fly.io on price, with a caveat: a shared-CPU machine starts at $2.19 a month for 256 MB and $3.69 for 512 MB, and nothing else here keeps an always-on app alive that cheap. The caveat: Fly has no free tier, so "cheapest" is not "free." Render's free tier sleeps after fifteen minutes, Railway's floor is $5, and Heroku's Eco dyno is $5 flat and sleeps too.

### Does Fly.io have a free tier?

No. New organizations get a $1 trial credit valid for seven days — enough to deploy and break something, not to host anything. Inbound traffic, shared IPv4/IPv6, and the first 10 GB of volume snapshots are free; there is no ongoing free compute allowance. The old three-free-VMs allowance died with the legacy plans in October 2024.

### How much does Heroku cost per month for a small app?

A sleeping hobby stack is $10: one $5 Eco dyno plus the $5 Essential-0 Postgres. An always-on small app is about $16 ($7 Basic + $9 Essential-1) — but Basic dynos sleep after 30 idle minutes, so real uptime starts at $25 for one Standard-1X. A production-ready setup — two Standard-1X dynos, a Standard-0 database, and basic logging — runs about $107 a month. The Fir generation requires a Private Space at roughly $1,000 a month before the first dyno.

### Should I run my database on the same platform as my app?

For prototypes, yes — it removes a class of networking setup. For production, usually no. Render's $19 Postgres is reasonable and managed; Railway's self-managed database on a 1 vCPU / 1 GB service runs about $30 a month plus your own backup discipline; Fly's managed Postgres starts at $38; Heroku's Essential tiers cap connections at 20 to 40. A dedicated Postgres vendor usually prices better at scale and stays up when the app platform has a bad day — the serverless Postgres comparison above breaks down that market.

Bottom line: the market for Heroku alternatives in 2026 splits into three clean lanes — Railway for usage-based pricing that treats idle compute as free, Render for fixed bills with the least configuration surface, Fly.io for the cheapest always-on machines and the cheapest bandwidth. Heroku remains defensible only when the Salesforce relationship or a Shield-grade compliance stack pays the premium for you. Price your workload the way this article did — same box, same bandwidth, same 730-hour month — and the ladder gaps ($0.5 GB dynos, $1,000 Spaces, $0.15 per GB egress) will make the decision faster than any feature matrix.
