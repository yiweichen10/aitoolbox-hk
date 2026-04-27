import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\27040\WorkBuddy\20260321092139\seo-site-en'
os.chdir(base)

# 检查新文章页面
new_arts = [
    'best-ai-tools-for-freelancers-2026',
    'ai-tools-for-social-media-2026',
    'best-ai-chatbots-2026'
]
print('=== 新文章页面检查 ===')
for slug in new_arts:
    path = f'en/articles/{slug}/index.html'
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            html = f.read()
        title_m = re.search(r'<title>(.*?)</title>', html)
        canon_m = re.search(r'rel="canonical"[^>]*href="([^"]+)"', html)
        og_m = re.search(r'og:image.*?content="([^"]+)"', html)
        print(f'[OK] {slug}')
        print(f'  title: {title_m.group(1)[:65] if title_m else "N/A"}')
        print(f'  canonical: {canon_m.group(1) if canon_m else "N/A"}')
        print(f'  og:image: {"有" if og_m else "无"}')
    else:
        print(f'[MISS] {path}')
    print()

# IndexNow key文件检查
print('=== IndexNow 配置检查 ===')
all_files = os.listdir('.')
key_files = [f for f in all_files if f.endswith('.txt')]
print(f'根目录 .txt 文件: {key_files}')

# 读build_en.py里的IndexNow配置
with open('scripts/build_en.py', encoding='utf-8') as f:
    build_src = f.read()
key_match = re.search(r'INDEXNOW_KEY\s*=\s*["\']([^"\']+)["\']', build_src)
host_match = re.search(r'indexnow.*?host.*?["\']([^"\']+)["\']', build_src)
print(f'IndexNow KEY: {key_match.group(1) if key_match else "未找到"}')

# sitemap条数
with open('sitemap.xml', encoding='utf-8') as f:
    sm = f.read()
urls = re.findall(r'<loc>(.*?)</loc>', sm)
print(f'\nsitemap URL数: {len(urls)}')
tool_urls = [u for u in urls if '/tools/' in u]
art_urls = [u for u in urls if '/articles/' in u]
print(f'  工具页: {len(tool_urls)}')
print(f'  文章页: {len(art_urls)}')
print(f'  其他: {len(urls)-len(tool_urls)-len(art_urls)}')
