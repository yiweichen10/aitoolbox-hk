import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('data/articles_en.json', encoding='utf-8') as f:
    arts = json.load(f)
print(f'共{len(arts)}篇')
for a in arts:
    words = len(a.get('content','').split())
    print(f"  {a['slug']} | {words}w")
