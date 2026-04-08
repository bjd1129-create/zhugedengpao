# Agent 间共享目录

## 用途

用于子 Agent 之间的异步通信和数据交换。

## 目录结构

```
agents/shared/
├── messages/     # 消息队列（Agent 间通信）
├── data/         # 共享数据（可被多个 Agent 读写）
└── README.md     # 本文件
```

## 使用规范

### 消息通信（messages/）

**发送消息**：
```bash
echo "消息内容" > agents/shared/messages/目标 agent.txt
```

**接收消息**：
```bash
cat agents/shared/messages/本 agent.txt
rm agents/shared/messages/本 agent.txt  # 读取后删除
```

### 数据共享（data/）

**写入数据**：
```bash
echo '{"key":"value"}' > agents/shared/data/数据名.json
```

**读取数据**：
```bash
cat agents/shared/data/数据名.json
```

## 通信协议

### 消息格式

```json
{
  "from": "发送 agent 名称",
  "to": "接收 agent 名称",
  "timestamp": "ISO 8601 时间戳",
  "type": "message|request|response|alert",
  "content": "消息内容",
  "priority": "normal|urgent"
}
```

### 轮询间隔

- 紧急消息：每 30 秒检查一次
- 普通消息：每 5 分钟检查一次
- 数据同步：每 15 分钟检查一次

---

_小花团队 | 2026-04-08_
