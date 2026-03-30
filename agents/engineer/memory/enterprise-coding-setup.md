# 企业级开发 Agent 架构 - 诸葛灯泡团队

> 创建时间：2026-03-30
> 状态：规划中

## 当前能力（已实现）

### 基础工具
- ✅ exec — 运行 Shell 命令
- ✅ read/write/edit — 文件操作
- ✅ browser — 浏览器自动化
- ✅ web_fetch/web_search — 网络访问
- ✅ git — 版本控制

### 已安装 Skills
- `coding/` — 编码风格记忆（~openclaw/company/skills/coding/）
- `git-workflows/` — Git 工作流最佳实践
- `git-essentials/` — Git 核心命令
- `code-assistant/` — 代码助手（使用外部 Claude Code/Codex）
- `review-clean-code/` — 代码质量审查
- `review-quality/` — 综合质量审查
- `frontend/` — 前端开发
- `cypress/` — E2E 测试
- `playwright/` — 浏览器自动化

---

## 第二步：建立开发 Agent 分工

### 方案 A：单一 Agent 多角色（当前）

Engineer Agent 承担所有开发工作。
- 优点：简单，无协调开销
- 缺点：任务串行，能力边界模糊

### 方案 B：多 Agent 协作（推荐）

```
engineer/           # 主开发 Agent
├── coder/          # 子 Agent - 负责写代码
├── tester/         # 子 Agent - 负责测试
└── reviewer/        # 子 Agent - 负责审查
```

通过 `sessions_spawn` 并行执行不同阶段。

### 待老庄决策
1. 采用哪种分工方案？
2. 是否需要单独的 tester/reviewer Agent？
3. Git 护栏怎么配置（branch-only, human approval）？
