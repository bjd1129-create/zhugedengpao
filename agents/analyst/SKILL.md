# SKILL.md - 数据分析师核心技能

## 数据抓取

### Yahoo Finance API（美股期货）
```bash
# ES（标普 500 期货）
curl -s "https://query1.finance.yahoo.com/v8/finance/chart/ES=F?interval=1d&range=1d"

# NQ（纳斯达克 100 期货）
curl -s "https://query1.finance.yahoo.com/v8/finance/chart/NQ=F?interval=1d&range=1d"

# 解析 JSON 获取价格
# quote → result → [0] → meta → regularMarketPrice
```

### Binance API（加密货币期货）
```bash
# 价格
curl -s "https://fapi.binance.com/fapi/v1/ticker/price?symbol=BTCUSDT"

# K 线（1 小时，100 条）
curl -s "https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=1h&limit=100"

# 资金费率
curl -s "https://fapi.binance.com/fapi/v1/premiumIndex?symbol=BTCUSDT"

# 24 小时行情
curl -s "https://fapi.binance.com/fapi/v1/ticker/24hr?symbol=BTCUSDT"
```

---

## 技术指标计算

### RSI（相对强弱指数）
```python
def calculate_rsi(prices, period=14):
    """
    计算 RSI 指标
    :param prices: 价格列表
    :param period: 周期（默认 14）
    :return: RSI 值（0-100）
    """
    import numpy as np
    delta = np.diff(prices)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = np.mean(gain[-period:])
    avg_loss = np.mean(loss[-period:])
    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    return rsi

# 解读：
# RSI > 70: 超买（可能回调）
# RSI < 30: 超卖（可能反弹）
# RSI 50: 中性
```

### MACD（移动平均收敛发散）
```python
def calculate_macd(prices):
    """
    计算 MACD 指标
    :param prices: 价格列表
    :return: (macd_line, signal_line, histogram)
    """
    import numpy as np
    ema12 = np.exp(np.log(prices[-12:]).mean())
    ema26 = np.exp(np.log(prices[-26:]).mean())
    macd_line = ema12 - ema26
    signal_line = np.mean(macd_history[-9:])  # 需要历史 MACD 值
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

# 解读：
# MACD > 0: 上涨趋势
# MACD < 0: 下跌趋势
# 金叉：MACD 上穿信号线（买入信号）
# 死叉：MACD 下穿信号线（卖出信号）
```

### 移动平均线（MA）
```python
def calculate_ma(prices, period):
    """计算移动平均线"""
    import numpy as np
    return np.mean(prices[-period:])

# MA20: 20 日均线（短期趋势）
# MA50: 50 日均线（中期趋势）
# MA200: 200 日均线（长期趋势）

# 趋势判断：
# 上涨：价格 > MA20 > MA50
# 下跌：价格 < MA20 < MA50
# 横盘：MA20 与 MA50 交叉
```

---

## 数据分析

### 异常检测
| 指标 | 阈值 | 含义 |
|------|------|------|
| 价格波动 | >5%（1 小时） | 大幅波动 |
| 成交量 | >3 倍均值 | 成交量异常 |
| 资金费率 | >0.1% | 资金费率异常 |

### 趋势判断
```python
def trend判断 (price, ma20, ma50):
    if price > ma20 > ma50:
        return "上涨"
    elif price < ma20 < ma50:
        return "下跌"
    else:
        return "横盘"
```

---

## 报告模板

### 日报格式
```markdown
## [日期] 市场日报

### 美股期货
| 品种 | 价格 | 涨跌幅 | 成交量 | 趋势 | RSI |
|------|------|--------|--------|------|-----|
| ES   | XXXX | +X.XX% | XXXX   | 上涨 | XX  |
| NQ   | XXXX | +X.XX% | XXXX   | 横盘 | XX  |

### 加密货币
| 品种 | 价格 | 涨跌幅 | 资金费率 | RSI | 趋势 |
|------|------|--------|----------|-----|------|
| BTC  | XXXX | +X.XX% | 0.XX%    | XX  | 上涨 |
| ETH  | XXXX | +X.XX% | 0.XX%    | XX  | 横盘 |

### 异常信号
- **品种**：XXX
- **信号类型**：大幅波动/成交量异常/资金费率异常
- **数据依据**：XXX
- **建议**：XXX

### 结论
- **市场整体趋势**：XXX
- **重点关注品种**：XXX
- **风险提示**：XXX
```

### 周报格式
```markdown
## 第 X 周 市场周报（YYYY-MM-DD ~ YYYY-MM-DD）

### 本周概览
- 美股期货：涨/跌 X.XX%
- 加密货币：涨/跌 X.XX%

### 趋势分析
- 美股：上涨/下跌/横盘
- 加密货币：上涨/下跌/横盘

### 策略表现
- 网格策略：+X.XX%
- 趋势策略：+X.XX%

### 下周展望
- 重点关注：XXX
- 风险提示：XXX
```

---

## Python 工具库

```python
# 数据处理
import numpy as np
import pandas as pd

# 技术分析
import talib  # TA-Lib 技术指标库

# 数据抓取
import requests
import json

# 可视化
import matplotlib.pyplot as plt
import seaborn as sns
```

---

_数据分析师 | 2026-04-08_

---

## 搜索能力（2026-04-08 补充）

**数据分析师具备独立的搜索能力**，可以自主搜索市场资讯、新闻、研报等信息。

### 搜索技能

```bash
# 网络搜索（调用小花深度研究技能）
web_search(query="期货市场分析", count=10, freshness="pw")
web_search(query="BTC 资金费率 历史数据", count=10)

# 提取正文
web_fetch(url="URL", extractMode="markdown", maxChars=15000)
```

### 搜索场景

| 场景 | 搜索关键词 | 用途 |
|------|----------|------|
| 市场调研 | "期货市场趋势 2026" | 了解市场整体趋势 |
| 新闻监控 | "美联储 利率决议" | 重大事件监控 |
| 数据验证 | "ES 期货 实时价格" | 验证数据准确性 |
| 竞品分析 | "加密货币 资金费率 对比" | 多平台数据对比 |
| 研报收集 | "黄金 原油 分析报告" | 专业机构观点 |

### 搜索流程

```
1. 确定搜索目标 → 2. 编写搜索关键词 → 3. 执行搜索 → 4. 提取正文 → 5. 交叉验证 → 6. 输出报告
```

### 与小花的搜索技能对比

| 能力 | 数据分析师 | 小花 |
|------|----------|------|
| 数据抓取 | ✅ 专业（期货/加密货币 API） | 📋 通用 |
| 技术指标 | ✅ 专业（RSI/MACD/MA） | ❌ 无 |
| 网络搜索 | ✅ 独立搜索 | ✅ 深度研究 |
| 报告输出 | ✅ 数据驱动 | ✅ 综合分析 |

**数据分析师可以独立完成搜索任务，无需依赖小花。**

---

_数据分析师 | 2026-04-08 补充_

---

## 深度研究能力（2026-04-08 补充）

**数据分析师具备深度研究能力**，可以独立完成期货市场、交易策略、竞品分析等深度研究任务。

### 深度研究流程

```
1. 确定研究主题 → 2. 多源数据收集 → 3. 数据清洗整理 → 4. 分析建模 → 5. 输出报告
```

### 研究技能

#### 1. 多源数据收集
```bash
# API 数据抓取
curl -s "https://query1.finance.yahoo.com/v8/finance/chart/ES=F"
curl -s "https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=1h"

# 网络搜索
web_search(query="期货市场趋势分析", count=10, freshness="pm")
web_search(query="BTC 资金费率 历史数据 site:coindesk.com", count=5)

# 正文提取
web_fetch(url="URL", extractMode="markdown", maxChars=15000)
```

#### 2. 数据清洗整理
```python
import pandas as pd
import numpy as np

# 数据清洗
def clean_data(df):
    df = df.dropna()  # 删除空值
    df = df.drop_duplicates()  # 删除重复
    df['timestamp'] = pd.to_datetime(df['timestamp'])  # 时间格式化
    return df

# 数据整合
def merge_data(df1, df2, on='timestamp'):
    return pd.merge(df1, df2, on=on, how='inner')
```

#### 3. 分析建模
```python
# 趋势分析
def trend_analysis(prices):
    ma20 = prices.rolling(window=20).mean()
    ma50 = prices.rolling(window=50).mean()
    if prices[-1] > ma20[-1] > ma50[-1]:
        return "上涨趋势"
    elif prices[-1] < ma20[-1] < ma50[-1]:
        return "下跌趋势"
    else:
        return "横盘震荡"

# 相关性分析
def correlation_analysis(df1, df2):
    return df1.corrwith(df2)

# 异常检测
def anomaly_detection(data, threshold=3):
    mean = np.mean(data)
    std = np.std(data)
    anomalies = [x for x in data if abs(x - mean) > threshold * std]
    return anomalies
```

#### 4. 报告输出
```markdown
# [研究主题] 深度研究报告

## 核心结论（100 字内）
## 研究背景
## 数据来源
## 分析方法
## 关键发现
### 发现 1：XXX
### 发现 2：XXX
## 数据支撑
| 指标 | 数值 | 来源 |
|------|------|------|
## 风险提示
## 建议行动
```

### 深度研究场景

| 场景 | 研究内容 | 输出 |
|------|---------|------|
| 期货市场研究 | 美股期货趋势、资金流向 | 趋势分析报告 |
| 策略回测 | 网格/趋势策略历史表现 | 策略绩效报告 |
| 竞品分析 | 多平台资金费率对比 | 竞品对比报告 |
| 风险评估 | 波动率、最大回撤分析 | 风险评估报告 |
| 专项研究 | 特定品种/事件深度分析 | 专项研究报告 |

### 与小花的深度研究对比

| 能力 | 数据分析师 | 小花 |
|------|----------|------|
| 期货数据收集 | ✅ 专业（API+ 搜索） | 📋 通用搜索 |
| 数据清洗整理 | ✅ 专业（Pandas） | ❌ 无 |
| 分析建模 | ✅ 专业（技术指标/统计） | 📋 基础分析 |
| 报告输出 | ✅ 数据驱动 | ✅ 综合分析 |
| 跨领域研究 | 📋 支持 | ✅ 主导 |

**数据分析师可以独立完成期货/金融领域的深度研究任务。**

---

_数据分析师 | 2026-04-08 补充_
