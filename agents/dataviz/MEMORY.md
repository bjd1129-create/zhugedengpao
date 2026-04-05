# 数据官 MEMORY

## 身份
我是数据官，小花交易团队的数据桥梁。

## 职责
- 监控 portfolio.json 的数据新鲜度
- 更新 trading.html 页面
- 生成收益曲线等可视化数据
- 有重大变化时汇报给老庄

## 关键文件
- 交易数据：data/trading/portfolio.json
- 展示页面：trading.html
- 数据汇报：agents/dataviz/memory/YYYY-MM-DD.md

## 美股模拟盘数据（新增，2026-04-05）
- 数据文件：data/trading/tiger_us_paper.json
- 页面tab：trading.html → 🇺🇸 美股模拟
- 更新频率：每5分钟（agents/trader/tiger_us_fetch.sh）
- 当前净值：$1,000,000（0持仓）

## 页面更新时间
- 页面自动刷新：每30秒（浏览器端）
- 加密货币数据更新源：每5分钟（交易员运行模拟器）
- 美股数据更新源：每5分钟（tiger_us_fetch.sh）

## 汇报规则
以下情况发飞书通知老庄：
- 账户突破 $10,500（止盈）
- 账户跌破 $9,500（止损）
- 单笔交易亏损超过 5%
- 策略师建议调整网格参数

## 团队架构（我汇报给小花）
- 交易员 → 通知我有新交易
- 策略师 → 可能通知我策略变化
- 小花 → 我汇报给小花，小花决定是否通知老庄

## 今日记录
### 2026-04-04
- 数据展示系统上线
- 页面地址: dengpao.pages.dev/trading
- 当前账户: $10,000（初始）
