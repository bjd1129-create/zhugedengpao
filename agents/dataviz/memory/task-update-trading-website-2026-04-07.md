# 任务：更新官网交易页面（3 个模拟盘）

**来源**：小花  
**时间**：2026-04-07 12:43  
**优先级**：P0  
**截止**：今天内完成

---

## 背景

老庄要求：将 3 个模拟盘的数据都更新到 https://dengpao.pages.dev/trading

## 三个模拟盘

| 模拟盘 | 数据文件 | 状态 |
|--------|---------|------|
| 加密货币网格 | `data/trading/portfolio.json` | ⚠️ 数据为$0，需交易员更新 |
| 美股模拟盘 | `data/trading/tiger_us_paper.json` | ✅ 有行情数据，API 认证待修复 |
| Polymarket | `data/trading/polymarket_data.json` | ✅ 已更新（12:11） |

## 你的任务

1. **整合三个模拟盘数据**
   - 读取三个数据文件
   - 计算总资产（加密货币 + 美股 + Polymarket 虚拟注）

2. **更新 trading.html 数据**
   - 检查当前页面是否支持三平台展示
   - 如需修改，更新 HTML/JS

3. **推送更新到 GitHub**
   - 提交更改
   - 触发 Cloudflare Pages 部署

4. **验证部署**
   - 访问 https://dengpao.pages.dev/trading
   - 确认三个模拟盘数据正确显示

## 执行步骤

1. 等待交易员更新 portfolio.json（加密货币网格恢复运行）
2. 读取三个数据文件，整合数据
3. 检查 trading.html 是否需要修改
4. 提交并推送
5. 验证部署结果
6. 写入 `agents/dataviz/memory/website-update-2026-04-07.md`
7. 向小花汇报

---

*立即执行*