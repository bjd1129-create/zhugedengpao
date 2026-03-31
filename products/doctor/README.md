# 🦐 虾医 — OpenClaw 私人医生

> 让每个 OpenClaw 用户都能自主运维。

虾医是 OpenClaw 的诊断工具，能检查健康状态、分析问题根因、展示修复步骤。

---

## 安装

```bash
cd products/doctor
npm install
npm run build
```

链接为全局命令：

```bash
npm link
# 之后可直接用 xianxia-doctor 命令
```

---

## 命令

### check — 健康检查

```bash
xianxia-doctor check
```

检查项：
- Gateway 进程是否存活
- 端口 18790 是否监听
- Cron 任务数量和状态

输出示例（正常）：

```
🏥 虾医 — 健康检查
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Gateway 运行正常
   PID: 12345
   运行时间: 2h

ℹ️  发现 3 个 cron 任务
   🟡 1 个使用 webhook 推送

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

输出示例（异常）：

```
🏥 虾医 — 健康检查
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 Gateway 运行异常
   PID: 5290（进程可能已死）
   🟡 Gateway 进程存在但端口未监听（可能卡死）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### diagnose — 诊断问题

```bash
xianxia-doctor diagnose [小时]
```

分析最近 N 小时的错误日志，找出根因并给出修复建议。

参数：
- `小时` — 分析范围，默认 2 小时

输出示例：

```
🔍 分析最近 2 小时日志...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 发现 1 个问题：

[1/1] 🔴 严重 Gateway 健康检查失败
   频率：1次
   描述：Gateway 进程存在但端口未监听（可能卡死）

   🟡 可能原因：
     - 进程启动后卡死
     - 端口被占用
     - 配置文件损坏

   ℹ️  修复建议：
     - openclaw gateway restart
     - 检查端口占用：lsof -i :18790

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏱️  耗时：8.7秒
```

---

### fix — 修复问题

```bash
xianxia-doctor fix --task <任务ID> [--dry-run|--auto]
```

根据 diagnose 的结果展示或执行修复步骤。

模式：
- `--dry-run`（默认）：只展示步骤，不执行
- `--auto`：执行修复并验证

输出示例：

```
🔧 [DRY-RUN] 开始修复：Gateway 健康检查失败
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1/3] 👉 停止当前 Gateway 进程
   ℹ️  （dry-run）命令：launchctl bootout ...

[2/3] 👉 重新启动 Gateway 服务
   ℹ️  （dry-run）命令：openclaw gateway start

[3/3] ✅ 等待 Gateway 启动并验证

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 🎉 修复预览完成！共 3 步，耗时 0.0秒
🟡 ⚠️  这是 dry-run 模式，未执行任何操作
```

---

## 完整流程

```bash
# 1. 健康检查
xianxia-doctor check

# 2. 诊断问题（分析最近2小时）
xianxia-doctor diagnose

# 3. 预览修复步骤
xianxia-doctor fix --task gateway_health

# 4. 确认后执行修复
xianxia-doctor fix --task gateway_health --auto
```

---

## 工作原理

虾医通过读取 OpenClaw 的运行数据来诊断问题：

```
~/.openclaw/
├── logs/
│   ├── gateway.err.log    ← 错误日志
│   └── gateway.log        ← 运行日志
├── cron/
│   └── jobs.json          ← Cron 任务状态
└── config.yaml            ← 配置文件
```

诊断引擎会：
1. 读取错误日志，分类错误类型
2. 统计错误频率，识别异常模式
3. 匹配历史案例（case 库）
4. 给出有针对性的修复建议

---

## 项目结构

```
products/doctor/
├── src/
│   ├── index.ts              # CLI 入口
│   ├── commands/
│   │   ├── check.ts          # check 命令
│   │   ├── diagnose.ts       # diagnose 命令
│   │   └── fix.ts           # fix 命令
│   ├── core/
│   │   ├── researcher.ts     # 诊断引擎
│   │   └── fixer.ts         # 修复引擎
│   ├── openclaw/
│   │   ├── logs.ts           # 日志读取
│   │   ├── health.ts         # 健康检查
│   │   └── cron.ts           # Cron 状态
│   └── ui/
│       └── output.ts          # 彩色输出
├── data/cases/                # Case 库
└── tests/                     # 测试用例
```

---

## 测试

```bash
cd products/doctor
npm test
```

当前 18 个测试用例，覆盖：
- check 命令（4个）
- diagnose 命令（6个）
- fix --dry-run（5个）
- 集成测试（3个）

---

## 状态说明

| 标识 | 含义 |
|------|------|
| 🟢 | 正常 |
| 🟡 | 警告 |
| 🔴 | 严重 |
| ✅ | 成功 |
| ⚠️ | 提示/警告 |

---

最后更新：2026-03-31 | 虾医团队
