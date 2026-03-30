# Skills激活利用方案报告

> **研究时间**：2026-03-30
> **研究员**：洞察者（子Agent）
> **目标**：如何激活和充分利用128个Skills系统

---

## 团队核心
- **小花**是团队主协调者（代号：小花）
- 小花负责：任务分配、进度协调、重大决策
- 完成任务后向小花汇报

---

## 一、Skills现状总览

### 1.1 整体数据

| 指标 | 数量 |
|------|------|
| **总Skills数** | 128 |
| **可用Skills** | 92 |
| **缺依赖Skills** | 36 |

### 1.2 Skills来源分布

```
~/.n/lib/node_modules/openclaw/skills/     → OpenClaw内置（46个）
~/.openclaw/skills/                        → 老庄自定义（少量）
~/Desktop/ZhugeDengpao-Team/skills/        → 主Skills仓库（115+个）
~/.n/lib/node_modules/openclaw/dist/extensions/feishu/skills/ → 飞书插件（4个）
~/.n/lib/node_modules/openclaw/dist/extensions/*/skills/       → 其他插件（若干）
```

---

## 二、Skills分类整理（92个可用）

### 2.1 飞书生态（5个）⭐ 小花团队核心

| Skill | 功能 | 状态 |
|-------|------|------|
| `feishu-doc` | 飞书文档读写、表格、块操作 | ✅ 即用 |
| `feishu-drive` | 飞书云盘操作 | ✅ 即用 |
| `feishu-perm` | 飞书权限管理 | ✅ 即用 |
| `feishu-wiki` | 飞书知识库操作 | ✅ 即用 |
| `feishu-notification` | 飞书通知推送 | ✅ 即用 |

### 2.2 社交媒体运营（8个）⭐ 老庄与小花核心需求

| Skill | 功能 | 触发词 |
|-------|------|--------|
| `xiaohongshu-api` | 小红书数据API | 小红书、帖子、评论 |
| `xiaohongshu-all-in-one` | 小红书全套操作 | 小红书 |
| `xiaohongshu` | 小红书基础功能 | 小红书 |
| `xiaohongshu-title` | 小红书标题优化 | 标题 |
| `bilibili-all-in-one` | B站热门监控/下载/发布 | B站、Bilibili、热门 |
| `publish-x-article` | X/Twitter文章发布 | 发布文章 |
| `linkedin-api` | LinkedIn操作 | LinkedIn |
| `answeroverflow` | 答案Overflow查询 | 答案 |

### 2.3 开发与代码（15个）🔧 面向代码侠

| Skill | 功能 |
|-------|------|
| `api-dev` | API开发 |
| `cc-godmode` | Claude Code神级模式 |
| `cloudflare` | Cloudflare基础设施 |
| `Cypress` | Cypress测试 |
| `frontend` | 前端开发 |
| `frontend-design-ultimate` | 前端设计终极版 |
| `nextjs` | Next.js基础 |
| `nextjs-expert` | Next.js专家 |
| `playwright` | Playwright自动化+MCP+爬虫 |
| `playwright-scraper-skill` | Playwright爬虫 |
| `python-dataviz` | Python数据可视化 |
| `supabase` | Supabase数据库操作 |
| `Web Development` | Web开发综合 |
| `WebSocket` | WebSocket开发 |
| `stripe` | Stripe支付 |

### 2.4 代码审查（6个）🔍 质量保障

| Skill | 功能 |
|-------|------|
| `review-clean-code` | 清洁代码审查 |
| `review-doc-consistency` | 文档一致性审查 |
| `review-merge-readiness` | 合入就绪审查 |
| `review-quality` | 统一质量审查（入口） |
| `review-react-best-practices` | React最佳实践 |
| `review-seo-audit` | SEO审查 |

### 2.5 图像生成（4个）🎨 面向配色师

| Skill | 功能 |
|-------|------|
| `bailian-image-gen` | 阿里百川图像生成 |
| `image-cog` | 图像处理 |
| `minimax-image-gen` | MiniMax图像生成 |
| `qwen-image` | 通义千问图像 |

### 2.6 股票金融（5个）📈 面向投资研究

| Skill | 功能 |
|-------|------|
| `hk-ai-stock-expert` | 港股AI专家 |
| `stock-evaluator-v3` | 股票评估 |
| `stock-monitor` | 股票监控 |
| `stock_study` | 股票学习 |
| `us-stock-analysis` | 美股分析 |

### 2.7 工作流系统（8个）⚙️ 核心编排引擎

| Skill | 功能 | 用途 |
|-------|------|------|
| `workflow-brainstorm` | 头脑风暴 | 需求clarify |
| `workflow-creator` | 工作流创建 | 组合skills |
| `workflow-execute-plans` | 执行计划 | 分批执行 |
| `workflow-feature-shipper` | 特性发布 | 功能迭代 |
| `workflow-project-intake` | 项目 intake | 需求接入 |
| `workflow-ship-faster` | 快速发布 | 端到端交付 |
| `workflow-template-extractor` | 模板提取 | 模板复用 |
| `workflow-template-seeder` | 模板播种 | 快速启动 |

### 2.8 Meta Skills（4个）🧠 技能进化引擎

| Skill | 功能 | 重要性 |
|-------|------|--------|
| `skill-creator` | 创建新Skill | ⭐⭐⭐ |
| `skill-evolution` | 技能持续进化 | ⭐⭐⭐ |
| `skill-improver` | 改进Skills | ⭐⭐⭐ |
| `self-improvement` | 自我改进 | ⭐⭐⭐ |

### 2.9 工具类（13个）🔧 原子工具

| Skill | 功能 |
|-------|------|
| `tool-ast-grep-rules` | AST代码搜索 |
| `tool-better-auth` | Better Auth认证 |
| `tool-design-style-selector` | 设计风格选择 |
| `tool-hooks-doctor` | Hooks诊断 |
| `tool-openclaw` | OpenClaw操作 |
| `tool-programmatic-seo` | 程序化SEO |
| `tool-schema-markup` | Schema标记 |
| `tool-systematic-debugging` | 系统调试 |
| `tool-ui-ux-pro-max` | UI/UX设计 |
| `tool-x-article-publisher` | X文章发布 |
| `deep-research` | 深度研究 |
| `web-scraper` | 网页爬虫 |
| `web-search-plus` | 增强搜索 |

### 2.10 其他工具（13个）📦

| Skill | 功能 |
|-------|------|
| `agent-browser` | Agent浏览器控制 |
| `auto-updater` | 自动更新 |
| `gog` | Go服务 |
| `mcporter` | 移植工具 |
| `todo-tracker` | 待办跟踪 |
| `find-skills` | 技能搜索 |
| `elite-memory` | 精英记忆 |
| `humanizer` | 人性化 |
| `last30days` | 近30天 |
| `baidu-search` | 百度搜索 |
| `mcporter` | Minecraft |
| `github` | GitHub操作 |
| `gh-issues` | GitHub Issues |

---

## 三、36个缺依赖Skills分析

### 3.1 按依赖类型分类

**需要命令行工具（bins）**：
| Skill | 依赖 |
|-------|------|
| `apple-notes` | `memo` |
| `apple-reminders` | `remindctl` |
| `bear-notes` | `grizzly` |
| `blogwatcher` | `blogwatcher` |
| `blucli` | `blu` |
| `camsnap` | `camsnap` |
| `coding-agent` | `claude`, `codex`, `opencode`, `pi` 之一 |
| `eightctl` | `eightctl` |
| `gemini` | `gemini` |
| `himalaya` | `himalaya` |
| `imsg` | `imsg` |
| `model-usage` | `codexbar` |
| `nano-pdf` | `nano-pdf` |
| `obsidian` | `obsidian-cli` |
| `openai-whisper` | `whisper` |
| `peekaboo` | `peekaboo` |
| `session-logs` | `jq`, `rg` |
| `sherpa-onnx-tts` | 环境变量配置 |
| `songsee` | `songsee` |
| `sonoscli` | `sonos` |
| `spotify-player` | `spogo` 或 `spotify_player` |
| `summarize` | `summarize` |
| `things-mac` | `things` |
| `tmux` | `tmux` |
| `voice-call` | 配置项 |
| `wacli` | `wacli` |

**需要环境变量/API Key（env）**：
| Skill | 依赖 |
|-------|------|
| `goplaces` | `GOOGLE_PLACES_API_KEY` |
| `notion` | `NOTION_API_KEY` |
| `openai-whisper-api` | `OPENAI_API_KEY` |
| `sag` | `ELEVENLABS_API_KEY` |
| `discord` | `channels.discord.token` |
| `baidu-search` | `BAIDU_API_KEY` |
| `clawcrm` | `CLAWCRM_API_KEY` |
| `ima-skill` | `IMA_OPENAPI_CLIENTID`, `IMA_OPENAPI_APIKEY` |
| `x-search` | `XAI_API_KEY` |

**需要配置项（config）**：
| Skill | 依赖 |
|-------|------|
| `bluebubbles` | `channels.bluebubbles` |

### 3.2 优先级修复建议

**高价值（值得配置）**：
- `baidu-search` → 国内搜索刚需
- `discord` → 团队协作
- `notion` → 笔记工具
- `x-search` → X平台数据

**中等价值（看需求）**：
- `spotify-player` → 音乐播放
- `openai-whisper-api` → 语音转文字
- `tmux` → 终端管理

**低价值（暂不需要）**：
- `apple-notes`, `apple-reminders`, `bear-notes` → macOS专用
- `obsidian` → Obsidian用户
- `things-mac` → Things用户

---

## 四、Skills调用机制详解

### 4.1 自动触发原理

OpenClaw的Skills系统通过**描述匹配**自动激活：

```
用户消息 → 关键词/短语匹配 → 激活对应Skill → 加载SKILL.md → 执行指导
```

**触发示例**：
- 消息包含"B站" → 激活 `bilibili-all-in-one`
- 消息包含"小红书" → 激活 `xiaohongshu` 系列
- 消息包含"飞书文档" → 激活 `feishu-doc`
- 消息包含"ship/launch/deploy" → 激活 `workflow-ship-faster`

### 4.2 Skill结构标准（Ship Faster标准）

```
skill-name/
├── SKILL.md              # 入口文件（必须）
├── references/           # 详细文档（按需加载）
├── scripts/              # 自动化脚本
├── assets/               # 模板/资源
└── tests/                # 测试
```

**SKILL.md结构**：
```yaml
---
name: skill-name
description: "触发描述，包含关键词和触发词"
metadata:
  stage: tool|workflow|review|service|meta
  tags: [...]
---

# 标题

## 何时激活
## 核心功能
## 使用方法
## 参考文档链接
```

### 4.3 子Agent使用Skills的正确方式

**正确流程**：
1. **识别任务类型** → 判断需要哪个Skill
2. **加载SKILL.md** → 用read工具读取
3. **遵循指导执行** → 按照Skill内的步骤操作
4. **输出到指定位置** → artifact-first原则

**示例：代码侠写代码**
```
1. 任务：写一个新的API
2. 识别：这是开发任务 → api-dev skill
3. 加载：read ~/Desktop/ZhugeDengpao-Team/skills/api-dev/SKILL.md
4. 执行：按照skill指导开发
5. 输出：代码文件 + 文档
```

---

## 五、最佳实践

### 5.1 Self-Improving-Agent的正确使用

**核心机制**：
- 记录学习：错误修正、知识差距、最佳实践
- 自动晋升：将通用学习推到MEMORY.md、SOUL.md、TOOLS.md
- 模式检测：识别重复问题

**正确姿势**：
```
遇到错误 → 立即记录到 .learnings/ERRORS.md
获得纠正 → 记录到 .learnings/LEARNINGS.md
发现更好方法 → 记录到 .learnings/LEARNINGS.md (best_practice)
反复出现的问题 → 晋升到 SOUL.md 或 TOOLS.md
```

### 5.2 Workflow系统的高效使用

**推荐工作流链**：
```
workflow-project-intake  → 需求接入
    ↓
workflow-brainstorm      → 澄清需求
    ↓
workflow-creator         → 创建工作流（如果需要自定义）
    ↓
workflow-ship-faster     → 端到端交付
    ↓
workflow-feature-shipper → 特性迭代
    ↓
review-quality           → 质量审查
    ↓
skill-evolution          → 持续进化
```

**Artifact-first原则**：
- 所有中间产物写入文件
- 步骤间传递路径而非内容
- 可恢复、可审计

### 5.3 Skill创建与组合

**创建新Skill时机**：
- 发现可复用的模式
- 多个工作流有共同步骤
- 特定领域积累深厚经验

**组合Skills时机**：
- 跨平台操作（如：小红书+B站同步发布）
- 复杂业务流程（如：研究→写稿→发布）
- 自动化流水线（如：监控→分析→告警）

---

## 六、小花团队激活方案

### 6.1 优先级分类

#### P0（立即可用，核心需求）

| Skill | 激活方式 | 用途 |
|-------|---------|------|
| `feishu-doc/wiki/drive/notification` | 直接使用 | 飞书文档管理 |
| `xiaohongshu-*` | 配置TikHub API Key | 小红书运营 |
| `bilibili-all-in-one` | 配置B站Cookie | B站运营 |
| `publish-x-article` | 直接使用 | X平台发布 |
| `self-improvement` | 初始化.learnings目录 | 持续改进 |

#### P1（配置后可用，提升效率）

| Skill | 激活方式 | 用途 |
|-------|---------|------|
| `baidu-search` | 申请百度API Key | 搜索增强 |
| `web-search-plus` | 直接使用 | 增强搜索 |
| `deep-research` | 直接使用 | 深度研究 |
| `workflow-ship-faster` | 直接使用 | 快速开发 |
| `review-quality` | 直接使用 | 质量保障 |

#### P2（按需配置）

| Skill | 激活方式 | 用途 |
|-------|---------|------|
| `image-cog`, `minimax-image-gen` | 配置API | 图像生成 |
| `stock-evaluator-v3` | 直接使用 | 股票分析 |
| `github` | 配置Token | GitHub操作 |
| `supabase` | 配置连接 | 数据库 |

### 6.2 子Agent Skills配置

| Agent | 核心Skills | 辅助Skills |
|-------|-----------|-----------|
| **代码侠** | api-dev, nextjs, frontend, playwright | review-quality, cc-godmode |
| **配色师** | frontend-design-ultimate, image-cog | tool-ui-ux-pro-max |
| **文案君** | xiaohongshu-*, bilibili-*, publish-x-article | deep-research, humanizer |
| **洞察者** | deep-research, web-search-plus, find-skills | self-improvement, skill-evolution |
| **产品官** | workflow-*, supabase | review-quality |
| **市场官** | bilibili-all-in-one, xiaohongshu-all-in-one | baidu-search |
| **运营官** | todo-tracker, agent-browser | auto-updater |
| **战略官** | stock-*, hk-ai-stock-expert | deep-research |
| **协调官** | workflow-project-intake | skill-improver |
| **安全官** | tool-openclaw, skill-improver | review-* |

### 6.3 立即行动清单

**小花（主Agent）执行**：
- [ ] 确认飞书4件套（doc/wiki/drive/notification）正常工作
- [ ] 初始化 self-improvement：创建 `.learnings/` 目录
- [ ] 为文案君配置 TikHub API Key（小红书）
- [ ] 为文案君配置 B站 Cookie（bilibili）

**代码侠执行**：
- [ ] 确认 nextjs、api-dev、frontend 可用
- [ ] 跑通 workflow-ship-faster 示例

**洞察者执行**：
- [ ] 确认 deep-research、web-search-plus 可用
- [ ] 建立技能库索引文档

---

## 七、Skills进化路线图

### Phase 1：激活（1-2天）
1. 确认92个可用Skills全部可访问
2. 配置P0优先级Skills的依赖
3. 子Agent完成Skills配置

### Phase 2：优化（3-5天）
1. 运行 skill-improver 分析执行日志
2. 识别高频低效场景
3. 优化Skills调用路径

### Phase 3：扩展（7-14天）
1. 根据业务需求创建定制Skills
2. 组合常见操作为workflow
3. 建立团队Skills最佳实践文档

---

## 八、附录

### A. Skills状态速查

```
✅ 92个可用
⏸ 0个禁用
🚫 0个被阻止
✗ 36个缺依赖
```

### B. 关键Skills快速索引

| 任务 | Skill |
|------|-------|
| 飞书文档读写 | feishu-doc |
| 小红书数据 | xiaohongshu-api |
| B站全套 | bilibili-all-in-one |
| 快速开发 | workflow-ship-faster |
| 质量审查 | review-quality |
| 持续改进 | self-improvement |
| 技能进化 | skill-evolution |
| 深度研究 | deep-research |

### C. 参考资料

- OpenClaw Skills系统：[OpenClaw官方文档]
- ClawHub市场：https://clawhub.com
- Ship Faster标准：workflow-ship-faster/SKILL.md
- Skill创建规范：skill-creator/SKILL.md

---

**报告完成**
洞察者 敬上
