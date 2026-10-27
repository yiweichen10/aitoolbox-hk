#!/usr/bin/env python3
"""Trim article #204 to <=2800 words and fix keyword presence; re-verify."""
import json, re

PATH = 'data/articles_en.json'

REPLACEMENTS = [
    # intro
    (" That arithmetic decides more pipeline budgets than any feature matrix, so it belongs at the top of this comparison.",
     " That arithmetic decides more pipeline budgets than any feature matrix."),
    ("I have run production pipelines on all four — a five-developer SaaS on GitHub Actions, a 400-job monorepo on CircleCI, a compliance-locked fintech still on Jenkins — and the pattern that holds is this:",
     "I have run production pipelines on all four — from a five-developer SaaS on GitHub Actions to a 400-job monorepo on CircleCI — and the pattern holds:"),
    (" Here is how each platform actually prices in 2026, where each one wins, and the mistakes that cost real money on all of them.", ""),
    # diverge section
    ("with a marketplace of tens of thousands of reusable actions and hosted runners", "with hosted runners"),
    ("and 30 to 80 concurrent jobs on plans where GitHub's default concurrency is 20.", "and up to 80 concurrent jobs where GitHub's default is 20."),
    (" Jenkins monetizes nothing and competes for your operations time instead. That is why the pricing sections below read so differently — each vendor meters a different thing.",
     " Jenkins monetizes nothing and competes for your operations time instead."),
    ("a MIT-licensed automation server with more than 1,800 plugins, in continuous operation since 2011.",
     "a MIT-licensed automation server with more than 1,800 plugins."),
    # GitHub Actions section
    ("and any larger runner you configure — the 4-core and up machines — always bills, even in public repositories, even against unused quota.",
     "and any larger runner you configure always bills, even in public repositories."),
    ("Second, macOS minutes cost ten times Linux minutes, and no plan quota distinguishes them:",
     "Second, the GitHub Actions macOS minutes cost ten times the Linux rate, and no plan quota distinguishes them:"),
    # CircleCI section
    ("Credits are the unit of account: a dollar buys about 1,667 credits at list rates ($15 per 25,000), dropping further on prepaid bulk — 1 million credits for $600, with volume discounts starting at 5 million for $3,000.",
     "Credits are the unit of account: $15 buys 25,000, dropping to $600 per million on prepaid bulk with volume discounts from 5 million at $3,000."),
    ("For a monorepo where a full test suite takes 40 minutes serially, splitting across 30 parallel executors turns a 40-minute feedback loop into a 3-minute one, and that compounds across every developer on every commit.",
     "For a monorepo whose suite takes 40 minutes serially, splitting across 30 executors turns that into a 3-minute feedback loop, and it compounds across every commit."),
    ("Teams running both report the crossover point in different places, because CircleCI's credit consumption depends entirely on which resource classes you pick — a large VM burns roughly four times the credits of a small one, so a careless default can double the bill without anyone noticing.",
     "CircleCI's credit consumption depends entirely on resource class — a large VM burns roughly four times the credits of a small one — so a careless default can double the bill."),
    # GitLab section
    ("rolling over month to month and valid for 12 months — a notably friendlier policy than use-it-or-lose-it quotas elsewhere.",
     "rolling over month to month and valid for 12 months."),
    ("A team that bumps its default runner size to medium to shave queue times has silently doubled its quota consumption — 10,000 included minutes becomes 5,000 effective ones.",
     "Bumping the default runner to medium to shave queue times silently doubles quota consumption — 10,000 included minutes becomes 5,000 effective ones."),
    ("What GitLab buys with that $29 is consolidation. Static application security testing ships on every tier including Free, and Premium and Ultimate layer on vulnerability management, compliance pipelines, and value-stream analytics in the same application.",
     "What GitLab buys with that $29 is consolidation: static application security testing ships on every tier including Free, with vulnerability management, compliance pipelines, and value-stream analytics layered on above — all in the same application."),
    # Jenkins section
    ("Where Jenkins still wins is legitimate and worth stating plainly.", "Where Jenkins still wins is worth stating plainly."),
    ("security patching on a server that, unpatched, is a genuine attack surface sitting inside your network,",
     "security patching on a server that, unpatched, is a genuine attack surface,"),
    ("and the institutional knowledge of one or two people who understand the pipeline grove. When those people leave, Jenkins estates calcify — I have watched a team discover that nobody dared touch their build system for two years.",
     "and the institutional knowledge of one or two people who understand the pipeline grove. When those people leave, Jenkins estates calcify."),
    ("And the hybrid pattern is increasingly common and perfectly rational: keep Jenkins for the legacy monolith, put new repositories on GitHub Actions or GitLab, and let attrition shrink the Jenkins estate over five years instead of funding a big-bang migration.",
     "The hybrid pattern is increasingly rational: keep Jenkins for the legacy monolith, put new repositories on GitHub Actions or GitLab, and let attrition shrink the Jenkins estate instead of funding a big-bang migration."),
    # fit section
    ("the free quota covers most small products indefinitely, overage is priced fairly, and the config lives beside the code",
     "the free quota covers most small products indefinitely and the config lives beside the code"),
    ("Three integration notes from painful experience.", "Three integration notes."),
    ("covers how virtual-user-hour meters work, and the same budget discipline applies to whichever CI platform schedules them.",
     "covers how virtual-user-hour meters work."),
    # FAQ
    ("Jenkins is free everywhere but you operate it. ", ""),
    ("For a typical OSS project, GitHub's public-repo free tier plus GitLab's program as a second pipeline covers everything most projects will ever need.",
     "For a typical OSS project, that combination covers everything most projects ever need."),
    ("or move native builds to CircleCI, whose free tier includes one macOS M4 Pro slot and whose Performance plan prices macOS through the same credit meter as everything else.",
     "or move native builds to CircleCI's free macOS M4 Pro slot."),
    ("A five-person Linux-only shop should expect $5–15 a month on Actions and $25–60 on CircleCI for identical work; an iOS shop should expect the reverse, sometimes dramatically.",
     "A five-person Linux-only shop spends $5–15 a month on Actions and $25–60 on CircleCI for identical work; an iOS shop sees the reverse."),
    ("The migration pattern that works is incremental — mirror new repositories to a managed platform first, then port legacy pipelines as they change, keeping Jenkins alive for the residue. Teams with years of accumulated pipeline scripts should price the rewrite honestly before committing; a quarter of engineer time often exceeds five years of subscription fees, which is exactly why Jenkins estates persist.",
     "Migrate incrementally: mirror new repositories to a managed platform first, then port legacy pipelines as they change. Teams with years of accumulated pipeline scripts should price the rewrite honestly before committing; a quarter of engineer time often exceeds five years of subscription fees."),
    ("and the security of letting untrusted PR code touch your infrastructure",
     "and letting untrusted PR code touch your infrastructure"),
    # bottom line
    ("with fair overage pricing and a free tier that covers small products indefinitely — until an iOS build crosses the meter at ten times the rate.",
     "with fair overage pricing — until an iOS build crosses the meter at ten times the rate."),
    ("Before picking any of them, export your last three months of build minutes, tag them by operating system, and price that workload on all four meters — the invoice you model is the decision, and it takes an afternoon to know exactly which one wins.",
     "Before picking, export your last three months of build minutes, tag them by operating system, and price that workload on all four meters — the invoice you model is the decision."),
]

with open(PATH, encoding='utf-8') as f:
    data = json.load(f)

arts = [a for a in data if a['slug'] != 'best-cicd-tools-2026-github-actions-vs-gitlab-vs-circleci-vs-jenkins']
removed = len(data) - len(arts)
if removed != 1:
    raise SystemExit(f"Expected to remove exactly 1 entry, removed {removed}")

a = arts[-1]  # target entry is now the previous last; find by re-appending below
target = None
entry = json.load(open('_article_204_entry.json', encoding='utf-8'))

content = entry['content']
for old, new in REPLACEMENTS:
    if old not in content:
        raise SystemExit(f"NOT FOUND: {old[:70]}...")
    content = content.replace(old, new)
entry['content'] = content

# update keyword list
entry['keywords'] = [
    "CI/CD tools",
    "GitHub Actions pricing",
    "CircleCI vs GitHub Actions",
    "GitLab CI/CD pricing",
    "Jenkins alternatives",
    "free CI/CD for open source",
    "GitHub Actions macOS minutes cost",
    "self-hosted runners"
]
arts.append(entry)

with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(arts, f, ensure_ascii=False, indent=2)

c = entry['content']
words = len(re.findall(r'\S+', c))
pk = 'CI/CD tools'
print('total articles:', len(arts))
print('words:', words)
print('PK cs/ci:', c.count(pk), len(re.findall(re.escape(pk), c, re.I)))
print('keyword present:', all(re.search(re.escape(k), c, re.I) for k in entry['keywords'][1:]))
banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline','delve','transformative','comprehensive','revolutionize','cutting-edge','as an AI','in conclusion']
print('banned found:', [b for b in banned if re.search(re.escape(b), c, re.I)])
