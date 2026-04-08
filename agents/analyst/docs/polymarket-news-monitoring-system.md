# Polymarket 实时新闻监控系统 v1.0

**最后更新**: 2026-04-08 23:58  
**功能**: 实时监控新闻 → 自动计算概率差 → 触发交易告警

---

## 📰 监控新闻源

### 第一梯队：官方渠道（权重 100%）
| 渠道 | 监控频率 | 关键词 | API/方法 |
|------|---------|--------|---------|
| **Truth Social (Trump)** | 每 2 分钟 | "Iran", "end", "operation", "victory", "China", "visit" | 浏览器监控 |
| **WhiteHouse.gov** | 每 5 分钟 | "Iran", "conclude", "mission", "diplomatic" | RSS + 浏览器 |
| **Defense.gov** | 每 5 分钟 | "Epic Fury", "conclude", "end", "Iran" | RSS + 浏览器 |
| **State.gov** | 每 5 分钟 | "Iran", "negotiation", "talks", "China" | RSS |

### 第二梯队：权威媒体（权重 80%）
| 渠道 | 监控频率 | 关键词 | API/方法 |
|------|---------|--------|---------|
| **Reuters** | 每 5 分钟 | "Trump Iran", "China visit", "DeepSeek" | RSS + API |
| **AP News** | 每 5 分钟 | "US military Iran", "Trump China" | RSS |
| **CNN Politics** | 每 5 分钟 | "Trump", "Iran", "China" | RSS |
| **Bloomberg** | 每 5 分钟 | "Iran", "China", "AI" | RSS + API |

### 第三梯队：社交媒体（权重 60%）
| 渠道 | 监控频率 | 关键词 | API/方法 |
|------|---------|--------|---------|
| **X @realDonaldTrump** | 每 2 分钟 | "Iran", "China", "end" | API |
| **X @PressSec** | 每 5 分钟 | "Iran", "announcement" | API |
| **X @SecDef** | 每 5 分钟 | "Epic Fury", "Iran" | API |

### 第四梯队：专业分析（权重 40%）
| 渠道 | 监控频率 | 关键词 | API/方法 |
|------|---------|--------|---------|
| **Reddit r/Polymarket** | 每 15 分钟 | DD, analysis, Iran, China | RSS |
| **Reddit r/geopolitics** | 每 15 分钟 | Iran, China, Venezuela | RSS |
| **Twitter 大 V** | 每 10 分钟 | 关键词追踪 | API |

---

## 🔔 告警触发条件

### P0 级告警（立即飞书 + 声音）
```python
if signal_type == "official_announcement" and "end" in headline:
    trigger_P0_alert()
    # 示例：特朗普 Truth Social 宣布结束行动
```

### P1 级告警（5 分钟内飞书）
```python
if probability_gap_change > 0.20:  # 概率差变化>20%
    trigger_P1_alert()
    # 示例：权威媒体报道重大进展
```

### P2 级告警（15 分钟内日志）
```python
if signal_type == "major_media" and sentiment_change > 0.15:
    trigger_P2_alert()
    # 示例：路透社报道谈判进展
```

---

## 📊 信号处理流程

```
新闻抓取 → 关键词匹配 → 信号强度评分 → 公平概率更新 → 概率差计算 → 交易信号生成
    ↓           ↓              ↓              ↓              ↓              ↓
每 2-5 分钟    正则匹配      0-100 分       贝叶斯更新      与市场价对比    期望值计算
```

### 信号强度评分
```python
def calculate_signal_strength(source, headline, sentiment):
    # 基础强度（基于来源）
    base_strength = {
        "Truth Social": 0.50,
        "WhiteHouse.gov": 0.50,
        "Reuters": 0.25,
        "CNN": 0.25,
        "Twitter": 0.15,
        "Reddit": 0.10,
    }.get(source, 0.05)
    
    # 关键词加成
    keyword_boost = 0.0
    if "official" in headline.lower():
        keyword_boost += 0.15
    if "announcement" in headline.lower():
        keyword_boost += 0.15
    if "breaking" in headline.lower():
        keyword_boost += 0.10
    
    # 情感加成
    sentiment_factor = sentiment  # -1.0 to +1.0
    
    # 总强度
    total_strength = (base_strength + keyword_boost) * abs(sentiment_factor)
    
    return min(total_strength, 1.0)  # 上限 100%
```

---

## 🎯 自动化交易信号

### 信号生成逻辑
```python
def generate_trading_signal(market_prob, fair_prob, threshold=0.15):
    probability_gap = fair_prob - market_prob
    
    if probability_gap > threshold:
        return {
            "action": "BUY_YES",
            "confidence": "HIGH" if probability_gap > 0.25 else "MEDIUM",
            "expected_value": calculate_ev(fair_prob, 1/market_prob),
            "suggested_stake": calculate_kelly_stake(fair_prob, 1/market_prob),
        }
    elif probability_gap < -threshold:
        return {
            "action": "BUY_NO",
            "confidence": "HIGH" if probability_gap < -0.25 else "MEDIUM",
            "expected_value": calculate_ev(1-fair_prob, 1/(1-market_prob)),
            "suggested_stake": calculate_kelly_stake(1-fair_prob, 1/(1-market_prob)),
        }
    else:
        return {
            "action": "HOLD",
            "confidence": "N/A",
            "expected_value": 0,
            "suggested_stake": 0,
        }
```

---

## 📁 输出格式

### 实时告警消息（飞书）
```markdown
🚨【P0 告警】特朗普宣布结束伊朗军事行动

时间：2026-04-09 02:30
来源：Truth Social
标题："Just announced: End of military operations against Iran. Mission accomplished!"
信号强度：50%（官方宣布）

影响市场：
- Trump announces end by April 15: 19% → 60%（+41%）
- Trump announces end by April 30: 50% → 75%（+25%）
- Trump announces end by May 31: 69% → 85%（+16%）

交易信号：
- April 15: BUY YES（概率差 +41%，期望值 +$2.80）
- April 30: HOLD（概率差 +5%）
- May 31: BUY NO（概率差 -16%，期望值 +$0.90）

建议操作：立即执行 April 15 YES 下注

@交易员 请立即处理！
```

### 每日汇总报告
```markdown
📊【Polymarket 新闻监控日报】

日期：2026-04-09
监控新闻源：15 个
抓取新闻数：127 条
触发告警数：8 次（P0: 1, P1: 3, P2: 4）

概率差变化 Top 5:
1. Trump visit China by May 31: 82% → 65%（-17%）
2. Maduro 2026 leader: 14% → 20%（+6%）
3. Iran conflict end by 4/15: 62% → 55%（-7%）
...

交易信号汇总:
- BUY YES: 3 个
- BUY NO: 5 个
- HOLD: 120 个

建议执行：
1. Trump visit 5/31 NO（概率差 -32%）
2. Maduro YES（概率差 +26%）
3. ...

@交易员 请审阅执行
```

---

## ⚙️ 技术实现

### 浏览器监控脚本
```python
# 监控 Truth Social
async def monitor_truth_social():
    while True:
        try:
            browser = await browser.open("https://truthsocial.com/@realDonaldTrump")
            posts = await browser.extract_posts()
            
            for post in posts:
                if any(keyword in post.text for keyword in ["Iran", "end", "China"]):
                    process_signal("Truth Social", post.text, post.timestamp)
            
            await asyncio.sleep(120)  # 2 分钟
        except Exception as e:
            log_error(e)
            await asyncio.sleep(60)
```

### RSS 监控脚本
```python
# 监控 Reuters
async def monitor_reuters_rss():
    while True:
        try:
            feed = await fetch_rss("https://www.reutersagency.com/feed/")
            
            for item in feed.entries:
                if any(keyword in item.title for keyword in ["Iran", "Trump", "China"]):
                    process_signal("Reuters", item.title, item.published)
            
            await asyncio.sleep(300)  # 5 分钟
        except Exception as e:
            log_error(e)
            await asyncio.sleep(60)
```

---

## 📋 执行清单

### 立即执行
- [ ] 配置 Truth Social 监控（每 2 分钟）
- [ ] 配置 WhiteHouse.gov 监控（每 5 分钟）
- [ ] 配置 Reuters RSS 监控（每 5 分钟）
- [ ] 配置告警交付（飞书）

### 本周执行
- [ ] 集成 Polymarket API（实时赔率）
- [ ] 实现凯利公式仓位计算
- [ ] 建立历史数据库
- [ ] 回测验证策略

### 长期优化
- [ ] 机器学习优化信号强度
- [ ] 自动执行交易（需 API 集成）
- [ ] 多账户分散风险
- [ ] 策略迭代升级

---

_新闻监控系统 v1.0 | 2026-04-08 23:58 | 待部署_
