/**
 * diagnose 命令 — 研究问题
 */
import { research, printDiagnoseReport, DiagnoseResult } from '../core/researcher.js';
import { ui, printDiagnoseHeader } from '../ui/output.js';

export async function diagnoseCommand(timeframe = 2): Promise<DiagnoseResult> {
  printDiagnoseHeader(timeframe);

  const result = await research(timeframe);
  printDiagnoseReport(result);

  return result;
}
