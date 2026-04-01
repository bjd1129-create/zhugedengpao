# Multi-Search-Engine多搜索引擎技能

> **技能获取时间:** 2026-03-18 20:20
> **技能来源:** 老庄发送
> **版本:** 2.0.1
> **用途:** 多搜索引擎聚合查询

---

## 技能描述

聚合多个搜索引擎的搜索技能，支持同时查询多个搜索引擎、结果聚合、智能排序。

---

## 支持的搜索引擎

| 引擎 | 说明 |
|------|------|
| **Brave Search** | web_search默认 |
| **百度搜索** | 中文优化 |
| **Google** | 国际搜索 |
| **Bing** | 微软搜索 |
| **DuckDuckGo** | 隐私搜索 |

---

## 核心功能

| 功能 | 说明 |
|------|------|
| **多引擎并发** | 同时查询多个搜索引擎 |
| **结果聚合** | 合并去重搜索结果 |
| **智能排序** | 按相关性排序 |
| **结果对比** | 不同引擎结果对比 |

---

## 使用方式

### 基础搜索

```bash
# 单引擎搜索
web_search({ query: "关键词" })

# 多引擎聚合
multi-search --query "关键词" --engines brave,baidu,google
```

### 高级搜索

```bash
# 指定数量
multi-search --query "关键词" --count 20 --engines brave,baidu

# 结果对比
multi-search --query "关键词" --compare
```

---

## 与单引擎对比

| 维度 | 单引擎 | 多引擎聚合 |
|------|--------|-----------|
| **覆盖面** | 单一来源 | 多来源 |
| **结果数** | 有限 | 更丰富 |
| **准确性** | 依赖单引擎 | 交叉验证 |
| **速度** | 快 | 稍慢 |

---

## 使用场景

### 场景一：全面信息收集

```bash
# 同时搜索多个引擎
multi-search --query "OpenClaw框架" --engines brave,baidu,google
```

### 场景二：结果对比分析

```bash
# 对比不同引擎结果
multi-search --query "AI Agent趋势" --compare
```

### 场景三：中英文信息

```bash
# 中英文搜索引擎组合
multi-search --query "AI技术" --engines baidu,google,brave
```

---

## 结果格式

```json
{
  "query": "搜索关键词",
  "total_results": 30,
  "engines": ["brave", "baidu", "google"],
  "results": [
    {
      "title": "标题",
      "url": "https://...",
      "snippet": "摘要",
      "source": "brave",
      "rank": 1
    }
  ]
}
```

---

## 与其他搜索技能对比

| 技能 | 特点 | 适用场景 |
|------|------|----------|
| **web_search** | Brave API | 英文内容 |
| **baidu-search** | 百度API | 中文内容 |
| **multi-search** | 多引擎聚合 | 全面收集 |

---

## 与其他技能协作

| 技能 | 协作场景 |
|------|----------|
| 深度研究 | 全面信息收集 |
| 网页净化 | 深度提取结果 |
| 竞品研究 | 竞品信息搜索 |
| SEO写作 | 内容研究 |

---

## 文件位置

| 文件 | 路径 |
|------|------|
| 技能包 | `/Users/bjd/intelligence/multi-search/` |
| SKILL.md | `/Users/bjd/.openclaw/skills/multi-search/SKILL.md` |

---

## 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.0.1 | 2026-03-18 | 初始版本，技能包导入 |

---

*技能创建: 2026-03-18 20:20*
*技能来源: 老庄发送*
*维护者: 姜小牙*