#!/usr/bin/env node
/**
 * 虾医 CLI 入口
 */
import { checkCommand } from './commands/check.js';
import { diagnoseCommand } from './commands/diagnose.js';
import { fixCommand } from './commands/fix.js';
import { monitorCommand } from './commands/monitor.js';
import { research } from './core/researcher.js';

const args = process.argv.slice(2);
const command = args[0];

async function main() {
  switch (command) {
    case 'check':
      await checkCommand();
      break;

    case 'diagnose': {
      const hours = parseInt(args[1]) || 2;
      await diagnoseCommand(hours);
      break;
    }

    case 'fix': {
      const isDryRun = !args.includes('--auto');
      const taskIndex = args.indexOf('--task');
      const taskId = taskIndex !== -1 ? args[taskIndex + 1] : 'gateway_health';
      await fixCommand(taskId, isDryRun);
      break;
    }

    case 'monitor': {
      const continuous = args.includes('--watch') || args.includes('-w');
      const intervalIndex = args.indexOf('--interval');
      const interval = intervalIndex !== -1 ? parseInt(args[intervalIndex + 1]) || 10 : 10;
      await monitorCommand(continuous, interval);
      break;
    }

    case 'research': {
      const hours = parseInt(args[1]) || 2;
      const result = await research(hours);
      console.log(`发现 ${result.problems.length} 个问题，共 ${result.totalErrors} 个错误`);
      break;
    }

    default:
      console.log(`
🦞 虾医 — OpenClaw 私人医生

用法：
  xianxia-doctor check           # 健康检查
  xianxia-doctor diagnose [小时]  # 诊断问题（默认2小时）
  xianxia-doctor fix --task <id> [--auto]  # 修复问题
  xianxia-doctor monitor [--watch] [--interval N]  # 实时监控
  xianxia-doctor research [小时]  # 研究日志

示例：
  xianxia-doctor check
  xianxia-doctor diagnose
  xianxia-doctor diagnose 4
  xianxia-doctor fix --task gateway_health
  xianxia-doctor fix --task gateway_health --auto
  xianxia-doctor monitor --watch
  xianxia-doctor monitor --watch --interval 5
      `);
  }
}

main().catch(console.error);
