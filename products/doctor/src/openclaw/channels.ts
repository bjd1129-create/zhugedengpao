/**
 * Channel 状态检测
 */
import fs from 'fs-extra';
import { PATHS } from './paths.js';

export interface ChannelStatus {
  name: string;
  type: string;
  account?: string;
  connected: boolean;
  error?: string;
}

interface OpenClawConfig {
  channels?: {
    feishu?: {
      accounts?: Record<string, { enabled?: boolean; connectionMode?: string }>;
    };
  };
}

/**
 * 获取所有配置的 channel 列表
 */
async function getConfiguredChannels(): Promise<ChannelStatus[]> {
  const channels: ChannelStatus[] = [];

  try {
    const content = await fs.readFile(PATHS.config, 'utf-8');
    const config: OpenClawConfig = JSON.parse(content);
    const feishuAccounts = config.channels?.feishu?.accounts || {};

    for (const [name, accountConfig] of Object.entries(feishuAccounts)) {
      // skip 'default' account (it's a template, not an actual account)
      if (name === 'default') continue;
      if (!accountConfig.enabled) continue;

      channels.push({
        name: `feishu/${name}`,
        type: 'feishu',
        account: name,
        connected: false,
        error: 'unknown',
      });
    }
  } catch (e) {
    // ignore - channel detection is best-effort
  }

  return channels;
}

/**
 * 检测 Gateway WebSocket 健康状态（间接反映 channel 连接状态）
 */
async function checkGatewayWebSocket(): Promise<boolean> {
  try {
    const http = await import('http');
    return new Promise((resolve) => {
      const req = http.get('http://127.0.0.1:18790/health', { timeout: 3000 }, (res) => {
        resolve(res.statusCode === 200);
      });
      req.on('error', () => resolve(false));
      req.on('timeout', () => { req.destroy(); resolve(false); });
    });
  } catch {
    return false;
  }
}

/**
 * 综合 channel 状态检测
 */
export async function checkChannelStatus(): Promise<ChannelStatus[]> {
  const channels = await getConfiguredChannels();
  const wsAlive = await checkGatewayWebSocket();

  // Gateway WebSocket 存活说明 channel 协议层是通的
  // 实际 channel 连接状态需要通过 Gateway 内部状态判断
  // 这里做简化：如果 Gateway WS 活着，channel 就认为是好的
  return channels.map(ch => ({
    ...ch,
    connected: wsAlive,
    error: wsAlive ? undefined : 'Gateway WebSocket 未连接',
  }));
}
