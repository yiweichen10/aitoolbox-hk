# -*- coding: utf-8 -*-
"""Append article #209: Best Log Management Tools 2026 (Grafana Loki vs Better Stack vs Axiom vs SigNoz)."""
import json, sys, re

PATH = "data/articles_en.json"

TITLE = "Best Log Management Tools in 2026: Grafana Loki vs Better Stack vs Axiom vs SigNoz"
SLUG = "best-log-management-tools-2026-grafana-loki-vs-better-stack-vs-axiom-vs-signoz"
DATE = "2026-11-02"
DATE_FULL = "November 2, 2026"
CATEGORY = "AI Web Development"
DESCRIPTION = ("Grafana Loki, Better Stack, Axiom, and SigNoz compared: 2026 pricing, metering models, retention costs, "
               "and which log platform cuts the Datadog bill without cutting visibility.")
KEYWORDS = [
    "log management tools",
    "Grafana Loki pricing",
    "SigNoz vs Grafana",
    "Axiom vs Datadog",
    "best self-hosted log management",
    "cheap log management for small teams",
    "why is Datadog so expensive",
    "Splunk alternatives for small teams",
]

CONTENT = r"""Indexing one terabyte of monthly logs on Datadog costs roughly $3,800 a month at list rates: about $102 to ingest the raw volume, then around $3,700 to keep it searchable in a Standard index at a typical 500 bytes per event. The same terabyte runs about $89 on Axiom, $236 on Better Stack in the EU, $307 on SigNoz Cloud, and roughly $555 on Grafana Cloud before volume discounts apply. A forty-fold spread for identical data — and the reason the four log management tools compared here deserve a closer look than any feature grid gives. I have migrated logging stacks at three companies; every rate below comes from the vendors' published pricing pages plus Axiom's machine-readable rate card, checked in early November 2026. The pattern worth internalizing: ingestion is almost never the expensive part — search, retention structure, and the meter's definition of an event are where the money hides.

## How the four log management tools meter your data

All four will collect, store, and search your logs. They disagree on what a dollar buys.

Grafana Cloud (powered by Loki) splits the log bill into three meters: process ($0.05 per GB), write ($0.40 per GB), and retention ($0.10 per GB per month), each with automatic volume discounts as usage grows. The Pro plan's $19 platform fee includes 50 GB a month with 30-day retention; the free tier gives 50 GB with 14-day retention.

Better Stack bills two meters: ingestion ($0.15 per GB in EU regions, $0.10 in the US) plus retention ($0.08 and $0.05 per GB per month respectively). Prepaid bundles — Nano at $25 a month yearly for 40 GB each of logs, traces, and metrics — cap the bill and add 30-day retention across all three telemetry types.

Axiom charges a $25 monthly platform fee and meters compute in credits: data loading is free up to 1,000 GB a month, then $0.12 per GB on the first tier, sliding to $0.06 at petabyte scale. Query compute is free up to 100 GB-hours, then $0.20 per GB-hour. Storage bills compressed data — Axiom claims a default 95 percent compression ratio — at $0.03 per GB per month while data is young, aging down to $0.005.

SigNoz keeps it flat: $0.30 per GB of logs ingested, with retention selectable from 15 days to a full year on the cloud product. The $49 monthly minimum includes $49 of usage, unlimited seats, and unlimited hosts — the only one of the four with neither a per-user charge nor a host charge anywhere on the invoice.

Datadog, the anchor most teams are migrating from, charges $0.10 per GB to ingest — and then makes search a separate product. Standard Indexing costs $1.70 per million log events per month for 15-day retention ($2.55 on-demand), Flex Storage starts at $0.05 per million events for up to 15 months, and overages bill at list price plus 50 percent. That ingest-versus-index split is why Datadog bills surprise people.

## The 2026 prices, in one table

| Platform | Free tier | Entry paid plan | Overage / usage rates | The gotcha |
| --- | --- | --- | --- | --- |
| Grafana Cloud (Loki) | $0: 50 GB/mo, 14-day retention, no card | Pro: $19/mo incl. 50 GB, 30-day retention | $0.05 process + $0.40 write + $0.10 retain per GB; volume discounts | Three meters on one bill; write dominates |
| Better Stack Logs | $0: 3 GB/mo, 3-day retention | Bundles from $25/mo yearly (Nano: 40 GB logs/traces/metrics) | EU: $0.15/GB ingest + $0.08/GB/mo retention; US: $0.10 + $0.05 | Query boost scans bill $0.001/GB; own-S3 hosting is $250/mo |
| Axiom | Personal: $0 forever — 500 GB/mo loading, 10 GB-hrs query, 25 GB storage, 30-day retention | Cloud: $25/mo platform fee + usage | DLC $0.12/GB after 1,000 free; query $0.20/GB-hr after 100 free; storage $0.03/GB/mo compressed | Query workload is the sleeper: heavy analysts can out-spend the data bill |
| SigNoz Cloud | OSS self-host: free forever | Teams: $49/mo minimum incl. $49 usage | Logs $0.30/GB, traces $0.30/GB, metrics $0.10/M samples; retention 15 days–1 year | $49 floor applies even at tiny volume; enterprise tier starts at $4,000/mo |
| Datadog (context) | None for logs | Usage-based, no plan ladder | $0.10/GB ingest; Standard Indexing $1.70/M events/mo (15-day); Flex from $0.05/M events | Ingestion is cheap; making logs searchable is the product you pay for |

One footnote: Axiom's governance add-ons — SAML SSO at $100 a month, RBAC at $50 — ship at no extra cost on SigNoz's base plan, and Better Stack's bundles include traces and metrics at no extra per-GB rate.

## The 100 GB reality check

Model a small team: 100 GB of logs a month, 30-day retention, a base query workload (roughly 0.40 GB-hours of query compute per GB ingested, per Axiom's guidance), and 500-byte average events.

Datadog bills $10.20 to ingest, then roughly $374 to index about 220 million events — call it $385. Grafana Cloud Pro lands at $19 plus 50 GB over the included allowance times $0.55 combined, or about $47. Better Stack pay-as-you-go in the EU runs 100 times $0.23 (ingest plus retention), or $23. Axiom's $25 platform fee covers everything — the data, the queries, and the 5 GB of compressed storage all sit inside the free allowances. SigNoz's usage comes to $30, so the $49 minimum applies.

Now scale to a terabyte a month, same assumptions. Datadog: roughly $3,800. Grafana: about $555 at list rates before its volume discounts bite. SigNoz: $307 flat. Better Stack EU: about $236. Axiom: around $89 — the terabyte barely clears the free loading allowance, query compute adds $62, compressed storage is pocket change.

The spread narrows at query-heavy workloads. If your team scans aggressively, Axiom's high-workload guidance (2.0 GB-hours per GB) turns that $89 into about $420 — still a tenth of Datadog, but no longer the bargain the loading numbers suggest. SigNoz vs Grafana at terabyte scale is similar: the flat $0.30/GB beats Grafana's $0.55 combined list rate until volume discounts and Adaptive Logs pattern-pruning (up to 50 percent ingest reduction) pull Grafana's effective rate down. Run your own scan patterns through each calculator — the ranking flips on query behavior more than on volume.

## Grafana Cloud (Loki): the generous free tier and the three-sided meter

Grafana Loki pricing starts with the best free tier in this comparison: 50 GB a month with 14-day retention, no card required, on the same platform that hosts your metrics and traces dashboards. For a side project, that is a production-grade logging pipeline at zero dollars, and LogQL is close enough to PromQL that Prometheus users feel at home on day one.

The paid side is where teams need to read carefully. The write meter at $0.40 per GB is the dominant term — nearly three-quarters of the $0.55 combined list rate — and it applies to every GB beyond the included 50. Volume discounts are automatic, so a team doing 5 TB a month pays materially less than headline rates. And Adaptive Logs analyzes incoming patterns and recommends dropping redundant streams — deleting one chatty debug service often cuts more dollars than any plan negotiation. Enterprise starts at a $25,000 annual commitment, which is Grafana's way of saying the self-serve tiers are where most teams should stay.

The honest limitation: 30-day retention is the ceiling on self-serve plans. Compliance workloads that need a year of searchable history should look at Axiom or SigNoz instead, because Grafana's answer to longer retention is a sales conversation.

## Better Stack Logs: the observability suite wearing a log pipeline

Better Stack's logs exist inside a suite that already does uptime monitoring, incident management, on-call scheduling, and status pages — and that changes the buying math. If you are paying for those capabilities anyway, the logs are close to free: the Nano bundle at $25 a month yearly includes 40 GB each of logs, traces, and metrics with 30-day retention, plus the monitoring stack. Pay-as-you-go rates ($0.15 per GB in the EU, $0.10 in the US) sit mid-pack, and the 3 GB free tier with 3-day retention is the weakest here — enough to evaluate, not to live on.

The querying experience deserves specific praise: SQL across logs, drag-and-drop query building, VRL transforms for shaping data at ingest, and live tail. One team showed me an on-call flow where a failed uptime check opens an incident, pulls the relevant log stream, and updates the status page from the same panel — no swivel-chair between tools. The catch: query boost scans cost $0.001 per GB, own-S3 hosting is a $250 monthly add-on, and Asia-Pacific rates ($0.35/GB ingest) more than double the EU price. Under a few hundred GB a month with one vendor for the whole incident loop, Better Stack Logs pricing is easy to defend; for pure high-volume storage, the dedicated stores below are cheaper.

## Axiom: the flat platform fee with a query-workload trap

Axiom vs Datadog is the comparison Axiom publishes on its own site, and the arithmetic backs it up: at 1 TB a month with 30-day retention, roughly $89 versus $3,800 — a 97 percent cut — mostly because the first 1,000 GB of monthly loading is free and storage bills compressed data. The company publishes a machine-readable rate card aimed at AI agents modeling spend — a refreshing posture: every number in this section is quotable.

Retention is configurable up to 24 months with automatic tiering — data ages from frequent access at $0.03 per GB into archive tiers at half a cent — so compliance teams keep a year of history without a separate cold-storage product. APL handles joins and virtual fields, an MCP server with SRE skills ships included, SOC 2 Type II is audited, and the HIPAA BAA is self-serve.

The trap is the query meter. A team of five running exploratory queries all day can burn 500-plus GB-hours, and at $0.20 per GB-hour the query bill overtakes the data bill — the 100 GB reality check above shows the swing. Axiom's own workload guidance concedes the range: 0.01 GB-hours per GB for compliance archives, 0.40 for normal observability, 2.0 for platform use. Pre-purchasing compute credits cuts rates up to 47 percent at scale, but the first-lever question for any Axiom evaluation is not how much you ingest — it is how much your humans (and agents) scan.

## SigNoz: the all-in-one with the honest minimum

SigNoz is the only product here that treats logs, traces, and metrics as one flat-priced pool: $0.30 per GB for either logs or traces, $0.10 per million metric samples, retention selectable from 15 days to a year, unlimited seats and hosts, and a $49 monthly minimum that includes the first $49 of usage. The base plan ships SOC 2 Type II, HIPAA coverage, SSO, and US, EU, and India data centers — features that sit behind enterprise gates at most vendors.

SigNoz vs Grafana comes down to architecture philosophy. SigNoz runs on ClickHouse, queries everything through one pipeline, and prices one ingest number; Grafana runs Loki's label-based store and prices three meters, but offers a deeper ecosystem (dashboards, alerting, and the enormous Grafana integration catalog) plus that unmatched free tier. Teams invested in the Grafana stack should stay and optimize; teams starting fresh that want traces correlated with logs will find SigNoz's single meter easier to budget.

The open source edition is the deeper argument. SigNoz OSS is free to self-host, Apache 2.0 licensed, and — alongside Loki's AGPL self-host option — makes this pair the best self-hosted log management combination in 2026 for teams with infrastructure appetite: you run ClickHouse and the collectors, you keep the data, and the vendor relationship becomes optional.

## Cheap log management for small teams: which tool fits each stack

The four log management tools split cleanly by team shape and data volume.

Solo developers and side projects: Grafana Cloud's free 50 GB, full stop. It out-features every other free tier here, and the Axiom Personal plan (500 GB loading, 25 GB storage, 30-day retention, no card) is the runner-up for teams that query in bursts rather than continuously.

Startups under ~200 GB a month that want one bill for monitoring, on-call, and logs: Better Stack. The bundle pricing means the logs ride along with incident infrastructure you would buy anyway, and the integrated on-call flow removes an entire tool from the stack; the [uptime monitoring comparison](/articles/best-uptime-monitoring-tools-2026-better-stack-vs-uptimerobot-vs-checkly-vs-pingdom) covers that side in detail.

Terabyte-scale teams with cost problems: Axiom, eyes open about query workload. Loading and storage economics beat everything here at volume, retention tiering removes a compliance blocker, and the published rate card makes the bill modelable — but instrument your query consumption for a month before signing anything annual.

All-in-one observability on one flat meter: SigNoz, especially if traces matter as much as logs. Pair it with the [error tracking comparison](/articles/best-error-tracking-tools-2026-sentry-vs-rollbar-vs-bugsnag-vs-datadog) for the exception layer; whichever platform wins, the [DevOps observability comparison](/articles/best-ai-devops-observability-tools-2026-datadog-vs-new-relic-vs-dynatrace-vs-splunk) shows what the legacy suites charge for the same meters — useful ammunition in renewal talks even if you never switch.

## Frequently Asked Questions

### Why is Datadog so expensive for logs?

The ingest rate is only $0.10 per GB — cheap. But ingestion buys collection and archival, not search. Making logs queryable requires an index, and Standard Indexing costs $1.70 per million events per month for 15-day retention. At a typical 500-byte event size, one terabyte is roughly 2.2 billion events, so indexing alone approaches $3,700 a month. Flex Storage (from $0.05 per million events) slashes that for rarely-queried history, but hot searchable logs stay expensive.

### How does Grafana Loki pricing work?

Grafana Cloud meters logs three ways: $0.05 per GB to process, $0.40 per GB to write, and $0.10 per GB per month to retain, with automatic volume discounts as usage grows. The Pro plan's $19 platform fee includes 50 GB of monthly ingestion and 30-day retention; the free tier offers 50 GB with 14-day retention. Enterprise — custom rates, custom retention, BYOC — starts at a $25,000 annual commitment, so anything beyond 30 days of retention means talking to sales.

### What is the best self-hosted log management option?

Grafana Loki and SigNoz OSS, both free, cover opposite temperaments. Loki pairs with the Grafana stack you may already run and handles high-volume storage efficiently, but requires operating object storage and agents carefully. SigNoz OSS ships ClickHouse plus its full UI (logs, traces, metrics) under an Apache 2.0 license with Docker and Helm install paths. Self-hosting trades license fees for an on-call rotation on your own storage cluster — budget that honestly before deciding the cloud versions are overpriced.

### How much log retention do I actually need?

Thirty days covers nearly all debugging: incidents resurface within weeks, and older logs rarely get queried. The exceptions are compliance (security audit trails often mandate 90 days to a year) and security forensics, where breaches are discovered months late. The cost-efficient pattern is tiering — hot storage for 30 days, cheap archive for the tail — which Axiom automates, Datadog sells as Flex Storage, and SigNoz offers as selectable retention. Paying hot-index rates for a year of history is the most common self-inflicted overspend here.

### Are these realistic Splunk alternatives for small teams?

For ingestion under a couple of terabytes a month, yes — and the numbers are not close. Splunk's ingestion-based licensing routinely runs five figures annually before search infrastructure, which is why Axiom, Grafana, and SigNoz all publish direct comparison pages against it. What you give up is the Splunk app ecosystem and the enterprise security integrations (ES, SOAR) that larger SOCs depend on. A small platform team debugging services, not a security operations center, gets equal or better answers from all four tools here at a tenth of the cost.

## The bottom line

In 2026, log management tools are priced on three questions, and the invoice follows whichever answer hurts: what the meter counts (events, GB, GB-hours), what the base fee includes, and where retention tiering starts. Axiom owns terabyte-scale economics with a $25 platform fee and free first TB; Better Stack bundles logs into an incident-response suite starting at $25; SigNoz flattens everything to $0.30 per GB under a $49 minimum with enterprise features included; Grafana Cloud offers the best free tier and a three-meter bill that rewards pattern pruning. Datadog's roughly $3,800 terabyte is not a pricing mistake — it is the price of one vendor's index — and every vendor here exists because teams ran that arithmetic on their own invoices. Run one month of your real query patterns through two of these platforms before you sign anything; on logs, the meter definition is the purchasing decision.
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
    pk = len(re.findall(r"log management tools", CONTENT, re.I))
    print(f"Appended {SLUG}: words={words}, primary_keyword={pk}")

if __name__ == "__main__":
    main()
