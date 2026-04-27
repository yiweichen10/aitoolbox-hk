import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'data/articles_en.json', encoding='utf-8') as f:
    arts = json.load(f)
for a in arts:
    words = len(a.get('content','').split())
    print(f"{a['slug']} | {a.get('title','')[:55]} | {words}w")
