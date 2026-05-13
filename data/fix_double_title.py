import json

json_path = r'C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data\articles_en.json'

with open(json_path, 'r', encoding='utf-8') as f:
    articles = json.load(f)

# The last article is the one I just added
last_article = articles[-1]

if last_article['title'] == "Top-Rated AI Video Generators 2026: The Ultimate Guide for Creators":
    content = last_article['content']
    lines = content.split('\n')
    # Remove the first line if it's the # title
    if lines[0].startswith('# '):
        lines = lines[1:]
        # Remove any leading empty lines
        while lines and not lines[0].strip():
            lines = lines[1:]
        last_article['content'] = '\n'.join(lines)
        print("Successfully removed duplicate title from content.")
    else:
        print("First line does not start with '# '. No change made.")
else:
    print("Last article title mismatch. Checking all articles...")
    for article in articles:
        if article['title'] == "Top-Rated AI Video Generators 2026: The Ultimate Guide for Creators":
            content = article['content']
            lines = content.split('\n')
            if lines[0].startswith('# '):
                lines = lines[1:]
                while lines and not lines[0].strip():
                    lines = lines[1:]
                article['content'] = '\n'.join(lines)
                print(f"Fixed article: {article['title']}")

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(articles, f, indent=2, ensure_ascii=False)
