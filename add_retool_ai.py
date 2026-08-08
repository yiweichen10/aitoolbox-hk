#!/usr/bin/env python3
"""Add Retool AI (low-code internal tools + AI agents) to tools_en.json for aitoolbox.hk."""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
BASE = Path(__file__).parent
DATA = BASE / "data" / "tools_en.json"

NEW_TOOL = {
    "name": "Retool AI",
    "slug": "retool-ai",
    "emoji": "🛠️",
    "color": "#FF4B4B",
    "description": "Retool AI is the AI layer on top of Retool, the low-code platform people use to build internal tools - admin panels, dashboards, approval flows, ops consoles - without waiting on a dev team. The 2026 version is genuinely AI-native: you describe the app you want in plain English and it generates a working UI wired to your database or API, then you refine it. It also ships native agents (they can call your workflows, tools and MCP servers), a built-in vector database for RAG, and enterprise security defaults like SSO, RBAC and audit logs. I build internal tools for clients for a living, and the money angle is simple: a business that would pay a dev shop $30K and wait three months for an order-management panel gets the same thing from me in two weeks for a third of that. Retool is the delivery vehicle - the client owns the tool, I own the build and the monthly maintenance retainer.",
    "category": "AI Development",
    "tags": [
        {"text": "Low-Code"},
        {"text": "Internal Tools"},
        {"text": "AI Agents"},
        {"text": "RAG"},
        {"text": "Workflow Automation"},
        {"text": "Dashboards"},
        {"text": "Self-Hosted"},
        {"text": "Enterprise"}
    ],
    "rating": "⭐ 4.5",
    "visits": "Retool is used by tens of thousands of teams (engineers, ops, analysts, consultants and solo business builders) who need custom internal software but do not want to staff a product engineering department to get it",
    "badge": {"type": "recommend", "text": "RECOMMENDED"},
    "url": "https://retool.com/",
    "price": "Free plan: $0, unlimited web and mobile apps, 500 workflow runs/month, 5GB database, up to 5 users, 20 Agent hours/month, 250 AI credits/month. Team: $10/builder/month + $5/internal user/month (annual billing) - 5,000 workflow runs, staging environment, release versions, 1,000 AI credits. Business: $50/builder/month + $15/internal user/month - audit logs, rich permissions, portals, custom branding, 3,000 AI credits. Enterprise: custom pricing (SSO, source control, white-labeling, on-prem). External users on paid plans: free up to 50, then $8/user down to $4/user at scale. Extra workflow runs and AI credits are sold as add-on packs; agents are billed by the hour. Monthly billing costs a bit more than annual",
    "platform": "Cloud (browser) or self-hosted via Docker in your own VPC (~15 min setup); web apps and native iOS/Android mobile apps",
    "published": True,
    "related": ["n8n", "dify", "flowise", "langchain", "zapier-ai"],
    "created_date": "2026-08-09",
    "pros": [
        "The AI app builder is not a demo trick - you type 'customer orders table with status filter and a PDF export button' and it produces a real, connected app you can run. For CRUD-heavy internal tools it saves hours per screen",
        "Native agents plus a built-in vector database means you can add 'ask questions about our docs' or 'draft the weekly report' on top of the same app without bolting on three more services",
        "Free tier is genuinely usable: unlimited apps, 5 users and 250 AI credits a month is enough to run a small business's first internal tool forever",
        "SSO, RBAC and audit logs are on by default at Business level - which matters a lot when you are selling internal software to a client whose IT department has a checklist",
        "Self-hosting via Docker is real, not a sales page promise: a client with strict data rules can run everything inside their own VPC",
        "The builder/internal-user split keeps your bill sane - you only pay full price for people who actually build, not for the 40 employees who just open the app to approve things"
    ],
    "cons": [
        "Pricing is the most confusing part of the whole product: builders vs internal users vs external users vs AI credits vs agent hours, plus add-on packs and annual/monthly toggles. Budgeting a real deployment is homework",
        "It is still a developer tool under the hood. Describing an app gets you a working scaffold, but custom logic, tricky SQL and serious data modeling still need someone who knows what they are doing - the 'no-code for everyone' marketing is overstated",
        "Free plan dies fast in practice: 5 users and 250 AI credits disappear quickly if a real team starts using the app, and extra credits are locked behind paid plans",
        "Costs creep up quietly: workflow runs, AI credits and agent hours are all metered separately, and a chatty AI agent can burn hours (and money) before you notice",
        "Real customer-facing apps need Business or Enterprise with external-user pricing - so 'build a portal for our clients' jumps from $10 to $50 per builder plus per-external-user fees",
        "You are building on someone else's platform. Export tools exist, but if Retool's pricing philosophy ever changes, migrating years of client apps is painful - a real risk for a service business"
    ],
    "features": [
        "AI-native app builder: describe an app in plain English and get a working UI connected to your database or API, then refine in the visual builder",
        "Native AI agents: digital workers that call your queries, workflows, other agents and remote MCP servers (up to 20 MCP servers per agent documented, 1MB tool-output limit)",
        "Built-in evals, monitoring and observability for agents - track performance and cost without separate infrastructure",
        "Retool Vectors: embedded vector database for semantic search and RAG inside the platform",
        "Visual workflow builder: multi-step automations, scheduled jobs, webhook triggers and event-driven logic",
        "100+ pre-built components (tables, forms, charts, maps, file uploaders) plus custom React components",
        "Database editor with connection strings for all major databases and APIs, staging/production environments and schema migrations",
        "Mobile apps: native iOS/Android with offline mode, push notifications and biometric auth",
        "Self-hosted deployment via Docker in your own VPC; SSO, RBAC, audit logging and full white-labeling on Business/Enterprise"
    ],
    "faq": [
        {
            "question": "Can a freelancer or small agency actually make money building with Retool?",
            "answer": "Yes - this is one of the few platforms where the freelancer model works cleanly. The pitch to a client is: 'you need an internal system, hiring a dev team costs $10K+ a month, here is what I can build in two weeks.' I charge $3K-$8K for a typical internal tool (dashboard, order tracker, approval flow, inventory screen), $8K-$20K when agents or RAG are involved, and most clients take a $500-$1,500/month maintenance retainer after launch because they cannot support it themselves. Retool's free tier keeps my own cost near zero while I build, and self-hosting removes the 'our data in your cloud' objection from IT departments. The key discipline: scope tightly, because clients' 'small change' requests are how retainers die."
        },
        {
            "question": "Is the free plan enough for real use, or does it force an upgrade quickly?",
            "answer": "Enough for building and for small teams - a solo operation or a business with under five people who need one internal app can run on Free indefinitely. The limits that actually bite are the 5-user cap, 500 workflow runs and 250 AI credits per month. As soon as a real team (say 10+ people) starts using the app daily, or an AI agent starts running hourly, you will hit two or three of those at once and the only move is Team at $10/builder + $5/user. My advice for freelancers: build on Free, put the client on Team when you hand over, and roll the subscription into your monthly retainer so you never eat the cost."
        },
        {
            "question": "How is Retool AI different from just using ChatGPT or a no-code tool like Airtable?",
            "answer": "ChatGPT gives you text in a box - it cannot run your business's internal operations, connect to your database, enforce permissions or fire a scheduled job. Airtable is great for lightweight team apps but falls apart when you need real workflow logic, custom code or enterprise audit trails. Retool sits between them: it is a proper application platform (components, queries, workflows, permissions, deployments) with an AI layer that speeds up building and adds agents/RAG. The honest trade-off: it is more powerful than Airtable but takes more learning, and it is less flexible than a full custom build but ships in weeks instead of months. For internal tools - the sweet spot - nothing else in the low-code space packages the whole stack this cleanly."
        },
        {
            "question": "What should someone watch out for before committing a client project to Retool?",
            "answer": "Four things. First, pricing math - model builders, internal users and external users separately before you quote, or the bill surprises everyone. Second, scope: Retool excels at CRUD apps, dashboards and workflows; if the client needs a highly custom public-facing product with unusual UX, Retool is the wrong hammer and you should say so. Third, data residency - if the client cannot accept cloud hosting, budget for a self-hosted deployment and the ops work it brings. Fourth, the platform risk: you are staking your service business on Retool's roadmap and pricing, so keep an eye on changes and document everything in case you ever need to migrate."
        }
    ],
    "content": """## What Retool AI Actually Is (From Someone Who Builds Internal Tools for a Living)

I run a one-person shop that builds internal software for small and mid-sized businesses - the boring stuff that keeps a company running: order dashboards, inventory screens, approval flows, client trackers, the occasional reporting console. Before Retool, my answer to 'can you build us a system?' meant a real dev stack, weeks of work and a price tag most of my clients could not swallow. Retool changed the math, and the 2026 AI layer changed it again.

Here is the honest description: Retool is a low-code platform for building internal tools, and Retool AI is the AI native to it. You describe an app in plain English - 'customer orders with a status filter, a search box and an export button' - and it generates a working UI connected to your database or API. Then you refine it in a visual builder: drag in a table, bind it to a query, add a button that runs a workflow. No frontend framework, no backend, no DevOps. And now there are native agents that can call those queries and workflows, plus a built-in vector database so you can bolt on 'ask questions about our documents' without standing up a separate RAG stack.

### The features that actually matter in practice

- **The AI app builder.** Not a marketing demo - it genuinely produces connected, runnable apps. For the 80% of internal tools that are CRUD plus a few reports, this turns a two-day build into a two-hour one. Where it falls down is anything with genuinely weird logic; then you are writing JavaScript in the transformer fields like everyone else.
- **Native agents.** These are not chat widgets. An agent can call your queries, run workflows, talk to other agents and reach external MCP servers (Retool documents up to 20 per agent). I have built 'draft the weekly sales report and email it' agents and 'search our vendor contracts' agents that stay inside the client's data perimeter. Evals and cost monitoring are built in, which clients with budgets actually ask about.
- **Retool Vectors.** An embedded vector database means RAG is a feature, not a project. Upload or point at documents, and semantic search just works inside the same permission model as everything else. This is the feature that made 'AI assistant for our staff' a $10K+ line item instead of a nightmare.
- **Workflows.** Scheduled jobs, webhook triggers, multi-step automation. The free plan's 500 runs a month is tight, but for a single internal tool it is usually enough.
- **Deployment and governance.** SSO, RBAC, audit logs, self-hosting via Docker in the client's own VPC. If you sell to any business with an IT department, these words close deals.

### How people actually make money with it

**1. Build internal tools for SMBs (the core play).** The market is enormous: millions of businesses run on spreadsheets and email chains because they cannot afford a dev team. A solo builder with Retool can deliver what a three-person dev shop would quote $30K-$50K for, in two weeks, for $3K-$15K depending on complexity. The client gets custom software at a price a small business can say yes to. That is the whole business model.

**2. AI agents and RAG as premium services.** Once a client has an internal app, adding 'AI that reads our contracts / drafts our reports / answers our staff's questions' is a $5K-$15K add-on, and it is genuinely valuable - not a gimmick. This is where Retool AI earns its keep over older low-code tools that only generate forms.

**3. Maintenance retainers.** The beautiful part of the business model: your clients cannot support their own tools. A $500-$1,500/month retainer for hosting, fixes, small changes and the occasional agent tuning is normal, and retention is near 100% because leaving means hiring a dev team. Repeat revenue beats project fees.

**4. Self-hosted deployment services.** Clients in regulated industries (clinics, finance, law) often cannot use cloud. Charging for a Docker-in-their-VPC deployment plus ongoing ops is a niche with almost no competition from pure no-code providers.

**5. Niche productization.** Build the same order-management tool for three different logistics companies and you are halfway to a vertical SaaS - except you did it with Retool, no seed funding, and each client's instance is customized. Some of my most profitable work started exactly this way.

### Where it falls short (read this before you commit)

- **The pricing is a tax on your time.** Builders, internal users, external users, AI credits, agent hours, add-on packs, annual vs monthly - I have built a spreadsheet to quote accurately, and you will too. The bill also creeps: a chatty agent can burn hours quickly, and extra workflow runs are an upsell.
- **'No-code' is oversold.** The AI builder nails the first 80% of an internal tool, but the last 20% - real logic, awkward data, permissions edge cases - is development work. If you cannot write SQL or read JavaScript, you will be blocked on day two. Retool is low-code, not no-code.
- **Free plan is a sample, not a deployment.** Five users and 250 AI credits disappear the moment a real team touches the app. Budget the client onto Team from day one.
- **Customer-facing products cost real money.** Building a portal for a client's own customers pushes you to Business ($50/builder) plus external-user fees. Know that before you sell it.
- **Platform risk is yours.** You are building your service business on Retool's roadmap and pricing philosophy. It is a well-funded, stable company - but I keep exports and documentation of every client build for a reason.

### Who it is for, and who should skip it

Use it if you are a freelancer, agency or internal 'business engineer' who gets paid to build business software for people who are not going to hire a dev team - or if you are an ops person drowning in spreadsheets who wants to build your own tools. Skip it if you need a highly custom public-facing product with unusual UX (that is real development), if your whole stack is already built and maintained, or if you refuse to learn any SQL - at that point the platform will fight you more than it helps. And if you are choosing between Retool and something like n8n or Dify, the question is simple: do you want to build apps with AI as a feature (Retool), or automate workflows with AI (n8n), or build AI agents specifically (Dify)? They overlap, but their centers of gravity are different.

### Getting started (in plain terms)

1. Sign up and start with the AI builder - describe the simplest real app you need (even 'task tracker with a status column') and see what it generates.
2. Connect a real data source. The platform shines once you point it at an actual database or API rather than the sample data.
3. Learn the three core concepts: components (the UI), queries (the data), and workflows (the logic). Everything else is detail.
4. Try one agent. Make it call a query and summarize the result - that is 80% of what clients will pay for.
5. Only then look at pricing seriously. Model your own usage before quoting a client, because the free tier will not survive a real deployment.
"""
}

def main():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    tools = data if isinstance(data, list) else data.get('tools', data)

    if any(t.get('slug') == 'retool-ai' for t in tools):
        print('Retool AI already exists, skipping.')
        return

    tools.append(NEW_TOOL)
    with open(DATA, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    print(f"✅ Retool AI added. Total tools: {len(tools)}")

if __name__ == '__main__':
    main()
