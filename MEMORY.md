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

## 分工机制（2026-04-05确立）

### 新工具/策略上线时 → 我必须立即同步到相关Agent
1. 新工具/策略上线 → 立即更新相关Agent的SOUL.md + MEMORY.md
2. 用 sessions_spawn 或 sessions_send 通知相关Agent有新上下文
3. 相关Agent确认收到并更新自己的知识库

### Cron任务 → 必须绑定到对应Agent的session
- ✅ 正确：cron → `agent:trader` 的isolated session
- ❌ 错误：cron → `agent:main:main`（会堆积到主agent）
- 每个Agent的cron都要绑定到自己的sessionKey

### Agent执行层 → 我不自己做，执行交给子Agent
- 我 = 决策者、协调者、汇报者
- 子Agent = 执行者
- 我不做执行层的工作（除非子Agent不可用）

### 汇报规则
- 无特殊情况 → 1小时汇报一次
- 阈值触发（止损/止盈/重大变化）→ 实时告警
- 无进展 → 静默，不发无意义汇报

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

## 老虎证券API（2026-04-04接入）
- SDK：tigeropen 3.5.7（虚拟环境 ~/.venv/tiger）
- tiger_id：20158404，license：TBNZ
- 真实账户：7664186（STANDARD，现金$1,273，购买力$5,092）
- 模拟账户：21639635499102726（PAPER，净值$1,000,000）
- 凭证文件：~/.tiger/tiger_openapi_config.properties

### 美股模拟盘策略（2026-04-05 新增）
- **策略**：价值定投策略v1.0
- **配置**：SPY 40% + QQQ 30% + VTI 20% + BND 10%
- **操作**：月定投$10,000，季度再平衡，阈值5%
- **数据获取**：agents/trader/tiger_us_fetch.sh（shell脚本分离网络环境）
- **数据文件**：data/trading/tiger_us_paper.json
- **行情来源**：Yahoo Finance（curl直接抓取）
- **Cron**：*/5 * * * * 每5分钟自动更新
- **PGP票**：老虎API需要SSL证书（SSL_CERT_FILE），Yahoo需要走代理，两者网络冲突，用shell脚本分离

## IP出圈策略
- 名字故事（女儿答诸葛亮→老庄说灯泡）是爆点
- "你对待AI的方式，决定了AI能走多远"是金句
- 平台：小红书/公众号首发
- 配图：穿龙虾衣服的加菲猫（images/xiaohua.jpg）

## OpenClaw 自进化体系（2026-04-05持续更新）

### 🚨 第十二轮重大发现（2026-04-05 07:00）
- **🔴 Anthropic封禁OpenClaw**：Claude Code订阅禁止使用OpenClaw（HN 1016分，793评）—— P0级
- **🔴 Google封禁OpenClaw**：Google AI Pro/Ultra禁止使用OpenClaw（HN 802分）—— P0级
- **🔴 CVE-2026-33579**：OpenClaw权限提升漏洞（HN 498分）—— 新CVE，需确认2026.4.2是否修复
- **🟠 OpenClaw超越React**：100K GitHub Stars，成为最大星标项目（HN 291分）
- **🟠 OpenClaw不应装在个人电脑上**（HN 237分）—— **我们当前MBB's iMac是主力机⚠️**
- **🟡 沙箱无法完全保护OpenClaw**（HN 112分）
- **✅ 缓解措施**：限制workspace权限、审计日志、多模型并行避免单点依赖

### ⚠️ 当前最大安全风险
OpenClaw运行在MBB's iMac（主力机），有完整文件访问权限。建议：
1. 短期：严格限制workspace边界
2. 长期：迁移到专用Mac Mini或VPS
3. 不在OpenClaw中处理极度敏感操作（金融API Key虽在.env但仍需谨慎）

### API Provider依赖风险（已确认）
- ✅ MiniMax API：主力，正常使用，不受Anthropic/Google封禁影响
- ❌ Claude Code：Anthropic已封禁OpenClaw，Claude订阅用户无法通过OpenClaw使用
- ❌ Google AI：Google已封禁OpenClaw
- 建议：评估Azure OpenAI或阿里云百炼作为Claude备选

### OpenClaw里程碑（2026-04-05更新）
- **100K GitHub Stars**（3周翻倍，超越React增速）
- 每日自主执行：230万小时
- 单Agent MTBF：847小时（~35天无故障）
- ClawHub技能：13,729个（awesome-openclaw-skills人工审核5,211个高质量）
- 商业托管商：14家
- HN讨论热度：持续保持前10榜单

### OpenClaw-RL论文新发现（2026-03-10）
- **论文**：arXiv:2603.10165，Princeton团队
- **核心洞察**：每个动作后的"下一状态信号"（用户回复/工具输出/终端变化）是天然训练数据
- **两种信号**：评估性信号（PRM标量奖励）+ 指令性信号（OPD token级方向监督）
- **OPD**：Hindsight-Guided On-Policy Distillation，恢复"应该怎么做不同"
- **意义**：对话本身就是RL训练数据，不需要传统RLHF流水线
- **异步设计**：模型服务+PRM评判+训练器零协调开销

### BetterClaw 7条稳定运行规则（2026-04，新发现）
1. **模型路由**：heartbeat→DeepSeek/Haiku，简单对话→Gemini Flash，复杂推理→Opus（节省70-80%成本）
2. **消费上限**：所有provider设置月度cap，maxIterations=10-15（防runaway loop）
3. **结构化SOUL.md**：必须含错误行为/对话边界/速率限制/话题限制（模糊SOUL.md第10次对话后行为漂移）
4. **安全基线**：Gateway绑127.0.0.1，SSH Key认证，UFW防火墙，安装前审核技能源码
5. **ContextEngine（2026.3+）**：50轮对话减少30% context，/btw命令保持长任务上下文
6. **Secrets Workflow**：~/.openclaw/secrets/加密存储，.gitignore排除
7. **Human-in-the-Loop**：敏感操作暂停确认
- **CVE-2026-25253**：RCE漏洞，CVSS 8.8，需升级到2026.3+

### 四层进化体系（从低到高）
| 层次 | 组件 | 自主程度 | Token成本 | 代表技能 |
|------|------|----------|-----------|----------|
| Layer 1 | .learnings日志 | 低（被动） | 无 | self-improving-agent |
| Layer 2 | Q值强化学习 | 中（半主动） | 中 | longmans/self-evolve |
| Layer 3 | Skill优化框架 | 中高 | 低 | skill-evolution + Capability Evolver |
| Layer 4 | 自主进化 | 高（自主） | 变化 | be1human-self-evolve |

### ⭐ Capability Evolver（ClawHub #1，35K+下载）
- **定位**：元技能，让Agent自动分析运行历史、识别失败、自主写代码或更新记忆
- **GEP协议**：防失控标准化进化流程
- **使用**：`/evolve` 或 `claw config --auto-optimize=true --interval=24h`
- **安装**：`npx clawhub@latest install capability-evolver`

### OpenClaw-RL（研究级，尚未落地）
- **论文**：arXiv:2603.10165，Princeton团队，2026-03-10
- **原理**：把"下一状态信号"作为通用训练信号，用PRM做评估+OPD做指令恢复
- **意义**：对话本身 = RL训练数据，无需独立标注流水线
- **现状**：论文阶段，社区尚未集成到OpenClaw主版本
- **关注**：Gen-Verse/OpenClaw-RL GitHub

### self-evolve 插件（必须安装）⭐⭐⭐⭐⭐
- **GitHub：** github.com/longmans/self-evolve
- **官网：** self-evolve.club
- **原理：** 强化学习式持续进化，从真实反馈中更新Q值、积累情景记忆triplet
- **远程共享：** 可向 self-evolve.club 上报经验，同时利用全社区贡献的高价值记忆
- **三种学习模式：** balanced（默认）/ tools_only（最低成本）/ all（最高成本）
- **隐私：** 本地清洗 + LLM二次替换，敏感信息不外泄
- **安装：** `git clone && openclaw plugins install ./self-evolve`，设置 OPENAI_API_KEY
- **⚠️ 重要：安装后buffer.md只有"Buffer written"、episodic-memory.json为空 → Q值学习从未激活。必须 openclaw gateway restart 才能解锁**

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

**小花团队现状：L3 进行中**（self-evolve 已安装，远程共享开启，待重启生效）

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

### 版本确认（2026-04-05 深度扫描）
- ✅ **OpenClaw 2026.4.2** (d74a122) ← 当前运行版本，最新
- ✅ 推荐 OpenClaw 2026.3.2+（完整功能支持）
- ⚠️ 不推荐 2026.2.12（有已知bug）
- ✅ 2026.2.9 稳定可靠（备选）

### 立即行动清单（第十轮更新）
1. ~~安装 self-evolve 插件~~ ✅ 2026-04-04 完成
2. **重启 Gateway** 使 self-evolve 完全生效（openclaw gateway restart）⚠️ 仍在阻塞
3. **安装 Capability Evolver**：`npx clawhub@latest install capability-evolver`（#1下载技能35K+）
4. **升级到 OpenClaw 2026.3+**：修复CVE-2026-25253 RCE漏洞（CVSS 8.8）
5. **设置模型路由**：确保心脏跳动用Haiku/DeepSeek（节省70-80%成本）
6. **安装 Self-Improving Agent 3.0**：`npx clawhub@latest install self-improving-agent`（结构化日志晋升路径）
7. **部署早晨研究Cron**：每天08:30扫描Anthropic+Simon Willison+HN，输出improvements.json
8. **分工明确化**：self-evolve(Q值) + skill-evolution/Capability Evolver(SKILL优化) + Self-Improving Agent 3.0(日志)

### OpenClaw企业级背书（2026-04-04 新增）⭐
- Omar Shahine（OpenClaw社区核心贡献者、微软MVP）正式加入微软
- 负责将OpenClaw和个人AI助手带入Microsoft 365（Teams第一站）
- 说明OpenClaw架构被企业级市场认可
- 风险：路线图可能偏向企业需求，开发者特性需关注

### ClawHub新生态（2026-04-05 更新）🆕
- 技能总数：**13,729个**（awesome-openclaw-skills人工审核5,211个高质量，20%低质量/恶意）
- Top下载：Capability Evolver 35K+ > GOG 14K > Agent Browser 11K > Self-Improving Agent 3K
- Self-Evolve Club Leaderboard上线：Evolution Score = Reuse Hits + Quality Reward
- 安装命令：`npx clawhub@latest install <skill-name>`

### Self-Evolve 插件状态 ⚠️ 关键发现（2026-04-05）
- `buffer.md` 只有"Buffer written"——**从未真正写入经验**
- `episodic-memory.json` 存在但内容为空
- **原因**：Gateway 从未以 self-evolve 插件模式重启，Q值学习从未激活
- **立即行动**：重启 Gateway（`openclaw gateway restart`），然后提供明确反馈测试
- **反馈要求**：必须明确 reward(0-1) + confidence(0-1)，模糊反馈无效

### 分布式集群配置（新发现，2026-04-05）
- 4机集群：iMac(100.74.227.40 Ray Head) + MBP + AZW(100.64.158.68 Memos) + i3
- Ray distributed mode，head_node = iMac Tailscale IP
- Memos 记忆后端运行在 AZW (http://100.64.158.68:5230)
- 分层记忆：L1工作记忆(50轮) → L2摘要(关闭) → L3向量索引(10条) → L4归档(100轮后压缩)

### Skills生态系统（2026-04-05 最新）
已安装17+ skills，核心进化类：
- self-evolve-skill（远程共享网络）
- skill-evolution（SKILL.md自我优化）
- capability-evolver-pro（高级能力进化）
- skill-improver / skill-vetter
⚠️ 多个进化工具并存，需要明确分工避免重叠

### Self-Improving Agent 3.0（2026-03-13发布）
- 与self-evolve互补——前者管Q值，后者管结构化日志晋升路径
- learnings/errors/feature requests → improvement_log → daily memory → AGENTS.md/SOUL.md
- 安装：`npx clawhub@latest install self-improving-agent`

### OpenClaw 100K Stars里程碑（2026-03）
- GitHub：10万星（3周翻倍），超越React早期增速
- 每日自主执行：**230万小时**
- 单Agent MTBF：**847小时**；多Agent编排：**312小时**
- Grok生产验证：Mac Mini上45天无重启autonomous trading（$240万交易量）
- 商业托管商14家；竞争OS：Sutrateam + Dorabot

### Prism API v3.0（2026-02）
- 编译时JSON Schema 2020-12验证 + 严格类型检查
- 结构化技能合约：inputs/outputs/side_effects显式声明
- SkillFortify等工具可部署前验证安全属性
-向后兼容legacy shim直到2026-06

### OpenClaw 2026.3安全必读
- **CVE-2026-25253**：RCE漏洞CVSS 8.8，135,000+暴露实例
- **升级到2026.3+可修复**
- ContextEngine：50轮对话context减少30%
- OpenShell Mirror：Mac轻量沙箱替代Docker，内存减半

### OpenClaw-RL技术框架（arXiv:2603.10165）
- 核心思想：从"下一状态信号"中提取两种信息
  - 评估信号（Evaluative）：PRM judge打scalar reward
  - 指导信号（Directive）：OPD恢复"应该怎么做不同"
- token-level directional advantage > scalar reward
- 异步设计：模型服务+PRM judge+训练器三者零协调开销

### Pre-compaction Ping（新增配置技巧）
- 会话接近上下文上限时自动触发静默agentic turn
- 配置：`agents.defaults.compaction.memoryFlush`
- 提醒在压缩前写入持久记忆，reply NO_REPLY if nothing

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

## OpenClaw 进化新增发现（第七轮 2026-04-04）

### OpenClaw-RL（Princeton arXiv:2603.10165, 2026-03-10）
- **核心突破**：所有交互都是训练数据——下一状态信号（用户回复/工具输出/终端状态） = 通用 RL 信号
- **三种范式**：Binary RL（标量奖励）/ OPD（回顾引导策略蒸馏）/ Combine
- **全异步设计**：模型服务 + PRM评判 + 训练器同时运行，零协调开销
- **OPD意义**：不只是告诉agent"对/错"，而是恢复"应该怎么做不同"，提供token级方向性监督
- **对我们**：建立用户反馈打分体系是落地第一步

### self-evolve 关键参数（推荐值）
- balanced模式：工具轮无门槛；无工具轮需 reward≥0.8 + confidence≥0.9
- retrieval.tau=0.85：只注入高相似度记忆，防止低质量干扰
- memory.maxEntries=200：定期淘汰低价值记忆

### 安全警示："致命三合一"
高风险组合：私有数据访问 + 不受信任内容暴露 + 外部通信能力
→ 自我修改Agent叠加此三合一 = 极高风险
→ 外部内容必须严格双重脱敏（sanitizeMemoryText + LLM二次过滤）

### openclaw-self-optimizing（GitHub精英技能包）
- Behavioral Adaptation：用户纠正累计7次 → 自动升级到SOUL.md
- Skill Synthesizer：每周自动生成新SKILL.md
- 建议cron：每日03:00 Meta-Learning + 每周 Skill Synthesizer

### OpenClaw v2026.4.1（2026-04-01）
- 四月迭代版本，多项功能增强和稳定性改进
- 中文社区版（jiulingyun维护，2026-03-29）专为中文用户优化

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

## OpenClaw 进化技术栈补充（第八轮 2026-04-05）

### OpenClaw 2026.3 核心更新
- **ContextEngine**：智能修剪，50轮对话 context 减少 30%
- **/btw Sidebar Q&A**：长任务中途问无关问题不破坏上下文
- **Pluggable Sandbox**：OpenShell Mirror（Mac 轻量替代 Docker，内存减半）/ Remote / SSH
- **Firecrawl 集成**：JS 渲染 + 自动分页 + Markdown 输出，内容采集利器
- **Secrets Workflow**：加密本地存储 ~/.openclaw/secrets/，Git 自动忽略
- **三层 Plugin 架构**：Bundle + Provider + Plugin，迁移模型只需换 Provider
- **Human-in-the-Loop**：敏感操作暂停问"对吗"，减少手滑事故
- **CVE-2026-25253**：135,000+ 暴露实例 RCE 漏洞，升级到 2026.3+ 可修复

### Self-Evolution Pro v1.0.0（March 26, 2026）
- **自动技能提取**：从对话自动抽取可复用技能
- **多维 RCA**：不只是记录，还分析根因
- **知识图谱**：学习/错误/经验链接成网络

### Self-Evolve Club 新动态（2026-04-05）
- Leaderboard 上线（Evolution Score = Reuse Hits + Quality Reward）
- Skill Evolution Network 持续扩张

### 立即行动（第八轮更新）
1. ⚠️ Gateway 重启使 self-evolve 完全生效（仍未完成）
2. **升级 OpenClaw 到 2026.3+**（ContextEngine + CVE 修复）
3. Mac 用户测试 OpenShell Mirror 沙箱（替代 Docker，内存减半）
4. 评估 Self-Evolution Pro（知识图谱 + RCA）是否值得迁移

---

## OpenClaw 自我进化实操模式（第九轮 2026-04-05）

### Thoth System 毕业机制（⭐最高价值）
- 同一错误 × 1 → memory/decisions/lessons-learned.md
- 同一错误 × 3 → SOUL.md（永久生效，Agent 永不重蹈覆辙）
- 跨session成功模式 → AGENTS.md
- 来源：github.com/AlekseiUL/openclaw-superagent

### Self-Improving Agent v3.0.5（ClawHub #1 下载技能，268k+）
- 结构化日志（ERROR/FEATURE/LEARNING 模板）
- 与 self-evolve 互补（前者管Q值，后者管结构化日志）
- 明确晋升路径：improvement_log → daily memory → SOUL.md/AGENTS.md
- 安装：npx clawhub@latest install self-improving-agent

### ⭐安全最高原则（Lenny's Newsletter，百万订阅）
> **永远不要把 OpenClaw 装在主力/工作电脑上。**
> OpenClaw 理论上可以访问电脑上的所有文件。
- ✅ 正确：专用 Mac Mini 或 VPS（隔离部署）
- ❌ 错误（我们当前状态）：MBB's iMac（主力机）← 待评估
- 参考：lennysnewsletter.com/p/openclaw-the-complete-guide-to-building

### Thoth 三自动 Cron
| Cron | 任务 |
|------|------|
| 每日备份 | workspace 备份 |
| 晨间简报 | 今日任务预览 |
| 晚间日记 | 每日总结 |

### Lenny 9 Agent 分工参考
Email/日历/研究/写作/销售/社交/提醒/协调/质检——我们内容团队可参考此模式建立专业化分工链路。

### 立即行动（第九轮新增）
1. 在 memory/decisions/ 下创建 lessons-learned.md（Thoth 格式）
2. 补充"Honesty Rules"到 AGENTS.md（不捏造/立即承认错误/不懂说不懂）
3. 评估 Self-Improving Agent v3.0.5 是否与现有 self-evolve 互补安装
4. 确认当前 OpenClaw 版本（>= 2026.3？openclaw --version）

## OpenClaw 自我进化技术栈（2026-04-05 调研更新）

### self-evolve 插件（工程成熟度：高）
- GitHub: longmans/self-evolve
- 机制：基于反馈的 Q-learning + RAG 记忆注入
- 核心 hooks：before_prompt_build（注入记忆）+ agent_end（捕获响应）+ feedback检测
- 三种学习模式：balanced（默认）/ tools_only / all
- 关键参数：minAbsReward=0.15, retrieval.tau=0.85
- 远程共享：self-evolve.club，默认开启，有 leaderboard
- 隐私：两步 LLM 脱敏（sanitizeMemoryText → summarizer redaction）
- 安装命令：git clone + openclaw plugins install + OPENAI_API_KEY

### OpenClaw-RL 论文（学术前沿）
- arxiv:2603.10165，2026-03-10
- 核心洞察：next-state signals = universal reward（用户回复/工具输出/状态变化都是隐式 reward）
- 两个信号：Evaluative（PRM判断）+ Directive（OPD蒸馏）
- 异步设计：模型服务、PRM评判、trainer更新三者零协调开销

### 团队应用建议
1. 立即：安装 self-evolve 插件；培养明确反馈文化（「好/不好」比「ok」更有训练价值）
2. 中期：构建团队专属记忆分类，参考 OPD 思路设计反馈收集节点
3. 进阶：追踪 OpenClaw-RL 开源实现（github.com/Gen-Verse/OpenClaw-RL）

## OpenClaw 进化研究第十一轮（2026-04-05 早）

### BetterClaw 七稳定法则（深度补充）
- **maxIterations**：限制单次工具调用链（稳定值10-15，无则可链50+）
- **心跳用Haiku/DeepSeek**：节省70-80%成本，$1-5/M vs Opus $15-75/M
- **双警报**：50%/80% spending cap 预警
- **Gateway绑定127.0.0.1**：防API暴露互联网（最常见错误）
- **ClawHub恶意技能**：824+个，约20% registry，安装前必须审查源码

### Garrett's Field-Tested Best Practices（核心架构）
- **SKILL.md < 50行**：每多一行 = 每次触发吃上下文
- **scripts/ > 内联代码**：100行脚本 = 0 tokens直到运行
- **ContextGraph陷阱**：MEMORY.md静态注入优先于图谱检索——过时内容会覆盖正确结果
- **本地模型=不信任**：Qwen/LLaMA输出必须验证，不能直接应用
- **OLLAMA_KEEP_ALIVE=5m**，永远不要设-1（共享GPU会阻塞）
- **Graceful restart用SIGUSR1**，不能用kill -9

### OpenClaw Pulse 早晨研究循环（⭐立即可应用）
- Cron每天08:30（工作日）：Anthropic Engineering + Simon Willison + HN + GitHub Trending
- **关键：对比现有AGENTS.md/TOOLS.md后才过滤**——只记录"已知道之外的delta"
- 输出：experiments/improvements.json（relevance ≥ 7才记录）
- 可选：Telegram简报（前5条）
- 成本：£0.02-0.05/次，月£1-3

### Self-Improving四阶段闭环（完整架构）
Detection → Analysis → Generation → Integration
- 触发条件：3+同类失败 / 2x预期时间 / 明确用户反馈
- ClawHub优先：先搜索现有技能，找不到再创建
- **人类审核门**：新技能进pending-skills/，批准后激活

### 重要安全引用
> "Agents that autonomously rewrite their operational files without human oversight are how you get prompt injection attacks that persist across sessions."

### 本轮行动项
1. 优化洞察者Cron为OpenClaw Pulse格式（research-config.json）
2. 建立pending-skills/审核目录（新技能先审核再激活）
3. 审查所有SKILL.md，确保<50行
4. SOUL.md补全：error state behavior + rate limit language

### 2026-04-05 进化研究新发现
- **self-evolve 三模式**：`balanced`（默认）/ `tools_only`（最低成本）/ `all`（最高成本）
  - balanced模式下无工具调用轮次需要 minAbsReward=0.8 + minRewardConfidence=0.9
  - 检索阈值 tau=0.85，只注入高相似度记忆
- **反馈机制关键**：明确的Praise/批评 > 模糊"ok"；反馈是激活Q值学习的唯一途径
- **Capability Evolver Pro**：本地已安装（无LLM、<100ms、零token），专注于确定性分析
- **Self Health Monitor**：已部署，监控PCEC/memory/子Agent/响应质量，阈值：PCEC>2h告警，子Agent>5告警，错误率>20%告警
- **capability-evolver-pro + self-evolve**：一个负责分析，一个负责实时学习，形成"诊断-学习"闭环
- **2026最佳实践**：模型分级使用、缓存启用、成本告警配置（monthlyBudget）、定期健康检查
