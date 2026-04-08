# Polymarket 策略回测框架 v1.0

**最后更新**: 2026-04-08 23:55  
**目的**: 验证概率差策略的历史表现  
**方法**: 基于历史数据回测

---

## 📊 回测目标

### 核心问题
1. **概率差策略是否有效？**
2. **最佳概率差阈值是多少？**（15%? 20%? 25%?）
3. **历史胜率是多少？**（目标>60%）
4. **最佳仓位配置是多少？**

### 回测指标
| 指标 | 目标值 | 说明 |
|------|--------|------|
| 胜率 | >60% | 盈利交易数 / 总交易数 |
| 期望值 | >$0.5/$1 | 平均每$1 下注的收益 |
| 夏普比率 | >1.5 | 风险调整后收益 |
| 最大回撤 | <-20% | 最大连续亏损 |
| 盈亏比 | >2:1 | 平均盈利 / 平均亏损 |

---

## 🔧 回测方法

### 数据收集
```python
# 需要收集的历史数据
historical_data = {
    "market_id": "市场 ID",
    "question": "市场问题",
    "outcome": "选项（YES/NO）",
    "timestamp": "下注时间",
    "market_prob": "市场定价概率",
    "fair_prob": "公平概率（基于新闻信号计算）",
    "probability_gap": "概率差",
    "odds": "赔率",
    "bet_amount": "下注金额",
    "result": "结果（WIN/LOSS）",
    "payout": "收益",
    "resolution_date": "决议日期",
}
```

### 回测策略
```python
# 策略 1: 固定概率差阈值
def strategy_fixed_threshold(probability_gap, threshold=0.15):
    if probability_gap > threshold:
        return "BUY_YES"
    elif probability_gap < -threshold:
        return "BUY_NO"
    else:
        return "HOLD"

# 策略 2: 动态阈值（基于市场流动性）
def strategy_dynamic_threshold(probability_gap, volume):
    if volume > 10_000_000:  # 高流动性
        threshold = 0.15
    elif volume > 1_000_000:  # 中等流动性
        threshold = 0.20
    else:  # 低流动性
        threshold = 0.25
    
    if probability_gap > threshold:
        return "BUY_YES"
    elif probability_gap < -threshold:
        return "BUY_NO"
    else:
        return "HOLD"

# 策略 3: 凯利公式仓位
def kelly_stake(fair_prob, odds, bankroll):
    # f* = (p * b - q) / b
    # p = 公平概率，b = 赔率 -1, q = 1-p
    p = fair_prob
    b = odds - 1
    q = 1 - p
    
    kelly_fraction = (p * b - q) / b
    kelly_fraction = max(0, min(kelly_fraction, 0.25))  # 限制 0-25%
    
    return bankroll * kelly_fraction
```

---

## 📈 回测场景

### 场景 1: 伊朗相关市场（2026 年 4 月）
```python
# 测试数据（基于当前市场）
test_markets_ir = [
    {
        "market": "Trump announces end by April 15",
        "market_prob": 0.19,
        "fair_prob": 0.30,
        "probability_gap": +0.11,
        "odds": 5.26,  # 1/0.19
        "recommended_action": "BUY_YES",
        "expected_value": +0.43,
    },
    {
        "market": "Trump announces end by April 30",
        "market_prob": 0.50,
        "fair_prob": 0.50,
        "probability_gap": 0.00,
        "odds": 2.00,
        "recommended_action": "HOLD",
        "expected_value": 0.00,
    },
    {
        "market": "Trump announces end by May 31",
        "market_prob": 0.69,
        "fair_prob": 0.45,
        "probability_gap": -0.24,
        "odds": 1.45,
        "recommended_action": "BUY_NO",
        "expected_value": +1.26,
    },
]
```

### 场景 2: 委内瑞拉市场
```python
test_markets_venezuela = [
    {
        "market": "Maduro leader end of 2026",
        "market_prob": 0.14,
        "fair_prob": 0.40,
        "probability_gap": +0.26,
        "odds": 7.14,
        "recommended_action": "BUY_YES",
        "expected_value": +2.40,
    },
]
```

### 场景 3: 特朗普访华市场
```python
test_markets_china_visit = [
    {
        "market": "Trump visit by May 31",
        "market_prob": 0.82,
        "fair_prob": 0.50,
        "probability_gap": -0.32,
        "odds": 1.22,
        "recommended_action": "BUY_NO",
        "expected_value": +2.10,
    },
    {
        "market": "Trump visit by June 30",
        "market_prob": 0.87,
        "fair_prob": 0.60,
        "probability_gap": -0.27,
        "odds": 1.15,
        "recommended_action": "BUY_NO",
        "expected_value": +1.80,
    },
]
```

---

## 📊 预期回测结果

### 策略表现预测
| 策略 | 胜率 | 期望值 | 夏普比率 | 最大回撤 |
|------|------|--------|---------|---------|
| 固定阈值 15% | 65% | +$1.20 | 1.8 | -15% |
| 固定阈值 20% | 70% | +$1.50 | 2.1 | -12% |
| 固定阈值 25% | 75% | +$1.80 | 2.5 | -10% |
| 动态阈值 | 68% | +$1.40 | 2.0 | -13% |
| 凯利公式 | 65% | +$2.00 | 2.3 | -18% |

### 最佳参数预测
- **概率差阈值**: 20-25%（胜率与交易频率平衡）
- **单笔仓位**: 5-10%（凯利公式优化）
- **总仓位**: 50-70%（分散风险）
- **止损线**: -20%（总账户）

---

## 🔍 回测验证步骤

### 步骤 1: 收集历史数据
- [ ] Polymarket 历史市场数据（API 或手动收集）
- [ ] 决议结果（WIN/LOSS）
- [ ] 历史赔率变化
- [ ] 成交量数据

### 步骤 2: 计算公平概率
- [ ] 基于新闻信号强度
- [ ] 基于时间衰减
- [ ] 基于市场流动性调整

### 步骤 3: 执行回测
- [ ] 应用不同策略
- [ ] 记录每笔交易结果
- [ ] 计算各项指标

### 步骤 4: 优化参数
- [ ] 测试不同阈值（15%、20%、25%、30%）
- [ ] 测试不同仓位（固定 vs 凯利）
- [ ] 测试不同止损线

### 步骤 5: 生成报告
- [ ] 策略对比
- [ ] 参数敏感性分析
- [ ] 最佳策略推荐

---

## 📁 输出文件

### 回测报告模板
```markdown
# Polymarket 策略回测报告

**回测期间**: 2026-01-01 至 2026-04-08
**初始资金**: $10,000
**最终资金**: $XX,XXX
**总收益**: +XX%

## 策略表现
| 策略 | 胜率 | 期望值 | 夏普比率 | 最大回撤 |
|------|------|--------|---------|---------|
| 固定 15% | XX% | +$X.XX | X.X | -XX% |

## 最佳参数
- 概率差阈值：XX%
- 单笔仓位：XX%
- 总仓位：XX%

## 建议
1. ...
2. ...
3. ...
```

---

## ⚠️ 回测局限性

1. **样本量有限**: Polymarket 历史数据有限
2. **幸存者偏差**: 已决议市场可能不代表全部
3. **流动性假设**: 假设能按市价进出（实际可能有滑点）
4. **新闻信号回溯**: 历史新闻信号难以精确还原

---

_回测框架 v1.0 | 2026-04-08 23:55 | 待数据收集_
