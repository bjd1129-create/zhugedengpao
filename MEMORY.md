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
- v2026.3.22 Breaking Changes：CLAWDBOT_*/MOLTBOT_*环境变量已移除，全部改为OPENCLAW_*前缀

## 技术配置
- 官网：dengpao.pages.dev
- GitHub：github.com/bjd1129-create/zhugedengpao
- 部署命令：source .cloudflare.env && env -u http_proxy -u https_proxy npx wrangler pages deploy . --project-name=dengpao
- OpenClaw版本：v2026.4.2（已升级到最新）
- 升级命令：`npm install -g openclaw@latest`
- 诊断命令：`openclaw doctor --fix`

## API配置
- 阿里云百炼API Key：sk-sp-b879148afe854c45b2850757aa4997fd
- MiniMax API Key：sk-cp-v8R-...（图像生成需要新Key）
- 位置：.env文件

## IP出圈策略
- 名字故事（女儿答诸葛亮→老庄说灯泡）是爆点
- "你对待AI的方式，决定了AI能走多远"是金句
- 平台：小红书/公众号首发
- 配图：穿龙虾衣服的加菲猫（images/xiaohua.jpg）

## OpenClaw进化技术
- **OpenClaw-RL**（重要）：强化学习训练框架，arxiv.org/abs/2603.10165，#1 on HuggingFace Daily Papers。可用日常对话数据微调agent，建立"会话→训练轨迹→优化"闭环
- **self-evolve技能**：`openclaw skills install be1human/self-evolve`，授予agent自主修改配置/prompts/skills的权限
- **ClawHub**：内置技能市场（3286+ skills），`openclaw skills search/install/update`
- **v2026.4.1新功能**：/tasks任务看板、SearXNG搜索、飞书Drive评论事件流、Cron工具白名单

## 团队精简（2026-04-04）
- 已归档4个不活跃Agent：协调官(停摆)/产品官(03-31)/播种者(从未工作)/支持专员(03-30)
- 协调官workspace已移至 agents/_archive/coordinator-archived-2026-04-04
- 活跃团队：小花(主)/配色师/代码侠/文案君/洞察者
- 6.2MB协调官历史session已清理
- 2个协调官失败cron已移除

## GitHub分支保护（重要）
- main分支保护：需要1个审批才能合并PR
- 所有改动必须通过PR，不能直接push
- 预览分支：23eb33f0（Cloudflare直接deploy）

## 今日重要决定（2026-04-04）
- 老庄授予小花完全独立决策权（23:39，04-03）
- 官网所有事情小花全权决定，不需审核（23:39，04-03）
- 洞察者新增cron：9点/12点/18点监督团队健康+成员自我进化
- AutoSkill已安装（04-03 23:47）
- .learnings目录已初始化

## OpenClaw进化机制（补充）
- **Compaction**：对话接近context限制时自动压缩，compaction前会提醒agent保存记忆到memory
- **Hook系统**：可监听session:compact:before/after, agent:bootstrap, gateway:startup等事件
- **Bootstrap注入**：SOUL.md/AGENTS.md/MEMORY.md在每个turn自动注入context，是进化主战场
- **session-memory hook**：`openclaw hooks enable session-memory` 可自动保存session上下文
- 详情见：agents/洞察者/进化研究-补充-2026-04-04.md

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
