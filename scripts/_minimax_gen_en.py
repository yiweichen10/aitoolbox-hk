#!/usr/bin/env python3
import requests, os, sys
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

KEY = os.getenv("MINIMAX_API_KEY")

SYSTEM = """You are a senior tech journalist who covers AI tools. Write honest, specific, opinionated reviews for a skeptical audience. Short punchy sentences mixed with longer ones. Contractions throughout. Real prices and real limitations. No corporate buzzwords: no leverage, seamlessly, game-changing, comprehensive, delve into, transformative."""

USER = """Write a 1500-word review page for ChatGPT. Use these keywords naturally — weave in, do NOT stuff:
- Primary "ChatGPT review": 3-4x — must be in first 100 words, one H2, and final paragraph
- Longtail (1-2x each): "ChatGPT alternative", "ChatGPT alternative for writing", "ChatGPT reviews 2025"
- FAQ H3 questions verbatim: "Is ChatGPT really any good?", "Is ChatGPT free and safe?", "What's a better free alternative to ChatGPT?", "Which is the best AI chatbot in 2026?"

Tool data: Price Free + Plus $20/mo | Pros: best-in-class reasoning, GPT ecosystem, code generation, free GPT-4o | Cons: hallucinates confidently, knowledge cutoff, latest models need Plus | Features: multimodal, Custom GPTs, code interpreter, voice, web browsing

Structure (NO H1): Intro 1-2 paras → 4-5 H2 sections (what it does / pricing / best for / limitations / vs alternatives) → comparison table ChatGPT vs Claude vs Gemini → 4 FAQ H3 → final recommendation para (no Conclusion header)

Raw Markdown only."""

r = requests.post(
    "https://api.minimaxi.com/v1/text/chatcompletion_v2",
    headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
    json={
        "model": "MiniMax-M2.7",
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": USER},
        ],
        "max_tokens": 3000,
        "temperature": 0.7,
    },
    timeout=120
)

print("Status:", r.status_code)
if r.status_code == 200:
    d = r.json()
    content = d["choices"][0]["message"]["content"]
    out = Path("C:/Users/27040/WorkBuddy/20260321092139/seo-site-en/data/_drafts_en/chatgpt-minimax.md")
    out.write_text(content, encoding="utf-8")
    print(f"Saved {len(content.split())} words to {out}")
else:
    print(r.text[:500])
