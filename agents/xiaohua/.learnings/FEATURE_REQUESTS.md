# Feature Requests

用户提出的新能力需求记录。

---

## 格式模板

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Requested Capability
What the user wanted to do

### User Context
Why they needed it, what problem they're solving

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this could be built, what it might extend

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_feature_name

---
```

---

---

## [FEAT-20260407-001] OpenClaw-RL 训练框架评估

**Logged**: 2026-04-07T13:15:00Z
**Priority**: medium
**Status**: pending
**Area**: infra

### Requested Capability
用自然对话反馈对 Agent 进行强化学习训练，特别是交易员/风控官的决策质量优化

### User Context
OpenClaw-RL（GitHub: Gen-Verse/OpenClaw-RL）发布于 2026-02-26，支持 Binary RL(GRPO) + OPD(On-Policy Distillation)。其中 OPD 方法无需 GPU，可通过 LoRA 在云端训练。2026-04-04 新增群体反馈优化能力。这对交易 Agent 的持续进化有潜在价值。

### Complexity Estimate
complex

### Suggested Implementation
1. 评估 Tinker 云端 LoRA 训练方案（无需本地 GPU）
2. 为交易员 Agent 设计反馈机制（决策 → 结果 → reward signal）
3. 测试 OPD 方法在交易场景的可行性

### Metadata
- Frequency: first_time
- Related Features: self-evolve, self-improving-agent

---

*Last updated: 2026-04-07 | 小花 🦞*
