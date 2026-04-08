# TOOLS.md - 数据分析师工具配置

## 数据源 API

### Yahoo Finance（美股期货）
- **API**：`query1.finance.yahoo.com`
- **品种**：ES=F（标普 500）、NQ=F（纳斯达克 100）
- **代理**：不需要
- **限流**：无严格限制

```bash
# 示例请求
curl -s "https://query1.finance.yahoo.com/v8/finance/chart/ES=F?interval=1d&range=1d"
```

### Binance（加密货币期货）
- **API**：`fapi.binance.com`
- **品种**：BTCUSDT、ETHUSDT 等
- **代理**：需要（`{"https":"http://127.0.0.1:7897"}`）
- **限流**：IP 限流，注意频率

```bash
# 示例请求
curl -s "https://fapi.binance.com/fapi/v1/ticker/price?symbol=BTCUSDT"
curl -s "https://fapi.binance.com/fapi/v1/premiumIndex?symbol=BTCUSDT"
```

### Alpha Vantage（商品期货）
- **API**：`www.alphavantage.co`
- **品种**：黄金、原油（待配置）
- **API Key**：待配置
- **限流**：5 次/分钟（免费版）

---

## Python 环境

```bash
# 虚拟环境（复用交易员环境）
/Users/bjd/.venv/tiger/bin/python

# 依赖库安装
pip install numpy pandas requests ta-lib

# TA-Lib 安装（需要先安装系统库）
brew install ta-lib
pip install TA-Lib
```

---

## 数据存储

### 目录结构
```
agents/analyst/
├── data/
│   ├── futures_prices.json       # 期货价格
│   ├── technical_indicators.json # 技术指标
│   └── reports/                  # 研究报告
│       ├── weekly-2026-W15.md    # 周报
│       └── special-xxx.md        # 专项研究
└── memory/
    └── YYYY-MM-DD.md             # 每日日志
```

### JSON 数据结构
```json
{
  "update_time": "2026-04-08T09:42:00+08:00",
  "futures": {
    "ES": {
      "price": 5123.50,
      "change_pct": 0.25,
      "volume": 123456,
      "trend": "上涨",
      "rsi": 55.2
    },
    "NQ": {
      "price": 18234.75,
      "change_pct": 0.50,
      "volume": 234567,
      "trend": "横盘",
      "rsi": 48.5
    }
  },
  "crypto": {
    "BTC": {
      "price": 67500.00,
      "change_pct": 1.20,
      "funding_rate": 0.0001,
      "rsi": 62.3,
      "trend": "上涨"
    },
    "ETH": {
      "price": 2050.00,
      "change_pct": 0.80,
      "funding_rate": 0.0002,
      "rsi": 58.1,
      "trend": "横盘"
    }
  }
}
```

---

## 工具脚本（待创建）

| 脚本 | 用途 | 状态 |
|------|------|------|
| `fetch_futures.py` | 抓取期货价格 | 🔴 待创建 |
| `calculate_indicators.py` | 计算技术指标 | 🔴 待创建 |
| `scan_signals.py` | 扫描异常信号 | 🔴 待创建 |
| `generate_report.py` | 生成日报/周报 | 🔴 待创建 |

---

## Git 配置

- **工作目录**：`/Users/bjd/Desktop/ZhugeDengpao-Team`
- **分支**：main
- **提交规范**：`analyst: 描述`
- **权限**：只能提交 `agents/analyst/` 目录

---

## 权限隔离（2026-04-08 起）

| Agent | analyst/权限 | 说明 |
|-------|------------|------|
| 数据分析师 | ✅ 完全控制 | 读/写/删除 |
| 小花 | ✅ 完全控制 | 主 Agent，拥有所有权限 |
| 交易员 | 📋 只读 | 可以查看研究报告 |
| 协调官 | ❌ 无权限 | 只能分配任务 |
| 工程师 | ❌ 无权限 | 只能接收数据可视化 |

---

_数据分析师 | 2026-04-08_
