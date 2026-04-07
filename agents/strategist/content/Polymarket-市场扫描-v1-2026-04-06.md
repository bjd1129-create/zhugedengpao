# Polymarket 市场扫描报告 v1

**报告类型**: 第一轮 - 市场扫描  
**生成时间**: 2026-04-06 22:22 UTC  
**数据源**: Polymarket 热门市场页面  
**铁律**: 只研究，不下注

---

## 一、热门市场 TOP20（按总成交量排序）

| 排名 | 市场名称 | 总成交量 | 24h成交量 | 流动性 | 当前最热选项 | 概率 | 到期时间 |
|------|----------|----------|-----------|--------|--------------|------|----------|
| 1 | Democratic Presidential Nominee 2028 | $992M | $9M | $47M | Gavin Newsom | 24% | 2年以上 |
| 2 | Republican Presidential Nominee 2028 | $525M | $4M | $33M | J.D. Vance | 38% | 2年以上 |
| 3 | 2026 FIFA World Cup Winner | $517M | $10M | $83M | Spain | 16% | 3个月 |
| 4 | Presidential Election Winner 2028 | $495M | $3M | $30M | JD Vance | 18% | 2年以上 |
| 5 | 2026 NBA Champion | $233M | $3M | $8M | Oklahoma City Thunder | 40% | 3个月 |
| 6 | US forces enter Iran by..? | $198M | $39M | $5M | (未显示) | 100% | 12月31日 |
| 7 | US x Iran ceasefire by...? | $103M | $10M | $2M | (未显示) | 76% | 12月31日 |
| 8 | F1 Drivers' Champion | $85M | $2M | $11M | George Russell | 44% | 8个月 |
| 9 | Eurovision Winner 2026 | $72M | $3M | $13M | Finland | 37% | 约1个月 |
| 10 | The Masters - Winner | $71M | $4M | $7M | Scottie Scheffler | 15% | 6天 |
| 11 | Fed decision in April? | $56M | $2M | $4M | No change | 98% | 22天 |
| 12 | Next Prime Minister of Hungary | $49M | $2M | $2M | Péter Magyar | 66% | 5天 |
| 13 | Who will Trump talk to in March? | $16M | $4M | $2M | Xi Jinping | <1% | - |
| 14 | Elon Musk # tweets March 31-April 7 | $11M | $2M | $2M | 260-279 | 61% | 约18小时 |
| 15 | WTI Crude Oil April 2026 | $9M | $2M | $1M | ↓ $110 | 91% | 23天 |
| 16 | Iran military action by March 31? | $7M | $2M | $3M | UAE | 100% | - |
| 17 | Connecticut vs. Michigan (NCAA) | $3M | $3M | $5M | Michigan | 74% | 约2小时 |
| 18 | LoL: Vitality vs KOI | $3M | $3M | $639K | Team Vitality | 100% | 约1小时 |
| 19 | Pistons vs. Magic (NBA) | $2M | $2M | $2M | Pistons | 54% | 37分钟 |
| 20 | Cavaliers vs. Grizzlies (NBA) | $2M | $2M | $2M | Cavaliers | 89% | 约2小时 |

---

## 二、24h 价格异动识别（成交量异常）

### 🚨 高异动市场（24h成交量 / 总成交量 > 15%）

| 市场 | 24h占比 | 异常原因分析 |
|------|---------|--------------|
| **US forces enter Iran by..?** | **19.7%** ($39M/$198M) | 地缘政治突发事件，资金大量涌入 |
| **Who will Trump talk to in March?** | **25%** ($4M/$16M) | 可能有新消息/传闻驱动 |
| **Connecticut vs. Michigan** | **100%** ($3M/$3M) | 即将开赛（2小时内），临场资金 |
| **LoL: Vitality vs KOI** | **100%** ($3M/$3M) | 即将开赛（1小时内），临场资金 |
| **Pistons vs. Magic** | **100%** ($2M/$2M) | 即将开赛（37分钟），临场资金 |
| **Cavaliers vs. Grizzlies** | **100%** ($2M/$2M) | 即将开赛（2小时内），临场资金 |

### ⚠️ 中等异动市场（24h成交量 > $5M）

| 市场 | 24h成交量 | 备注 |
|------|-----------|------|
| Democratic Presidential Nominee 2028 | $9M | 正常政治市场活跃度 |
| 2026 FIFA World Cup Winner | $10M | 体育大赛，持续热度 |
| US x Iran ceasefire | $10M | 与伊朗局势联动 |

---

## 三、本轮新发现

### 1. 地缘政治市场资金集中度极高
- **伊朗相关市场**占据 TOP20 中的 3 席（#6、#7、#16）
- "US forces enter Iran" 24h成交量$39M，是其他政治市场的 4-10 倍
- 市场隐含概率：进入伊朗 100%、停火 76%、军事行动对 UAE 100%
- **解读**: 资金认为中东局势升级几乎是确定性事件

### 2. 2028 美国大选市场已提前升温
- 4 个相关市场进入 TOP20，总成交量超 $2T
- 共和党方面 J.D. Vance 领先（38%），民主党 Gavin Newsom 领先（24%）
- **解读**: 距离大选还有 2 年多，但资金已开始布局，可能存在早期错误定价

### 3. 体育赛事临场交易特征明显
- 即将开赛的比赛 24h成交量 = 总成交量（100%）
- 这说明 Polymarket 体育市场以短期投机为主，非长期配置
- **对比**: FIFA 世界杯、NBA 总冠军等长期市场 24h占比仅 2-5%

### 4. The Masters 高尔夫锦标赛即将截止
- 距离结束仅 6 天，Scottie Scheffler 以 15% 领先
- 总成交量$71M，24h $4M，热度持续
- **待验证**: 赛前最后几天的价格波动规律

---

## 四、待验证问题（下轮研究必须回答）

### 问题 1: 伊朗局势市场的错误定价机会
- **观察**: "US forces enter Iran" 定价 100%，但地缘政治真有 100% 确定的事吗？
- **待验证**: 
  - 历史类似地缘政治市场的最终结算概率分布
  - 100% 定价是否意味着套利空间（如反向做空）
  - 与伊朗相关的其他市场（停火、军事行动）是否存在逻辑矛盾

### 问题 2: 2028 大选早期市场的预测有效性
- **观察**: 距离大选 2 年多，J.D. Vance 38%、Gavin Newsom 24%
- **待验证**:
  - 历史数据：提前 2 年的预测市场准确率 vs 提前 3 个月
  - 当前价格与博彩公司赔率、民调数据的偏差
  - 是否存在"名气溢价"（Newsom 媒体曝光度高）

### 问题 3: Polymarket 作为情绪指标的有效性
- **观察**: 伊朗市场 24h 成交量$39M，远超其他政治市场
- **待验证**:
  - 成交量激增是否领先于传统媒体报道？
  - 与 BTC/ETH 价格走势的相关性（风险情绪联动）
  - 能否作为"恐慌指数"的替代指标

### 问题 4: 临场体育市场的套利规律
- **观察**: 赛前 1-2 小时成交量占 100%
- **待验证**:
  - 赛前 1 小时 vs 赛前 1 分钟的价格波动幅度
  - 是否存在"最后时刻反转"规律
  - 流动性在临场时是否足以支持大资金进出

---

## 五、下轮研究方向建议

基于本轮扫描，建议第二轮（机会识别）优先分析：

1. **伊朗相关市场深度对比** - 3 个市场之间是否存在逻辑矛盾/套利空间
2. **2028 大选错误定价分析** - 对比民调、博彩赔率，找出偏差>15% 的选项
3. **The Masters 赛前价格走向** - 6 天倒计时，每日价格变化规律

---

**报告完成** | 下一轮：机会识别（每日 9:00/21:00 自动执行）  
**数据局限性**: 仅抓取页面显示数据，未调用 API 获取历史价格序列
