#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

tool = {
    "name": "Lindy",
    "slug": "lindy",
    "emoji": "🤵",
    "color": "#17171c",
    "description": "An AI employee that finishes jobs instead of drafting replies: it triages your inbox, updates the CRM, books meetings, takes phone calls, and runs scheduled routines inside Slack - then hands you anything customer-facing for approval. Paid by credits, roughly a cent per credit.",
    "category": "AI Agents",
    "tags": [
        {"text": "AI Employee"},
        {"text": "Inbox Triage"},
        {"text": "CRM Automation"},
        {"text": "Agency Retainers"}
    ],
    "rating": "⭐ 4.5",
    "badge": {"type": "new", "text": "NEW"},
    "url": "https://www.lindy.ai/",
    "price": "Free $50 credits · from $29.99/mo",
    "pricing_details": "Free plan: $50 in credits, valid 7 days, no credit card. Team plans are billed per active user with credits pooled across the team: the current homepage advertises from $29.99/month for 3,000 credits each, while a pricing-page variant still shows $49.99/month for 5,000 credits (the two official pages disagree - treat $29.99 as the advertised floor and confirm at checkout). Credit sliders run up to 1.75M credits at $9,999.50. Top-ups cost $10 per 1,000 credits and never expire, but monthly plan credits do not roll over. Credits measure work at roughly a cent each: everyday asks (answers, lookups, drafted replies, CRM updates) run 2-250 credits, deep work (competitor research with a report, support-queue triage, proposals from a week of calls) runs 250-1,000, and big builds (dashboards, internal tools, heavy scheduled workflows) run 1,000-2,500. When the pool runs dry, Lindy pauses rather than overbilling. Enterprise adds custom pricing with HIPAA and a signed BAA, SSO/SCIM, audit logs, shared bonus credits, and dedicated onboarding. Security posture: SOC 2 Type II, GDPR, PIPEDA; data is encrypted and never used to train models.",
    "platform": "Slack, Gmail, iMessage, browser + 1,500+ integrations + any MCP server",
    "published": True,
    "pros": [
        "It completes work, not drafts: inbox triage, CRM updates, meeting bookings, and scheduled routines come back done, with an approval gate on anything that leaves the building",
        "Slack-native with 1,500+ integrations and MCP support - adoption is an @mention, not an IT project",
        "Model-agnostic: you pick the model per task instead of being locked to one vendor's engine",
        "Approval-first design (prep, approve, then send) makes it safe enough to hand customer-facing work",
        "The credit system with pause-not-overbill behavior keeps costs legible, unlike per-seat agent platforms with surprise API bills"
    ],
    "cons": [
        "Credit burn is hard to predict: one deep-work task (250-1,000 credits) eats 8-33% of the advertised 3,000-credit base plan in a single job",
        "The two official pricing pages disagree on the entry tier ($29.99/3,000 vs $49.99/5,000) - budget for the higher number",
        "Every active user in a workspace is billed, and monthly credits vanish at cycle end - idle seats still cost money",
        "Computer use and multi-inbox setups sit on higher tiers, so the headline entry price buys less than the demo implies",
        "It is a teammate, not a workflow engine: complex deterministic pipelines still belong in n8n or Make"
    ],
    "features": [
        "Inbox management: drafts replies in your voice, connects 2-5 inboxes depending on tier, waits for approval",
        "Meeting stack: joins calls as a named participant, records, notes, schedules, and sends follow-ups",
        "Scheduled routines: describe a Monday-morning pipeline brief once, Lindy posts it weekly to the channel you choose",
        "Phone calls and iMessage: books and confirms with callers directly from your phone",
        "Computer use, 40+ skills plus custom ones, persistent workspace memory, and model choice across major providers"
    ],
    "faq": [
        {
            "question": "What does a Lindy credit actually buy?",
            "answer": "Roughly a cent of AI work. Small asks - a summary, a lookup, a drafted reply, a CRM note - cost 2 to 250 credits. A deep task like researching a competitor and writing the report, or triaging a day's support queue, runs 250 to 1,000. Complex builds such as a dashboard assembled from your CRM and analytics run 1,000 to 2,500. On the advertised 3,000-credit base plan, that means one serious deep-work job consumes up to a third of your monthly allowance - plan around it, and remember top-up credits ($10 per 1,000) never expire while monthly ones do."
        },
        {
            "question": "Why do two Lindy pages show different entry prices?",
            "answer": "They do. Lindy's homepage advertises Team from $29.99/month for 3,000 credits per user, while its pricing-page variant lists $49.99/month for 5,000 credits. Pricing has shifted between these tiers through 2026, and some official pages lag behind others. The safe budgeting assumption is $49.99 for 5,000; if checkout shows $29.99, take it. The free $50 in credits (7 days) exists exactly so you can measure your real credit burn before committing to either number."
        },
        {
            "question": "Can Lindy actually replace a virtual assistant?",
            "answer": "For structured admin work, largely yes: inbox triage and drafted replies, meeting scheduling and follow-ups, CRM hygiene, weekly briefs, and simple phone booking all run without a human. What it cannot do is judgment calls with real stakes - refund decisions, sensitive customer complaints, anything where being wrong costs money - those still need a person approving. Users report the realistic outcome as 'a VA's workload at a fraction of a VA's $1,000+ monthly cost, with you as the approver,' not full replacement."
        }
    ],
    "content": """## What Lindy Actually Is

Most AI assistants stop at an answer. Lindy stops at a finished job. You hand it work the way you would hand a new hire: clear the inbox, update the CRM after today's calls, book the demo the lead just asked for, send the Monday pipeline brief. It lives in Slack (plus Gmail, iMessage, and the browser), pulls context from 1,500+ integrations or any MCP server, and remembers your business across jobs - which is why the same Lindy gets better for your whole team over time.

The design choice that makes it sellable to cautious businesses is the approval loop: lookups happen on their own, but anything with outside impact - a customer reply, a booking confirmation, a discount code - waits for your OK until you explicitly let it run solo. It is also unusually credentialed for an agent product: SOC 2 Type II, GDPR, PIPEDA, and HIPAA with a signed BAA on Enterprise, with an explicit promise that your data never trains models.

Payment is by credit, at roughly a cent each. Small asks cost a few credits, deep work hundreds, big builds thousands. When the team pool runs low, Lindy pauses and says so instead of silently overbilling - a small thing, but it shows in an agent market full of surprise invoices.

## The Money Angle

1. **Sell AI-employee setups as retainers.** The clearest agency play in the agent space: configure Lindy for a client's inbox, CRM, and meeting ops, then charge $500-2,000/month for a managed "AI teammate" while your actual credit cost stays in the tens of dollars. The approval-first design is your sales script - the client stays in control, you stay on the bill.

2. **Replace your own admin stack.** A part-time VA for inbox and scheduling runs $800-1,200/month. Lindy's credit costs for the same workload land near $30-100. The realistic model: Lindy does the mechanical 80%, you approve the consequential 20%.

3. **Lead follow-up that never sleeps.** Every lead who replies gets a same-minute drafted response, a proposed meeting slot, and a CRM update - the hand-off layer where most pipelines leak. Sales teams pay for recovered leads far more readily than for software.

4. **Missed-call recovery for local businesses.** Lindy now takes phone calls. For clinics, salons, and contractors, an agent that answers the phone, books the slot, and texts a confirmation is a product you can set up in an afternoon and charge monthly for.

5. **Meeting-to-artifact pipelines.** Record calls, extract decisions, generate the proposal or the deck, post it before the next meeting. Selling "your week of calls becomes Friday's report" is a concrete deliverable, not a vague AI promise.

## What It Really Costs

| Layer | Cost | Notes |
|---|---|---|
| Free | $0 | $50 in credits, 7-day window, no card required |
| Team (advertised) | from $29.99/mo per active user | 3,000 credits each, pooled |
| Team (pricing-page variant) | from $49.99/mo | 5,000 credits each - official pages conflict |
| Top-ups | $10 per 1,000 credits | Never expire; monthly credits don't roll over |
| Enterprise | Custom | HIPAA/BAA, SSO/SCIM, audit logs, bonus credits |
| Everyday ask | 2-250 credits | Summaries, lookups, replies, CRM notes |
| Deep work | 250-1,000 credits | Research reports, queue triage, proposals |
| Big builds | 1,000-2,500 credits | Dashboards, internal tools, heavy routines |

Budget reality: a solo operator doing one deep-work task per day will outgrow the 3,000-credit plan within the first week. The $50 free credits exist to measure your actual burn rate - use them before choosing a tier, and assume the $49.99 number until checkout says otherwise.

## The Honest Cons

- **Credit opacity is the real tax.** Credits are honest in rate but unpredictable in count - a "quick competitor report" can quietly cost 1,000 credits. The pause-instead-of-overbill design helps, but planning a fixed monthly spend remains guesswork until you've run a real week.
- **Pricing pages disagree with each other.** $29.99 vs $49.99 entry tiers across official pages as of November 2026 - sloppy, and it matters when you're quoting a retainer.
- **Idle seats bill.** Every active user in the workspace is charged; monthly credits evaporate at cycle end. Team plans reward dense usage and punish part-timers.
- **The demo shows computer use and multi-inbox power; the entry tier buys less.** Higher capabilities sit on upper tiers.
- **Deterministic pipelines still need a workflow engine.** If your process must run the same 12 steps every time, n8n or Make do it cheaper and more predictably. Lindy wins where judgment is involved.

## vs The Field

| | Lindy | n8n / Make | Zapier AI |
|---|---|---|---|
| Model | Conversational AI employee with memory | Deterministic workflow automation | Workflow suite with AI steps |
| Pricing shape | Credits (~1 cent) pooled per team | Per-task/per-operation tiers | Per-task tiers |
| Judgment calls | Yes - reads, decides, drafts | Only via LLM nodes | Via AI steps |
| Best at | Inbox, meetings, CRM, phone, routines | Repeatable pipelines, self-hosting | SaaS glue at scale |
| Setup | @mention in Slack, minutes | Node graphs, hours-days | Low-code builder |

Against the site's existing reviews: crew-ai and langgraph remain the open-source route for developers building bespoke agent systems; Lindy is the productized version for operators and agencies who want an AI teammate live this afternoon, billed by the job. If your workload is deterministic, the workflow tools still cost less per action.

## Bottom Line

Lindy is currently the most complete "AI employee" a non-engineer can actually deploy - live in Slack in minutes, safe by default behind approvals, and priced by work done rather than seats guessing. The honest caveats are credit unpredictability and entry-price ambiguity across its own pages, both of which the free $50 credit week is designed to settle. The strongest money angle on this page is not internal efficiency - it is the agency retainer: businesses will pay monthly for a managed AI teammate that clears inboxes and never forgets a follow-up, and Lindy's approval-gated design finally makes that sellable to cautious clients."""
}

with open("_tmp_lindy.json", "w", encoding="utf-8") as f:
    json.dump(tool, f, ensure_ascii=False, indent=2)
print("OK _tmp_lindy.json", len(tool["content"]), "chars content")
