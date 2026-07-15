import json

PATH = r"C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data\tools_en.json"

with open(PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# Safety: do not double-add
if any(t.get("slug") == "looka" for t in data):
    print("Looka already present, aborting.")
    raise SystemExit(1)

content = """## What Looka Actually Is (From a Freelance Designer's Desk)

I run a small branding side business, and I have used Looka on and off since 2023 to deliver logo and brand-kit work for clients who cannot afford a $3,000 agency engagement. The pitch is dead simple: you type in a business name, pick a few colors and styles, and Looka spins up dozens of logo concepts in under a minute. Pick one you like, then expand it into a full brand kit - business cards, letterhead, social avatars, a brand guide.

Here is the part most reviews miss: Looka is not a design tool you "learn." It is a vending machine for brand assets. You are not crafting; you are selecting. That is exactly why it fits a freelancer who needs to turn around five client brands a week instead of one.

The honest framing: the logos it produces are competent and clean, rarely ugly, but also rarely surprising. If your client wants a safe, modern, legible mark, Looka delivers. If they want something an award jury would notice, it will not get you there.

---

## The Features That Actually Matter

### Fast Logo Generation

Type a name, choose industry and style chips, and you get 30-100 concepts immediately. The quality floor is high - even the throwaways are readable and on-brand-ish. I use this to show clients a range fast, which shortens the "I don't know what I want" phase that kills most logo projects.

### Full Brand Kit, Not Just a Mark

Once you pick a logo, Looka auto-builds matching business cards, letterhead, envelopes, email signatures, and social profile sets (Facebook, Instagram, LinkedIn, YouTube, Twitter). For a solopreneur, that is 90% of what they actually need. I have delivered a complete starter kit to a realtor in one sitting.

### Brand Guide Output

It generates a one-page brand guide: primary and secondary colors with hex codes, font pairings, logo clear-space rules, and do/don't examples. Clients love having this because it makes them feel like they have a "real" brand. For you, it is a ready-made deliverable page.

### Color and Font Explorer

You can reroll the palette and typography independently of the mark. This is genuinely useful when a client says "I like the shape but hate the blue." You swap the palette without regenerating the whole logo.

### Multi-Format Exports

PNG, SVG, PDF, EPS. The vector formats matter - any printer or sign shop needs EPS/SVG, and Looka includes them in the higher tiers. I have sent Looka SVGs straight to a laser cutter for a client's store sign.

---

## How to Actually Make Money With Looka

Looka charges per download, not a subscription. A logo file runs $20-$65, a brand kit $96, the full package $299. So your hard cost per client is roughly $100-$300. Here is how I turn that into real revenue.

### Path 1: Starter Brand Packages for Solopreneurs

Target: coaches, realtors, Etsy sellers, fitness trainers, consultants - people who need to look legitimate yesterday. You generate the logo + business card + social avatar set (asset cost ~$96), package it with a one-page brand guide you write, and sell it as a "Starter Brand Package" for $250-$450. Turnaround is 1-2 hours. Do 5-8 a month and you are at $1,500-$3,500/month. The client thinks they got a designer; you spent an afternoon.

### Path 2: Full Rebrand for Local Businesses

Target: restaurants, salons, gyms, clinics that have a tired or missing logo. You deliver logo + full brand kit + brand guide + 5 social templates + business card + letterhead (asset cost ~$299). Sell at $500-$900 per project. Three to four a month is $1,500-$3,600. This is the work I enjoy most because local owners are shocked that "a real brand" costs under a grand.

### Path 3: Logo Concept Service (Low Ticket, High Volume)

Some clients just want options to take to their own designer, or a quick mark for a side project. Generate 3-5 concepts, present them in a PDF, charge $50-$150. It costs you one $20 logo download. This is a great loss-leader: half of these buyers come back for the full package once they see the quality.

### The Unit Economics

Blended across those three paths at roughly 8 clients a month: asset cost $100-$300 each, revenue $300-$900 each, margin $200-$600 per client. Realistic monthly take: $2,500-$5,000. Your only real expense is the downloads, so margin stays above 70% even on the cheap packages. The constraint is lead flow, not delivery - same good problem as every service business.

---

## What Looka Is Bad At (The Honest List)

**1. The logos read as templated.** Experienced eyes spot the "Looka look" - same geometric sans, same circle-and-wordmark combos. For a $400 client this is fine. For a brand that needs to stand out in a crowded market, it is a liability. I have lost two pitches because the client's cousin "noticed it looked like three other logos."

**2. Editing is shallow.** You can change colors, fonts, and layout presets, but you cannot redraw the mark. If you want the icon's stroke thicker or the mascot facing the other way, you are out of luck - you regenerate and hope. For custom illustration work, Looka is the wrong tool.

**3. The "free" label is misleading.** You can design all day for free, but you pay to download anything. The logo is cheap, yet every extra format and kit tier adds cost, and the full package at $299 surprises people who expected a free file. Set client expectations up front or they resent the line item.

**4. Originality and rights are muddy.** You own the logo you buy, but the engine draws from shared template parts, so another business in another city can end up with a near-twin. It is rare and legally you are fine, but a client who finds a doppelganger will blame you. I always run a reverse image search before delivering.

**5. It is not brand strategy.** Looka gives you a pretty mark and a color sheet. It will not tell a client who they are, what they stand for, or how to talk to customers. That gap is your value-add - the businesses that thrive after a Looka brand are the ones where you also wrote the positioning line and the one-liner. Skip that and the logo alone collects dust.

---

## Looka vs the Alternatives

| Tool | Best For | Weakness | Price |
|------|----------|----------|-------|
| Looka | Fast full brand kits, resell to clients | Templated look, shallow editing | $20-$299 one-time |
| Canva Logo | Already-in-Canva users | Weak logo engine, manual kit assembly | Free-$12.99/mo |
| Hatchful (Shopify) | Ecommerce starters | Very basic, Shopify-centric | Free |
| Logo.com | Quick logo + basic site | Pushy upsells, weaker kit | $10-$250 |
| Fiverr designer | Truly custom, unique marks | $50-$500, 3-10 day wait, quality varies | $50-$500 |
| Adobe Express | Within Adobe workflow | Not a real brand system | Free-$9.99/mo |

The summary: if you need a unique, custom mark, hire a human or learn Illustrator. If you need a clean, complete, client-ready brand fast and cheap, Looka wins - especially when you are the one reselling the output.

---

## Getting Started Without Wasting Time

1. **Design your own brand first.** Run Looka on a fictional or personal project to learn its style chips and palette behavior before you touch a paying client's name. You will waste fewer downloads.

2. **Generate 80+ concepts, not 8.** The first screen is rarely the best. I scroll deep - the gems usually sit past the obvious suggestions. More options means a faster client yes.

3. **Always buy the vector tier for client work.** PNG alone is a trap; printers and sign shops need SVG/EPS. The $96-$299 tiers pay for themselves the first time a client asks for a banner.

4. **Wrap the output in a brand guide you write.** Looka's auto-guide is thin. Add a positioning sentence and a voice note and the package feels custom. That is the difference between $250 and $450.

5. **Reverse-image-search before delivery.** Thirty seconds prevents the awkward "this looks like my competitor's logo" call. Non-negotiable on paid work.

6. **Price the download into your quote.** Tell the client the brand kit is "included" and bake the $96-$299 into your project fee. Do not itemize it as a separate Looka charge - keep your margin clean.

---

## The Bottom Line

Looka is the tool I reach for when a client needs a real brand on a small budget and a short clock. It will not win design awards, and it should not be the last word on a company's identity. But as a delivery engine for solopreneur and local-business branding - where speed and price beat originality - it is hard to beat, and the resale margin is genuinely good.

The money angle is real and I live it: asset cost stays under $300 a client, packages sell for $250-$900, and a steady 8 clients a month clears $2,500-$5,000 with no subscription and no employees. The work is selection and packaging, not drafting. If you can sell and you have an eye for "good enough to ship," Looka is a quiet earner.
"""

looka = {
    "name": "Looka",
    "slug": "looka",
    "emoji": "\U0001F3A8",
    "color": "#0AA8D4",
    "description": "AI logo and brand-kit builder that turns a business name and a few style picks into dozens of logo concepts plus a full brand package - business cards, social sets, and a brand guide. A fast, cheap way for freelancers to deliver client-ready branding and keep most of the fee.",
    "category": "AI Design",
    "tags": [
        {"text": "Logo Maker"},
        {"text": "Branding"},
        {"text": "AI Design"},
        {"text": "Small Business"},
    ],
    "rating": "\u2b50 4.5",
    "visits": "2.1M",
    "badge": {"type": "tool", "text": "LOGO AI"},
    "url": "https://looka.com",
    "price": "Pay per download: Logo $20-$65, Brand Kit $96, Full package $299. No monthly fee.",
    "platform": "Web",
    "published": True,
    "pros": [
        "Generates 30-100 logo concepts in under a minute - shortens client 'I don't know what I want' stalls",
        "Auto-builds a full brand kit (cards, letterhead, social sets) from one chosen mark",
        "Vector exports (SVG, EPS, PDF) are printer- and sign-shop ready",
        "One-page brand guide gives clients a 'real brand' feeling with zero strategy work from you",
        "No subscription - you pay per download, so idle weeks cost nothing",
    ],
    "cons": [
        "Logos read as templated; experienced eyes spot the shared 'Looka look' across clients",
        "Editing is shallow - you can recolor and refont but cannot redraw or reshape the mark",
        "'Free' is misleading: you design for free but pay to download every asset",
        "Shared template parts mean another business can end up with a near-twin logo",
        "It is a mark generator, not brand strategy - positioning and messaging are still on you",
    ],
    "features": [
        "AI logo generation from business name, industry, and style picks",
        "Full brand kit: business cards, letterhead, envelopes, email signatures",
        "Social profile sets for Facebook, Instagram, LinkedIn, YouTube, Twitter",
        "Auto brand guide with hex codes, font pairings, and clear-space rules",
        "Independent color and font explorer - reroll palette without regenerating the logo",
        "Vector exports: PNG, SVG, PDF, EPS",
        "High-resolution and premium icon add-ons",
        "Web-based, no install",
    ],
    "faq": [
        {
            "question": "Can I really build a business reselling Looka logos?",
            "answer": "Yes - but be honest about what you are selling. You are not a custom logo designer; you are a brand-package assembler. Buy the logo + kit (cost $100-$300), wrap it in a guide you write, sell for $250-$900. Margin stays above 70%. The clients who pay are solopreneurs and local businesses that cannot justify a $3K agency. The risk is originality - run a reverse image search before delivery, and don't promise '100% unique.' At 8 clients a month you clear $2,500-$5,000. The hard part is lead generation, not the design.",
        },
        {
            "question": "Is Looka really free, or do I have to pay?",
            "answer": "You can design for free, but every download costs money. A single logo file is $20-$65, a brand kit $96, the full package $299. There is no monthly subscription. For client work, bake the download cost into your project fee and don't itemize it - clients resent seeing a 'Looka $96' line. Budget roughly $100-$300 of hard cost per client brand.",
        },
        {
            "question": "How is Looka different from hiring a Fiverr designer or using Canva?",
            "answer": "Speed and completeness. Looka delivers a logo plus a full brand kit (cards, letterhead, social sets, guide) in an hour; Fiverr takes 3-10 days and often delivers just a mark for similar money; Canva's logo engine is weak and you assemble the kit by hand. The tradeoff is originality - Fiverr can produce a custom mark, Looka cannot redraw the icon. For 'clean and fast,' Looka wins; for 'one of a kind,' hire a human.",
        },
        {
            "question": "Can two businesses end up with the same logo?",
            "answer": "It is possible, because Looka builds from shared template parts, and you only own the specific logo you purchase - not the underlying style. A near-twin in another city is rare but real, and a client who spots one will blame you. Mitigate by reverse-image-searching before delivery and by customizing the palette and layout so the result diverges from the template default. Legally you are in the clear; reputationally, do the search.",
        },
    ],
    "content": content,
    "aeo_geo_updated": True,
}

data.append(looka)

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Looka added. New total: {len(data)} tools")
