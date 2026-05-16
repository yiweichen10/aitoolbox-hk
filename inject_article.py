import json
import os

article_path = r"C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\article_draft.md"
json_path = r"C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data\articles_en.json"

with open(article_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

title = lines[0].strip('# ').strip()
content = "".join(lines[2:]) # Skip title and empty line

new_article = {
    "title": title,
    "slug": "best-ai-coding-assistants-2026",
    "date": "2026-05-16",
    "dateFull": "May 16, 2026",
    "category": "AI Coding",
    "description": "Best AI Coding Assistants 2026: We compare Cursor, Windsurf, and GitHub Copilot on speed, context, and developer ROI. Discover which AI coding tool actually ships code.",
    "keywords": "Best AI Coding Assistants 2026, Cursor AI vs Windsurf, best AI for coding python 2026, AI coding agents review, GitHub Copilot alternative 2026, vibe coding tools",
    "lang": "en",
    "type": "E",
    "content": content.strip()
}

with open(json_path, 'r', encoding='utf-8') as f:
    articles = json.load(f)

# Check if slug already exists to prevent duplicates
if any(a['slug'] == new_article['slug'] for a in articles):
    print(f"Article with slug {new_article['slug']} already exists. Updating it.")
    for i, a in enumerate(articles):
        if a['slug'] == new_article['slug']:
            articles[i] = new_article
            break
else:
    articles.append(new_article)

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(articles, f, indent=2, ensure_ascii=False)

print("Successfully appended the article.")
