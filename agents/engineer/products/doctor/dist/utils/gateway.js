"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.checkGatewayProcess = checkGatewayProcess;
exports.checkGatewayPort = checkGatewayPort;
exports.getGatewayStatus = getGatewayStatus;
const child_process_1 = require("child_process");
/**
 * 检测 Gateway 进程是否在运行
 */
function checkGatewayProcess() {
    try {
        // 使用 ps 命令检测 openclaw 或 clawd 进程
        const output = (0, child_process_1.execSync)('ps aux | grep -E "(openclaw|clawd)" | grep -v grep', {
            encoding: 'utf-8',
            timeout: 5000
        });
        if (output.includes('openclaw') || output.includes('clawd')) {
            // 尝试提取 PID
            const pidMatch = output.match(/(\d+)/);
            return {
                running: true,
                pid: pidMatch ? parseInt(pidMatch[1]) : undefined
            };
        }
        return { running: false };
    }
    catch {
        return { running: false };
    }
}
/**
 * 检测 Gateway 端口是否在监听
 */
function checkGatewayPort(port = 18789) {
    try {
        const output = (0, child_process_1.execSync)(`lsof -i :${port} 2>/dev/null || netstat -an 2>/dev/null | grep ${port}`, {
            encoding: 'utf-8',
            timeout: 5000
        });
        if (output.includes('LISTEN') || output.includes(port.toString())) {
            return {
                name: 'Gateway Port',
                status: 'pass',
                message: `端口 ${port} 正在监听`
            };
        }
        return {
            name: 'Gateway Port',
            status: 'fail',
            message: `端口 ${port} 未监听`
        };
    }
    catch {
        return {
            name: 'Gateway Port',
            status: 'fail',
            message: `无法检测端口 ${port} 状态`
        };
    }
}
/**
 * 获取完整的 Gateway 状态
 */
function getGatewayStatus() {
    const processStatus = checkGatewayProcess();
    return {
        ...processStatus,
        port: 18789 // 默认端口
    };
}
