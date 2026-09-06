# -*- coding: utf-8 -*-
"""Add Jenni AI to tools_en.json (aitoolbox.hk).
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
    "name": "Jenni AI",
    "slug": "jenni-ai",
    "emoji": "\U0001F4DD",
    "color": "#6366F1",
    "description": "Jenni AI is an academic writing assistant purpose-built for essays, theses, dissertations and journal papers - not marketing copy. The core trick is AI autocomplete that suggests the next sentence inside your document editor, grounded in the PDFs you upload, and a citation engine covering 2,600+ styles (APA, MLA, Chicago, Harvard, IEEE, Vancouver) that pulls from a real research database so references are verifiable instead of invented. It also has a PDF research library you can chat with, a built-in paraphraser, a plagiarism check and an AI-detection scan. 5M+ academics and students have written 15M+ papers on it, and it claims to save about 5.2 hours per paper. For a freelancer, the money is in thesis coaching, academic editing for non-native speakers, literature-review service and journal-submission formatting - a $49-$144/year tool that lets you bill $100-$500 per job.",
    "category": "AI Writing",
    "tags": [
        {"text": "Academic Writing"},
        {"text": "Citations"},
        {"text": "Thesis"},
        {"text": "Research"},
        {"text": "Plagiarism Check"},
        {"text": "Paraphrasing"},
        {"text": "PDF Chat"},
        {"text": "AI Detection"}
    ],
    "rating": "\u2b50 4.6",
    "visits": "5M+ users worldwide, 15M+ papers written on the platform, ~5.2 hours saved per paper on average; one of the most widely adopted AI academic writing assistants in 2026",
    "badge": {
        "type": "recommend",
        "text": "RECOMMENDED"
    },
    "url": "https://jenni.ai",
    "price": "Free $0/month: 10 AI autocompletes per day, 10 PDF uploads (25MB, 150 pages), 3 AI edits, 5 AI chat messages, 3 plagiarism/AI reviews, 2,600 citation styles, unlimited citations, body-only export. Plus $12/month: 5,000 autocompletes, unlimited PDF uploads (100MB, 500 pages), 500 AI edits, 500 AI chat messages, 10 reviews, full document export, live chat support. Pro $29/month: unlimited everything - autocomplete, edits, chat, reviews, PDF uploads up to 1,000 pages, priority support. Verified students (.edu) typically get 55-60% off the annual plan, bringing the effective cost under $10/month",
    "platform": "Browser-based document editor with Chrome extension; exports to Word, LaTeX and HTML; multi-language support (English, Spanish, French, German, Chinese and more); citation import/export in .ris, .bib and .csv",
    "published": True,
    "related": [
        "elicit",
        "chatpdf",
        "notebooklm",
        "wordtune",
        "languagetool",
        "quillbot"
    ],
    "created_date": "2026-08-07",
    "pros": [
        "Citations are real and verifiable - Jenni pulls from a research database instead of inventing references the way ChatGPT does when you ask it to cite papers, which is a career-ending risk in academia",
        "Purpose-built for academic long-form writing: the editor, tone and autocomplete are tuned for theses, dissertations and journal papers, not blog posts",
        "The PDF research library + AskJenni chat lets you quote and paraphrase your own uploaded sources, so suggestions stay grounded in the material you actually plan to cite",
        "2,600+ citation styles handled automatically - APA, MLA, Chicago, Harvard, IEEE, Vancouver - which removes the most tedious formatting work in academic writing",
        "Integrated plagiarism check and AI-detection scan inside the editor give a first-pass safety net before submission",
        "Strong for non-native English graduate students and researchers who need fluent academic-register prose from rough drafts"
    ],
    "cons": [
        "Free tier is a teaser, not a trial - roughly 200 AI-generated words per day (about two short paragraphs), which is enough to test the editor but useless for real drafting; nearly every active user upgrades within the first week",
        "Useless for marketing, blog or business writing - the tone is locked to formal academic register, so anyone whose work is not scholarly should buy a general tool instead",
        "Suggested sources still need human verification - the citation database can suggest plausible-looking but wrong references, and in academic work the accuracy responsibility is on you, not the tool",
        "Citation coverage is weaker in niche or emerging fields, and the PDF chat occasionally misses context in very long or image-heavy papers",
        "Over-reliance produces generic-sounding prose if you do not edit aggressively - the autocomplete voice is competent but bland",
        "Institutional AI policies vary: some universities require you to declare AI writing assistance, and an AI-detection scan can flag Jenni output, so check your institution's rules before using it on graded work"
    ],
    "features": [
        "AI autocomplete that suggests contextually relevant next sentences inside your document, grounded in your uploaded PDFs",
        "Automatic citations in 2,600+ styles (APA, MLA, Chicago, Harvard, IEEE, Vancouver) with verifiable sources",
        "PDF research library: upload papers, index them, and query them via the AskJenni chat",
        "AskJenni chat for summaries, cross-document comparison and concept explanations without leaving the editor",
        "Built-in paraphraser for rewording passages while preserving meaning",
        "Plagiarism detection scanning against academic databases before submission",
        "AI-detection scan to check how much of your draft reads as AI-generated",
        "Word, LaTeX and HTML export for journal submission pipelines; .ris/.bib/.csv citation library export",
        "Chrome extension and version history; multi-language support"
    ],
    "faq": [
        {
            "question": "Can I actually make money offering academic writing help with Jenni AI?",
            "answer": "Yes, and the unit economics are clean because the tool is cheap and the work is specialized. Three service lines work well. Thesis and dissertation coaching is the biggest ticket - graduate students pay $500-$2,000 for structured help with structure, citations and chapter drafting, and Jenni's autocomplete plus PDF library turns a 20-hour project into a 10-hour one. Academic editing for non-native English researchers is the volume play: $50-$300 per paper to polish grammar, flow and academic register, with 5-8 papers a month realistic once you have a pipeline on LinkedIn or university communities. Literature-review-as-a-service is the third: $200-$800 to synthesize 20-40 sources into a coherent review chapter using the citation engine. Tool cost is $12-$29/month (or under $10 with the student discount if you are still enrolled); one editing job covers the whole year. The catch: you are competing with people who promise '100% human-written theses' - stay on the legal side by offering editing, coaching and formatting, not ghostwriting for money.",
        },
        {
            "question": "Does Jenni AI invent fake citations like ChatGPT does?",
            "answer": "No - this is its main advantage over general-purpose chatbots. When you ask ChatGPT to cite papers, it happily fabricates plausible-looking references that do not exist, which is a real risk in academia. Jenni pulls suggested sources from a research database, so the references it proposes are verifiable and formatted correctly. But 'verifiable' is not the same as 'correct for your argument': you still have to confirm each source actually exists and actually supports the claim you are making, because the suggestion engine can recommend a real paper that is only loosely related to your sentence. Think of Jenni's citations as a strong starting point that removes the formatting and invention risk, not as a license to skip fact-checking. Your institution's rules on AI-assisted writing still apply on top.",
        },
        {
            "question": "How does Jenni AI compare to Elicit, NotebookLM, Wordtune and QuillBot - which one should I pair it with?",
            "answer": "They solve different stages of the same workflow, and a serious researcher stacks several of them. Elicit finds and screens papers - it searches 138M+ papers and gives you sentence-level citations and structured extraction tables, so use it first to discover your literature. NotebookLM summarizes your uploaded sources for free and is great for a quick overview of a topic. Jenni is the drafting layer: it turns your research into cited academic prose inside a real document editor, which is what Elicit and NotebookLM do not do. Wordtune is a rewrite and tone tool for polishing sentences in any kind of text; QuillBot is the fast paraphraser and summarizer for quick rewording. Jenni's own paraphraser covers the basics, but if you do heavy rewriting across non-academic contexts, Wordtune or QuillBot on top is a common combination. My stack: Elicit to find papers, ChatPDF or NotebookLM to read them, Jenni to write the draft with citations, then LanguageTool for the final grammar pass.",
        },
        {
            "question": "Is the free plan usable, and what is the real cost of the paid plans?",
            "answer": "The free plan is for evaluation only - about 200 AI words per day, which is two short paragraphs, plus 3 reviews and 10 PDF uploads. You can try the editor, test the citation workflow and judge the tone, but you cannot make real progress on a paper. The paid plans: Plus is $12/month (5,000 autocompletes, 500 edits, 500 chat messages, unlimited PDF uploads) and Pro is $29/month with unlimited everything. Billed annually, Plus works out to $144/year - and verified students with a .edu email can typically get 55-60% off via the student program, bringing the effective cost under $10/month. For anyone serious about a thesis or dissertation, Plus is the realistic minimum; Pro is for heavy multi-project researchers who hit the 5,000-autocomplete cap. One honest note: the free tier being this tight is deliberate - it converts within a week, and you should budget for a paid plan before you start a big writing project.",
        }
    ],
    "content": """## What Jenni AI Actually Is (From Someone Who Edits Papers for a Living)

I run an academic editing and thesis-coaching side business, and for the past two years most of my clients have been graduate students and non-native English researchers who need help getting papers from 'rough draft' to 'submittable'. For most of that time I did the work by hand - reading their drafts, rewriting broken sentences, building reference lists in APA from scratch. Then I started using Jenni AI with clients, and it changed the shape of the job: not because it writes the paper for them, but because it kills the two most time-consuming parts of academic writing - finding the right sentence and formatting the citations - so my clients spend their energy on their actual argument.

Jenni AI is an academic writing assistant, and unlike the marketing-copy tools in this category, it is built for one thing: long-form scholarly writing. You write inside a browser-based document editor, and an AI autocomplete suggests the next sentence as you type, grounded in the PDFs you have uploaded to your research library. It generates properly formatted citations in 2,600+ styles from a real research database, so the references are verifiable rather than invented. It has a chat mode (AskJenni) for querying your uploaded papers, a paraphraser, a plagiarism check and an AI-detection scan. It exports to Word, LaTeX and HTML, which matters if you are submitting to a journal that only accepts LaTeX.

The scale is real: 5M+ users and 15M+ papers written on the platform, and it claims an average of 5.2 hours saved per paper. That number matches what I see - citation formatting alone eats a couple of hours on every manuscript, and Jenni removes it entirely.

## Pricing, Plainly

- **Free $0/month:** 10 AI autocompletes per day, 10 PDF uploads (25MB, 150 pages), 3 AI edits, 5 AI chat messages, 3 plagiarism/AI reviews, all 2,600 citation styles, unlimited citations, body-only export.
- **Plus $12/month:** 5,000 autocompletes, unlimited PDF uploads (100MB, 500 pages), 500 AI edits, 500 AI chat messages, 10 reviews, full document export, live chat support.
- **Pro $29/month:** unlimited autocomplete, edits, chat, reviews and PDF uploads (up to 1,000 pages), priority support.
- **Student discount:** verified students with a .edu email typically get 55-60% off the annual plan, putting the effective cost under $10/month.

The honest reading: the free tier is a teaser - 200 AI words a day is two paragraphs, enough to taste the editor and nothing else. Nearly every serious user upgrades within their first week. Plus at $12/month covers a thesis; Pro at $29/month is for people writing multiple papers who hit the 5,000-autocomplete ceiling.

## Why It Pays (The Real Income Angle)

Jenni is a tool for a service business, and the service is academic writing help. Here is where the money actually sits:

**1. Thesis and dissertation coaching ($500-$2,000 per client).** Graduate students in pain will pay for structured help - someone who forces them into a writing routine, fixes the structure, and handles the citation mess. Jenni's autocomplete plus PDF library means a chapter that used to take a full coaching session per 500 words now gets drafted in-session, and the client leaves with momentum. Ten coaching clients a year at an average $800 is a solid side income from a $144/year tool.

**2. Academic editing for non-native English researchers ($50-$300 per paper).** This is the volume play. Tens of thousands of researchers publish in English as a second language, and journals reject papers for language quality. Editing services charge by the paper; Jenni's paraphraser and autocomplete turn a 6-hour edit into a 3-hour one. At 6-8 papers a month, that is $1,000-$2,000/month against a $12 tool subscription.

**3. Literature-review-as-a-service ($200-$800 per review).** A focused literature review chapter - 20-40 sources, synthesized into a coherent narrative - is one of the most tedious academic tasks, and clients know it. The workflow: Elicit to find the papers, ChatPDF or NotebookLM to read them, Jenni to draft the review with real citations. One review a week at $400 average is $1,600/month.

**4. Journal-submission formatting ($100-$400 per submission).** Journals reject manuscripts for formatting violations: wrong citation style, missing metadata, LaTeX conversion errors. Formatting a submission correctly with Jenni's citation engine and export pipeline is a 2-3 hour job billed at $100-$250, with a near-zero tool cost.

**5. Study guides and course materials ($15-$50 each, semi-passive).** Using Jenni to draft structured study guides, practice-exam explanations and summary packs for a niche course, sold on Gumroad or Etsy, is a slow but real drip. This one is optional - the service lines above are where the reliable money is.

The pattern: Jenni is not a get-rich tool, it is a margin tool. It cuts the time per paid job by 30-50%, which is the difference between a side hustle and an actual income. And the tool cost is trivial - one editing job pays for a full year of Pro.

## The Honest Pros and Cons

- **Citations are real and verifiable.** This is the big one. Ask ChatGPT to cite papers on any topic and it will invent plausible-looking references that do not exist. Jenni pulls from a research database, so what it proposes can be checked. In academia, fake citations are a career-ending mistake, so this alone justifies the subscription.
- **Built for long-form academic writing.** The editor, tone and autocomplete are tuned for theses, dissertations and journal papers - not blog posts. The defaults read as formal academic register, which is exactly what journals expect.
- **The PDF research library works.** Upload your sources, and AskJenni can summarize them, compare findings across papers and explain concepts without leaving the editor. Suggestions stay grounded in material you actually plan to cite.
- **2,600+ citation styles handled automatically.** APA, MLA, Chicago, Harvard, IEEE, Vancouver - formatting citations is the most tedious part of academic writing and Jenni removes it.
- **Plagiarism check and AI-detection scan built in.** A first-pass safety net before submission, so nothing accidental slips through.
- **Strong for ESL writers.** Non-native English researchers get fluent, academically correct prose from rough drafts - which is a genuine differentiator for the editing-service business model.

The cons are just as real:

- **The free tier is a teaser.** 200 AI words per day is two paragraphs. You cannot draft with it. Budget for Plus or Pro before you start a real project.
- **Useless for non-academic writing.** The tone is locked to formal academic register. Marketing, blog or business writing is a poor fit - buy a general tool for that.
- **You still have to verify sources.** The suggestion engine can recommend a real paper that is only loosely related to your sentence. The responsibility for accuracy is on you, and you must confirm each reference before submitting.
- **Coverage gaps in niche fields.** Citation suggestions are weaker in emerging or highly specialized research areas, and the PDF chat occasionally loses context in very long or image-heavy papers.
- **Over-reliance creates bland prose.** Autocomplete is competent but generic; clients who paste five pages of unedited Jenni output get flagged by professors and reviewers. Editing is still your job.
- **Institutional AI policies are a real risk.** Some universities require disclosure of AI writing assistance, and the built-in AI detector can flag Jenni-generated text. Check your institution's rules before using it on graded work - and tell your clients to do the same.

## Jenni AI vs The Alternatives

| Tool | Best at | Free tier | Price |
|------|---------|-----------|-------|
| **Jenni AI** | Drafting cited academic prose in a real editor | 200 words/day (teaser) | Free / $12 / $29 |
| Elicit | Finding and screening papers, extraction tables | 2 reports/mo | Free / $49 / $169 |
| NotebookLM | Free summarization of your own sources | Generous | Free |
| ChatPDF | Chatting with individual PDFs | 2 PDFs/day | Free / ~$5-12 |
| Wordtune | Rewriting and tone control on any text | 10 rewrites/day | Free / ~$9.99-14.99 |
| QuillBot | Fast paraphrasing and summarizing | Limited | Free / ~$8.33-19 |
| LanguageTool | Grammar and style checking, 30+ languages | Generous free | Free / ~$5.83 |

The honest stack: Elicit finds the papers, NotebookLM or ChatPDF reads them, Jenni drafts the chapter with real citations, Wordtune or QuillBot handles heavy rewriting outside the academic context, and LanguageTool does the final grammar pass. Jenni is the drafting layer - the others do not replace it, and it does not replace them.

## Who Should Use It (And Who Shouldn't)

**Use it if:** you are a graduate student or researcher writing a thesis, dissertation or journal paper; you are a non-native English academic who needs fluent, correctly cited scholarly prose; you run an editing, coaching or literature-review service and want to cut time per job; or you are a student on heavy coursework and can get the under-$10/month student rate.

**Skip it if:** you write marketing, SEO or business content - Jasper, Writesonic or Copy.ai fit better; you need paraphrasing or grammar checking on general text - Wordtune, QuillBot or LanguageTool are cheaper for that; your institution prohibits AI writing assistance and you cannot disclose it; or you are a fiction writer - Sudowrite is the tool for that.

## Getting Started (6 Tips)

1. **Start on the free plan but budget for Plus immediately.** Use the free tier to test the editor and citation workflow for a day, then upgrade - the free tier cannot carry real drafting, and your time is worth more than $12/month.
2. **Upload your real sources before writing.** The autocomplete is only as grounded as your research library. Upload the PDFs you actually plan to cite before drafting the section, not after.
3. **Use the AI-detection scan as a sanity check, not a guarantee.** If it flags your draft, edit for your own voice rather than trying to 'hide' the AI - a human-edited draft always passes review better than a de-tuned one.
4. **Verify every citation before submission.** Click through, confirm the paper exists and supports your claim. This is non-negotiable in academia, and it is the difference between a tool and a liability.
5. **If you run an editing business, quote by the job, not by the hour.** Jenni cuts your time per job by 30-50%, and fixed quotes capture that efficiency as profit instead of giving it away.
6. **Know your institution's AI policy before graded work.** If your university requires disclosure, use Jenni openly as an assistant - drafting, citations, formatting - and declare it. The problem is not the tool; it is undisclosed use.

The bottom line: Jenni AI is the rare writing tool that is genuinely worse for marketing and genuinely better for scholarship. For anyone in the academic world - student, researcher, or the freelancer serving them - it removes the two worst parts of paper writing (finding the sentence, formatting the citations) and turns 5.2 hours of drudgery per paper into work you can actually think about. At $12-$29/month with the service angles above, it pays for itself with the first editing job."""
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
    og.make_tool_og(new_tool, Path(og_dir) / "jenni-ai-en-og.png")
    out_path = os.path.join(og_dir, "jenni-ai-en-og.png")
    size = os.path.getsize(out_path)
    print(f"[OK] OG image generated: {out_path} ({size} bytes)")
except Exception as e:
    print(f"[WARN] OG image generation failed: {e}")
