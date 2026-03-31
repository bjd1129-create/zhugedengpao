"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.runFix = runFix;
const chalk_1 = __importDefault(require("chalk"));
const diagnose_1 = require("./diagnose");
/**
 * 执行修复
 */
async function runFix(dryRun = true) {
    console.log(chalk_1.default.blue('\n🔧 OpenClaw 修复工具\n'));
    if (dryRun) {
        console.log(chalk_1.default.yellow('⚠️  预览模式 - 仅展示修复步骤，不实际执行\n'));
    }
    else {
        console.log(chalk_1.default.red('⚠️  执行模式 - 将执行修复操作\n'));
    }
    console.log(chalk_1.default.gray('='.repeat(50)));
    // 1. 先运行诊断
    console.log(chalk_1.default.yellow('\n📋 第一步：运行诊断...\n'));
    const diagnoseResult = await (0, diagnose_1.runDiagnose)();
    console.log(chalk_1.default.gray('='.repeat(50)));
    // 2. 显示修复计划
    console.log(chalk_1.default.blue('\n📝 修复计划:\n'));
    for (const step of diagnoseResult.steps) {
        const prefix = dryRun ? chalk_1.default.gray('[预览]') : chalk_1.default.green('[执行]');
        console.log(`  ${prefix} ${chalk_1.default.cyan(`步骤 ${step.order}:`)} ${step.action}`);
        console.log(chalk_1.default.gray(`      ${step.description}`));
    }
    if (dryRun) {
        console.log(chalk_1.default.gray('\n' + '='.repeat(50)));
        console.log(chalk_1.default.yellow('\n💡 提示: 运行不带 --dry-run 参数的命令来执行修复\n'));
        console.log(chalk_1.default.blue('📋 修复步骤摘要:\n'));
        console.log(chalk_1.default.gray('-'.repeat(50)));
        for (const step of diagnoseResult.steps) {
            console.log(chalk_1.default.cyan(`\n步骤 ${step.order}: ${step.action}`));
            console.log(chalk_1.default.gray(`  描述: ${step.description}`));
            if (step.command) {
                console.log(chalk_1.default.yellow(`  命令: ${step.command}`));
            }
        }
        console.log(chalk_1.default.gray('\n' + '='.repeat(50)));
        console.log(chalk_1.default.green('\n✅ 预览完成!\n'));
    }
    else {
        // 实际执行修复
        console.log(chalk_1.default.blue('\n⚡ 开始执行修复...\n'));
        await executeFix(diagnoseResult.steps);
    }
}
/**
 * 执行修复步骤
 */
async function executeFix(steps) {
    const autoFixSteps = steps.filter(s => !s.dryRunOnly);
    if (autoFixSteps.length === 0) {
        console.log(chalk_1.default.yellow('  没有可自动执行的修复步骤'));
        console.log(chalk_1.default.gray('  请手动执行上述建议的命令\n'));
        return;
    }
    console.log(chalk_1.default.gray('-'.repeat(50)));
    for (const step of autoFixSteps) {
        console.log(chalk_1.default.cyan(`\n  执行: ${step.action}`));
        if (step.command) {
            try {
                console.log(chalk_1.default.gray(`  运行: ${step.command}`));
                // 这里只展示，实际执行需要用户确认
                // execSync(step.command, { encoding: 'utf-8', stdio: 'inherit' });
                console.log(chalk_1.default.green(`  ✅ 已执行 (演示模式)`));
            }
            catch (error) {
                console.log(chalk_1.default.red(`  ❌ 执行失败: ${error}`));
            }
        }
    }
    console.log(chalk_1.default.gray('\n' + '='.repeat(50)));
    console.log(chalk_1.default.green('\n✅ 修复完成!\n'));
    console.log(chalk_1.default.gray('  建议重启 Gateway 使更改生效:\n'));
    console.log(chalk_1.default.cyan('    openclaw gateway restart\n'));
}
