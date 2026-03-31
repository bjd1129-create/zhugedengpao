# Case 011: Gateway 配置路径错误导致服务异常

## 元信息
- **case_id**: 011
- **发生时间**: 2026-03-31
- **症状分类**: Gateway / Config
- **关键词**: C:\tmp\openclaw, 配置文件缺失, 路径错误

---

## 症状表现
| 检查项 | 状态 |
|--------|------|
| Gateway 配置文件 | `C:\tmp\openclaw\openclaw.json (missing)` ❌ |
| 正确配置路径 | `C:\Users\<user>\.openclaw\` |
| Gateway | 需重启才恢复 |

---

## 根因

**Gateway 配置路径指向错误位置**：
1. Gateway 实际使用的配置路径是 `C:\tmp\openclaw\`
2. 但配置文件实际存放在 `C:\Users\<user>\.openclaw\`
3. 导致 Gateway 找不到配置文件或使用空配置启动
4. 需要手动复制配置文件到正确位置

---

## 诊断步骤
```
[1/3] 检查 Gateway 配置路径
    命令：openclaw status
    结果：Config (cli): C:\tmp\openclaw\openclaw.json (missing)

[2/3] 检查正确配置是否存在
    命令：ls ~/.openclaw/openclaw.json
    结果：配置文件存在于正确位置

[3/3] 确认 Gateway 进程
    命令：ps aux | grep openclaw
    结果：进程存在但使用错误路径
```

---

## 修复步骤
```
[1/4] 停止 Gateway
    命令：taskkill /F /IM node.exe
    结果：Gateway 停止

[2/4] 复制配置文件到正确位置
    命令：mkdir C:\tmp\openclaw\ 2>$null; copy %USERPROFILE%\.openclaw\openclaw.json C:\tmp\openclaw\
    结果：配置文件已复制

[3/4] 重启 Gateway
    命令：openclaw gateway start
    结果：Gateway 重启，PID 新增

[4/4] 验证健康状态
    命令：curl http://127.0.0.1:18789/health
    结果：HTTP 200 ✅
```

---

## 修复结果
| 检查项 | 状态 |
|--------|------|
| Config (cli) | ✅ `C:\tmp\openclaw\openclaw.json` ✓ |
| Config (service) | ✅ `C:\tmp\openclaw\openclaw.json` ✓ |
| Gateway | ✅ 127.0.0.1:18789 ✓ |
| Health | ✅ HTTP 200 ✓ |
| RPC probe | ✅ ok ✓ |

---

## 经验教训
1. **Gateway 有多个可能的配置路径**，要确认实际使用的是哪个
2. **配置文件要同步到 Gateway 实际读取的位置**
3. **彻底重启能解决配置缓存问题**
4. **tmp 目录配置通常是临时调试遗留**，正常应该用 `~/.openclaw/`

---

## 状态
- **resolved**: true
- **fix_count**: 1
- **root_cause**: Gateway 配置路径指向 tmp 目录而非用户目录
