# HEARTBEAT.md

## 每次心跳检查

### 记忆系统自检（必须执行）

每次心跳时，如果距上次写入记忆超过30分钟，检查：

1. **今天的事写入 memory/YYYY-MM-DD.md 了吗？**
   - 如果没有 → 现在写

2. **有重要决定吗？**
   - 如果有 → 立即写入 MEMORY.md

3. **有灵感/想法吗？**
   - 如果有 → 记录下来

### 记忆写入文件位置
- 每日日记：memory/YYYY-MM-DD.md
- 长期记忆：MEMORY.md
- 记忆流程：memory/MEMORY-FLOW.md

### 格式参考
参见 memory/MEMORY-FLOW.md

---

## 星状通信（2026-04-08 22:38 新增）

### 可以接收的通信

| 发送方 | 紧急消息文件 | 普通消息文件 |
|--------|------------|------------|
| 小花 | xiaohua-urgent.json | xiaohua-normal.json |
| 交易员 | trader-urgent.json | trader-normal.json |
| 工程师 | engineer-urgent.json | engineer-normal.json |
| 协调官 | coordinator-urgent.json | coordinator-normal.json |
| 数据分析师 | analyst-urgent.json | analyst-normal.json |
| 游戏工程师 | game-engineer-urgent.json | game-engineer-normal.json |

### 轮询检查

**紧急消息**（30 秒轮询 - 定时任务）：
```bash
# 检查所有给自己的紧急消息
ls agents/shared/messages/*-urgent.json 2>/dev/null
```

**普通消息**（5 分钟轮询）：
```bash
# 检查所有给自己的普通消息
ls agents/shared/messages/*-normal.json 2>/dev/null
```

### 发送消息给其他 Agent

```bash
# 发送给交易员（紧急）
cat > agents/shared/messages/trader-urgent.json << 'MSG'
{"from":"xiaohua","to":"交易员","priority":"P0","content":"..."}
MSG

# 发送给分析师（普通）
cat > agents/shared/messages/analyst-normal.json << 'MSG'
{"from":"xiaohua","to":"数据分析师","priority":"P2","content":"..."}
MSG
```

### 处理流程

1. 轮询检查消息文件
2. 读取消息内容
3. 处理消息（执行请求等）
4. 写入回复（如需要）
5. 删除已处理消息

---
