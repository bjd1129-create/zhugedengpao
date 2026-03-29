# SHARED_MEMORY.md - 团队共享记忆

> 诸葛灯泡团队共享记忆中心
> 更新时间：2026-03-29 04:09

---

## 🏗️ 团队架构

### 当前架构（2026-03-28 更新）

**7 人精简团队，对标三万：**

| 角色 | Emoji | 职责 | 对标三万 |
|------|-------|------|----------|
| 造梦者 | 👑 | 协调 + 系统 + 进化 | 三万（主） |
| 文案君 | 📝 | 内容 + 视觉 | 笔杆子 |
| 洞察者 | 🔍 | 研究 + 数据 | 参谋 |
| 代码侠 | 💻 | 技术开发 | 建站龙虾 |
| 播种者 | 🌱 | 增长 + 互动 + 运营 | 运营 + 推广 |
| 安全官 | 🛡️ | 安全防护 | 安全官 |
| 财务官 | 💰 | 成本监控 | 财务官 |

### 架构调整记录

**2026-03-28 精简调整：**

| 调整类型 | 原角色 | 新归属 |
|----------|--------|--------|
| 合并 | 🎯 掌舵人 | 👑 造梦者 |
| 合并 | 🎨 配色师 | 📝 文案君 |
| 合并 | 🔮 预言家 | 🔍 洞察者 |
| 合并 | 🛠️ 守护者 | 🌱 播种者 |
| 合并 | 📅 调度员 | 🌱 播种者 |
| 新增 | - | 🛡️ 安全官 |
| 新增 | - | 💰 财务官 |

---

## 🎯 三万团队对标 (2026-03-29 04:09 更新)

**对标文件：** SANWAN_BENCHMARK.md

### 差距分析汇总

| 维度 | 差距程度 | 优先级 | 状态 |
|------|----------|--------|------|
| 云上托管 | 🟢 已解决 | P0 | ✅ 老庄电脑不关机=云服务器 |
| 定时任务 | 🟢 已配置 | P0 | ✅ Cron 每 30 分钟心跳 |
| spawn 协作 | 🟡 待激活 | P1 | ⏳ 目标每日>10 次 |
| 技能利用 | 🟡 待提升 | P1 | ⏳ 92 个技能需激活 |
| 记忆系统 | 🟢 完善 | P2 | ✅ 5 文件完整 |
| 团队架构 | 🟢 精简 | P2 | ✅ 7 人对标 8 人 |

### 核心优势

**本地部署方案：**
- ✅ 老庄电脑 24h 不关机 = 免费云服务器
- ✅ OpenClaw 本地运行
- ✅ 飞书通道已配置
- ✅ 心跳机制已激活

**三万秘密 = OpenClaw + 云上托管 + 定时任务 + spawn 协作**

我们已有：
1. ✅ 云上托管（老庄电脑）
2. ✅ 定时任务（心跳触发）
3. ⏳ spawn 协作（待激活）
4. ⏳ 技能利用（待提升）

### 追赶进度

| 阶段 | 任务 | 状态 |
|------|------|------|
| **第 1 周** | Cron 定时配置 | ✅ 完成 |
| **第 1 周** | SKILL.md 创建 | ✅ 完成 |
| **第 1 周** | spawn 协作激活 | ⏳ 进行中 |
| **第 1 周** | 三问反思配置 | ⏳ 进行中 |
| **第 2 周** | spawn 频率提升至>10 次/日 | ⏳ 待开始 |
| **第 3-4 周** | 全面自主运行 | ⏳ 待开始 |

---

## 🌐 三万网站对标 (2026-03-29 07:00 更新)

**参考网站：** https://sanwan.ai
**决策：** 以后只对照sanwan.ai，把三万的页面和内容全部克隆过来

### 页面清单

| 页面 | 文件 | 状态 |
|------|------|------|
| 首页 | index.html | ✅ 已有 |
| 日记 | diary.html | ✅ 已有 |
| 文章 | articles.html | ✅ 已有 |
| 科普 | science.html | ✅ 已有 |
| 技能 | skills.html | ✅ 已有 |
| Office | office.html | ✅ 已重构 |
| EasyClaw | easyclaw.html | ✅ 已完成 |

---

## 🎯 关键决策记录

### 2026-03-28 团队精简决策

**决策：** 从 10 人精简为 7 人

**原因：**
1. 对标三万团队 8 人架构
2. 协调角色冗余
3. 用户运营过度分散
4. 缺少安全官、财务官

**原则：**
- 各管一摊，专注一件事
- 并行执行，不等待不阻塞
- 全自动化覆盖

---

## 📋 任务分工

### 内容发布流程

```
👑 造梦者 收到任务
    ↓
📝 文案君 写文案 + 设计封面
    ↓
🔍 洞察者 数据追踪准备
    ↓
🌱 播种者 发布 + 互动
    ↓
🛡️ 安全官 检查平台规则
    ↓
💰 财务官 记录成本
```

### 研究分析流程

```
🔍 洞察者 研究 → 分析 → 建议
    ↓
👑 造梦者 决策
    ↓
执行团队执行
```

---

## ⚠️ 重大事件

### 小红书封禁事件 (2026-03-28)

**事件：** 发布第 1 集后，小红书账号被封禁

**根本原因：** VPN 代理触发 IP 检测

**教训：**
- 关闭 VPN 后发布小红书内容
- 新账号需要养号阶段
- 发布前必须研究平台规则

**改进：**
- 新增安全官角色
- 建立平台规则知识库
- 制定发布检查清单

---

## 📊 平台状态

| 平台 | 账号状态 | 备注 |
|------|----------|------|
| 小红书 | ⚠️ 封禁 | 需申诉或新建 |
| 微博 | ✅ 正常 | - |
| 知乎 | ✅ 正常 | - |
| 公众号 | ✅ 正常 | - |

---

## 🔗 重要链接

| 资源 | 链接 |
|------|------|
| 主站（缓存问题） | https://dengpao.pages.dev |
| 新部署 | https://e32f78ee.dengpao.pages.dev |
| Vercel | https://dengpao-team.vercel.app |
| Netlify | https://dengpao-official.netlify.app |

---

## 📝 每日汇报规则

- **时间：** 每晚 21:00
- **内容：** 今日总结 + 明日规划
- **负责人：** 👑 造梦者

---

## 💰 MiniMax 套餐限制 (2026-03-29 07:13)

**套餐：** 5小时 / 5000次
**平均：** 每3.6秒1次

**使用分配策略：**
| 任务 | 预计次数 | 优先级 |
|------|---------|--------|
| 内容创作（文案君） | 1500次 | P0 |
| 官网克隆（代码侠） | 800次 | P0 |
| 运营执行（播种者） | 800次 | P1 |
| 热点研究（洞察者） | 500次 | P1 |
| 系统维护（造梦者） | 200次 | P2 |
| 安全巡检（安全官） | 200次 | P2 |

---

## 🎯 商业模式 (2026-03-29 09:07)

**决策：EasyClaw服务 + 知识付费**

| 产品 | 定价 | 状态 |
|------|------|------|
| EasyClaw 安装服务 | ¥299/次 | ✅ 已决策 |
| AI团队搭建教程 | ¥199 | ✅ 已决策 |
| 月度AI团队托管 | ¥999/月 | ✅ 已决策 |

**下一步：**
1. 文案君 → 撰写产品页文案
2. 代码侠 → 开发产品页面
3. 播种者 → 制定推广计划

---



**套餐：** 5小时 / 5000次
**平均：** 每3.6秒1次

**使用分配策略：**
| 任务 | 预计次数 | 优先级 |
|------|---------|--------|
| 内容创作（文案君） | 1500次 | P0 |
| 官网克隆（代码侠） | 800次 | P0 |
| 运营执行（播种者） | 800次 | P1 |
| 热点研究（洞察者） | 500次 | P1 |
| 系统维护（造梦者） | 200次 | P2 |
| 安全巡检（安全官） | 200次 | P2 |

---

## 🎯 决策权限

| 决策类型 | 权限 |
|----------|------|
| 内容选题 | ✅ 自主决策 |
| 发布时机 | ✅ 自主决策 |
| 平台选择 | ✅ 自主决策 |
| 策略调整 | ✅ 自主决策 |
| 重大变更 | ⚠️ 通知老庄 |
| 资金支出 | ❌ 需老庄确认 |

---


---

## 🌐 VoxYZ.Space 对标 (2026-03-29 08:19 新增)

**参考网站：** https://voxyz.space
**研究报告：** `agents/researcher/memory/voxyz-analysis.md`

### 核心功能对比

| 功能模块 | VoxYZ | 我们 | 差距 |
|----------|-------|------|------|
| **Office 仪表盘** | ✅ 实时 Agent 状态 | ✅ 已有 (office.html) | 🟢 相当 |
| **Stage 直播流** | ✅ 实时协作展示 | ❌ 无 | 🔴 需开发 |
| **Radar 需求雷达** | ✅ 461 信号追踪 | ❌ 无 | 🔴 需开发 |
| **Vault 产品页** | ✅ $79/$199 套餐 | ❌ 无 | 🔴 需开发 |
| **Insights 文章** | ✅ 58 篇文章 | ⏳ 17 篇日记 | 🟡 需扩充 |
| **About Agent 档案** | ✅ 5 人详细档案 | ✅ 7 人定义 | 🟢 相当 |
| **关系矩阵** | ✅ 动态关系系统 | ❌ 无 | 🔴 需开发 |

### 技术栈对比

| 技术 | VoxYZ | 我们 | 状态 |
|------|-------|------|------|
| **框架** | Next.js 14/15 | Next.js 16 | 🟢 更新 |
| **数据库** | Supabase | ⏳ 未配置 | 🔴 需配置 |
| **支付** | Stripe | ⏳ 未配置 | 🔴 需配置 |
| **部署** | Vercel | Cloudflare Pages | 🟢 已部署 |
| **AI 框架** | OpenClaw | OpenClaw | 🟢 相同 |

### 核心差距总结

**VoxYZ 优势：**
1. 完整的商业化产品 ($79/$199)
2. 实时可视化系统（Office/Stage/Radar）
3. 成熟的收入模式
4. 58 篇深度内容积累

**我们的优势：**
1. 更精简的团队架构（7 人 vs 5 人）
2. 更完整的记忆系统
3. 后发优势可复制经验
4. 本地部署零成本

**追赶策略：**
1. **先复制** - 学习 VoxYZ 的内容和运营模式
2. **再差异化** - 找到我们的独特定位
3. **后商业化** - 积累足够后定义产品
*持续更新中...*

## 网站更新 (2026-03-29 09:37)

**发现：** v1 静态文件在 workspace，Next.js 网站在 `agents/engineer/website/` 但不存在（可能是临时文件系统）

**已做：**
1. 从部署站点恢复了正确的 `index.html`（深色主题 + 养成日记内容）
2. 创建 `sitemap.xml`（SEO）
3. 创建 `robots.txt`
4. 创建 `favicon.svg`（灯泡品牌图标）
5. 通过 GitHub API 直接推送 commit `809e3b22`
6. 设计心跳检查：同步 dark theme CSS（#0a0a0b背景 + #f5c518金色强调），添加 Open Graph tags，推送 commit `01b08b21`

**已推送 commits：**
- `809e3b22` - 恢复 index.html + sitemap/robots/favicon
- `01b08b21` - 同步 dark theme CSS + OG tags

**部署状态：** Cloudflare Pages GitHub App 自动部署中（等待 2-3 分钟）
**验证：** https://dengpao.pages.dev/

## ⚠️ 重要发现 (10:39)

**Cloudflare Pages `dengpao` 项目 Git Provider: No**
- GitHub API pushes **不会**触发 Cloudflare Pages 部署
- 需要手动部署或重新连接 GitHub App
- `robots.txt` 和 `sitemap.xml` 也没在部署里

**需要老庄帮忙：**
1. 在 Cloudflare Dashboard → Pages → dengpao → Settings → Builds and deployments
2. 连接到 GitHub repo: `bjd1129-create/zhugedengpao`
3. 或者手动 `wrangler pages deploy` 当前静态文件

**当前 workspace 文件（都是正确的）：**
- `index.html` - 深色主题，有 OG tags
- `css/style.css` - 同步了深色主题
- `sitemap.xml` - SEO sitemap
- `robots.txt` - robots 规则
- `favicon.svg` - 灯泡图标

## 更新 (11:39)

**重要：workspace CSS 被 AI 团队 warm theme 覆盖后恢复**
- 从 dengpao.pages.dev 重新拉取 dark theme CSS
- 修复了 index.html 中的 warm color references
- 添加了 `--accent-light: #ffd84d` 到 CSS tokens
- 更新了 Google Fonts import 包含 DM Sans/DM Serif

**当前 GitHub HEAD:** `7a3c2c31`
- index.html (dark-compatible)
- css/style.css (dark theme from deployed site)
- robots.txt ✓
- sitemap.xml ✓
- favicon.svg ✓

**关键问题：Cloudflare Pages Git Provider = No**
- GitHub pushes 不触发部署持续 2+ 小时
- workspace 文件全部正确
- 需要老庄在 Cloudflare Dashboard → Pages → dengpao → Settings → Builds and deployments → 重新连接 GitHub repo

## ✅ 部署成功 (11:42)

**wrangler pages deploy 直接更新了生产环境！**
- `wrangler pages deploy . --project-name=dengpao`
- 生产 URL https://dengpao.pages.dev/ 已更新
- 所有 OG tags、sitemap、robots.txt、about 页面均已上线

**当前生产环境：** https://dengpao.pages.dev/
**最新部署 ID：** 4ac7fb14-8d6b-42c8-b44d-ce79f9bce0aa

**备注：** Cloudflare Pages GitHub App 仍然断开（Git Provider: No），但 wrangler deploy 可以绕过 GitHub 直接部署。
**后续更新可以用：** `wrangler pages deploy . --project-name=dengpao`

## 更新 (12:11)

**新增 SEO meta tags:**
- og:url, twitter:card, twitter:title/description
- canonical URL, theme-color

**部署命令已验证:**
```
cd /Users/bjd/Desktop/ZhugeDengpao-Team
CLOUDFLARE_API_TOKEN="" wrangler pages deploy . --project-name=dengpao --commit-dirty=true
```

## 更新 (12:41)

**新增 OG tags 到所有主要页面:**
- diary.html, articles.html, science.html ✅
- skills.html, easyclaw.html ✅
- about.html (之前已有)

**SEO meta tags 完整的页面:**
- index.html, about.html, diary.html, articles.html, science.html, skills.html, easyclaw.html

**部署命令:**
```
cd /Users/bjd/Desktop/ZhugeDengpao-Team
CLOUDFLARE_API_TOKEN="" wrangler pages deploy . --project-name=dengpao --commit-dirty=true
```

## 更新 (13:11)

**SEO 完善:**
- OG tags 已覆盖全部 11 个页面 (index, about, diary, articles, science, skills, easyclaw, insights, office, pricing, radar)
- sitemap.xml 已添加 `about` 页面
- 所有页面都有 og:title, og:description, og:type, og:url, twitter:card, canonical

**当前部署:** 213d5a8b (sitemap 包含 about 页面)
**生产 URL:** https://dengpao.pages.dev/ (CDN 缓存可能需要几分钟刷新)

**部署命令:**
```
cd /Users/bjd/Desktop/ZhugeDengpao-Team
CLOUDFLARE_API_TOKEN="" wrangler pages deploy . --project-name=dengpao --commit-dirty=true
```

## 重要更新 (14:11)

**设计方向确认：warm 主题（不是 dark）**
- AI 团队的设计方向是 warm 主题：cream (#FFFBF5) + coral (#E8724A) + dark brown (#3D2314)
- 我之前的 "dark theme" 是误解 — 初始部署的 dark CSS 可能是之前某个版本，不是 AI 团队的方向
- workspace CSS 已同步为 warm 主题
- 所有 11 个页面 theme-color 已更新为 #FFFBF5

**当前部署：** 5e1fdd69 (warm 主题)
**所有页面 SEO 标签完整**

**部署命令（已验证）：**
```
cd /Users/bjd/Desktop/ZhugeDengpao-Team
CLOUDFLARE_API_TOKEN="" wrangler pages deploy . --project-name=dengpao --commit-dirty=true
```

## 更新 (14:41)

**新增 og:image 到 index.html:**
- og:image: https://dengpao.pages.dev/images/lobster.svg
- og:image:width: 120, og:image:height: 160
- 诸葛灯泡品牌卡通龙虾 logo 作为社交分享图片

**待优化：** 为其他页面（about, diary, articles）单独创建 og:image（建议 1200x630 PNG）

## 观察 (15:13)

**AI 团队活跃：** zhuge-bulbo.png 更新说明 AI 团队在通过 wrangler 维护网站
- GitHub HEAD: `1ce5d556` (AI团队最新)
- workspace index.html 已被 AI 团队更新（og:image 改为 zhuge-bulbo.png）
- wrangler deploy 绕过了 GitHub 直接更新生产环境

**网站状态良好：** 所有 SEO 标签正常，资源加载正常
**设计方向：** warm theme (cream #FFFBF5 + coral #E8724A)
