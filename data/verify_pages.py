import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\27040\WorkBuddy\20260321092139\seo-site-en'
slugs = [
    'best-ai-tools-for-freelancers-2026',
    'ai-tools-for-social-media-2026',
    'best-ai-chatbots-2026'
]

print('=== 新文章页面验证 ===\n')
for slug in slugs:
    path = os.path.join(base, 'articles', slug, 'index.html')
    if not os.path.exists(path):
        print(f'[MISS] {slug}')
        continue
    with open(path, encoding='utf-8') as f:
        html = f.read()
    title_m = re.search(r'<title>([^<]+)</title>', html)
    canon_m = re.search(r'canonical[^>]+href="([^"]+)"', html)
    og_img = 'og:image' in html
    size_kb = os.path.getsize(path) // 1024
    print(f'[OK] {slug}')
    print(f'  title   : {title_m.group(1)[:65] if title_m else "N/A"}')
    print(f'  canonical: {canon_m.group(1) if canon_m else "N/A"}')
    print(f'  og:image : {"有" if og_img else "无"}')
    print(f'  文件大小 : {size_kb} KB')
    print()

print('=== IndexNow 403 原因分析 ===')
with open(os.path.join(base, 'scripts', 'build_en.py'), encoding='utf-8') as f:
    src = f.read()
key_m = re.search(r'INDEXNOW_KEY\s*=\s*["\']([^"\']+)["\']', src)
key = key_m.group(1) if key_m else 'N/A'
print(f'IndexNow KEY: {key}')
key_file = os.path.join(base, f'{key}.txt')
print(f'Key验证文件 {key}.txt: {"存在" if os.path.exists(key_file) else "不存在！← 这是403原因"}')

print()
print('=== Sitemap 状态 ===')
with open(os.path.join(base, 'sitemap.xml'), encoding='utf-8') as f:
    sm = f.read()
urls = re.findall(r'<loc>([^<]+)</loc>', sm)
tool_urls = [u for u in urls if '/tools/' in u]
art_urls = [u for u in urls if '/articles/' in u]
print(f'总URL: {len(urls)} | 工具页: {len(tool_urls)} | 文章页: {len(art_urls)} | 其他: {len(urls)-len(tool_urls)-len(art_urls)}')
