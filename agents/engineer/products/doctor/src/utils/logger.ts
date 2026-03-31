import * as fs from 'fs-extra';
import * as path from 'path';
import { LogError, DiagnoseResult } from '../types';

/**
 * 获取日志文件路径
 */
export function getLogPaths(): string[] {
  const homeDir = process.env.HOME || process.env.USERPROFILE || '~';
  const possiblePaths = [
    path.join(homeDir, '.openclaw', 'logs'),
    path.join(homeDir, '.config', 'openclaw', 'logs'),
    '/var/log/openclaw',
    './logs'
  ];

  return possiblePaths.filter(logPath => {
    try {
      return fs.existsSync(logPath);
    } catch {
      return false;
    }
  });
}

/**
 * 解析日志文件，查找错误
 */
export async function parseLogs(logPath?: string): Promise<LogError[]> {
  const errors: LogError[] = [];
  const searchPaths = logPath ? [logPath] : getLogPaths();

  for (const logDir of searchPaths) {
    try {
      const logFiles = await fs.readdir(logDir);
      const recentLogs = logFiles
        .filter(f => f.endsWith('.log') || f.includes('log'))
        .sort()
        .slice(-5); // 最近5个日志文件

      for (const logFile of recentLogs) {
        const logContent = await fs.readFile(path.join(logDir, logFile), 'utf-8');
        const lines = logContent.split('\n');

        for (const line of lines) {
          // 查找 HTTP 400 错误
          if (line.includes('400') || line.includes('Bad Request') || line.includes('400 Bad Request')) {
            const error = parseErrorLine(line, logFile);
            if (error) {
              errors.push(error);
            }
          }

          // 查找 Cron 相关错误
          if (line.includes('Cron') && (line.includes('error') || line.includes('Error') || line.includes('ERR'))) {
            const error = parseErrorLine(line, logFile);
            if (error) {
              errors.push(error);
            }
          }
        }
      }
    } catch {
      // 跳过无法读取的日志
    }
  }

  return errors;
}

/**
 * 解析错误行
 */
function parseErrorLine(line: string, source: string): LogError | null {
  try {
    // 尝试提取时间戳
    const timestampMatch = line.match(/^(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})/);
    const timestamp = timestampMatch ? timestampMatch[1] : new Date().toISOString();

    // 提取错误类型
    let errorType = 'Unknown';
    if (line.includes('400')) errorType = 'HTTP 400';
    else if (line.includes('401')) errorType = 'HTTP 401';
    else if (line.includes('403')) errorType = 'HTTP 403';
    else if (line.includes('500')) errorType = 'HTTP 500';

    // 判断是否是 Cron 相关
    const isCronRelated = line.includes('Cron') || line.includes('cron') || line.includes('schedule');

    return {
      timestamp,
      type: isCronRelated ? `Cron ${errorType}` : errorType,
      message: line.substring(0, 200), // 限制消息长度
      details: `来源: ${source}`
    };
  } catch {
    return null;
  }
}

/**
 * 生成诊断结果
 */
export async function diagnoseLogs(logPath?: string): Promise<DiagnoseResult> {
  const errors = await parseLogs(logPath);

  // 过滤 Cron 400 错误
  const cron400Errors = errors.filter(e => 
    e.type.includes('Cron') && e.type.includes('400')
  );

  const summary = cron400Errors.length > 0
    ? `发现 ${cron400Errors.length} 个 Cron 400 错误`
    : errors.length > 0
    ? `发现 ${errors.length} 个错误，但无 Cron 400 错误`
    : '未发现明显错误';

  return {
    errors: cron400Errors.length > 0 ? cron400Errors : errors.slice(0, 10),
    summary
  };
}
