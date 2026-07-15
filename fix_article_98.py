"""Fix Article #98: primary keyword +1, inject missing long-tail, trim words"""
import json

ARTICLES_PATH = 'data/articles_en.json'
with open(ARTICLES_PATH, 'r', encoding='utf-8') as f:
    articles = json.load(f)

# Find article #98
for a in articles:
    if a['slug'] == 'best-ai-image-generation-tools-2026-midjourney-vs-dalle-vs-stable-diffusion-vs-firefly':
        art = a
        break

content = art['content']
print(f"Before: {len(content.split())} words")

# 1. Inject primary keyword (+1 occurrence)
# Find a good spot in the body where it's natural
old1 = "market splits into four distinct lanes:"
new1 = "market — the leading **AI image generation tools 2026** — splits into four distinct lanes:"
content = content.replace(old1, new1, 1)

# 2. Inject "AI art generator 2026" into the DALL-E 3 section
old2 = "Where Midjourney is a creative tool, DALL-E 3 is an infrastructure component."
new2 = "Where Midjourney is a creative tool, DALL-E 3 is an infrastructure component — the **AI art generator 2026** choice for developers who need API-first image generation."
content = content.replace(old2, new2, 1)

# 3. Trim text: remove some verbose sentences
trims = [
    # Trim from "But there's a catch" paragraph
    ("At 5 minutes per iteration cycle, it costs 40-75 minutes of your time.", ""),
    # Trim from Midjourney section
    ("It requires typing `/imagine` in a chat channel. But ", "It requires typing `/imagine` in a chat channel — but "),
    # Trim from DALL-E pricing paragraph
    ("The AI image generation pricing landscape shifts at volume: at 1,000 images/month, DALL-E 3 costs $40-80 through the API versus $30-60 on Midjourney. At 10,000 images/month, DALL-E 3 becomes significantly more expensive unless you have negotiated enterprise pricing.",
     "At 1,000 images/month, DALL-E 3 costs $40-80 through the API versus $30-60 on Midjourney; at 10,000 images/month the gap widens without enterprise pricing."),
]

for old, new in trims:
    content = content.replace(old, new, 1)

art['content'] = content

with open(ARTICLES_PATH, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

# Verify
word_count = len(content.split())
print(f"After: {word_count} words")

pk = "AI image generation tools 2026"
print(f"Primary keyword '{pk}': {content.count(pk)}x")

# Check all long-tail
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

# Banned words
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
