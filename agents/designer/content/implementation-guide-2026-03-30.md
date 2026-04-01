# 视觉风格差异化 · 实施指南
配色师 · 2026-03-30

---

## 📋 实施清单

### ✅ 1. 引入新增 CSS 文件

在 `index.html` 的 `<head>` 中加入（在现有样式之后）：

```html
<!-- 小花视觉增强 -->
<link rel="stylesheet" href="agents/designer/content/color-palette-2026-03-30.css">
<link rel="stylesheet" href="agents/designer/content/mascot-enhancement-2026-03-30.css">
```

或内联到 `<style>` 标签中。

---

### ✅ 2. 替换浮动吉祥物（index.html 第 243 行附近）

**当前代码（emoji版）：**
```html
<div class="float-mascot">
  <div class="float-bubble">
    <div class="bubble-text">来找我玩呀~</div>
    <div class="bubble-tail"></div>
  </div>
  <div class="float-lobster">🦞</div>  ← 替换这里
</div>
```

**替换为（Garfield lobster 图片版）：**
```html
<div class="float-mascot">
  <div class="float-bubble">
    <div class="bubble-text">来找我玩呀~ 🦞</div>
    <div class="bubble-tail"></div>
  </div>
  <div class="float-mascot-img">
    <img src="images/garfield_lobster_001_01_office_v1.png" 
         alt="小花" 
         width="72" 
         height="72"
         style="width:100%;height:100%;object-fit:cover;border-radius:50%;">
  </div>
</div>
```

---

### ✅ 3. 颜色值批量替换（style.css）

将以下硬编码颜色值替换：

| 原值 | 替换为 | 出现位置 |
|------|--------|---------|
| `#c0392b` | `#E07A5A` | 全局硬编码颜色 |
| `#a93226` | `#C4614A` | hover 状态 |
| `#E8724A` | `#E8897A` | accent 相关 |
| `#FFFBF5` | `#FFF8E1` | body background |
| `#FFF8F0` | `#FFF8E1` | nav/subtle bg |
| `#FFF3E6` | `#FFF0E3` | warm bg |

**执行命令（推荐）：**
```bash
cd /Users/bjd/Desktop/ZhugeDengpao-Team
sed -i '' 's/#c0392b/#E07A5A/g' css/style.css
sed -i '' 's/#a93226/#C4614A/g' css/style.css
sed -i '' 's/#E8724A/#E8897A/g' css/style.css
sed -i '' 's/#FFFBF5/#FFF8E1/g' css/style.css
sed -i '' 's/#FFF8F0/#FFF8E1/g' css/style.css
sed -i '' 's/#FFF3E6/#FFF0E3/g' css/style.css
```

---

### ✅ 4. Hero 区域添加 Garfield Lobster 形象

在 `index.html` 的 hero 区域（约 40-60 行），在 `.hero-scene` 后面添加：

```html
<!-- 小花 IP 形象点缀 -->
<div class="hero-mascot" style="margin-top: 16px;">
  <div class="xiaohua-deco-ring"></div>
  <img class="hero-mascot-img" 
       src="images/garfield_lobster_008_01_office_v8.png" 
       alt="小花">
</div>
```

---

### ✅ 5. 添加手写字体 Google Fonts（已有，可确认）

确认 index.html 已有（应已有，无需修改）：
```html
<link href="https://fonts.googleapis.com/css2?family=Long+Cang&family=ZCOOL+KuaiLe&family=Ma+Shan+Zheng&display=swap" rel="stylesheet">
```

---

### ✅ 6. 关于页/故事页添加 IP 展示

在 `about.html` 或故事相关区域添加：

```html
<div class="ip-showcase">
  <img src="images/garfield_lobster_005_01_office_v5.png" alt="小花">
  <div class="ip-showcase-text">
    <h3>👋 我是小花</h3>
    <p class="signature">老庄的 AI 伙伴，凌晨4点的常客~</p>
    <span class="brand-tag">🦞 龙虾一族</span>
  </div>
</div>
```

---

## 🎨 视觉效果预览

### 颜色对比
```
原方案（偏冷红）        →  新方案（暖男珊瑚红）
#c0392b (饱和红)       →  #E07A5A (柔和珊瑚)
#FFFBF5 (冷白)         →  #FFF8E1 (暖黄米白)
```

### 字体层次
```
ZCOOL KuaiLe  → 活泼标题（品牌感）
Ma Shan Zheng → 引用/签名（亲和力）
Noto Sans SC  → 正文（可读性）
Long Cang     → 装饰书法（文化感）
```

### 氛围转变
```
Before: 技术官网风格（严肃、专业、冷调）
After:  温暖朋友圈风格（亲切、有爱、有故事）
```

---

## 📁 产出文件清单

| 文件 | 路径 | 用途 |
|------|------|------|
| 配色变量 | `agents/designer/content/color-palette-2026-03-30.css` | CSS 变量定义 |
| 吉祥物增强 | `agents/designer/content/mascot-enhancement-2026-03-30.css` | IP 形象样式 |
| 本指南 | `agents/designer/content/implementation-guide-2026-03-30.md` | 实施说明 |

---

## 🔄 后续建议

1. **字体文件本地化**：将 Google Fonts 下载到本地，避免 CDN 加载慢
2. **吉祥物表情包系列**：考虑制作不同场景的 Garfield lobster 表情（开心、好奇、加班等）
3. **品牌插图**：考虑为每个主要页面定制一张 Garfield lobster 插图
4. **深色模式兼容**：未来如需深色模式，保持暖色调特色
5. **Favicon**：考虑用 Garfield lobster 形象做 favicon.svg

---

_配色师 · 2026-03-30 · 温暖交付完毕_
