# 百度搜索技能

> **技能获取时间:** 2026-03-18 20:09
> **技能来源:** 老庄发送
> **提供者:** 百度AI Search
> **用途:** 通过百度AI搜索获取实时信息

---

## 技能描述

通过百度AI Search Engine (BDSE) 搜索网络，获取实时信息、文档、研究主题等。

---

## 安装要求

| 要求 | 说明 |
|------|------|
| Python3 | 必需 |
| BAIDU_API_KEY | 环境变量配置 |

### 配置API Key

```bash
export BAIDU_API_KEY="your-api-key"
```

---

## 使用方式

```bash
python3 skills/baidu-search/scripts/search.py '<JSON>'
```

---

## 请求参数

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| query | string | ✅ | - | 搜索关键词 |
| count | int | ❌ | 10 | 返回结果数（1-50） |
| freshness | string | ❌ | null | 时间范围筛选 |

---

## 时间范围格式

### 格式一：日期范围

```
"freshness": "YYYY-MM-DDtoYYYY-MM-DD"

示例："2025-09-01to2025-09-08"
```

### 格式二：相对时间

| 值 | 说明 |
|------|------|
| `pd` | 过去24小时 |
| `pw` | 过去7天 |
| `pm` | 过去31天 |
| `py` | 过去365天 |

---

## 使用示例

### 基础搜索

```bash
python3 scripts/search.py '{"query":"人工智能"}'
```

### 时间范围搜索

```bash
# 指定日期范围
python3 scripts/search.py '{
  "query":"最新新闻",
  "freshness":"2025-09-01to2025-09-08"
}'

# 过去24小时
python3 scripts/search.py '{
  "query":"最新新闻",
  "freshness":"pd"
}'
```

### 设置结果数量

```bash
python3 scripts/search.py '{
  "query":"旅游景点",
  "count": 20
}'
```

---

## 返回格式

```json
[
  {
    "title": "文章标题",
    "url": "https://example.com/article",
    "content": "文章摘要内容..."
  },
  ...
]
```

---

## 使用场景

### 场景一：实时信息查询

```bash
# 查询最新AI新闻
python3 scripts/search.py '{
  "query":"AI最新突破",
  "freshness":"pd",
  "count": 10
}'
```

### 场景二：研究主题搜索

```bash
# 搜索研究资料
python3 scripts/search.py '{
  "query":"OpenClaw框架使用教程",
  "count": 20
}'
```

### 场景三：历史信息查询

```bash
# 查询特定时间段信息
python3 scripts/search.py '{
  "query":"2024年AI大事件",
  "freshness":"2024-01-01to2024-12-31"
}'
```

---

## 与其他搜索工具对比

| 工具 | 特点 | 适用场景 |
|------|------|----------|
| **百度搜索** | 中文优化、实时 | 中文内容、国内信息 |
| web_search | 国际化、Brave API | 英文内容、国际信息 |
| 网页净化 | 深度提取 | 单页面内容提取 |

---

## 注意事项

| 注意项 | 说明 |
|--------|------|
| **API配额** | 注意API调用次数限制 |
| **中文优化** | 中文搜索效果最佳 |
| **时效性** | 使用freshness获取最新信息 |
| **结果数量** | 合理设置count避免过多 |

---

## 与其他技能协作

| 技能 | 协作场景 |
|------|----------|
| 深度研究 | 搜索研究素材 |
| 今日热榜 | 补充国内热点 |
| 网页净化 | 深度提取搜索结果 |
| SEO写作 | 中文内容研究 |

---

## 文件位置

| 文件 | 路径 |
|------|------|
| 技能包 | `/Users/bjd/intelligence/baidu-search/` |
| SKILL.md | `/Users/bjd/intelligence/baidu-search/SKILL.md` |
| 搜索脚本 | `/Users/bjd/intelligence/baidu-search/scripts/search.py` |

---

## 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.1.2 | 2026-03-18 | 初始版本，技能包导入 |

---

*技能创建: 2026-03-18 20:09*
*技能来源: 老庄发送*
*提供者: 百度AI Search*
*维护者: 姜小牙*