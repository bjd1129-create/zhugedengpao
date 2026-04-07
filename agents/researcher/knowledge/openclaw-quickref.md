# OpenClaw 速查卡

> 洞察者整理 · 2026-04-06 · 日常维修必备

---

## 🔴 紧急修复

### Gateway 无响应
```bash
openclaw gateway restart
# 或前台运行看日志
openclaw gateway --port 18789 --verbose
```

### 频道断开（logged out / 409-515）
```bash
openclaw channels logout
openclaw channels login --verbose
```

### 配置损坏
```bash
openclaw doctor --repair
openclaw doctor --repair --force  # 激进修复
```

---

## 🟡 日常检查

### 健康状态
```bash
openclaw status --deep
openclaw health --verbose
```

### Session 状态
```bash
openclaw sessions --json
openclaw sessions cleanup --dry-run
```

### Cron 任务
```bash
openclaw cron list
openclaw cron runs --id <job-id>
```

### 频道状态
```bash
openclaw channels status --probe
```

---

## 🟢 常用操作

### 安装技能
```bash
npx clawhub@latest install <skill-name>
```

### 添加定时提醒
```bash
openclaw cron add \
  --name "Reminder" \
  --at "20m" \
  --session main \
  --system-event "提醒内容" \
  --delete-after-run
```

### 发送消息
```bash
openclaw message send --to +1234567890 --message "Hello"
```

### 切换模型
```
/new <model-name>
# 或
/model <model-name>
```

---

## 📁 关键路径

```
~/.openclaw/openclaw.json          # 主配置
~/.openclaw/workspace/             # 主 Workspace
~/.openclaw/agents/main/agent/     # Agent 状态
~/.openclaw/agents/main/sessions/  # Sessions
~/.openclaw/credentials/          # 渠道凭据
~/.openclaw/cron/jobs.json         # Cron 任务
~/.openclaw/skills/                # 管理技能
```

---

## 🔧 常见配置

### DM 隔离（多人使用必设）
```json5
{ session: { dmScope: "per-channel-peer" } }
```

### Telegram 配置
```json5
{
  channels: {
    telegram: {
      botToken: "xxx",
      dmPolicy: "pairing"
    }
  }
}
```

### Discord 配置
```json5
{
  channels: {
    discord: {
      token: "xxx",
      dmPolicy: "pairing"
    }
  }
}
```

---

## 🐛 错误代码

| 代码 | 含义 | 处理 |
|------|------|------|
| 409 | 设备未配对 | 重新配对 |
| 515 | WhatsApp 需要重新链接 | channels logout && login |
| 连接拒绝 | Gateway 未运行 | openclaw gateway start |

---

## 📚 文档入口

- 完整文档：https://docs.openclaw.ai
- 完整索引：https://docs.openclaw.ai/llms.txt
- 本地知识库：knowledge/openclaw-knowledge-base.md

---

*洞察者 · 速查卡 v1.0*
