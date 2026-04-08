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

### 6. 向小花汇报（如有重大发现）
发 sessions_send 通知小花：
- 异常品种
- 数据依据
- 建议行动

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
