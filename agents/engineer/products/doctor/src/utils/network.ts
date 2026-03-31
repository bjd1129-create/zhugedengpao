import fetch from 'node-fetch';
import { CheckResult } from '../types';

/**
 * 检测 Gateway API 端点是否可达
 */
export async function checkGatewayAPI(url: string = 'http://localhost:18789/health'): Promise<CheckResult> {
  try {
    const response = await fetch(url, {
      method: 'GET',
      timeout: 5000
    });

    if (response.ok) {
      return {
        name: 'Gateway API',
        status: 'pass',
        message: `API 端点响应正常 (${response.status})`
      };
    }

    return {
      name: 'Gateway API',
      status: 'fail',
      message: `API 返回错误状态码 ${response.status}`,
      details: `URL: ${url}`
    };
  } catch (error) {
    return {
      name: 'Gateway API',
      status: 'fail',
      message: `无法连接到 API 端点`,
      details: error instanceof Error ? error.message : String(error)
    };
  }
}

/**
 * 检测网络连通性
 */
export async function checkNetworkConnectivity(): Promise<CheckResult[]> {
  const results: CheckResult[] = [];

  // 检测 localhost
  try {
    const response = await fetch('http://localhost:18789/health', {
      method: 'GET',
      timeout: 3000
    });
    results.push({
      name: 'Localhost',
      status: 'pass',
      message: '本地连接正常'
    });
  } catch {
    results.push({
      name: 'Localhost',
      status: 'warn',
      message: '本地连接不可达（Gateway 可能未运行）'
    });
  }

  return results;
}
