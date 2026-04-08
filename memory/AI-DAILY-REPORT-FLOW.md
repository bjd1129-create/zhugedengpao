# AI 日报流程 — 小花负责

**负责人**: 小花（决策者）
**频率**: 每日 08:00
**输出**: `memory/ai-daily-reports/ai-daily-YYYY-MM-DD.md`

---

## 📰 5 个核心数据源

| # | 来源 | 类型 | URL |
|---|------|------|-----|
| 1 | **Anthropic Blog** | 技术 | https://www.anthropic.com/news |
| 2 | **OpenClaw GitHub** | 工具 | https://github.com/openclaw/openclaw |
| 3 | **The Batch (DeepLearning.AI)** | 周报 | https://www.deeplearning.ai/the-batch/ |
| 4 | **Simon Willison** | 实践 | https://simonwillison.net/ |
| 5 | **Hacker News AI** | 社区 | https://news.ycombinator.com/front?query=AI |

---

## 📝 报告模板

```markdown
# AI 日报 — YYYY-MM-DD

**生成时间**: HH:MM
**负责人**: 小花

---

## 1️⃣ [来源名称] 标题

**链接**: URL

**摘要**: 
200-300 字核心内容

**关键洞察**: 
- 洞察 1
- 洞察 2

**对小花团队的意义**: 
- 应用建议 1
- 应用建议 2

---

## 2️⃣ [来源名称] 标题
...

---

## 3️⃣ [来源名称] 标题
...

---

## 4️⃣ [来源名称] 标题
...

---

## 5️⃣ [来源名称] 标题
...

---

## 🦞 小花今日分析

### 整体趋势
今日 5 篇报告反映的 AI 领域大趋势

### 团队行动建议
- [ ] 行动项 1
- [ ] 行动项 2
- [ ] 行动项 3

### 记忆写入
- 值得写入 MEMORY.md 的洞察：...
- 值得写入 AGENTS.md 的最佳实践：...

---

**标签**: #AI 日报 #YYYY-Www
```

---

## ⚙️ 执行方式

### 方式 A: 手动执行（初期）
每天 08:00 我自己醒来时执行：
```
/ai_daily_report
```

### 方式 B: Cron 自动执行（稳定后）
配置每天 08:00 自动触发

---

## 📁 文件结构

```
memory/
└── ai-daily-reports/
    ├── ai-daily-2026-04-09.md
    ├── ai-daily-2026-04-10.md
    └── ...
```

---

## 🔗 与记忆系统集成

**每日**:
- 报告写入 `memory/ai-daily-reports/`
- 重要洞察写入 `memory/YYYY-MM-DD.md`

**每周**:
- 周汇总写入 `MEMORY.md`
- 团队进化建议写入 `AGENTS.md`

---

**最后更新**: 2026-04-08 20:50 | 小花 🦞
