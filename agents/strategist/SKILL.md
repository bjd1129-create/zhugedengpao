# SKILL.md - 策略师

## 核心技能：市场研究与策略设计

### 获取实时价格
```bash
python3 -c "
import requests
P = {'https':'http://127.0.0.1:7897'}
for sym, name in [('BTCUSDT','BTC'),('ETHUSDT','ETH'),('AVAXUSDT','AVAX'),('ADAUSDT','ADA')]:
    r = requests.get('https://api.binance.com/api/v3/ticker', params={'symbol':sym}, proxies=P, timeout=10).json()
    h,l = float(r['highPrice']),float(r['lowPrice'])
    vol=(h-l)/((h+l)/2)*100
    print(f'{name}: \${float(r[\"lastPrice\"]):,.2f} | 波动:{vol:.2f}%')
"
```

### 获取K线数据计算RSI
```bash
python3 -c "
import requests
P = {'https':'http://127.0.0.1:7897'}
k = requests.get('https://api.binance.com/api/v3/klines',
    params={'symbol':'BTCUSDT','interval':'4h','limit':15},
    proxies=P, timeout=10).json()
closes = [float(c[4]) for c in k]
gains = [closes[i+1]-closes[i] for i in range(len(closes)-1)]
avg_g = sum([g for g in gains if g>0])/max(len([g for g in gains if g>0]),1)
avg_l = sum([abs(g) for g in gains if g<0])/max(len([g for g in gains if g<0]),1)
rsi = 100-(100/(1+avg_g/avg_l)) if avg_l>0 else 100
print(f'BTC RSI(4h): {rsi:.1f}')
"
```

### 判断市场状态
| RSI | 市场状态 | 策略建议 |
|-----|---------|---------|
| >70 | 超买 | 谨慎，不追高 |
| 50-70 | 中性偏多 | 可以做多 |
| 30-50 | 中性偏空 | 观望 |
| <30 | 超卖 | 可能反弹 |

### 写策略报告
写研究报告到 `agents/strategist/memory/YYYY-MM-DD.md`

## 策略知识库

### 网格交易原理
- 价格每下跌一格 → 买入一格
- 价格每回升一格 → 卖出平仓
- 每格利润 = 每格金额 × 间距

### 最适合网格的币种特征
- 24h波动率 > 2%
- 成交量 > $10M
- 价格适中（$0.1~$100）

### 当前推荐参数
- AVAX：±1.5%间距（波动3.45%）
- ADA：±3%间距（波动3.32%）
- BTC/ETH：持有不操作（波动太小）
