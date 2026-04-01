# GitHub操作技能

> **技能获取时间:** 2026-03-18 19:41
> **技能来源:** 老庄指示
> **适用场景:** GitHub仓库管理、代码协作、CI/CD管理

---

## 技能描述

通过GitHub MCP实现GitHub仓库的完整操作，包括仓库管理、Issues管理、Pull Requests、代码搜索、Actions状态查看、Release管理等。

---

## 安装方式

```bash
# 安装GitHub MCP
clawhub install github-mcp

# 查看完整使用方法
clawhub docs github-mcp
```

---

## 支持操作

### 1. 仓库管理

| 功能 | 说明 |
|------|------|
| **创建仓库** | 创建新的GitHub仓库 |
| **克隆仓库** | 克隆远程仓库到本地 |
| **推送代码** | 推送本地代码到远程 |
| **拉取更新** | 拉取远程更新到本地 |
| **Fork仓库** | Fork他人仓库 |

---

### 2. Issues管理

| 功能 | 说明 |
|------|------|
| **创建Issue** | 提交新的Issue |
| **评论Issue** | 在Issue下评论 |
| **关闭Issue** | 关闭已解决的Issue |
| **标签管理** | 添加/删除标签 |
| **指派负责人** | 指派Issue负责人 |

---

### 3. Pull Requests

| 功能 | 说明 |
|------|------|
| **创建PR** | 提交Pull Request |
| **审查PR** | 代码审查、批准/请求修改 |
| **合并PR** | 合并Pull Request |
| **评论PR** | 在PR下评论 |
| **关闭PR** | 关闭未合并的PR |

---

### 4. 代码搜索

| 功能 | 说明 |
|------|------|
| **搜索代码** | 在仓库中搜索代码 |
| **搜索文件** | 搜索特定文件 |
| **搜索提交** | 搜索提交记录 |
| **搜索Issue** | 搜索Issue内容 |

---

### 5. Actions状态

| 功能 | 说明 |
|------|------|
| **查看运行状态** | 查看Workflow运行状态 |
| **查看运行日志** | 查看详细执行日志 |
| **触发Workflow** | 手动触发CI/CD |
| **取消运行** | 取消正在运行的任务 |

---

### 6. Release管理

| 功能 | 说明 |
|------|------|
| **创建Release** | 发布新版本 |
| **上传资源** | 上传发布资源 |
| **编辑Release** | 修改发布信息 |
| **删除Release** | 删除发布版本 |

---

## 使用场景

### 场景一：创建新项目

```
用户：在GitHub创建一个新仓库"ai-evo-research"

AI：正在创建仓库...
✅ 仓库已创建
🔗 地址：https://github.com/username/ai-evo-research
📝 默认分支：main
📄 已添加README.md

是否需要克隆到本地？
```

### 场景二：提交Issue

```
用户：在ai-evo-research创建一个Issue：需要研究AutoGPT

AI：正在创建Issue...
✅ Issue已创建
📋 编号：#1
📝 标题：需要研究AutoGPT
🏷️ 标签：research
👤 是否指派负责人？
```

### 场景三：创建PR

```
用户：创建一个PR，合并feature分支到main

AI：正在创建Pull Request...
✅ PR已创建
📋 编号：#5
🔀 feature → main
📝 标题：新增AutoGPT研究报告
🔍 检测到变更：3 files changed

等待审查中...
```

### 场景四：查看Actions状态

```
用户：查看最新Workflow运行状态

AI：正在查询Actions...
📊 【最近运行】
| Workflow | 状态 | 耗时 | 触发者 |
|----------|------|------|--------|
| CI | ✅ 成功 | 2m30s | push |
| Deploy | 🔄 运行中 | 1m | push |
| Test | ❌ 失败 | 5m | push |

是否查看失败日志？
```

---

## 常用命令示例

### 仓库操作

```bash
# 创建仓库
gh repo create ai-evo-research --public

# 克隆仓库
gh repo clone username/ai-evo-research

# 推送代码
git push origin main
```

### Issue操作

```bash
# 创建Issue
gh issue create --title "研究AutoGPT" --body "详细描述..."

# 查看Issue列表
gh issue list

# 关闭Issue
gh issue close 1
```

### PR操作

```bash
# 创建PR
gh pr create --title "新增功能" --body "描述..."

# 查看PR列表
gh pr list

# 合并PR
gh pr merge 5 --squash
```

### Actions操作

```bash
# 查看运行列表
gh run list

# 查看运行详情
gh run view [run-id]

# 查看日志
gh run view [run-id] --log
```

---

## 与其他技能协作

| 技能 | 协作场景 |
|------|----------|
| 代码助手 | 代码提交到GitHub |
| 项目管理 | Issue与任务关联 |
| 多AI协作 | 多人协作开发 |
| 飞书文档 | 同步项目文档 |

---

## 配置要求

### 认证配置

```bash
# 配置GitHub Token
gh auth login

# 或设置环境变量
export GITHUB_TOKEN=xxx
```

### 权限要求

| 权限 | 说明 |
|------|------|
| repo | 仓库读写权限 |
| workflow | Actions操作权限 |
| write:packages | Package发布权限 |

---

## 注意事项

| 注意项 | 说明 |
|--------|------|
| **Token安全** | 不要泄露GitHub Token |
| **分支保护** | 注意保护分支规则 |
| **PR审查** | 重要代码需要审查 |
| **CI状态** | 合并前检查CI状态 |

---

## 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-18 | 初始版本，记录技能获取 |

---

*技能创建: 2026-03-18 19:41*
*技能来源: 老庄指示*
*维护者: 姜小牙*