import chalk from 'chalk';
import { checkGatewayProcess, checkGatewayPort, getGatewayStatus } from '../utils/gateway';
import { checkGatewayAPI, checkNetworkConnectivity } from '../utils/network';
import { CheckResult } from '../types';

/**
 * 执行健康检查
 */
export async function runCheck(): Promise<void> {
  console.log(chalk.blue('\n🔍 OpenClaw Gateway 健康检查\n'));
  console.log(chalk.gray('=' .repeat(50)));

  const results: CheckResult[] = [];

  // 1. 检查进程
  console.log(chalk.yellow('\n📋 进程状态检查...'));
  const gatewayStatus = getGatewayStatus();

  if (gatewayStatus.running) {
    console.log(chalk.green('  ✅ Gateway 进程正在运行'));
    if (gatewayStatus.pid) {
      console.log(chalk.gray(`     PID: ${gatewayStatus.pid}`));
    }
    results.push({
      name: 'Gateway Process',
      status: 'pass',
      message: `进程运行中 (PID: ${gatewayStatus.pid || 'unknown'})`
    });
  } else {
    console.log(chalk.red('  ❌ Gateway 进程未运行'));
    results.push({
      name: 'Gateway Process',
      status: 'fail',
      message: '进程未运行'
    });
  }

  // 2. 检查端口
  console.log(chalk.yellow('\n📋 端口监听检查...'));
  const portResult = checkGatewayPort(gatewayStatus.port || 18789);
  results.push(portResult);

  if (portResult.status === 'pass') {
    console.log(chalk.green(`  ✅ ${portResult.message}`));
  } else {
    console.log(chalk.red(`  ❌ ${portResult.message}`));
  }

  // 3. 检查 API
  console.log(chalk.yellow('\n📋 API 连通性检查...'));
  const apiResult = await checkGatewayAPI();
  results.push(apiResult);

  if (apiResult.status === 'pass') {
    console.log(chalk.green(`  ✅ ${apiResult.message}`));
  } else {
    console.log(chalk.red(`  ❌ ${apiResult.message}`));
    if (apiResult.details) {
      console.log(chalk.gray(`     ${apiResult.details}`));
    }
  }

  // 4. 网络连通性
  console.log(chalk.yellow('\n📋 网络连通性检查...'));
  const networkResults = await checkNetworkConnectivity();
  
  for (const result of networkResults) {
    if (result.status === 'pass') {
      console.log(chalk.green(`  ✅ ${result.name}: ${result.message}`));
    } else {
      console.log(chalk.yellow(`  ⚠️  ${result.name}: ${result.message}`));
    }
    results.push(result);
  }

  // 汇总
  console.log(chalk.gray('\n' + '='.repeat(50)));
  console.log(chalk.blue('\n📊 检查汇总:\n'));

  const passCount = results.filter(r => r.status === 'pass').length;
  const failCount = results.filter(r => r.status === 'fail').length;
  const warnCount = results.filter(r => r.status === 'warn').length;

  console.log(chalk.green(`  ✅ 通过: ${passCount}`));
  console.log(chalk.red(`  ❌ 失败: ${failCount}`));
  console.log(chalk.yellow(`  ⚠️  警告: ${warnCount}`));

  if (failCount === 0 && warnCount === 0) {
    console.log(chalk.green('\n🎉 Gateway 运行正常!\n'));
  } else if (failCount > 0) {
    console.log(chalk.red('\n⚠️  检测到问题，请运行 diagnose 命令进行详细诊断\n'));
  } else {
    console.log(chalk.yellow('\n⚠️  存在一些警告，建议运行 diagnose 命令\n'));
  }
}
