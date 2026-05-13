import json
import os

article_path = r'C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data\article_draft.md'
json_path = r'C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data\articles_en.json'

with open(article_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_article = {
    "title": "Top-Rated AI Video Generators 2026: The Ultimate Guide for Creators",
    "slug": "best-ai-video-generators-2026",
    "date": "2026-05-13",
    "dateFull": "May 13, 2026",
    "category": "AI Video",
    "description": "The definitive guide to the best AI video generators in 2026. We compare Runway, HeyGen, Luma Dream Machine, and Kling AI on physics, speed, and ROI to help you choose the right tool for your content stack.",
    "keywords": "best AI video generators, AI video generator comparison, text to video AI 2026, free AI video generator no watermark, HeyGen vs Runway, AI video generators for YouTube",
    "lang": "en",
    "type": "E",
    "content": content
}

with open(json_path, 'r', encoding='utf-8') as f:
    articles = json.load(f)

articles.append(new_article)

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(articles, f, indent=2, ensure_ascii=False)

print("Successfully added new article to articles_en.json")
