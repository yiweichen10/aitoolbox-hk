import json
import re

forbidden_words = [
    "leverage", "utilize", "seamlessly", "game-changing", "empower", 
    "streamline", "delve into", "dive into", "transformative", 
    "comprehensive", "revolutionize", "cutting-edge", "as an AI", "in conclusion"
]

def check_content(text):
    found_forbidden = [w for w in forbidden_words if w.lower() in text.lower()]
    return found_forbidden

with open(r'C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data\tools_en.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    if item['slug'] in ['opus-clip', 'descript', 'capcut-ai']:
        content = item['content']
        forbidden = check_content(content)
        if forbidden:
            print(f"Slug: {item['slug']} - Found: {forbidden}")
        else:
            print(f"Slug: {item['slug']} - Clean")
