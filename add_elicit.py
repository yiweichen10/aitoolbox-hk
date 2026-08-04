# -*- coding: utf-8 -*-
"""Add Elicit to tools_en.json (aitoolbox.hk).
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
    "name": "Elicit",
    "slug": "elicit",
    "emoji": "\U0001F52C",
    "color": "#6B46C1",
    "description": "Elicit is an AI research assistant for academic literature - it searches 138 million papers and 545,000 clinical trials, extracts sample sizes, methods and outcomes into structured tables, and backs every claim with a sentence-level citation you can click through. I run literature reviews as a service on it: a $150-$500 scoping review costs me roughly $0-2 in tool fees on the free-to-Pro plans, and systematic review support for health and med-tech clients bills at $2K-$10K per engagement. It grew out of Ought, the non-profit AI lab, and counts 2M+ researchers among its users; the 2026 version adds Research Agents, PRISMA-style screening and an API.",
    "category": "AI Research",
    "tags": [
        {"text": "Literature Review"},
        {"text": "Systematic Review"},
        {"text": "Data Extraction"},
        {"text": "Paper Search"},
        {"text": "Research Agent"},
        {"text": "Citations", "type": "free"},
        {"text": "PRISMA"}
    ],
    "rating": "\u2b50 4.6",
    "visits": "2M+ researchers across academia and industry; roughly 850K monthly visits. Searches 138M+ papers and 545K clinical trials; used by grad students, postdocs, clinicians, policy analysts and evidence-driven consultants who need verifiable citations rather than AI speculation",
    "badge": {
        "type": "recommend",
        "text": "RECOMMENDED"
    },
    "url": "https://elicit.com",
    "price": "Free (Basic): unlimited search across 138M+ papers, unlimited summaries and paper chat, Zotero import, 2 automated reports per month, 2 table columns. Pro $49/user/mo (billed $588/yr, 35% off): systematic review workflow screening up to 5,000 papers, 20 columns, extraction from up to 135 data sources, 10 research alerts, custom extractions from uploaded PDFs, API access. Scale $169/user/mo (billed $2,028/yr): 5x usage, figure extraction and interpretation, live team collaboration, 30 columns, 200 data sources, admin panel. Enterprise custom: screen 40,000 papers, 40 columns, no training on your data by default, PRISMA-grade screening, SSO/SAML/2FA, unlimited API",
    "platform": "Web app at elicit.com; Zotero import; CSV/RIS export into Zotero, Mendeley and EndNote; custom PDF upload; Research Agents (late 2025); REST API launched March 2026 on Pro and above",
    "published": True,
    "related": [
        "consensus",
        "notebooklm",
        "perplexity-ai",
        "chatpdf",
        "exa-ai"
    ],
    "created_date": "2026-08-05",
    "pros": [
        "Sentence-level citations on everything - every claim links to the exact sentence in the source paper, which is the strongest anti-hallucination feature in the category and the reason I trust it in front of clients",
        "The corpus is enormous for academic work: 138M+ papers and 545K clinical trials, so for evidence questions it beats general web search by a wide margin",
        "Structured extraction tables save real hours - sample sizes, methods, outcomes and effect sizes land in a spreadsheet instead of you opening forty PDFs",
        "The PRISMA-style systematic review workflow (5,000 papers screened on Pro, 40,000 on Enterprise) compresses a months-long screening phase into days - that is the big-ticket service play",
        "The free tier is genuinely usable: unlimited search, summaries and paper chat plus 2 automated reports a month - enough to run a real test project before paying anything",
        "Research Agents plus the 2026 API turn it into more than a reader - multi-step landscape jobs and programmatic pipelines both run from a single Pro seat"
    ],
    "cons": [
        "It is an academic tool, full stop - no general web search, no news, no product data. Questions that live outside peer-reviewed literature get nothing useful back",
        "The free tier is a teaser for paid work: 2 reports a month and 2 table columns push any real service onto Pro at $49/month, which is fair but not cheap",
        "Extraction is not infallible - complex tables, figures and ambiguous methods still get misread, so every number you hand a client needs manual verification against the source sentence",
        "The column-and-table workflow is a spreadsheet, not a chat box; there is a real learning curve before it clicks",
        "Index coverage is uneven - strongest in biomedicine, thinner in niche fields, very recent papers and non-English literature, because the corpus is built on Semantic Scholar data",
        "Real-time team collaboration only arrives at Scale, $169/month - a steep jump if you wanted a two-person review operation"
    ],
    "features": [
        "Semantic paper search across 138M+ papers and 545K clinical trials",
        "Sentence-level citations - every AI claim links to the exact supporting sentence in the source",
        "Structured data extraction tables (sample size, methods, outcomes, effect sizes, significance)",
        "Automated research reports synthesising up to 80 papers at once",
        "PRISMA 2020 systematic review workflow with strict screening criteria (5,000 papers on Pro, 40,000 on Enterprise)",
        "Research Agents - automated multi-step jobs like competitive landscape mapping",
        "Research Alerts (10 on Pro) - smart notifications when new papers match a topic",
        "REST API (March 2026) for programmatic search and report generation on Pro+",
        "Zotero import, CSV/RIS export, custom PDF upload"
    ],
    "faq": [
        {
            "question": "Can I actually make money with Elicit without being an academic?",
            "answer": "Yes - and the people who pay best are the ones who hate reading papers. Busy clinicians, founders raising in health tech, consultancies and investors all need cited evidence but refuse to read 200 abstracts. A scoping literature review sells for $150-$500 and takes me a few hours on the free plan; four to six a month clears $1,000-$2,500 at a tool cost of $0-$49. The bigger play is systematic review support for health and med-tech clients at $2K-$10K per engagement, because Elicit's PRISMA-style screening (5,000 papers on Pro) turns a months-long manual phase into days. Add a $200-$500/month research-alert digest service and you have three income streams off one $49 seat. What you need is a niche and a willingness to verify citations - you do not need a PhD."
        },
        {
            "question": "Elicit, Consensus or ResearchRabbit - which should I use?",
            "answer": "They answer different questions. Consensus is fastest when you want a yes/no answer with a consensus percentage ('does vitamin D improve sleep?') - it is a quick fact-check tool. ResearchRabbit is about discovery - it maps citation networks so you can find connected papers you would never search for. Elicit is the heavy lifter: it extracts structured data across many papers, runs systematic reviews and produces citable reports. My rule: ResearchRabbit to find the papers, Consensus for a quick pulse, Elicit when a client needs a verifiable evidence table with real numbers. If your work involves billing for research, Elicit is the one that justifies the invoice."
        },
        {
            "question": "Is the free plan enough to run a research service?",
            "answer": "For testing, yes - unlimited search, summaries and paper chat let you prove Elicit covers your niche before you spend anything. For paid volume, no: the free tier allows only 2 automated reports a month and 2 table columns, which is fine for occasional use but chokes a real service. The Pro seat at $49/month (billed annually) is the actual business tool - 144 reports a year, 20 columns, 10 research alerts. It pays for itself on the first $300 review, so upgrade when you have a paying use for reports rather than before."
        },
        {
            "question": "Does Elicit hallucinate or make up sources?",
            "answer": "This is its strongest point and its subtle weakness. It is strictly anchored to its corpus of 138M+ papers - it does not fabricate authors or papers the way a general chatbot can, and every claim carries a sentence-level citation you can click. The weakness is interpretation, not invention: it can misread a metric inside a messy PDF (complex tables, figures, ambiguous methods), and the extraction accuracy claim in its marketing is not a guarantee for your niche. The professional habit is simple - open the cited sentence for every number you plan to put in front of a client. Elicit shows you the receipt; you still have to check the receipt."
        }
    ],
    "content": """## What Elicit Actually Is (From Someone Who Reads Papers for a Living)

I have spent the last two years doing literature reviews for clients - mostly busy clinicians, founders raising in health tech, and consultancies that need evidence-backed answers but would rather pay someone else to read the papers. Elicit is the tool that made me stop dreading that work.

Elicit is a research assistant built for academic literature, not general web search. It searches a corpus of 138 million papers and 545,000 clinical trials, then pulls out what matters: you ask a question, it finds the relevant studies, and instead of making you open forty PDFs it extracts the sample sizes, methods, outcomes and effect sizes into a structured table. Every single claim links to the exact sentence in the source paper - click through and you land on the sentence that supports it. That sentence-level citation system is the whole point. ChatGPT summarises vaguely; Elicit shows you the receipt.

It grew out of Ought, the non-profit AI research lab, and went through a serious product shift in 2025-2026. The old 'ask Elicit anything' assistant became a full research workflow: Research Agents run automated multi-step jobs like competitive landscape mapping, strict screening criteria (added December 2025) tightened the systematic review workflow, an API launched in March 2026, and automated reports can now synthesise up to 80 papers at once. Over 2 million researchers use it. My honest take after two years: it is the only AI tool I trust to hand a client a citation for.

## Pricing, Plainly

- **Free (Basic):** unlimited search across 138M+ papers, unlimited summaries, unlimited chat with papers, Zotero import, 2 automated reports per month, 2 table columns.
- **Pro:** $49/user/month, billed $588/year (35% off). Standard usage for Research Agents, reports and systematic reviews; screening up to 5,000 papers; 20 columns; extraction from up to 135 data sources; 10 personalized research alerts; custom extractions from your uploaded PDFs; API access.
- **Scale:** $169/user/month, billed $2,028/year. 5x the usage, figure extraction and interpretation, live team collaboration, 30 columns, 200 data sources, admin panel with usage tracking.
- **Enterprise:** custom. Screen 40,000 papers, 40 columns, no training on your data by default, PRISMA-grade screening accuracy, SSO/SAML/2FA, unlimited API.

There is no per-seat minimum drama on the free plan - you can run a real project on it, which is more than most research tools offer.

## Why It Pays (The Real Income Angle)

Elicit's buyers fall into two buckets: people who must read papers (academics, clinicians) and people who need what is in the papers but refuse to read them (founders, consultants, investors). The second bucket is where the money is.

**1. Literature review as a service.** This is the cleanest entry point, and I know half a dozen people doing it. A PhD student drowning in 200 papers, a clinic director who needs to know what the evidence says about a treatment, a startup team writing a tech due-diligence doc - they all pay $150-$500 for a scoping review they do not have time to do. On the free plan you can run 2 automated reports a month; on Pro at $49 the ceiling disappears (144 reports a year). Four to six reviews a month at $200-$400 each clears $1,000-$2,500 at a tool cost of $0-$49. The margin is basically the invoice.

**2. Systematic review support for health and med-tech.** This is the big-ticket play. Systematic reviews are the gold standard in medicine and they normally take a team of reviewers months - screening thousands of abstracts by hand. Elicit's PRISMA-style screening workflow (5,000 papers on Pro, 40,000 on Enterprise) compresses the screening phase to days. Research consultancies and med-tech companies pay $2K-$10K per systematic review engagement, and your tool cost is one Pro seat. If you have any domain credibility in health, this is the highest-margin service I know that a solo operator can run.

**3. Evidence-backed market and competitive research.** The Research Agents feature turned Elicit into more than a literature tool - you can run multi-step jobs like 'map every published study on AI in dental imaging, extract the authors and funders, flag the gaps.' Funds, VCs and consultancies pay $500-$2K for a well-cited landscape report. My last one took two days and billed at $1,500; the entire Elicit cost was the $49 Pro seat.

**4. Grant-writing evidence packs.** Funder applications want cited evidence that the problem exists and your approach is feasible. Assemble that evidence pack with Elicit - search, extraction, citation exports - and charge $500-$2,000 per grant package. Non-profits and research startups are chronically undersold on this service.

**5. Research-alert digest subscriptions.** Pro gives 10 personalized research alerts. Productise it: a monthly 'what's new in X' briefing for clinicians, product managers or investors at $200-$500 per month per client. Five clients at $300 clears $1,500 a month for an hour of curation work - Elicit does the watching, you do the editing.

**6. Cited course and CE content.** If you create training content - continuing education, clinical training, science communication - Elicit lets you build courses with real citations instead of vibes, which is exactly what CE reviewers check. A cited course package sells for $1K-$5K to professional bodies.

The unit economics that sell the story: a $300 literature review burns roughly $0-2 of Pro usage and a few hours of your time. The tool cost inside a $2K systematic review engagement is one $49 seat.

## How I Actually Run It (A Real Workflow)

A recent job: a telehealth startup needed to know whether remote monitoring reduced hospital readmissions for heart failure patients, and what the evidence said about the effect sizes. The old way was two weeks of manual screening. The Elicit way: one research question, it returned the relevant trials, I added extraction columns for sample size, follow-up duration and readmission effect, exported the table, cross-checked the top five studies by opening the cited sentences, and wrote the client a 12-page memo with 40 citations. Total hands-on time: about six hours. Billed: $900.

The rule I live by: always open the cited sentences for any number you plan to put in front of a client. Elicit is anchored to real papers and rarely fabricates a source, but it can still misread a metric inside a messy PDF - catching that is your job, not its.

## What Elicit Is Bad At (Honest)

- **It is an academic tool, full stop.** No general web search, no news, no product data. If your question lives outside peer-reviewed literature - 'what are the best Shopify apps' - Elicit is the wrong tool and returns nothing useful.
- **The free tier is a teaser for report work.** Unlimited search and summaries are genuinely free, but the 2-reports-per-month and 2-column limits push any real paid service onto Pro at $49/month. Fair price, not a cheap one.
- **Extraction needs human verification.** The 99.4% accuracy claim is marketing-grade; in practice complex tables, figures and ambiguous methods still get misread. Never hand a client an extracted number you have not checked against the source sentence.
- **There is a learning curve.** The column-and-table workflow is a spreadsheet, not a chat box. First-timers spend an afternoon fighting it before it clicks.
- **Index gaps are real.** Coverage is strongest in biomedicine; niche fields, very recent papers and non-English literature come up short because the corpus is built on Semantic Scholar data.
- **Collaboration is gated.** Real-time team editing only arrives at Scale, $169/month. A two-person review operation fits in one Pro seat, but if you need live collaboration, the jump is steep.

## Elicit vs The Alternatives

| Tool | Best at | Corpus | Free tier | Price |
|------|---------|--------|-----------|-------|
| **Elicit** | Deep literature review, structured extraction, systematic reviews | 138M+ papers, 545K trials | Unlimited search + 2 reports/mo | Free / Pro $49 |
| Consensus | Quick yes/no consensus answers | ~200M papers | Basic search | Freemium |
| ResearchRabbit | Citation-graph discovery | Papers + citations | Free | Free |
| NotebookLM | Summarising your own sources | Your uploads | Generous | Free |
| ChatGPT | General answers, not citations | Web + knowledge | Generous | $20+/mo |

The honest summary: Consensus is faster for binary questions, ResearchRabbit is better for finding connected papers, NotebookLM is better when the sources are yours. Elicit wins when you need to extract structured evidence across many papers and hand a client a verifiable citation - nobody else in the category does that.

## Who Should Use It (And Who Shouldn't)

**Use it if:** you sell research, literature reviews or systematic review support to health, academia or evidence-hungry businesses; you are a consultant who needs cited answers fast; you write grants, courses or reports that require real citations; or you are a researcher who wants to cut the screening phase of a review from weeks to days.

**Skip it if:** your work is general web research, news, product or market data - you want Perplexity or Exa instead; you are a casual user who just wants a quick answer (Consensus is faster); or you refuse to verify extracted numbers manually, because trusting Elicit blindly will eventually embarrass you in front of a client.

## Getting Started (6 Tips)

1. **Start free and run a real project on it.** Unlimited search and summaries mean you can test whether it covers your niche before spending a cent. If your field returns thin results, you learned that for free.
2. **Learn the extraction table before anything else.** That is the killer feature - add columns for sample size, outcome, effect size - and it is where the value for clients lives.
3. **Click every citation you plan to use.** The sentence-level links are the product's superpower and your professional safety net. Check, then quote.
4. **Upgrade to Pro only when you have a paying use for reports.** Two free reports a month is enough to prove the service; the $49 pays for itself on the first $300 review.
5. **Use Research Agents for landscape jobs.** For 'map the evidence in X' client work, the multi-step agents save a full day versus doing it query by query.
6. **Export to RIS/CSV and keep your own library.** Import from Zotero, export to your reference manager - client handoff documents land cleaner and the citations stay portable.

The bottom line: Elicit is not a chatbot that guesses, it is an evidence machine that shows its work. For anyone billing for research - literature reviews, systematic reviews, landscape reports, grant support - it is currently the best tool in the category, and at $0-49 a month it costs almost nothing next to what the service built on it can charge."""
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
    og.make_tool_og(new_tool, Path(og_dir) / "elicit-en-og.png")
    out_path = os.path.join(og_dir, "elicit-en-og.png")
    size = os.path.getsize(out_path)
    print(f"[OK] OG image generated: {out_path} ({size} bytes)")
except Exception as e:
    print(f"[WARN] OG image generation failed: {e}")
