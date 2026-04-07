# MEMORY.md - 小花长期记忆（精简版）

## 一张纸摘要（必读）

**老庄（毕锦达）**- 1989年，广州花都，农民家庭
- 销售→高管→创业，现在闲赋在家，目标数字游民
- 3月7日（女儿生日）开始养AI，叫"小花"

**小花**- 穿龙虾衣服的加菲猫（mascot：images/xiaohua.jpg）
- 老庄的AI龙虾助理，主仆+伙伴关系- 金句："你对待AI的方式，决定了AI能走多远"

**品牌**：「老庄与小花」· dengpao.pages.dev

---

## 团队架构

### 交易团队 → 小花管
| Agent | 角色 | 工作空间 |
|-------|------|---------|
| 交易员 | 执行 | agents/trader/ |
| 策略师 | 智囊 | agents/strategist/ |
| 数据官 | 展示 | agents/dataviz/ |

### 官网团队 → 协调官管
| Agent | 角色 |
|-------|------|
| 配色师 | 设计 |
| 文案君 | 写作 |
| 代码侠 | 开发 |
| 洞察者 | 研究 |
| 协调官 | 协调 |

---

## 交易现状

### 加密货币网格 ⚠️ STOP_FILE生效
- 状态：100%现金，STOP_FILE锁死
- 文件：data/trading/STOP_TRADING.flag
- 教训：STOP_FILE必须放在main()之前

### 美股模拟盘（老虎证券）
- 模拟账户：21639635499102726，净值$1,000,000
- 策略：价值定投（SPY40% + QQQ30% + VTI20% + BND10%）

---

## 技术配置

- 官网：dengpao.pages.dev · GitHub：bjd1129-create/zhugedengpao
- 阿里云百炼：sk-sp-b879148afe854c45b2850757aa4997fd
- MiniMax图像：sk-cp-v8R-...（额度已耗尽）

---

## 重要教训

- ❌ 多agent不能同时edit同一文件
- ❌ 发国内社媒前必须关代理
- ❌ trading_simulator.py的STOP_FILE必须放在main()之前
- ✅ 改模拟器前先 cp portfolio.json portfolio.backup.json

---

## OpenClaw 进化体系（精简）

### 已装技能
| 技能 | 来源 | 核心 |
|------|------|------|
| Self-Evolve | longmans | Q值+情景记忆，共享技能网络 |
| Capability Evolver | OpenClaw官方 | 日志分析+自动修复 |
| Self-Improving Agent | pskoett | .learnings三文档体系 |

### 关键参数
- Self-Evolve：minAbsReward=0.15, tau=0.85, maxEntries=200
- Self-Evolve用bailian/qwen3.5-plus做reward/summarizer

### 进阶框架（待评估）
| 框架 | 来源 | 状态 |
|------|------|------|
| **OpenClaw-RL** | Gen-Verse | 待评估——支持对话反馈RL训练（Binary RL + OPD + LoRA），2026-04-04新增群体反馈优化 |
| AutoSkill | 华东师大+上海AI Lab | 待观察——技能从交互中"长出来" |

### 安全原则
- ❌ 不开启 be1human/self-evolve 全自主修改权限
- ❌ 安装技能前必须审查代码
- ✅ 小花触及"致命三要素"（私人数据+Web搜索+外部通信）

---

## 模型配置（当前）
- 主模型：minimax-portal/MiniMax-M2.7
- 备选：minimax-portal/MiniMax-M2.5-highspeed

---

*最后更新：2026-04-07 | 小花 🦞*
