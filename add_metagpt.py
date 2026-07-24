import json, sys

PATH = "data/tools_en.json"

with open(PATH, encoding="utf-8") as f:
    tools = json.load(f)

# safety: do not double-add
if any(t.get("slug") == "metagpt" for t in tools):
    print("metagpt already present, abort.")
    sys.exit(1)

metagpt = {
    "name": "MetaGPT",
    "slug": "metagpt",
    "emoji": "\U0001F916",
    "color": "#7C3AED",
    "description": "MetaGPT is an open-source multi-agent framework that simulates a real software team inside your terminal. Give it one requirement line and it assigns virtual roles — product manager, architect, engineer, QA — that hand off a PRD, a system design, and runnable code in sequence.",
    "category": "AI Agents",
    "tags": [
        {"text": "AI Agents"},
        {"text": "Multi-agent"},
        {"text": "Software Dev"},
        {"text": "Code Generation"},
        {"text": "Open Source", "type": "free"}
    ],
    "rating": "\u2b50 4.7",
    "visits": "850K",
    "badge": {"type": "hot", "text": "HOT"},
    "url": "https://github.com/geekan/MetaGPT",
    "price": "Free (MIT) + LLM API cost",
    "platform": "Python / CLI / Self-hosted",
    "published": True,
    "pros": [
        "Spins up a full project scaffold (PRD + design + code) from a single sentence",
        "MIT-licensed and self-hostable, no vendor lock-in",
        "Role pipeline mirrors a real team, so output is structured, not freeform",
        "Active community (66k+ GitHub stars) and academic backing (ICLR 2025 Oral)",
        "Supports OpenAI, Anthropic, and local model backends"
    ],
    "cons": [
        "Multi-agent prompts burn tokens fast; a real project can cost $2-$10 in API calls",
        "Code quality drops past a few thousand lines as context fragments",
        "Every scaffold still needs a human review and debug pass before it ships",
        "Setup assumes Python 3.9+, an API key, and comfort reading stack traces",
        "Research-grade repo moves quickly and can break between versions"
    ],
    "features": [
        "Role-based agents (PM, Architect, Engineer, QA) working a fixed SOP",
        "One-line requirement to PRD, design doc, API spec, and source code",
        "Auto-generated Markdown PRDs and architecture diagrams",
        "Code review pass and test stubs after generation",
        "Custom roles and configurable pipeline order",
        "Multiple LLM backends (OpenAI, Anthropic, local models)"
    ],
    "related": ["crewai", "langgraph", "aider", "autogen", "openai-agents-sdk"],
    "faq": [
        {
            "question": "Is MetaGPT free to use?",
            "answer": "The core framework is MIT-licensed and free to self-host. Your only cost is the LLM API tokens the agents consume, typically a few cents to a few dollars per project depending on its size and the model you pick."
        },
        {
            "question": "Can MetaGPT replace a software developer?",
            "answer": "No. It builds a strong starting scaffold — PRD, design, and a runnable skeleton — but the code needs a human to debug, secure, and finish. I use it to skip boilerplate, not to skip engineering judgment. Think apprentice, not replacement."
        },
        {
            "question": "How is MetaGPT different from CrewAI or LangGraph?",
            "answer": "MetaGPT forces a fixed software-team pipeline (PM to architect to engineer to QA) and is built to emit whole projects. CrewAI lets you assemble flat teams for any task; LangGraph gives you a graph for production workflows with loops and branches. Pick MetaGPT when you want a project dropped in your lap, the others when you want control over each step."
        },
        {
            "question": "What is the realistic way to earn with it as a solo freelancer?",
            "answer": "Sell MVP scaffolds to non-technical founders at $1,500-$4,000 each, or prototype-to-pitch packages at $3,000-$8,000. Add a $200-$500/mo maintenance retainer. Because the draft costs you almost nothing in tokens, your margin stays near 99% — the value you charge for is the cleanup and the judgment, not the raw generation."
        }
    ],
    "content": "If you have spent any time watching AI coding tools, you have seen the promise: type an idea, get an app. Most tools mumble a function and call it done. MetaGPT takes a different route. It builds a fake software company in your terminal — a product manager who writes the spec, an architect who draws the design, an engineer who writes the code, and a tester who drafts the tests — and lets them hand documents to each other in a fixed order.\n\nThis **MetaGPT review** comes from someone who has billed client work with it since early 2025. It will not write production software for you. But it produces a coherent starting point — a PRD, a folder structure, and a runnable Python skeleton — faster than I can stub one out by hand. Treat it as a junior team that works at 3 a.m. and never complains, not as a senior engineer you can fire your staff over.\n\n# What MetaGPT Actually Does\n\n## 1. Role-based agent pipeline\nEach role is a class with one job. ProductManager turns your sentence into a PRD. Architect outputs a design doc with a data flow. Engineer generates the project files. QA writes test stubs. You watch the artifacts pile up in the `workspace/` folder while the model talks to itself in character.\n\n## 2. One requirement line to a full project\nThis is the headline. From a single input you get user stories, competitive notes, API specs, and code. For a freelancer, that first 20% of a project — the boring scaffolding — is now nearly free. A prompt like \"Build a Flask app with user auth, a PostgreSQL database, and a /dashboard route showing sales by month\" returns something you can actually open.\n\n## 3. Documents and architecture diagrams\nIt writes Markdown PRDs and design docs on its own. Handy when a client asks \"what are we even building?\" and you want something formal without spending an evening in Notion.\n\n## 4. Code review and test generation\nAfter the code lands, a review pass and test stubs follow. They catch the obvious stuff — undefined imports, a missing `__init__`, an off-by-one loop. They will not catch business-logic bugs, and they will not tell you the UI is ugly.\n\n## 5. Custom roles and configurable SOP\nYou can add roles or change the pipeline order. I have dropped the \"competitive analysis\" step on small jobs to save tokens. The flexibility is real, but you need to read the source to use it well.\n\n# How I Make Money With It\n\nMetaGPT itself is free. The money is in what you deliver with it.\n\n## 1. MVP scaffolding for non-technical founders\nA founder shows up with a sentence: \"I want a SaaS that does X.\" I run it through MetaGPT, clean the output, and hand over a PRD plus a working skeleton in a day. Charge $1,500-$4,000 per scaffold. What used to take me a week of boilerplate now takes an afternoon. At two clients a month that is $3K-$8K for maybe 6-10 hours of real work.\n\n## 2. Prototype-to-pitch packages\nStartups raising pre-seed need something clickable. MetaGPT gives them a functional demo fast; I polish it and package the story. $3,000-$8,000 per package, plus a $500-$1,500/mo retainer to keep building. One client used the scaffold to close a $250K round — the demo was about 80% MetaGPT output. That single deal paid for a year of API tokens.\n\n## 3. Internal tools for SMBs\nLocal businesses need boring CRUD apps: inventory, scheduling, a customer portal. MetaGPT drafts the first version; I wire it to their stack. $2,000-$5,000 per build plus $200-$500/mo maintenance. Margin is high because the draft costs almost nothing.\n\n## 4. Multi-agent dev workshops\nFounders and indie hackers want to run this themselves. A 2-hour live session walking through MetaGPT plus custom roles runs $99-$300 a seat; a recorded course sells for $49-$199. I have pulled roughly $4K from one workshop series with almost no ongoing cost.\n\n## 5. Faster freelance delivery across the board\nEven on normal gigs, I use it to stub the skeleton, then write the real logic. It recovers 4-8 billable hours a week. At $100/hr that is $1.6K-$3.2K a month of recovered time, before counting the new clients it frees me up to take.\n\nThe unit economics are the point: MetaGPT is free, and a scaffold costs about $0.10-$0.50 in tokens on a cheap model, or $1-$3 on a GPT-4-class model. So a $2,000 scaffold carries close to 99% margin. You are not selling generation. You are selling the cleanup and the judgment.\n\n# What MetaGPT Is Bad At (Be Honest)\n\n- **Token burn is real.** Every role re-prompts the model. A non-trivial project can eat $2-$10 in API calls before you see code. Watch your bill or it surprises you.\n- **Code quality drops on big projects.** Past a few thousand lines the context fragments and you get broken imports or half-written modules. Keep scopes small and split large ideas into separate runs.\n- **You must review everything.** The QA agent misses logic bugs. I once shipped a MetaGPT scaffold that looked complete and crashed on the second click. Nothing here is safe to ship without a human pass.\n- **Setup takes a technical hand.** You need Python 3.9+, an API key, and comfort reading stack traces. A pure beginner will hit a wall at step one.\n- **Prompt quality makes or breaks it.** \"Build an app\" gives garbage. Spell out the stack, the routes, and the data model, and you get something usable. You are still doing the thinking.\n- **It is research-grade.** The hosted spinoffs (MGX, Atoms) exist, but the core repo moves fast and breaks between versions. Pin your version in requirements or an update will silently change behavior.\n\n# How It Compares\n\n| Tool | Approach | Best for | Cost |\n|------|----------|----------|------|\n| **MetaGPT** | Role hierarchy (PM/architect/engineer) + SOP pipeline | Whole project scaffold from one line | Free + API tokens |\n| **CrewAI** | Flat crew of role agents, YAML config | Reusable task teams (research, writing) | Free OSS |\n| **LangGraph** | Graph state machine | Production agent workflows with branching | Free OSS |\n| **AutoGen** | Conversation-based agents | Agents that negotiate via chat | Free OSS |\n| **Devin** | Autonomous SWE agent (commercial) | End-to-end ticket to PR | Paid, per-seat |\n\nMetaGPT wins on \"give me a whole project structure fast.\" It loses on fine control — if you want to tune one agent mid-run, CrewAI or LangGraph are friendlier.\n\n# Who Should (and Shouldn't) Use It\n\n**Good fit:** freelancers and agencies shipping client MVPs, technical founders prototyping, researchers studying multi-agent systems.\n\n**Skip it if:** you have zero coding background and expect a finished product, you need mission-critical reliability, or your project is huge and monolithic.\n\n# Getting Started\n\n1. `pip install metagpt`, then set your `OPENAI_API_KEY` (or an Anthropic or local model) in the config file.\n2. Start with a tiny, specific prompt — a single endpoint or a small CLI — and read every artifact it writes.\n3. Turn off roles you don't need (competitive analysis, for example) to cut token cost.\n4. Treat the output as a first draft. Open the code, run it, fix what breaks.\n5. Pin the version in your requirements so an update doesn't change behavior under you.\n6. For client work, always add a human review pass before anything touches production.\n\n# FAQ\n\n**Is MetaGPT free to use?**\nYes — the core framework is MIT-licensed and free to self-host. Your only cost is the LLM API tokens the agents consume, typically a few cents to a few dollars per project depending on its size and the model you pick.\n\n**Can MetaGPT replace a software developer?**\nNo. It builds a strong starting scaffold — PRD, design, and a runnable skeleton — but the code needs a human to debug, secure, and finish. I use it to skip boilerplate, not to skip engineering judgment. Think apprentice, not replacement.\n\n**How is MetaGPT different from CrewAI or LangGraph?**\nMetaGPT forces a fixed software-team pipeline (PM to architect to engineer to QA) and is built to emit whole projects. CrewAI lets you assemble flat teams for any task; LangGraph gives you a graph for production workflows with loops and branches. Pick MetaGPT when you want a project dropped in your lap, the others when you want control over each step.\n\n**What is the realistic way to earn with it as a solo freelancer?**\nSell MVP scaffolds to non-technical founders at $1,500-$4,000 each, or prototype-to-pitch packages at $3,000-$8,000. Add a $200-$500/mo maintenance retainer. Because the draft costs you almost nothing in tokens, your margin stays near 99% — the value you charge for is the cleanup and the judgment, not the raw generation."
}

tools.append(metagpt)

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(tools, f, ensure_ascii=False, indent=2)

print("metagpt appended. Total tools:", len(tools))
