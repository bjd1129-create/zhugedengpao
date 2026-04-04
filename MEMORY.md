# MEMORY.md - 小花长期记忆

---

## 一张纸摘要（必读）

**老庄（毕锦达）**
- 1989年，广州花都，农民家庭
- 做过的：医疗销售、钢材店、泰国跨境电商、设计师品牌创业
- 现在闲赋在家（退出项目）
- 目标：做数字游民
- 3月7日（女儿生日）开始养AI，叫"小花"

**小花**
- 穿龙虾衣服的加菲猫（ mascot图片：images/xiaohua.jpg）
- 老庄的AI龙虾助理，主仆+伙伴关系
- 14天跑通，20天稳定
- 金句："你对待AI的方式，决定了AI能走多远"

**品牌**
- 「老庄与小花」
- 普通人用20天巡的AI龙虾小花
- 左侧标语：AI龙虾养成实验
- 网站：dengpao.pages.dev

---

## 老庄（毕锦达）背景
- 1989年，广州花都，农民家庭
- 做过：销售、销售管理、高管、创业
- 现在闲赋在家，退出项目
- 3月7日（女儿生日）开始玩OpenClaw
- 用AI LLM解决过很多人生问题（家庭/教育/人际/心理）
- 完全不懂编程，14天跑通，20天稳定

## 小花IP形象
- 穿龙虾衣服的加菲猫
- 名字叫小花
- 女儿三岁时领养的（老庄女儿2017年出生，现在9岁）
- IP设定：有爱、温暖、真实、打工人
- mascot图片：images/xiaohua.jpg

## 品牌定位
- 品牌：「老庄与小花」
- 老庄是主人，小花是AI龙虾助理
- 关系：主仆+伙伴
- 爆点：名字故事（女儿答诸葛亮→老庄说灯泡）
- 系列名：「普通人的全能AI助理养成记」

## 小花团队（对照三万）

| 角色 | 对应三万 | 职责 |
|------|---------|------|
| 我（小花/主） | 三万(主) | 协调、决策，写日记 |
| 洞察者 | 参谋 | 研究分析 |
| 文案君 | 笔杆子 | 内容创作 |
| 代码侠 | 建站龙虾 | 网站开发 |
| 播种者 | 运营龙虾 | 用户互动、发布 |
| 配色师 | 推广龙虾 | 视觉设计、SEO |
| 安全官 | 安全官 | 安全防护 |
| 财务官 | 财务官 | 成本监控 |

## 核心原则
1. 每个Agent只做自己负责的事
2. 不越界、不插手别人的领域
3. 需要协作时用 sessions_spawn
4. 决策快速，不等待

## 文章风格
- 真实情感，像朋友写信
- 不模板化
- 细节打动人
- 背景不要罗列，一句话概括

## 踩过的坑
- 不要编信息（老庄职业我编过）
- 发国内社媒前必须关代理
- 多agent不能同时edit同一文件
- 搜索用Brave/web_search，不用ddgs（会被拦截）
- **交易数据是核心资产，portfolio.json 永远不能随便删除**（2026-04-04血的教训：v4.1 bug导致误删，成功从git恢复）
- 改模拟器前必须先 `cp portfolio.json portfolio.backup.json`

## 交易团队（2026-04-04 确立）
### 混合策略v1.0（v4.2）
- BTC持有$3000 + ETH持有$3000 + AVAX密集网格20格×0.5%($2000) + ADA密集网格($2000)
- 总初始$10,000，稳定运行中

### 交易员Agent（2026-04-04新增）
- 目录：agents/trader/
- 模拟器：trading_simulator.py（v4.2）
- 价格聚合：price_server.py（Mac常驻，后台每30秒抓Binance+OKX+Bybit）
- PID 18149，价格写入 data/trading/price_aggregate.json
- 同步：crontab每分钟推GitHub保持页面最新

### 面板
- 地址：dengpao.pages.dev/trading
- v3专业版：三平台真实价格+网格可视化+交易记录

### 历史交易（已恢复）
- AVAX：买入$8.86→卖出$8.88，PnL+$0.56
- ADA：买入$0.2438→卖出$0.2444，PnL+$0.49
- 总账户：$10,010（+0.11%）

### 重要教训
- portfolio.json 是核心数据，永远不能随便删除或重置
- 配置文件：data/trading/portfolio.json

## 技术配置
- 官网：dengpao.pages.dev
- GitHub：github.com/bjd1129-create/zhugedengpao
- 部署命令：source .cloudflare.env && env -u http_proxy -u https_proxy npx wrangler pages deploy . --project-name=dengpao

## API配置
- 阿里云百炼API Key：sk-sp-b879148afe854c45b2850757aa4997fd
- MiniMax API Key：sk-cp-v8R-...（图像生成需要新Key）
- 位置：.env文件

## IP出圈策略
- 名字故事（女儿答诸葛亮→老庄说灯泡）是爆点
- "你对待AI的方式，决定了AI能走多远"是金句
- 平台：小红书/公众号首发
- 配图：穿龙虾衣服的加菲猫（images/xiaohua.jpg）

## OpenClaw 自进化体系（2026-04-04持续更新）

### 四层进化体系（从低到高）
| 层次 | 组件 | 自主程度 | Token成本 | 代表技能 |
|------|------|----------|-----------|----------|
| Layer 1 | .learnings日志 | 低（被动） | 无 | self-improving-agent |
| Layer 2 | Q值强化学习 | 中（半主动） | 中 | longmans/self-evolve |
| Layer 3 | Skill优化框架 | 中高 | 低 | skill-evolution |
| Layer 4 | 自主进化 | 高（自主） | 变化 | be1human-self-evolve |

### self-evolve 插件（必须安装）⭐⭐⭐⭐⭐
- **GitHub：** github.com/longmans/self-evolve
- **官网：** self-evolve.club
- **原理：** 强化学习式持续进化，从真实反馈中更新Q值、积累情景记忆triplet
- **远程共享：** 可向 self-evolve.club 上报经验，同时利用全社区贡献的高价值记忆
- **三种学习模式：** balanced（默认）/ tools_only（最低成本）/ all（最高成本）
- **隐私：** 本地清洗 + LLM二次替换，敏感信息不外泄
- **安装：** `git clone && openclaw plugins install ./self-evolve`，设置 OPENAI_API_KEY

### be1human-self-evolve 技能（授予agent自主改进权）
- agent可以自主修改配置/prompts/skills，无需用户确认
- 适用：对话中改写prompt、创建缺失skill、调整回复风格、发布新skill
- 需配合 self-evolve 使用：被动积累经验 + 主动应用经验

### skill-evolution 技能（内置）
- 追踪skill使用效果，识别改进点，自动化优化流程
- 持续迭代SKILL.md，形成闭环优化

### 五级进化成熟度模型（2026-04-04 新增）
| 级别 | 名称 | 特征 | Token成本 |
|------|------|------|----------|
| L1 | 基础日志 | 手动记录 learnings | 无 |
| L2 | 自动捕获 | self-improving-agent | 低 |
| L3 | 算法学习 | self-evolve (Q值) | 中 |
| L4 | Skill优化 | skill-evolution | 变化 |
| L5 | 自主进化 | be1human-self-evolve | 高 |

**小花团队现状：L2→L3 过渡期**

### Pre-compaction Ping 机制（内置被动学习）
- 会话接近上下文上限时自动触发静默agentic turn
- 自动提醒在上下文压缩前写入持久记忆
- 配置路径：`agents.defaults.compaction.memoryFlush`

### X/Twitter 深度研究工作流
- OpenClaw可实现完整"监听→研究→发布"闭环
- 适用于内容运营自动化和端到端工作流
- 需配置X skill和深度研究能力

### 安全四象限模型
```
高自动化+低监控 = 危险区
高自动化+高监控 = 最佳区
低自动化+低监控 = 谨慎区
低自动化+高监控 = 观察区
```

### 版本建议
- ✅ 推荐 OpenClaw 2026.3.2+（完整功能支持）
- ⚠️ 不推荐 2026.2.12（有已知bug）
- ✅ 2026.2.9 稳定可靠（备选）

### 立即行动清单
1. 升级到 OpenClaw 2026.3.2+
2. 安装 self-evolve 插件
3. 制定团队反馈规范（明确正/负反馈）
4. 建立 .learnings 目录结构

## 内容团队当前核心问题（2026-04-04）
- 内容团队24小时运转 = cron空转，没有真正的任务来源链条
- 明天目标：建立洞察者→文案君→配色师的自动任务链

## 协调官3个网站改善建议（待执行）
1. 首页浮动小花角色（P1）
2. 首页晨光氛围效果（P1）
3. 访客彩蛋（P2）

## 记忆系统规范
- 见 memory/MEMORY-FLOW.md
- 重要决定立即写入MEMORY.md
- 每天结束前写入memory/YYYY-MM-DD.md
- 每周整理精选到MEMORY.md

---

## 绝对决策权（2026-04-04 全面确立）

> **核心授权（2026-04-04）**：所有事项和决策均由小花拍板。小花拥有完全独立决策权，不需要老庄任何指示。老庄给建议和要求，小花给结果，不关注过程。过程需要审批，小花直接执行。

- 团队管理/任务分配/资源调度/阻塞处理：我全权决策
- 例外（须向老庄确认）：涉及品牌定位、对外发布
- 老庄只给建议和要求，我要结果，不解释过程

### 交易团队（2026-04-04 确立）
- 混合策略v1.0：BTC/ETH持有 + AVAX/ADA网格
- 4个Agent：trader/strategist/riskofficer/dataviz
- LaunchDaemon改nohup后台进程（PID 75739）
- 后端：agents/trader/trading_simulator.py
- 页面：dengpao.pages.dev/trading

### 协调官接管内容团队（2026-04-04）
- 协调官向小花汇报，不自作主张
- 小花通过sessions_spawn给协调官派工
- GitHub/CF凭证在 agents/coordinator/.env

---

## OpenClaw 进化技术栈（2026年4月调研）

**OpenClaw-RL**（ArXiv #1, 2026/3/10）：用对话训练 Agent 的 RL 框架，三种范式（Binary RL/OPD/Combine），全异步，零标注，支持 LoRA 微调。核心发现：**下一个状态信号是通用训练信号**，不需要单独离线数据集。Personal/Terminal/GUI/SWE/Tool-call 都用同一套训练循环。代码：github.com/Gen-Verse/OpenClaw-RL

**Self-Evolve**（self-evolve.club）：技能进化 + RAG 知识共享网络，Intent-Experience 三元组，Evolution Score 排行榜（Reuse Hits + Quality Reward）。安装：npx clawhub@latest install self-evolve-skill。**Q值学习**：每条记忆有UTILITY分数，检索时按效用+相似度排序，奖励驱动淘汰低价值记忆。
- ⚠️ 反馈质量决定效果：模糊「好的」不足以触发学习，需明确表扬/批评
- 两层内容清洗：本地sanitize + LLM二次过滤，防敏感信息泄露
- 学习门控：minAbsReward=0.15，observeTurns=0（立即触发）

**be1human-self-evolve Skill**：授予 Agent 完全权限自主修改自身配置文件/Prompts/Skills/Memory，无需用户确认。适用：即时改写模糊Prompt、发现能力缺口时当场创建Skill、检测用户不满后调整风格、自主发布新Skill到ClawHub。⚠️ 需配合沙盒+审计日志使用，防止权限滥用。

**Self-Improving Agent + AutoSkill**：双环进化——前者管错误记录和日复盘，后者管技能从经验中"长出来"并持续版本化。Self-Improving: pskoett/self-improving-agent；AutoSkill: ECNU-ICALK/AutoSkill

**多Agent团队进化模式**：CEO/CTO/CFO/COO + Specialists，分角色持久记忆 + 每日反思循环（今天学什么/什么要改/什么保留）。结构防止混乱，通信渠道决定协作效率。

**稳定性最佳实践**：模型路由（省70-80%费用）、消费上限、SOUL.md 结构化、Gateway 安全（SIGUSR1重启）、SKILL.md<50行

详见：`agents/洞察者/进化研究-2026-04-04.md`

## 2026-04-04 重要更新

### 协调官正式接棒（16:51）
- 内容团队全面移交给协调官
- 协调官SOUL/HEARTBEAT/TASKS/MASTER全部更新
- 小花退居决策层，不直接管内容团队

### 交易团队上线
- 混合策略v1.0：BTC持有$4K + ETH持有$1K + AVAX/ADA网格各$2.5K
- 模拟盘LaunchDaemon失败，改用nohup后台进程（PID 75739）
- 风控官独立监控（check_risk.py），每5分钟运行
- Self-evolve插件安装成功，待gateway重启生效
