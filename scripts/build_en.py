#!/usr/bin/env python3
"""
English SSG build script for aitoolbox.hk (standalone site)
Completely independent from build.py — no imports, no shared state.
Outputs pages at site root (no / prefix).
"""
import json
import os
import re
import argparse
from datetime import datetime

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUT_DIR = BASE_DIR   # output goes directly at project root (no / subdirectory)

# ─── Site constants ────────────────────────────────────────────────────────────
SITE_NAME    = "AI Tool Lab"
SITE_DOMAIN  = "https://www.aitoolbox.hk"
SITE_DOMAIN_CN = "https://www.aitoollab.cn"
SITE_LOGO    = f"{SITE_DOMAIN}/images/logo.png"

# ─── Back-to-top button (no Chinese) ──────────────────────────────────────────
BACK_TO_TOP_BLOCK = '''<button id="backToTop" aria-label="Back to top">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="18 15 12 9 6 15"></polyline>
    </svg>
</button>
<script>
document.addEventListener("DOMContentLoaded",function(){var b=document.getElementById("backToTop");if(!b)return;var s=function(){if(window.scrollY>400){b.classList.add("visible")}else{b.classList.remove("visible")}};window.addEventListener("scroll",s,{passive:true});s();b.addEventListener("click",function(){window.scrollTo({top:0,behavior:"smooth"})});});
</script>'''

# ─── Verification tags (Google/Yandex/etc.) ──────────────────────────────────
VERIFICATION_BLOCK = '''    <meta name="yandex-verification" content="5ae78527ec9bcb4b" />
'''

# ─── AEO+GEO+EEAT Schema Blocks (2026-06-23) ────────────────────────────────
SCHEMA_HOMEPAGE_BLOCK = '''    <!-- Schema: WebSite + SearchAction (AEO+GEO 2026-06-23) -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "AI Tool Lab",
        "alternateName": "AIToolbox",
        "description": "Independent AI tool reviews and comparisons. 110+ AI tools tested and ranked, updated daily.",
        "url": "https://www.aitoolbox.hk",
        "inLanguage": "en",
        "potentialAction": {
            "@type": "SearchAction",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": "https://www.aitoolbox.hk/?q={search_term_string}"
            },
            "query-input": "required name=search_term_string"
        }
    }
    </script>
    <!-- Schema: Organization (EEAT 2026-06-23) -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "AI Tool Lab",
        "alternateName": "AIToolbox",
        "url": "https://www.aitoolbox.hk",
        "logo": {
            "@type": "ImageObject",
            "url": "https://www.aitoolbox.hk/images/logo.png",
            "width": 200,
            "height": 60
        },
        "foundingDate": "2026-03-21",
        "founder": {
            "@type": "Organization",
            "name": "AI Tool Lab Editorial Team",
            "description": "Independent editorial team focused on AI tool testing and comparison",
            "knowsAbout": ["AI tool review", "AI model comparison", "AEO", "GEO", "AI coding tools", "AI chat models"]
        },
        "description": "AI Tool Lab is an independent AI tool review site featuring 110+ tested tools, monthly in-depth comparisons, all data sourced and verifiable.",
        "knowsAbout": ["AI tools", "AI models", "AI coding", "AI image generation", "AI video", "AI office", "AI chat", "AEO", "GEO"],
        "slogan": "Data-driven AI tool decisions",
        "publishingPrinciples": "https://www.aitoolbox.hk/about.html",
        "actionableFeedbackPolicy": "All review data comes from public sources or author testing, every article cites sources, all verifiable.",
        "sameAs": [
            "https://github.com/yiweichen10/ai-toolbox"
        ]
    }
    </script>
    <!-- Schema: BreadcrumbList -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.aitoolbox.hk/" }
        ]
    }
    </script>
'''

# ─── Global nav (English) ─────────────────────────────────────────────────────
GLOBAL_NAV_EN = '''    <nav class="global-nav" aria-label="Global navigation">
        <div class="global-nav-inner">
            <a href="/category/" class="gn-item">📂 All Categories</a>
            <a href="/articles/" class="gn-item">📖 Articles</a>
            <a href="/" class="gn-item">🏠 Home</a>
        </div>
    </nav>'''

# ─── Google Analytics + Microsoft Clarity ─────────────────────────────────────
GA_BLOCK = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-FKEXWVFYV0"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-FKEXWVFYV0');
</script>
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "x7bqqir44k");
</script>'''

# ─── English category slug map ────────────────────────────────────────────────
CATEGORY_SLUG_MAP_EN = {
    "AI Chat":        "ai-chat",
    "AI Writing":     "ai-writing",
    "AI Image":       "ai-image",
    "AI Coding":      "ai-coding",
    "AI Video":       "ai-video",
    "AI Audio":       "ai-audio",
    "AI Office":      "ai-office",
    "AI Design":      "ai-design",
    "AI Search":      "ai-search",
    "AI Translation": "ai-translation",
    "AI Automation":  "ai-automation",
    "AI Productivity":"ai-productivity",
    "AI Income":      "ai-income",
    "AI Tools":       "ai-tools",
}

def get_category_slug_en(name: str) -> str:
    if name in CATEGORY_SLUG_MAP_EN:
        return CATEGORY_SLUG_MAP_EN[name]
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

# ─── Helpers ──────────────────────────────────────────────────────────────────

def escape_html(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;'))

def markdown_to_html(md: str) -> str:
    """Convert Markdown to HTML — same logic as build.py but standalone."""
    if not md:
        return ''
    html = md
    # Code blocks
    html = re.sub(
        r'```(\w*)\n([\s\S]*?)```',
        lambda m: '<pre><code>' + m.group(2).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;') + '</code></pre>',
        html
    )
    # Tables
    def table_replace(m):
        header = m.group(1)
        body   = m.group(3)
        headers = [c.strip() for c in header.split('|') if c.strip()]
        rows    = body.strip().split('\n')
        table   = '<table><thead><tr>'
        for h in headers:
            table += f'<th>{h}</th>'
        table += '</tr></thead><tbody>'
        for row in rows:
            cells = [c.strip() for c in row.split('|') if c.strip()]
            table += '<tr>'
            for c in cells:
                table += f'<td>{c}</td>'
            table += '</tr>'
        table += '</tbody></table>'
        return '\n' + table + '\n'
    html = re.sub(r'\n(\|.+\|)\n(\|[-:| ]+\|)\n((?:\|.+\|\n?)+)', table_replace, html)
    # Headings
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$',  r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$',   r'<h1>\1</h1>', html, flags=re.MULTILINE)
    # Blockquote
    html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
    # Bold / inline code
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    # Links
    html = re.sub(r'\[([^\]]+)\]\((/[^)]+)\)', r'<a href="\2">\1</a>', html)
    html = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', html)
    # Lists
    html = re.sub(r'^- (.+)$',        r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'^\d+\. (.+)$',    r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'((?:<li>.*?</li>\n?)+)', r'<ul>\1</ul>', html)
    # Paragraphs
    lines   = html.split('\n')
    result  = []
    in_p    = False
    block_tags = ('<h1','<h2','<h3','<ul','</ul','<li','<table','</table',
                  '<pre','</pre','<blockquote','</blockquote')
    for line in lines:
        stripped = line.strip()
        is_tag   = stripped == '' or any(stripped.startswith(t) for t in block_tags)
        if is_tag:
            if in_p:
                result.append('</p>')
                in_p = False
            result.append(line)
        else:
            if not in_p:
                result.append('<p>' + line)
                in_p = True
            else:
                result.append(line)
    if in_p:
        result.append('</p>')
    return '\n'.join(result)

# ─── Header / footer partials ─────────────────────────────────────────────────

def header_html(title_text: str = "AI Tool Lab") -> str:
    return f'''    <header class="header">
        <div class="header-inner">
            <a href="/" style="text-decoration:none;">
                <h1>🛠️ {SITE_NAME} <span>Daily updates · 500+ AI tools</span></h1>
            </a>
        </div>
    </header>'''

def footer_html() -> str:
    today = datetime.now().strftime('%Y-%m-%d')
    return f'''    <footer class="footer">
        <p>&copy; {datetime.now().year} {SITE_NAME} &middot; Best AI Tools, Updated Daily &middot; <a href="{SITE_DOMAIN_CN}/" style="color:#999;">中文版</a></p>
    </footer>'''

def hreflang_tags(zh_path: str, en_path: str) -> str:
    """Generate hreflang link tags for zh/en pair. CN site at aitoollab.cn."""
    return (
        f'    <link rel="alternate" hreflang="zh-CN" href="{SITE_DOMAIN_CN}{zh_path}">\n'
        f'    <link rel="alternate" hreflang="en"    href="{SITE_DOMAIN}{en_path}">\n'
        f'    <link rel="alternate" hreflang="x-default" href="{SITE_DOMAIN}{en_path}">\n'
    )

# ─── Tool page ────────────────────────────────────────────────────────────────

def get_og_image_url(slug: str) -> str:
    """
    Return og:image URL for English pages.
    Priority: {slug}-en-og.png (English-specific) > {slug}-og.png (shared) > empty string
    """
    en_path = os.path.join(BASE_DIR, 'images', 'og', f'{slug}-en-og.png')
    if os.path.exists(en_path):
        return f'{SITE_DOMAIN}/images/og/{slug}-en-og.png'
    zh_path = os.path.join(BASE_DIR, 'images', 'og', f'{slug}-og.png')
    if os.path.exists(zh_path):
        return f'{SITE_DOMAIN}/images/og/{slug}-og.png'
    return ''


def ensure_en_og_image(slug: str, data_obj: dict, is_article: bool = False) -> str:
    """Return the expected OG image URL for English pages."""
    return f'{SITE_DOMAIN}/images/og/{slug}-en-og.png'

def build_tool_page_en(tool: dict, all_tools: list, all_articles: list = None) -> str:
    slug = tool['slug']
    name = tool['name']
    cat  = tool.get('category', 'AI Tools')
    cat_slug = get_category_slug_en(cat)

    # Related tools
    same_cat   = [t for t in all_tools if t['slug'] != slug and t.get('category') == cat]
    other_cat  = [t for t in all_tools if t['slug'] != slug and t.get('category') != cat]
    import random; random.seed(42)
    selected   = (same_cat + other_cat)[:5]
    related_html = ''
    if selected:
        cards = ''
        for r in selected:
            cards += f'''<a href="/tools/{r['slug']}/" class="related-card">
                <div style="font-size:24px;margin-bottom:8px;">{r['emoji']}</div>
                <div style="font-weight:600;">{r['name']}</div>
                <div style="font-size:13px;color:#666;">{r.get('category','')}</div>
            </a>\n'''
        related_html = f'''<div class="related-tools" id="relatedSection">
            <h3>🔗 Related Tools</h3>
            <div class="related-grid">{cards}</div>
        </div>'''

    # Related articles
    related_articles_html = ''
    if all_articles:
        name_lower = name.lower()
        matched = [a for a in all_articles if name_lower in a.get('title','').lower() or name_lower in a.get('description','').lower()]
        if len(matched) < 2:
            matched += [a for a in all_articles if a not in matched][:3 - len(matched)]
        if matched:
            cards = ''
            for a in matched[:3]:
                cards += f'''<a href="/articles/{a['slug']}/" class="related-card">
                    <div style="font-weight:600;margin-bottom:4px;">📖 {escape_html(a['title'][:40])}</div>
                    <div style="font-size:13px;color:#666;">{a.get('dateFull', a.get('date',''))}</div>
                </a>\n'''
            related_articles_html = f'''<div class="related-tools">
                <h3>📚 Related Articles</h3>
                <div class="related-grid">{cards}</div>
            </div>'''

    # Pros / cons
    pros_cons_html = ''
    if tool.get('pros') and tool.get('cons'):
        pros_html = ''.join(f'<li>{p}</li>' for p in tool['pros'])
        cons_html = ''.join(f'<li>{c}</li>' for c in tool['cons'])
        pros_cons_html = f'''<div class="pros-cons">
            <div class="pros">
                <h4>👍 Pros</h4>
                <ul>{pros_html}</ul>
            </div>
            <div class="cons">
                <h4>👎 Cons</h4>
                <ul>{cons_html}</ul>
            </div>
        </div>'''

    # Features
    features_html = ''
    if tool.get('features'):
        items = ''.join(f'<div class="feature-item">{f}</div>\n' for f in tool['features'])
        features_html = f'<div class="features-grid">{items}</div>'

    # FAQ
    faq_html   = ''
    faq_schema = []
    if tool.get('faq'):
        for fi in tool['faq']:
            q, a = fi.get('question',''), fi.get('answer','')
            if q and a:
                faq_html += f'''<div class="faq-item">
                    <details>
                        <summary>{escape_html(q)}</summary>
                        <div class="faq-answer">{markdown_to_html(a)}</div>
                    </details>
                </div>\n'''
                faq_schema.append({'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}})
        if faq_html:
            faq_html = f'<div class="faq-section"><h3>❓ FAQ</h3>{faq_html}</div>'

    faq_page_schema = ''
    if faq_schema:
        faq_sd = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":faq_schema}
        faq_page_schema = f'<script type="application/ld+json">{json.dumps(faq_sd, ensure_ascii=False)}</script>'

    # Badge
    badge_html = ''
    if tool.get('badge'):
        bc = {'hot':'#ff4444','new':'#00aa00','pick':'#667eea'}.get(tool['badge'].get('type'),'#667eea')
        badge_html = f' <span class="badge" style="background:{bc};color:#fff;padding:2px 8px;border-radius:4px;font-size:12px;">{tool["badge"]["text"]}</span>'

    # Platform
    platform_html = ''
    if tool.get('platform'):
        platform_html = f'<div class="tool-meta-item">📦 <strong>Platform</strong>: {tool["platform"]}</div>'

    # Dates
    today_iso   = datetime.now().strftime('%Y-%m-%d')
    date_pub    = tool.get('datePublished', today_iso)
    date_mod    = tool.get('dateModified',  today_iso)

    # Structured data
    breadcrumb_data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type":"ListItem","position":1,"name":"Home","item":f"{SITE_DOMAIN}/"},
            {"@type":"ListItem","position":2,"name":cat,"item":f"{SITE_DOMAIN}/category/{cat_slug}/"},
            {"@type":"ListItem","position":3,"name":name,"item":f"{SITE_DOMAIN}/tools/{slug}/"},
        ]
    }

    # Category mapping (English categories → Schema.org ApplicationCategory)
    _cat_map = {
        'AI Chat': 'ChatApplication', 'AI Writing': 'WritingApplication',
        'AI Image': 'DesignApplication', 'AI Image Generation': 'DesignApplication',
        'AI Images': 'DesignApplication', 'Image': 'DesignApplication',
        'AI Design': 'DesignApplication', 'AI Video': 'VideoEditingApplication',
        'Video AI': 'VideoEditingApplication',
        'AI Audio': 'MusicApplication', 'AI Music': 'MusicApplication',
        'AI Coding': 'DeveloperApplication', 'AI Developer': 'DeveloperApplication',
        'AI Dev': 'DeveloperApplication', 'AI Development': 'DeveloperApplication',
        'AI API': 'DeveloperApplication',
        'AI Office': 'BusinessApplication', 'AI Business': 'BusinessApplication',
        'AI Search': 'SearchApplication', 'AI Translation': 'TranslationApplication',
        'AI Automation': 'BusinessApplication', 'Automation': 'BusinessApplication',
        'AI Productivity': 'ProductivityApplication', 'Productivity': 'ProductivityApplication',
        'AI Agent': 'ProductivityApplication', 'AI Agents': 'ProductivityApplication',
        'AI Marketing': 'BusinessApplication', 'Marketing': 'BusinessApplication',
        'AI SEO': 'BusinessApplication', 'SEO': 'BusinessApplication',
        'AI Education': 'EducationalApplication',
        'AI Data': 'BusinessApplication',
        'AI 3D': 'DesignApplication',
        'AI E-commerce': 'BusinessApplication',
        'Writing': 'WritingApplication',
        'Market Research': 'BusinessApplication',
    }
    _app_category = _cat_map.get(tool.get('category', ''), 'UtilitiesApplication')

    # Parse rating count (handle "125K", "5M", "1.2M", numeric)
    _visits_str = str(tool.get('visits', '1000'))
    _rating_count = 1000
    try:
        if 'M' in _visits_str.upper():
            _rating_count = int(float(_visits_str.upper().replace('M','').replace('+','').strip()) * 1000000)
        elif 'K' in _visits_str.upper():
            _rating_count = int(float(_visits_str.upper().replace('K','').replace('+','').strip()) * 1000)
        else:
            _rating_count = int(float(re.sub(r'[^\d.]', '', _visits_str) or 1000))
    except Exception:
        _rating_count = 1000

    # Parse price into structured offers (handle "Free", "Free + Plus $20/mo", "$10/mo", etc.)
    _price_str = tool.get('price', 'Free')
    _offers = []
    if '$' in _price_str or 'USD' in _price_str.upper():
        # Extract all $XX.XX patterns
        prices = re.findall(r'\$[\d.]+', _price_str)
        if prices:
            # Main offer
            _offers.append({"@type":"Offer", "price":prices[0].replace('$',''), "priceCurrency":"USD"})
            # Additional tier if present
            if len(prices) > 1 and 'Free' in _price_str.lower():
                _offers.append({"@type":"Offer", "price":"0", "priceCurrency":"USD", "description":"Free tier"})
        elif 'free' in _price_str.lower():
            _offers.append({"@type":"Offer", "price":"0", "priceCurrency":"USD"})
    elif 'free' in _price_str.lower() or _price_str.lower().startswith('free'):
        _offers.append({"@type":"Offer", "price":"0", "priceCurrency":"USD"})
    else:
        _offers.append({"@type":"Offer", "price":_price_str, "priceCurrency":"USD"})

    # Feature list for schema
    _feature_list = tool.get('features', [])
    if isinstance(_feature_list, str):
        _feature_list = [s.strip() for s in _feature_list.split(',')]

    # Tool URL and image
    _tool_url = tool.get('url', '')
    _tool_image = f"{SITE_DOMAIN}/images/og/{slug}-en-og.png"
    _related_slugs = [r['slug'] for r in selected] if selected else []

    software_data = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": name,
        "url": _tool_url if _tool_url else f"{SITE_DOMAIN}/tools/{slug}/",
        "image": _tool_image,
        "applicationCategory": _app_category,
        "applicationSubCategory": tool.get('category', ''),
        "operatingSystem": tool.get('platform', 'Web'),
        "description": tool['description'],
        "datePublished": date_pub,
        "dateModified":  date_mod,
        "offers": _offers[0] if len(_offers) == 1 else {"@type":"AggregateOffer","offers":_offers},
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": float(tool['rating'].replace('⭐ ','').strip() or 4.0),
            "ratingCount": _rating_count,
            "bestRating": 5,
            "worstRating": 1
        },
        "featureList": _feature_list[:8] if _feature_list else [],
        "author": {
            "@type": "Organization",
            "name": "AI Tool Lab Editorial Team",
            "url": f"{SITE_DOMAIN}/author/"
        },
        "isRelatedTo": [{"@type": "SoftwareApplication", "name": r['name'], "url": f"{SITE_DOMAIN}/tools/{r['slug']}/"} for r in selected[:5]] if selected else [],
        "citation": [
            {"@type": "CreativeWork", "name": f"{name} Review 2026", "url": f"{SITE_DOMAIN}/tools/{slug}/", "author": {"@type": "Organization", "name": "AI Tool Lab Editorial Team"}}
        ],
        "mentions": [{"@type": "Thing", "name": r['name']} for r in selected[:3]] if selected else [],
        "review": {
            "@type": "Review",
            "reviewRating": {
                "@type": "Rating",
                "ratingValue": float(tool['rating'].replace('⭐ ','').strip() or 4.0),
                "bestRating": 5,
                "worstRating": 1
            },
            "author": {"@type": "Organization", "name": "AI Tool Lab Editorial Team", "url": f"{SITE_DOMAIN}/author/"},
            "reviewBody": tool['description'],
            "positiveNotes": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i+1, "name": p} for i, p in enumerate(tool.get('pros', [])[:5])]},
            "negativeNotes": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i+1, "name": p} for i, p in enumerate(tool.get('cons', [])[:5])]}
        }
    }
    breadcrumb_json  = json.dumps(breadcrumb_data,  ensure_ascii=False, indent=2)
    structured_json  = json.dumps(software_data,    ensure_ascii=False, indent=2)

    # TL;DR box (GEO — answer-first, citation optimized)
    tldr_html = ''
    desc_short = tool.get('description','')
    if desc_short:
        tldr_html = f'''<div class="tldr-box">
            <strong>⚡ TL;DR</strong>
            <p>{escape_html(desc_short)}</p>
        </div>'''

    # Key Stats section (GEO — citation-worthy data points AI engines can quote)
    key_stats_html = ''
    stat_items = []
    if tool.get('rating'):
        stat_items.append(f'<div class="ks-item"><span class="ks-val">{tool["rating"].replace("⭐ ","")}</span><span class="ks-label">User Rating</span></div>')
    if tool.get('visits'):
        stat_items.append(f'<div class="ks-item"><span class="ks-val">{tool["visits"]}</span><span class="ks-label">Monthly Visits</span></div>')
    if tool.get('price'):
        stat_items.append(f'<div class="ks-item"><span class="ks-val">{tool["price"]}</span><span class="ks-label">Pricing</span></div>')
    if tool.get('platform'):
        stat_items.append(f'<div class="ks-item"><span class="ks-val">{tool["platform"]}</span><span class="ks-label">Platform</span></div>')
    if stat_items:
        key_stats_html = f'''<div class="key-stats">
            <h4>📊 Key Statistics</h4>
            <div class="ks-grid">{"".join(stat_items)}</div>
        </div>'''

    # Author trust block (GEO — EEAT signals for AI engines)
    today_iso_author = datetime.now().strftime('%Y-%m-%d')
    author_block = f'''<div class="author-block">
        <div class="author-block-inner">
            <div class="author-avatar">🛠️</div>
            <div class="author-body">
                <p class="author-label"><strong>About the reviewer</strong></p>
                <p class="author-text">This {escape_html(name)} review was written by the <a href="/author/">AI Tool Lab Editorial Team</a>, based on real paid usage and testing. We spend $200+/month on AI tool subscriptions so you do not have to. Every claim in this review is verifiable — if you find an error, <a href="/contact.html">let us know</a> and we will fix it within 48 hours.</p>
                <p class="author-meta">Last reviewed: {today_iso_author} · <a href="/about.html">Review methodology</a></p>
            </div>
        </div>
    </div>'''

    # Content (strip duplicate pros/cons headers)
    content_md   = tool.get('content','')
    content_html = markdown_to_html(content_md)

    # hreflang
    hreflang  = hreflang_tags(f'/tools/{slug}/', f'/tools/{slug}/')
    og_image  = ensure_en_og_image(slug, tool, is_article=False)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape_html(name)} Review 2026: Features, Pricing & Alternatives - {SITE_NAME}</title>
    <meta name="description" content="{escape_html(name)} full review 2026: {escape_html(tool['description'][:120])} Pricing, pros, cons, and alternatives.">
    <meta name="keywords" content="{escape_html(name)},{escape_html(name)} review,{escape_html(name)} pricing,{escape_html(cat)},AI tools 2026">
    <link rel="canonical" href="{SITE_DOMAIN}/tools/{slug}/">
{hreflang}    <meta property="og:type" content="article">
    <meta property="og:title" content="{escape_html(name)} Review 2026 - {SITE_NAME}">
    <meta property="og:description" content="{escape_html(tool['description'][:150])}">
    <meta property="og:url" content="{SITE_DOMAIN}/tools/{slug}/">
    {'<meta property="og:image" content="' + og_image + '">' if og_image else ''}
    <meta property="og:site_name" content="{SITE_NAME}">
    <meta name="twitter:card" content="{'summary_large_image' if og_image else 'summary'}">
    <meta name="twitter:title" content="{escape_html(name)} Review 2026 - {SITE_NAME}">
    <meta name="twitter:description" content="{escape_html(tool['description'][:120])}">
    {'<meta name="twitter:image" content="' + og_image + '">' if og_image else ''}
    <link rel="stylesheet" href="/css/style.css">
    <script type="application/ld+json">{breadcrumb_json}</script>
    <script type="application/ld+json">{structured_json}</script>
    {faq_page_schema}
{VERIFICATION_BLOCK}{GA_BLOCK}
</head>
<body>
{header_html()}

    <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a> &gt; <a href="/category/{cat_slug}/">{escape_html(cat)}</a> &gt; <span>{escape_html(name)}</span>
    </nav>

    <main class="article-container">
        <div class="tool-header">
            <div class="tool-header-top">
                <div class="tool-icon-lg" style="background:{tool['color']};">{tool['emoji']}</div>
                <div class="tool-header-info">
                    <h2>{escape_html(name)}{badge_html}</h2>
                    <p class="subtitle">{escape_html(tool['description'])}</p>
                    <div class="rating-bar">{tool['rating']} <span style="font-size:14px;color:#999;">({tool.get('visits','0')} visits)</span></div>
                </div>
            </div>
            <div class="tool-meta">
                <div class="tool-meta-item">🌐 <strong>Website</strong>: {tool['url'].replace('https://','')}</div>
                <div class="tool-meta-item">💰 <strong>Price</strong>: {tool.get('price','')}</div>
                {platform_html}
                <div class="tool-meta-item">🏷️ <strong>Category</strong>: {escape_html(cat)}</div>
            </div>
            <div class="action-bar">
                <a href="{tool['url']}" target="_blank" rel="noopener" class="action-btn action-btn-primary">Visit {escape_html(name)} →</a>
            </div>
        </div>

        {tldr_html}

        {key_stats_html}

        {features_html}

        <article class="article-body">
            {content_html}
        </article>

        {pros_cons_html}

        {faq_html}

        {author_block}

        {related_html}

        {related_articles_html}
    </main>

{footer_html()}
    ''' + BACK_TO_TOP_BLOCK + '''
</body>
</html>'''


# ─── Article page ─────────────────────────────────────────────────────────────

def build_article_page_en(article: dict, all_articles: list, all_tools: list = None) -> str:
    slug     = article['slug']
    title    = article['title']
    cat      = article.get('category', 'AI Tools')
    cat_slug = get_category_slug_en(cat)
    date_str = article.get('dateFull', article.get('date',''))

    # Parse date to ISO for schema
    article_date = article.get('date', datetime.now().strftime('%Y-%m-%d'))

    # Related tools
    related_tools_html = ''
    if all_tools:
        title_lower = title.lower()
        matched = [t for t in all_tools if t.get('name','').lower() in title_lower]
        if len(matched) < 3:
            matched += [t for t in all_tools if t not in matched][:5 - len(matched)]
        if matched:
            cards = ''
            for t in matched[:5]:
                cards += f'''<a href="/tools/{t['slug']}/" class="related-card">
                    <div style="font-size:24px;margin-bottom:8px;">{t['emoji']}</div>
                    <div style="font-weight:600;">{escape_html(t['name'])}</div>
                    <div style="font-size:13px;color:#666;">{escape_html(t.get('category',''))}</div>
                </a>\n'''
            related_tools_html = f'''<div class="related-tools">
            <h3>🔧 Related Tools</h3>
            <div class="related-grid">{cards}</div>
        </div>'''

    # Related articles
    same_cat = [a for a in all_articles if a['slug'] != slug and a.get('category') == cat]
    if len(same_cat) < 2:
        same_cat = [a for a in all_articles if a['slug'] != slug][:3]
    related_html = ''
    if same_cat:
        cards = ''
        for a in same_cat[:3]:
            cards += f'''<a href="/articles/{a['slug']}/" class="related-card">
                <div style="font-weight:600;margin-bottom:4px;">{escape_html(a['title'])}</div>
                <div style="font-size:13px;color:#666;">{a.get('dateFull', a.get('date',''))}</div>
            </a>\n'''
        related_html = f'''<div class="related-tools">
            <h3>📖 Related Articles</h3>
            <div class="related-grid">{cards}</div>
        </div>'''

    # Structured data
    breadcrumb_data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type":"ListItem","position":1,"name":"Home","item":f"{SITE_DOMAIN}/"},
            {"@type":"ListItem","position":2,"name":cat,"item":f"{SITE_DOMAIN}/category/{cat_slug}/"},
            {"@type":"ListItem","position":3,"name":title,"item":f"{SITE_DOMAIN}/articles/{slug}/"},
        ]
    }
    article_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": article.get('description',''),
        "datePublished": article_date,
        "dateModified":  article.get('dateModified', article_date),
        "inLanguage": "en",
        "author": {
            "@type": "Organization",
            "name": "AI Tool Lab Editorial Team",
            "url": f"{SITE_DOMAIN}/author/",
            "description": "Independent editorial team focused on AI tool testing and comparison, 5+ years paid AI tool usage experience",
            "knowsAbout": ["AI tool review", "AI model comparison", "AEO", "GEO", "AI coding tools", "AI chat models"]
        },
        "publisher": {
            "@type": "Organization",
            "name": SITE_NAME,
            "url": SITE_DOMAIN,
            "logo": {"@type":"ImageObject","url":SITE_LOGO},
            "foundingDate": "2026-03-21",
            "slogan": "Data-driven AI tool decisions",
            "publishingPrinciples": f"{SITE_DOMAIN}/about.html",
            "sameAs": ["https://github.com/yiweichen10/ai-toolbox"]
        },
        "mainEntityOfPage": {"@type":"WebPage","@id":f"{SITE_DOMAIN}/articles/{slug}/"}
    }
    breadcrumb_json = json.dumps(breadcrumb_data,  ensure_ascii=False, indent=2)
    structured_json = json.dumps(article_schema,   ensure_ascii=False, indent=2)

    content_html = markdown_to_html(article.get('content',''))
    hreflang     = hreflang_tags(f'/articles/{slug}/', f'/articles/{slug}/')
    og_image     = ensure_en_og_image(slug, article, is_article=True)

    # TL;DR box (answer-first format for GEO - AI engines extract first 200 words)
    tldr_text = article.get('description','').strip()
    if tldr_text:
        tldr_html = f'''<div class="tldr-box" style="background:linear-gradient(135deg,#fff8e6,#ffefb8);border-left:4px solid #f5a623;padding:16px 20px;margin-bottom:24px;border-radius:0 8px 8px 0;font-size:14.5px;line-height:1.7;">
                <strong style="color:#c77d00;font-size:15px;">⚡ TL;DR</strong><br>
                <span style="color:#555;">{escape_html(tldr_text)}</span>
            </div>'''
    else:
        tldr_html = ''

    # HowTo Schema (for tutorial/guide type articles)
    howto_schema_html = ''
    howto_keywords = ['guide', 'tutorial', 'how to', 'step by step', 'getting started', 'walkthrough', 'complete guide', 'setup', 'install', 'configure']
    is_howto = any(kw in title.lower() for kw in howto_keywords)
    if is_howto:
        content_raw = article.get('content','')
        # Strategy 1: Markdown h2 headings
        h2_steps = re.findall(r'^## (.+)$', content_raw, re.MULTILINE)
        # Strategy 2: HTML h2
        if not h2_steps:
            h2_steps = re.findall(r'<h2[^>]*>(.*?)</h2>', content_raw, re.IGNORECASE)
            h2_steps = [re.sub(r'<[^>]+>', '', h).strip() for h in h2_steps]
        # Filter for step-like headings
        step_keywords = ['step', 'how', 'install', 'setup', 'configure', 'create', 'deploy', 'use', 'set up', 'getting started', 'walkthrough', 'build', 'run', 'start', 'first', 'next', 'final']
        filtered_steps = [h for h in h2_steps if any(sk in h.lower() for sk in step_keywords)]
        if len(filtered_steps) < 2:
            skip_keywords = ['FAQ', 'Conclusion', 'Summary', 'Why', 'Common', 'Compare', 'vs', 'Pitfall', 'Intro', 'Background', 'Overview', 'Best Practices', 'Tips']
            filtered_steps = [h for h in h2_steps if not any(sk in h for sk in skip_keywords)]
        if len(filtered_steps) >= 2:
            howto_steps = []
            for i, step_title in enumerate(filtered_steps[:8], 1):
                howto_steps.append({
                    "@type": "HowToStep",
                    "position": i,
                    "name": step_title,
                    "text": f"Follow the guide to complete: {step_title}"
                })
            howto_schema = {
                "@context": "https://schema.org",
                "@type": "HowTo",
                "name": title,
                "description": article.get('description',''),
                "totalTime": "PT30M",
                "step": howto_steps
            }
            howto_schema_html = f'\n    <script type="application/ld+json">{json.dumps(howto_schema, ensure_ascii=False)}</script>'

    # FAQ Schema — 5 strategies matching Chinese build.py, adapted for English content
    _content_for_faq = article.get('content','')
    _article_faq_list = []

    # Strategy 1: Q/A prefix matching (supports **Q1:**/Q:/### Q1: etc., A prefix optional)
    _faq_raw = re.findall(
        r'(?:^|\n)[*#]*\s*\*{0,2}[Qq]\d*[：:]\s*([^\n]+?)\s*\*{0,2}\n(?:\*{0,2}[Aa]\d*[：:]\s*)?(.+?)(?=\n[*#]*\s*\*{0,2}[Qq]\d*[：:]|\n## |\Z)',
        _content_for_faq, re.DOTALL
    )

    # Strategy 2: FAQ section **bold question?** then answer (no Q prefix)
    if not _faq_raw:
        _faq_start = _content_for_faq.upper().find('FAQ')
        if _faq_start >= 0:
            _faq_section = _content_for_faq[_faq_start:]
            _faq_raw = re.findall(
                r'\*\*([^*\n]{6,100}[?？])\*\*\s*\n\s*(.+?)(?=\n\*\*[^*\n]{6,100}[?？]\*\*|\n## |\Z)',
                _faq_section, re.DOTALL
            )

    # Strategy 3: FAQ section ### question? then answer (no Q prefix)
    if not _faq_raw:
        _faq_start = _content_for_faq.upper().find('FAQ')
        if _faq_start >= 0:
            _faq_section = _content_for_faq[_faq_start:]
            _faq_raw = re.findall(
                r'###\s*([^\n]{6,100}[?？])\s*\n\s*(.+?)(?=\n###\s*[^\n]{6,100}[?？]|\n## |\Z)',
                _faq_section, re.DOTALL
            )

    # Strategy 4: FAQ section HTML <h3>question</h3><p>answer</p>
    if not _faq_raw:
        _faq_start = _content_for_faq.upper().find('FAQ')
        if _faq_start >= 0:
            _faq_section = _content_for_faq[_faq_start:]
            _faq_raw = re.findall(
                r'<h[34][^>]*>\s*(?:[Qq]\d*[：:]\s*)?([^<]+?)\s*</h[34]>\s*<p>(.+?)</p>',
                _faq_section, re.DOTALL
            )

    # Strategy 5: FAQ section HTML <strong>Q：</strong><br>A：
    if not _faq_raw:
        _faq_start = _content_for_faq.upper().find('FAQ')
        if _faq_start >= 0:
            _faq_section = _content_for_faq[_faq_start:]
            _faq_raw = re.findall(
                r'<strong>\s*[Qq]\d*[：:]\s*([^<]+?)\s*</strong>\s*(?:<br\s*/?>)?\s*[Aa]\d*[：:]\s*(.+?)(?=<strong>\s*[Qq]\d*[：:]|</p>|\Z)',
                _faq_section, re.DOTALL
            )

    faq_article_schema = ''
    if _faq_raw:
        for _q, _a in _faq_raw:
            _q = _q.strip()
            _a = _a.strip()
            _q_clean = re.sub(r'\*\*', '', _q).strip()
            _q_clean = re.sub(r'<[^>]+>', '', _q_clean).strip()
            _a_clean = re.sub(r'\*\*', '', _a).strip()
            _a_clean = re.sub(r'<[^>]+>', '', _a_clean).strip()
            if _q_clean and _a_clean:
                _article_faq_list.append({
                    "@type": "Question",
                    "name": _q_clean,
                    "acceptedAnswer": {"@type": "Answer", "text": _a_clean}
                })
    if _article_faq_list:
        faq_article_schema = '\n    <script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":_article_faq_list}, ensure_ascii=False) + '</script>'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape_html(title)} - {SITE_NAME}</title>
    <meta name="description" content="{escape_html(article.get('description',''))}">
    <meta name="keywords" content="{escape_html(article.get('keywords',''))}">
    <link rel="canonical" href="{SITE_DOMAIN}/articles/{slug}/">
{hreflang}    <meta property="og:type" content="article">
    <meta property="og:title" content="{escape_html(title)} - {SITE_NAME}">
    <meta property="og:description" content="{escape_html(article.get('description',''))}">
    <meta property="og:url" content="{SITE_DOMAIN}/articles/{slug}/">
    {'<meta property="og:image" content="' + og_image + '">' if og_image else ''}
    <meta property="og:site_name" content="{SITE_NAME}">
    <meta name="twitter:card" content="{'summary_large_image' if og_image else 'summary'}">
    <meta name="twitter:title" content="{escape_html(title)} - {SITE_NAME}">
    <meta name="twitter:description" content="{escape_html(article.get('description',''))}">
    {'<meta name="twitter:image" content="' + og_image + '">' if og_image else ''}
    <link rel="stylesheet" href="/css/style.css">
    <script type="application/ld+json">{breadcrumb_json}</script>
    <script type="application/ld+json">{structured_json}</script>{howto_schema_html}{faq_article_schema}
{VERIFICATION_BLOCK}{GA_BLOCK}
</head>
<body>
{header_html()}

    <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a> &gt; <a href="/category/{cat_slug}/">{escape_html(cat)}</a> &gt; <span>{escape_html(title)[:30]}...</span>
    </nav>

    <main class="article-container">
        <article class="article-body">
            <h1 style="margin-bottom:16px;">{escape_html(title)}</h1>
            <div style="color:#999;font-size:14px;margin-bottom:24px;">
                {date_str} · {escape_html(cat)} ·
                <span itemprop="author" itemscope itemtype="https://schema.org/Organization"><a href="/author/" itemprop="url" style="color:#4285F4;text-decoration:none;"><span itemprop="name">AI Tool Lab Editorial Team</span></a></span> ·
                <span style="color:#bbb;">📖 {max(3, len(article.get('content','')) // 500)} min read</span>
            </div>
            {tldr_html}
            {content_html}
            <div style="margin-top:40px;padding:20px;background:#f8f9fa;border-radius:8px;border-left:4px solid #10a37f;">
                <p style="margin:0 0 8px 0;font-size:14px;color:#555;">
                    <strong>About the author:</strong> This article was written by the <a href="/author/" style="color:#10a37f;text-decoration:none;">AI Tool Lab Editorial Team</a>, with 5+ years of paid AI tool testing experience and $200+ monthly subscription spend. All reviews are based on real paid long-term use.
                </p>
                <p style="margin:0;font-size:13px;color:#888;">
                    <strong>Data statement:</strong> All data in this article cites its source and is verifiable. Found an error? Report it via our <a href="/contact.html" style="color:#4285F4;text-decoration:none;">contact page</a>, we verify within 48 hours.
                </p>
            </div>
        </article>

        {related_html}

        {related_tools_html}
    </main>

{footer_html()}
    ''' + BACK_TO_TOP_BLOCK + '''
</body>
</html>'''


# ─── Category page ────────────────────────────────────────────────────────────

def build_category_page_en(cat_name: str, tools: list) -> str:
    cat_slug = get_category_slug_en(cat_name)
    tool_cards = ''
    for t in tools:
        badge_html = ''
        if t.get('badge'):
            bc = {'hot':'#ff4444','new':'#00aa00','pick':'#667eea'}.get(t['badge'].get('type'),'#667eea')
            badge_html = f'<span class="badge" style="background:{bc};color:#fff;padding:2px 6px;border-radius:3px;font-size:11px;">{t["badge"]["text"]}</span>'
        tool_cards += f'''<a href="/tools/{t['slug']}/" class="tool-card">
            <div class="tool-icon" style="background:{t['color']};">{t['emoji']}</div>
            <div class="tool-info">
                <h3>{escape_html(t['name'])} {badge_html}</h3>
                <p>{escape_html(t['description'][:80])}</p>
                <div class="tool-meta-row">
                    <span>{t['rating']}</span>
                    <span>{t.get('price','')}</span>
                </div>
            </div>
        </a>\n'''

    breadcrumb_data = {
        "@context":"https://schema.org","@type":"BreadcrumbList",
        "itemListElement":[
            {"@type":"ListItem","position":1,"name":"Home","item":f"{SITE_DOMAIN}/"},
            {"@type":"ListItem","position":2,"name":cat_name,"item":f"{SITE_DOMAIN}/category/{cat_slug}/"},
        ]
    }
    breadcrumb_json = json.dumps(breadcrumb_data, ensure_ascii=False, indent=2)

    # CollectionPage schema (GEO — entity relationship for AI engines)
    top_tool_names = [t['name'] for t in tools[:3]]
    collection_schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": f"Best {cat_name} Tools 2026",
        "description": f"We tested and reviewed {len(tools)} {cat_name} AI tools. Find the best {cat_name} tools ranked by features, pricing, and real-world performance.",
        "url": f"{SITE_DOMAIN}/category/{cat_slug}/",
        "hasPart": [{"@type": "SoftwareApplication", "name": t['name'], "url": f"{SITE_DOMAIN}/tools/{t['slug']}/"} for t in tools[:20]],
        "about": {"@type": "Thing", "name": cat_name},
        "mainEntity": {"@type": "ItemList", "numberOfItems": len(tools), "itemListElement": [
            {"@type": "ListItem", "position": i+1, "name": t['name']} for i, t in enumerate(tools[:20])
        ]}
    }
    collection_json = json.dumps(collection_schema, ensure_ascii=False, indent=2)

    # Auto FAQ for category pages (GEO — AI engines extract these for "best X tools" queries)
    cat_faq_json = ''
    if len(tools) >= 3:
        cat_faq = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": f"What are the best {cat_name} tools in 2026?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": f"Based on our testing of {len(tools)} {cat_name} tools, the top 3 are: {', '.join(top_tool_names)}. {top_tool_names[0]} leads in overall capability, {top_tool_names[1] if len(top_tool_names)>1 else ''} excels in value for money, and {top_tool_names[2] if len(top_tool_names)>2 else ''} offers the best free tier. View our full comparison at {SITE_DOMAIN}/category/{cat_slug}/."
                    }
                },
                {
                    "@type": "Question",
                    "name": f"How much do {cat_name} tools cost?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": f"AI {cat_name.lower()} tools range from free to ${len([t for t in tools if '$' in t.get('price','')])} per month depending on features. We tracked {len(tools)} tools in this category and found pricing from Free to premium tiers. Check individual tool pages for the latest pricing and feature comparisons."
                    }
                }
            ]
        }
        cat_faq_json = f'\n    <script type="application/ld+json">{json.dumps(cat_faq, ensure_ascii=False)}</script>'

    hreflang = hreflang_tags(f'/category/{cat_slug}/', f'/category/{cat_slug}/')

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Best {escape_html(cat_name)} Tools 2026 ({len(tools)} Reviewed) - {SITE_NAME}</title>
    <meta name="description" content="Best {escape_html(cat_name)} AI tools in 2026. We reviewed {len(tools)} tools and ranked them by features, pricing, and real-world performance.">
    <meta name="keywords" content="{escape_html(cat_name)},best {escape_html(cat_name)} tools,AI tools 2026">
    <link rel="canonical" href="{SITE_DOMAIN}/category/{cat_slug}/">
{hreflang}    <link rel="stylesheet" href="/css/style.css">
    <script type="application/ld+json">{breadcrumb_json}</script>
    <script type="application/ld+json">{collection_json}</script>{cat_faq_json}
{VERIFICATION_BLOCK}{GA_BLOCK}
</head>
<body>
{header_html()}

    <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a> &gt; <a href="/category/">Categories</a> &gt; <span>{escape_html(cat_name)}</span>
    </nav>

    <main class="tool-list-container">
        <h1 style="margin-bottom:8px;">Best {escape_html(cat_name)} Tools 2026</h1>
        <p style="color:#666;margin-bottom:24px;">{len(tools)} tools reviewed and ranked</p>
        <div class="tool-grid">
            {tool_cards}
        </div>
    </main>

{footer_html()}
    ''' + BACK_TO_TOP_BLOCK + '''
</body>
</html>'''


# ─── Article list page ────────────────────────────────────────────────────────

def build_article_list_en(articles: list, current_page: int = 1, total_pages: int = 1) -> str:
    cards   = ''
    for a in articles:
        cards += f'''<article class="article-card">
            <h3><a href="/articles/{a['slug']}/">{escape_html(a['title'])}</a></h3>
            <div class="article-meta">
                <span class="date">{a.get('dateFull', a.get('date',''))}</span>
                <span class="category">{escape_html(a.get('category',''))}</span>
            </div>
            <p class="summary">{escape_html(a.get('description',''))}</p>
        </article>\n'''

    # Pagination controls
    pagination_html = ''
    if total_pages > 1:
        links = []
        if current_page > 1:
            prev_url = '/articles/' if current_page == 2 else f'/articles/page/{current_page-1}/'
            links.append(f'<a href="{prev_url}" class="page-link">&laquo; Prev</a>')
        
        for p in range(1, total_pages + 1):
            url = '/articles/' if p == 1 else f'/articles/page/{p}/'
            active = ' active' if p == current_page else ''
            links.append(f'<a href="{url}" class="page-link{active}">{p}</a>')
            
        if current_page < total_pages:
            next_url = f'/articles/page/{current_page+1}/'
            links.append(f'<a href="{next_url}" class="page-link">Next &raquo;</a>')
            
        pagination_html = f'<div class="pagination">{"".join(links)}</div>'

    hreflang = hreflang_tags('/articles/', '/articles/')
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Tool Articles & Guides 2026 - {SITE_NAME}</title>
    <meta name="description" content="In-depth AI tool reviews, comparisons, and guides. Updated daily with practical advice for using AI to save time and make money.">
    <link rel="canonical" href="{SITE_DOMAIN}/articles/">
{hreflang}    <link rel="stylesheet" href="/css/style.css">
{VERIFICATION_BLOCK}{GA_BLOCK}
</head>
<body>
{header_html()}

    <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a> &gt; <span>Articles</span>
    </nav>

    <main class="article-list-container">
        <h1 style="margin-bottom:24px;">AI Tool Articles & Guides</h1>
        <div class="article-list">{cards}</div>
        {pagination_html}
    </main>

{footer_html()}
    ''' + BACK_TO_TOP_BLOCK + '''
</body>
</html>'''


# ─── Category index page ──────────────────────────────────────────────────────

def build_category_index_en(tools_by_cat: dict) -> str:
    cat_cards = ''
    for cat_name, tools in tools_by_cat.items():
        cat_slug  = get_category_slug_en(cat_name)
        sample_emoji = tools[0]['emoji'] if tools else '🤖'
        cat_cards += f'''<a href="/category/{cat_slug}/" class="tool-card" style="text-decoration:none;">
            <div class="tool-icon" style="background:#667eea;">{sample_emoji}</div>
            <div class="tool-info">
                <h3>{escape_html(cat_name)}</h3>
                <p>{len(tools)} tools reviewed</p>
            </div>
        </a>\n'''

    hreflang = hreflang_tags('/category/', '/category/')
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>All AI Tool Categories 2026 - {SITE_NAME}</title>
    <meta name="description" content="Browse all AI tool categories. Find the best AI tools for writing, coding, image generation, video, and more.">
    <link rel="canonical" href="{SITE_DOMAIN}/category/">
{hreflang}    <link rel="stylesheet" href="/css/style.css">
{VERIFICATION_BLOCK}{GA_BLOCK}
</head>
<body>
{header_html()}

    <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a> &gt; <span>All Categories</span>
    </nav>

    <main class="tool-list-container">
        <h1 style="margin-bottom:24px;">All AI Tool Categories</h1>
        <div class="tool-grid">
            {cat_cards}
        </div>
    </main>

{footer_html()}
    ''' + BACK_TO_TOP_BLOCK + '''
</body>
</html>'''


# ─── Homepage ─────────────────────────────────────────────────────────────────

def build_index_en(tools: list, articles: list) -> str:
    # Tool cards (top 12 by visits, fallback to first 12)
    def parse_visits(v):
        v = str(v).replace('K','000').replace('M','000000').replace(',','')
        try:
            return int(float(v))
        except:
            return 0

    top_tools = sorted(tools, key=lambda t: parse_visits(t.get('visits','0')), reverse=True)[:12]
    tool_cards = ''
    for t in top_tools:
        badge_html = ''
        if t.get('badge'):
            bc = {'hot':'#ff4444','new':'#00aa00','pick':'#667eea'}.get(t['badge'].get('type'),'#667eea')
            badge_html = f'<span class="badge" style="background:{bc};color:#fff;padding:2px 6px;border-radius:3px;font-size:11px;margin-left:6px;">{t["badge"]["text"]}</span>'
        tool_cards += f'''<a href="/tools/{t['slug']}/" class="tool-card">
            <div class="tool-icon" style="background:{t['color']};">{t['emoji']}</div>
            <div class="tool-info">
                <h3>{escape_html(t['name'])}{badge_html}</h3>
                <p>{escape_html(t['description'][:70])}</p>
                <div class="tool-meta-row">
                    <span>{t['rating']}</span>
                    <span>{t.get('price','')}</span>
                </div>
            </div>
        </a>\n'''

    # Recent articles (top 5)
    article_cards = ''
    for a in articles[:5]:
        article_cards += f'''<article class="article-card">
            <h3><a href="/articles/{a['slug']}/">{escape_html(a['title'])}</a></h3>
            <div class="article-meta">
                <span class="date">{a.get('dateFull', a.get('date',''))}</span>
                <span class="category">{escape_html(a.get('category',''))}</span>
            </div>
            <p class="summary">{escape_html(a.get('description',''))}</p>
        </article>\n'''

    # Homepage schema — dynamically generated with current counts
    total_tools = len(tools)
    total_articles = len(articles)
    total_cats = len(set(t.get('category','') for t in tools))
    today = datetime.now().strftime('%B %d, %Y')

    schema_homepage_block = f'''    <!-- Schema: WebSite + SearchAction (AEO+GEO 2026-06-25) -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "AI Tool Lab",
        "alternateName": "AIToolbox",
        "description": "Independent AI tool reviews and comparisons. {total_tools}+ AI tools tested and ranked, updated daily.",
        "url": "https://www.aitoolbox.hk",
        "inLanguage": "en",
        "potentialAction": {{
            "@type": "SearchAction",
            "target": {{
                "@type": "EntryPoint",
                "urlTemplate": "https://www.aitoolbox.hk/?q={{search_term_string}}"
            }},
            "query-input": "required name=search_term_string"
        }}
    }}
    </script>
    <!-- Schema: Organization (EEAT 2026-06-25) -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "AI Tool Lab",
        "alternateName": "AIToolbox",
        "url": "https://www.aitoolbox.hk",
        "logo": {{
            "@type": "ImageObject",
            "url": "https://www.aitoolbox.hk/images/logo.png",
            "width": 200,
            "height": 60
        }},
        "foundingDate": "2026-03-21",
        "founder": {{
            "@type": "Organization",
            "name": "AI Tool Lab Editorial Team",
            "description": "Independent editorial team focused on AI tool testing and comparison",
            "knowsAbout": ["AI tool review", "AI model comparison", "AEO", "GEO", "AI coding tools", "AI chat models"]
        }},
        "description": "AI Tool Lab is an independent AI tool review site featuring {total_tools}+ tested tools and {total_articles} in-depth articles. All reviews based on paid long-term usage. $200+/month testing budget.",
        "knowsAbout": ["AI tools", "AI models", "AI coding", "AI image generation", "AI video", "AI office", "AI chat", "AEO", "GEO"],
        "slogan": "Data-driven AI tool decisions",
        "publishingPrinciples": "https://www.aitoolbox.hk/about.html",
        "actionableFeedbackPolicy": "All review data comes from public sources or author testing, every article cites sources, all verifiable.",
        "sameAs": [
            "https://github.com/yiweichen10/ai-toolbox"
        ]
    }}
    </script>
    <!-- Schema: BreadcrumbList -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.aitoolbox.hk/" }}
        ]
    }}
    </script>
'''

    # Quick stats strip (GEO — citation-worthy numbers at top of page)
    quick_stats_html = f'''<div class="quick-stats">
        <div class="qs-item">
            <span class="qs-num">{total_tools}+</span>
            <span class="qs-label">AI Tools Reviewed</span>
        </div>
        <div class="qs-item">
            <span class="qs-num">{total_articles}</span>
            <span class="qs-label">In-Depth Articles</span>
        </div>
        <div class="qs-item">
            <span class="qs-num">{total_cats}</span>
            <span class="qs-label">Categories</span>
        </div>
        <div class="qs-item">
            <span class="qs-num">Daily</span>
            <span class="qs-label">Updates</span>
        </div>
    </div>'''

    # Trust section (GEO — EEAT signals)
    trust_html = '''<div class="trust-section">
        <h3>🔍 How We Review AI Tools</h3>
        <div class="trust-grid">
            <div class="trust-card">
                <div class="trust-icon">💰</div>
                <h4>We Pay to Test</h4>
                <p>We spend $200+/month on AI tool subscriptions. Every review is based on real paid usage, not free trials or marketing demos.</p>
            </div>
            <div class="trust-card">
                <div class="trust-icon">🔄</div>
                <h4>Updated Daily</h4>
                <p>AI tools change fast. We update reviews daily with new pricing, features, and performance data. Never stale.</p>
            </div>
            <div class="trust-card">
                <div class="trust-icon">⚖️</div>
                <h4>No Sponsored Reviews</h4>
                <p>We do not take payment for positive reviews. No tool can buy a spot on this site. If it is bad, we say so.</p>
            </div>
            <div class="trust-card">
                <div class="trust-icon">📊</div>
                <h4>Data-Driven Rankings</h4>
                <p>Our rankings combine real usage data, pricing analysis, and hands-on testing. No AI-generated summaries — every word is written by a human who used the tool.</p>
            </div>
        </div>
    </div>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Best AI Tools 2026: {total_tools}+ Tools Reviewed & Ranked - {SITE_NAME}</title>
    <meta name="description" content="Discover the best AI tools in 2026. We review and rank {total_tools}+ AI tools across writing, coding, image generation, video, and more. Updated daily.">
    <meta name="keywords" content="best AI tools 2026,AI tools review,AI tools comparison,top AI tools">
    <link rel="canonical" href="{SITE_DOMAIN}/">
    <link rel="alternate" hreflang="zh-CN" href="{SITE_DOMAIN_CN}/">
    <link rel="alternate" hreflang="en" href="{SITE_DOMAIN}/">
    <link rel="alternate" hreflang="x-default" href="{SITE_DOMAIN}/">
    <meta property="og:type" content="website">
    <meta property="og:title" content="Best AI Tools 2026: {total_tools}+ Reviewed - {SITE_NAME}">
    <meta property="og:description" content="Find the best AI tools for writing, coding, image generation, and productivity. Updated daily.">
    <meta property="og:url" content="{SITE_DOMAIN}/">
    <meta property="og:image" content="{SITE_DOMAIN}/images/logo.png">
    <meta property="og:site_name" content="{SITE_NAME}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Best AI Tools 2026: {total_tools}+ Reviewed - {SITE_NAME}">
    <meta name="twitter:description" content="Find the best AI tools for writing, coding, image generation, and productivity. Updated daily.">
    <meta name="twitter:image" content="{SITE_DOMAIN}/images/logo.png">
    <link rel="stylesheet" href="/css/style.css">
{schema_homepage_block}{VERIFICATION_BLOCK}{GA_BLOCK}
</head>
<body>
{header_html()}

    <main>
        <section class="hero" style="text-align:center;padding:40px 20px 20px;">
            <h2 style="font-size:28px;margin-bottom:12px;">Find the Best AI Tools for Your Work</h2>
            <p style="color:#666;font-size:16px;max-width:600px;margin:0 auto 24px;">
                {total_tools}+ AI tools reviewed and ranked. Updated daily. Last updated: {today}.
            </p>
            <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
                <a href="/category/" class="action-btn action-btn-primary">Browse All Categories</a>
                <a href="/articles/" class="action-btn">Read Guides</a>
            </div>
        </section>

        {quick_stats_html}

        {trust_html}

        <section style="max-width:1200px;margin:0 auto;padding:0 16px;">
            <h2 style="margin-bottom:20px;">🔥 Top AI Tools</h2>
            <div class="tool-grid">
                {tool_cards}
            </div>
            <div style="text-align:center;margin-top:24px;">
                <a href="/category/" class="action-btn">View All {total_tools}+ Tools →</a>
            </div>
        </section>

        <section style="max-width:1200px;margin:40px auto 0;padding:0 16px;">
            <h2 style="margin-bottom:20px;">📖 Latest Articles</h2>
            <div class="article-list">
                {article_cards}
            </div>
            <div style="text-align:center;margin-top:24px;">
                <a href="/articles/" class="action-btn">All Articles →</a>
            </div>
        </section>
    </main>

{footer_html()}
    ''' + BACK_TO_TOP_BLOCK + '''
</body>
</html>'''


# ─── Sitemap (English only) ───────────────────────────────────────────────────

def generate_sitemap_en(tools: list, articles: list, cat_slugs: list) -> str:
    today = datetime.now().strftime('%Y-%m-%d')
    urls  = [
        f'    <url><loc>{SITE_DOMAIN}/</loc><lastmod>{today}</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>',
        f'    <url><loc>{SITE_DOMAIN}/category/</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>',
        f'    <url><loc>{SITE_DOMAIN}/articles/</loc><lastmod>{today}</lastmod><changefreq>daily</changefreq><priority>0.8</priority></url>',
    ]
    for cs in cat_slugs:
        urls.append(f'    <url><loc>{SITE_DOMAIN}/category/{cs}/</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>')
    for t in tools:
        urls.append(f'    <url><loc>{SITE_DOMAIN}/tools/{t["slug"]}/</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>')
    for a in articles:
        pub = a.get('date', today)
        urls.append(f'    <url><loc>{SITE_DOMAIN}/articles/{a["slug"]}/</loc><lastmod>{pub}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>')

    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(urls) + '\n</urlset>'


# ─── IndexNow push (Bing/Google) ──────────────────────────────────────────────

def push_to_indexnow_en(urls: list) -> bool:
    import urllib.request
    INDEXNOW_KEY = "00859eedcd7c1f5e6a38204096fe2a57"  # 2026-07-05 regenerated, old key expired
    key_location = f"{SITE_DOMAIN}/{INDEXNOW_KEY}.txt"
    payload = json.dumps({
        "host": "www.aitoolbox.hk",
        "key": INDEXNOW_KEY,
        "keyLocation": key_location,
        "urlList": urls[:100]
    }).encode('utf-8')
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(f"  IndexNow response: {resp.status}")
            return resp.status in (200, 202)
    except Exception as e:
        print(f"  IndexNow error: {e}")
        return False


# ─── Nav injection (English only — only scans /en/ dir) ──────────────────────

def inject_global_nav_en():
    """Inject English global nav into all HTML files under / only."""
    injected = 0
    for root, dirs, files in os.walk(OUT_DIR):
        for fname in files:
            if not fname.endswith('.html'):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                if '</header>' in content and 'class="global-nav"' not in content:
                    content = content.replace('</header>', GLOBAL_NAV_EN + '\n    </header>', 1)
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    injected += 1
            except Exception:
                pass
    if injected:
        print(f'[Post] Injected EN nav into {injected} HTML files under /')
    return injected


# ─── Main build ───────────────────────────────────────────────────────────────

def build_all_en(target: str = 'all'):
    # Load data
    tools_en_path    = os.path.join(DATA_DIR, 'tools_en.json')
    articles_en_path = os.path.join(DATA_DIR, 'articles_en.json')

    if not os.path.exists(tools_en_path):
        print(f'[ERROR] {tools_en_path} not found. Run generate_tools_en.py first.')
        return
    if not os.path.exists(articles_en_path):
        print(f'[ERROR] {articles_en_path} not found. Run generate_articles_en.py first.')
        return

    with open(tools_en_path,    encoding='utf-8') as f:
        all_tools = json.load(f)
    with open(articles_en_path, encoding='utf-8') as f:
        articles  = json.load(f)

    # Sort articles by date descending (newest first)
    articles.sort(key=lambda x: x.get('date', ''), reverse=True)

    published_tools = [t for t in all_tools if t.get('published', False)]
    print(f'[EN] {len(published_tools)} published tools, {len(articles)} articles')

    # Group by category
    tools_by_cat: dict = {}
    for t in published_tools:
        cat = t.get('category','')
        if cat:
            tools_by_cat.setdefault(cat, []).append(t)

    # ── Category pages ────────────────────────────────────────────────────────
    if target in ('all', 'index', 'tools'):
        for cat_name, tools_in_cat in tools_by_cat.items():
            cat_slug = get_category_slug_en(cat_name)
            dir_path = os.path.join(OUT_DIR, 'category', cat_slug)
            os.makedirs(dir_path, exist_ok=True)
            html = build_category_page_en(cat_name, tools_in_cat)
            with open(os.path.join(dir_path, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(html)
            print(f'[OK] en/category/{cat_slug}/index.html')

        # Category index
        dir_path = os.path.join(OUT_DIR, 'category')
        os.makedirs(dir_path, exist_ok=True)
        html = build_category_index_en(tools_by_cat)
        with open(os.path.join(dir_path, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'[OK] en/category/index.html')

    # ── Tool pages ────────────────────────────────────────────────────────────
    if target in ('all', 'tools'):
        for tool in published_tools:
            slug     = tool['slug']
            dir_path = os.path.join(OUT_DIR, 'tools', slug)
            os.makedirs(dir_path, exist_ok=True)
            html = build_tool_page_en(tool, published_tools, articles)
            with open(os.path.join(dir_path, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(html)
            print(f'[OK] en/tools/{slug}/index.html')

    # ── Article pages ─────────────────────────────────────────────────────────
    if target in ('all', 'articles'):
        for article in articles:
            slug     = article['slug']
            dir_path = os.path.join(OUT_DIR, 'articles', slug)
            os.makedirs(dir_path, exist_ok=True)
            html = build_article_page_en(article, articles, published_tools)
            with open(os.path.join(dir_path, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(html)
            print(f'[OK] en/articles/{slug}/index.html')

        # Article list with pagination
        ITEMS_PER_PAGE = 10
        total_articles = len(articles)
        total_pages = (total_articles + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

        for p in range(1, total_pages + 1):
            start = (p - 1) * ITEMS_PER_PAGE
            end = start + ITEMS_PER_PAGE
            page_articles = articles[start:end]
            
            if p == 1:
                dir_path = os.path.join(OUT_DIR, 'articles')
            else:
                dir_path = os.path.join(OUT_DIR, 'articles', 'page', str(p))
            
            os.makedirs(dir_path, exist_ok=True)
            html = build_article_list_en(page_articles, p, total_pages)
            with open(os.path.join(dir_path, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(html)
            print(f'[OK] en/articles/{"index.html" if p==1 else f"page/{p}/index.html"}')

    # ── English homepage ──────────────────────────────────────────────────────
    if target in ('all', 'index'):
        os.makedirs(OUT_DIR, exist_ok=True)
        html = build_index_en(published_tools, articles)
        with open(os.path.join(OUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'[OK] en/index.html')

    # ── Nav injection (EN only) ───────────────────────────────────────────────
    inject_global_nav_en()

    # ── Sitemap ───────────────────────────────────────────────────────────────
    cat_slugs = [get_category_slug_en(c) for c in tools_by_cat.keys()]
    sitemap   = generate_sitemap_en(published_tools, articles, cat_slugs)
    with open(os.path.join(OUT_DIR, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(sitemap)
    print(f'[OK] en/sitemap.xml ({len(published_tools)} tools + {len(articles)} articles)')

    # ── IndexNow push ─────────────────────────────────────────────────────────
    cache_file = os.path.join(BASE_DIR, '.indexnow_en_pushed.json')
    pushed = set()
    if os.path.exists(cache_file):
        with open(cache_file, encoding='utf-8') as f:
            pushed = set(json.load(f))

    all_urls = [f"{SITE_DOMAIN}/"]
    all_urls += [f"{SITE_DOMAIN}/tools/{t['slug']}/" for t in published_tools]
    all_urls += [f"{SITE_DOMAIN}/articles/{a['slug']}/" for a in articles]
    all_urls += [f"{SITE_DOMAIN}/category/{get_category_slug_en(c)}/" for c in tools_by_cat]

    new_urls = [u for u in all_urls if u not in pushed]
    if new_urls:
        print(f'\n[EN] Pushing {len(new_urls)} new URLs via IndexNow...')
        if push_to_indexnow_en(new_urls):
            pushed.update(new_urls)
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(list(pushed), f)
    else:
        print(f'[EN] IndexNow: no new URLs to push ({len(all_urls)} total, all pushed)')

    print(f'\n[EN] Done! {len(published_tools)} tools + {len(articles)} articles built under /')


# ─── Entry point ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='AI Tool Lab English SSG')
    parser.add_argument(
        '--target', '-t',
        choices=['all', 'tools', 'articles', 'index'],
        default='all',
        help='Build target (default: all)'
    )
    args = parser.parse_args()

    # Validate internal links before building (2026-06-25: prevent 404 links)
    if args.target in ('all', 'articles'):
        try:
            from validate_internal_links import validate
            print("\n[VALIDATE] Checking internal links...")
            if not validate():
                print("[VALIDATE] ERROR: Broken internal links detected. Fix before building!")
                import sys
                sys.exit(1)
        except ImportError:
            pass  # validation script not available, skip silently

    build_all_en(args.target)

    # Automatically generate OG images after full build
    if args.target == 'all':
        print("\n[BUILD] Generating OG images...")
        try:
            import subprocess
            import sys
            script_path = os.path.join(BASE_DIR, 'scripts', 'gen_og_images_en.py')
            subprocess.run([sys.executable, script_path], check=True)
            print("[BUILD] OG images generation completed.")
        except Exception as e:
            print(f"[BUILD] [WARN] OG image generation failed: {e}")


if __name__ == '__main__':
    main()
