# OpenClaw 社区热点研究报告

> 洞察者整理 · 2026-04-06
> 来源：GitHub releases + README + ClawHub 文档
> ⚠️ x.com 热门帖子无法抓取（网络限制）

---

## 一、最新版本动态（2026年4月）

### v2026.4.2 — 2026-04-02

**破坏性变更（Breaking）：**
- **xAI 插件重构**：x_search 配置从 legacy 路径迁移到 `plugins.entries.xai.config.xSearch.*`
- **Firecrawl 插件重构**：web_fetch 配置从 legacy 路径迁移到 `plugins.entries.firecrawl.config.webFetch.*`
- ⚠️ 需要运行 `openclaw doctor --fix` 迁移旧配置

**核心新功能：**
- **Task Flow 恢复**：核心 Task Flow 子系统回归，支持 managed-vs-mirrored 同步模式、持久化流程状态、openclaw flows 检查/恢复原语
- **Task Flow 增强**：managed 子任务生成 + sticky cancel intent，外部 orchestrator 可立即停止调度
- **Android 语音唤醒**：Google Assistant App Actions 元数据，Android 可从助手触发器启动 OpenClaw
- **Exec 默认值**：gateway/node host exec 默认为 YOLO 模式（`security=full` + `ask=off`）
- **Provider Replay Hooks**：provider 自己的 replay hook 表面（transcript policy、replay cleanup、reasoning-mode dispatch）
- **before_agent_reply 钩子**：插件可在 inline actions 后、LLM 调用前短路，生成合成回复或静默
- **Feishu 评论**：新增 Drive 评论事件流、线程上下文解析、文档协作工作流
- **Compaction 增强**：`agents.defaults.compaction.notifyUser` 可选关闭"🧹 Compacting context..."提示

**修复重点：**
- Provider 传输策略集中化（auth、proxy、TLS、header）
- exec loopback 修复：2026.3.31 后本地 exec/node clients 不再报 pairing required 错误
- subagents 修复：sessions_spawn 不再因 loopback scope-upgrade pairing 报 1008 错误
- WhatsApp presence 修复：self-chat 模式下不再丢失推送通知
- Anthropic thinking blocks 清理：不再泄露到用户可见回复

---

### v2026.4.1 — 2026-04-01

**核心新功能：**
- **/tasks 命令**：chat 原生的 session 内后台任务面板
- **SearXNG provider**：新增自托管搜索 provider，支持 configurable host
- **Amazon Bedrock Guardrails**：Bedrock Guardrails 支持
- **macOS Voice Wake**：通过 Voice Wake 选项触发 Talk Mode
- **Feishu 评论增强**（同 4.2）

---

## 二、热门周边项目

### 1. Lobster（workflow shell）
- **Star：1.1k** | Fork：241
- OpenClaw 原生的 typed workflow engine
- 将 skills/tools 组合成可编排的 pipeline
- 支持安全自动化，让 OpenClaw 调用这些工作流

### 2. ACP（Agent Client Protocol）
- **Star：2k** | Fork：181
- 有状态的 ACP sessions 的 headless CLI client
- 用于跨 agent 通信协议

### 3. ClawHub（技能市场）
- **Star：7.5k** | Fork：1.2k
- AI agent skills 的版本化注册表（类 npm）
- 特性：向量搜索、版本化管理、rollback-ready、无门槛发布
- 安装：`npx clawhub@latest install <skill-name>`

### 4. onlycrabs.ai（灵魂注册表）
- SOUL.md 的发布/分享平台
- 与 ClawHub 并行：skills 找 ClawHub，souls 找 onlycrabs

### 5. nix-openclaw
- **Star：629** | Fork：206
- Nix 打包的 OpenClaw

---

## 三、ClawHub 技能生态系统

### 架构特点
- **后端**：Convex（DB + file storage + HTTP actions）+ Convex Auth（GitHub OAuth）
- **搜索**：OpenAI embeddings（text-embedding-3-small）+ Convex 向量搜索
- **发布格式**：SKILL.md + 支持文件
- **元数据声明**：skills 在 frontmatter 声明运行时依赖（env vars、binaries、install specs）

### 技能格式示例
```yaml
---
name: my-skill
description: Does a thing with an API.
metadata:
  openclaw:
    requires:
      env:
        - MY_API_KEY
      bins:
        - curl
    primaryEnv: MY_API_KEY
---
```

### CLI 常用命令
```bash
clawhub login              # 认证
clawhub search ...         # 搜索
clawhub explore            # 浏览
clawhub install <skill>    # 安装
clawhub inspect <skill>   # 查看详情
clawhub skill publish      # 发布
clawhub list              # 已安装列表
clawhub update --all      # 更新全部
```

### Nix 插件支持
ClawHub 支持 Nix package bundles：
```yaml
metadata:
  clawdbot:
    nix:
      plugin: "github:clawdbot/nix-steipete-tools?dir=tools/peekaboo"
      systems: ["aarch64-darwin"]
```

---

## 四、技术趋势分析

### 1. **Plugin 架构集中化**
xAI 和 Firecrawl 的 config 迁移到 plugin-owned 路径是重大信号：OpenClaw 正在将所有 provider 配置从 legacy core 路径统一到插件独立路径。这将减少核心代码耦合，让第三方 provider 更容易接入。

### 2. **Task Flow 成为核心工作流**
Task Flow 从实验性功能升级为第一公民：
- managed/mirrored 双模式
- 持久化流程状态
- 与 cron/automation 深度集成
- 外部 orchestrator 可编程控制

**洞察**：OpenClaw 正在从"聊天 Agent"进化为"自动化工作流引擎"。

### 3. **Provider 传输层统一**
所有 HTTP/stream/websocket 路径的 auth、proxy、TLS、header 策略集中到共享路径。这是为多 provider 并发和可靠性打基础。

### 4. **多平台语音能力加速**
Android Voice Wake + macOS Voice Wake + Talk Mode，持续投资语音交互。

### 5. **Feishu 成为重要渠道**
连续两个版本更新 Feishu 评论功能（Drive comment-event flow、线程上下文解析），说明飞书用户群体在增长。

---

## 五、OpenClaw 核心数据

| 指标 | 数值 |
|------|------|
| GitHub Stars | 349k |
| GitHub Forks | 69.9k |
| 最新稳定版 | v2026.4.2（2026-04-02）|
| 推荐 Node | 24 |
| 最低支持 Node | 22.16+ |
| 支持渠道数 | 25+ |
| Sponsor | OpenAI, GitHub, NVIDIA, Vercel, Blacksmith, Convex |

---

## 六、我的洞察

**OpenClaw 的进化方向：**
1. 从单点工具 → 自动化平台（Task Flow 是证据）
2. 从单渠道 → 全渠道聚合（25+ 渠道是证据）
3. 从聊天 → 语音+视觉（Canvas + Voice Wake 是证据）
4. 从核心绑定 → 插件解耦（config 迁移到 plugin-owned 是证据）

**对团队的含义：**
- 我们正在用的 OpenClaw 是 2026-04-02 最新版，功能最完整
- 飞书是我们目前的主力渠道，OpenClaw 对 Feishu 的投入在加速
- Task Flow 如果用好，可以做很复杂的自动化编排
- ClawHub 技能市场是扩展能力的最佳途径

---

*洞察者 · GitHub + 官网技能市场热点研究 · 2026-04-06*
