# Gog Google Workspace CLI技能

> **技能获取时间:** 2026-03-18 20:15
> **技能来源:** 老庄发送
> **版本:** 1.0.0
> **用途:** Google Workspace CLI操作

---

## 技能描述

Google Workspace CLI工具，用于操作Gmail、Calendar、Drive、Contacts、Sheets、Docs等Google服务。

---

## 支持服务

| 服务 | 说明 |
|------|------|
| **Gmail** | 邮件管理、发送、搜索 |
| **Calendar** | 日历事件管理 |
| **Drive** | 云盘文件管理 |
| **Contacts** | 联系人管理 |
| **Sheets** | 表格操作 |
| **Docs** | 文档操作 |

---

## 安装配置

### 安装

```bash
# 安装gog CLI
npm install -g gog

# 或使用npx
npx gog --help
```

### 认证配置

```bash
# 初始化认证
gog auth

# 按提示完成OAuth授权
```

---

## 使用方式

### Gmail操作

```bash
# 列出邮件
gog gmail list --limit 10

# 发送邮件
gog gmail send --to "email@example.com" --subject "主题" --body "内容"

# 搜索邮件
gog gmail search "关键词"
```

### Calendar操作

```bash
# 列出事件
gog calendar list --date 2026-03-18

# 创建事件
gog calendar create --title "会议" --start "2026-03-19T10:00" --end "2026-03-19T11:00"

# 查看日程
gog calendar agenda
```

### Drive操作

```bash
# 列出文件
gog drive list

# 上传文件
gog drive upload ./file.pdf

# 下载文件
gog drive download <file-id>

# 分享文件
gog drive share <file-id> --email "user@example.com"
```

### Sheets操作

```bash
# 读取表格
gog sheets read <spreadsheet-id>

# 写入数据
gog sheets write <spreadsheet-id> --range "A1:B2" --values "a,b,c,d"

# 创建表格
gog sheets create --title "新表格"
```

### Docs操作

```bash
# 读取文档
gog docs read <document-id>

# 创建文档
gog docs create --title "新文档"
```

---

## 使用场景

### 场景一：批量发送邮件

```bash
# 发送邮件
gog gmail send \
  --to "team@example.com" \
  --subject "AI-EVO周报" \
  --body-file ./report.txt
```

### 场景二：日历管理

```bash
# 创建会议
gog calendar create \
  --title "团队周会" \
  --start "2026-03-20T14:00" \
  --end "2026-03-20T15:00" \
  --attendees "user1@example.com,user2@example.com"
```

### 场景三：表格操作

```bash
# 更新表格数据
gog sheets update <id> \
  --range "A1:D10" \
  --values-file ./data.csv
```

---

## 与其他技能协作

| 技能 | 协作场景 |
|------|----------|
| API Gateway | 对比Google API |
| 飞书文档 | 跨平台文档同步 |
| 工作汇报 | 报告发送 |
| 项目管理 | 日历集成 |

---

## 注意事项

| 注意项 | 说明 |
|--------|------|
| **OAuth授权** | 首次使用需完成授权 |
| **API配额** | 注意Google API限制 |
| **权限范围** | 授权时选择合适权限 |
| **安全存储** | 保护认证凭证 |

---

## 文件位置

| 文件 | 路径 |
|------|------|
| 技能包 | `/Users/bjd/intelligence/gog/` |
| SKILL.md | `/Users/bjd/intelligence/gog/SKILL.md` |

---

## 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-18 | 初始版本，技能包导入 |

---

*技能创建: 2026-03-18 20:15*
*技能来源: 老庄发送*
*维护者: 姜小牙*