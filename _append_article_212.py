# -*- coding: utf-8 -*-
"""Append article #212: Terraform Automation Platforms 2026 (Spacelift vs env0 vs Scalr vs Atlantis)."""
import json, sys, re

PATH = "data/articles_en.json"

TITLE = "Spacelift vs env0 vs Scalr vs Atlantis: Terraform Management Pricing in 2026"
SLUG = "best-terraform-automation-platforms-2026-spacelift-vs-env0-vs-scalr-vs-atlantis"
DATE = "2026-11-05"
DATE_FULL = "November 5, 2026"
CATEGORY = "AI Web Development"
DESCRIPTION = ("Spacelift, env0, Scalr, and self-hosted Atlantis compared on 2026 pricing: per-resource vs per-run "
               "billing, free tiers, drift detection, OpenTofu support, and which Terraform Cloud alternative fits "
               "each team size.")
KEYWORDS = [
    "Terraform automation platforms",
    "Terraform Cloud alternatives",
    "Spacelift pricing",
    "env0 vs Spacelift",
    "Scalr pricing",
    "Atlantis Terraform",
    "Terraform drift detection",
    "HCP Terraform pricing",
]

CONTENT = r"""A team managing 5,000 cloud resources on HCP Terraform Essentials now pays roughly $500 every month before a single plan or apply executes — $0.10 per resource per month is the entry rate on IBM's current rate card, and resource-based billing means the invoice grows with your infrastructure even if your usage never changes. That shift, layered on top of HashiCorp's 2023 license change that produced the OpenTofu fork, has made 2026 the first year in a decade that large numbers of Terraform shops are actively re-evaluating their tooling. Four credible Terraform automation platforms have absorbed most of that demand: Spacelift, env0, Scalr, and self-hosted Atlantis. One Scalr customer — a platform engineering lead in Accenture's cyber security practice, quoted on Scalr's pricing page — reports saving 80% on renewal versus Terraform Cloud. Your savings depend almost entirely on how your current vendor meters you, which is why this comparison starts with billing models rather than feature checklists. Every figure below comes from the four vendors' published pricing pages in early November 2026.

## Why Terraform teams are shopping right now

A managed layer for Terraform or OpenTofu does five jobs: stores and locks remote state, turns pull requests into plan-and-apply runs, gates deployments with policy-as-code (usually OPA), hosts a private module registry, and watches for configuration drift between your code and your live cloud. Terraform Cloud did all of this adequately for years, which is why most teams never thought about it. Two things broke the inertia.

First, the license. In August 2023 HashiCorp moved Terraform from open source to the Business Source License, and the community forked it into OpenTofu under the Linux Foundation. Every vendor on this list now runs OpenTofu alongside Terraform; the incumbent's own platform runs it too, which tells you how the fork resolved. Second, the billing. HCP Terraform pricing is now resource-based: Essentials starts at $0.10 per resource per month, Standard at $0.47, and Premium at $0.99, each also quoted hourly ($0.00013, $0.00064, and $0.00135 per hour respectively). A 20,000-resource estate on Standard runs about $9,400 a month — for software whose open-source core anyone can still self-host. IBM, which closed its acquisition of HashiCorp in early 2025, offers new accounts a $500 trial credit across the platform, but credits end and rate cards do not.

The alternatives attack that bill from three different angles: flat per-seat plans (Spacelift), per-successful-apply metering (env0), and per-run pricing with no user or resource charges at all (Scalr). This guide walks the credible Terraform Cloud alternatives in that order, with self-hosted Atlantis as the fourth angle: no vendor bill, because you host it.

## The 2026 rates, in one table

| Platform | Billing model | Free tier | Drift & policy tooling | Real cost at moderate scale |
| --- | --- | --- | --- | --- |
| HCP Terraform | Per resource/mo: $0.10 Essentials, $0.47 Standard, $0.99 Premium | $500 trial credit | Full suite; Standard+ adds Waypoint | 5,000 resources = $500 (Essentials) to $2,350 (Standard) monthly |
| Spacelift | Flat monthly plans | $0: 2 users, 1 API key, OIDC SSO, cost estimation | OPA policy engine from Starter; drift detection included | Starter from $399/mo for 10 users |
| env0 | Per successful apply or environment (custom quote) | 250 runs/mo, 30 environments, unlimited users, 1 concurrent run | Basic drift management in Navigator; AI remediation in Pilot | No public rate card; quote-based |
| Scalr | Per run, prepaid | 50 runs/mo free, all core features | OPA built in; scheduled drift runs never billed | 400 runs/mo ≈ $390/mo (vendor calculator); overage $0.99/run |
| Atlantis | Self-hosted, Apache-2.0, free | Everything, free | None native; bolt on Conftest and Infracost | Your server plus an engineer's on-call attention |

## HCP Terraform: the default, now billed by the resource

The incumbent still has the deepest integration surface — the module registry, Waypoint templates for self-service, and native policy sets — and for teams deep into the HashiCorp stack (Vault, Boundary, Nomad), that gravity is real — our [secrets management comparison](/articles/best-secret-management-tools-2026-doppler-vs-infisical-vs-1password-vs-hashicorp-vault) covers the Vault side of that bundle. But the resource-based model has a specific failure mode: the bill tracks estate size, not engagement. A team that provisions once a week pays the same as one applying hourly, and the Essentials tier caps test-integrated module publishing at ten private modules — Standard lifts that, at nearly five times the per-resource rate. Run the math on your own `terraform state list` output before anything else; it is the single number that decides whether leaving is worth the migration weekend. Teams under a few hundred resources often stay put; teams in the thousands increasingly do not.

## Spacelift: flat pricing and the deepest policy engine

Spacelift pricing is the simplest story here: a free tier for two users with OIDC single sign-on, cloud cost estimation, and resource visualization, then a Starter plan from $399 per month covering ten users, two public workers, webhooks, a private module registry, and the OPA-based policy engine. Business and Enterprise tiers add named support and quote-only features. Flat plans cut both ways. A ten-person team pushing thousands of runs a month gets cost predictability no metered competitor matches; a two-person shop paying $399 feels the opposite. Where Spacelift genuinely earns the fee is the automation surface: custom tasks, day-2 operations, context stacks, and what is still the most flexible policy-as-code implementation in the category — you can gate runs on anything OPA can express, including cost estimates and plan contents. Drift detection runs on schedules and can auto-reconcile. If your team lives in policy reviews and compliance evidence, this is the deepest tool here. If you just need state and PR runs, you are paying for capability you will not touch.

## env0: unlimited users, metered applies

The env0 vs Spacelift comparison comes down to a philosophical split. env0's free tier gives 250 runs a month, 30 active environments, unlimited users, and one self-hosted runner — but caps concurrency at one run and run duration at 20 minutes, and once you pass 250 runs, scheduled jobs like TTL destroys and drift detection silently skip until the next cycle. Paid tiers (Cloud Navigator and Cloud Pilot) are custom-quoted per successful apply or per environment, with no public rate card — the one vendor here you cannot price from a website. Navigator adds basic drift management (detection, cause analysis, code-to-cloud redeployment), RBAC, SAML, a private registry, and Infracost-based cost estimation; Pilot layers on an AI analyst, advanced drift remediation, and cost management. The unlimited-users model is genuinely attractive for organizations where fifty engineers touch infrastructure but only a few apply daily — per-seat billing punishes that shape, per-apply billing does not. The 20-minute free-run cap and quote-only paid tiers are the friction: budget real procurement time, and test your longest applies on the free tier before committing.

## Scalr: per-run pricing built to undercut Terraform Cloud

Scalr pricing bills runs — apply runs and dry runs (including PR plans) — and charges nothing for users, resources, workspaces, concurrency, environments, or self-hosted agents. Free covers 50 runs a month with all core features, including the OPA policy engine and Terraform drift detection on schedules that are explicitly not billed. The vendor's own calculator prices a 400-billable-run month at $390, overage beyond a prepaid plan is $0.99 per run, and runs never get blocked while you overage. The fine print rewards reading: failed plans and OPA-rejected runs are billed, but init failures, pre-plan rejections, and drift-detection runs are not, and Scalr ships a script that counts what your Terraform Cloud usage would have cost you as billable runs — an unusual level of confidence in its own math. The Enterprise tier starts at 20,000 runs per year with a technical account manager. The trade-off is surface area: fewer bells than Spacelift, no AI analyst like env0's Pilot, and a product identity as the cost-rebel rather than the category leader. For teams whose run counts are predictable and whose resource counts are scary, that identity is exactly the point.

## Atlantis: free, and you are the platform team

The Atlantis Terraform workflow is the ancestor of everything above: comment `atlantis plan` on a pull request, review the plan, comment `atlantis apply`. It is open source under Apache-2.0, self-hosted on one server with VCS webhooks, and it costs nothing in licensing. What it lacks is everything the vendors productized: no UI beyond PR comments, no drift detection, no policy engine (bolt on Conftest), no cost estimation (bolt on Infracost), no module registry, and no one to page when the single server wedges before a Friday deploy. You also own the security perimeter — the Atlantis token grants cloud credentials, and hardening it is your job; pair it with the practices in our [authentication platforms](/articles/authentication-platforms-2026-auth0-vs-clerk-vs-supabase-vs-workos) and secrets management guides. Atlantis still makes sense for small teams with strong GitOps discipline and a platform engineer who owns it as part of their role. The honest question is not the license fee but the labor: one engineer-day per month of maintenance equals $400–800 of payroll, which quietly exceeds a Spacelift or Scalr subscription. If you want the workflow without the babysitting, Terrateam is the managed successor worth a look.

## Terraform automation platforms compared: which one fits your team

The four Terraform automation platforms above sort cleanly by team shape. Under 5 engineers or under ~300 resources: stay on HCP Terraform Essentials or run Atlantis — neither bill justifies a migration. A growing team of 5–15 engineers with heavy PR traffic and compliance requirements: Spacelift, whose flat $399 Starter and OPA depth fit policy-driven shops. Large organizations with many occasional contributors: env0, where unlimited users plus per-apply metering beat both per-seat and per-resource models — provided you negotiate the quote down. High-volume, predictable run counts with big resource estates: Scalr, which is the only one publishing a script to prove its savings. And if your run counts are modest but your resource count is enormous — lots of long-lived, rarely-changed infrastructure — per-resource pricing is the worst model for you and per-run is the best; that single asymmetry explains most migrations in 2026. For the CI runners that feed these platforms, see our [CI/CD comparison](/articles/best-cicd-tools-2026-github-actions-vs-gitlab-vs-circleci-vs-jenkins), and for the bill they create, our [cloud cost management guide](/articles/best-cloud-cost-management-tools-2026-cloudzero-vs-finout-vs-vantage-vs-kubecost).

## Frequently Asked Questions

### What is the best Terraform Cloud alternative in 2026?

There is no single best — the answer tracks your billing exposure. If HCP Terraform's per-resource model costs you more than about $400 a month, Scalr's per-run pricing is the direct substitute with the published math to back it (its calculator and migration script estimate your equivalent run count). If you need the deepest policy-as-code and automation surface, pick Spacelift. If your team is large but only a few members apply changes, env0's unlimited-user, per-apply model wins. Atlantis remains the best zero-license option if you can staff its maintenance.

### How much does Spacelift cost per month?

Spacelift's free tier supports 2 users with 1 API key. The Starter plan starts at $399 per month and includes 10 users, 2 public workers, webhooks, a private module registry, and the policy-as-code engine. Business and Enterprise plans are quote-only, adding named customer success from 3 workers, silver support, and enterprise features. There are no per-run or per-resource charges, so a heavy-usage month bills the same as a quiet one.

### Is self-hosted Atlantis still a good idea?

For small teams with GitOps discipline, yes — it is free, mature, and its PR-comment workflow is what every commercial platform copied. The costs are hidden, not absent: you own uptime, upgrades, credential security, and drift monitoring, and there is no native drift detection, policy engine, or cost estimation without bolting on Conftest and Infracost. Once maintenance passes roughly one engineer-day a month, a managed platform becomes cheaper than your payroll.

### Do Spacelift, env0, and Scalr support OpenTofu?

All three run OpenTofu as a first-class framework alongside Terraform, including workspace support, drift detection, and their policy engines — as does HCP Terraform itself. Because OpenTofu stays backward-compatible with Terraform 1.x modules and state, migrating between any of these platforms is mostly a state-import and credentials exercise, not a rewrite. Verify your specific Terraform version is supported before committing, since vendor support for the newest releases can lag by weeks.

### Per-run or per-resource pricing: which is cheaper?

Per-resource billing (HCP Terraform) scales with estate size; per-run billing (Scalr) scales with change frequency. A 10,000-resource estate changed twice a month pays about $1,000 on HCP Essentials but under $50 at Scalr's $0.99 overage rate; a 500-resource estate applying 500 times a month pays $50 on HCP Essentials versus roughly $490 on Scalr. Count your resources and your monthly runs, then pick the axis that is smaller. env0's per-apply model behaves like per-run with a different meter, and Spacelift's flat plans ignore both axes entirely.

## The bottom line

In 2026, Terraform automation platforms finally compete on something more interesting than feature parity: they meter different things. HCP Terraform meters your estate, Spacelift meters your seats, env0 meters your applies, and Scalr meters your runs — with Atlantis metering nothing but your time. Pull two numbers before you decide: your `terraform state list` length and your last 90 days of run history. Whatever you choose, the migration itself is a weekend — state files move, OpenTofu keeps the modules working, and the vendors all publish import guides because they are all hunting the same dissatisfied incumbent customers. Every rate in this article comes from the vendors' own pricing pages in early November 2026; Scalr's $0.99 overage and HCP's per-resource tiers are recent enough that re-verifying before you sign a contract is not paranoia, it is diligence.
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
    pk_cs = len(re.findall(r"Terraform automation platforms", CONTENT))
    pk_ci = len(re.findall(r"Terraform automation platforms", CONTENT, re.I))
    print(f"Appended {SLUG}: words={words}, pk_case_sensitive={pk_cs}, pk_case_insensitive={pk_ci}")

if __name__ == "__main__":
    main()
