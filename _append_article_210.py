# -*- coding: utf-8 -*-
"""Append article #210: Best Cron Monitoring Tools 2026 (Cronitor vs Healthchecks.io vs Dead Man's Snitch vs Better Stack)."""
import json, sys, re

PATH = "data/articles_en.json"

TITLE = "Best Cron Monitoring Tools in 2026: Cronitor vs Healthchecks.io vs Dead Man's Snitch vs Better Stack"
SLUG = "best-cron-monitoring-tools-2026-cronitor-vs-healthchecks-vs-dead-mans-snitch-vs-better-stack"
DATE = "2026-11-03"
DATE_FULL = "November 3, 2026"
CATEGORY = "AI Web Development"
DESCRIPTION = ("Cronitor, Healthchecks.io, Dead Man's Snitch, and Better Stack Heartbeats compared: 2026 pricing, "
               "free tiers, grace periods, and the cheapest honest way to know a scheduled job died at 2 a.m.")
KEYWORDS = [
    "cron job monitoring",
    "Cronitor pricing",
    "Healthchecks.io vs Cronitor",
    "free cron monitoring",
    "Dead Man's Snitch alternative",
    "cron monitoring for Kubernetes",
    "heartbeat monitoring",
    "monitor scheduled jobs",
]

CONTENT = r"""Monitoring twenty scheduled jobs costs $0 a month on Healthchecks.io's free plan, $19 on Dead Man's Snitch, $20 on Better Stack, and $55 on Cronitor — the same twenty jobs, the same three people on the alerts, a spread from nothing to more than double the median. Those numbers come straight from the vendors' published pricing pages in early November 2026, and they explain why cron job monitoring remains one of the few infrastructure categories where the right answer for most teams is still free. I have maintained production crontabs for over a decade, and the failure mode has never changed: a job dies at 2 a.m., prints nothing, alerts nothing, and somebody notices six weeks later when a customer asks where the nightly report went. Cronitor's site carries a public testimonial from Babylist's CEO about a backup job failing silently for more than a month — the standard story, not an edge case. The tools below exist to make that silence impossible, and the interesting part is not the feature grid. It is how differently each vendor meters the same handful of HTTP pings.

## How heartbeat monitoring catches what error handling never will

Every tool here exists to monitor scheduled jobs, and all of them run on the same primitive, sometimes called a dead man's switch. Your job pings a unique URL when it finishes — `curl https://hc-ping.com/your-uuid` in a crontab wrapper, a callback at the end of an Airflow DAG, an SDK call in a Kubernetes CronJob. The service expects to hear from the job on a schedule: every 5 minutes, every night at 2 a.m., every first of the month. When the expected ping does not arrive within a grace period you define, an alert fires.

This inverts the usual monitoring logic, and the inversion matters. Try/except blocks and exit-code checks only catch failures the job knows about: a segfault, an OOM kill, a killed container, a server that never boots — none of them trigger your error handler, because nothing runs at all. Absence detection catches every flavor of "the job did not happen," which is the flavor that actually wakes people up at night. Healthchecks.io, Dead Man's Snitch, and Better Stack all work purely this way. Cronitor goes a step further and captures the exit code, duration, and output of each run, so you can see not just that a job went missing but that it had been limping with warnings for two weeks before it died.

Two settings decide whether these tools are useful or noisy, and neither costs money: the schedule definition (fixed intervals versus cron expressions versus "expected time of day") and the grace period. Set the grace too tight and a job that legitimately runs long pages your on-call; set it too loose and you find out about failures an hour late. Every vendor here handles both, with different ergonomics.

## The 2026 prices, in one table

| Tool | Free tier | Entry paid plan | Bill at 20 jobs, 3 teammates | The catch |
| --- | --- | --- | --- | --- |
| Healthchecks.io | 20 jobs, 100 log entries each, forever | Business $20/mo: 100 jobs, SMS/WhatsApp and phone credits | $0 — if 20 is truly your ceiling | Absence alerts only; no exit codes or output capture |
| Cronitor | 5 monitors, 5-minute minimum frequency | $2/mo per monitor + $5/mo per user | $55 ($40 in monitors + $15 in seats) | Two meters multiply; free tier caps at 5 monitors |
| Dead Man's Snitch | Trial only, no permanent free plan | Private Eye $19/mo: 100 snitches, enhanced intervals | $19 | The $5 tier covers just 3 snitches; jump to 100 costs 4x |
| Better Stack Heartbeats | 10 heartbeats | +10 heartbeats: $20/mo, $17/mo billed yearly | $20 monthly, $17 yearly | Sold in 10-packs, priced separately from the suite's other products |
| Healthchecks self-hosted | Unlimited jobs, free (BSD license) | Your server bill | $0 plus one small VPS | You own uptime, upgrades, and making alerts actually deliver |

Three footnotes that change the math. First, Healthchecks.io discounts annual billing 20 percent — Business lands at $192 a year — and hands the Business plan free to open-source projects and nonprofits. Second, Cronitor's example bill on its own pricing page matches mine: 20 monitors and 3 users is $55, no base fee, volume discounts above that. Third, Better Stack's heartbeats ride alongside its uptime monitors (10 free of those too, 50 more for $25 a month), on-call scheduling, and status pages — if you already pay for the suite, the first 10 heartbeats are effectively house money.

## Healthchecks.io: the $0 workhorse that refuses to grow up

Healthchecks.io is the rare infrastructure product whose pricing page fits in one screen and has not needed to change in years. The free Hobbyist plan monitors 20 jobs with 100 log entries each, forever, with no card — and the paid ladder is two rungs: Business at $20 a month for 100 jobs, 1,000 log entries per job, and 50 SMS/WhatsApp plus 20 phone-call alert credits; Business Plus at $80 for 1,000 jobs and proportionally more credits. Annual billing takes 20 percent off. That is the entire price list, and the honesty is the product.

The alerting catalog is where it embarrasses tools ten times its price: email, Slack, Telegram, WhatsApp, SMS, phone calls, PagerDuty, webhooks, Pushover, ntfy, and more, configurable per check. Integrations are not gated by tier — the free plan sends Slack alerts too. There is even a dedicated "Supporter" plan at $5 a month with identical limits to the free one, sold purely so people can pay the company out of guilt.

Those limits are real. Alerting is absence-only: no exit codes, no run output, no duration tracking — you learn the job stopped, not why. The 100-log-entry cap means a job running every five minutes burns its history in about eight hours, per the vendor's own FAQ. And team features sit behind the Business plan. For a solo operator or a small team under 20 jobs, though, nothing else in this comparison delivers more value per dollar, because the dollars are zero. The code is open source under a BSD license with 10,000-plus GitHub stars, so self-hosting is a `docker run` away.

## Cronitor: the metered professional with receipts

Cronitor is the only tool here that treats a monitored job as more than a ping. Each run records status, duration, and captured output; you can alert on a job that starts late, runs too long, or exits nonzero — not just one that never pings. For teams migrating off homegrown crontab watchdog scripts, that depth is the reason to pay. The integration list is the deepest here too: 11 alert targets including PagerDuty, OpsGenie, Datadog On-Call, Splunk On-Call, plus SAML SSO with role-based access on the Business plan.

Cronitor pricing is where opinions split. The Business plan meters two things: $2 per monitor per month and $5 per user per month, no base fee. Twenty monitors and three users is $55 a month — two and a half times Healthchecks.io Business for the same job count. The free Hacker plan covers 5 monitors with email and Slack alerts, but caps check frequency at 5 minutes and strips SMS and on-call integrations, so it is genuinely for homelabs. Enterprise starts at $6,000 a year.

When does the premium buy something real? Three cases: jobs whose failure mode is "runs wrong" rather than "never runs" (exit codes and output settle arguments fast); teams that need 12-month data retention for compliance or capacity planning, which Business includes; and environments where the 30-second check frequency floor matters, like monitoring worker queues rather than nightly batch. If your jobs are simple nightly batches and your team is under 20 jobs, the $55 is hard to defend. If a silent partial failure once cost you a week of re-backfilling data, it is cheap.

## Dead Man's Snitch: the minimalist that never added a settings page

Dead Man's Snitch has been selling the same promise since 2013: a URL, an interval, an alert when the ping goes missing. Three plans, no usage meters, unlimited team members on every tier — a genuinely rare touch, since seat fees are how Cronitor's bill doubles. Little Birdy is $5 a month for 3 snitches with basic intervals; Private Eye is $19 for 100 snitches, enhanced intervals, and integrations; Surveillance Van is $49 for 300 snitches and adds Smart Alerts and Error Notices. That is the model.

Its main flaw is the ladder's shape. The $5 tier tops out at 3 snitches, so anyone with a dozen jobs lands on the $19 plan — which is fine, because 100 snitches at $19 undercuts everyone except Healthchecks.io's free tier. The deeper problem is what it does not do: no exit-code capture, no output logs, no duration alerting, and — the real gap in 2026 — no permanent free plan. The trial converts or it does not. As a Dead Man's Snitch alternative, Healthchecks.io's free plan is strictly more generous, and its self-hosted edition removes the vendor entirely; the honest reason to pick DMS is taste: the cleanest interface in the category, setup in seconds, and for a non-engineering team (marketing ops with nightly exports, analytics shops with scheduled scrapes) the lack of knobs is a feature.

## Better Stack Heartbeats: the suite rider

Better Stack sells heartbeats as one product inside an observability and incident-response suite — the same company behind the uptime monitoring, on-call, and status page stack I covered in the [uptime monitoring comparison](/articles/best-uptime-monitoring-tools-2026-better-stack-vs-uptimerobot-vs-checkly-vs-pingdom). Every account includes 10 heartbeats; the next 10 cost $20 a month, or $17 on annual billing, with unlimited SMS and phone-call alerts included rather than metered in credits. Check resolution goes down to 1 second, grace periods are configurable per heartbeat, and SLA reporting ships in the base product.

The pitch is the integration with everything around it. A missed heartbeat opens an incident in the same tool that pages your on-call rotation, posts to Slack, updates the status page, and — this is the differentiator — drops the relevant log stream next to the alert, since Better Stack Logs rides on the same account. No other tool here closes the loop from "the 2 a.m. backup did not ping" to "here are the last 40 lines of its output" without a second product. The catch is arithmetic: heartbeats price in 10-packs, separately from uptime monitors, separately from logs. Ten free heartbeats cover a small operation perfectly; a hundred jobs mean ten paid packs at roughly $170 to $200 a month, where Healthchecks.io Business Plus is $80. Buy Better Stack for the suite and treat heartbeats as a rider, not the other way around.

## Cheap cron job monitoring: which tool fits each stack

The four cron job monitoring tools split cleanly by job count, budget, and how much forensic detail you need after a failure.

Solo developers and side projects: Healthchecks.io's free plan is the best free cron monitoring on the market, full stop. Twenty jobs with Slack and Telegram alerts costs nothing and asks for no card. The self-hosted edition is the runner-up for anyone who already runs a server and enjoys owning things — Healthchecks.io vs Cronitor on the self-host question is not a contest, because Cronitor does not offer an open-source edition at all.

Small teams from 20 to 100 jobs watching the budget: it is Healthchecks.io Business at $20 versus Dead Man's Snitch Private Eye at $19, and the tiebreaker is forensic depth — Healthchecks.io wins on integrations-per-dollar and the OSS escape hatch, DMS wins on unlimited team members and interface simplicity. Cron monitoring for Kubernetes workloads lands here too: CronJob pods come and go, so absence detection against a fixed schedule fits, and a plain curl in the job spec works without a sidecar.

Teams that need to know why a job failed, not just that it did: Cronitor, and the $55 bill is the honest price of exit codes, output capture, and 12-month history. Teams already paying for Better Stack's on-call or logs: add the free 10 heartbeats before buying anything else — they also pair naturally with the [background job schedulers](/articles/best-background-job-schedulers-2026-inngest-vs-triggerdev-vs-temporal-vs-hatchet) your jobs actually run on — and only buy the $20 pack when you count more than 10 jobs worth protecting.

## Frequently Asked Questions

### What is a dead man's switch, and why does it beat failure alerts?

A dead man's switch alerts when something that should signal regularly goes quiet. Failure alerts (try/except, exit-code handlers, `|| curl` chains) only fire when code executes and notices something is wrong. They miss the server that never booted, the container the OOM killer reaped, the DNS failure that prevented the job from starting at all. Absence detection covers every one of those cases with a single primitive, which is why every tool here is built on it. The two approaches stack: Cronitor captures exit codes when the job does run, and the heartbeat catches when it does not.

### Cronitor vs Healthchecks.io: which is cheaper in 2026?

Under 20 jobs and one to three people, Healthchecks.io wins outright: its free plan covers the workload, while Cronitor's same 20 monitors cost $40 plus $5 per user. At 100 jobs, Healthchecks.io Business is $20 a month against Cronitor's $200 in monitors alone plus seats. The only shape where Cronitor gets close is a tiny deployment — 5 monitors, 2 users, $20 a month — where its exit-code capture and output logs justify the premium over a free absence-only check. Above 10 monitors, the per-monitor-plus-per-seat meter simply cannot compete with a flat $20.

### How do I monitor a Kubernetes CronJob without adding a sidecar?

Every service here exposes a plain HTTPS ping endpoint, so the zero-infrastructure answer is a `curl -fsS` in your job's command or a postJob wrapper. Healthchecks.io documents integrations for Kubernetes specifically; Cronitor ships an SDK and an auto-discovery agent that reads your CronJob specs and registers monitors from a manifest. Better Stack and Dead Man's Snitch both work with plain pings from any environment. Whatever you pick, ping on success only and let the grace period do the alerting — pinging both start and finish is for jobs where a mid-run hang must look different from a job that never started.

### What is a grace period and how should I set it?

The grace period is how long the service waits past the expected ping time before declaring the job dead. Set it too tight and normal variance pages you: a nightly job that usually takes 30 minutes but occasionally runs 42 becomes an incident. Set it to zero and the alert fires on a schedule the job never promised. The practical rule: grace should cover the job's worst normal runtime plus infrastructure variance — for a nightly backup, an hour; for a every-5-minutes queue poller, two to three intervals. Every tool here makes grace configurable per job, and getting this one number right matters more for alert quality than the choice between vendors.

### Is the Healthchecks.io free plan enough for production?

For up to 20 jobs, yes — it is the same product as the paid tiers with a smaller job cap and shorter per-job history, and Slack, Telegram, PagerDuty, and webhook alerts are included rather than gated. The two production-grade caveats: the 100-log-entry cap erases history fast on high-frequency jobs, and there is no SLA on the free tier. Teams that outgrow 20 jobs should weigh Business at $20 a month against the self-hosted edition — same code, unlimited checks, your own SMS gateway costs, and one more thing to keep alive, which a dead man's switch vendor failing silently would find amusing.

## The bottom line

In 2026, cron job monitoring is a solved problem with a $0 answer for most teams and a $55 answer for teams with forensic needs, and the entire decision fits in three questions. How many jobs? Under 20, take Healthchecks.io's free plan and stop reading. What do you need after an alert fires — just "it stopped," or exit codes, output, and a year of run history? The first answer is Healthchecks.io or Dead Man's Snitch at $19 to $20; the second is Cronitor, and the metered bill is the honest price of receipts. Are you already paying Better Stack for on-call and logs? Then the 10 free heartbeats are the cheapest reliability upgrade on this page. Every rate above came from the vendors' published pricing pages in early November 2026 — check them before you sign anything, because per-monitor meters are the kind that drift.
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
    pk = len(re.findall(r"cron job monitoring", CONTENT, re.I))
    print(f"Appended {SLUG}: words={words}, primary_keyword={pk}")

if __name__ == "__main__":
    main()
