#!/usr/bin/env python3
"""
gen_og_images_en.py — Generate OG images for aitoolbox.hk (English site)

Outputs 1200x630 PNG for every tool page and article page.
Uses Pillow only — no external API, no network calls, no emoji dependency.

Usage:
  python scripts/gen_og_images_en.py            # skip existing
  python scripts/gen_og_images_en.py --force    # regenerate all
"""

import argparse
import json
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent.parent
DATA_DIR   = BASE_DIR / "data"
OG_DIR     = BASE_DIR / "images" / "og"

# ─── Canvas ───────────────────────────────────────────────────────────────────
W, H = 1200, 630

# ─── Palette ──────────────────────────────────────────────────────────────────
C_BG       = (13,  18,  35)   # deep navy
C_CARD     = (22,  32,  56)   # card surface
C_ACCENT   = (59, 130, 246)   # #3b82f6 blue
C_ACCENT2  = (139, 92, 246)   # #8b5cf6 purple
C_BORDER   = (40,  55,  90)   # subtle border
C_WHITE    = (248, 250, 252)
C_SUB      = (148, 163, 184)
C_MUTED    = (71,  85, 105)
C_TAG_BG   = (30,  42,  72)

# ─── Category → colour map ───────────────────────────────────────────────────
CAT_COLOR = {
    "ai chat":       (59, 130, 246),
    "ai image":      (168, 85, 247),
    "ai video":      (239, 68, 68),
    "ai coding":     (16, 185, 129),
    "ai audio":      (245, 158, 11),
    "ai writing":    (99, 102, 241),
    "ai office":     (20, 184, 166),
    "ai search":     (236, 72, 153),
    "ai research":   (139, 92, 246),
    "ai tools":      (59, 130, 246),
}

def _cat_color(category):
    return CAT_COLOR.get(category.lower(), C_ACCENT)

# ─── Fonts ────────────────────────────────────────────────────────────────────
def _font(size, bold=False):
    candidates = (
        ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/calibrib.ttf"]
        if bold else
        ["C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/calibri.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    )
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

# ─── Text helpers ─────────────────────────────────────────────────────────────
def _wrap(text, font, max_w, draw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textbbox((0,0), test, font=font)[2] > max_w and cur:
            lines.append(cur)
            cur = w
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines

def _tw(text, font, draw):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0], bb[3] - bb[1]

# ─── Drawing primitives ───────────────────────────────────────────────────────
def _gradient_bg(img):
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        r = int(C_BG[0] + (C_CARD[0] - C_BG[0]) * t)
        g = int(C_BG[1] + (C_CARD[1] - C_BG[1]) * t)
        b = int(C_BG[2] + (C_CARD[2] - C_BG[2]) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

def _left_bar(draw, color):
    """Left accent bar — thin 4px line, single color, subtle."""
    bar_w = 4
    bar_color = (color[0], color[1], color[2])
    draw.rectangle([(0, 0), (bar_w - 1, H)], fill=bar_color)

def _glow_circle(img, cx, cy, radius, color, alpha=18):
    """Soft glow circle as decorative element."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for r in range(radius, 0, -radius // 6):
        a = int(alpha * (1 - r / radius))
        d.ellipse([(cx - r, cy - r), (cx + r, cy + r)],
                  fill=(color[0], color[1], color[2], a))
    base = img.convert("RGBA")
    combined = Image.alpha_composite(base, overlay)
    img.paste(combined.convert("RGB"))

def _category_badge(draw, text, x, y, color, font):
    """Coloured category pill. Returns (right_x, bottom_y)."""
    tw, th = _tw(text, font, draw)
    px, py = 16, 7
    rx1, ry1 = x, y
    rx2, ry2 = x + tw + px * 2, y + th + py * 2
    # filled coloured pill
    draw.rounded_rectangle([(rx1, ry1), (rx2, ry2)], radius=6,
                            fill=(*color, 255), outline=None)
    draw.text((rx1 + px, ry1 + py), text, font=font, fill=C_WHITE)
    return rx2, ry2

def _info_pill(draw, text, x, y, font):
    """Semi-transparent info pill. Returns right_x."""
    tw, th = _tw(text, font, draw)
    px, py = 14, 6
    x2, y2 = x + tw + px * 2, y + th + py * 2
    draw.rounded_rectangle([(x, y), (x2, y2)], radius=6,
                            fill=C_TAG_BG, outline=C_BORDER, width=1)
    draw.text((x + px, y + py), text, font=font, fill=C_SUB)
    return x2

def _feature_tags(draw, features, y, font, color):
    """Row of feature tags near the bottom."""
    x = 72
    for feat in features:
        tw, th = _tw(feat, font, draw)
        px, py = 14, 7
        x2 = x + tw + px * 2
        if x2 > W - 60:
            break
        draw.rounded_rectangle([(x, y), (x2, y + th + py * 2)],
                                radius=5, fill=C_TAG_BG, outline=C_BORDER, width=1)
        # small colour dot
        dot_x = x + px
        dot_y = y + py + th // 2
        draw.ellipse([(dot_x, dot_y - 3), (dot_x + 6, dot_y + 3)], fill=color)
        draw.text((x + px + 12, y + py), feat, font=font, fill=C_SUB)
        x = x2 + 10

def _divider(draw, y, color):
    """Thin horizontal divider line."""
    draw.rectangle([(72, y), (72 + 48, y + 2)], fill=color)

# ─── Tool OG Image ────────────────────────────────────────────────────────────
def make_tool_og(tool, out_path):
    import re as _re

    img = Image.new("RGB", (W, H))
    _gradient_bg(img)

    category = tool.get("category", "AI Tools")
    color    = _cat_color(category)

    _glow_circle(img, W - 160, 120, 280, color, alpha=22)
    _glow_circle(img, 80, H - 80, 200, C_ACCENT2, alpha=14)

    draw = ImageDraw.Draw(img)
    _left_bar(draw, color)

    f_badge = _font(13, bold=True)
    f_title = _font(54, bold=True)
    f_sub   = _font(19)
    f_meta  = _font(14)
    f_tag   = _font(13)
    f_label = _font(12)

    PAD      = 72
    BRAND_H  = 38
    USABLE_H = H - BRAND_H        # 592px
    RIGHT_W  = 200
    LEFT_MAX = W - PAD - RIGHT_W - 24

    name     = tool.get("name", "Unknown Tool")
    desc     = tool.get("description") or ""
    pros     = tool.get("pros", [])[:3]
    features = tool.get("features", [])[:6]
    price    = (tool.get("price") or "Free").split("+")[0].strip()
    platform = tool.get("platform", "")
    # Best-for tags: text-only tags from the tags field (skip type=free/paid/hot badges)
    _SKIP_WORDS = {"free", "paid", "free tier", "hot", "new", "trending"}
    raw_tags  = tool.get("tags", [])
    best_tags = [t["text"] for t in raw_tags
                 if isinstance(t, dict) and not t.get("type")
                 and t.get("text","").lower() not in _SKIP_WORDS][:4]
    visits = tool.get("visits", "")

    name_lines = _wrap(name, f_title, LEFT_MAX, draw)[:2]
    desc_lines = _wrap(desc, f_sub,   LEFT_MAX, draw)[:2]

    # Tagline and brand strip both fixed at bottom
    TAGLINE_RULE_Y = H - BRAND_H - 54
    TAGLINE_Y      = TAGLINE_RULE_Y + 12
    # Body starts at fixed top margin — clean, predictable, Twitter-card style
    y = 44

    # ── Right panel: SCORE block, top-aligned with content ──
    rating_raw   = tool.get("rating", "")
    rating_clean = _re.sub(r'[^\x00-\x7F]', '', rating_raw).strip()
    if rating_clean:
        f_big_num   = _font(78, bold=True)
        f_big_sub   = _font(13)
        f_big_label = _font(11)
        num_tw, _   = _tw(rating_clean, f_big_num, draw)
        num_x  = W - num_tw - 60
        num_y  = y + 6
        cx     = num_x + num_tw // 2
        bb     = draw.textbbox((num_x, num_y), rating_clean, font=f_big_num)
        num_bottom = bb[3]
        draw.text((cx - 22, num_y - 17), "SCORE", font=f_big_label, fill=C_MUTED)
        draw.text((num_x, num_y), rating_clean, font=f_big_num, fill=(*color, 230))
        slash_tw, _ = _tw("/ 10", f_big_sub, draw)
        draw.text((cx - slash_tw // 2, num_bottom + 4), "/ 10", font=f_big_sub, fill=C_MUTED)

    # ── Badge ──
    _, badge_b = _category_badge(draw, category.upper(), PAD, y, color, f_badge)
    y = badge_b + 22

    # ── Tool name ──
    for line in name_lines:
        draw.text((PAD, y), line, font=f_title, fill=C_WHITE)
        y += 62
    y += 4

    # ── Description ──
    for line in desc_lines:
        draw.text((PAD, y), line, font=f_sub, fill=C_SUB)
        y += 26
    y += 14

    # ── Divider ──
    _divider(draw, y, color)
    y += 16

    # ── Info row: PRICING / PLATFORM ──
    x = PAD
    for label, val in [("PRICING", price), ("PLATFORM", platform)]:
        if not val:
            continue
        draw.text((x, y),      label, font=f_label, fill=C_MUTED)
        draw.text((x, y + 17), val,   font=f_meta,  fill=C_WHITE)
        x += 240
    y += 50

    # ── Pros ──
    for pro in pros:
        dot_x, dot_y = PAD + 3, y + 5
        draw.ellipse([(dot_x, dot_y), (dot_x + 7, dot_y + 7)], fill=color)
        draw.text((PAD + 18, y), pro[:60], font=f_meta, fill=C_SUB)
        y += 26
    if pros:
        y += 20

    # ── Feature tags ──
    if features:
        _feature_tags(draw, features, y, f_tag, color)
        y += 52

    # ── Best For row ──
    if best_tags:
        draw.text((PAD, y), "BEST FOR", font=f_label, fill=C_MUTED)
        y += 18
        bx = PAD
        for bt in best_tags:
            btw, bth = _tw(bt, f_tag, draw)
            px = 10
            bx2 = bx + btw + px * 2
            if bx2 > W - 200:
                break
            draw.rounded_rectangle([(bx, y), (bx2, y + bth + 10)],
                                    radius=4, fill=C_TAG_BG, outline=C_BORDER)
            draw.text((bx + px, y + 5), bt, font=f_tag, fill=C_WHITE)
            bx = bx2 + 8
        y += 40

    # ── Monthly visits stat (fills remaining space above tagline) ──
    if visits:
        y += 8
        draw.text((PAD, y), "MONTHLY VISITS", font=f_label, fill=C_MUTED)
        draw.text((PAD + 130, y), visits, font=f_label, fill=color)
    # ── Tagline — pinned above brand strip ──
    f_tagline = _font(13)
    draw.rectangle([(PAD, TAGLINE_RULE_Y), (W - PAD, TAGLINE_RULE_Y + 1)], fill=C_BORDER)
    draw.text((PAD, TAGLINE_Y),
              "Reviewed on aitoolbox.hk — your independent AI tool guide",
              font=f_tagline, fill=C_MUTED)

    # ── Subtle decorative watermark (very faint, right side) ──
    f_wm = _font(72, bold=True)
    cat_short = category.split()[0].upper()
    wm_tw, wm_th = _tw(cat_short, f_wm, draw)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.text((W - wm_tw - 52, H - BRAND_H - wm_th - 56), cat_short,
            font=f_wm, fill=(*color, 8))
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"))
    draw = ImageDraw.Draw(img)

    # ── Horizontal rule above brand strip ──
    draw.rectangle([(0, H - BRAND_H - 1), (W, H - BRAND_H)], fill=C_BORDER)

    # ── Bottom brand strip ──
    draw.rectangle([(0, H - BRAND_H), (W, H)], fill=(10, 14, 28))
    draw.text((PAD, H - 26), "aitoolbox.hk — AI Tool Reviews & Comparisons",
              font=f_label, fill=C_MUTED)
    draw.text((W - 160, H - 26), "AI Tool Lab", font=f_label, fill=color)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(out_path), "PNG", optimize=True)


# ─── Article OG Image ─────────────────────────────────────────────────────────
def make_article_og(article, out_path):
    import re as _re

    img = Image.new("RGB", (W, H))
    _gradient_bg(img)

    category = article.get("category", "AI Tools")
    color    = _cat_color(category)

    _glow_circle(img, W - 100, 80, 320, color, alpha=18)
    _glow_circle(img, 60, H - 60, 180, C_ACCENT2, alpha=12)

    draw = ImageDraw.Draw(img)
    _left_bar(draw, color)

    f_badge = _font(13, bold=True)
    f_main  = _font(48, bold=True)
    f_sub   = _font(21)
    f_desc  = _font(16)
    f_meta  = _font(14)
    f_label = _font(12)

    PAD     = 72
    BRAND_H = 38

    title = article.get("title", "")
    if ":" in title:
        main_t, sub_t = title.split(":", 1)
        main_t, sub_t = main_t.strip(), sub_t.strip()
    else:
        main_t, sub_t = title, ""

    main_lines = _wrap(main_t, f_main, W - PAD - 100, draw)[:2]
    sub_lines  = _wrap(sub_t,  f_sub,  W - PAD - 100, draw)[:1] if sub_t else []
    desc       = (article.get("description") or "")[:170]
    desc_lines = _wrap(desc, f_desc, W - PAD - 90, draw)[:3] if desc else []

    # ── Tags: prefer keywords field, fallback to meaningful title nouns ──
    tags = article.get("keywords", article.get("tags", []))
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    if not tags:
        stop = {"the","a","an","and","or","for","in","of","to","with","how",
                "what","best","top","vs","is","are","your","you","2026","2025",
                "free","no","new","get","use","make","all","that","this","its"}
        words = _re.findall(r'[A-Za-z][A-Za-z0-9+\-]*', title)
        tags  = [w for w in words if w.lower() not in stop and len(w) >= 4][:6]
    tags = tags[:6]

    # ── Stats row pinned above brand strip ──
    # ── Pin stats just above brand strip; derive y_start by measuring body upward ──

    _GAP = 22   # gap between last content element and stats rule

    # ── Dry-run: measure full block height (badge → stats value row) ──
    _dummy2 = Image.new("RGB", (W, H))
    _dd2    = ImageDraw.Draw(_dummy2)
    _ay     = 0
    _, _abb = _category_badge(_dd2, category.upper(), PAD, _ay, color, f_badge)
    _ay     = _abb + 20
    _ay    += len(main_lines) * 56 + 6
    _ay    += len(sub_lines) * 30 + (8 if sub_lines else 0)
    _ay    += 18   # divider
    _ay    += len(desc_lines) * 22 + (16 if desc_lines else 0)
    _ay    += 36   # tags row (or blank gap)
    _ay    += _GAP + 1 + 10 + 36   # rule + padding + stats label + value rows
    art_total_h = _ay

    # Centre full block in usable area; min 40px top
    USABLE_ART = H - BRAND_H
    y = max(40, (USABLE_ART - art_total_h) // 2)
    _, badge_b = _category_badge(draw, category.upper(), PAD, y, color, f_badge)
    y = badge_b + 20

    for line in main_lines:
        draw.text((PAD, y), line, font=f_main, fill=C_WHITE)
        y += 56
    y += 6

    if sub_lines:
        for line in sub_lines:
            draw.text((PAD, y), line, font=f_sub, fill=C_SUB)
            y += 30
        y += 8

    _divider(draw, y, color)
    y += 18

    if desc_lines:
        block_h = len(desc_lines) * 22
        draw.rectangle([(PAD, y), (PAD + 3, y + block_h + 4)], fill=color)
        for line in desc_lines:
            draw.text((PAD + 16, y), line, font=f_desc, fill=C_SUB)
            y += 22
        y += 16

    # ── Tags ──
    # ── Tags ──
    if tags:
        x = PAD
        for tag in tags:
            tw, th = _tw(tag, f_label, draw)
            px = 12
            x2 = x + tw + px * 2
            if x2 > W - 60:
                break
            draw.rounded_rectangle([(x, y), (x2, y + th + 14)],
                                    radius=4, fill=C_TAG_BG, outline=C_BORDER)
            draw.text((x + px, y + 7), tag, font=f_label, fill=C_SUB)
            x = x2 + 10
    y += 36   # advance y regardless of tags

    # ── Stats row: flows _GAP px after last content element ──
    rule_y   = y + _GAP
    stats_y  = rule_y + 10
    draw.rectangle([(PAD, rule_y), (PAD + 500, rule_y + 1)], fill=C_BORDER)
    date_str = article.get("dateFull", article.get("date", ""))
    sx = PAD
    for slabel, sval in [("UPDATED", date_str), ("READ TIME", "8 min read"), ("BY", "AI Tool Lab")]:
        if not sval:
            continue
        draw.text((sx, stats_y),      slabel, font=f_label, fill=C_MUTED)
        draw.text((sx, stats_y + 18), sval,   font=f_meta,  fill=C_WHITE)
        sx += 220

    # ── Separator + brand strip ──
    draw.rectangle([(0, H - BRAND_H - 1), (W, H - BRAND_H)], fill=C_BORDER)
    draw.rectangle([(0, H - BRAND_H), (W, H)], fill=(10, 14, 28))
    draw.text((PAD, H - 26), "aitoolbox.hk — AI Tool Reviews & Comparisons",
              font=f_label, fill=C_MUTED)
    draw.text((W - 160, H - 26), "AI Tool Lab", font=f_label, fill=color)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(out_path), "PNG", optimize=True)


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Regenerate all")
    args = parser.parse_args()

    tools    = json.loads((DATA_DIR / "tools_en.json").read_text(encoding="utf-8"))
    articles = json.loads((DATA_DIR / "articles_en.json").read_text(encoding="utf-8"))
    published = [t for t in tools if t.get("published", False)]

    print(f"[OG] {len(published)} tools, {len(articles)} articles")
    ok = skipped = fail = 0

    for tool in published:
        slug = tool["slug"]
        out  = OG_DIR / f"{slug}-en-og.png"
        if out.exists() and not args.force:
            skipped += 1
            continue
        print(f"  [GEN] {slug}-en-og.png ...", end="", flush=True)
        try:
            make_tool_og(tool, out)
            print(" OK")
            ok += 1
        except Exception as e:
            print(f" FAIL ({e})")
            fail += 1

    for article in articles:
        slug = article["slug"]
        out  = OG_DIR / f"{slug}-en-og.png"
        if out.exists() and not args.force:
            skipped += 1
            continue
        print(f"  [GEN] {slug}-en-og.png ...", end="", flush=True)
        try:
            make_article_og(article, out)
            print(" OK")
            ok += 1
        except Exception as e:
            print(f" FAIL ({e})")
            fail += 1

    print(f"\n[OG] Done — {ok} generated, {skipped} skipped, {fail} failed")

if __name__ == "__main__":
    main()
