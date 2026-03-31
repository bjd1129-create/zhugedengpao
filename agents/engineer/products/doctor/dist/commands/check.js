"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.runCheck = runCheck;
const chalk_1 = __importDefault(require("chalk"));
const gateway_1 = require("../utils/gateway");
const network_1 = require("../utils/network");
/**
 * 执行健康检查
 */
async function runCheck() {
    console.log(chalk_1.default.blue('\n🔍 OpenClaw Gateway 健康检查\n'));
    console.log(chalk_1.default.gray('='.repeat(50)));
    const results = [];
    // 1. 检查进程
    console.log(chalk_1.default.yellow('\n📋 进程状态检查...'));
    const gatewayStatus = (0, gateway_1.getGatewayStatus)();
    if (gatewayStatus.running) {
        console.log(chalk_1.default.green('  ✅ Gateway 进程正在运行'));
        if (gatewayStatus.pid) {
            console.log(chalk_1.default.gray(`     PID: ${gatewayStatus.pid}`));
        }
        results.push({
            name: 'Gateway Process',
            status: 'pass',
            message: `进程运行中 (PID: ${gatewayStatus.pid || 'unknown'})`
        });
    }
    else {
        console.log(chalk_1.default.red('  ❌ Gateway 进程未运行'));
        results.push({
            name: 'Gateway Process',
            status: 'fail',
            message: '进程未运行'
        });
    }
    // 2. 检查端口
    console.log(chalk_1.default.yellow('\n📋 端口监听检查...'));
    const portResult = (0, gateway_1.checkGatewayPort)(gatewayStatus.port || 18789);
    results.push(portResult);
    if (portResult.status === 'pass') {
        console.log(chalk_1.default.green(`  ✅ ${portResult.message}`));
    }
    else {
        console.log(chalk_1.default.red(`  ❌ ${portResult.message}`));
    }
    // 3. 检查 API
    console.log(chalk_1.default.yellow('\n📋 API 连通性检查...'));
    const apiResult = await (0, network_1.checkGatewayAPI)();
    results.push(apiResult);
    if (apiResult.status === 'pass') {
        console.log(chalk_1.default.green(`  ✅ ${apiResult.message}`));
    }
    else {
        console.log(chalk_1.default.red(`  ❌ ${apiResult.message}`));
        if (apiResult.details) {
            console.log(chalk_1.default.gray(`     ${apiResult.details}`));
        }
    }
    // 4. 网络连通性
    console.log(chalk_1.default.yellow('\n📋 网络连通性检查...'));
    const networkResults = await (0, network_1.checkNetworkConnectivity)();
    for (const result of networkResults) {
        if (result.status === 'pass') {
            console.log(chalk_1.default.green(`  ✅ ${result.name}: ${result.message}`));
        }
        else {
            console.log(chalk_1.default.yellow(`  ⚠️  ${result.name}: ${result.message}`));
        }
        results.push(result);
    }
    // 汇总
    console.log(chalk_1.default.gray('\n' + '='.repeat(50)));
    console.log(chalk_1.default.blue('\n📊 检查汇总:\n'));
    const passCount = results.filter(r => r.status === 'pass').length;
    const failCount = results.filter(r => r.status === 'fail').length;
    const warnCount = results.filter(r => r.status === 'warn').length;
    console.log(chalk_1.default.green(`  ✅ 通过: ${passCount}`));
    console.log(chalk_1.default.red(`  ❌ 失败: ${failCount}`));
    console.log(chalk_1.default.yellow(`  ⚠️  警告: ${warnCount}`));
    if (failCount === 0 && warnCount === 0) {
        console.log(chalk_1.default.green('\n🎉 Gateway 运行正常!\n'));
    }
    else if (failCount > 0) {
        console.log(chalk_1.default.red('\n⚠️  检测到问题，请运行 diagnose 命令进行详细诊断\n'));
    }
    else {
        console.log(chalk_1.default.yellow('\n⚠️  存在一些警告，建议运行 diagnose 命令\n'));
    }
}
