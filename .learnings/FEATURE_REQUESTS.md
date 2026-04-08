# FEATURE_REQUESTS.md - 功能需求

**用途**：记录用户请求的缺失能力、希望新增的工具或工作流

---

## [FEAT-20260408-001] 自动化反馈信号检测

**Logged**: 2026-04-08T07:30:00+08:00  
**Priority**: high  
**Status**: pending  
**Requester**: 小花  
**Category**: automation

### 需求描述

建立一套自动反馈检测机制，替代当前的人工判断"3 次失败触发进化"规则。

### 期望行为

- 自动识别用户反馈信号（正/负）
- 自动记录到 `.learnings/` 对应文件
- 达到阈值时自动触发技能优化流程

### 技术参考

- self-evolve 插件的反馈检测机制
- Q-Learning 奖励门控（minAbsReward=0.15）

### 实现建议

1. 在 OpenClaw hooks 中添加反馈检测脚本
2. 配置关键词匹配规则（否定词/表扬词）
3. 与 `.learnings/` 日志系统集成

---

## [FEAT-20260408-002] 三元组记忆检索

**Logged**: 2026-04-08T07:30:00+08:00  
**Priority**: medium  
**Status**: pending  
**Requester**: 小花  
**Category**: memory

### 需求描述

在 `memory/triplets/` 目录下建立可检索的三元组记忆库，替代纯叙事型日志。

### 期望行为

- 支持按标签检索（#进化研究 #工具使用）
- 支持按意图关键词搜索
- 支持相似度排序（高相关性优先）

### 技术参考

- self-evolve 的 RAG 检索机制（τ=0.85）
- elite-longterm-memory 向量嵌入

### 实现建议

1. 先建立简单的关键词检索脚本
2. 后续评估是否需要引入向量检索
3. 与现有 memory 系统保持兼容

---
