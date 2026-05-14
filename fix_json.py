import json
import os

path = 'C:/Users/27040/WorkBuddy/20260321092139/seo-site-en/data/tools_en.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for tool in data:
    if tool['slug'] == 'surfer-seo':
        c = tool['content']
        # Fix the escaped newlines and headers
        # c contains literal \ and n because of the previous bad edit.
        c = c.replace('\\n', '\n').replace('\\"', '"').replace('\\$', '$')
        # Remove the H1 at the start
        if c.startswith('# Surfer SEO Review 2026:'):
            lines = c.split('\n')
            if lines:
                lines = lines[1:] # remove first line (H1)
                # Skip any leading empty lines
                while lines and not lines[0].strip():
                    lines = lines[1:]
                c = '\n'.join(lines)
        tool['content'] = c

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

for tool in data:
    if tool['slug'] == 'surfer-seo':
        tool['content'] = tool['content'].strip().rstrip('-').strip()

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
