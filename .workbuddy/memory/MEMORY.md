# seo-site-en 项目长期记忆（MEMORY.md）

## 价格字段规范（2026-08-05 确立，治本）
- `tools_en.json` 每个工具的 `price` 字段 = 卡片/徽章用的**短价格标签**（语义化，≤50 字符，如 "From $199 one-time" / "Free + Pro from $19/mo"）。
- 长价格说明**禁止**写进 `price` 字段；应放在 `pricing_details` 字段（结构化备份），且正文 content 的 Pricing 小节已覆盖详情。
- 历史污染（2026-08-05 修复）：23 个工具 price 超长（Exa 750 / Elicit 670 / LanguageTool 503 … Topaz 276 字符），已用 AI 语义化重写为短标签，原长文移入 `pricing_details`。
- 修复脚本：`scripts/fix_price_labels.py`（映射表 SHORT_MAP，可复用）。

## 禁止治标，必须治本（用户 2026-08-05 跨项目原则）
- 任何"显示异常/溢出/格式问题"优先根治数据/架构根因，禁用截断/CSS 隐藏/占位省略等表现层修补。
- 已落地防御：`build_en.py` 构建时校验 `price>80` 字符打印 `[PRICE WARNING]`（报警非截断）；`gen_tools_en.py` 迁移时自动拆分短标签 + `pricing_details`。

## 构建 / 部署
- 构建：`python scripts/build_en.py --target tools`（仅工具页）/ `--target all`（全量 + OG 图）
- OUT_DIR = 项目根（BASE_DIR）；日志前缀 `en/` 是历史硬编码，实际产物在 `tools/`、`articles/`、`category/`。
- 数据治理前务必备份 `data/tools_en.json`（铁律 #3）。

## 录入脚本是历史污染源（2026-08-05 标注）
- 根目录 `add_*.py` 与 `scripts/add_*.py` 在写入 tools_en.json 时直接填了超长 price（如 add_cleanvoice.py / add_exa.py / add_elicit.py）。
- 这些工具已通过 fix_price_labels.py 治理；未来新增工具若复用此类脚本，必须遵循 price 短标签规范（build 校验会报警）。
