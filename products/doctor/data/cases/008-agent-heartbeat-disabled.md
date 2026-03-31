# Case 008: Agent 心跳功能被禁用导致 Gateway 无响应

## 元信息
- **case_id**: 008
- **发生时间**: 2026-03-31
- **症状分类**: Gateway / Agent
- **关键词**: heartbeat disabled, Agent 超时, 11个Agent无响应

---

## 症状表现
| Agent | 心跳状态 | 调用结果 |
|-------|----------|----------|
| main | 30m（正常） | ✅ 正常 |
| canmou | disabled | ❌ 超时无响应 |
| coder | disabled | ❌ 超时无响应 |
| community | disabled | ❌ 超时无响应 |
| creator | disabled | ⚠️ 有时超时异常 |
| evolution | disabled | ❌ 超时无响应 |
| finance | disabled | ❌ 超时无响应 |
| growth | disabled | ❌ 超时无响应 |
| pmo | disabled | ❌ 超时无响应 |
| product | disabled | ❌ 超时无响应 |
| trading | disabled | ❌ 超时无响应 |
| yunying | disabled | ❌ 超时无响应 |

---

## 根因

**Agent 心跳功能被禁用**：
- 心跳是 Agent 与 Gateway 保持活跃连接的关键机制
- 心跳禁用后，Agent 无法与 Gateway 保持长连接
- Gateway 认为 Agent 已离线，拒绝或忽略请求
- 导致调用时超时无响应

**常见原因**：
- 配置文件中显式设置 `heartbeat: disabled`
- 某次维护/调试时人为禁用了非主 Agent 的心跳
- 新增 Agent 时未配置心跳功能

---

## 诊断步骤
```
[1/2] 检查 Agent 心跳状态
    命令：openclaw status
    结果：Heartbeat 行显示各 Agent 状态

[2/2] 检查 Gateway 连接状态
    命令：openclaw status
    结果：Gateway reachable + Agent sessions 状态
```

---

## 修复步骤
```
[1/3] 检查当前心跳配置
    命令：openclaw config get
    结果：查看 heartbeat 相关配置

[2/3] 为指定 Agent 启用心跳
    命令：openclaw config set agents.<agentId>.heartbeat.enabled=true
    命令：openclaw config set agents.<agentId>.heartbeat.interval=5m
    结果：为各 Agent 启用心跳

[3/3] 重启 Gateway 使配置生效
    命令：openclaw gateway restart
    结果：Gateway 重启，各 Agent 重新注册
```

---

## 修复结果
| Agent | 心跳状态（修复后） |
|-------|-------------------|
| main | 30m ✅ |
| 其他 11 个 Agent | 5m（建议值）✅ |

---

## 经验教训
1. **心跳是 Agent 保持在线的关键**，禁用后 Gateway 会认为 Agent 已离线
2. **main Agent 心跳正常不代表其他 Agent 也正常**，要逐个检查
3. **心跳间隔要平衡**：太短产生过多流量，太长发现故障慢（建议 5-10m）
4. **非主 Agent 心跳被禁用通常是配置遗漏**，要检查新增 Agent 的配置

---

## 状态
- **resolved**: true
- **fix_count**: 1
- **root_cause**: 心跳配置被禁用
