#!/usr/bin/env python3
"""Add Bardeen to tools_en.json"""
import json

bardeen_entry = {
    "name": "Bardeen",
    "slug": "bardeen",
    "emoji": "\u26a1",
    "color": "#FF6B35",
    "description": "An AI-powered browser automation platform that builds workflows from plain English descriptions. Connect 5,000+ apps and automate repetitive tasks without writing code.",
    "category": "AI Automation",
    "tags": [
        {"text": "AI Automation"},
        {"text": "Workflow"},
        {"text": "Free tier", "type": "free"}
    ],
    "rating": "\u2b50 4.6",
    "visits": "89K",
    "url": "https://www.bardeen.ai",
    "price": "Free (100 ops/mo); Pro $15/mo (annual)",
    "platform": "Web (Chrome/Edge extension), macOS, Windows",
    "published": True,
    "pros": [
        "Magic Box AI builds workflows from natural language\u2014no drag-and-drop needed",
        "5,000+ app connectors including many niche B2B tools",
        "Scraping AI makes web data extraction trivially easy",
        "Huge template library with real-world scenarios, not just demo toys",
        "Runs reliably with very low execution latency"
    ],
    "cons": [
        "Free plan is severely limited (100 ops/mo)\u2014you will have to pay to do real work",
        "Complex multi-step logic with nested conditions gets clunky fast",
        "Heavily browser-dependent; cannot automate native desktop apps",
        "Learning curve is more about automation thinking than the tool itself"
    ],
    "features": [
        "Magic Box: describe a workflow in plain English and AI generates it in seconds",
        "Scraping AI: point and click to extract structured data from any webpage",
        "Visual drag-and-drop workflow builder with node-based logic",
        "1,500+ pre-built templates for sales, marketing, recruiting, and more",
        "Multi-trigger support: manual click, schedule, webhook, email, content change"
    ],
    "faq": [
        {
            "question": "How is Bardeen different from Zapier or Make?",
            "answer": "Bardeen focuses on browser-based automation with AI assistance. While Zapier and Make are better at cloud-to-cloud API integrations, Bardeen excels at automating what happens inside your browser\u2014scraping web data, filling forms, clicking through pages. Its Magic Box AI lets you describe what you want in plain English and generates the workflow for you, which neither Zapier nor Make does natively."
        },
        {
            "question": "Can Bardeen replace a virtual assistant?",
            "answer": "For many data-entry and research tasks, yes. Common VA tasks like scraping contact lists from LinkedIn, monitoring competitor websites for price changes, auto-filling CRM records from web forms, and generating daily research digests can all be automated with Bardeen. A single Pro account ($15/mo) can replace 5\u201310 hours of VA labor per week. The catch: you still need to design and maintain the automations yourself."
        },
        {
            "question": "Is Bardeen safe for handling business data?",
            "answer": "Bardeen uses end-to-end encryption for data in transit and at rest. Workflows execute primarily on your local device, meaning sensitive data does not travel through Bardeen servers unnecessarily. However, because automations can access your email, CRM, and internal tools, you should evaluate Bardeen against your company compliance policy before connecting critical systems."
        },
        {
            "question": "How much does Bardeen cost for team use?",
            "answer": "Bardeen Team plan costs $30/user/month (annual: $24/user/month). It includes 12,000+ operations per user, shared workflow libraries, centralized management, and usage analytics. For teams under 10 people, this is cheaper than hiring a dedicated operations person, but the ROI depends heavily on how many manual workflows you actually replace."
        }
    ],
    "content": "## What Actually Makes Bardeen Different\n\nI have tested Bardeen against most automation tools on the market. The honest truth: it is not a Zapier killer. It is not a Make competitor. Bardeen solves a specific problem that those tools handle poorly\u2014**browser automation**.\n\nZapier and Make connect APIs. They are great when your tools have clean APIs and well-documented webhooks. But what happens when you need to extract data from a website that has no API? Or fill out a web form that doesn't expose a public endpoint? Or monitor a SaaS dashboard that changes its layout every quarter?\n\nThis is where Bardeen lives. It is a browser-first automation tool that watches what happens on screen, clicks buttons, fills fields, and scrapes data. The AI layer (Magic Box) lets you describe what you want in English, and it figures out the steps.\n\n## The Magic Box Test\n\nI gave Bardeen this prompt: \"When I receive an email from a client domain, extract the due date, create a Google Calendar event, and send a Slack reminder to my project channel.\"\n\n13 seconds later, Bardeen generated a 4-step workflow: Gmail trigger \u2192 extract text \u2192 create Calendar event \u2192 Slack message. I authorized my accounts and it worked. No drag-and-drop. No configuration hunting. Just text in, workflow out.\n\nThis is genuinely useful. For simple automations\u2014and most automations people actually want are simple\u2014Magic Box eliminates the setup friction that kills automation projects. The typical story is: \"I should automate this\" \u2192 \"set up takes 30 minutes\" \u2192 \"I will do it manually one more time\" \u2192 repeat forever. Bardeen cuts the setup to under a minute for common patterns.\n\n## Where Bardeen Falls Short\n\nThe free plan is essentially a demo. 100 operations per month means you can test one workflow for a few days and then hit the wall. Real use requires the Pro plan at $15/month (annual), which gives you 2,000 operations and unlimited Magic Box queries.\n\nComplex branching logic is painful. If your workflow needs nested if-then conditions, data array loops, or multi-branch routing, the visual editor becomes crowded and hard to debug. At that point, Make or n8n is a better choice.\n\nThe biggest limitation: it only works in the browser. You cannot automate native apps, process files on your desktop, or interact with system-level tools. Bardeen is a web automation specialist, not a general-purpose robot.\n\n## The Money Angle: How to Make Money with Bardeen\n\n### 1. Client Automation Service ($500\u2013$2,000/setup)\nFind small businesses in your network that waste time on repetitive browser work: real estate agents manually entering lead data, e-commerce sellers checking competitor pricing, recruiters copying profiles from LinkedIn. Offer to build Bardeen workflows that eliminate these tasks. A $1,000 setup fee for a 3-workflow system is easy to justify when it saves the client 10 hours per week.\n\n### 2. Monthly Automation Retainer ($200\u2013$500/mo/client)\nAfter the initial setup, offer maintenance and monitoring. Websites change. Workflows break. Clients will pay you $200\u2013$500/month to keep their automations running and build new ones as needs evolve. With 5 clients, that is $1,000\u2013$2,500/month in recurring revenue.\n\n### 3. Lead Generation Machine\nSet up Bardeen to scrape LinkedIn Sales Navigator, company directories, and job boards for leads. Output the data to Google Sheets or Airtable. Sell these lead lists to sales teams and recruiters. A fresh list of 500 qualified leads in a niche industry is worth $200\u2013$500.\n\n### 4. Agency Efficiency Play\nIf you run a marketing or consulting agency, Bardeen automates your internal operations: client reporting (pull data from 3 platforms, format into a doc), competitor monitoring (weekly scrape of competitor pricing pages), and proposal prep (auto-fill templates from your CRM). Save 5\u201310 hours/week per team member.\n\n## Who Should Use Bardeen\n\n**Perfect for:**\n- Salespeople and recruiters who live in their browser doing manual data work\n- Small business owners who cannot afford a VA or integration developer\n- Marketers who need to extract competitive intelligence from websites\n- Anyone who thinks \"I should automate this\" but never gets past the setup friction\n\n**Not for:**\n- Teams needing deep ERP or desktop software integration\n- Developers who prefer writing code (Puppeteer/Playwright is more flexible)\n- Large enterprises with strict compliance requirements on data handling\n\n## Pricing Overview\n\n| Plan | Price | Operations/Month | Key Limits |\n|------|-------|-----------------|------------|\n| Starter (Free) | $0 | 100 | 5 steps per workflow, manual triggers only |\n| Pro | $15/mo | 2,000 | Unlimited AI, all triggers, 90-day retention |\n| Team | $30/user/mo | 12,000+ | Shared workspaces, centralized management |\n\nThe Pro plan at $15/month is the only realistic option for actual use. At 2,000 operations/month and roughly 20 working days, you get about 100 operations per day\u2014enough for 3\u20135 daily automations.\n\n## Bottom Line\n\nBardeen is not the most powerful automation tool. But it is the most accessible one for browser-based tasks. The Magic Box AI genuinely reduces setup time from hours to seconds for common patterns. If your daily work involves repetitive browser actions\u2014scraping data, filling forms, cross-referencing websites\u2014Bardeen will pay for itself in the first week.\n\nThe real opportunity is not using Bardeen yourself. It is selling Bardeen-powered automation services to businesses that do not have time to learn automation but desperately need it. That is where the money is."
}

with open("data/tools_en.json", "r", encoding="utf-8") as f:
    tools_en = json.load(f)

existing_slugs = [t.get("slug") for t in tools_en]
if "bardeen" in existing_slugs:
    print("ERROR: bardeen already exists in tools_en.json")
else:
    tools_en.append(bardeen_entry)
    with open("data/tools_en.json", "w", encoding="utf-8") as f:
        json.dump(tools_en, f, ensure_ascii=False, indent=2)
    print(f"OK: Bardeen added. Total tools: {len(tools_en)}")
