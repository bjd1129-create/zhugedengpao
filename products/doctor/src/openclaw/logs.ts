/**
 * 读取 OpenClaw 日志文件
 */
import fs from 'fs-extra';
import { PATHS } from './paths.js';

export interface LogEntry {
  timestamp: string;
  level: 'INFO' | 'WARN' | 'ERROR';
  message: string;
  raw: string;
}

/**
 * 解析单行日志
 */
function parseLine(line: string): LogEntry | null {
  // 格式: [2026-03-31T10:00:00.000Z] INFO  message
  const match = line.match(/^\[([^]]+)\]\s+(\w+)\s+(.+)$/);
  if (!match) return null;

  return {
    timestamp: match[1],
    level: match[2] as 'INFO' | 'WARN' | 'ERROR',
    message: match[3],
    raw: line,
  };
}

/**
 * 读取错误日志
 */
export async function readErrorLog(hoursAgo = 2): Promise<LogEntry[]> {
  if (!await fs.pathExists(PATHS.gatewayErrLog)) {
    return [];
  }

  const content = fs.readFileSync(PATHS.gatewayErrLog, 'utf-8');
  const lines = content.split('\n').filter(Boolean);
  const cutoff = Date.now() - hoursAgo * 60 * 60 * 1000;

  return lines
    .map(parseLine)
    .filter((entry): entry is LogEntry => {
      if (!entry) return false;
      const entryTime = new Date(entry.timestamp).getTime();
      return entryTime >= cutoff;
    });
}

/**
 * 统计错误类型
 */
export function categorizeErrors(entries: LogEntry[]): Map<string, LogEntry[]> {
  const categories = new Map<string, LogEntry[]>();

  for (const entry of entries) {
    let key = 'unknown';

    if (entry.message.includes('HTTP 400') || entry.message.includes('400 error')) {
      key = 'cron_400';
    } else if (entry.message.includes('session') && entry.message.includes('lock')) {
      key = 'session_lock';
    } else if (entry.message.includes('Gateway') && entry.message.includes('crash')) {
      key = 'gateway_crash';
    } else if (entry.message.includes('timeout')) {
      key = 'timeout';
    } else if (entry.message.includes('delivery')) {
      key = 'delivery_failed';
    } else if (entry.level === 'ERROR') {
      key = 'general_error';
    }

    if (!categories.has(key)) {
      categories.set(key, []);
    }
    categories.get(key)!.push(entry);
  }

  return categories;
}
