import json
data = json.load(open(r'C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data\tools_en.json', encoding='utf-8'))
for slug in ['zapier-ai', 'veo']:
    tool = [t for t in data if t['slug'] == slug][0]
    content = tool['content']
    print(f"Slug: {slug}")
    print(f"Word count: {len(content.split())}")
    print(f"H2 count: {content.count('## ')}")
    print(f"Table: {'| Feature |' in content}")
    print(f"FAQ: {'### FAQ' in content}")
    print("-" * 20)
