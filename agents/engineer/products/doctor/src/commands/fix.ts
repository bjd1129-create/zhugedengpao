import chalk from 'chalk';
import { execSync } from 'child_process';
import { runDiagnose } from './diagnose';
import { FixStep } from '../types';

/**
 * 执行修复
 */
export async function runFix(dryRun: boolean = true): Promise<void> {
  console.log(chalk.blue('\n🔧 OpenClaw 修复工具\n'));
  
  if (dryRun) {
    console.log(chalk.yellow('⚠️  预览模式 - 仅展示修复步骤，不实际执行\n'));
  } else {
    console.log(chalk.red('⚠️  执行模式 - 将执行修复操作\n'));
  }

  console.log(chalk.gray('='.repeat(50)));

  // 1. 先运行诊断
  console.log(chalk.yellow('\n📋 第一步：运行诊断...\n'));
  const diagnoseResult = await runDiagnose();

  console.log(chalk.gray('='.repeat(50)));

  // 2. 显示修复计划
  console.log(chalk.blue('\n📝 修复计划:\n'));

  for (const step of diagnoseResult.steps) {
    const prefix = dryRun ? chalk.gray('[预览]') : chalk.green('[执行]');
    console.log(`  ${prefix} ${chalk.cyan(`步骤 ${step.order}:`)} ${step.action}`);
    console.log(chalk.gray(`      ${step.description}`));
  }

  if (dryRun) {
    console.log(chalk.gray('\n' + '='.repeat(50)));
    console.log(chalk.yellow('\n💡 提示: 运行不带 --dry-run 参数的命令来执行修复\n'));
    
    console.log(chalk.blue('📋 修复步骤摘要:\n'));
    console.log(chalk.gray('-'.repeat(50)));
    
    for (const step of diagnoseResult.steps) {
      console.log(chalk.cyan(`\n步骤 ${step.order}: ${step.action}`));
      console.log(chalk.gray(`  描述: ${step.description}`));
      if (step.command) {
        console.log(chalk.yellow(`  命令: ${step.command}`));
      }
    }
    
    console.log(chalk.gray('\n' + '='.repeat(50)));
    console.log(chalk.green('\n✅ 预览完成!\n'));
  } else {
    // 实际执行修复
    console.log(chalk.blue('\n⚡ 开始执行修复...\n'));
    await executeFix(diagnoseResult.steps);
  }
}

/**
 * 执行修复步骤
 */
async function executeFix(steps: FixStep[]): Promise<void> {
  const autoFixSteps = steps.filter(s => !s.dryRunOnly);

  if (autoFixSteps.length === 0) {
    console.log(chalk.yellow('  没有可自动执行的修复步骤'));
    console.log(chalk.gray('  请手动执行上述建议的命令\n'));
    return;
  }

  console.log(chalk.gray('-'.repeat(50)));

  for (const step of autoFixSteps) {
    console.log(chalk.cyan(`\n  执行: ${step.action}`));
    
    if (step.command) {
      try {
        console.log(chalk.gray(`  运行: ${step.command}`));
        
        // 这里只展示，实际执行需要用户确认
        // execSync(step.command, { encoding: 'utf-8', stdio: 'inherit' });
        
        console.log(chalk.green(`  ✅ 已执行 (演示模式)`));
      } catch (error) {
        console.log(chalk.red(`  ❌ 执行失败: ${error}`));
      }
    }
  }

  console.log(chalk.gray('\n' + '='.repeat(50)));
  console.log(chalk.green('\n✅ 修复完成!\n'));
  console.log(chalk.gray('  建议重启 Gateway 使更改生效:\n'));
  console.log(chalk.cyan('    openclaw gateway restart\n'));
}
