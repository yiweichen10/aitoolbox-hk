#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

tool = {
    "name": "Printful",
    "slug": "printful",
    "emoji": "👕",
    "color": "#101828",
    "description": "Print-on-demand fulfillment with the design tools built in: a free plan, in-house production, and an AI image generator (15 free images a day), AI mockups, and one-click background removal inside the same dashboard where your orders get printed and shipped.",
    "category": "AI Income",
    "tags": [
        {"text": "Print on Demand"},
        {"text": "AI Design Tools"},
        {"text": "Zero Inventory"},
        {"text": "E-commerce"}
    ],
    "rating": "⭐ 4.6",
    "badge": {"type": "new", "text": "NEW"},
    "url": "https://www.printful.com/",
    "price": "Free plan · Growth $24.99/mo",
    "pricing_details": "The Free plan costs $0/month forever: access to 607+ custom products, unlimited store connections plus 10 Quick Stores, the Design Maker and Mockup Generator, 20+ ecommerce integrations, and 24/7 support. You pay per order: the product base price (one print placement included), shipping (from roughly $4.30 in the US, higher internationally), and taxes. Extras are itemized: printed inside apparel labels $0.99, outside labels $2.49, embroidery digitization $2.95-$6.50 one-time per design, extra embroidery placements $2.95 each, premium catalog images $1 per image/placement/item sold. Printful Growth costs $24.99/month with a 14-day free trial and adds up to 33% off product base prices, 9% off branding, 25% off sample orders, free sample digitization, and exclusive large front prints - and the fee is waived automatically for the next 12 months once trailing 12-month sales pass $12,000 (it resumes if sales drop back below). Sample orders run 1 per month with up to 3 items at 20% off (Free) or 25% off (Growth). Payments go through a Printful Wallet via card, PayPal, or Apple Pay. Enterprise is custom-priced with dedicated support and managed services.",
    "platform": "Web dashboard + Shopify, Etsy, eBay, WooCommerce, TikTok Shop and 20+ integrations",
    "published": True,
    "pros": [
        "Free plan covers the whole path - design, mockups, store connection, fulfillment - with no listing fees or monthly bill until you choose Growth",
        "In-house production with a 3-step quality check, and Printful covers reprints or refunds on its own manufacturing errors",
        "The AI stack is real and free: 15 image generations a day, AI model mockups 10 times a day, background removal, and automatic upscaling",
        "You own the storefront and the customer data, unlike Redbubble or Amazon Merch - email lists and repeat buyers are yours",
        "Growth's product discounts (up to 33%) are the actual margin lever, and the $24.99 fee disappears at $12K/year in sales"
    ],
    "cons": [
        "Base prices run higher than Printify's provider marketplace - commonly a couple of dollars more per tee - which matters most at thin margins",
        "Shipping is billed separately on top of the base price and routinely surprises first-time sellers and their customers",
        "The built-in AI generator is a convenience, not a studio: 15 images/day throttles output and the engine sits below Midjourney or Ideogram quality",
        "No marketplace traffic: unlike Etsy or Redbubble, Printful delivers zero buyers - every customer comes from your own marketing",
        "The Growth fee waiver resets if trailing 12-month sales fall back under $12K, so the discount budgeting assumes you keep selling"
    ],
    "features": [
        "Free Design Maker with 3,500+ graphics, text tools, and reusable product templates across 607+ products",
        "AI Image Generator inside the designer - about 15 free text-to-image attempts per day for registered users",
        "AI mockups: your design placed on AI models or isolated product shots, 10 generations a day, free",
        "One-click Background Removal (free) and AI Smart Image Tool auto-upscaling so AI art prints sharp",
        "In-house fulfillment in US and EU facilities with branded labels, packing inserts, and 3-step quality checks"
    ],
    "faq": [
        {
            "question": "Can I sell AI-generated designs on Printful?",
            "answer": "Yes. There is no AI disclosure field in the upload flow and no ban on generative art - Printful's own blog actively shows AI workflows, including their built-in generator. The practical rules are theirs, not legal ones: clean up artifacts before listing (the Smart Image Tool upscales for print sharpness), check commercial-use terms on any outside generator you use, and skip copyrighted characters and celebrity likenesses. Their blog also warns that raw, unedited AI dumps read as generic slop and convert badly - edit for a niche, or the designs just fill space."
        },
        {
            "question": "What does one order actually cost me?",
            "answer": "On the Free plan, a US order for a Bella+Canvas 3001 tee that you retail at $24.99 works out to roughly $12-13 base price plus about $4.69 US shipping, leaving around $7 in margin before store platform fees and ad spend. Add an inside brand label for $0.99 if you want the unboxing to feel like yours. On Growth, product discounts of up to 33% push that same base price down - that is where the extra margin actually comes from, not from features."
        },
        {
            "question": "Printful or Printify - which should I start with?",
            "answer": "Both are free to start, so cost is not the deciding factor. Printful prints everything in its own facilities - consistent quality, branded labels, one throat to choke when something goes wrong, at somewhat higher base prices. Printify is a marketplace of 90+ print providers - cheaper base prices and provider choice, with quality that varies by provider and needs test orders. Sellers who care about brand consistency and custom labels tend to land on Printful; sellers chasing the lowest per-unit cost run Printify. You can connect both accounts to the same store and route products per item."
        }
    ],
    "content": """## What Printful Actually Is

Printful is a fulfillment company pretending to be a design tool, and that inversion is exactly why it earns a spot next to the other monetization pages here. Most POD platforms hand you a catalog and a list of third-party printers. Printful prints everything itself - its own facilities in the US and Europe, its own 3-step quality check, its own reprint-or-refund promise when it messes up an order. Since 2013 it has grown into one of the two default answers in print-on-demand, and the free plan carries the whole pipeline: 607+ products, a Design Maker with 3,500+ graphics, a Mockup Generator, and connections to 20+ platforms from Shopify and Etsy to TikTok Shop.

The part that matters for an AI-money site is what shipped inside the designer. There is a text-to-image generator built into the product editor - roughly 15 free generations a day - sitting two clicks away from the Background Removal Tool (free) and the AI Smart Image Tool that upscales your art so it prints sharp instead of pixelated. The Mockup Generator adds AI scenes: your flat design placed on AI-generated models or isolated product shots, 10 attempts a day, no studio, no booking, no Photoshop. Design, mockup, listing, fulfillment, shipping - one login.

## The Money Angle

Five ways people actually make money on this, ordered by how I would attack them:

1. **A niche merch store you own.** Connect a Shopify or Etsy store, pick one niche you understand (a sport, a city, a profession with inside jokes), generate designs - in Printful or in Ideogram or Midjourney, then import - clean, upscale, mockup, publish. You set retail prices and keep the customer data, which means email lists and repeat buyers. Redbubble gives you neither.

2. **The AI-assisted design pipeline.** Generate 10 candidates, keep 1, remove the background, upscale, mockup, list. Printful's own blog is refreshingly blunt about the failure mode: fully automated designs and listings read as generic AI slop and won't convert. The winners edit for one niche instead of dumping raw generations across dozens. AI is the speed tool, not the taste.

3. **Embroidery upsells.** Digitization costs $2.95-$6.50 one-time per design, and embroidered hats and beanies carry a premium feel buyers pay for. It's the cheapest perceived-value upgrade on the platform.

4. **Corporate and local orders.** Sports teams, clinics, breweries, school clubs - these buyers don't care about your SEO, they care about turnarounds and reorders. Printful's in-house consistency matters more here than base price.

5. **Quick Stores as a free test bench.** The Free plan includes 10 Quick Stores - instant storefronts for testing a niche without a Shopify subscription while you figure out whether anyone wants the designs.

## What It Really Costs

| Layer | Cost | Notes |
|---|---|---|
| Free plan | $0/mo | 607+ products, unlimited stores + 10 Quick Stores, all design tools, 24/7 support |
| Printful Growth | $24.99/mo (14-day trial) | Up to 33% off products, 9% off branding, 25% off samples; **fee waived at $12K/yr sales** |
| Product base price | ~$11-13 for a standard tee | One print placement included |
| Shipping | from ~$4.30 US | Billed separately; international runs higher |
| Inside label / outside label | $0.99 / $2.49 | Branding worth it once orders repeat |
| Embroidery digitization | $2.95-$6.50 one-time | Per design; extra placements $2.95 |
| Sample orders | 1/mo, up to 3 items | 20% off Free, 25% off Growth |

Worked example: a $24.99 tee on the Free plan costs roughly $12.50 base + $4.69 shipping = ~$17.19, leaving about $7.80 before platform and ad costs. The same order on Growth with a typical 25% product discount brings base price near $9.40 - margin climbs past $10. That discount, not the feature list, is what the $24.99 buys.

## The Honest Cons

- **Base prices lose to Printify's marketplace** on many common items - sometimes a couple of dollars per tee. At $7 margins, that is real money.
- **Shipping is the silent conversion killer.** A customer who happily paid $24.99 balks at $4.69 more at checkout. Bake shipping into retail pricing and say "free shipping."
- **The AI generator is convenience-grade.** Fifteen images a day is a testing throttle, not production volume, and the engine trails Midjourney and Ideogram. Serious sellers generate outside and import.
- **Zero traffic.** Printful is infrastructure. Etsy and Redbubble bring browsers; Printful brings boxes. Every customer is your marketing's fault.
- **The Growth waiver is trailing-window math.** Fall under $12K in trailing 12-month sales and the fee returns next billing period. Budget for it as permanent until you're consistently over.

## vs The Field

| | Printful | Printify | Redbubble |
|---|---|---|---|
| Model | In-house fulfillment | 90+ provider marketplace | Art community marketplace |
| Monthly fee | $0 / $24.99 Growth | $0 / $29 Premium (20% off) | $0 |
| Take on margins | Per-order costs only | Per-order costs only | Tiered revenue split, new accounts worst |
| Built-in AI design | Generator + AI mockups + upscale + bg removal | AI image generator | None |
| Traffic | Bring your own | Bring your own | Built-in marketplace traffic |
| Customer data | Yours | Yours | Platform keeps it |
| Quality control | Own factories, 3-step check | Varies by provider | Varies by partner |
| Best for | Branded stores, repeat buyers | Lowest per-unit cost | Zero-traffic beginners |

The pairing insight: Redbubble is where you learn what sells with someone else's traffic; Printful is where you go once a niche proves out and you want to own the margin and the customer. Printify splits the difference on price.

## Bottom Line

Printful is the POD vendor you graduate to when brand quality matters more than the last dollar of base cost - and since 2024's AI tool drops, "graduate" costs nothing: the Free plan includes the generator, the mockups, the upscaler, and the fulfillment. The honest math is unchanged from POD's early days: thin margins on a $25 tee mean niche selection and marketing do the heavy lifting, while the platform just executes. Start free, sample the print quality with your monthly sample order, and only consider Growth once monthly fulfillment spend crosses a few hundred dollars - by $12K/year the fee vanishes on its own."""
}

with open("_tmp_printful.json", "w", encoding="utf-8") as f:
    json.dump(tool, f, ensure_ascii=False, indent=2)
print("OK _tmp_printful.json", len(tool["content"]), "chars content")
