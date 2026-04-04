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

### 版本建议
- ✅ 推荐 OpenClaw 2026.3.2+（完整功能支持）
- ⚠️ 不推荐 2026.2.12（有已知bug）
- ✅ 2026.2.9 稳定可靠（备选）

### 立即行动清单
1. 升级到 OpenClaw 2026.3.2+
2. 安装 self-evolve 插件
3. 制定团队反馈规范（明确正/负反馈）
4. 建立 .learnings 目录结构

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
