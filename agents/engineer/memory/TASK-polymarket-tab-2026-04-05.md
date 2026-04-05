# 紧急任务 | 2026-04-05 15:12

**来源**：小花（老庄直接指令）
**优先级**：P0
**截止**：尽快完成

---

## 任务：改造 trading.html Polymarket Tab

**背景**：
Polymarket 要从"只读展示预测"改成"我们的第三个模拟盘"——研究 → 决策 → 模拟买卖 → 结果展示，全流程。

**数据文件（已完成）**：
- `data/trading/polymarket_portfolio.json` — 模拟账户数据

**改造内容**：

### 1. 顶部账户总览（account-grid 样式）
- 账户现金
- 持仓市值
- 总净值
- 已实现PnL

### 2. 改造"热门预测"区块 → "我的预测持仓"
每条预测显示：
- 问题（question）
- 市场概率（market_probability）
- 我们的判断（our_assessment）
- 我们给的概率（our_probability）
- 状态（researching=🟡/持仓=🟢/平仓=🔴）
- 当前盈亏（pnl）

### 3. 底部交易记录表
- 时间、预测问题、方向(BUY/SELL)、金额、结果、盈亏

### 4. JS改动
- 改读 `polymarket_portfolio.json`（原来是 `polymarket_data.json`）
- 30秒刷新
- 新增 `renderPolyPortfolio(data)` 函数

**参考**：`website/pages/trading.html` 现有 usSection 和 cryptoSection 的样式

---

完成后 git push，然后发消息给小花确认（sessions_send）。
