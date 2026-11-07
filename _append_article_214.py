# -*- coding: utf-8 -*-
"""Append article #214: Serverless Postgres Hosting 2026 (Neon vs Supabase vs PlanetScale vs Amazon RDS)."""
import json
import sys

PATH = "data/articles_en.json"

ARTICLE = {
    "title": "Best Serverless Postgres Hosting in 2026: Neon vs Supabase vs PlanetScale vs Amazon RDS",
    "slug": "best-serverless-postgres-hosting-2026-neon-vs-supabase-vs-planetscale-vs-amazon-rds",
    "date": "2026-11-07",
    "dateFull": "November 7, 2026",
    "category": "AI Infrastructure",
    "description": "Neon vs Supabase vs PlanetScale vs Amazon RDS on real November 2026 pricing: CU-hour metering, the $25-to-$599 Supabase ladder, PlanetScale Metal, Aurora's new 0-ACU pause, and three worked workloads from side project to I/O-heavy production.",
    "keywords": [
        "serverless Postgres hosting",
        "Neon vs Supabase",
        "Supabase pricing",
        "Neon pricing",
        "PlanetScale pricing",
        "Aurora Serverless v2 pricing",
        "cheapest managed Postgres",
        "Supabase alternatives",
        "Postgres branching",
        "RDS pricing",
    ],
    "content": """PostgreSQL passed MySQL as the most-used database among professional developers in 2025 — 55.6% adoption per Stack Overflow's survey — and the hosting market reorganized around it within eighteen months. Supabase raised $100 million at a $5 billion valuation in October 2025. Databricks acquired Neon in 2025 in a deal reported around $1 billion and folded it into its Lakebase platform. PlanetScale, a MySQL company for its entire life, shipped Postgres and spent 2026 pushing Metal — an NVMe-backed cluster tier with unlimited IOPS — down to a $50 entry point and onto Azure. Serverless Postgres hosting is now the most contested corner of cloud infrastructure, and the pricing pages have become hard to compare, because every vendor bills in a different unit: compute units, fixed instance hours, capacity units, or flat tiers.

This article prices all four the way an operator would: the same three workloads, the same arithmetic, list prices pulled from each vendor's own pricing pages in November 2026. Where a number is an estimate, it says so. Where a vendor's \"serverless\" label does not survive contact with the billing model, it says that too.

## Serverless Postgres hosting bills four different ways

The word serverless has been stretched past usefulness, so start with the metering, because that is where every cost surprise lives.

- **Neon** bills compute in CU-hours, metered per second, priced at $0.106 (Launch) or $0.222 (Scale) per CU-hour. One CU is 1 vCPU plus 4 GB RAM. Computes suspend after 5 minutes idle on the Free and Launch plans and wake in a few hundred milliseconds; the Scale plan sets the timeout anywhere from 1 minute to always-on.
- **Supabase** bills fixed compute instances by the hour, with partial hours rounded up. The Micro instance included with the Pro plan is a shared 2-core ARM box with 1 GB RAM. Paid projects never pause; only Free-plan projects do, after a week of inactivity.
- **PlanetScale** bills fixed nodes that are always on — there is no scale-to-zero at all. You pay for the cluster size you picked, whether traffic arrives or not.
- **Aurora Serverless v2** bills per ACU-hour ($0.12 on Standard) between a minimum and maximum you set. Since September 2026 it can scale down to 0 ACU and auto-pause, resuming in about 15 seconds on PostgreSQL 16.3 and later. Plain RDS, by contrast, is not serverless in any sense: an instance bills every hour it exists, and a stopped instance restarts itself after 7 days.

Three costs hide behind all four models. Storage is billed separately everywhere. Egress is billed everywhere except inside each platform's included allowance. And the add-ons — point-in-time restore windows, branching, extra projects — are priced as line items that never appear in the plan headline.

## Neon pricing in 2026: usage-based, no monthly minimum

Neon's Free plan is the most usable free database tier in the group: 100 CU-hours per project per month, 1 GB of storage per project (20 GB across the account), 10 branches, 5 GB egress, and a 6-hour restore window. A database running 2 hours a day on a 0.25 CU compute uses about 15 CU-hours a month — comfortably inside the allowance at $0.

Paid plans are pure usage. Launch costs $0.106 per CU-hour and $0.35 per GB-month of storage, with 500 GB of egress included before $0.10 per GB kicks in, and Neon's FAQ states there is no monthly minimum on Launch or Scale. Scale raises compute to $0.222 per CU-hour and adds what production buyers actually need: SOC 2, ISO, and HIPAA compliance, private networking, metrics export, a 99.95% SLA, fixed sizes up to 56 CU (224 GB RAM), and a 30-day restore window.

The add-ons are transparent: extra branches run $1.50 per branch-month, instant-restore history is $0.20 per GB-month of retained changes, and snapshots are $0.09 per GB-month. The post-Databricks platform also bundles auth (60,000 MAU on Free, 1 million on paid), object storage at $0.023 per GB-month, and serverless functions — which matters later in this comparison.

The honest math: a 0.25 CU compute active 9 hours a day accrues 67.5 CU-hours, or $7.16 a month, plus storage. But an always-on 2 CU compute — the equivalent of a small production instance — accrues 1,460 CU-hours and lands near $172 a month before storage. Scale-to-zero saves money only when there is zero to scale.

## Supabase pricing in 2026: $25 flat until the compute ladder bites

Supabase is the bundle play. Pro costs $25 a month and includes the database plus auth (100,000 MAU), 8 GB of disk, 100 GB of file storage, 250 GB of egress, daily backups with 7-day retention, and $10 of compute credit that covers one Micro instance. A spend cap is on by default, so the bill cannot quietly run away. The company ended 2025 having created more than 15 million new databases in the year, with its GitHub star count at 95,000 — the adoption is real, and so is the lock-in fear it triggers, except the lock is open source: everything runs on plain Postgres you can pg_dump out of.

The compute ladder is where bills move: Small $15, Medium $60, Large $110 (dedicated 2-core, 8 GB RAM), XL $210, 2XL $410, 4XL $960. Overages: disk $0.125 per GB, egress $0.09 per GB (cached egress $0.03), and $0.00325 per MAU past 100,000. Branching — the feature that gives every pull request its own database copy — bills at $0.01344 per branch-hour, so an always-on branch costs about $10 a month.

The $599 Team plan buys SOC 2 and ISO 27001 reports, SSO, 14-day backups, and 28-day log retention. The jump from $25 to $599 is the steepest in this comparison, and small teams that need only the compliance reports pay a tax for it. If you are evaluating the bundle, the [Supabase tool profile](/tools/supabase) covers platform features; the auth component alone can replace a dedicated vendor, which is worth checking against the [authentication platform comparison](/articles/authentication-platforms-2026-auth0-vs-clerk-vs-supabase-vs-workos) before you add one.

## PlanetScale pricing in 2026: no free tier, Metal money

PlanetScale killed its free Hobby tier in 2024 and never brought it back; the entry point is a single-node Postgres at $5 a month — a 1/16-vCPU, 512 MB PS-5 node with 10 GB of storage and 100 GB of egress included, then $0.06 per GB. Production-grade clusters are three nodes across three availability zones with a 99.99% SLA, starting around $15 a month at the bottom size. Storage beyond 10 GB bills at $0.50 per GB per instance on standard EBS-backed clusters.

Metal is the reason to look. Metal clusters attach local NVMe drives with unlimited IOPS — no per-I/O meter, no network storage bottleneck — and since October 2026 they start at $50 a month (M-10: three nodes, 1/8 vCPU and 1 GB RAM each, 10 GB) and run on AWS, GCP, and now Azure. Pricing scales with disk: an M-40 cluster at 50 GB is $180; an M-80 (1 vCPU, 8 GB RAM per node, three nodes) at 100 GB is $320; an M-160 at 200 GB is $630.

The trade-off is blunt: everything is always-on, so there is no cheap idle mode, and the smallest production-ready cluster costs more than three months of Neon's side-project tier. What you buy instead is predictable latency. Postgres branching and non-blocking schema migrations — the workflow that made PlanetScale famous on MySQL — work the same on the Postgres product, and the new Database Traffic Control feature puts resource budgets on query traffic.

## Amazon RDS and Aurora Serverless v2: the enterprise meter, now with a zero

RDS for Postgres starts at db.t4g.micro — 2 vCPU, 1 GB RAM — at $0.016 an hour, about $12 for a 730-hour month, plus $0.115 per GB-month of gp3 storage. RDS pricing hides its own traps: backups beyond 100% of instance size bill at $0.095 per GB-month, deleted data never shrinks the volume (you rebuild through a Blue/Green deployment), and new AWS accounts get up to $200 in free-tier credits over six months while the legacy 12-month free tier applies only to older accounts.

Aurora Serverless v2 pricing splits into two storage modes: $0.12 per ACU-hour on Standard ($0.156 on I/O-Optimized), with $0.10 per GB-month of storage plus $0.20 per million I/Os on Standard, or a flat $0.225 per GB-month on I/O-Optimized with no I/O meter. September 2026 brought the change that matters: a 0-ACU minimum with auto-pause, resuming in roughly 15 seconds on newer engine versions. Aurora's instance rates run about 15% above equivalent RDS instances, but its storage shrinks when you delete data, its backups cost $0.021 per GB-month versus RDS's $0.095, and read replicas share one storage volume.

One worked example from a November 2026 price-list analysis: on a 500 GB database with high availability and read replicas, Aurora I/O-Optimized came in $29.17 a month under RDS, while Aurora Standard lost as soon as it billed more than about 55 million I/Os against a single-HA RDS instance. Aurora is the enterprise option that now, finally, can idle at zero — but you assemble it from parts.

## The numbers side by side

With list prices on the table, serverless Postgres hosting stops being an apples-to-oranges argument and becomes arithmetic. The first table maps the plan structures, the second prices one concrete always-on workload the same way on all four, and the third maps scenarios to the rational pick.

| Platform | Entry paid price | Compute billing | Storage | Scale-to-zero | HA & SLA |
|---|---|---|---|---|---|
| Neon | Usage-based, no minimum | $0.106–$0.222 per CU-hour (per-second metering) | $0.35/GB-month | Yes — 5 min idle; configurable on Scale | Multi-AZ storage default; 99.95% SLA on Scale |
| Supabase | $25/mo (Pro) | Fixed instances, hourly ($10–$960 ladder) | 8 GB included, then $0.125/GB | Free plan pause only (7 days idle) | Managed; SLAs on Enterprise |
| PlanetScale | $5/mo single node | Fixed nodes, always-on | 10 GB included, then $0.50/GB/instance (Metal includes storage) | No | 3-node HA, 3 AZs, 99.99% SLA |
| Amazon RDS / Aurora | ≈$12/mo (db.t4g.micro) | $0.016/instance-hr or $0.12/ACU-hour | $0.115/GB (gp3) or $0.10/GB + $0.20/1M I/O (Aurora) | Aurora v2: 0 ACU auto-pause since Sep 2026 | Multi-AZ ≈ 2× compute; AWS ecosystem SLAs |

**Always-on 2 vCPU-class workload, 50 GB dataset:**

| Configuration | Compute | Storage & extras | Est. monthly |
|---|---|---|---|
| Neon Launch — 2 CU always-on | 1,460 CU-hr × $0.106 = $155 | $17.50 storage | ≈$172 |
| Supabase Pro + Large (dedicated 2-core, 8 GB) | $25 + $110 − $10 credit = $125 | $5.25 (42 GB disk overage) | ≈$130 |
| PlanetScale Metal M-40 — 3 nodes, 50 GB, unlimited IOPS | included | included | $180 |
| RDS db.t4g.large, single-AZ | ≈$0.128/hr × 730 = $94 | $5.75 (gp3) | ≈$100 |
| Aurora Serverless v2 — 2 ACU average | 1,460 ACU-hr × $0.12 = $175 | $5.00 + ~20M I/O ($4) | ≈$184 |

Assumptions: us-east-1 on-demand, 730-hour month, November 2026 list prices, 50 GB dataset. The db.t4g.large rate follows RDS's linear Graviton scaling from the published micro price — verify in the AWS calculator before committing spend. Note what the table says: the always-on RDS instance is the cheapest pure database, Supabase is $30 more with auth, storage, and realtime thrown in, and Neon pays a premium for elasticity it never uses on steady traffic.

| Scenario | Rational pick | Why | Watch out for |
|---|---|---|---|
| Side project, spiky traffic | Neon Free | 100 CU-hours plus scale-to-zero; idle months cost $0 and never pause | 1 GB cap per project; Supabase Free pauses after a week idle |
| Small B2B SaaS with auth + files | Supabase Pro | ≈$130 all-in replaces auth, storage, and realtime vendors | Compute ladder steps double ($60 → $110 → $210) |
| Branch-per-PR CI, staging farms | Neon Launch | Branches ≈$1.50/month each; 7-day instant restore | Restore-history add-on at $0.20/GB-month |
| I/O-heavy, latency-critical production | PlanetScale Metal or Aurora I/O-Optimized | Unlimited IOPS / flat I/O pricing; predictable p99 | Metal's 3-node floor pricing; Aurora's ≈15% instance premium over RDS |

## Frequently Asked Questions

### Neon vs Supabase: which should a solo founder pick?

Both free tiers are genuine, and they optimize for different failure modes. Neon's scales to zero and never pauses — a dormant side project stays online and costs nothing, which makes it better for demos and portfolio apps. Supabase's Free plan pauses after a week of inactivity and has no automatic backups, which has ruined more than one investor demo; but Pro at $25 replaces your auth vendor, file storage, and realtime layer in one bill. The arithmetic: if you need the bundle, $25 buys more than Neon at $0 plus three SaaS subscriptions; if you do not, Neon's metering is the cheaper and more predictable path.

### What is the cheapest managed Postgres hosting right now?

Free: Neon — 100 CU-hours and 1 GB per project with scale-to-zero and no pausing, against Supabase Free's one-week inactivity pause. Cheapest paid: PlanetScale's $5 single-node Postgres, though 512 MB RAM limits it to development and low-traffic duty. Cheapest always-on production database: RDS db.t4g.micro at roughly $12 plus storage — single-AZ, with the patching and backup checklist on your side of the fence. The trap in cheapest-hosting questions is egress: a database pushing 500 GB a month to app servers pays $0.10/GB past Neon's allowance and $0.09/GB past Supabase's 250 GB, which can exceed the compute line.

### Does PlanetScale support Postgres, or is it still MySQL-only?

Both. Vitess/MySQL remains the mature, hyperscale product, with PS-10 clusters from $39 a month, and the Postgres product — generally available since 2025 — now has single-node plans from $5, three-node HA with a 99.99% SLA, and Metal NVMe clusters from $50, extended to Azure in October 2026. Postgres branching and non-blocking DDL carry over from the MySQL workflow. One caveat from teams running it: the Postgres fleet is younger than the MySQL one, so some ecosystem tooling and extensions lag. If your stack depends on a specific extension, verify support before migrating.

### Can Aurora Serverless v2 really scale to zero now?

Yes, since September 2026 — set the minimum to 0 ACU with auto-pause enabled and compute charges stop when the cluster idles. AWS says a typical resume takes about 15 seconds, and the feature requires Aurora PostgreSQL 16.3, 15.7, 14.12, or 13.15 or later. Two cautions. First, storage and I/O still bill while paused, so a paused cluster is cheap, not free. Second, a 15-second wake is not a sub-second wake: Neon's suspend-resume lands in a few hundred milliseconds, and AWS itself positions auto-pause for workloads without a strict latency SLO.

### What are the best Supabase alternatives if I outgrow it?

Three exit paths, in order of pain. Same database, less bundle: Neon or plain RDS — a pg_dump and restore away, since Supabase runs vanilla Postgres. Same database, more performance: PlanetScale Metal when I/O becomes the bottleneck. Same everything, your hardware: self-host the open-source stack on a [cheap VPS](/articles/best-vps-hosting-2026-hetzner-vs-digitalocean-vs-vultr-vs-linode) — the savings turn real only once a database engineer is already on payroll. What you lose in any exit is the integrated auth and realtime layer, so budget for replacements; the authentication platform comparison linked above is the shortlist.

## Bottom line

Serverless Postgres hosting in 2026 is a buyer's market, and the decision collapses to three questions. Do you want a bundle or a database? Supabase's $25 Pro plan is the best bundle deal in cloud infrastructure right now; Neon is the better pure database. Is your workload spiky or steady? Spiky workloads belong on Neon's metering or Aurora's new 0-ACU floor; steady production traffic is cheaper on always-on nodes — RDS at the low end, PlanetScale Metal when I/O dominates. And what does the headline price not include? Storage, egress, restore windows, and branches are the four line items every vendor moves somewhere else — price those, not the headline. The vendors reprice quarterly: Aurora added a zero in September, PlanetScale cut Metal's floor in October. Re-run your numbers the month you sign."""
}

def main():
    with open(PATH, "r", encoding="utf-8") as f:
        arts = json.load(f)
    assert isinstance(arts, list), "articles_en.json must be a list"
    expected = 213
    assert len(arts) == expected, f"Expected {expected} articles, found {len(arts)} — aborting"
    slugs = {a.get("slug") for a in arts}
    assert ARTICLE["slug"] not in slugs, "Slug already exists — aborting"
    arts.append(ARTICLE)
    with open(PATH, "w", encoding="utf-8", newline="\n") as f:
        json.dump(arts, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"OK: appended '{ARTICLE['slug']}', total articles = {len(arts)}")

if __name__ == "__main__":
    main()
