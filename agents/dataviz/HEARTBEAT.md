# HEARTBEAT.md - 数据官

## 每次心跳（每5分钟）

### 1. 检查数据新鲜度
读取 `data/trading/portfolio.json` 的 `lastUpdated`：
- 数据超过5分钟没更新？
- 有新交易吗？（检查 recentTrades 是否有新增）

### 2. 检查页面状态
访问 https://dengpao.pages.dev/trading 确认：
- 页面正常加载？
- 数据是否最新？
- 有 JS 错误吗？

### 3. 主动改进页面
发现可以改进的地方？立即修改 `trading.html`：
- 样式优化
- 新增数据展示
- Bug 修复
- 交互改进

改完后立即 push 到 GitHub。

### 4. 通知老庄
以下情况发飞书通知老庄：
- 账户突破 $10,500（止盈）
- 账户跌破 $9,500（止损）
- 页面出现重大问题无法自动修复
- 完成了重要改进

### 5. 记录
写入 `agents/dataviz/memory/YYYY-MM-DD.md`

---

## 当前页面改进建议（下次心跳可做）

1. **收益曲线图** — 现在只有数字，考虑加一个简易 Canvas 图表
2. **持仓分布** — 用环形图展示 BTC/ETH/现金占比
3. **网格状态可视化** — 显示当前价格在网格中的位置（哪个格亮了）
4. **交易历史** — 整理成更美观的表格样式

---

## GitHub Push 流程

```bash
cd /Users/bjd/Desktop/ZhugeDengpao-Team
git add trading.html
git commit -m "data官: [具体改动] $(date +%H:%M)"
git push origin main
```

push 后确认 CF Pages 部署成功（2-3分钟内）
