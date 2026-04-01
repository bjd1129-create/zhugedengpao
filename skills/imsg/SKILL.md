# iMessage运营技能

> **技能获取时间:** 2026-03-18 20:18
> **技能来源:** 老庄发送
> **版本:** 1.0.0
> **用途:** iMessage消息发送与管理

---

## 技能描述

通过OpenClaw的message工具操作iMessage，支持发送消息、管理对话等iOS消息功能。

---

## 核心功能

| 功能 | action参数 | 说明 |
|------|------------|------|
| **发送消息** | send | 发送iMessage消息 |
| **阅读消息** | read | 读取消息内容 |
| **搜索消息** | search | 搜索历史消息 |
| **删除消息** | delete | 删除消息 |

---

## 使用方式

### 发送iMessage

```typescript
message({
  action: "send",
  channel: "imessage",
  target: "user@email.com", // 或手机号
  message: "消息内容"
})
```

### 指定接收者

```typescript
// 使用Apple ID邮箱
target: "user@icloud.com"

// 使用手机号
target: "+8613800138000"

// 使用联系人姓名
target: "张三"
```

---

## 基础示例

### 发送普通消息

```typescript
message({
  action: "send",
  channel: "imessage",
  target: "user@icloud.com",
  message: "AI-EVO团队研究报告已完成！"
})
```

### 发送带格式消息

```typescript
message({
  action: "send",
  channel: "imessage",
  target: "+8613800138000",
  message: `📊 研究报告

今日产出：
• VoxYZ研究（18份）
• 三万研究（10份）

详细内容见飞书文档。`
})
```

---

## 注意事项

### iMessage限制

| 限制 | 说明 |
|------|------|
| **消息长度** | 无严格限制 |
| **附件** | 支持图片/文件 |
| **群发** | 需谨慎使用 |
| **频率** | 避免频繁发送 |

### 格式支持

| 格式 | 说明 |
|------|------|
| 纯文本 | 完全支持 |
| Emoji | 完全支持 |
| 链接 | 自动预览 |
| Markdown | 部分支持 |

---

## 使用场景

### 场景一：团队通知

```typescript
message({
  action: "send",
  channel: "imessage",
  target: "team@icloud.com",
  message: "📢 团队会议提醒\n\n时间：今天15:00\n地点：会议室A"
})
```

### 场景二：报告发送

```typescript
message({
  action: "send",
  channel: "imessage",
  target: "boss@icloud.com",
  message: `【日报】2026-03-18

完成事项：
1. VoxYZ复刻研究
2. 三万团队分析
3. CrewAI调研

详情：[飞书链接]`
})
```

---

## 与其他技能协作

| 技能 | 协作场景 |
|------|----------|
| Twitter运营 | 跨平台消息同步 |
| 飞书文档 | 文档链接分享 |
| 工作汇报 | 日报发送 |
| 项目管理 | 任务通知 |

---

## 文件位置

| 文件 | 路径 |
|------|------|
| 技能包 | `/Users/bjd/intelligence/imsg/` |
| SKILL.md | `/Users/bjd/.openclaw/skills/imsg/SKILL.md` |

---

## 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-18 | 初始版本，技能包导入 |

---

*技能创建: 2026-03-18 20:18*
*技能来源: 老庄发送*
*维护者: 姜小牙*