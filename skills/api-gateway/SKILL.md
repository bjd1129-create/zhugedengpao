# API Gateway技能

> **技能获取时间:** 2026-03-18 20:03
> **技能来源:** 老庄发送
> **提供者:** Maton.ai
> **支持服务:** 138个

---

## 技能描述

连接100+ APIs（Google Workspace, Microsoft 365, GitHub, Notion, Slack, Airtable, HubSpot等）的统一网关，使用托管OAuth进行安全认证。

---

## 核心特点

| 特点 | 说明 |
|------|------|
| **统一API** | 一个API Key访问138个服务 |
| **托管OAuth** | 自动管理OAuth令牌 |
| **安全隔离** | 需要用户明确授权每个服务 |
| **原生API** | 直接调用原生API端点 |

---

## 配置

### 获取API Key

1. 访问 https://maton.ai
2. 注册账号
3. 在 https://maton.ai/settings 获取API Key

### 环境变量

```bash
export MATON_API_KEY="your-api-key"
```

---

## 使用方式

### 基础调用

```bash
# Slack发消息
curl -X POST https://gateway.maton.io/slack/api/chat.postMessage \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"channel": "C0123456", "text": "Hello!"}'
```

### Python示例

```python
import urllib.request, os, json

data = json.dumps({'channel': 'C0123456', 'text': 'Hello!'}).encode()
req = urllib.request.Request(
    'https://gateway.maton.io/slack/api/chat.postMessage',
    data=data, method='POST'
)
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.load(urllib.request.urlopen(req)))
```

---

## 支持的服务（138个）

### Google系列

| 服务 | 说明 |
|------|------|
| google-mail | Gmail |
| google-calendar | 日历 |
| google-drive | 云盘 |
| google-sheets | 表格 |
| google-docs | 文档 |
| google-slides | 演示文稿 |
| google-ads | 广告 |
| google-analytics | 分析 |

### Microsoft系列

| 服务 | 说明 |
|------|------|
| outlook | 邮箱 |
| microsoft-teams | Teams |
| microsoft-excel | Excel |
| microsoft-to-do | 待办 |
| one-drive | 云盘 |
| sharepoint | 协作 |

### 协作工具

| 服务 | 说明 |
|------|------|
| slack | 团队沟通 |
| notion | 知识库 |
| github | 代码托管 |
| jira | 项目管理 |
| asana | 任务管理 |
| trello | 看板 |
| linear | 项目管理 |

### 营销工具

| 服务 | 说明 |
|------|------|
| hubspot | CRM |
| mailchimp | 邮件营销 |
| salesforce | CRM |
| pipedrive | 销售 |
| active-campaign | 营销自动化 |

### 通讯工具

| 服务 | 说明 |
|------|------|
| telegram | 消息 |
| whatsapp-business | 商业消息 |
| twilio | 短信/语音 |
| sendgrid | 邮件 |
| mailgun | 邮件 |

### AI工具

| 服务 | 说明 |
|------|------|
| elevenlabs | 语音合成 |
| fal-ai | AI模型 |
| tavily | AI搜索 |
| brave-search | 搜索 |

---

## 连接管理

### 列出已连接服务

```bash
curl https://ctrl.maton.io/connections?status=ACTIVE \
  -H "Authorization: Bearer $MATON_API_KEY"
```

### 发起新连接

```bash
curl https://ctrl.maton.io/connect?app=slack \
  -H "Authorization: Bearer $MATON_API_KEY"
```

---

## 安全说明

| 安全特性 | 说明 |
|----------|------|
| **无默认权限** | API Key本身不授予任何第三方访问权限 |
| **明确授权** | 每个服务需用户通过Maton明确授权 |
| **范围限制** | 访问严格限制在用户授权的连接 |
| **令牌托管** | OAuth令牌由Maton安全托管 |

---

## 使用场景

### 场景一：发送Slack消息

```python
# 发送Slack消息
import requests, os

requests.post(
    'https://gateway.maton.io/slack/api/chat.postMessage',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={'channel': 'C0123456', 'text': 'AI-EVO团队报告已生成！'}
)
```

### 场景二：更新Google Sheets

```python
# 更新Google Sheets
requests.put(
    'https://gateway.maton.io/google-sheets/v4/spreadsheets/{id}/values/A1:B2',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={'values': [['任务', '状态'], ['研究', '完成']]}
)
```

### 场景三：创建GitHub Issue

```python
# 创建GitHub Issue
requests.post(
    'https://gateway.maton.io/github/repos/owner/repo/issues',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={'title': '新功能请求', 'body': '描述...'}
)
```

---

## 与其他技能协作

| 技能 | 协作场景 |
|------|----------|
| 项目管理 | 同步任务到Notion/Jira |
| Twitter运营 | 发布后通知Slack |
| 飞书文档 | 同步到Google Docs |
| 深度研究 | 保存到Notion |

---

## 文件位置

| 文件 | 路径 |
|------|------|
| 技能包 | `/Users/bjd/intelligence/api-gateway/` |
| SKILL.md | `/Users/bjd/intelligence/api-gateway/SKILL.md` |
| 参考文档 | `/Users/bjd/intelligence/api-gateway/references/` |

---

## 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-18 | 初始版本，技能包导入 |

---

*技能创建: 2026-03-18 20:03*
*技能来源: 老庄发送*
*提供者: Maton.ai*
*维护者: 姜小牙*