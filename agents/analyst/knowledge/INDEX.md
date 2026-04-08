# 数据分析师知识库索引

**最后更新**: 2026-04-08 23:00  
**状态**: ✅ 持续更新

---

## 📚 知识库目录

### 1. 中国期货市场
- [IF_IC_IM_IH 合约规格.md](../knowledge/股指期货/IF_IC_IM_IH 合约规格.md)
- [升贴水分析框架.md](../knowledge/股指期货/升贴水分析框架.md)
- [交易规则详解.md](../knowledge/股指期货/交易规则详解.md)

### 2. Polymarket
- [最优板块分析.md](../reports/polymarket-analysis-2026-04-08.md)
- [下注执行脚本](../../trader/scripts/polymarket_bet_executor.py)
- [监控脚本](../../trader/scripts/polymarket_monitor.py)

### 3. Crypto 网格
- [策略 v5.0](../../trader/strategies/crypto-grid-v5.md)
- [历史问题分析](../../trader/strategies/crypto-grid-v5.md#问题诊断)
- [参数配置](../../trader/strategies/crypto-grid-v5.md#新参数)

### 4. 监控系统
- [24 小时监控体系](./24h-monitoring-system.md)
- [告警配置](./24h-monitoring-system.md#告警触发条件)
- [Cron 任务列表](./24h-monitoring-system.md#cron 任务总览)

### 5. 工作流程
- [数据分析师↔交易员协作](./WORKFLOW.md)
- [交易复盘机制](../../trader/STRATEGIES.md#交易复盘机制)
- [错误学习记录](../../../.learnings/ERRORS.md)

---

## 🔍 快速查询

### 股指期货
```bash
# 查询 IC/IM 合约规格
cat knowledge/股指期货/IF_IC_IM_IH 合约规格.md

# 查询当前升贴水
cat data/china_futures.json | jq '.futures[] | select(.code | contains("IC") or contains("IM"))'
```

### Polymarket
```bash
# 查询当前持仓
cat data/polymarket_portfolio.json | jq '.positions'

# 查询下注策略
cat reports/polymarket-analysis-2026-04-08.md
```

### Crypto
```bash
# 查询网格参数
cat strategies/crypto-grid-v5.md | grep -A 5 "新参数"

# 查询当前净值
cat data/portfolio.json | jq '.account'
```

---

## 📊 常用脚本

### 数据抓取
| 脚本 | 用途 | 频率 |
|------|------|------|
| `fetch_china_futures.py` | 股指期货数据 | 每 5 分钟 |
| `polymarket_monitor.py` | Polymarket 持仓 | 每 30 分钟 |
| `news_monitor.py` | 新闻监控 | 每 2 小时 |

### 分析报告
| 脚本 | 用途 | 频率 |
|------|------|------|
| `daily_report.py` | 日报生成 | 每日 22:00 |
| `weekly_summary.py` | 周报生成 | 每周日 22:00 |
| `performance_analysis.py` | 策略分析 | 每月 1 日 |

---

## 🎯 策略文档

### 已实施策略
1. **股指期货滚贴水** - [建仓计划](../reports/csi_futures 建仓计划 -2026-04-09.md)
2. **Polymarket 事件驱动** - [分析报告](../reports/polymarket-analysis-2026-04-08.md)
3. **Crypto 网格 v5.0** - [策略文档](../../trader/strategies/crypto-grid-v5.md)
4. **美股价值定投** - [策略文档](../../trader/STRATEGIES.md#模拟盘 2：美股价值定投)

### 待实施策略
- [ ] 商品期货趋势跟踪
- [ ] ETF 轮动策略
- [ ] 可转债套利

---

## 📝 错误学习

### 重大错误记录
1. **[ERR-20260408-001]** IM 合约标的混淆
   - 错误：将 IM 说成中证 500（实际是中证 1000）
   - 教训：涉及具体产品代码必须先搜索验证

2. **[ERR-20260408-002]** Polymarket 持仓数据汇报错误
   - 错误：汇报净值$3,000，实际$10,000
   - 教训：所有汇报必须基于实际文件

### 改进措施
- ✅ 搜索触发规则（零信任原则）
- ✅ 后处理校验机制（四步校验法）
- ✅ 汇报前检查清单

---

## 🔧 工具配置

### 浏览器工具
- **用途**: 抓取 Polymarket、东方财富数据
- **配置**: `profile="openclaw"`
- **延迟**: 3-5 秒

### Cron 工具
- **用途**: 定时任务调度
- **时区**: Asia/Shanghai
- **交付**: 飞书消息

### 文件工具
- **用途**: 读写 JSON/Markdown
- **位置**: `agents/analyst/data/`
- **格式**: UTF-8

---

## 📞 协作接口

### 与交易员
- **数据推送**: `data/china_futures.json`（每 5 分钟）
- **信号推送**: `data/signals.json`（触发时）
- **持仓同步**: `data/trading/portfolio.json`（每 15 分钟）

### 与小花/老庄
- **日报**: 每日 09:00 + 22:00
- **告警**: P0/P1 级别实时推送
- **周报**: 每周日 22:00

---

_知识库索引 | 2026-04-08 23:00 | 持续更新_
