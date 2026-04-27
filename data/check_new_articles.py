import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','dive into','transformative','comprehensive','revolutionize',
          'cutting-edge','as an AI','in conclusion']

with open('data/articles_en.json', encoding='utf-8') as f:
    arts = json.load(f)

new_slugs = [
    'best-ai-tools-for-freelancers-2026',
    'ai-tools-for-social-media-2026',
    'best-ai-chatbots-2026'
]

print(f'文章库总数: {len(arts)} 篇\n')

for a in arts:
    if a['slug'] not in new_slugs:
        continue
    content = a.get('content', '')
    words = len(content.split())
    h2s = re.findall(r'^## .+', content, re.MULTILINE)
    table_rows = re.findall(r'^\|.+\|', content, re.MULTILINE)
    hits = [w for w in banned if w.lower() in content.lower()]
    ok = words >= 1800 and len(table_rows) >= 4 and not hits
    status = 'GOOD' if ok else 'CHECK'
    print(f'[{status}] {a["slug"]}')
    print(f'  字数:{words} | H2数:{len(h2s)} | 表格行:{len(table_rows)} | 禁用词:{hits if hits else "无"}')
    print(f'  title: {a.get("title","")[:60]}')
    print()
