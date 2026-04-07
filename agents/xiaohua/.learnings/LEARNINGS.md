# Learnings

纠正、洞察、知识缺口、最佳实践记录。

**Categories**: correction | insight | knowledge_gap | best_practice

---

## 格式模板

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
One-line description of what was learned

### Details
Full context: what happened, what was wrong, what's correct

### Suggested Action
Specific fix or improvement to make

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-20250110-001 (if related to existing entry)
- Pattern-Key: simplify.dead_code | harden.input_validation (optional)
- Recurrence-Count: 1 (optional)
- First-Seen: 2025-01-15 (optional)
- Last-Seen: 2025-01-15 (optional)

---
```

---

## 晋升规则

| 学习类型 | 晋升目标 | 触发条件 |
|----------|----------|----------|
| 行为模式 | SOUL.md | 跨场景适用的行为准则 |
| 工作流改进 | AGENTS.md | 影响多个任务的流程优化 |
| 工具坑点 | TOOLS.md | 特定工具的使用注意事项 |
| 重复模式 | 系统提示 | 同一问题出现 ≥3 次 |

---

*Last updated: 2026-04-07 | 小花 🦞*
