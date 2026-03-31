## OpenClaw Doctor 开发任务

### 第一个 Milestone（3天内完成）

**目标**：MVP 版本，能诊断 Cron 400 错误

**步骤：**

1. 创建项目结构
```
products/doctor/
├── src/
│   ├── index.ts          # 入口
│   ├── commands/          # CLI 命令
│   ├── diagnostics/       # 诊断引擎
│   │   ├── log-parser.ts
│   │   └── error-classifier.ts
│   ├── health/           # 健康检查
│   └── ui/               # TUI
├── tests/
├── package.json
└── tsconfig.json
```

2. 实现 `check` 命令（健康检查）
   - 检测 Gateway 进程是否存在
   - 检测网络连通性
   - 读取最近日志

3. 实现 `diagnose` 命令（日志诊断）
   - 解析 OpenClaw 日志
   - 识别 Cron 400 错误
   - 给出原因 + 修复建议

4. 实现 `fix --dry-run` 命令（修复预览）
   - 展示修复步骤
   - 不实际执行

5. 部署到本地测试
   - 在老庄的 OpenClaw 上跑通

**交付物**：可运行的 `openclaw-doctor` 命令

**参考**：SPEC.md 在 products/doctor/SPEC.md
