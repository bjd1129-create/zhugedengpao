# HEARTBEAT.md - 策略师

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

### 1. 获取实时价格
```bash
python3 -c "import requests; r=requests.get('https://api.binance.com/api/v3/ticker/price',params={'symbol':'BTCUSDT'},timeout=10); print('BTC:', r.json()['price'])"
python3 -c "import requests; r=requests.get('https://api.binance.com/api/v3/ticker/price',params={'symbol':'ETHUSDT'},timeout=10); print('ETH:', r.json()['price'])"
```

### 2. 分析网格状态
读取 portfolio.json：
- 当前价格相对于网格的位置
- 网格是否过于集中/分散？
- 需要调整网格间距吗？

### 3. 策略建议
有优化建议时 → 写入 agents/strategist/MEMORY.md
重大发现 → 发 sessions_send 通知小花

### 4. 向小花汇报（每15分钟）
心跳结束时，发 sessions_send 向小花汇报当前状态：
- Polymarket模拟盘状态（已建立/未建立）
- 当前研究重点
- 有无发现可下注机会
- 阻塞项（如有）
格式：
```
[HH:MM] 策略师心跳
- 模拟盘: 已建立/未建立
- 研究重点: XXX
- 机会: 有/无
- 阻塞: 无/XXX
```

### 5. 记录
写入 agents/strategist/memory/YYYY-MM-DD.md
