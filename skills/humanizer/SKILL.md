# Humanizer文本人性化技能

> **技能获取时间:** 2026-03-18 20:17
> **技能来源:** 老庄发送
> **版本:** 1.0.0
> **用途:** AI生成文本人性化处理

---

## 技能描述

对AI生成的文本进行人性化处理，检测AI痕迹，转换写作风格，使内容更加自然真实。

---

## 核心功能

| 功能 | 说明 |
|------|------|
| **AI痕迹检测** | 识别AI生成特征 |
| **人性化处理** | 自然化文本表达 |
| **风格转换** | 多种写作风格 |
| **前后对比** | 处理效果对比 |

---

## 与ai-text-humanize技能对比

两个技能功能类似，可互相补充：

| 维度 | humanizer | ai-text-humanize |
|------|-----------|------------------|
| AI检测 | 支持 | 支持（16种模式） |
| 场景适配 | 通用 | social/tech/formal |
| 风格转换 | 多种风格 | 6种中文风格 |
| 语言支持 | 通用 | 中文优化 |

---

## 使用方式

### 基础人性化

```bash
# 处理文本
humanizer input.txt -o output.txt

# 指定强度
humanizer input.txt --intensity high -o output.txt
```

### 风格转换

```bash
# 正式风格
humanizer input.txt --style formal -o output.txt

# 口语风格
humanizer input.txt --style casual -o output.txt

# 技术风格
humanizer input.txt --style technical -o output.txt
```

---

## 处理前后对比

```markdown
## 处理前（AI痕迹明显）

在当今数字化时代，人工智能技术正在快速发展。
这种技术具有革命性的意义，将深刻改变我们的生活方式。

## 处理后（更自然）

AI发展很快，已经渗透到生活的方方面面。
这不仅是技术升级，更是生活方式的变革。
```

---

## AI痕迹检测

### 常见AI痕迹

| 痕迹 | 说明 |
|------|------|
| 开头模式 | "在当今..."、"随着..." |
| 过度工整 | 段落结构过于整齐 |
| 词汇重复 | 频繁使用"进一步"、"从而" |
| 缺乏个性 | 没有个人观点和情感 |
| 空洞表达 | "具有重要意义"、"深刻影响" |

### 检测结果

```json
{
  "ai_probability": 0.85,
  "detected_patterns": [
    "开头套话",
    "过度使用连接词",
    "缺乏个人风格"
  ],
  "suggestions": [
    "改写开头",
    "添加个人观点",
    "使用更口语化表达"
  ]
}
```

---

## 使用场景

### 场景一：报告人性化

```bash
humanizer report.md --style formal -o report_human.md
```

### 场景二：社媒内容

```bash
humanizer draft.txt --style casual -o social_post.txt
```

### 场景三：技术文档

```bash
humanizer docs.md --style technical -o docs_final.md
```

---

## 与其他技能协作

| 技能 | 协作场景 |
|------|----------|
| SEO写作 | SEO文章人性化 |
| 飞书文档 | 文档内容优化 |
| Twitter运营 | 推文人性化 |
| LinkedIn运营 | 专业内容优化 |

---

## 文件位置

| 文件 | 路径 |
|------|------|
| 技能包 | `/Users/bjd/intelligence/humanizer/` |
| SKILL.md | `/Users/bjd/.openclaw/skills/humanizer/SKILL.md` |

---

## 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-18 | 初始版本，技能包导入 |

---

*技能创建: 2026-03-18 20:17*
*技能来源: 老庄发送*
*维护者: 姜小牙*