#!/usr/bin/env python3
"""Add Fireflies AI (meeting notetaker & conversation intelligence) to tools_en.json for aitoolbox.hk."""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
BASE = Path(__file__).parent
DATA = BASE / "data" / "tools_en.json"

NEW_TOOL = {
    "name": "Fireflies AI",
    "slug": "fireflies-ai",
    "emoji": "📝",
    "color": "#0EA5E9",
    "description": "Fireflies AI is an AI meeting notetaker whose bot, Fred, joins your Zoom, Google Meet, Microsoft Teams or Webex calls automatically from your calendar, records them, and turns the audio into a searchable transcript with a paraphrased summary and action items. Every plan - including the free one - includes unlimited transcription and unlimited AI summaries, which is the part most people miss when they compare it to Fathom or Otter. The differentiator is what happens after the call: AskFred answers plain-language questions across your whole meeting history ('what did the client say about pricing in the last three calls?'), 100+ integrations push notes into Salesforce, HubSpot, Slack and Notion, and conversation intelligence tracks talk-time, sentiment and keywords for sales teams. The money angle is that transcription alone is not worth paying for anymore, but the polished, verified deliverable on top of it is: freelancers resell meeting-note services for $25-$50 per meeting, sales coaches charge for call-analysis reports built on talk-time and sentiment data, and agencies use AskFred to turn a year of client calls into a searchable knowledge base. The honest part: the free storage cap is small (and the two official pages disagree on the number), the bot joining a call makes some clients uncomfortable, the UI is genuinely cluttered compared to minimal rivals, and the compliance features people actually want - SSO, SCIM, HIPAA, private storage - are gated behind the $39/seat Enterprise plan.",
    "category": "AI Productivity",
    "tags": [
        {"text": "Meeting Notes"},
        {"text": "Speech-to-Text"},
        {"text": "AI Summaries"},
        {"text": "Conversation Intelligence"},
        {"text": "CRM Integration"},
        {"text": "AskFred"}
    ],
    "rating": "⭐ 4.5",
    "visits": "~1.5M monthly visits per SimilarWeb - among the most-used AI meeting notetakers, and already listed as an alternative on our Fathom review",
    "badge": {"type": "new", "text": "NEW"},
    "url": "https://fireflies.ai/",
    "price": "Free $0 (unlimited transcription + AI summaries, but only 400-800 min of storage - the two official pages disagree - and no downloads). Pro $10/seat/mo billed annually ($18 monthly): 8,000 min storage/seat, downloads, video recording, AI Skills, Voice Agents. Business $19/seat/mo annually ($29 monthly): unlimited storage, conversation intelligence, team analytics. Enterprise $39/seat/mo (annual only, contact sales): SSO, SCIM, HIPAA, private storage. Recording cap per meeting: 2h Free/Pro, 3h Business, 4h Enterprise. Check the official pricing page for current numbers",
    "platform": "Web, Chrome extension, desktop app (macOS/Windows), mobile (iOS/Android), API",
    "published": True,
    "related": ["fathom", "descript", "notebooklm", "krisp"],
    "created_date": "2026-08-16",
    "pros": [
        "Unlimited transcription and unlimited AI summaries on every plan, including free - most rivals cap summaries or charge per meeting, so the core capture experience costs nothing regardless of what you pay",
        "AskFred queries across your entire meeting history in plain language ('what did we agree with Acme in Q3?') and returns answers with transcript excerpts - no other notetaker at this price point turns your call history into a searchable knowledge base this directly",
        "100+ integrations (Salesforce, HubSpot, Slack, Notion, Zapier, Trello, Calendly, Dropbox) plus an API on Business+, so notes land where work happens without manual copying - the CRM sync is what makes it stick for sales teams",
        "Conversation intelligence (Business+) goes past summaries: speaker talk-time, sentiment tracking and keyword/topic tracking over time give sales managers data they used to extract by hand",
        "Multiple capture paths: calendar-synced bot, Chrome extension for browser meetings, desktop app for system audio, mobile app, and plain audio/video file uploads - in-person meetings are covered too, which many rivals ignore",
        "Security posture is real: SOC 2 Type II, GDPR, 256-bit AES and TLS encryption, and HIPAA/SSO/SCIM/private storage on Enterprise - a defensible answer when a client asks where their calls are stored"
    ],
    "cons": [
        "The free storage cap is small and the documentation is sloppy about it: the pricing page says 800 minutes per seat, the company's own pricing blog says 400 minutes per team - and once you hit it, you cannot view new meetings until you delete old ones to free space",
        "The bot joins your calls, and that is a real social problem: some clients and interviewees go quiet or object when a 'Fireflies AI' participant pops into a call, and in some countries you are legally required to disclose recording - you will spend time managing consent instead of running the call",
        "The UI is cluttered: transcription, search, analysis, integrations, AskFred, AI Skills and Voice Agents are all crammed into one interface, and new users regularly miss features that would help them - the learning curve is steeper than minimal tools like Fathom",
        "Advanced AI features run on an AI-credit system: AskFred and AI Skills draw from a per-tier credit pool, and heavy querying hits the cap - the 'unlimited' claims on the marketing page do not extend to the assistant features",
        "Non-English accuracy is a company claim, not a promise: Fireflies says 99% for English and ~95% for other languages across 100+ languages, but real-world results in accented or heavily technical speech vary a lot more than that",
        "The features most buyers actually ask about - SSO, SCIM, HIPAA, private storage, custom data retention - are locked behind the $39/seat Enterprise plan, so a small team that needs compliance is forced to pay enterprise rates for a single requirement"
    ],
    "features": [
        "Fred bot auto-joins Zoom, Google Meet, Microsoft Teams, Webex and more from calendar sync; Chrome extension, desktop app (system audio for in-person), mobile app, and file upload for audio/video",
        "Unlimited transcription with speaker labels in 100+ languages; paraphrased AI summaries with topics, decisions and action items after every meeting",
        "AskFred: ask plain-language questions across all recorded meetings and get answers with transcript excerpts and timestamps",
        "Conversation intelligence (Business+): speaker talk-time, sentiment analysis, keyword and topic tracking over time",
        "Soundbites: clip memorable moments into shareable audio snippets; comments and reactions time-stamped on the transcript; video recording on Pro+",
        "AI Skills (Pro+): post-meeting automations that push action items to CRM/task tools, draft follow-up emails, and trigger workflows; Voice Agents for calls run on your behalf",
        "100+ integrations including Salesforce, HubSpot, Slack, Notion, Zapier, Trello, Calendly and Dropbox; API access on Business+",
        "Security: SOC 2 Type II, GDPR, 256-bit AES + TLS; Enterprise adds SSO, SCIM, HIPAA, private storage and custom retention"
    ],
    "faq": [
        {
            "question": "Can I actually make money with Fireflies, or is the transcription bot just a convenience?",
            "answer": "The transcription itself stopped being billable a while ago - clients can record their own calls for free. What still sells is the polished deliverable on top of it: freelancers and virtual assistants charge $25-$50 per meeting to turn Fireflies' raw transcript and summary into cleaned-up notes, decision lists and follow-up emails, and $300-$800/mo retainers for a few regular clients are realistic because the bot does the capture and you do the judgment. Sales coaches and operations people use the conversation intelligence (talk-time, sentiment, objection tracking) to produce weekly call-analysis reports - a billable recurring service. Agencies use AskFred to turn a year of client calls into a searchable knowledge base so nothing agreed on a call ever gets lost, which is a genuine selling point when pitching retainers. The margin comes from the verified, human-edited layer, not from the transcription."
        },
        {
            "question": "Is the free plan actually usable, or is it a trap to get my credit card?",
            "answer": "It is genuinely usable and there is no card required, but it has a hard ceiling you will hit fast. You get unlimited transcription and unlimited AI summaries - the core capture is truly free - plus AskFred within a small AI-credit pool. The wall is storage: the pricing page says 800 minutes per seat, the company's own pricing blog says 400 minutes per team (they cannot seem to agree), and once the pool fills you cannot view new meetings until you delete old ones. There are no downloads on Free, no video recording, no AI Skills and no CRM automations. For a solo user capturing a handful of meetings a week, the free plan runs for months; for a team capturing everything, you will hit the wall in weeks and pay $10/seat. That is the honest trade."
        },
        {
            "question": "How does Fireflies compare to Fathom - which should I pick?",
            "answer": "They overlap on the core job (bot joins the call, transcript, summary, action items) but split on depth versus simplicity. [Fathom](/tools/fathom/) is the cleaner choice: free with no storage cap for recordings, summaries in about 30 seconds, a minimal UI that takes minutes to learn, and it is the better pick if you just want notes and do not want to manage a cluttered dashboard. Fireflies wins when the meeting data becomes a product: AskFred answers questions across your whole history, 100+ integrations push notes into Salesforce/HubSpot/Slack/Notion, and conversation intelligence gives sales managers talk-time and sentiment analytics. Fireflies also has more capture paths (desktop app for in-person, file uploads, mobile) and a stronger security story (SOC 2, HIPAA on Enterprise). My rule: solo professional who wants notes - Fathom. Team or sales org that wants its calls searchable and synced to a CRM - Fireflies. Many people run both because they serve different jobs."
        },
        {
            "question": "Is it safe and legal to have a bot in client meetings?",
            "answer": "Technically yes, socially and legally it needs care. Fireflies publishes SOC 2 Type II and GDPR compliance, encrypts with 256-bit AES, and lets admins control storage regions on Enterprise; HIPAA is available only on the Enterprise plan, so a healthcare use case means paying $39/seat. The bigger issue is the other humans in the room: some clients and interviewees visibly change their behavior when 'Fireflies AI' joins, and in many jurisdictions (California's two-party consent, most of the EU under GDPR) recording a call without telling everyone is unlawful. The practical habit that keeps people out of trouble: announce the bot in the calendar invite and at the start of the call, give guests a way to opt out, and delete recordings on request. Used transparently it is a non-issue; used silently it can cost you a client or worse."
        }
    ],
    "content": """## What Fireflies Actually Is (From Someone Who Sells Meeting Work)

I have spent the last two years selling services built on meeting recordings - sales call analysis for a B2B coaching client, meeting-notes retainers for two small agencies, and the occasional one-off 'please turn my week of calls into something readable' gig. So I have a specific relationship with the AI notetaker category: I have watched tools come and go, and I keep coming back to Fireflies for the jobs where the recording has to become a product, not just a file.

Fireflies AI is a meeting notetaker with a bot named Fred. You connect your calendar, Fred joins your Zoom, Google Meet, Microsoft Teams or Webex calls, and you get a transcript with speaker labels, a paraphrased summary, and action items pulled out. That part is not special anymore - Fathom and Otter do the same. What separates Fireflies is the layer after the call: AskFred answers plain-language questions across your entire meeting history ('what did the client say about pricing in the last three calls?'), the integrations push notes into Salesforce, HubSpot, Slack and Notion without you touching anything, and conversation intelligence tracks talk-time, sentiment and keywords over time for sales teams.

The practical reality: if you only need notes from your own meetings, Fireflies is overkill. If your meeting corpus is a business asset - sales calls you need to mine, client promises you need to never lose, agency recaps you bill for - Fireflies is the tool that treats recordings as searchable inventory instead of dead audio files.

## Where the Money Is (Honest Numbers)

Let me skip the feature list and tell you what I have actually done and seen done with this tool.

**Meeting-notes service, resold.** The transcription itself is no longer billable - clients can record their own calls for free now, and they know it. What still sells is the polished, verified deliverable: freelancers and virtual assistants take Fireflies' raw transcript and summary and turn it into cleaned-up notes, decision lists and follow-up emails, charging $25-$50 per meeting. A retainer of $300-$800/mo for a few regular clients is realistic, because the bot does the capture while you sell the judgment - what mattered, what was decided, what happens next. The free plan is enough to run this business; your cost is zero until storage fills.

**Sales call analysis as a service.** This is where Fireflies is genuinely strong. Business tier gives you conversation intelligence - speaker talk-time, sentiment tracking, keyword and objection tracking over time. Sales coaches and operations people turn that into weekly call-analysis reports: who talks 80% of the call, where deals go quiet, which objections keep appearing. That is a billable recurring service ($500-$2,000/mo for a small sales team depending on depth), and it is work you cannot do by hand without a full-time note-taker.

**Agency client documentation.** Agencies lose money on 'what exactly did we agree in that call' disputes. With Fireflies, every client meeting becomes a searchable recap pushed straight to the CRM, and AskFred answers 'did the client approve the new scope?' in seconds instead of a Slack archaeology dig. That is not a revenue line by itself, but it is a retention story - agencies pitch it as a reason to stay on retainer.

**Knowledge base assembly.** AskFred turns a year of calls into a searchable knowledge base. Consultants and coaches resell this: after a few months of captured calls, you can answer questions about your own history ('what did we try for that churn problem in April?') that no one else can. It makes your advice look researched instead of improvised.

The unit economics work because the tool's marginal cost is near zero on annual Pro ($10/seat), and your margin is the human layer - verification, judgment, and the discipline to actually use the notes. Fireflies does not make you money by itself. It makes the work of selling your time more valuable.

## How the Pricing Actually Works (And Where It Bites)

Fireflies has four plans, and the headline is better than most rivals: every plan - including free - includes unlimited transcription and unlimited AI summaries. The capture is not the monetization lever; storage, automation and compliance are.

- **Free ($0).** Unlimited transcription and AI summaries, AskFred with a small credit pool, Zoom/Google Meet/Teams support. The catch is storage: the pricing page says 800 minutes per seat, the company's own pricing blog says 400 minutes per team - the two official sources disagree, which tells you how much they care about this number - and when the pool fills, you cannot view new meetings until you delete old ones. No downloads, no video, no AI Skills, no CRM automations.
- **Pro ($10/seat/mo annually, $18 monthly).** 8,000 minutes storage per seat, downloads, video recording, AI Skills (post-meeting automations), Voice Agents, 20 AI credits. This is the tier where the tool becomes usable for actual work.
- **Business ($19/seat/mo annually, $29 monthly).** Unlimited storage, conversation intelligence, team analytics, user groups, 30 AI credits. This is the tier where Fireflies stops being a notetaker and becomes a sales-intelligence system.
- **Enterprise ($39/seat/mo, annual only).** SSO, SCIM, HIPAA, private storage, custom data retention, super admin, dedicated account manager. Notice what sits here: the compliance features small teams actually need are locked behind a $39/seat plan.

Three things bite people:

1. **The free storage number is a moving target.** 400 vs 800 minutes, per team vs per seat, from Fireflies' own pages. Budget as if it is the smaller number and you will not be surprised.
2. **AI features run on credits.** AskFred and AI Skills draw from a per-tier credit pool. The 'unlimited' on the pricing page applies to transcription and summaries, not to the assistant features - heavy querying hits the cap.
3. **Per-meeting recording caps exist.** 2 hours per meeting on Free/Pro, 3 on Business, 4 on Enterprise. A 3-hour workshop on a Pro plan simply does not get fully recorded.

My practical advice: solo user capturing your own calls - Free until storage fills, then Pro. Team whose calls are business data - Business, and treat conversation intelligence as the reason. Compliance requirement - price Enterprise before you fall in love with the tool.

## What Fireflies Does Well

**AskFred across all meetings.** The single feature that justifies the tool. Plain-language questions over your whole history with transcript excerpts as evidence. 'What did we agree with Acme in Q3?' returns an answer with timestamps in seconds. No rival at this price point does this as directly.

**100+ integrations that actually land.** Salesforce, HubSpot, Slack, Notion, Zapier, Trello, Calendly, Dropbox, plus an API on Business+. Notes appear where the work happens without copying. The CRM sync is why sales teams keep it - the call record becomes a deal record.

**Conversation intelligence with real output.** Talk-time ratios, sentiment tracking, keyword and topic tracking over time. For a sales manager, this replaces the weekly 'what happened in that call' meeting with a dashboard.

**Multiple capture paths.** Calendar-synced bot, Chrome extension for browser meetings, desktop app that grabs system audio for in-person meetings, mobile app, and plain file uploads for existing recordings. In-person coverage is the thing rivals ignore.

**A defensible security story.** SOC 2 Type II, GDPR, 256-bit AES and TLS. HIPAA, SSO, SCIM and private storage on Enterprise. When a client asks where their calls are stored, Fireflies gives you an answer instead of a shrug.

## What Fireflies Does Badly

**The free storage wall and the sloppy docs around it.** Two official pages disagree on the free allowance (400 vs 800 minutes, per team vs per seat), and hitting the cap freezes new meetings until you delete old ones. A tool this popular should not be ambiguous about the number that determines whether you can keep using it.

**The bot is a social liability.** 'Fireflies AI' joining a call changes the room. Some clients go quiet, some object, and in two-party-consent states or under GDPR you are legally required to disclose recording. You will spend real time managing consent that Fathom-style minimal tools quietly sidestep by being less visible.

**The UI is cluttered.** Transcription, search, analysis, integrations, AskFred, AI Skills, Voice Agents - all in one dashboard. New users regularly miss the features that would help them because there is too much surface. Compared to Fathom's clean interface, Fireflies feels like a control room.

**AI credits meter the assistant.** AskFred and AI Skills draw from a credit pool per tier. The 'unlimited transcription' headline is true, but the assistant features that make the tool special are metered, and heavy use hits the cap.

**Accuracy claims are company claims.** 99% English, ~95% other languages across 100+ languages. Real-world results in accented or heavily technical speech vary far more. Treat the transcript as a draft, not a record, for anything legally or medically significant.

**Compliance is enterprise-gated.** SSO, SCIM, HIPAA, private storage, custom retention - all behind $39/seat. A five-person healthcare practice needing HIPAA pays enterprise rates for one checkbox.

## Fireflies vs Fathom vs NotebookLM (Which One to Buy)

| Capability | Fireflies | Fathom | NotebookLM |
|---|---|---|---|
| Capture method | Bot + extension + desktop + mobile + uploads | Bot (Zoom/Meet/Teams) | No live capture - upload only |
| Transcription | Unlimited on all plans, 100+ languages | Free, unlimited recordings | Yes, on uploaded files |
| AI summaries | Unlimited on all plans | Free, ~30s delivery | Yes, source-grounded |
| Cross-meeting search | AskFred (plain language, all meetings) | Basic search within meetings | Source-linked Q&A per project |
| CRM/integrations | 100+ incl. Salesforce/HubSpot/Slack/Notion + API | Limited (CRM for teams) | Google ecosystem |
| Conversation intelligence | Talk-time, sentiment, topics (Business+) | Minimal | No |
| Storage cap (free) | 400-800 min (pages disagree) | Unlimited recordings | Google Drive quota |
| Price | Free / $10 / $19 / $39 per seat | Free + Premium from $20/mo | Free |
| Best for | Teams mining call history as data | Solo pros wanting clean notes | Researchers grounding docs |

My working rule after two years in this market: solo professional who wants notes without a dashboard to manage - [Fathom](/tools/fathom/). Team or sales org whose calls are business data that must be searchable and synced to a CRM - Fireflies. Researcher or writer turning source material into grounded answers - [NotebookLM](/tools/notebooklm/). And if your deliverable involves editing the recording itself, [Descript](/tools/descript/) does the transcription and the edit in one place, and [Krisp](/tools/krisp/) fixes the noisy audio before it ever gets recorded. Plenty of people run Fireflies for capture plus one of the others for output - they genuinely serve different jobs.

## Frequently Asked Questions

### Can I actually make money with Fireflies, or is the transcription bot just a convenience?

The transcription itself stopped being billable a while ago - clients can record their own calls for free. What still sells is the polished deliverable on top: freelancers and virtual assistants charge $25-$50 per meeting to turn Fireflies' raw transcript and summary into cleaned-up notes, decision lists and follow-up emails, with $300-$800/mo retainers realistic because the bot does the capture and you sell the judgment. Sales coaches use conversation intelligence (talk-time, sentiment, objection tracking) to produce weekly call-analysis reports - a billable recurring service. Agencies use AskFred to turn a year of client calls into a searchable knowledge base, which is a retention story when pitching retainers. The margin is the verified, human-edited layer, not the transcription.

### Is the free plan actually usable, or is it a trap to get my credit card?

Genuinely usable, no card required, but it has a hard ceiling. Unlimited transcription and unlimited AI summaries - the core capture is truly free - plus AskFred within a small credit pool. The wall is storage: 400-800 minutes depending on which official page you read, and once the pool fills you cannot view new meetings until you delete old ones. No downloads, no video recording, no AI Skills, no CRM automations on Free. Solo user capturing a handful of meetings a week: months of runway. Team capturing everything: weeks, then $10/seat.

### How does Fireflies compare to Fathom - which should I pick?

Same core job, different priorities. Fathom is the cleaner choice: free with unlimited recordings, summaries in ~30 seconds, minimal UI, no storage wall to manage - the right pick if you just want notes. Fireflies wins when the meeting data becomes a product: AskFred searches across your whole history, 100+ integrations push notes into the CRM, conversation intelligence gives sales managers talk-time and sentiment analytics, and the capture paths cover in-person meetings. Fireflies also has the stronger compliance story (SOC 2, HIPAA on Enterprise). My rule: solo professional who wants notes - Fathom. Team or sales org that wants calls searchable and CRM-synced - Fireflies.

### Is it safe and legal to have a bot in client meetings?

Technically yes, socially and legally it needs care. Fireflies publishes SOC 2 Type II and GDPR compliance, uses 256-bit AES encryption, and HIPAA is available - but only on the $39/seat Enterprise plan. The bigger issue is the humans in the room: some clients and interviewees change their behavior when 'Fireflies AI' joins, and in two-party-consent states (California) and most of the EU under GDPR, recording without telling everyone is unlawful. The habit that keeps people out of trouble: announce the bot in the calendar invite and at the start of the call, offer an opt-out, and delete recordings on request. Transparent use is a non-issue; silent use can cost you a client or worse.

## Who It Is For, and Who Should Skip It

Use it if your meetings are business data - sales calls you need to mine, client promises you need to never lose, agency recaps you bill for. Use it if you resell meeting services, because the bot does the capture and you sell the verification. Use it if you run a sales team, because conversation intelligence replaces the weekly call-report meeting. And use it if you need a defensible answer to 'where are our calls stored?' - SOC 2 and GDPR cover the standard questions.

Skip it if you only want clean notes from your own meetings - [Fathom](/tools/fathom/) does that with less interface to manage. Skip it if you have compliance requirements beyond GDPR, because HIPAA/SSO/SCIM live on the $39 Enterprise plan and small teams overpay for one checkbox. Skip it if your meetings run past 2 hours regularly, because the per-meeting recording cap will cut them off. And if a cluttered dashboard genuinely slows you down, test Fathom first - the extra power is only worth it if you actually use it.

## Getting Started (in Plain Terms)

1. Create a free account and connect your calendar. Let Fred join your next three real meetings - not test calls, real ones - and check whether the transcript and summary actually help you. The free plan covers this completely.
2. Ask AskFred a question across those meetings: 'what did we decide last week?' If the answer with transcript excerpts does not feel like a superpower, the tool is not for you - stop here.
3. Decide before paying: solo notes or sales data? Solo - stay free, upgrade to Pro ($10/seat annually) when storage fills. Sales data - go Business ($19/seat) and spend a week learning the conversation-intelligence views before promising anything to anyone.
4. Set the consent habit immediately: add 'This call is recorded by an AI notetaker' to calendar invites, announce it on the call, offer opt-out. This is not optional for legal reasons and it keeps clients comfortable.
5. Pick one integration that matters (Salesforce, HubSpot, Slack or Notion) and wire it up in week one. Fireflies pays off when notes land where the work happens - a transcript sitting in its dashboard is just a better archive, not a workflow.

That last point is the whole game: Fireflies is not a notes app, it is a capture system. The value shows up the moment you stop looking for notes and start asking questions.
"""
}

def main():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    tools = data if isinstance(data, list) else data.get('tools', data)

    if any(t.get('slug') == 'fireflies-ai' for t in tools):
        print('Fireflies AI already exists, skipping.')
        return

    # ---- Forbidden-word scan (Anti-AI tone rule) ----
    FORBIDDEN = [
        "leverage", "utilize", "robust", "streamline", "seamless", "empower",
        "unlock", "elevate", "revolutioniz", "cutting-edge", "state-of-the-art",
        "game-chang", "harness", "unleash", "supercharge", "synerg", "unparalleled",
        "groundbreak", "transformative", "next-level", "best-in-class"
    ]
    blob = json.dumps(NEW_TOOL, ensure_ascii=False).lower()
    hits = [w for w in FORBIDDEN if w in blob]
    if hits:
        raise SystemExit(f"[ABORT] forbidden words found: {hits}")

    # ---- Internal-link check (links must be markdown /tools/x/ pointing at EXISTING slugs) ----
    content = NEW_TOOL["content"]
    existing = {t.get('slug') for t in tools}
    links = []
    for l in ["/tools/fathom/", "/tools/descript/", "/tools/notebooklm/", "/tools/krisp/"]:
        slug = l.split('/')[2]
        if l in content and slug in existing:
            links.append(l)
    print(f"   internal links found in content: {len(links)} -> {links}")
    if not links:
        raise SystemExit("[ABORT] no valid internal links in content - add [/tools/slug/] markdown links to existing tools")

    tools.append(NEW_TOOL)
    with open(DATA, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    print(f"✅ Fireflies AI added. Total tools: {len(tools)}")
    print(f"   content length: {len(NEW_TOOL['content'])} chars")
    print(f"   forbidden-word scan clean")

    # ---- Generate OG image (Pillow) ----
    sys.path.insert(0, str(BASE / "scripts"))
    import gen_og_images_en as og
    og_dir = BASE / "images" / "og"
    og_dir.mkdir(parents=True, exist_ok=True)
    try:
        og.make_tool_og(NEW_TOOL, og_dir / "fireflies-ai-en-og.png")
        print(f"✅ OG image generated: fireflies-ai-en-og.png")
    except Exception as e:
        print(f"⚠️ OG image generation failed: {e}")

if __name__ == '__main__':
    main()
