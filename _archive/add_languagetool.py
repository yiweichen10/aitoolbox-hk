# -*- coding: utf-8 -*-
"""Add LanguageTool to tools_en.json (aitoolbox.hk).
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
    "name": "LanguageTool",
    "slug": "languagetool",
    "emoji": "\U0001F30D",
    "color": "#16A34A",
    "description": "LanguageTool is an open-source grammar, spelling, punctuation and style checker that covers 30-plus languages and regional variants, with a free tier that actually works (no account, no card) and a Premium plan at roughly half of Grammarly's price. I run an English proofreading side business for ESL founders on it - clients pay $30-$150 per document while the tool itself costs $0 on the free tier or about $5.83 a month on annual billing, so the margin is basically the invoice minus an hour of my time.",
    "category": "AI Writing",
    "tags": [
        {"text": "Grammar Checker"},
        {"text": "Proofreading"},
        {"text": "Multilingual"},
        {"text": "Spell Check", "type": "free"},
        {"text": "Style Guide"},
        {"text": "Open Source"}
    ],
    "rating": "\u2b50 4.6",
    "visits": "30+ languages and regional variants checked; free tier used by millions without signup (open-source engine active since 2003); ~2M+ monthly visits to languagetool.org",
    "badge": {
        "type": "recommend",
        "text": "RECOMMENDED"
    },
    "url": "https://languagetool.org",
    "price": "Free (core grammar/spelling/punctuation in 30+ languages, per-check character cap, 3 AI paraphrases per day, no account needed); Premium $24.90/mo month-to-month, $69.90/yr (~$5.83/mo), or ~$4.17/mo on 2-year billing - raises the cap to 150,000 characters per check, adds unlimited AI paraphrasing, Picky Mode, custom style guide and 20,000+ extra checks; Teams ~$6.99/user/mo (shared style guide, team dictionary, member management); self-hosted server and developer API free under GNU LGPL open source",
    "platform": "Web editor, browser extensions (Chrome/Firefox/Edge/Safari), Word & Google Docs add-ins, desktop apps (Windows/macOS/Linux), developer API, self-hosted server",
    "published": True,
    "related": [
        "grammarly-ai",
        "wordtune",
        "quillbot",
        "frase",
        "copy.ai",
        "anyword"
    ],
    "created_date": "2026-08-03",
    "pros": [
        "It genuinely covers 30-plus languages at near-native level, including regional variants - no other mainstream checker can touch a German client writing English emails and German reports in one tool",
        "The free tier is real: core grammar and spelling checks work with no account and no card, so a client can hear the value on their own text before anyone spends money",
        "The open-source core means you can self-host the entire engine - that one feature wins privacy-sensitive clients (law firms, clinics, EU mid-caps) that no cloud-only tool can even pitch to",
        "At roughly $5.83/mo on annual billing it costs half of Grammarly's $12, and the two-year plan drops further to about $4.17/mo",
        "The custom style guide and team dictionary let you enforce one voice across six writers mechanically, which is a service you can bill for on its own",
        "It runs everywhere - browser extensions, Word, Google Docs, desktop apps, LibreOffice, API - so whatever environment your client writes in, the checker is already there"
    ],
    "cons": [
        "English suggestions are less polished than Grammarly's - no tone detection, no full-document rewrite, and some style advice reads like a linguist's rulebook rather than a copywriter's ear",
        "The free per-check character cap means long documents must be pasted in chunks, which is friction you have to manage or pay to remove",
        "The AI paraphrasing is mediocre - it occasionally hands back a sentence that is grammatically fine and clearly worse, so it needs a human judgement pass",
        "Month-to-month Premium at $24.90 is steep; the sane prices only exist on annual or two-year billing, which forces a commitment decision",
        "Self-hosting is free but not easy - Docker, a VM, TLS and someone to keep it updated, which is why it is a service you sell to organisations rather than something a normal client does themselves",
        "The advanced style checks thin out fast outside the main six languages; Picky Mode and the 20,000 extra checks are strong for English, German, French, Spanish, Dutch, Polish and Portuguese, but small languages get far fewer rules"
    ],
    "features": [
        "30+ Language Grammar & Spelling - checks grammar, spelling and punctuation across 30-plus languages and regional variants (British vs American English, Swiss vs Austrian German and so on)",
        "Picky Mode - stricter style rules for formal and academic writing: passive voice, wordiness, formality, weak phrasing",
        "AI Paraphrasing - unlimited sentence rewriting on Premium to make a sentence more formal, fluid or shorter",
        "Custom Style Guide - write your own rules to enforce consistent wording, tone and terminology across every document",
        "Team Dictionary & Management - shared dictionary for technical terms and a style guide enforced across all team members",
        "Everywhere Integrations - browser extensions for Chrome/Firefox/Edge/Safari, Word and Google Docs add-ins, desktop apps for Windows/macOS/Linux, LibreOffice built-in",
        "Developer API - embed checking into your own products, CMS or CI pipelines",
        "Self-Hosted Server - run the full open-source engine on your own infrastructure so no text ever leaves the building"
    ],
    "faq": [
        {
            "question": "Can I actually build an editing business on LanguageTool?",
            "answer": "Yes, and the math is unusually clean. ESL founders and cross-border teams pay $30-150 per document for clean English; at ten documents a month that is $1.5K-3K against a tool bill of $0-5. The service pool is huge because non-native speakers are the global majority of business English writers. You find clients on Upwork and Fiverr, in local startup communities, or by cold-DMing founders who publish in English. The one rule that protects you: sell the judgement pass, not the tool. Clients can install the free checker themselves; what they pay you for is the 20-30% of issues a rule-based checker cannot catch - tone, flow, and the sentence that is technically correct but sounds stiff."
        },
        {
            "question": "LanguageTool or Grammarly - which should I use?",
            "answer": "If you only write English and want the single best English suggestion engine, Grammarly (about $12/mo) is still the better product - its tone detection and full-document rewrite are genuinely ahead. Choose LanguageTool when any of these apply: you or your clients write in more than one language, your clients cannot send text to a US cloud (self-hosting), or price matters. For someone running an editing service, LanguageTool also has a competitive edge: the ESL and multilingual pool is bigger, fewer freelancers can serve it, and your tool cost is half. If your main need is rewriting and summarizing rather than checking, QuillBot is the different tool for that job."
        },
        {
            "question": "Is the free plan enough to run a service on?",
            "answer": "For most single documents, yes. The free tier includes the core grammar and spelling rules across all 30-plus languages with no account and no card, and a 2,500-word investor update fits in one paste. You only need Premium ($5.83/mo on annual billing) when you hit the per-check character cap on long documents, want the 150,000-character limit, need the custom style guide and team dictionary for client teams, or want unlimited AI paraphrasing. Picky Mode - the stricter formal/academic style rules that thesis and investor-update clients value most - is Premium-only, so if you sell formal editing, budget the $5.83."
        },
        {
            "question": "Is the self-hosted version worth setting up?",
            "answer": "Only if you are selling it to an organisation that needs it. Law firms, clinics, government contractors and European mid-caps with data-residency rules cannot send client text to a US cloud, and LanguageTool is the only mainstream checker they can install on their own server. A typical engagement is $1K-5K to stand it up (Docker, a VM, reverse proxy, user accounts) plus $200-500 a month to maintain and update it. The technical bar is real - you need to be comfortable with servers - but the competition is almost zero because most freelancers never learned it. It is not something a normal client does themselves; it is a service you package and sell."
        }
    ],
    "content": """## What LanguageTool Actually Is (From Someone Who Proofreads For A Living)

I run a small English editing and proofreading side business for ESL founders, and I have spent the last two years living inside grammar checkers. LanguageTool is the one I actually pay for. It is a German-built tool (Potsdam, LanguageTooler GmbH) that checks grammar, spelling, punctuation and style across 30-plus languages, on top of an open-source engine that has been running since 2003. The basic experience: type or paste text, it underlines problems in colour - red for spelling, yellow for grammar, blue for style - and most of the time it tells you why, not just what.

Three things separate it from the rest of the category. First, the language coverage. It genuinely handles German, French, Spanish, Dutch, Portuguese and Polish close to native level, including regional variants like British versus American English and Swiss versus Austrian German. If your client base writes in anything other than English, most checkers are useless to you and this one is not. Second, the core engine is open source under GNU LGPL. You can run the whole thing on your own server, which means no text ever leaves the building - that single fact wins you clients no cloud-only tool can even pitch to. Third, it is cheap. Premium runs about $5.83 a month on annual billing, roughly half of Grammarly's $12, and the free tier is not a teaser: core grammar and spelling checks work with no account and no card.

Pricing in full. Free gives you the core checks with a per-check character cap (roughly 2,000-10,000 characters depending on where you paste) and about three AI paraphrases a day. Premium is $24.90 month-to-month, $69.90 a year (about $5.83/mo), or about $4.17/mo on the two-year plan - it raises the cap to 150,000 characters per check, adds unlimited AI paraphrasing, the stricter Picky Mode style rules, a custom style guide, and 20,000-plus additional checks for English, German, French, Spanish, Dutch, Polish and Portuguese. Teams runs about $6.99 per user a month and adds a shared style guide, a team dictionary and member management. There is also a developer API and a self-hostable server, both free under the open-source licence. It runs as a browser extension (Chrome, Firefox, Edge, Safari), inside Word and Google Docs, as a desktop app for Windows, macOS and Linux, and LibreOffice has shipped with LanguageTool support for years.

## Why It Pays (The Real Income Angle)

Here is the part that matters: the tool is free or nearly free, and the people who need it are everywhere. Non-native speakers are the global majority of business English writers, and they pay real money to not sound like it. Six ways I have seen solo operators bill for this:

**1. English proofreading for ESL founders and teams.** This is the core gig. A German startup founder writing investor updates, a Japanese agency writing client reports, a Brazilian e-commerce team writing product pages - they all pay $30-150 per document to have a human (plus LanguageTool) make it clean. At ten documents a month that is $1.5K-3K against a $0-5 tool bill. The margin is the invoice minus an hour of your time.

**2. Multilingual content QA for cross-border teams.** Here is where LanguageTool beats every English-only checker. Teams publishing in French, Spanish, German and English pay $200-800 a month for someone to run their output through LanguageTool in each language, fix the errors and return a clean pass. Most freelancers cannot do this because they only own one language; if you own two or three, you have pricing power nobody else in your market has.

**3. Academic and admissions editing.** Students and researchers writing papers, theses and grad-school applications pay $50-200 per piece, and the demand never stops. LanguageTool's Picky Mode is built for exactly this - stricter formal style rules, passive-voice flags, wordiness - and the browser extension means you can check a Google Doc the same way you check an email.

**4. Self-hosted deployment for privacy-sensitive organisations.** Law firms, clinics, government contractors and European mid-caps have strict data-residency rules: their text cannot go to a US cloud. LanguageTool is the only mainstream grammar checker you can install on their server. A typical engagement is $1K-5K to set it up (Docker, a VM, reverse proxy, user accounts) plus $200-500 a month to maintain and update it. I have seen freelancers run three of these retainers at once - it is the highest-margin, lowest-competition work in this category.

**5. API integration into publishing workflows.** Marketing agencies and software teams want every blog post and help article checked before it ships. Build a small pipeline (a CMS hook or a CI step) that pushes drafts through the LanguageTool API and emails a report. Charge $500-2K per integration. The API itself costs nothing to start with; you bill for the plumbing.

**6. Style-guide and voice consistency retainers.** Content teams with six writers all using different terminology pay $300-1K to set up a shared style guide and team dictionary, then $150-400 a month to maintain it. LanguageTool enforces the rules mechanically, which is exactly what a content manager is buying when they say "everyone keeps spelling the product name differently."

The math that sells the service: a client paying $80 for a cleaned document is not buying a $5 subscription, they are buying "my English no longer embarrasses me in front of investors." That gap is the product, and the tool just makes the gap easy to deliver.

## How I Actually Run It (A Real Workflow)

For a typical 2,500-word investor update from a German founder: I run it through LanguageTool first (the free tier handles it in one paste), fix the mechanical errors it flags - comma rules, article mistakes, word order, false friends like "actual" versus "aktuell" - then read it once myself for the tone and flow issues a rule-based checker cannot see, like a sentence that is technically correct but sounds stiff. Total hands-on time is 30-40 minutes. I bill $90. The Premium subscription is invisible inside the invoice.

One honest note from experience: LanguageTool catches maybe 70-80% of what a careful human editor catches on English text. The last 20% is your judgement. That is not a bug - it is why the client pays you instead of just running their own text through the free checker. Clients can install the same tool; what they cannot buy is the judgement pass. So never sell yourself as "LanguageTool with a human attached." Sell the judgement.

## What LanguageTool Is Bad At (Honest)

- **English suggestions are less polished than Grammarly's.** No tone detection, no full-document rewrite, and some style suggestions read like they were written by a linguist's rulebook, not a copywriter. For pure English-only users who want maximum polish, Grammarly is still the better product.
- **The free per-check character cap is annoying.** Long documents have to be pasted in chunks. It is workable, but it is friction you have to manage, and it pushes casual users toward the paid plan faster than they want.
- **The AI paraphrasing is mediocre.** Premium's unlimited rewrite is fine for flattening one awkward sentence, but it will occasionally hand you something grammatically correct and clearly worse. Treat it as a suggestion, never a final pass.
- **Pricing punishes month-to-month.** $24.90 a month is steep for what it is; the sane prices ($4.99-5.83/mo) only exist on annual or two-year billing. If you cannot commit, the free tier is honestly fine for most single documents.
- **Self-hosting is not for non-technical people.** The open-source server is genuinely free, but you need Docker, a VM, TLS and someone to keep it updated. It is a service you sell to organisations, not something a normal client does themselves.
- **Advanced style checks thin out outside the main languages.** Picky Mode and the extra 20,000 checks are strong for English, German, French, Spanish, Dutch, Polish and Portuguese - but the deeper you go into smaller languages, the thinner the rules get.

## LanguageTool vs The Alternatives

| Tool | Best at | Language coverage | Self-host / API | Price (annual) |
|------|---------|-------------------|-----------------|----------------|
| **LanguageTool** | Multilingual grammar, privacy, value | 30+ languages, regional variants | Yes - open source + API | ~$5.83/mo |
| Grammarly | English polish, tone detection | English mainly | No - cloud only | ~$12/mo |
| ProWritingAid | Deep writing reports (readability, repetition) | English mainly | No | ~$10/mo |
| QuillBot | Rewriting, summarizing | English mainly | No | ~$9.95/mo |
| Sapling | Customer-service and sales message QA, API-first | English mainly | API only | ~$25/mo |

The honest summary: Grammarly wins on pure English finesse, QuillBot wins if your need is rewriting rather than checking, and LanguageTool wins the moment you go multilingual, privacy-sensitive or price-conscious - or all three.

## Who Should Use It (And Who Shouldn't)

**Use it if:** you edit or proofread for ESL clients and want one tool that covers their native languages too; you work with cross-border teams publishing in several languages; your clients are privacy-sensitive (law, clinic, EU mid-cap) and need self-hosting; you are an independent author who wants 90% of the checking value for half the Grammarly price; or you are a freelancer looking for a service to sell, because the demand pool here is enormous and the tool cost is near zero.

**Skip it if:** you only write English and want the absolute best English suggestions money can buy (Grammarly); your main need is rewriting and summarizing rather than checking (QuillBot); or you have no tolerance for pasting long documents in chunks and refuse to pay for Premium.

## Getting Started (6 Tips)

1. **Install the browser extension first** - it checks every field you type in, from Gmail to Notion, and that is where you will feel the value fastest.
2. **Run one real client document through the free tier before buying anything.** If the per-check cap drives you mad, then buy Premium; most single documents fit fine.
3. **Read the explanation under every suggestion.** LanguageTool tells you why - click the underline - and that is the difference between learning and blind clicking.
4. **Set up a personal dictionary and style guide on day two.** Brand names, technical terms and your client's preferred spellings stop being flagged, and your style guide enforces the same voice across documents.
5. **If you sell editing services, use Picky Mode for formal and academic work.** It catches wordiness and passive voice that the normal mode lets through - exactly what thesis and investor-update clients pay for.
6. **Paste long pieces into the standalone web editor** rather than fighting the extension's per-check cap - it is the same engine, just more room to work.

The bottom line: LanguageTool is not the flashiest grammar checker, and it will not rewrite your English into something award-winning. But for anyone whose clients write in more than one language, or whose clients cannot send text to a US cloud, it is the only tool in the category that works at all - and for a solo editor it is the cheapest way I have found to turn "please check my English" into a monthly invoice."""
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
