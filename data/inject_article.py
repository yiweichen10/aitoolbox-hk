import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

# 读草稿
with open('data/article_draft.md', encoding='utf-8') as f:
    content = f.read().strip()

# 验证质量
words = len(content.split())
h2s = re.findall(r'^## .+', content, re.MULTILINE)
h3s = re.findall(r'^### .+', content, re.MULTILINE)
table_rows = re.findall(r'^\|.+\|', content, re.MULTILINE)
banned = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
          'delve into','dive into','transformative','comprehensive','revolutionize',
          'cutting-edge','as an AI','in conclusion']
hits = [w for w in banned if w.lower() in content.lower()]

print(f'字数: {words}')
print(f'H2数: {len(h2s)}')
print(f'H3数(FAQ): {len(h3s)}')
print(f'表格行数: {len(table_rows)}')
print(f'禁用词: {hits if hits else "无"}')

ok = words >= 2000 and len(table_rows) >= 5 and len(h3s) >= 2 and not hits
print(f'\n质检结果: {"GOOD ✅" if ok else "CHECK ⚠️"}')

if ok:
    new_article = {
        "slug": "how-to-use-ai-to-make-money-online-2026",
        "title": "How to Use AI to Make Money Online in 2026: 9 Proven Methods",
        "description": "Nine tested ways to make money online with AI in 2026, from freelance writing to selling AI art. Includes real income ranges, tools needed, and how to start.",
        "keywords": "how to use AI to make money online, make money with AI, AI side hustle 2026",
        "category": "AI Guide",
        "date": "2026-04-19",
        "dateFull": "April 19, 2026",
        "content": content
    }

    with open('data/articles_en.json', encoding='utf-8') as f:
        arts = json.load(f)

    # 检查是否已存在
    existing = [a for a in arts if a['slug'] == new_article['slug']]
    if existing:
        print(f'\n已存在该slug，跳过写入')
    else:
        arts.append(new_article)
        with open('data/articles_en.json', 'w', encoding='utf-8') as f:
            json.dump(arts, f, ensure_ascii=False, indent=2)
        print(f'\n已写入 articles_en.json，总篇数: {len(arts)}')
else:
    print('\n质检未通过，未写入')
