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
    print(f\"{name}({sym}): \${meta['regularMarketPrice']:.2f} ({meta['regularMarketChangePercent']:+.2f}%)\")
"
```

### RSI计算（任何标的）
```bash
python3 -c "
import requests
sym = 'SPY'
r = requests.get(f'https://query1.finance.yahoo.com/v8/finance/chart/{sym}',
    params={'interval':'1h','range':'5d'}, timeout=10).json()
closes = [c for c in r['chart']['result'][0]['indicators']['quote'][0]['close'] if c]
if len(closes) >= 15:
    gains = [closes[i+1]-closes[i] for i in range(len(closes)-1)]
    avg_g = sum([g for g in gains if g>0])/max(len([g for g in gains if g>0]),1)
    avg_l = sum([abs(g) for g in gains if g<0])/max(len([g for g in gains if g<0]),1)
    rsi = 100-(100/(1+avg_g/avg_l)) if avg_l>0 else 100
    print(f'{sym} RSI(1h): {rsi:.1f}')
"
```

---

### Polymarket热门市场（官方API）
```bash
curl -s "https://gamma-api.polymarket.com/markets?limit=50&closed=false" | python3 -c "
import sys,json
data=json.load(sys.stdin)
by_vol=sorted(data,key=lambda x:float(x.get('volume24hr',0)),reverse=True)
for m in by_vol[:20]:
    p=json.loads(m.get('outcomePrices','[]'))
    vol=float(m.get('volume24hr',0))
    print(f'[\${vol:,.0f}] {m[\"question\"][:70]}')
    print(f'  YES={float(p[0]):.1%} NO={float(p[1]):.1%}' if len(p)==2 else '')
"
```

---

## Polymarket深度研究框架（核心技能）

完整版研究流程见：`SKILLS/POLYMARKET.md`

### 快速判断标准
| 偏差范围 | 结论 | 仓位建议 |
|---------|------|---------|
| >+20% | 市场低估NO | 轻仓BET NO |
| >+15% | 可能低估NO | 观察 |
| -15%~+15% | 无偏差 | 不下注 |
| <-15% | 市场高估YES | 轻仓BET YES |
| <-20% | 严重高估YES | 稍大仓位 |

**仓位原则：** 总资金5-10%，不重仓

### 研究流程（简版）
```
获取市场 → 深度搜索 → 独立判断 → 对比偏差>15% → 写报告
```

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
| **Polymarket Gamma API** | 热门预测市场 | curl/requests（官方API，无需Key） |
| stockanalysis.com | 分析师评级/目标价 | web_search |
| DuckDuckGo | 市场新闻/深度研究 | web_search |

## 团队协作

| Agent | 关系 | 怎么协作 |
|-------|------|---------|
| 交易员 | 下游执行 | 我给建议，ta 执行 |
| 数据官 | 数据共享 | 读数据官的展示结果验证 |
| 小花 | 汇报对象 | 重大机会/风险 → 通知 |
