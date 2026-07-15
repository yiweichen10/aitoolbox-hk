"""Fix Article #98 v3: final fixes"""
import json

with open('data/articles_en.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

for a in articles:
    if a['slug'] == 'best-ai-image-generation-tools-2026-midjourney-vs-dalle-vs-stable-diffusion-vs-firefly':
        art = a
        break

content = art['content']

# 1. Restore primary keyword
old1 = ("The tools are good enough that choosing wrong isn't catastrophic "
        "\u2014 but it is expensive in time.")
new1 = ("The **AI image generation tools 2026** market has matured enough "
        "that choosing wrong isn't catastrophic \u2014 but it is expensive in time.")
content = content.replace(old1, new1, 1)
print("Restore PK:", "OK" if old1 in art['content'] or new1 in content else "NOT FOUND")

# 2. Trim integration section header
old2 = ("The integration cost nobody talks about. "
        "The **text to image AI tools** comparison rarely accounts for workflow integration cost.")
new2 = ("The **text to image AI tools** comparison rarely accounts for workflow integration cost.")
if old2 in content:
    content = content.replace(old2, new2, 1)
    print("Trim 1: OK")
else:
    print(f"Trim 1: NOT FOUND. Looking for partial...")
    # Try finding just the first part
    if "integration cost nobody talks about" in content:
        print("  Found integration cost text")
    if "text to image AI tools" in content:
        print("  Found text to image AI tools")

# 3. Trim setup section
old3 = ("Setup is a barrier. Getting Automatic1111 or ComfyUI running with CUDA "
        "support, appropriate model weights, and VAE configurations is not a "
        "Saturday afternoon project for non-technical users.")
new3 = ("Getting Automatic1111 or ComfyUI running with CUDA support and "
        "appropriate model weights is not a Saturday afternoon project.")
if old3 in content:
    content = content.replace(old3, new3, 1)
    print("Trim 2: OK")
else:
    print("Trim 2: NOT FOUND")

# 4. Trim opening stat sentence
old4 = ("The global stock photography market hit $5.2 billion in 2025, yet "
        "68% of marketing teams now generate custom visuals in-house using AI "
        "\u2014 at 3% of the traditional cost per image, according to a 2026 "
        "Venngage visual content survey.")
new4 = ("The global stock photography market hit $5.2 billion in 2025, yet "
        "68% of marketing teams now generate custom visuals in-house using AI "
        "at 3% of the traditional cost per image, per Venngage's 2026 visual "
        "content survey.")
if old4 in content:
    content = content.replace(old4, new4, 1)
    print("Trim 3: OK")
else:
    print("Trim 3: NOT FOUND")

art['content'] = content

with open('data/articles_en.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

wc = len(content.split())
print(f'\nWord count: {wc}')
pk = 'AI image generation tools 2026'
print(f'Primary keyword \'{pk}\': {content.count(pk)}x')

lts = ['midjourney vs dalle', 'stable diffusion vs midjourney', 'AI art generator 2026',
       'best AI image creator', 'AI image generation pricing', 'AI image generator for business',
       'text to image AI tools', 'midjourney alternatives', 'free AI image generator',
       'AI image generation API']
all_ok = True
for kw in lts:
    c = content.count(kw)
    s = "OK" if c > 0 else "MISSING!"
    if c == 0:
        all_ok = False
    print(f'  {s}: {kw} = {c}x')

banned = ['leverage', 'utilize', 'seamlessly', 'game-changing', 'empower', 'streamline',
          'delve into', 'transformative', 'comprehensive', 'revolutionize', 'cutting-edge',
          'as an AI', 'in conclusion']
cl = content.lower()
for w in banned:
    if w in cl:
        print(f'BANNED: {w}')
        all_ok = False

print(f'\n{"ALL CHECKS PASSED!" if all_ok else "ISSUES REMAIN!"}')
