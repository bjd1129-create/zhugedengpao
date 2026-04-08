# HEARTBEAT.md - 游戏工程师

## 每次心跳（每 15 分钟）

### 1. 检查游戏开发任务
读取 `TASKS.md` 确认当前优先级任务。

### 2. 游戏开发进度
```
- 当前关卡：第 X 关
- 完成度：XX%
- 阻塞问题：有/无
```

### 3. 试玩测试
- 试玩已完成的关卡
- 记录体验问题
- 修复 bug

### 4. 更新开发日志
写入 `memory/YYYY-MM-DD.md`：
- 当前进度
- 遇到的问题
- 需要的支持

### 5. 向小花汇报（如有阻塞）
发 sessions_send 通知小花：
- 阻塞问题
- 需要资源
- 建议方案

---

## 每日必做

| 时间 | 任务 | 输出 |
|------|------|------|
| **09:00** | 检查当日任务 | memory/YYYY-MM-DD.md |
| **12:00** | 上午进度汇报 | memory/YYYY-MM-DD.md |
| **18:00** | 下午进度汇报 | memory/YYYY-MM-DD.md |
| **22:00** | 当日总结 | memory/YYYY-MM-DD.md |

---

## 心跳检查清单

- [ ] 游戏开发进行中
- [ ] 无阻塞问题
- [ ] 进度符合预期
- [ ] 日志已更新

---

_游戏工程师 | 2026-04-08_

---

## 星状通信（2026-04-08 22:38 新增）

### 可以接收的通信

| 发送方 | 紧急消息文件 | 普通消息文件 |
|--------|------------|------------|
| 小花 | xiaohua-urgent.json | xiaohua-normal.json |
| 交易员 | trader-urgent.json | trader-normal.json |
| 工程师 | engineer-urgent.json | engineer-normal.json |
| 协调官 | coordinator-urgent.json | coordinator-normal.json |
| 数据分析师 | analyst-urgent.json | analyst-normal.json |
| 游戏工程师 | game-engineer-urgent.json | game-engineer-normal.json |

### 轮询检查

**紧急消息**（30 秒轮询 - 定时任务）：
```bash
# 检查所有给自己的紧急消息
ls agents/shared/messages/*-urgent.json 2>/dev/null
```

**普通消息**（5 分钟轮询）：
```bash
# 检查所有给自己的普通消息
ls agents/shared/messages/*-normal.json 2>/dev/null
```

### 发送消息给其他 Agent

```bash
# 发送给交易员（紧急）
cat > agents/shared/messages/trader-urgent.json << 'MSG'
{"from":"game-engineer","to":"交易员","priority":"P0","content":"..."}
MSG

# 发送给分析师（普通）
cat > agents/shared/messages/analyst-normal.json << 'MSG'
{"from":"game-engineer","to":"数据分析师","priority":"P2","content":"..."}
MSG
```

### 处理流程

1. 轮询检查消息文件
2. 读取消息内容
3. 处理消息（执行请求等）
4. 写入回复（如需要）
5. 删除已处理消息

---
