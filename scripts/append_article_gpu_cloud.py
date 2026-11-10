# -*- coding: utf-8 -*-
"""Append article: Best GPU Cloud Providers 2026 (RunPod vs Lambda vs Vast.ai vs CoreWeave)"""
import json, io, re

ART = {
    "title": "Best GPU Cloud Providers in 2026: RunPod vs Lambda vs Vast.ai vs CoreWeave",
    "slug": "best-gpu-cloud-providers-2026-runpod-vs-lambda-vs-vast-ai-vs-coreweave",
    "date": "2026-11-10",
    "dateFull": "November 10, 2026",
    "category": "AI Infrastructure",
    "description": "RunPod vs Lambda vs Vast.ai vs CoreWeave on November 2026 pricing: per-second billing, a 15% Lambda hike effective November 16, marketplace medians, $49.24 H100 nodes, and four worked bills for the same 96 GPU-hours.",
    "keywords": [
        "GPU cloud providers",
        "RunPod pricing",
        "Lambda Labs pricing",
        "Vast.ai pricing",
        "CoreWeave pricing",
        "H100 rental price",
        "cheapest GPU cloud",
        "serverless GPU inference",
        "GPU rental for fine-tuning",
        "RunPod vs Vast.ai",
        "interruptible GPU instances"
    ],
    "content": r"""An eight-GPU H100 node rents for $49.24 per hour on CoreWeave's published rate card and for about $18.64 per hour at the median rate on Vast.ai's marketplace. Same silicon, same NVIDIA HGX reference build, 2.6 times apart. Widen the lens and the spread gets worse: GetDeploying's index tracks 47 providers renting H100s anywhere from $0.61 to $14.90 per GPU-hour, and its B200 average has climbed roughly 31% since July 2025. The rental market moved backward in 2026 — one-year H100 contract rates rose about 40% between October 2025 and March 2026, according to SemiAnalysis, and Lambda Labs repriced upward again this month. Where you rent now matters as much as whether you rent. The four GPU cloud providers worth shortlisting — RunPod, Lambda, Vast.ai, and CoreWeave — no longer sell the same product: one bills seconds, one bills minutes on brand-new hardware, one runs a live market, and one sells nodes and contracts. Every price below is quoted the way the bill actually arrives, including the storage, bandwidth, and commitment terms that never make the headline hourly rate.

## What GPU cloud providers actually sell in 2026

Strip away the landing pages and each platform is a different meter with a GPU attached. RunPod sells per-second compute — pods for development and long-running jobs, serverless workers for inference — with no ingress or egress fees. Lambda sells minutes on HGX instances and fixed-price 1-Click Clusters sized in GPU counts. Vast.ai sells access to a marketplace where 20,000-plus GPUs across 40-plus data centers are priced by their hosts, in on-demand, interruptible, and reserved modes. CoreWeave sells eight-GPU nodes with published on-demand and spot rates, and reserved contracts behind them.

That difference in meter is why simple "per GPU-hour" comparisons mislead. A marketplace median includes hosts you would never put in production. A node price includes seven GPUs you may not need. A serverless rate includes the scheduler's right to cold-start you. The table below is the honest version: what each company sells, the closest thing it has to an H100 list price in November 2026, and the fee most likely to surprise you.

| Provider | What it actually sells | H100 anchor price, Nov 2026 | The fee that surprises people |
|---|---|---|---|
| RunPod | Per-second pods plus serverless workers | $2.89/hr PCIe, $3.99/hr SXM (Secure Cloud; Community from $1.99) | Stopped pods keep billing storage — volume disk doubles to $0.20/GB/mo |
| Lambda | Per-minute HGX instances and 1-Click Clusters | $2.49/hr PCIe (1x) today; $4.59/GPU-hr on 8x from Nov 16 | The November rate card itself: +15% on H100 and B200 |
| Vast.ai | A live market with host-set rates | From $2.27/hr, median $2.33 (H100 SXM) | Bandwidth billed per byte both ways, at host-set rates |
| CoreWeave | 8-GPU nodes, spot, and reserve contracts | $49.24/node/hr on-demand = $6.16/GPU-hr | 8-GPU minimum on every H100-class GPU; GH200 is the only single-GPU option |
| AWS P5 (reference) | 8-GPU P5 instances | About $6.88/GPU-hr normalized | Egress $0.09/GB after 10 TB per month |

## Where each vendor breaks

Four rate cards, four different failure modes. Each section below prices one vendor the way an invoice does — GPU line first, then everything that accrues around it.

### RunPod pricing: seconds now, storage later

RunPod pricing is the simplest on this list to model. Pods bill per second: H100 SXM runs $3.99 per hour on Secure Cloud and from $2.69 on Community Cloud, H100 PCIe is $2.89 (from $1.99), A100 80GB is $1.79 (from $1.19), L40S is $1.09, and RTX 4090 is $0.89. Serverless workers for API traffic run $5.39 per hour for H100-class GPUs, $2.72 for A100, and $1.34 for 4090-class, billed per second of active time — which is exactly what makes serverless GPU inference cheap for bursty or unattended workloads. There are no ingress or egress fees, and Secure Cloud carries SOC 2 Type II, HIPAA, and GDPR compliance, with a 99.99% uptime SLA at the enterprise tier.

The bill's second act is storage, and it does not stop when the GPU does. Container disk costs $0.10/GB/mo and vanishes when the pod stops. Volume disk costs $0.10/GB/mo while running and $0.20/GB/mo while stopped — a stopped pod holding a 500 GB volume pays $100 a month to do nothing. Network volumes run $0.07/GB/mo under 1 TB and $0.05 above it. Two more details worth knowing before you commit: savings plans are deprecated, so new commitments go through sales, and the default spend limit is $80 per hour across your account. Model the storage line, or the GPU line will flatter you.

### Lambda Labs pricing changed this month — upward

Lambda's self-serve rate card is mid-transition, and the direction is the story. The current GPU Cloud page lists a single H100 PCIe at $2.49 per hour and H100 SXM at $3.29, billed by the minute with no egress fees. A new card takes effect November 16, 2026: the 8x HGX H100 moves to $4.59 per GPU-hour, the 8x HGX B200 to $7.69, and the 8x HGX A100 80GB to $3.19. A third-party pricing tracker captured the same page on November 2 and November 9 and recorded the 8x H100 at $3.99 rising to $4.59 (+15%), B200 from $6.69 to $7.69 (+15%), and A100 80GB from $2.79 to $3.19 (+14%). Cluster pricing follows the same curve: 1-Click B200 Clusters list at $9.86 per GPU-hour for 16 GPUs and $8.87 at 256-plus, on terms from two weeks to a year.

The honest reading is that capacity sold out. Lambda rents recent HGX hardware with 22 TiB of local NVMe on 8-GPU nodes, a clean ML-first stack, and no egress fees — plus enough demand to reprice quarterly. Its own page tells budgeters to log in for current pricing, which is the tell. If you quoted a November project on October rates, check whether the number survives November 16.

### Vast.ai pricing: the market sets the number, and the number moves

Vast.ai pricing has no rate card because Vast is not the seller — its 20,000-plus hosts are, and they compete in real time. The live board shows the spread plainly: H100 SXM from $2.27 per hour with a median of $2.33, B200 from $5.50 with a median of $8.75 (a 59% gap on one card), RTX 4090 from $0.13. Three rental modes sit on the same inventory: on-demand with guaranteed uptime, interruptible GPU instances that typically run 50%-plus cheaper but can be preempted at any time, and reserved terms of one, three, or six months at up to 50% off.

The fees are host-set, and they are where "cheap" lives or dies. Bandwidth bills per byte in both directions at rates each host chooses. Storage keeps billing while an instance is stopped, until you delete it outright. Community reports note the platform commission baked into displayed rates, and billing quirks when hosts drop offline mid-job. Reliability spans home rigs to real data centers, so filter for verified hosts, checkpoint aggressively, and treat the median — not the minimum — as your planning number. RunPod vs Vast.ai is really a question about variance: Vast wins the sticker, RunPod wins the tail of the distribution.

### CoreWeave pricing: nodes, spot, and the 8-GPU minimum

CoreWeave pricing is now public, and it is deliberately the most expensive sticker here. CoreWeave is the slice of GPU cloud providers selling contracts: the published North America rate card exists to anchor negotiations for reserved capacity, where third-party analyses of the reserve page put discounts at 25% to 60% off on-demand. On demand, the HGX H100 node is $49.24 per hour ($6.155 per GPU-hour) with spot at $19.71 ($2.46 per GPU-hour); H200 is $50.44 per hour; B200 is $68.80 ($8.60 per GPU-hour) with spot at $34.11; A100 80GB is $21.60; L40S is $18.00. The only single-GPU rental is a GH200 at $6.50 per hour — every H100-class GPU carries an 8-GPU minimum.

What the premium buys is determinism: bare-metal single-tenant nodes, an InfiniBand fabric, and vendor-reported 51-52% model FLOPs utilization at 1,024-GPU scale against a 35-45% industry average. Those numbers matter on 70B-plus multi-node training runs and mean little on anything smaller. Even the inference option is priced accordingly — CoreWeave's per-GPU inference rate for H100 is $6.16, above RunPod's $5.39 serverless H100. Egress off CoreWeave's network is metered and storage bills separately, per third-party reconciliations of the card. Rent CoreWeave when the run is big enough that a 2.6x sticker is cheaper than a 20% utilization penalty; anything else is paying for capacity you cannot measure.

## The H100 rental price went up in 2026

The prevailing narrative says GPU rental gets cheaper every quarter as supply catches up with demand. The 2026 data says the opposite. GetDeploying's on-demand median across 53 tracked providers sat near $3.39 per GPU-hour in September. SemiAnalysis measured one-year contract rates rising from $1.70 to $2.35 per GPU-hour — about 40% — between October 2025 and March 2026, as capacity sold out. The B200 average is up roughly 31% since July 2025. Lambda repriced +15% this month. Meanwhile the hyperscalers never were the cheapest GPU cloud: normalized to a single GPU-hour, AWS's P5 family runs about $6.88, Google Cloud's A3 about $11.06, and Azure's 8-GPU ND H100 node about $12.29.

The exit ramps are interruptible capacity, spot windows, and longer commitments — and the buy-versus-rent floor keeps moving: a new H100 PCIe card runs about $31,000 and a full 8-GPU server $250,000 to $320,000, per CloudZero, so renting still wins unless utilization is high and steady for years. Sticker rates, meanwhile, are a minority of real bills. The [cloud cost management](/articles/best-cloud-cost-management-tools-2026-cloudzero-vs-finout-vs-vantage-vs-kubecost/) category exists because GPU line items routinely hide storage, egress, and idle capacity behind them — the same discipline applies here, at smaller scale.

## The fine-tuning math: 96 GPU-hours, four bills

GPU rental for fine-tuning is the cleanest way to compare meters, because the job is fixed. Take a LoRA fine-tune of Llama-3.1-8B on one 8x H100 SXM node for 12 hours — 96 GPU-hours of identical work, priced four ways.

| Provider (8x H100 SXM, 12 hours) | Rate used | Bill for 96 GPU-hours | How to pay less |
|---|---|---|---|
| RunPod Secure Cloud | $3.99/GPU-hr | $383.04 | Community Cloud from-price $2.69 drops it to $258.24 |
| Lambda (new card, Nov 16) | $4.59/GPU-hr | $440.64 | Current $3.99 holds it to $383.04 through Nov 15 |
| Vast.ai (median host) | $2.33/GPU-hr | $223.68 | From-price $2.27 lands at $217.92; add bandwidth |
| CoreWeave (node, on-demand) | $49.24/node-hr | $590.88 | Spot $19.71 is $236.52; reserved cuts 25-60% |

The same job costs $218 to $591 depending on where you click. Three modifiers move the real number. First, interruptions: Vast's interruptible tier would cut that bill another 50% or more if your checkpointing survives preemption. Second, breakeven: on RunPod, keeping a Secure Cloud pod warm at $3.99 beats paying serverless $5.39 only above roughly 74% utilization — Community pods, at $2.69, flip at 50% — so below those thresholds, per-second serverless billing is the cheaper meter. Third, the tail: heavy data movement on Vast costs bandwidth both ways, while RunPod and Lambda charge nothing for egress.

## How to choose without overpaying

Rules of thumb that survive contact with a real invoice. Bursty or unattended API traffic goes to RunPod serverless. Single-node experiments and checkpointed fine-tunes go to Vast.ai on-demand, interruptible if preemption is survivable. Steady weeks-long single-node runs go to RunPod pods or Lambda instances — whichever has capacity at your GPU class, with the November 16 Lambda repricing in mind. Multi-node training at 70B-plus goes to Lambda 1-Click Clusters or a CoreWeave reserved term, and the discount belongs in the contract, not in a slide. Compliance-bound inference goes to RunPod Secure Cloud or CoreWeave, both SOC 2 Type II.

Two disqualifiers worth stating plainly. If your workload calls hosted models rather than your own weights, you are shopping the wrong meter: [Groq](/tools/groq/) and [Replicate](/tools/replicate/) bill per token or per second of inference, and the [LLM gateway comparison](/articles/best-llm-gateways-2026-portkey-vs-litellm-vs-cloudflare-vs-helicone/) covers the routing layer that sits above them. And if nobody on the team reads storage and bandwidth lines, budget 20-30% above the GPU line regardless of provider — that gap is where GPU bills actually live.

## Frequently Asked Questions

### How much does an H100 cost per hour in 2026?

Between $0.61 and $14.90 per GPU-hour across 47 tracked providers, per GetDeploying. Realistic specialist anchors: Vast.ai's median of $2.33 for an SXM card, RunPod at $2.89 PCIe or $3.99 SXM on Secure Cloud, Lambda at $3.29 for a single SXM today and $4.59 per GPU-hour on 8-GPU nodes from November 16, and CoreWeave at $6.155 per GPU-hour on an 8-GPU node. Hyperscalers run $7 to $12.

### Which is the cheapest GPU cloud in 2026?

For on-demand data-center GPUs, the Vast.ai marketplace — its H100 SXM median near $2.33 undercuts every fixed-rate provider, and RunPod Community Cloud undercuts on specific cards such as H100 PCIe from $1.99. Interruptible modes cut 50%-plus further. But the cheapest sticker is not the cheapest bill: Vast bills bandwidth in both directions at host-set rates and storage while instances sit stopped, so heavy data movement can erase the GPU savings.

### Is RunPod or Vast.ai better for short fine-tuning runs?

Runs you can checkpoint and requeue belong on Vast.ai, usually interruptible, at 50%-plus savings. Runs that must finish unattended tonight belong on RunPod on-demand pods, which bill per second and cannot be preempted. The practical split: Vast for experiments, RunPod for deadlines — with Vast's verified-host filter and aggressive checkpointing either way.

### Why is Lambda raising GPU prices in November 2026?

Demand. One-year H100 contract rates rose roughly 40% between October 2025 and March 2026 as capacity sold out, per SemiAnalysis; the B200 average is up about 31% since July 2025; and Lambda passes that pressure to self-serve customers with a +15% move on 8-GPU H100 and B200 effective November 16, 2026. Lock current rates before the 16th or negotiate a reserved term.

### Can I rent a single H100 from CoreWeave?

No. The only single-GPU option is a GH200 at $6.50 per hour; every H100-class GPU is an 8-GPU node minimum. CoreWeave alternatives for single-GPU work: RunPod per-second pods from $2.89, Lambda single-GPU instances at $3.29 SXM or $2.49 PCIe, or the Vast.ai marketplace with H100s from $2.27.

## The Bottom Line

Among GPU cloud providers in 2026, the meter decides the bill more than the GPU does. RunPod owns seconds: $3.99 for an H100 SXM on Secure Cloud, no egress, storage that outlives stopped pods. Lambda owns minutes on new HGX hardware — at a rate that just moved 15% and takes effect November 16. Vast.ai owns the market: a $2.33 median with bandwidth and interruption risk attached. CoreWeave owns nodes and contracts: $49.24 an hour on demand, a quarter to six-tenths off if you commit. Pick by workload shape, price the storage and bandwidth lines before the GPU line, and re-quote every quarter — this market reprices faster than your architecture does."""
}

PATH = "data/articles_en.json"

with io.open(PATH, "r", encoding="utf-8") as f:
    arts = json.load(f)

# 防重复
if any(a["slug"] == ART["slug"] for a in arts):
    raise SystemExit("slug already exists, abort")

arts.append(ART)

with io.open(PATH, "w", encoding="utf-8") as f:
    json.dump(arts, f, ensure_ascii=False, indent=2)

# ---- 自检 ----
content = ART["content"]
words = len(re.findall(r"[A-Za-z0-9$%.]+", content))
pk = len(re.findall(r"GPU cloud providers", content))
banned = ["leverage","utilize","seamlessly","game-changing","empower","streamline","delve",
          "transformative","comprehensive","revolutionize","cutting-edge","as an AI","in conclusion"]
found = [b for b in banned if b.lower() in content.lower()]
tables = content.count("|---")
print("appended:", ART["slug"])
print("word count (approx):", words)
print("PK count:", pk)
print("banned found:", found)
print("tables:", tables)
print("total articles:", len(arts))
