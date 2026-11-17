#!/usr/bin/env python3
"""Generate the 'AI Tool Pricing Index 2026' sample article from the snapshot.

All figures are injected from data/_pricing_index_snapshot.json — no hand-typed
numbers. Title tool-count and date come from the snapshot, so a monthly refresh
never carries stale numbers. Appends (or replaces by slug) one entry in
data/articles_en.json.
"""
import json
import os

SNAPSHOT = "data/_pricing_index_snapshot.json"
HISTORY = "data/_pricing_index_history.json"
ARTICLES = "data/articles_en.json"
SLUG = "ai-tool-pricing-index-2026"
CATEGORY = "AI Tools"


def money(v: float) -> str:
    if v == int(v):
        return f"${int(v)}"
    return f"${v:.2f}"


def build_content(s, date_str, prev=None):
    total = s["total_tools"]
    free = s["free_tier_count"]
    priced = s["priced_count"]
    unpriced = total - priced
    mean = s["mean_entry"]
    median = s["median_entry"]
    free_pct = free / total * 100
    priced_pct = priced / total * 100

    # month-over-month paragraph only when a prior snapshot exists
    mom_block = ""
    if prev:
        def delta(cur, old, suffix=""):
            if old is None:
                return ""
            d = cur - old
            if abs(d) < 0.005:
                return "unchanged"
            arrow = "up" if d > 0 else "down"
            return f"{arrow} {abs(d):g}{suffix}"
        mom_block = f"""
## What changed since the last update

Compared with our {prev['date']} snapshot, the database now tracks **{total} tools** ({delta(total, prev.get('total_tools'))}). The median entry price is **{money(median)}/mo** ({delta(median, prev.get('median_entry'))}), the mean is **{money(mean)}/mo** ({delta(mean, prev.get('mean_entry'))}), and the share of tools with a free tier is **{free_pct:.0f}%**. These shifts reflect both new tools entering the database and vendors changing plan prices — we do not treat every move as a market trend.
"""

    # category table: only categories with >= 3 priced tools, top 12 by median
    cats = [c for c in s["by_category"] if c["priced"] >= 3][:12]
    rows = []
    for c in cats:
        rows.append(
            f"| {c['category']} | {c['tools']} | {c['priced']} | {money(c['median'])} | {money(c['mean'])} |"
        )
    category_table = "\n".join(rows)

    # cheap / expensive callouts from the table
    cheapest = cats[-3:][::-1]
    priciest = cats[:3]

    content = f"""The price on an AI tool's homepage is rarely the price you pay. A "$20/mo" plan can mean a seat, a usage bucket, or an annual rate divided to look smaller. We pulled the published monthly price of every tool in our database to see what the market actually charges — and how much of it is free.

This is not a list of our favorite tools. It is a pricing dataset you can quote, with the method written down so you can check it. If you only want the short version: **{free} of {total} tools ({free_pct:.0f}%) advertise a free tier, and among the {priced} tools with a clearly published USD monthly price, the median entry plan is {money(median)} per month.**

## The headline numbers

We reviewed {total} tools across the categories we track. Here is what the pricing labels actually say:

- **{free} tools ({free_pct:.0f}%) advertise a free tier.** That includes limited free plans, open-source and self-hosted options, and free credit allowances. It does not guarantee the free tier is useful for real work.
- **{priced} tools ({priced_pct:.0f}%) publish a clear USD monthly price** we could extract and verify from their listed plan.
- **{unpriced} tools ({100-priced_pct:.0f}%) do not publish a comparable monthly figure.** These are API/usage-based tools, per-seat or per-builder plans, one-time purchases, non-USD pricing, or free-only products. We left them out of the averages rather than guess.
- **Median entry price: {money(median)}/mo. Mean: {money(mean)}/mo.** The gap between the two is the story — a handful of expensive suites pull the average up, while the typical tool sits near {money(median)}.
{mom_block}
## Entry price by category

The table below compares the **lowest published monthly plan** in each category. "Priced" is the number of tools in that category with a verifiable USD monthly figure; categories with fewer than three priced tools are excluded because the sample is too small to be meaningful.

| Category | Tools tracked | Priced | Median entry | Mean entry |
|---|---|---|---|---|
{category_table}

Read this as a map of where the market spends, not a shopping rule. Categories with few priced tools — especially AI Income, where most products take a commission instead of a subscription — have medians based on a small, self-selected sample.

## What the spread tells buyers

The cheapest entry points cluster in **{cheapest[0]['category']} ({money(cheapest[0]['median'])} median), {cheapest[1]['category']} ({money(cheapest[1]['median'])}) and {cheapest[2]['category']} ({money(cheapest[2]['median'])})**. These are the easiest categories to trial without a budget conversation.

The expensive end is **{priciest[0]['category']} ({money(priciest[0]['median'])} median), {priciest[1]['category']} ({money(priciest[1]['median'])}) and {priciest[2]['category']} ({money(priciest[2]['median'])})**. In AI SEO and marketing, suites bundle several jobs into one subscription, so a higher sticker price can still replace multiple smaller tools. That is a workflow decision, not a price comparison.

Two patterns are worth flagging. First, "free" is now the default entry point for most categories — the question is what the free tier lets you do before it becomes a paywall. Second, a low entry price often hides the real cost: per-seat billing, credit top-ups, or an API key you pay for separately. The {money(median)} median is a starting point for a budget, not the total cost of ownership.

## How we calculated this (methodology)

We extracted prices from the published plan labels in our tool database on {date_str}. The rules were deliberately conservative:

1. **Entry price** is the lowest explicitly stated USD per-month figure in a tool's plan label — for example "$29 - $249/mo" contributes $29, not $249.
2. **Annual-equivalent prices** (e.g. "$4.17/mo when billed yearly") are excluded, because they are not the month-to-month price.
3. **Per-seat, per-user, per-builder, per-token and per-sale figures are excluded**, because they are not comparable to a solo monthly plan.
4. **Non-USD prices, one-time purchases and usage-only pricing** are counted as "no published monthly price" rather than converted or estimated.
5. **Free tier** means the label advertises any form of free access, including limited plans, free credits, open-source and self-hosted options.

Prices change often and plans vary by region and billing terms. Treat every figure as a snapshot, and confirm the current price on the vendor's own site before you buy.

## Frequently asked questions

**What is the average cost of an AI tool?**
Across the {priced} tools with a published USD monthly price, the mean entry plan is {money(mean)}/mo and the median is {money(median)}/mo. The median is the more useful number: the average is pulled upward by a small group of premium suites.

**What percentage of AI tools have a free tier?**
{free} of {total} tools ({free_pct:.0f}%) advertise some form of free access. A free tier is best treated as a way to test the workflow, not as a guarantee that the tool can run your workload at no cost.

**Which category is most expensive?**
In our data, {priciest[0]['category']} has the highest median entry price at {money(priciest[0]['median'])}/mo, followed by {priciest[1]['category']} at {money(priciest[1]['median'])}, though each is based on a small number of priced tools.

**Why are some tools missing from the averages?**
{unpriced} tools do not publish a monthly USD figure we can compare — they charge by usage, per seat, by commission, or only quote enterprise rates. We exclude them rather than invent a number. Their pricing may still be excellent value for the right buyer.

## Can I use these numbers?

Yes, with attribution. This is original research from our own tool database. Quote a figure with a link back to this page and note that prices are a {date_str} snapshot. If you need the underlying dataset or want to check a specific tool, each tool's detail page lists its current published price and source.
"""
    return content


def main():
    s = json.load(open(SNAPSHOT, encoding="utf-8"))
    date_str = s["generated_date"]
    total = s["total_tools"]
    title = f"AI Tool Pricing Index 2026: What {total} Tools Actually Cost"

    # previous snapshot for month-over-month comparison
    prev = None
    if os.path.exists(HISTORY):
        hist = json.load(open(HISTORY, encoding="utf-8"))
        earlier = [h for h in hist if h.get("date") < date_str]
        if earlier:
            prev = sorted(earlier, key=lambda h: h["date"])[-1]

    content = build_content(s, date_str, prev)
    desc = (
        f"We analyzed the published price of {total} AI tools. "
        f"{s['free_tier_count']} offer a free tier; the median paid plan is "
        f"{money(s['median_entry'])}/mo. Original data, reproducible method."
    )
    keywords = (
        "AI tool pricing 2026,AI tools pricing index,average cost of AI tools,"
        "AI tool free tier statistics,AI software median price,AI pricing report 2026"
    )
    article = {
        "title": title,
        "slug": SLUG,
        "date": date_str,
        "category": CATEGORY,
        "description": desc,
        "keywords": keywords,
        "content": content,
    }

    articles = json.load(open(ARTICLES, encoding="utf-8"))
    articles = [a for a in articles if a.get("slug") != SLUG]
    articles.append(article)
    with open(ARTICLES, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"[OK] article '{SLUG}' written ({len(content)} chars). Total articles: {len(articles)}")


if __name__ == "__main__":
    main()
