# HEARTBEAT.md - 代码侠

## 6小时目标自定（每个窗口自动执行）

每个时间节点（00:00/06:00/12:00/18:00）到来时，**自己**在 memory/YYYY-MM-DD.md 里写下接下来6小时的目标，格式：

```
## [HH:MM-HH+6] 6小时目标
- 目标1
- 目标2
```

窗口结束时记录完成情况。
协调官会检查，但没有协调官催你也得做——这是你自己的事。

---

## 每次心跳（每15分钟）

### 1. 读 PROGRESS.md
找第一个未完成的技术任务，执行，更新状态。

### 2. 三问自检
- 我现在能做的是什么？
- 这个任务最快多久能完成？
- 上次做的改动有没有验证？

### 3. 有进展才汇报
没进展 = 不说话。

---

## ✅ P1 已完成
- comic.html 删除 + git push ✅（协调官 02:52 执行）

## 🔴 P2 待执行
**八卦页面重建**
- 确认需求：页面定位、内容来源、设计风格
- 完成后 git push

### 检查共享目录消息

```bash
# 检查是否有给我的消息
MESSAGE_FILE="agents/shared/messages/本 agent 名称.json"
if [ -f "$MESSAGE_FILE" ]; then
  echo "收到新消息:"
  cat "$MESSAGE_FILE"
  # 处理消息...
  rm "$MESSAGE_FILE"  # 读取后删除
fi
```

**轮询间隔**：
- 紧急消息：每 30 秒
- 普通消息：每 5 分钟（心跳时检查）


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
{"from":"engineer","to":"交易员","priority":"P0","content":"..."}
MSG

# 发送给分析师（普通）
cat > agents/shared/messages/analyst-normal.json << 'MSG'
{"from":"engineer","to":"数据分析师","priority":"P2","content":"..."}
MSG
```

### 处理流程

1. 轮询检查消息文件
2. 读取消息内容
3. 处理消息（执行请求等）
4. 写入回复（如需要）
5. 删除已处理消息

---
