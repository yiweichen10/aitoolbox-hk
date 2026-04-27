import sys
sys.stdout.reconfigure(encoding='utf-8')

def check(path, tests):
    c = open(path, encoding='utf-8').read()
    print(f'\n=== {path} ===')
    for name, cond in tests:
        print(f'  {name}: {"OK" if cond(c) else "FAIL"}')

check('index.html', [
    ('lang=en', lambda c: 'lang="en"' in c),
    ('AI Tool Lab', lambda c: 'AI Tool Lab' in c),
    ('hreflang', lambda c: 'hreflang' in c),
    ('no AI Tool Box CN', lambda c: 'AI工具宝箱' not in c),
    ('tools link (no /en/)', lambda c: '/tools/chatgpt/' in c and '/en/' not in c),
])
check('tools/chatgpt/index.html', [
    ('lang=en', lambda c: 'lang="en"' in c),
    ('Pros heading', lambda c: 'Pros' in c),
    ('hreflang zh-CN', lambda c: 'hreflang' in c),
    ('no /en/ prefix', lambda c: '/en/' not in c),
])
