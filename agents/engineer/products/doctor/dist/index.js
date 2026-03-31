#!/usr/bin/env node
"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const chalk_1 = __importDefault(require("chalk"));
const check_1 = require("./commands/check");
const diagnose_1 = require("./commands/diagnose");
const fix_1 = require("./commands/fix");
/**
 * 主入口
 */
async function main() {
    const args = process.argv.slice(2);
    const command = args[0] || 'help';
    const options = args.slice(1);
    // 检查是否包含 --dry-run
    const dryRun = options.includes('--dry-run') || options.includes('-n');
    switch (command) {
        case 'check':
            await (0, check_1.runCheck)();
            break;
        case 'diagnose':
        case 'diag':
            const logPath = options.find(opt => !opt.startsWith('-'));
            await (0, diagnose_1.runDiagnose)(logPath);
            break;
        case 'fix':
            await (0, fix_1.runFix)(dryRun);
            break;
        case 'help':
        case '--help':
        case '-h':
        default:
            showHelp();
            break;
    }
}
/**
 * 显示帮助信息
 */
function showHelp() {
    console.log(chalk_1.default.blue(`
╔══════════════════════════════════════════════════════╗
║                                                      ║
║              OpenClaw Doctor v0.1.0                  ║
║           Gateway 诊断与修复工具                      ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
  `));
    console.log(chalk_1.default.cyan('用法:'));
    console.log(chalk_1.default.gray('  openclaw-doctor <命令> [选项]\n'));
    console.log(chalk_1.default.cyan('命令:'));
    console.log(chalk_1.default.gray('  check              '), '检查 Gateway 健康状态');
    console.log(chalk_1.default.gray('  diagnose, diag     '), '诊断问题并生成修复建议');
    console.log(chalk_1.default.gray('  fix [--dry-run]    '), '修复问题（加 --dry-run 仅预览）\n');
    console.log(chalk_1.default.cyan('选项:'));
    console.log(chalk_1.default.gray('  --dry-run, -n      '), '仅显示修复步骤，不实际执行\n');
    console.log(chalk_1.default.cyan('示例:'));
    console.log(chalk_1.default.gray('  openclaw-doctor check'));
    console.log(chalk_1.default.gray('  openclaw-doctor diagnose'));
    console.log(chalk_1.default.gray('  openclaw-doctor fix --dry-run'));
    console.log(chalk_1.default.gray('  openclaw-doctor fix\n'));
}
// 执行
main().catch(error => {
    console.error(chalk_1.default.red(`\n❌ 错误: ${error.message}\n`));
    process.exit(1);
});
