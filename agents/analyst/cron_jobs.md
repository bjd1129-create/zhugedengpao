# 数据分析师定时任务配置

## 数据更新任务（每 5 分钟）

```bash
# 编辑 crontab
crontab -e

# 添加以下任务（每 5 分钟执行一次）
*/5 * * * * cd /Users/bjd/Desktop/ZhugeDengpao-Team/agents/analyst && /Users/bjd/.venv/tiger/bin/python fetch_futures.py >> /tmp/analyst_fetch.log 2>&1

# 每分钟扫描信号
* * * * * cd /Users/bjd/Desktop/ZhugeDengpao-Team/agents/analyst && /Users/bjd/.venv/tiger/bin/python scan_signals.py >> /tmp/analyst_signals.log 2>&1
```

## 报告生成任务

```bash
# 每日 09:00 生成日报
0 9 * * * cd /Users/bjd/Desktop/ZhugeDengpao-Team/agents/analyst && /Users/bjd/.venv/tiger/bin/python generate_report.py daily >> /tmp/analyst_report.log 2>&1

# 每周日 20:00 生成周报
0 20 * * 0 cd /Users/bjd/Desktop/ZhugeDengpao-Team/agents/analyst && /Users/bjd/.venv/tiger/bin/python generate_report.py weekly >> /tmp/analyst_report.log 2>&1
```

## 日志查看

```bash
# 查看实时日志
tail -f /tmp/analyst_fetch.log
tail -f /tmp/analyst_signals.log

# 查看最近的错误
grep ERROR /tmp/analyst_fetch.log | tail -20
```

## 任务管理

```bash
# 查看当前 crontab
crontab -l

# 暂停任务（注释掉）
crontab -e

# 删除所有任务
crontab -r

# 恢复任务
crontab /path/to/cron_backup.txt
```

---

## OpenClaw Cron 配置（推荐）

使用 OpenClaw 的 cron 系统管理定时任务：

```json
{
  "name": "期货数据更新",
  "schedule": {
    "kind": "every",
    "everyMs": 300000
  },
  "payload": {
    "kind": "systemEvent",
    "text": "reminder: 期货数据更新任务 - 请执行 fetch_futures.py 抓取最新数据"
  },
  "sessionTarget": "main"
}
```

---

_数据分析师 | 2026-04-08_
