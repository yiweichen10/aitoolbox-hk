# -*- coding: utf-8 -*-
import re, os, json

raw = open('_article_170_draft.txt', encoding='utf-8').read()
parts = raw.split('\n---\n', 1)
meta = dict(line.split(':', 1) for line in parts[0].strip().splitlines() if ':' in line)
content = parts[1].strip()

print('META LEAK:', content[:80].replace('\n', ' '))
print('words:', len(content.split()), '(need 2200-2800)')

pk = meta['KEYWORDS'].split('|')[0].strip()
print('PK =', repr(pk), '->', content.count(pk), '(need exactly 4)')
for m in re.finditer(re.escape(pk), content):
    print('   ...', content[max(0, m.start()-60):m.end()+40].replace('\n', ' '))

banned = ['leverage', 'utilize', 'seamlessly', 'game-changing', 'empower', 'streamline',
          'delve into', 'transformative', 'comprehensive', 'revolutionize', 'cutting-edge',
          'as an AI', 'in conclusion']
print('banned:', [b for b in banned if b.lower() in content.lower()])

print('--- long tails ---')
lts = [x.strip() for x in meta['KEYWORDS'].split('|')[1:]]
miss = []
for lt in lts:
    n = content.lower().count(lt.lower())
    print(f'  {lt}: {n}')
    if n < 1:
        miss.append(lt)
print('MISSING:', miss)

print('--- internal links ---')
links = re.findall(r'\[[^\]]+\]\((/[^)]+)\)', content)
print('links:', links, 'count', len(links))
for l in links:
    target = l.strip('/').split('/')
    p = os.path.join(*target) if target else ''
    ok = os.path.isdir(p)
    print('   ', l, 'exists' if ok else '*** MISSING ***')

print('--- tables ---')
rows = [l for l in content.splitlines() if l.strip().startswith('|')]
print('table lines:', len(rows))

print('--- FAQ ---')
m = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
h3 = re.findall(r'### ', m.group(1)) if m else []
print('FAQ H3:', len(h3))

print('--- H2s ---')
for h in re.findall(r'^## .*', content, re.M):
    print('  ', h)

print('--- slug dup check ---')
arts = json.load(open('data/articles_en.json', encoding='utf-8'))
slugs = {a['slug'] for a in arts}
print('slug exists already:', meta['SLUG'].strip() in slugs)
print('total articles now:', len(arts))
