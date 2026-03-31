# Case 004: sessions_send 双重权限开关故障

## 元信息
- **case_id**: 004
- **发生时间**: 2026-03-31 14:00-15:00
- **症状分类**: Session / Auth
- **关键词**: sessions_send, forbidden, visibility, agentToAgent, open_id cross app

---

## 症状表现

### 第一层（先暴露）
| 症状 | 错误信息 |
|------|----------|
| sessions_send 发送失败 | `Session send visibility is restricted. Set tools.sessions.visibility=all` |
| delivery.to 发送失败 | `Unknown target "小花"` |

### 第二层（修复第一层后暴露）
| 症状 | 错误信息 |
|------|----------|
| sessions_send 仍失败 | `Agent-to-agent messaging is disabled. Set tools.agentToAgent.enabled=true` |

---

## 根因

**openclaw 版本升级（2026.3.13 → 2026.3.28）后，跨 agent 通信需要双重开关：**

| 开关 | 控制内容 | 旧配置是否有 |
|------|----------|-------------|
| `tools.sessions.visibility=all` | 能否看到其他 session | ❌ 缺失 |
| `tools.agentToAgent.enabled=true` | 能否主动发消息给其他 agent | ❌ 缺失 |

**为什么之前没发现？**
- `sessions.visibility` 旧版默认允许，新版默认关闭
- `agentToAgent.enabled` 是新版新增的开关
- 两层开关都是静默阻断，不报错直到调用时才暴露

---

## 诊断步骤
```
[1/4] 检查第一层权限
    命令：grep "visibility" ~/.openclaw/config.yaml
    结果：无输出 → sessions.visibility 未设置

[2/4] 尝试 sessions_send
    命令：openclaw sessions send test
    结果：forbidden（第一层阻断）

[3/4] 修复第一层后检查第二层
    命令：openclaw config set tools.sessions.visibility=all
    结果：重新测试仍 forbidden（第二层阻断）

[4/4] 检查 agentToAgent 配置
    命令：grep "agentToAgent" ~/.openclaw/config.yaml
    结果：无输出 → 第二层开关也缺失
```

---

## 修复步骤
```
[1/4] 设置第一层权限
    命令：openclaw config set tools.sessions.visibility=all
    结果：✅

[2/4] 设置第二层权限
    命令：openclaw config set tools.agentToAgent.enabled=true
    结果：✅

[3/4] 重启 Gateway
    命令：openclaw gateway restart
    结果：Gateway 重启生效

[4/4] 验证 sessions_send
    命令：coordinator cron 触发测试
    结果：deliveryStatus: delivered ✅
```

---

## 各应用下正确 open_id（备用）
| 应用 | open_id |
|------|---------|
| zhuge | `ou_489687303d4994b12b614f9afde89217` |
| coordinator | `ou_71bf6382be997d640eeada9f92302c98` |
| writer | `ou_a1880795f6cb683e78c22cfd87bff6d3` |
| researcher | `ou_7f9889f134b9b14ecf36087dae1d4ccf` |
| engineer | `ou_e305d5fd0ee9a86c33d6bf217724fbfd` |

---

## 经验教训
1. **openclaw 版本升级会静默新增配置项**
2. **跨 agent 通信是双重开关，需要逐层排查**
3. **静默故障：配置缺失不报错，直到调用才暴露**
4. **升级后要对比新旧 schema，补全缺失字段**
5. **黄金备份需要跟随版本更新**

---

## 状态
- **resolved**: true
- **fix_count**: 1
- **root_cause**: openclaw 版本升级配置未同步
