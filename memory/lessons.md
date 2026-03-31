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

最后更新：2026-03-31 | 小花
