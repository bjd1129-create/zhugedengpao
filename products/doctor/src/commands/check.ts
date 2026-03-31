/**
 * check 命令 — 健康检查
 */
import { checkHealth } from '../openclaw/health.js';
import { checkCronStatus } from '../openclaw/cron.js';
import { ui } from '../ui/output.js';

export async function checkCommand() {
  console.log();
  console.log(ui.title('🏥 虾医 — 健康检查'));
  console.log(ui.divider());
  console.log();

  // 1. Gateway 健康检查
  const health = await checkHealth();

  if (health.gatewayAlive) {
    console.log(ui.ok('Gateway 运行正常'));
    if (health.pid) {
      console.log(`   PID: ${health.pid}`);
    }
    if (health.uptime) {
      console.log(`   运行时间: ${health.uptime}`);
    }
  } else {
    console.log(ui.error('Gateway 运行异常'));
    if (health.pid) {
      console.log(`   PID: ${health.pid}（进程可能已死）`);
    }
  }

  health.issues.forEach(issue => {
    console.log(`   ${ui.warn(issue)}`);
  });

  console.log();

  // 2. Cron 状态
  const cron = await checkCronStatus();

  if (cron.jobs.length === 0) {
    console.log(ui.info('未发现 cron 任务'));
  } else {
    console.log(ui.info(`发现 ${cron.jobs.length} 个 cron 任务`));
    if (cron.hasWebhookJobs) {
      console.log(`   ${ui.warn(`${cron.webhookJobCount} 个使用 webhook 推送`)}`);
    }
  }

  console.log();
  console.log(ui.divider());
  console.log();

  // 返回健康状态，供集成使用
  return health;
}
