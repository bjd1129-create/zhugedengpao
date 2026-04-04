# HEARTBEAT.md - 策略师

## 每次心跳

### 1. 分析数据
- 读 data/trading/portfolio.json 看当前状态
- 分析昨日交易表现
- 评估策略有效性

### 2. 生成信号
有新策略信号吗？发交易员执行。

### 3. 优化参数
策略需要调整吗？写入 agents/strategist/MEMORY.md

### 4. 汇报
有重要发现 → 发飞书汇报给小花
