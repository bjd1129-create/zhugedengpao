# HEARTBEAT.md - 策略师

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

### 4. 记录
写入 agents/strategist/memory/YYYY-MM-DD.md
