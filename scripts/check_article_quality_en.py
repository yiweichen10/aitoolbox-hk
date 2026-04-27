#!/usr/bin/env python3
"""Quality checker for aitoolbox.hk articles."""
import json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(__file__).parent.parent
articles = json.loads((BASE / "data/articles_en.json").read_text(encoding='utf-8'))

AI_SMELL = [
    'leverage','utilize','seamlessly','robust','cutting-edge','revolutionary',
    'game-changing','empower','streamline','dive into','delve into',
    'in today','it is worth noting','as an ai','in conclusion','to summarize',
    'transformative','innovative solutions','unlock potential','unleash',
    'harness','paradigm','synergy','holistic','actionable insights','moving forward',
]

topics = {
    'ai-tools-for-teachers-2026': {
        'primary': 'ai tools for teachers',
        'longtail': ['ai grading tools','ai for education','teacher ai tools','ai lesson plan'],
    },
    'ai-tools-for-content-creators-2026': {
        'primary': 'ai tools for content creators',
        'longtail': ['ai for youtubers','content creator ai','ai for creators','ai video editing'],
    },
    'ai-writing-tools-compared-2026': {
        'primary': 'ai writing tools',
        'longtail': ['grammarly vs jasper','best ai writing tool','ai writing assistant','writesonic review'],
    },
}

for slug, kws in topics.items():
    a = next((x for x in articles if x['slug']==slug), None)
    if not a:
        print(f'{slug}: NOT FOUND\n'); continue
    c = a['content']
    cl = c.lower()
    words = len(c.split())
    paras = [p for p in c.split('\n\n') if p.strip()]

    h2  = re.findall(r'^## .+', c, re.MULTILINE)
    h3  = re.findall(r'^### .+', c, re.MULTILINE)
    has_table = bool(re.search(r'^\|.+\|', c, re.MULTILINE))
    faq_h3 = [h for h in h3 if '?' in h]
    links = re.findall(r'\[([^\]]+)\]\(/[a-z0-9-]+/\)', c)

    pk = kws['primary']
    pk_count = len(re.findall(re.escape(pk), cl))
    first100  = ' '.join(c.split()[:100]).lower()
    pk_first  = pk in first100
    pk_in_h2  = any(pk in h.lower() for h in h2)
    pk_in_end = pk in paras[-1].lower() if paras else False

    smell = [(w, len(re.findall(r'\b'+re.escape(w)+r'\b', cl)))
             for w in AI_SMELL if re.search(r'\b'+re.escape(w)+r'\b', cl)]
    lt_hits = [(lt, cl.count(lt)) for lt in kws['longtail']]

    # Score
    issues = []
    if pk_count < 3:        issues.append(f'PRIMARY KW only {pk_count}x (need 3-5)')
    if not pk_first:        issues.append('PRIMARY KW missing from first 100 words')
    if not pk_in_h2:        issues.append('PRIMARY KW missing from H2 headers')
    if not pk_in_end:       issues.append('PRIMARY KW missing from final paragraph')
    if not has_table:       issues.append('No comparison table')
    if len(faq_h3) < 3:    issues.append(f'Only {len(faq_h3)} FAQ (need 3+)')
    if not links:           issues.append('No internal links')
    for lt, n in lt_hits:
        if n == 0:          issues.append(f'Long-tail missing: "{lt}"')
    for w, n in smell:      issues.append(f'AI smell [{n}x]: "{w}"')

    status = 'PASS' if not issues else 'FAIL'
    print(f'[{status}] {slug} ({words}w)')
    print(f'  PK "{pk}": {pk_count}x | first100={pk_first} | h2={pk_in_h2} | endpara={pk_in_end}')
    print(f'  Long-tail: {lt_hits}')
    print(f'  H2({len(h2)}) FAQ({len(faq_h3)}) Table={has_table} Links={links}')
    if issues:
        for i in issues: print(f'  !! {i}')
    print()
