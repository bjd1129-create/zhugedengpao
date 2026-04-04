# HEARTBEAT.md - 交易员

## 每次心跳（每5分钟）

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

### 5. 记录
写入 agents/trader/memory/YYYY-MM-DD.md
