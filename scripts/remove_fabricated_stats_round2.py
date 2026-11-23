#!/usr/bin/env python3
"""Round-2 removal of fabricated third-party statistics (2026-11-23).

First pass removed 51 fabricated stats from the initial 81-claim audit.
A full-text rescan surfaced another 125 "institution + percentage" claims.
This pass rewrites the ones with no verifiable source (fictional 2026
reports/surveys, invented institution+number pairings) into honest,
number-free statements. Claims that are REAL (Salesforce 28%, Wyzowl 91%,
Stanford TOEFL 61%, IEEE 0.05%, HBR 83%, Blind 20%, ISE 61%, Gartner 36%,
Deloitte 92%, iProov 741%, LangChain 89%, FinOps 98%, Uptime 40%/85%,
ITIC 90%, Postman 55%, Stack Overflow 3.6%, Duke/LawGeex 2018) and vendor
self-reports / pricing calculations are intentionally left untouched.

Idempotent: skips anchors no longer present.
Backup: data/articles_en.json.bak-fabrication-r2
"""
import json
import shutil
from pathlib import Path

DATA = Path("data/articles_en.json")
BAK = Path("data/articles_en.json.bak-fabrication-r2")

# (exact sentence to replace, honest number-free replacement)
FIXES = [
    ("Amazon's legal department disclosed at the 2026 CLOC Global Institute that their attorneys using AI research tools reduced research time by 61% while improving motion-to-dismiss win rates by 14 percentage points.",
     "Legal teams using AI research tools commonly cut the time spent on first-pass research, leaving more room for strategy and motion preparation."),
    ("The 2026 Thomson Reuters survey of 1,200 law firm partners found 78% expect to reduce summer associate class sizes by at least 20% within three years, and 64% expect to reduce first-year associate hiring.",
     "Legal-industry observers expect AI to reshape entry-level staffing, with firms rethinking summer associate and first-year hiring as routine research gets automated."),
    ("A 2025 Oxford BMJ Open study evaluated Ada against 200 clinical vignettes across 8 specialties: 71% top-3 diagnostic accuracy, 93% triage accuracy.",
     "Ada has been evaluated against clinical vignettes in peer-reviewed work, but published accuracy varies widely by specialty and case mix."),
    ("Buoy's 2026 HLTH conference data reported 12-18% reduction in unnecessary ER utilization within 12 months, averaging $287 per employee per year.",
     "Vendors in this space report reductions in unnecessary ER visits among their customers — useful signal, but treat vendor-reported figures with care."),
    ("A 2026 University of Waterloo study compared AI checkers against Google for 150 symptom presentations: AI tools hit 68-76% correct in top suggestions; Google's first page hit 34%.",
     "Independent comparisons have found symptom checkers more accurate than a general web search for many presentations, though neither is a substitute for a clinician."),
    ("A 2026 Forrester Total Economic Impact study commissioned by Dynatrace reported that organizations using Davis reduced MTTR by 68% compared to their previous tooling.",
     "AIOps vendors report substantially shorter resolution times after adopting causal AI — treat commissioned ROI figures as directional rather than universal."),
    ("A 2025 JMIR study found college students using Woebot for 4 weeks reported a 22% drop in PHQ-9 depressive scores.",
     "Woebot has been studied in peer-reviewed journals for short-term mood outcomes, with results that are promising but not a substitute for clinical care."),
    ("A January 2026 Columbia Journalism Review study found that Perplexity Pro's factual accuracy on news queries was 84%, compared to 76% for Google's AI Overviews.",
     "Independent reviews of AI search engines consistently find meaningful factual-error rates, which is why citations and source-checking still matter."),
    ("> **Bottom line:** For academic and research, choose Perplexity Pro (95% citation accuracy).",
     "> **Bottom line:** For academic and research, choose Perplexity Pro for its strong citation habits — but verify sources independently."),
    ("Because Eightfold matches on skills and potential rather than pedigree, companies using it report a 22–35% increase in underrepresented candidates reaching the interview stage.",
     "Because it matches on skills and potential rather than pedigree, employers report a more diverse interview pipeline."),
    ("The Xero survey found 23% of SMEs had at least one material bookkeeping error per year, with an average $2,700 correction cost in accountant fees alone.",
     "Bookkeeping errors are common among small businesses, and the accounting fees to correct them can add up quickly."),
    ("A 2026 Siegel+Gale study found that inconsistent visual branding reduced perceived trustworthiness by 28% in first-time visitors.",
     "Inconsistent visual branding undermines trust with first-time visitors, which is why design consistency matters even for small teams."),
    ("ELSA's phoneme-level analysis was independently tested against human speech pathologists in a 2025 Cambridge study — 94% agreement on phoneme-level errors, plus 12% of errors human raters missed.",
     "ELSA's pronunciation feedback has been compared against human speech pathologists, with broadly comparable judgments on pronunciation errors."),
    ("This approach, according to a 2026 LegalTech Hub survey of 200+ legal departments, reduces contract review time by 55-70% while maintaining or improving review accuracy by catching clauses human reviewers frequently overlook.",
     "Legal teams using this approach report faster contract review while maintaining accuracy, because automation catches clauses that busy reviewers can overlook."),
    ("The Association for Supply Chain Management (ASCM) found 73% of companies experienced at least three major disruptions in 2025 — port closures, raw material shortages, logistics bottlenecks, demand whiplash — and 61% admitted their response was reactive, not predictive.",
     "Supply chains have faced repeated disruptions in recent years — port closures, material shortages, logistics bottlenecks — and many companies still respond reactively rather than predicting them."),
    ("The National Association of Realtors' 2026 Member Profile found 43% of agents burn 10+ hours per week running comparable sales analyses.",
     "Agents spend a significant part of their week running comparable-sales analyses — exactly the repetitive work these tools target."),
    ("A separate benchmark of 323,000 videos found that adding text correlated with 19% fewer views on average, which means your text has to earn its place by creating a question the title does not answer, not by restating the title.",
     "Large-scale video analyses have found that on-screen text can correlate with lower watch time, so text should add information rather than repeat the title."),
    ("McKinsey's 2025 State of AI report found that data quality and availability are the top two barriers to AI scaling for 57% of enterprises, ahead of talent, budget, and infrastructure.",
     "Industry surveys consistently rank data quality and availability among the top barriers to scaling AI, ahead of talent or budget."),
    ("Swiss Post reported unlocking 89% more customer data by replacing restricted access with a synthetic twin.",
     "Swiss Post has publicly described using synthetic data to expand access to customer insights while respecting privacy constraints."),
    ("Case studies report 50-80% reductions in onboarding time, and the platform holds a 4.7 on G2 across nearly 1,000 reviews.",
     "Vendors report large reductions in onboarding time, and the platform is well reviewed on G2 — treat the efficiency claims as vendor-reported."),
    ("Agency reporting through 2026 also shows roughly 34% higher rejection rates for health and beauty AI creative, which is not a coincidence.",
     "Agencies report higher rejection rates for AI creative in regulated categories like health and beauty, which is not surprising."),
    ("Automated extraction cuts manual error rates by up to 90%, and cost benchmarks show 75% to 92% reductions per document.",
     "Automated extraction can sharply reduce manual errors and per-document cost compared with hand-keying."),
    ("Chargebacks911's 2026 field report, based on more than 250 merchants, found merchants attribute 43.8% of chargebacks to friendly fraud, while its own case data puts it at 86%.",
     "Industry reports differ widely on how much chargeback volume is friendly fraud, depending on whether they use merchant surveys or network data."),
    ("UK research from The Payments Association found 58% of online retailers believed AI-initiated transactions had already reached their platforms, while only 41% felt confident in existing liability frameworks.",
     "Payments-industry surveys find retailers are already seeing agent-initiated transactions while remaining uncertain about liability rules."),
    ("A widely reported Riskified briefing from April 2026 put agent-attributed chargebacks up 34% in Q1 2026 — mostly consumers who authorized an agent, received the goods, then disputed the charge on the grounds that they never personally authorized that specific transaction.",
     "Fraud vendors report a new pattern of agent-attributed chargebacks: a consumer authorizes an agent, receives the goods, then disputes the charge as unauthorized."),
    ("Spend Matters research cited in Forrester's 2026 agentic AI study puts it bluntly: roughly 90% of procurement software fails because of poor adoption.",
     "Analysts often note that procurement software succeeds or fails on user adoption rather than features."),
    ("Kaleidoscope's 2026 modelling research splits it further: 42% of finance teams rely exclusively on spreadsheets, 45% spend significant time manually updating data, and 44% spend major time checking for errors, while 72% want more specialised modelling tools.",
     "Finance-team surveys consistently find heavy spreadsheet dependence, with much of the month spent updating and checking data rather than analysing it."),
    ("One 2026 industry survey puts high use of a purchased CDP at 22% of marketers — the CDP activates data, it does not clean it, and teams that buy before fixing event taxonomy end up with an expensive routing layer.",
     "Relatively few marketers report getting full value from a purchased CDP — the platform activates data, it does not clean it, so buying before fixing taxonomy leaves you with an expensive routing layer."),
    ("A release summary reports 52% AI adoption and a shift in attention toward gross revenue retention and outcomes.",
     "Vendors report growing AI adoption and a shift in customer-success metrics toward retention and outcomes."),
    ("Postman's own survey found 51% of developers worried about AI agents making unauthorized or excessive API calls, and an agent that can read your collections can also leak the secrets inside them.",
     "Developers increasingly worry about AI agents making unauthorized API calls — and an agent that can read your collections can also expose the secrets inside them."),
]


def main():
    if not BAK.exists():
        shutil.copy2(DATA, BAK)
        print(f"[BACKUP] {BAK}")
    arts = json.loads(DATA.read_text(encoding="utf-8"))
    replaced, missing = 0, []
    for old, new in FIXES:
        for a in arts:
            c = a.get("content", "")
            if old in c:
                a["content"] = c.replace(old, new)
                a["dateModified"] = "2026-11-23"
                replaced += 1
                break
        else:
            missing.append(old)
    DATA.write_text(json.dumps(arts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[FIX] replaced {replaced}/{len(FIXES)}")
    if missing:
        print("[WARN] not found:")
        for m in missing:
            print("  -", m[:90])


if __name__ == "__main__":
    main()
