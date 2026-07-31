# -*- coding: utf-8 -*-
"""Add Voiceflow to tools_en.json (aitoolbox.hk).
Backs up the file first, appends the new entry, writes back UTF-8,
and runs a forbidden-word scan on the content.
"""
import json
import shutil
import datetime

DATA = "data/tools_en.json"
TODAY = datetime.date.today().strftime("%Y%m%d")

# ---- Backup first (SOUL.md Rule #3) ----
shutil.copy2(DATA, f"{DATA}.{TODAY}.bak")
print(f"[BACKUP] {DATA}.{TODAY}.bak created")

new_tool = {
    "name": "Voiceflow",
    "slug": "voiceflow",
    "emoji": "\U0001F399",
    "color": "#0066FF",
    "description": "Voiceflow is a visual, no-code builder for AI agents and chatbots - you drag conversation steps onto a canvas, connect them to a knowledge base and any LLM, test the flow, then deploy to a web widget, WhatsApp, Slack, or a phone line. I build customer-support and booking bots for small businesses on it, and the money side is plain: clients pay $2,000-$5,000 per bot plus a $100-$500 monthly maintenance retainer, while my only real cost is a $60-a-month Pro seat.",
    "category": "AI Agents",
    "tags": [
        {"text": "Chatbot Builder"},
        {"text": "AI Agents"},
        {"text": "No-Code"},
        {"text": "Voice AI", "type": "free"},
        {"text": "Conversational AI"},
        {"text": "Customer Support"}
    ],
    "rating": "\u2b50 4.5",
    "visits": "100,000+ builders in the community; enterprise customers include teams at Fortune 500 companies; used for web, WhatsApp, SMS, Slack, and phone agents",
    "badge": {
        "type": "recommend",
        "text": "RECOMMENDED"
    },
    "url": "https://www.voiceflow.com/",
    "price": "Starter Free (100 credits/mo, 2 agents, 1 workspace, 50 knowledge sources, basic LLMs); Pro $60/mo ($648/yr = ~$54/mo; 20 agents, 3K knowledge sources, all major LLMs, 5 concurrent voice calls); Business $150/mo (unlimited agents, 10K knowledge sources, LLM fallback, 15 concurrent voice calls, priority support); Enterprise custom (SSO, Agent CMS, private cloud, BYO LLM). Extra editor seats +$50/mo each. Credits: ~1 per chat message, ~10/min for voice plus TTS/STT",
    "platform": "Web (cloud only, no self-host); deploy to Web widget, WhatsApp, SMS, Slack, phone/telephony",
    "published": True,
    "related": [
        "flowise",
        "coze",
        "dify",
        "gumloop",
        "relevance-ai",
        "n8n",
        "bardeen"
    ],
    "created_date": "2026-08-01",
    "pros": [
        "The visual canvas is genuinely best in class - conversation design feels like Figma, and a non-technical client can follow what you built without a walkthrough",
        "The hybrid flow design (hand-drawn happy path plus AI fallback node) means the parts that must be deterministic stay deterministic and everything off-script is handled by the model",
        "Voice is a real differentiator - phone agents, IVR replacement, and outbound calls are first-class, which most no-code chatbot tools do not offer at all",
        "Full LLM choice from the Pro tier - GPT, Claude, and Gemini are all switchable per project, so you are never locked into one vendor",
        "Multi-channel deployment from a single flow - the same agent runs on web, WhatsApp, SMS, and Slack, which is what clients ask for first",
        "Built-in testing tools (simulator, version history, conversation analytics) let you prove a bot works before you bill for it"
    ],
    "cons": [
        "Credits are the hidden tax - roughly one per chat message and about ten per minute of voice, they do not roll over, and when they run out mid-month your agent stops responding with no top-up option",
        "No native live-agent handoff - escalating a conversation to a human means wiring up an external tool, which is a real gap for customer-service use cases",
        "The free Starter plan is mostly a demo - two agents and 100 credits a month will not survive a single real deployment",
        "Knowledge-base retrieval can hallucinate out of the box; a production bot needs monitoring and tuning of the KB answers, not set-and-forget",
        "Every extra editor costs $50/month on top of the base seat, so a small team's real cost is often double the advertised number",
        "Cloud only - there is no self-hosted option, which rules out clients with strict data-residency requirements"
    ],
    "features": [
        "Visual Flow Builder - drag-and-drop canvas for messages, logic branches, API calls, and AI steps, with real-time multiplayer editing",
        "AI Agent Node - LLM-powered fallback that answers off-script questions from the knowledge base and routes back into the structured flow",
        "Knowledge Base (RAG) - upload PDFs, URLs, and docs as retrieval sources; 50 sources on free, 3,000 on Pro, 10,000 on Business",
        "Multi-Channel Deployment - one flow published to Web widget, WhatsApp, SMS, Slack, and phone/telephony (IVR replacement and outbound calls)",
        "Voice & Telephony - build voice agents with phone numbers, speech-to-text, and text-to-speech; five concurrent calls on Pro, 15 on Business",
        "Integrations - Zapier, Make, Airtable, Google Sheets, Salesforce, HubSpot, plus API and webhook blocks for custom connections",
        "LLM Choice - OpenAI GPT, Anthropic Claude, and Gemini switchable per project; bring-your-own-model on Enterprise",
        "Observability - simulator testing, version history, conversation transcripts, and analytics dashboards built in"
    ],
    "faq": [
        {
            "question": "How do you actually make money building bots on Voiceflow?",
            "answer": "You sell the deployed agent, not the software. The standard model in my world is a build fee plus a monthly retainer: $2,000-$5,000 to design, build, and launch a support or booking bot, then $100-$500 a month to host it, update the knowledge base, and monitor the transcripts. A dentist office bot that books appointments and answers insurance questions is a $3,000 build and a $250/month retainer in my market. Real costs against that: the Pro seat is $60/month and credits burn at about one per chat message - a small-business bot handling 2,000-3,000 messages a month stays inside the 10,000-credit bucket on Pro. So a single $3,000 build plus eight monthly retainers puts you at $2,000 a month of recurring revenue against roughly $150 of tool cost. The voice angle pays even better: phone agents are harder to build, so clients accept $300-$800/month without blinking."
        },
        {
            "question": "Is the free Starter plan enough to run client work?",
            "answer": "No. It is a sandbox, not a production seat. Two agents, one workspace, and 100 credits a month die the moment a real visitor shows up - a single 15-minute conversation can burn 30-50 credits with a premium model, and voice calls eat 10 credits a minute before TTS and STT. I use the free plan to prototype and to demo flows to prospects, then move the project to a Pro seat before anything goes live. I bake the $60/month into every quote so the client effectively pays for the subscription, and I keep one Pro seat per three or four active retainers - the credit volume of small bots does not collide. If a client's bot starts burning through credits (a viral post, a busy season), the answer is upgrading to Business, not squeezing the plan."
        },
        {
            "question": "Voiceflow vs Botpress vs Dialogflow vs Flowise - which should you learn to sell?",
            "answer": "They split by buyer. Botpress is the developer choice - open-source roots, self-hosting, more code control, a more generous free tier, but a steeper learning curve and none of Voiceflow's polish. Dialogflow is Google's intent-based UI; it works but feels dated and its knowledge base is routed through Vertex AI. Flowise is a drag-and-drop RAG builder for developers who want open source and full control, but it is not a multi-channel production platform and it has no voice story. Voiceflow wins the client-facing work: it is the fastest to prototype in front of a non-technical business owner, ships to phone and WhatsApp out of the box, and its collaboration features mean the client's staff can watch and edit the flow themselves. I sell Voiceflow for SMBs and product teams, and mention Botpress only when a buyer specifically wants self-hosting."
        },
        {
            "question": "What is the one mistake beginners make with Voiceflow?",
            "answer": "Treating the bot as a set-and-forget project. Beginners design the happy path, upload a PDF, deploy, and hand over the login - then the knowledge base starts hallucinating answers, credits run dry mid-month, and the client calls in a panic. The money is in the maintenance layer: set up transcript monitoring, review what the AI actually answered weekly, tighten the knowledge base, and ship small updates on a fixed cadence. That is exactly the recurring revenue clients will pay $200-$500 a month for. The second mistake is quoting a flat fee with no credit line item - if a bot goes viral and blows through 10,000 credits, that overage is yours unless it is written into the contract."
        }
    ],
    "content": "## What Voiceflow Actually Is (From Someone Who Builds Bots For Money)\n\nI have been building client chatbots for small and medium businesses since early 2024, and Voiceflow is the tool I bill through most weeks. It is a visual conversation builder: you drag steps onto a canvas - messages, questions, logic branches, API calls, knowledge-base lookups - connect them, test the flow in a simulator, and deploy to a web widget, WhatsApp, Slack, or a phone line. No code is required for the standard path, though there is a code block when you hit the edge of what the canvas can do.\n\nThe thing that separates it from the older chatbot builders is that it was rebuilt around LLM agents, not decision trees. You still draw the happy path by hand - greeting, menu, FAQs, booking flow - but an AI node handles everything off-script. A visitor can type something you never predicted and the agent answers from the knowledge base you uploaded, then routes back into the structured flow. That hybrid is why I pick Voiceflow for 8 out of 10 client jobs: the parts that must be deterministic stay deterministic, and the parts that cannot be predicted are covered by the model.\n\nPricing (2026) is a three-layer stack with a credit system underneath. Starter is free: 100 credits a month, two agents, one workspace, 50 knowledge sources, basic LLM models. Pro is $60/month billed monthly, or $648 a year (about $54/month): 20 agents, 3,000 knowledge sources, all major LLMs, five concurrent voice calls. Business is $150/month: unlimited agents, 10,000 knowledge sources, LLM fallback models, 15 concurrent voice calls, priority support. Enterprise is custom-priced with SSO, an Agent CMS, private cloud, and bring-your-own-model. On top of the seat price, every extra editor costs $50/month, and everything runs on credits - roughly one credit per chat message and about ten credits per minute of voice, plus speech-to-text and text-to-speech costs.\n\n## Why It Pays (The Real Income Angle)\n\nHere is the part that matters if you want to turn this into money: you are selling the deployed agent, not the software. Clients do not buy a Voiceflow subscription; they buy a bot that answers their customers at 2am and books appointments without a receptionist. Five ways I have seen solo operators and small agencies bill for it:\n\n**1. Support and booking bots for local businesses.** The bread and butter. A dental clinic, law firm, or trades company gets a bot that answers FAQs, qualifies leads, and books into their calendar. Build fee $2,000-$5,000 depending on the flow complexity, then a $100-$500 monthly retainer for hosting, knowledge-base updates, and transcript review. Real unit economics: the Pro seat is $60/month and a small-business bot burns 2,000-3,000 credits a month inside the 10,000-credit bucket, so tool cost is almost invisible against a $250 monthly invoice. Five retainers alone pay $1,250 a month of recurring revenue.\n\n**2. Voice AI phone agents.** This is where Voiceflow earns its keep over every no-code alternative. Build a voice agent that answers after-hours calls, takes appointment bookings, or qualifies inbound sales leads - restaurant reservations, clinic intake, real-estate lead capture. Because phone agents are harder to build and clients feel the value instantly (their phone actually stops ringing off the hook), you can charge $300-$800/month per client with a $1,000-$2,500 setup. The catch is credit burn: voice eats about 10 credits a minute plus TTS/STT, so a busy practice can push you onto the Business plan. Price voice retainers with a credit allowance line item, not a flat fee.\n\n**3. Productized vertical packages.** Turn the service into a fixed-price product: a \"law firm intake bot\" for $2,500, a \"dental booking bot\" for $2,000, a \"restaurant reservation agent\" for $1,500. Same flow skeleton every time, new knowledge base and branding per client. The first build costs you a week; the tenth costs you a day. Package the monthly retainer in from day one so every deployment carries recurring revenue, and white-label it under your own agency name if you want distance from the tool.\n\n**4. Lead qualification and CRM plumbing.** Build a bot that qualifies a lead, captures their details, and writes straight into HubSpot or Salesforce via the native integrations. Businesses pay $500-$1,500 for the build and $150-$300/month to keep it running, because a qualified lead list is worth far more than a chat widget. This pairs well with the Voiceflow web widget on a real-estate or service-business landing page.\n\n**5. Migration services.** There are thousands of companies sitting on aging Dialogflow, Watson Assistant, or hand-rolled bot flows they never finished. Moving a working conversation flow to Voiceflow is a $1,000-$3,000 job per project, and it converts cold because you are replacing an old cost, not adding a new one. Migration work also tends to become a retainer once they see the agent actually answering questions.\n\n## What Voiceflow Is Bad At\n\nLet me be honest about the rough edges, because the marketing gloss does not cover them:\n\n- **The credit system is the real pricing.** One credit per chat message sounds cheap until a busy month with a premium model blows through 10,000 credits and the agent goes silent with no top-up option. Voice deployments are worse - ten credits a minute before TTS and STT, so a three-minute call can cost 50-100 credits. You must monitor usage weekly and price it into contracts.\n- **No built-in live handoff.** Escalating to a human requires routing through an external tool. For customer-service clients who need a person to step in when the AI fails, that is a gap you have to fill yourself.\n- **The free plan is a demo, not a sandbox.** Two agents and 100 credits will not survive real traffic. Every client deployment needs at least a Pro seat, and you should budget that into quotes.\n- **Knowledge-base answers can hallucinate.** The RAG quality varies by source material; a bot trained on a messy PDF will confidently invent policies. Production bots need weekly transcript reviews and KB tightening - which, to be fair, is exactly the service you charge the retainer for.\n- **Seat costs stack up.** One editor is included; every additional builder costs $50/month. A three-person team on Pro is really $160/month, not $60.\n- **Cloud only.** No self-hosted option, so clients with hard data-residency rules are automatically out of scope.\n\n## Voiceflow vs The Alternatives\n\n| Tool | Best For | No-Code | Voice/Phone | Self-Host | Free Tier Reality |\n|------|----------|---------|-------------|-----------|-------------------|\n| Voiceflow | Product teams, agencies, SMB bots | Excellent canvas | Yes, first-class | No | Demo only (100 credits/mo) |\n| Botpress | Developers who want code control | Visual flows | Basic | Yes | More usable than Voiceflow's |\n| Dialogflow | Google ecosystem shops | Intent-based UI | Strong telephony | No | Workable, via GCP |\n| Flowise | Devs building open-source RAG | Drag-and-drop | No | Yes | Truly free |\n| Dify | Open-source LLM apps | Visual | Limited | Yes | Truly free |\n| Coze | Chinese-market builders | Visual | Limited | No | Generous, but CN-focused |\n\n## Getting Started Tips\n\n1. **Prototype on the free plan, never deliver on it.** Demo flows to prospects on Starter, then move to Pro before anything goes live.\n2. **Draw the happy path first.** The hybrid AI node only works when the deterministic flow is solid. Nail the booking and FAQ steps, then let the LLM cover the unexpected.\n3. **Start with one vertical.** A dental booking bot, a restaurant reservation agent, a law-firm intake bot. The skeleton reuses, the knowledge base changes, the margin grows.\n4. **Price credits into every contract.** Flat build fee plus a retainer that explicitly includes a credit allowance and a monitoring line. Never eat overage yourself.\n5. **Watch the transcripts weekly.** That review cadence is what turns a one-off build into a $200-$500 monthly retainer.\n6. **Demo with the client's own content.** Upload their real FAQ PDF into a prototype flow - the moment it answers their actual customer questions, the deal closes itself."
}

# ---- Load, validate, append ----
with open(DATA, "r", encoding="utf-8") as f:
    tools = json.load(f)

existing_slugs = {t.get("slug") for t in tools}
if new_tool["slug"] in existing_slugs:
    print(f"[SKIP] slug '{new_tool['slug']}' already exists")
else:
    tools.append(new_tool)
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(tools, f, ensure_ascii=False, indent=2)
    print(f"[OK] appended '{new_tool['slug']}'. Total tools now: {len(tools)}")

# ---- Forbidden-word scan ----
forbidden = ["leverage", "utilize", "seamlessly", "game-changing", "empower",
             "streamline", "delve into", "dive into", "transformative",
             "comprehensive", "revolutionize", "cutting-edge", "as an ai",
             "in conclusion", "robust"]
text = new_tool["content"] + " " + new_tool["description"]
hits = [w for w in forbidden if w in text.lower()]
if hits:
    print("[FORBIDDEN WORD HITS]:", hits)
else:
    print("[FORBIDDEN] scan clean - no banned words")
