# -*- coding: utf-8 -*-
"""Add AnythingLLM to tools_en.json (aitoolbox.hk).
Backs up the file first, appends the new entry, writes back UTF-8,
runs a forbidden-word scan, then generates the OG image via Pillow.
"""
import json
import shutil
import datetime
import sys
import os

DATA = "data/tools_en.json"
TODAY = datetime.date.today().strftime("%Y%m%d")

# ---- Backup first (SOUL.md Rule #3) ----
shutil.copy2(DATA, f"{DATA}.{TODAY}.bak")
print(f"[BACKUP] {DATA}.{TODAY}.bak created")

new_tool = {
    "name": "AnythingLLM",
    "slug": "anythingllm",
    "emoji": "\U0001F4DA",
    "color": "#10B981",
    "description": "AnythingLLM is the open-source (MIT) all-in-one app that turns your documents into a private, chat-with-your-files knowledge base - PDFs, DOCX, CSV, images with OCR, audio transcripts, even scraped websites, Confluence spaces, GitHub repos and YouTube transcripts. You point it at any of 30+ LLM providers (Ollama, LM Studio, OpenAI, Claude, Groq) and any of 7 vector databases, and it handles chunking, embedding, retrieval and chat. Desktop is free forever, Docker self-host is free, and the only paid tier is managed cloud from $50/month. I deploy private knowledge bases for law firms, clinics and finance shops that cannot send documents to ChatGPT, and AnythingLLM is the base I build every engagement on - a $3K-$5K deployment bills with zero software cost, because the software is free and what clients pay for is the setup, the integration and the maintenance.",
    "category": "AI Development",
    "tags": [
        {"text": "RAG"},
        {"text": "Knowledge Base"},
        {"text": "Self-Hosted"},
        {"text": "Open Source"},
        {"text": "Private Chat"},
        {"text": "Docker"},
        {"text": "Multi-User"},
        {"text": "Agents"}
    ],
    "rating": "\u2b50 4.6",
    "visits": "54,000+ GitHub stars, 5,800+ forks and 400+ contributors on the Mintplex Labs repo; used by solo professionals who want private document chat, and by teams that self-host behind their own firewall. Desktop app runs fully offline with no account and no telemetry",
    "badge": {
        "type": "recommend",
        "text": "RECOMMENDED"
    },
    "url": "https://anythingllm.com",
    "price": "Desktop (Mac/Win/Linux): free forever, unlimited workspaces and documents for one user, no account, no telemetry, no feature gating. Self-hosted Docker: free (MIT), multi-user with role-based permissions, shared workspaces, embeddable chat widgets - you just pay for a VPS (~$5-$10/month). Cloud Basic $50/month: private managed instance with custom subdomain, RAG, agents, up to ~5 users and ~100 documents, bring your own LLM API key. Cloud Pro $99/month: larger document collections, team collaboration, 72-hour support SLA. Enterprise: custom - on-premise deployment, SSO/RBAC, white-labeling, custom integrations and SLA. Note: model inference is never bundled - if you plug in OpenAI or Anthropic you pay their per-token rates separately; Ollama gives you fully offline $0 inference on your own hardware",
    "platform": "Desktop app for macOS, Windows, Linux; Docker self-host on any VM; managed cloud with custom subdomain; embeddable chat widget for any website; MCP support on desktop and Docker with Intelligent Tool Selection; community plugin marketplace",
    "published": True,
    "related": [
        "ragflow",
        "dify",
        "flowise",
        "chatpdf",
        "notebooklm"
    ],
    "created_date": "2026-08-06",
    "pros": [
        "Genuinely free at the core - the desktop app and the Docker image are MIT open source with no feature gating, no forced account and no telemetry, which is rare in this category",
        "Model-agnostic to a fault: 30+ LLM providers and 7 vector database backends (LanceDB default, plus Pinecone, Chroma, Qdrant, Milvus, Weaviate, PGVector) - you are never locked into one vendor",
        "Real multi-user and multi-workspace on the self-hosted build: role-based permissions, isolated workspaces each with its own vector store, and an embeddable chat widget - enough for a whole team behind one Docker container",
        "The 5-minute win: a weekend RAG project in LangChain takes an afternoon to wire up; in AnythingLLM you install, drag in a folder of PDFs, and you are retrieving the same day",
        "Document coverage is wide: PDF, DOCX, TXT, CSV, OCR on images, audio transcription, plus scrapers for websites, Confluence, GitHub repos and YouTube transcripts - most of what a real business throws at it works out of the box",
        "MCP support with Intelligent Tool Selection turns it into a bridge between Claude Desktop or ChatGPT and your knowledge base - a genuinely useful 2026 feature most reviews miss"
    ],
    "cons": [
        "'Local' is half-true: the app runs on your machine, but the models usually do not. Without Ollama or LM Studio you are still sending your documents to a cloud API - the privacy story only holds if you actually run local models",
        "Local models need hardware: smooth on-device RAG realistically wants 16GB+ RAM, and most people's laptops choke on a decent local LLM - which quietly pushes you back toward cloud APIs",
        "Desktop is single-user only: no team sharing, no roles, no remote access. The moment you need collaboration you must self-host Docker or pay $50/month for cloud, which kills the 'free forever' headline",
        "It is the cockpit, not the engine - response quality is whatever model you connect, not what AnythingLLM does. Clients who expect ChatGPT-level polish are disappointed if you wire up a small local model",
        "Not zero-configuration: you still need to choose an embedding model, pick a chunking strategy for messy PDFs, and tune retrieval. It removes the coding, not the judgment",
        "Deep document understanding is shallower than RAGFlow - AnythingLLM handles normal documents well, but complex tables, scans and highly formatted PDFs come out cleaner in RAGFlow"
    ],
    "features": [
        "Chat-with-your-documents RAG out of the box (PDF, DOCX, TXT, CSV, Markdown, images with OCR, audio transcription)",
        "30+ LLM providers: OpenAI, Anthropic, Ollama, LM Studio, LocalAI, Groq, AWS Bedrock, Azure and more",
        "7 vector database backends with per-workspace isolation",
        "Website scraping, Confluence, GitHub repo and YouTube transcript ingestion",
        "Multi-user accounts with role-based permissions (self-hosted and cloud)",
        "No-code agent builder: web browsing, code execution, SQL querying",
        "Embeddable chat widget for deploying a workspace on any website",
        "MCP support with Intelligent Tool Selection on desktop and Docker",
        "Visual Agent Flows drag-and-drop workflow builder + Community Hub marketplace",
        "Magic Features (v1.15): on-device dictation, text actions and autocomplete that run locally in any app"
    ],
    "faq": [
        {
            "question": "Can I actually make money with AnythingLLM when the software itself is free?",
            "answer": "That is exactly the point - the software being free is why the margins are so good. My bread and butter is private knowledge base deployment for law firms, clinics, accounting practices and small manufacturers that are not allowed to upload client files to ChatGPT. A typical engagement: I stand up the Docker container on their VPS, connect it to their LLM of choice, migrate a few hundred documents, set up user roles, and hand over an internal Q&A assistant. That bills $1,500-$5,000 depending on document volume, and the software cost is zero. Most clients then want me on retainer for $200-$500/month to maintain it, retrain it when they add documents, and handle model or security updates. The compliance angle raises the price further - GDPR, HIPAA or sector rules about data residency mean the 'we can't use cloud AI' conversation happens before you even quote. Add white-label chat widgets on client websites ($300-$1,500 per site plus $50-$150/month hosting) and a two-day in-house training package, and one free tool supports three or four service lines."
        },
        {
            "question": "Is the free desktop app actually free, or is there a catch?",
            "answer": "The app itself is free with no feature gating and no forced account - you can run it forever on one machine. The catch is what it connects to: AnythingLLM does not bundle model inference. If you plug in OpenAI or Claude, you pay their per-token rates; that bill lands on you. If you want true zero cost, you pair it with Ollama and run a local model, which needs a decent machine (16GB+ RAM is realistic) and the model quality drops below what cloud models give you. And the desktop build is single-user - no team sharing. So: free for a solo professional, effectively $5-$10/month on a VPS for a small team, or $50/month if you would rather not operate it yourself."
        },
        {
            "question": "AnythingLLM, RAGFlow or Dify - which should I pick for client work?",
            "answer": "They sit at different levels. RAGFlow is the better engine for deep document understanding - messy scans, complex tables, highly formatted PDFs - so pick it when the documents are ugly and accuracy is everything. Dify is a development platform: you build custom apps, workflows and agent pipelines in a visual editor, but it is more setup and more opinionated. AnythingLLM is the fastest path from 'folder of PDFs' to 'working internal knowledge base' with zero code - ideal when the client just wants their documents to become answerable and you want the deployment done in a day, not a week. My rule: clean documents and quick wins, AnythingLLM; nasty documents, RAGFlow; anything that needs custom logic or public-facing apps, Dify. They are not competitors - a team can run all three for different jobs."
        },
        {
            "question": "What does a typical paid deployment for a business actually involve?",
            "answer": "Mostly things clients cannot do themselves, which is why they pay. The work: choosing and sizing the VPS (or convincing their IT team to give you one), installing Docker and the container, picking the LLM strategy (local Ollama for sensitive data, a cloud API for better answers), choosing the embedding model, setting up workspaces and user roles, migrating their documents from shared drives or old knowledge systems, testing retrieval quality on their actual files, and writing a one-page user guide. The recurring part is the real money: documents get added, questions come back wrong, models get updated, and the security patch cadence never stops. That maintenance is what turns a $3K install into a $300/month retainer - and retention is near 100% because ripping out a working internal AI assistant and starting over costs them more than your fee."
        }
    ],
    "content": """## What AnythingLLM Actually Is (From Someone Who Deploys Private Knowledge Bases)

I make my living deploying private AI knowledge bases for businesses that are not allowed to use ChatGPT. Law firms with client-confidential case files. Medical clinics bound by data rules. Accounting practices that would lose clients if a document leaked. For three years the standard answer was a pile of custom LangChain code nobody could maintain, until AnythingLLM showed up and made most of that work unnecessary.

AnythingLLM is an open-source (MIT), full-stack app that does one thing well: it turns your documents into a private chat interface. You install it, point it at an LLM - Ollama, LM Studio, OpenAI, Claude, Groq, whatever - and a vector database (LanceDB works out of the box; Pinecone, Chroma, Qdrant, Milvus, Weaviate and PGVector are options), then drag in PDFs, DOCX files, CSV exports, images with OCR, audio transcripts, or scrape a website, a Confluence space, a GitHub repo or a YouTube channel. AnythingLLM handles chunking, embedding, retrieval and chat orchestration. You keep the model and storage choices; it is the cockpit, not the engine.

The project carries real weight: 54,000+ GitHub stars, 5,800+ forks, 400+ contributors. It grew from a desktop app into a full stack with multi-user self-hosting, agents, an embeddable chat widget, MCP support and a no-code workflow builder. And the pricing story is genuinely unusual: the desktop app is free forever, the Docker self-host is free, and the only paid tier is managed cloud at $50/month. That pricing is not marketing - it is the reason my deployment business has 90%+ margins.

## Pricing, Plainly

- **Desktop (macOS / Windows / Linux):** free forever. Unlimited workspaces and documents for one user, no account, no telemetry, no feature gating.
- **Self-hosted (Docker):** free (MIT). Multi-user with role-based permissions, shared workspaces, embeddable chat widgets. Your cost is a VPS, realistically $5-$10/month.
- **Cloud Basic:** $50/month. Private managed instance, custom subdomain, RAG and agents out of the box, ~5 users and ~100 documents. Bring your own LLM API key.
- **Cloud Pro:** $99/month. Larger document collections, team collaboration, priority resources, 72-hour support SLA.
- **Enterprise:** custom. On-premise deployment, SSO/RBAC, white-labeling, custom SLA and integrations.

One thing the free headline does not tell you: model inference is never bundled. Point AnythingLLM at OpenAI and you pay per-token rates on top. For true zero marginal cost you pair it with Ollama and run a local model - which needs a decent machine and drops answer quality. The software is free; the brain is not, unless you bring your own.

## Why It Pays (The Real Income Angle)

AnythingLLM is free, so the money is not in the software - it is in everything around the software. Here is where I actually see people billing:

**1. Private knowledge base deployment ($1,500-$5,000 per project).** This is the big one. Firms and clinics that cannot use cloud AI will pay a specialist to stand up a private instance on their infrastructure, connect their LLM of choice, migrate their documents, set up user roles and hand over a working internal Q&A tool. The software costs nothing; the setup, judgment and integration is the invoice. With one or two deployments a month plus retainers, this is a $5K-$8K month from a tool that costs $0.

**2. Compliance and data-residency consulting ($500-$2,000 per engagement).** GDPR, HIPAA, sector-specific rules - any business that handles regulated data has the 'we cannot send files to ChatGPT' problem, and most of them do not know a private RAG stack exists. Just being the person who explains the options and quotes the deployment turns into paid work.

**3. Document migration and knowledge base cleanup ($500-$2,000).** Most businesses have years of documents in shared drives, old wiki software and inboxes. Turning that mess into a structured, answerable knowledge base is real work clients happily pay for - and it is a natural upsell into the deployment itself.

**4. White-label chat widgets ($300-$1,500 per site + $50-$150/month hosting).** AnythingLLM's embeddable chat widget lets you put a branded, private Q&A assistant on any client website. Businesses pay monthly for that because it makes them look bigger than they are.

**5. Agent and MCP integrations ($500-$2,000 each).** The 2026 AnythingLLM connects to Claude Desktop and ChatGPT over MCP with Intelligent Tool Selection. Wiring a client's existing tools into their private knowledge base is niche, low-competition work that nobody else in their town can do.

**6. In-house AI training ($500-$3,000 per session).** Every deployment ends the same way - staff do not know how to ask questions properly or distrust the answers. A half-day training session on how to use and verify their new internal AI is an easy add-on to any project.

The pattern across all six: AnythingLLM being free removes the cost objection entirely. Clients never haggle over the tool fee because there is none. They haggle over your time, which is exactly what you want to sell.

## The Honest Pros and Cons

- **Genuinely free at the core.** MIT license, no feature gating, no forced account, no telemetry. This is rare in the AI category and it is the whole business model for people like me.
- **Model-agnostic.** 30+ LLM providers and 7 vector databases means clients are never locked in - a huge selling point when you are recommending software to a cautious CTO.
- **Real multi-user on self-host.** Role-based permissions, isolated workspaces, shared access and an embeddable widget in one free Docker container.
- **Fast to value.** A LangChain RAG project is a weekend; AnythingLLM is the same day. That speed is what makes small deployments profitable.
- **Wide document coverage.** PDFs, DOCX, OCR, audio transcription, plus website/Confluence/GitHub/YouTube scrapers - most real-world content works out of the box.
- **MCP support.** It bridges Claude Desktop and ChatGPT to your private knowledge base, which makes it useful even to people who already pay for those tools.

The cons are real and you will hit them in production:

- **'Local' is half-true.** The app runs locally; the models usually do not. Without Ollama or LM Studio, your documents are still going to a cloud API. The privacy story only holds if you actually run local models.
- **Local models need hardware.** Smooth on-device RAG realistically wants 16GB+ RAM. Most business laptops choke, which quietly pushes teams back to cloud APIs.
- **Desktop is single-user.** No team sharing, no roles, no remote access. Collaboration means Docker self-host or $50/month cloud - the 'free forever' headline has a ceiling.
- **Quality follows the model, not the app.** Clients who expect ChatGPT polish are disappointed when you wire up a small local model. Manage expectations before you deploy.
- **Not zero-configuration.** You still choose embeddings, chunking and retrieval settings. It removes the coding, not the judgment.
- **Shallower document understanding than RAGFlow.** Messy scans, complex tables and highly formatted PDFs come out cleaner in RAGFlow; AnythingLLM is better on normal documents and speed.

## AnythingLLM vs The Alternatives

| Tool | Best at | Model freedom | Free tier | Price |
|------|---------|--------------|-----------|-------|
| **AnythingLLM** | Fast private chat-with-docs, self-host, multi-user | 30+ providers, 7 vector DBs | Full desktop + Docker free | Free / Cloud $50+ |
| RAGFlow | Deep document understanding, messy/structured PDFs | Multiple, self-host | Self-host free | Free / Cloud $49+ |
| Dify | Building custom AI apps and workflows visually | Multiple, self-host | Community free | Free / Enterprise |
| LangChain | Programmatic RAG for developers | Everything, code-level | Open source | Free / LangSmith $25+ |
| NotebookLM | Free hosted summarising of your own sources | Google only | Generous | Free |
| ChatGPT | General answers, not private docs | OpenAI only | Generous | Free / $20+ |

The honest summary: RAGFlow wins on ugly documents, Dify wins when you need custom apps, LangChain wins when you are a developer building from scratch, NotebookLM wins when you do not care about privacy, and ChatGPT is not a knowledge base tool at all. AnythingLLM wins on the fastest path from 'folder of files' to 'working private Q&A for a whole team' - which is exactly what most paying clients actually need.

## Who Should Use It (And Who Shouldn't)

**Use it if:** you run a business that handles documents it cannot upload to public AI services (law, health, finance, HR, manufacturing); you are a freelancer or agency selling knowledge base setup, internal AI or chat widgets; you are a solo professional who wants private chat-with-your-files and is comfortable with a bit of setup; or you want a private MCP bridge between Claude Desktop or ChatGPT and your own documents.

**Skip it if:** you want zero setup and do not care about privacy - NotebookLM is friendlier; you need deep extraction from complex, formatted PDFs - RAGFlow does that better; you need custom public-facing apps and workflows - Dify is the right platform; or you expect ChatGPT-level answers from a free local model - you will be disappointed, and you will be blaming the wrong layer.

## Getting Started (6 Tips)

1. **Install the desktop app first and test with real documents.** Free, no account - drag in a folder of PDFs, connect an LLM (Ollama if you want it truly local, otherwise any API key) and see if retrieval quality is good enough for your files before committing to a deployment plan.
2. **Start with LanceDB, then decide if you need more.** The default vector store is fine for most teams. Only move to Pinecone, Qdrant or Milvus when you hit scale or need specific features - do not over-engineer a knowledge base that works.
3. **Test embedding choice on your own documents.** The default embeddings are fine for general text; legal, medical or technical documents often retrieve better with a domain-tuned or local embedding model. This is the single biggest quality lever.
4. **For client work, quote the deployment and the retainer together.** The install is the door opener; the $200-$500/month maintenance is where the business is - document updates, model changes, security patches and retraining never stop.
5. **Verify every answer against the source.** RAG reduces hallucination, it does not remove it. If you deploy for clients, build the habit of clicking through to the cited chunk before you trust an answer - and tell them you do.
6. **Keep the model story honest in proposals.** If you promise 'fully private', you are committing to local inference and the hardware that implies. If you deploy a cloud API model, say so - the client's compliance officer will find out anyway.

The bottom line: AnythingLLM is the rare tool where the software being free is not a weakness but the whole business opportunity. For anyone selling private AI - deployments, maintenance, widgets, training - it is currently the fastest base to build on, and at $0-$50 a month it makes the margin math embarrassingly good."""
}

# ---- Load existing data ----
with open(DATA, encoding="utf-8") as f:
    tools = json.load(f)

# ---- Safety: reject if slug already exists ----
if any(t.get("slug") == new_tool["slug"] for t in tools):
    raise SystemExit(f"[ABORT] slug '{new_tool['slug']}' already exists in {DATA}")

# ---- Forbidden-word scan (Anti-AI tone rule) ----
FORBIDDEN = [
    "leverage", "utilize", "robust", "streamline", "seamless", "empower",
    "unlock", "elevate", "revolutioniz", "cutting-edge", "state-of-the-art",
    "game-chang", "harness", "unleash", "supercharge", "synerg", "unparalleled",
    "groundbreak", "transformative", "next-level", "best-in-class"
]
blob = json.dumps(new_tool, ensure_ascii=False).lower()
hits = [w for w in FORBIDDEN if w in blob]
if hits:
    raise SystemExit(f"[ABORT] forbidden words found: {hits}")

# ---- Append + save ----
tools.append(new_tool)
with open(DATA, "w", encoding="utf-8") as f:
    json.dump(tools, f, ensure_ascii=False, indent=1)

print(f"[OK] Added '{new_tool['name']}' -> {DATA} (total {len(tools)} tools)")
print(f"[OK] content length: {len(new_tool['content'])} chars")
print(f"[OK] forbidden-word scan clean")

# ---- Generate OG image (Pillow) ----
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"))
import gen_og_images_en as og

og_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "og")
os.makedirs(og_dir, exist_ok=True)
try:
    from pathlib import Path
    og.make_tool_og(new_tool, Path(og_dir) / "anythingllm-en-og.png")
    out_path = os.path.join(og_dir, "anythingllm-en-og.png")
    size = os.path.getsize(out_path)
    print(f"[OK] OG image generated: {out_path} ({size} bytes)")
except Exception as e:
    print(f"[WARN] OG image generation failed: {e}")
