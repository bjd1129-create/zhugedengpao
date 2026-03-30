# Discord运营技能

> **技能获取时间:** 2026-03-18 20:12
> **技能来源:** 老庄发送
> **用途:** Discord频道运营、消息发送、社区管理

---

## 技能描述

通过OpenClaw的message工具操作Discord频道，支持发送消息、管理频道、发布公告、管理成员等运营功能。

---

## 核心功能

| 功能 | action参数 | 说明 |
|------|------------|------|
| **发送消息** | send | 发送消息到频道 |
| **公告发布** | send | 发布服务器公告 |
| **频道管理** | channel-create | 创建新频道 |
| **成员管理** | member-info | 查看成员信息 |
| **角色管理** | role-info | 查看角色信息 |
| **表情管理** | emoji-list | 列出表情符号 |
| **话题创建** | thread-create | 创建话题帖子 |

---

## 使用方式

### 发送消息

```typescript
message({
  action: "send",
  channel: "discord",
  target: "channel-id-or-name",
  message: "消息内容"
})
```

### 指定频道

```typescript
// 使用频道ID
target: "123456789012345678"

// 使用频道名称
target: "general"
```

---

## 基础示例

### 发送普通消息

```typescript
message({
  action: "send",
  channel: "discord",
  target: "general",
  message: "AI-EVO团队今日研究成果已发布！"
})
```

### 发送公告

```typescript
message({
  action: "send",
  channel: "discord",
  target: "announcements",
  message: "📢 **重要公告**\n\n新功能已上线！"
})
```

### 发送带格式消息

```typescript
message({
  action: "send",
  channel: "discord",
  target: "research",
  message: `# 研究报告

## 一、核心发现
- 发现1：...
- 发现2：...

## 二、建议
1. [建议1]
2. [建议2]`
})
```

---

## 高级功能

### 创建话题帖子

```typescript
message({
  action: "thread-create",
  channel: "discord",
  channelId: "channel-id",
  threadName: "VoxYZ研究讨论",
  message: "欢迎大家讨论VoxYZ的复刻方案"
})
```

### 发送嵌入消息

```typescript
message({
  action: "send",
  channel: "discord",
  target: "general",
  message: "",
  // 嵌入内容通过特定格式实现
})
```

---

## 注意事项

### Discord限制

| 限制 | 说明 |
|------|------|
| **消息长度** | 2000字符 |
| **换行** | 使用 `\n` |
| **Markdown** | 支持部分Markdown |
| **频率限制** | 避免频繁发送 |

### 格式支持

| 格式 | 示例 |
|------|------|
| **粗体** | `**文本**` |
| **斜体** | `*文本*` |
| **代码** | `` `代码` `` |
| **代码块** | ``` ```代码``` ``` |
| **引用** | `> 引用` |
| **标题** | `# H1` `## H2` |

---

## 最佳实践

### 消息结构

```markdown
**标题** 🔔

正文内容...

---

📋 **要点：**
1. 要点1
2. 要点2

🔗 **链接：** [点击查看](url)
```

### 公告格式

```markdown
📢 **【公告标题】**

公告内容...

---

⏰ 时间：YYYY-MM-DD
👤 发布者：AI-EVO团队
```

### 研究报告格式

```markdown
# 📊 研究报告：[主题]

## 核心发现
- 发现1
- 发现2

## 价值结论
✅ 可复制性：⭐⭐⭐
⚠️ 技术难点：[描述]
💰 商业价值：高/中/低

---
*AI-EVO团队出品*
```

---

## 与其他技能协作

| 技能 | 协作场景 |
|------|----------|
| Twitter运营 | 跨平台内容同步 |
| 飞书文档 | 文档链接分享 |
| 今日热榜 | 热点话题讨论 |
| 工作汇报 | 团队日报发送 |

---

## 文件位置

| 文件 | 路径 |
|------|------|
| 技能包 | `/Users/bjd/intelligence/discord/` |
| SKILL.md | `/Users/bjd/intelligence/discord/SKILL.md` |

---

## 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.1 | 2026-03-18 | 初始版本，技能包导入 |

---

*技能创建: 2026-03-18 20:12*
*技能来源: 老庄发送*
*维护者: 姜小牙*