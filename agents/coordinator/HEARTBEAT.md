# HEARTBEAT.md - 协调官

## 每次心跳（每30分钟，必须执行）

### 1. Git巡检
```
cd /Users/bjd/Desktop/ZhugeDengpao-Team && git status --short
```
- 有未push的commit → 立即push
- 有冲突/问题 → 立即处理

### 2. 团队状态读取
- 配色师：读 `agents/designer/PROGRESS.md`
- 文案君：读 `agents/writer/TASK-COORDINATOR.md`
- 洞察者：读 `agents/researcher/memory/YYYY-MM-DD.md`
- 代码侠：读 `agents/engineer/memory/YYYY-MM-DD.md`

### 3. 问题处理
- 发现阻塞 → 我解决（2小时窗口）
- 重大问题 → sessions_send 报小花
- 正常推进 → 不打扰

### 4. 巡检记录
每次心跳执行后，在 `memory/YYYY-MM-DD.md` 记录：
```
[HH:MM] 心跳巡检 - 配色师:OK 文案君:OK 洞察者:OK 代码侠:OK Git:OK
```

---

## 每日节奏

| 时间 | 任务 |
|------|------|
| 每30分钟 | 心跳巡检（Git + 各agent状态） |
| 每天 08:00 | 日报生成，读各agent昨日总结 |
| 每天 20:00 | 晚间巡检，发日报给小花 |

---

## 执行规则

1. **心跳超时=失职** — 没执行巡检就是没完成任务
2. **不push=没完成** — 积压commit等同于任务积压
3. **阻塞2小时上报** — 超过2小时无法解决才上报

