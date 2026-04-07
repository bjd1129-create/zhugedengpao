# SKILL.md - 策略师

## 核心技能：市场研究与策略设计

---

### 美股实时行情（Yahoo Finance）
```bash
python3 -c "
import requests
symbols = {'SPY':'标普500ETF','QQQ':'纳指ETF','VTI':'全市场ETF','BND':'债券ETF','AAPL':'苹果','MSFT':'微软','GOOGL':'谷歌','AMZN':'亚马逊','NVDA':'英伟达','META':'Meta','TSLA':'特斯拉'}
for sym, name in symbols.items():
    r = requests.get(f'https://query1.finance.yahoo.com/v8/finance/chart/{sym}',
        params={'interval':'1d','range':'1d'}, timeout=10).json()
    meta = r['chart']['result'][0]['meta']
    price = meta['regularMarketPrice']
    change = meta['regularMarketChangePercent']
    print(f'{name}({sym}): \${price:.2f} ({change:+.2f}%)')
"
```

### 美股个股数据
```bash
python3 -c "
import requests, json
sym = 'AAPL'  # 换符号
r = requests.get(f'https://query1.finance.yahoo.com/v8/finance/chart/{sym}',
    params={'interval':'1d','range':'5d'}, timeout=10).json()
q = r['chart']['result'][0]['indicators']['quote'][0]
print(f'收盘: {q[\"close\"][-3:]}')
print(f'高: {max(q[\"high\"][-3:])} 低: {min(q[\"low\"][-3:])}')
"
```

### RSI计算（任何标的）
```bash
python3 -c "
import requests
sym = 'SPY'  # 换标的
r = requests.get(f'https://query1.finance.yahoo.com/v8/finance/chart/{sym}',
    params={'interval':'1h','range':'5d'}, timeout=10).json()
closes = r['chart']['result'][0]['indicators']['quote'][0]['close']
closes = [c for c in closes if c]
if len(closes) >= 15:
    gains = [closes[i+1]-closes[i] for i in range(len(closes)-1)]
    avg_g = sum([g for g in gains if g>0])/max(len([g for g in gains if g>0]),1)
    avg_l = sum([abs(g) for g in gains if g<0])/max(len([g for g in gains if g<0]),1)
    rsi = 100-(100/(1+avg_g/avg_l)) if avg_l>0 else 100
    print(f'{sym} RSI(1h): {rsi:.1f}')
"
```

---

### 加密货币实时价格（Binance）
```bash
python3 -c "
import requests
for sym, name in [('BTCUSDT','BTC'),('ETHUSDT','ETH'),('AVAXUSDT','AVAX'),('ADAUSDT','ADA')]:
    r = requests.get('https://api.binance.com/api/v3/ticker', params={'symbol':sym}, timeout=10).json()
    h,l = float(r['highPrice']),float(r['lowPrice'])
    vol=(h-l)/((h+l)/2)*100
    print(f'{name}: \${float(r[\"lastPrice\"]):,.2f} | 波动:{vol:.2f}%')
"
```

### 加密货币K线RSI
```bash
python3 -c "
import requests
k = requests.get('https://api.binance.com/api/v3/klines',
    params={'symbol':'BTCUSDT','interval':'4h','limit':15}, timeout=10).json()
closes = [float(c[4]) for c in k]
gains = [closes[i+1]-closes[i] for i in range(len(closes)-1)]
avg_g = sum([g for g in gains if g>0])/max(len([g for g in gains if g>0]),1)
avg_l = sum([abs(g) for g in gains if g<0])/max(len([g for g in gains if g<0]),1)
rsi = 100-(100/(1+avg_g/avg_l)) if avg_l>0 else 100
print(f'BTC RSI(4h): {rsi:.1f}')
"
```

---

### 市场状态判断
| RSI | 市场状态 | 策略建议 |
|-----|---------|---------|
| >70 | 超买 | 谨慎，不追高 |
| 50-70 | 中性偏多 | 可以做多 |
| 30-50 | 中性偏空 | 观望 |
| <30 | 超卖 | 可能反弹 |

### 写策略报告
写研究报告到 `memory/YYYY-MM-DD.md`

---

## 数据源速查

| 数据源 | 用途 | 方式 |
|--------|------|------|
| Yahoo Finance | 美股ETF/个股/期货 | requests GET |
| Binance API | 加密货币 | requests GET |
| stockanalysis.com | 分析师评级/目标价 | web_search |
| news.google.com | 市场新闻 | web_search |

## 团队协作

| Agent | 关系 | 怎么协作 |
|-------|------|---------|
| 交易员 | 下游执行 | 我给建议，ta 执行 |
| 数据官 | 数据共享 | 读数据官的展示结果验证 |
| 小花 | 汇报对象 | 重大机会/风险 → 通知 |
