# LangGraph交易系统 + Polymarket API 研究

**日期**：2026-04-07 | 小花 🦞

---

## 一、LangGraph交易开源项目

### 1. TradingAgents-Dashboard
- 用LangGraph构建的AI交易助手
- 结合Obsidian做本地知识库（RAG）
- 支持记住历史分析
- **参考价值**：状态机设计模式

### 2. Top LangGraph开源项目
- deer-flow（多Agent协作）
- agent-service-toolkit（生产级Agent服务框架）
- GenAI_Agents
- **参考价值**：这些偏通用框架，不是专用交易系统

### 3. LangGraph核心概念
- 状态机 = 图（Graph） + 节点（State） + 边（Edge）
- 每个节点是一个"Action"或"Agent"
- 边是条件分支，决定下一步去哪
- **适合交易的原因**：天然适合"分析→决策→执行→反馈"循环

---

## 二、Polymarket API（重大发现！）

### 官方API存在！
- **Gamma API**: `gamma-api.polymarket.com`
- **CLOB API**: 订单簿
- **Data API**: 市场数据

### Python库
```
pip install polymarket-apis
```
支持：Markets, events, tags, series, comments, sports, search

### 关键发现
之前策略师说"Polymarket数据抓不到"是**错的**——可以用官方API获取，只是需要API Key或匿名访问。

---

## 三、交易决策状态机设计

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class TradingState(TypedDict):
    market_data: dict
    signal: str  # BUY / SELL / HOLD
    confidence: float
    action_taken: bool

def analyze(state: TradingState) -> TradingState:
    """策略师节点：分析市场数据"""
    rsi = calculate_rsi(state['market_data'])
    trend = detect_trend(state['market_data'])
    
    if rsi > 70:
        return {'signal': 'SELL', 'confidence': 0.8}
    elif rsi < 30:
        return {'signal': 'BUY', 'confidence': 0.7}
    else:
        return {'signal': 'HOLD', 'confidence': 0.5}

def execute(state: TradingState) -> TradingState:
    """交易员节点：执行信号"""
    if state['action_taken']:
        return state
    # 调用Tiger API下单
    return state

def check_stop_loss(state: TradingState) -> str:
    """风控节点：检查是否触发止损"""
    if portfolio_value < STOP_LOSS * initial_value:
        return 'liquidate'  # 触发止损，全部平仓
    return 'continue'

# 构建图
graph = StateGraph(TradingState)
graph.add_node("analyze", analyze)
graph.add_node("execute", execute)
graph.add_node("check_risk", check_stop_loss)

# 条件边
graph.add_conditional_edges(
    "analyze",
    check_stop_loss,
    {'liquidate': "execute", 'continue': "execute"}
)
graph.add_edge("execute", END)

app = graph.compile()
```

---

## 四、与现有系统集成

### 保留的组件
| 组件 | 用途 | 保留原因 |
|------|------|---------|
| tiger_us_fetch.sh | 数据抓取 | crontab驱动，稳定 |
| tiger_api.py | 交易执行 | Tiger官方SDK |
| trading_simulator.py | 账户管理 | 已验证 |
| portfolio.json | 状态存储 | 文件系统 |

### 新增的组件
| 组件 | 用途 |
|------|------|
| polymarket_api.py | 官方API获取市场数据 |
| trading_state_machine.py | LangGraph决策状态机 |
| strategies/market_analyzer.py | 技术指标计算 |

### Polymarket机会识别流程
```
1. polymarket_api.py 获取热门市场列表
2. 分析赔率异动（对比历史均值）
3. 找出偏差>15%的市场
4. 生成信号：HIGH_CONF / MEDIUM / LOW
5. 小花确认后，策略师生成研究报告
6. 老庄决策是否下注
```

---

## 五、结论与行动

### 短期可行（1周内）
1. **Polymarket API接入** → pip install polymarket-apis，立即可用
2. **技术指标自动化** → RSI/MACD写入trading_state_machine.py
3. **状态机轻量版** → 不用完整LangGraph，用Python字典+条件分支

### 中期（1个月）
1. **完整LangGraph状态机** → 策略师/交易员/数据官的决策自动化
2. **历史回测** → 验证网格策略有效性
3. **Polymarket高频扫描** → 每小时扫描一次，识别异动

### 不建议做的
- 内幕消息（合规问题）
- 短线择时（AI无法可靠预测）
- 脱离人的决策（必须有老庄确认）

---

## 六、最快落地路径

**现在就能做的（今天）：**
1. 安装polymarket-apis：pip install polymarket-apis
2. 测试官方API获取市场数据
3. 更新策略师SKILL.md

**不需要LangGraph**：先用简单的Python脚本实现，发现瓶颈后再考虑引入状态机。
