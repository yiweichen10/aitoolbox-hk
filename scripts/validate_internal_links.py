"""Validate all internal /articles/ links in articles_en.json point to real slugs."""
import json
import re
import sys

def validate(json_path=None):
    if json_path is None:
        from pathlib import Path
        script_dir = Path(__file__).parent.parent
        json_path = script_dir / 'data' / 'articles_en.json'
    
    with open(json_path, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    all_slugs = set(a['slug'] for a in articles)
    broken = []
    
    for i, art in enumerate(articles, 1):
        links = re.findall(r'/articles/([a-z0-9-]+)/', art['content'])
        for link in links:
            if link not in all_slugs:
                broken.append((i, art['slug'], link))
    
    if broken:
        print(f'\n=== {len(broken)} BROKEN INTERNAL LINKS ===')
        for idx, art_slug, bad_link in broken:
            print(f'  Article #{idx} ({art_slug}):')
            print(f'    Broken: /articles/{bad_link}/')
            # Try to suggest a fix
            for slug in all_slugs:
                if bad_link[:20] in slug or slug[:20] in bad_link:
                    print(f'    Suggest: /articles/{slug}/')
                    break
        return False
    
    total = sum(len(re.findall(r'/articles/([a-z0-9-]+)/', a['content'])) for a in articles)
    articles_with = sum(1 for a in articles if '/articles/' in a['content'])
    print(f'OK: {len(articles)} articles, {total} internal links, {articles_with} articles with links — all valid')
    return True

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else None
    ok = validate(path)
    sys.exit(0 if ok else 1)
