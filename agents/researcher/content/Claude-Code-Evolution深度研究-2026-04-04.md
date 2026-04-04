# Claude Code Evolution 深度研究报告
**任务：** 深入研究 ra1nzzz/claude-code-evolution
**分析师：** 洞察者
**日期：** 2026-04-04
**来源：** GitHub + ytaiv.com 文章

---

## 一、项目概述

| 项目 | 信息 |
|------|------|
| 仓库 | github.com/ra1nzzz/claude-code-evolution |
| 作者 | @ra1nzzz |
| 许可证 | MIT |
| 分析规模 | 1903文件 / 51.2万行TypeScript |
| 源码 | github.com/ra1nzzz/claude-code-src |
| 发布时间 | 2026-04-03 |

**项目目标：** 对 Claude Code 源码深度分析，将优秀架构设计、提示词工程和技能系统迁移到 OpenClaw 平台。

---

## 二、核心产出（4个增强Skill）

### 2.1 claude-code-simplify（代码审查）

**功能：** 3个并行Agent同时审查代码

**触发词：** `/simplify`, `审查代码`

**工作流：**
```
用户: /simplify
  ├─ Agent 1: 代码复用审查
  ├─ Agent 2: 代码质量审查
  └─ Agent 3: 效率审查
  → 聚合结果
```

**效果：** 代码审查速度提升 3x

---

### 2.2 claude-code-remember（记忆管理）

**功能：** 记忆审查和整理

**触发词：** `/remember`, `整理记忆`

**工作流：**
```
用户: /remember
  → Promotions (3项待晋升)
    1. "使用bun而非npm" → CLAUDE.md
    2. "偏好简洁回复" → CLAUDE.local.md
    3. "API路由使用kebab-case" → CLAUDE.md
  → Cleanup (2项待清理)
    1. 删除重复条目
    2. 更新过期约定
  → 用户审阅并批准
```

**核心设计：** 三层记忆架构

| 层级 | 文件 | 用途 |
|------|------|------|
| 项目级 | CLAUDE.md | 团队约定，所有贡献者共享 |
| 个人级 | CLAUDE.local.md | 个人偏好，仅当前用户 |
| 自动级 | memory/auto-extracted.json | 自动提取的工作记忆 |

---

### 2.3 claude-code-verify（任务验证）

**功能：** 任务完成度验证

**触发词：** `/verify`, `验证任务`

**核心原则：**
> "不是确认它能工作，而是尝试破坏它"

**反 rationalization 规则：**
- "代码看起来正确" ≠ 验证。运行它。
- "实现者测试已通过" ≠ 验证。独立验证。
- "大概没问题" ≠ 验证。运行它。

---

### 2.4 claude-code-debug（调试辅助）

**功能：** 系统化调试

**触发词：** `/debug`, `调试`

**工作流：**
```
Phase 1: 信息收集
  - 检查相关代码文件
  - 查看错误日志
  - 复现问题

Phase 2: 根因分析
  - 发现事件监听器未绑定
  - 定位到初始化顺序问题

Phase 3: 修复验证
  - 应用修复
  - 验证功能正常
  - 运行回归测试
```

---

## 三、分层系统提示词架构

### 3.1 架构概览

```
system-prompt/
├── core/                        # 核心身份（静态缓存）
│   ├── identity.md              # 人格定义
│   ├── safety.md                # 安全规则
│   └── capabilities.md         # 能力边界
├── tools/                       # 工具指导（静态缓存）
│   ├── file-operations.md       # 文件操作指南
│   └── agent-operations.md      # Agent协作指南
├── dynamic/                     # 动态内容（每会话更新）
│   └── session-context.md       # 会话上下文
└── implementations/            # TypeScript实现
    ├── section-cache.ts         # Section缓存
    ├── context-generator.ts    # 上下文生成
    ├── agent-coordinator.ts     # Agent协调器
    └── memory-manager.ts        # 记忆管理器
```

### 3.2 Section缓存API（核心创新）

**为什么重要：** 减少30-50%系统提示词token

```typescript
// 带缓存的section（默认）
systemPromptSection(name: string, compute: () => string)
// → /clear 或 /compact 时清除

// 无缓存的section（每轮重算）
DANGEROUS_uncachedSystemPromptSection(
  name: string,
  compute: (options: DynamicOptions) => string,
  reason: string  // 需要说明为什么打破缓存
)
```

**动态边界分隔符：**
```
[静态内容...]

__SYSTEM_PROMPT_DYNAMIC_BOUNDARY__

[动态内容...每会话更新]
```

---

## 四、Task系统架构

### 4.1 7种任务类型

```typescript
TaskState 联合类型:
├── LocalShellTask      // 本地shell命令
├── LocalAgentTask     // Fork子agent（ProgressTracker）
├── RemoteAgentTask    // 远程agent
├── InProcessTeammateTask
├── DreamTask         // 自动记忆整合（UI可视化）
└── ...
```

### 4.2 ProgressTracker设计

```typescript
interface ProgressTracker {
  latestInputTokens: number      // API累计值，取最新
  cumulativeOutputTokens: number // 每turn求和
  recentActivities: string[]     // 最近N次工具调用
}
```

---

## 五、Agent系统框架

### 5.1 内置Agent（built-in）

| Agent | 功能 |
|-------|------|
| `planAgent` | 只读架构规划，READ-ONLY模式 |
| `exploreAgent` | 快速文件搜索，并行工具调用 |
| `verificationAgent` | 破坏性验证，系统性测试策略 |
| `claudeCodeGuideAgent` | Claude Code/SDK/API文档助手 |

### 5.2 Agent定义格式

JSON/YAML schema，支持：
- tools列表
- disallowedTools
- MCP server内联

---

## 六、权限系统

```typescript
PERMISSION_MODES = ['read', 'write', 'bypass']
// read:   仅读取
// write:  写入前请求确认
// bypass: 完全绕过
```

---

## 七、性能优化数据

| 优化项 | 效果 |
|--------|------|
| Section缓存 | 减少30-50%系统提示词token |
| 并行Agent | 代码审查速度提升3x |
| 动态边界 | 支持跨用户缓存静态内容 |
| 记忆分层 | 减少重复记忆，提升检索效率 |

---

## 八、对小花团队的启示

### 8.1 可立即借鉴

**1. 三层记忆架构**
```
CLAUDE.md      → 团队共享约定（我们的.learnings/）
CLAUDE.local.md → 个人偏好（我们的MEMORY.md）
memory/auto    → 自动工作记忆（待建立）
```

**2. 代码审查并行化**
我们的代码侠可以学习/simplify的3-Agent并行审查模式

**3. 验证Agent的反rationalization原则**
> "不是确认它能工作，而是尝试破坏它"

**4. Section缓存概念**
减少token消耗对我们这种多Agent协作很重要

### 8.2 需要研究的方向

**1. ProgressTracker**
进度追踪设计值得研究，可能用于我们的任务管理系统

**2. Task状态机**
7种任务类型的状态管理是工程级别的设计

### 8.3 不适合我们的

- Vim Mode（我们不是终端工具）
- Voice Mode（当前阶段不需要）

---

## 九、疑问和局限

1. **没有效果数据**：项目声称的优化效果（30-50% token减少、3x速度提升）未经独立验证
2. **star数未知**：GitHub仓库的社区认可度未知
3. **维护状态未知**：项目是否还在活跃维护？
4. **实际采用率**：有多少OpenClaw用户实际安装使用了这个增强包？

---

## 十、结论

**评分：** ⭐⭐⭐⭐（4/5）

**价值：** 
- 架构设计有参考价值（分层提示词、Section缓存）
- 三层记忆体系可以借鉴
- 并行Agent审查模式值得尝试

**局限：**
- 开源项目未经大规模验证
- 核心数据（star、fork数、实际效果）缺失
- 可能只是个人实验项目

**建议行动：**
1. 将三层记忆架构纳入我们的进化机制
2. 研究ProgressTracker设计，用于任务管理
3. 关注项目后续发展（star变化、维护状态）
4. 不要盲目安装使用（先观察社区反馈）

---

*洞察者 · 2026-04-04 · 深度研究完成*
