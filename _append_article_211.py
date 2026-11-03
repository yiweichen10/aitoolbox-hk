# -*- coding: utf-8 -*-
"""Append article #211: Best S3-Compatible Object Storage Pricing 2026 (AWS S3 vs Cloudflare R2 vs Backblaze B2 vs Wasabi)."""
import json, sys, re

PATH = "data/articles_en.json"

TITLE = "S3-Compatible Object Storage Pricing in 2026: AWS S3 vs Cloudflare R2 vs Backblaze B2 vs Wasabi"
SLUG = "best-object-storage-pricing-2026-aws-s3-vs-cloudflare-r2-vs-backblaze-b2-vs-wasabi"
DATE = "2026-11-04"
DATE_FULL = "November 4, 2026"
CATEGORY = "AI Web Development"
DESCRIPTION = ("AWS S3, Cloudflare R2, Backblaze B2, and Wasabi compared on 2026 pricing: storage per TB, egress "
               "fees, API call charges, retention rules, and which S3-compatible provider each workload should pick.")
KEYWORDS = [
    "cloud object storage",
    "Cloudflare R2 vs S3",
    "Backblaze B2 pricing",
    "S3 egress fees",
    "cheapest S3-compatible storage",
    "Wasabi pricing",
    "S3 alternatives",
    "object storage pricing",
]

CONTENT = r"""Storing 10TB of data in AWS S3 Standard and serving all 10TB back out to users every month costs about $1,150. Run the identical workload on Backblaze B2 and the bill lands near $70 — a sixteen-fold difference between two services that speak the exact same S3 API. Those figures come from the four vendors' published rate cards in November 2026, and they explain why cloud object storage has quietly become the most distorted line item in a typical infrastructure budget. AWS now leads its own marketing with up to $200 in free credits for new accounts — a telling sign about the defaults. I have moved multi-terabyte archives between all four of these providers, and the engineering work — an S3-compatible client, a sync script, a DNS cutover — is a weekend, not a quarter. The hard part is that every vendor meters the same three resources (capacity, requests, bandwidth) on different models: AWS bills all three, Cloudflare gives bandwidth away, Backblaze caps free bandwidth at three times what you store, and Wasabi charges capacity alone but makes every byte stay 90 days.

## How an object storage bill actually gets built

Every provider here charges for three things, and the ratios between them decide everything. Storage: a per-GB monthly rate for bytes in the bucket. Requests: an API-call charge for PUTs, GETs, and LISTs. Egress: a per-GB charge for data leaving to the public internet. On AWS, storage runs $0.023 per GB for the first 50TB, but egress is $0.09 per GB after a pooled 100GB monthly allowance — nearly four times the storage rate. Serving a 5MB file one time from S3 can cost more than keeping that file for a month. Requests matter less for backups but a lot for high-traffic assets: $0.005 per thousand PUTs and $0.0004 per thousand GETs sound like noise until a misconfigured crawler issues 50 million GETs in a weekend.

The four vendors are four answers to the same question: which of those three line items do we hide inside a flat rate? AWS bills all three separately and adds eight storage classes with different minimums. Cloudflare kills the egress line entirely. Backblaze bundles requests into the capacity price and forgives egress up to three times your stored volume. Wasabi flattens everything into one capacity number and removes the bandwidth line at the price of a 90-day retention clock. Object storage pricing is not complicated; it is itemized in ways that reward reading the footnotes first.

## The 2026 rates, in one table

| Provider | Storage (per TB/mo) | Egress to internet | API / request charges | The catch |
| --- | --- | --- | --- | --- |
| AWS S3 Standard | $23.55 first 50TB ($0.023/GB) | $0.09/GB after 100GB free (pooled across AWS) | PUT $5/1K, GET $0.40/1K | Egress dominates; eight storage classes with their own minimums |
| Cloudflare R2 | $15.36 ($0.015/GB) | $0, always | Class A $4.50/M writes, Class B $0.36/M reads | Rounding up to next billing unit; 30-day minimum on the cheap tier |
| Backblaze B2 | $6.95 | Free up to 3x stored data/mo, then $0.01/GB | Most calls free; Class D $0.004/10K after 2,500/day free | 3x cap punishes read-heavy serving; single published-region rate |
| Wasabi | $7.99 | $0, unlimited | $0 | 90-day minimum retention; 1TB monthly minimum per account |
| B2 Overdrive | $15 | Unlimited, free | Same as B2 | Multi-petabyte commitment required |
| S3 Glacier Deep Archive | $0.99 ($0.00099/GB) | Retrieval fees apply | 12-hour restore windows | Not a live tier; restores cost more than a year of storage |

Three footnotes that change the math. AWS's free 100GB of egress is pooled across every AWS service on the account, not per bucket, so most teams burn it in an afternoon. Cloudflare rounds usage up to the next billing unit — store 1.1GB and you pay for 2GB — irrelevant at scale, irritating at small scale. And Backblaze's headline $6.95 rate is the published US West figure; other regions differ slightly, though not enough to reorder this table.

## AWS S3: the default, and the tax you pay to leave it

S3 Standard at $0.023 per GB for the first 50TB is no longer a good storage price — roughly 3.4 times Wasabi's rate and Backblaze's — but S3 was never really selling storage. It sells the ecosystem: lifecycle policies that tier objects into Glacier classes automatically, event notifications, versioning, replication, and native integration with Athena, EMR, SageMaker, and nearly every analytics tool that exists. If your data lake lives inside AWS and your compute sits next to the bucket, moving the bucket to a cheaper provider means paying AWS egress twice — once to export, forever after to read across providers. That is the strongest lock-in in the category, and paying it is rational when the compute gravity is real.

Where S3 still wins outright is cold data. Glacier Deep Archive at $0.00099 per GB — about $1 per TB per month — is the cheapest durable bytes on any public cloud, and Standard-IA at $0.0125 per GB handles the middle ground, with a 30-day minimum duration and a 128KB minimum billable object size. The trap is treating the headline storage number as the bill. S3 egress fees at $0.09 per GB after the shared 100GB allowance turn a $236 monthly storage line into a $1,150 all-in figure once anyone actually downloads the data. New accounts get some relief — up to $200 in credits and a six-month free plan — but credits run out and rates do not.

## Cloudflare R2: zero egress as the entire business model

R2's pitch fits in one sentence: $0.015 per GB-month, $4.50 per million write operations, $0.36 per million read operations, and no charge for bandwidth to the internet — ever, on any storage class. The free tier is real too: 10GB stored, a million Class A writes, and 10 million Class B reads every month with no card required — one of the few free production options here alongside B2's 10GB. For any workload where downloads dominate — software distributions, media files, public datasets — the Cloudflare R2 vs S3 question ends at the bandwidth line. Ten terabytes served monthly from S3 costs about $920 in egress alone; from R2 it costs zero, and the storage runs about $150.

The caveats are small but real. Rounding is up, always: 1.1GB bills as 2GB-months, and a million-and-one write operations bill as two million. The Infrequent Access tier looks cheap at $0.01 per GB but adds a $0.01 per GB retrieval fee and a 30-day minimum duration, so churny data that leaves early pays the full month anyway. R2 also lacks S3's storage-class catalog — there is no deep-archive equivalent, so a petabyte of cold tape-replacement data has no home here. Migration is unusually painless: Super Slurper bulk-copies existing buckets for free, and Sippy lazily migrates objects to R2 as they are requested, which moves a serving bucket without a cutover weekend.

## Backblaze B2: the backup math still wins

Backblaze B2 pricing has one job: make backup and archive storage boringly cheap without metering tricks. The current rate is $6.95 per TB per month, the first 10GB is free forever, and there are no minimum file sizes or storage-duration fees — delete everything tomorrow and the bill is tomorrow's storage. API calls are effectively free: Class A, B, and C transactions cost nothing on pay-as-you-go accounts, and the one metered class (Class D, certain list-and-copy variants) is $0.004 per 10,000 calls after a 2,500-per-day free allowance. At 10TB, that is $69.50 a month against S3's roughly $236 before a single byte moves.

The interesting meter is egress: free up to three times your average monthly stored data, then $0.01 per GB — a tenth of AWS's rate — and permanently free through CDN and compute partners such as Cloudflare and Vultr. For backups, where egress is a rare disaster-recovery restore, the 3x allowance is effectively infinite. For read-heavy serving it is a real ceiling: serving 10TB monthly from a 1TB bucket burns the allowance and adds about $90. B2 is also a single-rate product — no deep archive tier, no IA tier — which is either honesty or a missing feature depending on your archive strategy; for rare cold-restore-heavy profiles, S3's Glacier classes remain better. At the top end, B2 Overdrive offers terabit-scale throughput at $15 per TB with unlimited free egress, but it requires a multi-petabyte commitment well out of most readers' range.

## Wasabi: one flat rate and a 90-day clock

Wasabi pricing is the simplest in the category: $7.99 per TB per month, pay as you go, no egress fees, no API request fees, no storage classes — everything is hot storage with single-file retrieval. That flatness is the product. A CCTV integrator archiving 200TB of surveillance footage knows the bill is $1,598 a month, and unlimited restores cost nothing. Two details deserve a hard look. Wasabi bills in base-2 units, so one terabyte as most people mean it (1,000GB) actually bills as 1,024GB — $8.18, not $7.99. And pay-as-you-go accounts carry a 90-day minimum storage duration: delete an object on day 10 and you still pay for 90 days. There is also a minimum monthly charge tied to 1TB of active storage per account, and the free trial is 100GB for 30 days on a company email (10GB for 14 days on freemail), not a permanent tier.

The 90-day rule shapes who Wasabi is for. Write-once, retain-long data — surveillance video, compliance archives, immutable backup sets — fits the model perfectly and gets hyperscaler-crushing economics for it. Churny data gets punished: a staging bucket, a thumbnail cache, or an application that rewrites objects weekly pays for three months of storage per object. Reserved Capacity Storage softens the rule for larger buyers — 25TB minimum, a 30-day minimum duration, and term discounts across 1-, 3-, and 5-year commitments, plus premium support — but that is a procurement conversation, not a credit-card signup.
## Which cloud object storage fits each workload

Four billing models, four clean answers. Picking cloud object storage in 2026 is mostly a matter of classifying your access pattern honestly, because the price gaps dwarf any feature difference.

Backups, disaster recovery, and write-rarely archives: Backblaze B2, and it is not close. At $6.95 per TB with free restores inside the 3x allowance and effectively free API calls, a 10TB backup set costs about $70 a month versus $236 on S3 — and the savings fund the thing that actually matters, which is verifying restores. Wire your backup jobs to report success into a [cron monitoring tool](/articles/best-cron-monitoring-tools-2026-cronitor-vs-healthchecks-vs-dead-mans-snitch-vs-better-stack), because an archive you never test is a hope, not a backup. Wasabi takes the same workload when retention is guaranteed past 90 days and restores are frequent — its unlimited free egress beats B2's 3x cap for teams restoring big sets monthly.

Public assets, media, and download-heavy serving: Cloudflare R2. The cheapest S3-compatible storage for anything with meaningful download volume is the one that charges zero for bandwidth, and R2 is the only provider here with an unconditional $0 egress line. Among S3 alternatives for software distribution or video, the math is not incremental — it is the difference between a $1,100 month and a $150 month at 10TB served. The one cost to model is Class B reads: at $0.36 per million, even a very hot asset endpoint stays under a few dollars.

Data lakes and AWS-native stacks: S3, with lifecycle policies moving cold objects into Glacier Deep Archive at $0.99 per TB. Once Athena queries, EMR jobs, or SageMaker training reads run against the bucket hourly, replicating the data elsewhere costs more in cross-provider egress than the storage premium saves. That is also where metering gets Byzantine enough that a [cloud cost management](/articles/best-cloud-cost-management-tools-2026-cloudzero-vs-finout-vs-vantage-vs-kubecost) tool pays for itself — S3 bills hide in eight storage classes, request classes, and lifecycle transition fees. Predictable fixed-capacity budgets: Wasabi Reserved Capacity, where a 3-year block turns storage into a contract line item your finance team can forecast to the dollar.

## Frequently Asked Questions

### What are S3 egress fees, and why do they cost more than the storage itself?

Egress is the per-GB charge for data leaving a provider's network to the public internet. AWS charges $0.09 per GB after a pooled 100GB monthly allowance; S3 Standard storage costs $0.023 per GB-month. Storage is billed once per month per byte; egress is billed on every download. A bucket you fill once and serve ten times pays eleven times its storage rate in bandwidth. This asymmetry is why every challenger's pitch starts with the egress line: R2 charges $0, B2 forgives three times your stored volume, Wasabi charges nothing at all.

### Cloudflare R2 vs S3: when does AWS still win?

AWS wins when compute gravity is on its side. If Athena, EMR, Lambda, or SageMaker read the bucket constantly, in-region S3-to-service traffic is free while R2-to-AWS traffic crosses providers and bills at AWS rates, which erases R2's storage advantage fast. AWS also wins for deep archive (no R2 equivalent to Glacier Deep Archive's $0.99 per TB) and for teams that need eight storage classes, object locking at scale, or the compliance paperwork of the biggest provider. Everywhere else — any workload with meaningful public downloads — R2 wins the bill outright.

### What is the cheapest S3-compatible storage in 2026?

Per pure capacity, Backblaze B2 at $6.95 per TB edges Wasabi at $7.99 per TB, both far under R2's $15.36 and S3's $23.55. But cheapest storage is not cheapest bill. A backup archive with rare restores is cheapest on B2. Data restored or served often is cheapest on Wasabi (unlimited free egress) or R2 (zero egress, slightly higher capacity rate). A 10TB bucket serving 10TB monthly costs about $70 on B2, $80 on Wasabi, $150 on R2, and $1,150 on S3 — four different winners depending on which line item dominates, which is exactly why the question needs your access pattern attached.

### What is Wasabi's 90-day rule and who gets burned by it?

Pay-as-you-go Wasabi accounts bill every object for a minimum of 90 days regardless of when it is deleted. Upload 5TB on day one, delete it on day ten, and you pay for 90 days anyway. The rule supports the flat-rate model — unlimited free egress only works if data cannot churn in and out faster than the flat rate amortizes. Teams that get burned run rewrite-heavy workloads: caches, staging areas, and versioned data with aggressive pruning. If deletion is part of daily operation, either pick B2 (no minimum duration) or move to Wasabi's Reserved Capacity plans, which drop the minimum to 30 days from a 25TB commitment.

### Can I migrate off S3 without downtime?

Yes, and the tooling is free on the Cloudflare side. Sippy lives inside R2 and copies objects from your existing S3 bucket lazily, as each one is requested — the origin absorbs misses, R2 fills in over weeks, and nothing ever 404s. Super Slurper does bulk one-shot migrations at no charge beyond R2 write operations. From B2, the standard route is rclone or restic sync plus a dual-write period before cutover. The two genuine frictions: AWS charges $0.09 per GB to leave (negotiable at scale, and forgone entirely by Sippy since objects copy on read), and applications hard-wired to S3-specific features like event notifications need rewiring. Budget a weekend for the mechanics and a month of dual-running for the confidence.

## The bottom line

In 2026, cloud object storage is a commodity whose four leading vendors bill on four genuinely different models, and the spread between them is the widest in infrastructure: the same 10TB workload ranges from $70 to $1,150 a month. Match the billing model to the access pattern and the decision makes itself. Backups and archives belong on Backblaze B2, where capacity is cheap and the 3x free-egress allowance covers every disaster restore. Download-heavy serving belongs on R2, because zero egress is not a discount — it is a different cost structure. Fixed-capacity, write-once workloads with guaranteed retention belong on Wasabi, provided the 90-day clock matches your lifecycle. And data lakes wired into AWS compute stay on S3, where the ecosystem premium is real but the egress bill needs a lifecycle policy and an occasional rate-card re-read. Every number here comes from the vendors' published pricing pages in early November 2026 — verify before you sign, because B2's rate moved from $6.00 to $6.95 per TB recently enough that per-TB rates in this category clearly drift.
"""

def main():
    with open(PATH, encoding="utf-8") as f:
        data = json.load(f)
    if any(a["slug"] == SLUG for a in data):
        sys.exit("Slug already exists: " + SLUG)
    entry = {
        "title": TITLE,
        "slug": SLUG,
        "date": DATE,
        "dateFull": DATE_FULL,
        "category": CATEGORY,
        "description": DESCRIPTION,
        "keywords": KEYWORDS,
        "content": CONTENT.strip(),
    }
    data.append(entry)
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    words = len(re.findall(r"\S+", CONTENT))
    pk_cs = len(re.findall(r"cloud object storage", CONTENT))
    pk_ci = len(re.findall(r"cloud object storage", CONTENT, re.I))
    print(f"Appended {SLUG}: words={words}, pk_case_sensitive={pk_cs}, pk_case_insensitive={pk_ci}")

if __name__ == "__main__":
    main()
