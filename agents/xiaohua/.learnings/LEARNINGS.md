# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice
**Areas**: frontend | backend | infra | tests | docs | config
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively being worked on |
| `resolved` | Issue fixed or knowledge integrated |
| `wont_fix` | Decided not to address (reason in Resolution) |
| `promoted` | Elevated to CLAUDE.md, AGENTS.md, or copilot-instructions.md |
| `promoted_to_skill` | Extracted as a reusable skill |

## Skill Extraction Fields

When a learning is promoted to a skill, add these fields:

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

---

## [LRN-20260408-001] best_practice

**Logged**: 2026-04-08T08:30:00+08:00
**Priority**: high
**Status**: promoted
**Promoted**: AGENTS.md, MEMORY.md
**Area**: config

### Summary
OpenClaw 自我进化体系研究完成，建立系统化日志记录和晋升机制

### Details
研究了 self-improving-agent skill 和 OpenClaw 官方文档，发现：
1. 三层记忆架构已成熟（.learnings/ → memory/ → MEMORY.md/SOUL.md/AGENTS.md/TOOLS.md）
2. 我们已有基础框架，但缺少系统化执行流程
3. Pattern-Key 追踪机制可有效识别重复问题

### Suggested Action
1. 任务完成后必须记录 learnings
2. 使用 Pattern-Key 追踪重复问题
3. Recurrence-Count >= 3 时晋升到核心文件

### Metadata
- Source: conversation
- Related Files: AGENTS.md, MEMORY.md, agents/洞察者/进化研究 -2026-04-08.md
- Tags: self-improvement, openclaw, workflow
- Pattern-Key: workflow.task-closure

---
