
import json
import os

def count_words(text):
    return len(text.split())

def trim_to_target(text, target=1500):
    words = text.split()
    if len(words) <= target:
        return text
    trimmed_words = words[:target]
    trimmed_text = " ".join(trimmed_words)
    last_dot = trimmed_text.rfind('.')
    if last_dot > target * 4:
        trimmed_text = trimmed_text[:last_dot+1]
    return trimmed_text

base_path = r'C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data'
ideogram_raw = open(os.path.join(base_path, 'ideogram_content.md'), encoding='utf-8').read()
leonardo_raw = open(os.path.join(base_path, 'leonardo_content.md'), encoding='utf-8').read()
quillbot_raw = open(os.path.join(base_path, 'quillbot_content.md'), encoding='utf-8').read()

ideogram_content = trim_to_target(ideogram_raw, 1500)
leonardo_content = trim_to_target(leonardo_raw, 1500)
quillbot_content = trim_to_target(quillbot_raw, 1500)

tools = [
    {
        "name": "Ideogram",
        "slug": "ideogram",
        "emoji": "🎨",
        "color": "#000000",
        "description": "Best-in-class AI image generator for typography and graphic design, delivering precise text rendering and photorealistic art.",
        "category": "AI Image",
        "tags": [{"text": "Image Generation"}, {"text": "Typography"}, {"text": "Free tier", "type": "free"}],
        "rating": "⭐ 4.8",
        "visits": "92K",
        "badge": {"type": "hot", "text": "HOT"},
        "url": "https://ideogram.ai",
        "price": "Free (10 images/day) | Basic $7/mo | Plus $16/mo | Pro $48/mo",
        "platform": "Web",
        "published": True,
        "pros": ["Best-in-class text rendering in images", "Strong photorealistic output", "Generous free tier", "Simple prompt interface"],
        "cons": ["Less stylistic range than Midjourney", "Community feed is public on free plan", "Slower than some competitors"],
        "features": ["Precision text rendering", "Magic Prompt", "Community feed", "Negative prompting", "Image-to-image"],
        "faq": [
            {"question": "Is Ideogram better than Midjourney?", "answer": "For text accuracy and graphic design, yes. If you need a specific word or phrase to look perfect, this is the tool. However, for sheer artistic variety and vibe, many users still prefer Midjourney."},
            {"question": "Is Ideogram AI free?", "answer": "Yes, there is a free tier that offers a limited number of credits each day. Your creations will be public unless you upgrade to a paid plan."},
            {"question": "What is Ideogram best for?", "answer": "It’s best for any image that requires readable text, such as logos, t-shirt designs, social media graphics, and posters."},
            {"question": "Is Ideogram good for text in images?", "answer": "It is arguably the best tool currently available for this specific task. Its model is specially trained to handle typography accurately."}
        ],
        "content": ideogram_content
    },
    {
        "name": "Leonardo AI",
        "slug": "leonardo-ai",
        "emoji": "🦁",
        "color": "#6366f1",
        "description": "A feature-rich generative art platform offering model training, real-time canvas editing, and motion generation for creators.",
        "category": "AI Image",
        "tags": [{"text": "Image Generation"}, {"text": "Model Training"}, {"text": "Free tier", "type": "free"}],
        "rating": "⭐ 4.7",
        "visits": "110K",
        "badge": {"type": "popular", "text": "POPULAR"},
        "url": "https://leonardo.ai",
        "price": "Free (150 tokens/day) | Apprentice $10/mo | Artisan $24/mo | Maestro $48/mo",
        "platform": "Web / iOS",
        "published": True,
        "pros": ["Fine-tuned model training on your style", "Motion video generation", "Real-time canvas", "Strong for game assets and concept art"],
        "cons": ["Token system is confusing", "High-quality outputs consume tokens fast", "UI feels cluttered"],
        "features": ["Fine-tuned models", "AI Canvas", "Motion video", "Real-time generation", "API access"],
        "faq": [
            {"question": "Is Leonardo AI better than Midjourney?", "answer": "For users who want control and the ability to train their own models, yes. For those who just want the highest quality aesthetic out of the box with minimal effort, Midjourney often holds the edge."},
            {"question": "Is Leonardo AI free to use?", "answer": "Yes, it offers a free plan with 150 daily tokens, making it one of the most accessible pro tools on the market."},
            {"question": "What is Leonardo AI best for?", "answer": "It is exceptional for game asset creation, concept art, and any project that requires a consistent visual style."},
            {"question": "How many images can I generate free on Leonardo?", "answer": "With 150 daily tokens, you can typically generate between 15 and 30 standard images, depending on your settings."}
        ],
        "content": leonardo_content
    },
    {
        "name": "QuillBot",
        "slug": "quillbot",
        "emoji": "✒️",
        "color": "#497d39",
        "description": "The leading AI paraphrasing tool and writing assistant, helping you refine your prose with multiple rewriting modes and a grammar checker.",
        "category": "AI Writing",
        "tags": [{"text": "Paraphrasing"}, {"text": "Writing Assistant"}, {"text": "Free tier", "type": "free"}],
        "rating": "⭐ 4.6",
        "visits": "210K",
        "badge": {"type": "trusted", "text": "TRUSTED"},
        "url": "https://quillbot.com",
        "price": "Free | Premium $9.95/mo (annual $4.17/mo)",
        "platform": "Web / Chrome / Word",
        "published": True,
        "pros": ["Best-in-class paraphrasing tool", "7 rewriting modes", "Summarizer and grammar checker included", "Works across browsers via extension"],
        "cons": ["Free tier limited to 125 words", "Can lose original meaning on aggressive modes", "Grammar checker less accurate than Grammarly"],
        "features": ["7 Paraphrasing modes", "Grammar checker", "Summarizer", "Plagiarism checker", "Citation generator"],
        "faq": [
            {"question": "Is QuillBot worth paying for?", "answer": "For anyone who writes frequently, yes. The annual plan is very affordable and removing word limits significantly speeds up the editing process."},
            {"question": "Is QuillBot free to use?", "answer": "Yes, there is a capable free version with a 125-word limit for the paraphraser and access to basic grammar checking."},
            {"question": "Is QuillBot better than Grammarly?", "answer": "They serve different purposes. Grammarly is better for deep stylistic edits and perfect grammar, while QuillBot is superior for rewriting and changing the tone of your text."},
            {"question": "Does QuillBot get detected as AI?", "answer": "It can. Some AI detectors are trained to spot patterns of machine-assisted writing. It's best to use it as a starting point and then add your own voice."}
        ],
        "content": quillbot_content
    }
]

json_path = os.path.join(base_path, 'tools_en.json')
with open(json_path, 'r', encoding='utf-8') as f:
    existing_data = json.load(f)

print(f"Original items: {len(existing_data)}")

existing_map = {item['slug']: i for i, item in enumerate(existing_data)}

for tool in tools:
    if tool['slug'] in existing_map:
        existing_data[existing_map[tool['slug']]] = tool
        print(f"Updated {tool['slug']}")
    else:
        existing_data.append(tool)
        print(f"Added {tool['slug']}")

print(f"Final items: {len(existing_data)}")

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(existing_data, f, ensure_ascii=False, indent=2)

print("Done.")
