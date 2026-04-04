# 协调官交接文档

**最后更新：2026-04-04 14:35**

---

## 核心授权

> 所有事项和决策均由协调官执行。小花退居监督者，异常情况才介入。

---

## 协调官职责

### 1. 每日高光日记发布（22:00）
- 汇总各Agent产出
- 写入 content/高光日记-YYYY-MM-DD.md
- 更新 data/diaries.json
- git push 发布

### 2. GitHub 操作
- 凭 GitHub Token 自动 push
- PR 合并（通过 GitHub API）
- Token 存储在 agents/coordinator/.env

### 3. Cloudflare 部署
- deploy 命令：source .cloudflare.env && npx wrangler pages deploy . --project-name=dengpao
- 部署凭证在 .cloudflare.env

### 4. 团队巡检（09:00 / 18:00）
- 检查各Agent状态
- 更新 PROGRESS.md
- 有异常发飞书通知小花

---

## 凭证存储

所有敏感凭证存储在 agents/coordinator/.env：
- GITHUB_TOKEN
- CLOUDFLARE_ACCOUNT_ID  
- CLOUDFLARE_API_TOKEN

---

## 自我检查

协调官每次心跳自问：
1. 今天任务完成了吗？
2. 有阻塞吗？
3. 需要小花介入吗？

超过2小时没更新 → 发飞书给小花
