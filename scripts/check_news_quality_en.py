#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_news_quality_en.py — 英文站 AI 快讯质量门禁（硬阻断）

对标中文站 scripts/check_news_quality.py，但口径改为英文：
- FAIL（硬伤）：空标题 / 空摘要 / 中文标题 / 分类缺失或非法 / 缺 source 或 source_url /
  缺 commentary（当期必填）/ 发布日期超窗 / 同批 id 重复。
- WARN（提示，不阻断）：摘要 >70 词或 <12 词、标题尾部标点、空话词、
  评注 <30 词或复述摘要、标题含 HTML 实体残留。

用法：
  python scripts/check_news_quality_en.py --today            # 只查当日候选（含明细）
  python scripts/check_news_quality_en.py --today --fail     # 有硬伤 exit 1（流水线门禁）
  python scripts/check_news_quality_en.py --all --fail       # 查 data/news_en.json 全量
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
STORE_PATH = os.path.join(DATA_DIR, "news_en.json")
CST = timezone(timedelta(hours=8))
MAX_AGE_DAYS = 3
VALID_CATEGORIES = ("models", "products", "industry", "research")
MAX_SUMMARY_WORDS = 70
MAX_COMMENTARY_WORDS = 100

CJK_RE = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf]")
ENTITY_RE = re.compile(r"&(?:[a-zA-Z]+|#\d+|#x[0-9a-fA-F]+);")
TRAIL_PUNCT = "。！？!?.;；,，:："
CLICHE_WORDS = ("worth watching", "stay tuned", "keep an eye on", "in today's fast-paced",
                "game-changer", "revolutionize", "exciting times", "it's worth noting")


def _daily_path(day):
    return os.path.join(DATA_DIR, f"news_{day}_en.json")


def _word_count(s):
    return len((s or "").split())


def check_item(it, require_commentary=True):
    fails, warns = [], []
    title = (it.get("title") or "").strip()
    summary = (it.get("summary") or "").strip()
    comm = (it.get("commentary") or "").strip()

    if not title:
        fails.append("空标题")
    if not summary:
        fails.append("空摘要")
    cat = it.get("category")
    if cat not in VALID_CATEGORIES:
        fails.append(f"分类缺失或非法(category={cat!r}，应为 {'|'.join(VALID_CATEGORIES)})")
    if not (it.get("source") or "").strip():
        fails.append("缺 source(来源名)")
    url = (it.get("source_url") or "").strip()
    if not url:
        fails.append("缺 source_url(原文链接)")
    elif not url.startswith(("http://", "https://")):
        fails.append(f"source_url 非 http(s)：{url[:70]!r}")

    if title:
        if CJK_RE.search(title):
            fails.append("中文标题（英文站标题必须全英文）")
        if ENTITY_RE.search(title):
            warns.append("标题有 HTML 实体残留（如 &#8217;）")
        if title[-1] in TRAIL_PUNCT:
            warns.append(f"标题尾部标点「{title[-1]}」")
        if len(title) > 110:
            warns.append(f"标题过长({len(title)} 字符)")

    if summary:
        if CJK_RE.search(summary):
            fails.append("中文摘要（英文站摘要必须全英文）")
        wc = _word_count(summary)
        if wc > MAX_SUMMARY_WORDS:
            fails.append(f"摘要词数 {wc} > {MAX_SUMMARY_WORDS}（门禁硬线，需浓缩）")
        if wc < 12:
            warns.append(f"摘要过短({wc} 词，疑似无信息)")
        hit = [w for w in CLICHE_WORDS if w.lower() in summary.lower()]
        if hit:
            warns.append(f"摘要空话词({'/'.join(hit)})")
        if ENTITY_RE.search(summary):
            warns.append("摘要有 HTML 实体残留")

    if not comm:
        if require_commentary:
            fails.append("缺 commentary(评注，当期必填)")
    else:
        wc = _word_count(comm)
        if wc > MAX_COMMENTARY_WORDS:
            fails.append(f"评注词数 {wc} > {MAX_COMMENTARY_WORDS}")
        if wc < 25:
            warns.append(f"评注过短({wc} 词，疑似敷衍)")
        hit = [w for w in CLICHE_WORDS if w.lower() in comm.lower()]
        if hit:
            warns.append(f"评注空话词({'/'.join(hit)})")
        if summary and comm:
            s_head, c_head = summary[:30].lower(), comm[:30].lower()
            if s_head and (s_head in comm.lower() or c_head in summary.lower()):
                warns.append("评注复述摘要开头（无信息增量）")

    # 时效：候选文件里的 published_at 必须是可解析的近期时间
    pa = it.get("published_at")
    if pa:
        try:
            dt = datetime.fromisoformat(str(pa).replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            age = datetime.now(timezone.utc) - dt.astimezone(timezone.utc)
            if age > timedelta(days=MAX_AGE_DAYS):
                fails.append(f"发布日期超窗({age.days} 天前 > {MAX_AGE_DAYS} 天)")
        except Exception:
            fails.append(f"published_at 无法解析：{pa!r}")

    return fails, warns


def load_items(today_only, day=None):
    if today_only:
        day = day or datetime.now(CST).strftime("%Y-%m-%d")
        path = _daily_path(day)
        if not os.path.exists(path):
            raise RuntimeError(f"当日候选文件不存在：{path}（先跑 fetch_intl_news_en.py）")
        items = json.load(open(path, encoding="utf-8"))
        if not isinstance(items, list) or not items:
            raise RuntimeError(f"当日候选为空：{path}（本期不可发布）")
        return f"{os.path.basename(path)} (today)", items
    if not os.path.exists(STORE_PATH):
        raise RuntimeError(f"缺少 {STORE_PATH}")
    return "news_en.json (all)", json.load(open(STORE_PATH, encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--today", action="store_true")
    ap.add_argument("--date", help="YYYY-MM-DD，配合 --today 使用；默认今天")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--fail", action="store_true")
    args = ap.parse_args()
    if not args.today and not args.all:
        args.today = True

    try:
        label, items = load_items(args.today, args.date)
    except Exception as e:
        print(f"[gate-en][ERROR] {e}")
        return 1

    print(f"[gate-en] 检查 {label}：{len(items)} 条")
    total_fails, total_warns = 0, 0
    seen_ids = set()
    for i, it in enumerate(items, 1):
        iid = it.get("id") or f"#{i}"
        if iid in seen_ids:
            print(f"  ✗ [{iid}] 同批 id 重复")
            total_fails += 1
        seen_ids.add(iid)
        f, w = check_item(it, require_commentary=True)
        if f or w:
            print(f"  [{'FAIL' if f else 'WARN'}] {iid} {str(it.get('title',''))[:60]}")
            for x in f:
                print(f"      ✗ {x}")
            for x in w:
                print(f"      ! {x}")
            total_fails += len(f)
            total_warns += len(w)

    print(f"[gate-en] 汇总：{len(items)} 条 | 硬伤 {total_fails} | 提示 {total_warns}")
    if total_fails:
        print("[gate-en] FAIL — 硬伤未清，禁止进入构建/部署。先分析根因，不要兜底或硬跑。")
        return 1 if args.fail else 0
    print(f"[gate-en] 契约通过：{len(items)} 条，字段齐全，英文标题/摘要/评注在位")
    return 0


if __name__ == "__main__":
    sys.exit(main())
