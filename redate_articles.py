
import json
from datetime import datetime, timedelta

path = r'C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data\articles_en.json'

with open(path, 'r', encoding='utf-8') as f:
    articles = json.load(f)

# Sort articles by their current date if possible, otherwise just use order
# Since many have the same date, we'll rely on the list order as "chronological"
# But we want the last ones (newest) to be today.

total = len(articles)
end_date = datetime(2026, 5, 11)

for i, article in enumerate(articles):
    # Calculate date: end_date - (total - 1 - i) days
    # This ensures the last article is today, and they go back in time.
    d = end_date - timedelta(days=(total - 1 - i))
    article['date'] = d.strftime('%Y-%m-%d')
    article['dateFull'] = d.strftime('%B %d, %Y')

with open(path, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print(f"Redated {total} articles. Newest: {articles[-1]['date']}, Oldest: {articles[0]['date']}")
