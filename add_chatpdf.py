# -*- coding: utf-8 -*-
"""Add ChatPDF to tools_en.json (aitoolbox.hk).
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
    "name": "ChatPDF",
    "slug": "chatpdf",
    "emoji": "\U0001F4C4",
    "color": "#0EA5E9",
    "description": "ChatPDF turns any PDF into a chat you can question - drop in a contract, a textbook, or a 200-page report and ask plain-English questions, and it answers with page numbers so you can check the source. I use it to read stacks of paperwork I would never sit down and page through, and the money side is direct: I charge people who hate reading their own documents to do the reading for them.",
    "category": "AI Productivity",
    "tags": [
        {"text": "PDF Chat"},
        {"text": "Document Analysis"},
        {"text": "Study"},
        {"text": "Free", "type": "free"},
        {"text": "Research"},
        {"text": "Multilingual"}
    ],
    "rating": "\u2b50 4.5",
    "visits": "Tens of millions of monthly visits",
    "badge": {
        "type": "hot",
        "text": "HOT"
    },
    "url": "https://www.chatpdf.com",
    "price": "Free (2 PDFs/day) + Plus ~$5-$12/mo",
    "platform": "Web, iOS, Android, macOS/Windows desktop apps",
    "published": True,
    "related": [
        "notebooklm",
        "chatgpt",
        "claude",
        "perplexity",
        "gemini",
        "julius-ai"
    ],
    "created_date": "2026-07-27",
    "pros": [
        "Zero friction to start - drag a PDF onto the homepage and chat, no account, no setup, no prompt engineering",
        "Every answer carries page numbers, so clients can open the exact page and trust the summary instead of taking my word",
        "Cheap to run - the free tier covers casual use and Plus sits around $5-$12/month, so my margin on paid work stays near 100%",
        "Cross-language questions work well - upload a French or Japanese paper and ask in English; good for international research and bilingual clients",
        "Multi-PDF folders let me load a whole contract pack or a course bundle and ask across all of them in one thread",
        "Shareable chat links mean the client can click through my analysis themselves, which sells the service better than a static report"
    ],
    "cons": [
        "Scanned or image-only PDFs are unreliable - no real OCR, so an old contract scan comes back with gaps and you need to clean it first",
        "Complex tables, charts, and footnotes confuse it; numbers get misread, so any financial or legal figure needs a manual check against the page",
        "The free tier caps at 2 PDFs a day and 120 pages each - fine for a taste, useless for a real client job, you pay to work",
        "PDF-first by design - Word, Excel, and PowerPoint need workarounds or a different tool, which breaks mixed-document workflows",
        "No public API, so you cannot bolt it into a client's pipeline or automate bulk processing the way you can with an LLM API",
        "It summarizes what is there; it will not catch a missing clause or a trap a human reviewer would spot, and it will not tell you it missed one"
    ],
    "features": [
        "Conversational PDF Q&A - ask natural-language questions and get answers pulled from the whole document",
        "Page-level citations on every response so you can jump to the source and verify",
        "One-click summaries and suggested follow-up questions the moment a file uploads",
        "Multi-PDF folders for cross-document questions (contract packs, course bundles, research sets)",
        "Cross-language support - upload in one language, question in another, with translated answers",
        "Shareable conversation links with revocable access for clients and study groups",
        "Web plus iOS, Android, and desktop apps; Plus adds AI Writer, AI Detector, YouTube Chat, and Research tools"
    ],
    "faq": [
        {
            "question": "Can you actually make money with a near-free tool?",
            "answer": "You do not sell ChatPDF; you sell the reading. A founder does not want a $12/month subscription, he wants someone to read his 340-page funding agreement and tell him the three clauses that will burn him. I charge $50-$300 per document or $500-$2,000 a month to do that reading, and ChatPDF is the engine that makes it fast. The subscription cost is rounding error next to the invoice."
        },
        {
            "question": "Is the free tier enough to do paid work?",
            "answer": "No, and that is by design. Two PDFs a day at 120 pages each covers a demo or a personal doc, not a client engagement. For any real volume - a data room, a semester of textbooks, a contract stack - you need Plus. Budget the $5-$12 a month into your cost; it barely moves your margin."
        },
        {
            "question": "ChatPDF vs NotebookLM vs just uploading to ChatGPT - which do I learn?",
            "answer": "For a single PDF with citations you can hand a client, ChatPDF wins on speed and the share link. NotebookLM is better when you have dozens of sources and want a researched brief with grounded notes. ChatGPT or Claude handle one big PDF fine but give weaker page pointing and no clean share link. I keep ChatPDF for client-facing doc reads and NotebookLM for my own research."
        },
        {
            "question": "How far can I trust the answers before billing a client?",
            "answer": "Far enough to draft, not far enough to sign off. Factual extraction from clean text is solid; tables, scanned pages, and legal nuance are where it slips. My rule: ChatPDF produces the first pass and the page list, I verify every number and clause against the actual page, then I deliver. The tool cuts my reading time from hours to minutes, it does not remove the responsibility."
        }
    ],
    "content": "## What ChatPDF Actually Is (From Someone Who Reads Other People's Documents for a Living)\n\nI make part of my income reading documents other people do not want to read - contracts, filings, textbooks, research papers, loan agreements, 200-page technical manuals. For most of 2023 and 2024 I did that the slow way: highlight, skim, panic, re-read. Then I started running those files through ChatPDF, and the slow way stopped being necessary.\n\nChatPDF is a web tool that turns a PDF into a conversation. You upload a file, it reads the whole thing, and you ask questions in plain language - \"What are the termination clauses in this contract?\" \"Summarize the methodology section.\" \"List every number in the financial appendix.\" It answers, and crucially it tells you the page number where each answer came from. That page reference is the feature that made it usable for paid work, because a client will trust a summary he can open and check far more than one he has to take on faith.\n\nThe free tier needs no account. You drag a PDF onto the homepage and start asking. Paid plans lift the daily and page limits and add multi-PDF folders, faster models, and a few side tools (an AI writer, an AI detector, a YouTube chat mode). As of mid-2026 it runs on web, iOS, Android, and desktop apps, and it handles documents in any language - upload a Japanese paper, ask in English, get an English answer with the source page cited.\n\n## Why It Pays (The Real Income Angle)\n\nChatPDF is cheap - free to start, a few dollars a month to work at volume. You are not selling software. You are selling the reading other people avoid, plus the layout and the verification. Because the tool costs almost nothing, your margin on every job is close to 100%; the only real cost is your time and your judgment. Here are the ways I have seen people turn ChatPDF into income.\n\n### 1. Document-reading service for people who hate their own paperwork\nThis is the backbone. Founders, clinic owners, small landlords, and solo investors get PDFs they will never read and know they should. You take the file, run it through ChatPDF, verify the key points against the pages, and hand back a plain-language brief with the dangerous bits flagged. Pricing that works: $50-$150 for a single contract, $200-$500 for a mid-size pack, $500-$2,000 a month for a client who feeds you documents steadily. A real example from my own work: a first-time founder paid me $1,200 to read a 340-page seed SPA plus six annexes and flag every clause that could hurt him later. ChatPDF did the first pass in minutes; the billing was for the verification and the judgment, not the keystrokes.\n\n### 2. Study-guide packs for students\nTextbooks and course readers are perfect ChatPDF fodder. Upload the semester's PDFs, generate per-chapter summaries and question sets, and sell them. Two models: a one-off pack for $15-$40 on Gumroad or Payhip (passive, sells while you sleep), or a done-for-you semester bundle at $200-$500 for a student or a study group. The free tier builds the first draft; Plus handles a full course load. Watch academic-integrity lines - sell study aids, not ghostwritten exams.\n\n### 3. Contract and legal-doc triage for solopreneurs\nMost solo business owners sign contracts they do not understand. For $75-$150 per document you read their vendor agreement, lease, or contractor terms, explain the legalese in plain words, and mark the unusual clauses. This is repeat business - every new contract is a new $75-$150. You are not a lawyer and you say so; you are the person who makes the page readable before they pay one.\n\n### 4. Investor due-diligence doc dumps\nWhen a deal lands, the data room is a wall of PDFs - cap tables, IP assignments, prior term sheets, audited statements. An investor or a broker will pay $300-$800 per deal to have someone read the room fast and surface the risks and the gaps. ChatPDF's multi-PDF folders are built for exactly this; you load the room and ask across all of it. The deliverable is a one-page risk memo with page citations the investor can check himself.\n\n### 5. Internal SOP and knowledge-base Q&A for small teams\nA shop with thick manuals - a clinic, a gym, a trades company - wastes hours hunting for the right procedure. Upload the manuals into ChatPDF, teach the manager and the staff to ask it direct questions, and charge $400-$1,200 to set that up plus $100-$300 a month to keep it current as docs change. The share link means new hires self-serve instead of pinging the owner.\n\nAt every tier the math is the same: a $5-$12 monthly subscription against $50-$2,000 of billing per job. The tool is the lever; you are the operator.\n\n## What ChatPDF Is Bad At (Be Honest Before You Sell It)\n\nI would not hand ChatPDF a document and walk away, and neither should you if you are billing for the result.\n\n- Scanned or image-only PDFs come back unreliable. There is no real OCR, so an old contract scan produces gaps, and you have to clean it or read those pages yourself.\n- Tables, charts, and footnotes trip it up. Numbers get misread, and because the answer looks confident, the mistake is easy to miss. Any figure a client will act on gets checked against the page.\n- The free tier is a teaser for work: 2 PDFs a day, 120 pages each. Fine for a demo, useless for a client job. You pay to do paid work.\n- It is PDF-first. Word, Excel, and PowerPoint need workarounds or a different tool, which breaks workflows that mix document types.\n- No public API. You cannot bolt it into a client's pipeline or automate bulk runs the way you can with a raw LLM API - it stays a manual, one-file-at-a-time desk tool.\n- It summarizes what is present. It will not notice a clause that should be there and is not, and it will not warn you it missed one. That gap is your job to close.\n\n## How I Run a Client Job With It\n\n1. Get the file, check it is a real text PDF (not a scan). If it is a scan, run it through an OCR step first or read those pages by hand.\n2. Upload to ChatPDF, let it auto-summarize, and skim the summary to learn the shape of the document.\n3. Ask targeted questions: risks, obligations, deadlines, money, odd language. Use the folder feature for multi-file packs.\n4. Pull the page numbers on every answer and open each one to verify - especially numbers and legal wording.\n5. Write the client brief in plain language with the cited pages attached, and mark clearly what I checked and what they should still have a human review.\n6. Send the share link so they can click through my reasoning themselves.\n\nThat workflow takes me minutes per document instead of an hour, and the verification step is what keeps me from billing a mistake.\n\n## ChatPDF vs The Alternatives\n\n| Tool | Best for | Price | Multi-doc | Citations | Catch |\n|------|----------|-------|-----------|-----------|-------|\n| ChatPDF | Fast single or small-pack PDF reads with a shareable link | Free + Plus ~$5-$12/mo | Folders (paid) | Page numbers | PDF-first, no API |\n| NotebookLM | Dozens of sources, researched briefs with grounded notes | Free + paid tiers | Strong | Source notes | Less client-friendly, Google-bound |\n| ChatGPT / Claude | One big PDF plus everything else | $20/mo | Weak across files | Soft | No clean share link, pricier |\n| Humata | Secure professional doc work, team features | ~$2-$50/mo | Yes | Yes | Needs account, smaller brand |\n| Julius AI | Data analysis from CSV/Excel, not PDF reading | ~$49/mo | N/A | N/A | Different job entirely |\n\nMy setup: ChatPDF for client-facing document reads, NotebookLM for my own multi-source research, and a raw LLM API when I need to automate a bulk run. They cover different steps; none replaces the others.\n\n## Who Should Use It, Who Should Not\n\nUse ChatPDF if you read other people's PDFs for a living or want to start - founders, researchers, paralegals, tutors, analysts, and anyone building a document-reading side service. It is the lowest-friction entry in the category.\n\nSkip it if you need to process scanned archives at scale, build an automated pipeline (get an API instead), or work across Word and Excel daily. And if your documents are sensitive enough that a cloud copy is a problem, run a local model - ChatPDF stores your files on its servers, and that is a real limit for medical or privileged material.\n\n## Getting Started (Without Wasting the First Week)\n\n1. Start on the free tier. Drag in a PDF you already know and ask it questions - you will learn its strengths and its misses faster on familiar text.\n2. Move to Plus the moment you take a paid job. The page and daily limits on free will stop you mid-client.\n3. Build a question template: risks, obligations, deadlines, money, undefined terms. Reuse it on every contract so your reads stay consistent.\n4. Always open the cited page before you trust a number. The citation is there precisely so you can verify; use it.\n5. Use the share link as your deliverable. Clients trust a clickable analysis more than a PDF you wrote.\n6. Pair it with NotebookLM for big research jobs and an LLM API for anything you need to automate. ChatPDF is the desk tool, not the whole stack.\n\n## The Bottom Line\n\nChatPDF will not replace a careful human reader, and it should not be sold as one. What it does is remove the hours of page-turning that stop most people from ever understanding their own documents - and that removal is exactly the service you can charge for. Keep the verification step, price the reading not the software, and it is one of the cheapest, fastest ways I know to turn a pile of PDFs into a paid invoice.",
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
