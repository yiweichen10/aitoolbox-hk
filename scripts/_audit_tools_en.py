import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

tools = json.loads(Path('data/tools_en.json').read_text(encoding='utf-8'))
AI_SMELL = ['leverage','utilize','seamlessly','game-changing','streamline',
            'delve into','as an ai','transformative','comprehensive']

need_rewrite = []
already_good = []

for t in tools:
    c  = t.get('content','')
    cl = c.lower()
    words = len(c.split())
    smell = [w for w in AI_SMELL if w in cl]
    h3q   = len([h for h in re.findall(r'^### .+', c, re.MULTILINE) if '?' in h])
    table = bool(re.search(r'^\|.+\|', c, re.MULTILINE))
    links = len(re.findall(r'\[([^\]]+)\]\(/[a-z0-9.-]+/\)', c))
    good  = words >= 1200 and not smell and h3q >= 2 and table
    tag   = 'GOOD' if good else 'REWRITE'
    smell_flag = 'Y' if smell else 'N'
    if good:
        already_good.append(t['slug'])
    else:
        need_rewrite.append(t['slug'])
    print(f"{t['slug']:<25} {words:>5}w  faq={h3q}  tbl={int(table)}  lnk={links}  smell={smell_flag}  [{tag}]")

print()
print(f"GOOD    ({len(already_good)}): {already_good}")
print(f"REWRITE ({len(need_rewrite)}): {need_rewrite}")
