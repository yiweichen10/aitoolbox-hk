"""Fix Article #98 v2: restore lost long-tail, final trim"""
import json

ARTICLES_PATH = 'data/articles_en.json'
with open(ARTICLES_PATH, 'r', encoding='utf-8') as f:
    articles = json.load(f)

for a in articles:
    if a['slug'] == 'best-ai-image-generation-tools-2026-midjourney-vs-dalle-vs-stable-diffusion-vs-firefly':
        art = a
        break

content = art['content']
print(f"Before: {len(content.split())} words")

# 1. Inject "AI image generation pricing" — put it in the economics intro
old1 = ("Here's the per-image cost across platforms at three usage volumes, assuming "
        "standard-quality output suitable for web and social media.")
new1 = ("Here's the per-image cost across platforms at three usage volumes — the **AI image generation pricing** "
        "reality for anyone comparing these tools head-to-head, assuming standard-quality output suitable for web and social media.")
content = content.replace(old1, new1, 1)

# 2. Trim word count: remove verbose phrases
trims = [
    # Trim DALL-E pricing paragraph
    (". OpenAI's API documentation, rate limiting, and billing are production-grade in a way that self-hosted Stable Diffusion rarely achieves without dedicated DevOps investment.",
     ". OpenAI's API documentation and billing are production-grade; self-hosted Stable Diffusion rarely matches this without DevOps investment."),
    # Trim Midjourney pricing
    ("on average. The midjourney vs dalle pricing comparison reveals that Midjourney is subscription-only — no pay-per-image option for light users.",
     "on average. Midjourney is subscription-only — no pay-per-image option for light users."),
    # Trim FAQ answer
    ("Stable Diffusion via Replicate or RunPod offers more model choices, custom fine-tuning, and lower per-image costs at volume — but requires understanding of model selection, scheduler configuration, and prompt syntax.",
     "Stable Diffusion via Replicate or RunPod offers more model choices and lower per-image costs at volume, but requires model selection and prompt syntax knowledge."),
]

for old, new in trims:
    content = content.replace(old, new, 1)

art['content'] = content

with open(ARTICLES_PATH, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

word_count = len(content.split())
print(f"After: {word_count} words")

pk = "AI image generation tools 2026"
print(f"Primary keyword '{pk}': {content.count(pk)}x")

long_tail = [
    'midjourney vs dalle',
    'stable diffusion vs midjourney',
    'AI art generator 2026',
    'best AI image creator',
    'AI image generation pricing',
    'AI image generator for business',
    'text to image AI tools',
    'midjourney alternatives',
    'free AI image generator',
    'AI image generation API',
]
all_ok = True
for kw in long_tail:
    count = content.count(kw)
    status = "✅" if count > 0 else "❌ MISSING"
    if count == 0:
        all_ok = False
    print(f"  {status} '{kw}': {count}x")

banned = ['leverage', 'utilize', 'seamlessly', 'game-changing', 'empower', 'streamline',
          'delve into', 'transformative', 'comprehensive', 'revolutionize', 'cutting-edge',
          'as an AI', 'in conclusion']
content_lower = content.lower()
for word in banned:
    if word in content_lower:
        print(f"BANNED: '{word}'")
        all_ok = False

print()
print("ALL CHECKS PASSED!" if all_ok else "SOME CHECKS FAILED!")
