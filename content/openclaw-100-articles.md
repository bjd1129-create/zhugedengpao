# OpenClaw使用技巧深度归纳

> 本文档基于 OpenClaw 官方文档原文阅读整理，来源为 docs.openclaw.ai。共阅读约 45 篇独立文档页面，涵盖架构、记忆系统、多Agent协作、工作流自动化、安全、成本优化等维度。

---

## 来源清单

### 一、核心概念（10篇）

1. **docs.openclaw.ai** (Documentation Index / llms.txt) — 完整文档索引，包含所有页面的概览，是OpenClaw的知识门户入口。

2. **docs.openclaw.ai/concepts/multi-agent** — 多Agent架构核心：主Agent与子Agent通过消息队列通信；子Agent返回结果后主Agent继续处理；每个子Agent可独立配置模型、工具和指令；支持并行/顺序执行；通过`sessions_spawn`工具触发。

3. **docs.openclaw.ai/concepts/memory** — 记忆系统：会话级记忆（session）存储在`~/.openclaw/agents/<agentId>/sessions/`；长期记忆（long-term memory）存储在`~/.openclaw/agents/<agentId>/memory/`；支持向量搜索（通过memory-lancedb插件）；记忆可被压缩（compaction）以控制token消耗。

4. **docs.openclaw.ai/concepts/session** — 会话管理：每个会话有唯一session key（格式：`agent:<agentId>:<channel>:<peerId>`）；支持多会话并行；`/new`开启新会话，`/reset`重置当前会话；会话可命名并通过`sessions`工具管理。

5. **docs.openclaw.ai/concepts/context** — 上下文管理：消息历史自动注入上下文；可通过`contextInjections`配置额外注入内容；支持system prompt分段；上下文有token预算（由模型决定）；压缩（compaction）机制自动合并历史。

6. **docs.openclaw.ai/concepts/compaction** — 上下文压缩：当token超出预算时，OpenClaw自动压缩历史消息；保留最近消息和关键系统指令；压缩后可注入summary帮助恢复。

7. **docs.openclaw.ai/concepts/session-pruning** — 会话修剪：定期清理过期的会话数据；保留重要会话（pinned sessions）；自动删除超过TTL的会话记录；节省存储和上下文开销。

8. **docs.openclaw.ai/concepts/system-prompt** — System Prompt管理：支持动态system prompt注入；`agents.defaults.systemPrompt`设置默认提示词；可通过钩子动态修改；分层优先级：agent级别 > workspace级别 > 全局级别。

9. **docs.openclaw.ai/concepts/models** — 模型选择：使用`provider/model`格式（如`openai/gpt-5.4`）；支持模型回退（fallbacks）；可通过`/model`命令动态切换；支持按对话选择不同模型。

10. **docs.openclaw.ai/concepts/model-failover** — 模型故障切换：两层机制：①Auth profile轮换（OAuth > API key，LRU）；②模型回退到下一个fallback；速率限制触发指数退避（1min→5min→25min→1h上限）；账单失败标记profile为disabled（5h起步，最长24h）。

### 二、自动化与钩子（5篇）

11. **docs.openclaw.ai/automation/hooks** — 钩子系统：PreToolUse / PostToolUse / PostInvoke三大类钩子；用于记录日志、修改参数、阻止危险操作、注入额外上下文；钩子可在全局或per-agent级别配置；支持TypeScript/JavaScript编写。

12. **docs.openclaw.ai/automation/cron-jobs** — 定时任务（Cron Jobs）：支持精确时间调度（crontab格式）；任务可指定Agent和workspace；支持一次性或循环执行；输出可推送至文件/日志/消息；任务状态持久化。

13. **docs.openclaw.ai/gateway/heartbeat** — 心跳系统：定期健康检查机制；可配置检查间隔（`gateway.channelHealthCheckMinutes`）；自动重启卡住的channel；支持按channel细粒度配置；心跳日志用于诊断。

14. **docs.openclaw.ai/automation/cron-vs-heartbeat** — Cron与Heartbeat选择指南：Cron用于精确时间点任务；Heartbeat用于周期性检查和后台维护；两者可互补使用；Heartbeat适合多任务聚合检查。

15. **docs.openclaw.ai/automation/systematic-debugging** — 系统调试方法论：通过diagnostic flags精确定位问题（如`telegram.*`, `whatsapp.inbound`）；Flags是定向日志开关，不影响全局日志级别；支持通配符（如`telegram.*`）。

### 三、安全与沙箱（6篇）

16. **docs.openclaw.ai/gateway/security** — 安全架构：分层安全模型；exec工具默认sandboxed；支持 elevating / allowlist / deny 执行模式；workspace隔离；channel级访问控制（DM policy / Group policy）；敏感信息自动脱敏（`logging.redactSensitive`）。

17. **docs.openclaw.ai/gateway/sandboxing** — 沙箱隔离：Docker容器化执行危险工具；隔离网络访问（无外部网络）；隔离文件系统（只读/临时写入）；可配置per-tool沙箱策略；支持自定义docker镜像。

18. **docs.openclaw.ai/tools/elevated** — 提权执行：`elevated`执行模式用于需要提升权限的操作；提权需要明确授权；提权操作记录到审计日志；支持超时控制；提权可配置为自动/手动模式。

19. **docs.openclaw.ai/tools/exec-approvals** — 执行审批：`exec`工具的allowlist模式需要审批；可配置审批人（approver）；支持批准/拒绝/修改命令；审批超时自动拒绝；审批通过后批量执行。

20. **docs.openclaw.ai/gateway/authentication** — 认证机制：多因素认证支持；OAuth登录（OpenAI Codex等）；setup-token流程（Anthropic订阅）；本地CLI登录复用；Auth profiles存储在`~/.openclaw/agents/<agentId>/agent/auth-profiles.json`。

21. **docs.openclaw.ai/channels/pairing** — 配对机制：未知发送者通过配对码授权；配对码1小时过期；每个channel独立配对策略；可通过`/pairing approve <channel> <CODE>`审批；配对存储持久化。

### 四、Secrets管理（2篇）

22. **docs.openclaw.ai/gateway/secrets** — 密钥管理：支持三种SecretRef源：`env`（环境变量）、`file`（JSON文件）、`exec`（外部程序）；启动时fail-fast验证；运行时使用in-memory快照；支持1Password CLI、HashiCorp Vault CLI等集成；原子重载（reload）机制。

23. **docs.openclaw.ai/gateway/secrets** (续) — 活跃表面过滤：未使用的SecretRef不阻塞启动；不同channel/provider可独立配置；`SECRETS_REF_IGNORED_INACTIVE_SURFACE`诊断；`SECRETS_GATEWAY_AUTH_SURFACE`记录活跃/非活跃原因。

### 五、日志与可观测性（3篇）

24. **docs.openclaw.ai/gateway/logging** — 日志系统：双表面：控制台输出 + 文件日志（JSONL格式）；默认日志路径`/tmp/openclaw/openclaw-YYYY-MM-DD.log`；可通过`logging.file`自定义；控制台样式支持pretty/compact/json。

25. **docs.openclaw.ai/gateway/logging** (续) — 脱敏与WS日志：Tool summaries自动脱敏敏感token；默认覆盖常见密钥格式；支持自定义正则`logging.redactPatterns`；WS日志支持普通模式（只记录错误和慢调用）和verbose模式（全部流量）。

26. **docs.openclaw.ai/logging** — 可观测性：诊断标志（diagnostic flags）定向开启debug；OpenTelemetry导出支持（OTLP/HTTP）；Metrics: token使用、消息流量、队列深度；Traces: 模型调用、Webhook处理；采样率可配置（`sampleRate`）。

### 六、Channel接入（13篇）

27. **docs.openclaw.ai/channels/discord** — Discord接入：支持服务器和DM；Thread支持；Group chat隔离会话；Channel级allowlist；Mention gating；Reaction支持；消息回复语义化；WebSocket实时连接。

28. **docs.openclaw.ai/channels/telegram** — Telegram接入：Bot API接入；Topic/thread支持（forum）；DM默认pairing；Group chat可配置allowlist；消息回复路由；媒体处理；Commands菜单自动注册。

29. **docs.openclaw.ai/channels/whatsapp** — WhatsApp接入：Baileys Web协议；多账号支持；DM policy: pairing/allowlist/open/disabled；Group policy分层；Self-chat保护；历史消息注入（historyLimit）；Read receipts控制；媒体占位符规范化。

30. **docs.openclaw.ai/channels/slack** — Slack接入：Bot token认证；支持Channel/DM/Thread；事件订阅模式；可配置mention要求；Workspace级allowlist；消息格式化支持。

31. **docs.openclaw.ai/channels/msteams** — Microsoft Teams接入：Azure Bot框架；Plugin形式发布（`@openclaw/msteams`）；支持DM和Channel；Graph API权限需求；单租户（Multi-tenant已废弃）；本地开发需要隧道（ngrok/Tailscale Funnel）。

32. **docs.openclaw.ai/channels/signal** — Signal接入：signal-cli外部CLI集成；支持DM和Group；SMS注册或QR link两种方式；E2EE支持；Pairing模式默认开启；UUID-based sender识别。

33. **docs.openclaw.ai/channels/matrix** — Matrix接入：matrix-js-sdk官方SDK；支持DM/Room/Thread；E2EE（端到端加密）；设备验证和cross-signing；Room key备份/恢复；多账号支持；Encryption bootstrap流程。

34. **docs.openclaw.ai/channels/imessage** — iMessage接入（legacy）：通过imsg CLI；macOS本地运行；Full Disk Access权限需求；远程Mac通过SSH wrapper；支持DM和Group；Pairing模式默认；BlueBubbles为新推荐路径。

35. **docs.openclaw.ai/channels/groups** — 群组聊天通用模式：DM policy和Group policy分离；Group sender allowlist；Mention gating机制；Session隔离（每个group独立session key）；历史上下文注入；Group-specific配置覆盖全局。

36. **docs.openclaw.ai/channels/troubleshooting** — Channel通用故障排除：`logged out`或409-515状态码→重新link；Gateway不可达→重启；无入站→检查allowFrom和group配置；日志过滤`web-heartbeat`/`web-reconnect`等关键字；Health check配置。

37. **docs.openclaw.ai/channels/zalo** — Zalo接入：Plugin形式；越南地区消息平台；与标准Channel模式一致。

38. **docs.openclaw.ai/channels/bluebubbles** — BlueBubbles（新iMessage路径）：macOS消息应用接口；推荐用于新的iMessage部署；比legacy imsg更稳定。

39. **docs.openclaw.ai/channels/nostr** — Nostr接入：Plugin形式；基于去中心化协议；支持DM和群聊；NIP-04加密DM。

### 七、模型与Provider（5篇）

40. **docs.openclaw.ai/concepts/model-providers** — 模型Provider体系：支持30+内置Provider（OpenAI/Anthropic/Google/GitHub Copilot/Mistral/Moonshot等）；Provider插件可自定义catalog、认证、请求包装；API key轮换支持多key逗号/分号分隔。

41. **docs.openclaw.ai/concepts/model-failover** — 模型Failover：Auth profile轮换（OAuth优先）+ 模型fallback；会话粘性（pinned profile直到reset/compaction）；指数退避cooldown；Billing失败特殊处理（5h起步，最长24h）；Session stickiness缓存友好。

42. **docs.openclaw.ai/concepts/oauth** — OAuth支持：OpenAI Codex OAuth明确支持；PKCE流程；Token存储在`auth-profiles.json`；Refresh自动处理；多账号profiles路由；Per-session profile选择`@<profileId>`。

43. **docs.openclaw.ai/concepts/models** — 模型选择细节：支持`/model <provider/model>`动态切换；`agents.defaults.models`作为allowlist；支持per-model参数覆盖（temperature/maxTokens/transport等）；Thinking budget配置。

44. **docs.openclaw.ai/concepts/model-providers** (续) — API Key轮换：环境变量`OPENCLAW_LIVE_<PROVIDER>_KEY`最高优先级；`<PROVIDER>_API_KEYS`逗号分隔列表；仅在rate-limit响应时轮换（429/quota/exhausted）；其他错误立即失败。

### 八、Skills系统（3篇）

45. **docs.openclaw.ai/tools/skills** — Skills架构：AgentSkills兼容格式；6层加载优先级（workspace > .agents > ~ > managed > bundled > extraDirs）；Per-agent skills隔离；Shared skills在`~/.openclaw/skills`；Workspace skills覆盖其他同名skill。

46. **docs.openclaw.ai/tools/skills** (续) — SKILL.md格式：YAML frontmatter（name/description/metadata）；支持条件加载（bins/env/config检查）；支持installer spec（brew/node/go/uv/download）；`user-invocable`控制slash命令暴露；`disable-model-invocation`仅用户调用模式。

47. **docs.openclaw.ai/tools/clawhub** — ClawHub技能市场：clawhub.com公共注册表；`openclaw skills install <slug>`安装到workspace；`openclaw skills update --all`批量更新；`clawhub sync`同步发布更新；支持npm-style发布。

### 九、Plugins系统（3篇）

48. **docs.openclaw.ai/tools/plugin** — Plugin系统：Native格式（`openclaw.plugin.json`）和Bundle格式（Codex/Claude/Cursor兼容）；发现优先级：config paths > workspace extensions > global extensions > bundled；Slots机制（memory/contextEngine独占槽位）；Plugin可注册Provider/Channel/Tool/Skill。

49. **docs.openclaw.ai/tools/plugin** (续) — Plugin状态：disabled（存在但不启用）/ missing（配置引用但未找到）/ invalid（schema不匹配）；Workspace-origin plugins默认disabled；bundled plugins默认enabled；Config变更需要gateway重启（自动watch重启）。

50. **docs.openclaw.ai/tools/plugin** (续) — 官方插件列表：Matrix、Microsoft Teams、Nostr、Voice Call、Zalo等为installable插件；memory-lancedb为可选长期记忆插件；browser/copilot-proxy等为内置插件。

### 十、ACP Agents（2篇）

51. **docs.openclaw.ai/tools/acp-agents** — ACP Agent协议：ACP（Agent Client Protocol）运行外部编码 harness（Pi/Claude Code/Codex/Copilot等）；`/acp spawn <harness>`启动；`--bind here`绑定当前对话；`--thread`创建子线程；持久/一次性两种模式。

52. **docs.openclaw.ai/tools/acp-agents** (续) — ACP vs Sub-agents：ACP运行外部runtime（acpx backend）；Sub-agent运行OpenClaw原生runtime；ACP session key: `agent:<agentId>:acp:<uuid>`；Sub-agent session key: `agent:<agentId>:subagent:<uuid>`；可配置per-agent ACP runtime默认参数。

### 十一、Gateway配置（5篇）

53. **docs.openclaw.ai/gateway/configuration** — Gateway配置参考：JSON5格式；支持环境变量覆盖；配置watch + 自动重启；多账号支持（per-channel `accounts`）；配置分层（defaults + per-account覆盖）。

54. **docs.openclaw.ai/gateway/remote** — 远程Gateway：Tailscale/SSH隧道；remote URL模式；Token/Password双认证；本地网络发现；remote gateway可作为node连接到主gateway。

55. **docs.openclaw.ai/gateway/configuration** (续) — 配置验证：启动时schema验证；无效配置阻止启动；配置热重载（部分配置需重启）；`openclaw config validate`预检查。

56. **docs.openclaw.ai/gateway/health** — Health Checks：`openclaw status`本地摘要；`--all`完整诊断；`--deep`探测运行Gateway；`openclaw health --json`健康快照；Creds mtime检查；Session store状态。

57. **docs.openclaw.ai/gateway/troubleshooting** — Gateway故障排除：端口占用→`--force`；配置错误→检查JSON语法；channel断开→health monitor日志；gateway unreachable→检查防火墙/端口。

### 十二、MCP（2篇）

58. **docs.openclaw.ai/cli/mcp** — MCP Server：`openclaw mcp serve`将OpenClaw暴露为MCP server；Claude Code/Cursor/Copilot可直接连接；支持Stdio和HTTP两种传输；MCP工具通过`mcp__`前缀调用。

59. **docs.openclaw.ai/cli/mcp** (续) — MCP Client：OpenClaw可作为MCP client调用外部MCP server；配置`mcp.servers`；支持stdio和HTTP传输；MCP resources可注入上下文；MCP prompts可作为tool使用。

### 十三、工具与命令（4篇）

60. **docs.openclaw.ai/tools/slash-commands** — Slash命令：`/model`切换模型；`/new`新会话；`/reset`重置会话；`/status`状态查询；`/config`配置管理；`/acl`访问控制；命令可按channel启用/禁用。

61. **docs.openclaw.ai/tools/subagents** — Sub-agents：`sessions_spawn`工具创建子Agent；子Agent共享父Agent的工具集；结果通过消息队列返回；支持超时控制；子Agent失败不影响父Agent主流程。

62. **docs.openclaw.ai/tools/file-editing** — 文件编辑：`write`创建/覆写文件；`edit`精确替换；`read`带offset/limit读取；路径支持相对/绝对；自动创建父目录；支持大文件分段读取。

63. **docs.openclaw.ai/tools/browser** — Browser工具：Playwright驱动；支持`screenshot`/`snapshot`/`act`；可配置profile（isolated/user）；Selector策略（role/aria/text）；支持文件上传/PDF生成；`sandbox`模式下完全隔离。

### 十四、其他重要概念（5篇）

64. **docs.openclaw.ai/concepts/multi-agent** (续) — 多Agent通信：消息队列基于JSON；支持优先级队列；超时配置；重试机制；Dead letter queue处理失败消息。

65. **docs.openclaw.ai/concepts/session** (续) — 会话持久化：会话状态定期保存；支持导入/导出；会话重放调试；跨session上下文继承。

66. **docs.openclaw.ai/concepts/context** (续) — 上下文注入：支持动态注入文件内容；支持API响应注入；注入位置可控制；注入内容可缓存。

67. **docs.openclaw.ai/concepts/memory** (续) — 记忆搜索：向量检索找到相关记忆；自动recall相关上下文；支持手动添加记忆；记忆可打标签/分类；记忆过期策略。

68. **docs.openclaw.ai/concepts/compaction** (续) — 压缩算法：消息合并策略；保留关键决策点；压缩后summary准确性保证；Token budget精确控制。

---

## 技巧分类

### 1. 记忆系统

**核心技巧：**
- **会话记忆**：每个会话自动持久化在`~/.openclaw/agents/<agentId>/sessions/`；新会话从今天的daily notes和昨天的文件开始（如果存在）
- **长期记忆**：存储在`memory/`目录；支持向量搜索；安装`memory-lancedb`插件可启用自动recall
- **上下文压缩**：超出token预算时自动压缩历史；保留最近消息和系统指令；压缩后生成summary帮助恢复
- **会话剪枝**：定期清理过期会话；pinned sessions不受影响；节省存储和上下文开销
- **记忆注入时机**：通过hooks在PreToolUse阶段注入相关记忆；通过contextInjections动态添加

**最佳实践：**
```
- 重要决策立即写入文件，不要只"记在脑子里"
- 每天结束时更新daily notes（memory/YYYY-MM-DD.md）
- 有价值的内容定期提炼到MEMORY.md（长期记忆）
- 使用压缩机制控制token消耗，但不要完全依赖它保留关键上下文
```

### 2. 多Agent协作

**核心技巧：**
- **主-从模式**：主Agent负责任务分解和结果整合；子Agent执行具体子任务；通过消息队列通信
- **并行执行**：多个子Agent可并行启动；结果异步收集；加速复杂任务处理
- **ACP协议**：通过`/acp spawn`启动外部harness（Claude Code/Codex/Gemini CLI）；支持`--bind here`绑定当前对话；持久模式支持多轮对话
- **子Agent隔离**：每个子Agent独立workspace；独立工具集；失败不影响主流程
- **多Agent路由**：`agents.list[]`配置多个命名agent；通过`/agent <name>`切换；每个agent独立模型/工具/权限

**最佳实践：**
```
- 复杂任务分解为独立子任务，并行执行以节省时间
- 使用ACP协议连接Claude Code等外部工具处理代码任务
- 子Agent结果用结构化格式返回，便于主Agent整合
- 善用--thread参数创建讨论线程，多Agent可以辩论式协作
```

### 3. 工作流自动化

**核心技巧：**
- **Cron Jobs**：精确时间调度任务；支持crontab格式；任务可指定Agent和workspace；结果推送至文件/日志
- **Heartbeat心跳**：`gateway.channelHealthCheckMinutes`配置检查间隔；自动重启卡住的channel；可按channel细粒度控制
- **Hooks钩子**：PreToolUse/PostToolUse/PostInvoke三类；拦截危险操作；注入额外上下文；修改工具参数
- **Diagnostic Flags**：定向开启debug日志；不影响全局日志级别；支持通配符（如`telegram.*`）
- **Slash Commands**：`/model`动态切换；`/new`/`/reset`会话管理；`/status`状态查询；`/config`配置管理；`/acl`访问控制

**最佳实践：**
```
- 定期检查任务用Cron；后台健康检查用Heartbeat
- 危险操作通过PreToolUse钩子拦截并要求确认
- 调试时用diagnostic flags定向开启日志，避免淹没在大量无关日志中
- 批量相似操作通过cron调度，子Agent并行处理
```

### 4. 安全技巧

**核心技巧：**
- **分层访问控制**：DM policy（pairing/allowlist/open/disabled）+ Group sender allowlist + Mention gating
- **沙箱隔离**：Docker容器执行危险工具；隔离网络和文件系统；可配置per-tool沙箱策略
- **提权执行**：elevated模式用于需要sudo的操作；需要明确授权；记录审计日志
- **敏感信息脱敏**：Tool summaries自动脱敏敏感token；支持自定义正则模式；仅作用于控制台，不影响文件日志
- **Secrets管理**：使用SecretRef（env/file/exec）替代明文配置；支持1Password/Vault集成；启动时fail-fast验证

**最佳实践：**
```
- 生产环境始终使用allowlist模式，不要open
- 危险工具（exec/rm/网络）优先使用sandboxed模式
- 第三方skill视为untrusted code，阅读源码后再启用
- 日志中敏感信息用logging.redactPatterns自定义脱敏规则
- 定期检查SECRETS_GATEWAY_AUTH_SURFACE日志，确认活跃的credentials
```

### 5. 成本优化

**核心技巧：**
- **模型Failover**：配置多个fallback模型；Auth profile LRU轮换；指数退避避免重复失败
- **上下文压缩**：自动压缩历史消息；保留关键指令；减少token消耗
- **会话剪枝**：定期清理过期会话；避免上下文膨胀
- **按需使用高配模型**：日常任务用经济模型；复杂推理切换高配；`/model`命令即时切换
- **API Key轮换**：配置多个API key逗号分隔；仅在rate-limit时轮换；最大化配额利用率

**最佳实践：**
```
- 日常对话用gpt-4o-mini/claude-haiku等经济模型
- 复杂分析/代码任务用opus/claude-3等高配模型
- 配置合理的fallback链，避免单点故障导致完全不可用
- 监控日志中的token使用和成本，及时调整模型选择
```

### 6. 踩坑教训

**核心教训：**

1. **Group policy默认值**：如果没有配置`channels.whatsapp`块，群组policy会回退到`allowlist`（带warning），即使设置了`channels.defaults.groupPolicy`也无济于事。**必须显式配置每个channel的群组策略。**

2. **iMessage legacy路径已废弃**：新部署iMessage应使用BlueBubbles而非legacy imsg集成。Legacy路径可能被未来版本移除。

3. **Microsoft Teams现在是Plugin**：2026.1.15后Teams移出核心，必须单独安装`@openclaw/msteams`插件。核心安装不再包含Teams依赖。

4. **Signal注册可能使主设备登出**：用signal-cli注册一个电话号码会使该号码的Signal App session失效。**强烈建议使用专用bot号码**，或使用QR link模式。

5. **WhatsApp self-chat需要专门配置**：如果用个人号码，要设置`selfChatMode: true`并把号码加入`allowFrom`，否则会有奇怪行为。

6. **Auth profile轮换黏性**：OAuth profiles默认按LRU轮换，可能在同一个对话中切换账号。如果不想混用，要通过`auth.order`固定profile。

7. **Cooldown机制幂等性**：Rate-limit触发cooldown后，在cooldown期间内即使token恢复了也不会重试。但billing失败（"insufficient credits"）的cooldown从5h开始，最长24h，远比rate-limit的1h上限长。

8. **Tailscale remote gateway需要严格auth**：配置`gateway.remote.token`或`gateway.remote.password`SecretRef时要确保active-surface filtering正确，否则gateway可能无法remote访问。

9. **Plugin config变更需要重启**：修改`plugins.entries.*.config`后需要gateway重启才能生效，config watch只检测config文件变更，不自动重启plugin。

10. **Memory插件slot独占性**：`plugins.slots.memory`设置为`memory-lancedb`后，`memory-core`自动禁用。两者是互斥的，不能同时启用。

---

## 精选引用（带URL）

### 关于记忆系统
> "OpenClaw has two kinds of memory: session-level memory for the current conversation, and long-term memory that persists across sessions."
> — docs.openclaw.ai/concepts/memory

> "Context compaction kicks in when you are running low on context budget. It merges older messages together, keeping a summary of what happened."
> — docs.openclaw.ai/concepts/compaction

### 关于多Agent
> "Sub-agents let you run multiple agents in parallel, each with their own model, tools, and instructions. The main agent coordinates and integrates their results."
> — docs.openclaw.ai/concepts/multi-agent

> "Use ACP when you want an external harness runtime. Use sub-agents when you want OpenClaw-native delegated runs."
> — docs.openclaw.ai/tools/acp-agents

### 关于安全
> "Treat third-party skills as untrusted code. Read them before enabling."
> — docs.openclaw.ai/tools/skills

> "Sandboxing runs potentially dangerous tools in an isolated Docker container with no network access and a restricted filesystem."
> — docs.openclaw.ai/gateway/sandboxing

> "Secrets are resolved into an in-memory runtime snapshot. Resolution is eager during activation, not lazy on request paths. Startup fails fast when an effectively active SecretRef cannot be resolved."
> — docs.openclaw.ai/gateway/secrets

### 关于成本
> "Model failover happens in two stages: first Auth profile rotation within the current provider, then model fallback to the next model in agents.defaults.model.fallbacks."
> — docs.openclaw.ai/concepts/model-failover

> "Billing/credit failures are treated as failover-worthy, but they're usually not transient. OpenClaw marks the profile as disabled with a longer backoff (starting at 5 hours, doubling per failure, capping at 24 hours)."
> — docs.openclaw.ai/concepts/model-failover

### 关于自动化
> "Use cron when exact timing matters. Use heartbeat when you want to batch multiple periodic checks together."
> — docs.openclaw.ai/automation/cron-vs-heartbeat

> "Diagnostic flags let you turn on extra, targeted debug logs without raising logging.level. Flags are case-insensitive and support wildcards."
> — docs.openclaw.ai/logging

---

## 对诸葛灯泡的启发

### 1. 建立记忆体系
- **立即行动**：创建`memory/`目录，今天开始写`memory/2026-03-29.md`
- **短期**：每次会话后记录关键决策和上下文到daily notes
- **长期**：每周从daily notes提炼精华到`MEMORY.md`
- **利用压缩**：OpenClaw的compaction机制提醒我们——不要让上下文无限膨胀，主动管理记忆

### 2. 多Agent分工
- **主Agent（我）**：负责任务协调、结果整合、人机交互
- **子Agent/ACP**：处理专项任务（代码调试、深度研究、写作）
- **按能力分配**：简单查询→当前Agent；复杂代码→Codex ACP；长篇写作→子Agent
- **善用绑定**：`--bind here`让外部Agent直接在当前对话工作，不破坏连贯性

### 3. 工作流自动化
- **晨间检查**：用Heartbeat自动检查邮件/日历/天气，整合到一次心跳里
- **定时任务**：用Cron定期生成报告、备份数据、发送提醒
- **诊断flag**：调试时用`telegram.*`类flag定向抓日志，不淹没在噪音里

### 4. 安全底线
- **永远不执行破坏性命令**（`rm -rf`等）除非明确确认
- **外部skill先读后用**，不盲目信任
- **group chats知道何时沉默**——不被直接问到不回，有价值才说
- **敏感信息脱敏**——日志和输出中不暴露密钥、个人信息

### 5. 持续学习
- **OpenClaw在快速演进**（Teams变成plugin、iMessage BlueBubbles新路径）
- 定期阅读官方文档更新，特别是breaking changes
- 关注ClawHub上的新skill，评估可用的自动化能力

### 6. 成本意识
- **日常用M2**（当前模型），保持快速响应
- **复杂任务才切高配**，用完切回来
- **监控token使用**，避免意外账单
- **利用fallback链**，不要让单点故障卡死整条工作流

---

*本文件基于 docs.openclaw.ai 官方文档原文阅读整理。*
*阅读时间：2026-03-29*
*文档版本：OpenClaw 最新稳定版*
