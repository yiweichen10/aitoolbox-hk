#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fetch_intl_news_en.py — 英文站 AI 快讯「国际源直采」(2026-11-25 立规)

设计对标中文站 scripts/fetch_aihot_news.py，但数据源换成国际 RSS / 官方博客：
英文站是国际化站点，直接抓一手英文源，比「中文站快讯→翻译」更及时、无翻译损耗。

## 契约（禁止兜底，2026-09-14 用户拍板沿用）
- 上游条目缺 title / summary / published_at，或解析不出 source_url → 直接拒收并打印明细，
  名额由其他合格条目补位，**如实少发不凑数**。禁止默认值 / 关键词猜测 / 静默跳过。
- category 来自本脚本 SOURCES 里**人工声明**的 source→category 静态映射（与中文站 CAT_MAP
  同性质），不是按正文猜出来的；不在白名单的映射是配置错误，硬失败。
- published_at 必须存在、可解析、且在 MAX_AGE_DAYS 窗口内，否则拒收（防止旧文混入）。

## 去重
- 跨天：与 data/news_en.json 全量比对（source_url 归一化 + 标题归一化）。
- 同批：批内 source_url / 标题归一化去重。
- 语义级「同事件不同措辞」由 Agent 在提炼步骤裁定（脚本不做模糊猜测）。

## 产物
  data/news_<YYYY-MM-DD>_en.json   # 当日候选（commentary 留空，等 Agent 提炼）

## 用法
  python scripts/fetch_intl_news_en.py [--date 2026-11-25] [--limit 8] [--force]
  python scripts/fetch_intl_news_en.py --list-sources
  python scripts/fetch_intl_news_en.py --audit-fields     # 只体检上游，不写文件

幂等：当日候选文件已存在且非空 → 直接跳过（--force 强制重采）。
"""
from __future__ import annotations

import argparse
import html as html_mod
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
STORE_PATH = os.path.join(DATA_DIR, "news_en.json")

CST = timezone(timedelta(hours=8))
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

MAX_AGE_DAYS = 3
DEFAULT_LIMIT = 8
MAX_PER_SOURCE = 2

# source→category 静态声明（人工核定，非正文猜测）
# 合法值必须与 build_en.py::NEWS_CATS 对齐：models / products / industry / research
VALID_CATEGORIES = ("models", "products", "industry", "research")

SOURCES = [
    # name, url, declared_category
    ("OpenAI Blog (RSS)", "https://openai.com/news/rss.xml", "models"),
    ("Google DeepMind Blog (RSS)", "https://deepmind.google/blog/rss.xml", "research"),
    ("Hugging Face Blog (RSS)", "https://huggingface.co/blog/feed.xml", "models"),
    ("MarkTechPost (RSS)", "https://www.marktechpost.com/feed/", "research"),
    ("The Decoder (RSS)", "https://the-decoder.com/feed/", "products"),
    ("TechCrunch AI (RSS)", "https://techcrunch.com/category/artificial-intelligence/feed/", "industry"),
    ("The Verge AI (RSS)", "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "products"),
    ("Ars Technica AI (RSS)", "https://arstechnica.com/ai/feed/", "research"),
    ("MIT Tech Review AI (RSS)", "https://www.technologyreview.com/topic/artificial-intelligence/feed", "industry"),
]

ATOM_NS = "{http://www.w3.org/2005/Atom}"
REQUIRED_FIELDS = ("title", "summary", "source", "source_url", "published_at", "category")


# ── RSS / Atom helpers ───────────────────────────────────────────────────────
def _text(node):
    if node is None:
        return ""
    return "".join(node.itertext()).strip()


def _strip_html(raw):
    """RSS description 常带 HTML；只做纯文本化，不猜内容。"""
    if not raw:
        return ""
    s = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = html_mod.unescape(s)
    s = s.replace("\u00a0", " ").replace("\r", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _parse_date(value):
    """支持 RFC822 / ISO8601；返回带时区的 datetime，失败返回 None。"""
    v = (value or "").strip()
    if not v:
        return None
    try:
        dt = parsedate_to_datetime(v)
        if dt is not None:
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
    except Exception:
        pass
    try:
        dt = datetime.fromisoformat(v.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


def _item_link(item):
    """RSS <link>text</link> 或 Atom <link href=...>。"""
    link = item.find("link")
    if link is not None:
        href = (link.get("href") or "").strip()
        if href:
            return href
        txt = _text(link)
        if txt:
            return txt
    alt = item.find(ATOM_NS + "link")
    if alt is not None:
        href = (alt.get("href") or "").strip()
        if href:
            return href
    return ""


def _item_summary(item):
    for tag in ("description", "content:encoded", ATOM_NS + "summary", ATOM_NS + "content"):
        node = item.find(tag)
        if node is not None:
            txt = _strip_html(_text(node))
            if txt:
                return txt
    return ""


def _item_date(item):
    for tag in ("pubDate", "published", "updated", ATOM_NS + "published", ATOM_NS + "updated"):
        node = item.find(tag)
        if node is not None and _text(node):
            return _text(node)
    return ""


def _fetch_feed(name, url):
    """抓单个源。Google 系 RSS 偶发返回截断 body（ParseError at line 1 col 0），
    做 2 次重试；仍失败则如实上报，由调用方打印 SOURCE-FAIL，不静默跳过。"""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rss+xml, application/xml, text/xml, */*"})
    last_err = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read()
            root = ET.fromstring(raw)
            break
        except ET.ParseError as e:
            last_err = e
            if attempt < 2:
                print(f"[news-en][RETRY] {name} XML 解析失败（第 {attempt+1} 次）：{e}")
                import time
                time.sleep(2)
                continue
            raise
    items = root.findall(".//item")
    if not items:
        items = root.findall(".//" + ATOM_NS + "entry")
    out = []
    for it in items:
        title_node = it.find("title") if it.find("title") is not None else it.find(ATOM_NS + "title")
        # RSS title 里常带 &#8217; / &amp; 等实体；ElementTree 只解标准 5 实体，数字实体需手动解
        title = html_mod.unescape(_text(title_node))
        out.append({
            "title": title,
            "summary": _item_summary(it),
            "source_url": _item_link(it),
            "published_raw": _item_date(it),
        })
    return out


# ── contract / dedup ─────────────────────────────────────────────────────────
def _norm_title(t):
    return re.sub(r"[^a-z0-9]+", "", (t or "").lower())


def _norm_url(u):
    return re.sub(r"[?#].*$", "", (u or "").strip().rstrip("/")).lower()


def check_item(it):
    """返回缺陷列表（空 = 合格）。禁止在调用侧补默认值。"""
    bad = []
    if not (it.get("title") or "").strip():
        bad.append("title 为空")
    if not (it.get("summary") or "").strip():
        bad.append("summary 为空（上游 description 无正文）")
    url = (it.get("source_url") or "").strip()
    if not url:
        bad.append("source_url 为空")
    elif not url.startswith(("http://", "https://")):
        bad.append(f"source_url 非 http(s)：{url[:80]!r}")
    pa = it.get("published_at")
    if not pa:
        bad.append("published_at 无法解析（上游未给时间或格式未知）")
    else:
        dt = _parse_date(pa) if isinstance(pa, str) else pa
        if dt is None:
            bad.append(f"published_at 无法解析：{pa!r}")
        else:
            age = datetime.now(timezone.utc) - dt.astimezone(timezone.utc)
            if age > timedelta(days=MAX_AGE_DAYS):
                bad.append(f"published_at 超窗（{age.days} 天前 > {MAX_AGE_DAYS} 天）")
            if age < timedelta(days=-1):
                bad.append("published_at 在未来（>1 天，上游时间错乱）")
    cat = it.get("category")
    if cat not in VALID_CATEGORIES:
        bad.append(f"category={cat!r} 不在白名单 {'|'.join(VALID_CATEGORIES)}（来源静态映射配置错误）")
    return bad


def _existing_keys():
    """从 news_en.json 取跨天去重的 url / title 键。"""
    urls, titles = set(), set()
    if os.path.exists(STORE_PATH):
        try:
            data = json.load(open(STORE_PATH, encoding="utf-8"))
            for it in data:
                if it.get("source_url"):
                    urls.add(_norm_url(it["source_url"]))
                if it.get("title"):
                    titles.add(_norm_title(it["title"]))
        except Exception as e:
            raise RuntimeError(f"读取 {STORE_PATH} 失败（跨天去重无法保证，禁止继续）：{e}") from e
    return urls, titles


def _daily_path(day):
    return os.path.join(DATA_DIR, f"news_{day}_en.json")


def _write_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


# ── main ─────────────────────────────────────────────────────────────────────
def run(day, limit, force, audit_only):
    if any(cat not in VALID_CATEGORIES for _, _, cat in SOURCES):
        bad = [(n, c) for n, _, c in SOURCES if c not in VALID_CATEGORIES]
        raise RuntimeError(f"SOURCES 静态 category 映射有非法值（配置错误）：{bad}")

    out_path = _daily_path(day)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 0 and not force and not audit_only:
        n = len(json.load(open(out_path, encoding="utf-8")))
        print(f"[news-en] 当日候选已存在且非空（{n} 条）→ 跳过采集：{os.path.basename(out_path)}")
        print("[news-en] 如需强制重采：加 --force（会覆盖当日候选，请先确认未提炼）")
        return 0

    existing_urls, existing_titles = _existing_keys()
    all_candidates, rejected = [], []

    for name, url, cat in SOURCES:
        try:
            raw_items = _fetch_feed(name, url)
        except Exception as e:
            # 单个源失败不静默：打印出来，但允许其他源补位（与中文站「少发不凑数」一致）
            print(f"[news-en][SOURCE-FAIL] {name}: {type(e).__name__}: {str(e)[:160]}")
            continue
        print(f"[news-en] {name}: 抓到 {len(raw_items)} 条")
        for raw in raw_items:
            pub_dt = _parse_date(raw["published_raw"])
            it = {
                "title": (raw["title"] or "").strip(),
                "summary": (raw["summary"] or "").strip(),
                "source": name,
                "source_url": (raw["source_url"] or "").strip(),
                "published_at": pub_dt.astimezone(CST).isoformat() if pub_dt else "",
                "category": cat,
            }
            bad = check_item(it)
            if bad:
                rejected.append((name, it.get("title", "")[:50], bad))
                continue
            it["summary"] = it["summary"][:900]  # 原始素材上限，Agent 再浓缩到 <=70 词（门禁硬线）
            all_candidates.append(it)

    print(f"\n[news-en] 上游合计 {len(all_candidates)} 条合格 / {len(rejected)} 条被字段契约拒收")
    # 大型归档源（OpenAI 1430 条 / HuggingFace 916 条）里超窗旧文占绝大多数，属预期的时效过滤，
    # 不是上游缺陷。按原因归类统计，明细只打印前 15 条，避免刷屏淹没真正的异常。
    from collections import Counter
    reason_counter = Counter()
    for _, _, bad in rejected:
        for b in bad:
            key = b.split("（")[0].split("：")[0]
            reason_counter[key] += 1
    print("[news-en] 拒收原因归类：" + " | ".join(f"{k}×{v}" for k, v in reason_counter.most_common()))
    for name, title, bad in rejected[:15]:
        print(f"  ⛔ [{name}] {title!r}: {'; '.join(bad)}")
    if len(rejected) > 15:
        print(f"  ... 另有 {len(rejected) - 15} 条同类拒收未逐条列出（完整清单可用 --audit-fields 配合重定向查看）")

    if audit_only:
        print("[news-en] --audit-fields：只体检，不写文件")
        return 0

    if not all_candidates:
        raise RuntimeError("采集结果为空（所有源失败或全被契约拒收）——本期不可发布，先分析上游，不要凑数")

    # 跨天 + 批内去重
    deduped, dup_n = [], 0
    seen_urls = set(existing_urls)
    seen_titles = set(existing_titles)
    for it in all_candidates:
        u, t = _norm_url(it["source_url"]), _norm_title(it["title"])
        if not u or not t:
            continue
        if u in seen_urls or t in seen_titles:
            dup_n += 1
            continue
        seen_urls.add(u)
        seen_titles.add(t)
        deduped.append(it)
    print(f"[news-en] 去重剔除 {dup_n} 条（与历史库重复或批内重复）")

    # 按源分组 + 轮转挑选，保证来源多样性
    by_src = {}
    for it in deduped:
        by_src.setdefault(it["source"], []).append(it)
    for k in by_src:
        by_src[k].sort(key=lambda x: x["published_at"], reverse=True)
    chosen = []
    srcs = list(by_src)
    while len(chosen) < limit and any(by_src.values()):
        progressed = False
        for s in srcs:
            if len(chosen) >= limit:
                break
            if by_src[s] and sum(1 for c in chosen if c["source"] == s) < MAX_PER_SOURCE:
                chosen.append(by_src[s].pop(0))
                progressed = True
        if not progressed:
            break

    chosen.sort(key=lambda x: x["published_at"], reverse=True)
    for i, it in enumerate(chosen, 1):
        it["id"] = f"{day.replace('-', '')}-{i:03d}"
        it["commentary"] = ""  # Agent 步骤填；空评注会被门禁拦下（设计如此）
    # 固定字段顺序，便于人读
    fields = ("id", "title", "summary", "category", "source", "source_url", "published_at", "commentary")
    chosen = [{k: it[k] for k in fields} for it in chosen]

    if len(chosen) < 4:
        print(f"[news-en] ⚠️ 本期仅 {len(chosen)} 条（历史常见 6-8 条）。若明显偏低，先分析："
              "上游断更？去重过严？契约拒收过多？不要补条目凑数。")

    _write_json(out_path, chosen)
    print(f"\n[news-en] 候选 {len(chosen)} 条 → {os.path.basename(out_path)}")
    print("[news-en] NEXT: Agent 逐条英文提炼（title/summary/commentary），再跑流水线门禁与合并")
    for it in chosen:
        print(f"  - {it['id']} [{it['category']}] {it['title'][:70]}")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="YYYY-MM-DD，默认今天（北京时间）")
    ap.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--audit-fields", action="store_true")
    ap.add_argument("--list-sources", action="store_true")
    args = ap.parse_args()

    if args.list_sources:
        for name, url, cat in SOURCES:
            print(f"{cat:9} | {name:28} | {url}")
        return 0

    day = args.date or datetime.now(CST).strftime("%Y-%m-%d")
    try:
        return run(day, args.limit, args.force, args.audit_fields)
    except Exception as e:
        print(f"[news-en][FATAL] {type(e).__name__}: {e}")
        print("[news-en] 先分析根因，不要加兜底或盲目重试（参见中文站快讯第一原则）")
        return 1


if __name__ == "__main__":
    sys.exit(main())
