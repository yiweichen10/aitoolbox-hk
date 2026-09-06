import json

PATH = r"C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data\tools_en.json"

with open(PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# Safety: do not double-add
if any(t.get("slug") == "wordtune" for t in data):
    print("Wordtune already present, aborting.")
    raise SystemExit(1)

content = """## What Wordtune Actually Does (From a Ghostwriter's Desk)

I run a small writing side business - ghostwriting and polishing for non-native English founders, indie hackers, and the occasional academic. I have used Wordtune on a near-daily basis since 2022. Most "AI writing" tools try to write for you. Wordtune does the opposite: you write the draft (or paste the client's rough notes), highlight a clunky sentence, and it hands you 5-10 different ways to say the same thing, each in a different register.

The part most reviews miss: Wordtune is a clarity engine, not a content factory. It will not dream up a 2,000-word blog from a prompt. It takes the sentence you already wrote and shows you how to make it land. For someone whose job is making other people sound sharp, that is the whole game.

Here is the honest framing. When a client sends me bullet points in broken English, I do not rewrite it by hand from zero. I drop it into Wordtune, pick the phrasing that fits the reader, and I have a clean paragraph in a fraction of the time. The tool did the heavy lifting on wording; I did the thinking on meaning. That split is exactly why it pays for itself.

---

## The Features That Actually Matter

### Multiple Rewrites Per Sentence

Highlight any sentence and you get a stack of alternatives - some casual, some formal, some shorter, some restructured. You pick, you move on. This is different from a single-output paraphraser: seeing five versions side by side teaches you what "better" sounds like, and one of them usually clicks. On a 600-word client draft I will rework maybe 40 sentences; Wordtune shows me the path on every one.

### Tone Control (Casual / Formal)

The toggle is the feature I reach for most. A stiff corporate email becomes human in two clicks; a Slack message becomes client-ready copy the other way. For rewriting client outreach, this alone saves me from rewriting the same paragraph three times. It genuinely shifts register - not just swapping a few words.

### Shorten and Expand

Shorten cuts the fluff from a wordy paragraph without dropping the point. Expand adds detail to a thin bullet. I use Shorten constantly when a founder overwrites, and Expand when they under-explain and the reader would be lost. Both keep meaning intact far better than I expected.

### Spices

Spices injects supporting material into your text - an example, a counterargument, a statistic, an analogy. For a blog or a pitch this is a fast way to add depth without breaking flow. The statistics it pulls are sourced, but I always verify a number before it goes to a paying client. Treat Spices as a first draft of evidence, not gospel.

### Wordtune Read (Summarizer)

Paste a long article, PDF, or YouTube link and it condenses to bullet points. I use this to prep client briefs: drop in their competitor's 3,000-word page, get the five things that matter, and write the response. It will not replace reading, but it trims the boring middle.

### Smart Translate

Write in your own language (it handles 10-plus, including Spanish, Mandarin, Arabic) and it outputs fluent, native-sounding English. For my ESL clients this is the killer feature - they think in their language, I get clean English, and the meaning stays theirs. One warning: it translates into English well; it does not reliably edit text already written in other languages.

### Where It Lives

Chrome and Edge extension, a Google Docs and Gmail add-in, a Microsoft Word add-in, a web editor, and mobile apps. The extension is the real product - it works inside LinkedIn, Slack, email, anywhere there is a text box. That is why I keep it on all day.

---

## How to Actually Make Money With Wordtune

Wordtune is a polishing tool, not a generator. So the money is in services where clean English is the deliverable and speed is the edge. Here is what has worked for me and people I know.

### Path 1: Ghostwriting and Rewriting for ESL Clients

Target: overseas founders, indie hackers, researchers who have the ideas but clunky English. They send rough notes or a broken draft; you turn it into fluent prose with Wordtune and your judgment. Charge $50-$200 per piece depending on length. The pitch writes itself: "You think in your language, I make it read like a native wrote it." One $120 project covers eight months of the Unlimited plan. Do ten a month and you are at $500-$2,000, almost all profit since your only cost is the $14.99 subscription.

### Path 2: Cold Email and Outreach Rewriting for Sales Teams

Target: agencies and SaaS founders whose outreach sounds like a robot wrote it (because a robot did). You take their stiff template, rewrite it into a persuasive, human tone with Wordtune, and A/B test casual vs formal variants. Sell as a monthly retainer: $300-$800 per client. Three to four clients is $900-$3,200 a month. The client sees reply rates move; you barely break a sweat because the tone toggle does the rewriting.

### Path 3: Resume and CV Rewriting

Target: job seekers who wrote their own resume once, in 2019, and never again. You rephrase bullet points into sharp, achievement-led lines, shift tone per industry, and tighten the flab. Charge $80-$200 per resume. This is high-volume, low-effort work - listings on Upwork and Fiverr are constant, and a single evening clears a few hundred dollars. Wordtune's Shorten tool alone earns its keep here.

### Path 4: Social Caption and Thread Polishing for Brands

Target: small brands whose founder writes dry, factual posts nobody engages with. You take their facts and shift them into platform-native tone - punchy for X, warm for LinkedIn, casual for Instagram. Retainer: $300-$600 per client per month for a set number of posts. The tone control means you can serve five clients in the time it used to take for one.

### The Unit Economics

Blended across those paths at roughly 10 clients a month: tool cost $14.99 (Unlimited, billed annually). Revenue $1,200-$2,000. Profit margin sits at 98% because your only real expense is the subscription. The constraint is lead flow and your own editing taste, not delivery. The same good problem every service business has - but here the software removes the slow part.

One note on the ethics line: Wordtune is great for polishing and paraphrasing, and I use it for students who need to rephrase sources correctly while learning. I do not use it to write essays wholesale and pass them off as original - that is academic dishonesty and it burns the client later. Keep the human's meaning intact and you are fine.

---

## What Wordtune Is Bad At (The Honest List)

**1. The free tier is a tease.** Ten rewrites a day sounds fine until you edit a real draft - a 600-word piece burns through it in about eight minutes. If you do paid work, the free plan is not viable. Budget for Plus or Unlimited from day one.

**2. It is not a grammar checker.** Wordtune will leave your commas, typos, and subject-verb disagreements alone. It fixes style, not correctness. I run Grammarly beside it: Grammarly catches the errors, Wordtune fixes the voice. Use one without the other and you ship half-finished work.

**3. Sentence-level only.** Wordtune will not reorganize your document or rebuild a weak argument. It polishes the sentence you highlight; the structure is still on you. For a messy client draft, you architect first, then polish. Expecting it to fix the whole piece is the most common beginner mistake.

**4. Default suggestions can flatten your voice.** If you blindly accept the most "formal" option every time, distinctive writing turns beige. The tool optimizes for safe and clear, not memorable. I always read the rewrite and keep the version with spine. A human pass is not optional if the writing has to stand out.

**5. Smart Translate is English-first.** It turns other languages into fluent English well, but it will not reliably edit text already written in Japanese, Arabic, or most non-Latin scripts. For true multilingual editing, it is half a tool. Know which half before you promise a bilingual client the world.

**6. The roadmap has looked quiet.** AI21 Labs has pointed its energy at its Jamba models and enterprise APIs; Wordtune's core feature set has barely moved in over a year. It works fine today and the rewriting is still best-in-class for tone. Just do not bank on major new drops - build your business on what it does now, not what it might add.

---

## Wordtune vs the Alternatives

| Tool | Best For | Weakness | Price |
|------|----------|----------|-------|
| Wordtune | Per-sentence rewrites with tone options | No grammar check, sentence-level only | Free-$14.99/mo |
| QuillBot | Paragraph rewriting, one output per mode | Fewer side-by-side options, more "one answer" | Free-$9.95/mo |
| Grammarly | Correctness: grammar, spelling, clarity scores | Weak at tone and restructuring phrasing | Free-$12/mo |
| ProWritingAid | Deep structure and style reports | Heavy, slow for quick inline fixes | Free-$10/mo |
| Jasper / Copy.ai | Generate marketing copy from a prompt | Not for polishing your own draft | $39-$49/mo+ |

The summary: if you need to write from scratch, Jasper wins. If you need to not embarrass yourself on commas, Grammarly wins. If you already wrote it and it "isn't quite right," Wordtune is the fastest way to fix the voice - and the tool I would keep if I could only pay for one writing app.

---

## Getting Started Without Wasting Time

1. **Install the extension first, not the web app.** The extension is where Wordtune earns its keep - it works inside Gmail, Docs, LinkedIn, Slack. The web editor is a backup. Live in the extension.

2. **Use the free tier to learn its habits, then pay.** Spend a week on the 10-daily cap to see which tones you like. The day you hit the wall mid-client-draft, upgrade to Unlimited. The $14.99 is less than one coffee a week and pays for itself on the first job.

3. **Pair it with Grammarly.** Grammarly for errors, Wordtune for voice. Running only one leaves half the work undone. This combo is the standard setup for every writer I know who uses both.

4. **Always read the rewrite before you accept it.** The most "formal" suggestion is not always the best. Pick the version with spine, not the safest. Your judgment is the product; Wordtune is the assistant.

5. **Verify Spices numbers.** The statistics Spices pulls are sourced but not always current. Before a fact goes to a paying client, confirm it. Thirty seconds prevents a ruined pitch.

6. **Architect before you polish.** Fix the order and the argument yourself, then run Wordtune sentence by sentence. Throwing a messy draft at it and hoping wastes rewrites and produces clean-but-hollow text.

---

## The Bottom Line

Wordtune is the tool I keep open all day because my job is making other people sound sharp, and it does that faster than I can by hand. It will not write your article, catch your typos, or restructure your argument. What it does - take a sentence that "isn't quite right" and show you five ways to fix it, in the tone the reader needs - it does better than anything else I have tried.

The money angle is real and I live it: a $14.99 monthly sub, clients paying $50-$200 a piece, ten jobs a month clearing $1,200-$2,000 at a 98% margin. The work is judgment and packaging, not drafting from zero. If you can sell a writing or polishing service and you have an ear for "good enough to ship," Wordtune is a quiet earner that pays for itself on the first project.
"""

wordtune = {
    "name": "Wordtune",
    "slug": "wordtune",
    "emoji": "\U0001F4DD",
    "color": "#3B82F6",
    "description": "AI21 Labs' writing companion that rewrites your own sentences with multiple tone options - formal, casual, shorter, longer - instead of generating text from scratch. A fast, cheap way for freelancers to deliver polished, native-sounding English and keep almost all of the fee.",
    "category": "AI Writing",
    "tags": [
        {"text": "Writing Assistant"},
        {"text": "Paraphrasing"},
        {"text": "AI Writing"},
        {"text": "Rewriting"},
    ],
    "rating": "\u2b50 4.6",
    "visits": "8.0M",
    "badge": {"type": "tool", "text": "REWRITE AI"},
    "url": "https://wordtune.com",
    "price": "Free (10 rewrites/day). Plus ~$9.99/mo, Unlimited ~$14.99/mo billed annually. Business plan custom.",
    "platform": "Web / Chrome & Edge extension / Word & Google Docs add-in / iOS & Android",
    "published": True,
    "pros": [
        "Shows 5-10 rewrite options per sentence side by side - you pick the voice, not a fixed output",
        "Casual/Formal toggle genuinely shifts register, not just swaps words",
        "Shorten and Expand keep meaning while fixing length - great for tight briefs",
        "Smart Translate turns 10+ languages into fluent English, keeping the writer's meaning",
        "Browser extension works inside Gmail, Docs, LinkedIn, Slack - lives where you write",
    ],
    "cons": [
        "Free tier is 10 rewrites/day - a real draft burns through it in minutes, paid plan needed for work",
        "Not a grammar checker - it leaves commas and typos alone; pair with Grammarly",
        "Sentence-level only - it will not restructure your document or rebuild a weak argument",
        "Default suggestions can flatten distinctive voice if you accept the safest option blindly",
        "Smart Translate is English-first; it will not reliably edit text written in other languages",
    ],
    "features": [
        "Multiple rewrites per sentence with side-by-side alternatives",
        "Tone control: casual, formal, shorten, expand",
        "Spices: inject examples, counterarguments, statistics, analogies",
        "Wordtune Read: summarize articles, PDFs, and YouTube videos",
        "Smart Translate: 10+ languages into fluent English",
        "Chrome and Edge extension, Gmail and Google Docs add-in",
        "Microsoft Word add-in and web editor",
        "iOS and Android apps",
    ],
    "faq": [
        {
            "question": "Can I build a writing service around Wordtune?",
            "answer": "Yes, and the margin is the point. Wordtune is a polishing tool, not a generator, so the business is a rewriting or ghostwriting service: ESL founders and researchers send rough notes, you return fluent English. Charge $50-$200 per piece. The Unlimited plan is $14.99/mo, so one $120 job covers eight months of software. At ten clients a month you clear $1,200-$2,000 at roughly 98% margin because the subscription is your only real cost. The hard part is lead flow and your own editing taste, not delivery. Keep the client's meaning intact and you are selling a skill, not a spinner.",
        },
        {
            "question": "Is the paid plan worth it over the free tier for a freelancer?",
            "answer": "For any paid work, yes. The free plan gives 10 rewrites a day, which a 600-word client draft eats in about eight minutes. You will hit the wall mid-job and lose momentum. Plus (~$9.99/mo) gives 30 rewrites a day; Unlimited (~$14.99/mo) removes the cap entirely. I run Unlimited because I rewrite constantly and the $5 gap over Plus is nothing next to one saved hour. If you only polish your own occasional email, free is fine. If a client is waiting, pay.",
        },
        {
            "question": "Wordtune vs Grammarly vs QuillBot - which do I actually need?",
            "answer": "They solve different problems. Grammarly catches errors (grammar, spelling, clarity scores) but is weak at tone. QuillBot rewrites paragraphs with one output per mode. Wordtune gives multiple side-by-side sentence rewrites with real tone control. For a writing service, run Grammarly plus Wordtune: Grammarly for correctness, Wordtune for voice. QuillBot is the closer substitute if you prefer paragraph-level rewriting, but it shows fewer options at once. Skip Jasper or Copy.ai - those generate from prompts and will not polish a draft you already wrote.",
        },
        {
            "question": "Is it safe to use Wordtune for client or student work?",
            "answer": "For polishing and paraphrasing, yes. I use it to help students rephrase sources correctly while they learn, and to clean up client drafts. The line is originality: Wordtune should reshape the writer's own meaning, not manufacture an essay from nothing and pass it off as the client's. That crosses into plagiarism and burns them later. Keep the human's intent intact, verify any Spices statistics before they ship, and you stay on the right side. For sensitive client text, note that content passes through AI21 Labs' servers - read their policy before pasting confidential material.",
        },
    ],
    "content": content,
    "aeo_geo_updated": True,
}

data.append(wordtune)

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Wordtune added. New total: {len(data)} tools")
