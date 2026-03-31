# Case 009: 切换工作区导致崩溃

## 元信息
- **case_id**: 009
- **发生时间**: 2026-03-31
- **症状分类**: Workspace
- **关键词**: 工作区切换, C:\openclaw 不存在, 目录丢失

---

## 症状表现
| 检查项 | 状态 |
|--------|------|
| C:\openclaw 目录 | ❌ 不存在 |
| 实际工作区 | C:\openclaw-pc（存在） |
| Gateway | 需重启才恢复 |

---

## 诊断步骤
```
[1/5] 检查 C:\openclaw 是否存在
    命令：ls C:\openclaw
    结果：目录不存在

[2/5] 检查实际工作区
    命令：ls C:\openclaw-pc
    结果：目录存在，基本配置文件正常

[3/5] 检查 Gateway 状态
    命令：curl http://127.0.0.1:18789/health
    结果：无响应 → Gateway 未运行

[4/5] 查看日志
    命令：ls ~/.openclaw/logs/
    结果：发现 .clobbered 和 .broken 备份文件（配置损坏记录）

[5/5] 重启 Gateway
    命令：C:\openclaw-pc\gateway.cmd
    结果：Gateway PID 16540 online，HTTP 200 ✅
```

---

## 根因

**工作区切换时配置文件损坏**：
1. 用户切换工作区时，openclaw 配置被破坏
2. 配置目录从 `C:\openclaw` 丢失或被清空
3. Gateway 因配置无效而无法启动
4. 日志显示多次 `.clobbered`（配置被覆盖/损坏）事件

**修复**：Gateway 重启后自动恢复正常（因为实际工作区 `C:\openclaw-pc` 完好）

---

## 修复步骤
```
[1/3] 确认实际工作区位置
    命令：ls C:\openclaw-pc
    结果：目录存在，配置完好

[2/3] 重启 Gateway
    命令：C:\openclaw-pc\gateway.cmd
    结果：Gateway PID 16540 online ✅

[3/3] 验证健康状态
    命令：curl http://127.0.0.1:18789/health
    结果：HTTP 200 OK ✅
```

---

## 经验教训
1. **工作区切换是危险操作**，容易触发配置损坏
2. **.clobbered 文件 = 配置被意外覆盖的备份**，要定期清理
3. **Gateway 重启能自动恢复**，因为实际配置通常完好
4. **Windows 路径问题**：`C:\openclaw` vs `C:\openclaw-pc` 要区分清楚

---

## 状态
- **resolved**: true
- **fix_count**: 1
- **root_cause**: 工作区切换导致配置目录丢失/损坏
