import json, sys
sys.stdout.reconfigure(encoding='utf-8')
path = 'data/articles_en.json'
articles = json.loads(open(path, encoding='utf-8').read())
a = next(x for x in articles if x['slug'] == 'ai-tools-for-teachers-2026')
content = a['content']

old_frag = "But tonight, I\u2019m clicking"
new_frag = "But tonight, the AI tools for teachers I\u2019ve been testing are changing that\u2014I\u2019m clicking"

if old_frag in content:
    a['content'] = content.replace(old_frag, new_frag, 1)
    open(path, 'w', encoding='utf-8').write(json.dumps(articles, ensure_ascii=False, indent=2))
    words = a['content'].split()
    first100 = ' '.join(words[:100]).lower()
    print('Fixed. KW in first 100 words:', 'ai tools for teachers' in first100)
    print('KW count total:', a['content'].lower().count('ai tools for teachers'))
else:
    print('Fragment not found. Showing idx 370-500:')
    print(repr(content[370:500]))
