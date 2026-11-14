#!/usr/bin/env python3
"""
Cloudflare Pages 部署准备脚本（aitoolbox.hk）

用途：把站点「产物」复制到干净的 _deploy_cf/ 目录，再（可选）上传到 Cloudflare Pages。
只复制网站运行所需的文件，排除 data/、scripts/、_archive/、草稿、备份等本地资产。

用法：
  python scripts/deploy_cf.py            # 仅准备 _deploy_cf/ 并打印统计（dry-run）
  python scripts/deploy_cf.py --upload   # 准备 + 调用 wrangler 上传
                                           # 需要环境变量 CLOUDFLARE_API_TOKEN（禁止硬编码）

安全：token 只从环境变量读取，不落盘、不回显。
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_deploy_cf"
PROJECT = "aitoolbox-hk"

# 网站根目录下的静态文件白名单
ROOT_FILES = [
    "index.html", "404.html", "about.html", "tts-demo.html",
    "favicon.ico", "robots.txt", "sitemap.xml", "llms.txt",
    "_headers", "_redirects",
    "00859eedcd7c1f5e6a38204096fe2a57.txt",   # IndexNow key
    "google06ea2c88965e9881.html",             # Google 验证
    "yandex_5ae78527ec9bcb4b.html",            # Yandex 验证
]

# 需要整目录复制的站点资源
DIRS = ["articles", "author", "category", "css", "images", "js", "tools"]


def prepare() -> tuple[int, int]:
    # 注意：不能 rmtree 整个 _deploy_cf（1000+ 文件会触发沙箱的批量删除保护，
    # 报 SAFE_DELETE_BULK_CONFIRM_REQUIRED）。改为原地覆盖复制。
    # 代价：源里已删除的旧文件会在 _deploy_cf 中残留，需要时手动清理一次。
    OUT.mkdir(parents=True, exist_ok=True)

    copied, missing = 0, []
    for name in ROOT_FILES:
        src = ROOT / name
        if src.is_file():
            shutil.copy2(src, OUT / name)
            copied += 1
        else:
            missing.append(name)

    files = 0
    for d in DIRS:
        src = ROOT / d
        if src.is_dir():
            shutil.copytree(src, OUT / d, dirs_exist_ok=True)
            files += sum(1 for _ in src.rglob("*") if _.is_file())
        else:
            missing.append(d + "/")

    size = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
    total_files = sum(1 for f in OUT.rglob("*") if f.is_file())

    print(f"OUT            {OUT}")
    print(f"ROOT_FILES     {copied}/{len(ROOT_FILES)}")
    print(f"DIR_FILES      {files}")
    print(f"TOTAL_FILES    {total_files}  (CF Pages 免费上限 20000)")
    print(f"TOTAL_SIZE     {size / 1048576:.1f} MB")
    biggest = max((f.stat().st_size, f) for f in OUT.rglob("*") if f.is_file())
    print(f"BIGGEST_FILE   {biggest[0] / 1048576:.2f} MB  {biggest[1].relative_to(OUT)}  (CF 单文件上限 25 MiB)")
    if missing:
        print(f"MISSING        {missing}")
    return total_files, size


def upload() -> int:
    # 两种鉴权方式任选其一：
    #  1) wrangler OAuth 登录态（推荐，先跑一次 `wrangler login`）
    #  2) 环境变量 CLOUDFLARE_API_TOKEN（CI/无交互环境）
    token = os.environ.get("CLOUDFLARE_API_TOKEN")
    print("AUTH_MODE      " + ("api_token" if token else "wrangler_oauth（本地已登录态）"))

    # Windows 下 wrangler 是 npm 生成的 .cmd，Python subprocess 不会自动补扩展名，
    # 必须先用 shutil.which 解析出完整路径，否则报 WinError 2。
    exe = (shutil.which("wrangler")
           or shutil.which("wrangler.cmd")
           or shutil.which("wrangler.exe"))
    if not exe:
        print("ERROR: 未找到 wrangler 可执行文件。请先执行：npm i -g wrangler")
        return 2
    print("WRANGLER       " + exe)

    cmd = [
        exe, "pages", "deploy", str(OUT),
        "--project-name", PROJECT, "--branch", "main", "--commit-dirty=true",
    ]
    print("RUN", " ".join(cmd[:4]), "...")
    return subprocess.call(cmd, cwd=str(ROOT))


if __name__ == "__main__":
    n, size = prepare()
    if n > 20000:
        print(f"ERROR: 文件数 {n} 超过 CF Pages 免费上限 20000，需要拆分或升级。")
        sys.exit(1)
    if "--upload" in sys.argv:
        sys.exit(upload())
    print("\nDRY-RUN 完成。加 --upload 参数执行真实部署。")
