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

