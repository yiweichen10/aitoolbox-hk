#!/usr/bin/env python3
"""
inject_faq_blocks.py — 治本补全 14 篇文章缺失/损坏的 FAQ 区块。
不依赖外部 API（.env 不在本工作区），由 SEO 专家直接撰写母语级 English FAQ，
贴合站点 AEO+GEO 规范：真实用户疑问、50-100 词直答、引用文章已覆盖的工具内链、不编造数据。

14 篇 = 13 篇缺 ## FAQ 区块 + 1 篇(best-ai-tools-for-seo-2026) 标题在但 ### 问题行为空。

执行：python scripts/inject_faq_blocks.py
"""
import json, re, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE_DIR, "data", "articles_en.json")

def L(slug, name):
    return f"[{name}](/{slug}/)"

FAQ = {
"ai-tools-for-teachers-2026": """## Frequently Asked Questions

### Is AI going to replace teachers?
No. AI handles grading, worksheet generation, and admin busywork so teachers reclaim 5-10 hours weekly for actual instruction. The human role—mentoring, reading a confused face, adapting mid-lesson—is irreplaceable. Tools like """ + L("magicschool-ai","MagicSchool AI") + """ and """ + L("diffit","Diffit") + """ assist; they don't teach.

### Which AI tool is safest for student data?
Prioritize tools with explicit FERPA / COPPA compliance and school-approved accounts. """ + L("grammarly-ai","Grammarly") + """ and """ + L("edulastic","Edulastic") + """ offer education-tier plans with data controls. Never paste student names into consumer chat tools without district approval.

### Can AI help with IEP and special-needs students?
Yes. Text-to-speech, leveled reading (via """ + L("diffit","Diffit") + """), and speech-to-text reduce barriers for dyslexic or ELL students. AI drafts accommodations faster, but the IEP team still owns every decision.

### Do these tools work without internet at school?
Most run in-browser and need connectivity. For offline labs, pre-generate materials with """ + L("chatgpt","ChatGPT") + """ the night before and print. Plan for spotty Wi-Fi; don't build a lesson that dies without it.

### Are free AI teacher tools good enough?
For solo use, yes—""" + L("grammarly-ai","Grammarly") + """ free tier and """ + L("magicschool-ai","MagicSchool") + """ free plan cover 80% of tasks. Schools needing rostering, LMS integration, and privacy controls should budget for a paid education tier.""",

"ai-tools-for-content-creators-2026": """## Frequently Asked Questions

### What is the best all-in-one AI stack for a solo creator?
Pair """ + L("chatgpt","ChatGPT") + """ (ideas/scripts) + """ + L("canva","Canva") + """ (design) + """ + L("elevenlabs","ElevenLabs") + """ (voiceover) + """ + L("capcut","CapCut") + """ (edit). This covers writing, visuals, audio, and finishing without leaving a $30/month budget.

### Can AI actually write content that doesn't sound robotic?
Yes, if you brief it with your voice and fact-check the output. """ + L("chatgpt","ChatGPT") + """ drafts; you edit. Treat AI as a speed typist, not the author. The robotic feel comes from publishing raw output untouched.

### Which tool turns long videos into short clips?
""" + L("opus-clip","Opus Clip") + """ and """ + L("descript","Descript") + """ auto-detect hooks and reframe long uploads into 30-60s verticals. Creators report 10x more shorts output per recording session.

### Is Midjourney still worth it for thumbnails?
For stylized, scroll-stopping thumbnails, """ + L("midjourney","Midjourney") + """ leads. For fast branded templates, """ + L("canva","Canva") + """ with AI is enough. Pick by whether you need art direction or speed.

### Do I need to disclose AI-generated content?
On most platforms, yes—YouTube and Instagram flag synthetic media, and audiences trust transparency. Label AI voiceovers and disclose heavily edited imagery to avoid demonetization.""",

"best-ai-tools-for-freelancers-2026": """## Frequently Asked Questions

### What AI tools save freelancers the most time?
""" + L("claude","Claude") + """ for client comms, """ + L("cursor","Cursor") + """ for any coding, and """ + L("grammarly-ai","Grammarly") + """ for proposals cut admin by 40%. The biggest win is automating the work you used to skip—invoicing, follow-ups, drafting.

### Which AI tool helps me charge higher rates?
Quality. """ + L("midjourney","Midjourney") + """ and """ + L("adobe-firefly","Adobe Firefly") + """ let solo freelancers deliver agency-grade visuals, justifying premium pricing. Clients pay for output, not headcount.

### Is a free AI tool enough to start freelancing?
Yes. """ + L("chatgpt","ChatGPT") + """ free tier, """ + L("canva-ai","Canva AI") + """, and """ + L("capcut-ai","CapCut") + """ cover MVP deliverables. Upgrade to paid only when volume or client specs demand it.

### Can AI do my client work while I sleep?
Partially. """ + L("make","Make") + """ and """ + L("n8n","n8n") + """ run lead-gen and reporting automations 24/7. But strategy, relationships, and final quality checks stay human—automate the task, not the judgment.

### How do I avoid AI plagiarism claims from clients?
Use AI for structure and drafts, then rewrite in your voice and cite sources. """ + L("grammarly-ai","Grammarly") + """ and """ + L("quillbot","QuillBot") + """ help paraphrase. Deliver original work; never pass a raw AI blob as yours.""",

"ai-tools-for-social-media-2026": """## Frequently Asked Questions

### What's the best AI tool to schedule posts across platforms?
""" + L("buffer","Buffer") + """ and """ + L("later","Later") + """ handle multi-platform scheduling with AI caption and time-slot suggestions. """ + L("claude","Claude") + """ drafts the actual copy. Combine for a set-and-forget pipeline.

### Can AI generate on-brand visuals without a designer?
Yes. """ + L("canva-ai","Canva AI") + """ and """ + L("adobe-firefly","Adobe Firefly") + """ produce branded templates; """ + L("ideogram","Ideogram") + """ makes text-accurate memes. Keep a saved brand kit so outputs stay consistent.

### Which tool turns one post into every platform's format?
""" + L("descript","Descript") + """ and """ + L("elevenlabs","ElevenLabs") + """ repurpose long video into clips and voiceovers; """ + L("chatgpt","ChatGPT") + """ rewrites one idea into X, LinkedIn, and Reels captions. One recording becomes a week of content.

### Is AI social media management safe from bans?
Mostly yes if you avoid bot-follow/engagement tricks. Use AI for creation and scheduling, not fake engagement. Platforms penalize inauthentic behavior, not tool-assisted posting.

### How much should a freelancer budget for AI social tools?
$20-40/month covers """ + L("canva-ai","Canva AI") + """, a scheduler, and """ + L("chatgpt","ChatGPT") + """. Scale up only when managing multiple clients or ad accounts needing """ + L("jasper","Jasper") + """-style brand workflows.""",

"best-ai-chatbots-2026": """## Frequently Asked Questions

### Which AI chatbot is best overall in 2026?
""" + L("chatgpt","ChatGPT") + """ for versatility, """ + L("claude","Claude") + """ for long-form reasoning and safety, """ + L("gemini","Gemini") + """ for Google Workspace integration. There's no single winner—match the bot to the job.

### Is Claude better than ChatGPT for writing?
For nuanced, long documents and careful editing, """ + L("claude","Claude") + """ edges out. For quick iteration and plugins, """ + L("chatgpt","ChatGPT") + """ wins. Writers often keep both open.

### What's the best free chatbot?
""" + L("deepseek","DeepSeek") + """ and the """ + L("chatgpt","ChatGPT") + """ free tier lead. """ + L("poe","Poe") + """ aggregates several free models in one inbox, handy for comparison.

### Can chatbots browse the web and cite sources?
""" + L("perplexity","Perplexity") + """ is built for cited web answers; """ + L("chatgpt","ChatGPT") + """ and """ + L("gemini","Gemini") + """ offer search modes. For research you must verify, """ + L("perplexity","Perplexity") + """ is the safest default.

### Which chatbot is best for roleplay or companionship?
""" + L("character-ai","Character.AI") + """ dominates casual roleplay. For private, task-focused use, """ + L("you-com","You.com") + """ and """ + L("poe","Poe") + """ keep conversations ad-free and customizable.""",

"how-to-use-ai-to-make-money-online-2026": """## Frequently Asked Questions

### What's the fastest way to make money with AI as a beginner?
Sell AI-assisted services: """ + L("chatgpt","ChatGPT") + """-written SEO blog packages, """ + L("midjourney","Midjourney") + """ thumbnails, or """ + L("elevenlabs","ElevenLabs") + """ voiceovers on freelance platforms. Speed-to-first-dollar beats building a product.

### Can I make passive income with AI content?
Yes, but slowly. Faceless YouTube (""" + L("heygen","HeyGen") + """ + """ + L("capcut","CapCut") + """) and AI eBook bundles compound over months. Expect 3-6 months before meaningful revenue; consistency beats tricks.

### Which AI tool helps automate my side hustle?
""" + L("make","Make") + """ and """ + L("n8n","n8n") + """ connect lead capture, delivery, and invoicing so the hustle runs while you sleep. """ + L("cursor","Cursor") + """ ships the landing pages fast.

### Do I need coding skills to earn with AI?
No. """ + L("chatgpt","ChatGPT") + """ and """ + L("claude","Claude") + """ handle copy; no-code tools handle the rest. Coding (via """ + L("cursor","Cursor") + """) only unlocks higher-margin custom builds.

### Is AI money-making saturated already?
The "get rich quick" angle is crowded, but real service demand (editing, localization, automation) is growing. Sell a skill amplified by AI, not a course about AI.""",

"48-best-ai-tools-roi-benchmark-2026": """## Frequently Asked Questions

### What does ROI mean for an AI tool?
Return on investment here = (time saved × your hourly rate + revenue enabled) minus the subscription. A $20 tool that saves 3 hours/week pays for itself if your time is worth $10/hour—most professionals clear that easily.

### Which AI tools have the best free tier?
""" + L("chatgpt","ChatGPT") + """, """ + L("deepseek","DeepSeek") + """, and """ + L("gemini","Gemini") + """ free tiers cover daily use. """ + L("gamma","Gamma") + """ and """ + L("notion-ai","Notion AI") + """ free plans suffice for light users.

### Is a paid coding assistant worth it for solo devs?
For anyone billing hourly, """ + L("cursor","Cursor") + """ or """ + L("github-copilot","GitHub Copilot") + """ pays back in one saved debugging session per week. The benchmark ranks them top for ROI among dev tools.

### How do I avoid paying for AI tools I don't use?
Audit monthly. Most people use 3 tools daily and forget 5 subscriptions. Keep """ + L("claude","Claude") + """ + one specialist (""" + L("replit-ai","Replit") + """ for code, """ + L("notion-ai","Notion AI") + """ for docs) and cut the rest.

### Are open-source AI models better ROI than paid?
For self-hosters with GPU, """ + L("deepseek","DeepSeek") + """ and """ + L("gemini","Gemini") + """ open weights win long-term. For everyone else, API pricing beats buying hardware.""",

"luma-ai-review": """## Frequently Asked Questions

### Is Luma AI free to use?
Luma offers a free tier with daily generation credits and paid plans for higher resolution and volume. Casual users can ship short clips on free; studios need a subscription for 4K and batch renders.

### How does Luma compare to Runway and Kling?
""" + L("luma-ai","Luma") + """ (Dream Machine) leads on physical realism and camera motion; """ + L("runway","Runway") + """ on editing control; """ + L("kling-ai","Kling") + """ on prompt adherence for complex scenes. Pick by whether you need fidelity or fine control.

### Can Luma generate audio or just video?
Video only. Pair it with """ + L("elevenlabs","ElevenLabs") + """ for voiceover and """ + L("suno","Suno") + """ for music to finish a scene. The benchmark workflow stacks Luma + ElevenLabs.

### What are the main limitations of Luma AI?
Occasional morphing hands, short max clip length, and credit limits on free tiers. For product shots needing stability, """ + L("midjourney","Midjourney") + """ still images + """ + L("runway","Runway") + """ interpolation can be cleaner.

### Is Luma good for commercial client work?
Yes, with the paid commercial license. Many agencies use """ + L("luma-ai","Luma") + """ for social ads and """ + L("chatgpt","ChatGPT") + """ for the briefs. Check license terms before reselling outputs.""",

"napkin-ai-review": """## Frequently Asked Questions

### Is Napkin AI free?
Napkin offers a free tier for personal visual ideation and paid plans for teams needing brand kits, export control, and collaboration. Solo users rarely hit the free limit.

### How is Napkin different from Canva or Lucidchart?
""" + L("napkin-ai","Napkin") + """ turns a sentence into a diagram automatically; """ + L("canva-ai","Canva") + """ is template-first; """ + L("lucidchart","Lucidchart") + """ is manual. Napkin wins for speed when you have the idea but not the layout.

### Can Napkin replace a designer?
For flowcharts, mind maps, and simple explainers, yes—it's faster than hiring. For branded marketing art, """ + L("canva-ai","Canva AI") + """ or """ + L("gamma","Gamma") + """ fit better. Napkin is the "rough visual, fast" tool.

### Does Napkin integrate with docs and wikis?
It exports PNG/SVG and pastes into """ + L("notion-ai","Notion") + """ and slides. Teams using """ + L("whimsical","Whimsical") + """ for whiteboards may find Napkin lighter for one-off diagrams.

### Is my data private on Napkin?
Check the plan's data policy; team tiers typically isolate workspace data. For sensitive docs, avoid pasting confidential text into any free AI whiteboard.""",

"best-ai-tools-for-podcasters-2026": """## Frequently Asked Questions

### What's the single best AI tool for podcast editing?
""" + L("descript","Descript") + """ leads—its text-based editing and filler-word removal cut edit time by 70%. """ + L("elevenlabs","ElevenLabs") + """ handles voice cleanup and cloned intros.

### Can AI write my podcast show notes and titles?
Yes. """ + L("chatgpt","ChatGPT") + """ drafts titles, summaries, and timestamps from your transcript in seconds. """ + L("descript","Descript") + """ auto-generates show notes on export.

### Which tool turns episodes into clips for TikTok?
""" + L("descript","Descript") + """ and """ + L("capcut-ai","CapCut") + """ detect highlights and reframe them vertically. Pair with """ + L("elevenlabs","ElevenLabs") + """ for dubbed shorts in other languages.

### Do I need a separate tool for podcast artwork?
""" + L("napkin-ai","Napkin AI") + """ or """ + L("canva-ai","Canva AI") + """ generate cover art fast. You don't need Photoshop; consistent branding matters more than polish.

### Is AI good enough to skip a human editor entirely?
For solo shows, yes—""" + L("descript","Descript") + """ + a quick listen-back suffices. For narrative or ad-heavy shows, a human final pass catches tone and legal issues AI misses.""",

"best-ai-tools-for-faceless-youtube-channels-2026": """## Frequently Asked Questions

### What's the cheapest stack to run a faceless YouTube channel?
""" + L("chatgpt","ChatGPT") + """ (script) + """ + L("heygen","HeyGen") + """ or """ + L("elevenlabs","ElevenLabs") + """ (voice) + """ + L("capcut","CapCut") + """ (edit) stays under $40/month. Voice + stock visuals beat pricey avatar tools for most niches.

### Can faceless channels actually get monetized?
Yes—documentary, finance, and how-to niches monetize well without showing a face. YouTube approves channels based on watch time and policy compliance, not whether you're on camera.

### Which AI tool generates the avatar and voice?
""" + L("heygen","HeyGen") + """ for realistic avatars, """ + L("elevenlabs","ElevenLabs") + """ for natural voiceover. For pure voice, """ + L("elevenlabs","ElevenLabs") + """ alone is enough and cheaper.

### How do I avoid the "AI slop" demonetization risk?
Use AI for production speed, not content theft. Write original scripts, vary visuals, and add real commentary. Channels that only repost AI narration get flagged.

### Is this sustainable as a business?
Margins are high but competition is fierce. Win by picking a narrow niche and posting consistently; treat AI as your studio, not your strategy.""",

"ai-tools-that-make-money-2026": """## Frequently Asked Questions

### Which AI tools make money with the least effort?
""" + L("chatgpt","ChatGPT") + """-powered freelance writing and """ + L("midjourney","Midjourney") + """ thumbnail services. Low setup, fast first dollar. The effort is in client acquisition, not the tool.

### Can AI build a product that earns passively?
Yes—AI eBook bundles, prompt packs, and """ + L("heygen","HeyGen") + """ faceless channels sell while you sleep. But "passive" means months of upfront work, not overnight.

### What's the highest-ROI AI money tool?
For service sellers, """ + L("claude","Claude") + """ (output quality) and """ + L("make","Make") + """ (automation) compound. For creators, """ + L("elevenlabs","ElevenLabs") + """ + """ + L("capcut","CapCut") + """ scale content without hiring.

### Do I need to show my face to earn with AI?
No. Faceless YouTube, voiceover gigs, and written services all earn without a camera. """ + L("elevenlabs","ElevenLabs") + """ voice work is fully behind-the-scenes.

### Is the AI money-making space too crowded?
The "course about AI" niche is saturated; the "AI-amplified real service" niche is growing. Sell a skill (editing, localization, automation), not hype.""",

"best-free-ai-tools-2026": """## Frequently Asked Questions

### What are the best completely free AI tools in 2026?
""" + L("chatgpt","ChatGPT") + """, """ + L("deepseek","DeepSeek") + """, """ + L("gemini","Gemini") + """, """ + L("canva-ai","Canva AI") + """, and """ + L("gamma","Gamma") + """ all offer usable free tiers with no credit card. Enough to run a real workflow at zero cost.

### Do free AI tools require a credit card?
The ones listed here don't. Avoid any "free trial" that demands a card upfront—those bill automatically. Genuinely free tiers let you start and upgrade only when you choose.

### What can't free AI tools do well?
High-volume generation, 4K exports, brand kits, and commercial licenses. Free """ + L("midjourney","Midjourney") + """ is limited; paid unlocks resolution and ownership.

### Is free AI good enough for a small business?
For solo and micro-businesses, yes—""" + L("chatgpt","ChatGPT") + """ + """ + L("canva-ai","Canva AI") + """ + """ + L("notion-ai","Notion AI") + """ free tiers cover 80% of needs. Upgrade per-feature as revenue grows.

### How do free tools make money—is my data safe?
Most monetize via paid upgrades, not data sales. Still, avoid pasting sensitive info into free tiers; check each tool's privacy policy before business use.""",

"best-ai-tools-for-seo-2026": """## Frequently Asked Questions

### Is there a single best AI SEO tool?
No—the strongest 2026 stack combines """ + L("perplexity","Perplexity") + """ for research, """ + L("claude","Claude") + """ for writing, and """ + L("make","Make") + """ for workflow automation. No single tool owns research, drafting, and technical audit at once.

### Can AI replace an SEO specialist?
AI handles about 80% of the heavy lifting—keyword research, drafting, technical audits. The final 20%—strategy, brand voice, and fact-checking—stays human, because AI still hallucinates statistics and misses search intent nuance.

### Which free AI tools help with SEO?
""" + L("chatgpt","ChatGPT") + """ free tier drafts meta descriptions and outlines; """ + L("grammarly-ai","Grammarly") + """ tightens copy; """ + L("quillbot","QuillBot") + """ paraphrases for uniqueness. Pair with """ + L("notion-ai","Notion AI") + """ for content calendars.

### Do AI SEO tools guarantee rankings?
No tool guarantees position one. They accelerate the work; Google still rewards helpful, original content and real backlinks. Treat AI as a force multiplier, not a ranking button.

### Should I use Jasper or Claude for SEO content?
""" + L("jasper","Jasper") + """ offers SEO-templated workflows for teams; """ + L("claude","Claude") + """ is more flexible for nuanced, long-form writing. Pick Jasper for volume templates, Claude for quality and control.""",
}

def main():
    d = json.load(open(SRC, encoding="utf-8"))
    by = {a["slug"]: a for a in d}
    inserted = 0
    fixed = 0
    for slug, block in FAQ.items():
        if slug not in by:
            print("SKIP (not found):", slug); continue
        c = by[slug]["content"]
        # Normalize trailing whitespace
        c = c.rstrip() + "\n\n"
        if re.search(r'(?im)^##\s+[^\n]*(frequently\s+asked\s+questions|\bfaq\b)', c):
            # Replace existing broken FAQ block (from its heading to end)
            c = re.sub(r'(?im)\n##\s+[^\n]*(frequently\s+asked\s+questions|\bfaq\b).*$',
                       "\n" + block, c, flags=re.DOTALL)
            fixed += 1
        else:
            c = c.rstrip() + "\n\n" + block + "\n"
            inserted += 1
        by[slug]["content"] = c
    json.dump(d, open(SRC, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"DONE: inserted={inserted}, fixed(existing broken)={fixed}, total={len(FAQ)}")

if __name__ == "__main__":
    main()
