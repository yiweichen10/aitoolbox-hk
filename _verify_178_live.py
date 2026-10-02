# -*- coding: utf-8 -*-
"""Poll live URL until it serves the FULL page (pitfall #10: 200 != deployed)."""
import time, urllib.request, re

SLUG = 'best-ai-service-desk-software-2026-servicenow-vs-freshservice-vs-jira-service-management-vs-moveworks'
URL = 'https://www.aitoolbox.hk/articles/' + SLUG + '/'
SITEMAP = 'https://www.aitoolbox.hk/sitemap.xml'
LIST = 'https://www.aitoolbox.hk/articles/'

def get(url, timeout=30):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; aitoolbox-verify/1.0)'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode('utf-8', 'replace')

deadline = time.time() + 30 * 60
attempt = 0
ok = False
while time.time() < deadline:
    attempt += 1
    ts = time.strftime('%H:%M:%S')
    try:
        status, html = get(URL)
        pk = html.count('AI service desk software')
        trs = html.count('<tr>')
        title_ok = 'AI Service Desk Software 2026' in html
        links_ok = all(x in html for x in ['/tools/glean/',
                                           'best-ai-customer-service-tools-2026',
                                           'best-ai-enterprise-search-tools-2026'])
        full = pk >= 4 and trs >= 5 and title_ok and links_ok
        print(f'[{ts}] #{attempt} HTTP {status} | bytes={len(html)} pk={pk} rows={trs} title={title_ok} links={links_ok} -> {"FULL PAGE OK" if full else "INCOMPLETE (stale/partial)"}')
        if full:
            ok = True
            break
    except Exception as e:
        code = getattr(e, 'code', None)
        print(f'[{ts}] #{attempt} {type(e).__name__} {code if code else ""} {str(e)[:90]}')
        if code == 404:
            try:
                ls, lb = get(LIST)
                sm, sb = get(SITEMAP)
                print(f'          list={ls} has_slug={SLUG in lb} | sitemap={sm} has_slug={SLUG in sb}')
            except Exception as e2:
                print('          probe failed:', str(e2)[:80])
    time.sleep(43)

print('\n=== RESULT ===')
print('LIVE VERIFIED' if ok else 'NOT LIVE AFTER 30 MIN')
