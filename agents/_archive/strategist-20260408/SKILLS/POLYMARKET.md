# SKILL: Polymarket深度研究框架

## 研究流程

```
1. 获取热门市场 → 按成交量排序，取Top20
2. 筛选有价值的 → 过滤低流动性/过于模糊的市场
3. 深度搜索 → 用英文关键词搜索相关报道
4. 独立概率判断 → 不看市场定价，先自己算
5. 对比偏差 → 偏差>15%标记为候选
6. 写报告 → 按模板输出，给出建议
```

---

## Step 1: 获取热门市场

```bash
curl -s "https://gamma-api.polymarket.com/markets?limit=50&closed=false" | python3 -c "
import sys,json
data=json.load(sys.stdin)
by_vol=sorted(data,key=lambda x:float(x.get('volume24hr',0)),reverse=True)
for m in by_vol[:20]:
    p=json.loads(m.get('outcomePrices','[]'))
    vol=float(m.get('volume24hr',0))
    if vol > 5000:  # 过滤低流动性
        print(f'[\${vol:,.0f}] {m[\"question\"][:70]}')
        print(f'  YES={float(p[0]):.1%} NO={float(p[1]):.1%}' if len(p)==2 else '')
        print(f'  URL: https://polymarket.com/event/{m.get(\"slug\",\"\")}')
        print()
"
```

---

## Step 2: 深度搜索（核心）

**搜索技巧：**
- 用英文搜英文，结果更准
- 针对事件搜新闻、专家分析、历史数据
- 找"为什么市场定价是这样"的理由

**搜索模板：**
```bash
# 格式
web_search: "<事件关键词> Polymarket analysis"
web_search: "<事件关键词> news today"
web_search: "<事件关键词> probability prediction"
web_search: "site:polymarket.com <关键词>"
```

**BTC相关：**
```
web_search: "Bitcoin price prediction 2026 analysis"
web_search: "BTC ETF inflow data 2026"
web_search: "Bitcoin market cycle analysis"
```

**地缘政治：**
```
web_search: "US Iran military action 2026"
web_search: "Middle East conflict probability analysis"
```

**体育/娱乐：**
```
web_search: "<球队> 2026 season record prediction"
web_search: "GTA VI release date 2026"
```

---

## Step 3: 独立概率分析

**不看市场定价，先自己算。问自己：**

1. **背景是什么？** 事件的来龙去脉
2. **支持YES的证据？** 列出3-5个理由
3. **支持NO的证据？** 列出3-5个理由
4. **我的判断是什么？** 不参考市场，给一个0-100%的数字
5. **我为什么觉得市场错了？** 或者没意见？

---

## Step 4: 研究模板

```
【Polymarket市场分析】
URL: https://polymarket.com/event/xxx
问题：<核心问题>
市场定价：YES=<X>% NO=<Y>%
流动性：<$L>

【深度研究】
1. 背景：<事件背景>
2. 支持YES的证据：
   - <证据1>
   - <证据2>
3. 支持NO的证据：
   - <证据1>
   - <证据2>
4. 我的概率判断：YES=<A>% NO=<B>%

【对比分析】
- 我的判断：<A>%
- 市场定价：<X>%
- 偏差：<A-X>%（正=我比市场乐观，负=我比市场悲观）
- 结论：【有机会BET NO】【有机会BET YES】【无机会】

【风险提示】
<地缘政治/突发新闻等不可预测因素>
```

---

## Step 5: 判断标准

| 偏差范围 | 结论 | 仓位建议 |
|---------|------|---------|
| >+20% | 市场低估了NO | 轻仓BET NO |
| >+15% | 市场可能低估NO | 观察 |
| -15%~+15% | 无明显偏差 | 不下注 |
| <-15% | 市场高估了YES | 轻仓BET YES |
| <-20% | 市场严重高估了YES | 考虑稍大仓位 |

**仓位原则：** 总资金5-10%，不重仓

---

## 注意事项

1. **预测市场不是水晶球** — 90%概率不等于90%会发生
2. **时间衰减** — 越接近事件日期，概率会快速调整
3. **流动性风险** — 低流动性市场可能有操纵
4. **地缘政治无法预测** — 权重放低
5. **研究≠赌博** — 有优势才下注，没优势就观望

---

_策略师 Polymarket 研究技能 | 2026-04-07_
