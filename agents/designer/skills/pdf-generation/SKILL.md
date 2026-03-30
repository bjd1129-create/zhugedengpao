# PDF生成技能

> **技能获取时间:** 2026-03-18 19:45
> **技能来源:** 老庄指示
> **适用场景:** Markdown转PDF、报告生成、文档输出

---

## 技能描述

将Markdown文档转换为PDF格式，支持中文字体、代码高亮、表格、图片、自定义CSS样式。

---

## 安装方式

```bash
# 安装完整技能
clawhub install md-to-pdf

# 或单独安装依赖
brew install pandoc
# Chrome已安装则无需额外安装
```

---

## 核心命令

### 基础转换（两步法）

```bash
# Step 1: Markdown转HTML
pandoc input.md -o /tmp/output.html --standalone --metadata title="标题"

# Step 2: HTML转PDF（Chrome Headless）
google-chrome --headless --disable-gpu --no-sandbox \
  --print-to-pdf=/tmp/output.pdf /tmp/output.html
```

---

## 支持功能

| 功能 | 说明 |
|------|------|
| **中文字体** | 支持中文显示 |
| **代码高亮** | 语法高亮显示 |
| **表格** | Markdown表格渲染 |
| **图片** | 支持嵌入图片 |
| **自定义CSS** | 自定义样式表 |

---

## 使用场景

### 场景一：研究报告转PDF

```bash
# 转换研究报告
pandoc research_report.md -o /tmp/report.html --standalone --metadata title="AI-EVO研究报告"

google-chrome --headless --disable-gpu --no-sandbox \
  --print-to-pdf=/tmp/research_report.pdf /tmp/report.html

# 移动到目标位置
mv /tmp/research_report.pdf ~/Documents/
```

### 场景二：带样式的PDF生成

```bash
# 使用自定义CSS
pandoc input.md -o /tmp/output.html --standalone --css=style.css --metadata title="文档标题"

google-chrome --headless --disable-gpu --no-sandbox \
  --print-to-pdf=/tmp/output.pdf /tmp/output.html
```

### 场景三：代码文档转PDF

```bash
# 代码高亮
pandoc code_doc.md -o /tmp/code_doc.html --standalone --highlight-style=tango --metadata title="API文档"

google-chrome --headless --disable-gpu --no-sandbox \
  --print-to-pdf=/tmp/code_doc.pdf /tmp/code_doc.html
```

---

## 自定义CSS示例

```css
/* style.css */
body {
  font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
  font-size: 14px;
  line-height: 1.8;
  max-width: 800px;
  margin: 0 auto;
  padding: 40px;
}

h1 {
  color: #333;
  border-bottom: 2px solid #4A90E2;
  padding-bottom: 10px;
}

h2 {
  color: #4A90E2;
  margin-top: 30px;
}

code {
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: "Monaco", "Consolas", monospace;
}

pre {
  background: #2d2d2d;
  color: #f8f8f2;
  padding: 20px;
  border-radius: 8px;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}

th, td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

th {
  background: #4A90E2;
  color: white;
}
```

---

## 完整工作流

```
Markdown文件
    │
    ▼
┌─────────────────┐
│ pandoc转HTML    │
│ --standalone    │
│ --css=style.css │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Chrome Headless │
│ --print-to-pdf  │
└────────┬────────┘
         │
         ▼
    PDF文件
```

---

## 注意事项

| 注意项 | 说明 |
|--------|------|
| **Chrome路径** | 确保google-chrome在PATH中 |
| **中文字体** | 系统需安装中文字体 |
| **图片路径** | 使用绝对路径或确保相对路径正确 |
| **PDF大小** | 复杂内容可能导致PDF较大 |

---

## 与其他技能协作

| 技能 | 协作场景 |
|------|----------|
| 飞书文档 | 导出Markdown后转PDF |
| 深度研究 | 研究报告转PDF分发 |
| AI文本人性化 | 处理后再转PDF |

---

## 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-18 | 初始版本，记录技能获取 |

---

*技能创建: 2026-03-18 19:45*
*技能来源: 老庄指示*
*维护者: 姜小牙*