# AI文本人性化技能

> **技能获取时间:** 2026-03-18 19:38
> **技能来源:** 老庄指示
> **适用场景:** AI生成文本的人性化处理、风格转换、AI痕迹检测

---

## 技能描述

对AI生成的中文文本进行人性化处理，检测AI痕迹，转换写作风格，使内容更加自然真实。

---

## 核心功能

### 1. AI痕迹检测（16种模式）

```bash
python3 clawhub install humanize-chinese/scripts/detect_cn.py 文件.txt
```

**检测内容：**
- AI常用句式
- 过于工整的段落
- 机械化的表达
- 不自然的过渡

---

### 2. 人性化处理

#### 基础人性化
```bash
python3 clawhub install humanize-chinese/scripts/humanize_cn.py input.txt -o output.txt
```

#### 指定场景
```bash
# 社媒场景
python3 .../humanize_cn.py input.txt --scene social -o output.txt

# 技术场景
python3 .../humanize_cn.py input.txt --scene tech -o output.txt

# 正式场景
python3 .../humanize_cn.py input.txt --scene formal -o output.txt
```

---

### 3. 风格转换（6种）

| 风格 | 命令 | 适用场景 |
|------|------|----------|
| **口语化** | `--style casual` | 日常聊天、评论区 |
| **知乎风** | `--style zhihu` | 知乎回答、专业讨论 |
| **小红书风** | `--style xiaohongshu` | 小红书笔记、种草 |
| **微信公众号风** | `--style wechat` | 公众号文章 |
| **学术风** | `--style academic` | 论文、研究报告 |
| **文艺风** | `--style literary` | 散文、随笔 |

**命令示例：**
```bash
# 口语化
python3 .../style_cn.py input.txt --style casual -o output.txt

# 知乎风
python3 .../style_cn.py input.txt --style zhihu -o output.txt

# 小红书风
python3 .../style_cn.py input.txt --style xiaohongshu -o output.txt

# 微信公众号风
python3 .../style_cn.py input.txt --style wechat -o output.txt

# 学术风
python3 .../style_cn.py input.txt --style academic -o output.txt

# 文艺风
python3 .../style_cn.py input.txt --style literary -o output.txt
```

---

### 4. 前后对比

```bash
python3 .../compare_cn.py input.txt -o clean.txt
```

---

## 使用场景

### 场景一：研究报告人性化

```bash
# 1. 检测AI痕迹
python3 .../detect_cn.py report.md

# 2. 人性化处理
python3 .../humanize_cn.py report.md --scene formal -o report_human.md

# 3. 风格调整
python3 .../style_cn.py report_human.md --style academic -o report_final.md
```

### 场景二：社媒内容优化

```bash
# 小红书风格
python3 .../style_cn.py draft.txt --style xiaohongshu -o xiaohongshu_post.txt

# 微信公众号风格
python3 .../style_cn.py draft.txt --style wechat -o wechat_article.txt
```

### 场景三：知乎回答优化

```bash
# 知乎风格
python3 .../style_cn.py answer.txt --style zhihu -o zhihu_answer.txt
```

---

## 工作流程

```
原始AI文本
    │
    ▼
┌─────────────────┐
│ 1. AI痕迹检测   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. 人性化处理   │
│ (指定场景)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. 风格转换     │
│ (选择风格)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. 前后对比     │
└────────┬────────┘
         │
         ▼
    输出人性化文本
```

---

## 注意事项

| 注意项 | 说明 |
|--------|------|
| **保留核心内容** | 人性化不改变原文核心意思 |
| **场景适配** | 根据发布平台选择场景 |
| **风格一致性** | 同一系列内容保持风格统一 |
| **人工校验** | 处理后建议人工审核 |

---

## 与其他技能协作

| 技能 | 协作场景 |
|------|----------|
| Twitter运营 | 发推前人性化处理 |
| 飞书文档 | 文档内容优化 |
| 深度研究 | 研究报告人性化 |

---

## 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-18 | 初始版本，记录技能获取 |

---

*技能创建: 2026-03-18 19:38*
*技能来源: 老庄指示*
*维护者: 姜小牙*