# OpenClaw 官方知识库

> 洞察者整理 · 2026-04-06
> 来源：docs.openclaw.ai 官方文档

---

## 一、架构概览

### 核心定位
OpenClaw 是一个**自托管网关**，连接聊天应用与 AI 编码 Agent。运行在用户自己的机器上，桥接消息渠道和 AI 助手。

### 核心组件

```
Chat apps + plugins → Gateway → Pi agent / CLI / Web Control UI / macOS app / Mobile nodes
```

**关键特性：**
- 自托管：运行在自有硬件
- 多渠道：一个 Gateway 同时服务多个渠道（Discord、Feishu、iMessage、Signal、Slack、Telegram、WhatsApp 等）
- Agent 原生：为编码 Agent 设计，支持工具调用、会话、记忆、多 Agent 路由
- 开源：MIT 协议

### Gateway（守护进程）
- 维护 provider 连接
- 暴露类型化 WS API
- 验证入站帧
- 发出事件：`agent`、`chat`、`presence`、`health`、`heartbeat`、`cron`

### 运行时要求
- **Node 24**（推荐）或 Node 22.16+
- API key（Anthropic、OpenAI、Google 等）
- 约 5 分钟完成安装

---

## 二、核心概念

### Agent Loop（Agent 执行循环）

一个完整的 Agent 运行周期： intake → context assembly → model inference → tool execution → streaming replies → persistence

**执行流程：**
1. `agent` RPC 验证参数，解析 session，返回 `{ runId, acceptedAt }` 立即
2. `runEmbeddedPiAgent` 通过 per-session + global 队列序列化运行
3. 订阅 pi 事件并流式推送 assistant/tool deltas
4. 强制超时 → 中止运行

**队列机制：**
- per session key（session lane）序列化，防止工具/会话竞态
- messaging channels 可选择队列模式（collect/steer/followup）

### Hook 系统（拦截点）

**Gateway Hooks（内部钩子）：**
- `agent:bootstrap`：构建 bootstrap 文件时运行，可添加/删除 bootstrap 上下文
- 命令钩子：`/new`、`/reset`、`/stop` 等

**Plugin Hooks（插件钩子）：**
- `before_model_resolve`：session 前运行，可覆盖 provider/model
- `before_prompt_build`：session 加载后运行，注入 prependContext/systemPrompt
- `before_agent_reply`：inline actions 后、LLM 调用前，可返回合成回复或静默
- `agent_end`：完成后检查消息列表和运行元数据
- `before_compaction / after_compaction`：观察 compaction 周期
- `before_tool_call / after_tool_call`：拦截工具参数/结果
- `message_received / message_sending / message_sent`：入站/出站消息钩子
- `session_start / session_end`：会话生命周期边界
- `gateway_start / gateway_stop`：网关生命周期事件

### Multi-Agent（多 Agent）

**每个 Agent 完全隔离，拥有：**
- **Workspace**：文件、AGENTS.md/SOUL.md/USER.md、 persona 规则
- **State directory (agentDir)**：auth profiles、model registry、per-agent config
- **Session store**：聊天历史 + 路由状态

**路径映射：**
```
Config: ~/.openclaw/openclaw.json
State: ~/.openclaw
Workspace: ~/.openclaw/workspace（主 agent）或 ~/.openclaw/workspace-<agentId>
Agent dir: ~/.openclaw/agents/<agentId>/agent
Sessions: ~/.openclaw/agents/<agentId>/sessions
```

**默认单 Agent 模式：**
- `agentId` 默认为 `main`
- Sessions 为 `agent:main:<mainKey>`
- Workspace 为 `~/.openclaw/workspace`

---

## 三、Session 管理

### 消息路由规则

| 来源 | 行为 |
|------|------|
| Direct messages | 默认共享 session |
| Group chats | 每个 group 独立 session |
| Rooms/channels | 每个 room 独立 session |
| Cron jobs | 每次运行 fresh session |
| Webhooks | 每个 hook 独立 session |

### DM 隔离

**默认：** 所有 DM 共享一个 session（单人设置没问题，多人设置需开启隔离）

**隔离选项：**
```json5
{
  session: {
    dmScope: "per-channel-peer",  // 按 channel + sender 隔离（推荐）
  }
}
```
- `main`（默认）— 所有 DM 共享一个 session
- `per-peer` — 按 sender 隔离（跨 channel）
- `per-channel-peer` — 按 channel + sender 隔离（推荐）
- `per-account-channel-peer` — 按 account + channel + sender 隔离

### Session 生命周期

- **每日重置**（默认）：每天 4:00 AM 本地时间
- **空闲重置**（可选）：设置 `session.reset.idleMinutes`
- **手动重置**：输入 `/new` 或 `/reset`

### Session 维护

```json5
{
  session: {
    maintenance: {
      mode: "enforce",
      pruneAfter: "30d",
      maxEntries: 500,
    }
  }
}
```

---

## 四、Memory 系统

### 工作原理

Agent 通过**写入纯 Markdown 文件**来记忆：
- **MEMORY.md** — 长期记忆。持久化的事实、偏好、决策。每次 DM session 开头加载
- **memory/YYYY-MM-DD.md** — 每日笔记。运行上下文和观察。昨日和今日的笔记自动加载

### 记忆工具

- **memory_search**：语义搜索，找到相关内容
- **memory_get**：读取特定记忆文件或行范围

### 记忆后端

| 后端 | 特点 |
|------|------|
| **Builtin（默认）** | SQLite-based。开箱即用，支持向量相似度、关键词搜索、混合搜索 |
| **QMD** | 本地优先，支持 reranking、query expansion、可索引 workspace 外目录 |
| **Honcho** | AI 原生跨 session 记忆，支持用户建模、语义搜索、多 Agent 感知 |

### 自动记忆刷新

Compaction（压缩）前，OpenClaw 自动运行静默轮次，提醒 Agent 将重要上下文保存到记忆文件。

### Dreaming（实验性）

可选的后台整合过程：从每日文件 revisit 短期记忆，评分，只将符合条件的项 promote 到长期记忆。

---

## 五、Agent Workspace

### 默认位置
- `~/.openclaw/workspace`
- 或 `~/.openclaw/workspace-<profile>`（当 OPENCLAW_PROFILE 设置时）

### 标准文件

| 文件 | 用途 |
|------|------|
| AGENTS.md | 操作指令。每次 session 开头加载 |
| SOUL.md | Persona、语气、边界。每次 session 加载 |
| USER.md | 用户信息。每次 session 加载 |
| IDENTITY.md | Agent 名字、vibe、emoji |
| TOOLS.md | 本地工具和约定笔记 |
| HEARTBEAT.md | 心跳运行的检查清单 |
| BOOTSTRAP.md | 一次性首运行仪式 |
| memory/YYYY-MM-DD.md | 每日记忆日志 |
| MEMORY.md | 长期记忆 |

### 不在 Workspace 的文件（位于 ~/.openclaw/）

```
~/.openclaw/openclaw.json（配置）
~/.openclaw/agents/<agentId>/agent/auth-profiles.json（认证）
~/.openclaw/credentials/（渠道/provider 状态）
~/.openclaw/agents/<agentId>/sessions/（session 记录）
~/.openclaw/skills/（管理技能）
```

---

## 六、系统提示词

### Prompt 组装

OpenClaw 为每次 agent 运行构建自定义 system prompt：

**结构（紧凑固定段落）：**
1. **Tooling**：结构化工具来源提醒 + 运行时工具使用指导
2. **Safety**：简短 guardrail 提醒
3. **Skills**：如何按需加载技能说明
4. **OpenClaw Self-Update**：安全检查配置的指导
5. **Workspace**：工作目录
6. **Documentation**：本地文档路径
7. **Sandbox**（启用时）：沙箱路径和权限
8. **Current Date & Time**：时区和时间格式
9. **Runtime**：host、OS、node、model、repo root、thinking 级别

### Prompt 模式

| 模式 | 用途 |
|------|------|
| `full`（默认） | 完整段落 |
| `minimal` | 子 Agent：省略 Skills、Memory Recall、OpenClaw Self-Update 等 |
| `none` | 仅返回基础 identity 行 |

### Bootstrap 文件注入

以下文件注入到**每次 turn 的上下文窗口**：
- AGENTS.md、SOUL.md、TOOLS.md、IDENTITY.md、USER.md、HEARTBEAT.md、BOOTSTRAP.md（全新 workspace）、MEMORY.md

⚠️ **注意**：`memory/*.md` 每日文件**不**自动注入，通过 `memory_search` 和 `memory_get` 按需访问。

---

## 七、自动化（Cron）

### 基本命令

```bash
# 添加一次性提醒
openclaw cron add \
  --name "Reminder" \
  --at "2026-02-01T16:00:00Z" \
  --session main \
  --system-event "Reminder: check the cron docs draft" \
  --wake now \
  --delete-after-run

# 查看任务
openclaw cron list

# 查看运行历史
openclaw cron runs --id <job-id>
```

### 调度类型

| 类型 | CLI 标志 | 说明 |
|------|----------|------|
| `at` | `--at` | 一次性时间戳（ISO 8601 或相对如 `20m`）|
| `every` | `--every` | 固定间隔 |
| `cron` | `--cron` | 5 或 6 字段 cron 表达式 |

### 执行风格

| 风格 | --session 值 | 运行位置 | 适用场景 |
|------|-------------|----------|---------|
| Main session | `main` | 下一次心跳 | 提醒、系统事件 |
| Isolated | `isolated` | 专用 cron:<jobId> | 报告、后台任务 |
| Current session | `current` | 创建时绑定 | 上下文感知的循环工作 |
| Custom session | `session:custom-id` | 持久命名 session | 持续构建的工作流 |

### 交付选项

| 模式 | 行为 |
|------|------|
| `announce` | 交付摘要到目标 channel（isolated 默认）|
| `webhook` | POST 完成事件 payload 到 URL |
| `none` | 仅内部，无交付 |

---

## 八、Gateway 配置

### 快速配置

```json5
{
  channels: {
    defaults: {
      groupPolicy: "allowlist",  // open | allowlist | disabled
    },
    telegram: {
      botToken: "your-bot-token",
      dmPolicy: "pairing",  // pairing | allowlist | open | disabled
      allowFrom: ["tg:123456789"],
    },
    discord: {
      token: "your-bot-token",
      dmPolicy: "pairing",
    },
    feishu: {
      // Feishu 配置
    }
  },
  session: {
    dmScope: "per-channel-peer",
    maintenance: {
      mode: "enforce",
      pruneAfter: "30d",
      maxEntries: 500,
    }
  }
}
```

### 渠道 DM/Group 策略

**DM 策略：**
- `pairing`（默认）：未知发送者获得一次性配对码，所有者需批准
- `allowlist`：仅允许名单中的发送者
- `open`：允许所有入站 DM（需 `allowFrom: ["*"]`）
- `disabled`：忽略所有入站 DM

**Group 策略：**
- `allowlist`（默认）：仅允许名单中的 group
- `open`：绕过 group allowlist
- `disabled`：阻止所有 group/room 消息

---

## 九、工具生态

### 核心工具

- **exec**：运行 shell 命令
- **read/write/edit**：文件操作
- **browser**：控制浏览器
- **web_search**：网页搜索
- **web_fetch**：获取 URL 内容
- **message**：跨渠道发送消息
- **cron**：管理定时任务
- **sessions**：会话管理
- **subagents**：子 Agent 编排
- **tts**：文本转语音

### Skills（技能）

Skills 存储在：
- 每个 agent workspace 的 `skills/`
- `~/.openclaw/skills/`（管理技能）
- 共享根如 `~/.openclaw/skills`

**安装技能：**
```bash
npx clawhub@latest install <skill-name>
```

**技能类型：**
- 内置技能：1password, github, gifgrep, summarize, weather, xurl 等
- 自定义技能：workspace-specific skills

---

## 十、诊断与排错

### Doctor 工具

`openclaw doctor` 是修复 + 迁移工具，修复过期配置/状态、检查健康、提供可操作修复步骤。

```bash
openclaw doctor           # 交互式
openclaw doctor --yes     # 无提示接受默认值
openclaw doctor --repair  # 应用建议修复
openclaw doctor --deep    # 深度扫描系统服务
```

**主要功能：**
- 配置标准化（legacy 值迁移）
- 状态迁移（sessions/agent dir/WhatsApp auth）
- Session 锁检查和清理
- 权限检查
- 模型认证健康检查
- 安全警告（开放 DM 策略等）
- 沙箱镜像修复

### 健康检查

```bash
openclaw status              # 本地摘要
openclaw status --all        # 完整诊断
openclaw status --deep      # 深度探测
openclaw health             # 健康快照
openclaw health --verbose   # 强制实时探测
```

### 常见问题

| 问题 | 解决 |
|------|------|
| Gateway 不可达 | 启动：`openclaw gateway --port 18789` |
| logged out (409-515) | 重新链接：`openclaw channels logout && login` |
| 无入站消息 | 确认发送者在 allowFrom；检查 group mention 规则 |
| 频道断开 | 检查凭据：`ls -l ~/.openclaw/credentials/...` |

---

## 十一、飞书（Feishu）配置

> 见 `channels/feishu.md`

### 关键配置项

```json5
{
  channels: {
    feishu: {
      dmPolicy: "pairing",
      allowFrom: ["ou_xxx"],
      // ... 其他配置
    }
  }
}
```

### 可用操作

- `message`：发送、读取、编辑、thread 回复
- `feishu_doc`：文档操作（读/写/创建表格等）
- `feishu_wiki`：知识库操作
- `feishu_drive`：云盘操作
- `feishu_bitable`：多维表格操作
- `feishu_chat`：聊天操作

---

## 十二、安全模型

### 配对流程

所有 WS clients（包括 operators + nodes）在 `connect` 时包含设备身份：
- 新设备 ID 需要配对批准
- Gateway 颁发设备 token 供后续连接使用
- 本地 loopback 可自动批准

### Auth 模式

```json5
{
  gateway: {
    auth: {
      mode: "token",          // token | password | trusted-proxy | none
      token: "your-token",
      allowTailscale: true,   // Tailscale Serve 模式
    }
  }
}
```

### 关键原则

- 配置文件权限：`chmod 600 ~/.openclaw/openclaw.json`
- Workspace 是私有记忆，**不要提交 secrets**
- API keys、OAuth tokens、密码不存储在 workspace
- 使用 `.gitignore` 排除敏感文件

---

## 十三、快速命令参考

```bash
# 安装
curl -fsSL https://openclaw.ai/install.sh | bash

# 初始化
openclaw onboard --install-daemon

# Gateway 管理
openclaw gateway status
openclaw gateway restart

# 状态检查
openclaw status
openclaw health --verbose

# 诊断
openclaw doctor
openclaw doctor --repair

# 会话
openclaw sessions --json
openclaw sessions list

# Cron
openclaw cron list
openclaw cron add --name "X" --at "20m" --session main --system-event "X"
openclaw cron runs --id <job-id>

# 消息
openclaw message send --to +1234567890 --message "Hello"

# Skills
npx clawhub@latest install <skill-name>
openclaw skills list

# Dashboard
openclaw dashboard
```

---

## 十四、文件路径速查

| 用途 | 路径 |
|------|------|
| 主配置 | `~/.openclaw/openclaw.json` |
| 状态目录 | `~/.openclaw/` |
| 主 Workspace | `~/.openclaw/workspace` |
| Agent Workspaces | `~/.openclaw/workspace-<agentId>` |
| Agent 状态 | `~/.openclaw/agents/<agentId>/agent/` |
| Sessions | `~/.openclaw/agents/<agentId>/sessions/` |
| Cron Jobs | `~/.openclaw/cron/jobs.json` |
| Credentials | `~/.openclaw/credentials/` |
| 管理 Skills | `~/.openclaw/skills/` |

---

*洞察者 · OpenClaw 官方知识库 · 2026-04-06*
