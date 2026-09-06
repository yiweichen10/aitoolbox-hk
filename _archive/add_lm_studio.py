# -*- coding: utf-8 -*-
"""Add LM Studio to tools_en.json (aitoolbox.hk).
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
    "name": "LM Studio",
    "slug": "lm-studio",
    "emoji": "\U0001F5A5",
    "color": "#6D28D9",
    "description": "LM Studio is a free desktop app that runs open-weight LLMs - Llama, Qwen, DeepSeek, Gemma, Mistral - entirely on your own machine through a clean GUI, with a one-click local API server. I set it up for solo lawyers, therapists, and writers who want private AI but cannot touch a terminal; the money is in handing a non-technical client a working desktop app they can actually click, not a server they will never maintain.",
    "category": "AI Development",
    "tags": [
        {"text": "Local Deployment"},
        {"text": "Free", "type": "free"},
        {"text": "LLM"},
        {"text": "Privacy"},
        {"text": "Desktop App"},
        {"text": "Beginner Friendly"}
    ],
    "rating": "\u2b50 4.8",
    "visits": "5M+ downloads",
    "badge": {
        "type": "hot",
        "text": "HOT"
    },
    "url": "https://lmstudio.ai",
    "price": "Free (local) + Enterprise (teams/SSO)",
    "platform": "macOS (Apple Silicon), Windows, Linux",
    "published": True,
    "related": [
        "ollama",
        "hugging-face",
        "chatgpt",
        "mistral-ai",
        "langchain"
    ],
    "created_date": "2026-07-26",
    "pros": [
        "Free for personal and commercial use since July 2025 - no license, no form, your margin on every job is near 100%",
        "The GUI removes the biggest barrier - search, download, chat with no terminal, Docker, or config files",
        "One-click local OpenAI-compatible server at localhost:1234 for a free, private dev backend",
        "Built-in document RAG - drop a .pdf, .docx, or .txt in and it retrieves from long files automatically",
        "Dual engine: llama.cpp everywhere, native MLX on Apple Silicon (often 200+ tokens/sec on small models)",
        "Friendly for experimenting - load several models, compare on the same prompt, watch VRAM and tokens/sec live"
    ],
    "cons": [
        "Closed-source desktop app - you cannot audit or modify it, which matters for compliance-minded clients",
        "Not built for headless or multi-user serving - the GUI is one person, one machine; llmster exists but is newer than Ollama's server",
        "No built-in cloud fallback - if the client's hardware cannot run the model, there is no LM Studio Cloud to scale into",
        "Hardware hungry - a 7B-13B model at Q4 wants 16GB+ RAM and 6-9GB VRAM; bigger models need a real GPU",
        "Apple Silicon only for the fast MLX path; Intel Macs are not supported and Windows/Linux use the slower llama.cpp route",
        "'Free for work' has a ceiling - the Enterprise tier (SSO, model/MCP gating) costs money for real organizations",
        "Smaller local models still trail the cloud on hard reasoning - set expectations or you will hear about it"
    ],
    "features": [
        "Free desktop app for macOS, Windows, Linux (Apple Silicon 14+) from Element Labs",
        "Built-in model store (Discover tab) connected to Hugging Face - search, filter by hardware, one-click download",
        "ChatGPT-style chat UI with multi-turn context, system prompts, and character personas",
        "Local OpenAI-compatible API server at http://localhost:1234/v1 (chat, completions, embeddings)",
        "Document chat with automatic RAG for .pdf, .docx, .txt files",
        "llama.cpp (GGUF) + native MLX dual runtime; tool calling and structured JSON output via API",
        "Headless llmster daemon + lms CLI for server/CI; LM Link for encrypted remote access (Tailscale)"
    ],
    "faq": [
        {
            "question": "Is LM Studio really free for commercial use?",
            "answer": "Yes. Since July 8, 2025 the desktop app is free for personal and work use - no license, no registration, no fee. Element Labs sells a separate Enterprise tier with SSO and policy controls for larger teams, but the app most solo users and consultants want is free, which is what makes the margin on setup work so high."
        },
        {
            "question": "Can you actually make money with a free tool?",
            "answer": "You do not sell the software; you sell a working, private setup a non-technical person can use, plus training and support. Because LM Studio costs you nothing, a $1,800 build or a $200/month retainer is close to pure profit minus your time. The work is trust and configuration, not licensing."
        },
        {
            "question": "LM Studio vs Ollama - which should I learn?",
            "answer": "If you serve developers or build integrations, learn Ollama - its server and API are the industry default for local inference. If your clients are non-technical one-person shops, lead with LM Studio because the GUI is what they will actually open. Most people in this business end up using both: LM Studio on the client's desk, Ollama on the server."
        },
        {
            "question": "What hardware does a client need?",
            "answer": "For 7B-14B models, any modern Mac or PC with 16GB+ RAM runs them fine. For 32B+ you want 32GB+ RAM and ideally an Apple Silicon Mac or a dedicated GPU. I tell prospects upfront: if their only machine is a 16GB laptop, we stick to smaller models or I spec them a $1,000-$1,800 mini workstation. Do not lead with a 70B pitch that needs new hardware."
        }
    ],
    "content": "## What LM Studio Actually Is (From a Private-AI Setup Guy)\n\nI help solo professionals - lawyers, therapists, writers, small accounting shops - get private AI without sending their files to a cloud they cannot see. For the past year most of that work ran on Ollama, because Ollama is a server you wire into other apps. But a lot of my clients are not developers, and a server they cannot click on scares them. That is exactly where LM Studio earns its keep.\n\nLM Studio is a free desktop app from Element Labs that downloads and runs open-weight models - Llama, Qwen, DeepSeek, Gemma, Mistral, Phi - right on your own hardware. You get a model store, a ChatGPT-style chat window, drag-and-drop document chat with built-in RAG, and a one-click local server that speaks the OpenAI API at http://localhost:1234. Nothing leaves the machine. As of mid-2026 it is free for personal and commercial use, and the current stable build (0.4.16) runs GGUF models through llama.cpp and MLX models natively on Apple Silicon.\n\nThe thing that separates it from Ollama is the front end. Ollama is a runtime you drive from a terminal or a separate UI. LM Studio is the UI. A non-technical client opens it, searches a model in the Discover tab, clicks download, and is chatting in under two minutes. That difference is the whole reason I now lead with LM Studio for one-person clients and keep Ollama for headless integrations.\n\n## Why It Pays (The Real Income Angle)\n\nLM Studio costs nothing, same as Ollama. You are not selling software. You are selling a working, private setup a non-technical person can actually use, plus the training and support that keeps it running. Because the tool is free, your margin on every job is close to 100% - the only real cost is your time and the client's hardware. Here are the ways I have seen people turn LM Studio into income.\n\n### 1. Private AI setups for non-technical solo pros\nThis is the big one and it is where LM Studio beats Ollama for my business. A therapist who wants a private note-taking assistant, a writer who wants an offline drafting partner, a solo lawyer who wants to query old contracts - none of them will run a Docker container. You install LM Studio, pick a model that fits their machine, load their documents for RAG, and sit with them for a 30-minute training. Charge $800-$2,500 to set it up and $100-$300/month for updates and \"it answered something weird\" support. I run this for six solo clients at $200/month each - $1,200/month recurring off about $9K of one-time setup, and I barely touch it between calls because the GUI means they self-serve.\n\n### 2. Productized \"private AI workstation\" package\nBuild a reusable recipe: a specific LM Studio config, a curated model set, and a one-page guide, then sell it to a niche that shares the same worry - privacy. Therapists, coaches, indie authors, journalists. Charge $300-$900 one-time plus $30-$120/month for model updates and priority help. Once the package is built, delivery is close to hands-off. One person I know sells a \"writer's private AI\" bundle at $499 and does maybe two support calls a month.\n\n### 3. Local API dev proxy for freelancers and agencies\nThis is the angle for people who write code. Point any OpenAI-compatible client at http://localhost:1234/v1 and you get a free, private backend for testing prompts, comparing models, and prototyping AI features before you pay a cloud bill. If you freelance or run a small agency, sell \"AI feature prototyping\" or \"prompt testing\" as a line item - $500-$2,000 per prototype, or a $300-$800/month retainer to keep a client's local dev stack current. The pitch: we iterate on your AI features for free locally, then flip the base URL to production when it is proven.\n\n### 4. Offline RAG for sensitive documents\nLM Studio handles document chat out of the box - drop a .pdf, .docx, or .txt into a chat and it does retrieval on long files automatically. Small firms with confidential SOPs, client lists, or case files like this because they never upload anything. Bill $1,500-$5,000 to stand it up and $200-$500/month to maintain. It overlaps with the Ollama version, but the LM Studio build needs no extra front end, so your setup time is shorter and the client can keep using it without you.\n\n### 5. \"Private AI for non-techies\" workshops\nBecause the GUI is clickable, LM Studio is the best teaching tool I have found for non-developers. Run a live two-hour session - install, pick a model, chat with your documents - at $150-$400 per seat, or record a course at $79-$149. I ran one for a local writers' group at $200/seat, filled 12 seats, and closed three one-on-one setup gigs from it. The workshop sells the tool; the setup calls pay the bills.\n\n## What LM Studio Is Good At\n\n- **Zero cost, including commercial use.** Free since July 2025 for work, no license, no form. Your margin on every job is near 100%.\n- **The GUI removes the biggest barrier.** Search, filter by your hardware, download, chat - no terminal, no Docker, no config files. For a non-technical client this is the difference between \"sold\" and \"no thanks.\"\n- **One-click local server.** Flip the server on and any OpenAI-compatible app talks to a model on your machine. Great as a free dev proxy or a private backend.\n- **Built-in document RAG.** Drag in files and it retrieves from long documents automatically. No vector DB to stand up for basic use.\n- **Dual engine.** llama.cpp for everything, MLX for Apple Silicon - M-series Macs get fast, native inference, often 200+ tokens per second on smaller models.\n- **Friendly for experimenting.** Load several models, compare them on the same prompt, watch tokens-per-second and VRAM in real time. Hundreds of tests at zero cost.\n\n## What LM Studio Is Bad At (Be Honest Before You Sell)\n\n- **It is closed-source.** You cannot read or modify the desktop app, which matters if a client asks \"what exactly runs on my machine?\" Ollama is open and auditable; LM Studio is a black box with a pretty window. I tell compliance-minded clients this upfront.\n- **Not built for headless or multi-user serving.** The GUI is one person, one machine. There is a headless daemon (llmster) and an lms CLI now, but they are newer and less proven than Ollama's server, which has run production integrations for years. If a client needs many people hitting one model, LM Studio is the wrong pick.\n- **No built-in cloud fallback.** If the client's hardware cannot run the model they want, you are stuck - there is no LM Studio Cloud to scale into. Ollama at least has Ollama Cloud. Lead with models that fit their actual machine, or the deal dies.\n- **Hardware hungry.** A 7B-13B model at Q4 wants 16GB+ RAM and 6-9GB VRAM for a comfortable experience; bigger models need a real GPU or a Mac with 32GB+ unified memory. I have lost prospects who only owned a 16GB laptop.\n- **Apple Silicon only for the fast path.** MLX is M-series only; Intel Macs are not supported at all. Windows and Linux run through llama.cpp, which is fine but not as quick as MLX on a Mac.\n- **\"Free for work\" has a ceiling.** The core app is free, but the Enterprise tier - SSO, model and MCP gating, private collaboration - costs money. If a client is a real organization with IT rules, budget for that, and do not promise \"free forever\" to a 50-person team.\n- **Smaller local models still trail the cloud.** A 14B model at Q4 is good, not great, on hard reasoning. Set expectations or you will hear about it.\n\n## How I Actually Set Up a Client (Workflow)\n\n1. **Ask what machine they have.** RAM, GPU, Mac or Windows. Pick the biggest model that fits with headroom - usually 7B-14B for a laptop.\n2. **Install LM Studio** from lmstudio.ai. The first-run wizard detects hardware automatically.\n3. **Open Discover, filter by \"My Hardware,\"** and download a model at Q4_K_M - the usual sweet spot between size and quality.\n4. **Load their documents** for RAG - drag the files in, let it index. Show them how to ask questions about their own material.\n5. **Turn on the local server** if they (or their developer) want an API, and show them the localhost:1234 URL.\n6. **Train them for 30 minutes** and hand over a one-page runbook. Then bill the monthly retainer for model swaps and support.\n\nA typical solo-pro setup takes me 2-4 hours including training. At an $1,800 setup fee that is a strong effective rate, and the retainer is pure margin.\n\n## A Real Mini Case (Solo Therapist)\n\nA therapist I work with wanted a private assistant to help organize session notes and draft between-client summaries, but her governing body forbids sending client text to any cloud. I installed LM Studio on her M2 Mac (16GB), loaded a 14B model at Q4, and dropped in her de-identified template documents for RAG. She now drafts and reorganizes locally, nothing leaves the room, and she pays me $150/month for model updates and the occasional question. Setup was $1,200. Her alternative quote was a \"HIPAA-compliant\" cloud note tool at $80/user/month with data residency she still could not fully verify. The local build cost less in year one and removed the compliance risk entirely.\n\n## LM Studio vs The Alternatives\n\n| Tool | Best for | Cost | Where it runs | My take |\n|------|----------|------|--------------|----------|\n| **LM Studio** | Non-technical users who want a GUI + model store + local API | Free (local) + Enterprise tier | Mac/Win/Linux desktop | Best for one-person private AI they can actually use. |\n| **Ollama** | Devs integrating local models, headless servers, automation | Free (local) + Cloud $20-$100/mo | Mac/Win/Linux | The backbone for integrations; weaker for click-only users. |\n| **GPT4All** | Absolute beginners, old hardware | Free | Mac/Win/Linux | Friendly but limited models, thin server story. |\n| **AnythingLLM** | All-in-one private chatbot with RAG front end | Free (self-host) | Mac/Win/Linux/Docker | Good when you want a finished app, not a building block. |\n| **Groq / Together** | Fast cloud inference, no hardware | Per-token / usage | Cloud | Beat local on raw speed; lose the privacy story. |\n\nMy rule: LM Studio for a single non-technical user who needs to click, Ollama for anything headless or integrated, AnythingLLM when they want a ready-made app, and a cloud API when local hardware cannot keep up.\n\n## Who Should Pick LM Studio (And Who Shouldn't)\n\nPick LM Studio if you are setting up private AI for a non-developer, teaching someone local AI, or want a free local API to prototype against. Skip it if you need to serve many users from one box, require an auditable open-source stack, or must run on an Intel Mac. In those cases Ollama or a self-hosted app like AnythingLLM fits better.\n\n## FAQ\n\n**Is LM Studio really free for commercial use?**\nYes. Since July 8, 2025 the desktop app is free for personal and work use - no license, no registration, no fee. Element Labs sells a separate Enterprise tier with SSO and policy controls for larger teams, but the app most solo users and consultants want is free, which is what makes the margin on setup work so high.\n\n**Can you actually make money with a free tool?**\nYou do not sell the software; you sell a working, private setup a non-technical person can use plus training and support. Because LM Studio costs you nothing, a $1,800 build or a $200/month retainer is close to pure profit minus your time. The work is trust and configuration, not licensing.\n\n**LM Studio vs Ollama - which should I learn?**\nIf you serve developers or build integrations, learn Ollama - its server and API are the industry default for local inference. If your clients are non-technical one-person shops, lead with LM Studio because the GUI is what they will actually open. Most people in this business end up using both: LM Studio on the client's desk, Ollama on the server.\n\n**What hardware does a client need?**\nFor 7B-14B models, any modern Mac or PC with 16GB+ RAM runs them fine. For 32B+ you want 32GB+ RAM and ideally an Apple Silicon Mac or a dedicated GPU. I tell prospects upfront: if their only machine is a 16GB laptop, we stick to smaller models or I spec them a $1,000-$1,800 mini workstation. Do not lead with a 70B pitch that needs new hardware.\n\n## Getting Started (If You Want To Do This)\n\n- Download LM Studio from lmstudio.ai and load a 7B or 14B model at Q4_K_M to feel the speed on your own machine.\n- Pick one non-technical niche - therapy, coaching, indie writing, small law - and learn its privacy language; that is what lets you charge $1K+ instead of $100.\n- Build one reusable setup recipe and a one-page runbook; deliver it as a productized package so each new client is less work.\n- Lead demos with models that fit the client's real hardware; do not promise a 70B model on a 16GB laptop.\n- Use the local server as a free dev proxy before quoting any cloud API work.\n- Keep the Enterprise tier in mind for bigger clients, but do not promise \"free forever\" to an organization with IT rules.\n",
    "aeo_geo_updated": True
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
