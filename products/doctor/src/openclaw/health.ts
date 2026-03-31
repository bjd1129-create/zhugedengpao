/**
 * Gateway 健康检查
 */
import { execSync } from 'child_process';
import * as fs from 'fs-extra';
import { PATHS } from './paths.js';

export interface HealthStatus {
  gatewayAlive: boolean;
  pid: number | null;
  portListening: boolean;
  networkReachable: boolean;
  uptime?: string;
  issues: string[];
}

/**
 * 检查 Gateway 进程状态
 */
export async function checkGatewayProcess(): Promise<{ alive: boolean; pid: number | null; uptime?: string }> {
  try {
    const output = execSync('openclaw gateway status --deep 2>/dev/null', {
      encoding: 'utf-8',
      timeout: 10000,
    });

    // 解析 PID
    const pidMatch = output.match(/pid[= ](\d+)/i);
    const uptimeMatch = output.match(/uptime[: ] (.+)/i);

    return {
      alive: true,
      pid: pidMatch ? parseInt(pidMatch[1]) : null,
      uptime: uptimeMatch ? uptimeMatch[1] : undefined,
    };
  } catch {
    // 尝试从 PID 文件读取
    try {
      if (await fs.pathExists(PATHS.gatewayPid)) {
        const pid = parseInt(await fs.readFile(PATHS.gatewayPid, 'utf-8'));
        return { alive: false, pid, uptime: undefined }; // 进程可能已死
      }
    } catch {
      // ignore
    }

    return { alive: false, pid: null };
  }
}

/**
 * 检查端口是否监听
 */
export function checkPortListening(port = 18790): boolean {
  try {
    const output = execSync(`lsof -i :${port} 2>/dev/null || true`, {
      encoding: 'utf-8',
    });
    return output.includes(`${port}`);
  } catch {
    return false;
  }
}

/**
 * 综合健康检查
 */
export async function checkHealth(): Promise<HealthStatus> {
  const issues: string[] = [];
  const { alive, pid, uptime } = await checkGatewayProcess();
  const portListening = checkPortListening();

  if (!alive) {
    issues.push('Gateway 进程未运行');
  }

  if (alive && !portListening) {
    issues.push('Gateway 进程存在但端口未监听（可能卡死）');
  }

  return {
    gatewayAlive: alive && portListening,
    pid,
    portListening,
    networkReachable: portListening, // 如果端口在监听，网络就是通的
    uptime,
    issues,
  };
}
