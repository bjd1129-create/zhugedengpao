# Case 006: Next.js task-ui 高 CPU 游离进程干扰系统

## 元信息
- **case_id**: 006
- **发生时间**: 2026-03-31 14:42
- **症状分类**: Process
- **关键词**: Next.js, task-ui, 高CPU, 56267, 游离进程

---

## 症状表现
| 检查项 | 状态 |
|--------|------|
| OpenClaw Gateway | ✅ 正常（PM2 托管，HTTP 200 OK） |
| PM2 进程 | ✅ online，PID 6888，内存 530MB |
| 游离 node 进程 | PID 33480 CPU 56267（极高！）|
| 游离 node 进程 | PID 34580 CPU 55（正常） |

---

## 根因
`C:\openclaw-pc\task-ui` 的 Next.js 前端进程脱离 PM2 托管，变成游离进程：

1. **Next.js dev server** 未用 PM2 托管
2. PID 33480 进入死循环/内存泄漏，CPU 爆表
3. 系统资源被占满，影响其他服务响应

---

## 诊断步骤
```
[1/3] 检查 OpenClaw Gateway 状态
    命令：curl http://127.0.0.1:18790/health
    结果：200 OK ✅（Gateway 本身正常）

[2/3] 检查 PM2 进程列表
    命令：pm2 list
    结果：openclaw-gateway online ✅

[3/3] 检查游离高 CPU 进程
    命令：ps aux | grep node | grep -v grep
    结果：PID 33480 CPU 56267，来源 C:\openclaw-pc\task-ui
```

---

## 修复步骤
```
[1/2] Kill 高 CPU 游离进程
    命令：kill -9 33480
    结果：CPU 资源释放

[2/2] 将 task-ui 纳入 PM2 管理（防止复发）
    命令：pm2 start --name task-ui "cd C:\openclaw-pc\task-ui && npm run dev"
    结果：进程 PM2 托管，自动重启
```

---

## 修复结果
| 检查项 | 状态 |
|--------|------|
| 游离进程 PID 33480 | ✅ 已清除 |
| 系统 CPU | ✅ 资源释放 |
| task-ui | 待纳入 PM2 |

---

## 经验教训
1. **不只是 Gateway，所有长时间运行的 node 进程都要 PM2 托管**
2. **Next.js dev server 容易游离**，开发环境尤其常见
3. **CPU 累积值 56267 = 长期卡死**，不是瞬时值
4. **Gateway 正常不代表系统正常**，要检查所有进程

---

## 状态
- **resolved**: true
- **fix_count**: 1
- **note**: Gateway 本身正常，是 task-ui 干扰
