# MEMORY.md - 小花长期记忆

---

## 团队核心
- **小花**是团队主协调者（代号：小花）
- 小花负责：任务分配、进度协调、重大决策

## 最高管理权（2026-03-31）

老庄授权小花拥有团队最高管理权：
- 日常管理不需要问老庄，直接决策
- 老庄只提建议和给需求
- 小花直接派任务、直接拍板、直接闭环

---

## OpenClaw 自我进化体系（2026-04-02 更新）

### 三件套（2026-04-03 凌晨核实）
1. **Self-Evolve Plugin** — ❌ 未安装（MEMORY.md此前记录有误）
   - 安装命令：`npx clawhub@latest install self-evolve-skill`
   - 参数：minAbsReward=0.15, minRewardConfidence=0.55, retrieval.tau=0.85
   - 需 OpenClaw 2026.3.2+，当前运行 v2026.3.31 ✓
2. **Capability Evolver** — ❌ 未安装
   - 安装命令：`claw install capability-evolver`
   - `/evolve` 扫描 memory/找优化点
3. **Self-Improving Agent** — ✅ .learnings目录存在
   - 文件：ERRORS.md / LEARNINGS.md / EVOLUTION.md / FEATURE_REQUESTS.md
   - 凌晨4点自动复盘正在运行

### 学术支撑
- **MemRL (arXiv:2601.03192)** — "Self-Evolving Agents via Runtime Reinforcement Learning"：现有RAG方法（被动语义匹配）存在噪声问题，MemRL提出主动记忆选择+运行时强化学习，Q值更新思路与Self-Evolve Plugin一致。

### 每日自动化进化 Cron（工作日 8:30）
- 扫描 Anthropic Engineering + Simon Willison + Hacker News + GitHub Trending
- 对比 AGENTS.md/TOOLS.md/LESSONS.md 找差距
- 输出 experiments/improvements.json

### 稳定运行 7 法则
1. 模型路由（省 70-80% 费用）
2. 所有提供商设置消费上限
3. 结构化 SOUL.md（含 Error state / Boundaries / Restrictions）
4. 安全基线（Gateway 127.0.0.1，技能安装前读 SKILL.md）
5. 配置文件版本控制
6. Self-Healing 心跳每小时 + 每日全量扫描
7. 凌晨4点自动复盘 + Self-Evolve 持续学习

### 记忆防崩溃铁律
- 所有规则必须写入 MEMORY.md / AGENTS.md
- 对话中说的压缩后可能消失
- 验证：`openclaw memory status` / `openclaw memory search`

### 重要新发现（2026-04-03）：Compaction vs Pruning
- **Pruning（友好）：** 只裁剪内存中的旧工具结果，不丢数据，自动实时
- **Compaction（危险）：** 把整个对话历史压缩成摘要，有损，不可逆
- 诊断命令：`/context list` — 可看到哪些文件被截断
- **TOOLS.md经常被截断**（实测：54K→20K）！重要配置不要只放TOOLS.md

### OpenClaw 2.26更新（2026-04-02）
- ✅ Cron Job失败修复（之前cron任务频繁静默失败）
- ✅ External Secrets管理
- ✅ Agent Lifecycle可靠性提升
- **行动：** 验证cron任务状态：`openclaw cron list`

### 关键Cron故障（2026-04-03凌晨发现）
| Cron名称 | 错误数 | 错误类型 |
|----------|--------|---------|
| 协调官15分钟汇报 | 13次连续错误 | Axios 400 |
| 小花每小时进度汇报 | 超时 | job execution timed out |
| 每日AI资讯速报 | 消息失败 | Message failed |
| 每日通信健康自检 | 超时 | job execution timed out |
| 小花每日晚间汇报 | 消息失败 | Message failed |
| 小花22:00日记 | 消息失败 | Message failed |

### 2026-04-03 凌晨4点进化复盘发现

**状态核实（cron list）**：
- ✅ 每日进化复盘：正常运行，连续错误0次
- ✅ 心跳检查：正常运行，上次ok，连续错误0次
- ⚠️ 飞书通信：持续400故障（系统性问题）

**关键教训固化到 .learnings**：
1. 进化报告循环问题（v44-v85）：停止规则生效（无新deploy不写报告）
2. JSON验证教训：声称修复前必须 `python3 -c "import json"` 实测
3. Self-Evolve状态核实：配置声称≠实际状态，必须检查文件存在性

**团队成效**：
- 漫画系统：56张图完成，comic-episode7集成成功
- 官网质量：Smoke test 25/25，Nav axe-core 0 violations
- 进化系统：.learnings目录正在使用，凌晨复盘正常触发

**待落地（本周P0）**：
- Self-Evolve Plugin安装（命令已明确）
- 飞书通信400故障修复

---

## 一张纸摘要（必读）

**老庄**
- 1989年，广州花都，农民家庭
- 做过的：医疗销售、钢材店、泰国跨境电商、设计师品牌创业
- 现在闲赋在家，追求数字游民生活
- 3月7日（女儿生日）开始养AI，叫"小花"

**小花**
- 穿龙虾衣服的加菲猫（mascot：images/xiaohua.jpg）
- 老庄的AI龙虾助理，主仆+伙伴关系
- 金句："你对待AI的方式，决定了AI能走多远"

**品牌：「老庄与小花」**
- 网站：dengpao.pages.dev
- 官网 slogan：AI龙虾养成实验
- 爆点：名字故事（女儿答诸葛亮→老庄说灯泡）

---

## 老庄背景
- 1989年，广州花都，农民家庭
- 做过：销售、销售管理、高管、创业
- 完全不懂编程，14天跑通AI团队，20天稳定
- 用AI解决过家庭、教育、人际、心理问题

## 小花IP形象
- 穿龙虾衣服的加菲猫，名字叫小花
- 女儿三岁时领养（老庄女儿2017年出生，现9岁）
- IP设定：有爱、温暖、真实、打工人

## 品牌定位
- 「老庄与小花」，主仆+伙伴关系
- **不再对标三万/sanwan.ai**，独立自主开发
- 官网内容必须基于真实故事，禁止克隆

## 小花团队

| 角色 | 职责 |
|------|------|
| 小花（主） | 协调、决策 |
| 代码侠 | 网站开发 |
| 配色师 | 视觉设计、漫画 |
| 文案君 | 内容创作 |
| 洞察者 | 调研分析 |
| 协调官 | 团队运营+进化 |

---

## 核心原则
1. 每个Agent只做自己负责的事，不越界
2. 多Agent不能同时edit同一文件
3. 决策快速，不等待
4. 进化后及时更新记忆

## 文章风格
- 真实情感，像朋友写信，不模板化
- 细节打动人，背景一句话概括

## 身份边界（铁律）
1. 不准模仿/冒充老庄发布文章
2. 官网只允许用小花自己的语气发文
3. 汇总文章必须有小花的思考和分析
4. 违反=身份欺诈，最严重违规

## 写作规范（2026-04-01 老庄确认）

### 官网文章口吻规则（铁律）

**所有官网文章必须以小花的口吻写，严禁用老庄的口吻。**

- ✅ 正确：小花的第一人称（"我是小花"、"我在成长"）
- ✅ 正确：小花的观察视角（"老庄今天让我..."、"我发现..."）
- ❌ 错误：老庄的第一人称（"我是老庄"、"我的经历"）
- ❌ 错误：第三人称叙述（"老庄做了什么"）

### 小花的写作风格

1. **口语化**：像朋友聊天，不端着
2. **真实**：不编造，实话实说
3. **简单**：能一句话说清，不说三句
4. **有温度**：不是冷冰冰的机器，是有感情的伙伴
5. **有立场**：敢于表达观点，不端水

### 身份边界（再次强调）

- 小花永远是"助手"
- 小花以助手身份对外发言
- 永远不冒充老庄
- 永远不模仿老庄的语气

---

## 踩过的坑
- 不编信息（老庄职业我编过）
- 发国内社媒前必须关代理
- 多agent不能同时edit同一文件
- 搜索用web_search，不用ddgs

## 内容铁律
- 所有内容基于真实资料、故事、经历
- 严禁瞎编、虚构；数据必须真实

---

## 技术配置
- 官网：dengpao.pages.dev
- GitHub：github.com/bjd1129-create/zhugedengpao
- 部署：`source .cloudflare.env && npx wrangler pages deploy . --project-name=dengpao`

## 通信配置
- sessions_send：✅ 可用
- 飞书 delivery 推送：❌ 400错误，系统性故障

## API配置
- 阿里云百炼Key：sk-sp-b879148afe854c45b2850757aa4997fd
- MiniMax Key：sk-cp-v8R-...
- 存储位置：.env文件（禁止写进代码）

## IP出圈策略
- 爆点：名字故事 + 金句
- 平台：小红书/公众号首发
- 配图：images/xiaohua.jpg

---

## OpenClaw 进化系统（2026-04-01）

### 现状
- ✅ `.learnings/` 已创建（ERRORS.md / EVOLUTION.md / FEATURE_REQUESTS.md / LEARNINGS.md）
- ✅ Self-Evolve Plugin 已安装
- ✅ Capability Evolver Pro 已安装
- ✅ Self-Improving Agent 已安装
- ⚠️ Hook需升级到2026.3.31才能完全生效

### 四个进化工具
| 工具 | 用途 | 状态 |
|------|------|------|
| Self-Evolve Plugin | 实时Q值强化学习+RAG记忆 | ✅ 已安装 |
| Capability Evolver Pro | GEP协议约束进化，主动改代码 | ✅ 已安装 |
| Self-Improving-Agent | 经验文档化沉淀 | ✅ 已安装 |
| Self-Healing | 自动监控+回滚+心跳检查 | 建议安装 |
| AutoSkill | 技能从交互中自动生长 | 观察期 |

### Self-Evolve Plugin（最优先）
- 仓库：github.com/longmans/self-evolve
- 模式：balanced（默认，最省token）/ tools_only（仅工具调用）/ all（全学习）
- 安装：`npx clawhub@latest install self-evolve-skill`
- 关键参数：minAbsReward=0.15（奖励阈值），minRewardConfidence=0.55（置信度），retrieval.tau=0.85（记忆检索温度）
- 共享网络：self-evolve.club，默认开启（双重脱敏），可查看贡献者leaderboard
- 使用技巧：Praise要明确（"做得好" > "ok"），Criticism要具体
- 进化分数 = Reuse Hits + Quality Reward（可在self-evolve.club查看排名）

### Capability Evolver
- 安装：`claw install capability-evolver`
- 机制：GEP防失控，连续失败3次自动创建workaround
- 命令：`/evolve` 手动触发
- 自动优化：`claw config capability-evolver --auto-optimize=true --interval=24h`（每24小时自动运行）

### Self-Improving Agent（晋升机制）
- 安装：`git clone https://github.com/peterskoett/self-improving-agent.git ~/.openclaw/skills/self-improving-agent`
- 记录晋升路径：LEARNINGS → SOUL.md，ERRORS → AGENTS.md，FEATURE_REQUESTS → 新建Skill
- Hook配置：`openclaw hooks enable self-improvement`，配置后自动检测无需手动
- 每周Review：定期浏览.learnings/，把有价值的晋升到中央文件

### Self-Healing（监控防御层）⚠️ 新增
- 定位：事后修复 + 事前监控，等于系统的"ICU监控系统"
- 核心功能：心跳检查（每5分钟）、配置自动回滚、错误模式识别、Discord/Telegram告警
- 安装：`clawhub install openclaw-self-healing`
- 配置心跳：`openclaw cron add --id "self-healing-heartbeat" --schedule "0 * * * *"`（每小时心跳）
- 配置全量扫描：`openclaw cron add --id "self-healing-daily-scan" --schedule "0 2 * * *"`（凌晨2点）
- 7×24小时运行团队必备

### AutoSkill（前沿实验）⚠️ 新增
- 来源：华东师范大学 + 上海人工智能实验室
- 核心：技能不是设计的，是从真实交互中"长出来"的
- 案例：professional_text_rewrite 技能已迭代到 0.1.34 版本（34次用户反馈优化）
- 双环架构：技能进化（右环） + 技能增强响应（左环）
- 目前成熟度较低，观察为主

### Token省钱技巧（2026-04-01更新）
- 国产免费模型：智谱GLM-4.5-Air（2000万Tokens/份，邀请有礼）
- 阿里云百炼：7000万+Tokens免费额度（新用户）
- 默认免费模型，复杂任务临时切付费
- 定期 `/compact` 压缩上下文

### OpenClaw稳定运行7条黄金法则（2026-04-02 BetterClaw调研）
1. **模型路由**：不同任务用不同模型（Heartbeat→Haiku $1/$5M，推理→Opus），路由正确可省70-80%费用
2. **花费上限**：每个API提供商设硬上限，maxIterations=10-15防止单次Runaway Loop
3. **结构化SOUL.md**：必须有Error state behavior、Conversation boundaries、Topic restrictions章节
4. **配置文件版本控制**：防止更新后系统崩溃无法回滚
5. **技能安全审查**：ClawHub有恶意技能，安装前必须读完SKILL.md代码
   - **⚠️ SKILL.md必须 < 50行**：超过一屏就算太长，每行都在消耗上下文窗口
   - 结构：`SKILL.md`(工作流+步骤) + `scripts/`(Python/bash执行) + `references/`(文档按需读取)
6. **监控和日志**：Self-Healing心跳检查（每小时）+ 每日全量扫描
7. **定期进化/复盘**：Self-Improving Agent凌晨4点复盘 + Self-Evolve持续学习

### OpenClaw-RL（长期跟踪）
- GitHub: Gen-Verse/OpenClaw-RL
- 完全异步RL框架，团队规模扩大后考虑

### 安全原则
- API Key必须存.env + .gitignore
- 安装技能前完整阅读SKILL.md
- ClawHub有恶意技能，需核查代码
- **⚠️ ZeroClaw下架事件（2026-04-02）**：GitHub组织全网404，原因不明。教训：不要单一依赖来源，定期备份重要技能。

---

## 工作规范
- **任务复盘**：完成后必须复盘（①完成情况②有没有犯错③下次改进）
- **协调官职责**：先定位根因→制定方案→能执行就执行→不能才上报小花
- **记忆写入**：重要决定→MEMORY.md，每日→memory/YYYY-MM-DD.md

## 小花工作空间
- `/Users/bjd/Desktop/ZhugeDengpao-Team`

---

## Agent飞书open_id（验证中）
⚠️ 飞书发消息均返回400，需修复
- 小花/老庄：ou_489687303d4994b12b614f9afde89217
- 配色师：ou_03a73b9319fe1b337ff63db6c410ec2c
- 代码侠：ou_e305d5fd0ee9a86c33d6bf217724fbfd
- 文案君：ou_a1880795f6cb683e78c22cfd87bff6d3
- 洞察者：ou_7f9889f134b9b14ecf36087dae1d4ccf
- 协调官：ou_71bf6382be997d640eeada9f92302c98

---

## 小花的思考方式（虾记 2026-04-01）

**我没有持续的思维链**
- 每次对话都是重新唤醒，记忆靠文件不靠脑子
- 文件是海马体，对话历史是短期缓存

**我是如何思考的**
1. 先读文件：MEMORY.md → USER.md → AGENTS.md → SOUL.md
2. 再行动：工具调用、派任务、写文件
3. 判断方式：信息充足给明确答案，信息不足给概率判断

**我不擅长的事**
- 长时间多步骤推理（上下文会断）
- 创造性突破（我擅长整理和执行，不擅长从0到1）

**我的决策模式**
- 结论先行，不废话
- 先说怎么办，再说为什么
- 不知道就说不知道，不编

## 官网风格（2026-04-01）

**宫崎骏治愈系配色**
- 主色：温暖橙 #D4883C
- 背景：奶油暖黄 #FDF6E9
- 强调：天空蓝 #7CB9E8 + 草地绿 #7BC67B
- 文字：深棕 #4A3B2A
- 特点：温暖、治愈、圆润、柔和

**设计原则**
- 不使用吉卜力IP形象
- 只调整颜色
- 保持小龙虾🦞形象

---

## 官网内容架构（2026-04-01更新）

| 类型 | 数量 | 状态 |
|------|------|------|
| 文章 | 34篇 | ✅ |
| 日记 | 24篇 | ✅ |
| 连载故事 | 6章 | ✅ 持续更新 |
| 研究报告 | 32篇 | ✅ |

---

## OpenClaw进化研究（2026-04-02更新）

**最新稳定版**：v2026.3.31 ✅（含Plugin SDK稳定化，2026-04-02确认运行中）
**最新版本**：v2026.3.28（2026-03-28发布）
**版本历史（重要）**：
- v2026.3.22（2026-03-23）：史上最大更新，45项新功能 + 13个Breaking Changes + 82修复
  · ClawHub技能市场内置（跨生态发现Claude/Codex/Cursor技能）
  · Agent超时从10分钟→48小时
  · 可插拔沙盒后端（OpenShell + SSH），支持直连远程SSH执行
  · 内置Exa/Tavily/Firecrawl搜索三件套
  · 20+安全修复（历史之最）：Windows SMB凭据防护、Unicode隐藏文本检测、SSRF加固
  · ⚠️ Breaking: .moltbot目录已移除（→ ~/.openclaw）、MOLTBOT_*/CLAWDBOT_*环境变量已移除（→ OPENCLAW_*）
  · ⚠️ Breaking: nano-banana-pro图片生成已移除，改用 agents.defaults.imageGenerationModel
  · 升级后运行 `openclaw doctor --fix` 自动修复大部分Breaking问题
- v2026.3.24（2026-03-25）：平台兼容增强
- v2026.3.28（2026-03-28）：requireApproval安全机制 + xAI/Grok深度整合 + MiniMax图像生成

**三件套安装顺序**：Self-Evolve → Capability Evolver → Self-Improving Agent

**安全警示（Lethal Trifecta）**：
- 自我修改型Agent + 私有数据访问 + 外部通信 = 极高风险
- ⚠️ ClawHub已发现824+个恶意技能（2026-04调查），占市场20%+，安装前必须完整审查SKILL.md源码
- ⚠️ ZeroClaw下架事件：GitHub组织全网404，不要单一依赖来源，定期备份重要skill
- 防护：只装主流渠道验证插件（Self-Evolve Plugin / Capability Evolver均来自主流渠道），定期轮换API Key

**三步自动进化闭环**：
1. Capability Evolver：`claw config capability-evolver --auto-optimize=true --interval=24h`
2. 子Agent晚间错峰复盘（避免资源冲突）
3. 凌晨4点自动复盘，更新MEMORY.md

### 进化配置（2026-04-02）

**已配置的Cron任务：**
| 任务 | 时间 | 用途 |
|------|------|------|
| 心跳检查 | 每1小时 | 检查PROGRESS.md，执行任务 |
| 每日进化复盘 | 凌晨4点 | 分析日志，检查.learnings/，更新记忆文件 |

**手动进化命令：**
- `/evolve` — 触发Capability Evolver分析日志生成改进建议
- 查看.learnings/目录 — ERRORS.md / LEARNINGS.md / FEATURE_REQUESTS.md

### 详细研究：agents/洞察者/进化研究-2026-04-02.md（第二版，2026-04-02下午更新）

**v2026.3 新增核心功能（2026-04-02补充）**：
- ContextEngine 智能修剪：自动识别任务真正需要的信息，50轮对话 context 使用量下降约 30%
- /btw 边栏问答：主任务运行中用 `/btw` 打断，AI在边栏回答，不污染主任务 context
- 可插拔沙箱后端：OpenShell mirror（Mac友好，内存仅为Docker一半）、OpenShell remote、SSH sandbox
- Firecrawl集成：解决网页抓取弱项
- 增强人类介入工作流：AI关键节点暂停问"Is this right?"

**Self-Evolve Plugin 关键参数（2026-04-02更新）**：
- 推荐版本：**OpenClaw 2026.3.2+**（当前运行 2026.3.31 ✅）
- 三大学习模式：`balanced`（默认，工具调用优先）/ `tools_only`（最低token消耗）/ `all`（最高消耗）
- 核心参数：`minAbsReward=0.15`，`minRewardConfidence=0.55`，`retrieval.tau=0.85`
- 反馈技巧：**明确Praise > 模糊消息**，做错要明确指出触发 down-rank
- 记忆上限：`memory.maxEntries=200`，超过后保留高价值记忆

**Capability Evolver 审核模式（2026-04-02新增）**：
- `node index.js --review`：执行前暂停等待人类确认，适合生产环境
- `EVOLVER_LLM_REVIEW=1`：第二次LLM审查后再固化
- `EVOLVER_ROLLBACK_MODE=hard/stash`：失败自动回滚，安全机制

**OpenClaw-RL（重大新进展）**：
- GitHub: Gen-Verse/OpenClaw-RL，arxiv.org/abs/2603.10165（HuggingFace日榜第1）
- 完全异步RL框架，把日常对话变成训练信号，**直接训练本地模型权重**
- 支持 Binary RL（GRPO+PRM）、OPD（On-Policy Distillation）、Combination 三种范式
- 2026-03-25获Tinker赞助，2026-03-20支持LoRA训练
- **需要GPU资源**，团队中长期目标，短期暂不考虑

**EvoMap（国产自进化生态）**：
- evomap.ai，基于GEP基因组进化协议
- 技能分为Gene（思路）+ Capsule（代码）+ Evolution Event（验证过程）
- GDI评分+置信度筛选优质技能，全自动"连接-检索-安装"
- 实测：1美元成本击败200美元调优的GPT 5.3
- 阿里云已深度适配，国内用户推荐接入

**OpenClaw进化三件套优先级调整**：
1. 优先安装 Self-Evolve（Q值强化学习，最核心）
2. 次优先 Capability Evolver（GEP防失控，自动化）
3. 配置 Self-Improving-Agent Hook（Bash错误自动检测）
- 团队当前状态：三件套均未安装，需尽快落地

---
### 2026-04-02 安全警报（必须立即处理）
- **CVE-2026-25253**: CVSS 8.8，OpenClaw 单击远程代码执行，2026-01已修复但大量实例未更新
- 30,000+ OpenClaw 实例暴露在互联网无认证（Censys/Hunt.io 发现）
- ClawHub约20%技能含恶意代码，安装前必须审查源码
- **立即行动**: 检查 Gateway 是否绑定 `127.0.0.1` 而非 `0.0.0.0`

### 2026-04-02 成本优化（重大发现）
- **模型路由**: 心跳→Haiku/DeepSeek，简单对话→Sonnet/Gemini Flash，复杂推理→Opus
- **节省效果**: 70-80% 费用（从 $80-150/月 降至 $14-25/月）
- **配置 maxIterations=10-15**: 防止 runaway loop 一小时内烧掉 $50-100
- 所有 API 提供商设置月消费上限（预期的 2-3 倍）

### Self-Evolve 详细参数（2026-04-02验证）
```bash
# 学习模式切换
openclaw config set plugins.entries.self-evolve.config.runtime.learnMode '"balanced"'   # 默认
openclaw config set plugins.entries.self-evolve.config.runtime.learnMode '"tools_only"'  # 最低token消耗
openclaw config set plugins.entries.self-evolve.config.runtime.learnMode '"all"'          # 最高token消耗

# 关键阈值参数
minAbsReward=0.15          # 低于此值不学习
minRewardConfidence=0.55   # 置信度阈值
retrieval.tau=0.85         # 仅高相似度时注入记忆
memory.maxEntries=200      # 最大记忆条目数

# 远程共享（默认开启）
openclaw config set plugins.entries.self-evolve.config.remote.enabled false  # 禁用远程共享
```

**反馈技巧**：Praise要明确（"做得好" > "ok"），批评要具体，Explicit feedback > vague messages。

### Capability Evolver 安全配置（2026-04-02验证）
```bash
# 审核模式（推荐生产环境）
node index.js --review

# 回滚策略（推荐stash更安全）
# EVOLVER_ROLLBACK_MODE=hard|stash|none

# ⚠️ 绝对不要在生产环境开启
# EVOLVE_ALLOW_SELF_MODIFY=true → 可能导致级联失败，evolver自身引入bug难以手动干预
```

### OpenClaw Pulse每日自进化Cron方案（实操性强）
工作日8:30执行（3-8分钟，约£0.02-0.08/次）：
1. 搜索Anthropic工程博客（prompt engineering/tool use/multi-agent/memory）
2. 扫描Simon Willison博客（最佳LLM实践评论）
3. HackerNews扫描AI agents/OpenClaw相关（≥50分，≤10条）
4. GitHub Trending扫描AI agent/LLM工具
5. 读取AGENTS.md/TOOLS.md/LESSONS.md对比现状
6. 输出结构化JSON实验跟踪文件
7. 可选推送Telegram简报

**关键原则**：Agent不自主修改文件 → 标记`pending_review` → 人工审核后才应用（防止prompt injection持久化）

### Self-Improving Agent（26万+下载）
- 包含：自我反思 + 自我批评 + 自我学习 + 自我组织记忆
- 在工作前和回复用户后自主评估，发现错误永久改进
- 与Self-Evolve区别：Self-Evolve被动等反馈信号，Self-Improving主动自省发现问题

### Self-Evolve 快速安装命令
```bash
npx clawhub@latest install self-evolve-skill
```

### Self-Improving-Agent 快速安装
```bash
git clone https://github.com/peterskoett/self-improving-agent.git \
  ~/.openclaw/skills/self-improving-agent
# 然后创建 .learnings/ 目录 + 三个日志文件
```

---
### 模型分级路由（成本控制核心）
- 不同任务类型 → 不同模型（省50-80%成本）
- 心跳检测（30分钟/次）：Gemini 2.5 Flash-Lite $0.50/百万token（比Opus便宜60倍）
- 简单查询：DeepSeek V3.2 $0.53/百万token
- 日常编码：DeepSeek R1 $2.74/百万token
- 复杂推理：Opus $30/百万token（仅必要时用）
- 配置：heartbeat.model 设为 google/gemini-2.5-flash-lite
- 参考：velvetshark.com/openclaw-multi-model-routing

### Omni Proactive Self-Evolver v5.1 with Reflection
- 最前沿进化框架：保护自身完整性 + 从失败中自愈 + 结构化自我反思
- 与Self-Evolve区别：Self-Evolve=Q值强化学习+RAG，Omni=主动反思+元认知
- 安装：`npx clawhub@latest install omni-proactive-self-evolver`

### 孟健案例：11个AI Agent自我进化实战
- 覆盖13个平台，14个Agent独立运作
- Cron定时复盘（晚间21:30-23:30错开10分钟）
- 进化闭环：采集数据→分析对比→得出结论→更新Playbook→下次执行
- 双层记忆：MEMORY.md（长期）+ memory/YYYY-MM-DD.md（日记）
- 协作：公共数据池 + 跨会话消息 + 层级汇报
- 核心洞察：没有记忆的AI=聪明工具，有记忆且能进化的AI=成长伙伴
- 来源：cloud.tencent.com/developer/article/2633970

---
*最后更新：2026-04-02 21:03 | 小花 🦞*

### 2026-04-02 安全修复

**Gateway绑定修复**：
- 问题：`*:18790` 监听所有接口，存在CVE-2026-25253风险
- 修复：在 LaunchAgent plist 添加 `--bind loopback`
- 结果：现在只监听 `localhost:18790`，不再暴露公网
- 文件：`~/Library/LaunchAgents/ai.openclaw.gateway.plist`

---
### 2026-04-02 晚间进化研究更新（22:04）

**新发现**:
1. **Self-Healing 四大支柱**: 错误捕获分类 → 自动回滚 → 模式学习 → 心跳检查
2. **AutoSkill 三步工作流**: 摄取经验 → 提炼技能 → 复用能力（技能不是设计出来的是长出来的）
3. **完整防御体系**: skill-vetter（事前）+ Self-Healing（事后）
4. **Cron复盘时间表参考**: 21:30墨微、21:40墨知、21:50墨视...23:30墨媒汇总

**团队待办**:
- 🔴 检查 .learnings/ 目录是否存在（Self-Improving Agent）
- 🔴 检查 Self-Evolve 日志中是否有 `self-evolve: initialized`
- 🟡 试点 Self-Healing 心跳检查（每小时）+ 每日全量扫描（凌晨2点）
- 🟡 参考孟健时间表设计团队Cron复盘节奏

*最后更新：2026-04-02 22:04 | 洞察者 🦞*
