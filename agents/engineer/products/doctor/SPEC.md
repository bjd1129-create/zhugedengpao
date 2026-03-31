# OpenClaw Doctor - 产品规格

## 概述

OpenClaw Doctor 是一个命令行诊断工具，用于检测和修复 OpenClaw Gateway 的常见问题。

## 核心功能

### 1. check 命令
检测 Gateway 进程状态和网络连通性

**检查项：**
- Gateway 进程是否存在
- Gateway 端口是否监听
- Gateway API 端点是否可达
- 网络连通性测试

**输出：**
- ✅ 绿色表示正常
- ❌ 红色表示异常
- 详细的诊断信息

### 2. diagnose 命令
解析日志文件，识别 Cron 400 错误

**诊断项：**
- 读取最近的日志文件
- 识别 HTTP 400 错误
- 分析错误原因（认证失败、请求格式错误等）
- 提供错误摘要

### 3. fix --dry-run 命令
展示修复步骤，不实际执行

**功能：**
- 分析检测到的问题
- 生成修复建议
- 使用 `--dry-run` 参数时只展示不执行
- 修复步骤透明可见

## 技术栈

- TypeScript + Node.js
- chalk - 终端UI着色
- fs-extra - 文件操作
- node-fetch - HTTP请求

## 项目结构

```
products/doctor/
├── src/
│   ├── commands/
│   │   ├── check.ts
│   │   ├── diagnose.ts
│   │   └── fix.ts
│   ├── utils/
│   │   ├── gateway.ts      # Gateway 进程检测
│   │   ├── network.ts      # 网络连通性检测
│   │   └── logger.ts       # 日志解析
│   ├── types/
│   │   └── index.ts        # 类型定义
│   └── index.ts
├── package.json
├── tsconfig.json
└── SPEC.md
```

## 验收标准

1. ✅ `openclaw-doctor check` 能显示 Gateway 健康状态
2. ✅ `openclaw-doctor diagnose` 能分析最近的 Cron 400 错误
3. ✅ 修复过程透明可见

## 进度状态 (2026-03-31)

### 已完成
- [x] 项目结构创建 (TypeScript + Node.js)
- [x] `check` 命令 - 检测 Gateway 进程 + 网络连通性
- [x] `diagnose` 命令 - 解析日志，识别 Cron 400 错误
- [x] `fix --dry-run` - 展示修复步骤，不实际执行

### 测试结果
```
# check 命令
- 检测到 Gateway 进程运行中 (PID: 40996)
- 检测到端口 18789 未监听
- 检测到 API 端点不可达

# diagnose 命令
- 成功读取 ~/.openclaw/logs/
- 发现 20 个 Cron HTTP 400 错误
- 错误分析准确，修复建议合理

# fix --dry-run 命令
- 正确展示诊断结果
- 修复步骤清晰可见
- 预览模式正常工作
```

## 使用方式

```bash
# 检查 Gateway 状态
openclaw-doctor check

# 诊断问题
openclaw-doctor diagnose

# 预览修复步骤
openclaw-doctor fix --dry-run

# 执行修复
openclaw-doctor fix
```
