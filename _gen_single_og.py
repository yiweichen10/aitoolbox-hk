#!/usr/bin/env python3
"""Generate OG image for a single article, bypassing sandbox permission issues."""
import json
import os
import sys

# Add scripts dir to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OG_DIR   = BASE_DIR / "images" / "og"

# Import drawing functions from the existing script
sys.path.insert(0, str(BASE_DIR / "scripts"))
import gen_og_images_en as og

# Load articles
articles = json.loads((DATA_DIR / "articles_en.json").read_text(encoding="utf-8"))

for a in articles:
    if a['slug'] == 'best-ai-website-builders-2026':
        out_path = OG_DIR / f"{a['slug']}-en-og.png"
        print(f"Generating: {out_path}")
        try:
            og.make_article_og(a, out_path)
            print(f"OK: {out_path}")
            print(f"File size: {out_path.stat().st_size} bytes")
        except Exception as e:
            print(f"FAIL: {e}")
            import traceback
            traceback.print_exc()
        break
