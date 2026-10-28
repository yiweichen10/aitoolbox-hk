#!/usr/bin/env python3
"""Append article #205: API testing tools comparison (Postman vs Insomnia vs Bruno vs Hoppscotch)."""
import json

PATH = 'data/articles_en.json'

content = """Postman's 2025 State of the API survey put a hard number on a fear most teams had not budgeted for: 51% of developers worry about AI agents making unauthorized or excessive calls to their APIs — on top of endpoint counts growing faster than headcount. The client you poke those endpoints with has quietly become infrastructure, and in 2026 four API testing tools divide the desktop market: Postman, Insomnia, Bruno, and Hoppscotch. Two of them sell platform subscriptions with usage meters attached; two are open-source projects that monetize enterprise controls instead. I have run real work on all four — Postman as the team default, Insomnia inside a Kong-gateway shop, Bruno as the offline-first escape hatch, Hoppscotch on locked-down laptops where nothing installs. The pattern that holds: the tool matters less than where your collections live and who can see them. Get it wrong and you pay for it in duplicated requests, stale environments, and the lone engineer who can still reproduce a bug. Here is what each client costs in 2026, where each wins, and the trade-offs the pricing pages gloss over.

## How the four clients actually diverge

Every client here sends requests, saves collections, manages environments, and runs tests. On a checklist they look interchangeable. The differences that decide budgets: where collections are stored, how collaboration is metered, and how much of the API lifecycle the vendor tries to own.

- **Postman** is the platform play: API client, collections, mock servers, monitors, generated documentation, an AI credit meter, and a public API network, all tied to a cloud workspace model. Everything syncs to Postman's cloud by default — the feature or the problem depending on your security posture.
- **Insomnia**, owned by Kong, is a lighter desktop app that pairs OpenAPI design with REST, GraphQL, gRPC, WebSocket, and SSE clients, plus an Inso CLI that runs the same collections in CI. Cloud sync is end-to-end encrypted, and a local-only Scratch Pad mode remains free forever.
- **Bruno** stores every collection as plain-text `.bru` files inside your own Git repository. No vendor cloud, no login, no sync service — collaboration happens through Git branches and pull requests like the rest of your code, and the desktop app works fully offline.
- **Hoppscotch** runs in a browser tab — zero install, 80,000+ GitHub stars, an MIT-licensed core, and a Docker-based community edition you can self-host so collections never leave your server. REST, GraphQL, WebSocket, SSE, Socket.IO, and MQTT panels sit in one interface.

A market note: Postman monetizes the workspace, Insomnia monetizes the seat inside a gateway vendor's ecosystem, and Bruno and Hoppscotch monetize governance and support on top of a free core. That is why the pricing sections read so differently — each vendor meters a different thing.

## Postman pricing 2026: what the platform really costs

Postman's pricing changed shape in 2026: the old Basic and Professional plans are gone, replaced by Free, Solo, Team, and Enterprise, with annual billing saving up to 25% and monthly rates no longer published. Free covers a single user with 1,000 monitoring calls a month, 10,000 Postman API calls, and a small AI credit allowance (the page shows 50 to 100 depending where you look) with overage at $0.05 per credit. Solo costs $9 per month billed annually and stays single-player: 400 AI credits, unlimited private npm packages, custom domains for published docs, and extended monitoring quotas. Team is the real collaboration tier at $19 per user per month billed annually — unlimited users and workspaces, basic RBAC, 400 AI credits per user, automation flow credits, and cloud performance tests at $0.04 per virtual-user-hour. Enterprise is quote-only, with 800 pooled AI credits per user, the API Catalog, advanced RBAC, SSO through a security add-on, audit logs, and 24x5 support.

The meters that surprise teams are monitoring and AI. Monitor quotas start at 1,000 calls a month on Free and top out at 10,000 on paid tiers — scheduled smoke tests against a busy API burn through that fast, and more capacity means sales calls or moving the job to CI. AI credits are spent on Postman's assistant features, and a team that leans on them daily will hit the 400-per-user ceiling and pay overage. None of this is unreasonable, but model it: six developers on Postman Team pay $114 a month before add-ons — the honest baseline for the comparisons below.

## Bruno vs Postman: Git-native, offline, and the trade-offs

The Bruno vs Postman argument is really about whether your API collections are code or cloud documents. Bruno treats them as code: collections live as human-readable files in your repository, version-controlled with the service they test, reviewed in pull requests alongside the changes that break them. Nothing leaves your machine. For regulated environments where a third-party cloud holding your internal endpoint inventory is a non-starter, Bruno is often the only acceptable option among the big four — open source API testing, no data-residency conversation required.

The free open-source edition has real limits: 2 workspaces, Git providers limited to public repositories, and 5 OpenAPI syncs per month. Bruno Pro, at $6 per user per month billed annually, removes those caps and adds private Git providers, unlimited workspaces, an AI assistant, data-driven testing, and a 48-hour support SLA. Ultimate, at $11 per user per month, adds SSO, SCIM, audit logs, license management, and 24-hour support with PO-based invoicing — the enterprise package for teams that standardized on it.

Run the same six-developer team through Bruno's math: $0 on open source if public repos and 2 workspaces suffice, $36 a month on Pro, $66 on Ultimate — against Postman Team's $114. That arithmetic is why Bruno tops most Postman alternatives shortlists. What you give up is Postman's ecosystem: no native public mock servers or scheduled monitors, no API network, a smaller plugin library, and a collaboration model that assumes your engineers already think in Git. Teams that don't want collections reviewed like code will find the workflow odd; teams that live in Git wonder why they ever synced collections to someone else's cloud.

## Insomnia vs Postman: the Kong bundle and the lighter desktop

Insomnia's current lineup is the simplest of the four. Essentials is free: unlimited collection runs, unlimited environments, end-to-end encryption, custom linting rules, plugins, Inso CLI for CI automation, and unlimited Git Sync projects for up to 3 users — the free collaboration ceiling. Mock servers include 1,000 requests a month, with additional packs at $10 per 25,000. Pro costs $12 per user per month billed annually and lifts those limits: unlimited users and organizations, RBAC, and 10,000 mock requests. Enterprise is $45 per user per month billed annually, self-serve up to 50 users, and adds SAML/OIDC SSO, SCIM provisioning, enforced storage policies (local, Git, or cloud), domain capture, SOC2 reporting access, and native integrations with vault managers from AWS, GCP, Azure, and HashiCorp — useful when your test secrets already live in one.

The Scratch Pad exists for a reason: a local-only, no-account mode that stays free forever, added after Insomnia's 2023 move to mandatory cloud accounts triggered a revolt serious enough to reshape the roadmap. Bruno's rise is the measurable consequence of that episode, and it is fair to evaluate both before committing a team.

The case for Insomnia is strongest in Kong shops, where the desktop client integrates natively with Konnect and the spec-first workflow fits gateway-first architecture. Postman's own comparison page concedes the pricing point, listing Insomnia as starting at $12 per user against its own $19 Team tier. Outside the Kong ecosystem, Insomnia wins by being lighter than Postman while keeping cloud sync, mocking, and CI testing; it loses on ecosystem breadth — no public API network and fewer integrations.

## Hoppscotch and the self-hosted math

Hoppscotch is the zero-install option: open a browser tab, paste a URL, send. The free plan covers REST, GraphQL, and realtime testing with a personal workspace, collections, environments, pre-request scripts, and a collection runner — no account required. Business costs $6 per user per month billed annually and adds team workspaces with real-time collaboration, shared collections, published API documentation, mocking, MCP server support, and an admin dashboard. Enterprise Cloud, introduced in the September 2026 release, is $11 per user per month billed annually ($14 monthly) and adds identity and access management, RBAC, SAML/OIDC SSO, SCIM, audit logs, domain whitelisting, AI agent features, and priority support through Slack Connect.

The Hoppscotch self-hosted route is where it diverges from everyone else on price. The Community Edition is a free Docker deployment under the MIT license — same core features, your server, your data. The self-hosted Enterprise edition, documented at $19 per user per month, adds SSO, audit logs, and admin controls for organizations that must keep tooling inside their own perimeter. For a 20-person team, that is $380 a month minus a small VM and an afternoon of Docker setup — usually the cheapest enterprise-grade governance in this comparison once you accept the operational ownership.

One caveat matters more than any pricing line: browser tabs live inside CORS rules, so requests to localhost or private networks need the Hoppscotch extension or a self-hosted instance with the proxy enabled. Desktop clients like Bruno and Insomnia never ask for that step. Teams testing internal services behind a VPN should self-host or pick a desktop client; teams testing public APIs will never notice.

## Feature and cost comparison

The table distills what each client costs to adopt, where the free tier ends, and who each fits. Prices are list prices from each vendor's pricing page as of October 2026.

| Client | Free tier | Paid entry | Collaboration & metering model | Best fit |
| --- | --- | --- | --- | --- |
| Postman | 1 user, 1,000 monitor calls/mo, ~100 AI credits | Solo $9/mo annual; Team $19/user/mo annual | Cloud workspaces, unlimited users on Team; meters on AI credits, monitors, perf tests at $0.04/VuH | Teams wanting one platform across the API lifecycle |
| Insomnia | Unlimited runs, Git Sync for 3 users, 1,000 mocks/mo | Pro $12/user/mo annual; Enterprise $45/user/mo annual | Per-seat, E2EE cloud sync, unlimited users on Pro; mock packs $10 per 25K | Kong shops and spec-first teams wanting a lighter desktop |
| Bruno | Full offline client, 2 workspaces, public Git only | Pro $6/user/mo annual; Ultimate $11/user/mo annual | Collections in your Git repo, no vendor cloud; paid tiers add SSO, SCIM, audit logs | Compliance-locked and offline-first teams |
| Hoppscotch | Free web app, personal workspace, no account needed | Business $6/user/mo annual; Enterprise Cloud $11/user/mo annual | Cloud orgs or free MIT self-host; self-hosted Enterprise $19/user/mo adds SSO and audit logs | Zero-install testing and self-hosting teams |

## Which API testing tools fit which team

Matching API testing tools to a team comes down to one question first and everything else second: where should collections live? If the answer is "in Postman's cloud, shared by default, with a public API network," Postman Team at $19 per user is the mature choice — the ecosystem, mock servers, monitors, and documentation generators are years ahead. If the answer is "in our Git repository, next to the code, reviewed in pull requests," Bruno wins at $6 per user and runs entirely offline; compliance teams will not find a cleaner story anywhere. If the answer is "end-to-end encrypted cloud, lighter than Postman, wired into our Kong gateway," Insomnia at $12 per user is the pragmatic middle. If the answer is "on our own server, in a browser, with enterprise SSO for $11 a seat," Hoppscotch's cloud tiers or its $19 self-hosted enterprise edition deliver governance at the lowest infrastructure cost here.

Three integration notes. First, testing authenticated endpoints is half the job, and token lifecycles, SSO flows, and service credentials deserve the same rigor as the requests — our [authentication platforms comparison](/articles/authentication-platforms-2026-auth0-vs-clerk-vs-supabase-vs-workos) covers where those credentials should live and what identity infrastructure really costs. Second, a saved request is not a monitor: Postman's 1,000-call monthly quota is fine for smoke tests, but anything real belongs in dedicated uptime checks, and our [uptime monitoring tools comparison](/articles/best-uptime-monitoring-tools-2026-better-stack-vs-uptimerobot-vs-checkly-vs-pingdom) covers tools built for that job. Third, documentation drifts the moment it decouples from the collection — if docs are part of your workflow, our [API documentation tools comparison](/articles/best-api-documentation-tools-2026-mintlify-vs-gitbook-vs-readme-vs-fern) covers platforms that generate reference docs your clients actually read.

## Frequently Asked Questions

### What is the best free API client in 2026?

For a solo developer, all four free tiers are genuinely usable. Bruno's open-source edition is the most generous if you work in Git — no account, no cloud, a full offline client, with the caps (2 workspaces, public Git providers, 5 OpenAPI syncs a month) invisible to most individuals. Hoppscotch Free is the most accessible — zero install, no account, runs on locked-down laptops where you cannot install software. Insomnia Essentials adds unlimited collection runs and encrypted sync for 3 users. Postman Free works but meters monitors and AI credits tightly. If forced to one answer: Bruno for Git-native developers, Hoppscotch for everyone else.

### Is Bruno actually free for teams?

The desktop client is free for any number of users forever — there is no seat meter and no cloud service to pay for, since collaboration happens through your own Git infrastructure. What teams pay for is convenience and governance: Pro at $6 per user per month adds private Git providers, unlimited workspaces, the AI assistant, and support with a 48-hour SLA; Ultimate at $11 adds SSO, SCIM, audit logs, and invoicing. A team comfortable with public GitHub repos and two workspaces pays $0 indefinitely; an enterprise needing SCIM and audit trails pays less than half of a comparable Postman deployment.

### Postman vs Insomnia: which should a small team pick?

For a team of three to ten, the decision usually comes down to ecosystem versus weight. Postman Team ($19/user) buys the API network, mature mocking and monitoring, generated docs, and the largest integration catalog — pay for it if any of those matter. Insomnia Pro ($12/user) buys a lighter desktop app with end-to-end encrypted sync, unlimited users, RBAC, and Inso CLI for CI; teams already running Kong get native integration on top. The quiet tiebreaker: Insomnia's free tier lets 3 people collaborate through Git Sync at $0, so a three-person team can defer the decision entirely until scale forces it.

### Can you self-host Postman?

No. Postman's cloud workspace model is the product, and there is no self-hosted edition at any price — air-gapped teams get an offline export workflow at best. That single fact is why Bruno and Hoppscotch exist as serious alternatives: Bruno keeps collections in your Git repository by design, and Hoppscotch's Community Edition is a free Docker deployment with the self-hosted Enterprise edition at $19 per user per month adding SSO, audit logs, and admin controls. If your security review requires the tooling inside your perimeter, Postman is the one option on this list you cannot have.

### Do these clients still matter when AI agents write the requests?

More than ever, and for an uncomfortable reason. Postman's own survey found 51% of developers worried about AI agents making unauthorized or excessive API calls, and an agent that can read your collections can also leak the secrets inside them. The clients are responding in different ways: Postman meters AI features through credits and sells security administration as an add-on, Hoppscotch shipped an agentic assistant in its Enterprise tiers with configurable model providers, and Bruno's model — secrets scoped per environment, collections in your own repo, nothing synced to a vendor cloud — is increasingly what security reviews ask for. The testing client is where human API knowledge and agent API access now meet — choose accordingly.

## The bottom line

In 2026, API testing tools have stopped competing on request-sending — every client here does that well — and started competing on where collections live and how governance is sold. Postman is the platform default at $19 per user, worth it for teams that live in its ecosystem and priced fairly once you model the meters. Insomnia at $12 per user is the lighter desktop with encrypted sync and the strongest story for Kong shops. Bruno at $6 per user (or $0) is the Git-native, offline-first choice that compliance teams keep discovering, with the trade-off of a smaller ecosystem. Hoppscotch wins the zero-install and self-hosting arguments outright, with enterprise governance at $11 in the cloud or $19 self-hosted. Before deciding, do the audit almost nobody does: check where your collections live today, count who can see them, and price that same team on all four meters — the collaboration model is the decision, and an afternoon of math tells you which one wins."""

article = {
    "title": "Best API Testing Tools in 2026: Postman vs Insomnia vs Bruno vs Hoppscotch — Pricing, Free Tiers & Self-Hosting",
    "slug": "best-api-testing-tools-2026-postman-vs-insomnia-vs-bruno-vs-hoppscotch",
    "date": "2026-10-29",
    "dateFull": "October 29, 2026",
    "category": "AI Development",
    "description": "Postman, Insomnia, Bruno, and Hoppscotch compared: 2026 pricing, free tiers, self-hosting options, and which client fits your team's workflow.",
    "keywords": [
        "API testing tools",
        "Postman pricing 2026",
        "Postman alternatives",
        "Bruno vs Postman",
        "Insomnia vs Postman",
        "Hoppscotch self-hosted",
        "best free API client",
        "open source API testing"
    ],
    "content": content
}

with open(PATH, encoding='utf-8') as f:
    data = json.load(f)

if any(a['slug'] == article['slug'] for a in data):
    raise SystemExit(f"Duplicate slug guard: {article['slug']} already exists")

data.append(article)

with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Appended article: {article['slug']} (total: {len(data)})")
