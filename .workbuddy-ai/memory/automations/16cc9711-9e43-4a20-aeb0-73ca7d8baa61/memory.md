# Automation memory — add new English tool to aitoolbox.hk

2026-10-03: Added new English tool **arcads** (Arcads, category AI Video) — AI UGC ad studio with 300-1,500 AI actors. Chosen for a strong monetization angle (sell UGC ad creative at ~$11/clip vs $80-200 human creators). Not previously in data/tools_en.json (was 212 tools).

Process (canonical, reuse next run):
1. Wrote tool JSON to temp `_tool_arcads.json` (all fields: name/slug/url/category/price/description/pricing_details/pros/cons/faq/badge/color/emoji/platform/rating/tags/features/content/published).
2. `price` = short card label "From $77/mo · ~$11 per video" (28 chars); full pricing in `pricing_details`.
3. Upserted via `python scripts/upsert_tool_en.py _tool_arcads.json` → 1 added, total 213.
4. `python scripts/check_price_labels.py` → PASS 213 tools, 0 polluted.
5. `python scripts/build_en.py` → exit 0; tool page at tools/arcads/index.html, sitemap 213 tools, IndexNow pushed 1 URL (HTTP 200), OG image generated.
6. Committed + pushed to aitoolbox-hk main: commit b7e97e902 (prev 5f9e0f7a3). Worktree clean.

Notes for next run: no root Chinese tools.json exists — pick from trending global tools. Build log labels paths as `en/tools/<slug>/index.html` but actual output is root-relative `tools/<slug>/index.html`. Pillow IS available now (OG images generated OK).

2026-10-04: Added new English tool **vapi** (Vapi, category AI Agents) — voice-agent orchestration platform ($0.05/min platform fee + pass-through STT/LLM/TTS/telephony; ~$0.10-0.30/min all-in). Chosen for monetization angle: sell AI receptionists to local businesses at $500-2,000/mo vs ~$75-125 usage for 500 min. Not previously in data/tools_en.json (was 213 tools). Category AI Agents is underrepresented (was 6 tools) — good source of future picks (Vapi/Retell/Bland/Synthflow family).

Process (same as prior run, all worked first try):
1. Wrote tool JSON to temp `_tool_vapi.json` (all fields incl. pricing_details).
2. `price` = "From $0.05/min · ~$0.15/min all-in" (34 chars); full cost stack in pricing_details.
3. `python scripts/upsert_tool_en.py _tool_vapi.json` → 1 added, total 214.
4. `python scripts/check_price_labels.py` → PASS 214, 0 polluted.
5. `python scripts/build_en.py` → exit 0; tools/vapi/index.html, category/ai-agents, sitemap 214 tools, OG image, IndexNow 1 URL (200).
6. `git add -A && commit` (604d47073, prev 4c76a76e8) + push origin main. Worktree clean.
7. Live check: apex aitoolbox.hk 308-redirects to www.aitoolbox.hk; the new page 404'd for ~1-2 min then went 200 (deploy propagation). Don't panic on an immediate 404 — recheck after a minute.

Tip: ~453 files change per build (all articles regenerated) — that is normal, `git add -A` is fine. `_tool_*.json` temp files ARE committed by convention (arcads was).

2026-10-06: Added new English tool **apify** (Apify, category AI Automation) — web-scraping/automation platform with an Actor Store; monetization angle = publish Actors on pay-per-event (PPE) pricing and keep ~80%, or sell scraped data/lead-gen as a service. Not previously in data/tools_en.json (was 214 tools). Category AI Automation was underrepresented (7 tools). Pricing verified from apify.com/pricing + use-apify docs: Free $0 ($5 credit), Starter $19/mo, Scale $199/mo, Business $999/mo (plan fee returns as prepaid usage; CU $0.20/$0.16/$0.13); Creator plan $500 free usage/6mo; payout min bank $100 / PayPal $20; rental model retiring Oct 1 2026.

Process (all worked first try):
1. Wrote tool JSON to temp `_tool_apify.json` (all fields incl. pricing_details).
2. `price` = "Free + Starter $19/mo · Scale $199/mo" (37 chars); full cost stack + PPE/80% split + payout in pricing_details.
3. `python scripts/upsert_tool_en.py _tool_apify.json` → 1 added, total 215.
4. `python scripts/check_price_labels.py` → PASS 215, 0 polluted.
5. `python scripts/build_en.py` → exit 0; tools/apify/index.html, category/ai-automation, sitemap 215 tools, OG image apify-en-og.png, IndexNow 1 URL (200).
6. `git add -A && commit` (b628ed705, prev b6a20e796) + push origin main (aitoolbox-hk). 456 files changed (normal). Worktree clean.
7. Live: www.aitoolbox.hk/tools/apify/ 404 immediately, 200 after ~90s. Title renders correctly.

Notes for next run: candidate pool still rich in under-served categories — Clay (AI Marketing, GTM enrichment), Instantly.ai/Smartlead (AI cold email), Retell AI/Bland (voice agents, but Vapi already covers), GoHighLevel (agency white-label). The "best-ai-*-2026" comparison articles already reference some of these (e.g. clay, instantly, apify) — adding the matching tool page is a natural fit.

2026-10-06 (2nd run today): Added new English tool **clay** (Clay, category AI Marketing) — GTM data workbench with provider-waterfall enrichment + Claygent AI columns. Monetization angle = sell the output (lead-gen as a service $500-3,000/list; outbound done-for-you retainers; bolt-on data product for existing SEO/ads clients), NOT reselling the tool (no big affiliate program). Not previously in data/tools_en.json (was 215). Category AI Marketing was thin (5 tools). Pricing verified from clay.com/pricing + nynch.com (Aug 2026): Free $0 (100 credits/500 actions, 200-row cap); Launch $167/mo annual / $185 monthly (2,500 credits, 15K actions); Growth $446/mo annual / $495 monthly (6,000 credits, 40K actions); Enterprise custom. Workspace pricing, unlimited seats/tables; top-ups +30%; rollover capped 1 month; annual saves ~10%. Name collision noted: old personal CRM "Clay" is now Mesh.

Process (all worked first try):
1. Wrote tool JSON to temp `_tool_clay.json` (all fields incl. pricing_details).
2. `price` = "Free + Launch $167/mo · Growth $446/mo" (38 chars); full cost stack in pricing_details.
3. `python scripts/upsert_tool_en.py _tool_clay.json` → 1 added, total 216.
4. `python scripts/check_price_labels.py` → PASS 216, 0 polluted (33 in 50-80 gray zone).
5. `python scripts/build_en.py` → exit 0; tools/clay/index.html, sitemap 216 tools + 181 articles, OG image images/og/clay-en-og.png, IndexNow 1 URL (200).
6. `git add -A && commit` (aefc70f95, prev 4763cf7a1) + push origin main (aitoolbox-hk). 455 files changed (normal). Worktree clean.
7. Live: www.aitoolbox.hk/tools/clay/ 404 immediately, 200 within ~20s this time. Title renders, price label renders correctly.

Bonus: an existing article `best-ai-lead-enrichment-tools-2026-apollo-vs-lusha-vs-zoominfo-vs-clay` already references Clay, so the new tool page has a natural internal-link target.

Notes for next run: still-untapped under-served categories — AI Marketing is now 6 tools; candidates: Instantly.ai / Smartlead (AI cold email, strong agency monetization), GoHighLevel (agency white-label SaaS reseller), Retell AI / Bland (voice agents, Vapi covers the niche), Lemlist, Apollo. Also AI Agents (7) and AI Automation (8) remain thin.

2026-10-07: Added new English tool **instantly-ai** (Instantly, category AI Marketing) — cold email platform: Outreach sending engine (unlimited accounts + warmup, sequences) + 450M+ B2B lead database/Credits + AI email writer & researcher agent. Chosen as the send-side complement to Clay (list-side), strong agency monetization: run cold email/appointment-setting as a service ($1,500-$5,000/mo retainer vs $47-$194/mo tool cost) + 30% recurring affiliate (PartnerStack). Not previously in data/tools_en.json (was 216). Pricing verified from instantly.ai/pricing + /affiliate: Outreach Growth $47/mo (annual $37.60), Hypergrowth $97/mo, Light Speed $358/mo; Credits (lead DB+AI) from $47/mo; bundles Starter $94 / Scale $194 / Agency $555 (annual saves ~10%); no free plan, trial only.

Process (all worked first try):
1. Wrote tool JSON to temp `_tool_instantly.json` (all fields incl. pricing_details).
2. `price` = "From $47/mo · Starter bundle $94/mo" (35 chars); full cost stack in pricing_details.
3. `python scripts/upsert_tool_en.py _tool_instantly.json` → 1 added, total 217.
4. `python scripts/check_price_labels.py` → PASS 217, 0 polluted (33 in 50-80 gray zone).
5. `python scripts/build_en.py` → exit 0; tools/instantly-ai/index.html, sitemap 217 tools + 182 articles, OG image images/og/instantly-ai-en-og.png, IndexNow 1 URL (200).
6. `git add -A && commit` (f3926fbc0, prev 2e6ae7e7c) + push origin main (aitoolbox-hk). 461 files changed (normal). Worktree clean.
7. Live: www.aitoolbox.hk/tools/instantly-ai/ → HTTP 200 within ~25s this time; title + price label render correctly.

Notes for next run: AI Marketing now 7 tools (clay + instantly form a natural internal-link pair). Remaining thin categories: AI Agents (7), AI Automation (8), AI Search (7). Candidates: Smartlead (alt cold email), GoHighLevel (agency white-label reseller), Apollo (lead DB), Lemlist, Retell AI/Bland. The "best-ai-*-2026" articles may already reference some of these — check for a natural internal-link target when picking.

2026-10-09: Added new English tool **gohighlevel** (GoHighLevel, category AI Marketing) — all-in-one agency platform (CRM, funnels, calendars, email/SMS, reviews, AI agents) whose real story is the reseller model: on Agency Pro you white-label it, spin up a sub-account per client and resell seats at $200-500/mo, plus SaaS mode for recurring software revenue. Not previously in data/tools_en.json (was 217). Pricing verified from skillmammoth.com/blog/gohighlevel-pricing (Oct 2026) + grow-highlevel.com: Starter $97/mo (annual $970, 3 sub-accounts), Unlimited $297/mo ($2,970, unlimited sub-accounts, rebill at cost), Agency Pro $497/mo ($4,970, SaaS mode + rebill with markup), Enterprise custom; 14-day trial; usage wallet — numbers $1.15/mo, SMS $0.00747/segment + carrier fees, outbound calls $0.0166/min, inbound $0.01165/min, email $0.675/1k, AI Employee $50/$97 per sub-account. A real single-business bill lands ~$135-150/mo on Starter.

Process (all worked first try):
1. Wrote tool JSON to temp `_tool_gohighlevel.json` (all fields incl. pricing_details).
2. `price` = "From $97/mo · Agency Pro $497/mo" (34 chars); full cost stack + usage rates in pricing_details.
3. `python scripts/upsert_tool_en.py _tool_gohighlevel.json` → 1 added, total 218.
4. `python scripts/check_price_labels.py` → PASS 218, 0 polluted (33 in 50-80 gray zone).
5. `python scripts/build_en.py` → exit 0; tools/gohighlevel/index.html, category/ai-marketing, sitemap 218 tools + 185 articles, OG image images/og/gohighlevel-en-og.png, IndexNow 1 URL (200).
6. `git add -A && commit` (27667662f, prev efc33d8e3) + push origin main (aitoolbox-hk). 466 files changed (normal). Worktree clean.
7. Live: www.aitoolbox.hk/tools/gohighlevel/ 404 immediately, 200 after ~75s. Title + price label render correctly.

Notes for next run: AI Marketing now 8 tools. Still-thin categories: AI Agents (7), AI Automation (8), AI Search (7). Candidates: Smartlead (alt cold email), Apollo (lead DB), Lemlist, Retell AI/Bland (Vapi covers voice), GoHighLevel alternatives. The `best-ai-crm-tools-2026` and `best-ai-email-marketing-tools-2026` articles are natural internal-link targets for GoHighLevel. Reminder: ~460+ files change per build (all articles regenerated) — `git add -A` is fine; `_tool_*.json` temp files are committed by convention.

2026-10-10: Added new English tool **apollo** (Apollo.io, category AI Marketing) — B2B contact database (200M+ contacts) with outbound kit bolted on (reveals, sequences, dialer, Chrome extension, CRM sync). Not previously in data/tools_en.json (was 218). Chosen because it is referenced 41x across articles_en.json but had NO tool page → strong internal-link target (esp. `best-ai-lead-enrichment-tools-2026-apollo-vs-lusha-vs-zoominfo-vs-clay` and `best-ai-cold-email-tools-2026-instantly-vs-smartlead-vs-lemlist-vs-woodpecker`). Monetization angle (honest): run outbound/appointment-setting as a service (retainers $1,500-5,000/mo) + 15-20% recurring affiliate — NOT reselling the DB (Apollo ToS bars external/product use of its data without an Enterprise agreement). Pricing verified from allaboutinsights.com + ditlead.com (2026): Free $0 (900 credits/yr, Gmail-only sending), Basic $49/user/mo annual (30k credits/yr), Professional $79 (48k credits, dialer/A-B/AI), Organization $119 (min 3 seats, 72k credits, SSO), Enterprise custom (only tier with API/external use). Credits: verified email ~1, mobile ~8, enrichment/AI vary, export credits burn on CSV/CRM/API push; no rollover; Fair-Use cap 10k/mo non-paying or lesser of ($paid/$0.025) or 1M/yr paying. Annual saves ~24%.

Process (all worked first try):
1. Wrote tool JSON to temp `_tool_apollo.json` (all fields incl. pricing_details).
2. `price` = "Free + Basic $49/mo · Pro $79/mo" (32 chars); full cost stack in pricing_details.
3. `python scripts/upsert_tool_en.py _tool_apollo.json` → 1 added, total 219.
4. `python scripts/check_price_labels.py` → PASS 219, 0 polluted (33 in 50-80 gray zone).
5. `python scripts/build_en.py` → exit 0; tools/apollo/index.html, category/ai-marketing, sitemap 219 tools + 186 articles, OG image images/og/apollo-en-og.png, IndexNow 1 URL (200).
6. `git add -A && commit` (49deaca48, prev 86a000287) + push origin main (aitoolbox-hk). 465 files changed (normal). Worktree clean.
7. Live: www.aitoolbox.hk/tools/apollo/ 404 on attempt 1, 200 on attempt 2 (~20s). Title + price label render correctly.

Notes for next run: AI Marketing now 9 tools. Still-thin categories: AI Agents (7), AI Automation (8), AI Search (7). Strong untapped internal-link candidates (referenced in articles but no tool page): smartlead (30 refs), lemlist (22), retell (24), bland (21) — Smartlead/Lemlist are the cleanest fits for AI Marketing. Consider AI Search (7) or AI Agents (7) to diversify. Reminder: ~460+ files change per build; `_tool_*.json` temp files are committed by convention.

2026-10-11: Added new English tool **smartlead** (Smartlead, category AI Marketing) — agency-focused cold email platform (unlimited mailboxes on every plan, isolated per-client workspaces, built-in lead DB). Not previously in data/tools_en.json (was 219). Chosen because it is referenced 30x in articles_en.json but had no tool page → natural internal-link target, esp. `best-ai-cold-email-tools-2026-instantly-vs-smartlead-vs-lemlist-vs-woodpecker`; also the send-side sibling to the existing Instantly page. Monetization angle: run outbound/appointment-setting as a service ($1,500-5,000/mo retainer vs $39-174/mo tool), paid setup-and-audit, + up to 35% recurring lifetime affiliate (Rewardful). Pricing verified from emailchaser.com/learn/smartlead-pricing (checked 4 Oct 2026) + smartlead.ai/affiliate-partners: Base $39/mo (2,000 contacts, 6,000 emails), Pro $94/mo (30,000/90,000), Unlimited Smart $174/mo (unlimited contacts, 150,000 emails), Unlimited Prime $379/mo (500,000 emails, 170,000 prospect emails, 3 dedicated servers + 3 client workspaces); lead data $59/mo add-on on Base/Pro (included on Unlimited); client workspaces $29/mo each from Pro up; dedicated servers $39/mo each; verification $0.0017-0.0034/addr; no free plan, trial only, 50% off first month.

Process (all worked first try):
1. Wrote tool JSON to temp `_tool_smartlead.json` (all fields incl. pricing_details).
2. `price` = "From $39/mo · Pro $94/mo" (24 chars); full cost stack + agency extras in pricing_details.
3. `python scripts/upsert_tool_en.py _tool_smartlead.json` → 1 added, total 220.
4. `python scripts/check_price_labels.py` → PASS 220, 0 polluted (33 in 50-80 gray zone).
5. `python scripts/build_en.py` → exit 0; tools/smartlead/index.html, sitemap 220 tools + 187 articles, OG image images/og/smartlead-en-og.png, IndexNow 1 URL (200).
6. `git add -A && commit` (7f0761369, prev bb95c26af) + push origin main (aitoolbox-hk). 465 files changed (normal). Worktree clean.
7. Live: www.aitoolbox.hk/tools/smartlead/ 404 immediately, 200 after ~20s. Title + price label render correctly.

Notes for next run: AI Marketing now 10 tools (getting crowded). Prioritize thin categories: AI Agents (7), AI Automation (8), AI Search (7). Remaining high-ref internal-link candidates with no tool page: retell (24 refs, AI Agents - Vapi already covers voice), bland (21, AI Agents), lemlist (22, AI Marketing). Consider AI Search or AI Automation for diversification. Reminder: ~465 files change per build; `_tool_*.json` temp files are committed by convention.

2026-10-12: Added new English tool **retell-ai** (Retell AI, category AI Agents). ⚠️ IMPORTANT LESSON — the first pick was "zapier", but it turned out to be a NEAR-DUPLICATE: the site already had a `zapier-ai` page (name "Zapier AI", category "Automation"), and `make` (make.com) also already existed. My slug-presence scan was flawed because I only tested exact slugs like 'zapier' / 'make.com' and missed compound slugs ('zapier-ai', 'make'). ALWAYS scan existing slugs with a substring match (e.g. any(s for s in slugs if 'zapier' in s)) before committing to a pick. The zapier commit (53b083b36) was reverted with `git revert --no-commit 53b083b36`, then retell added and both landed in one commit. Note: that revert also swept away an uncommitted daily-log file (2026-10-12.md) and an appended line in the 5d9eccfb automation memory that had been created by the article automation but not yet committed — both were restored from the reverted commit via `git show 53b083b36:<path>`. Lesson: before reverting, check `git show --stat <commit> -- .workbuddy-ai/memory/` for swept-up uncommitted memory files.

Retell AI chosen because AI Agents is the thinnest category (7 tools), it has 24 article refs with no tool page, and the natural internal-link target already exists: `best-ai-voice-agents-2026-vapi-vs-retell-vs-bland-vs-twilio`. Monetization angle (honest): sell an AI phone agent (receptionist / after-hours answering / appointment setter) to local businesses at $500-$2,000/mo + $500-$3,000 setup, while usage is ~$0.11/min (500 min ≈ $55). Pricing verified from retellai.com/pricing (official): pay-as-you-go, NO platform fee, $10 free credits; published $0.07-$0.31/min voice, $0.002+/msg chat; default stack = Retell voice infra $0.055 + TTS $0.015 (Retell/MiniMax/Fish) up to $0.04-$0.10 (ElevenLabs) + LLM ~$0.04 (GPT-5 class) + telephony $0.00 (Retell) = ~$0.11/min all-in; realistic production $0.11-$0.15/min. Add-ons: extra concurrency $8/concurrent call/mo (first 20 free), knowledge base $8/each/mo (first 10 free), verified phone number $10/mo + one-time $10. Enterprise custom, volume discounts toward $0.05/min at $3,000+/mo spend.

Process (all worked):
1. Wrote tool JSON to temp `_tool_retell.json` (all fields incl. pricing_details).
2. `price` = "From $0.07/min · ~$0.11/min all-in" (34 chars); full cost stack in pricing_details.
3. `python scripts/upsert_tool_en.py _tool_retell.json` → 1 added, total 221.
4. `python scripts/check_price_labels.py` → PASS 221, 0 polluted (33 in 50-80 gray zone).
5. `python scripts/build_en.py` → exit 0; tools/retell-ai/index.html, images/og/retell-ai-en-og.png, sitemap 221 tools + 188 articles, IndexNow 1 URL (200).
6. `git add -A && commit` (7c92bd886, prev 53b083b36/744e34ecf) + push origin main (aitoolbox-hk). 472 files changed (normal). Worktree clean.
7. Live: www.aitoolbox.hk/tools/retell-ai/ → HTTP 200 within ~20s (fast this time); /tools/zapier/ → 404 as intended (duplicate removed). Title + price label render.

Notes for next run: AI Agents now 8 tools. Still-thin categories: AI Search (7), AI Automation (8, but make/zapier/n8n/apify already cover it well). Candidate pool (verified NOT present as of this run): replit (75 refs), bolt.new (67), fireflies (139), otter (111), canva (396), notion (304), airtable (43), framer (45), semrush (28), surfer (58), copy.ai (70), v0 (48), lemlist (22), bland (21). Beware near-duplicate slugs: zapier-ai, perplexity-ai, perplexity, make, webflow-ai all exist — do a substring slug scan first. Reminder: ~470 files change per build; `_tool_*.json` temp files are committed by convention.

2026-10-13: Added new English tool **peec-ai** (Peec AI, category AI SEO) — AI search visibility / GEO tracker ($95/$245/$495 per month). Chosen because AI SEO was the thinnest category (only 1 tool: vryse-ai) and the newest article `ai-search-visibility-tools-2026-profound-vs-peec-vs-scrunch-vs-otterly` (2026-10-12) names it with NO tool page → strong internal-link target. Substring slug scan confirmed profound / peec / scrunch / otterly all absent. Monetization angle: sell AI-visibility (GEO) audits ($500-1,500 one-time) and monthly reporting retainers ($500-2,000/mo per brand) — NOT reselling (no fat affiliate). Pricing verified from peec.ai/pricing (official, 2026-10-13): Starter $95/mo (50 prompts, 3 models, 1 project, 1 country, 5 competitors, unlimited users, daily, ~4,500 answers/mo, 4M bot visits); Pro $245/mo (150 prompts, 2 projects, 3 countries, ~13,500 answers); Advanced $495/mo (350 prompts, 5 projects, 25 competitors, ~31,500 answers, Looker Studio); Enterprise custom (up to 13 models incl. Perplexity/Claude/Grok, API+MCP, SSO, unlimited). Base models: ChatGPT, AI Mode, AI Overviews, Copilot, Gemini, Naver AI (choose 3); extra-model add-ons $30/$70/$140 per tier. No free plan; annual saves ~10%; separate agency plan.

Process (all worked first try):
1. Wrote a temp builder `_build_peec_json.py` (emits `_tool_peec.json`; never touches data/tools_en.json), then DELETED the builder so only `_tool_peec.json` remains.
2. `price` = "From $95/mo · Pro $245/mo" (25 chars); full cost stack in `pricing_details`.
3. `python scripts/upsert_tool_en.py _tool_peec.json` → 1 added, total 222.
4. `python scripts/check_price_labels.py` → PASS 222, 0 polluted (33 in 50-80 gray zone).
5. `python scripts/build_en.py` → exit 0; tools/peec-ai/index.html, images/og/peec-ai-en-og.png, sitemap 222 tools + 189 articles, IndexNow 1 URL (200).
6. Committed + pushed to origin main (aitoolbox-hk). Note: `outputs/` (a site-audit artifact dir from a different automation, never tracked, not gitignored) was deliberately EXCLUDED from the commit via `git add -A -- . ':(exclude)outputs'` to keep the commit focused.

Notes for next run: AI SEO now 2 tools (vryse-ai, peec-ai). Remaining thin categories: AI Search (7), AI Agents (8), AI Automation (8), AI Office (3), AI E-commerce (1), AI Research (1), AI Translation (1), AI Website Builder (1). Untapped high-ref internal-link candidates still with no page: profound / scrunch / otterly (same article, AI SEO), airtable (43 refs), lemlist (22), bland (21), hubspot (102), pipedrive (31), zoominfo (44), lusha (22), woodpecker (21). Prefer AI Search or AI Office next for diversification. `_tool_*.json` temp files ARE committed by convention; delete any temp builder script.

2026-10-14: Added new English tool **klaviyo** (Klaviyo, category AI E-commerce) — the email/SMS retention platform most Shopify/DTC brands run on, now marketed as a B2C CRM with AI built in (AI subject lines + copy, Composer data assistant, Customer Agent; predictive CLV/churn sits behind the Marketing Analytics add-on). Chosen because AI E-commerce was the thinnest real category (1 tool: Doba Pilot) and Klaviyo has 22 article refs with no page → natural internal-link target, esp. `best-ai-tools-for-ecommerce-2026` and `best-ai-ecommerce-tools-2026-shopify-magic-vs-salesforce-vs-bigcommerce-vs-wix`. Substring slug scan confirmed klaviyo absent. Monetization angle (honest, not reselling): one-time flow build $1,000-3,000, monthly lifecycle retainer $1,500-5,000/mo per brand, + Klaviyo Solutions Partner revenue share 10-20% on referred accounts; sales stat = Klaviyo's Oct 2026 abandoned-cart benchmark $6.77 RPR email / $4.48 SMS (top 10% $13.70/$8.69). Pricing verified from klaviyo.com/pricing (free tier) + a May 2026 Omnisend breakdown: active-profile billing since Feb 2025 (pay for every non-suppressed profile); Free 250 profiles/500 sends/150 SMS credits; Email $20/mo at 500 profiles, $30/1k, $45/1.5k, $60/2.5k, $100/5k, $150/10k, $400/25k, $720/50k, $1,380/100k (~10x send limit); Email+SMS +$15/mo min (1,250 credits), $35/mo at 500; SMS credits 1,250=$15 … 50,000=$450 (US 1 credit/SMS, MMS 3, UK 5, 24 countries); add-ons Reviews $25 / Marketing Analytics $100 (13.5k profiles) / CDP $500; Klaviyo One = mandatory +20% surcharge over $10,000/mo; 90-day suppression lock; no annual discount on self-serve; no agency console (each client = separate account/bill).

Process (all worked first try):
1. Wrote tool JSON directly to temp `_tool_klaviyo.json` (no builder script needed this time).
2. `price` = "Free + Email $20/mo · Email+SMS $35/mo" (38 chars); full cost stack in `pricing_details`.
3. Caught a false-positive banned-word hit: "as an AI-powered B2C CRM" contains the substring "as an ai" → rephrased to "markets as a B2C CRM with AI built in". NOTE: the checker uses plain substring matching, so avoid the literal string "as an ai" anywhere.
4. `python scripts/upsert_tool_en.py _tool_klaviyo.json` → 1 added, total 223.
5. `python scripts/check_price_labels.py` → PASS 223, 0 polluted (33 in 50-80 gray zone).
6. `python scripts/build_en.py` → exit 0; tools/klaviyo/index.html, category/ai-e-commerce (dir is `ai-e-commerce`, not `ai-ecommerce`), sitemap 223 tools + 190 articles, OG image images/og/klaviyo-en-og.png, IndexNow 1 URL (200).
7. Committed with `git add -A -- . ':(exclude)outputs'` (the untracked `outputs/site-audit-2026-10-13` dir from another automation is NOT gitignored — keep excluding it) → commit 276ee9db7, prev a1b480252. 472 files changed (normal). Pushed origin main (aitoolbox-hk). Worktree clean.
8. Live: www.aitoolbox.hk/tools/klaviyo/ 404 on attempt 1, 200 on attempt 2 (~15s). Title + price label + OG image all verified.

Notes for next run: AI E-commerce now 2 tools. Still-thin categories: AI Search (7), AI Agents (8), AI Automation (8), AI Office (3), AI Research (1), AI Translation (1), AI Website Builder (1), Market Research (1). Strong untapped internal-link candidates (verified absent, refs in articles_en.json): hubspot (102), airtable (43), zoominfo (44), pipedrive (31), brevo (30), mailchimp (45), ghost (27), profound (22), lemlist (22), bland (22), lusha (22), woodpecker (21), otterly (14), scrunch (16). Category page dirs use the hyphenated form of the raw category name (e.g. "AI E-commerce" → `category/ai-e-commerce/`). Reminder: ~470 files change per build; `_tool_*.json` temp files are committed by convention.

2026-10-15: Added new English tool **intercom** (Intercom, category AI Office) — AI-first customer service platform; Fin AI Agent resolves chat/email tickets at $0.99 per outcome on top of seat fees. Chosen because AI Office was thin (3 tools) and two existing articles name Intercom Fin with no tool page (`best-ai-customer-service-tools-2026-intercom-fin-vs-zendesk-ai-vs-tidio-vs-ada`, `best-ai-tools-customer-support-2026`) → natural internal-link targets. Substring slug scan confirmed intercom absent. Monetization angle (honest, no fat affiliate): help-center + Fin build ($1,500-5,000 one-time), monthly AI support retainer ($500-2,000/mo per client), and the easiest sale — Fin standalone on a client's existing helpdesk (Salesforce/HubSpot/Freshdesk/Freshchat, $0.99/outcome, no seat fee, no migration). Retainer math: 1,500 tickets/mo × 50% resolved = 750 outcomes × $0.99 = $742 + 3 Essential annual seats $87 = ~$830/mo cost vs ~$3,000/mo of agent capacity (750 × 12 min @ $20/hr). Pricing verified from intercom.com/pricing + intercom.com/help/en/articles/9061614 (official, Oct 2026): Essential $39/seat/mo monthly, $29 annual; Advanced $99/$85 (20 Lite seats); Expert $139/$132 (50 Lite seats); Fin from $0.99/outcome on every plan, or standalone on external helpdesks (min commitments, no seat cost); unlimited live chat/support email/in-app chats/banners/tooltips included; email/SMS/WhatsApp/phone pay-as-you-go with volume tiers; add-ons Pro from $100/mo (incl. Operator), Copilot (10 conv/agent/mo free), Proactive Support Plus $99/mo; 14-day trial no card; Early Stage startup deal 93% off yr1 ($65/mo Advanced) / 50% yr2 / 25% yr3 + 300 free Fin outcomes/mo + 6 seats; Fin Voice = quote only; 25,000+ businesses.

Process (all worked first try):
1. Wrote a temp emitter `_gen_intercom_json.py` (emits `_tool_intercom.json` only), then DELETED it. (JSON content is 10.7k chars with tables → hand-escaping was too error-prone.)
2. `price` = "From $0.99/resolution · seats from $29/mo" (41 chars); full cost stack in `pricing_details`.
3. Pre-flight scan for smell words + the literal "as an ai" substring: 0 hits (this trap bit the klaviyo run).
4. `python scripts/upsert_tool_en.py _tool_intercom.json` → 1 added, total 224.
5. `python scripts/check_price_labels.py` → PASS 224, 0 polluted (33 in 50-80 gray zone).
6. `python scripts/build_en.py` → exit 0; tools/intercom/index.html, category/ai-office/, sitemap 224 tools + 191 articles, OG image images/og/intercom-en-og.png, IndexNow 1 URL (200). Pillow IS working (contradicts the 2026-10-15 article-run note in the daily log).
7. Committed with `git add -A -- . ':(exclude)outputs' ':(exclude).workbuddy-ai/memory'` (commit cece7c52a, prev b3fdf1175) then a separate memory commit; pushed origin main (aitoolbox-hk). 477 files changed (normal).

IMPORTANT convention fix found this run: earlier tool contents link tools as bare `/[slug]/` (e.g. klaviyo → `/instantly-ai/`, peec-ai → `/vryse-ai/`), but tool pages actually live at `/tools/<slug>/` (there are NO root-level slug dirs, no redirects in vercel.json) — so those bare links are silent 404s (validate_internal_links.py only checks `/articles/`). New content should use `/tools/<slug>/`. Consider a cleanup pass for old tool content.

Notes for next run: AI Office now 4 tools. Still-thin categories: AI Research (1), AI Translation (1), AI Website Builder (1), Market Research (1), AI SEO (2), AI E-commerce (2), AI Office (4), AI Search (7), AI Agents (8), AI Automation (8). Untapped high-ref candidates verified absent (substring scan, refs in articles_en.json): hubspot (102), shopify (97), zendesk (55), gong (49), mailchimp (45), clickup (45), activecampaign (45), zoominfo (44), intercom (now added), airtable (43), loom (42), outreach (40), monday (37), calendly (37), asana (35), tableau/power bi/looker (35 each), pipedrive (31), posthog (30), brevo (30), ahrefs (28), 10web (28), lemlist (22), bland (22), lusha (22), woodpecker (21), profound (22), scrunch (16), otterly (14). Note "mode"/"close" counts are substring false positives. Prefer AI Research / AI Translation / AI Website Builder / Market Research next for diversification.
