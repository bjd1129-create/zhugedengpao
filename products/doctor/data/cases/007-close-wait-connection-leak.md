# Case 007: CLOSE_WAIT 连接堆积导致 Agent 超时无待命

## 元信息
- **case_id**: 007
- **发生时间**: 2026-03-27 23:46
- **症状分类**: Gateway / Network
- **关键词**: CLOSE_WAIT, 连接泄露, 9个Agent超时, 端口18789

---

## 症状表现
| 检查项 | 状态 |
|--------|------|
| 端口 18789 | LISTENING（正在监听） |
| 连接状态 | 几乎全部 CLOSE_WAIT |
| Agent 并发 | 1/10（仅内容总监正常） |
| Gateway | 无响应超时 |
| 9 个 Agent | 因 Gateway 超时无法待命 |

---

## 根因

**TCP 连接泄露**：端口 18789 的连接处于 CLOSE_WAIT 状态，说明：

1. **TCP 被动关闭方收到 FIN，但未完成关闭**（未发送自己的 FIN）
2. **应用层资源未释放**，连接无法真正关闭
3. **Gateway 处理能力下降**，无法响应 Agent 心跳
4. **9 个 Agent 全部超时无待命**

**常见原因**：
- 服务端连接处理逻辑异常（未在应答后关闭/复用连接）
- 资源竞争/锁问题导致连接处理线程阻塞
- 心跳/保活间隔配置过短或超时阈值过低
- 客户端存在请求风暴或重试逻辑不当

---

## 诊断步骤
```
[1/4] 检查端口连接状态
    命令：netstat -ano | findstr :18789
    结果：LISTENING + 大量 CLOSE_WAIT

[2/4] 读取 CLOSE_WAIT 连接的 PID
    命令：netstat -ano | findstr CLOSE_WAIT
    结果：找出对应 PID

[3/4] 检查进程资源占用
    命令：tasklist | findstr <PID>
    结果：CPU/内存/句柄使用情况

[4/4] 检查进程日志
    命令：tail ~/.openclaw/logs/gateway.err.log
    结果：查找连接处理相关错误
```

---

## 修复步骤

### 步骤 A：重启 Gateway（释放僵死连接）
```
[1/3] 找出监听 18789 的进程
    命令：netstat -ano | findstr :18789 | findstr LISTENING
    结果：PID xxx

[2/3] 检查进程健康
    命令：tasklist | findstr xxx
    结果：CPU/内存/句柄状态

[3/3] 平滑终止并重启
    命令：taskkill /PID xxx /F
    命令：openclaw gateway restart
    结果：Gateway 重启，CLOSE_WAIT 释放
```

### 步骤 B：Agent 重连注册
```
[1/2] 依次触发 Agent 重新注册
    命令：对每个 Agent 执行刷新保活请求
    结果：Agent 状态从"超时"转为"待命"

[2/2] 验证并发恢复
    命令：检查 Agent 并发状态
    结果：10/10 全部待命 ✅
```

---

## 加固方案（避免 CLOSE_WAIT 再次出现）

### 方向 1：修复服务端连接生命周期
- 在应答完成后立即关闭闲置连接
- 为每个请求设置读写超时，超时时主动断开
- 实现 Keep-Alive 与连接复用，控最大空闲时间 30-60s

### 方向 2：优化心跳/保活参数
- 加宽保活超时阈值（3s → 5-10s），容忍网络抖动
- 缩短心跳间隔（5-10s 一次），避免误判超时

### 方向 3：客户端请求与重试策略
- 限制并发连接数与重试上限
- 加入指数退避重试，避免瞬间流量风暴
- 确保客户端在收到错误/超时后正确关闭本地连接

---

## 验证步骤
```
[1/3] 检查 CLOSE_WAIT 数量
    命令：netstat -ano | findstr CLOSE_WAIT | findstr 18789
    结果：数量显著下降 ✅

[2/3] 验证 Agent 并发
    命令：检查 10 个 Agent 状态
    结果：10/10 待命 ✅

[3/3] 压力测试
    命令：短时间 10 并发心跳
    结果：无超时，无大量 CLOSE_WAIT 复现 ✅
```

---

## 经验教训
1. **CLOSE_WAIT 堆积 = 连接泄露**，通常是应用层未正确关闭连接
2. **LISTENING 端口不等于 Gateway 健康**，还要看连接状态
3. **重启 Gateway 能快速释放连接**，但要同步 Agent 重连
4. **心跳参数要平衡**：太短容易误判，太长发现问题慢
5. **10 并发压力下更容易暴露连接管理问题**

---

## 状态
- **resolved**: true
- **fix_count**: 1
- **root_cause**: TCP CLOSE_WAIT 连接堆积
