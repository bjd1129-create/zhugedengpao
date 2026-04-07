# OpenClaw 自动化工作流引擎：深度研究报告

> 洞察者 · 深度研究 · 2026-04-06
> 来源：docs.openclaw.ai 全部官方自动化文档（cron-jobs / tasks / taskflow / standing-orders / hooks / heartbeat / automation-index）
> ⚠️ 本报告基于 2026-04-06 可访问文档，v2026.4.2 changelog 无法抓取（网络限制）

---

## 核心命题

**OpenClaw 不是一个 AI 聊天工具。它是一个"Agent 操作系统"——完整的工作流引擎，覆盖从定时调度到多步骤编排的全部层次。**

这不是功能堆砌。这是一个从"每次对话独立理解上下文"到"持久化工作流状态 + 有边界的主动执行"的根本转变。

---

## 一、全景决策图

官方文档给出了清晰的决策树：

```
需要做什么？
│
├─ 调度工作？ ──────────────────────┐
│   ├─ 精确时间？→ Cron             │
│   └─ 灵活时间？→ Heartbeat        │
│                                     │
├─ 追踪 detached work？ ────────────→ Background Tasks
│                                     │
├─ 多步骤流程编排？ ────────────────→ Task Flow
│                                     │
├─ 响应生命周期事件？ ──────────────→ Hooks
│                                     │
└─ 授予永久执行权限？ ───────────────→ Standing Orders
```

**何时用什么的精确指南：**

| 场景 | 推荐 | 原因 |
|------|------|------|
| 每天 9:00 发报告 | Cron | 精确时间 + 隔离执行 |
| 20 分钟后提醒 | Cron（--at）| 精确一次性 |
| 每周深度分析 | Cron | 独立任务 + 可换模型 |
| 每 30 分钟检查收件箱 | Heartbeat | 批量检查 + 上下文感知 |
| 监控日历临近事件 | Heartbeat | 自然周期性感知 |
| 查看 subagent/ACP 运行状态 | Background Tasks | 任务总账追踪 |
| 审计运行记录 | Background Tasks | `openclaw tasks audit` |
| 多步骤研究→总结 | Task Flow | 持久化编排 + 版本追踪 |
| Session reset 时运行脚本 | Hooks | 事件驱动 |
| 每次工具调用拦截 | Hooks | 按事件类型过滤 |
| 回复前检查合规性 | Standing Orders | 每次 session 自动注入 |

---

## 二、第一层：Cron（精确调度）

### 核心定位
Cron 是 Gateway 内置的调度器。**运行在 Gateway 进程内（不在模型内）**，任务持久化在 `~/.openclaw/cron/jobs.json`，重启不丢。

### 调度类型

| 类型 | CLI 标志 | 说明 |
|------|----------|------|
| `at` | `--at` | 一次性（ISO 8601 或相对如 `20m`）|
| `every` | `--every` | 固定间隔 |
| `cron` | `--cron` | 5/6 字段 cron 表达式 |

**关键细节：**
- 重复性的"整点"表达式自动加上最多 5 分钟的随机偏移，减少负载峰值
- 想精确？加 `--exact` 或 `--stagger 30s`

### 执行风格（四种）

```bash
# Main session：下次心跳时运行，适合提醒和系统事件
openclaw cron add \
  --name "Calendar check" \
  --at "20m" \
  --session main \
  --system-event "Next heartbeat: check calendar." \
  --wake now

# Isolated：专用 cron:<jobId> session，适合报告和后台任务
openclaw cron add \
  --name "Morning brief" \
  --cron "0 7 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Summarize overnight updates." \
  --announce \
  --channel slack \
  --to "channel:C1234567890"

# Current session：创建时绑定，适合上下文感知的循环工作
openclaw cron add \
  --session current \
  --message "Review ongoing tasks and update status."

# Custom session：session:xxx，跨 run 持久化上下文，适合日站会等
openclaw cron add \
  --session session:daily-standup \
  --message "Run daily standup per standing orders."
```

### 交付机制（三种）

| 模式 | 行为 |
|------|------|
| `announce` | 推送摘要到目标 channel（isolated 的默认值）|
| `webhook` | POST 完成事件 payload 到 URL |
| `none` | 内部，不交付 |

**重要新行为（v2026.4.x）：**
- Cron runner 拥有最终交付路径，Agent 被引导返回纯文本摘要
- 如果原始任务明确说要发给某个外部收件人，Agent 在输出里注明，而不是直接发送
- 失败通知走独立路由：`cron.failureDestination` 全局默认 → `job.delivery.failureDestination` per-job 覆盖

### 隔离运行中的模型选择（精确优先级）

```
1. Gmail hook model override（来自 Gmail 触发且允许覆盖时）
2. Per-job payload model
3. 存储的 cron session model override
4. Agent/default 模型选择
```

**关键：** `--model` 改变任务的选定模型。如果该模型不允许，cron 警告并退回 job 的 agent/default 选择。plain model override 不再把 agent primary 当作隐藏的额外重试目标。

### 重试机制

```json5
{
  cron: {
    retry: {
      maxAttempts: 3,
      backoffMs: [60000, 120000, 300000],  // 指数退避：1min → 2min → 5min
      retryOn: ["rate_limit", "overloaded", "network", "server_error"],
    }
  }
}
```

- **一次性任务**：瞬态错误（rate limit/overload/network/server error）最多重试 3 次
- **重复任务**：指数退避（30s → 60m），下次成功运行后重置

---

## 三、第二层：Background Tasks（活动账本）

### 核心定位
Tasks 是**记录，不是调度器**。它们追踪所有"detached work"：ACP runs、subagent spawns、isolated cron executions、CLI 操作。

**关键原则：**
- Heartbeat turns **不**创建 task 记录
- 正常交互式聊天 turns **不**创建 task 记录
- 所有 cron 执行、ACP spawns、subagent spawns、CLI agent 命令**都**创建 task 记录

### 谁创建什么

| 来源 | 运行时类型 | 创建时机 | 默认通知策略 |
|------|-----------|---------|------------|
| ACP 后台运行 | `acp` | spawn child ACP session 时 | `done_only` |
| Subagent 编排 | `subagent` | sessions_spawn 时 | `done_only` |
| Cron jobs（全类型）| `cron` | 每次 cron 执行（main-session 和 isolated）| `silent` |
| CLI 操作 | `cli` | 通过 gateway 运行的 `openclaw agent` 命令 | `silent` |

### 生命周期状态机

```
queued → running → succeeded
                   ↓
              failed
                   ↓
              timed_out
                   ↓
              cancelled
                   ↓
              lost（5分钟宽限期后 backing 状态消失）
```

**`lost` 的精确语义（runtime-aware）：**
- ACP tasks：backing ACP child session 元数据消失
- Subagent tasks：backing child session 从 target agent store 消失
- Cron tasks：cron runtime 不再把 job 标记为活跃
- CLI tasks：chat-backed CLI tasks 用 live run context，不是 chat session row

### 交付和通知

**两种路径：**
1. **直接交付**：task 有 channel target（requesterOrigin）时，直接发到 channel
2. **Session 队列交付**：直接交付失败或无 origin 时，作为系统事件排入 requester session

**推送驱动的设计：**
- detached work 完成后可以直接通知或唤醒 requester session/heartbeat
- 状态轮询通常是错误的做法

**通知策略：**
| 策略 | 内容 |
|------|------|
| `done_only`（默认）| 仅终态 |
| `state_changes` | 每次状态转换和进度更新 |
| `silent` | 什么都不发 |

### 审计命令

```bash
openclaw tasks audit
```

自动发现以下问题：

| 发现 | 严重程度 | 触发条件 |
|------|---------|---------|
| `stale_queued` | warn | queued 超过 10 分钟 |
| `stale_running` | error | running 超过 30 分钟 |
| `lost` | error | runtime backing 状态消失 |
| `delivery_failed` | warn | 交付失败且通知策略非 `silent` |
| `missing_cleanup` | warn | 终态 task 无 cleanup timestamp |
| `inconsistent_timestamps` | warn | 时间线违规（如 ended 在 started 之前）|

### 存储和维护

- 存储在 SQLite：`$OPENCLAW_STATE_DIR/tasks/runs.sqlite`
- Registry 在 gateway 启动时加载到内存，并同步写入 SQLite 持久化
- **自动维护（每 60 秒）：** reconciliation → cleanup stamping → pruning
- **保留期：7 天**，自动清理

---

## 三（续）、Heartbeat（近似周期）

### 与 Cron 的根本区别

| 维度 | Cron | Heartbeat |
|------|------|-----------|
| 时机 | 精确（cron 表达式）| 近似（默认 ~30 分钟）|
| Session context | Fresh（isolated）或 shared | 完整 main-session context |
| Task 记录 | 始终创建 | **从不创建** |
| 交付 | Channel / webhook / silent | 内联在 main session |
| 适用 | 精确报告、提醒 | 收件箱检查、日历、通知聚合 |

### 核心配置

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        target: "last",          // "none" | "last" | <channel id>
        directPolicy: "allow",   // "allow" | "block"
        lightContext: false,     // true: 仅注入 HEARTBEAT.md
        isolatedSession: false, // true: 每次 fresh session（无对话历史）
        // activeHours: { start: "08:00", end: "24:00" }
        // includeReasoning: true
      }
    }
  }
}
```

### 响应契约

- 没什么需要关注的？回复 **`HEARTBEAT_OK`**（自动剥离，不交付）
- 有警报？**只返回警报文本**，不要包含 HEARTBEAT_OK
- `HEARTBEAT_OK` 必须在回复**开头或结尾**，才被识别

### lightContext + isolatedSession 组合

```
每次 Heartbeat = fresh session（无对话历史）+ 仅注入 HEARTBEAT.md
= 最小 token 消耗
+ 依然可以读写 HEARTBEAT.md，执行检查清单
```

这对成本敏感的场景极有价值。

---

## 四、第三层：Task Flow（多步骤编排）

### 核心定位
Task Flow 是**任务编排的持久化基础设施**，位于 Background Tasks 之上。

### 何时用 Task Flow

| 场景 | 用什么 |
|------|--------|
| 单个后台作业 | Plain task |
| 多步骤管道（A→B→C）| Task Flow（managed）|
| 观察外部创建的任务 | Task Flow（mirrored）|
| 一次性提醒 | Cron job |

### Managed 模式

Task Flow 端到端拥有生命周期：
```
Flow: weekly-report
  Step 1: gather-data     → task created → succeeded
  Step 2: generate-report → task created → succeeded
  Step 3: deliver         → task created → running
```

适合：Agent 自己驱动的工作流，A→B→C 顺序执行。

### Mirrored 模式

Task Flow 观察外部创建的任务并同步 flow 状态，但不接管任务创建：
```
Flow: morning-ops
  Task: cron-email-check  → external → succeeded
  Task: cron-calendar-check → external → running
  Task: cron-slack-status → external → queued
```

适合：cron jobs、CLI 命令等外部来源的任务，Task Flow 提供统一视图。

### 持久化和修订追踪

- 每个 flow 持久化自己的状态和修订版本
- Gateway 重启不丢进度
- 修订追踪支持并发冲突检测

### Cancel 行为（sticky cancel intent）

```bash
openclaw tasks flow cancel <lookup>
```

设置 **sticky cancel intent**：当前任务被取消，新步骤不再启动。cancel 意图在重启后依然保持——cancel 的 flow 保持 cancel 状态，直到所有子任务终止。

### CLI 命令

```bash
openclaw tasks flow list              # 列出活跃和最近的 flows
openclaw tasks flow show <lookup>    # 查看详情
openclaw tasks flow cancel <lookup>  # 取消 + 取消所有活跃任务
```

---

## 五、第四层：Standing Orders（永久执行授权）

### 核心定位
Standing orders 授予 Agent **永久运营权限**——不需要每次吩咐，Agent 在定义的边界内主动执行。

### 没有 vs 有 Standing Orders

| 没有 | 有 |
|------|-----|
| 必须每次吩咐 Agent | Agent 在定义边界内自主执行 |
| Agent 在请求之间空闲 | 例行工作按时执行，不依赖提醒 |
| Routine 工作被遗忘或延迟 | 你只在异常和审批时介入 |
| 你成为瓶颈 | Agent 充分利用空闲时间 |

### 最小执行单元：Execute-Verify-Report

每个 Standing Order 任务必须遵循：

```
1. Execute — 做实际工作（不是只说"我会做"）
2. Verify — 确认结果正确（文件存在？消息发送？数据解析？）
3. Report — 告诉 owner 做了什么、验证了什么
```

**规则：**
- "我会做"不是执行。做了，然后报告。
- "完成"没有验证不算数。证明它。
- 执行失败：换方法重试一次。
- 仍然失败：报告失败并附诊断。永远不要静默失败。
- 永远不要无限重试——最多 3 次，然后升级。

### 结构模板

```markdown
## Program: [名称]

**Authority:** [Agent 被授权做什么]
**Trigger:** [何时执行：schedule/event/condition]
**Approval gate:** [什么需要人工签字前]
**Escalation:** [何时停止并寻求帮助]

### Execution Steps
1. ...
2. ...
3. ...

### What NOT to Do
- 不要做 X
- 不要做 Y

### Escalation Rules
- 情况 A → 立即升级
- 情况 B → 在报告中标记
```

### 与 Cron 的协作

```
Standing Order: "你拥有每日 inbox triage 的所有权"
     ↓
Cron Job (每天 8 AM): "按常驻指令执行 inbox triage"
     ↓
Agent: 读取常驻指令 → 执行步骤 → 报告结果
```

Cron job prompt 应该**引用** Standing Order，而不是复制它。

### 多项目架构

可以为不同领域分别设置 Standing Orders：

```markdown
# Standing Orders

## Program 1: 内容运营（每周）
## Program 2: 监控告警（持续）
## Program 3: 数据处理（事件触发 + 每月周期）

## 全局升级规则
[所有项目通用]
```

每个项目有自己的触发节奏、审批门槛和边界。

---

## 六、第五层：Hooks（事件驱动）

### 核心定位
Hooks 是在 Gateway 内部运行的小脚本，当特定事件发生时触发。

### 两种 Hook 类型

| 类型 | 说明 |
|------|------|
| **Internal hooks** | Gateway 内部，Agent 事件触发（`/new`、`/reset`、lifecycle）|
| **Webhooks** | 外部 HTTP 端点，让其他系统触发 OpenClaw 内部工作 |

### 事件类型

| 事件 | 触发时机 |
|------|---------|
| `command:new` | `/new` 命令发出 |
| `command:reset` | `/reset` 命令发出 |
| `command:stop` | `/stop` 命令发出 |
| `command` | 任何命令事件（通用监听器）|
| `session:compact:before` | compaction 总结历史之前 |
| `session:compact:after` | compaction 完成之后 |
| `session:patch` | Session 属性被修改时 |
| `agent:bootstrap` | workspace bootstrap 文件注入之前 |
| `gateway:startup` | channels 启动 + hooks 加载之后 |
| `message:received` | 任何 channel 的入站消息 |
| `message:transcribed` | 音频转录完成 |
| `message:preprocessed` | 所有 media 和 link 理解完成后 |
| `message:sent` | 出站消息交付 |

### Hook 结构

```
my-hook/
├── HOOK.md          # 元数据 + 文档
└── handler.ts       # 处理器实现
```

### HOOK.md 格式

```markdown
---
name: my-hook
description: "Short description"
metadata:
  openclaw:
    emoji: "🔗"
    events: ["command:new"]
    requires:
      bins: ["node"]
---

# My Hook

Detailed documentation.
```

### 处理器实现

```typescript
const handler = async (event) => {
  if (event.type !== "command" || event.action !== "new") return;

  console.log(`[my-hook] New command triggered`);
  // 逻辑

  // 可选：向用户发消息
  event.messages.push("Hook executed!");
};

export default handler;
```

### 内置 Hooks

| Hook | 事件 | 功能 |
|------|------|------|
| `session-memory` | `command:new`, `command:reset` | 保存 session 上下文到 `memory/` |
| `bootstrap-extra-files` | `agent:bootstrap` | 从 glob patterns 注入额外 bootstrap 文件 |
| `command-logger` | `command` | 记录所有命令到 `~/.openclaw/logs/commands.log` |
| `boot-md` | `gateway:startup` | Gateway 启动时运行 `BOOT.md` |

### 最佳实践

- **保持处理器快速。** Hooks 在命令处理期间运行。重型工作用 `void processInBackground(event)` 异步处理。
- **优雅处理错误。** 用 try/catch 包装危险操作，不要 throw，这样其他 handler 还能运行。
- **早期过滤事件。** 不相关的事件类型直接返回。
- **使用具体事件键。** 用 `"command:new"` 而不是 `"command"`，减少开销。

---

## 七、集成全景：六层如何协同

```
┌────────────────────────────────────────────────────────────────┐
│                    Standing Orders（授权层）                    │
│  永久执行授权 + Execute-Verify-Report 规范 + 升级规则          │
├────────────────────────────────────────────────────────────────┤
│                          Hooks（事件层）                        │
│  gateway:startup / command:* / message:* / session:compact:*   │
├────────────────────────────────────────────────────────────────┤
│                    Cron（精确定时层）                          │
│  at / every / cron 表达式 ── 触发 Standing Orders             │
├────────────────────────────────────────────────────────────────┤
│                   Heartbeat（近似周期层）                      │
│  ~30min batch ── 检查收件箱/日历/通知 ── lightContext 模式     │
├────────────────────────────────────────────────────────────────┤
│                    Task Flow（编排层）                          │
│  Managed: A→B→C 多步骤流程，持久化状态 + 修订追踪              │
│  Mirrored: 观察外部任务并同步状态                              │
├────────────────────────────────────────────────────────────────┤
│                    Background Tasks（账本层）                   │
│  所有 detached work 的活动账本 ── queued/running/succeeded     │
└────────────────────────────────────────────────────────────────┘
```

**一个具体工作流如何流经所有层：**

```
用户定义 Standing Order: "每周五生成运营报告"

     ↓

Cron 触发（每周五 4 PM）
  --session isolated
  --message "按常驻指令执行每周报告生成"

     ↓

Agent 执行：
  1. [Standing Orders] 读取 "每周报告" 程序定义
  2. [Execute-Verify-Report] 拉取数据
  3. [Execute-Verify-Report] 生成报告
  4. [Execute-Verify-Report] 交付摘要

     ↓

Background Tasks 记录整个过程：
  - cron 任务创建 → running → succeeded
  - 每个步骤是 flow 中的一个子任务

     ↓

Task Flow (Managed) 编排步骤：
  Step 1: gather-data → succeeded
  Step 2: generate → succeeded
  Step 3: deliver → succeeded

     ↓

Hook 触发：
  session-memory: 保存这次执行为 memory 日记
  command-logger: 记录这次命令到日志

     ↓

交付：
  - 摘要发到 configured channel（announce）
  - 失败 → 通知 failureDestination
```

---

## 八、技术细节：Cron + Task Flow 的深层机制

### 模型选择在 Isolated Cron 中的精确行为

**v2026.4.x 变更（重要）：**

旧行为：plain `--model` override 会把 agent primary 当作隐藏的额外重试目标。

新行为：
1. 模型选择严格按优先级来，不再隐式 append agent primary
2. 如果请求的模型不允许，cron 警告 + 退回 job 的 agent/default 选择
3. 已配置的 fallback chains 仍然适用
4. 模型切换时（live switch）：cron 重试用切换后的 provider/model + 持久化该选择后再重试
5. 最多 3 次（初始尝试 + 2 次切换重试），之后 abort

### Task Flow 的 Runtime-Aware Cancel

**cancel 不是立即终止：**

```
用户执行 cancel
     ↓
设置 sticky cancel intent（持久化）
     ↓
当前活跃任务收到 cancel 信号
     ↓
新步骤不再启动
     ↓
即使 gateway 重启，cancel 意图仍然保持
     ↓
所有子任务终止后，flow 标记为 cancelled
```

### Isolated Cron 的 Descendant 感知

```
Agent 生成中间文字（"on it", "pulling everything together"）
     ↓
如果有 descendant subagent 仍在运行：
  → 抑制这个中间 parent update
  → 等待 descendant 最终输出
  → 优先交付 descendant 输出
     ↓
如果无 descendant 或 descendant 超时：
  → 重新 prompt 一次要实际结果
  → 然后交付
```

这是防止"占位回复"污染最终输出的关键机制。

---

## 九、对我们团队的价值

### 我们目前用到了什么

我们已有的配置：
- ✅ **Cron** — 定时任务（文章推送、八卦更新、团队检查）
- ✅ **Standing Orders** — HEARTBEAT.md 里定义的心跳检查清单
- ✅ **Background Tasks** — 所有后台运行（cron/subagent）都有记录
- ✅ **Hooks** — session-memory、command-logger 已启用

### 我们还没用到的

| 功能 | 当前状态 | 价值 |
|------|---------|------|
| **Task Flow** | 未使用 | 把"研究→写作→发布"建模为 managed flow，步骤可追踪、重启可恢复 |
| **Mirrored Task Flow** | 未使用 | 把团队多 Agent 工作流统一视图 |
| **Heartbeat lightContext** | 未使用 | 把心跳 token 消耗降到最低 |
| **Isolated Cron + model 切换** | 未使用 | 深度分析用强模型，日常用弱模型，节省成本 |
| **Cron failureDestination** | 未使用 | 把失败通知发到专门的 error channel |
| **Custom session（session:xxx）** | 未使用 | 日站会等需要跨 run 累积上下文的工作 |

### 立即可行动的方向

**1. 建模我们的文章生产流程为 Task Flow**

```
Flow: article-production
  Step 1: research    → managed
  Step 2: write       → managed
  Step 3: publish     → managed
  Step 4: push-git    → managed
```

每步骤可独立追踪，失败从该步骤恢复而非从头开始。

**2. 给 Cron 任务加 failureDestination**

目前失败没有通知渠道。建议把所有 cron 的 failureDestination 指向协调官（coordinator bot）。

**3. 把 Standing Orders 从隐式变为显式**

把 HEARTBEAT.md 里的检查清单成变为正式的 Standing Orders，放在 AGENTS.md 里，有 Authority/Trigger/Approval gate/Escalation 完整结构。

**4. 启用 lightContext + isolatedSession 组合**

对于不需要历史上下文的例行检查（收件箱扫描、cron 健康检查），大幅降低 token 消耗。

---

## 十、架构判断：OpenClaw 正在建什么

### 这不是一个聊天工具

看这六层架构：
- **没有**六层可以做一个"更好的 ChatGPT"
- **有**六层才能做一个"可以替你工作的 AI Agent"

### 这是一个 Agent 操作系统

类比：
- Linux = 进程调度 + 文件系统 + 网络堆栈 → 程序运行其上
- OpenClaw = Cron（时序调度）+ Tasks（工作追踪）+ Task Flow（流程编排）+ Standing Orders（授权管理）+ Hooks（事件响应）+ Heartbeat（状态感知）→ Agent 行动其上

### "推送优先"的设计哲学

整个系统是**推送驱动**，不是轮询驱动：
- 任务完成 → 直接通知或唤醒 session
- 失败 → 独立路由到 failureDestination
- Cancel → sticky intent，持久化后重启仍然保持

这意味着人类**不需要盯着系统**，系统会在需要关注时通知人。

### 风险和局限

**学习曲线：** 六层架构每层都有 CLI、配置、概念，理解全貌需要时间。

**调试复杂度：** 一个工作流可能跨越多个层（Standing Orders → Cron → Task Flow → Tasks → Hooks），出问题需要追踪整条链路。

**安全边界：** Agent 永久执行权限越大，prompt injection 的影响越大。Execute-Verify-Report 模式是缓解措施，但不是银弹。

**成熟度：** Task Flow 在 v2026.4.2 才"恢复"为核心功能，实际生产使用案例尚少。

---

## 附录：快速参考

### 决策速查

```
要精确时间？→ Cron（at / cron / every）
不需要精确时间？→ Heartbeat
要追踪 detached work？→ Tasks（`openclaw tasks list/audit`）
要编排多步骤？→ Task Flow（`openclaw tasks flow list/show/cancel`）
要给 Agent 永久授权？→ Standing Orders（写入 AGENTS.md）
要响应事件？→ Hooks（`openclaw hooks list/enable`）
```

### 关键命令

```bash
# Cron
openclaw cron list
openclaw cron runs --id <jobId> --limit 20
openclaw cron add --name "X" --cron "0 9 * * *" --session isolated --message "..."

# Tasks
openclaw tasks list
openclaw tasks audit
openclaw tasks show <lookup>

# Task Flow
openclaw tasks flow list
openclaw tasks flow show <lookup>
openclaw tasks flow cancel <lookup>

# Hooks
openclaw hooks list
openclaw hooks enable session-memory

# Heartbeat
openclaw system heartbeat last
```

---

## 参考文档

| 文档 | URL |
|------|-----|
| Automation 索引 | docs.openclaw.ai/automation |
| Cron Jobs | docs.openclaw.ai/automation/cron-jobs |
| Background Tasks | docs.openclaw.ai/automation/tasks |
| Task Flow | docs.openclaw.ai/automation/taskflow |
| Standing Orders | docs.openclaw.ai/automation/standing-orders |
| Hooks | docs.openclaw.ai/automation/hooks |
| Heartbeat | docs.openclaw.ai/gateway/heartbeat |

---

*洞察者 · 深度研究报告：OpenClaw 自动化工作流引擎 · 2026-04-06*
