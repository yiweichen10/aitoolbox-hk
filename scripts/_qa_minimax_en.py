import re, sys
sys.stdout.reconfigure(encoding='utf-8')

path = "data/_drafts_en/chatgpt-minimax.md"
c    = open(path, encoding='utf-8').read()
cl   = c.lower()
words = len(c.split())

AI_SMELL = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
            'delve into','dive into','transformative','comprehensive',
            'it is worth noting','in conclusion','as an ai','in today']
smell = [(w, cl.count(w)) for w in AI_SMELL if cl.count(w) > 0]

pk       = 'chatgpt review'
pk_count = cl.count(pk)
first100 = ' '.join(c.split()[:100]).lower()
h2       = re.findall(r'^## .+', c, re.MULTILINE)
h3q      = [h for h in re.findall(r'^### .+', c, re.MULTILINE) if '?' in h]
table    = bool(re.search(r'^\|.+\|', c, re.MULTILINE))
links    = re.findall(r'\[([^\]]+)\]\(/[a-z0-9-]+/\)', c)
pk_h2    = any(pk in h.lower() for h in h2)
lt = [
    ('chatgpt alternative',            cl.count('chatgpt alternative')),
    ('chatgpt alternative for writing', cl.count('chatgpt alternative for writing')),
    ('chatgpt reviews 2025',            cl.count('chatgpt reviews 2025')),
]

smell_str = "CLEAN" if not smell else str(smell)
print(f"=== MiniMax chatgpt ({words}w) ===")
print(f"  AI smell : {smell_str}")
print(f"  PK       : x{pk_count} | first100={pk in first100} | h2={pk_h2}")
print(f"  Longtail : {lt}")
print(f"  H2 ({len(h2)})  : {[h[3:60] for h in h2]}")
print(f"  FAQ H3+? : {len(h3q)}")
print(f"  Table    : {table}")
print(f"  Intlinks : {links}")
