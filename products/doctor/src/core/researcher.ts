/**
 * 研究问题引擎 — 分析错误日志，找根因
 */
import { readErrorLog, categorizeErrors, LogEntry } from '../openclaw/logs.js';
import { checkHealth } from '../openclaw/health.js';
import { checkCronStatus } from '../openclaw/cron.js';
import { ui } from '../ui/output.js';

export interface Problem {
  id: string;
  severity: 'critical' | 'medium' | 'low';
  name: string;
  description: string;
  count: number;
  firstOccurrence: string;
  lastOccurrence: string;
  possibleCauses: string[];
  suggestedFix: string[];
}

export interface DiagnoseResult {
  problems: Problem[];
  totalErrors: number;
  scanDuration: number; // 秒
}

/**
 * 研究问题入口
 */
export async function research(hoursAgo = 2): Promise<DiagnoseResult> {
  const startTime = Date.now();

  // 1. 健康检查
  const health = await checkHealth();

  // 2. Cron 状态
  const cron = await checkCronStatus();

  // 3. 读取错误日志
  const entries = await readErrorLog(hoursAgo);
  const categories = categorizeErrors(entries);

  // 4. 分析问题
  const problems: Problem[] = [];

  // Gateway 问题
  if (health.issues.length > 0) {
    problems.push({
      id: 'gateway_health',
      severity: 'critical',
      name: 'Gateway 健康检查失败',
      description: health.issues.join('；'),
      count: health.issues.length,
      firstOccurrence: '当前',
      lastOccurrence: '当前',
      possibleCauses: [
        '进程启动后卡死',
        '端口被占用',
        '配置文件损坏',
      ],
      suggestedFix: [
        'openclaw gateway restart',
        '检查端口占用：lsof -i :18790',
        '检查日志：tail -f ~/.openclaw/logs/gateway.err.log',
      ],
    });
  }

  // Cron 400 错误
  const cron400Entries = categories.get('cron_400') || [];
  if (cron400Entries.length > 0) {
    problems.push({
      id: 'cron_400',
      severity: 'critical',
      name: 'Cron 推送失败（HTTP 400）',
      description: `共 ${cron400Entries.length} 次 400 错误`,
      count: cron400Entries.length,
      firstOccurrence: cron400Entries[0].timestamp,
      lastOccurrence: cron400Entries[cron400Entries.length - 1].timestamp,
      possibleCauses: [
        '飞书 webhook 推送频率超限（429/400）',
        '飞书应用权限不足',
        'webhook URL 配置错误',
      ],
      suggestedFix: [
        '降低 cron deliveryInterval（5min → 15min）',
        '将 delivery 模式从 webhook 改为 poll',
        '检查飞书应用权限配置',
      ],
    });
  }

  // Session 锁问题
  const sessionLockEntries = categories.get('session_lock') || [];
  if (sessionLockEntries.length > 0) {
    problems.push({
      id: 'session_lock',
      severity: 'medium',
      name: 'Session 锁堆积',
      description: `共 ${sessionLockEntries.length} 次 session 锁异常`,
      count: sessionLockEntries.length,
      firstOccurrence: sessionLockEntries[0].timestamp,
      lastOccurrence: sessionLockEntries[sessionLockEntries.length - 1].timestamp,
      possibleCauses: [
        'subagent 异常退出，锁未清理',
        '会话超时未释放',
      ],
      suggestedFix: [
        '清理孤立 session 锁文件',
        '检查 subagent 任务是否正常结束',
      ],
    });
  }

  // Delivery 失败
  const deliveryEntries = categories.get('delivery_failed') || [];
  if (deliveryEntries.length > 0 && !categories.has('cron_400')) {
    problems.push({
      id: 'delivery_failed',
      severity: 'medium',
      name: 'Cron delivery 失败',
      description: `共 ${deliveryEntries.length} 次 delivery 失败`,
      count: deliveryEntries.length,
      firstOccurrence: deliveryEntries[0].timestamp,
      lastOccurrence: deliveryEntries[deliveryEntries.length - 1].timestamp,
      possibleCauses: [
        '网络问题导致推送失败',
        '目标服务不可达',
      ],
      suggestedFix: [
        '检查网络连接',
        '降低推送频率',
      ],
    });
  }

  const scanDuration = (Date.now() - startTime) / 1000;

  return {
    problems,
    totalErrors: entries.filter(e => e.level === 'ERROR').length,
    scanDuration,
  };
}

/**
 * 打印诊断报告
 */
export function printDiagnoseReport(result: DiagnoseResult) {
  console.log();
  console.log(ui.divider());
  console.log();

  if (result.problems.length === 0) {
    console.log(ui.ok('未发现问题，系统运行正常'));
    console.log();
    console.log(ui.divider());
    console.log();
    console.log(`⏱️  耗时：${result.scanDuration.toFixed(1)}秒`);
    return;
  }

  console.log(ui.error(`发现 ${result.problems.length} 个问题：`));
  console.log();

  result.problems.forEach((problem, index) => {
    const severityIcon = problem.severity === 'critical' ? ui.severity.critical() :
                          problem.severity === 'medium' ? ui.severity.medium() :
                          ui.severity.low();

    console.log(`[${index + 1}/${result.problems.length}] ${severityIcon} ${ui.title(problem.name)}`);
    console.log(`   频率：${problem.count}次（${problem.firstOccurrence} - ${problem.lastOccurrence}）`);
    console.log(`   描述：${problem.description}`);
    console.log();

    if (problem.possibleCauses.length > 0) {
      console.log(`   ${ui.warn('可能原因：')}`);
      problem.possibleCauses.forEach(cause => {
        console.log(`     - ${cause}`);
      });
      console.log();
    }

    if (problem.suggestedFix.length > 0) {
      console.log(`   ${ui.info('修复建议：')}`);
      problem.suggestedFix.forEach(fix => {
        console.log(`     - ${fix}`);
      });
      console.log();
    }
  });

  console.log(ui.divider());
  console.log();
  console.log(`⏱️  耗时：${result.scanDuration.toFixed(1)}秒`);
  console.log();
}
