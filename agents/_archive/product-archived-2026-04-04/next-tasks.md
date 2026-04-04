# 虾医 — 待完成任务
> 由 cron 自动生成，每4小时更新

## 未完成模块

### fix --auto（自动执行修复）
- 文件: src/commands/fix.ts
- 现状: 只有 --dry-run，缺少 --auto 实际执行
- 需要:
  1. 实现 executeFix(taskId) 函数
  2. 执行每个 fixSteps 中的命令
  3. 捕获执行结果
  4. 成功则更新 case 库 successRate
  5. 失败则回滚或报错误
### evolver 自我进化引擎
- 文件: src/core/evolver.ts（不存在）
- 需要:
  1. 读取 diagnose 结果
  2. 提取根因和 fixSteps
  3. 生成/更新 patterns.json
  4. 记录 successRate 变化
  5. 淘汰低成功率 pattern
### learn 命令
- 文件: src/commands/learn.ts（不存在）
- 功能: 从指定 case 学习，生成 pattern
- 需要:
  1. 读取 data/cases/{caseId}.md
  2. 提取 keywords / rootCause / fixSteps
  3. 更新 patterns.json
  4. 输出学习结果
### Case 库扩充
- 现状: 11 个 case
- 目标: 15+ 个真实 case
- 需要: 从老庄 gateway.err.log 提取新案例
