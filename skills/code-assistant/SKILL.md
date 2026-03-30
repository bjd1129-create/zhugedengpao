# 代码助手技能

> **技能获取时间:** 2026-03-18 19:32
> **技能来源:** 老庄指示
> **适用场景:** 代码编写、调试、运行脚本

---

## 技能描述

执行代码相关任务的能力，包括代码编写、调试、运行脚本等。

---

## 核心能力

### 1. 复杂代码任务 → 委托Claude Code

**使用场景：** 复杂编程任务、大型项目开发、架构设计

**执行方式：**
```bash
# PTY模式启动（必须！）
exec(command="claude 'your coding task'", pty=true, workdir="/path/to/project")
```

**示例：**
```bash
exec(command="claude 'create a REST API with authentication'", pty=true, workdir="/Users/bjd/projects/myapp")
```

---

### 2. Codex执行代码任务

**使用场景：** 快速代码生成、bug修复、代码优化

**执行方式：**
```bash
exec(command="codex exec 'fix the login bug in auth.py'", pty=true)
```

**示例：**
```bash
exec(command="codex exec 'refactor the database connection pool'", pty=true)
```

---

### 3. 简单文件编辑 → 直接edit

**使用场景：** 小范围代码修改、配置更新

**执行方式：**
```python
edit(file_path="app.py", old_string="old code", new_string="new code")
```

**示例：**
```python
# 修改配置
edit(file_path="config.py", old_string="DEBUG = False", new_string="DEBUG = True")

# 修复bug
edit(file_path="auth.py", old_string="if user = None:", new_string="if user is None:")
```

---

### 4. 运行脚本

**使用场景：** 执行Python/Node脚本、运行测试

**执行方式：**
```bash
# Python脚本
exec(command="python3 script.py")

# Node.js脚本
exec(command="node app.js")

# 运行测试
exec(command="pytest tests/")
```

---

## 决策树

```
代码任务
    │
    ├── 复杂任务（架构、大型功能）
    │   └── Claude Code (pty=true)
    │
    ├── 中等任务（bug修复、重构）
    │   └── Codex (pty=true)
    │
    ├── 简单任务（小修改、配置）
    │   └── 直接 edit
    │
    └── 运行任务（测试、脚本）
        └── 直接 exec
```

---

## 注意事项

### PTY模式必须开启

Claude Code 和 Codex 需要PTY模式才能正常交互：

```bash
# ✅ 正确
exec(command="claude 'task'", pty=true)

# ❌ 错误（可能失败）
exec(command="claude 'task'")
```

### 工作目录

复杂任务应指定工作目录：

```bash
exec(command="claude 'task'", pty=true, workdir="/Users/bjd/projects/myapp")
```

### 简单修改优先直接edit

不要用Claude Code做简单修改：

```python
# ✅ 正确
edit(file_path="config.py", old_string="DEBUG = False", new_string="DEBUG = True")

# ❌ 不推荐（浪费资源）
exec(command="claude 'change DEBUG to True'", pty=true)
```

---

## 常用命令速查

| 任务类型 | 命令 |
|----------|------|
| 复杂开发 | `exec(command="claude 'task'", pty=true)` |
| Bug修复 | `exec(command="codex exec 'fix bug'", pty=true)` |
| 小修改 | `edit(file_path="x", old_string="a", new_string="b")` |
| Python脚本 | `exec(command="python3 script.py")` |
| Node脚本 | `exec(command="node app.js")` |
| 测试 | `exec(command="pytest tests/")` |

---

## 与其他技能协作

| 技能 | 协作场景 |
|------|----------|
| 测试子Agent能力 | 验证代码执行能力 |
| 多AI协作 | 派发代码任务给子Agent |
| 飞书文档同步 | 将代码输出整合到文档 |

---

## 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-18 | 初始版本，记录技能获取 |

---

*技能创建: 2026-03-18 19:32*
*技能来源: 老庄指示*
*维护者: 姜小牙*