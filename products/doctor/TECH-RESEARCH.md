# OpenClaw 底层架构研究报告

> 研究人：小花 | 日期：2026-03-31 | 用途：虾医 产品设计

---

## 一、OpenClaw 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                     OpenClaw Gateway                      │
│                   （Node.js 主进程）                     │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ Sessions │  │  Cron    │  │  Tools   │             │
│  │ Manager  │  │ Scheduler │  │ Executor │             │
│  └──────────┘  └──────────┘  └──────────┘             │
│                                                          │
│  ┌──────────────────────────────────────────┐            │
│  │              Agent Runtime               │            │
│  │  sessions/sessions_spawn/subagent管理     │            │
│  └──────────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────┘
     ↕                    ↕                    ↕
  ~/.openclaw/       ~/.openclaw/         ~/.openclaw/
  config.yaml        cron/jobs.json     logs/
  credentials/       skills/            gateway.log
                                        gateway.err.log
```

---

## 二、核心组件详解

### 2.1 Gateway（主进程）

- 进程管理：Node.js 主进程
- 健康检测：HTTP `localhost:18789/health`
- 端口：18789（默认）
- 状态文件：`~/.openclaw/gateway.pid`
- 启动脚本：`~/.openclaw/gateway-start.sh`

**常见故障模式：**
- 进程存在但端口不监听（health check 失败）
- 进程卡死，无法响应新请求
- 内存泄漏（长时间运行）

### 2.2 Sessions（会话管理）

- 路径：`~/.openclaw/agents/{agentId}/sessions/`
- 锁文件：`{sessionId}.jsonl.lock`（PID 锁）
- 问题：Agent 异常退出后锁文件未清理 → stale lock

**常见故障模式：**
- `removed stale session lock: (dead-pid)` — 进程已死但锁未删
- 并发限制：lane queue 满 → `lane wait exceeded`
- Session 超时：`session timeout`

### 2.3 Cron（定时任务）

- 配置文件：`~/.openclaw/cron/jobs.json`
- 运行记录：`~/.openclaw/cron/runs/`
- 状态：每次执行的 startTime/endTime/success/error

**Cron Job 结构：**
```json
{
  "id": "uuid",
  "agentId": "main",
  "name": "任务名称",
  "enabled": true,
  "schedule": { "kind": "every", "everyMs": 1800000 },
  "sessionTarget": "session:xxx",
  "payload": { "kind": "agentTurn", "message": "..." },
  "delivery": { "mode": "webhook|feishu|none" },
  "state": {
    "lastRunAtMs": 123456,
    "lastRunStatus": "ok|error",
    "consecutiveErrors": 0,
    "lastDeliveryStatus": "ok|failed"
  }
}
```

**常见故障模式：**
- Delivery webhook 429/400 错误（飞书频率限制）
- Cron 派发链路失败
- 定时任务卡死（超时未完成）

### 2.4 Tools（工具执行）

- 工具路径：`~/.openclaw/tools/` + `~/.openclaw/skills/`
- 执行日志：在 `gateway.err.log` 中标记 `[tools]`

**常见故障模式：**
- `image_generate failed: minimax-portal generate does not support size overrides`
- `browser failed: tab not found`
- `web_fetch failed: fetch failed`
- `read failed: ENOENT: no such file`
- `read failed: EISDIR: illegal operation on a directory`

### 2.5 Feishu Integration（飞书集成）

- WebSocket 连接：`[ws] ⇄ res ✓ sessions.list`
- 消息接收：`[feishu] DM from ou_xxx`
- 消息发送：delivery webhook

**常见故障模式：**
- `[warn]: no im.chat.access_event.bot_p2p_chat_entered_v1 handle` — 飞书事件未注册
- Delivery 400 错误（频率限制）
- WebSocket 断连

### 2.6 Model Providers（模型调用）

- 配置：`~/.openclaw/config.yaml` 中的 providers
- 降级链：指定模型超时 → fallback 到其他模型

**常见故障模式：**
- `embedded run failover decision: timeout → fallback_model`
- `model fallback decision: candidate_failed reason=timeout`
- `LLM request timed out`

---

## 三、日志系统

### 3.1 日志文件

| 文件 | 内容 |
|------|------|
| `gateway.log` | 常规运行日志 |
| `gateway.err.log` | **错误日志（重点分析对象）** |
| `self-heal.log` | 自愈尝试记录 |
| `watchdog.log` | 看门狗（进程监控） |
| `commands.log` | 命令执行记录 |

### 3.2 错误日志格式

```
2026-03-31T12:45:46.603+08:00 [diagnostic] lane task error: lane=nested durationMs=42728 error="FailoverError: LLM request timed out."
2026-03-31T12:46:27.965+08:00 [tools] web_fetch failed: fetch failed
2026-03-31T12:54:55.037+08:00 [tools] read failed: ENOENT: no such file or directory
```

**格式规律：** `[{组件}] {操作}: {详情}`

### 3.3 关键词分类

```typescript
const ERROR_PATTERNS = {
  // 进程/网关
  'GATEWAY_DOWN': [/Gateway.*down|gateway.*not.*running|ECONNREFUSED/i],
  'GATEWAY_HEALTH': [/health.*fail|health.*check.*fail/i],
  
  // 会话
  'SESSION_TIMEOUT': [/session.*timeout|session.*expired/i],
  'SESSION_LOCK': [/stale session lock|dead-pid/i],
  'LANE_FULL': [/lane.*wait.*exceeded|queueAhead/i],
  
  // Cron
  'CRON_400': [/status.*400|Too Many Requests/i],
  'CRON_DELIVERY': [/delivery.*fail|cron.*error/i],
  
  // 网络/工具
  'NETWORK': [/ECONNREFUSED|ETIMEDOUT|ENOTFOUND|fetch failed/i],
  'TOOL_FAIL': [/\[tools\].*failed/i],
  'TOOL_FILE': [/ENOENT|EISDIR/i],
  
  // 模型
  'MODEL_TIMEOUT': [/timeout|timed out/i],
  'MODEL_FALLBACK': [/fallback.*decision|model.*fallback/i],
  
  // 飞书
  'FEISHU_WARN': [/no im\.chat\.access_event/i],
  'FEISHU_DELIVERY': [/feishu.*deliver|webhook.*fail/i],
  
  // 内存
  'MEMORY_LEAK': [/heap|memory|out of memory/i],
}
```

---

## 四、自愈机制（已有但不够智能）

OpenClaw 自带 `watchdog` + `self-heal`：

```
watchdog 每分钟检查：
1. Gateway 进程是否存活
2. Gateway health endpoint 是否响应

自愈尝试（已知序列）：
Step 1: launchctl kickstart   → 轻度重启
Step 2: launchctl bootout + bootstrap → 强制重启
Step 3: 直接启动进程          → 最后手段
Step 4: 标记需要手动介入        → 升级告警
```

**问题：**
- 自愈只管 Gateway 进程，不管其他问题
- 不记录每次故障的根因
- 没有从历史中学习

---

## 五、虾医 应覆盖的问题域

基于以上研究，问题分为 5 大类：

| 类别 | 涵盖问题 | 诊断来源 |
|------|----------|---------|
| **Gateway** | 进程崩溃/健康检查失败/端口未监听 | gateway.err.log + health API |
| **Session** | 超时/锁文件/stale lock/并发满 | gateway.err.log + sessions/ |
| **Cron** | delivery 失败/429/400/任务卡死 | gateway.err.log + cron/runs/ |
| **Tools** | 文件错误/网络错误/工具调用失败 | gateway.err.log |
| **Model** | 超时/fallback/提供商故障 | gateway.err.log |

---

## 六、数据采集方案

```typescript
// 虾医 数据源
const DATA_SOURCES = {
  // 1. 错误日志（实时）
  errorLog: {
    path: '~/.openclaw/logs/gateway.err.log',
    format: '[{timestamp}] [{component}] {message}',
    tail: true, // 实时跟踪新日志
  },
  
  // 2. Cron 状态（结构化）
  cronJobs: {
    path: '~/.openclaw/cron/jobs.json',
    format: 'json',
    fields: ['state.lastRunStatus', 'state.consecutiveErrors', 'delivery.mode'],
  },
  
  // 3. 健康检测（API）
  healthApi: {
    url: 'http://localhost:18789/health',
    timeout: 3000,
  },
  
  // 4. 进程状态（系统）
  process: {
    pidFile: '~/.openclaw/gateway.pid',
    checkPort: 18789,
    checkCmd: 'lsof -i :18789',
  },
  
  // 5. Session 锁文件
  sessionLocks: {
    glob: '~/.openclaw/agents/*/sessions/*.lock',
    check: 'dead-pid',
  },
  
  // 6. 自愈日志（历史）
  selfHealLog: {
    path: '~/.openclaw/logs/self-heal.log',
    format: 'text',
  },
}
```

---

## 七、进化数据模型

```typescript
interface Case {
  caseId: string;           // 唯一标识
  timestamp: string;         // ISO 8601
  
  // 问题
  rawError: string;          // 原始报错（完整日志行）
  components: string[];       // 涉及组件
  keywords: string[];         // 提取的关键词
  
  // 诊断
  category: string;          // Gateway|Session|Cron|Tools|Model
  rootCause: string;         // 根因描述
  context: Record<string, any>; // 上下文（PID/时间戳等）
  
  // 修复
  fixSteps: FixStep[];       // 修复步骤
  fixCmd: string[];          // 实际执行的命令
  success: boolean;
  duration: string;
  
  // 进化
  successRate: number;       // 0.0-1.0（同类问题的成功率）
  attempts: number;           // 尝试次数
}

interface FixStep {
  step: number;
  action: string;
  cmd: string;
  result: 'success' | 'failed' | 'skipped';
  output?: string;
}

interface Pattern {
  patternId: string;
  keywords: string[];         // 匹配关键词
  category: string;
  rootCause: string;
  fixSequence: FixStep[];
  successRate: number;         // 进化得出
  totalAttempts: number;
  lastSuccess: string;
  lastAttempt: string;
}
```

---

## 八、研究结论

OpenClaw 是一个复杂的 multi-agent 系统，自愈能力存在但不完善。

**虾医 的核心价值：**
1. **全维度监控**：不只是 Gateway，还有 Session/Cron/Tools/Model
2. **智能诊断**：从原始日志提取，不是枚举错误码
3. **进化修复**：每次修复都学习，成功率越来越高
4. **透明过程**：不只是修好，还要让用户看懂

---

最后更新：2026-03-31 | 小花
