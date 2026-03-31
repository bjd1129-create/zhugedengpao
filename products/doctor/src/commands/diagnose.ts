/**
 * diagnose 命令 — 研究问题
 */
import { research, printDiagnoseReport, DiagnoseResult } from '../core/researcher.js';
import { ui, printDiagnoseHeader } from '../ui/output.js';
import { printDiagnosisStart, printDiagnosisEnd } from '../core/emotion.js';

export async function diagnoseCommand(timeframe = 2): Promise<DiagnoseResult> {
  printDiagnosisStart(timeframe);

  const result = await research(timeframe);
  printDiagnoseReport(result);
  printDiagnosisEnd(result.problems.length);

  return result;
}
