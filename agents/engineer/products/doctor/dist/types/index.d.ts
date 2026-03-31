export interface CheckResult {
    name: string;
    status: 'pass' | 'fail' | 'warn';
    message: string;
    details?: string;
}
export interface GatewayStatus {
    running: boolean;
    pid?: number;
    port?: number;
    version?: string;
}
export interface DiagnoseResult {
    errors: LogError[];
    summary: string;
}
export interface LogError {
    timestamp: string;
    type: string;
    message: string;
    details?: string;
}
export interface FixStep {
    order: number;
    action: string;
    description: string;
    command?: string;
    dryRunOnly: boolean;
}
export interface FixResult {
    steps: FixStep[];
    canAutoFix: boolean;
    requiresManualAction: boolean;
}
