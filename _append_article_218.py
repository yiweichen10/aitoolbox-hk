# -*- coding: utf-8 -*-
"""Append article #218: Best Managed Kubernetes 2026 (EKS vs GKE vs AKS vs DOKS)."""
import json

ARTICLE = {
    "title": "Best Managed Kubernetes in 2026: EKS vs GKE vs AKS vs DOKS Pricing Compared",
    "slug": "best-managed-kubernetes-2026-eks-vs-gke-vs-aks-vs-doks-pricing-compared",
    "date": "2026-11-11",
    "dateFull": "November 11, 2026",
    "category": "AI Infrastructure",
    "description": "EKS vs GKE vs AKS vs DOKS on November 2026 list prices: $73 control planes, the $438 extended-support trap, per-pod Autopilot billing, and worked monthly bills for the same 3-node cluster.",
    "keywords": [
        "managed Kubernetes",
        "Amazon EKS pricing",
        "GKE pricing",
        "AKS pricing",
        "DOKS pricing",
        "DigitalOcean Kubernetes",
        "EKS vs GKE",
        "Kubernetes control plane cost",
        "cheapest Kubernetes hosting",
        "GKE Autopilot pricing",
        "Kubernetes extended support fee",
    ],
    "content": """Nearly 90% of Kubernetes users now run their clusters on a cloud-managed service, up from roughly 70% in 2020, according to CNCF's cloud native survey — and the fee for that privilege ranges from $0 to $73 a month before a single worker node exists. The control plane is the smallest line on the bill and the one teams still get wrong: leave an EKS cluster on a Kubernetes version past its 14-month standard support window, and AWS bills $438 a month for it — six times the normal rate — until somebody runs the upgrade. This guide compares Amazon EKS, Google GKE, Microsoft AKS, and DigitalOcean DOKS on list prices pulled from each vendor's pricing pages in November 2026: control-plane fees, node rates, per-pod Autopilot billing, bandwidth, and the version-support fees that quietly multiply across a fleet. On managed Kubernetes pricing, the short version: AKS is free without an SLA, GKE makes one zonal cluster free per billing account, EKS charges $73 for every cluster, and DOKS charges nothing for the control plane while selling the cheapest nodes of the four.

## Managed Kubernetes Control Plane Cost: $0 to $73 a Month

All four vendors run the control plane for you — API server, etcd, scheduler. What they charge for it differs more than any other line item.

Amazon EKS charges $0.10 per cluster per hour, about $73 a month, with no free tier and no discount for running many clusters. The fee applies to every cluster in every region. EKS also sells a Provisioned Control Plane for clusters that need guaranteed burst capacity: tiers run from XL at $1.65 per hour to 8XL at $13.90 per hour, which makes a single top-tier cluster cost about $10,147 a month before any worker node exists.

GKE pricing lands on the same $0.10 per cluster per hour, charged across Standard and Autopilot modes in one-second increments. Google offsets it with a free tier: $74.40 in monthly credits per billing account, enough to cover exactly one zonal or Autopilot cluster running full-time. Regional clusters don't qualify — a regional GKE cluster pays the full $73.

AKS pricing splits into three published tiers: Free (no cluster fee, no SLA, a 1,000-node ceiling, and Microsoft's own documentation steering anything past 10 nodes toward a paid tier), Standard at $73 per cluster per month with a financially backed 99.95% API-server SLA, and Premium at $438 per month, which adds two years of version support. A fourth mode, AKS Automatic, carries a $116.80 monthly hosted-component fee before compute surcharges.

DigitalOcean DOKS charges nothing for the control plane. The free stance covers a bandwidth allowance and a starter container registry too; an HA control plane add-on buys the 99.95% SLA.

| Platform | Standard control-plane fee | Free tier | Stale-version fee | Control-plane SLA |
|---|---|---|---|---|
| Amazon EKS | $0.10/cluster-hr (~$73/mo) | None | $0.60/cluster-hr, on by default | 99.95% |
| Google GKE | $0.10/cluster-hr (~$73/mo) | $74.40/mo credit = 1 zonal or Autopilot cluster | +$0.50/hr on Extended channel ($0.60 total) | 99.95% (Autopilot/regional), 99.5% (zonal) |
| Microsoft AKS | $0 (Free) / $73/mo (Standard) | Entire Free tier, no SLA | $438/mo Premium tier, opt-in only | None (Free), 99.95% (Standard) |
| DigitalOcean DOKS | $0 | Free control plane, bandwidth allowance, starter registry | No published extended-support fee | 99.95% with HA add-on |

The stale-version column deserves its own section, and gets one below.

## Node Pricing Is Where the Bill Actually Lives

Control-plane fees are trivia; nodes are where 85% of a healthy cluster's spend sits. On the standard small node — 2 vCPU, 4 GB — the four diverge immediately:

- AWS t3.medium (us-east-1): $0.0416 per hour, about $30.37 for a 730-hour month.
- GCP e2-medium (us-central1): $0.0335 per hour, about $24.46.
- Azure B2s (East US): $0.0416 per hour, about $30.37.
- DOKS s-2vcpu-4gb: $24 flat, with 4,000 GiB of outbound transfer included per node.

AWS and Azure also meter public IPv4 addresses (about $3.65 per node per month since 2024) and bill load balancers hourly plus per-gigabyte; DigitalOcean's load balancers start at $12 flat.

GKE Autopilot rebuilds the model: instead of nodes, you are billed per pod for what the pod requests. In us-central1 that is $0.0445 per vCPU-hour and $0.0049225 per GiB-hour of memory, rounded up to 0.25 vCPU and 1 GiB. Autopilot is the only managed Kubernetes mode that bills at pod level, which cuts two ways. A pod requesting 1 vCPU and 2 GiB costs about $39.67 a month with zero idle-node overhead — but every over-requested core is billed whether the container touches it or not. Spot pods drop the vCPU rate to $0.0133, roughly a 70% cut, for anything that tolerates eviction.

AKS Automatic stacks its own layer on VM prices: a $7.05 monthly surcharge per general-purpose vCPU. On a 2 vCPU node that is $14.10 — about 46% on top of a B2s — before the $116.80 hosted-component fee.

Worked example: one cluster, three 2 vCPU/4 GB nodes, zonal, 730 hours, excluding load balancers and disks (budget another $12-20 a month for a load balancer on any platform):

| Platform | Control plane | 3 × 2 vCPU / 4 GB nodes | Monthly total |
|---|---|---|---|
| Amazon EKS | $73.00 | $91.11 (t3.medium × 3) | $164.11 |
| GKE, zonal, free credit applied | $0.00 | $73.38 (e2-medium × 3) | $73.38 |
| GKE, regional | $73.00 | $73.38 | $146.38 |
| AKS Free tier | $0.00 | $91.11 (B2s × 3) | $91.11 |
| AKS Standard | $73.00 | $91.11 | $164.11 |
| DigitalOcean DOKS | $0.00 | $72.00 (s-2vcpu-4gb × 3) | $72.00 |

Three clusters instead of one? Multiply the control-plane column: EKS hits $219, AKS Standard $219, GKE $146 after its single free credit, DOKS still $0.

## The Bandwidth Line Item Nobody Budgets

Hyperscaler node prices exclude outbound traffic. AWS charges $0.09 per GB after 100 free GB, Azure about $0.087 after its own 100 GB allowance, and GCP's standard-tier egress runs roughly $0.085. DigitalOcean pools a per-node bandwidth allowance and charges $0.01/GiB beyond it.

DigitalOcean's own comparison table — vendor math, so weight it accordingly — prices one 4 GB node pushing 4 TB of monthly egress at $24 all-in on DO against $342 on AWS, $368 on GCP, and $399 on Azure. Discount the vendor's numbers by a third and the egress tail still outweighs the control-plane fee three to five times over on a chatty cluster.

EKS adds one more meter: traffic from nodes to the Kubernetes API counts as cross-AZ traffic at $0.01 per GB each way when nodes and control plane land in different zones. Fleet-scale teams have built entire cost dashboards just to explain that line.

When storage and transfer dominate the bill more than compute, the same per-gigabyte math applies to cluster backup targets — see the [object storage pricing comparison (S3 vs R2 vs B2 vs Wasabi)](/articles/best-object-storage-pricing-2026-aws-s3-vs-cloudflare-r2-vs-backblaze-b2-vs-wasabi).

## EKS vs GKE vs AKS: Which Cloud Wins on Total Cost

For a 100-vCPU fleet, one 2026 FinOps analysis puts the on-demand compute lines within about 20% of each other — $2,300 to $2,900 a month across the three hyperscalers. The tiebreakers are discounts, egress, and operational depth.

Pick EKS if you are all-in on AWS: IAM and ALB integration, Graviton nodes running 15-20% cheaper per vCPU than Intel equivalents, and the deepest managed add-on catalog of the three. On EKS vs GKE control-plane fees it is a tie; EKS loses on the extended-support trap and IPv4/egress metering and wins on ecosystem depth.

Pick GKE for Autopilot's per-pod billing on spiky or under-used workloads, or for the free zonal cluster as a dev environment. GKE's committed-use discounts cut compute 37% at one year and 55% at three, and Autopilot's 1-year flexible CUD drops the vCPU rate from $0.0445 to $0.0356.

Pick AKS if you are an Azure shop or run Windows containers — it is the only one of the three with first-class Windows node pools. The Free tier is genuinely free, but the moment finance wants a written SLA you are on Standard at the same $73 everyone else charges.

Pick DOKS for budget-constrained teams and invoices that read like receipts: free control planes at any cluster count, $24 nodes with bandwidth included, node pools that scale to zero when idle, and a short path from zero to a working cluster. The trade-off is a thinner managed add-on catalog and far fewer regions than the hyperscalers.

| If you... | Pick | Why | The catch |
|---|---|---|---|
| Run everything on AWS with IAM/RDS/S3 glue | EKS | Deepest AWS integration, Graviton price cuts, richest add-ons | Extended-support trap; IPv4 and egress metering |
| Have spiky or low-usage workloads | GKE Autopilot | Per-pod billing, no idle-node waste, 70% Spot cut | Over-requests bill directly; regional clusters lose the free credit |
| Are an Azure shop or need Windows nodes | AKS | Genuinely free tier, Windows node pools, single-vendor integration | SLA requires Standard ($73/mo); Premium LTS is $438/mo |
| Want flat, predictable invoices on a budget | DOKS | $0 control plane at any scale, $24 nodes with 4 TB egress included | Fewer regions, thinner managed add-on catalog |

If the workloads would honestly fit on plain VMs, the cheaper conversation is a [VPS comparison — three Hetzner nodes](/articles/best-vps-hosting-2026-hetzner-vs-digitalocean-vs-vultr-vs-linode) run a self-managed cluster for less than one hyperscaler control-plane fee.

## Don't Sleep on the Kubernetes Extended Support Fee

All three hyperscalers now price version staleness at the same rate. EKS standard support runs 14 months per version; after that the cluster bills $0.60 per hour — $438 a month — by default until you upgrade or the extended window closes and AWS force-upgrades it. GKE charges the identical $0.60 combined rate on its Extended channel once standard support lapses; clusters on the Rapid, Regular, and Stable channels upgrade automatically and never see the fee. AKS keeps versions patched for about a year and sells longer windows only through the $438 Premium tier. Two stale EKS clusters cost an extra $730 a month for the privilege of postponing an upgrade that gets harder the longer it waits. Set the EKS upgrade policy to STANDARD, stay on GKE's standard channels, and the fee never fires. Third-party support-calendar trackers put EKS 1.34 at the end of standard support on December 2, 2026 — clusters still sitting on 1.32 or 1.33 are already paying the six-times rate.

## Frequently Asked Questions

### How much does Amazon EKS cost per month?

Amazon EKS pricing starts at $73 a month for the control plane ($0.10 per hour) with no free tier. A minimal three-node cluster on t3.medium lands near $164 before load balancers, disks, IPv4 addresses, and egress. EKS Auto Mode adds roughly 12% on top of the EC2 bill for its management fee. And if the cluster's version slips past 14 months of standard support, the control plane bills $438 a month until you upgrade.

### Is GKE Autopilot cheaper than running your own nodes?

GKE Autopilot pricing bills $0.0445 per vCPU-hour plus $0.0049225 per GiB-hour against pod requests, so a pod asking for 1 vCPU and 2 GiB costs about $39.67 a month with no idle-node overhead. Standard mode bills about $24.46 per e2-medium node whether the pods use it or not. Third-party benchmarks put a well-packed Standard fleet 10-30% cheaper than Autopilot at steady state; under-used fleets flip the result. Buying the 1-year flexible CUD cuts the Autopilot vCPU rate to $0.0356 and narrows the gap further.

### What is the cheapest Kubernetes hosting option for small teams?

For one dev cluster, AKS Free and GKE's free zonal credit both get you a control plane for $0 — GKE with a 99.5% SLA, AKS with none. For production on a budget, DOKS pricing wins: three 2 vCPU/4 GB nodes cost $72 with bandwidth included, the control plane stays free at any cluster count, and load balancers start at $12. The trade is fewer regions and fewer managed extras.

### Do you pay for the control plane on AKS?

Only on Standard ($73 a month, backed by the 99.95% SLA) or Premium ($438 a month with two-year long-term support). The AKS Free tier charges nothing for the control plane — you pay for VMs, disks, and load balancers only — but carries no SLA and a 1,000-node ceiling, and Microsoft's documentation steers production clusters toward Standard. AKS Automatic starts at $116.80 a month for the hosted component before compute surcharges.

### What happens if you don't upgrade your Kubernetes version?

On EKS, the cluster auto-enters extended support at 14 months and bills $0.60 per hour — six times the standard rate — with no action needed to trigger the fee, only to stop it (set the upgrade policy to STANDARD). GKE bills the same combined $0.60 rate, but only on its Extended channel. AKS stops patching after roughly a year unless you have bought Premium LTS. DOKS publishes no extended-support fee; upgrades run through the console with maintenance windows. The fee buys security patches only — it does not make your Helm charts compatible, and the forced upgrade at the end of the window still arrives.

## Bottom Line

Managed Kubernetes pricing in 2026 is three bills pretending to be one: the control plane ($0-73 per cluster per month), the nodes ($24-30 each at the small end), and everything the landing pages omit — egress near $0.09 per GB, IPv4, cross-AZ chatter, and the $438-a-month stale-version tax all three hyperscalers now charge. On raw math, DOKS runs the same three-node dev cluster for $72 where EKS and AKS Standard land at $164 and GKE's free-credit cluster costs $73 but loses the credit on your second cluster. The hyperscalers earn their premium in regions, managed add-ons, and enterprise integration — pay it when you actually need those, not because a landing page equates Kubernetes with one vendor. Audit the version calendar before anything else; it is the only line item that can 6x itself overnight. And if no workload here truly needs an orchestrator, the [Heroku alternatives comparison](/articles/heroku-alternatives-2026-railway-vs-render-vs-flyio-pricing-compared) shows where plain PaaS hosting still wins."""
}

def main():
    path = "data/articles_en.json"
    with open(path, encoding="utf-8") as f:
        articles = json.load(f)

    slugs = {a["slug"] for a in articles}
    if ARTICLE["slug"] in slugs:
        raise SystemExit(f"ERROR: slug already exists: {ARTICLE['slug']}")

    articles.append(ARTICLE)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"OK appended '{ARTICLE['slug']}' — total articles: {len(articles)}")

if __name__ == "__main__":
    main()
