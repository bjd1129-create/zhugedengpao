# Case 003: openclaw doctor 触发 Gateway 重启，误判为崩溃

## 元信息
- **case_id**: 003
- **发生时间**: 2026-03-31 15:45
- **症状分类**: Gateway
- **关键词**: doctor, restart, 1006, WebSocket 断连

---

## 症状表现
| 检查项 | 之前 | 之后 |
|--------|------|------|
| Gateway WebSocket | reachable 66ms | unreachable (gateway closed (1006)) |
| Gateway PID | 7931 | 11128（换了新进程） |
| Gateway 进程 | 正常 | 正常（只是换了 PID） |
| Sessions | 453 | 453（未变） |

---

## 根因
`openclaw doctor` 命令在诊断过程中会重启 Gateway 服务：
1. doctor 检测 Gateway 状态
2. 触发 Gateway 服务重启（PID 7931 → 11128）
3. 重启期间 WebSocket 连接断开，openclaw status 捕获到 1006（异常关闭）
4. 新进程就绪后自动恢复 reachable

**这是正常行为，不是故障。**

---

## 诊断步骤
```
[1/3] 检查 Gateway 进程是否存活
    命令：ps aux | grep openclaw | grep -v grep
    结果：pid 11128 running ✅

[2/3] 尝试 HTTP 请求
    命令：curl http://127.0.0.1:18790/health
    结果：{"ok":true,"status":"live"} ✅

[3/3] 对比 PID 是否变化
    命令：openclaw status
    结果：Gateway PID 从 7931 变为 11128
    结论：doctor 触发了服务重启，不是崩溃
```

---

## 修复步骤
```
无需修复。等待 3-5 秒，新进程自动就绪。

验证：
    curl http://127.0.0.1:18790/health
    → {"ok":true,"status":"live"} ✅
```

---

## 经验教训
1. **doctor 命令会触发 Gateway 重启，这是预期行为**
2. **1006 = WebSocket 异常关闭，不一定是崩溃**
3. **Gateway PID 变更 + 进程存活 = 正常重启，不是崩溃**
4. **误判为崩溃会导致不必要的修复动作**

---

## 状态
- **resolved**: true（自动恢复）
- **is_normal_behavior**: true
