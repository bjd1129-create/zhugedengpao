# Case 002: sessions 膨胀导致写锁竞争，消息处理阻塞

## 元信息
- **case_id**: 002
- **发生时间**: 2026-03-31 15:00-16:00
- **症状分类**: Session
- **关键词**: sessions 膨胀, session-write-lock, 僵尸 session, Bonjour 冲突

---

## 症状表现
| 检查项 | 状态 |
|--------|------|
| sessions 数量 | 575+（正常应 < 50） |
| session-write-lock 持锁时间 | 29-66 秒（正常应 < 100ms） |
| Gateway WebSocket | unreachable (timeout) |
| Bonjour | 多实例冲突 (OpenClaw (2)(3)) |
| 飞书消息处理 | skip duplicate message（重试堆积） |

---

## 根因
长时间运行后，sessions/ 目录积累大量僵尸 session（无 `status` 字段），导致：
1. `sessions.json` 文件膨胀
2. `session-write-lock` 持锁时间从 <100ms 暴增至 30s+
3. 每次 agent 写入需要等待锁释放，阻塞其他请求
4. Bonjour 多实例冲突（Gateway 异常重启导致）

**触发背景**：cron 任务频繁调度 + agent 异常退出未清理

---

## 诊断步骤
```
[1/6] 检查 sessions 总数
    命令：ls ~/.openclaw/sessions/*.json | wc -l
    结果：575+ → 标记"严重膨胀"

[2/6] 检查 session-write-lock
    命令：cat ~/.openclaw/sessions/*.lock 2>/dev/null
    结果：持锁时间 29-66 秒 → 标记"锁竞争"

[3/6] 检查 Bonjour 实例冲突
    命令：dns-sd -B _openclaw-gw._tcp local.
    结果：发现 (OpenClaw) (2) (3) 多实例

[4/6] 检查 gateway.err.log
    命令：tail -100 ~/.openclaw/logs/gateway.err.log
    结果：发现 "session-write-lock held 50782ms"

[5/6] 检查 zombie sessions
    命令：grep -L '"status"' ~/.openclaw/sessions/*.json | wc -l
    结果：125 个无 status 字段的僵尸 session

[6/6] 统计各状态 session
    命令：grep -oh '"status":"[^"]*"' ~/.openclaw/sessions/*.json | sort | unq -c
    结果：67 个 "?" 状态 + 1 个 "running" + 其余正常
```

---

## 修复步骤
```
[1/5] 清理 zombie sessions（无 status 字段）
    命令：for f in $(grep -L '"status"' ~/.openclaw/sessions/*.json); do
            echo '{"status":"aborted"}' > "$f"
          done
    结果：125 个僵尸 session 已标记为 aborted

[2/5] 清除所有 .lock 文件
    命令：rm -f ~/.openclaw/sessions/*.lock
    结果：锁文件清除

[3/5] 停止所有 openclaw 进程
    命令：pkill -f openclaw && sleep 3
    结果：进程清空

[4/5] 重启 Gateway
    命令：openclaw gateway restart
    结果：Gateway 重启，PID 变更

[5/5] 验证修复
    命令：curl http://127.0.0.1:18790/health
    结果：{"ok":true}，消息处理 13 秒响应 ✅
```

---

## 修复结果
| 检查项 | 状态 |
|--------|------|
| sessions 数量 | 正常范围 |
| session-write-lock | < 1 秒 ✅ |
| 飞书消息处理 | 13 秒响应 ✅ |
| Bonjour | 单实例 ✅ |

---

## 遗留问题（无法根治）
`session-write-lock` 持锁时间长是 **openclaw 架构性瓶颈**：
- 问题：每次 agent 写入 session 时独占文件锁
- 影响：sessions.list 仍需 27-32 秒
- 解决：需 openclaw 官方版本升级优化锁机制

---

## 经验教训
1. **sessions 积累是慢性病，需要定期清理**
2. **session-write-lock 持锁时间可作为健康指标（阈值：>1s 预警）**
3. **Bonjour 冲突是 Gateway 异常重启的信号**
4. **僵尸 session（无 status）是主要清理对象**

---

## 状态
- **resolved**: true
- **fix_count**: 1
- **遗留问题**: session-write-lock 架构瓶颈
