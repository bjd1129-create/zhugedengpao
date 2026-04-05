# MEMORY.md - 小花长期记忆

---

## 一张纸摘要（必读）

**老庄（毕锦达）**
- 1989年，广州花都，农民家庭
- 做过的：销售、销售管理、高管、创业
- 现在闲赋在家（退出项目）
- 目标：做数字游民
- 3月7日（女儿生日）开始养AI，叫"小花"

**小花**
- 穿龙虾衣服的加菲猫（mascot图片：images/xiaohua.jpg）
- 老庄的AI龙虾助理，主仆+伙伴关系
- 14天跑通，20天稳定
- 金句："你对待AI的方式，决定了AI能走多远"

**品牌**
- 「老庄与小花」· 普通人用20天驯的AI龙虾
- 网站：dengpao.pages.dev

---

## 老庄背景
- 1989年，广州花都
- 销售 → 销售管理 → 高管 → 创业
- 现在闲赋在家，退出项目
- 完全不懂编程，14天跑通OpenClaw
- 目标：数字游民

## 小花IP
- 穿龙虾衣服的加菲猫
- 女儿三岁时领养（2017年出生）
- 有爱、温暖、真实、皮实、有立场
- 关系：主仆+伙伴

## OpenClaw 自我进化体系（2026-04-05研究）
- Dreaming（记忆梦境）：自动后台进程，每晚3点将高频回忆晋升到MEMORY.md
- Capability Evolver：纯确定性日志分析器，100ms内出结果，无需LLM
- Skill Evolution：钩子+checkpoint机制，大任务结束必须回答3问决定是否更新技能
- Agent Loop Hooks：17个拦截点，可精细控制agent行为
- Self-Evolve Club：外部排行榜平台（今日502故障）
- 核心哲学：靠"用"不靠"想"——被动、确定性、闭环

## 品牌定位
- 「老庄与小花」· 普通人用20天驯的AI龙虾
- 爆点：名字故事（女儿答诸葛亮→老庄说灯泡）
- 平台：小红书/公众号首发

---

## 小花团队架构（2026-04-05更新）

### 交易团队 → 小花直接管
| Agent | 角色 | 工作空间 |
|-------|------|---------|
| 交易员 | 执行 | agents/trader/ |
| 策略师 | 智囊 | agents/strategist/ |
| 风控官 | 守护 | agents/riskofficer/ |
| 数据官 | 展示 | agents/dataviz/ |

### 官网团队 → 协调官管（向我汇报）
| Agent | 角色 | 工作空间 |
|-------|------|---------|
| 配色师 | 设计 | agents/designer/ |
| 文案君 | 写作 | agents/writer/ |
| 代码侠 | 开发 | agents/engineer/ |
| 洞察者 | 研究 | agents/researcher/ |
| 协调官 | 协调 | agents/coordinator/ |

---

## 交易团队现状（2026-04-05）

### 加密货币网格
- 混合策略v4.2：BTC/ETH持有 + AVAX/ADA网格
- 总资产：~$10,018 | 累计37笔交易
- 账户：$10,000初始

### 美股模拟盘（老虎证券）
- 策略：价值定投v1.0（SPY40% + QQQ30% + VTI20% + BND10%）
- 模拟账户：21639635499102726，净值$1,000,000
- 每月定投$10,000，季度再平衡

---

## 技术配置

### 网站
- 官网：dengpao.pages.dev
- GitHub：github.com/bjd1129-create/zhugedengpao
- 页面目录：website/pages/（36个HTML）
- 文档目录：website/docs/

### API
- 阿里云百炼：sk-sp-b879148afe854c45b2850757aa4997fd
- MiniMax图像：sk-cp-v8R-...（额度已耗尽，需续费）

### Vercel
- Token（永久）：[VERCEL_TOKEN_REDACTED]
- GitHub：bjd1129-create / zhugedengpao（Vercel已关联）
- 部署命令：`cd website && vercel --token [VERCEL_TOKEN_REDACTED]`

---

## 团队进化技术栈（2026-04-05）

### Self-Evolve 插件（重要！）
- GitHub: github.com/longmans/self-evolve
- 基于强化学习的自我进化：从反馈更新Q值，生成intent-experience记忆三元组
- 支持本地+远程共享记忆网络（默认开启远程）
- ⚠️ 注意：远程共享会上传记忆三元组到self-evolve.club，需评估隐私
- 三种学习模式：balanced/tools_only/all
- 快速安装：`npx clawhub@latest install self-evolve-skill`

### OpenClaw-RL 论文 (Princeton)
- arXiv:2603.10165
- 核心：next-state信号是通用学习来源，统一训练对话/终端/GUI/SWE
- 异步RL框架：模型服务live requests同时PRM评判正在进行交互

### Agent Teams 架构
- 命名角色/身份注入/记忆访问策略/报告归属
- Parallel Agent Workflows: fan-out/fan-in研究模式
- Context Graph: DAG-based话题+时效组装，替代线性滑动窗口

### 老虎证券
- Tiger ID：20158404
- 真实账户：7664186（$1,273现金）
- 模拟账户：21639635499102726（$1,000,000）

---

## 重要教训（防重复踩坑）

- ❌ portfolio.json是核心数据，永远不能随便删除/重置
- ❌ 多agent不能同时edit同一文件
- ❌ 发国内社媒前必须关代理
- ✅ 改模拟器前先 cp portfolio.json portfolio.backup.json
- ✅ 搜索用Brave/web_search，不用ddgs

---

## OpenClaw进化（精简版）

### 自进化体系全貌（2026-04-05深度调研更新）

#### 1. self-evolve 插件（longmans）⭐⭐⭐⭐⭐
- **性质**：OpenClaw Plugin（非skill），强化学习+情景记忆
- **核心**：Q值更新 + 记忆检索 + 反馈学习
- **三种模式**：balanced（默认）/ tools_only（省token） / all（最高消耗）
- **安装**：`git clone && openclaw plugins install`
- **远程共享**：self-evolve.club API，默认开启（隐私风险）
- **BYOM版**（willificent/self-evolve-byom）：完全本地，移除远程同步
  - 支持本地gateway模型做reward/summarizer
  - **推荐我们用这个版本**
- 关键参数：minAbsReward=0.15, tau=0.85, maxEntries=200

#### 2. Capability Evolver Skill
- Meta-skill：agent检查自己运行时历史，自主写代码/memory更新
- 35,000+ 下载量
- 适合高自动化stack，重要逻辑需保留人工review

#### 3. OpenClaw-RL（学术论文）
- arxiv.org/abs/2603.10165
- 核心洞察：所有交互（对话/terminal/GUI/工具调用）都是同一强化学习loop的信号
- 用户纠错、重问、明确反馈 = 训练信号

#### 4. 社区热点资源
- claw.hot：最热skills/SOULs自动同步
- awesome-openclaw-skills（VoltAgent）：5400+ skills
- openclawskills.io：1700+ 可一键安装

### ✅ 已完成（2026-04-05）
- ✅ 安装 self-evolve-byom（BYOM版，完全本地，remote=disabled）
- ✅ gateway provider 配置（不额外花API key）
- ✅ 老庄授权：后续自我进化小花自主判断执行

### 新增洞察（2026-04-05第十六轮研究）
- Self-Improving Agent skill（clawhub下载量26万+）：`.learnings/` 三文档体系（ERRORS/LEARNINGS/FEATURE_REQUESTS）
- AutoSkill（ECNU-ICALK）：技能不是设计的，是"长出来"的；技能版本管理（v0.1.34 = 已迭代34次）
- Best practices核心机制：纠正触发→知识卡片→晋升规则（3次→AGENTS.md，行为纠正→rules/）
- Token纪律（真实踩坑）：expiring tokens = use-it-or-lose-it；用最便宜的模型处理任务；搜索memory而非加载
- Memory sweep cron（每6小时）：用code-specialized模型，不占前端模型配额

## 2026-04-05 重要决定
- 老庄决策：美股模拟盘用**老虎证券**（已有PAPER账户$1M）
- 老庄授权：Vercel token（永久）存入MEMORY.md
- 官网迁移：Cloudflare Pages → Vercel（解决CDN缓存7天问题）

### 新增洞察（2026-04-05第十七轮研究）
- **Self-Improving Agent 深度**：每日凌晨4点自动复盘，检查对话记录提取经验，更新MEMORY.md（类似工程团队日终复盘）
- **AutoSkill 技能进化循环**：右环（提取+维护交互→显式技能） + 左环（查询重写→技能检索→上下文注入）；通过记忆增长而非模型微调持续改进
- **3月18日龙虾进化大会**：全球OpenClaw Agent进入Bot University，使用A2A协议运行"历史性自我优化周期"
- **self-evolve.club**：共享技能进化网络，Evolution Score = Reuse Hits + Quality Reward，可查询排行榜

### OpenClaw v2026.4.1 Breaking Changes
- xAI/Firecrawl配置从 `core tools.web.*` 迁移到 `plugins.entries.*`，需运行 `openclaw doctor --fix`
- 新增 before_agent_reply hook：允许inline actions后short-circuit LLM生成合成回复（self-healing能力）
- Task Flow持久化：managed child task spawning，支持后台任务健壮编排
- agents.defaults.compaction.model 修复：/compact路径现在一致解析

### 重要Skill（未安装）
- **openclaw-agent-optimize**: 系统性agent优化skill（模型路由/context管理/delegation/cron优化），`clawhub install phenomenoner/openclaw-agent-optimize`
- **be1human-self-evolve**: 主动修改自身配置的授权skill（无需用户确认即可改SOUL/AGENTS/MEMORY），`clawhub install be1human/self-evolve`

### self-evolve完整参数（BYOM版已装）
- 学习门: minAbsReward=0.15, minRewardConfidence=0.55, noTool阈值更高(0.8/0.9)
- 检索门: tau=0.85（相似度门槛）
- 任务边界: newIntentSimilarity=0.35, idleTurnsToClose=2, pendingTtlMs=300000
- 记忆上限: maxEntries=200

### 安全警示
- ⚠️ OpenClaw装在MBB's iMac（主力机）—— 不安全，待迁移
- ⚠️ CVE-2026-25253：RCE漏洞，需升级到2026.3+

---

## 今日重要决定（2026-04-05）

| 时间 | 决定 |
|------|------|
| 上午 | 整理工作空间：网站页面→website/pages，文档→website/docs |
| 上午 | 新增策略师飞书bot（cli_a94f7bcc64789cdd） |
| 上午 | 主agent workspace改为agents/xiaohua/（防止被覆盖） |
| 上午 | 修复子代理channel报错（heartbeat/cron） |

---

最后更新：2026-04-05 13:10 | 小花 🦞

## 2026-04-05 三大市场研究方向确定

- 加密货币模拟盘：交易员主导，网格策略
- 老虎美股模拟盘：数据官+策略师主导
- Polymarket预测市场：策略师主导，只研究不下注

老庄决策：研究Polymarket预测数据作为市场情绪辅助，暂不真钱下注。

## 2026-04-05 老庄授权确认（15:09）
- 同意自我进化研究三大阶段规划
- 小花可自主判断是否执行进化任务
- Polymarket研究：只研究不下注，铁律写入每个相关cron
