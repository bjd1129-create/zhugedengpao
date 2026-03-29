# OpenClaw X使用技巧深度归纳

> 研究来源：awesome-openclaw-usecases、OpenClaw官方文档（docs.openclaw.ai）、GitHub discussions、社区实战经验
> 研究范围：50+真实使用场景、官方最佳实践、安全指南、社区踩坑总结

---

## 技巧分类

### 1. 记忆系统技巧

**双层记忆架构——短记忆+长记忆**

OpenClaw的记忆本质是**Markdown文件**，不是玄学数据库。核心原则：

- `memory/YYYY-MM-DD.md` — 每日日志（append-only），会话启动时自动读取今天+昨天的内容
- `MEMORY.md` — 精选长记忆， curated后的持久知识
- **"Mental notes don't survive session restarts"** — 所有重要信息必须写文件，不要相信"我会记住"

**自动记忆刷新（Pre-compaction Ping）**

会话接近上下文上限时，OpenClaw会自动触发一个**静默的agentic turn**，提醒模型在上下文压缩前写入持久记忆。配置示例：

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "reserveTokensFloor": 20000,
        "memoryFlush": {
          "enabled": true,
          "softThresholdTokens": 4000,
          "prompt": "Write any lasting notes to memory/YYYY-MM-DD.md; reply with NO_REPLY if nothing to store."
        }
      }
    }
  }
}
```

**如果想让某事被记住——直接让bot写进memory**——不要猜它会不会自动记住。

**向量语义搜索**

OpenClaw支持对`MEMORY.md`和`memory/*.md`建立向量索引，实现语义搜索（即使措辞不同也能找到相关笔记）。支持混合搜索（BM25 + vector）。

---

### 2. 多Agent协作技巧

**STATE.yaml去中心化协调模式**

经典"主会话=纯协调者"模式，避免中央编排瓶颈。适用于复杂项目（多仓库重构、研究冲刺、内容管道）：

```yaml
# STATE.yaml - 项目协调文件
project: website-redesign
updated: 2026-02-10T14:30:00Z
tasks:
  - id: homepage-hero
    status: in_progress
    owner: pm-frontend
  - id: api-auth
    status: done
    owner: pm-backend
next_actions:
  - "pm-content: Resume migration now that api-auth is done"
```

**PM委托模式规则：**
- 主会话：0-2个tool calls（只做spawn/send）
- PM拥有自己的STATE.yaml
- PM可以spawn子子agent做并行子任务
- 所有状态变更git提交

**Sub-agent与主会话隔离**

- 每个sub-agent有独立session（`agent:<agentId>:subagent:<uuid>`）
- sub-agent默认不获取session tools（安全隔离）
- 子agent任务文件分两个角色：
  - `AUTONOMOUS.md` — 只存目标和开放 backlog，**只有主会话写入**
  - `memory/tasks-log.md` — append-only日志，**子agent只追加，从不编辑已有行**

> ⚠️ **踩坑警告**：多agent同时编辑同一文件会导致静默失败——edit工具需要精确oldText匹配，如果中间有其他agent改了行，匹配失败则编辑静默失败。

**thread-bound sessions（线程绑定）**

Discord支持持久线程绑定的sub-agent session：
- `sessions_spawn` with `thread: true`
- 后续线程消息路由到同一个sub-agent session
- `/focus` 手动绑定，`/unfocus` 解绑，`/session idle` 控制超时

**成本技巧：子agent用更便宜的模型**

每个sub-agent有独立上下文和token使用量。重度/重复任务设置更便宜的子模型，主agent保持高质量模型：

```json
{
  "agents": {
    "defaults": {
      "subagents": {
        "model": "anthropic/claude-haiku"  // 比主力模型便宜
      }
    }
  }
}
```

---

### 3. 工作流自动化技巧

**Goal-Driven Autonomous Tasks（目标驱动自主任务）**

最强大的模式之一：一次性灌入所有目标，每天AI自主生成+执行任务：

```
Here are my goals and missions. Remember all of this:
Career:
- Grow my YouTube channel to 100k subscribers
- Launch my SaaS product by Q3
Personal:
- Read 2 books per month
...
Every morning at 8:00 AM, come up with 4-5 tasks that you can complete
on my computer today that bring me closer to my goals.
Then schedule and complete those tasks yourself.
Track all tasks on a Kanban board.
```

**n8n Webhook代理模式（凭证隔离）**

OpenClaw不直接持有API密钥，通过webhook调用n8n工作流：

```
OpenClaw → webhook call → n8n Workflow（持有凭证）→ 外部服务
```

关键优势：
- OpenClaw永不接触凭证
- 所有工作流可在n8n UI中可视化调试
- 锁定工作流后agent无法修改行为
- 确定性任务不消耗LLM token

**Cron Jobs分层调度**

```
每15分钟：检查Kanban板继续任务
每1小时：健康监控、邮件分类
每6小时：知识库录入、自我诊断(openclaw doctor)
每12小时：代码质量审计
```

**多源情报聚合管道**

109+来源（RSS、Twitter KOL、GitHub releases、Web搜索），自动去重+质量评分：

```
RSS(46源) + Twitter KOL(44账号) + GitHub(19仓库) + Brave搜索(4话题)
→ 合并去重 → 质量评分 → Discord/邮件/Telegram投递
```

---

### 4. 安全技巧

**DM政策默认pairing模式**

- 未知发送者收到配对码，bot不处理其消息
- 配对：`openclaw pairing approve <channel> <code>`
- 公开DM需要opt-in：设置`dmPolicy="open"` + `"*"`在allowlist

**安全审计命令**

```bash
openclaw security audit
openclaw security audit --deep
openclaw security audit --fix
```

定期运行，尤其在更改配置或暴露网络接口后。

**沙箱执行**

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main",  // 只沙箱非主会话
        "scope": "session"   // 每个session一个容器
      }
    }
  }
}
```

- `"non-main"`：普通聊天在宿主机，项目/风险操作在沙箱
- **elevated exec始终在宿主机，绕过沙箱**
- 沙箱docker容器默认使用独立网络，非全局bridge

**第三方Skills安全原则**

- 安装前**必须阅读源码**
- 检查VirusTotal报告（ClawHub合作提供）
- 优先使用sandboxed runs处理不可信输入
- 永远不要把API key硬编码在prompt或日志里
- 使用`skills.entries.*.env`注入secrets到host进程（不是沙箱）

**多用户信任边界**

- 推荐：每个用户独立机器/VPS，一个gateway服务该用户
- 共享Slack工作区：任何能发消息的人共享相同tool权限
- adversarial用户隔离：必须分开gateway

---

### 5. 成本优化技巧

**Model Failover自动轮换**

- Auth profile轮转：OAuth优先于API Key（基于usageStats.lastUsed）
- 模型降级：按配置的fallback列表自动切换
- 速率限制/超时触发指数退避：1分钟→5分钟→25分钟→1小时上限

**Compaction配置**

- 上下文快满时自动压缩对话历史为摘要
- 可配置不同模型做压缩（用便宜的本地模型处理summarization）
- 手动触发：`/compact` 或 `/compact 聚焦于决策和开放问题`

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "model": "ollama/llama3.1:8b"  // 专用压缩模型
      }
    }
  }
}
```

**Session维护自动清理**

```bash
openclaw sessions cleanup --dry-run
openclaw sessions cleanup --enforce
```

- 30天 stale条目自动清除
- 超过500条目或10MB自动rotate
- 可选sessions目录磁盘配额

**子agent token优化**

- 重度重复任务：spawn便宜模型子agent
- 确定性任务（发邮件、更新表格）→ n8n webhook模式，不消耗LLM token
- 限制sub-agent运行超时：`runTimeoutSeconds`

---

### 6. 踩坑教训

**1. 多人协作edit工具冲突（静默失败）**

多agent同时编辑同一文件时，edit工具的oldText匹配机制会导致静默失败：
- 解决：文件分职责（主会话写AUTONOMOUS.md，子agent只追加tasks-log.md）
- 永远不要让多个agent edit同一文件的同一区域

**2. 第三方Skills安全风险**

awesome-openclaw-usecases仓库明确警告：
- 大量Skills未经审计
- 可能包含prompt注入、tool poisoning、恶意payload
- **先读源码，再安装**
- 检查VirusTotal报告

**3. OAuth vs API Key轮转问题**

同时有OAuth和API Key时，round-robin可能在两者间切换导致缓存失效。解决：明确用`auth.order`固定profile。

**4. DM政策配置错误**

生产环境如果DM设为`open`且allowlist包含`*`，任何人都能向你的bot发指令+触发tool。必须运行`openclaw doctor`检查。

**5. 生产环境credential暴露**

- 不要把API key放在skill文件、环境变量以外的任何地方
- n8n代理模式是最佳实践：credentials永远在n8n，不在OpenClaw

**6. 沙箱模式理解错误**

- `"non-main"`不是按agent id区分，是按session.mainKey
- group/channel session使用独立key，算作non-main，会被沙箱
- 如果沙箱关闭，elevated tool始终在宿主机

**7. Session持久化位置误解**

- 在远程模式（VPS等），session文件在远程主机
- 本地Mac检查不到远程文件的状态
- 通过Gateway查询：`/status`

---

## 精选场景案例

### 案例1：X/Twitter全自动化

使用TweetClaw插件实现发推、互动、数据提取：

```
openclaw plugins install @xquik/tweetclaw

发推：Post a tweet: "Just shipped a new feature"
抽奖：Pick 3 random winners from retweeters of this tweet, 
     exclude accounts with < 50 followers
提取：Extract all users who liked this tweet and export as CSV
监控：Monitor @elonmusk and notify me whenever he posts
```

### 案例2：Overnight Mini-App Builder

每晚自主构建一个惊喜MVP：
- 早上brain dump所有目标
- AI每天生成4-5个可自动完成的任务
- 自己执行并更新Kanban板
- 每周日晚分析任务日志发现模式

### 案例3：Personal CRM

```
每日6AM cron：扫描邮件+日历提取新联系人，更新CRM数据库
每日7AM：当日会议准备简报（研究外部参会者背景）
Telegram查询："What do I know about [person]?"
```

### 案例4：Self-Healing Home Server

```
每15分钟：健康检查 → 自动重启崩溃的pod
每1小时：Gmail分类、标签待办事项
每6小时：openclaw doctor自检、磁盘/内存监控
每12小时：代码质量审计、安全扫描
```

---

## 对诸葛灯泡的启发

### 可以立即借鉴的模式

1. **STATE.yaml项目管理**：我们团队的任务管理也可以用类似模式，每个任务负责人透明看到阻塞关系

2. **n8n webhook凭证隔离**：外部API调用通过n8n代理，诸葛灯泡的API keys得到保护

3. **自动记忆flush**：确保每次长会话结束前，重要信息被持久化，不依赖"AI会记住"

4. **多层Cron调度**：根据任务性质分配不同频率的检查周期，避免无效轮询

5. **子agent成本分离**：重度研究任务spawn便宜模型子agent，主agent保持高质量响应

### 记忆系统优化建议

根据OpenClaw最佳实践，我们的MEMORY.md应该：
- 严格区分：MEMORY.md（精选长记忆）vs 每日memory/YYYY-MM-DD.md（原始日志）
- 重要信息写入时**明确告知**"写入MEMORY.md"
- 上下文压缩前检查是否有需要持久化的内容

### 安全建议

- 所有外部Skills必须经过源码审查
- 不在prompt中暴露任何credentials
- DM policy检查：`openclaw doctor`定期运行
- 生产环境优先使用sandboxed runs处理高风险操作

### 工作流建议

- **日启动简报**：每天早8点诸葛灯泡生成当日任务列表
- **周末回顾**：每周日分析本周任务完成情况，更新MEMORY.md
- **凭证管理**：所有第三方API通过n8n代理，诸葛灯泡只持有webhook URL
