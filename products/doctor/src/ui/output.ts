/**
 * UI 输出 — chalk 样式化
 */
import chalk from 'chalk';

export const ui = {
  // 状态标识
  ok: (text: string) => chalk.green(`✅ ${text}`),
  warn: (text: string) => chalk.yellow(`🟡 ${text}`),
  error: (text: string) => chalk.red(`🔴 ${text}`),
  info: (text: string) => chalk.blue(`ℹ️  ${text}`),

  // 步骤
  step: (current: number, total: number, text: string) => {
    const icon = text.includes('读取') ? '📋' : text.includes('修改') || text.includes('降低') ? '⚙️' : text.includes('重启') || text.includes('启动') || text.includes('停止') ? '🔄' : text.includes('验证') || text.includes('等待') ? '✅' : '👉';
    return chalk.yellow(`[${current}/${total}]`) + ` ${icon} ${text}`;
  },

  // 标题
  title: (text: string) => chalk.bold.cyan(text),

  // 分隔线
  divider: () => chalk.gray('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'),

  // 错误级别
  severity: {
    critical: () => chalk.red('🔴 严重'),
    medium: () => chalk.yellow('🟡 中等'),
    low: () => chalk.blue('🔵 轻微'),
  },

  // dry-run 标识
  dryRun: () => chalk.yellow('[DRY-RUN]'),
};

/**
 * 打印诊断报告头部
 */
export function printDiagnoseHeader(timeframe: number) {
  console.log(ui.title(`🔍 分析最近 ${timeframe} 小时日志...`));
  console.log(ui.divider());
  console.log();
}

/**
 * 打印修复报告头部
 */
export function printFixHeader(taskName: string, isDryRun: boolean) {
  if (isDryRun) {
    console.log(ui.dryRun(), ui.title(`开始修复预览 — 不会执行任何操作`));
  } else {
    console.log(ui.title(`🔧 开始修复：${taskName}`));
  }
  console.log(ui.divider());
  console.log();
}
