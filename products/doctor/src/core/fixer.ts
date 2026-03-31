/**
 * 修复执行引擎 — 生成并执行修复步骤
 */
import { execSync } from 'child_process';
import { exec } from 'child_process';
import { Problem } from './researcher.js';
import { ui } from '../ui/output.js';
import { checkCronStatus } from '../openclaw/cron.js';

export interface FixStep {
  step: number;
  total: number;
  description: string;
  command?: string;
  dryRunResult?: string;
  executed?: boolean;
  success?: boolean;
}

export interface FixResult {
  taskName: string;
  steps: FixStep[];
  totalSteps: number;
  dryRun: boolean;
  duration: number; // 秒
}

/**
 * 执行命令（异步，避免卡死）
 */
function execAsync(command: string, timeout = 30000): Promise<{ success: boolean; output: string }> {
  return new Promise((resolve) => {
    exec(command, { encoding: 'utf-8', timeout }, (error, stdout, stderr) => {
      if (error) {
        resolve({ success: false, output: error.message });
      } else {
        resolve({ success: true, output: stdout + stderr });
      }
    });
  });
}

/**
 * 为问题生成修复步骤
 */
async function generateFixSteps(problem: Problem, isDryRun: boolean): Promise<FixStep[]> {
  const steps: FixStep[] = [];

  switch (problem.id) {
    case 'gateway_health':
      steps.push({
        step: 1,
        total: 3,
        description: '停止当前 Gateway 进程',
        command: 'launchctl bootout gui/`id -u`/ai.openclaw.gateway 2>/dev/null || true',
      });
      steps.push({
        step: 2,
        total: 3,
        description: '重新启动 Gateway 服务',
        command: 'launchctl bootstrap gui/`id -u` ~/Library/LaunchAgents/ai.openclaw.gateway.plist 2>/dev/null || openclaw gateway start',
      });
      steps.push({
        step: 3,
        total: 3,
        description: '等待 Gateway 启动并验证',
        command: isDryRun ? '（等待10秒后检查状态）' : 'sleep 10 && openclaw gateway status --deep',
      });
      break;

    case 'cron_400':
      const cron = await checkCronStatus();

      steps.push({
        step: 1,
        total: 4,
        description: `读取 cron 配置（发现 ${cron.webhookJobCount} 个 webhook jobs）`,
      });

      if (cron.hasWebhookJobs) {
        steps.push({
          step: 2,
          total: 4,
          description: '将 webhook 推送频率从 5min 降低到 15min',
          command: 'openclaw config set cron.deliveryInterval=15',
        });
        steps.push({
          step: 3,
          total: 4,
          description: '重启 cron scheduler',
          command: 'openclaw cron restart',
        });
        steps.push({
          step: 4,
          total: 4,
          description: '验证修复（触发测试 cron）',
          command: 'openclaw cron run test',
        });
      } else {
        steps.push({
          step: 2,
          total: 3,
          description: '将 delivery 模式从 webhook 改为 poll',
          command: 'openclaw config set cron.delivery=poll',
        });
        steps.push({
          step: 3,
          total: 3,
          description: '重启 cron scheduler',
          command: 'openclaw cron restart',
        });
      }
      break;

    case 'session_lock':
      steps.push({
        step: 1,
        total: 3,
        description: '查找孤立 session 锁文件',
        command: 'find ~/.openclaw/agents -name "*.lock" -type f',
      });
      steps.push({
        step: 2,
        total: 3,
        description: '清理孤立锁文件（>24小时未更新）',
        command: isDryRun
          ? 'find ~/.openclaw/agents -name "*.lock" -type f -mtime +1 -delete（dry-run，未执行）'
          : 'find ~/.openclaw/agents -name "*.lock" -type f -mtime +1 -delete',
      });
      steps.push({
        step: 3,
        total: 3,
        description: '验证清理结果',
        command: 'find ~/.openclaw/agents -name "*.lock" -type f | wc -l',
      });
      break;

    default:
      steps.push({
        step: 1,
        total: 1,
        description: '需要手动检查问题',
        command: 'openclaw status --deep',
      });
  }

  return steps;
}

/**
 * 执行修复（预览或执行）
 */
export async function fix(problem: Problem, isDryRun = true): Promise<FixResult> {
  const startTime = Date.now();
  const steps = await generateFixSteps(problem, isDryRun);

  console.log();
  console.log(ui.title(`🔧 ${isDryRun ? '[DRY-RUN] ' : ''}开始修复：${problem.name}`));
  console.log(ui.divider());
  console.log();

  for (const step of steps) {
    if (step.command) {
      if (isDryRun) {
        console.log(ui.step(step.step, step.total, step.description));
        console.log(`   ${ui.info('（dry-run）命令：' + step.command)}`);
      } else {
        console.log(ui.step(step.step, step.total, step.description));
        const { success, output } = await execAsync(step.command);
        if (success) {
          console.log(`   ${ui.ok('✅ ' + (output.trim() || '执行成功'))}`);
        } else {
          console.log(`   ${ui.error('❌ ' + output.trim())}`);
        }
      }
    } else {
      console.log(ui.step(step.step, step.total, step.description));
    }

    console.log();
  }

  const duration = (Date.now() - startTime) / 1000;

  return {
    taskName: problem.name,
    steps,
    totalSteps: steps.length,
    dryRun: isDryRun,
    duration,
  };
}

/**
 * 打印修复结果总结
 */
export function printFixSummary(result: FixResult) {
  console.log(ui.divider());
  console.log();

  if (result.dryRun) {
    console.log(ui.ok(`🎉 修复预览完成！共 ${result.totalSteps} 步，耗时 ${result.duration.toFixed(1)}秒`));
    console.log(ui.warn('⚠️  这是 dry-run 模式，未执行任何操作'));
    console.log();
    console.log(ui.info('执行以下命令开始修复：'));
    console.log(ui.info(`  xianxia-doctor fix --task=${result.taskName} --auto`));
  } else {
    console.log(ui.ok(`🎉 修复完成！共 ${result.totalSteps} 步，耗时 ${result.duration.toFixed(1)}秒`));
  }

  console.log();
}
