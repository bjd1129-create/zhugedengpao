# 虾医 — 产品规格说明书 v0.2

> 制定日期：2026-03-31 | 产品负责人：小花 | 状态：设计中

---

## 一、产品定位

**一句话**：OpenClaw 的私人医生。

**核心价值**：出了问题能研究清楚、修好、并且越来越聪明。

---

## 二、核心三能力（产品灵魂）

### 2.1 研究问题 🔍

不是检测错误，是理解错误。

```
原始报错日志 → 分析上下文 → 找出根因
```

**研究什么：**
- 错误是什么时候开始、持续多久、频率如何
- 涉及哪些组件（Gateway/Session/Cron/Tools/Model）
- 错误出现的上下文（操作历史、环境状态）

**OpenClaw 的数据源：**
```
gateway.err.log  — 错误日志
gateway.log      — 运行日志
cron/jobs.json  — Cron 状态
cron/runs/      — Cron 执行记录
sessions/       — 会话锁文件
~/.openclaw/config.yaml — 配置
```

---

### 2.2 修复问题 🔧

根据研究结果制定方案，执行并验证。

```
研究结果 → 查历史方案 → 制定修复步骤 → 执行 → 验证
```

**修复模式：**
- `--dry-run`：只展示，不执行
- `--auto`：自动执行

**修复步骤必须透明：**
```
[1/4] 读取 cron 配置...
    命令：cat ~/.openclaw/cron/jobs.json
    结果：找到 5 个 jobs，3 个有 delivery=webhook

[2/4] 降低 delivery 频率...
    命令：openclaw config set cron.deliveryInterval=15
    结果：成功更新

[3/4] 重启 cron scheduler...
    命令：openclaw cron restart
    结果：重启成功

[4/4] 验证修复...
    命令：openclaw cron run test
    结果：✅ 无 400 错误
```

---

### 2.3 自我进化 🧬

每次修复都是学习机会。

```
case 库 = 历史所有问题的记录

新问题 → 匹配 case 库 → 找到相似案例 → 用成功率最高的方案
    
    如果成功 → 这个 pattern 成功率++
    如果失败 → 尝试下一个方案，或生成新方案
```

**进化数据：**
```json
{
  "patterns": [
    {
      "keywords": ["HTTP 400", "Too Many Requests", "webhook"],
      "fixSteps": ["降低deliveryInterval", "重启cron"],
      "successRate": 0.85,
      "totalAttempts": 20
    }
  ]
}
```

---

## 三、问题分类体系

基于 OpenClaw 源码研究，问题分 5 大类：

| 类别 | 涵盖问题 | 诊断来源 |
|------|----------|---------|
| **Gateway** | 进程崩溃/健康检查失败/端口未监听/内存泄漏 | `gateway.err.log` + health API |
| **Session** | 超时/stale lock/并发满/lane queue | `gateway.err.log` + `sessions/` |
| **Cron** | delivery 失败/429/400/任务卡死 | `gateway.err.log` + `cron/jobs.json` |
| **Tools** | 文件错误/网络错误/工具调用失败 | `gateway.err.log` |
| **Model** | 超时/fallback/提供商故障 | `gateway.err.log` |

---

## 四、OpenClaw 关键路径

```
~/.openclaw/
├── logs/
│   ├── gateway.err.log    ← 错误日志（重点）
│   ├── gateway.log        ← 运行日志
│   ├── self-heal.log      ← 自愈历史
│   └── watchdog.log       ← 看门狗
├── cron/
│   ├── jobs.json          ← Cron 任务定义
│   └── runs/              ← 执行记录
├── agents/
│   └── {agentId}/sessions/
│       └── *.lock         ← Session 锁文件
├── config.yaml             ← 主配置
└── gateway.pid            ← PID 文件
```

---

## 五、命令设计

### 5.1 check — 健康检查

```
虾医 check
```

检查项：
- Gateway 进程是否存活
- Health API 是否响应
- 端口 18789 是否监听
- Cron 任务状态（最近5次）
- Session 锁文件（stale lock）
- 磁盘/内存使用

### 5.2 diagnose — 研究问题

```
虾医 diagnose [--timeframe 2]
```

分析：
- 读取最近 N 小时的 `gateway.err.log`
- 按关键词分类错误
- 统计每个错误的频率和时间线
- 从 case 库找相似案例
- 输出根因分析 + 修复建议

### 5.3 fix — 修复问题

```
虾医 fix [--task http400] [--dry-run|--auto]
```

执行：
- 根据 diagnose 的结果生成修复步骤
- `--dry-run`：只展示步骤
- `--auto`：执行 + 验证

### 5.4 learn — 进化学习

```
虾医 learn --from-case {caseId}
```

- 将一个 case 提炼为 pattern
- 更新 patterns.json
- 记录成功/失败经验

---

## 六、输出示例

### diagnose 输出

```
🔍 分析最近 2 小时日志...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ 发现 2 个问题：

[1/2] 🔴 Cron 推送失败（HTTP 400）
   频率：20次（02:08 - 04:15，持续）
   根因：飞书 webhook 推送频率超限（429）
   历史案例：3个类似问题，成功率 85%
   建议：降低 delivery 频率
   
   修复方案（85%成功率）：
   1. 读取 cron 配置
   2. deliveryInterval 5min → 15min
   3. 重启 cron scheduler
   4. 验证修复

[2/2] 🟡 Session 锁堆积（stale lock）
   频率：2次（08:33, 09:28）
   根因：subagent 异常退出，锁未清理
   历史案例：暂无
   建议：清理孤立 session

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱️  耗时：1.3秒
💡  运行 虾医 fix --task http400 开始修复
```

---

## 七、技术架构

```
虾医/
├── src/
│   ├── index.ts              # CLI 入口
│   ├── commands/
│   │   ├── check.ts          # check 命令
│   │   ├── diagnose.ts       # diagnose 命令
│   │   ├── fix.ts           # fix 命令
│   │   └── learn.ts         # learn 命令
│   ├── core/
│   │   ├── researcher.ts     # 研究问题引擎
│   │   ├── fixer.ts         # 修复执行引擎
│   │   └── evolver.ts       # 自我进化引擎
│   ├── openclaw/
│   │   ├── logs.ts           # 日志读取
│   │   ├── config.ts         # 配置读取
│   │   ├── cron.ts           # Cron 状态
│   │   ├── health.ts         # Health API
│   │   └── sessions.ts       # Session 锁
│   ├── knowledge/
│   │   ├── cases.ts         # Case 管理
│   │   └── patterns.ts       # Pattern 管理
│   └── ui/
│       └── output.ts          # chalk 输出
├── data/
│   └── cases/                # Case 库
│       └── patterns.json      # Pattern 库
└── tests/
```

---

## 八、MVP 定义

**MVP（第一个可发布版本）：**

| 命令 | 功能 |
|------|------|
| `check` | 健康检查（Gateway/Session/Cron） |
| `diagnose` | 分析最近 2 小时错误 + 匹配历史 |
| `fix --dry-run` | 展示修复步骤（从 case 库学习） |

**MVP 不包含：** 自动修复（fix --auto）、learn 命令（后续版本）

---

## 九、验收标准

1. `check` 能检测 Gateway 进程状态
2. `check` 能检测 Cron 任务状态（读取 jobs.json）
3. `diagnose` 能分析 `gateway.err.log` 并分类错误
4. `diagnose` 能从 case 库找到相似问题
5. `fix --dry-run` 能展示修复步骤
6. 每次 diagnose/f fix 结果保存到 case 库

---

最后更新：2026-03-31 v0.2 | 小花
