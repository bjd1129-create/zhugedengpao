# Case 001: plugins.allow 无效插件导致 Gateway 启动失败

## 元信息
- **case_id**: 001
- **发生时间**: 2026-03-31 02:11
- **症状分类**: Gateway
- **关键词**: plugins.allow, minimax, Config invalid, 进程崩溃

---

## 症状表现
| 检查项 | 状态 |
|--------|------|
| Gateway HTTP 端口 18790 | 无监听 (connection refused) |
| Gateway 进程 | 存活但高 CPU 空转 |
| 飞书 WebSocket | 全部断开 |
| Bonjour | 多实例冲突 (OpenClaw (2)(3)) |

---

## 根因
`~/.openclaw/config.yaml` 的 `plugins.allow` 列表包含 `"minimax"` 插件，但该插件已不存在。openclaw 认为这是 **Config invalid**，导致 Gateway 启动后立即退出。

**触发背景**：openclaw 版本升级（2026.3.13 → 2026.3.28），配置未同步新增字段。

---

## 诊断步骤
```
[1/5] 检查 Gateway HTTP 端口
    命令：curl http://127.0.0.1:18790/health
    结果：connection refused → Gateway 未监听端口

[2/5] 检查 Gateway 进程状态
    命令：ps aux | grep openclaw
    结果：进程存在但 PID 频繁换

[3/5] 检查进程端口监听
    命令：lsof -i :18790
    结果：无输出 → 进程存活但未监听

[4/5] 查看错误日志
    命令：tail ~/.openclaw/logs/gateway.err.log
    结果：发现 "plugin not found: minimax" + "Config invalid"

[5/5] 检查 plugins.allow 配置
    命令：grep -A5 "plugins" ~/.openclaw/config.yaml
    结果：allow 列表有 "minimax" 但插件不存在
```

---

## 修复步骤
```
[1/4] 停止所有残留进程
    命令：pkill -f openclaw && sleep 2
    结果：僵尸进程清除

[2/4] 从 plugins.allow 移除无效插件
    命令：openclaw config set plugins.allow='["feishu"]'
    结果：minimax 从 allow 列表移除

[3/4] 运行 openclaw doctor --fix
    命令：openclaw doctor --fix
    结果：配置修复，launchctl 服务重启

[4/4] 等待 Gateway 就绪
    命令：curl http://127.0.0.1:18790/health
    结果：{"ok":true,"status":"live"} ✅
```

---

## 修复结果
| 检查项 | 状态 |
|--------|------|
| Gateway HTTP | ✅ {"ok":true,"status":"live"} |
| 飞书 WebSocket (10 bots) | ✅ 全部恢复 |
| Bot open_id 解析 | ✅ 全部成功 |

---

## 经验教训
1. **openclaw 版本升级后要检查新增配置项**
2. **plugins.allow 必须与实际安装插件匹配**
3. **静默故障需要检查 err.log 而非只看 status**

---

## 状态
- **resolved**: true
- **fix_count**: 1
