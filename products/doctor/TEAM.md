# 虾医 团队规划

> 制定日期：2026-03-31 | 制定人：小花 | 状态：规划中

---

## 一、团队使命

**打造 虾医，让每个 OpenClaw 用户都能自主运维。**

---

## 二、团队架构（5人）

| 角色 | 代号 | 核心职责 |
|------|------|---------|
| 产品负责人 | Doctor-PM | 产品规划、需求优先级、技术决策、老庄需求对接 |
| 架构师 | Doctor-Architect | 技术方案设计、代码审查、最佳实践 |
| 开发工程师 | Doctor-Engineer | 核心代码开发（TypeScript/Node.js） |
| 测试工程师 | Doctor-Tester | 测试验证、bug追踪、用户验收 |
| 技术写作 | Doctor-Writer | 文档、README、用户手册、示例 |

---

## 三、团队协作流程

### 3.1 传达链
```
小花（总协调） → Doctor-PM → Doctor-Architect → 开发/测试/写作
```

### 3.2 开发流程（每两周一个冲刺）

```
Sprint 计划（周一）
    ↓
设计评审（周二）
    ↓
开发（周三-周五）
    ↓
测试验证（周六）
    ↓
发布 + 复盘（周日）
```

### 3.3 任务闭环标准

```
收到任务 → 立即记录到 memory/YYYY-MM-DD.md
执行 → 每完成一个功能更新 TODO.md
完成后 → 写复盘（what/wow/next）
```

---

## 四、各角色详细职责

### Doctor-PM（产品负责人）
- 理解老庄的真实需求，转化为产品功能
- 维护 SPEC.md，确保产品方向不偏离
- 优先级决策：什么先做，什么后做
- 里程碑制定：每个 Sprint 交付什么

### Doctor-Architect（架构师）
- 技术方案设计（听开发工程师的意见，但有最终决定权）
- 代码审查（每个 PR 必须经过 Architect 评审）
- 质量把控：代码风格、安全性、可维护性
- 解决技术争议

### Doctor-Engineer（开发工程师）
- 核心功能开发
- 遵守 Architect 制定的技术方案
- 写单元测试
- 修复 bug

### Doctor-Tester（测试工程师）
- 编写测试用例
- 执行功能测试
- 记录 bug 并跟踪修复
- 用户验收测试（老庄视角）

### Doctor-Writer（技术写作）
- README.md（安装、使用、常见问题）
- API 文档
- 用户手册
- 示例和教程

---

## 五、第一个 Sprint 目标（1-2周）

**目标**：MVP — 健康检查 + Cron 400 诊断

| 任务 | 负责人 | 状态 |
|------|--------|------|
| 项目结构搭建 | Doctor-Engineer | 待开始 |
| check 命令实现 | Doctor-Engineer | 待开始 |
| diagnose 命令实现 | Doctor-Engineer | 待开始 |
| fix --dry-run 实现 | Doctor-Engineer | 待开始 |
| 单元测试 | Doctor-Tester | 待开始 |
| README 草稿 | Doctor-Writer | 待开始 |
| 用户验收（老庄） | Doctor-PM | 待开始 |

---

## 六、验收标准

**MVP 交付条件：**
1. `虾医 check` 能检测 Gateway 存活状态
2. `虾医 diagnose` 能分析 Cron 400 错误并给出修复建议
3. `虾医 fix --dry-run` 能展示修复步骤
4. 修复过程透明可见（不是黑箱）
5. README 完整可用

---

## 七、团队规则

1. **每个角色只做自己的事**：不越界
2. **遇到阻塞立即上报**：不要等
3. **每周复盘一次**：周日 18:00 前各角色更新 memory
4. **重大决策经过团队讨论**：不要一个人拍板

---

## 八、工作空间

各角色在以下目录工作：
- Doctor-PM：products/doctor/
- Doctor-Architect：products/doctor/
- Doctor-Engineer：products/doctor/
- Doctor-Tester：products/doctor/tests/
- Doctor-Writer：products/doctor/docs/

---

最后更新：2026-03-31 | 小花
