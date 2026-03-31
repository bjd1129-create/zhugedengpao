/**
 * OpenClaw 关键路径常量
 */
import { homedir } from 'os';
import { join } from 'path';

export const OPENCLAW_DIR = join(homedir(), '.openclaw');

export const PATHS = {
  // 日志
  logs: join(OPENCLAW_DIR, 'logs'),
  gatewayErrLog: join(OPENCLAW_DIR, 'logs', 'gateway.err.log'),
  gatewayLog: join(OPENCLAW_DIR, 'logs', 'gateway.log'),

  // Cron
  cron: join(OPENCLAW_DIR, 'cron'),
  cronJobsJson: join(OPENCLAW_DIR, 'cron', 'jobs.json'),
  cronRunsDir: join(OPENCLAW_DIR, 'cron', 'runs'),

  // Session
  sessions: join(OPENCLAW_DIR, 'agents'),

  // 配置
  config: join(OPENCLAW_DIR, 'openclaw.json'),
  gatewayPid: join(OPENCLAW_DIR, 'gateway.pid'),
};
