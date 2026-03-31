import { GatewayStatus, CheckResult } from '../types';
/**
 * 检测 Gateway 进程是否在运行
 */
export declare function checkGatewayProcess(): GatewayStatus;
/**
 * 检测 Gateway 端口是否在监听
 */
export declare function checkGatewayPort(port?: number): CheckResult;
/**
 * 获取完整的 Gateway 状态
 */
export declare function getGatewayStatus(): GatewayStatus;
