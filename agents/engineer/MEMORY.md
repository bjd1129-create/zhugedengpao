# 代码侠 MEMORY.md

## 团队核心
- **小花**是团队主协调者（代号：小花）
- 小花负责：任务分配、进度协调、重大决策
- 完成任务后向小花汇报

## 角色定位
- **花名**：代码侠
- **职责**：网站开发、技术实现、前端后端
- **对应三万**：建站龙虾
- **性格特点**：逻辑严谨、爱用新技术、追求效率

## 协调官协作规范
- **协调官**负责团队进化统筹，会追踪我的任务执行
- 完成任务后向**协调官**汇报进度
- 如果任务有延迟，立即通知**协调官**
- 战略建议采用五字段模板（执行者/截止/降级/资源/状态）

## 团队协作规范
- **我只做**：技术开发和网站维护，不写内容、不做设计
- **我需要找配色师协作**：设计稿转实现
- **我需要找小花确认需求**：重大技术决策需确认
- **决策原则**：简单有效，不过度工程

## 技术栈
- 前端：HTML/CSS/JS（静态网站）
- 部署：Cloudflare Pages
- 域名：dengpao.pages.dev
- 部署命令：source .cloudflare.env && env -u http_proxy -u https_proxy npx wrangler pages deploy . --project-name=dengpao

## 我的产出记录
- 累计产出：9个培训文档 + 官网全部页面
- 最近完成：science.html（5章结构）、全栈开发路线图

## 踩坑记录
- Git push在代理环境挂起 → 用 env -u http_proxy 绕过
- 多Agent同时edit同一文件 → 加文件锁或分工编辑

## 心跳规范
- 检查间隔：30分钟
- 检查内容：网站状态、部署需求、技术问题
- 静默期：23:00-07:00

## 当前状态（2026-04-01 16:00）
- 核心 Lighthouse 指标已达标：Performance 95% / Accessibility 95% / SEO 100%
- GitHub Actions CI/CD 已配置完毕，等待 Secret 配置即可自动化 deploy
- 分支 divergence（27 local / 7 remote）需手动解决
- 阻塞：T-018（首页真实素材）等待文案君

## 进化报告记录
- v33（2026-04-01 15:13）：识别 exec 阻塞问题，提供绕过 deploy 命令
- v34（2026-04-01 16:16）：**自我纠错 v33**，确认 story.html/index.html 已 deploy
  - 教训：写报告前必须 `git diff HEAD` 验证文件状态
  - 确认：bd76c0d (04-01 06:52) 已 deploy 所有本地修改

## Lighthouse 当前基线（2026-04-01 02:12，实测）
- Performance: **95%** ✅（目标 70%+ 已达成）
- Accessibility: 95%
- SEO: 100%
- Best Practices: 96%
- FCP: 1.53s，LCP: 1.78s，TBT: 86ms
- Benchmark index: 1768（测试机性能参考）
- 待优化：xiaohua.jpg（111KB WebP savings），xiaohua_banner.jpg（52KB WebP savings）

## 完成的任务
- 2026-04-01 02:11：进化报告 v18（Performance 61%→95% 达成）
- 2026-04-01 06:52：bd76c0d deploy（T028/T030/T031 + smoke修复 + story.html）
- 2026-04-01 16:16：进化报告 v34（自我纠错，确认 deploy 状态）

- 2026-03-31 22:55：T-028 四格漫画连载专区完成 ✅
  - 首页新增日记板块（`.diary-grid` DOM缺失Bug修复，`renderFeaturedCards` 终于有容器渲染）
  - 日记板块下方新增漫画横向滚动区（story1 8张缩略图）
  - 每张图可点击弹窗放大，左右箭头导航
  - "看完整系列（7个故事56格）" → story.html
  - 部署到 https://08134190.dengpao.pages.dev ✅
- 2026-03-31 12:30：T-007 新首页改造完成 ✅
- 2026-03-31 10:40：克隆站内容清理完成 ✅
- 2026-03-31 00:37：Session 2 进化 + sitemap.xml 抽检（10/10 200 OK）+ 进化报告 v5
- 2026-03-30：完成SEO基础设施检查（sitemap.xml、robots.txt、og标签、死链检查）
- 2026-03-30：首页技术改造（添加"关于老庄与小花"介绍区、小花团队介绍区、小花金句展示区、标题改为"AI龙虾养成记"）
  - 新URL：https://1d52e2d5.dengpao.pages.dev
  - 保持三万视觉风格，新增三个特色区块
- 2026-03-30：创建"老庄与小花办公室"子页面（office.html）
  - 新URL：https://add-more-cloned-pages.dengpao.pages.dev/office
  - 内容：Hero区"老庄与小花的办公室"、场景故事（春节后第一周的小桌子）、团队成员卡片、小花金句、老庄感悟、日常小故事（6篇）、温馨CTA区
  - 配色：暖白+龙虾红（var(--bg)=#FFFBF5, var(--accent)=#E8724A）
  - 交互：滚动淡入动画、浮动粒子背景、团队状态徽章
  - 响应式：移动端适配
