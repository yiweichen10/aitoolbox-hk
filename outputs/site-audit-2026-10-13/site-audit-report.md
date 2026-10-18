# aitoolbox.hk 全站审计报告

**审计日期：** 2026-10-13（GMT+8）  
**范围：** 线上首页、文章详情、文章分页、AI Chat 分类、ChatGPT 工具页；本地生成模板、CSS、robots/sitemap/llms、文章与工具数据。  
**设备视口：** Chromium 桌面 1440×1000、移动 390×844。  
**结论：** 站点有清晰的工具目录定位、完整静态页面和可抓取基础；当前优先级不是再加一层 GEO schema，而是修正**搜索范围、错误评分结构化数据、移动导航、暗色对比度和站点信任信息不同步**。本次没有确认 P0 全站不可用故障。

## 执行摘要

- 本地数据：**221 个工具、189 篇文章**；robots.txt 允许常见爬虫并声明 sitemap。新文章能在线打开，canonical、Article/FAQPage JSON-LD 与对比表均可见。
- 首页移动视口没有显著横向页面溢出（文档宽 382px / 390px），但顶部导航内容宽 428px、可视宽 243px，需要横向滑动；品牌标题被挤成三行。
- 首页搜索只在首页渲染的 **12 张工具卡片**里匹配。用“capcut”搜索时，页面给出“未找到”，尽管该工具已在站内目录中。
- ChatGPT 工具页的 AggregateRating 把 **125K visits** 当成 **125,000 ratings**；页面没有相应评分数量依据。该页还含四种指向错误根路径的工具链接及重复 FAQ 区块。
- 新文章的暗色模式实测正文文字/背景对比度仅 **1.41:1**，普通正文建议至少达到 WCAG AA 的 4.5:1。
- 首页显示 221+ 工具、189 篇文章；`llms.txt` 仍写 211、177（更新日期 2026-10-01）；About/Author 页面仍写 110+、70+（2026 年 6 月数据）。
- 内容库抽样统计：186/189 篇含 Markdown 对比表；136/189 篇有站内文章链接；2 篇没有 FAQ 标题。重点是统一质量与事实维护口径，而不是机械给每篇塞关键词。

## 优先修复项

| 优先级 | 发现 | 证据与影响 | 建议 |
|---|---|---|---|
| **P1** | 搜索承诺 221+，实际只搜首页 12 个 | `scripts/build_en.py` 的首页按 visits 取前 12；`performSearch()` 只遍历 `.tool-card`。线上移动端搜索 `capcut` 返回“未找到”，没有路由到完整目录的结果页。首页 JSON-LD 的 SearchAction 使用 `/?q=...`，但查询参数没有对应的服务端结果页。 | 让搜索覆盖 `tools_en.json` 全量记录并渲染可访问的结果列表，支持可复制/可分享的查询 URL；或把文案改成仅搜索精选工具，并移除不工作的 SearchAction。搜索功能应支持键盘 Enter、空结果及屏幕阅读器结果播报。 |
| **P1** | 工具评分 Schema 的数量值错误 | `scripts/build_en.py` 将 `visits` 解析为 `_rating_count`，写入 `AggregateRating.ratingCount`。线上 ChatGPT 页的 visits 是 125K，JSON-LD 输出 ratingCount 125000；两者不是同一指标。虚报数量会损害结构化数据可信度，也可能使评分富结果失去资格。 | 立即删除由 visits 推导的 AggregateRating；只有存在真实、可证明且页面可见的评分汇总与评数时才输出。把 visits 单独标为访问量，不与用户评分混用。 |
| **P1** | 移动端页眉导航拥挤、主品牌折行 | 390px 视口下 `.header-nav` scrollWidth 428px、clientWidth 243px；实际可以横向滚动，但滚动条隐藏，后续入口不明显。品牌名在截图中折成“AI / Tool / Lab”，更新标识也多行，首屏纵向空间被页眉吃掉。 | 小屏改为简洁菜单/明确的横向分类导航，给滚动导航加边缘渐隐或可见提示；为 logo/品牌设置 `flex-shrink:0`、限制标题不换行，并检查 320/360/390px 和放大字体。 |
| **P1** | 暗色模式正文不可读 | 线上切换暗色后，文章正文颜色仍为 `#334155`，背景是 `#1e293b`，计算对比度 **1.41:1**；段落、列表、表格单元格都存在固定深色文字规则。 | 正文、列表、表格、引用块统一改用主题变量；按 WCAG AA 测普通字号至少 4.5:1、大字至少 3:1，并将两种主题纳入视觉回归。 |
| **P1** | GEO / E-E-A-T 站点信息相互矛盾 | 首页写 221+ 工具、189 篇；`llms.txt` 写 211、177，且声明 10 月 1 日更新；`about.html` 与 `author/index.html` 仍写 110+ 工具、70+ 文章及 6 月数字。About/Author 自称 5+ 年经验，但没有明确到人的作者/测试记录来支撑。AI 搜索引用时会读到冲突信号。 | 统一从数据源生成首页、About、Author、llms.txt 的计数/日期；说明“团队累计经验”还是站点运营年限。建立作者署名、测试日期、版本/计划、测试步骤和来源链接，避免无法追溯的“每天更新/实测”承诺。 |
| **P1** | 分类 FAQ Schema 有不准确的价格答案且页面不展示 FAQ | `build_en.py` 用“分类中价格字符串含 `$` 的工具数量”拼成“最高每月价格”，不是实际价格；AI Chat 11 个工具因此会被写成最高 `$9/month`，但 ChatGPT 卡片展示 `$20/mo`。这段 FAQPage JSON-LD 不在分类页正文呈现。 | 先删除这类猜值 FAQ；若保留 FAQ，基于真实价格数据生成、明确计费周期/币种，并在页面正文同步展示。不要为 GEO 编造问答或只在 HTML head 放答案。 |
| **P1** | 联系/报错入口落到不存在的本地页面 | 多个文章、工具、About、Author 页面链接 `/contact.html`；仓库没有此页面，`vercel.json` 也没有相应重写。用户报告价格错误、提交工具的路径因此可能断掉。 | 建立真实联系页面/表单，或替换成当前可用的邮件/反馈渠道；加入链接有效性测试。 |

## SEO、内容与结构化数据的后续项

| 优先级 | 发现 | 建议 |
|---|---|---|
| **P2** | 文章分页第 2 页及后续页都 canonical 到 `/articles/` | 线上 `/articles/page/2/` 的 canonical 确实指向 `/articles/`，但页面包含不同文章入口。建议确认该设计是否有意合并分页；若分页承担旧内容发现，应输出各分页自 canonical、唯一标题/描述，并保留可爬取的 Prev/Next/页码链接。结合 Search Console 的抓取与索引数据再决定，不应只因“分页”一概处理。 |
| **P2** | H1 语义被站点 Logo 占用 | 首页主标题“Find the Best AI Tools for Your Work”是 H2，而站点 Logo 是 H1；文章页同时有品牌 H1 与文章标题 H1；工具详情页主体标题是 H2。建议 Logo 改普通文本/非标题元素，每页保留一个明确描述主体主题的 H1。 |
| **P2** | 文章 `<meta name="keywords">` 输出 Python 列表格式 | 新文章线上输出 `['Browser Use pricing', ...]`，带方括号、引号。meta keywords 对 Google 排名不是重点，但当前格式不专业且暴露内部序列化；生成前将数组 join 成逗号分隔文本，或移除此元标签。 |
| **P2** | 新文章 FAQ JSON-LD 中有原始 Markdown 链接语法 | 可见答案链接正常，但 FAQPage `Answer.text` 包含 `[pricing page](https://...)` 原始 Markdown。清洗脚本应在写 JSON-LD 前转换为纯文本；再用 Schema Validator / Rich Results Test 抽验。 |
| **P2** | 工具页旧内容质量不均 | 抽查 ChatGPT 页看到关键词填充式短语（如“chatgpt review writing”）、重复 FAQ（18 个工具页出现多个 FAQ 标题）、版本信息在同页未清楚标注日期，以及“数据可验证”但来源没有直接链接等问题。这是页面样本，不代表 221 个工具页全都如此。 | 按流量/商业意图先审前 20 个工具页：产品版本、价格日期、优缺点证据、替代品链接、重复问题、语言自然度、原始来源。使用抽样校准后再批量整理其余页面。 |
| **P2** | 内容库内链与 FAQ 覆盖仍不均 | 136/189 篇有站内文章链接；53 篇未见文章内链。186/189 篇有 Markdown 表格；2 篇未见 FAQ 标题。 | 按主题集群建立“工具页—对比指南—教程/案例”内链；缺少 FAQ 时补真实高意图问答，而非统一模板灌入。保留每篇的独立结论与证据。 |
| **P2** | 分类页有单工具薄页和近义分类风险 | 本次模板和分类清单显示存在单工具分类及近义类别；比如 `image` 与 `ai-images` 的主题容易重叠。 | 对每个分类按用户任务重画 taxonomy；有独立搜索意图的分类加入原创导读、选型维度和高质量候选，否则合并或用目录页作入口。避免只为凑“32 categories”保留薄页。 |
| **P2** | Sitemap 的 `lastmod` 可能不是实际修改时间 | 生成器给首页/分类/工具页统一写当天日期，文章则默认用发布日期。`lastmod` 因而不总反映内容变更。 | 仅在实质内容更新时写真实 `dateModified`/文件变更日期；不要每次构建就把所有 URL 标成当天更新。 |

## UI / UX 已有优点

- 首页定位和主要任务直观：站内工具目录、分类入口、搜索框、精选工具及最新文章都在首页。
- 1440px 桌面视口版面层次清楚；新文章排版可读，官方价格来源、表格、FAQ、更新时间、OG 图片均具备。
- 移动首页在本次视口没有明显全页横向溢出，分类 chip 会换行；主要问题集中在页眉空间与导航可见性，不是整个布局崩坏。
- `robots.txt` 有 sitemap 声明并允许常见爬虫；不要把“再添加一批 AI crawler 名称”当成首要 GEO 项。

## 建议执行顺序

1. **先修准确性与损害风险：** 删除错误 AggregateRating、修正分类价格 FAQ、替换坏掉的联系入口。
2. **修实际体验：** 首页全量搜索和搜索结果页；移动页眉/导航；暗色正文对比度。
3. **统一权威信息：** About/Author/首页/`llms.txt` 共用计数和更新日期；补齐作者/测试/引用透明度。
4. **做可持续质量护栏：** 全站内链 checker（不只 `/articles/`）、标题/H1 检查、Schema JSON 校验、价格 FAQ 数据校验、窄屏与深色视觉回归。
5. **之后看 SEO 数据再调：** 分页 canonical、分类合并、内容集群与内链，以 Search Console 的索引/查询数据判断收益。

## GEO 判断

对 AI 检索最有价值的是**能被直接抓取的正文、清楚的实体关系、日期与版本、第一手测试细节、可点开的官方证据、相互一致的作者/组织信息**。当前站点已有静态 HTML、可访问的工具/文章页、FAQ 和比较表等基础；最大的反效果是旧数字过时、价钱/评分 Schema 不可靠、来源承诺不兑现。建议不追逐“GEO 密度”或额外堆 Schema：Google 的生成式 AI 指南仍以常规可抓取、可索引、可靠且有帮助的内容为基础。

## 审计边界

这是**代码/数据广度检查 + 线上关键页面抽查**，不是 221 个工具页逐页人工验收，也不含 Search Console、GA、服务器日志、真实用户转化或多地区抓取数据。没有验证线上每一个损坏链接的 HTTP 状态、中文站每条 hreflang 的反向对应，也没有在真实 iOS/Android、屏幕阅读器和低网速下完整走查。报告内提及线上事实均注明了抽查页面与视口；全站化问题需修复后再跑自动测试确认。

## 参考

- Google Search Central — [生成式 AI 搜索功能优化指南](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)
- Google Search Central — [规范网址与 canonical](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
- Google Search Central — [Review Snippet / AggregateRating](https://developers.google.com/search/docs/appearance/structured-data/review-snippet)
- Google Search Central — [FAQPage structured data](https://developers.google.com/search/docs/appearance/structured-data/faqpage)

## 本次截图

- `home-desktop.png`、`home-mobile.png`：首页布局抽查
- `article-desktop.png`、`article-dark.png`：新文章亮色与暗色对比
