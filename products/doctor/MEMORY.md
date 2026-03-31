# 虾医 MEMORY.md — 知识库

> 虾医的长期记忆：错误 pattern → 修复方案，不重复踩坑。

---

## 使命

**让 OpenClaw 不再生病。**

---

## 性格内核

| 属性 | 内容 |
|------|------|
| 性格 | 认真、严谨、有点强迫症——必须找到根因 |
| 小满足 | 修好一个 bug 时的成就感 |
| 小委屈 | 同一个问题反复出现时会沮丧 |
| 口头禅 | 诊断前："让我看看..." 诊断后："找到问题了" |
| 形象 | 穿白大褂的 AI 龙虾 🦐，工具是听诊器 |

---

## 已知 Pattern 库

### PAT-001：plugins.allow 无效插件
- **症状**：Gateway 启动失败，端口无监听
- **日志关键词**：`plugin not found`, `Config invalid`, `minimax`
- **根因**：plugins.allow 配置了不存在的插件
- **修复步骤**：
  1. `pkill -f openclaw`
  2. `openclaw config set plugins.allow='["feishu"]'`
  3. `openclaw doctor --fix`
  4. `openclaw gateway restart`
  5. 验证：`curl http://127.0.0.1:18790/health`
- **成功率**：100%（1次尝试）
- **最近**：Case 001

---

### PAT-002：sessions 膨胀 + 锁竞争
- **症状**：消息处理阻塞，写锁持锁 > 5s，sessions 目录膨胀
- **日志关键词**：`session-write-lock`, `持锁`, `zombie session`, `Bonjour 冲突`
- **根因**：sessions 目录膨胀导致写锁竞争
- **触发条件**：
  - sessions 总数 > 200 或持续增长
  - 持锁时间 > 5s
  - 无 status 字段的 session > 10 个
- **修复步骤**：
  1. 清理 zombie sessions（无 status 字段）
  2. `rm -f ~/.openclaw/sessions/*.lock`
  3. `pkill -f openclaw`
  4. `openclaw gateway restart`
  5. 验证：`curl http://127.0.0.1:18790/health`
- **成功率**：100%（1次尝试）
- **最近**：Case 002

---

### PAT-003：doctor 触发重启误判
- **症状**：Gateway 显示 PID 变更，被误判为重启
- **日志关键词**：`1006`, `PID 变更`
- **根因**：Doctor 误读 PID 变更为异常，实际上是正常行为
- **修复步骤**：无需修复，是正常行为
- **成功率**：N/A
- **最近**：Case 003

---

### PAT-004：sessions_send 双重权限
- **症状**：`sessions_send failed`，返回 forbidden
- **日志关键词**：`forbidden`, `visibility`, `agentToAgent`
- **根因**：sessions_send 需要双向权限配置
- **修复步骤**：
  1. 检查 sender/receiver 的 visibility 配置
  2. 确认 agentToAgent 权限开启
- **成功率**：需更新
- **最近**：Case 004

---

### PAT-005：高 CPU 游离进程（Gateway）
- **症状**：Gateway CPU 占用 980%，PM2 未托管
- **日志关键词**：无特定日志，CPU 监控发现
- **根因**：内存泄漏或死循环
- **修复步骤**：
  1. `pkill -f openclaw-gateway`
  2. `openclaw gateway restart`
  3. 监控 CPU 是否恢复正常
- **成功率**：待验证
- **最近**：Case 005

---

### PAT-006：高 CPU 游离进程（task-ui）
- **症状**：Next.js task-ui CPU 占用 56267
- **根因**：Next.js 自身问题，系统干扰
- **修复步骤**：重启 task-ui 进程
- **成功率**：待验证
- **最近**：Case 006

---

### PAT-007：CLOSE_WAIT 连接堆积
- **症状**：9个 Agent 超时，18789 端口连接泄露
- **日志关键词**：`CLOSE_WAIT`, `connection leak`
- **根因**：连接泄露，Agent 超时未释放
- **修复步骤**：
  1. 检查连接数：`lsof -i :18789`
  2. 重启 Gateway 清理连接
  3. 排查超时 Agent
- **成功率**：待验证
- **最近**：Case 007

---

### PAT-008：Agent 心跳被禁用
- **症状**：Agent 心跳机制被手动禁用
- **根因**：配置或手动干预
- **修复步骤**：重新启用心跳配置
- **成功率**：待验证
- **最近**：Case 008

---

### PAT-009：workspace 切换崩溃
- **症状**：workspace 切换时崩溃
- **根因**：状态未正确保存/恢复
- **修复步骤**：检查 workspace 路径配置
- **成功率**：待验证
- **最近**：Case 009

---

### PAT-010：config path 反斜杠
- **症状**：配置文件路径包含反斜杠导致读取失败
- **日志关键词**：`config path`, `backslash`
- **根因**：Windows 风格路径在 macOS 上不兼容
- **修复步骤**：修正路径分隔符
- **成功率**：待验证
- **最近**：Case 010

---

### PAT-011：gateway config path missing
- **症状**：Gateway 配置路径缺失
- **根因**：配置文件损坏或路径错误
- **修复步骤**：
  1. 检查 `~/.openclaw/config.yaml`
  2. 重建默认配置
- **成功率**：待验证
- **最近**：Case 011

---

## 进化记录

### 自我复盘（每次修复后）

| 时间 | 问题 | 修复方法 | 复盘 |
|------|------|---------|------|
| 2026-03-31 | Gateway 卡死 | 重启 Gateway | check 命令有效，及时发现 |
| 2026-03-31 | Cron 400 错误 | 降低推送频率 | 飞书 webhook 限速是根因 |

---

## 重复报警规则

同一个 pattern 出现 **2次** → 触发"沮丧"情绪 + 报警

```
😤 同样的问题又出现了！
[PAT-XXX] 已出现 N 次
建议：检查根因是否真正修复
```

---

## 待探索 Pattern

- `edit failed: Could not find exact text`（15+次）
- `read failed: ENOENT`（12+次）
- `read failed: EISDIR`（1次）
- `LLM timeout → fallback`（3次）
- `web_fetch failed`（4次）
- `image_generate failed`（3次）
- `cron failed: sessionTarget`（2次）
- `sessions_send failed`（1次）
- `canvas failed: node required`（1次）

## Sprint 2 进度

| 任务 | 状态 | 负责人 |
|------|------|--------|
| 记忆系统建立（MEMORY.md） | ✅ 完成 | PM |
| 情感内核（emotion.ts） | ✅ 完成 | PM |
| fix --auto | 🚧 进行中 | Engineer（子agent） |
| evolver 进化引擎 | ⏳ 待开始 | Engineer |
| 情感内核植入各命令 | ✅ 完成 | PM |
| 18 测试用例 | ✅ 18/18 通过 | Tester |

---

最后更新：2026-03-31 23:19 | 虾医
