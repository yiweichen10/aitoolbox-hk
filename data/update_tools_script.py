import json
import os
import re

def intelligent_trim(content, target_total=1500):
    # Remove banned words first
    banned_map = {
        r'leverage': 'use',
        r'utilize': 'use',
        r'seamlessly': 'easily',
        r'game-changing': 'innovative',
        r'empower': 'help',
        r'streamline': 'simplify',
        r'delve into': 'explore',
        r'dive into': 'examine',
        r'transformative': 'impressive',
        r'comprehensive': 'detailed',
        r'revolutionize': 'change',
        r'cutting-edge': 'modern',
        r'as an AI': '',
        r'in conclusion': ''
    }
    for pattern, replacement in banned_map.items():
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

    words = content.split()
    if len(words) <= target_total:
        return content

    # Find the split points
    # Intro: First 2 paragraphs (~150 words)
    # End: Everything from the Table/FAQ onwards
    
    faq_split = content.find("| Feature |")
    if faq_split == -1:
        faq_split = content.find("### FAQ")
    
    if faq_split == -1:
        # Fallback to simple word trim
        return ' '.join(words[:target_total])

    intro_end_idx = content.find("\n\n", content.find("\n\n") + 1)
    if intro_end_idx == -1:
        intro_end_idx = 500 # fallback char index
    
    intro_part = content[:intro_end_idx]
    end_part = content[faq_split:]
    
    intro_word_count = len(intro_part.split())
    end_word_count = len(end_part.split())
    
    middle_target = target_total - intro_word_count - end_word_count
    
    middle_part_raw = content[intro_end_idx:faq_split]
    middle_words = middle_part_raw.split()
    
    trimmed_middle = middle_words[:middle_target]
    middle_str = ' '.join(trimmed_middle)
    last_period = middle_str.rfind('.')
    if last_period > 0:
        middle_str = middle_str[:last_period+1]
        
    final_content = intro_part + "\n\n" + middle_str + "\n\n" + end_part
    final_content = re.sub(r' +', ' ', final_content)
    
    return final_content

tools_metadata = [
    {
        "name": "Dify",
        "slug": "dify",
        "emoji": "🛠️",
        "color": "#155EEF",
        "description": "Open-source LLM app development platform with visual orchestration and RAG pipeline support.",
        "category": "AI Dev",
        "tags": [{"text": "AI Dev"}, {"text": "Open Source"}, {"text": "No-code"}],
        "rating": "⭐ 4.8",
        "visits": "42K",
        "badge": {"type": "hot", "text": "HOT"},
        "url": "https://dify.ai",
        "price": "Free self-hosted | Sandbox free | Professional $59/mo | Team $159/mo",
        "platform": "Web / Docker",
        "published": True,
        "pros": ["Build LLM apps visually without coding", "RAG pipeline support", "Self-hostable open source", "30+ model integrations"],
        "cons": ["Complex setup for self-hosting", "Enterprise features expensive", "Steeper learning curve than no-code tools"],
        "features": ["Visual Workflow Designer", "Unified RAG Engine", "Model Orchestration", "Agentic Capabilities", "Open Source & Self-hostable"],
        "faq": [
            {"question": "Is Dify free to use?", "answer": "Yes, Dify offers a free self-hosted community version and a cloud-based Sandbox plan with some usage limits."},
            {"question": "What is Dify AI used for?", "answer": "Dify is used for building LLM apps like chatbots, internal knowledge bases, and AI agents with RAG capabilities."},
            {"question": "Is Dify better than n8n?", "answer": "Dify is more specialized for LLM orchestration and RAG, while n8n is better for general-purpose business automation."},
            {"question": "Can Dify be self-hosted?", "answer": "Yes, Dify is open-source and provides Docker images for easy self-hosting on your own infrastructure."}
        ]
    },
    {
        "name": "Zapier AI",
        "slug": "zapier-ai",
        "emoji": "⚡",
        "color": "#FF4F00",
        "description": "The leading automation platform now featuring AI to build workflows, process data, and create persistent AI agents.",
        "category": "Automation",
        "tags": [{"text": "Automation"}, {"text": "Productivity"}, {"text": "AI Agent"}],
        "rating": "⭐ 4.7",
        "visits": "95K",
        "badge": {"type": "pick", "text": "Editor's Pick"},
        "url": "https://zapier.com/ai",
        "price": "Free (100 tasks/mo) | Starter $19.99/mo | Professional $49/mo | Team $69/mo",
        "platform": "Web",
        "published": True,
        "pros": ["Easiest automation setup for non-developers", "6000+ app integrations", "AI to build workflows from plain English", "Reliable enterprise track record"],
        "cons": ["Gets expensive fast at scale", "Limited logic complexity vs n8n", "AI features still maturing"],
        "features": ["AI-Powered Workflow Builder", "Zapier Central AI Agents", "Natural Language App Connections", "6000+ App Ecosystem", "Enterprise-Grade Reliability"],
        "faq": [
            {"question": "Is Zapier AI worth it?", "answer": "For businesses needing quick, reliable integrations across 6000+ apps, the time savings usually justify the premium cost."},
            {"question": "Is Zapier AI better than n8n?", "answer": "Zapier is easier to use and has more integrations, but n8n is more powerful for complex logic and much cheaper at scale."},
            {"question": "What does Zapier AI do?", "answer": "It allows you to build automations using natural language, process data with AI, and create agents that work across your apps."},
            {"question": "Is Zapier AI free?", "answer": "Zapier offers a free tier with 100 tasks per month, but most advanced AI features require a paid subscription."}
        ]
    },
    {
        "name": "Veo",
        "slug": "veo",
        "emoji": "🎬",
        "color": "#4285F4",
        "description": "Google DeepMind's state-of-the-art AI video generator for cinematic, high-fidelity 1080p video production.",
        "category": "AI Video",
        "tags": [{"text": "AI Video"}, {"text": "Creative"}, {"text": "Google"}],
        "rating": "⭐ 4.9",
        "visits": "18K",
        "badge": {"type": "new", "text": "NEW"},
        "url": "https://deepmind.google/technologies/veo/",
        "price": "Limited access | Vertex AI pricing",
        "platform": "Web / Google Cloud",
        "published": True,
        "pros": ["Google DeepMind backing", "High realism video output", "Long video generation capability", "Strong physics understanding"],
        "cons": ["Very limited public access", "No self-serve pricing", "Requires Google Cloud setup for API"],
        "features": ["1080p 60fps Video Generation", "Cinematic Physics Understanding", "60+ Second Clips", "Character and Style Consistency", "Vertex AI Integration"],
        "faq": [
            {"question": "Is Veo better than Sora?", "answer": "Both are top-tier; Veo emphasizes physics and cinematic control, while Sora is known for hyper-realistic textures and variety."},
            {"question": "Is Google Veo free to use?", "answer": "Currently, access is limited to selected partners and not available as a free public tool."},
            {"question": "What is Google Veo used for?", "answer": "Veo is used for high-fidelity video generation in film, advertising, and creative production."},
            {"question": "How do I access Google Veo?", "answer": "You can join the waitlist on Google's VideoFX platform or access it via Vertex AI if you are an enterprise customer."}
        ]
    }
]

json_path = r'C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data\tools_en.json'
content_files = {
    "dify": r'C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data\dify_content.md',
    "zapier-ai": r'C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data\zapier_content.md',
    "veo": r'C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data\veo_content.md'
}

with open(json_path, 'r', encoding='utf-8') as f:
    existing_tools = json.load(f)

for tool in tools_metadata:
    with open(content_files[tool['slug']], 'r', encoding='utf-8') as f:
        raw_content = f.read()
    
    # We'll use 1500 as the target.
    final_content = intelligent_trim(raw_content, 1500)
    tool['content'] = final_content
    print(f"Tool: {tool['name']}, Final Word Count: {len(final_content.split())}")

# Merge
slug_to_index = {t['slug']: i for i, t in enumerate(existing_tools)}
for tool in tools_metadata:
    if tool['slug'] in slug_to_index:
        existing_tools[slug_to_index[tool['slug']]] = tool
    else:
        existing_tools.append(tool)

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(existing_tools, f, ensure_ascii=False, indent=2)

print("Successfully updated tools_en.json with intelligent trimming.")
