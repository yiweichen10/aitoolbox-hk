import re, sys
sys.stdout.reconfigure(encoding='utf-8')

path  = "data/_drafts_en/claude-accio.md"
c     = open(path, encoding='utf-8').read()
cl    = c.lower()
words = len(c.split())

AI_SMELL = ['leverage','utilize','seamlessly','game-changing','empower','streamline',
            'delve into','dive into','transformative','comprehensive',
            'it is worth noting','in conclusion','as an ai','in today']
smell = [(w, cl.count(w)) for w in AI_SMELL if w in cl]

pk       = 'claude review'
pk_count = cl.count(pk)
first100 = ' '.join(c.split()[:100]).lower()
h2       = re.findall(r'^## .+', c, re.MULTILINE)
h3q      = [h for h in re.findall(r'^### .+', c, re.MULTILINE) if '?' in h]
table    = bool(re.search(r'^\|.+\|', c, re.MULTILINE))
links    = re.findall(r'\[([^\]]+)\]\(/[a-z0-9-]+/\)', c)
pk_h2    = any(pk in h.lower() for h in h2)
lt = [
    ('claude alternative',   cl.count('claude alternative')),
    ('claude vs chatgpt',    cl.count('claude vs chatgpt')),
    ('is claude ai',         cl.count('is claude ai')),
]

print(f"=== ACCIO claude ({words}w) ===")
print(f"  AI smell   : {'CLEAN' if not smell else smell}")
print(f"  Primary KW : '{pk}' x{pk_count} | first100={pk in first100} | h2={pk_h2}")
print(f"  Long-tail  : {lt}")
print(f"  H2 ({len(h2)})   : {[h[3:55] for h in h2]}")
print(f"  FAQ H3+?   : {len(h3q)}")
print(f"  Table      : {table}")
print(f"  Int links  : {links}")
