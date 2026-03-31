/**
 * monitor 命令 — 实时检测 OpenClaw 和 Channel 状态
 */
import { checkHealth, HealthStatus } from '../openclaw/health.js';
import { checkCronStatus } from '../openclaw/cron.js';
import { checkChannelStatus, ChannelStatus } from '../openclaw/channels.js';
import { ui } from '../ui/output.js';

export interface MonitorResult {
  gateway: HealthStatus;
  cron: { jobs: number; webhookJobs: number };
  channels: ChannelStatus[];
  timestamp: string;
}

export async function monitorCommand(continuous = false, intervalSeconds = 10): Promise<void> {
  const printHeader = () => {
    console.clear();
    console.log(ui.title('📡 虾医 — 实时监控'));
    console.log(ui.divider());
    console.log();
  };

  const printStatus = async () => {
    const [gateway, cron, channels] = await Promise.all([
      checkHealth(),
      checkCronStatus(),
      checkChannelStatus(),
    ]);

    // Gateway
    if (gateway.gatewayAlive) {
      console.log(ui.ok('Gateway') + '  ' + (gateway.pid ? `PID ${gateway.pid}` : '') + (gateway.uptime ? ` (${gateway.uptime})` : ''));
    } else {
      console.log(ui.error('Gateway') + '  ' + gateway.issues.join(' / '));
    }

    // Cron
    if (cron.jobs.length === 0) {
      console.log(ui.info('Cron') + '  未发现任务');
    } else {
      console.log(ui.info('Cron') + `  ${cron.jobs.length} 个任务`);
      if (cron.hasWebhookJobs) {
        console.log(`       ${ui.warn(`${cron.webhookJobCount} 个 webhook 推送`)}`);
      }
    }

    // Channels
    console.log();
    console.log(ui.title('Channel 状态：'));
    if (channels.length === 0) {
      console.log(ui.warn('  未配置任何 channel'));
    } else {
      for (const ch of channels) {
        // 如果 Gateway 挂了，即使 channel 配置存在也显示警告
        if (!gateway.gatewayAlive) {
          console.log(ui.warn(`  ${ch.name}`) + `  ${ch.type} @ ${ch.account || 'default'} — Gateway异常`);
        } else if (ch.connected) {
          console.log(ui.ok(`  ${ch.name}`) + `  ${ch.type} @ ${ch.account || 'default'}`);
        } else {
          console.log(ui.error(`  ${ch.name}`) + `  ${ch.type} — ${ch.error || 'disconnected'}`);
        }
      }
    }

    console.log();
    console.log(ui.divider());
    console.log(ui.info(`⏱  ${new Date().toLocaleString()}`));
  };

  if (!continuous) {
    printHeader();
    await printStatus();
    return;
  }

  // 持续监控模式
  console.log(ui.info('持续监控模式已启动，按 Ctrl+C 停止'));
  console.log();

  // eslint-disable-next-line no-constant-condition
  while (true) {
    printHeader();
    await printStatus();
    console.log(ui.info(`⏱  下次刷新：${intervalSeconds}秒后...`));

    await new Promise(resolve => setTimeout(resolve, intervalSeconds * 1000));
  }
}
