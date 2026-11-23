#!/usr/bin/env python3
"""Remove fabricated statistics from EN articles (2026-11-23 E-E-A-T fix).

A fact-check of 81 "institution + precise number" claims found 51 with no
verifiable source (fabricated by the original content generator). This script
replaces each fabricated sentence with an honest, number-free version that
keeps the qualitative point, so articles stay readable. REAL claims (24) and
UNVERIFIED-but-plausible (6) are left untouched.

Source: outputs/suspicious-citations-audit-2026-11-22.md + fact-check report.
Idempotent: safe to re-run (skips anchors no longer present).
"""
import json
from pathlib import Path

DATA = Path("data/articles_en.json")
# (anchor prefix locating the exact sentence, replacement sentence)
# Replacement keeps the argument, drops the invented number/institution.
FIXES = [
    ("The American Bar Association's 2026 Legal Technology Survey found 67%",
     "Missed controlling authority is a real risk in legal research: the practical failure mode is opposing counsel citing a case your own research missed."),
    ("At 287 minutes — the mean time to resolution (MTTR)",
     "Long MTTR on unplanned outages turns each incident into a six-figure event once you multiply engineering hours by the business cost of downtime."),
    ("The average on-call rotation generates 173 alerts per week;",
     "A noisy on-call rotation generates more alerts than any human can triage, and most turn out to be duplicates or false positives."),
    ("41% of on-call engineers report burnout directly linked to alert fatigue",
     "Alert fatigue is one of the most common causes of on-call burnout, which is why alert grouping and deduplication matter more than adding more dashboards."),
    ("At weekly frequency, that is $13,780 per year — and 42% of private-practice therapists",
     "At weekly frequency the annual cost adds up fast, and many private-practice therapists no longer accept insurance at all."),
    ("A January 2026 APA survey found 46% of practicing psychologists report burnout",
     "Burnout and full caseloads are recurring themes in psychology workforce reporting, with many practitioners unable to take new clients."),
    ("Meanwhile, 53% of independent podcasters who switched to AI-assisted production tools",
     "Independent podcasters who adopt AI-assisted production generally protect their publishing consistency without a visible drop in listenership."),
    ("The same report found that 68% of in-house legal departments exceeded their outside counsel budget",
     "In-house legal teams routinely overspend on outside counsel, and contract review is one of the largest line items driving that overrun."),
    ("The Duke Law study found that experienced lawyers missed 17% of risky clauses",
     "Even experienced reviewers miss risky clauses under time pressure — which is exactly how in-house counsel works when the queue is deep and the business is waiting."),
    ("A 2026 Major Lindsey & Africa survey found 41% of mid-level associates",
     "Repetitive document review is a well-known driver of associate attrition at mid-level."),
    ("DeepSeek V4 Pro delivers a 82.6% success rate on the HumanEval coding benchmark",
     "DeepSeek V4 Pro is positioned as a frontier-level coding model at a fraction of Western frontier-model pricing, making it a cost-effective choice for developers and researchers."),
    ("73% of B2B marketers report that they have already automated at least 40%",
     "B2B marketing teams have widely adopted AI to automate lead qualification, though the exact share varies by survey."),
    ("According to data from the 2026 Video Marketing Trends Report",
     "Short-form video now dominates online attention, yet many small businesses still produce little video at scale because of the skill and equipment barrier."),
    ("82% of professional creators now report that AI-assisted video production",
     "Professional creators increasingly report lower per-project video costs after adopting AI-assisted production."),
    ("The top three AI website builders now ship sites that pass Lighthouse scores",
     "The leading AI website builders produce respectable out-of-the-box performance, though serious projects still benefit from manual optimization."),
    ("Another 41% reported higher click-through rates directly tied to AI-driven send-time optimization",
     "Marketers also report better click-through rates from AI-driven send-time optimization and subject-line testing."),
    ("Marketing teams spent an average of $12,400 per month on external design agencies",
     "External design agencies are a significant line item in many marketing budgets."),
    ("The same companies now spend $340 per month on AI design subscriptions",
     "AI design subscriptions cost a small fraction of agency retainers, which is why many teams are reallocating spend."),
    ("A June 2026 Tow Center for Digital Journalism study found Google's AI Overviews",
     "Research from the Tow Center has documented factual and citation problems in AI search summaries of current events."),
    ("67% of knowledge workers use at least three separate apps to manage notes",
     "Knowledge workers typically juggle several separate apps for notes, tasks, and research, and often lose track of where they saved something."),
    ("A 2025 McKinsey study found that data professionals spend 42% of their workweek",
     "Data professionals spend a large share of their week on manual preparation — cleaning, formatting, and wrestling with CSV files — instead of interpreting results."),
    ("McKinsey's 2026 Digital Operations Survey puts the global cost of manual data handling",
     "Manual data handling carries a large and growing cost as data volumes outpace hiring budgets."),
    ("Operators who wire their stack together report 15-25% operational cost cuts",
     "Teams that connect their automation stack usually see meaningful operational cost savings in the first year."),
    ("Atlassian's 2026 Workplace Productivity Report found that 62% of professionals forget",
     "People routinely forget action items within a day of a meeting and struggle to reconstruct decisions without checking the source."),
    ("The average small business in the United States pays $6,700 for a professional website build",
     "A professional website build is a meaningful expense for a small business, and the work is often abandoned when the owner cannot make basic updates."),
    ("According to the American Writers & Artists Institute, in-house copywriters burn 40%",
     "In-house copywriters spend a large share of their time on drafts that stakeholders heavily rewrite."),
    ("A 2026 DesignRush survey of 1,800 small business owners found",
     "Small business owners often spend more than they expected on a first logo, then replace it within a year or two as the brand evolves."),
    ("Portkey AI's 2026 State of GenAI Infrastructure report found",
     "Engineering teams increasingly use two or more model providers rather than betting on a single vendor."),
    ('A 2026 Social Media Examiner survey of 1,700 marketers found 64% cite "not enough time',
     'Marketers consistently cite "not enough time for content creation" as a top challenge, and teams using AI report faster publishing.'),
    ("while teams already using AI report a 47% reduction in publishing time",
     "while teams already using AI publish noticeably faster."),
    ("Buffer's 2026 State of Social Media report found that teams using AI-assisted scheduling",
     "Teams using AI-assisted scheduling often see better engagement, less because the copy is smarter and more because it frees time for higher-quality creative work."),
    ("because the questions were poorly structured and 61% of respondents dropped off halfway through",
     "because the questions were poorly structured and many respondents abandoned them halfway through."),
    ("SurveyMonkey's 2026 State of Surveys report found the average completion rate",
     "Survey completion rates are often disappointing, and poor question design invalidates many of the responses that do come in."),
    ('A 2026 Qualtrics research brief confirmed what anyone who\'s filled out a survey already knows: 67%',
     'Anyone who has filled out a survey knows that satisficing — giving minimally acceptable answers just to finish — is common.'),
    ("Legal departments report an even grimmer number: contract review teams at mid-sized firms spend 41%",
     "Contract review teams spend a large share of their time extracting and cross-referencing data across PDFs before any real analysis begins."),
    ("Meanwhile, freelance videographers on Fiverr reported 37% fewer inquiry-to-booking conversions",
     "Freelance videographers have faced softer demand as AI video tools absorb some entry-level work."),
    ("A 2026 survey by the Content Marketing Institute found that 64% of marketing teams",
     "Marketing teams spend more time editing and proofreading existing content than writing new material, and sloppy copy costs relationships."),
    ("Eye-tracking studies from the University of Sheffield's 2024 Language Processing Lab",
     "Proofreading accuracy falls with sustained editing as the brain starts autocorrecting what it expects to see rather than what is actually on the page."),
    ("The same study tracked 5,000 U.S. travelers and found 68% never cross-checked",
     "Travelers rarely cross-check every booking detail, which is exactly where planning tools earn their keep."),
    ("That's the percentage of RAG (Retrieval-Augmented Generation) pipelines that silently return",
     "RAG pipelines can silently return irrelevant or hallucinated context when vector retrieval is poorly tuned."),
    ("A 2026 Microsoft Research study found defect detection drops from 71% on the first review",
     "Code review quality decays as review volume rises, and senior reviewers often carry an outsized share of the queue."),
    ("Voices.com reported a 41% drop in average project value",
     "Voice-over project values have come under pressure as AI voice tools mature."),
    ("ElevenLabs' Turbo v2.5 model, released in March 2026, can clone a voice from 30 seconds",
     "Modern voice-cloning models can reproduce a speaker from a very short audio sample with striking fidelity."),
    ("67% of gym members quit within six months — 41% with unused sessions",
     "Many gym members quit within six months, leaving unused sessions on their accounts."),
    ("The CDC's 2026 National Health Statistics Report found 78% of adults",
     "A large share of adults who start a structured fitness program abandon it within the first few months."),
    ("4.7 diagrams per week is what the average product manager or engineer creates",
     "Product managers and engineers create diagrams regularly, and a large share go stale within months as systems and teams change."),
    ("Global web scraping revenue hit $6.35 billion in 2024 and is compounding",
     "The web-scraping market is growing quickly, yet many small teams still collect business data by hand — copy, paste, dedupe, repeat."),
    ("About 72% of organic search traffic now lands on pages that target long-tail keywords",
     "Long-tail keywords account for a large share of organic search traffic."),
    ("Meanwhile, 87% of marketers say keyword research is their top SEO priority",
     "Keyword research remains a top SEO priority, and the vast majority of keywords see negligible monthly search volume."),
    ("The 2026 FP&A Statistics Report from Limelight, which stitches together more than 50 benchmarks",
     "Industry benchmarks consistently show that finance teams still rely heavily on spreadsheets for monthly planning and reporting."),
    ("Frontline IT agent attrition runs at 41.5% a year with average tenure",
     "Frontline IT support roles see high attrition and burnout, which is why knowledge capture and deflection matter."),
    ("In dbt Labs' State of Analytics Engineering 2026, 57% of teams reported",
     "Analytics teams are seeing warehouse and compute costs rise faster than their budgets."),
]


def sentence_bounds(text, anchor):
    """Return (start, end) of the sentence containing anchor."""
    i = text.find(anchor)
    if i < 0:
        return None
    start = i
    for j in range(i - 1, max(-1, i - 500), -1):
        if text[j] in '.!?\n':
            start = j + 1
            while start < len(text) and text[start] in ' \t':
                start += 1
            break
    # sentence end: first ". " after anchor (skip decimals)
    end = i + len(anchor)
    while True:
        k = text.find('.', end)
        if k < 0:
            end = min(len(text), i + len(anchor) + 600)
            break
        if k + 1 < len(text) and text[k + 1].isdigit():
            end = k + 1
            continue
        end = k + 1
        break
    return start, end


def main():
    arts = json.loads(DATA.read_text(encoding="utf-8"))
    replaced, missing = 0, []
    for anchor, new in FIXES:
        hit = False
        for a in arts:
            c = a.get("content", "")
            b = sentence_bounds(c, anchor)
            if b:
                a["content"] = c[:b[0]] + new + c[b[1]:]
                replaced += 1
                hit = True
                break
        if not hit:
            missing.append(anchor)
    DATA.write_text(json.dumps(arts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[FIX] replaced {replaced}/{len(FIXES)} fabricated statements")
    if missing:
        print("[WARN] anchors not found:")
        for m in missing:
            print("  -", m)


if __name__ == "__main__":
    main()
