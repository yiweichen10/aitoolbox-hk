#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""news_daily_pipeline_en.py — 英文站 AI 快讯日更「单一入口」串联器（2026-11-25 立规）

对标中文站 scripts/news_daily_pipeline.py。英文站差异：
- 采集源为国际 RSS / 官方博客（fetch_intl_news_en.py），非 aihot；
- 存储为单文件 data/news_en.json（非按天分文件），当日候选落在 data/news_<day>_en.json；
- 部署走 deploy_cf_en.py --upload（无 .deploy_last_result.json，以 rc + 线上验收为准）；
- 线上域名 https://www.aitoolbox.hk。

## 链路
  fetch → gate → merge → build → deploy → verify → backup
其中 gate 之后有一段**判断**不是确定性代码，脚本串不了，必须 Agent 做：
  - 同日/跨天「同事件」去重裁定
  - 标题主体核对（上游标题张冠李戴 / 标题党）
  - 英文事实浓缩（summary <=70 词）与原创 commentary（<=100 词）
所以流程切成两段：
  1) --until gate    （采集 + 硬门禁；首次必然因缺 commentary 中止，这是设计如此）
  2) Agent 提炼候选文件（就地改 data/news_<day>_en.json，保持 JSON 合法）
  3) --from gate     （门禁复检 → 合并 → 构建 → 部署 → 线上验收 → git 版本备份）

backup 步骤是非阻塞的：commit/push 失败只 WARN，不把已上线链路判为失败。
此前本链路不入库，靠 daily_growth_en.py（09:02）git add -A 顺带提交；
若那条自动化暂停/失败，快讯数据就无 git 版本备份，故在此自带一份。

## 用法
  python scripts/news_daily_pipeline_en.py                 # 全链路（适合 Agent 已提炼完时）
  python scripts/news_daily_pipeline_en.py --until gate    # 只跑采集 + 门禁
  python scripts/news_daily_pipeline_en.py --from gate     # 门禁复检 + 后半段（含 backup）
  python scripts/news_daily_pipeline_en.py --from verify --until verify  # 只重跑线上验收
  python scripts/news_daily_pipeline_en.py --dry-run       # 只打印计划

## 第一原则：禁止兜底（沿用中文站 2026-09-14 用户拍板）
任一步失败即非零退出，打印「先分析」指引。不要用默认值 / 猜测 / 静默跳过把缺陷填上。
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(BASE_DIR, "scripts")
DATA_DIR = os.path.join(BASE_DIR, "data")
STORE_PATH = os.path.join(DATA_DIR, "news_en.json")
CST = timezone(timedelta(hours=8))
SITE = "https://www.aitoolbox.hk"
STEPS = ["fetch", "gate", "merge", "build", "deploy", "verify", "backup"]


def _py():
    return sys.executable


def _run(script, step, *extra):
    cmd = [_py(), os.path.join(SCRIPTS, script), *extra]
    print(f"\n=== [{step}] $ python scripts/{script} {' '.join(extra)}")
    p = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    out = (p.stdout or "") + (p.stderr or "")
    print(out.rstrip())
    if p.returncode != 0:
        raise RuntimeError(f"步骤 [{step}] 失败 rc={p.returncode}\n--- 输出尾部 ---\n{out[-2000:]}")
    return out


def _today():
    return datetime.now(CST).strftime("%Y-%m-%d")


def _daily_path(day):
    return os.path.join(DATA_DIR, f"news_{day}_en.json")


# ── steps ────────────────────────────────────────────────────────────────────
def step_fetch(args):
    _run("fetch_intl_news_en.py", "fetch", "--date", args.date)
    path = _daily_path(args.date)
    items = json.load(open(path, encoding="utf-8"))
    if not items:
        raise RuntimeError(f"采集结果为空：{path}")
    print(f"  → 本期 {len(items)} 条：{os.path.basename(path)}")


def step_gate(args):
    _run("check_news_quality_en.py", "gate", "--today", "--date", args.date, "--fail")
    items = json.load(open(_daily_path(args.date), encoding="utf-8"))
    print(f"  → 门禁通过：{len(items)} 条")


def step_merge(args):
    """把当日候选合并进 news_en.json：按 id 覆盖、slug 生成、按发布时间倒序。
    写前备份；id 冲突但来源不同 → 拒绝（防止误覆盖他人条目）。"""
    day = args.date
    daily = json.load(open(_daily_path(day), encoding="utf-8"))
    if not daily:
        raise RuntimeError("当日候选为空，禁止合并")

    store = json.load(open(STORE_PATH, encoding="utf-8")) if os.path.exists(STORE_PATH) else []
    by_id = {it["id"]: it for it in store}
    added = updated = 0
    for it in daily:
        iid = it["id"]
        if iid in by_id:
            old = by_id[iid]
            if old.get("source_url") and it.get("source_url") and old["source_url"] != it["source_url"]:
                raise RuntimeError(f"id {iid} 已存在但 source_url 不同（拒绝覆盖）："
                                   f"old={old['source_url']} new={it['source_url']}")
            by_id[iid] = it
            updated += 1
        else:
            by_id[iid] = it
            added += 1
        # slug 由 id 日期 + 标题生成；标题被 Agent 改过则重算
        slug_title = re.sub(r"[^a-z0-9]+", "-", it["title"].lower()).strip("-")[:60]
        by_id[iid]["slug"] = f"{day}-{slug_title}"

    merged = sorted(by_id.values(),
                    key=lambda x: (str(x.get("published_at") or ""), str(x.get("id") or "")),
                    reverse=True)
    # 备份：固定名覆盖式保留最近 1 份（避免无限增长）。
    # 切勿用 STORE_PATH + f".bak-{day}"：那种命名不以 .bak 结尾，会绕过
    # .gitignore 的 *.bak 规则被永久入库，且每天一个新文件无限累积（2026-11-25 踩坑）。
    if os.path.exists(STORE_PATH):
        bak = STORE_PATH + ".bak"
        with open(bak, "w", encoding="utf-8") as f:
            json.dump(store, f, ensure_ascii=False, indent=1)
        print(f"  → 备份 {os.path.basename(bak)}")
    tmp = STORE_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=1)
    os.replace(tmp, STORE_PATH)
    print(f"  → 合并完成：新增 {added} / 更新 {updated} / 总计 {len(merged)} → data/news_en.json")


def step_build(args):
    _run("build_en.py", "build")


def step_deploy(args):
    out = _run("deploy_cf_en.py", "deploy", "--upload")
    if "DEPLOY failed after retries" in out:
        raise RuntimeError("部署脚本输出含 DEPLOY failed after retries（虽然 rc=0，仍视为失败）")
    print("  → 部署 SUCCESS（deploy_cf_en.py rc=0）")


def step_verify(args):
    """线上验收：/news/ 含本期日期 + 最新标题；期次页 200 且标题数不少于条数。"""
    day = args.date
    items = json.load(open(_daily_path(day), encoding="utf-8"))
    n = len(items)
    # 校验全部条目标题（原先只取前 3 条，第 4 条起只能靠期次页计数兜底）。
    titles = [it["title"] for it in items]

    def get(url):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 news-pipeline-en-verify"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.getcode(), r.read().decode("utf-8", "replace")

    errors = []
    # Cloudflare Pages 上传后 CDN 可能有数秒传播延迟；重试 3 次（每次间隔 8s）只针对
    # "内容还没到" 的情况，不做任何数据兜底。3 次仍不符则如实报错。
    import time
    for attempt in range(3):
        errors = []
        try:
            code, idx = get(f"{SITE}/news/")
            if code != 200:
                errors.append(f"/news/ HTTP {code}")
            if day not in idx:
                errors.append(f"/news/ 不含本期日期 {day}")
            # build_en._news_linkify 会把标题中匹配到工具名的词包成
            # <a href="/tools/{slug}/" class="news-inlink">词</a>（如 Claude、Nvidia），
            # 纯文本标题片段因此不连续。比对前先把这类锚点还原成纯文本副本，
            # 消除渲染层内链造成的假阴性；只用于比对，不改线上页面/数据。
            # 同理，build 会对 HTML 特殊字符做转义（如 2026-11-26 标题里的
            # "S&P" → "S&amp;P"，撇号 → "&#39;"），JSON 里是未转义的原文，
            # 故锚点还原后再 html.unescape 页面与标题，避免转义造成的假阴性
            # （2026-11-26 首轮 verify 即因此误报 S&P 标题缺失）。
            idx_plain = html.unescape(re.sub(r'<a href="/tools/[^"]*" class="news-inlink">(.*?)</a>',
                                             r'\1', idx))
            for t in titles:
                t_plain = html.unescape(t)
                if t_plain[:40] not in idx_plain:
                    errors.append(f"/news/ 不含本期标题片段：{t_plain[:40]!r}")
            code, page = get(f"{SITE}/news/{day}/")
            if code != 200:
                errors.append(f"/news/{day}/ HTTP {code}")
            if page.count('class="news-item-title"') < n:
                errors.append(f"期次页标题渲染数 {page.count('class=\"news-item-title\"')} < {n}")
        except Exception as e:
            errors.append(f"线上请求异常：{e}")
        if not errors:
            break
        if attempt < 2:
            print(f"  → 线上验收第 {attempt+1} 次未通过（CDN 传播中？），8s 后重试：{errors[0][:80]}")
            time.sleep(8)

    if errors:
        raise RuntimeError("线上验收未通过：\n  - " + "\n  - ".join(errors))
    print(f"  → 线上验收通过：{SITE}/news/{day}/ （{n} 条，标题命中）")


def step_backup(args):
    """版本备份：把本期产物 commit & push 到 GitHub，非阻塞。

    背景：本链路此前不入库，靠 daily_growth_en.py（09:02）的 git add -A 顺带提交。
    一旦 daily build 暂停/失败，快讯数据就一直无版本备份。这里自带一份，
    失败只 WARN 不中断——上线已由 deploy+verify 确认，git 只是可恢复性兜底。

    注意：git 属外部动作，但 push 到自有仓库 main 属于项目既有的版本备份惯例
    （daily_growth_en.py 同款），非公开发布，故纳入自动化链路。
    """
    def git(*argv):
        return subprocess.run(["git", *argv], cwd=BASE_DIR, capture_output=True,
                              text=True, encoding="utf-8", errors="replace")

    try:
        git("add", "-A")
        staged = git("diff", "--cached", "--quiet")
        if staged.returncode == 0:
            print("  → git 无改动，跳过 commit")
            return
        day = args.date
        msg = f"News briefs {day} (EN)"
        c = git("commit", "-m", msg)
        if c.returncode != 0:
            print(f"  ⚠ git commit 失败（非阻塞，不影响上线）：{(c.stderr or c.stdout).strip()[-300:]}")
            return
        print(f"  → git commit OK：{msg}")
        p = git("push", "origin", "main")
        if p.returncode != 0:
            print(f"  ⚠ git push 失败（非阻塞，不影响上线）：{(p.stderr or p.stdout).strip()[-300:]}")
            return
        print("  → git push OK（版本备份完成）")
    except Exception as e:
        # 非阻塞：任何异常都只告警，绝不让它把已上线的链路判为失败
        print(f"  ⚠ git 备份异常（非阻塞，不影响上线）：{e}")


STEP_FN = {
    "fetch": step_fetch,
    "gate": step_gate,
    "merge": step_merge,
    "build": step_build,
    "deploy": step_deploy,
    "verify": step_verify,
    "backup": step_backup,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="frm", default=STEPS[0], choices=STEPS)
    ap.add_argument("--until", dest="until", default=STEPS[-1], choices=STEPS)
    ap.add_argument("--date", default=_today(), help="候选日期 YYYY-MM-DD，默认今天（北京时间）")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    i0, i1 = STEPS.index(args.frm), STEPS.index(args.until)
    if i0 > i1:
        print(f"❌ --from({args.frm}) 在 --until({args.until}) 之后")
        return 2
    plan = STEPS[i0:i1 + 1]
    print(f"[news_daily_pipeline_en] 计划执行：{' → '.join(plan)}  (date={args.date})")
    if args.dry_run:
        print("(--dry-run 仅打印，不执行)")
        return 0

    t0 = datetime.now()
    step = plan[0]
    try:
        for step in plan:
            STEP_FN[step](args)
    except Exception as e:
        print(f"\n❌ 英文站快讯日更链路中止于 [{step}]：{e}")
        print("\n── 先分析，别硬跑（沿用中文站 2026-09-14 用户拍板）────────────────────")
        print("  1) 取证：读完原始输出，用 repr() 区分 None / '' / 键不存在，别用真值判断猜")
        print("  2) 分侧定位：谁写坏的（生产侧）+ 谁放行的（门禁侧），两侧都查")
        print("  3) 判断根因类型：上游数据？采集策略？契约没覆盖？边界没写？")
        print("  4) 只修根因；存量坏数据由人读过正文后判定写回（逐文件 .bak + 写后读回校验）")
        print("  5) 复现验证后再用 --from <step> 重跑对应段，不要从头盲跑、不要加兜底")
        print(f"\n  体检命令：{_py()} scripts/fetch_intl_news_en.py --audit-fields")
        print(f"           {_py()} scripts/check_news_quality_en.py --today")
        return 1
    print(f"\n🎉 英文站快讯日更全链路完成（{int((datetime.now()-t0).total_seconds())}s）："
          f"{SITE}/news/{args.date}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
