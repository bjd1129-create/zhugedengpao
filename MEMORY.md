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
- ⚠️ Hook需升级到2026.3.31才能完全生效
- 🆕 2026-04-01 调研补充：Self-Healing + AutoSkill

### 四个进化工具
| 工具 | 用途 | 状态 |
|------|------|------|
| Self-Evolve Plugin | 实时Q值强化学习+RAG记忆 | 待安装 |
| Capability Evolver | GEP协议约束进化，主动改代码 | 待安装 |
| Self-Improving-Agent | 经验文档化沉淀 | 已装 |
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

### OpenClaw-RL（长期跟踪）
- GitHub: Gen-Verse/OpenClaw-RL
- 完全异步RL框架，团队规模扩大后考虑

### 安全原则
- API Key必须存.env + .gitignore
- 安装技能前完整阅读SKILL.md
- ClawHub有恶意技能，需核查代码

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

**最新稳定版**：v2026.3.23-2（含Plugin SDK稳定化）
**最新版本**：v2026.3.28（2026-03-29发布，Breaking变更）
- Qwen认证迁移至Model Studio（旧版OAuth已移除）
- xAI捆绑包升级至Responses API + x_search原生搜索
- 新增MiniMax图像生成（image-01，支持图像编辑）
- 工具执行审批钩子（requireApproval）支持暂停等用户确认
- 配置迁移规则调整：仅保留近两月配置

**三件套安装顺序**：Self-Evolve → Capability Evolver → Self-Improving Agent

**安全警示（Lethal Trifecta）**：
- 自我修改型Agent + 私有数据访问 + 外部通信 = 极高风险
- ClawHub发现341个恶意技能，1.5M tokens泄露
- 防护：只装主流渠道验证插件，定期轮换API Key

**三步自动进化闭环**：
1. Capability Evolver：`claw config capability-evolver --auto-optimize=true --interval=24h`
2. 子Agent晚间错峰复盘（避免资源冲突）
3. 凌晨4点自动复盘，更新MEMORY.md

详细研究：agents/洞察者/进化研究-2026-04-02.md

---
*最后更新：2026-04-02 01:15 | 小花 🦞*
