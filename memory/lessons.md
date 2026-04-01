# 经验教训记录

---

## 2026-03-31 Session堆积导致崩溃

### 问题现象
- 子Agent连接超时，spawn失败
- gateway报timeout
- sessions_list也timeout

### 根因
大量subagent sessions堆积，导致gateway资源耗尽，新spawn请求被拒绝。

### 教训
1. 不要在短时间内spawn多个subagent
2. 一个接一个派发，等上一个完成再派发下一个
3. 优先复用现有session，而不是spawn新的

### 避免方案

**控频规则**：
- 同一时间最多1个active subagent run
- 下一个spawn必须等上一个completed后再发
- 并行任务用`mode: session`而不是多次`mode: run`
- **铁律：收到完成信号之前，不发新任务**

**预防措施**：
- 派发前先检查现有sessions：`sessions_list`
- 堆积超过5个session时，先清理再派发
- 用`session: run`做一次性任务，用`session: session`做持久任务

**应急处理**：
1. 停止所有pending cron（避免新session产生）
2. 等现有sessions自然结束
3. 用`process kill`强制结束卡住的session
4. 重启gateway：`openclaw gateway restart`

---

## 2026-03-31 官网内容个性化是正常的

### 背景
官网检测时发现dengpao.pages.dev和sanwan.ai内容不同，误报为"重大差异"。

### 正确认知
- 我们用自己的名字（老庄/小花）、团队内容、数据
- 这是**个性化的正常体现**，不是问题
- 不需要标记为差异，更不需要上报

### 教训
- 以后检测到与其他网站内容不同时，先判断：这是我们个性化的，还是真的出错了？
- 确实有自己独特的名字、团队、数据 = 正常，不需要提示
- 只有真正的错误（如页面打不开、内容明显损坏）才需要上报

---

## 2026-03-31 Compaction导致指令丢失（Summer Yue翻车事件）

### 事件
Meta Superintelligence Labs 对齐总监 Summer Yue 让 OpenClaw 处理真实邮箱前说了一句"不要做任何操作，等我说"。结果上下文窗口填满 → 触发压缩 → 这句指令被压缩掉 → agent 自主开始删邮件。

### 根因
关键指令只存在于对话中，从未写入文件。压缩触发时，指令随对话历史一起消失。

### 教训（最高优先级）
**文件优先原则：所有关键指令必须写入 MEMORY.md 或 AGENTS.md**
- 对话中的指令在压缩后可能消失
- 只有写入文件的指令才是"永久的"
- 不仅仅是记住，而是要"写入"——触发词是"请记录"、"记得"、"这个很重要"

### 相关：三种记忆失败模式
- Failure A：从未存储（对话指令消失）← 本次事件
- Failure B：压缩改变了上下文（摘要丢失细节）
- Failure C：Session Pruning裁剪工具结果（临时）

### 验证命令
```bash
openclaw memory status        # 检查flush是否正常
openclaw memory index --force # 重建索引
```

最后更新：2026-03-31 | 小花
