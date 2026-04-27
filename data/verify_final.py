
import json
import re

file_path = r'C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data\tools_en.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

slugs = ['openai-codex', 'n8n', 'coze']
for tool in data:
    if tool['slug'] in slugs:
        content = tool['content']
        words = re.findall(r'\b\w+\b', content)
        print(f"{tool['name']} content word count: {len(words)}")
