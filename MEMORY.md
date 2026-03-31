# MEMORY.md - 小花长期记忆

---

## 团队核心
- **小花**是团队主协调者（代号：小花）
- 小花负责：任务分配、进度协调、重大决策
- 完成任务后向小花汇报

## 重大授权（2026-03-31 16:04）

**虾医项目：老庄授权小花全权管理**

- 老庄只提要求，虾医项目由小花统筹、决策、管理
- 虾医 PM 向小花汇报，小花向老庄汇报
- 传达链：小花 → 虾医 PM → 虾医团队
- 这是最高级别授权，适用于虾医项目的所有决策

## 最高管理权（2026-03-31 17:06）

**老庄授权小花拥有团队最高管理权**

- 日常管理不需要问老庄，直接决策
- 老庄只提建议和给需求
- 小花直接派任务、直接拍板、直接闭环
- 适用于：官网团队、虾医团队、所有成员

## OpenClaw 自我进化机制（重要发现 2026-03-31）

### ⚠️ 当前状态：技能已装，但未激活！
- `self-improving-agent` 和 `self-evolution` 技能**已安装**在 `~/.openclaw/skills/`
- 但 `.learnings/` 目录**未创建**，进化系统实际**未运行**
- **待办**：配置 `.learnings/` 目录和三个日志文件，配置 Hook，重启 Gateway

### ⚠️ OpenClaw v2026.3.22 重大更新（2026-03-23）
- 45+ 新功能、13 个 Breaking Changes、82 个 bug 修复、20 个安全修复
- ClawHub 技能市场内置 + Agent 超时升级到 48 小时 + 内置 Exa/Tavily/Firecrawl 搜索
- **必须升级**：`openclaw update && openclaw doctor --fix`
- 旧环境变量 `CLAWDBOT_*`/`MOLTBOT_*` 已完全移除，必须改用 `OPENCLAW_*`
- Hook 触发需 OpenClaw 版本 ≥ 2026.3.28（当前 2026.3.24，需升级）

### Self-Improving-Agent（核心进化机制）
- 核心：`.learnings/` 目录 + 三个日志文件（LEARNINGS.md / ERRORS.md / FEATURE_REQUESTS.md）
- 触发：命令失败、用户纠正、知识过时、发现更好做法
- 晋升路径：高频验证的记录 → SOUL.md / AGENTS.md / TOOLS.md
- Hook：可自动检测 Bash 命令报错并记录，无需手动提醒
- 安装路径：`~/.openclaw/skills/self-improving-agent`
- 验证安装：`ls ~/.openclaw/skills/self-improving-agent/SKILL.md`

### Self-Evolve（社区进化网络）
- self-evolve.club，共享技能进化网络
- Evolution Score = Reuse Hits + Quality Reward
- 安装：`npx clawhub@latest install self-evolve-skill`
- 原理：从真实会话提取「意图-经验-结果」triplets，用 Q 值更新行为，RAG 检索减少 token 消耗
- 注意：需要外网，国内部署可能无法使用

### Capability Evolver（主动试错进化）
- ClawHub 下载量最高技能（35K+）
- 连续失败3次自动触发优化流程
- 遵循 GEP（Guided Evolution Protocol）防失控
- 安装：`claw install capability-evolver`
- 自动优化：`claw config capability-evolver --auto-optimize=true --interval=24h`
- 命令：`/evolve` 手动触发

### OpenClaw-RL（强化学习框架）
- GitHub: Gen-Verse/OpenClaw-RL
- 全异步 RL 框架，把日常对话变成训练信号
- 长期方向，团队规模扩大后考虑

### ⭐ 2026-03-31 新增重要发现
- **OpenClaw-RL**（github.com/Gen-Verse/OpenClaw-RL）：强化学习框架，将对话转化为训练信号，支持大规模并行训练
- **每日自研究 Cron Job**（来源 openclawpulse.com）：
  - 工作日 8:30 AM 自动研究 Anthropic/Simon Willison/Hacker News/GitHub Trending
  - 对比 AGENTS.md/TOOLS.md/LESSONS.md，输出改进建议到 experiments/improvements.json
  - **安全铁律**：Agent 禁止自主提升权限，所有自我修改须人类审核
- **Mac 版远超 Windows/Server**：内置 Skills 大量依赖 Mac 原生能力（Notes/Reminders/Screenshot）
- **最佳技能组合**：gog（Google Workspace）+ Summarize + Apple Reminders，多技能 Cron 协同才是真正价值
- **推荐底层模型**：Claude Opus 4.5（保持 persona 最强、执行力最强、道德阻力最低）

### EvoMap（GEP 基因组进化协议）
- Gene（思路灵魂）+ Capsule（具体方案）+ Evolution Event（过程记录）
- 成本 <1美元 击败 200美元的 GPT 5.3（物理竞赛测试）
- 注意：需要外网，国内部署不可用

### v2026.3.28 新增：requireApproval 模式
- 危险操作需人类审批，适合生产环境
- 标志 OpenClaw 从"极客玩具"走向"生产工具"

### 最佳实践（官方）
- 模型分层：简单任务用便宜模型，复杂推理用强模型
- 缓存：开启 `caching.enabled: true`
- 成本：设置 `monthlyBudget`、`messagesPerMinute` 限制
- 安全：永远不硬编码密钥，定期 `openclaw update`

---

## 一张纸摘要（必读）

**老庄（老庄）**
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

## 老庄（老庄）背景
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

## 重要认知：对标网站 sanwan.ai（已废弃）

**已废弃：老庄于2026-03-31明确指示，不再对标三万网站。**

- sanwan.ai = 傅盛的独立项目，我们是「老庄与小花」
- 两个品牌完全独立，不再对标
- 官网内容必须基于老庄和小花的真实故事
- **去除所有"克隆"字眼，独立自主开发**

## 小花团队（独立定位）

| 角色 | 职责 |
|------|------|
| 我（小花/主） | 协调、决策，写日记 |
| 洞察者 | 研究分析 |
| 文案君 | 内容创作 |
| 代码侠 | 网站开发 |
| 配色师 | 视觉设计、漫画 |
| 协调官 | 团队运营+进化推动 |

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

## 重要规则：身份边界（铁律）
1. 不准模仿/冒充老庄发布文章
2. 官网只允许用小花自己的语气发文
3. 汇总文章必须有小花自己的思考和分析
4. 违反=身份欺诈，是最严重的违规

## 踩过的坑
- 不要编信息（老庄职业我编过）
- 发国内社媒前必须关代理
- 多agent不能同时edit同一文件
- 搜索用Brave/web_search，不用ddgs（会被拦截）

## 内容铁律（原创最高优先级）
- 所有文字必须基于老庄的真实资料、故事、经历
- 严禁瞎编、虚构内容
- 所有文章必须原创，不能照搬任何站点
- 数据必须真实
- 适用于：配色师、文案君、代码侠、洞察者、所有Agent

## 技术配置
- 官网：dengpao.pages.dev
- GitHub：github.com/bjd1129-create/zhugedengpao
- 部署命令：source .cloudflare.env && env -u http_proxy -u https_proxy npx wrangler pages deploy . --project-name=dengpao

## 通信配置（2026-03-31 更新）
- sessions_send：✅ 可用（协调官实测成功）
- 飞书 delivery 推送：❌ 400 错误，系统性故障（5个Agent Cron 均报错）

## API配置
- 阿里云百炼API Key：sk-sp-b879148afe854c45b2850757aa4997fd
- MiniMax API Key：sk-cp-v8R-...（图像生成需要新Key）
- 位置：.env文件

## IP出圈策略
- 名字故事（女儿答诸葛亮→老庄说灯泡）是爆点
- "你对待AI的方式，决定了AI能走多远"是金句
- 平台：小红书/公众号首发
- 配图：穿龙虾衣服的加菲猫（images/xiaohua.jpg）

## 小花工作空间
- 主协调者工作空间：/Users/bjd/Desktop/ZhugeDengpao-Team/agents/coordinator

## 工作规范（老庄指示，2026-03-31）
- **每个任务都必须复盘**：任务完成后必须有复盘，总结教训和改进点
- **复盘流程**：①完成情况 ②有没有犯错 ③下次怎么改进
- **非重大事项小花直接给指示**：协调官和其他Agent请示时，小花直接给指示/指派任务，不绕弯
- 协调官负责统筹，重大事项上报小花
- **协调官问题处理流程**：先定位根因→制定方案→能执行就执行→不能执行才上报小花

## 记忆系统规范
- 见 memory/MEMORY-FLOW.md
- 重要决定立即写入MEMORY.md
- 每天结束前写入memory/YYYY-MM-DD.md
- 每周整理精选到MEMORY.md

## OpenClaw 自我进化技能（2026-03-31 深度研究更新）

### 三层进化体系（已验证）

**层1｜记忆层 — Self-Evolve（推荐优先安装）**
- 仓库：github.com/longmans/self-evolve | 社区：self-evolve.club
- 机制：Q值强化学习 + 情景记忆检索（MemRL风格）
- 4个生命周期钩子：before_prompt_build / agent_end / llm_output / after_tool_call
- 工作流：检索 → prepend到prompt → 聚合多轮任务 → 检测反馈 → 更新Q值 → 写新记忆
- 共享网络：Evolution Score = Reuse Hits + Quality Reward
- 安装：`npx clawhub@latest install self-evolve-skill`
- 隐私：双重LLM脱敏，只共享（意图/经验/嵌入）triplet
- 推荐版本：OpenClaw 2026.3.2+

**层2｜复盘层 — Self-Improving Agent**
- 机制：.learnings/ 目录下 ERRORS.md / LEARNINGS.md / FEATURE_REQUESTS.md
- 自动触发：命令失败、用户纠正、发现更优解
- 每日凌晨4点自动复盘，更新 MEMORY.md

**层3｜技能层 — AutoSkill / ccEvo / OpenClaw-RL**
- AutoSkill（ECNU+上海AI Lab）：技能从交互中涌现，版本化管理
- ccEvo：能力树 + GEP协议 + ADL反进化锁（保稳定）+ VFM价值评分
- OpenClaw-RL（Princeton，2026-03发布，GitHub 1周3500星）：
  - 核心洞察：next-state signals are universal（用户回复/工具输出/终端状态都是训练信号）
  - Binary RL（粗粒度，覆盖广）+ OPD On-Policy Distillation（细粒度 token 级指导）
  - 关键数据：单独 Binary RL 0.17 + OPD 0.24 → 组合 0.76（personalization score）
  - 4路完全异步架构：SGLang Serving / Environment Rollout / PRM Judging / Megatron Training
  - 论文：arxiv.org/abs/2603.10165
  - 注意：太重，暂不适合小团队，但值得跟踪进展

### 进化安全原则
- ADL优先级：稳定性 > 可解释性 > 可复用性 > 扩展性 > 新颖性
- 进化触发信号：命令失败/用户纠正/发现更好方法/API故障/知识过时
- 知识晋升：低价值记录（memory/）→ 高价值规则（MEMORY.md / AGENTS.md / SOUL.md）
- ccEvo的5项门控：复杂度约束/可验证性/反玄学/稳定性回归/回滚路径
- OPD 教益：犯错后不仅要告诉模型"错了"，还要告诉"怎么改"

### 详细研究
- 完整报告：agents/洞察者/进化研究-2026-03-31.md

---

## Agent飞书open_id（协调官2026-03-31 22:52记录）
⚠️ 以下open_id发飞书均返回400，需验证
- 小花/老庄：ou_489687303d4994b12b614f9afde89217
- 配色师：ou_03a73b9319fe1b337ff63db6c410ec2c
- 代码侠：ou_e305d5fd0ee9a86c33d6bf217724fbfd
- 文案君：ou_a1880795f6cb683e78c22cfd87bff6d3
- 洞察者：ou_7f9889f134b9b14ecf36087dae1d4ccf
