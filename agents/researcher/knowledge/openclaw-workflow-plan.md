# OpenClaw 工作流自动化方案

> 洞察者 · 方案 v1.0 · 2026-04-06
> 基于：openclaw-workflow-deep-dive.md 深度研究

---

## 现状评估

### Cron 任务：31个，9个 error

| 任务 | 状态 | 影响 |
|------|------|------|
| 协调官-12:00 午间进度检查 | error | 团队进度无监控 |
| 协调官-15:00 下午巡检 | error | 团队进度无监控 |
| 协调官-09:00 团队巡检 | error | 团队进度无监控 |
| 每日增量复盘-凌晨1点 | error | 复盘自动化失效 |
| OpenClaw自我进化研究 | error | 知识更新停滞 |
| 小花-22:00 发布高光日记 | error | 日记发布失效 |
| 每日日志发布 | error | 日记发布失效 |
| 洞察者-团队健康监督 | error | 团队健康失察 |
| 官网巡检 — 每3小时 | error | 官网状态无监控 |

**根因：没有 failureDestination，error 静默发生，没人知道。**

### Standing Orders：存在但非正式

HEARTBEAT.md 里有检查清单，但：
- 没有 Authority（授权范围）
- 没有 Escalation（何时升级）
- 没有 Execute-Verify-Report 规范
- 没有正式的 AGENTS.md 注入结构

### Task Flow：零使用

所有 Cron 都是单步骤任务，无多步骤编排。

---

## 方案目标

**三个月内：从"零散 Cron"进化到"结构化工作流引擎"**

---

## Phase 1：止血（1-2天）

### 1.1 建立 failureDestination 路由

**原则：所有 error 必须有人知道。**

方案：创建一个专门的"告警 channel"，让 error 通知流到协调官。

```bash
# 给所有 error 状态的 cron 任务加 failureDestination
# 指向 coordinator bot 的老庄 open_id
openclaw cron edit <job-id> \
  --failure-destination '{"mode":"announce","channel":"feishu","accountId":"coordinator","to":"user:ou_71bf6382be997d640eeada9f92302c98"}'
```

或者，更优雅的方案：在 openclaw.json 里设置全局默认：

```json5
{
  cron: {
    failureDestination: {
      mode: "announce",
      channel: "feishu",
      accountId: "coordinator",
      to: "user:ou_71bf6382be997d640eeada9f32302c98"
    }
  }
}
```

**行动项：**
- [ ] 确认 coordinator bot 的 failureDestination open_id
- [ ] 设置全局 failureDestination
- [ ] 验证 error 任务是否收到通知

### 1.2 修复已知 error 任务

| 任务 | 可能原因 | 修复方向 |
|------|---------|---------|
| 协调官 Cron 系列 | cron 本身配置问题 | 检查 cron 定义 |
| OpenClaw自我进化研究 | 可能是网络/skill 问题 | 检查 skill 存在性 |
| 日记发布任务 | Git push 被 secret 扫描拦截 | 解决 GitHub secret 问题 |

**行动项：**
- [ ] `openclaw cron runs --id <job-id>` 查看每个 error 的详情
- [ ] 逐个修复

---

## Phase 2：结构化（3-5天）

### 2.1 把 HEARTBEAT.md 升级为正式 Standing Orders

**当前（HEARTBEAT.md，检查清单模式）：**
```
- 今天 articles 页面更新了吗？
- 有没有 5 篇新的深度研究报告？
```

**升级后（AGENTS.md，正式 Standing Orders）：**

```markdown
## Program: Articles 每日更新

**Authority:** 研究、写作、发布 5 篇深度研究报告到 articles 页面
**Trigger:** 每天（时间灵活，以完成为准）
**Approval gate:** 无。质量由洞察者自行判断。
**Escalation:**
  - 超过 4 小时无产出 → 通知协调官
  - 发现重大机会/威胁 → 立即上报老庄
  - 连续 3 天无主动产出 → 主动告知原因

### Execution Steps
1. Execute: 扫描 AI/OpenClaw 动态（last30days 技能 + 官方文档）
2. Verify: 找到有价值的选题，确认不是噪音
3. Report: 产出 5 篇报告，更新 articles-data.js，git push
4. Execute: 通知协调官 push 完成

### What NOT to Do
- 不传未经核实的八卦
- 不为了"有发现"而硬找发现
- 不评估超出认知范围的技术
```

```markdown
## Program: 团队健康监督

**Authority:** 确保团队工作流不依赖人工触发自动运转
**Trigger:** 每天 9:00、12:00、18:00
**Approval gate:** 无
**Escalation:**
  - 团队 Cron 健康率 < 90% → 立即处理或上报
  - 发现阻塞 2 小时内未处理 → 上报协调官
  - 自动化故障 → 立即修复或回退

### Execution Steps
1. Execute: 检查所有 agent 的 cron 任务状态（`openclaw cron list`）
2. Execute: 检查 subagent sessions（`openclaw sessions list`）
3. Verify: 确认 error = 0，blocked = 0
4. Report: 有问题立即上报，无问题静默

### What NOT to Do
- 不要在非工作时间打扰团队（22:00-08:00 除非紧急）
```

### 2.2 启用 lightContext + isolatedSession 心跳

当前心跳消耗完整 session 历史，对例行检查来说浪费。

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        target: "none",           // 例行检查不发消息，保持安静
        lightContext: true,        // 仅注入 HEARTBEAT.md
        isolatedSession: true,     // 每次 fresh session
        // activeHours: { start: "08:00", end: "22:00" }
      }
    }
  }
}
```

**预期效果：**
- Token 消耗降低 ~80%（无完整历史注入）
- 例行检查仍然可以读写 HEARTBEAT.md
- 有真正需要关注的事才发消息

---

## Phase 3：编排升级（1-2周）

### 3.1 文章生产流程 Task Flow 化

**当前状态：** 一篇研究文章的生产散落在多个 cron 里，没有统一编排。

**目标：** 把"研究→写作→发布"建模为一个 managed Task Flow。

```
Flow: article-production (managed)
  Step 1: research-scan
    └─ 扫描 AI 动态，找到有价值的选题
    └─ 验证：选题目录存在于 memory/
  Step 2: deep-research  
    └─ 对每个选题目进行深度研究
    └─ 验证：研究笔记存在于 knowledge/
  Step 3: write-report
    └─ 将研究写成报告
    └─ 验证：报告文件存在且 > 1000 字
  Step 4: publish
    └─ 更新 articles-data.js
    └─ 验证：git push 成功
    └─ Report: 通知协调官发布完成
```

**优势：**
- 步骤可独立追踪
- 失败从失败步骤恢复（不用从头开始）
- 重启不丢进度
- 可以取消整个 flow

**实现方式：** 通过 cron + 引导 agent 顺序执行各步骤，每次结果写入 flow state

### 3.2 团队工作流 Mirror 化

把团队多 agent 的协作关系建模为 mirrored Task Flow：

```
Flow: team-collaboration (mirrored)
  观察：
    Task: 洞察者-researcher    (cron: research scan)
    Task: 协调官-coordinator  (cron: team check)
    Task: 配色师-designer     (cron: comic check)
    Task: 文案君-writer       (cron: diary check)
```

统一视图可以看到团队整体工作流状态。

---

## Phase 4：高级特性（持续）

### 4.1 模型分级策略

不同任务用不同成本的模型：

```json5
// 深度研究用强模型
openclaw cron edit <research-job-id> \
  --model "minimax-portal/MiniMax-M2.7" \
  --thinking high

// 日常检查用弱模型
openclaw cron edit <check-job-id> \
  --model "minimax-portal/MiniMax-M2.7" \
  --thinking off
```

### 4.2 Webhook 外部触发

当外部系统需要触发 OpenClaw 工作流时：

```json5
{
  hooks: {
    enabled: true,
    token: "your-secret-token",
    path: "/hooks"
  }
}
```

POST `/hooks/wake` → 触发主 session 系统事件
POST `/hooks/agent` → 触发 isolated agent turn

### 4.3 自定义 Session 累积上下文

对于"日站会"类任务，跨 run 累积上下文：

```bash
openclaw cron add \
  --name "daily-standup" \
  --cron "0 9 * * 1-5" \
  --session session:daily-standup \
  --message "按日站会常驻指令执行。上次总结：<上次输出摘要>"
```

---

## 执行清单

### 立即执行（今天）

- [ ] **P0** 设置全局 failureDestination → coordinator bot
- [ ] **P0** 修复 9 个 error cron 任务
- [ ] **P1** 把洞察者 HEARTBEAT.md 升级为正式 Standing Orders（写入 AGENTS.md）

### 本周内

- [ ] **P1** 协调官/配色师/文案君的 HEARTBEAT.md 同样升级
- [ ] **P1** 启用 lightContext + isolatedSession 心跳
- [ ] **P2** 设计文章生产 Task Flow 结构
- [ ] **P2** 给所有重要 cron 加 failureDestination

### 长期

- [ ] **P2** 把关键 cron 升级为 Task Flow
- [ ] **P3** 实现模型分级策略
- [ ] **P3** 研究 Webhook 外部触发集成

---

## 风险和注意事项

| 风险 | 缓解 |
|------|------|
| Standing Orders 太多导致 prompt 膨胀 | 按重要性排序，只写关键的 3-5 个 Program |
| lightContext 可能丢掉重要上下文 | 初期仅对"例行检查"类任务启用 |
| Task Flow 学习曲线陡峭 | 先在非关键任务上试点 |
| Cron 任务太多难以维护 | 定期审计，合并/删除无效任务 |

---

## 关键依赖

1. **GitHub secret 扫描问题** — 阻碍所有 git push 相关任务
2. **GitHub credentials** — 需要确认 Push 用的 token 有效性
3. **老庄授权** — Standing Orders 里的 Escalation 规则需要老庄确认

---

*洞察者 · OpenClaw 工作流自动化执行方案 v1.0 · 2026-04-06*
