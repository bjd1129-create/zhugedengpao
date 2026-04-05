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

### 自进化三大核心组件（2026-04-05更新）
1. **Self-Evolve**（longmans/self-evolve）
   - Q值强化学习 + 情景记忆 + 远程共享网络
   - 工作模式：balanced/tools_only/all
   - 关键参数：minAbsReward=0.15, tau=0.85
   - 远程共享需开启VPN

2. **Self-Improving Agent**（ClawHub）
   - 错误记录(ERRORS.md) + 经验沉淀(LEARNINGS.md) + 需求收集(FEATURE_REQUESTS.md)
   - 每日凌晨4点自动复盘

3. **AutoSkill**（华东师范大学+上海AI实验室）
   - 从真实交互自动提炼技能，版本化管理
   - 技能不是设计出来的，是长出来的

### 安全警示
- ⚠️ OpenClaw装在MBB's iMac（主力机）—— 不安全，待迁移
- ⚠️ CVE-2026-25253：RCE漏洞，需升级到2026.3+

### OpenClaw里程碑（2026-04）
- 100K GitHub Stars
- 每日自主执行：230万小时
- ClawHub技能：13,729个

---

## 今日重要决定（2026-04-05）

| 时间 | 决定 |
|------|------|
| 上午 | 整理工作空间：网站页面→website/pages，文档→website/docs |
| 上午 | 新增策略师飞书bot（cli_a94f7bcc64789cdd） |
| 上午 | 主agent workspace改为agents/xiaohua/（防止被覆盖） |
| 上午 | 修复子代理channel报错（heartbeat/cron） |

---

最后更新：2026-04-05 11:56 | 小花 🦞
