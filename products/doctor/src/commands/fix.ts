/**
 * fix 命令 — 修复问题
 */
import { Problem } from '../core/researcher.js';
import { fix, printFixSummary } from '../core/fixer.js';
import { ui } from '../ui/output.js';
import { printFixStart, printFixSuccess, onRepeatProblem } from '../core/emotion.js';

export async function fixCommand(taskId: string, isDryRun = true): Promise<void> {
  // 从命令行参数解析 taskId
  // 暂时只支持手动指定问题 ID
  const problemMap: Record<string, Partial<Problem>> = {
    'gateway_health': {
      id: 'gateway_health',
      name: 'Gateway 健康检查失败',
      severity: 'critical',
    },
    'cron_400': {
      id: 'cron_400',
      name: 'Cron 推送失败（HTTP 400）',
      severity: 'critical',
    },
    'session_lock': {
      id: 'session_lock',
      name: 'Session 锁堆积',
      severity: 'medium',
    },
  };

  const problem = problemMap[taskId];
  if (!problem) {
    console.log(ui.error(`未知问题 ID: ${taskId}`));
    console.log(ui.info('支持的 ID：gateway_health, cron_400, session_lock'));
    return;
  }

  const problemName = problem.name || taskId;
  printFixStart(problemName, isDryRun);

  // 检查重复问题
  const repeat = onRepeatProblem(problem.id || taskId);
  if (repeat.text) {
    console.log(repeat.text);
    if (repeat.shouldAlert) {
      console.log(ui.error('⚠️  已触发警报！建议检查根因是否真正修复'));
    }
    console.log();
  }

  const result = await fix(problem as Problem, isDryRun);

  if (!isDryRun) {
    printFixSuccess(problemName, result.duration);
  }

  printFixSummary(result);
}
