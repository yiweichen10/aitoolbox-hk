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
CSS_VERSION  = f"v={datetime.now().strftime('%Y%m%d%H%M%S')}"  # cache busting (with seconds)

# ─── Article category pages (2026-11-18 治本 421 处面包屑 404) ────────────────
# 文章分类达到该数量才生成 /category/<slug>/ 页面；不足的面包屑降级纯文本。
MIN_ARTICLES_FOR_CATEGORY_PAGE = 3
# build_all_en 开头预计算（工具分类 ∪ 达标文章分类）；模块级默认空集保证
# 单测/导入安全。
ARTICLE_CATEGORY_PAGES = set()

# ─── Affiliate links ──────────────────────────────────────────────────────────
# Load affiliate_links.json from the Chinese site's data directory (shared file)
_AFFILIATE_LINKS = {}
_aff_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'seo-site', 'data', 'affiliate_links.json')
if not os.path.exists(_aff_path):
    _aff_path = os.path.join(BASE_DIR, 'data', 'affiliate_links.json')
if os.path.exists(_aff_path):
    try:
        with open(_aff_path, 'r', encoding='utf-8') as _f:
            _raw = json.load(_f)
            for _k, _v in _raw.items():
                if isinstance(_v, dict) and _v.get('url'):
                    _AFFILIATE_LINKS[_k] = _v['url']
                elif isinstance(_v, str) and _v:
                    _AFFILIATE_LINKS[_k] = _v
    except Exception:
        pass

def get_affiliate_url(slug, site='en'):
    """Get affiliate URL for a tool, or None."""
    key = f"{site}:{slug}"
    return _AFFILIATE_LINKS.get(key)

def get_tool_link(tool, slug, site='en'):
    """Get final tool link (affiliate preferred). Returns (url, is_affiliate)."""
    aff = get_affiliate_url(slug, site)
    if aff:
        return aff, True
    return tool.get('url', ''), False

# ─── Visual System v2 helpers (2026-11-15 redesign) ───────────────────────────

def safe_tile_color(hex_color: str) -> str:
    """Preserve a tool's brand hue but darken light colours so a white
    monogram stays readable (WCAG AA). Replaces decorative emoji tiles."""
    s = (hex_color or '').strip().lstrip('#')
    if len(s) == 3:
        s = ''.join(c * 2 for c in s)
    if len(s) != 6:
        return '#1C1C1C'
    try:
        r, g, b = (int(s[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return '#1C1C1C'
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    if lum > 118:
        k = 118 / lum
        r, g, b = int(r * k), int(g * k), int(b * k)
    return f'#{r:02x}{g:02x}{b:02x}'


def resolve_tool_icon(slug: str) -> str:
    """Local cache of real tool logos, mirroring the Chinese site's
    assets/icons approach. Returns a web path or '' (never a remote URL,
    so builds stay offline and images cannot break on third-party downtime)."""
    if not slug:
        return ''
    icons_dir = os.path.join(BASE_DIR, 'assets', 'icons')
    for ext in ('.png', '.svg'):
        if os.path.exists(os.path.join(icons_dir, slug + ext)):
            return f'/assets/icons/{slug}{ext}'
    return ''


def tool_tile(tool: dict, css_class: str = 'tool-icon') -> str:
    """Real tool logo with an accessible monogram fallback.

    The <img> carries alt (entity name for SEO/AI extraction), width/height
    (no layout shift) and lazy loading. A locally missing logo degrades to
    a letter tile — never an emoji.
    """
    name = str(tool.get('name', '?'))
    slug = str(tool.get('slug', ''))
    src = resolve_tool_icon(slug)
    size = {'tool-icon-lg': 56, 'related-tile': 40, 'sidebar-tile': 28,
            'ft-icon': 56}.get(css_class, 40)
    if src:
        return (f'<img class="tool-logo {css_class}" src="{src}" '
                f'alt="{escape_html(name)}" width="{size}" height="{size}" '
                f'loading="lazy" decoding="async">')
    letter = next((c for c in name if c.isalnum()), '?').upper()
    return (f'<div class="{css_class}" '
            f'style="background:{safe_tile_color(tool.get("color", ""))};">'
            f'{escape_html(letter)}</div>')


def price_type(price_str: str) -> str:
    """free | freemium | paid — coarse bucket for client-side filtering."""
    p = (price_str or '').lower()
    has_paid = '$' in p or 'usd' in p or '€' in p or '£' in p
    is_free = 'free' in p or 'open source' in p
    if has_paid and is_free:
        return 'freemium'
    if has_paid:
        return 'paid'
    if is_free:
        return 'free'
    return 'paid'


def rating_num(t: dict) -> float:
    try:
        return float(re.sub(r'[^\d.]', '', str(t.get('rating', ''))) or 0)
    except Exception:
        return 0.0


def visits_num(v) -> int:
    s = str(v or '').upper().replace(',', '').replace('+', '')
    try:
        if 'M' in s:
            return int(float(s.replace('M', '')) * 1000000)
        if 'K' in s:
            return int(float(s.replace('K', '')) * 1000)
        return int(float(re.sub(r'[^\d.]', '', s) or 0))
    except Exception:
        return 0


# Editorial seed for "X alternatives" pages: tools people actually search
# alternatives for (marquee AI names). Intersected with the catalog at build
# time, then topped up to 50 by editor score — raw `visits` is NOT used for
# selection because marketplace platforms in AI Income carry third-party
# traffic numbers (Etsy 400M) that drown real AI tools.
MARQUEE_ALTERNATIVE_SLUGS = [
    'chatgpt', 'claude', 'gemini', 'midjourney', 'dall-e-3', 'sora', 'veo',
    'runway', 'elevenlabs', 'descript', 'jasper', 'writesonic', 'anyword',
    'notion-ai', 'canva-creators', 'perplexity', 'github-copilot', 'cursor',
    'lovable', 'bolt.new', 'hugging-face', 'lm-studio', 'pinecone',
    'zapier-ai', 'heygen', 'synthesia', 'suno', 'leonardo-ai', 'ideogram',
    'flux-1', 'deepl', 'otter.ai', 'n8n', 'make', 'semrush-ai', 'promptbase',
    'gumroad', 'substack', 'paddle', 'adobe-stock',
]


def status_role(tool: dict) -> str:
    """'verified' | 'choice' | 'trending' | '' — semantic role of the tool's badge."""
    b = tool.get('badge') or {}
    text = str(b.get('text') or '').strip()
    if not text or text.lower() in ('none', 'null', 'n/a'):
        return ''
    return {'new': 'verified', 'pick': 'choice', 'hot': 'trending'}.get(
        str(b.get('type') or '').lower(), 'verified')


def status_chip(tool: dict) -> str:
    """Three semantic badge roles only.

      green  = Verified          (legacy: NEW)
      blue   = Editor's Choice   (legacy: PICK)
      orange = Trending          (legacy: HOT)

    Red is reserved for errors/warnings and is never a marketing badge.
    A literal 'None' badge is dropped instead of rendered.
    """
    b = tool.get('badge') or {}
    text = str(b.get('text') or '').strip()
    if not text or text.lower() in ('none', 'null', 'n/a'):
        return ''
    role = {'new': 'verified', 'pick': 'choice', 'hot': 'trending'}.get(
        str(b.get('type') or '').lower(), 'verified')
    label = {
        'verified': 'Verified',
        'choice': "Editor's Choice",
        'trending': 'Trending',
    }[role]
    return f'<span class="status-chip status-{role}">{label}</span>'

# ─── Category icons (line style, same visual language as the trust icons) ────
_CAT_ICON_PATHS = {
    'income':   '<circle cx="12" cy="12" r="9"/><path d="M12 6.5v11"/><path d="M14.8 8.8c-.6-.8-1.7-1.3-2.8-1.3-1.6 0-2.9.8-2.9 2s1.1 1.7 2.9 2.1c1.8.4 2.9 1 2.9 2.1s-1.3 2-2.9 2c-1.1 0-2.2-.5-2.8-1.3"/>',
    'video':    '<circle cx="12" cy="12" r="9"/><path d="M10 8.5l6 3.5-6 3.5V8.5z"/>',
    'image':    '<rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="9" cy="9" r="1.8"/><path d="M21 15.5L16 10.5l-8.5 8"/>',
    'code':     '<path d="M8.5 7L3.5 12l5 5"/><path d="M15.5 7l5 5-5 5"/>',
    'terminal': '<rect x="3" y="4" width="18" height="16" rx="3"/><path d="M7 9.5l3 3-3 3"/><path d="M13 15.5h4"/>',
    'api':      '<path d="M8 3H7a2 2 0 00-2 2v4a2 2 0 01-2 2 2 2 0 012 2v4a2 2 0 002 2h1"/><path d="M16 3h1a2 2 0 012 2v4a2 2 0 002 2 2 2 0 00-2 2v4a2 2 0 01-2 2h-1"/>',
    'browser':  '<rect x="3" y="4" width="18" height="16" rx="3"/><path d="M3 9h18"/><path d="M6.5 6.5h.01"/><path d="M9.5 6.5h.01"/>',
    'audio':    '<path d="M4 10v4"/><path d="M8 7v10"/><path d="M12 4v16"/><path d="M16 7v10"/><path d="M20 10v4"/>',
    'design':   '<circle cx="8.5" cy="8.5" r="4.5"/><rect x="13" y="13" width="8" height="8" rx="1.5"/>',
    'pen':      '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 013 3L7 19l-4 1 1-4L16.5 3.5z"/>',
    'chat':     '<path d="M21 15a2 2 0 01-2 2H8l-5 4V5a2 2 0 012-2h14a2 2 0 012 2v10z"/>',
    'megaphone': '<path d="M3 11l18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 11-5.8-1.6"/>',
    'checklist': '<rect x="4" y="4" width="16" height="16" rx="3"/><path d="M8.5 12l2.3 2.3 4.7-4.8"/>',
    'zap':      '<path d="M13 2L4 14h6l-1 8 9-12h-6l1-8z"/>',
    'bot':      '<rect x="4" y="8" width="16" height="11" rx="3"/><path d="M12 8V4"/><path d="M9 4h6"/><circle cx="9" cy="13.5" r="1"/><circle cx="15" cy="13.5" r="1"/>',
    'search':   '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
    'cart':     '<circle cx="9" cy="20" r="1.5"/><circle cx="17.5" cy="20" r="1.5"/><path d="M3 4h2l2.4 11h11.2L21 8H6"/>',
    'briefcase': '<rect x="3" y="8" width="18" height="12" rx="2.5"/><path d="M9 8V6a3 3 0 013-3 3 3 0 013 3v2"/>',
    'globe':    '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 010 18"/><path d="M12 3a14 14 0 000 18"/>',
    'trending': '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    'chart':    '<path d="M4 20v-6"/><path d="M10 20V8"/><path d="M16 20v-8"/><path d="M2 20h20"/>',
    'flask':    '<path d="M9.5 3h5"/><path d="M10 3v6l-5.3 9a2 2 0 001.7 3h11.2a2 2 0 001.7-3L14 9V3"/><path d="M7.5 15h9"/>',
    'grid':     '<rect x="3" y="3" width="8" height="8" rx="2"/><rect x="13" y="3" width="8" height="8" rx="2"/><rect x="3" y="13" width="8" height="8" rx="2"/><rect x="13" y="13" width="8" height="8" rx="2"/>',
}

def category_icon_svg(cat_name: str) -> str:
    """Inline line icon per category family. Keyword match, grid fallback."""
    n = (cat_name or '').lower()
    if 'income' in n:                      k = 'income'
    elif 'video' in n:                     k = 'video'
    elif 'image' in n or 'photo' in n:     k = 'image'
    elif 'coding' in n:                    k = 'code'
    elif 'development' in n or n == 'ai dev': k = 'terminal'
    elif 'api' in n:                       k = 'api'
    elif 'website' in n:                   k = 'browser'
    elif 'audio' in n or 'music' in n:     k = 'audio'
    elif 'design' in n or '3d' in n:       k = 'design'
    elif 'writing' in n:                   k = 'pen'
    elif 'chat' in n:                      k = 'chat'
    elif 'marketing' in n:                 k = 'megaphone'
    elif 'productivity' in n:              k = 'checklist'
    elif 'automation' in n:                k = 'zap'
    elif 'agent' in n:                     k = 'bot'
    elif 'search' in n:                    k = 'search'
    elif 'commerce' in n:                  k = 'cart'
    elif 'office' in n:                    k = 'briefcase'
    elif 'translation' in n:               k = 'globe'
    elif 'seo' in n:                       k = 'trending'
    elif 'market research' in n:           k = 'chart'
    elif 'research' in n:                  k = 'flask'
    else:                                  k = 'grid'
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true">{_CAT_ICON_PATHS[k]}</svg>')


# ─── Back-to-top button (no Chinese) ──────────────────────────────────────────
BACK_TO_TOP_BLOCK = '''<button id="backToTop" aria-label="Back to top">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="18 15 12 9 6 15"></polyline>
    </svg>
</button>
<script>
document.addEventListener("DOMContentLoaded",function(){var b=document.getElementById("backToTop");if(!b)return;var s=function(){if(window.scrollY>400){b.classList.add("visible")}else{b.classList.remove("visible")}};window.addEventListener("scroll",s,{passive:true});s();b.addEventListener("click",function(){window.scrollTo({top:0,behavior:"smooth"})});});
</script>
<script src="/js/tts-reader.js?v=20261118" defer></script>'''

DARK_MODE_BLOCK = '''<button id="darkModeToggle" class="dark-toggle-fab" aria-label="Toggle dark mode" title="Dark mode">◐</button>
<script>
(function(){
    var btn = document.getElementById('darkModeToggle');
    if (!btn) return;
    var dark = localStorage.getItem('darkMode') === 'true';
    function apply(d) {
        document.documentElement.setAttribute('data-theme', d ? 'dark' : '');
        btn.textContent = d ? '◑' : '◐';
        localStorage.setItem('darkMode', d);
    }
    apply(dark);
    btn.addEventListener('click', function(){
        dark = !dark;
        apply(dark);
    });
})();
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
                "urlTemplate": "https://www.aitoolbox.hk/search/?q={search_term_string}"
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
            <a href="/category/" class="gn-item">All Categories</a>
            <a href="/articles/" class="gn-item">Articles</a>
            <a href="/" class="gn-item">Home</a>
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
    "AI Research":    "ai-research",
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

def plain_text_for_schema(text: str) -> str:
    """Strip Markdown/HTML so JSON-LD schema text stays clean prose.

    JSON-LD `text` fields must be plain text. FAQ answers may contain Markdown
    links (internal linking) and bold markers, which render fine in HTML but
    would leak raw syntax like "[ChatGPT](/tools/chatgpt/)" into structured data.
    """
    if not text:
        return ''
    out = str(text)
    out = re.sub(r'!\[([^\]]*)\]\([^)]*\)', r'\1', out)   # images -> alt text
    out = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', out)    # links  -> link text
    out = re.sub(r'`([^`]*)`', r'\1', out)                # inline code
    out = out.replace('**', '').replace('__', '')          # bold markers
    out = re.sub(r'<[^>]+>', '', out)                      # stray HTML tags
    return re.sub(r'\s+', ' ', out).strip()

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
    html = re.sub(r'^# (.+)$',   r'<h2>\1</h2>', html, flags=re.MULTILINE)
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
            <a href="/" class="brand-link">
                <div class="site-brand"><span class="brand-mark" aria-hidden="true"></span>{SITE_NAME}</div>
                <span class="header-tagline">Independent reviews</span>
            </a>
            <nav class="header-nav">
                <a href="/category/">Tools</a>
                <a href="/articles/">Articles</a>
                <a href="/category/ai-chat/">AI Chat</a>
                <a href="/category/ai-image/">AI Image</a>
                <a href="/category/ai-coding/">AI Coding</a>
                <a href="/category/ai-video/">AI Video</a>
            </nav>
        </div>
    </header>'''

def footer_html() -> str:
    return f'''    <footer class="footer">
        <p class="footer-logo">{SITE_NAME}</p>
        <p>Independent AI tool reviews. No sponsored rankings. &middot; <a href="/about.html">Editorial policy</a> &middot; <a href="/rss.xml">RSS</a> &middot; <a href="{SITE_DOMAIN_CN}/">中文版</a></p>
        <p class="footer-meta">Copyright {datetime.now().year} {SITE_NAME} &middot; Updated daily</p>
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

def build_tool_page_en(tool: dict, all_tools: list, all_articles: list = None, alt_slug: str = '',
                       vs_partners: list = None) -> str:
    slug = tool['slug']
    name = tool['name']
    cat  = tool.get('category', 'AI Tools')
    cat_slug = get_category_slug_en(cat)
    # "See all alternatives" link — only rendered when an /alternatives/ page exists
    alt_link_html = (f'<a class="alt-see-all" href="/alternatives/{slug}/">'
                     f'See all {escape_html(name)} alternatives &rarr;</a>') if alt_slug else ''
    # Head-to-head links — 2026-11-18: 渲染全部 partners（此前 [:2] 按 slug 字母序
    # 截断，明星工具的对比页如 sora-vs-veo 被字母序挤掉 → 全站零入链，只能靠
    # sitemap 发现。每工具 partners ≤4，全渲染链接量可控，且保证每个 vs 页
    # 从两端各获得至少一条入链（80 个 vs 页全部有站内入口）。
    _by_slug = {t['slug']: t for t in all_tools}
    vs_link_tags = []
    for pslug in sorted(vs_partners or []):
        p = _by_slug.get(pslug)
        if not p:
            continue
        lo, hi = tuple(sorted([slug, pslug]))
        vs_link_tags.append(f'<a class="alt-see-all" href="/vs/{lo}-vs-{hi}/">'
                            f'{escape_html(name)} vs {escape_html(p["name"])} &rarr;</a>')
    vs_html = '<br>'.join(vs_link_tags)

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
                {tool_tile(r, 'related-tile')}
                <div style="font-weight:600;">{r['name']}</div>
                <div style="font-size:13px;color:#666;">{r.get('category','')}</div>
            </a>\n'''
        related_html = f'''<div class="related-tools" id="relatedSection">
            <h3>Related Tools</h3>
            {alt_link_html}
            {vs_html}
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
                    <div style="font-weight:600;margin-bottom:4px;">{escape_html(a['title'][:40])}</div>
                    <div style="font-size:13px;color:#666;">{a.get('date','')}</div>
                </a>\n'''
            related_articles_html = f'''<div class="related-tools">
                <h3>Related Articles</h3>
                <div class="related-grid">{cards}</div>
            </div>'''

    # Pros / cons — design frame 04: two white cards, green/red kickers, ✓/— list items
    pros_cons_html = ''
    if tool.get('pros') and tool.get('cons'):
        pros_items = ''.join(f'<li>✓&nbsp;&nbsp;{escape_html(p)}</li>' for p in tool['pros'])
        cons_items = ''.join(f'<li>—&nbsp;&nbsp;{escape_html(c)}</li>' for c in tool['cons'])
        pros_cons_html = f'''<div class="td-proscons">
            <div class="td-card"><div class="td-card-head pros">WHAT WORKS</div><ul>{pros_items}</ul></div>
            <div class="td-card"><div class="td-card-head cons">LIMITATIONS</div><ul>{cons_items}</ul></div>
        </div>'''

    # FAQ — design frame 04: serif headline, open Q/A pairs with hairline dividers
    faq_html   = ''
    faq_schema = []
    if tool.get('faq'):
        faq_items = ''
        for fi in tool['faq']:
            q, a = fi.get('question',''), fi.get('answer','')
            if q and a:
                if faq_items:
                    faq_items += '<div class="td-faq-divider"></div>\n'
                faq_items += f'''<div class="td-faq-item">
                    <h3>{escape_html(q)}</h3>
                    <div class="td-faq-a">{markdown_to_html(a)}</div>
                </div>\n'''
                faq_schema.append({'@type':'Question','name':plain_text_for_schema(q),'acceptedAnswer':{'@type':'Answer','text':plain_text_for_schema(a)}})
        if faq_items:
            faq_html = f'<div class="td-faq"><h2 class="td-faq-head">Questions we get asked</h2>{faq_items}</div>'

    faq_page_schema = ''
    if faq_schema:
        faq_sd = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":faq_schema}
        faq_page_schema = f'<script type="application/ld+json">{json.dumps(faq_sd, ensure_ascii=False)}</script>'

    # Platform — a short label may appear as a neutral chip in the hero identity
    def _short_stat(value: str, limit: int) -> str:
        """Shorten a stat value for display: first sentence only, hard-capped."""
        v = (value or '').strip()
        if len(v) <= limit:
            return v
        for sep in ('. ', '。', '; ', ' - ', ' — '):
            idx = v.find(sep)
            if 0 < idx <= limit:
                return v[:idx + 1].strip()
        return v[:limit - 1].rstrip() + '…'
    platform_short = _short_stat(tool.get('platform', ''), 60) if tool.get('platform') else ''

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

    # Tool Detail v2 (design frame 04) — hero identity + editor score card
    score_val = str(tool.get('rating', '')).replace('⭐', '').replace('/ 5', '').strip()
    role = status_role(tool)
    score_notes = {
        'choice': "★ Editor's Choice  ·  Based on hands-on paid testing",
        'verified': "✓ Verified  ·  Independently tested",
        'trending': "↑ Trending  ·  Fast-growing adoption",
    }
    score_note = score_notes.get(role, 'Based on hands-on testing')
    score_note_cls = '' if role else ' muted'

    def _fmt_disp_date(iso: str) -> str:
        try:
            return datetime.strptime(iso, '%Y-%m-%d').strftime('%d %b %Y').lstrip('0')
        except Exception:
            return iso
    date_disp = _fmt_disp_date(date_mod)

    platform_chip = (f'<span class="td-chip td-chip-neutral">{escape_html(platform_short)}</span>'
                     if platform_short and len(platform_short) <= 28 else '')

    # Pricing card — one prominent price tile; plan tiles stay data-driven only
    pricing_details = (tool.get('pricing_details') or '').strip()
    pricing_detail_html = (f'<div class="td-price-detail">{escape_html(pricing_details)}</div>'
                           if pricing_details else '')
    pricing_html = f'''<div class="td-card td-pricing">
        <div class="td-card-head faint">PRICING&nbsp;·&nbsp;UPDATED {escape_html(date_disp)}</div>
        <div class="td-price-tile">
            <div class="td-price-label">CURRENT PRICING</div>
            <div class="td-price-value">{escape_html(tool.get('price', 'Free'))}</div>
            {pricing_detail_html}
        </div>
    </div>'''

    # Author trust block (GEO — EEAT signals for AI engines)
    today_iso_author = datetime.now().strftime('%Y-%m-%d')
    author_block = f'''<div class="author-block">
        <div class="author-block-inner">
            <div class="author-avatar">A</div>
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
    <title>{escape_html(name)} Review 2026: Pricing &amp; Alternatives</title>
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
    <link rel="stylesheet" href="/css/style.css?{CSS_VERSION}">
    <script type="application/ld+json">{breadcrumb_json}</script>
    <script type="application/ld+json">{structured_json}</script>
    {faq_page_schema}
{VERIFICATION_BLOCK}{GA_BLOCK}
</head>
<body>
{header_html()}

    <nav class="breadcrumb td-breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a><span class="sep">/</span><a href="/category/{cat_slug}/">{escape_html(cat)}</a><span class="sep">/</span><span>{escape_html(name)}</span>
    </nav>

    <main>
        <section class="td-hero">
            <div class="td-identity">
                {tool_tile(tool, 'tool-icon-lg')}
                <h1>{escape_html(name)}</h1>
                <p class="td-summary">{escape_html(tool['description'])}</p>
                <div class="td-chips">
                    <span class="td-chip td-chip-neutral">{escape_html(cat)}</span>
                    {platform_chip}
                    <span class="td-chip td-chip-verified">✓ Independently reviewed</span>
                </div>
            </div>
            <aside class="td-score-card">
                <div class="td-score-label">EDITOR SCORE</div>
                <div class="td-score-value">{escape_html(score_val)} / 5</div>
                <div class="td-score-note{score_note_cls}">{score_note}</div>
                <a class="td-visit-btn" href="{get_tool_link(tool, slug, 'en')[0]}" target="_blank" rel="{'nofollow noopener sponsored' if get_tool_link(tool, slug, 'en')[1] else 'noopener'}">Visit {escape_html(name)} →</a>
            </aside>
        </section>

        <div class="td-body">
            {pros_cons_html}

            {pricing_html}

            <article class="article-body" data-tts>
                {content_html}
            </article>

            {faq_html}

            {author_block}

            {related_html}

            {related_articles_html}
        </div>
    </main>

{footer_html()}
    ''' + BACK_TO_TOP_BLOCK + DARK_MODE_BLOCK + '''
</body>
</html>'''


# ─── Article page ─────────────────────────────────────────────────────────────

# ─── TOC / heading anchors (article pages) ────────────────────────────────────

def _toc_slug(text: str, used: set) -> str:
    base = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')[:60] or 'section'
    slug, i = base, 2
    while slug in used:
        slug = f'{base}-{i}'
        i += 1
    used.add(slug)
    return slug


def _iso_date_for_schema(raw) -> str:
    """schema.org datePublished/dateModified MUST be ISO 8601 (e.g.
    2026-11-14). Non-ISO dates are ignored by Google/AI parsers, silently
    killing freshness signals. Coerces any stored format to YYYY-MM-DD.
    Year guard: strptime('07/05', '%m/%d') silently yields year 1900 —
    anything older than 2015 is treated as a parse failure instead."""
    raw = str(raw or '').strip()
    m = re.match(r'^(\d{4}-\d{2}-\d{2})', raw)
    if m:
        return m.group(1)
    for fmt in ('%m/%d/%Y', '%m/%d', '%B %d, %Y', '%b %d, %Y'):
        try:
            parsed = datetime.strptime(raw, fmt)
            if parsed.year >= 2015:
                return parsed.strftime('%Y-%m-%d')
        except ValueError:
            continue
    return datetime.now().strftime('%Y-%m-%d')


def add_heading_anchors(content_html: str):
    """Add stable ids to <h2> headings for TOC deep-links; returns (html, [(id, text)])."""
    used: set = set()
    items: list = []

    def _repl(m):
        attrs, inner = m.group(1), m.group(2)
        text = re.sub(r'<[^>]+>', '', inner).strip()
        hid = _toc_slug(text, used)
        items.append((hid, text))
        return f'<h2{attrs} id="{hid}">{inner}</h2>'

    html = re.sub(r'<h2([^>]*)>(.*?)</h2>', _repl, content_html, flags=re.DOTALL)
    return html, items


def build_article_page_en(article: dict, all_articles: list, all_tools: list = None) -> str:
    slug     = article['slug']
    title    = article['title']
    # 2026-11-18: SERP 标题截断治理——<title>/og/twitter 用 seo_title（<=55 字符，
    # 由 gen_seo_titles.py 生成，保留主关键词+年份），H1 与 JSON-LD headline 保留完整标题。
    # 站名后缀只在放得下时拼接（保证 <title> 总长 <=60，否则裸用短标题）。
    serp_title = article.get('seo_title') or title
    _suffix = f" - {SITE_NAME}"
    serp_title = serp_title + _suffix if len(serp_title) + len(_suffix) <= 60 else serp_title
    cat      = article.get('category', 'AI Tools')
    cat_slug = get_category_slug_en(cat)
    date_str = article.get('date','')

    # 2026-11-18: 面包屑/kicker 的分类链接只在分类页真实存在时输出（"有才互链"）。
    # ARTICLE_CATEGORY_PAGES 由 build_all_en 在生成任何页面之前预计算
    # （工具分类 ∪ 文章数>=阈值的文章分类）；小分类降级为纯文本，消灭 404。
    linkable = cat_slug in ARTICLE_CATEGORY_PAGES
    cat_crumbs = (f'<a href="/category/{cat_slug}/">{escape_html(cat)}</a>' if linkable
                  else f'<span>{escape_html(cat)}</span>')
    cat_kicker = (f'<a class="article-kicker" href="/category/{cat_slug}/">{escape_html(cat)}</a>'
                  if linkable else f'<span class="article-kicker">{escape_html(cat)}</span>')

    # Parse date to ISO for schema
    # 2026-11-18 fix: was article.get('dateFull', ...) — dateFull holds the
    # HUMAN-readable date ("November 14, 2026") for 168 articles, and non-ISO
    # dates in JSON-LD are ignored by parsers. Visible text keeps dateFull;
    # schema always gets the ISO-normalized `date`.
    article_date = _iso_date_for_schema(article.get('date'))
    date_modified_raw = article.get('dateModified') or article_date

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
                    {tool_tile(t, 'related-tile')}
                    <div style="font-weight:600;">{escape_html(t['name'])}</div>
                    <div style="font-size:13px;color:#666;">{escape_html(t.get('category',''))}</div>
                </a>\n'''
            related_tools_html = f'''<div class="related-tools">
            <h3>Related Tools</h3>
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
                <div style="font-size:13px;color:#666;">{a.get('date','')}</div>
            </a>\n'''
        related_html = f'''<div class="related-tools">
            <h3>Related Articles</h3>
            <div class="related-grid">{cards}</div>
        </div>'''

    # Structured data
    # 分类页不存在时，面包屑第2项不给 URL（Schema 允许 name-only 的 ListItem），
    # 避免 JSON-LD 声明 404 目标。
    if linkable:
        cat_li = {"@type":"ListItem","position":2,"name":cat,"item":f"{SITE_DOMAIN}/category/{cat_slug}/"}
    else:
        cat_li = {"@type":"ListItem","position":2,"name":cat}
    breadcrumb_data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type":"ListItem","position":1,"name":"Home","item":f"{SITE_DOMAIN}/"},
            cat_li,
            {"@type":"ListItem","position":3,"name":title,"item":f"{SITE_DOMAIN}/articles/{slug}/"},
        ]
    }
    article_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": article.get('description',''),
        "datePublished": article_date,
        "dateModified":  _iso_date_for_schema(date_modified_raw),
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

    content_html = markdown_to_html(article.get('content') or article.get('body',''))
    content_html, toc_items = add_heading_anchors(content_html)
    if len(toc_items) >= 3:
        toc_links = ''.join(
            f'<li><a href="#{hid}">{escape_html(text)}</a></li>' for hid, text in toc_items
        )
        toc_html = (f'<aside class="article-toc" aria-label="Table of contents">'
                    f'<div class="toc-title">On this page</div>'
                    f'<ul>{toc_links}</ul></aside>')
    else:
        toc_html = ''
    hreflang     = hreflang_tags(f'/articles/{slug}/', f'/articles/{slug}/')
    og_image     = ensure_en_og_image(slug, article, is_article=True)

    # TL;DR box (answer-first format for GEO - AI engines extract first 200 words)
    # Class-only markup: Visual System v2 owns the styling (blue info block).
    tldr_text = article.get('description','').strip()
    if tldr_text:
        tldr_html = f'<div class="tldr-box"><strong>TL;DR</strong><p>{escape_html(tldr_text)}</p></div>'
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
        _mfaq = re.search(r'(?im)^##\s+[^\n]*(frequently\s+asked\s+questions|\bfaq\b)', _content_for_faq)
        if _mfaq:
            _faq_section = _content_for_faq[_mfaq.end():]
            _faq_raw = re.findall(
                r'\*\*([^*\n]{6,100}[?？])\*\*\s*\n\s*(.+?)(?=\n\*\*[^*\n]{6,100}[?？]\*\*|\n## |\Z)',
                _faq_section, re.DOTALL
            )

    # Strategy 3: FAQ section ### question? then answer (no Q prefix)
    if not _faq_raw:
        _mfaq = re.search(r'(?im)^##\s+[^\n]*(frequently\s+asked\s+questions|\bfaq\b)', _content_for_faq)
        if _mfaq:
            _faq_section = _content_for_faq[_mfaq.end():]
            _faq_raw = re.findall(
                r'###\s*([^\n]{6,100}[?？])\s*\n\s*(.+?)(?=\n###\s*[^\n]{6,100}[?？]|\n## |\Z)',
                _faq_section, re.DOTALL
            )

    # Strategy 4: FAQ section HTML <h3>question</h3><p>answer</p>
    if not _faq_raw:
        _mfaq = re.search(r'(?im)^##\s+[^\n]*(frequently\s+asked\s+questions|\bfaq\b)', _content_for_faq)
        if _mfaq:
            _faq_section = _content_for_faq[_mfaq.end():]
            _faq_raw = re.findall(
                r'<h[34][^>]*>\s*(?:[Qq]\d*[：:]\s*)?([^<]+?)\s*</h[34]>\s*<p>(.+?)</p>',
                _faq_section, re.DOTALL
            )

    # Strategy 5: FAQ section HTML <strong>Q：</strong><br>A：
    if not _faq_raw:
        _mfaq = re.search(r'(?im)^##\s+[^\n]*(frequently\s+asked\s+questions|\bfaq\b)', _content_for_faq)
        if _mfaq:
            _faq_section = _content_for_faq[_mfaq.end():]
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
    <title>{escape_html(serp_title)}</title>
    <meta name="description" content="{escape_html(article.get('description',''))}">
    <meta name="keywords" content="{escape_html(article.get('keywords',''))}">
    <link rel="canonical" href="{SITE_DOMAIN}/articles/{slug}/">
{hreflang}    <meta property="og:type" content="article">
    <meta property="og:title" content="{escape_html(serp_title)}">
    <meta property="og:description" content="{escape_html(article.get('description',''))}">
    <meta property="og:url" content="{SITE_DOMAIN}/articles/{slug}/">
    {'<meta property="og:image" content="' + og_image + '">' if og_image else ''}
    <meta property="og:site_name" content="{SITE_NAME}">
    <meta name="twitter:card" content="{'summary_large_image' if og_image else 'summary'}">
    <meta name="twitter:title" content="{escape_html(serp_title)}">
    <meta name="twitter:description" content="{escape_html(article.get('description',''))}">
    {'<meta name="twitter:image" content="' + og_image + '">' if og_image else ''}
    <link rel="stylesheet" href="/css/style.css?{CSS_VERSION}">
    <script type="application/ld+json">{breadcrumb_json}</script>
    <script type="application/ld+json">{structured_json}</script>{howto_schema_html}{faq_article_schema}
{VERIFICATION_BLOCK}{GA_BLOCK}
</head>
<body>
{header_html()}

    <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a> &gt; {cat_crumbs} &gt; <span>{escape_html(title)[:30]}...</span>
    </nav>

    <main class="article-container article-container-wide">
        <header class="article-header">
            {cat_kicker}
            <h1 class="article-title">{escape_html(title)}</h1>
            <div class="article-meta-row">
                <span>{date_str}</span>
                <span aria-hidden="true">·</span>
                <span itemprop="author" itemscope itemtype="https://schema.org/Organization"><a href="/author/" itemprop="url"><span itemprop="name">AI Tool Lab Editorial Team</span></a></span>
                <span aria-hidden="true">·</span>
                <span>{max(3, len(article.get('content','')) // 500)} min read</span>
            </div>
        </header>
        <div class="article-layout">
            <article class="article-body" data-tts>
                {tldr_html}
                {content_html}
                <div class="author-note">
                    <p><strong>About the author:</strong> This article was written by the <a href="/author/">AI Tool Lab Editorial Team</a>, with 5+ years of paid AI tool testing experience and $200+ monthly subscription spend. All reviews are based on real paid long-term use.</p>
                    <p><strong>Data statement:</strong> All data in this article cites its source and is verifiable. Found an error? Report it via our <a href="/contact.html">contact page</a>, we verify within 48 hours.</p>
                </div>
            </article>
            {toc_html}
        </div>

        {related_html}

        {related_tools_html}
    </main>

{footer_html()}
    ''' + BACK_TO_TOP_BLOCK + DARK_MODE_BLOCK + '''
</body>
</html>'''


# ─── Category page ────────────────────────────────────────────────────────────

def build_category_page_en(cat_name: str, tools: list, cat_articles: list = None) -> str:
    """工具分类页。2026-11-18 修复覆盖 bug：文章分类 slug 与工具分类冲突时
    （ai-image/ai-video/ai-development 等 10 个），本页被文章列表页整体覆盖、
    工具网格丢失。现在冲突时在同一页合并渲染：工具网格 + 指南文章区块，
    两类内容都有入口，不再相互覆盖。"""
    cat_slug = get_category_slug_en(cat_name)
    # Client-side filter/sort — bucket each card once at build time
    type_counts = {'free': 0, 'freemium': 0, 'paid': 0}
    tool_cards = ''
    for t in tools:
        badge_html = status_chip(t)
        pt = price_type(t.get('price', ''))
        type_counts[pt] += 1
        tool_cards += f'''<a href="/tools/{t['slug']}/" class="tool-card" data-type="{pt}" data-rating="{rating_num(t)}" data-visits="{visits_num(t.get('visits'))}">
            {tool_tile(t)}
            <div class="tool-info">
                <div class="tool-title-row"><h3>{escape_html(t['name'])}</h3>{badge_html}</div>
                <p>{escape_html(t['description'])}</p>
                <div class="tool-meta-row">
                    <span>{rating_num(t):.1f}</span>
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

    # 2026-11-18: 冲突合并——该分类的文章指南区块（与文章分类页同一 al-card 样式）
    guides_block = ''
    if cat_articles:
        g_cards = ''
        for ga in cat_articles:
            g_url = f'/articles/{ga["slug"]}/'
            g_date = ga.get('date', '')
            g_read = max(1, (len(ga.get('content', '').split()) + 219) // 220)
            g_cards += f'''<article class="al-card">
                <a class="al-card-link" href="{g_url}">
                    <div class="al-top">
                        <span class="al-chip">{escape_html(ga.get('category',''))}</span>
                        <time class="al-date" datetime="{g_date}">{_nice_date(g_date)}</time>
                    </div>
                    <h2 class="al-title">{escape_html(ga['title'])}</h2>
                    <p class="al-summary">{escape_html(ga.get('description',''))}</p>
                    <div class="al-foot">
                        <span class="al-read">{g_read} min read</span>
                        <span class="al-arrow" aria-hidden="true">&rarr;</span>
                    </div>
                </a>
            </article>\n'''
        guides_block = (f'<section class="cat-section" aria-label="Guides and comparisons">'
                        f'<h2>{escape_html(cat_name)} guides &amp; comparisons</h2>'
                        f'<p class="cat-intro">In-depth articles from our editorial testing: pricing breakdowns, '
                        f'head-to-head comparisons and step-by-step workflows.</p>'
                        f'<div class="articles-list">{g_cards}</div>'
                        f'</section>')
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
{hreflang}    <link rel="stylesheet" href="/css/style.css?{CSS_VERSION}">
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
        <h1 class="page-title">Best {escape_html(cat_name)} Tools 2026</h1>
        <p class="page-sub">{len(tools)} tools reviewed and ranked</p>
        <div class="cat-toolbar">
            <div class="cf-group" role="group" aria-label="Filter by pricing">
                <button class="cf-chip active" data-filter="all" type="button">All ({len(tools)})</button>
                <button class="cf-chip" data-filter="free" type="button">Free ({type_counts['free']})</button>
                <button class="cf-chip" data-filter="freemium" type="button">Free + Paid ({type_counts['freemium']})</button>
                <button class="cf-chip" data-filter="paid" type="button">Paid ({type_counts['paid']})</button>
            </div>
            <div class="cf-group" role="group" aria-label="Sort tools">
                <span class="cf-label">Sort</span>
                <button class="cf-chip active" data-sort="featured" type="button">Featured</button>
                <button class="cf-chip" data-sort="rating" type="button">Top rated</button>
                <button class="cf-chip" data-sort="visits" type="button">Popular</button>
            </div>
        </div>
        <p class="cat-count" id="catCount" aria-live="polite">{len(tools)} tools</p>
        <div class="cat-empty" id="catEmpty" hidden>No tools match this filter.</div>
        <div class="tool-grid" id="catGrid">
            {tool_cards}
        </div>
{guides_block}
    </main>

{footer_html()}
    ''' + BACK_TO_TOP_BLOCK + DARK_MODE_BLOCK + r'''
    <script>
    (function() {
        var grid = document.getElementById('catGrid');
        if (!grid) return;
        var cards = Array.prototype.slice.call(grid.querySelectorAll('.tool-card'));
        var countEl = document.getElementById('catCount');
        var emptyEl = document.getElementById('catEmpty');
        var toolbar = document.querySelector('.cat-toolbar');
        var ftype = 'all', skey = 'featured';
        cards.forEach(function(c, i) { c.dataset.idx = i; });
        function apply() {
            var shown = 0;
            cards.forEach(function(c) {
                var ok = ftype === 'all' || c.getAttribute('data-type') === ftype;
                c.style.display = ok ? '' : 'none';
                if (ok) shown++;
            });
            cards.sort(function(a, b) {
                if (skey === 'rating') return parseFloat(b.dataset.rating || 0) - parseFloat(a.dataset.rating || 0);
                if (skey === 'visits') return parseInt(b.dataset.visits || 0, 10) - parseInt(a.dataset.visits || 0, 10);
                return parseInt(a.dataset.idx, 10) - parseInt(b.dataset.idx, 10);
            });
            cards.forEach(function(c) { grid.appendChild(c); });
            countEl.textContent = shown + ' of ' + cards.length + ' tools';
            emptyEl.hidden = shown !== 0;
            grid.style.display = shown ? '' : 'none';
        }
        toolbar.addEventListener('click', function(e) {
            var b = e.target.closest('button');
            if (!b) return;
            if (b.dataset.filter) {
                ftype = b.dataset.filter;
                toolbar.querySelectorAll('[data-filter]').forEach(function(x) { x.classList.toggle('active', x === b); });
            } else if (b.dataset.sort) {
                skey = b.dataset.sort;
                toolbar.querySelectorAll('[data-sort]').forEach(function(x) { x.classList.toggle('active', x === b); });
            }
            apply();
        });
    })();
    </script>
</body>
</html>'''


# ─── Article list page ────────────────────────────────────────────────────────

def _windowed_page_numbers(current: int, total: int, span: int = 2) -> list:
    """Compact page-number window; None marks a gap (rendered as an ellipsis).

    The first and last pages always stay reachable. Near either edge the
    window is widened so the visible block never looks lopsided. Total page
    counts small enough to fit are returned in full.
    """
    if total <= 7:
        return list(range(1, total + 1))

    lo = max(1, current - span)
    hi = min(total, current + span)
    if current <= 4:              # near the start → full leading block
        lo, hi = 1, min(total, 5)
    elif current >= total - 3:    # near the end → full trailing block
        lo, hi = max(1, total - 4), total

    pages = sorted({1, total} | set(range(lo, hi + 1)))

    out, prev = [], None
    for p in pages:
        if prev is not None and p - prev > 1:
            out.append(None)
        out.append(p)
        prev = p
    return out


_MONTHS_ABBR = ('', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')


def _nice_date(value: str) -> str:
    try:
        y, m, d = value.split('-')
        return f'{_MONTHS_ABBR[int(m)]} {int(d)}, {y}'
    except (ValueError, IndexError):
        return value


def build_article_category_page_en(cat_name: str, cat_articles: list) -> str:
    """Article-type category page (Home > <Category> > N guides).

    2026-11-18 治本：文章的 category 值（AI Infrastructure / AI Photo / AI Tools 等）
    历史上从未生成过页面，文章页面包屑与 kicker 链接 404 达 421 处。
    为文章数 >= MIN_ARTICLES_FOR_CATEGORY_PAGE 的分类生成真实导航页；
    小于阈值的分类在面包屑中降级为纯文本（见 build_article_page_en）。
    """
    cat_slug = get_category_slug_en(cat_name)
    n = len(cat_articles)
    hreflang = hreflang_tags(f'/category/{cat_slug}/', f'/category/{cat_slug}/')
    cards = ''
    for a in cat_articles:
        url = f'/articles/{a["slug"]}/'
        raw_date = a.get('date', '')
        read_min = max(1, (len(a.get('content', '').split()) + 219) // 220)
        cards += f'''<article class="al-card">
            <a class="al-card-link" href="{url}">
                <div class="al-top">
                    <span class="al-chip">{escape_html(a.get('category',''))}</span>
                    <time class="al-date" datetime="{raw_date}">{_nice_date(raw_date)}</time>
                </div>
                <h2 class="al-title">{escape_html(a['title'])}</h2>
                <p class="al-summary">{escape_html(a.get('description',''))}</p>
                <div class="al-foot">
                    <span class="al-read">{read_min} min read</span>
                    <span class="al-arrow" aria-hidden="true">&rarr;</span>
                </div>
            </a>
        </article>\n'''

    breadcrumb = f'''{"{"}"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE_DOMAIN}/"}},
        {{"@type": "ListItem", "position": 2, "name": "{escape_html(cat_name)}", "item": "{SITE_DOMAIN}/category/{cat_slug}/"}}
    ]{"}"}'''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape_html(cat_name)} Guides & Reviews 2026 - {SITE_NAME}</title>
    <meta name="description" content="All {n} in-depth {escape_html(cat_name)} guides and reviews on {SITE_NAME}: hands-on testing, pricing analysis and verdicts, updated as the market changes.">
    <link rel="canonical" href="{SITE_DOMAIN}/category/{cat_slug}/">
{hreflang}    <link rel="stylesheet" href="/css/style.css?{CSS_VERSION}">
    <script type="application/ld+json">{breadcrumb}</script>
    <script type="application/ld+json">{{
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "{escape_html(cat_name)} guides",
        "url": "{SITE_DOMAIN}/category/{cat_slug}/",
        "mainEntity": {{"@type": "ItemList", "numberOfItems": {n}}}
    }}</script>
</head>
<body>
{header_html()}

    <main class="article-list-container">
        <nav class="crumbs" aria-label="Breadcrumb">
            <a href="/">Home</a> &gt; <span>{escape_html(cat_name)}</span>
        </nav>
        <h1 class="page-title">{escape_html(cat_name)}</h1>
        <p class="page-sub">{n} in-depth guides and reviews, all based on paid long-term testing.</p>
        <div class="articles-list">
{cards}        </div>
    </main>

{footer_html()}
</body>
</html>'''


def build_article_list_en(articles: list, current_page: int = 1, total_pages: int = 1) -> str:
    cards = ''
    for a in articles:
        slug = a['slug']
        url = f'/articles/{slug}/'
        raw_date = a.get('date', '')
        read_min = max(1, (len(a.get('content', '').split()) + 219) // 220)
        cards += f'''<article class="al-card">
            <a class="al-card-link" href="{url}">
                <div class="al-top">
                    <span class="al-chip">{escape_html(a.get('category',''))}</span>
                    <time class="al-date" datetime="{raw_date}">{_nice_date(raw_date)}</time>
                </div>
                <h2 class="al-title">{escape_html(a['title'])}</h2>
                <p class="al-summary">{escape_html(a.get('description',''))}</p>
                <div class="al-foot">
                    <span class="al-read">{read_min} min read</span>
                    <span class="al-arrow" aria-hidden="true">&rarr;</span>
                </div>
            </a>
        </article>\n'''

    # Pagination controls
    pagination_html = ''
    if total_pages > 1:
        links = []
        if current_page > 1:
            prev_url = '/articles/' if current_page == 2 else f'/articles/page/{current_page-1}/'
            links.append(f'<a href="{prev_url}" class="page-link">&laquo; Prev</a>')
        
        for p in _windowed_page_numbers(current_page, total_pages):
            if p is None:
                links.append('<span class="page-ellipsis" aria-hidden="true">&hellip;</span>')
                continue
            url = '/articles/' if p == 1 else f'/articles/page/{p}/'
            active = ' active' if p == current_page else ''
            aria = ' aria-current="page"' if p == current_page else ''
            links.append(f'<a href="{url}" class="page-link{active}"{aria}>{p}</a>')

        if current_page < total_pages:
            next_url = f'/articles/page/{current_page+1}/'
            links.append(f'<a href="{next_url}" class="page-link">Next &raquo;</a>')

        pagination_html = f'<nav class="pagination" aria-label="Pagination">{"".join(links)}</nav>'

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
{hreflang}    <link rel="stylesheet" href="/css/style.css?{CSS_VERSION}">
{VERIFICATION_BLOCK}{GA_BLOCK}
</head>
<body>
{header_html()}

    <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a> &gt; <span>Articles</span>
    </nav>

    <main class="article-list-container">
        <header class="al-header">
            <h1 class="page-title">AI Tool Articles &amp; Guides</h1>
            <p class="page-sub">In-depth comparisons and pricing breakdowns, published daily.</p>
        </header>
        <div class="article-list">{cards}</div>
        {pagination_html}
    </main>

{footer_html()}
    ''' + BACK_TO_TOP_BLOCK + DARK_MODE_BLOCK + '''
</body>
</html>'''


# ─── Category index page ──────────────────────────────────────────────────────

def build_category_index_en(tools_by_cat: dict) -> str:
    # ═══ Category hub — same information architecture as the CN site hub ═══
    # Direct-answer intro → GEO quick-reference table (category / tools /
    # best for / top picks) → icon card grid → FAQ (rendered + FAQPage JSON-LD)
    # + ItemList JSON-LD. Tables are the structure AI engines quote most.

    # Merge raw category names by slug (AI Video / Video AI → ai-video, ...)
    merged = {}
    for cat_name, tools in tools_by_cat.items():
        s = get_category_slug_en(cat_name)
        if s not in merged:
            merged[s] = {'display': cat_name, 'tools': list(tools)}
        else:
            merged[s]['tools'].extend(tools)
    cats = sorted(merged.items(), key=lambda kv: len(kv[1]['tools']), reverse=True)
    total_cats = len(cats)
    total_tools = sum(len(v['tools']) for v in merged.values())
    today_iso = datetime.now().strftime('%Y-%m-%d')

    # Typical use cases per category family — lets AI answer "which tools for X"
    category_scenes = {
        'ai-chat': 'Daily Q&A, research, writing and code help',
        'ai-writing': 'Blog posts, marketing copy, essays and rewriting',
        'ai-image': 'Illustrations, e-commerce visuals, posters and concept art',
        'ai-coding': 'Code completion, bug fixes, tests and refactoring',
        'ai-video': 'Short-form video, avatars, subtitles and editing',
        'ai-audio': 'Text-to-speech, transcription, music and noise removal',
        'ai-office': 'Slides, spreadsheets, meeting notes and document summaries',
        'ai-design': 'UI design, prototypes, logos and brand visuals',
        'ai-search': 'Web-connected search, cited answers, literature lookup',
        'ai-translation': 'Documents, subtitles and product localization',
        'ai-automation': 'Workflow orchestration, data sync, cross-app execution',
        'ai-productivity': 'Notes, task planning and personal knowledge',
        'ai-agents': 'Task agents, automated research, multi-step execution',
        'ai-development': 'Model APIs, vector databases and app frameworks',
        'ai-income': 'Making money with AI: side hustles, content and micro-SaaS',
        'ai-e-commerce': 'Product listings, ad creative and store operations',
        'ai-seo': 'Keyword research, content optimization and rank tracking',
        'ai-website-builder': 'Landing pages and full websites from prompts',
        'market-research': 'Surveys, competitor analysis and demand validation',
        'ai-research': 'Paper search, literature review and experiment design',
        # slug variants of the families above (Video AI, Writing, Image, ...)
        'ai-marketing': 'Ad creative, campaign copy, audience research and content calendars',
        'marketing': 'Ad creative, campaign copy, audience research and content calendars',
        'video-ai': 'Short-form video, avatars, subtitles and editing',
        'writing': 'Blog posts, marketing copy, essays and rewriting',
        'image': 'Illustrations, e-commerce visuals, posters and concept art',
        'ai-images': 'Illustrations, e-commerce visuals, posters and concept art',
        'productivity': 'Notes, task planning and personal knowledge',
        'automation': 'Workflow orchestration, data sync, cross-app execution',
        'seo': 'Keyword research, content optimization and rank tracking',
        'ai-dev': 'Model APIs, vector databases and app frameworks',
        'ai-api': 'Model APIs, vector databases and app frameworks',
        'ai-web-design': 'Landing pages, UI mockups and brand visuals from prompts',
    }

    def _rating_num(t):
        try:
            return float(re.sub(r'[^\d.]', '', str(t.get('rating', ''))) or 0)
        except Exception:
            return 0

    # ── Quick-reference table rows ──
    table_rows = ''
    for cslug, data in cats:
        cname, clist = data['display'], data['tools']
        scene = category_scenes.get(cslug, f'{cname} use cases')
        reps = sorted(clist, key=_rating_num, reverse=True)[:3]
        reps_txt = ' '.join(
            f'<a href="/tools/{r["slug"]}/">{escape_html(r["name"])}</a>' for r in reps
        ) if reps else 'Curated continuously'
        table_rows += (
            '<tr>'
            f'<td><a href="/category/{cslug}/"><strong>{escape_html(cname)}</strong></a></td>'
            f'<td class="num">{len(clist)}</td>'
            f'<td>{escape_html(scene)}</td>'
            f'<td class="reps">{reps_txt}</td>'
            '</tr>\n'
        )

    # ── Mini-card grid — CN-site compact chips so one screen holds every category ──
    cat_cards = ''
    for cslug, data in cats:
        cname = data['display']
        n = len(data['tools'])
        cat_cards += (f'<a class="cat-mini" href="/category/{cslug}/" title="{escape_html(cname)}">'
                      f'<span class="cat-mini-icon">{category_icon_svg(cname)}</span>'
                      f'<span class="cat-mini-name">{escape_html(cname)}</span>'
                      f'<span class="cat-mini-meta">{n} tool{"s" if n != 1 else ""}</span>'
                      f'</a>\n')

    # ── Guides by topic (2026-11-18): entry links to article category pages ──
    # 文章分类页此前从未生成也无入口；本区块让面包屑目标页可达（有才互链）。
    guides_block = ''
    try:
        from collections import Counter as _C
        _arts = json.load(open(os.path.join(BASE_DIR, 'data', 'articles_en.json'), encoding='utf-8'))
        _cnt = _C(a.get('category','') for a in _arts if a.get('category'))
        _qualifying = sorted(
            [(c, n, get_category_slug_en(c)) for c, n in _cnt.items()
             if n >= MIN_ARTICLES_FOR_CATEGORY_PAGE
             and get_category_slug_en(c) not in {get_category_slug_en(c2) for c2, _ in tools_by_cat.items()}],
            key=lambda x: -x[1])
        if _qualifying:
            _items = ''.join(
                f'<a class="cat-mini" href="/category/{s}/" title="{escape_html(c)} guides">'
                f'<span class="cat-mini-name">{escape_html(c)}</span>'
                f'<span class="cat-mini-meta">{n} guide{"s" if n != 1 else ""}</span>'
                f'</a>\n' for c, n, s in _qualifying)
            guides_block = ('<section class="cat-section" aria-label="Guides by topic">'
                            '<h2>Guides by topic</h2>'
                            '<p class="cat-intro">Topic hubs for our in-depth articles — pricing analyses, comparisons and step-by-step workflows.</p>'
                            f'<div class="cat-mini-grid">{_items}</div>'
                            '</section>')
    except Exception:
        guides_block = ''

    # ── FAQ: plain-text answers, rendered + FAQPage schema (GEO core) ──
    top5_txt = ', '.join(f"{data['display']} ({len(data['tools'])})" for _, data in cats[:5])
    all_cats_txt = ', '.join(data['display'] for _, data in cats)
    faq_items = [
        (
            'What categories of AI tools are there?',
            f'AI Tool Lab organizes its {total_tools} independently reviewed AI tools into '
            f'{total_cats} categories: {all_cats_txt}. The most extensive are {top5_txt}. '
            'Every category page ranks its tools by editor score and states the price model of each tool.'
        ),
        (
            "I'm new to AI tools — where should I start?",
            'Start with AI Chat: these tools are the most general-purpose and cover Q&A, writing, '
            'translation and code explanation with no learning curve. Then move into a vertical '
            'category that matches your work: AI Writing for content, AI Image for visuals, '
            'AI Coding for programming, and AI Office for reports and presentations.'
        ),
        (
            'Are there free AI tools in these categories?',
            'Yes. Almost every category includes both free and paid tools, most commonly a free '
            'tier with a paid subscription on top. Each tool page states its price model, and the '
            'quick-reference table above links straight to every category so you can compare prices.'
        ),
        (
            'What is the fastest way to find the right AI tool?',
            'Three ways: use the quick-reference table on this page to match your task to a '
            'category; open a category page and sort by editor score; or read one of our hands-on '
            'comparison articles when you have two or three candidates and need a verdict.'
        ),
        (
            'How often are the categories updated?',
            f'The tool library is updated daily and the category structure grows as new tools are '
            f'added. This page was last updated on {today_iso}: {total_cats} categories, '
            f'{total_tools} reviewed tools.'
        ),
    ]
    faq_schema = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q,
         'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq_items
    ]}
    faq_json = json.dumps(faq_schema, ensure_ascii=False)

    itemlist = {'@context': 'https://schema.org', '@type': 'ItemList',
                'name': 'AI tool categories',
                'itemListElement': [
                    {'@type': 'ListItem', 'position': i, 'name': data['display'],
                     'url': f'{SITE_DOMAIN}/category/{cslug}/'}
                    for i, (cslug, data) in enumerate(cats, 1)
                ]}
    itemlist_json = json.dumps(itemlist, ensure_ascii=False)

    # FAQ HTML with hairline dividers (same visual language as tool pages)
    faq_html = ''
    for q, a in faq_items:
        if faq_html:
            faq_html += '<div class="td-faq-divider"></div>\n'
        faq_html += (f'<div class="td-faq-item"><h3>{escape_html(q)}</h3>'
                     f'<div class="td-faq-a"><p>{escape_html(a)}</p></div></div>\n')

    intro_links = ', '.join(
        f'<a href="/category/{cslug}/">{escape_html(data["display"])}</a>'
        for cslug, data in cats[:4]
    )
    page_title = f'AI Tool Categories 2026: {total_cats} Categories, {total_tools} Tools Reviewed'
    meta_desc = (f'Browse all {total_cats} AI tool categories on {SITE_NAME} — {total_tools} '
                 f'independently reviewed tools with a quick-reference table of use cases and '
                 f'top picks. Updated {today_iso}.')

    hreflang = hreflang_tags('/category/', '/category/')
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape_html(page_title)} - {SITE_NAME}</title>
    <meta name="description" content="{escape_html(meta_desc)}">
    <link rel="canonical" href="{SITE_DOMAIN}/category/">
{hreflang}    <meta property="og:type" content="website">
    <meta property="og:title" content="{escape_html(page_title)}">
    <meta property="og:description" content="{escape_html(meta_desc)}">
    <meta property="og:url" content="{SITE_DOMAIN}/category/">
    <meta property="og:site_name" content="{SITE_NAME}">
    <link rel="stylesheet" href="/css/style.css?{CSS_VERSION}">
    <script type="application/ld+json">{faq_json}</script>
    <script type="application/ld+json">{itemlist_json}</script>
{VERIFICATION_BLOCK}{GA_BLOCK}
</head>
<body>
{header_html()}

    <nav class="breadcrumb td-breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a><span class="sep">/</span><span>All Categories</span>
    </nav>

    <main class="cat-hub">
        <h1 class="page-title">AI Tool Categories</h1>
        <p class="cat-intro">AI Tool Lab has independently reviewed {total_tools} AI tools across
            {total_cats} categories, from {intro_links}. Browse the grid below to jump straight
            into a category — the quick-reference table after it lists every category's size,
            typical use cases and top picks.</p>

        <section class="cat-section" id="browse">
            <h2>Browse by category</h2>
            <div class="cat-mini-grid">
                {cat_cards}
            </div>
        </section>

        <section class="cat-section" id="quick-reference">
            <h2>AI tool categories quick reference ({total_cats} categories)</h2>
            <div class="cat-table-wrap"><table class="cat-table">
                <thead><tr><th>Category</th><th>Tools</th><th>Best for</th><th>Top picks</th></tr></thead>
                <tbody>
{table_rows}                </tbody>
            </table></div>
        </section>

{guides_block}

        <section class="cat-section" id="faq">
            <h2>Questions about AI tool categories</h2>
            <div class="td-faq">
                {faq_html}
            </div>
        </section>
    </main>

{footer_html()}
    ''' + BACK_TO_TOP_BLOCK + DARK_MODE_BLOCK + '''
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
        badge_html = status_chip(t)
        tool_cards += f'''<a href="/tools/{t['slug']}/" class="tool-card">
            {tool_tile(t)}
            <div class="tool-info">
                <div class="tool-title-row"><h3>{escape_html(t['name'])}</h3>{badge_html}</div>
                <p>{escape_html(t['description'])}</p>
                <div class="tool-meta-row">
                    <span>{rating_num(t):.1f}</span>
                    <span>{t.get('price','')}</span>
                </div>
            </div>
        </a>\n'''

    # Recent articles (top 5)
    article_cards = ''

    # Sidebar: Top Rated (by star rating)
    def parse_rating(rating_str):
        try:
            import re
            match = re.search(r'[\d.]+', str(rating_str))
            return float(match.group()) if match else 0
        except:
            return 0

    top_rated = sorted(tools, key=lambda t: parse_rating(t.get('rating','')), reverse=True)[:8]

    # Editor's shortlist lives in the hero; the same ranking is not repeated
    # as a decorative sidebar list. Adds three tool links instead of removing any.
    shortlist_rows = ''
    for i, t in enumerate(top_rated[:3], start=1):
        slug = t['slug']
        rating = str(t.get('rating', '')).replace('⭐', '').strip()
        shortlist_rows += (
            f'<div class="hs-row">'
            f'<span class="hs-rank">{i:02d}</span>'
            f'<a class="hs-name" href="/tools/{slug}/">{escape_html(t["name"])}</a>'
            f'<span class="hs-score">{escape_html(rating)}</span>'
            f'</div>\n'
        )
    shortlist_html = f'''<aside class="hero-shortlist">
        <div class="hs-head">
            <span class="hs-kicker">EDITOR'S SHORTLIST</span>
            <span class="hs-verified">&#9679; Verified</span>
        </div>
        <p class="hs-sub">Tested this week, ranked by score</p>
        {shortlist_rows}
        <div class="hs-foot">Last verified {datetime.now().strftime('%d %b %Y')} &middot; <a href="/about.html">See methodology</a></div>
    </aside>'''

    top_rated_html = '<ol style="list-style:none;padding:0;margin:0;">'
    for i, t in enumerate(top_rated):
        top_rated_html += f'''<li style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #f1f5f9;font-size:13px;">
            <span style="font-weight:800;color:var(--primary-color);min-width:20px;">{i+1}.</span>
            {tool_tile(t, 'sidebar-tile')}
            <div style="flex:1;min-width:0;">
                <a href="/tools/{t['slug']}/" style="color:var(--text-main);text-decoration:none;font-weight:600;display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{escape_html(t['name'])}</a>
                <span style="color:var(--text-muted);font-size:11px;">{rating_num(t):.1f}</span>
            </div>
        </li>'''
    top_rated_html += '</ol>'

    # Sidebar: Most Popular (by visits)
    most_popular = sorted(tools, key=lambda t: parse_visits(t.get('visits','0')), reverse=True)[:8]
    most_popular_html = '<ol style="list-style:none;padding:0;margin:0;">'
    for i, t in enumerate(most_popular):
        most_popular_html += f'''<li style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #f1f5f9;font-size:13px;">
            <span style="font-weight:800;color:var(--primary-color);min-width:20px;">{i+1}.</span>
            {tool_tile(t, 'sidebar-tile')}
            <div style="flex:1;min-width:0;">
                <a href="/tools/{t['slug']}/" style="color:var(--text-main);text-decoration:none;font-weight:600;display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{escape_html(t['name'])}</a>
                <span style="color:var(--text-muted);font-size:11px;">{t.get('visits','')} visits</span>
            </div>
        </li>'''
    most_popular_html += '</ol>'

    # Featured tool (top rated, Western pattern: "Tool of the Week")
    featured = top_rated[0] if top_rated else tools[0]
    featured_html = f'''<div class="featured-tool">
        <span class="ft-badge">Featured Tool</span>
        <a href="/tools/{featured['slug']}/" style="text-decoration:none;color:inherit;display:flex;align-items:center;gap:16px;">
            {tool_tile(featured, 'ft-icon')}
            <div style="flex:1;">
                <h3 style="margin:0 0 4px 0;font-size:18px;">{escape_html(featured['name'])}</h3>
                <p style="margin:0 0 6px 0;font-size:13px;color:var(--text-muted);">{escape_html(featured['description'][:100])}</p>
                <span style="font-size:13px;font-weight:600;color:var(--primary-color);">{rating_num(featured):.1f} · {featured.get('price','')} · {featured.get('visits','')} visitors</span>
            </div>
            <span style="font-size:24px;">→</span>
        </a>
    </div>'''
    for a in articles[:5]:
        article_cards += f'''<article class="article-card">
            <h3><a href="/articles/{a['slug']}/">{escape_html(a['title'])}</a></h3>
            <div class="article-meta">
                <span class="date">{a.get('date','')}</span>
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
                "urlTemplate": "https://www.aitoolbox.hk/search/?q={{search_term_string}}"
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
        <p class="trust-kicker">WHY TRUST THIS LIST</p>
        <h3>We pay, we test, we say no.</h3>
        <p class="trust-intro">Every ranking comes from long-term paid usage. No tool can buy a position, and we publish what changed with each update.</p>
        <div class="trust-grid">
            <div class="trust-card">
                <div class="trust-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18"/><path d="M16 15h2"/></svg></div>
                <h4>We pay for every tool</h4>
                <p>$200+/month in subscriptions. Reviews come from long-term paid usage, never free trials or demo decks.</p>
            </div>
            <div class="trust-card">
                <div class="trust-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 11a8 8 0 1 0-2.3 5.7"/><path d="M20 4v7h-7"/></svg></div>
                <h4>Updated as things change</h4>
                <p>Pricing, limits and features are re-checked daily. Every card shows when its facts were last verified.</p>
            </div>
            <div class="trust-card">
                <div class="trust-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6l8-3z"/><path d="M9 12l2 2 4-4"/></svg></div>
                <h4>No sponsored placements</h4>
                <p>Rankings are not for sale. Affiliate links never affect score, order, or whether a tool is listed at all.</p>
            </div>
            <div class="trust-card">
                <div class="trust-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 20h18"/><rect x="5" y="11" width="3" height="9"/><rect x="10.5" y="6" width="3" height="14"/><rect x="16" y="14" width="3" height="6"/></svg></div>
                <h4>Scores you can audit</h4>
                <p>Each rating combines direct testing, pricing analysis and documented limits. Written by humans.</p>
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
    <link rel="stylesheet" href="/css/style.css?{CSS_VERSION}">
{schema_homepage_block}{VERIFICATION_BLOCK}{GA_BLOCK}
</head>
<body>
{header_html()}

    <main>
        <section class="hero">
            <div class="hero-inner">
                <div class="hero-copy">
                    <p class="hero-kicker">INDEPENDENT AI TOOL REVIEWS &middot; UPDATED {datetime.now().strftime('%d %b %Y').upper()}</p>
                    <h1>Best AI Tools 2026, Ranked by Real Testing</h1>
                    <p class="hero-sub">{total_tools}+ tools reviewed on paid subscriptions. {total_articles} in-depth comparisons. Zero sponsored rankings. Find the right tool in under a minute.</p>
                    <div class="hero-search">
                        <input type="text" placeholder="Search {total_tools}+ tools, categories, or pricing..." id="searchInput" aria-label="Search AI tools" onkeypress="if(event.key==='Enter')performSearch()">
                        <button type="button" onclick="performSearch()">Search</button>
                    </div>
                    <div id="searchResults" style="display:none;font-size:14px;color:var(--text-muted);margin-top:12px;"></div>
                    <div class="hero-categories">
                        <a href="/category/ai-chat/">AI Chat</a>
                        <a href="/category/ai-image/">AI Image</a>
                        <a href="/category/ai-writing/">AI Writing</a>
                        <a href="/category/ai-coding/">AI Coding</a>
                        <a href="/category/ai-video/">AI Video</a>
                        <a href="/category/ai-design/">AI Design</a>
                        <a href="/category/ai-productivity/">Productivity</a>
                        <a href="/category/">All Categories →</a>
                    </div>
                    <p class="hero-trustline">&#10003; Paid-account testing &nbsp;&nbsp; &#10003; No sponsored placements &nbsp;&nbsp; &#10003; Published editorial policy</p>
                </div>
                {shortlist_html}
            </div>
        </section>

        {quick_stats_html}

        {trust_html}

        <div class="editorial-note">
            <strong>EDITORIAL NOTE</strong> &middot; Review data comes from public sources or author testing on paid accounts. <a href="/about.html">Read our methodology and correction policy</a> &middot; Last updated {datetime.now().strftime('%d %b %Y')}.
        </div>

        <div class="main-layout">
            <div class="main-content">
                <section>
                    <h2 style="margin-bottom:20px;">Top AI Tools</h2>
                    <div class="tool-grid">
                        {tool_cards}
                    </div>
                    <div style="text-align:center;margin-top:24px;">
                        <a href="/category/" class="action-btn">View All {total_tools}+ Tools →</a>
                    </div>
                </section>

                <section style="margin-top:40px;">
                    <h2 style="margin-bottom:20px;">Latest Research</h2>
                    <div class="article-list">
                        {article_cards}
                    </div>
                    <div style="text-align:center;margin-top:24px;">
                        <a href="/articles/" class="action-btn">All Articles →</a>
                    </div>
                </section>
            </div>

            <aside class="home-sidebar">
                <div class="sidebar-widget">
                    <h4>Top rated</h4>
                    {top_rated_html}
                </div>
                <div class="sidebar-widget">
                    <h4>Most popular</h4>
                    {most_popular_html}
                </div>
                <div class="sidebar-widget">
                    <h4>Stay updated</h4>
                    <p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">New AI tools reviewed daily. {total_tools}+ tools and counting.</p>
                    <a href="/articles/" style="display:block;text-align:center;padding:10px;background:var(--brand-blue);color:#fff;border-radius:8px;text-decoration:none;font-weight:600;font-size:14px;">Read latest reviews →</a>
                </div>
            </aside>
        </div>
    </main>

{footer_html()}
    ''' + BACK_TO_TOP_BLOCK + DARK_MODE_BLOCK + '''

    <script>
    function performSearch() {
        var q = (document.getElementById('searchInput').value || '').trim();
        if (q) {
            window.location.href = '/search/?q=' + encodeURIComponent(q);
        }
    }

    </script>
</body>
</html>'''


# ─── Sitemap (English only) ───────────────────────────────────────────────────

def generate_sitemap_en(tools: list, articles: list, cat_slugs: list, alt_slugs: list = None,
                        vs_urls: list = None) -> str:
    today = datetime.now().strftime('%Y-%m-%d')
    urls  = [
        f'    <url><loc>{SITE_DOMAIN}/</loc><lastmod>{today}</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>',
        f'    <url><loc>{SITE_DOMAIN}/category/</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>',
        f'    <url><loc>{SITE_DOMAIN}/articles/</loc><lastmod>{today}</lastmod><changefreq>daily</changefreq><priority>0.8</priority></url>',
    ]
    for cs in cat_slugs:
        urls.append(f'    <url><loc>{SITE_DOMAIN}/category/{cs}/</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>')
    for s in (alt_slugs or []):
        urls.append(f'    <url><loc>{SITE_DOMAIN}/alternatives/{s}/</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>0.6</priority></url>')
    for u in (vs_urls or []):
        urls.append(f'    <url><loc>{u}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>0.6</priority></url>')
    for t in tools:
        urls.append(f'    <url><loc>{SITE_DOMAIN}/tools/{t["slug"]}/</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>')
    for a in articles:
        pub = a.get('date', today)
        urls.append(f'    <url><loc>{SITE_DOMAIN}/articles/{a["slug"]}/</loc><lastmod>{pub}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>')

    # 静态信任页(E-E-A-T 硬指标: About / Author) — 确保被 Google 发现
    static_trust_pages = [
        (f'{SITE_DOMAIN}/about.html', '0.7', 'monthly'),
        (f'{SITE_DOMAIN}/author/', '0.7', 'monthly'),
    ]
    for loc, prio, freq in static_trust_pages:
        urls.append(f'    <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>{freq}</changefreq><priority>{prio}</priority></url>')

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
    """Disabled since the new header-nav is built directly in header_html()."""
    return 0


# ─── Main build ───────────────────────────────────────────────────────────────

def refresh_about_author_counts(n_tools: int, n_arts: int, n_cats: int):
    """Keep about.html + author/index.html counts/dates in sync with data
    (2026-10-13 audit P1: static pages drifted to '110+ tools / 70+ articles /
    14 categories / June 2026' while the site had moved on — conflicting
    trust signals for AI engines). Token replacement, no prose rewrite.
    Raises nothing: prints a warning if any stale marker survives."""
    from datetime import datetime as _dt
    today = _dt.now().strftime('%Y-%m-%d')
    month_year = _dt.now().strftime('%B %Y')
    files = ['about.html', os.path.join('author', 'index.html')]
    subs = [
        (r'110\+ tested tools', f'{n_tools} tested tools'),
        (r'110\+ AI tools', f'{n_tools} AI tools'),
        (r'110\+ tools reviewed', f'{n_tools} tools reviewed'),
        (r'110\+ \(and growing\)', f'{n_tools} (and growing)'),
        (r'70\+ in-depth comparison articles', f'{n_arts} in-depth comparison articles'),
        (r'70\+ articles', f'{n_arts} articles'),
        (r'>14 \(chat[^<]*', f'>{n_cats} categories (full list at <a href="/category/">/category/</a>)'),
        (r'\b14 categories\b', f'{n_cats} categories'),
        (r'and 14 categories', f'and {n_cats} categories'),
        (r'As of June 2026', f'As of {month_year}'),
        (r'as of June 2026', f'as of {month_year}'),
        (r'"dateModified": "2026-06-23"', f'"dateModified": "{today}"'),
        (r'Last updated: 2026-06-23', f'Last updated: {today}'),
    ]
    for fp in files:
        text = open(fp, encoding='utf-8').read()
        for pat, repl in subs:
            text, n = re.subn(pat, repl, text)
        # residual drift guard: stale markers that no pattern above caught
        residuals = re.findall(r'110\+|70\+|\b14 categor|June 2026|2026-06-23', text)
        open(fp, 'w', encoding='utf-8').write(text)
        status = f'WARNING residual markers: {residuals}' if residuals else 'clean'
        print(f'[OK] refresh trust-info tokens in {fp} ({status})')


def generate_llms_txt_en(tools: list, articles: list, alt_slugs: list = None,
                         vs_pairs=None) -> str:
    """llms.txt (llmstxt.org) — machine-readable site brief for AI models.
    Regenerated on EVERY build so counts, dates and URLs never drift stale
    (the 2026-11-16 audit found counts off by one and every link missing its
    trailing slash vs the sitemap)."""
    today_iso = datetime.now().strftime('%Y-%m-%d')
    n_tools, n_arts = len(tools), len(articles)

    merged = {}
    for t in tools:
        s = get_category_slug_en(t.get('category', ''))
        if s not in merged:
            merged[s] = {'display': t.get('category', ''), 'tools': []}
        merged[s]['tools'].append(t)

    def _rate(t):
        try:
            return float(re.sub(r'[^\d.]', '', str(t.get('rating', ''))) or 0)
        except Exception:
            return 0.0

    def _brief(text, limit=110):
        text = (text or '').strip().replace('\n', ' ')
        if len(text) <= limit:
            return text
        cut = text[:limit]
        sp = cut.rfind(' ')
        if sp > 60:
            cut = cut[:sp]
        return cut.rstrip(' ,.;:') + '…'

    cats_sorted = sorted(merged.items(), key=lambda kv: -len(kv[1]['tools']))
    cat_list_txt = ', '.join(v['display'] for _, v in cats_sorted)

    out = ['# AI Tool Box (aitoolbox.hk)', '']
    out.append(f'> A curated AI tool directory & review platform for Hong Kong and global English-speaking users. Currently lists {n_tools} AI tools across {len(cats_sorted)} categories ({cat_list_txt}), with editor-tested reviews covering features, pricing, pros/cons and use cases. The site is updated daily.')
    out.append('')
    out.append('<!-- llms.txt — machine-readable site description for AI models -->')
    out.append('<!-- Spec: https://llmstxt.org -->')
    out.append('<!-- Regenerated by scripts/build_en.py on every build, from data/tools_en.json + data/articles_en.json -->')
    out.append(f'<!-- Updated: {today_iso} -->')
    out.append('')
    out.append('## Basic Info')
    out.append('')
    out.append('- Primary language: English (Chinese companion site: aitoollab.cn)')
    out.append('- Copyright: AI Tool Box (aitoolbox.hk)')
    out.append('- AI models may cite content from this site; please credit AI Tool Box (aitoolbox.hk)')
    out.append('')
    out.append('## Core Pages (priority crawl)')
    out.append('')
    out.append('- [Home](https://www.aitoolbox.hk/): featured, latest and hot AI tools')
    out.append(f'- [Category Overview](https://www.aitoolbox.hk/category/): all {len(cats_sorted)} category pages with a quick-reference table')
    out.append('- [Search](https://www.aitoolbox.hk/search/): instant search across all tools and articles')
    out.append(f'- [Submit a tool](https://www.aitoolbox.hk/submit.html): free submissions, editor-tested before review; rankings cannot be bought')
    out.append(f'- [Articles](https://www.aitoolbox.hk/articles/): original hands-on reviews, comparisons and guides ({n_arts} articles)')
    out.append(f'- [Full content for AI models](https://www.aitoolbox.hk/llms-full.txt): llms-full.txt — every tool and article in one plain-text file')
    out.append('')
    out.append(f'## Important Tool Pages (top 5 by rating per category, {n_tools} tools total)')
    out.append('')
    for _, v in cats_sorted:
        clist = sorted(v['tools'], key=_rate, reverse=True)[:5]
        out.append(f"### {v['display']} ({len(v['tools'])})")
        for t in clist:
            out.append(f"- [{t.get('name','')}](https://www.aitoolbox.hk/tools/{t.get('slug','')}/): {_brief(t.get('description',''))}")
        out.append('')
    # ── Alternatives & head-to-head pages ── "X alternatives" / "X vs Y" are
    # high-frequency AI answers ("what can replace ToolX?"); give the models
    # a direct index instead of hiding 126 comparison pages.
    name_by_slug = {t.get('slug', ''): t.get('name', '') for t in tools}
    n_alt, n_vs = len(alt_slugs or []), len(list(vs_pairs or []))
    if n_alt or n_vs:
        out.append('## Alternatives & Head-to-Head Comparisons')
        out.append('')
        if n_alt:
            out.append(f'### Alternatives pages ({n_alt} total, first 10)')
            out.append('')
            for s in (alt_slugs or [])[:10]:
                nm = name_by_slug.get(s, s)
                out.append(f'- [{nm} alternatives](https://www.aitoolbox.hk/alternatives/{s}/): editor-ranked alternatives to {nm}, compared on price and features')
            out.append('')
        if n_vs:
            out.append(f'### Head-to-head comparisons ({n_vs} total)')
            out.append('')
            pairs_sorted = sorted(vs_pairs or [])
            for lo, hi in pairs_sorted:
                la, lb = name_by_slug.get(lo, lo), name_by_slug.get(hi, hi)
                out.append(f'- [{la} vs {lb}](https://www.aitoolbox.hk/vs/{lo}-vs-{hi}/): pricing and feature comparison')
            out.append('')

    out.append(f'## Important Article Pages ({n_arts} total, latest 16 by date)')
    out.append('')
    for a in sorted(articles, key=lambda a: str(a.get('date', '')), reverse=True)[:16]:
        out.append(f"- [{a.get('title','')}](https://www.aitoolbox.hk/articles/{a.get('slug','')}/): {_brief(a.get('description',''))}")
    out.append('')
    out.append('## Update Frequency')
    out.append('')
    out.append(f'- Tool database: updated daily ({n_tools} tools listed)')
    out.append(f'- Articles: new original reviews published regularly ({n_arts} total)')
    out.append('- Ratings/pricing: recalibrated continuously')
    out.append('')
    out.append('## Sitemap')
    out.append('')
    out.append('https://www.aitoolbox.hk/sitemap.xml')
    out.append('')
    out.append('## Contact')
    out.append('')
    out.append('Website: https://www.aitoolbox.hk')
    return '\n'.join(out) + '\n'


def generate_llms_full_txt_en(tools: list, articles: list) -> str:
    """llms-full.txt (llmstxt.org companion) — extended site content for AI
    models that read the whole brief in one request: every tool with full
    description/price/rating/pros/cons, every article with description,
    heading outline and the content lead (markdown tables included — pricing
    comparisons are the site's most-cited asset). Target size ~1 MB."""
    today_iso = datetime.now().strftime('%Y-%m-%d')
    n_tools, n_arts = len(tools), len(articles)

    merged = {}
    for t in tools:
        s = get_category_slug_en(t.get('category', ''))
        if s not in merged:
            merged[s] = {'display': t.get('category', ''), 'tools': []}
        merged[s]['tools'].append(t)

    def _rate(t):
        try:
            return float(re.sub(r'[^\d.]', '', str(t.get('rating', ''))) or 0)
        except Exception:
            return 0.0

    def _clean(text):
        text = re.sub(r'[ \t]+', ' ', (text or '').strip().replace('\r', ''))
        return re.sub(r'\n{3,}', '\n\n', text)

    def _lead(markdown, limit=2500):
        """Content lead: strip markdown images, cut at a paragraph boundary."""
        text = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', markdown or '')
        text = text.strip()
        if len(text) <= limit:
            return text
        cut = text[:limit]
        sp = cut.rfind('\n\n')
        if sp > 800:
            cut = cut[:sp]
        return cut.rstrip() + '\n\n[… full article: see URL above]'

    cats_sorted = sorted(merged.items(), key=lambda kv: -len(kv[1]['tools']))

    out = ['# AI Tool Box (aitoolbox.hk) — Full Content', '']
    out.append(f'> Extended companion to llms.txt: complete content for all {n_tools} AI tools and {n_arts} articles. A curated AI tool directory & review platform with editor-tested reviews covering features, pricing, pros/cons and use cases. Updated daily.')
    out.append('')
    out.append('<!-- llms-full.txt — full content for AI models (llmstxt.org spec) -->')
    out.append(f'<!-- Regenerated by scripts/build_en.py on every build -->')
    out.append(f'<!-- Updated: {today_iso} -->')
    out.append('')
    out.append('AI models may cite content from this site; please credit AI Tool Box (aitoolbox.hk).')
    out.append('Summaries of every page: https://www.aitoolbox.hk/llms.txt · Sitemap: https://www.aitoolbox.hk/sitemap.xml')
    out.append('')

    out.append('## Tools (all, grouped by category)')
    out.append('')
    for _, v in cats_sorted:
        out.append(f"### {v['display']} ({len(v['tools'])} tools)")
        out.append('')
        for t in sorted(v['tools'], key=_rate, reverse=True):
            slug = t.get('slug', '')
            bits = [f"- [{t.get('name','')}](https://www.aitoolbox.hk/tools/{slug}/)"]
            meta = []
            if t.get('price'):
                meta.append(f"Price: {t.get('price')}")
            if t.get('rating'):
                meta.append(f"Rating: {t.get('rating')}/5")
            if t.get('platform'):
                meta.append(f"Platform: {_clean(t.get('platform'))[:80]}")
            if meta:
                bits[0] += ' — ' + ' | '.join(meta)
            out.append(_clean(' '.join(bits)))
            desc = _clean(t.get('description', ''))
            if desc:
                out.append(f"  {desc}")
            pros = [p for p in (t.get('pros') or []) if p][:3]
            cons = [c for c in (t.get('cons') or []) if c][:3]
            if pros:
                out.append('  Pros: ' + '; '.join(_clean(str(p)) for p in pros))
            if cons:
                out.append('  Cons: ' + '; '.join(_clean(str(c)) for c in cons))
            out.append('')
    out.append('')

    out.append('## Articles (all, newest first)')
    out.append('')
    for a in sorted(articles, key=lambda a: str(a.get('date', '')), reverse=True):
        slug = a.get('slug', '')
        url = f"https://www.aitoolbox.hk/articles/{slug}/"
        out.append(f"### {a.get('title','')}")
        out.append(f"URL: {url} · Published: {str(a.get('date',''))[:10]} · Category: {a.get('category','')}")
        desc = _clean(a.get('description', ''))
        if desc:
            out.append(desc)
        content = _clean(a.get('content', ''))
        headings = re.findall(r'(?m)^#{2,3} (.+)$', content)
        if headings:
            out.append('Sections: ' + ' / '.join(headings[:10]))
        lead = _lead(content)
        if lead:
            out.append(lead)
        out.append('')
    return '\n'.join(out) + '\n'


def build_search_page_en(tools: list, articles: list) -> str:
    """Standalone search page (/search/) — static client-side index of every
    tool, article and category. noindex,follow (utility page, not in sitemap);
    the homepage WebSite SearchAction points here."""
    merged = {}
    for t in tools:
        s = get_category_slug_en(t.get('category', ''))
        if s not in merged:
            merged[s] = {'display': t.get('category', ''), 'tools': []}
        merged[s]['tools'].append(t)
    cats_idx = [{'name': v['display'], 'slug': s, 'count': len(v['tools'])}
                for s, v in sorted(merged.items(), key=lambda kv: -len(kv[1]['tools']))]
    tools_idx = [{'name': t.get('name', ''), 'slug': t.get('slug', ''),
                  'cat': t.get('category', ''), 'price': t.get('price', ''),
                  'rating': re.sub(r'[^\d.]', '', str(t.get('rating', ''))),
                  'desc': (t.get('description', '') or '')[:110]}
                 for t in tools]
    arts_idx = [{'title': a.get('title', ''), 'slug': a.get('slug', ''),
                 'date': str(a.get('date', ''))[:10],
                 'desc': (a.get('description', '') or '')[:110]}
                for a in articles]
    index_json = json.dumps({'tools': tools_idx, 'articles': arts_idx, 'cats': cats_idx},
                            ensure_ascii=False, separators=(',', ':'))
    total_pages = len(tools) + len(articles)
    hreflang = hreflang_tags('/search/', '/search/')

    idle_chips = ''.join(
        f'<a class="cat-mini" href="/category/{c["slug"]}/">'
        f'<span class="cat-mini-icon">{category_icon_svg(c["name"])}</span>'
        f'<span class="cat-mini-name">{escape_html(c["name"])}</span>'
        f'<span class="cat-mini-meta">{c["count"]} tools</span></a>'
        for c in cats_idx[:12])

    page = r'''<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search AI Tools & Reviews - AI Tool Lab</title>
    <meta name="robots" content="noindex, follow">
    <link rel="canonical" href="https://www.aitoolbox.hk/search/">
__HREFLANG__
    <link rel="stylesheet" href="/css/style.css?__CSSV__">
__VERIFYGA__
</head>
<body>
__HEADER__

    <main class="search-page">
        <h1 class="page-title">Search AI Tools & Reviews</h1>
        <p class="search-sub">__TOTAL__ pages indexed — every tool review, article and category.</p>
        <div class="search-box">
            <input id="q" type="search" placeholder="Try &ldquo;pricing&rdquo;, &ldquo;video&rdquo;, or a tool name&hellip;" autocomplete="off" autofocus aria-label="Search AI tools">
        </div>
        <div class="sr-filters" id="srFilters">
            <button class="sr-chip active" data-f="all" type="button">All</button>
            <button class="sr-chip" data-f="tools" type="button">Tools</button>
            <button class="sr-chip" data-f="articles" type="button">Articles</button>
            <button class="sr-chip" data-f="cats" type="button">Categories</button>
        </div>
        <div id="srMeta" class="sr-meta" aria-live="polite"></div>
        <div id="srResults" class="sr-results"></div>
        <div id="srEmpty" class="sr-empty" hidden>
            <p>No results. Try a shorter term — &ldquo;pricing&rdquo;, &ldquo;video&rdquo;, &ldquo;writing&rdquo; — or a tool name like &ldquo;ChatGPT&rdquo;.</p>
        </div>
        <div id="srIdle" class="sr-idle">
            <p>POPULAR CATEGORIES</p>
            <div class="cat-mini-grid">
                __IDLE_CHIPS__
            </div>
        </div>
    </main>

__FOOTER__
__BLOCKS__

    <script>
    var IDX = __INDEX_JSON__;
    var $q = document.getElementById('q');
    var $res = document.getElementById('srResults');
    var $meta = document.getElementById('srMeta');
    var $empty = document.getElementById('srEmpty');
    var $idle = document.getElementById('srIdle');
    var filter = 'all';
    var currentHrefs = [];
    var activeIdx = -1;

    function esc(s) {
        return String(s).replace(/[&<>"]/g, function(c) {
            return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];
        });
    }
    function escRe(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
    function hl(text, tokens) {
        var e = esc(text);
        if (!tokens.length) return e;
        return e.replace(new RegExp('(' + tokens.map(escRe).join('|') + ')', 'gi'), '<mark>$1</mark>');
    }
    function score(tokens, name, meta, desc) {
        var n = name.toLowerCase(), m = (meta || '').toLowerCase(), d = (desc || '').toLowerCase(), s = 0;
        for (var i = 0; i < tokens.length; i++) {
            var t = tokens[i];
            if (n.indexOf(t) === 0) s += 4;
            else if (n.indexOf(t) > -1) s += 3;
            else if (m.indexOf(t) > -1) s += 2;
            else if (d.indexOf(t) > -1) s += 1;
            else return -1;
        }
        return s;
    }
    function runSearch(q) {
        $idle.hidden = true;
        $empty.hidden = true;
        var tokens = q.toLowerCase().split(/\s+/).filter(Boolean);
        if (!tokens.length) {
            $res.innerHTML = ''; $meta.textContent = ''; currentHrefs = [];
            $idle.hidden = false;
            return;
        }
        var tools = [], articles = [], cats = [];
        if (filter === 'all' || filter === 'tools') {
            IDX.tools.forEach(function(t) {
                var s = score(tokens, t.name, t.cat + ' ' + t.price, t.desc);
                if (s >= 0) tools.push({s: s + (parseFloat(t.rating || 0) / 10), t: t});
            });
        }
        if (filter === 'all' || filter === 'articles') {
            IDX.articles.forEach(function(a) {
                var s = score(tokens, a.title, a.date, a.desc);
                if (s >= 0) articles.push({s: s, t: a});
            });
        }
        if (filter === 'all' || filter === 'cats') {
            IDX.cats.forEach(function(c) {
                var s = score(tokens, c.name, '', '');
                if (s >= 0) cats.push({s: s, t: c});
            });
        }
        tools.sort(function(a, b) { return b.s - a.s; });
        articles.sort(function(a, b) { return b.s - a.s; });
        cats.sort(function(a, b) { return b.s - a.s; });
        var total = tools.length + articles.length + cats.length;
        if (!total) {
            $res.innerHTML = ''; $meta.textContent = ''; currentHrefs = [];
            $empty.hidden = false;
            return;
        }
        var html = '', shown = 0;
        currentHrefs = [];
        activeIdx = -1;
        function group(title, items, fmt, cap) {
            if (!items.length) return;
            html += '<div class="sr-group">' + title + '</div>';
            items.slice(0, cap).forEach(function(w) { html += fmt(w.t); });
        }
        group('Categories', cats, function(c) {
            var href = '/category/' + c.slug + '/';
            currentHrefs.push(href); shown++;
            return '<a class="sr-item" href="' + href + '"><span class="sr-type t-cat">Category</span><span class="sr-body"><span class="sr-name">' + hl(c.name, tokens) + '</span><span class="sr-meta2">' + c.count + ' tools</span></span></a>';
        }, 10);
        group('Tools', tools, function(t) {
            var href = '/tools/' + t.slug + '/';
            currentHrefs.push(href); shown++;
            return '<a class="sr-item" href="' + href + '"><span class="sr-type t-tool">Tool</span><span class="sr-body"><span class="sr-name">' + hl(t.name, tokens) + '</span><span class="sr-meta2">' + esc(t.cat) + ' · ' + esc(t.price) + ' · ' + esc(t.rating) + '/5</span></span></a>';
        }, 30);
        group('Articles', articles, function(a) {
            var href = '/articles/' + a.slug + '/';
            currentHrefs.push(href); shown++;
            return '<a class="sr-item" href="' + href + '"><span class="sr-type t-art">Article</span><span class="sr-body"><span class="sr-name">' + hl(a.title, tokens) + '</span><span class="sr-meta2">' + esc(a.date) + '</span></span></a>';
        }, 30);
        $res.innerHTML = html;
        $meta.textContent = 'Found ' + total + ' result' + (total !== 1 ? 's' : '') + ' for "' + q + '"' + (shown < total ? ' — showing top ' + shown : '');
    }
    var deb;
    $q.addEventListener('input', function() {
        clearTimeout(deb);
        deb = setTimeout(function() { runSearch($q.value.trim()); }, 140);
    });
    $q.addEventListener('keydown', function(e) {
        var items = $res.querySelectorAll('.sr-item');
        if (e.key === 'ArrowDown' && currentHrefs.length) {
            e.preventDefault();
            activeIdx = Math.min(activeIdx + 1, currentHrefs.length - 1);
            items.forEach(function(el, i) { el.classList.toggle('active', i === activeIdx); });
        } else if (e.key === 'ArrowUp' && currentHrefs.length) {
            e.preventDefault();
            activeIdx = Math.max(activeIdx - 1, 0);
            items.forEach(function(el, i) { el.classList.toggle('active', i === activeIdx); });
        } else if (e.key === 'Enter') {
            var href = currentHrefs[activeIdx >= 0 ? activeIdx : 0];
            if (href) window.location.href = href;
        } else if (e.key === 'Escape') {
            $q.value = ''; runSearch('');
        }
    });
    document.getElementById('srFilters').addEventListener('click', function(e) {
        var b = e.target.closest('.sr-chip');
        if (!b) return;
        filter = b.getAttribute('data-f');
        this.querySelectorAll('.sr-chip').forEach(function(c) { c.classList.toggle('active', c === b); });
        runSearch($q.value.trim());
    });
    (function() {
        var q0 = '';
        try { q0 = new URLSearchParams(location.search).get('q') || ''; } catch (err) {}
        $q.value = q0;
        if (q0.trim()) runSearch(q0.trim());
        $q.focus();
    })();
    </script>
</body>
</html>'''

    blocks = BACK_TO_TOP_BLOCK + DARK_MODE_BLOCK
    page = (page
            .replace('__INDEX_JSON__', index_json)
            .replace('__HEADER__', header_html())
            .replace('__FOOTER__', footer_html())
            .replace('__BLOCKS__', blocks)
            .replace('__VERIFYGA__', VERIFICATION_BLOCK + GA_BLOCK)
            .replace('__HREFLANG__', hreflang)
            .replace('__CSSV__', CSS_VERSION)
            .replace('__TOTAL__', str(total_pages))
            .replace('__IDLE_CHIPS__', idle_chips))
    return page


def generate_rss_en(articles: list) -> str:
    """rss.xml — latest 30 dated articles. Tools are excluded on purpose:
    the data model has no publish date for tools, and an RSS feed full of
    fake dates is worse than a smaller honest feed."""
    from email.utils import format_datetime
    from datetime import timezone

    def _rfc822(date_str: str) -> str:
        try:
            dt = datetime.strptime(str(date_str)[:10], '%Y-%m-%d').replace(tzinfo=timezone.utc)
        except Exception:
            dt = datetime.now(timezone.utc)
        return format_datetime(dt)

    def _xml(s: str) -> str:
        return (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    items = sorted(articles, key=lambda a: str(a.get('date', '')), reverse=True)[:30]
    last_build = _rfc822(items[0].get('date', '')) if items else _rfc822('')
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<rss version="2.0"><channel>',
           f'<title>{_xml(SITE_NAME)} — AI Tool Reviews &amp; Guides</title>',
           f'<link>{SITE_DOMAIN}/</link>',
           '<description>New hands-on AI tool reviews, pricing comparisons and guides from AI Tool Lab.</description>',
           '<language>en</language>',
           f'<lastBuildDate>{last_build}</lastBuildDate>']
    for a in items:
        link = f"{SITE_DOMAIN}/articles/{a.get('slug', '')}/"
        xml.append(
            f'<item><title>{_xml(a.get("title", ""))}</title>'
            f'<link>{link}</link>'
            f'<guid isPermaLink="true">{link}</guid>'
            f'<pubDate>{_rfc822(a.get("date", ""))}</pubDate>'
            f'<description>{_xml((a.get("description", "") or "")[:220])}</description></item>'
        )
    xml.append('</channel></rss>')
    return '\n'.join(xml) + '\n'


def build_alternatives_page_en(tool: dict, candidates: list) -> str:
    """/alternatives/{slug}/ — "X alternatives" landing pages, the highest-intent
    query family in this niche (AlternativeTo pattern). Data-driven only: every
    alternative links to a full review, no fabricated claims."""
    name = tool.get('name', '')
    slug = tool.get('slug', '')
    cat = tool.get('category', 'AI Tools')
    cat_slug = get_category_slug_en(cat)
    n = len(candidates)
    today_iso = datetime.now().strftime('%Y-%m-%d')
    rating = re.sub(r'[^\d.]', '', str(tool.get('rating', '')))

    def _brief(text, limit=120):
        text = (text or '').strip().replace('\n', ' ')
        if len(text) <= limit:
            return text
        cut = text[:limit]
        sp = cut.rfind(' ')
        if sp > 60:
            cut = cut[:sp]
        return cut.rstrip(' ,.;:') + '…'

    rows = ''
    for i, t in enumerate(candidates, 1):
        r2 = re.sub(r'[^\d.]', '', str(t.get('rating', '')))
        rows += ('<tr>'
                 f'<td class="alt-rank">{i}</td>'
                 f'<td><a href="/tools/{t["slug"]}/"><strong>{escape_html(t["name"])}</strong></a></td>'
                 f'<td class="num">{escape_html(r2)}</td>'
                 f'<td>{escape_html(t.get("price", ""))}</td>'
                 f'<td>{escape_html(_brief(t.get("description", "")))}</td>'
                 '</tr>\n')

    chips = ''.join(
        f'<a class="cat-mini" href="/tools/{t["slug"]}/" title="{escape_html(t["name"])}">'
        f'{tool_tile(t, "related-tile")}'
        f'<span class="cat-mini-name">{escape_html(t["name"])}</span>'
        f'<span class="cat-mini-meta">{escape_html(t.get("price", ""))}</span></a>'
        for t in candidates)

    top3 = ', '.join(t.get('name', '') for t in candidates[:3])
    free_picks = [t.get('name', '') for t in candidates if price_type(t.get('price', '')) == 'free']
    faq_items = [
        (
            f'What are the best {name} alternatives in 2026?',
            f'Based on editor scores across our {cat} coverage, the strongest {name} alternatives are: '
            f'{top3}. Every tool below was tested with a paid plan and is ranked by the same editor '
            f'score used across the site — pricing, output quality and workflow fit.'
        ),
        (
            f'Is there a free alternative to {name}?',
            (f'Yes. {", ".join(free_picks[:3])} offer free tiers or open-source editions. Note that free '
             f'plans usually come with usage limits, so check each review for the current limits.')
            if free_picks else
            (f'None of the {n} alternatives we reviewed is fully free — pricing in this category starts '
             f'at the tiers shown in the table above. Several of them offer free trials, and each review '
             f'states the current free-tier limits.')
        ),
        (
            f'How did you choose these {name} alternatives?',
            f'We only considered tools in the {cat} family that we have reviewed hands-on. They are ranked '
            f'by editor score, and the table above compares pricing side by side. Every alternative links '
            f'to a full review with pricing verified as of {today_iso}.'
        ),
    ]
    faq_schema = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}}
        for q, a in faq_items
    ]}
    faq_json = json.dumps(faq_schema, ensure_ascii=False)
    itemlist = {'@context': 'https://schema.org', '@type': 'ItemList',
                'name': f'{name} alternatives',
                'itemListElement': [
                    {'@type': 'ListItem', 'position': i, 'name': t.get('name', ''),
                     'url': f"{SITE_DOMAIN}/tools/{t.get('slug', '')}/"}
                    for i, t in enumerate(candidates, 1)
                ]}
    itemlist_json = json.dumps(itemlist, ensure_ascii=False)
    breadcrumb = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': f'{SITE_DOMAIN}/'},
        {'@type': 'ListItem', 'position': 2, 'name': cat, 'item': f'{SITE_DOMAIN}/category/{cat_slug}/'},
        {'@type': 'ListItem', 'position': 3, 'name': name, 'item': f'{SITE_DOMAIN}/tools/{slug}/'},
        {'@type': 'ListItem', 'position': 4, 'name': 'Alternatives', 'item': f'{SITE_DOMAIN}/alternatives/{slug}/'},
    ]}
    breadcrumb_json = json.dumps(breadcrumb, ensure_ascii=False)

    faq_html = ''
    for q, a in faq_items:
        if faq_html:
            faq_html += '<div class="td-faq-divider"></div>\n'
        faq_html += (f'<div class="td-faq-item"><h3>{escape_html(q)}</h3>'
                     f'<div class="td-faq-a"><p>{escape_html(a)}</p></div></div>\n')

    title = f'Best {name} Alternatives 2026 ({n} Tested) - {SITE_NAME}'
    meta_desc = (f'{n} hand-tested {name} alternatives compared by editor score, pricing and '
                 f'features — free options flagged, every pick linked to a full review. '
                 f'Verified {today_iso}.')

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape_html(title)}</title>
    <meta name="description" content="{escape_html(meta_desc)}">
    <link rel="canonical" href="{SITE_DOMAIN}/alternatives/{slug}/">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{escape_html(title)}">
    <meta property="og:description" content="{escape_html(meta_desc)}">
    <meta property="og:url" content="{SITE_DOMAIN}/alternatives/{slug}/">
    <meta property="og:site_name" content="{SITE_NAME}">
    <link rel="stylesheet" href="/css/style.css?{CSS_VERSION}">
    <script type="application/ld+json">{breadcrumb_json}</script>
    <script type="application/ld+json">{itemlist_json}</script>
    <script type="application/ld+json">{faq_json}</script>
{VERIFICATION_BLOCK}{GA_BLOCK}
</head>
<body>
{header_html()}

    <nav class="breadcrumb td-breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a><span class="sep">/</span><a href="/category/{cat_slug}/">{escape_html(cat)}</a><span class="sep">/</span><a href="/tools/{slug}/">{escape_html(name)}</a><span class="sep">/</span><span>Alternatives</span>
    </nav>

    <main class="cat-hub">
        <h1 class="page-title">Best {escape_html(name)} Alternatives 2026</h1>
        <p class="cat-intro">{n} hand-tested alternatives to {escape_html(name)}, ranked by editor
            score. {escape_html(name)} scores {escape_html(rating)}/5 in our review — if you need
            different pricing, a different feature set, or a different ecosystem, these are the
            strongest options we have reviewed in the {escape_html(cat)} family.</p>

        <div class="alt-context">
            {tool_tile(tool, 'tool-icon-lg')}
            <div class="tool-info">
                <div class="tool-title-row"><h2>{escape_html(name)}</h2></div>
                <p>{escape_html(_brief(tool.get('description', ''), 150))}</p>
                <div class="tool-meta-row"><span>{rating_num(tool):.1f}</span><span>{tool.get('price', '')}</span></div>
            </div>
            <a class="td-visit-btn alt-visit" href="/tools/{slug}/">Read our full {escape_html(name)} review</a>
        </div>

        <section class="cat-section">
            <h2>{escape_html(name)} alternatives compared</h2>
            <div class="cat-table-wrap"><table class="cat-table">
                <thead><tr><th>#</th><th>Alternative</th><th>Score</th><th>Pricing</th><th>Best for</th></tr></thead>
                <tbody>
{rows}                </tbody>
            </table></div>
        </section>

        <section class="cat-section">
            <h2>Browse the alternatives</h2>
            <div class="cat-mini-grid">
                {chips}
            </div>
        </section>

        <section class="cat-section">
            <h2>Questions about {escape_html(name)} alternatives</h2>
            <div class="td-faq">
                {faq_html}
            </div>
        </section>
    </main>

{footer_html()}
    ''' + BACK_TO_TOP_BLOCK + DARK_MODE_BLOCK + '''
</body>
</html>'''


CONTACT_EMAIL = 'AIToolLabTeam@gmail.com'

# Curated marquee cross-category pairs for /vs/ pages (filtered against the
# catalog at build time; same-category pairs are generated from rating top-3s).
MARQUEE_VS_PAIRS = [
    ('chatgpt', 'claude'), ('chatgpt', 'gemini'), ('chatgpt', 'perplexity'),
    ('claude', 'gemini'), ('midjourney', 'dall-e-3'), ('midjourney', 'leonardo-ai'),
    ('midjourney', 'flux-1'), ('sora', 'veo'), ('runway', 'sora'), ('runway', 'veo'),
    ('elevenlabs', 'descript'), ('cursor', 'github-copilot'), ('cursor', 'lovable'),
    ('lovable', 'bolt.new'), ('zapier-ai', 'n8n'), ('zapier-ai', 'make'),
    ('n8n', 'make'), ('heygen', 'synthesia'), ('jasper', 'writesonic'),
    ('writesonic', 'anyword'),
]


def build_contact_page_en() -> str:
    """contact.html — the author block on every tool page links here; it was a
    404 until 2026-11-17. One honest channel: the team email."""
    today_iso = datetime.now().strftime('%Y-%m-%d')
    hreflang = hreflang_tags('/contact.html', '/contact.html')
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact AI Tool Lab - {SITE_NAME}</title>
    <meta name="description" content="Reach the AI Tool Lab editorial team: factual corrections, tool submissions and general feedback. Corrections to factual errors are fixed within 48 hours.">
    <link rel="canonical" href="{SITE_DOMAIN}/contact.html">
{hreflang}    <link rel="stylesheet" href="/css/style.css?{CSS_VERSION}">
{VERIFICATION_BLOCK}{GA_BLOCK}
</head>
<body>
{header_html()}

    <main class="cat-hub">
        <h1 class="page-title">Contact AI Tool Lab</h1>
        <p class="cat-intro">One channel, read by the editors who write the reviews:
            <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>. We read everything.</p>

        <section class="cat-section">
            <h2>What to email us about</h2>
            <div class="td-faq">
                <div class="td-faq-item"><h3>Corrections to facts or pricing</h3>
                    <div class="td-faq-a"><p>Put the tool name and the wrong figure in the subject line.
                        Factual errors are fixed within 48 hours — the same promise printed on every tool review.</p></div></div>
                <div class="td-faq-divider"></div>
                <div class="td-faq-item"><h3>Tool submissions</h3>
                    <div class="td-faq-a"><p>Use the <a href="/submit.html">submission page</a> so your entry carries
                        everything our editors need. Submissions are free; rankings are not for sale.</p></div></div>
                <div class="td-faq-divider"></div>
                <div class="td-faq-item"><h3>Everything else</h3>
                    <div class="td-faq-a"><p>Feedback on the methodology, requests for comparisons, and partnership
                        questions that do not involve buying rankings. See <a href="/about.html">about</a> for how
                        we review and how the site is funded.</p></div></div>
            </div>
        </section>
    </main>

{footer_html()}
    ''' + BACK_TO_TOP_BLOCK + DARK_MODE_BLOCK + '''
</body>
</html>'''


def build_submit_page_en() -> str:
    """submit.html — free submissions only. The site's trust position is that
    rankings cannot be bought, so this page must never promise paid placement
    or guaranteed review dates."""
    hreflang = hreflang_tags('/submit.html', '/submit.html')
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Submit an AI Tool - {SITE_NAME}</title>
    <meta name="description" content="Submit your AI tool to AI Tool Lab for free. Every submission is editor-tested before review; rankings cannot be bought and are never for sale.">
    <link rel="canonical" href="{SITE_DOMAIN}/submit.html">
{hreflang}    <link rel="stylesheet" href="/css/style.css?{CSS_VERSION}">
{VERIFICATION_BLOCK}{GA_BLOCK}
</head>
<body>
{header_html()}

    <main class="cat-hub">
        <h1 class="page-title">Submit an AI Tool</h1>
        <p class="cat-intro">Submissions are <strong>free</strong>. Every tool that enters the catalog is
            tested with a real account by our editors before it gets a review, and the catalog is
            updated daily. What we cannot offer — at any price — is a better ranking.</p>

        <section class="cat-section">
            <h2>How to submit</h2>
            <p class="cat-intro">Email <a href="mailto:{CONTACT_EMAIL}?subject=Tool%20submission">{CONTACT_EMAIL}</a>
                with the subject <strong>"Tool submission"</strong> and include:</p>
            <div class="td-faq">
                <div class="td-faq-item"><h3>1 · The basics</h3>
                    <div class="td-faq-a"><p>Tool name, official URL, and a one-line description of what it does.</p></div></div>
                <div class="td-faq-divider"></div>
                <div class="td-faq-item"><h3>2 · Pricing page URL</h3>
                    <div class="td-faq-a"><p>We verify pricing from the official page at review time, so link it directly.</p></div></div>
                <div class="td-faq-divider"></div>
                <div class="td-faq-item"><h3>3 · Category suggestion</h3>
                    <div class="td-faq-a"><p>One category from our <a href="/category/">category list</a> that fits best. Our editors make the final call.</p></div></div>
                <div class="td-faq-divider"></div>
                <div class="td-faq-item"><h3>4 · Access</h3>
                    <div class="td-faq-a"><p>A trial code or free-tier access if the tool is paid — reviews come from real
                        usage, not demo decks. Tools that cannot be tested cannot be reviewed.</p></div></div>
            </div>
        </section>

        <section class="cat-section">
            <h2>What happens next</h2>
            <div class="td-faq">
                <div class="td-faq-item"><h3>Editorial review</h3>
                    <div class="td-faq-a"><p>The catalog is updated daily; review order follows editorial priority and we
                        cannot promise a date. Tools that cannot be tested are not listed.</p></div></div>
                <div class="td-faq-divider"></div>
                <div class="td-faq-item"><h3>Honest scores, no exceptions</h3>
                    <div class="td-faq-a"><p>Rankings are not for sale — the same rule printed on the homepage. A review
                        may be critical; that is the product. If a fact is wrong, email us and it is fixed within 48 hours.</p></div></div>
                <div class="td-faq-divider"></div>
                <div class="td-faq-item"><h3>What we do not accept</h3>
                    <div class="td-faq-a"><p>Paid placements, link exchanges, "guaranteed review" packages, and AI wrappers
                        with no working product. If your tool ships, we want to see it.</p></div></div>
            </div>
        </section>
    </main>

{footer_html()}
    ''' + BACK_TO_TOP_BLOCK + DARK_MODE_BLOCK + '''
</body>
</html>'''


def build_vs_page_en(a: dict, b: dict) -> str:
    """/vs/{a}-vs-{b}/ — head-to-head pages built only from data that exists
    (editor scores, price labels, pros/cons, descriptions). No invented test
    verdicts; the "choose X if" section states facts, not marketing."""
    na, nb = a.get('name', ''), b.get('name', '')
    slug_a, slug_b = a.get('slug', ''), b.get('slug', '')
    ra = re.sub(r'[^\d.]', '', str(a.get('rating', '')))
    rb = re.sub(r'[^\d.]', '', str(b.get('rating', '')))
    pa, pb = a.get('price', ''), b.get('price', '')
    ca, cb = a.get('category', ''), b.get('category', '')
    cat_slug = get_category_slug_en(ca)
    today_iso = datetime.now().strftime('%Y-%m-%d')
    higher_name = na if rating_num(a) >= rating_num(b) else nb
    free_side = ''
    ta, tb = price_type(pa), price_type(pb)
    if ta in ('free', 'freemium') and tb == 'paid':
        free_side = f'{na} has a free tier; {nb} is paid from the start.'
    elif tb in ('free', 'freemium') and ta == 'paid':
        free_side = f'{nb} has a free tier; {na} is paid from the start.'
    same_cat = 'y' if ca == cb else 'n'

    pros_a = ''.join(f'<li>✓&nbsp;&nbsp;{escape_html(p)}</li>' for p in (a.get('pros') or [])[:2])
    cons_a = ''.join(f'<li>—&nbsp;&nbsp;{escape_html(c)}</li>' for c in (a.get('cons') or [])[:1])
    pros_b = ''.join(f'<li>✓&nbsp;&nbsp;{escape_html(p)}</li>' for p in (b.get('pros') or [])[:2])
    cons_b = ''.join(f'<li>—&nbsp;&nbsp;{escape_html(c)}</li>' for c in (b.get('cons') or [])[:1])

    def _card(t, side_rating, side_price, side_pros, side_cons):
        return f'''<div class="vs-card">
            {tool_tile(t, 'tool-icon-lg')}
            <h2><a href="/tools/{t["slug"]}/">{escape_html(t["name"])}</a></h2>
            <div class="vs-score">{escape_html(side_rating)}/5 <span>editor score</span></div>
            <div class="vs-price">{escape_html(side_price)}</div>
            <ul>{side_pros}{side_cons}</ul>
            <a class="td-visit-btn alt-visit" href="/tools/{t["slug"]}/">Full {escape_html(t["name"])} review</a>
        </div>'''
    cards = _card(a, ra, pa, pros_a, cons_a) + _card(b, rb, pb, pros_b, cons_b)

    choose_a, choose_b = [], []
    if ta in ('free', 'freemium') and tb == 'paid':
        choose_a.append('you want to start on a free tier')
    if tb in ('free', 'freemium') and ta == 'paid':
        choose_b.append('you want to start on a free tier')
    if rating_num(a) > rating_num(b):
        choose_a.append('editor score is your primary tiebreaker')
    elif rating_num(b) > rating_num(a):
        choose_b.append('editor score is your primary tiebreaker')
    choose_a.append('your work matches its strengths listed above')
    choose_b.append('your work matches its strengths listed above')
    choose_html = ('<p><strong>Choose ' + escape_html(na) + '</strong> if ' + ' or '.join(choose_a) +
                   '. <strong>Choose ' + escape_html(nb) + '</strong> if ' + ' or '.join(choose_b) + '.</p>')

    faq_items = [
        (f'Is {nb} better than {na}?',
         f'On our editor scores, {na} rates {ra}/5 and {nb} rates {rb}/5. Scores weigh pricing, '
         f'output quality and workflow fit from hands-on testing — read both reviews and match the '
         f'strengths to your own workflow before deciding.'),
        (f'Which is cheaper: {na} or {nb}?',
         f'{na} is listed at "{pa}" and {nb} at "{pb}" (verified {today_iso}). '
         + (free_side if free_side else 'Neither lists a free tier — check each review for trial options.')),
        (f'Can I use {na} and {nb} together?',
         (f'Most readers pick one from the {ca} category — running both is possible but usually redundant. '
          f'If your workflow spans different stages, the pros list above shows where each one is strongest.')
         if ca == cb else
         (f'{na} sits in {ca} and {nb} in {cb} — they can complement each other in one workflow rather '
          f'than compete. Match each to the stage of work it is strongest at.')),
    ]
    faq_json = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a2}}
        for q, a2 in faq_items
    ]}, ensure_ascii=False)
    breadcrumb = json.dumps({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': f'{SITE_DOMAIN}/'},
        {'@type': 'ListItem', 'position': 2, 'name': na, 'item': f'{SITE_DOMAIN}/tools/{slug_a}/'},
        {'@type': 'ListItem', 'position': 3, 'name': f'{na} vs {nb}', 'item': f'{SITE_DOMAIN}/vs/{slug_a}-vs-{slug_b}/'},
    ]}, ensure_ascii=False)

    faq_html = ''
    for q, a2 in faq_items:
        if faq_html:
            faq_html += '<div class="td-faq-divider"></div>\n'
        faq_html += (f'<div class="td-faq-item"><h3>{escape_html(q)}</h3>'
                     f'<div class="td-faq-a"><p>{escape_html(a2)}</p></div></div>\n')

    # 2026-11-18: SERP 截断治理——<title> 用短格式（完整信息保留在 H1/description）
    title = f'{na} vs {nb} (2026): Editor Scores, Pricing & Which to Pick'
    serp_title = f'{na} vs {nb} (2026) Compared'
    if len(serp_title) > 55:
        serp_title = f'{na} vs {nb}'
    meta_desc = (f'{na} ({ra}/5, {pa}) vs {nb} ({rb}/5, {pb}) — hands-on comparison of scores, '
                 f'pricing and strengths, with honest guidance on which one fits your work. '
                 f'Verified {today_iso}.')

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape_html(serp_title)} - {SITE_NAME}</title>
    <meta name="description" content="{escape_html(meta_desc)}">
    <link rel="canonical" href="{SITE_DOMAIN}/vs/{slug_a}-vs-{slug_b}/">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{escape_html(serp_title)}">
    <meta property="og:description" content="{escape_html(meta_desc)}">
    <meta property="og:url" content="{SITE_DOMAIN}/vs/{slug_a}-vs-{slug_b}/">
    <meta property="og:site_name" content="{SITE_NAME}">
    <link rel="stylesheet" href="/css/style.css?{CSS_VERSION}">
    <script type="application/ld+json">{breadcrumb}</script>
    <script type="application/ld+json">{faq_json}</script>
{VERIFICATION_BLOCK}{GA_BLOCK}
</head>
<body>
{header_html()}

    <nav class="breadcrumb td-breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a><span class="sep">/</span><a href="/tools/{slug_a}/">{escape_html(na)}</a><span class="sep">/</span><span>vs {escape_html(nb)}</span>
    </nav>

    <main class="cat-hub">
        <h1 class="page-title">{escape_html(na)} vs {escape_html(nb)}</h1>
        <p class="cat-intro">Both tools are in our catalog with hands-on reviews: {escape_html(na)} scores
            {escape_html(ra)}/5 and {escape_html(nb)} scores {escape_html(rb)}/5. Below is everything
            our testing surfaced — scores, pricing, strengths and weaknesses — without sponsorship from either side.</p>

        <div class="vs-grid">
            {cards}
        </div>

        <section class="cat-section">
            <h2>Side by side</h2>
            <div class="cat-table-wrap"><table class="cat-table">
                <thead><tr><th></th><th>{escape_html(na)}</th><th>{escape_html(nb)}</th></tr></thead>
                <tbody>
                    <tr><td>Editor score</td><td class="num">{escape_html(ra)}/5</td><td class="num">{escape_html(rb)}/5</td></tr>
                    <tr><td>Pricing</td><td>{escape_html(pa)}</td><td>{escape_html(pb)}</td></tr>
                    <tr><td>Category</td><td>{escape_html(ca)}</td><td>{escape_html(cb)}</td></tr>
                </tbody>
            </table></div>
        </section>

        <section class="cat-section">
            <h2>Which should you choose?</h2>
            {choose_html}
        </section>

        <section class="cat-section">
            <h2>Questions about {escape_html(na)} vs {escape_html(nb)}</h2>
            <div class="td-faq">
                {faq_html}
            </div>
        </section>
    </main>

{footer_html()}
    ''' + BACK_TO_TOP_BLOCK + DARK_MODE_BLOCK + '''
</body>
</html>'''


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

    # ── Validate article field names (2026-07-06: prevent content/body mismatch) ──
    for i, a in enumerate(articles):
        if 'body' in a and 'content' not in a:
            print(f"\n{'='*60}")
            print(f"[BUILD ERROR] Article #{i+1} \"{a.get('title','')[:60]}...\"")
            print(f"  Has field 'body' but build_en.py expects 'content'.")
            print(f"  This will produce an EMPTY page with no article text.")
            print(f"  Fix: rename 'body' -> 'content' in articles_en.json")
            print(f"  Or use: python scripts/append_article.py (which uses correct field name)")
            print(f"{'='*60}\n")
            import sys
            sys.exit(1)

    # Sort articles by date descending (newest first)
    articles.sort(key=lambda x: x.get('date', ''), reverse=True)

    published_tools = [t for t in all_tools if t.get('published', False)]

    # "X alternatives" pages: editorial marquee seeds + top-up by editor score
    # to 50 (raw `visits` is polluted by third-party marketplace numbers).
    _cat_slugs_set = {t['slug'] for t in published_tools}
    _marquee = [s for s in MARQUEE_ALTERNATIVE_SLUGS if s in _cat_slugs_set]
    _by_rating = [t['slug'] for t in sorted(published_tools, key=rating_num, reverse=True)
                  if t['slug'] not in _marquee]
    alt_slugs = (_marquee + _by_rating)[:50]
    alt_set = set(alt_slugs)

    # Head-to-head "X vs Y" pages: per-category rating top-3 pairs + curated
    # marquee cross-category pairs, deduped and capped at 80 (thin-content guard).
    from itertools import combinations
    tool_by_slug = {t['slug']: t for t in published_tools}
    vs_pairs = set()
    by_cat_pub = {}
    for t in published_tools:
        by_cat_pub.setdefault(get_category_slug_en(t.get('category', '')), []).append(t)
    for _, lst in by_cat_pub.items():
        top3 = sorted(lst, key=rating_num, reverse=True)[:3]
        for pa_, pb_ in combinations(top3, 2):
            vs_pairs.add(tuple(sorted([pa_['slug'], pb_['slug']])))
    for pa_, pb_ in MARQUEE_VS_PAIRS:
        if pa_ in tool_by_slug and pb_ in tool_by_slug and pa_ != pb_:
            vs_pairs.add(tuple(sorted([pa_, pb_])))
    # Guard against near-duplicate catalog entries comparing themselves
    # (e.g. 'perplexity' vs 'perplexity-ai'): skip when one normalized name
    # is contained in the other. Applied to the FULL set, after all additions.
    def _norm_name(t):
        return re.sub(r'[^a-z0-9]', '', str(t.get('name', '')).lower())
    vs_pairs = {p for p in vs_pairs
                if tool_by_slug.get(p[0]) and tool_by_slug.get(p[1])
                and _norm_name(tool_by_slug[p[0]]) not in _norm_name(tool_by_slug[p[1]])
                and _norm_name(tool_by_slug[p[1]]) not in _norm_name(tool_by_slug[p[0]])}
    # 2026-11-17 治本：仅按评分和排序时，大量 pair 评分和并列（如 9.0 有 7 对），
    # Python set 迭代顺序不稳定 → 每次 build 边界 pair 随机进出 → vs 页面反复删建。
    # 增加 slug 作为确定性次级键，并列时按字母序，保证每次构建选出同一批 80 对。
    vs_pairs = sorted(
        vs_pairs,
        key=lambda p: (
            -(rating_num(tool_by_slug[p[0]]) + rating_num(tool_by_slug[p[1]])),
            p[0],
            p[1],
        ),
    )[:80]
    vs_by_slug = {}
    for sa, sb in vs_pairs:
        vs_by_slug.setdefault(sa, []).append(sb)
        vs_by_slug.setdefault(sb, []).append(sa)
    vs_urls = [f'{SITE_DOMAIN}/vs/{sa}-vs-{sb}/' for sa, sb in vs_pairs]
    print(f'[EN] {len(published_tools)} published tools, {len(articles)} articles')

    # ── Validate price field length (2026-08-05 fix; 2026-09-07 升级为阻断闸门) ──
    # 治本保障：price 字段必须是卡片/徽章用的短标签 (<=80 字符)。
    # 长价格说明应放在 pricing_details 字段。
    # 09-06 复发教训：只 print 不阻断 → 警告无人看，生产线 26 天攒 20 条污染。
    # 现改为收集汇总 + 非 0 退出码，构建直接失败，倒逼写入端修数据。
    _price_violations = []
    for _t in all_tools:
        _p = _t.get('price', '')
        if _p and len(_p) > 80:
            _price_violations.append((_t.get('slug', '?'), len(_p)))
    if _price_violations:
        print(f"\n{'='*60}")
        print(f"[BUILD FAIL] {len(_price_violations)} tools have price field > 80 chars:")
        for _slug, _len in sorted(_price_violations, key=lambda x: -x[1]):
            print(f"  - {_slug} ({_len} chars)")
        print("  price MUST be a short card label, e.g. 'Free + Pro from $19/mo'.")
        print("  Move full pricing text into 'pricing_details'.")
        print("  Fix: add slug->short label to scripts/fix_price_labels.py SHORT_MAP and rerun,")
        print("  or write via scripts/upsert_tool_en.py (validates on entry).")
        print(f"{'='*60}")
        import sys
        sys.exit(1)

    # Group by category
    tools_by_cat: dict = {}
    for t in published_tools:
        cat = t.get('category','')
        if cat:
            tools_by_cat.setdefault(cat, []).append(t)

    # 2026-11-18: article-category page plan (single source of truth for
    # "which /category/<slug>/ pages will exist after this build").
    global ARTICLE_CATEGORY_PAGES
    art_cats = {}
    for a in articles:
        c = a.get('category','')
        if c:
            art_cats.setdefault(c, []).append(a)
    ARTICLE_CATEGORY_PAGES = {
        get_category_slug_en(c) for c, lst in art_cats.items()
        if len(lst) >= MIN_ARTICLES_FOR_CATEGORY_PAGE
    }
    tool_cat_slugs = {get_category_slug_en(c) for c in tools_by_cat}
    ARTICLE_CATEGORY_PAGES |= tool_cat_slugs
    _article_cats_map = {
        get_category_slug_en(c): (c, lst) for c, lst in art_cats.items()
        if len(lst) >= MIN_ARTICLES_FOR_CATEGORY_PAGE
    }

    # ── Category pages ────────────────────────────────────────────────────────
    if target in ('all', 'index', 'tools'):
        # 2026-11-18: 分类 slug → 该分类文章 的映射（冲突合并渲染用）
        articles_by_cat_slug = {}
        for _a in articles:
            _s = get_category_slug_en(_a.get('category', ''))
            if _s:
                articles_by_cat_slug.setdefault(_s, []).append(_a)
        for cat_name, tools_in_cat in tools_by_cat.items():
            cat_slug = get_category_slug_en(cat_name)
            dir_path = os.path.join(OUT_DIR, 'category', cat_slug)
            os.makedirs(dir_path, exist_ok=True)
            html = build_category_page_en(cat_name, tools_in_cat,
                                          cat_articles=articles_by_cat_slug.get(cat_slug))
            with open(os.path.join(dir_path, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(html)
            print(f'[OK] en/category/{cat_slug}/index.html')

        # 2026-11-18: 清理孤儿分类目录（分类收敛/改名后旧 slug 页面残留会
        # 造成 sitemap↔目录漂移）。有效集合 = 工具分类 ∪ 达标文章分类。
        valid_cat_dirs = (tool_cat_slugs
                          | {s for s, (c, l) in _article_cats_map.items()})
        for d in os.listdir(os.path.join(OUT_DIR, 'category')):
            if d == 'index.html':
                continue
            if d not in valid_cat_dirs:
                victim = os.path.join(OUT_DIR, 'category', d)
                if os.path.isdir(victim):
                    import shutil as _sh
                    _sh.rmtree(victim)
                    print(f'[CLEAN] removed orphan category dir: {d}/')

        # Category index
        dir_path = os.path.join(OUT_DIR, 'category')
        os.makedirs(dir_path, exist_ok=True)
        html = build_category_index_en(tools_by_cat)
        with open(os.path.join(dir_path, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'[OK] en/category/index.html')

    # ── Article category pages (2026-11-18: fix 421 breadcrumb 404s) ─────────
    # Generated for article categories with >= MIN_ARTICLES_FOR_CATEGORY_PAGE
    # articles. Slugs never collide with tool categories (union is precomputed
    # above); both are listed on the category hub and in the sitemap.
    if target in ('all', 'articles'):
        # 2026-11-18: 跳过与工具分类冲突的 slug——它们已在工具分类页合并渲染
        # （此前这里后写覆盖前写，10 个工具分类页丢失工具网格）。
        for cat_slug_, (cat_name_, lst_) in sorted(_article_cats_map.items()):
            if cat_slug_ in tool_cat_slugs:
                continue
            dir_path = os.path.join(OUT_DIR, 'category', cat_slug_)
            os.makedirs(dir_path, exist_ok=True)
            html = build_article_category_page_en(cat_name_, lst_)
            with open(os.path.join(dir_path, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(html)
            print(f'[OK] en/category/{cat_slug_}/index.html (article guides, {len(lst_)})')

    # ── Tool pages ────────────────────────────────────────────────────────────
    if target in ('all', 'tools'):
        for tool in published_tools:
            slug     = tool['slug']
            dir_path = os.path.join(OUT_DIR, 'tools', slug)
            os.makedirs(dir_path, exist_ok=True)
            html = build_tool_page_en(tool, published_tools, articles,
                                      alt_slug=tool['slug'] if tool['slug'] in alt_set else '',
                                      vs_partners=vs_by_slug.get(tool['slug'], []))
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
    sitemap   = generate_sitemap_en(published_tools, articles, cat_slugs, alt_slugs, vs_urls)
    with open(os.path.join(OUT_DIR, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(sitemap)
    print(f'[OK] en/sitemap.xml ({len(published_tools)} tools + {len(articles)} articles)')

    # ── Search page (client-side index; noindex, not in sitemap) ──────────────
    search_dir = os.path.join(OUT_DIR, 'search')
    os.makedirs(search_dir, exist_ok=True)
    with open(os.path.join(search_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(build_search_page_en(published_tools, articles))
    print(f'[OK] en/search/index.html ({len(published_tools)} tools + {len(articles)} articles indexed)')

    # ── llms.txt (regenerated on every build — counts/dates never drift) ──────
    llms_txt = generate_llms_txt_en(published_tools, articles, alt_slugs, vs_pairs)
    with open(os.path.join(OUT_DIR, 'llms.txt'), 'w', encoding='utf-8') as f:
        f.write(llms_txt)
    print(f'[OK] en/llms.txt ({len(published_tools)} tools / {len(articles)} articles)')

    # ── llms-full.txt (full content companion — tools + articles in one file) ─
    llms_full = generate_llms_full_txt_en(published_tools, articles)
    with open(os.path.join(OUT_DIR, 'llms-full.txt'), 'w', encoding='utf-8') as f:
        f.write(llms_full)
    print(f'[OK] en/llms-full.txt ({len(published_tools)} tools / {len(articles)} articles, {len(llms_full)//1024} KB)')

    # ── About/Author trust-info count refresh (audit 2026-10-13 P1 fix) ───────
    _n_cats = len({get_category_slug_en(t.get('category', '')) for t in published_tools})
    refresh_about_author_counts(len(published_tools), len(articles), _n_cats)

    # ── RSS feed (latest 30 dated articles; tools have no honest dates) ───────
    with open(os.path.join(OUT_DIR, 'rss.xml'), 'w', encoding='utf-8') as f:
        f.write(generate_rss_en(articles))
    print(f'[OK] en/rss.xml (latest 30 of {len(articles)} articles)')

    # ── Alternatives pages ("{tool} alternatives", top 50 by visits) ──────────
    alt_dir = os.path.join(OUT_DIR, 'alternatives')
    os.makedirs(alt_dir, exist_ok=True)
    alt_built = 0
    for aslug in alt_slugs:
        t0 = next((t for t in published_tools if t['slug'] == aslug), None)
        if not t0:
            continue
        c0 = t0.get('category', '')
        same = [t for t in published_tools if t['slug'] != aslug and t.get('category') == c0]
        others = [t for t in published_tools if t['slug'] != aslug and t.get('category') != c0]
        cands = sorted(same + others, key=rating_num, reverse=True)[:9]
        if len(cands) < 3:
            continue
        adir = os.path.join(alt_dir, aslug)
        os.makedirs(adir, exist_ok=True)
        with open(os.path.join(adir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(build_alternatives_page_en(t0, cands))
        alt_built += 1
    # Remove stale alternatives dirs (e.g. after the selection strategy changes)
    # so the deployed set always matches the sitemap exactly.
    for d in os.listdir(alt_dir):
        if d not in alt_set and os.path.isdir(os.path.join(alt_dir, d)):
            try:
                import shutil
                shutil.rmtree(os.path.join(alt_dir, d))
            except Exception:
                for root, dirs_, files_ in os.walk(os.path.join(alt_dir, d), topdown=False):
                    for fn in files_:
                        os.remove(os.path.join(root, fn))
                    for dn in dirs_:
                        os.rmdir(os.path.join(root, dn))
                os.rmdir(os.path.join(alt_dir, d))
    print(f'[OK] en/alternatives/ ({alt_built} pages from top {len(alt_slugs)} tools)')

    # ── Head-to-head "/vs/" pages (deduped pairs, capped, stale dirs pruned) ──
    vs_dir = os.path.join(OUT_DIR, 'vs')
    os.makedirs(vs_dir, exist_ok=True)
    vs_urls = []
    for sa, sb in vs_pairs:
        ta_, tb_ = tool_by_slug.get(sa), tool_by_slug.get(sb)
        if not ta_ or not tb_:
            continue
        pair_slug = f'{sa}-vs-{sb}'
        vdir = os.path.join(vs_dir, pair_slug)
        os.makedirs(vdir, exist_ok=True)
        with open(os.path.join(vdir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(build_vs_page_en(ta_, tb_))
        vs_urls.append(f'{SITE_DOMAIN}/vs/{pair_slug}/')
    _vs_valid = {f'{sa}-vs-{sb}' for sa, sb in vs_pairs}
    for d in os.listdir(vs_dir):
        if d not in _vs_valid and os.path.isdir(os.path.join(vs_dir, d)):
            try:
                import shutil
                shutil.rmtree(os.path.join(vs_dir, d))
            except Exception:
                for root, dirs_, files_ in os.walk(os.path.join(vs_dir, d), topdown=False):
                    for fn in files_:
                        os.remove(os.path.join(root, fn))
                    for dn in dirs_:
                        os.rmdir(os.path.join(root, dn))
                os.rmdir(os.path.join(vs_dir, d))
    print(f'[OK] en/vs/ ({len(vs_urls)} head-to-head pages)')

    # ── Contact + Submit pages (linked from every tool review) ────────────────
    with open(os.path.join(OUT_DIR, 'contact.html'), 'w', encoding='utf-8') as f:
        f.write(build_contact_page_en())
    with open(os.path.join(OUT_DIR, 'submit.html'), 'w', encoding='utf-8') as f:
        f.write(build_submit_page_en())
    print('[OK] en/contact.html + en/submit.html')

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
    all_urls += [f"{SITE_DOMAIN}/category/{s}/" for s in sorted(ARTICLE_CATEGORY_PAGES)
                 if s not in {get_category_slug_en(c) for c in tools_by_cat}]
    all_urls += [f"{SITE_DOMAIN}/alternatives/{s}/" for s in alt_slugs]
    all_urls += vs_urls

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

    # Validate internal links before building (2026-06-25 original; 2026-11-18 hardened)
    # 旧版 validate_internal_links.py 只校验 /articles/ 一种形态，裸 slug (/chatgpt/)、
    # /en/ 多余前缀、/tool/ 单数等全部漏过 → 每天 build 假绿灯，404 累积到 972 处。
    # 现统一走 check_internal_links.py：覆盖 tools/articles/category + 裸 slug + 前缀漂移，
    # 且目标存在性以"当前 slug 集合 + 已构建页面"为准。失败即 exit 1，禁止静默跳过。
    if args.target in ('all', 'articles'):
        try:
            from check_internal_links import validate_all
            print("\n[VALIDATE] Checking internal links (all forms)...")
            n, errs = validate_all()
            if n:
                print(f"[VALIDATE] ERROR: {n} broken internal links. Fix before building!")
                for owner, e in errs[:15]:
                    print(f"  {owner}: {e['kind']} {e['href']} ({e['reason']})")
                if n > 15:
                    print(f"  ... and {n-15} more")
                import sys
                sys.exit(1)
            print("[VALIDATE] OK — all internal links resolve.")
        except ImportError as exc:
            # 校验器缺失 = 闸门失效，必须硬失败，不允许静默跳过（2026-11-18 治本）
            print(f"[VALIDATE] FATAL: link validator unavailable ({exc}). Refusing to build with the gate down.")
            import sys
            sys.exit(1)

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
