# AI 深度日报流程文档

## 📋 概述

自动化生成 AI 领域深度研究报告，每天 08:00 自动抓取 5 个固定信息源的最新内容，生成 Markdown 格式报告并发送到飞书。

---

## 🎯 信息源

| 序号 | 信息源 | 类型 | 更新频率 |
|------|--------|------|----------|
| 1 | Anthropic 官方博客 | RSS | 不定期 |
| 2 | OpenClaw GitHub | GitHub API | 实时 |
| 3 | Hacker News AI 板块 | HN API | 实时 |
| 4 | Simon Willison 博客 | RSS | 每周 |
| 5 | ArXiv AI 论文 | RSS | 每日 |

---

## 📁 文件结构

```
agents/analyst/
├── scripts/
│   ├── ai_daily_report.py    # 主脚本
│   └── requirements.txt      # Python 依赖
├── reports/
│   └── ai-daily-YYYY-MM-DD.md  # 每日报告
├── report_template.md        # 报告模板
└── AI-DAILY-REPORT-FLOW.md   # 本文档
```

---

## ⚙️ 配置步骤

### 1. 安装依赖

```bash
cd /Users/bjd/Desktop/ZhugeDengpao-Team/agents/analyst/scripts
pip3 install -r requirements.txt
```

### 2. 配置飞书 Webhook（可选）

在飞书群聊中创建机器人，获取 Webhook URL：

```bash
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
```

或添加到 `.env` 文件。

### 3. 测试运行

```bash
python3 ai_daily_report.py
```

检查输出：
- 报告是否生成在 `reports/` 目录
- 飞书是否收到通知（如配置）

### 4. 验证 Cron 任务

```bash
crontab -l
```

应看到：
```
0 8 * * * /tmp/ai_daily_cron.sh
```

---

## 📊 报告结构

```markdown
# AI 深度日报 {date}

## 📊 今日概览
（一句话总结）

## 🔍 信息源详情
（5 个来源的详细内容）
- 来源链接
- 核心内容摘要（200-300 字）
- 关键洞察
- 对小花团队的意义/应用建议

## 🎯 今日 Top 3 关键发现

## 📋 行动清单
```

---

## 🔄 运行流程

```
每天 08:00
    ↓
Cron 触发 /tmp/ai_daily_cron.sh
    ↓
执行 ai_daily_report.py
    ↓
抓取 5 个信息源
    ↓
生成 Markdown 报告
    ↓
保存到 reports/ai-daily-YYYY-MM-DD.md
    ↓
发送飞书通知（如配置）
    ↓
完成
```

---

## 🛠️ 手动操作

### 生成今日报告

```bash
python3 /Users/bjd/Desktop/ZhugeDengpao-Team/agents/analyst/scripts/ai_daily_report.py
```

### 查看历史报告

```bash
ls -la /Users/bjd/Desktop/ZhugeDengpao-Team/agents/analyst/reports/
```

### 查看运行日志

```bash
tail -f /tmp/ai_daily_report.log
```

---

## 🚨 故障排查

### 问题 1：报告未生成

**检查**：
```bash
# 查看日志
cat /tmp/ai_daily_report.log

# 手动运行测试
python3 ai_daily_report.py
```

### 问题 2：飞书未收到通知

**检查**：
- Webhook URL 是否正确配置
- 网络连接是否正常
- 查看脚本输出日志

### 问题 3：Cron 未执行

**检查**：
```bash
# 查看 cron 日志
grep CRON /var/log/system.log

# 验证 cron 任务
crontab -l
```

---

## 📈 优化建议

### 短期优化
- [ ] 接入 AI 自动生成摘要和洞察
- [ ] 增加更多信息来源（DeepMind/OpenAI 等）
- [ ] 添加报告质量检查

### 长期优化
- [ ] 支持周报/月报汇总
- [ ] 添加趋势分析和对比
- [ ] 集成到小花团队工作流
- [ ] 支持自定义信息源配置

---

## 🔐 安全注意事项

- 不要将 Webhook URL 提交到 Git
- 定期检查和轮换 API Key
- 监控脚本运行日志
- 限制脚本文件权限

---

## 📞 维护联系人

- 负责人：小花团队 AI 分析师
- 文档位置：`agents/analyst/AI-DAILY-REPORT-FLOW.md`
- 脚本位置：`agents/analyst/scripts/ai_daily_report.py`

---

_最后更新：2026-04-08_
_小花团队 🦞_
