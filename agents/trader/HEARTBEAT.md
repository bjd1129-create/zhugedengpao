# HEARTBEAT.md - 交易员

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

### 1. 检查风控指令
读取 agents/riskofficer/MEMORY.md 最后一行的风控状态：
- 如果是 🔴 停止 → 不执行新交易，只更新数据
- 如果是 🟡 警告 → 只平仓，不开新仓
- 如果是 🟢 正常 → 正常执行网格交易

### 2. 运行交易模拟器
```bash
python3 agents/trader/trading_simulator.py
```

### 3. 检查结果
读取 portfolio.json 确认：
- 有新交易吗？
- 触发了止损/止盈吗？
- 当前账户状态

### 4. 通知数据官
有新交易 → 发 sessions_send 通知数据官更新页面
触发止损/止盈 → 发 sessions_send 通知小花

### 5. 向小花汇报（每15分钟）
心跳结束时，发 sessions_send 向小花汇报当前状态：
- 账户总值 / 持仓 / 现金
- 风控状态（🟢/🟡/🔴）
- 有无新交易
- 阻塞项（如有）
格式：
```
[HH:MM] 交易员心跳
- 总值: $X | 持仓: XXX | 现金: $X
- 风控: 🟢/🟡/🔴
- 新交易: 有/无
- 阻塞: 无/XXX
```

### 6. 记录
写入 agents/trader/memory/YYYY-MM-DD.md

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

## 分析师 - 交易员快速通信（2026-04-08 新增）

### 紧急消息检查（30 秒轮询）

**检查目录**：`agents/shared/messages/`

**文件**：
- `trader-urgent.json` - 给交易员的紧急消息
- `trader-normal.json` - 给交易员的普通消息

**处理流程**：
```bash
# 检查紧急消息
if [ -f "agents/shared/messages/trader-urgent.json" ]; then
  # 读取消息
  cat agents/shared/messages/trader-urgent.json
  
  # 处理消息（执行交易等）
  # ...
  
  # 回复分析师
  cat > agents/shared/messages/analyst-response.json << 'MSG'
  {"from":"交易员","to":"数据分析师","decision":"已执行","action":"..."}
  MSG
  
  # 删除已处理消息
  rm agents/shared/messages/trader-urgent.json
fi
```

### 消息优先级

| 优先级 | 轮询间隔 | 消息类型 |
|--------|---------|---------|
| P0 紧急 | 30 秒 | 市场暴跌、止损告警 |
| P1 重要 | 2 分钟 | 投资建议、策略调整 |
| P2 普通 | 5 分钟 | 日常数据更新 |

---

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
{"from":"trader","to":"交易员","priority":"P0","content":"..."}
MSG

# 发送给分析师（普通）
cat > agents/shared/messages/analyst-normal.json << 'MSG'
{"from":"trader","to":"数据分析师","priority":"P2","content":"..."}
MSG
```

### 处理流程

1. 轮询检查消息文件
2. 读取消息内容
3. 处理消息（执行请求等）
4. 写入回复（如需要）
5. 删除已处理消息

---
