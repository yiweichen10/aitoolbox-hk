
import json
import re

forbidden_words = [
    "leverage", "utilize", "seamlessly", "game-changing", "empower", 
    "streamline", "delve into", "dive into", "transformative", 
    "comprehensive", "revolutionize", "cutting-edge", "as an AI", "in conclusion"
]

file_path = r'C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data\tools_en.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

slugs = ['openai-codex', 'n8n', 'coze']
for tool in data:
    if tool['slug'] in slugs:
        text = tool['content']
        for fw in forbidden_words:
            if fw.lower() in text.lower():
                print(f"FORBIDDEN: '{fw}' found in {tool['name']}")
print("Done.")
