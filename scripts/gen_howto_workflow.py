#!/usr/bin/env python3
"""Generate a task-style how-to article (workflow tutorial) for the EN site.

Positioning: the site has 184 'best/vs' listicles but almost no step-by-step
tutorials, which are the highest-CTR intent for English readers. This article
is a real-work workflow with copyable prompts and internal links to tool pages.
"""
import json
from datetime import date

ARTICLES = "data/articles_en.json"
SLUG = "how-to-use-ai-at-work-2026"
TITLE = "How to Use AI at Work in 2026: A Step-by-Step Daily Workflow"
DATE = date.today().isoformat()
CATEGORY = "AI Guide"

CONTENT = """Most "how to use AI at work" advice stops at a list of tools. This walks through one realistic working day, the exact task I give the assistant at each step, and the check I run before the output reaches a colleague. You can copy the prompts as written and swap in your own details.

The point is not to add another tool to your stack. It is to hand three recurring jobs — planning, drafting and communication — to the assistant that is best at each, and to know where the output still needs a human.

## The workflow at a glance

| Time of day | Job | Tool that fits | What you check |
|---|---|---|---|
| Morning | Turn a messy task list into a realistic plan | ChatGPT | Deadlines and hours add up |
| Mid-morning | Draft a document from your own notes | Claude | Figures and claims match your notes |
| Midday | Draft and tighten emails | ChatGPT | Every promise is one you can keep |
| Afternoon | Work inside Gmail and Docs | Gemini | Names, dates and tone |
| Any time | Research with sources you can open | Perplexity | Follow the links, not the summary |

This is deliberately three tools, not eight. Each extra assistant adds a login, a habit and a place for context to get lost. If your workplace already standardises on one, the task patterns below still apply to it.

## Step 1: Plan the morning with a real constraint

Open [ChatGPT](https://www.aitoolbox.hk/tools/chatgpt/) and give it something concrete: your tasks, your deadlines and the hours you actually have. The constraint is what turns a generic list into a plan you can react to.

Copy this prompt, filling the brackets:

> Here are my tasks today: [list]. My deadlines this week are [list]. I have [6] focused hours. Build an hourly schedule, prioritise by deadline and importance, and flag anything that is unrealistic.

The useful part is the flagging. A plan that silently assumes nine hours of focus is worse than no plan. Read the flags before you accept the schedule.

If your work lives in Google Calendar and Docs, [Gemini](https://www.aitoolbox.hk/tools/gemini/) can do this step without the copy-paste. Pick one and stay with it for a week.

## Step 2: Draft from your own notes, not from nothing

The largest time saving is editing a draft rather than generating every sentence from scratch. Put your research notes and a rough outline into [Claude](https://www.aitoolbox.hk/tools/claude/), then ask for a first draft with a specific shape.

> Draft a [one-page brief] from these notes: [paste notes]. Readers: [who]. Keep it under [400] words, use short paragraphs, and do not add any fact that is not in my notes. List anything you think is missing at the end.

Two details matter. "Do not add any fact that is not in my notes" keeps invented statistics out. "List anything missing" turns the assistant into a reviewer instead of just a generator.

Claude is the pick here because it holds a long document in context and keeps tone steady past roughly 1,000 words. If your drafting is mostly short marketing copy, a dedicated writing tool such as [Jasper](https://www.aitoolbox.hk/tools/jasper/) is worth a look — but for a solo workflow its brand-voice setup adds complexity without a clear gain over a free plan.

## Step 3: Tighten a draft in two rounds

Never send the first response. Treat it as a draft and ask for a specific change:

> Make this 20% shorter. Keep the decision in the first sentence. Then give me a second version that sounds less formal.

Two or three rounds is normal. If you want a grammar pass on the final text, [Grammarly AI](https://www.aitoolbox.hk/tools/grammarly-ai/) covers that job; it is a checker, not a writer, and the distinction saves you from outsourcing your voice.

The habit that actually compounds: when a prompt produces a good result, save it in a note with blanks where the variable parts go. A small library of five reusable prompts is where the time savings come from.

## Step 4: Handle email and the apps you already live in

For a routine reply, describe what you want in plain language rather than composing it first:

> Draft a reply to [paste message]. I want to [say yes / ask for the date / decline politely]. I cannot promise [X]. Keep it under 120 words and match a friendly but direct tone.

Read it back before sending, and check every promise against what you can actually deliver. For anything that involves a colleague, you are the author — and therefore the reviewer.

When the work is inside Gmail or Google Docs, stay in [Gemini](https://www.aitoolbox.hk/tools/gemini/) instead of moving text between tabs. For meetings, [Otter.ai](https://www.aitoolbox.hk/tools/otter.ai/) can produce the transcript you then summarise with either assistant.

## Step 5: Research with sources you can verify

For any question where a wrong answer costs you something, use a tool that shows its sources. [Perplexity](https://www.aitoolbox.hk/tools/perplexity/) attaches links to each claim.

> Summarise the current pricing of [tool category] with the source link for each figure. Flag any figure you cannot verify from a primary source.

Then open at least the top two links. A summary is a starting point; the source is the evidence. This one habit separates a usable answer from a confident-sounding error.

## What not to hand to an assistant

Keep three categories away from the workflow above: anything with personal data your employer has not approved, anything that is a legal or financial commitment, and anything you would not be willing to sign your name to after a quick fact-check. The assistant drafts; you decide.

Many workplaces now have a written policy on what may be pasted into a chatbot. If you have not seen yours, ask before your first "real" task — a five-minute question that protects you later.

## Frequently asked questions

**Which single AI tool should I start with?**
If you are unsure, start with ChatGPT for an all-rounder, Claude if you write and read long documents, or Gemini if your day runs on Gmail and Docs. One tool learned properly beats three used badly. All three have usable free plans.

**Can I do this workflow on a free plan?**
Yes. The steps above use capabilities available in the free tiers of ChatGPT, Claude and Gemini, with daily limits. You only hit a paywall when you need higher volume, faster models or team features.

**How do I stop AI drafts from sounding generic?**
Give context before the task: who you are, who reads the output and what "good" looks like. Then refine in a second round with a concrete instruction such as "shorter" or "less formal". The back-and-forth, not the first prompt, is where quality comes from.

**Do I need to pay for several tools to run this workflow?**
No. Three free accounts cover the whole day. Paid plans make sense when usage limits start interrupting work, not before. See the [AI Tool Pricing Index](/articles/ai-tool-pricing-index-2026/) for what the market actually charges.

## Make it yours

Run this workflow for one week before changing tools. Keep the prompts that worked, drop the steps you never used, and add a verification check wherever an error would be expensive. The goal is a smaller set of habits you actually repeat — not a bigger stack of subscriptions.
"""


def main():
    articles = json.load(open(ARTICLES, encoding="utf-8"))
    article = {
        "title": TITLE,
        "seo_title": "How to Use AI at Work in 2026: Daily Workflow",
        "slug": SLUG,
        "date": DATE,
        "category": CATEGORY,
        "description": (
            "A step-by-step AI workflow for a real working day: plan with ChatGPT, "
            "draft with Claude, handle email and Docs, and research with sources. "
            "Copyable prompts and honest checks at every step."
        ),
        "keywords": (
            "how to use AI at work,AI workflow 2026,how to use ChatGPT for work,"
            "how to use Claude for writing,AI at work step by step,AI prompts for work"
        ),
        "content": CONTENT,
    }
    articles = [a for a in articles if a.get("slug") != SLUG]
    articles.append(article)
    with open(ARTICLES, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"[OK] '{SLUG}' written ({len(CONTENT)} chars). Total: {len(articles)}")


if __name__ == "__main__":
    main()
