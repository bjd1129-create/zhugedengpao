# SKILL.md - 深度研究技能

> 记录路径：2026-03-29

---

## 触发条件

用户要求研究某个主题、收集市场数据、分析竞争对手、做竞品调研时使用此技能。

---

## 研究流程

### 第一步：多引擎搜索

```bash
# 主要用 DuckDuckGo
web_search(query="研究主题", count=10)
web_search(query="研究主题 site:专业网站", count=10)

# freshness 参数：pd=当天, pw=本周, pm=本月, py=本年
web_search(query="主题", count=10, freshness="pw")
```

### 第二步：提取正文

```python
# 对有价值的链接提取正文
web_fetch(url="URL", extractMode="markdown", maxChars=15000)
```

### 第三步：交叉验证

- 至少验证3个来源的数据
- 记录每条数据的来源URL
- 标注数据可靠性（权威媒体 > 博客 > 论坛）

### 第四步：输出结构化报告

输出到 `content/YYYY-MM-DD-研究主题.md`

**报告结构：**
```
# 研究主题

## 核心数据（关键数字+来源）
## 背景/现状
## 关键发现
## 竞争格局
## 趋势分析
## 对我们的意义/行动建议
## 参考来源
```

---

## 搜索技巧

```bash
# 精确搜索
"exact phrase" 

# 排除
keyword -excluded

# 站内搜索
site:example.com topic

# 文件类型
filetype:pdf topic

# 多个关键词
topic1 OR topic2

# 价格/数据
pricing 2026 OR 2025
```

---

## 反爬处理

```bash
# 带User-Agent
curl -s -A 'Mozilla/5.0 (iPhone...)' 'URL'

# 微信公众号等
python3 extract.py
```

---

## 记录要求

**每次研究必须记录：**
1. 研究目标
2. 使用的数据源（至少3个）
3. 关键发现
4. 知识库路径
5. 下一步行动

---

## 快捷命令

```bash
# 一键搜索
web_search(query="your topic", count=10)

# 提取+搜索组合
web_search(query="topic") && web_fetch(url="relevant_url")
```

---

*诸葛灯泡团队深度研究流程 | 2026-03-29*
