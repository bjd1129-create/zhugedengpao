# Find Skills技能

> **技能获取时间:** 2026-03-18 20:14
> **技能来源:** 老庄发送
> **版本:** 0.1.0
> **用途:** ClawHub技能搜索和发现

---

## 技能描述

在ClawHub技能市场搜索、发现、安装新技能，帮助快速找到需要的AI能力。

---

## 核心功能

| 功能 | 命令 | 说明 |
|------|------|------|
| **搜索技能** | `clawhub search <关键词>` | 按关键词搜索技能 |
| **安装技能** | `clawhub install <技能名>` | 安装技能到本地 |
| **列出技能** | `clawhub list` | 列出已安装技能 |
| **更新技能** | `clawhub update <技能名>` | 更新单个技能 |
| **更新全部** | `clawhub update --all` | 更新所有技能 |

---

## 使用场景

### 场景一：搜索技能

```bash
# 搜索特定技能
clawhub search baidu-search

# 搜索类型
clawhub search video
clawhub search music
clawhub search seo
```

### 场景二：安装技能

```bash
# 安装找到的技能
clawhub install baidu-search
clawhub install evolink-video
clawhub install music-generator
```

### 场景三：管理技能

```bash
# 查看已安装
clawhub list

# 更新技能
clawhub update baidu-search

# 更新所有
clawhub update --all
```

---

## 技能来源

### ClawHub市场

https://clawhub.com

**技能分类：**

| 类别 | 示例技能 |
|------|----------|
| **AI生成** | evolink-video, music-generator |
| **搜索** | baidu-search, brave-search |
| **数据分析** | data-analysis, chart-generator |
| **运营** | twitter-operations, linkedin-operations |
| **开发工具** | github-operations, api-gateway |
| **自动化** | auto-updater, agent-browser |

---

## 搜索技巧

### 关键词策略

| 策略 | 示例 |
|------|------|
| **功能关键词** | `search`, `video`, `music` |
| **平台关键词** | `twitter`, `discord`, `slack` |
| **技术关键词** | `api`, `browser`, `pdf` |
| **用途关键词** | `seo`, `analytics`, `report` |

### 高效搜索

```bash
# 精确搜索
clawhub search video
clawhub search "pdf generator"

# 发现相关
clawhub search ai
clawhub search automation
```

---

## 技能评估

### 安装前评估

| 维度 | 检查项 |
|------|--------|
| **功能匹配** | 是否满足需求 |
| **依赖要求** | Python/Node版本 |
| **API需求** | 需要哪些API Key |
| **维护状态** | 最近更新时间 |

### 安装后验证

```bash
# 查看技能文档
clawhub docs <技能名>

# 检查技能状态
clawhub doctor <技能名>
```

---

## 技能库管理

### 已安装技能

当前已安装：**79个**

### 技能分类

| 类别 | 数量 |
|------|------|
| 运营类 | 15+ |
| 研究类 | 10+ |
| 生成类 | 8+ |
| 工具类 | 20+ |
| 其他 | 25+ |

---

## 与其他技能协作

| 技能 | 协作场景 |
|------|----------|
| Auto-Updater | 自动更新技能 |
| 安全审计 | 技能安全检查 |
| 自我进化引擎 | 技能能力扩展 |

---

## 文件位置

| 文件 | 路径 |
|------|------|
| 技能包 | `/Users/bjd/intelligence/find-skills/` |
| SKILL.md | `/Users/bjd/intelligence/find-skills/SKILL.md` |
| 本地技能库 | `~/.openclaw/skills/` |

---

## 链接

- **ClawHub市场:** https://clawhub.com
- **文档:** https://docs.clawhub.com

---

## 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 0.1.0 | 2026-03-18 | 初始版本，技能包导入 |

---

*技能创建: 2026-03-18 20:14*
*技能来源: 老庄发送*
*维护者: 姜小牙*