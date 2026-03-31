import { CheckResult } from '../types';
/**
 * 检测 Gateway API 端点是否可达
 */
export declare function checkGatewayAPI(url?: string): Promise<CheckResult>;
/**
 * 检测网络连通性
 */
export declare function checkNetworkConnectivity(): Promise<CheckResult[]>;
