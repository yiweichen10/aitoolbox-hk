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

    # Step 2: git commit & push（仅作版本备份，失败不中断后续部署）
    log("STEP 2: git commit & push (backup to GitHub)")
    subprocess.run(["git", "add", "-A"], cwd=BASE_DIR)
    staged = subprocess.run(
        ["git", "diff", "--cached", "--quiet"], cwd=BASE_DIR
    ).returncode
    if staged == 0:
        log("  no changes to commit, skip")
    else:
        msg = "Daily build " + datetime.now().strftime("%Y-%m-%d %H:%M")
        c = subprocess.run(["git", "commit", "-m", msg], cwd=BASE_DIR,
                           text=True, encoding="utf-8", errors="replace")
        if c.returncode != 0:
            log("  WARN: git commit failed, continue anyway")
        else:
            p = subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR,
                               text=True, encoding="utf-8", errors="replace")
            log("  git push exit " + str(p.returncode) + " (backup only, non-blocking)")

    # Step 3: 部署到 Cloudflare Pages（真正上线这一步）
    log("STEP 3: Deploy to Cloudflare Pages")
    run([sys.executable, os.path.join(SCRIPTS_DIR, 'deploy_cf.py'), "--upload"])

    log("=" * 55)
    log("Pipeline complete: built, pushed, deployed.")
    log("Live: https://www.aitoolbox.hk/")
    log("=" * 55)

if __name__ == "__main__":
    main()
