import json
import re

forbidden_words = [
    "leverage", "utilize", "seamlessly", "game-changing", "empower", 
    "streamline", "delve into", "dive into", "transformative", 
    "comprehensive", "revolutionize", "cutting-edge", "as an AI", "in conclusion"
]

def check_content(text):
    words = re.findall(r'\w+', text)
    word_count = len(words)
    found_forbidden = [w for w in forbidden_words if w.lower() in text.lower()]
    return word_count, found_forbidden

with open(r'C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data\draft_reviews.md', 'r', encoding='utf-8') as f:
    content = f.read()

parts = content.split('---')
for i, part in enumerate(parts):
    count, forbidden = check_content(part)
    print(f"Part {i+1} Word Count: {count}")
    print(f"Part {i+1} Forbidden Words: {forbidden}")
