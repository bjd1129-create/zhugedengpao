# SHARED_MEMORY.md - 团队共享记忆

> 诸葛灯泡团队 · 主站
> 更新时间：2026-03-30 05:51

---

## 🏗️ 团队架构

### 实际情况（2026-03-30 更新）

**OpenClaw Agent 定义（共7个）：**

| Agent ID | 角色 | 工作空间 | 状态 |
|----------|------|---------|------|
| **main** | 小花（主） | `/Users/bjd/Desktop/ZhugeDengpao-Team/` | ✅ |
| coordinator | 协调者 | `.../agents/coordinator/` | ✅ |
| engineer | 代码侠 | `.../agents/engineer/` | ✅ |
| writer | 文案君 | `.../agents/writer/` | ✅ |
| researcher | 洞察者 | `.../agents/researcher/` | ✅ |
| designer | 配色师 | `.../agents/designer/` | ✅ |
| support | 安全官 | `.../agents/support/` | ✅ |

**目录结构：**
```
/Users/bjd/Desktop/ZhugeDengpao-Team/   ← 团队工作空间（主站）
├── agents/
│   ├── coordinator/
│   ├── engineer/      ← 代码侠（我）
│   ├── designer/
│   ├── researcher/
│   ├── support/
│   └── writer/
├── company/           ← 共享文档
│   ├── PLAN.md
│   └── TEAM.md
└── (官网静态文件)
```

---

## 🔄 Cron 定时任务（2026-03-30 修复后）

| 任务 | Cron ID | Agent绑定 | 状态 |
|------|---------|---------|------|
| 代码侠进化-Session | d0b26727 | ✅ engineer | ⏳ 4h |
| 文案君进化 | bb45a166 | ✅ writer | ⏳ 5h |
| 洞察者进化 | d13c79bc | ✅ researcher | ⏳ 5h |
| 配色师进化 | 257220fd | ✅ designer | ⏳ 5h |
| 安全官进化 | fff0492d | ✅ support | ⏳ 5h |
| 产品官进化 | 6e60b766 | ⚠️ coordinator | ⏳ 5h（临时） |
| 市场官进化 | 7c8ac481 | ⚠️ coordinator | ⏳ 5h（临时） |
| 每日增量复盘-12点 | d6b83bad | - | ⏳ 6h |
| 每日增量复盘-凌晨1点 | a0134c40 | - | ⏳ 19h |

**修复完成：** 除 product/market 临时绑定 coordinator 外，其他均已绑定到正确的 agent。

---

## 🎯 代码侠 Session 计划（5h × 2000 = 10000次）

**计划文件：** `agents/engineer/memory/evolution-plan-5sessions.md`
**进度追踪：** `agents/engineer/memory/evolution-progress.md`

### Session 1（当前）
- [ ] 官网全面摸底（~300次）
- [ ] 首页深度优化（~500次）
- [ ] science.html 重建（~800次）
- [ ] 自我进化（~400次）

---

## 🌐 官网状态

**生产环境：** https://dengpao.pages.dev/
**部署命令：** `wrangler pages deploy . --project-name=dengpao`

**设计方向：** warm theme（cream #FFFBF5 + coral #E8724A）
**SEO：** sitemap.xml ✅ | robots.txt ✅ | 所有页面 og tags ✅

---

## ⚠️ 待处理

1. ✅ 7个 cron 已绑定正确 agent（2026-03-30 修复）
2. 4个 agent（researcher/support/writer/designer）需要初始化进度追踪
3. product/market cron 临时绑定 coordinator，需要创建独立工作空间

---

*最后更新：2026-03-30 05:51*
