// 检查结果类型
export interface CheckResult {
  name: string;
  status: 'pass' | 'fail' | 'warn';
  message: string;
  details?: string;
}

// Gateway 状态
export interface GatewayStatus {
  running: boolean;
  pid?: number;
  port?: number;
  version?: string;
}

// 诊断结果
export interface DiagnoseResult {
  errors: LogError[];
  summary: string;
}

// 日志错误
export interface LogError {
  timestamp: string;
  type: string;
  message: string;
  details?: string;
}

// 修复步骤
export interface FixStep {
  order: number;
  action: string;
  description: string;
  command?: string;
  dryRunOnly: boolean;
}

// 修复结果
export interface FixResult {
  steps: FixStep[];
  canAutoFix: boolean;
  requiresManualAction: boolean;
}
