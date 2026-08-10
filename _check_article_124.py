# -*- coding: utf-8 -*-
"""Article #124 self-check script"""
import re

with open('_article_124_draft.txt', encoding='utf-8') as f:
    raw = f.read()

parts = raw.split('\n---\n', 1)
meta = {}
for line in parts[0].strip().splitlines():
    if ':' in line:
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()
content = parts[1].strip()
print('标题:', meta.get('TITLE'))
print('Slug:', meta.get('SLUG'))
print('分类:', meta.get('CATEGORY'))

words = len(content.split())
print(f'1. 词数: {words} (要求 2200-2800)')

pk = 'AI voice agents 2026'
pk_count = content.count(pk)
print(f'2. PK "{pk}" 精确计数: {pk_count} (要求 4)')

banned = ['leverage', 'utilize', 'seamlessly', 'game-changing', 'empower',
          'streamline', 'delve into', 'transformative', 'comprehensive',
          'revolutionize', 'cutting-edge', 'as an AI', 'in conclusion']
found = [b for b in banned if b.lower() in content.lower()]
print(f'3. 违禁词: {found if found else "无"}')

lts = meta.get('KEYWORDS', '').split('|')
print(f'4. 长尾词 ({len(lts)-1}个):')
missing = []
for lt in lts[1:]:
    c = content.lower().count(lt.lower())
    if c >= 1:
        print(f'   [OK] {lt} x{c}')
    else:
        missing.append(lt)
        print(f'   [MISSING] {lt} x0')

links = re.findall(r'\[([^\]]+)\]\((/[^)]+)\)', content)
print(f'5. 内链 {len(links)} 个:')
for text, url in links:
    print(f'   [{text}] -> {url}')

table_lines = [l for l in content.splitlines() if l.strip().startswith('|')]
sep_rows = [l for l in table_lines if re.match(r'^\|[\s\-:|]+\|$', l.strip())]
data_rows = len(table_lines) - len(sep_rows) - 1
cols = len([c for c in table_lines[0].split('|') if c.strip()]) if table_lines else 0
print(f'6. 表格: {data_rows} 数据行 x {cols} 列 (要求 >=4x4)')

faq = re.search(r'## Frequently Asked Questions(.*?)(?=\n## |\Z)', content, re.S)
if faq:
    h3s = re.findall(r'^### (.+)$', faq.group(1), re.M)
    print(f'7. FAQ H3 数量: {len(h3s)}')
    for h in h3s:
        print(f'   - {h}')
else:
    print('7. FAQ 段缺失!')
    h3s = []

h2s = re.findall(r'^## (.+)$', content, re.M)
print('8. H2 列表:')
for h in h2s:
    print(f'   - {h}')

print()
print('== 结论 ==')
issues = []
if not (2200 <= words <= 2800):
    issues.append(f'词数不达标({words})')
if pk_count != 4:
    issues.append(f'PK 不是 4x({pk_count})')
if found:
    issues.append(f'有违禁词: {found}')
if missing:
    issues.append(f'长尾缺失: {missing}')
if len(links) < 2:
    issues.append(f'内链不足({len(links)})')
if data_rows < 4 or cols < 4:
    issues.append(f'表格不达标({data_rows}x{cols})')
if not faq or len(h3s) < 3:
    issues.append('FAQ 不足')
print('全部通过 OK' if not issues else '需修复: ' + '; '.join(issues))
