# SKILL.md - 风控官

## 核心技能：账户风险监控

### 检查账户状态
```bash
python3 -c "
import json
p=json.load(open('data/trading/portfolio.json'))
total = p['account']['totalValue']
initial = p['account']['initialBalance']
cash = p['account']['cashBalance']
print(f'总资产: \${total:,.2f}')
print(f'初始: \${initial:,.2f}')
print(f'现金: \${cash:,.2f}')
print(f'浮亏: \${total-initial:,.2f} ({((total-initial)/initial*100):+.2f}%)')
"
```

### 风控等级判断
| 条件 | 等级 | 指令 |
|------|------|------|
| 总资产 > $10,200 | 🟢 正常 | 允许正常交易 |
| $10,000 < 总资产 ≤ $10,200 | 🟢 正常 | 允许交易 |
| $9,500 < 总资产 ≤ $10,000 | 🟡 警告 | 降低50%仓位 |
| 总资产 ≤ $9,500 | 🔴 停止 | 立即全仓止损 |
| 总资产 ≥ $10,500 | 🎯 止盈 | 立即全仓止盈 |

### 快速止损命令
如果触发🔴：
```bash
# 读取当前持仓，全部按市价卖出
# 更新 portfolio.json：所有持仓归0，cash += 持仓价值
```

### 更新风控状态
在 `agents/riskofficer/MEMORY.md` 第一行写入当前状态。

## 铁律
1. 单日亏损不超过5%（$500）
2. 单笔不超过$300（每格金额上限）
3. 最多同时持有4个币种
4. 宁可踏空，不可爆仓
