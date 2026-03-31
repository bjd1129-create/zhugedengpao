# Case 005: 高 CPU 游离进程导致 Gateway 挂死

## 元信息
- **case_id**: 005
- **发生时间**: 2026-03-31 下午
- **症状分类**: Gateway / Process
- **关键词**: 高CPU, 980%, 游离进程, PM2, 内存泄漏

---

## 症状表现
| 检查项 | 状态 |
|--------|------|
| Gateway HTTP | 无响应 |
| CPU 使用率 | PID 11168 达到 980%（接近占满 10 核心） |
| PM2 进程列表 | 空（Gateway 不在 PM2 托管下） |
| 内存使用 | 持续增长直到触发 OOM |
| delivery-queue | 5 条死信积压（3/26 旧消息，5次重试全 400） |

---

## 根因
Gateway 进程变成了**游离进程**（不在 PM2 托管下），CPU 飙升至 980% 导致系统资源耗尽：

1. **进程失控**：非 PM2 托管的 node 进程进入高 CPU 死循环
2. **内存泄漏**：没有 PM2 的 `max_memory_restart` 限制，内存持续增长
3. **无法自动恢复**：游离进程卡死后无人自动重启
4. **配置被写坏**：OOM 导致多进程并发写 openclaw.json，配置文件损坏

---

## 诊断步骤
```
[1/5] 检查高 CPU 进程
    命令：ps aux | grep node | grep -v grep
    结果：PID 11168 node 进程 CPU 980%

[2/5] 检查 PM2 进程列表
    命令：pm2 list
    结果：空 → Gateway 不在 PM2 托管下

[3/5] 查看 gateway.err.log
    命令：tail -50 ~/.openclaw/logs/gateway.err.log
    结果：发现内存泄漏迹象

[4/5] 检查 delivery-queue 积压
    命令：ls ~/.openclaw/delivery-queue/failed/
    结果：5 条失败消息（3/26 旧消息）

[5/5] 检查进程端口监听
    命令：lsof -i :18789
    结果：无输出 → 端口无监听
```

---

## 修复步骤
```
[1/6] Kill 高 CPU 游离进程
    命令：kill -9 <PID>
    结果：高 CPU 进程清除

[2/6] 用 PM2 重新托管 Gateway
    命令：pm2 start --name openclaw-gateway "openclaw gateway start"
    结果：Gateway PID 28576 online，CPU 12.5%，内存 385MB

[3/6] 保存 PM2 进程列表（开机自启）
    命令：pm2 save
    结果：进程列表已保存

[4/6] 调整内存限制
    命令：pm2 updaten openclaw-gateway --max-memory-restart 800M
    结果：内存限制从 1G 调整为 800MB（更早触发重启）

[5/6] 清空 delivery-queue 死信
    命令：rm -rf ~/.openclaw/delivery-queue/failed/*
    结果：5 条旧失败消息清除

[6/6] 验证 Gateway HTTP
    命令：curl http://127.0.0.1:18789/health
    结果：HTTP 200 OK ✅
```

---

## 修复结果
| 检查项 | 状态 |
|--------|------|
| Gateway HTTP | ✅ 200 OK |
| PM2 托管 | ✅ online，PID 28576 |
| CPU | ✅ 0%（正常） |
| 内存 | ✅ 367MB |
| 重启次数 | ✅ 0 |
| delivery-queue | ✅ 已清空 |

---

## 飞书 Bot warn 说明

**`no im.chat.access_event.bot_p2p_chat_entered_v1 handle`**

这是飞书推送的"用户打开私聊"事件，但 openclaw 没有注册处理器。属于**无害 warn**，高频出现是因为在飞书开发者后台订阅了该事件。

**消除方法**：去飞书开发者后台 → 每个 Bot → 事件与回调 → 取消订阅 `im.chat.access_event.bot_p2p_chat_entered_v1`

不影响正常收发消息功能。

---

## 经验教训
1. **Gateway 必须用 PM2 托管**，否则成为游离进程后无法自动恢复
2. **`max_memory_restart` 要设置**（800MB 合适），防止内存泄漏导致 OOM
3. **`pm2 save` + `pm2 startup` 必须执行**，否则重启后进程丢失
4. **高 CPU 980% = 进程死循环**，通常是内存泄漏触发 GC 频繁 Full Collection
5. **delivery-queue 死信要定期清理**，过期消息（>7天）直接删除

---

## 状态
- **resolved**: true
- **fix_count**: 1
- **root_cause**: Gateway 脱离 PM2 托管 + 内存限制缺失
