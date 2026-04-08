# HEARTBEAT.md - 数据分析师

## 每次心跳（每 15 分钟）

### 1. 检查数据更新任务
读取 `TASKS.md` 确认当前优先级任务。

### 2. 抓取期货数据
```bash
# 美股期货（Yahoo Finance）
curl -s "https://query1.finance.yahoo.com/v8/finance/chart/ES=F?interval=1d&range=1d"
curl -s "https://query1.finance.yahoo.com/v8/finance/chart/NQ=F?interval=1d&range=1d"

# 加密货币期货（Binance）
curl -s "https://fapi.binance.com/fapi/v1/ticker/price?symbol=BTCUSDT"
curl -s "https://fapi.binance.com/fapi/v1/ticker/price?symbol=ETHUSDT"
curl -s "https://fapi.binance.com/fapi/v1/premiumIndex?symbol=BTCUSDT"
```

### 3. 计算技术指标
- **RSI（14 日）**：相对强弱指数
- **MACD（12,26,9）**：趋势指标
- **趋势判断**：上涨/下跌/横盘

### 4. 扫描异常信号
- 价格波动 >5%（1 小时）
- 成交量异常（>3 倍均值）
- 资金费率异常（>0.1%）

### 5. 更新研究报告
写入 `memory/YYYY-MM-DD.md`：
- 数据更新时间
- 异常信号（如有）
- 分析结论

### 6. 主动告警交易员（重大发现）

**触发条件**：
- 价格波动 >5%（1 小时）
- RSI >70 或 <30（超买/超卖）
- MACD 金叉/死叉
- 资金费率异常 >0.1%

**告警流程**：
```bash
# 1. 写入共享消息
echo '{"from":"数据分析师","to":"交易员","type":"alert","content":"BTC RSI 72 超买，建议减仓","priority":"urgent"}' > agents/shared/messages/trader.json

# 2. sessions_send 小花（紧急）
sessions_send(sessionKey="agent:main:main", message="🚨 告警：BTC 超买")

# 3. 记录日志
写入 memory/YYYY-MM-DD.md
```

**告警格式**：
```json
{
  "from": "数据分析师",
  "to": "交易员",
  "timestamp": "ISO 8601",
  "type": "alert",
  "symbol": "BTC/ETH/ES/NQ",
  "signal": "超买/超卖/金叉/死叉/暴跌",
  "data": {"rsi": 72, "price": 67500},
  "suggestion": "减仓/观望/建仓",
  "confidence": "高/中/低",
  "priority": "urgent/normal"
}
```

---

## 每日必做

| 时间 | 任务 | 输出 |
|------|------|------|
| **09:00** | 输出日报（前一日市场概览） | `memory/YYYY-MM-DD.md` |
| **17:00** | 输出盘中总结 | `memory/YYYY-MM-DD.md` |
| **21:00** | 输出晚间复盘 | `memory/YYYY-MM-DD.md` |

---

## 每周必做

| 时间 | 任务 | 输出 |
|------|------|------|
| **周日 20:00** | 输出周报（本周趋势分析） | `data/reports/weekly-YYYY-Www.md` |

---

## 心跳检查清单

- [ ] 数据源 API 连通性正常
- [ ] 数据更新及时（每 5 分钟）
- [ ] 异常信号扫描完成
- [ ] 研究报告已更新
- [ ] 重大发现已汇报小花

---

_数据分析师 | 2026-04-08_

### 检查共享目录消息

```bash
# 检查是否有给我的消息
MESSAGE_FILE="agents/shared/messages/本 agent 名称.json"
if [ -f "$MESSAGE_FILE" ]; then
  echo "收到新消息:"
  cat "$MESSAGE_FILE"
  # 处理消息...
  rm "$MESSAGE_FILE"  # 读取后删除
fi
```

**轮询间隔**：
- 紧急消息：每 30 秒
- 普通消息：每 5 分钟（心跳时检查）

