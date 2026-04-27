import json
import re
import os

def check_forbidden(text):
    forbidden = ["leverage", "utilize", "seamlessly", "game-changing", "empower", "streamline", "delve into", "dive into", "transformative", "comprehensive", "revolutionize", "cutting-edge", "as an AI", "in conclusion"]
    found = []
    for word in forbidden:
        if re.search(r'\b' + re.escape(word) + r'\b', text, re.IGNORECASE):
            found.append(word)
    return found

def count_words(text):
    clean_text = re.sub(r'#+\s+', '', text)
    clean_text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1', clean_text)
    return len(clean_text.split())

def trim_to_limit(text, limit=1600):
    words = text.split()
    if len(words) <= limit:
        return text
    # Very crude trimming: remove last few sentences of the longer sections
    # Or just return the first limit words and hope for the best (not ideal for markdown)
    # Let's just manually trim in the text files instead of a script to keep structure.
    return text

base_path = r'C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data'
json_path = os.path.join(base_path, 'tools_en.json')

# I will manually edit the content strings here to ensure they are within limit
with open(os.path.join(base_path, 'comet_content.txt'), 'r', encoding='utf-8') as f:
    comet_content = f.read().strip()
with open(os.path.join(base_path, 'pixverse_content.txt'), 'r', encoding='utf-8') as f:
    pixverse_content = f.read().strip()
with open(os.path.join(base_path, 'fliki_content.txt'), 'r', encoding='utf-8') as f:
    fliki_content = f.read().strip()

# Trimming function: remove some sentences from the middle sections
def manual_trim(text, target=1550):
    words = text.split()
    while len(words) > 1580:
        paras = text.split('\n\n')
        # Target the middle paragraphs to remove the last sentence
        for i in range(2, len(paras)-1):
            sentences = re.split(r'(?<=[.!?]) +', paras[i])
            if len(sentences) > 2:
                paras[i] = " ".join(sentences[:-1])
                text = "\n\n".join(paras)
                words = text.split()
                if len(words) <= 1580: break
        if len(words) > 1580: # If still too long, break first paras
             paras = text.split('\n\n')
             paras[1] = " ".join(re.split(r'(?<=[.!?]) +', paras[1])[:-1])
             text = "\n\n".join(paras)
             words = text.split()
    return text

comet_content = manual_trim(comet_content, 1600)
pixverse_content = manual_trim(pixverse_content, 1600)
fliki_content = manual_trim(fliki_content, 1600)

print(f"Comet after trim: {count_words(comet_content)}")
print(f"PixVerse after trim: {count_words(pixverse_content)}")
print(f"Fliki after trim: {count_words(fliki_content)}")

# Final data update
with open(json_path, 'r', encoding='utf-8') as f:
    tools = json.load(f)

articles = {'comet': comet_content, 'pixverse': pixverse_content, 'fliki': fliki_content}

# ... (rest of tool definitions as before)
new_tools = [
    {
        "name": "Comet",
        "slug": "comet",
        "emoji": "☄️",
        "color": "#6366f1",
        "description": "Comet is an AI-powered task manager that uses natural language processing to organize your day. It prioritizes tasks based on deadlines and importance, integrating with your calendar to suggest the best times for deep work.",
        "category": "AI Office",
        "tags": [{"text": "Productivity"}, {"text": "Task Management"}, {"text": "Free tier", "type": "free"}],
        "rating": "⭐ 4.7", "visits": "12K", "url": "https://withcomet.com", "price": "Free | Pro $15/mo | Team custom", "platform": "Web / macOS / iOS", "published": True,
        "pros": ["AI task prioritization", "Natural language task creation", "Calendar integration", "Smart scheduling suggestions"],
        "cons": ["Newer tool smaller user base", "Limited integrations vs Notion", "Learning curve for daily workflow"],
        "features": ["Natural language task entry", "AI-driven prioritization", "Calendar sync", "Smart Focus Blocks", "Automated rescheduling"],
        "faq": [
            {"question": "Is Comet AI free?", "answer": "Yes, Comet offers a free tier that includes basic task creation and calendar integration. The Pro plan at $15/month unlocks advanced AI scheduling and priority support."},
            {"question": "What is Comet AI used for?", "answer": "Comet is a task management and scheduling tool that uses AI to organize your to-do list based on deadlines and calendar availability."},
            {"question": "Is Comet better than Notion AI?", "answer": "Comet is more specialized for task scheduling and calendar management, while Notion AI is better for document writing and knowledge management."},
            {"question": "How does Comet AI work?", "answer": "Comet connects to your calendar and uses natural language processing to understand tasks, then automatically fits them into your schedule based on priority."}
        ],
        "content": articles['comet']
    },
    {
        "name": "PixVerse",
        "slug": "pixverse",
        "emoji": "🎬",
        "color": "#ec4899",
        "description": "PixVerse is a high-performance AI video generation platform that supports text-to-video and image-to-video. It specializes in character consistency and 1080p output, making it a strong competitor for cinematic content.",
        "category": "AI Video",
        "tags": [{"text": "AI Video"}, {"text": "Content Creation"}, {"text": "Free tier", "type": "free"}],
        "rating": "⭐ 4.8", "visits": "85K", "url": "https://pixverse.ai", "price": "Free (80 credits/day) | Standard $22.99/mo | Pro $76.99/mo", "platform": "Web / Discord", "published": True,
        "pros": ["Text-to-video and image-to-video", "Character consistency", "1080p video output", "Fast generation"],
        "cons": ["Credits drain fast", "Limited to 8-second clips free", "Watermark on free outputs"],
        "features": ["Text-to-Video generation", "Image-to-Video animation", "Character Consistency models", "1080p HD export", "Multi-motion control"],
        "faq": [
            {"question": "Is PixVerse free to use?", "answer": "Yes, PixVerse offers a free tier with 80 credits per day, allowing for several video generations daily with watermarks."},
            {"question": "Is PixVerse better than Sora?", "answer": "PixVerse is currently available and produces high-quality 1080p video, whereas Sora is in limited beta and not yet public."},
            {"question": "What is PixVerse used for?", "answer": "PixVerse is used to create cinematic AI videos from text or images, ideal for social media, marketing, and storytelling."},
            {"question": "How good is PixVerse AI?", "answer": "It is widely considered one of the top tools for character consistency and visual fidelity in the AI video space."}
        ],
        "content": articles['pixverse']
    },
    {
        "name": "Fliki",
        "slug": "fliki",
        "emoji": "🎙️",
        "color": "#ef4444",
        "description": "Fliki turns text into videos with AI voices. With over 2000 voices and 75 languages, it's a go-to tool for creating social media content, podcasts, and localized videos with built-in stock media.",
        "category": "AI Video",
        "tags": [{"text": "AI Video"}, {"text": "Text-to-Speech"}, {"text": "Free tier", "type": "free"}],
        "rating": "⭐ 4.6", "visits": "110K", "url": "https://fliki.ai", "price": "Free (5 min/mo) | Standard $21/mo | Premium $66/mo", "platform": "Web", "published": True,
        "pros": ["Text-to-video with AI voiceover", "2000+ voices in 75+ languages", "Stock media built-in", "Podcast-to-video"],
        "cons": ["Free only 5 min/month", "Avatars less realistic than HeyGen", "Occasional sync issues"],
        "features": ["Text-to-Video workflow", "AI Voiceover", "Podcast to Video", "Stock Media library", "Auto-summarization"],
        "faq": [
            {"question": "Is Fliki worth it?", "answer": "For content creators needing high volume, the time saved in voiceover and stock selection makes it highly valuable."},
            {"question": "Is Fliki AI free?", "answer": "Fliki has a free tier with 5 minutes of credits per month and watermarks on exported videos."},
            {"question": "What is Fliki best for?", "answer": "Fliki is best for rapid creation of social media videos, explainer content, and repurposing blog posts into video."},
            {"question": "Is Fliki better than HeyGen?", "answer": "Fliki is better for general video production with stock media, while HeyGen specializes in realistic AI talking avatars."}
        ],
        "content": articles['fliki']
    }
]

# Check forbidden and slugs
for tool in new_tools:
    f = check_forbidden(tool['content'])
    if f: print(f"Forbidden in {tool['name']}: {f}")
    
    slugs = [t['slug'] for t in tools]
    if tool['slug'] in slugs:
        for i, t in enumerate(tools):
            if t['slug'] == tool['slug']: tools[i] = tool
    else:
        tools.append(tool)

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(tools, f, ensure_ascii=False, indent=2)

print("Update completed.")
