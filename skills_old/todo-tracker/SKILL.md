---
name: todo-tracker
description: Persistent TODO scratch pad for tracking tasks across sessions. Use when user says "add to TODO", "what's on the TODO", "mark X done", "show TODO list", "remove from TODO", or asks about pending tasks. Also triggers on heartbeat to remind about stale items.
---

# TODO Tracker

Maintain a persistent TODO.md scratch pad in the workspace.

## File Location

`TODO.md` in workspace root (e.g., `/Users/nuthome/nuri-bot/TODO.md`)

## Commands

### View TODO
When user asks: "what's on the TODO?", "show TODO", "pending tasks?"
```bash
cat TODO.md
```
Then summarize the items by priority.

### Add Item
When user says: "add X to TODO", "TODO: X", "remember to X"
```bash
bash skills/todo-tracker/scripts/todo.sh add "<priority>" "<item>"
```
Priorities: `high`, `medium`, `low` (default: medium)

Examples:
```bash
bash skills/todo-tracker/scripts/todo.sh add high "Ingest low-code docs"
bash skills/todo-tracker/scripts/todo.sh add medium "Set up Zendesk escalation"
bash skills/todo-tracker/scripts/todo.sh add low "Add user memory feature"
```

### Mark Done
When user says: "mark X done", "completed X", "finished X"
```bash
bash skills/todo-tracker/scripts/todo.sh done "<item-pattern>"
```
Matches partial text. Moves item to ✅ Done section with date.

### Remove Item
When user says: "remove X from TODO", "delete X from TODO"
```bash
bash skills/todo-tracker/scripts/todo.sh remove "<item-pattern>"
```

### List by Priority
```bash
bash skills/todo-tracker/scripts/todo.sh list high
bash skills/todo-tracker/scripts/todo.sh list medium
bash skills/todo-tracker/scripts/todo.sh list low
```

## Heartbeat Integration

On heartbeat, check TODO.md:
1. Count high-priority items
2. Check for stale items (added >7 days ago)
3. If items exist, include brief summary in heartbeat response

Example heartbeat check:
```bash
bash skills/todo-tracker/scripts/todo.sh summary
```

## TODO.md Format

```markdown
# TODO - Nuri Scratch Pad

*Last updated: 2026-01-17*

## 🔴 High Priority
- [ ] Item one (added: 2026-01-17)
- [ ] Item two (added: 2026-01-15) ⚠️ STALE

## 🟡 Medium Priority
- [ ] Item three (added: 2026-01-17)

## 🟢 Nice to Have
- [ ] Item four (added: 2026-01-17)

## ✅ Done
- [x] Completed item (done: 2026-01-17)
```

## Response Format

When showing TODO:
```
📋 **TODO List** (3 items)

🔴 **High Priority** (1)
• Ingest low-code docs

🟡 **Medium Priority** (1)  
• Zendesk escalation from Discord

🟢 **Nice to Have** (1)
• User conversation memory

⚠️ 1 item is stale (>7 days old)
```

## 逾期检测（增强）

### 自动检测逻辑

心跳检查时自动检测以下问题：

| 逾期类型 | 定义 | 标记 |
|----------|------|------|
| 高优先级逾期 | high 优先级 >3 天未完成 | 🔴 |
| 中优先级逾期 | medium 优先级 >7 天未完成 | 🟡 |
| 低优先级逾期 | low 优先级 >14 天未完成 | 🟢 |
| 过期未处理 | 添加后超过 30 天无更新 | ⚠️ |

### 逾期提醒格式

```
⚠️ **逾期提醒** (2 items need attention)

🔴 逾期 5 天：Ingest low-code docs (添加于 2026-01-10)
🟡 逾期 2 天：Set up Zendesk escalation (添加于 2026-01-15)

建议：标记完成或重新评估优先级
```

### 清理建议

对于逾期项目，优先：
1. 标记完成（如已完成）
2. 删除（如不再需要）
3. 降低优先级（如暂缓）

### 定期清理 Cron

建议设置每日心跳检查：

```bash
# 心跳时自动执行
bash skills/todo-tracker/scripts/todo.sh stale-check
```

这会输出：
- 逾期项目列表
- 建议清理数量
- 整体健康度评分

## 健康度评分

| 评分 | 状态 | 说明 |
|------|------|------|
| 90-100 | 🟢 优秀 | 任务流转正常，无逾期 |
| 70-89 | 🟡 良好 | 有少量逾期，需关注 |
| 50-69 | 🟠 警告 | 逾期较多，建议清理 |
| <50 | 🔴 危险 | TODO 列表失控，需要全面整理 |
