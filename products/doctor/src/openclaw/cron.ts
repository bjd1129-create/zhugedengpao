/**
 * Cron 任务状态检查
 */
import * as fs from 'fs-extra';
import { PATHS } from './paths.js';

export interface CronJob {
  id: string;
  name: string;
  schedule: string;
  delivery: string;
  enabled: boolean;
}

export interface CronStatus {
  jobs: CronJob[];
  hasWebhookJobs: boolean;
  webhookJobCount: number;
}

/**
 * 读取 Cron 配置
 */
export async function checkCronStatus(): Promise<CronStatus> {
  if (!await fs.pathExists(PATHS.cronJobsJson)) {
    return { jobs: [], hasWebhookJobs: false, webhookJobCount: 0 };
  }

  let raw: any;
  try {
    raw = await fs.readJson(PATHS.cronJobsJson);
  } catch {
    return { jobs: [], hasWebhookJobs: false, webhookJobCount: 0 };
  }

  const jobs: CronJob[] = (raw.jobs || raw.items || []).map((j: any) => ({
    id: j.id || j.name || 'unknown',
    name: j.name || 'unnamed',
    schedule: j.schedule || '',
    delivery: j.delivery || 'poll',
    enabled: j.enabled !== false,
  }));

  const webhookJobs = jobs.filter(j => j.delivery === 'webhook');
  const webhookJobCount = webhookJobs.length;

  return {
    jobs,
    hasWebhookJobs: webhookJobCount > 0,
    webhookJobCount,
  };
}
