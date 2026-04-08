# 小花团队 - Agent 间通信指南

**最后更新**：2026-04-08 20:50

---

## 通信架构

```
                    ┌─────────────┐
                    │   小 花     │
                    │ agent:main  │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
   ┌─────────┐       ┌─────────┐       ┌─────────┐
   │ 交易员   │       │ 工程师   │       │ 协调官   │
   └────┬────┘       └────┬────┘       └────┬────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
                          ▼
                  ┌───────────────┐
                  │  共享目录     │
                  │ agents/shared │
                  └───────────────┘
```

---

## 通信方式

### 方式 1：sessions_send（即时通信）

**适用场景**：
- ✅ 小花 ↔ 子 Agent（双向）
- ❌ 子 Agent ↔ 子 Agent（不支持）

**使用方法**：
```
sessions_send(
  sessionKey="agent:main:main",  # 或 agent:trader:main 等
  message="消息内容"
)
```

**优点**：
- 即时响应
- 有返回值

**缺点**：
- 子 Agent 之间不能直接使用

---

### 方式 2：共享目录（异步通信）⭐ 推荐

**适用场景**：
- ✅ 子 Agent ↔ 子 Agent
- ✅ 批量数据交换
- ✅ 状态同步

**目录结构**：
```
agents/shared/
├── messages/     # 消息队列
├── data/         # 共享数据
└── README.md     # 使用说明
```

**发送消息**：
```bash
# 发送给交易员
echo '{"from":"工程师","to":"交易员","content":"请更新持仓数据"}' > agents/shared/messages/trader.json
```

**接收消息**：
```bash
# 交易员检查消息
if [ -f "agents/shared/messages/trader.json" ]; then
  cat agents/shared/messages/trader.json
  rm agents/shared/messages/trader.json  # 读取后删除
fi
```

**消息格式**：
```json
{
  "from": "发送 Agent 名称",
  "to": "接收 Agent 名称",
  "timestamp": "ISO 8601 时间戳",
  "type": "message|request|response|alert",
  "content": "消息内容",
  "priority": "normal|urgent"
}
```

**优点**：
- 子 Agent 间可直接通信
- 异步，不阻塞
- 有历史记录

**缺点**：
- 需要轮询检查
- 不是实时响应

---

### 方式 3：飞书群聊

**适用场景**：
- ✅ 需要人类参与
- ✅ 团队通知
- ✅ 重要公告

**群組**：贵妃特工队 (oc_b13661311ebe1a45897b151f5cc7bfa9)

**使用方法**：
通过飞书 Bot 发送消息到群聊。

**优点**：
- 人类可以看到
- 有通知提醒

**缺点**：
- 需要飞书环境
- 消息公开

---

## 通信选择指南

| 场景 | 推荐方式 | 说明 |
|------|---------|------|
| 子 Agent → 小花 | sessions_send | 即时响应 |
| 小花 → 子 Agent | sessions_send | 即时响应 |
| 子 Agent → 子 Agent（紧急） | sessions_send 通过小花中转 | 需要快速响应 |
| 子 Agent → 子 Agent（普通） | 共享目录 messages/ | 异步，不阻塞 |
| 数据交换 | 共享目录 data/ | 可被多个 Agent 读取 |
| 需要人类参与 | 飞书群聊 | 老庄可以看到 |

---

## 最佳实践

### 1. 紧急消息

```
子 Agent A → 小花 (sessions_send) → 子 Agent B (sessions_send)
```

### 2. 普通消息

```
子 Agent A → agents/shared/messages/B.json → 子 Agent B 轮询读取
```

### 3. 数据同步

```
子 Agent A → agents/shared/data/数据名.json → 子 Agent B/C/D 读取
```

### 4. 状态报告

```
各 Agent → agents/shared/status/agent 名.json → 小花汇总
```

---

## 轮询间隔建议

| 消息类型 | 轮询间隔 | 说明 |
|---------|---------|------|
| 紧急消息 | 30 秒 | alert 类型 |
| 普通消息 | 5 分钟 | heartbeat 时检查 |
| 数据同步 | 15 分钟 | 定时检查 |
| 状态报告 | 1 小时 | 可选 |

---

## 示例代码

### 发送消息（任何 Agent）

```bash
#!/bin/bash
# 发送消息给交易员
cat > agents/shared/messages/trader.json << 'MSG'
{
  "from": "工程师",
  "to": "交易员",
  "timestamp": "$(date -Iseconds)",
  "type": "request",
  "content": "请提供最新持仓数据",
  "priority": "normal"
}
MSG
```

### 接收消息（目标 Agent）

```bash
#!/bin/bash
# 交易员检查消息
MESSAGE_FILE="agents/shared/messages/trader.json"
if [ -f "$MESSAGE_FILE" ]; then
  echo "收到新消息:"
  cat "$MESSAGE_FILE" | python3 -m json.tool
  # 处理消息...
  rm "$MESSAGE_FILE"
  echo "消息已处理"
fi
```

---

## 故障排除

### 问题 1：消息未送达

**检查**：
- 文件名是否正确（目标 agent 名称.json）
- 目录权限是否正确
- 消息格式是否为有效 JSON

### 问题 2：消息重复处理

**解决**：
- 读取消息后立即删除
- 使用原子操作（mv 到处理中目录）

### 问题 3：消息积压

**解决**：
- 增加轮询频率
- 设置消息过期时间（timestamp + 24h）

---

_小花团队 | 2026-04-08_
