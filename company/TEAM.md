# 小花团队配置

## 实际情况（2026-03-30）

### Agent 定义（openclaw.json）

| Agent ID | 角色 | 工作空间 | 状态 |
|----------|------|---------|------|
| main | 小花（主） | ZhugeDengpao-Team/ | ✅ |
| coordinator | 协调者 | agents/coordinator/ | ✅ |
| engineer | 代码侠 | agents/engineer/ | ✅ 最活跃 |
| writer | 文案君 | agents/writer/ | ⚠️ 待激活 |
| researcher | 洞察者 | agents/researcher/ | ⚠️ 待激活 |
| designer | 配色师 | agents/designer/ | ⚠️ 待激活 |
| support | 安全官 | agents/support/ | ⚠️ 待激活 |

### 缺失
- **产品官** - 有 cron 无工作空间
- **市场官** - 有 cron 无工作空间

---

## 核心原则

1. ✅ 每个Agent只做自己负责的事
2. ✅ 不越界、不插手别人的领域
3. ✅ 需要协作时用 sessions_spawn
4. ✅ 决策快速，不等待

---

## 协作机制（sessions_spawn）

1. 主收到任务
2. 分析需要哪些Agent
3. spawn子Agent
4. 各Agent并行执行
5. 主整合结果

---

## ⚠️ 待修复

- 7个 cron 需要绑定正确的 agent（目前只有 engineer 正确）
- 4个 agent 需要初始化进度追踪

---

*更新时间：2026-03-30 05:51*
