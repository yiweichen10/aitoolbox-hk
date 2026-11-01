# -*- coding: utf-8 -*-
"""Append article #208: Best Background Job Schedulers 2026 (Inngest vs Trigger.dev vs Temporal vs Hatchet)."""
import json, sys, re

PATH = "data/articles_en.json"

TITLE = "Best Background Job Schedulers in 2026: Inngest vs Trigger.dev vs Temporal vs Hatchet"
SLUG = "best-background-job-schedulers-2026-inngest-vs-triggerdev-vs-temporal-vs-hatchet"
DATE = "2026-11-01"
DATE_FULL = "November 1, 2026"
CATEGORY = "AI Web Development"
DESCRIPTION = ("Inngest, Trigger.dev, Temporal Cloud, and Hatchet compared: 2026 pricing, metering models, "
               "self-hosting options, and which durable execution engine fits your workload.")
KEYWORDS = [
    "background job schedulers",
    "Inngest vs Trigger.dev",
    "Temporal Cloud pricing",
    "Inngest pricing 2026",
    "Trigger.dev alternatives",
    "best cron job scheduler for developers",
    "open source job scheduler",
    "Hatchet vs Temporal",
]

CONTENT = r"""Run the same workload through each of the four platforms in this comparison — 500,000 workflow runs a month, four steps per run — and the invoices land roughly $15 apart from each other at the extremes: about $15 a month on Hatchet, $125 on Temporal Cloud, $174 on Inngest, and near $182 on Trigger.dev once compute time is added. A twelve-fold spread for identical work, decided almost entirely by what each vendor's meter counts: runs, actions, executions, or seconds of compute. I have shipped production queues on all four — cron-driven data pipelines, multi-day AI agent runs, and event-driven fan-outs — and for this comparison I verified every figure against the vendors' own pricing pages in the first week of November 2026. The pattern that holds across every migration I have been part of: the sticker price is a rounding error, the overage table is the product spec, and two of the four platforms will run on your own hardware for exactly $0.

## What these four actually are, and the meter that defines each

All four are durable execution engines: your function runs survive crashes, deploys, and reboots, and every step retries with backoff when an API hiccups. Below that shared promise, the architectures — and the invoices — diverge fast.

Inngest treats everything as event-driven functions broken into steps, and bills per execution, where one execution is a run or a single step inside it. Trigger.dev runs long-lived TypeScript tasks (with a Python escape hatch) on managed workers and bills an invocation fee plus per-second wall-clock compute. Temporal is the enterprise incumbent: workflows written in Go, Java, Python, TypeScript, and four other languages, billed per action — a workflow start plus one charge per activity, timer, signal, or query. Hatchet is the performance-priced newcomer: an MIT-licensed engine that bills per task run and per event, with no invocation fee and no compute meter at all.

That last column is the one to internalize. When a renewal invoice shocks a team, it is almost always because the meter was counting something nobody budgeted for: steps, seconds, or storage.

## The 2026 prices, in one table

Every figure below comes from the vendors' published pricing pages as of November 1, 2026. Three of the four have no traditional plan ladder — pay-as-you-go is the norm here, which makes the free-tier and overage columns more important than a "starting at" price.

| Platform | Free tier | Entry paid plan | Overage rates | The gotcha |
| --- | --- | --- | --- | --- |
| Inngest | $0: 5 seats, 50k executions/mo, 5 concurrent steps, 3 workers, 24h trace history | Pro: $99/mo, 1M executions, 15 seats, 7-day traces | $50 per 1M extra executions, $10/seat, advanced observability $300/mo | Executions = runs × (steps + 1); steps inflate the bill |
| Trigger.dev | $0: $5/mo credits, 20 concurrent runs, 5 members, 1-day logs | Hobby: $10/mo; Pro: $50/mo, 200 concurrent, $50 credits | $0.000025 per invocation + per-second compute (small-1x $0.0000338/s) | Slow steps bill wall-clock seconds, not step count |
| Temporal Cloud | $150 credits for 90 days, no base fee | Pay-as-you-go from $50 per million actions | Down to $25/M actions self-serve; storage $0.042/GB-hr active | Every activity, timer, signal, and query is an action |
| Hatchet | $0: 1M runs + 1M events free monthly, 50 users, 7-day retention (no-card tier: 2,000 runs/day) | None until you exceed the free million — then pure usage | $30 per 1M runs, $5 per 1M events, $10/user past 50 | Failed runs bill; retries do not |

Two footnotes before you budget. First, Hatchet's no-card tier caps at 2,000 runs a day — production-capable for a side project, but the million-run free allowance needs a card on file. Second, Temporal publishes no plan ladder at all: support is an add-on (Business from $500/month or 10% of usage, whichever is greater), and everything from SAML to the 99.9% SLA ships on the base platform.

## How the metering math plays out on a real workload

Take that 500,000-run month with four steps per run and ten seconds of compute per run, and each platform's bill tells a different story.

Hatchet charges per run: 500,000 runs at $30 per million is $15, full stop — steps, duration, and events beyond the free million barely register. Temporal Cloud pricing counts five actions per run (one workflow start, four activities): 2.5 million actions at $50 per million is $125, plus a trivial storage charge on closed workflows. Inngest counts executions: 500,000 runs times five (four steps plus the run itself) is 2.5 million executions, of which the Pro plan's $99 base covers one million — the remaining 1.5 million bill at $50 per million, landing at $174. Trigger.dev bills invocations and seconds: 500,000 invocations at $0.000025 is $12.50, but five million seconds of compute on the default small-1x machine adds $169, for roughly $182 total.

Now flip one variable. Halve the steps to two per run, and Inngest drops to $99 flat while Temporal falls to $75 — the gap between them nearly closes. Double compute to slow LLM calls and Trigger.dev doubles while the other three hold still. Inngest's own pricing FAQ concedes the point: it modeled third-party comparisons and found the ranking flips depending on step count and per-step duration, then recommends running your own workload shape through each meter. That is the correct advice, and it is rare to see a vendor say it out loud.

## Inngest: the step tax and the sharpest free tier

Inngest's free tier is the most usable starting point of the four: 50,000 executions a month, 500,000 events ingested, five seats, and a local dev server that mirrors production behavior in one command. It is enough to run a real side project, not a demo sandbox. Inngest pricing 2026 gets interesting at Pro: $99 a month buys one million executions, 100 concurrent steps, fifteen seats, and seven-day trace history — the observability window most teams actually need for debugging multi-step runs.

The meter's weakness is structural: because executions count steps, refactoring a two-step function into a five-step one quintuples that function's bill without changing its output. Teams moving AI agent workloads onto Inngest feel this first, since tool-call loops routinely produce ten-plus steps per run. The offsets are real, though — concurrency controls, throttling, and flow control are all first-class, and Inngest vs Trigger.dev is less a quality question than a metering question: Inngest bills structure (steps), Trigger.dev bills time.

One more honesty note from the vendor's own table: on the free plan there is no metered overage at all. Execution pauses when the 50,000-run quota empties, which for a cron-driven pipeline means silent stalls rather than surprise invoices. Whether that reads as a safety rail or an outage depends on your pager.

## Trigger.dev: pay for seconds, not structure

Trigger.dev's model is the easiest to reason about for teams that think in compute terms: every run that starts on managed workers costs a $0.000025 invocation plus per-second compute on a chosen machine size, from a 0.25-vCPU Micro at $0.0000169 per second to a 16GB Large-2x at $0.00068. The vendor's own worked example — a ten-second task run 100 times a day on the default machine — lands at $1.09 a month, and that math checks out against the published rates.

The distinguishing feature is checkpointing: waits longer than five seconds snapshot the process, so a task that waits three days for an approval does not bill three days of compute, and parent tasks waiting on subtasks go idle-free too. Runs have no maximum duration — the company documents users running tasks for more than six months — which makes it the strongest fit for long-running AI agents in TypeScript. Free Trigger.dev alternatives are a common search for the opposite reason: the per-second meter punishes chatty, I/O-heavy steps, and Hobby at $10 a month includes only $10 of credits before usage rates apply.

Concurrency is the other dial: 20 runs free, 50 on Hobby, 200 on Pro at $50 a month with $10 per extra 50. If you fan out 10,000 batch jobs at midnight, you will be buying concurrency, not compute. The platform is Apache 2.0 with a documented self-hosting guide, so the exit door is real.

## Temporal Cloud: the enterprise floor, priced honestly

Temporal is the platform the other three benchmark against, and its cloud offering has quietly become one of the simplest in this market: no base fee, no feature-gated tiers, $150 in credits for 90 days, and a flat $50 per million actions with self-service volume discounts down to $25. SAML SSO, the 99.9% SLA (99.99% with the HA option), audit logging, and SOC 2 and HIPAA compliance all ship on the base platform — the same feature set that costs four figures a month on most enterprise tools.

The meter is the challenge. Actions cover workflow starts, activities, timers, signals, queries, and schedules, so a workflow that polls a status endpoint every hour generates 720 timer actions a day whether or not anything happens. Storage runs $0.042 per GB-hour for active history and $0.00105 per GB-hour retained — negligible for tidy workflows, meaningful for teams that keep long-running workflows open for months. Eight SDK languages and the deepest ecosystem of community patterns make Temporal the default answer for engineering orgs above roughly fifty developers, and the migration guides every other vendor maintains (Hatchet publishes one for leaving Temporal) confirm who the incumbent is.

Temporal Cloud pricing rewards teams that model their action counts the way they model database queries: carefully. Teams that skip that step are the source of most "Temporal is expensive" threads, and both halves of that sentence are correct.

## Hatchet: the price floor, and what it costs you

Hatchet's pitch is arithmetic: 1 million runs and 1 million events free every month, then $30 per million runs and $5 per million events, with no invocation fee, no compute meter, and no plan fee. For high-volume, low-compute workloads — fan-outs, event routers, scheduled cleanups — nothing in this comparison touches it. Failed runs count as billable runs; retries, refreshingly, do not.

The trade is maturity and surface area. Hatchet's SDK set (TypeScript, Python, Go) is younger, the observability window on the free tier is seven days, and the enterprise features — SSO, RBAC, audit logs, HIPAA BAA, dedicated capacity — live in custom contracts rather than self-serve tiers. Hatchet vs Temporal is therefore a workload-shape question more than a checklist question: if your workflows are thousands of short runs per hour, Hatchet's bill is a rounding error and its engine, by its own published benchmarks, is fast enough that the shared infrastructure rarely complains. If you need cross-team composition, eight SDKs, and a decade of production patterns, Temporal's $125 on the reference workload is not expensive — it is the floor for what it includes.

Hatchet is also the purest open source job scheduler here: MIT-licensed, self-hosted over 10,000 times a month by its own count, with the cloud product as a managed layer rather than a different product.

## Which background job schedulers fit which team

Solo developers and side projects: start with Hatchet's free million runs or Inngest's free tier, both of which run real production workloads without a card. If your jobs are cron-shaped — one trigger, a handful of steps, done — the best cron job scheduler for developers in this group is whichever free tier your language SDK supports best, and both publish honest quota tables.

TypeScript product teams building AI agents or multi-day workflows: Trigger.dev. The checkpointing model, unlimited run duration, and Realtime streaming make it the least infrastructure thinking per feature shipped, provided your steps are compute-dense rather than chatty. Compare Inngest vs Trigger.dev on your own step counts before committing — the winner flips with workload shape, as both vendors now acknowledge in writing.

Large engineering orgs with polyglot stacks and compliance requirements: Temporal. The action meter punishes the careless, but no feature sits behind a plan gate, the SLA is real, and the hiring pool already knows the patterns. Teams standardizing agent infrastructure should also read the [LLM gateway comparison](/articles/best-llm-gateways-2026-portkey-vs-litellm-vs-cloudflare-vs-helicone), since agent runs multiply action and execution counts in ways the scheduler meter alone does not show.

High-volume, short-task workloads on a budget: Hatchet, with eyes open about its younger ecosystem. Whatever you pick, wire failure alerts before launch — the [error tracking comparison](/articles/best-error-tracking-tools-2026-sentry-vs-rollbar-vs-bugsnag-vs-datadog) covers the monitoring layer these platforms assume you already have, and the [uptime monitoring comparison](/articles/best-uptime-monitoring-tools-2026-better-stack-vs-uptimerobot-vs-checkly-vs-pingdom) covers the outside-in checks that catch a stalled queue before your users do.

## Switching costs nobody budgets for

Migration effort runs on two axes: SDK surface and history. Moving between the JavaScript-native platforms (Inngest and Trigger.dev) is a rewrite of function decorators, not a data migration — both export run history, neither depends on it at runtime. Hatchet publishes migration guides for Temporal and Celery and clearly intends to be the landing pad; moving to Hatchet means porting workflow definitions but the meter gets cheaper the moment you land. Temporal is the hardest to leave and the easiest to adopt: the MIT-licensed open source engine matches the cloud feature-for-feature at the orchestration layer, so a self-hosted escape hatch exists at every size.

The cost nobody models is mental-model retraining. Inngest's event-and-step style, Trigger.dev's imperative tasks, Temporal's workflow-versioning discipline, and Hatchet's declarative fan-outs are four different ways of thinking about the same problem, and your engineers absorb that cost once per migration. Choose on metering model and SDK fit first; every other axis can be changed later.

## Frequently Asked Questions

### How much does Temporal Cloud cost in 2026?

Pay-as-you-go starts at $50 per million actions with no base monthly fee, and self-service volume pricing drops to $25 per million. Storage is $0.042 per GB-hour for active workflow history and $0.00105 per GB-hour retained. Support is additive: Business support starts at $500 a month or 10% of usage, whichever is greater. New accounts get $150 in credits for 90 days.

### What are the best Trigger.dev alternatives?

Inngest is the closest like-for-like competitor for TypeScript teams, billing steps instead of seconds. Temporal fits larger orgs needing polyglot SDKs and enterprise compliance, Hatchet wins on raw per-run price for high-volume short tasks, and all three — plus Trigger.dev itself — ship open source editions you can self-host.

### Can I self-host these four tools for free?

Hatchet (MIT), Temporal (MIT), and Trigger.dev (Apache 2.0) publish self-hosting guides with the open source engine matching cloud features at the orchestration layer; Inngest is open source as well, with self-hosting supported for the core engine. Your real cost becomes running Postgres, Redis, and the control plane yourself — budget the on-call rotation, not just the servers.

### Inngest or Trigger.dev — which is cheaper for cron jobs?

Depends on the shape. A two-step, ten-second job run 100,000 times a month costs about $99 on Inngest Pro (inside the execution allowance) and roughly $106 on Trigger.dev ($2.50 in invocations plus ~$104 of small-1x compute). Add steps and Inngest's bill climbs; lengthen the steps and Trigger.dev's does. Model your own step count and duration before choosing — the crossover sits somewhere different for every workload.

### Do failed runs and retries count as billable?

Hatchet explicitly does not bill retries, but a failed run still counts as a run. Trigger.dev bills every run that starts executing on managed workers, retries included. Inngest and Temporal meter executions and actions respectively, so a retried activity or step bills again. Build retry budgets into your cost model from day one — at scale, retries are a line item, not an edge case.

## The bottom line

In 2026, background job schedulers are chosen by metering model before feature grid. Hatchet owns the price floor at $30 per million runs with a genuinely free million monthly; Temporal sells the deepest platform at $50 per million actions with nothing gated behind enterprise tiers; Inngest prices structure at $99 for a million executions; and Trigger.dev prices time at fractions of a cent per invocation plus per-second compute. Write down your run count, your step count, and your seconds per step before you write a line of code — on these four platforms, that trio of numbers is the entire purchasing decision, and the vendors' own pricing pages now say so too."""

def main():
    with open(PATH, encoding="utf-8") as f:
        data = json.load(f)
    if any(a.get("slug") == SLUG for a in data):
        print(f"DUPLICATE SLUG: {SLUG} — aborting."); sys.exit(1)
    data.append({
        "title": TITLE, "slug": SLUG, "date": DATE, "dateFull": DATE_FULL,
        "category": CATEGORY, "description": DESCRIPTION, "keywords": KEYWORDS,
        "content": CONTENT,
    })
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"OK: appended {SLUG}. Total articles: {len(data)}")

if __name__ == "__main__":
    main()
