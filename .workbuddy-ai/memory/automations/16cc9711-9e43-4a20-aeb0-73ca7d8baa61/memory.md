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
