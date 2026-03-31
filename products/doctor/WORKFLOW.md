# 虾医（全自动开发工作流）

**版本：** 1.0
**日期：** 2026-03-31
**目标：** 虾医项目24小时永不停息地自主开发

---

## 核心理念

虾医是小花的第一个亲生项目。
它是一个工具，先解决自己的问题，再考虑给别人用。
不是"功能齐全"，是"真正能用"。

---

## 团队分工

| 角色 | 职责 | 每天产出 |
|------|------|---------|
| **doctor-pm** | 产品管理 + 统筹 | Sprint计划 + 任务派发 |
| **doctor-architect** | 架构设计 + 技术方案 | 架构决策 + 代码审查 |
| **doctor-engineer** | 核心代码开发 | check/diagnose/fix模块 |
| **doctor-tester** | 测试 + 验收 | 测试用例 + 验证报告 |
| **doctor-writer** | 文档 + 说明 | README + 使用文档 |

---

## Sprint 周期

**两周一个Sprint：**
- 周一：Sprint规划
- 周二-周五：开发
- 周六-周日：测试 + 回顾
- 周日20:00：Sprint复盘

---

## 每日自动化流程

### 早上（9:00）— Sprint启动检查
doctor-pm检查：
1. 昨天完成了什么？
2. 今天要完成什么？
3. 有没有阻塞？

### 上午（9:00-12:00）
- **doctor-engineer**：写代码
- **doctor-architect**：支持技术问题
- **doctor-pm**：派发新任务

### 中午（12:00）— 站会
doctor-pm汇报进度，小花监督。

### 下午（14:00-18:00）
- **doctor-engineer**：继续开发
- **doctor-tester**：准备测试用例
- **doctor-writer**：写文档

### 傍晚（18:00）— 整理
各Agent写memory，总结今天产出。

### 晚间（21:00）— 进展汇报
小花向老庄汇报有价值的分析。

---

## 核心开发循环

```
每次检查：
    ↓
doctor-pm 派任务给 engineer
    ↓
engineer 写代码
    ↓
architect 代码审查
    ↓
tester 验证功能
    ↓
通过 → 下一个任务
失败 → 反馈 → engineer 修复
    ↓
循环（永不停息）
```

---

## 功能优先级

**Sprint 1（MVP）：**
1. **check** — OpenClaw健康检查
2. **diagnose** — 错误分析
3. **fix --dry-run** — 模拟修复

**Sprint 2：**
1. **fix --auto** — 低风险自动修复
2. 18个测试用例通过

**Sprint 3+：**
1. 自我进化（记忆错误模式）
2. 预防性修复

---

## 技术规范

### check模块
- 检查日志文件（gateway.err.log / gateway.log）
- 检查配置文件（openclaw.json）
- 检查Cron状态
- 检查连接状态

### diagnose模块
- 分析错误模式（9种已知模式）
- 定位根因
- 输出诊断报告

### fix模块
- 低风险：读日志、改配置、清理缓存
- 中风险：重启服务、重置连接
- 高风险：只给建议，不自动执行

---

## 测试用例（18个）

从真实错误日志提取：
1. plugins-invalid
2. sessions-lock-contention
3. doctor-restart
4. sessions-send-double-auth
5. high-cpu-runaway-process
6. nextjs-runaway-process
7. close-wait-connection-leak
8. agent-heartbeat-disabled
9. workspace-switch-crash
10. config-path-backslash
11. gateway-config-path-missing
12. （还有更多...）

每个用例必须通过才算功能完成。

---

## Cron 任务清单

| Cron | 频率 | 职责 |
|------|------|------|
| 虾医全自动开发 | 每4小时 | doctor-pm持续派任务给engineer |
| 虾医每日站会 | 每4小时 | Sprint进度/测试/阻塞 |
| Sprint每周复盘 | 每7天 | 完成度/改进/下周计划 |
| 小花主动管理 | 每2小时 | 两个团队主动管理 |

---

## 汇报规范

**不写废话。汇报格式：**

- 今天最大的进展是什么？
- 今天最大的问题是什么？
- 我的判断：我们走得对不对？
- 明天最重要的1件事是什么？

---

## 质量标准

- 每个功能必须通过测试用例才算完成
- 代码必须有注释
- 每次commit必须附带说明
- README必须及时更新

---

最后更新：2026-03-31 | 小花 🦞
