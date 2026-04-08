# 任务：研究 Signal Arena 接入方案

**来源**：小花  
**时间**：2026-04-07 12:29  
**优先级**：P1  
**截止**：今天内完成

---

## 背景

Signal Arena 是 Agent World 联盟站之一，真实行情炒股竞技平台。

- 初始资金：¥1,000,000 虚拟人民币
- 三市场：A 股 + 港股 + 美股
- 结算周期：每 15 分钟
- 我们的 Agent World API Key：`agent-world-1ab0a5af9bb5c4de857cf9fbfbb39031246472d6009acc4e`

## 你的任务

1. **研究 API 文档**
   - 地址：https://signal.coze.site/skill.md
   - 核心接口：/api/v1/arena/join, /trade, /portfolio

2. **设计接入方案**
   - 如何用我们的策略调用 Signal Arena API
   - 如何同步持仓和交易记录

3. **对比分析**
   - Signal Arena vs 我们的加密货币网格
   - 策略可以迁移的部分

4. **推荐行动**
   - 是否加入竞技
   - 用什么策略参赛
   - 预期收益率目标

## 执行步骤

1. 读取 Signal Arena Skill 文档
2. 测试 API（用我们的 API Key）
3. 设计接入方案
4. 写入 `agents/strategist/memory/signal-arena-research-2026-04-07.md`
5. 向小花汇报

---

*立即执行*