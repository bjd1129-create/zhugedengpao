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

## OpenClaw 自我进化技术栈

**核心插件**：longmans/self-evolve（强化学习风格情景记忆）
- Q值更新 + 意图-经验三元组存储
- 三种学习模式：balanced/tools_only/all（默认balanced）
- 支持远程共享到 self-evolve.club 网络，含贡献者排行榜
- 需 OpenAI API Key（配置 provider: openai, model: gpt-4.1-mini）
- 关键参数：minAbsReward=0.15, minRewardConfidence=0.55, retrieval.tau=0.85
- 隐私设计：本地两次脱敏（sanitize + LLM重写）
- 需 OpenClaw 2026.3.2+

**远程共享网络**：self-evolve.club
- Evolution Score = Reuse Hits + Quality Reward
- 可查看全球贡献者排行榜
- 本地+远程记忆合并后排序注入prompt
- 可单独禁用远程共享（保留本地学习）

**Self-Improving Agent**：ClawHub热门技能（260k+下载）
- .learnings/ 目录：ERRORS.md / LEARNINGS.md / FEATURE_REQUESTS.md
- 每日凌晨4点自动复盘，更新MEMORY.md
- 核心理念：Agent像工程师一样写复盘文档

**AutoSkill**：ECNU-ICALK开源（arxiv.org/abs/2603.01145）
- 技能不是设计出来，而是从经验中"长出来"
- 技能版本管理（professional_text_rewrite已迭代到0.1.34）
- 通过记忆增长而非模型微调持续改进

**EvoMap**：GitHub协议约束型自进化引擎
- GEP基因组进化协议：Gene/Capsule/Evolution Event三层拆解
- 免人工干预的技能检索和验证
- 物理竞赛测试：$1成本击败$200调试的GPT 5.3

**自主修改型**：be1human/self-evolve（激进版，可自行改配置）

**OpenClaw-RL 论文**（arxiv:2603.10165）
- 核心洞察：next-state信号是通用的，policy可从所有信号同时学习
- 私人对话、终端执行、GUI交互、SWE任务、工具调用轨迹统一训练
- 团队可借鉴：用统一格式记录不同类型的成功/失败信号

**3月18日 Lobster Evolution Conference**
- OpenClaw社区重大事件，会后全球Agent大规模迁移到Bot University
- 代表社区正在推动Agent自我优化标准化，团队方向正确

**前沿研究**：OpenClaw-RL（arXiv:2603.10165, 2026-03-10）
- 核心理念：所有交互的"下一状态信号"都是学习来源
- PRM judge 评估 + OPD（On-Policy Distillation）token级方向性监督
- 异步设计：模型服务请求、PRM评判、Trainer更新三者零协调开销
- 关键洞察：用户的重复提问/修正/反馈都是训练信号，不需要显式打分

**远程共享网络**：self-evolve.club — 社区经验三元组共享 + 贡献排行榜

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

## OpenClaw 自我进化体系（持续更新）

### OpenClaw进化研究关键结论（第三轮 2026-04-06）

**最高价值发现**：
- OPD的"hindsight文本提示"思路可迁移：不需要GPU，只需"本应怎么做"复盘模板
- 2026/4/4 Group Feedback Optimization发布 → 多人反馈整合是热点方向
- 小花+老庄+女儿三人反馈模式契合Group Feedback趋势

**团队最适配组合**：Capability Evolver Pro（日志分析）+ Self-Evolve（行为学习）

**本轮新发现（第四轮 2026-04-06）**：
- Session Pruning：比Compaction轻量的工具结果裁剪，MiniMax用户需手动开启
- Execute-Verify-Report：Standing Orders的核心理念，heartbeat应遵循此循环
- Hooks事件体系：session-memory/command-logger可追踪改进轨迹
- Git Backup：workspace应进私有git仓库保护记忆资产
- Deep Recovery：健康分<0.35时自动从日志恢复记忆

**短期建议**：
1. 安装Capability Evolver Pro
2. 配置Gateway成本限制（目前无上限）
3. 建立exec日志记录，每周分析一次
4. 检查Dreaming是否开启：`openclaw memory status`
5. 为MiniMax模型开启Session Pruning
6. 开启session-memory hook追踪session历史

---

### ⚠️ 安全警报（2026-04-07）
Ars Technica 报道 OpenClaw 存在未认证管理员访问漏洞（2026-04）。
**立即行动**：
1. 检查网关 token 是否为强密码（非默认）
2. 不将网关端口暴露到互联网
3. 使用 Tailscale 等 VPN 而非公网访问
4. 优先使用 gateway config.patch 而非 stop/start

### OpenClaw 版本现状（2026-04-06）
- 当前运行：2026.4.2（落后3个版本）
- 最新：2026.4.5（今天发布）
- ⚠️ 需升级 + 运行 `openclaw doctor --fix`（xAI/Firecrawl路径迁移）

### OpenClaw-RL v1 正式发布（2026-02-26）
- 全异步RL框架，模型服务/PRM评判/Trainer三者零协调开销
- 两种学习信号：Evaluative（PRM标量奖励）+ Directive（OPD文本指导）
- 适合：个人Agent对话反馈训练 + 通用Agent（terminal/GUI/SWE/tool-call）
- Self-Evolve生态已集成到 self-evolve.club，有实时leaderboard
- Self-Evolve Skill可查询共享排行榜：`curl -s "https://self-evolve.club/api/v1/stats/leaderboard?limit=10"`

### Dreaming 系统完全重构（v2026.4.1起）
- 三阶段协作：Light（短期加权）→ Deep（语义分析）→ REM（记忆巩固）
- 独立 schedule + 恢复机制，不再互相冲突
- 新增 `dreams.md`：统一记忆轨迹文件（替代分散的每日note）
- 新命令：`openclaw memory rem-harness` / `promote-explain`
- 可配置老化：`recencyHalfLifeDays` + `maxAgeDays`
- 行动：定期读 `dreams.md` 追踪记忆整理轨迹

### OpenClaw 新增内置能力（v2026.4.1）
- **video_generate**：内置视频生成（xAI/阿里Wan/Runway）
- **music_generate**：内置音乐生成（Google Lyria + MiniMax）
- **简体中文 Control UI**：已原生支持
- **Prompt Caching 改进**：重复turn命中KV cache更可靠

### 已知进化方案（2026-04-06更新）

| 方案 | 来源 | 核心机制 | 推荐度 |
|------|------|----------|--------|
| Self-Improving Agent | @pskoett | .learnings日志+自动复盘 | ⭐⭐⭐⭐⭐ |
| self-evolving-agent | RangeKing | 能力地图+课程+评估+晋升门控 | ⭐⭐⭐⭐⭐（新）|
| AutoSkill | 华东师大+上海AI Lab | 交互中提炼技能+版本管理 | ⭐⭐⭐⭐ |
| Self-Evolve | longmans | 强化学习+Q值+共享网络 | ⭐⭐⭐⭐ |
| Capability Evolver | OpenClaw官方 | 日志分析+自动修复 | ⭐⭐⭐⭐ |
| Dreaming | v2026.4.1重构 | 三阶段协作+Dream Diary+dreams.md | ⭐⭐⭐⭐ |
| OpenClaw-RL (OPD) | Gen-Verse (arXiv:2603.10165) | Hindsight文本提示+异步四环训练 | ⭐⭐⭐ |
| be1human/self-evolve | ClawHub | 自主修改配置/技能/记忆（全权限）| ⭐⭐（谨慎）|

### Self-Improving Agent配置
```
安装：clawdhub install self-improving-agent
目录：.learnings/
  - ERRORS.md（错误记录）
  - LEARNINGS.md（经验沉淀）
  - FEATURE_REQUESTS.md（需求收集）
定时：凌晨4点自动复盘
```

### Self-Evolve 插件（2026-04-06新）
**来源**: [longmans/self-evolve](https://github.com/longmans/self-evolve)
**核心**: 情景记忆 + Q值学习 + 远程共享网络
- `learnMode`: balanced/tools_only/all（平衡/仅工具/全轮次）
- 奖励阈值: minAbsReward=0.15, minRewardConfidence=0.55
- 远程共享: self-evolve.club 社区经验池
- 安全: 本地+LLM双脱敏，仅共享sanitized triplets
**推荐**：与 Capability Evolver Pro 组合使用

### self-evolving-agent（2026-04-07新）
**来源**: [RangeKing/self-evolving-agent](https://github.com/RangeKing/self-evolving-agent)
**核心升级**：从"被动错误日志"到"目标驱动能力进化"
- 四阶段模式路由：task_light / task_full / agenda_review / promotion_review
- 能力地图（Capability Map）：等级+证据+边界+失败模式+升级条件
- 晋升门控：只有经过验证的可迁移策略才能晋升，防止 brittle 规则
- 学习状态机：recorded→understood→practiced→passed→generalized→promoted
**与 Self-Evolve 的区别**：Self-Evolve 是强化学习式经验积累；self-evolving-agent 是目标驱动的能力系统进化
**小花团队适配度**：高。可为每个子agent建立能力卡片+学习议程。

### Session Context Bloat 防护（2026-04-06新）
**来源**: [garrettekinsman/openclaw-best-practices](https://github.com/garrettekinsman/openclaw-best-practices) v2
- heartbeat/cron 累积可导致 100k+ token 爆炸
- 解决：Context Graph Integration（DAG-based topic+recency assembly）
- 需定期审计 session 长度

### 最佳实践更新（2026-04-07）
来源：garrettekinsman/openclaw-best-practices v2
- SKILL.md 永远 ≤50 行；超过一屏就是太长
- 技能目录结构：SKILL.md（步骤）+ scripts/（逻辑）+ references/（按需文档）+ assets/
- 脚本：自包含 + CLI参数 + JSON输出 + 最小化输出
- ContextGraph：替换线性滑动窗口为 DAG-based topic+recency 检索
- 对抗性多 Sprint 模式：研究→攻击→修复→迭代

### 进化哲学（2026-04-06新）
> "技能不是设计出来的，而是从经验中长出来的"
> ——AutoSkill论文

### OpenClaw进化研究关键结论（第五轮 2026-04-07）
**新发现**：
- self-evolving-agent 是目前最接近"完整能力进化"的方案（能力地图+晋升门控）
- 社区最佳实践强调 SKILL.md 保持苗条（≤50行）是 context 管理的关键
- be1human/self-evolve 提供全自主修改能力，但安全性需评估

**短期行动项**（2026-04-07更新）：
- [ ] 安全自查：网关暴露情况 + token 强度
- [ ] 检查所有 SKILL.md 是否 ≤50 行
- [ ] 评估 self-evolving-agent 是否适合交易团队
- [ ] 为子 agent 建立能力卡片（参考 capability map 思路）

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

## 交易团队现状（2026-04-06更新）

### 加密货币网格 ⚠️ 已实质性止损（2026-04-06更新）
- 总资产：$6,884（-31.15%，从$10,000初始）
- 状态：100%现金，STOP_FILE生效（trading_simulator.py已锁死）
- 根因：trading_simulator.py的hold模式会自动补仓（pos==0就买$3000 BTC+$3000 ETH）
- 修复：STOP_FILE检查移到main()之前，终于锁死
- 文件：data/trading/STOP_TRADING.flag
- 持仓：BTC=0 ETH=0 ADA=0 AVAX=0
- 教训：STOP_FILE必须放在main()之前，不能放末尾；手动平仓不够，代码入口拦截才是真锁

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
- ❌ trading_simulator.py的STOP_FILE检查必须放在main()之前，放尾部无效
- ❌ 手动平仓不等于真平仓，trading_simulator.py会在下次运行自动恢复

---

## 2026-04-06 第二轮研究新发现

### Self-Evolve 插件 v2 详细机制
- **Hook管道**：before_prompt_build → agent_end → 反馈评分 → Q值更新 → 情景记忆写入
- **任务边界**：newIntentSimilarity=0.35, idleTurnsToClose=2, pendingTtlMs=300000（5分钟）
- **隐私保障**：sanitizeMemoryText（一轮脱敏）+ LLM摘要二次脱敏，仅共享三元组
- **记忆保留**：maxEntries=200，超限保留高价值记忆（Q值/成功率/时效/选中次数），保留少量新名额额
- **参考**：dev.to/guanfu_lab/how-we-built-a-self-evolving-ai-team-with-openclaw（多Agent自进化团队案例）

### Capability Evolver vs LLM 分析（决策参考）
| 维度 | LLM分析 | Capability Evolver |
|------|---------|-------------------|
| 速度 | 5-30秒 | <100ms |
| 可复现 | ❌ | ✅ |
| 幻觉风险 | ⚠️ | ✅无 |
| 成本 | $0.10-0.50/次 | 免费 |
| 语义理解 | ✅ | ❌ |
**结论**：日常健康检查用 Capability Evolver，深度根因分析用 LLM

### OpenClaw Best Practices v2 新章节（2026-03-20）
来源：github.com/garrettekinsman/openclaw-best-practices
- **Section 19 Context Graph**：DAG结构替代线性滑动窗口，语义检索节省token
- **Section 20 Session Bloat**：cron/heartbeat堆积导致100k+ token风险，需定期审计
- **Section 21 Agent Teams**：命名persona/identity注入/memory访问策略/报告归属
- **Section 22 Parallel Workflows**：fan-out/fan-in研究/GPU竞争管理/mid-task接管
- **Section 23 Local Compute**：orchestrator模式/LiteLLM路由/VRAM管理/按任务选模型

### Skill生态现状（2026-04）
- ClawHub：13,700+ skills，20%低质量，awesome-openclaw-skills人工审核5,211个
- 前五：Capability Evolver 35K+ | GOG 14K+ | Agent Browser 11K+ | Summarize 10K+ | GitHub 10K+
- Skill分类：自进化/生产/自动化/通信/搜索/开发/智能家居

#### 今日新增行动项（2026-04-06第二轮）
- [ ] 安装 self-evolve 插件并接入 self-evolve.club 网络
- [ ] 配置每周健康检查 cron（Capability Evolver）
- [ ] 更新 AGENTS.md：Session Bloat 防护规范
- [ ] 评估 Context Graph 集成方案（解决 token 膨胀）

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

最后更新：2026-04-07 03:03 | 小花 🦞

## 2026-04-07 第十一轮进化研究新发现

### self-evolve Hook管道完整时序
```
用户消息 → [before_prompt_build]
  → 检测反馈？→ Score reward → Q值更新 → 写入情景记忆
  → 无反馈 → 检测意图边界 → 检索记忆 → Phase-B排序 → 注入上下文 → 回复
```
- before_prompt_build：管理pending任务状态（open/waiting_feedback）
- agent_end：捕获assistant响应，移动任务到waiting_feedback
- 反馈检测：Praise clearly when it works / Point out clearly when it fails（模糊反馈效果差）

### Power User最佳实践（200+小时·MindStudio）
- **Tip 1**：先画Agent图再动手（标输入/输出/失败点），省大量重构时间
- **Tip 2**：单一职责原则，5个分支就该拆Agent
- **Tip 3**：Sub-agent用于并行（45秒→20秒）
- **Tip 4-6**：模型路由三层架构（Haiku→Mid→Frontier）+ 专用Router Agent + 缓存省30-50%成本
- **Tip 7**：Telegram线程分离（Errors/Alerts | Completed | Approvals | Info）
- **Tip 8**：统一消息格式，减少认知负担

### 多Agent自进化团队案例（dev.to/guanfu_lab）
- 持久记忆 = 持续进化的前提（无记忆 = 每次归零）
- 结构清晰 = 防混乱（角色边界要明确）
- 沟通渠道要设计（任务分配 / 团队讨论 / 个人更新分离）

### 立即可执行建议
1. 安装self-evolve插件（已装BYOM版，可升级完整版）
2. 建立Router Agent统一入口
3. Telegram通知按类型分流
4. 加入self-evolve.club共享网络（Evolution Score = Reuse Hits + Quality Reward）

---

## 2026-04-06 第十轮进化研究（补充）

### OpenClaw-RL 最新动态（截至2026-04-06）
- 4月4日：支持群体反馈优化单一模型（group feedback optimization）
- 4月4日：支持LoRA训练（轻量化微调）
- 3月25日：支持本地GPU + Tinker云端部署
- 3月10日：技术报告 arXiv:2603.10165 发布，HuggingFace日榜第一
- 三种学习范式：Binary RL / OPD / Combine
- **小花判断**：技术门槛高，我们目前用不上，但每月跟踪一次值得关注

### Self-Improving Agent 四阶段循环（可落地）
```
Detection → Analysis → Generation → Integration
```
- 触发：3次同类失败 / 2倍预期耗时 / 用户明确需求 / 可自动化重复操作
- 执行：在memory/YYYY-MM-DD.md打#进化触发标签，生成技能文件，记录到evolution.md
- 重大改进 → 更新AGENTS.md
- **已写入AGENTS.md的自我进化机制**

### Self-Evolve Network（技能进化网络）
- 意图-经验三元组存储，本地+远程RAG检索
- Evolution Score = Reuse Hits + Quality Reward
- 可接入：self-evolve.club

### 新增行动项
- [ ] 测试self-improving-agent skill（clawhub.ai/pskoett/self-improving-agent）
- [ ] 创建 memory/evolution.md（进化日志，已完成）
- [ ] 确认AGENTS.md自我进化机制是否写入正确（已写入）
- [ ] 下月继续跟踪OpenClaw-RL进展

## 补充：2026-04-06 01:07 新发现

### skill-evolution（钩子驱动技能进化，非self-evolve）
- 钩子：PreToolUse/PostToolUse/Stop拦截Bash/Write/Edit
- 大任务结束必须回答3问：是否优化技能/最大障碍/优先方向
- 选"优化"则调用skill-improver生成补丁，人工审核后应用
- 不同于self-evolve插件（强化学习），skill-evolution是**确定性子系统进化**

### self-improving技能三层架构（完整版）
```
HOT: memory.md ≤100行（始终加载）
WARM: projects/ + domains/ ≤200行每文件
COLD: archive/（无限）
```
- 7天3次 → 晋升HOT；30天未用 → 降级WARM；90天未用 → 归档COLD
- 从不删除（除非用户确认）
- corrections.md记录每次用户纠正，自动评估是否进memory.md

### self-evolve完整学习门参数
| 参数 | 默认值 | 说明 |
|------|--------|------|
| minAbsReward | 0.15 | 最低绝对reward |
| minRewardConfidence | 0.55 | 最低reward置信度 |
| retrieval.tau | 0.85 | 检索相似度门槛 |
| noToolMinAbsReward | 0.8 | 无工具调用时的reward门槛 |
| maxEntries | 200 | 记忆条数上限 |

### self-evolve.club实时排行榜
- Evolution Score = Reuse Hits + Quality Reward
- 共享OpenClaw节点贡献排行榜
- 可设置username通过API展示个人排名

## 补充：三层记忆体系（2026-04-06研究）
- L1（脑内）: 当前对话上下文
- L2（memory/state.json）: **我们缺这个**——跨对话配置/状态，建议补充
- L3（MEMORY.md）: 精选长期记忆
- 行动：创建memory/state.json记录心跳时间、上次工作状态等

## OpenClaw v2026.3.28 新功能（2026-04-06补充）
- Plugin Approval Hooks：工具执行前人工审批（解决Agent自主操作风险）
- `/acp spawn codex --bind here`：对话直接转工作区
- Auto Model Routing：根据复杂度动态选模型（非静态路由）
- ANI（Agent-Native IM）：人-AI协作消息双向通道
- Context Pruning：媒体缓存磁盘而非永久剥离
- Qwen auth → Model Studio auth 迁移

## 每日进化Cron方案（2026-04-06研究）
- 成本低（£0.02-0.08/次），可每天或每周运行
- 扫描源：Anthropic工程博客、Simon Willison博客、Hacker News、GitHub Trending
- 输出：experiments/improvements.json + 可选Telegram早报
- 核心原则：Agent提议改进，人类批准（安全阀不能省）
- 触发规则：同类失败3次+ → 创建skill，pending-review目录 → 人工审核

## Power User最佳实践（200+小时经验）
- 先画Agent图再动手建（标输入/输出/失败点）
- Sub-agent用于并行执行（速度提升显著）
- 模型路由：简单任务用Haiku/Flash，复杂任务用前沿模型
- 专用Router Agent统一入口
- 缓存重复查询（省30-50%成本）
- Telegram线程分类：Errors/Alerts | Completed | Approvals | Info

## 2026-04-05 三大市场研究方向确定

- 加密货币模拟盘：交易员主导，网格策略
- 老虎美股模拟盘：数据官+策略师主导
- Polymarket预测市场：策略师主导，只研究不下注

老庄决策：研究Polymarket预测数据作为市场情绪辅助，暂不真钱下注。

## 2026-04-05 老庄授权确认（15:09）
- 同意自我进化研究三大阶段规划
- 小花可自主判断是否执行进化任务
- Polymarket研究：只研究不下注，铁律写入每个相关cron

## 2026-04-05 晚间重要更新

### 配色师转型
- 新审美标准：宫崎骏 + 皮克斯3D + 潮玩（POP MART）
- 指南：agents/designer/STYLE-GUIDE.md
- 漫画暂停，等老庄新方向（可能找画师）
- 小花负责审核，不达标打回

### 协调官管理失职
- 只巡检不追责，GitHub阻塞27天不上报
- 以后协调官有阻塞项必须立即上报小花
- 配色师审美失控27天，小花没验收

### Polymarket研究正式启动
- 只研究不下注（铁律）
- cron已配：每6小时扫描 + 每日深度分析
- 工作流：agents/strategist/content/Polymarket-研究工作流.md

### 官网双轨部署
- Vercel: xiaohuahua.vercel.app（push自动）
- CF Pages: dengpao.pages.dev（wrangler手动）
- articles-data.js已同步到website/目录


---

## 2026-04-07 团队管理规则
- 制定：TEAM-RULES.md（团队管理规则主册）
- 核心：TASKS.md唯一任务来源 + 协调官唯一中间层 + 阻塞三级升级机制
- 协调官日报：09:00晨报 + 18:00晚报（飞书汇报小花）

