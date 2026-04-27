#!/usr/bin/env python3
"""
daily_growth_en.py — aitoolbox.hk content pipeline orchestrator

Steps:
  1. build_en.py     — regenerate all static HTML (tools + articles + sitemap)

Later steps (not yet wired in):
  [manual]           — new articles written by Accio agent, saved to articles_en.json
  [future]           — git commit & push once deployment is confirmed

Usage:
  python scripts/daily_growth_en.py
"""

import os
import sys
import subprocess
from datetime import datetime

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, 'scripts')

# ─── Helper ───────────────────────────────────────────────────────────────────
def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def run(cmd, cwd=None):
    cwd = cwd or BASE_DIR
    log(f"RUN: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, text=True, encoding='utf-8', errors='replace')
    if result.returncode != 0:
        log(f"FAILED (exit {result.returncode}) — aborting.")
        sys.exit(1)

# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    log("=" * 55)
    log("aitoolbox.hk — Daily Build Pipeline")
    log("=" * 55)

    # Step 1: Build static site
    log("STEP 1: Rebuild static site")
    run([sys.executable, os.path.join(SCRIPTS_DIR, 'build_en.py')])

    log("=" * 55)
    log("Pipeline complete. Static files updated under /en/")
    log("Next step: git add . && git commit && git push (manual for now)")
    log("=" * 55)

if __name__ == "__main__":
    main()
