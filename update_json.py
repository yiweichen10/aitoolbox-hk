import json
import os

article_path = r"C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\article_draft.md"
json_path = r"C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data\articles_en.json"

with open(article_path, "r", encoding="utf-8") as f:
    content = f.read()

new_article = {
    "title": "Kling AI vs Sora vs Luma Dream Machine: The 2026 ROI Guide for Video Creators",
    "slug": "kling-ai-review-vs-sora-luma-2026",
    "date": "2026-05-14",
    "dateFull": "May 14, 2026",
    "category": "AI Video",
    "description": "Looking for an honest Kling AI Review? We compare Kling 3.0 vs Sora 2.0 vs Luma Dream Machine on ROI, features, and quality. Discover the best AI video generator for your production workflow in 2026.",
    "keywords": "Kling AI Review, Kling AI vs Sora vs Luma, Kling AI pricing guide 2026, Kling AI free credits, Kling AI video quality, best AI video generator for filmmakers",
    "content": content
}

if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = []

# Check if slug already exists to avoid duplicates
if any(a["slug"] == new_article["slug"] for a in data):
    print(f"Article with slug {new_article['slug']} already exists. Updating...")
    data = [new_article if a["slug"] == new_article["slug"] else a for a in data]
else:
    data.append(new_article)

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Successfully updated articles_en.json")
