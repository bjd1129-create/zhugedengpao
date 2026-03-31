import { LogError, DiagnoseResult } from '../types';
/**
 * 获取日志文件路径
 */
export declare function getLogPaths(): string[];
/**
 * 解析日志文件，查找错误
 */
export declare function parseLogs(logPath?: string): Promise<LogError[]>;
/**
 * 生成诊断结果
 */
export declare function diagnoseLogs(logPath?: string): Promise<DiagnoseResult>;
