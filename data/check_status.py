import os, sys, json, re
sys.stdout.reconfigure(encoding='utf-8')
base = r'C:\Users\27040\WorkBuddy\20260321092139\seo-site-en'

# 文章数据
for fname in ['articles_en.json', 'articles.json']:
    art_path = os.path.join(base, 'data', fname)
    if os.path.exists(art_path):
        with open(art_path, encoding='utf-8') as f:
            arts = json.load(f)
        print(f'文章数据文件: {fname}, 共 {len(arts)} 篇')
        statuses = {}
        for a in arts:
            s = a.get('status', 'N/A')
            statuses[s] = statuses.get(s, 0) + 1
        print(f'  状态分布: {statuses}')
        for a in arts[:3]:
            words = len(a.get('content','').split())
            print(f'  {a["slug"]}: {words}w status={a.get("status","N/A")}')
        break

print()

# OG图
og_dir = os.path.join(base, 'images', 'og')
if os.path.exists(og_dir):
    og_files = [f for f in os.listdir(og_dir) if f.endswith('.png')]
    print(f'OG图数量: {len(og_files)}')
else:
    print('OG目录不存在')

# sitemap
sitemap = os.path.join(base, 'sitemap.xml')
if os.path.exists(sitemap):
    with open(sitemap, encoding='utf-8') as f:
        content = f.read()
    urls = re.findall(r'<loc>(.*?)</loc>', content)
    print(f'sitemap.xml: {len(urls)} 条URL')
    print(f'  前3条: {urls[:3]}')
else:
    print('sitemap.xml: 不存在')

# robots.txt
robots = os.path.join(base, 'robots.txt')
print(f'robots.txt: {"存在" if os.path.exists(robots) else "不存在"}')

# IndexNow
indexnow = os.path.join(base, '.indexnow_en_pushed.json')
if os.path.exists(indexnow):
    with open(indexnow, encoding='utf-8') as f:
        data = json.load(f)
    print(f'IndexNow已推送: {len(data)} 条URL')
else:
    print('IndexNow推送记录: 不存在')

# 已build的工具页
tools_built = []
tools_dir = os.path.join(base, 'tools')
if os.path.exists(tools_dir):
    for d in os.listdir(tools_dir):
        idx = os.path.join(tools_dir, d, 'index.html')
        if os.path.exists(idx):
            tools_built.append(d)
print(f'\n已build工具页: {len(tools_built)} 个')

# 已build文章页
arts_built = []
arts_dir = os.path.join(base, 'articles')
if os.path.exists(arts_dir):
    for d in os.listdir(arts_dir):
        idx = os.path.join(arts_dir, d, 'index.html')
        if os.path.exists(idx):
            arts_built.append(d)
print(f'已build文章页: {len(arts_built)} 个')
