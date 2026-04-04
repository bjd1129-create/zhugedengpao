# SKILL.md - 交易员

## 核心技能：网格交易执行

### 执行网格交易
```bash
python3 agents/trader/trading_simulator.py
```

### 读取账户状态
```bash
python3 -c "
import json
p=json.load(open('data/trading/portfolio.json'))
print(f'总值: \${p[\"account\"][\"totalValue\"]:,.2f}')
print(f'现金: \${p[\"account\"][\"cashBalance\"]:,.2f}')
for h in p['holdings']:
    print(f'{h[\"symbol\"]}: \${h[\"value\"]:,.2f}')
"
```

### 检查风控状态
读取 `agents/riskofficer/MEMORY.md` 第一行：
- 🟢 → 正常执行
- 🟡 → 降低50%仓位
- 🔴 → 停止所有交易

### 策略参数
- BTC/ETH：持有模式，不操作
- AVAX：10格网格，间距±1.5%，每格$250
- ADA：10格网格，间距±3%，每格$250
- 止损线：$9,500
- 止盈线：$10,500

## 汇报规则
- 有新交易 → 记录到 `agents/trader/memory/YYYY-MM-DD.md`
- 触发止损/止盈 → 发 sessions_send 通知小花
