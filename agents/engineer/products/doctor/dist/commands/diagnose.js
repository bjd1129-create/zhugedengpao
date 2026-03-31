"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.runDiagnose = runDiagnose;
const chalk_1 = __importDefault(require("chalk"));
const logger_1 = require("../utils/logger");
/**
 * 执行诊断
 */
async function runDiagnose(logPath) {
    console.log(chalk_1.default.blue('\n🔬 OpenClaw 诊断分析\n'));
    console.log(chalk_1.default.gray('='.repeat(50)));
    // 1. 分析日志
    console.log(chalk_1.default.yellow('\n📋 正在分析日志...'));
    const logPaths = (0, logger_1.getLogPaths)();
    if (logPaths.length > 0) {
        console.log(chalk_1.default.gray(`  找到日志目录: ${logPaths.join(', ')}`));
    }
    else {
        console.log(chalk_1.default.gray('  未找到标准日志目录，将检查当前目录'));
    }
    const diagnoseResult = await (0, logger_1.diagnoseLogs)(logPath);
    console.log(chalk_1.default.blue('\n📊 诊断结果:\n'));
    console.log(chalk_1.default.gray('-'.repeat(50)));
    if (diagnoseResult.errors.length === 0) {
        console.log(chalk_1.default.green('  ✅ 未发现错误'));
        console.log(chalk_1.default.gray('\n  日志中没有检测到明显的 HTTP 错误或 Cron 问题。\n'));
    }
    else {
        console.log(chalk_1.default.red(`  发现 ${diagnoseResult.errors.length} 个错误:\n`));
        // 按类型分组显示
        const errorGroups = new Map();
        for (const error of diagnoseResult.errors) {
            const count = errorGroups.get(error.type) || 0;
            errorGroups.set(error.type, count + 1);
        }
        console.log(chalk_1.default.yellow('  错误类型统计:'));
        for (const [type, count] of errorGroups) {
            console.log(chalk_1.default.gray(`    - ${type}: ${count} 次`));
        }
        console.log(chalk_1.default.gray('\n  最近错误详情:'));
        for (let i = 0; i < Math.min(diagnoseResult.errors.length, 10); i++) {
            const error = diagnoseResult.errors[i];
            console.log(chalk_1.default.red(`\n  [${i + 1}] ${error.type}`));
            console.log(chalk_1.default.gray(`      时间: ${error.timestamp}`));
            console.log(chalk_1.default.gray(`      消息: ${error.message.substring(0, 100)}...`));
            if (error.details) {
                console.log(chalk_1.default.gray(`      来源: ${error.details}`));
            }
        }
    }
    // 2. 生成修复建议
    console.log(chalk_1.default.gray('\n' + '='.repeat(50)));
    console.log(chalk_1.default.blue('\n🔧 修复建议:\n'));
    const fixSteps = generateFixSteps(diagnoseResult);
    for (const step of fixSteps) {
        console.log(chalk_1.default.cyan(`  ${step.order}. ${step.action}`));
        console.log(chalk_1.default.gray(`     ${step.description}`));
        if (step.command && step.dryRunOnly) {
            console.log(chalk_1.default.yellow(`     命令: ${step.command}`));
            console.log(chalk_1.default.gray(`     (仅预览，不执行)`));
        }
        else if (step.command) {
            console.log(chalk_1.default.green(`     命令: ${step.command}`));
        }
    }
    console.log(chalk_1.default.gray('\n' + '='.repeat(50)));
    return {
        steps: fixSteps,
        canAutoFix: fixSteps.some(s => !s.dryRunOnly),
        requiresManualAction: fixSteps.some(s => s.dryRunOnly)
    };
}
/**
 * 根据诊断结果生成修复步骤
 */
function generateFixSteps(diagnoseResult) {
    const steps = [];
    let order = 1;
    // 根据错误类型生成修复建议
    const hasCron400 = diagnoseResult.errors.some(e => e.type.includes('Cron 400'));
    const hasAuthError = diagnoseResult.errors.some(e => e.type.includes('401') || e.message.includes('auth'));
    const hasNetworkError = diagnoseResult.errors.some(e => e.message.includes('network') || e.message.includes('connect'));
    if (hasCron400) {
        steps.push({
            order: order++,
            action: '检查 Cron 配置',
            description: 'HTTP 400 错误通常是请求格式错误或认证失败',
            command: 'openclaw config get cron',
            dryRunOnly: true
        });
        steps.push({
            order: order++,
            action: '验证 Cron 端点',
            description: '确保 Cron 触发器的目标 URL 正确且可访问',
            dryRunOnly: true
        });
        steps.push({
            order: order++,
            action: '检查 API Key',
            description: '确认认证凭据有效且未过期',
            command: 'openclaw config get apiKey',
            dryRunOnly: true
        });
    }
    if (hasAuthError) {
        steps.push({
            order: order++,
            action: '重新认证',
            description: '认证令牌可能已过期，需要重新登录',
            command: 'openclaw auth refresh',
            dryRunOnly: true
        });
    }
    if (hasNetworkError) {
        steps.push({
            order: order++,
            action: '检查网络连接',
            description: '确保 Gateway 可以访问外部网络',
            command: 'curl -I https://api.openclaw.com',
            dryRunOnly: true
        });
        steps.push({
            order: order++,
            action: '检查防火墙',
            description: '确认端口 18789 未被防火墙阻止',
            dryRunOnly: true
        });
    }
    // 如果没有特定问题，提供通用建议
    if (steps.length === 0) {
        steps.push({
            order: order++,
            action: '重启 Gateway',
            description: '如果问题持续，尝试重启 Gateway 服务',
            command: 'openclaw gateway restart',
            dryRunOnly: true
        });
    }
    steps.push({
        order: order++,
        action: '查看完整日志',
        description: '使用详细模式查看所有日志条目',
        command: 'tail -f ~/.openclaw/logs/*.log',
        dryRunOnly: true
    });
    return steps;
}
