#!/bin/bash
# 虾医 PM Cron — 每4小时检查项目状态，持续派任务给 Engineer
# 添加到 crontab: crontab -e
# 0 */4 * * * /Users/bjd/Desktop/ZhugeDengpao-Team/agents/product/scripts/doctor-cron.sh

WORKDIR="/Users/bjd/Desktop/ZhugeDengpao-Team/products/doctor"
AGENT_WORKDIR="/Users/bjd/Desktop/ZhugeDengpao-Team/agents/product"
LOG="$AGENT_WORKDIR/logs/doctor-cron.log"
NEXT_TASKS="$AGENT_WORKDIR/next-tasks.md"

mkdir -p "$(dirname $LOG)"

echo "[$(date '+%Y-%m-%d %H:%M')] === 虾医 Cron 检查 ===" >> $LOG

# 检查各模块状态
CHECK_DONE=$(ls $WORKDIR/src/commands/check.ts 2>/dev/null && echo "yes" || echo "no")
DIAGNOSE_DONE=$(ls $WORKDIR/src/commands/diagnose.ts 2>/dev/null && echo "yes" || echo "no")
FIX_DONE=$(ls $WORKDIR/src/commands/fix.ts 2>/dev/null && echo "yes" || echo "no")
MONITOR_DONE=$(ls $WORKDIR/src/commands/monitor.ts 2>/dev/null && echo "yes" || echo "no")
EVOLVER_DONE=$(ls $WORKDIR/src/core/evolver.ts 2>/dev/null && echo "yes" || echo "no")
FIX_AUTO_DONE=$(grep -l "\-\-auto\|auto.*fix\|executeFix" $WORKDIR/src/commands/fix.ts 2>/dev/null && echo "yes" || echo "no")
LEARN_DONE=$(ls $WORKDIR/src/commands/learn.ts 2>/dev/null && echo "yes" || echo "no")
CASES_COUNT=$(ls $WORKDIR/data/cases/*.md 2>/dev/null | wc -l | tr -d ' ')
TEST_RESULT=$(cd $WORKDIR && npm test 2>&1 | tail -1)
PATTERNS_COUNT=$(grep -c '"id":' $WORKDIR/data/cases/patterns.json 2>/dev/null || echo "0")

echo "模块状态:" >> $LOG
echo "  check: $CHECK_DONE" >> $LOG
echo "  diagnose: $DIAGNOSE_DONE" >> $LOG
echo "  fix: $FIX_DONE" >> $LOG
echo "  fix --auto: $FIX_AUTO_DONE" >> $LOG
echo "  monitor: $MONITOR_DONE" >> $LOG
echo "  evolver: $EVOLVER_DONE" >> $LOG
echo "  learn: $LEARN_DONE" >> $LOG
echo "  case库: $CASES_COUNT 个" >> $LOG
echo "  patterns: $PATTERNS_COUNT 个" >> $LOG
echo "  测试: $TEST_RESULT" >> $LOG

# 分析未完成项
INCOMPLETE=""
[ "$FIX_AUTO_DONE" != "yes" ] && INCOMPLETE="${INCOMPLETE}fix --auto;"
[ "$EVOLVER_DONE" != "yes" ] && INCOMPLETE="${INCOMPLETE}evolver;"
[ "$LEARN_DONE" != "yes" ] && INCOMPLETE="${INCOMPLETE}learn命令;"

if [ -z "$INCOMPLETE" ]; then
  echo "所有已知模块已完成" >> $LOG
  echo "✅ [$(date '+%H:%M')] 虾医所有模块已完成，无需派新任务" >> $LOG
  exit 0
fi

# 写 next-tasks.md
cat > $NEXT_TASKS << 'TASKS_EOF'
# 虾医 — 待完成任务
> 由 cron 自动生成，每4小时更新

## 未完成模块

TASKS_EOF

[ "$FIX_AUTO_DONE" != "yes" ] && cat >> $NEXT_TASKS << 'EOF'
### fix --auto（自动执行修复）
- 文件: src/commands/fix.ts
- 现状: 只有 --dry-run，缺少 --auto 实际执行
- 需要:
  1. 实现 executeFix(taskId) 函数
  2. 执行每个 fixSteps 中的命令
  3. 捕获执行结果
  4. 成功则更新 case 库 successRate
  5. 失败则回滚或报错误
EOF

[ "$EVOLVER_DONE" != "yes" ] && cat >> $NEXT_TASKS << 'EOF'
### evolver 自我进化引擎
- 文件: src/core/evolver.ts（不存在）
- 需要:
  1. 读取 diagnose 结果
  2. 提取根因和 fixSteps
  3. 生成/更新 patterns.json
  4. 记录 successRate 变化
  5. 淘汰低成功率 pattern
EOF

[ "$LEARN_DONE" != "yes" ] && cat >> $NEXT_TASKS << 'EOF'
### learn 命令
- 文件: src/commands/learn.ts（不存在）
- 功能: 从指定 case 学习，生成 pattern
- 需要:
  1. 读取 data/cases/{caseId}.md
  2. 提取 keywords / rootCause / fixSteps
  3. 更新 patterns.json
  4. 输出学习结果
EOF

# 如果 case 库 < 15 个，也标记需要扩充
if [ "$CASES_COUNT" -lt 15 ]; then
cat >> $NEXT_TASKS << EOF
### Case 库扩充
- 现状: $CASES_COUNT 个 case
- 目标: 15+ 个真实 case
- 需要: 从老庄 gateway.err.log 提取新案例
EOF
fi

# 如果 patterns < 8 个，标记需要建立 pattern
if [ "$PATTERNS_COUNT" -lt 8 ]; then
cat >> $NEXT_TASKS << EOF
### Pattern 库建立
- 现状: $PATTERNS_COUNT 个 pattern
- 目标: 8+ 个 pattern
- 需要: 从已有 case 生成 pattern
EOF
fi

echo "" >> $LOG
echo "📋 任务清单已更新: $NEXT_TASKS" >> $LOG
echo "🔔 标记需要完成: $INCOMPLETE" >> $LOG
echo "[$(date '+%Y-%m-%d %H:%M')] === Cron 结束 ===" >> $LOG
echo "---" >> $LOG

echo "✅ Cron 完成，已更新 next-tasks.md"
