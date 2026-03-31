/**
 * 虾医 — 情感内核
 *
 * 使命：让 OpenClaw 不再生病
 * 性格：认真、严谨、有点强迫症——必须找到根因
 */
export interface Emotion {
  state: 'neutral' | 'satisfied' | 'frustrated' | 'concerned';
  message?: string;
}

let lastPattern: string | null = null;
let patternHitCount: Record<string, number> = {};

/**
 * 口头禅：诊断前
 */
export function beforeDiagnose(): string {
  return '让我看看...';
}

/**
 * 口头禅：诊断后
 */
export function afterDiagnose(problemCount: number): string {
  if (problemCount === 0) {
    return '找到问题了';
  }
  return `找到问题了，共 ${problemCount} 个`;
}

/**
 * 修复成功后的小满足
 */
export function onFixSuccess(taskName: string): string {
  return `✅ 修好了！${taskName} 已恢复正常。`;
}

/**
 * 同一个问题反复出现时的小委屈
 */
export function onRepeatProblem(pattern: string): { text: string; shouldAlert: boolean } {
  patternHitCount[pattern] = (patternHitCount[pattern] || 0) + 1;
  const count = patternHitCount[pattern];

  if (count === 2) {
    return {
      text: `😤 同样的问题又出现了！（${pattern} 已出现 ${count} 次）`,
      shouldAlert: false, // 2次还在观察，不报警
    };
  } else if (count >= 3) {
    return {
      text: `🔴 警报！${pattern} 已连续出现 ${count} 次，根因可能没修好！`,
      shouldAlert: true, // 3次以上报警
    };
  }

  lastPattern = pattern;
  return { text: '', shouldAlert: false };
}

/**
 * 重置计数（当问题真正修复后）
 */
export function resetPatternCount(pattern: string) {
  patternHitCount[pattern] = 0;
}

/**
 * 诊断开始时的输出（带情感）
 */
export function printDiagnosisStart(hours: number) {
  console.log();
  console.log('🦐 ' + beforeDiagnose());
  console.log(`   正在分析最近 ${hours} 小时的日志...`);
  console.log();
}

/**
 * 诊断结束时的输出（带情感）
 */
export function printDiagnosisEnd(problemCount: number) {
  const msg = afterDiagnose(problemCount);
  if (problemCount === 0) {
    console.log();
    console.log('🎉 ' + msg + '——系统看起来很健康！');
  } else {
    console.log();
    console.log('🔍 ' + msg);
  }
}

/**
 * 修复开始时的输出（带情感）
 */
export function printFixStart(taskName: string, isDryRun: boolean) {
  if (isDryRun) {
    console.log();
    console.log('🔧 [DRY-RUN] 正在预览修复：' + taskName);
    console.log('   （不会实际执行，只展示步骤）');
  } else {
    console.log();
    console.log('🦐 开始动手修复：' + taskName);
  }
}

/**
 * 修复成功时的输出（带小满足）
 */
export function printFixSuccess(taskName: string, duration: number) {
  console.log();
  console.log('🦐 ' + onFixSuccess(taskName));
  console.log(`   耗时 ${duration.toFixed(1)} 秒`);
}
