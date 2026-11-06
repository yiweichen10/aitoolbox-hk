A $5.99 Hetzner CX23 ships with 4 GB of RAM, two shared vCPUs and 20 TB of monthly outbound traffic. DigitalOcean's $6 Droplet ships with 1 GB of RAM and 1 TB. Vultr's and Linode's five-dollar plans match that 1 GB of memory while splitting the difference on bandwidth. Same budget, four times the memory, twenty times the traffic — that spread is the defining fact of 2026 VPS hosting, and most comparison posts still refuse to do the arithmetic.

The market context makes the choice more interesting, not less. DigitalOcean reported $1.03 billion in ARR for Q1 2026, up 22% year over year, with gross margin down five points to 56% as it funds AI-focused capacity. Hetzner, a private German company that publishes no growth figures, raised the floor price of its cheapest shared-CPU line by roughly a third in its 2026 restructure — the CX22's roughly €4.50 became the CX23's €5.99 — and still leads every US rival on entry-tier specs by a factor of three to four. Both facts are true simultaneously. Which provider wins depends on what you run, where your users live, and how much data you actually push. This article does the arithmetic line by line, using each vendor's official pricing as of November 2026.

## What VPS hosting actually costs in 2026: the entry-tier math

Start at the bottom of each lineup, because that is where nearly everyone starts. The table below compares each provider's cheapest credible plan — the one you would actually run a side project on.

| Provider & plan | Price/mo | vCPU / RAM | Storage | Included transfer |
|---|---|---|---|---|
| Hetzner CX23 (EU) | €5.99 (~$7) | 2 shared / 4 GB | 40 GB NVMe | 20 TB |
| Hetzner CAX11 (ARM, EU) | €6.49 | 2 Ampere / 4 GB | 40 GB NVMe | 20 TB |
| DigitalOcean Basic | $4 | 1 shared / 512 MB | 10 GB SSD | 500 GiB |
| DigitalOcean Basic | $6 | 1 shared / 1 GB | 25 GB SSD | 1 TB |
| Vultr Regular Performance | $5 | 1 shared / 1 GB | 25 GB SSD | 1 TB |
| Vultr High Performance | $6 | 1 AMD / 1 GB | 25 GB NVMe | 2 TB |
| Linode Nanode 1 GB | $5 | 1 shared / 1 GB | 25 GB SSD | 1 TB |
| Vultr Regular, IPv6-only | $2.50 | 1 shared / 512 MB | 10 GB SSD | 0.5 TB |

Three things jump out. First, Hetzner's €5.99 (call it $7 at recent exchange rates, and remember EU prices exclude VAT) buys double the RAM and up to twenty times the transfer of any five-dollar US plan; Hetzner's price-cap billing means the meter can run hourly, but the bill never exceeds the printed monthly ceiling. Second, the American trio has held the $5 = 1 GB + 1 TB anchor for nearly a decade — DigitalOcean pricing, Vultr pricing and Linode pricing barely move at this tier, which is exactly why bandwidth, not compute, became the competitive battleground. Third, the cheapest sticker price in the table, Vultr's $2.50 IPv6-only instance, is a niche pick: it ships without an IPv4 address (adding one brings it to $3.50), and plenty of corporate networks still route IPv6 badly.

Scale one rung up, to the class most production apps actually live in, and the gap widens rather than closes:

| Provider & plan | Price/mo | vCPU / RAM | Storage | Included transfer |
|---|---|---|---|---|
| Hetzner CX43 (EU) | €16.49 (~$19) | 8 shared / 16 GB | 160 GB NVMe | 20 TB |
| DigitalOcean Basic | $48 | 4 shared / 8 GB | 160 GB SSD | 5 TB |
| Vultr Regular Performance | $40 | 4 shared / 8 GB | 160 GB SSD | 4 TB |
| Linode 8 GB | $48 | 4 shared / 8 GB | 160 GB SSD | 5 TB |

At roughly $19 versus $40-48, Hetzner hands you double the cores, double the RAM and four times the included traffic. That is not a rounding error or a launch coupon — it is the structural result of running data centers in Falkenstein and Nuremberg, where land and power cost a fraction of what Ashburn or San Francisco cost. A solo operator running two or three mid-size VMs saves $300-700 a year on Hetzner pricing alone. Whether that saving survives contact with reality depends on what the next sections cover: geography, managed services, and egress.

## Bandwidth is the real invoice: egress overage math

Sticker prices sell servers; bandwidth bills run them. The four providers charge for outbound traffic beyond the included pool at wildly different rates:

| Provider | Included (entry plan) | Overage rate | Overage per TB |
|---|---|---|---|
| Hetzner (EU) | 20 TB | €1.00/TB | ~$1.15 |
| DigitalOcean | 1 TB, pooled team-wide | $0.01/GiB | ~$10.24 |
| Vultr | 0.5-2 TB per instance | $0.01/GB | ~$10.24 |
| Linode (Akamai) | 1 TB, pooled account-wide | $0.005/GB | ~$5.12 |

For context, AWS charges roughly $90 per TB beyond its negligible free allowance, which is how "egress fees" became a meme. Against that backdrop, Linode's 2026 cut to $0.005/GB is genuinely aggressive — Akamai now advertises the lowest transfer costs in its market segment, and against DO and Vultr the claim holds. But Hetzner's €1/TB still clears the field at five to ten times cheaper than the American median.

The ROI math for a traffic-heavy month — say your API or download server moves 30 TB:

| Provider & plan | Included | Bill for 30 TB outbound | Effective monthly cost |
|---|---|---|---|
| Hetzner CX23 | 20 TB | €10 (10 TB over × €1) | ~€16 (~$18) |
| Linode Nanode | 1 TB | $148.50 (29 TB × $0.005) | ~$153.50 |
| Vultr $5 plan | 1 TB | $290 (29 TB × $0.01) | ~$295 |
| DigitalOcean $6 Droplet | 1 TB | ~$297 (29 TB × $0.01/GiB) | ~$303 |

Two footnotes matter here. DigitalOcean and Linode pool transfer across your whole account, so multiple servers share the allowance; Vultr meters per instance. And Hetzner's US locations play a different game entirely — CPX servers in Ashburn and Hillsboro include just 1-4 TB of traffic, and Singapore, opened in 2024, carries the smallest pools of all — so the 20 TB figure is an EU privilege, not a global guarantee. If your month regularly exceeds 30 TB, stop serving large static files from a VM and put the object storage layer in front; we compared S3, Cloudflare R2, Backblaze B2 and Wasabi on exactly that problem in our [object storage pricing breakdown](/articles/best-object-storage-pricing-2026-aws-s3-vs-cloudflare-r2-vs-backblaze-b2-vs-wasabi). And for accounts running many servers, a dedicated cost tool pays for itself — we compared CloudZero, Finout, Vantage and Kubecost in our [cloud cost management roundup](/articles/best-cloud-cost-management-tools-2026-cloudzero-vs-finout-vs-vantage-vs-kubecost).

## Hetzner vs DigitalOcean: specs versus the managed ecosystem

The Hetzner vs DigitalOcean question is not really about the VMs — it is about everything wrapped around them.

Hetzner wins the raw-hardware comparison almost everywhere: more RAM per euro, 20 TB of included EU traffic, snapshots at €0.012/GB-month, and price-cap billing where your worst-case monthly bill is printed on the product page. Its 2026 restructure added a 99.9% SLA and 24/7 email support, and the one-click app catalog — Docker, WordPress, Nextcloud, GitLab, Coolify — narrows the "it's just a bare Linux box" objection. Data centers sit in Falkenstein, Nuremberg, Helsinki, Hillsboro (Oregon), Ashburn (Virginia) and Singapore. What Hetzner does not have: a managed database, a managed Redis, an App-Platform-style PaaS, or any Asian region beyond one in Singapore. Support runs email-first, and the docs assume you already know Linux. You are trading operational convenience for a materially cheaper invoice.

DigitalOcean is the opposite trade. Fifteen regions from New York to Sydney and Bangalore, a managed Postgres/MySQL/Redis/Kafka lineup, DOKS-managed Kubernetes, App Platform for push-to-deploy, Spaces for object storage, and one of the best documentation libraries in the industry — DO's real product is not the Droplet, it is the 15-minute path from git push to running production. DigitalOcean pricing is the most predictable of the four (per-second billing arrived January 1, 2026 with a 60-second minimum, which makes short-lived CI and batch work almost free), but every managed add-on resets the clock on value: backups cost 20% of the Droplet price weekly or 30% daily, snapshots run $0.06/GB/month, and managed databases start well above an equivalent self-managed Droplet.

If you came looking for a DigitalOcean alternative because of bill shock, egress is usually the culprit — check the overage table above before you migrate. And if you are moving workloads between providers, our [Terraform automation platform comparison](/articles/best-terraform-automation-platforms-2026-spacelift-vs-env0-vs-scalr-vs-atlantis) covers the tooling that makes the migration survivable. Whichever side of the Hetzner vs DigitalOcean split you land on, pair the deployment with real alerting; our [uptime monitoring tools comparison](/articles/best-uptime-monitoring-tools-2026-better-stack-vs-uptimerobot-vs-checkly-vs-pingdom) covers the four options worth shortlisting.

## Vultr vs Hetzner: location coverage and the $2.50 floor

Vultr vs Hetzner is geography versus price. Vultr operates 32 cloud locations — Johannesburg, São Paulo, Santiago, Tel Aviv, Seoul, Osaka, Mexico City, Delhi, Mumbai and the usual US/EU/Japan set. Hetzner has six. If your users live in Lagos, São Paulo or Johannesburg, Vultr is the only provider in this comparison with a local region, and 80 milliseconds of latency is worth more than any RAM-per-euro table.

On specs, the comparison tightens. Vultr's $6 High Performance plan (AMD EPYC, NVMe, 2 TB) beats DigitalOcean's $6 Basic on bandwidth and disk class, and its $20 mid-tier (2 vCPU / 4 GB / 80 GB / 3 TB) undercuts DO's equivalent $24 plan while trailing Hetzner by a wide margin. The 2026 addition worth knowing about is VX1, Vultr's new dedicated-CPU enterprise line with up to 50 Gbps networking and billing on actual hours used rather than a 672-hour cap — a sign the company is chasing bigger customers, not cheaper ones.

The verdict: choose Vultr when geography is the binding constraint, or when you need many small regional edge nodes; choose Hetzner when it is not. A single-region product with European users has no reason to pay Vultr's premium for the same specification.

## Linode pricing in 2026: the Akamai trade

Akamai bought Linode in 2022 and has been repositioning it as the Akamai Connected Cloud — enterprise cloud with developer DNA. Linode pricing tells the story of that pivot: the $5 Nanode (1 vCPU, 1 GB, 25 GB, 1 TB) has not moved in roughly a decade and remains the museum piece of the entry tier, while the 2 GB plan at $12 is comfortably the worst value-per-GB in this comparison — you could run Hetzner's 4 GB CX23 for half the money.

What the Akamai trade actually buys: current-generation dedicated AMD EPYC instances (the G8 line, from $0.074/hour), LKE Kubernetes with no per-cluster control-plane fee, managed MySQL, PostgreSQL and Valkey, the $0.005/GB egress overage (the cheapest US overage rate of the four), and integration with Akamai's edge network spanning 130+ countries. There is also a managed-service offering at $100 per instance per month — a line item that says plainly who Linode now courts. For an indie developer it is priced out of range; for a mid-market team that wants Akamai's security and CDN stack one API call away, it is a different story.

The honest framing: Linode stopped trying to win the low end years ago. The Nanode survives as a cheap US sandbox, the overage rate is now genuinely competitive, and everything above 2 GB exists for teams buying the Akamai bundle, not the VM.

## Which VPS provider should you pick: four honest verdicts

| Provider | Pick it when | Walk away when | 3-year cost signal |
|---|---|---|---|
| Hetzner | EU or global users, self-managed stack, bandwidth-heavy apps | You need managed databases, Sydney or Mumbai regions, or hands-on support | ~55-65% cheaper than the US trio on equivalent specs |
| DigitalOcean | Fast-moving SaaS, managed DB and PaaS, 15-region reach | Traffic above ~5 TB/month on entry plans, or every dollar counts | Predictable base; add-ons inflate the bill 30-60% |
| Vultr | Users in emerging markets, many small edge regions, GPU options | A single-region EU product chasing the lowest price | Mid-pack specs, premium pricing in far-flung locations |
| Linode (Akamai) | Enterprise adjacency to Akamai CDN and security, high US egress | Indie budgets at the low end | $5 floor, but $100/month managed ceiling signals its audience |

VPS hosting is one of the few infrastructure markets where the cheapest option and the best option are usually the same answer, and for a majority of solo developers and small teams that answer is Hetzner. The exceptions are real, though: the managed-ecosystem buyer lands on DigitalOcean, the geography-constrained buyer lands on Vultr, and the enterprise buyer signs with Linode with eyes open.

## Frequently Asked Questions

### Is Hetzner cheaper than DigitalOcean?

Yes — usually by a wide margin on identical workloads. The entry-tier Hetzner CX23 costs €5.99 (about $7) and includes 4 GB of RAM and 20 TB of EU traffic; DigitalOcean's nearest spec match costs $24-48 with 4-8 GB and 4-5 TB. Hetzner's 2026 price restructure narrowed the gap by about a third, and its US data centers include far less traffic (1-4 TB) than its EU ones, so the savings shrink for US deployments — but they do not disappear.

### What is the cheapest VPS option in 2026?

Vultr's $2.50 IPv6-only instance is the cheapest paid VM among major providers, but it ships without IPv4 (that adds $1). The cheapest practical full-featured plan is the $5 tier shared by Vultr Regular and Linode's Nanode: 1 vCPU, 1 GB RAM, 25 GB storage, 1 TB transfer. If you can use ARM, Hetzner's CAX11 at €6.49 delivers 4 GB of RAM and 20 TB of traffic — the best absolute value in the tier despite not being the lowest number on the price tag.

### Do Hetzner US servers include less traffic than EU servers?

Yes. Hetzner EU locations (Falkenstein, Nuremberg, Helsinki) include 20 TB per month with €1/TB overage. US locations (Ashburn, Hillsboro) include 1-4 TB depending on plan type, and Singapore includes the smallest pools of all — as little as 0.5 TB on some plans. If your traffic profile is heavy, the EU locations remain dramatically better value.

### Which is the best VPS for developers shipping side projects?

For most: Hetzner's CX23 or CAX11 if you are comfortable managing a Linux box — nothing else comes close per dollar. If you would rather never touch a firewall config, DigitalOcean's $6 Droplet plus its tutorials and one-click marketplace will get a side project live faster, and team-level transfer pooling forgives experimentation. Both stay under $10/month including backups if you skip the managed add-ons.

### Does DigitalOcean pricing include bandwidth, or will overage bills hit me?

Every Droplet plan includes transfer — from 500 GiB on the $4 tier up to 11 TB on larger plans — pooled across your whole team account. Beyond the pool, outbound traffic bills at $0.01/GiB, and inbound is always free. A side project that pushes 2 TB in a month on a $6 plan would owe roughly $10 in overage: visible in the billing dashboard's projection tool, and rarely a surprise if you glance at it weekly.

## Bottom line

VPS hosting in 2026 splits cleanly along one question: are you buying hardware or an operating environment? Hetzner sells hardware at prices the US market stopped offering years ago — 4 GB and 20 TB for €5.99, a 99.9% SLA, and invoices with a printed ceiling — and accepts that you will run your own databases and read your own logs. DigitalOcean, Vultr and Linode sell different bundles around thinner VMs: managed services and 15 regions, 32 locations and edge reach, and Akamai's enterprise stack respectively. The arithmetic in this article will not stay current forever — Hetzner restructured its lineup this year, Linode cut its overage rate in half, and DigitalOcean moved to per-second billing in January — so treat these tables as the November 2026 snapshot they are. Price your workload, count your terabytes, and pick the trade-off you can live with. The $2 difference per month was never the decision; what the $2 does not include is.
