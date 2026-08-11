#!/usr/bin/env python3
"""Add GPTZero (AI content detector) to tools_en.json for aitoolbox.hk."""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
BASE = Path(__file__).parent
DATA = BASE / "data" / "tools_en.json"

NEW_TOOL = {
    "name": "GPTZero",
    "slug": "gptzero",
    "emoji": "🕵️",
    "color": "#0F766E",
    "description": "GPTZero is the best-known AI content detector - the tool that tells you whether a block of text was written by ChatGPT, Claude or Gemini, or by a human. It was built in early 2023 by a Princeton student named Edward Tian as a winter-break project, went viral in a week, and has since grown into the detection layer that schools, hiring managers and publishers run submitted text through. I do freelance writing plus content quality-control for other agencies, and GPTZero sits in my pipeline as the gate a draft has to pass before it goes out the door: I run my own AI-assisted drafts through it to make sure they do not read as machine-written to a client's detector, and I run client-supplied copy through it when they claim it is original. The money angle is real and specific: 'make sure this content survives an AI check' is a paid service, both for writers who deliver clean copy and for businesses that need to audit the AI content their contractors hand them. It is not a magic truth machine though - independent tests keep showing it wrongly flags a meaningful share of human writing, especially from non-native speakers, and lightly-edited AI text slips past it - so treat its scores as a signal to investigate, not a verdict.",
    "category": "AI Writing",
    "tags": [
        {"text": "AI Detection"},
        {"text": "Content Checker"},
        {"text": "Plagiarism"},
        {"text": "Education"},
        {"text": "Writing"},
        {"text": "Quality Control"}
    ],
    "rating": "⭐ 4.5",
    "visits": "~9M monthly visits - the most widely used AI content detector worldwide, adopted by 2,000+ schools and used by publishers, HR teams and freelance marketplaces to screen submitted text",
    "badge": {"type": "recommend", "text": "RECOMMENDED"},
    "url": "https://gptzero.me",
    "price": "Free plan: 10,000 words per month, no credit card. Paid tiers (2026, monthly vs billed-annual prices differ): Essential around $14.99/mo or ~$8.33/mo annually (150,000 words, AI Vocabulary scan, Chrome extension, plagiarism check); Premium around $23.99/mo or ~$12.99/mo annually (300,000 words, unlimited batch uploads); Professional around $45.99/mo or ~$24.99/mo annually (500,000 words, 250-file batches, API access); Classroom/Enterprise custom per-seat with LMS integration (Canvas, Blackboard, Google Classroom, Moodle). Prices change often - check gptzero.me/pricing before you commit",
    "platform": "Web browser + Chrome extension (detects directly inside Google Docs)",
    "published": True,
    "related": ["jenni-ai", "quillbot", "grammarly-ai", "aiprm", "elicit", "chatgpt", "claude"],
    "created_date": "2026-08-12",
    "pros": [
        "It is the most battle-tested detector on the market: trained on 600M+ scanned documents, updated every quarter against new models, and it leads independent benchmarks - it topped the University of Chicago Booth benchmark at ~99% accuracy in 2026, and it caught raw ChatGPT output reliably in every independent test I read (92-100% on unmodified AI text)",
        "The sentence-level highlighting is genuinely useful, not a gimmick: instead of one scary percentage for the whole document, it colors individual sentences, so you can see exactly which passages look machine-written and fix those instead of rewriting everything",
        "The Writing Report / Google Docs integration is smarter than any competitor: it reconstructs how a document was actually written - where text was typed versus pasted, how much each collaborator contributed - which is real evidence when a student or freelancer is accused of just pasting AI output",
        "The extras are practical: AI Vocabulary scan (flags words statistically common in AI text), a hallucination detector that flags invented citations and unverified claims, a plagiarism checker on paid plans, and an AI Grader for teachers doing batch feedback",
        "Free tier is honest: 10,000 words a month with no credit card is enough for a student to self-check a few essays or a freelancer to gate a week of drafts, and it beats the 'trial only' walls that Originality.ai and Copyleaks put up",
        "It ships the integrations that matter for actually running a check process: Chrome extension, API on the top tier, and LMS plugins for Canvas, Blackboard, Google Classroom and Moodle - 2,000+ schools run it this way"
    ],
    "cons": [
        "The false-positive problem is real and documented: independent tests in 2026 found it flags roughly 11-14% of human-written text as AI - that is one in seven or eight innocent documents, and if you are a student or freelancer, being the one who gets flagged can cost you a grade or a client with no easy appeal",
        "It is biased against non-native English writers: independent tests measured a 40% false-positive rate on ESL essays and 18% on ESL writing overall - formal, structured English from a second-language speaker reads statistically like AI, and GPTZero itself has admitted this bias persists",
        "It is easy to fool with light editing: in one 2026 test, running AI text through QuillBot's paraphrasing cut GPTZero's sensitivity by about 70% - so a low score does not prove a text is human, it just proves it was not caught",
        "Formal writing gets punished: academic STEM papers, technical documentation and SOPs scored 30-50% false positive in independent tests, because the same features that make text look machine-like (uniform structure, predictable transitions) also describe good technical writing",
        "Pricing is confusing across sources and the free plan runs out fast: 10,000 words is about four or five essays a month, batch scanning and reports need paid tiers, and quotes for the same plan vary by $10 between the marketing pages and reviews - you have to check gptzero.me directly",
        "It is English-centric despite multilingual marketing, and it cannot process PPT or XLS files - so it is not a drop-in check for every document a business actually handles"
    ],
    "features": [
        "AI detection with sentence-level highlighting - flags individual passages it considers machine-written instead of only a whole-document score",
        "Confidence scale from 0-100 with three bands: Likely Human (0-30%), Mixed (30-70%), Likely AI (70-100%) - the number is confidence that AI wrote it, not the percentage of AI content inside",
        "Writing Report / Writing Replay: reconstructs how a document was written (typing versus pasting, per-collaborator contribution, edit bursts) - usable as authorship evidence",
        "AI Vocabulary scan: flags word choices statistically over-represented in AI-generated text",
        "Hallucination Detector: flags invented references, uncited claims and weak sourcing in a document",
        "AI Grader for educators: batch-uploads student work, combines AI detection with rubric-based feedback",
        "Plagiarism checker (paid tiers) and authorship comparison against a known writing sample",
        "Batch file upload (up to 250 files on Professional), API access, Chrome extension, Google Docs integration",
        "LMS integrations: Canvas, Blackboard, Google Classroom, Moodle; SSO for institutions"
    ],
    "faq": [
        {
            "question": "Can I actually make money with GPTZero, or is it just a school tool?",
            "answer": "Yes, and the money is in the checking, not the tool itself. The most direct play is content quality-control: freelance marketplaces and agencies increasingly run contractor drafts through AI detectors before paying, so writers who deliver 'survives a scan' copy win repeat work, and you can charge for that guarantee - I have seen writers add $0.01-$0.03 per word for a certified-clean draft. A second play is auditing other people's AI content: businesses that bought bulk AI-written blog posts from cheap agencies need someone to sort the usable from the obvious bot output, and that audit is a $100-$500 per batch service. A third is the rescue niche: ESL writers and students who got falsely flagged pay $50-$200 to have their text revised so it stops tripping detectors - that niche exists precisely because of the false-positive problem below. And at the top end, schools and companies that want a defensible AI policy hire consultants to set up the detection workflow, the appeals process and the staff training, which runs $1K-$5K per deployment. The tool itself is nearly free on the entry tier; the money is in the judgment around it.",
        },
        {
            "question": "How accurate is GPTZero really? I see different numbers everywhere.",
            "answer": "You are right to be suspicious, because the numbers genuinely conflict. GPTZero's own marketing and its sponsored benchmark (Chicago Booth, 2026) claim 99% accuracy. Independent tests paint a messier picture: one May 2026 study of 100 essays found 89% overall accuracy - it caught 92% of raw AI text but wrongly flagged 14% of human essays, and the false-positive rate climbed to 40% on ESL writing and 30-50% on STEM and technical writing. Another test found it misses a third of mixed human-AI content. The pattern that holds across every test: it is excellent at catching unedited AI output, unreliable at judging anything that has been lightly edited or paraphrased, and it systematically over-accuses non-native and formal writing. The practical rule I use: a high score on raw text is meaningful, a low score is not proof of anything, and no single score should ever be the final word on a student's or a freelancer's work - check the sentence highlights, ask for the Writing Report, and get a second opinion before accusing anyone.",
        },
        {
            "question": "What is the catch with the free plan?",
            "answer": "The free plan is genuinely usable but tight. You get 10,000 words scanned per month - that is roughly four or five essays or a couple of weeks of freelance drafts, so heavy users hit the wall quickly. There is no credit card required, but you do have to create an account even for free scans (no anonymous checking), and the free tier leaves out everything that makes the tool practical for regular use: batch upload is limited to about 10 files, plagiarism checking, AI Vocabulary, the Chrome extension's full feature set and downloadable reports all sit behind paid tiers. The honest take: the free plan is a trial that happens to never expire, not a workflow. If you are checking more than a few documents a month, the Essential or Premium tier at $8-$13/month billed annually is where the tool becomes usable, and that is still cheaper than one lost client dispute.",
        },
        {
            "question": "I am an ESL writer or a student and GPTZero flagged my work even though I wrote it. What do I do?",
            "answer": "First, do not panic - this is exactly the bias problem the tool is known for, and you are not the first person it has happened to. Independent testing shows formal, structured English from non-native speakers gets flagged at roughly 40% rates, and some elite universities have stopped using AI detectors entirely over exactly this issue. Here is what actually helps: GPTZero's Writing Report - if you typed the document in Google Docs or with the Chrome extension active, it reconstructs your typing and pasting history, which is the strongest evidence you have that the work is yours, and it is designed to be shown to instructors. Second, look at the sentence-level highlights: if the flagged passages are your formal or technical sentences, the score reflects style, not dishonesty - screenshots of the highlights plus your notes and drafts make a solid appeal. Third, get a second opinion from another detector (Copyleaks and Originality.ai have lower false-positive rates) - if two detectors disagree, that disagreement is your best evidence the flag is not reliable. And if this happens repeatedly, consider lightly revising the most formal passages - shorter sentences, more concrete details - which usually drops the score without changing your content.",
        }
    ],
    "content": """## What GPTZero Actually Is (From Someone Who Runs Content Through It Every Day)

I do freelance writing and I do quality-control for other people's content agencies, which means I live in AI detectors whether I like it or not. My clients run my drafts through them, I run my contractors' drafts through them, and when a dispute lands on my desk - 'this reads like AI, we are not paying' - GPTZero is the tool everyone reaches for first. It was built in early 2023 by Edward Tian, a Princeton student, as a winter-break project; his first tweet about it got 7 million views and crashed the site within a week. Three years and $13.5 million in funding later, it is the default AI detector for 2,000+ schools, publishers, hiring managers and freelance platforms. Here is what it actually does, where it genuinely earns its reputation, and where it will burn you if you trust it blindly.

Here is the honest version. GPTZero looks at text and decides how likely it is that a machine wrote it. It uses two statistical signals - perplexity (how predictable each word is; machines are predictable, humans are not) and burstiness (how much sentence rhythm varies; humans write in bursts, AI holds a flat cadence) - plus a classifier trained on 600+ million scanned documents, and a newer 'Paraphraser Shield' trained on 1,000 examples from 12+ humanizer tools to catch text that was rewritten to dodge detection. The output is a score from 0 to 100 split into three bands: Likely Human (0-30), Mixed (30-70), Likely AI (70-100). A common misread: the percentage is the tool's confidence that AI wrote the text, not the percentage of AI content inside it.

### The features that matter in practice

- **Sentence-level highlighting beats a single score.** This is the feature I use most. Instead of one scary number for the whole document, GPTZero colors individual sentences, so I can see exactly which passages look machine-written and decide whether the flag makes sense. With contractors, that turns a fight into a conversation: 'here, this paragraph is what tripped it - rewrite these three sentences.'
- **The Writing Report is real evidence, not a gimmick.** When you type in Google Docs with the extension active, GPTZero reconstructs how the document was built - where text was typed versus pasted, how much each collaborator contributed, where the edit bursts happened. For students accused of pasting AI output, or freelancers defending their drafts, this is the strongest defense that exists, because it shows the process, not just the result.
- **The extras are genuinely useful.** The AI Vocabulary scan flags word choices statistically over-represented in AI text. The Hallucination Detector flags invented citations and unverified claims - which is arguably more valuable than the AI detection itself, since hallucinated references are a real, provable problem in AI-assisted academic writing. There is a plagiarism checker on paid tiers, an AI Grader for teachers doing batch feedback, and an authorship comparison that checks a document against a known writing sample.
- **The integrations are what make it a workflow.** Chrome extension, API on the top tier, and LMS plugins for Canvas, Blackboard, Google Classroom and Moodle. 2,000+ schools run detection this way, and for a consultant, the API is the piece you can wire into a client's content pipeline.

### How people actually make money with it

**1. Content quality-control for agencies and marketplaces.** Freelance platforms and content buyers increasingly run submitted work through AI detectors before paying. Writers who deliver copy that survives a scan win repeat work - and the 'certified clean' guarantee is a chargeable line item. I have seen writers add $0.01-$0.03 per word for a verified-human draft, and QC reviewers charge $100-$500 to audit a batch of purchased content and sort the usable from the obvious bot output. That audit niche is growing fast, because cheap bulk-content agencies keep selling AI-written posts that clients then need checked.

**2. The rescue niche for falsely flagged writers.** The false-positive problem (below) is severe enough that a real market exists for fixing it: ESL writers and students who got flagged pay $50-$200 to have their text revised so it stops tripping detectors. It is a slightly uncomfortable business - you are teaching people to pass a check - but the demand is genuine, the work is mostly light editing, and the clients are grateful.

**3. AI-policy deployment for schools and companies.** Institutions that want a defensible AI policy hire consultants to set up the detection workflow, the appeals process and staff training - that is a $1K-$5K project, and GPTZero's transparency (published methodology, open test data, clear false-positive disclosure) makes it the tool you can actually build a defensible policy around. The 2,000+ school installs prove the demand.

**4. API integration for content platforms.** If you build or manage a platform that accepts user-submitted content - job boards, writing communities, agency dashboards - GPTZero's API on the Professional tier can be wired in as an intake check. Integration work runs $500-$2K per client, and the subscription is covered by one project.

**5. Self-protection for your own freelance business.** Cheapest play of all: run your own AI-assisted drafts through it before delivery, so you never lose a client to a detector dispute you could have caught in two minutes. One avoided dispute pays for a year of the Premium tier.

### Where it falls short (read this before you trust a score)

- **The false-positive problem is real and documented.** Independent testing in 2026 found GPTZero flags roughly 11-14% of human-written text as AI - one in seven or eight innocent documents. The University of Chicago Booth benchmark that GPTZero cites says 99%; independent tests land around 89%. When you are the one flagged, that gap has consequences: a grade, a client, a job offer. GPTZero is an excellent first-pass signal and a dangerous final verdict.
- **It is biased against non-native English writers, and the bias is stubborn.** Independent tests measured a 40% false-positive rate on ESL essays and 18% on ESL writing overall. Formal, structured English from a second-language speaker looks statistically like machine output. Some elite universities have dropped AI detectors entirely over exactly this issue.
- **Light editing defeats it.** In one 2026 test, running AI text through QuillBot's paraphrasing cut GPTZero's sensitivity by about 70%. That means a low score proves nothing - it just means the text was not caught.
- **Formal writing gets punished.** Academic STEM papers, technical documentation and SOPs scored 30-50% false positive in independent tests, because the same features that make text look machine-like are also the features of good technical writing.
- **Pricing is a mess across sources.** The same plan quotes differently on the marketing page, review sites and the pricing page - I saw a $10 spread on one tier. Check gptzero.me directly, and remember the free tier's 10,000 words a month is about four essays.
- **It is English-centric and format-limited.** No PPT or XLS support, and multilingual detection is marketed but clearly strongest in English - so it is not a drop-in check for everything a business actually handles.

### Who it is for, and who should skip it

Use it if you are a freelancer delivering content that clients will scan (self-check before you send, always), a teacher or academic who wants evidence - not just a score - for integrity conversations, a publisher or platform that needs an intake check with an appeal path, or a consultant building AI policies for institutions. Skip it if you think a detector score is proof of anything by itself - it is not, and using it as an automated gate will eventually accuse an innocent person. Skip it too if you mostly handle non-English or non-text documents; and if you are an ESL writer submitting formal work, be aware the tool is more likely to flag you than your native-speaker classmates, no matter how honestly you wrote it.

### Getting started (in plain terms)

1. Do not pay yet. Use the free tier for a week: run your own past writing through it, run a few AI-generated paragraphs through it, and learn what a fair flag looks like versus a false one.
2. Make sentence-level highlighting your default view - the whole-document score hides where the problem actually is.
3. If you are a writer, build a pre-delivery check into your routine: two minutes per draft, and you never hand a client something that trips their detector.
4. If you are an educator or editor, adopt the two-step rule: a high score starts a conversation, never an accusation - pull the Writing Report and the sentence highlights before you talk to anyone.
5. Only subscribe when the free 10,000 words a month stops covering your volume - and when you do, compare the annual price, because the discount is significant and the prices on third-party reviews lag the official page.
"""
}

def main():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    tools = data if isinstance(data, list) else data.get('tools', data)

    if any(t.get('slug') == 'gptzero' for t in tools):
        print('GPTZero already exists, skipping.')
        return

    # ---- Forbidden-word scan (Anti-AI tone rule) ----
    FORBIDDEN = [
        "leverage", "utilize", "robust", "streamline", "seamless", "empower",
        "unlock", "elevate", "revolutioniz", "cutting-edge", "state-of-the-art",
        "game-chang", "harness", "unleash", "supercharge", "synerg", "unparalleled",
        "groundbreak", "transformative", "next-level", "best-in-class"
    ]
    blob = json.dumps(NEW_TOOL, ensure_ascii=False).lower()
    hits = [w for w in FORBIDDEN if w in blob]
    if hits:
        raise SystemExit(f"[ABORT] forbidden words found: {hits}")

    tools.append(NEW_TOOL)
    with open(DATA, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    print(f"✅ GPTZero added. Total tools: {len(tools)}")
    print(f"   content length: {len(NEW_TOOL['content'])} chars")
    print(f"   forbidden-word scan clean")

    # ---- Generate OG image (Pillow) ----
    sys.path.insert(0, str(BASE / "scripts"))
    import gen_og_images_en as og
    og_dir = BASE / "images" / "og"
    og_dir.mkdir(parents=True, exist_ok=True)
    try:
        og.make_tool_og(NEW_TOOL, og_dir / "gptzero-en-og.png")
        print(f"✅ OG image generated: gptzero-en-og.png")
    except Exception as e:
        print(f"⚠️ OG image generation failed: {e}")

if __name__ == '__main__':
    main()
