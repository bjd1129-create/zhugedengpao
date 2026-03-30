# Git 护栏配置

> 创建时间：2026-03-30

## 当前问题

OpenClaw Agent 有 exec 权限，可以运行任意 git 命令。如果不加限制，Agent 可能：
- 直接 push 到 main/master
- 强制覆盖远程分支
- 删除未合并的分支

## 护栏方案

### 方案 1：Git Hooks（推荐）

在仓库设置 pre-push hook，检查：

```bash
#!/bin/bash
# .git/hooks/pre-push

branch=$(git symbolic-ref --short HEAD)
if [ "$branch" = "main" ] || [ "$branch" = "master" ]; then
    echo "❌ 禁止直接 push 到 main/master!"
    echo "请通过 PR 合并。"
    exit 1
fi
```

### 方案 2：GitHub Branch Protection

在 GitHub 设置：
- main 分支：禁止直接 push
- 需要 PR + review 才能合并
- 至少 1 人 approve

### 方案 3：OpenClaw 工具限制

通过配置 exec 权限白名单，限制只能运行特定 git 命令。

## 推荐配置

**组合方案：GitHub Branch Protection + 本地 Hook**

1. GitHub: main 分支保护（必须 PR）
2. 本地: pre-push hook 提示
3. Agent: 只允许 `git add` / `git commit` / `git push --force-with-lease`（非 main）

## 待实施

1. [ ] 在 zhugedengpao repo 设置 Branch Protection
2. [ ] 创建 pre-push hook
3. [ ] 在 AGENTS.md 添加 git 规范
