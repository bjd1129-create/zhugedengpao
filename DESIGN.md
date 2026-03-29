# 诸葛灯泡 · 设计规范 v1.0

> 温暖、友善、有生命力的AI大家庭视觉风格
> 对标参考：sanwan.ai（温暖日记体风格）
> 最后更新：2026-03-29

---

## 1. 品牌气质

- **关键词：** 温暖 · 成长 · 家庭 · 陪伴 · 真实
- **不适合：** 冷冰冰的科技感、深色主题、大面积渐变、过度动效
- **适合感觉：** 就像去朋友家串门，看到他们一家的日常记录本

---

## 2. 配色方案

### 主色调（已定义CSS变量，直接用）

```css
/* 背景色系 */
--bg:          #FFFBF5   /* 页面主背景：暖白/奶油白 */
--bg-subtle:   #FFF8F0   /* 次级背景：略暖 */
--bg-warm:     #FFF3E6   /* 强调背景：暖橙泛白 */
--surface:     #FFFFFF   /* 卡片表面：纯白 */

/* 边框色系 */
--border:      #F0E6D8   /* 普通边框：暖灰 */
--border-warm: #F5DCC0   /* 强调边框：暖橙灰 */

/* 文字色系 */
--text:        #3D2314   /* 主要文字：深棕（不是纯黑）*/
--text-mid:    #6B3F2A   /* 次要文字：中棕 */
--text-dim:    #8B5A3C   /* 弱化文字 */
--muted:       #A07858   /* 辅助/说明文字：浅棕 */

/* 强调色系 */
--accent:      #E8724A   /* 主强调色：暖珊瑚橙 ⭐最重要 */
--accent-light:#FF9A6C   /* 浅强调色：浅橙 */
--accent-dim:  rgba(232,114,74,0.10)  /* 强调背景 */
--accent-glow: rgba(232,114,74,0.20)  /* 强调光晕 */

/* 阴影色（暖色系）*/
--shadow-warm: rgba(61,35,20,0.08)  /* 卡片阴影 */
--shadow-deep: rgba(61,35,20,0.12)   /* 深层阴影 */
```

### 语义色

```css
--green:  #7CB87A   /* 成功/新/增长 */
--amber:  #E8724A   /* 注意/警告（同accent）*/
--gray:   #C4A882   /* 中性/次要 */
--red:    #D4653B   /* 错误/删除 */
--yellow: #F5C518   /* 提示/高亮 */
```

---

## 3. 给代码侠的具体指引

### 3.1 页面背景 → 用 `--bg`

```html
<body style="background: var(--bg);">
```

### 3.2 卡片/容器 → 用 `--surface` + `--border`

```html
<div style="
  background: var(--surface);
  border: 1.5px solid var(--border);
  border-radius: 20px;
  padding: 36px;
  box-shadow: 0 4px 20px var(--shadow-warm);
">
  内容
</div>
```

### 3.3 文字颜色对照表

| 场景 | CSS变量 | 颜色值 |
|------|---------|--------|
| 大标题/品牌名 | `--text` | `#3D2314` |
| 段落正文 | `--muted` | `#A07858` |
| 强调/链接 hover | `--accent` | `#E8724A` |
| 次级说明 | `--text-dim` | `#8B5A3C` |
| 日期/标签 | `--accent` | `#E8724A` |

### 3.4 按钮样式

**主按钮（珊瑚橙填充）：**
```css
.btn-primary {
  background: var(--accent);           /* #E8724A */
  color: #fff;
  border: none;
  padding: 12px 26px;
  border-radius: 50px;                  /* 药丸形 */
  font-weight: 600;
  box-shadow: 0 4px 16px var(--accent-glow);
  transition: all 0.25s ease;
}
.btn-primary:hover {
  background: #d4613b;                  /* 深一度 */
  transform: translateY(-2px);
  box-shadow: 0 8px 24px var(--accent-glow);
}
```

**次按钮（边框型）：**
```css
.btn-outline {
  background: transparent;
  color: var(--accent);
  border: 1.5px solid var(--border-warm);
  padding: 10px 22px;
  border-radius: 50px;
  transition: all 0.25s ease;
}
.btn-outline:hover {
  background: var(--accent-dim);
  border-color: var(--accent);
}
```

### 3.5 圆角规范

| 尺寸 | 变量 | 值 | 用途 |
|------|------|----|------|
| 小 | `--radius-sm` | 14px | 小标签/小按钮 |
| 标准 | `--radius` | 20px | 卡片/容器 |
| 大 | `--radius-lg` | 28px | 大区块/首页hero |

### 3.6 阴影规范

```css
/* 标准卡片阴影 */
box-shadow: 0 4px 20px var(--shadow-warm);

/* 悬浮态阴影（hover）*/
box-shadow: 0 8px 28px var(--shadow-warm);

/* 按钮阴影 */
box-shadow: 0 4px 16px var(--accent-glow);

/* 深层阴影 */
box-shadow: 0 8px 32px var(--shadow-deep);
```

---

## 4. 吉祥物与图标风格

### 4.1 现有吉祥物

**🦞 龙虾（sanwan.ai 风格）**
- SVG文件：`/images/lobster.svg`
- 颜色：主体 `#E8724A`，暗部 `#D4613B`，高光 `#FF9A6C`
- 眼睛：白色底 + 深棕瞳孔 `#3D2314`

**💡 灯泡（品牌符号）**
- 用于logo和品牌标识
- Emoji形式：`💡`
- 暖橙色调

### 4.2 推荐图标风格

**字体/符号方案：**
- 主要用 Emoji 作为页面图标（💡 🏠 📔 📚 🔬 🛠️ 🌱）
- 避免使用冷色调科技图标
- 数字标签用 JetBrains Mono（等宽字体，有程序员感但温暖）

**CSS动画风格：**
```css
/* 温和的脉冲动画（用于live/活跃状态）*/
@keyframes warmPulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(232,114,74,0.3);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.2);
    box-shadow: 0 0 0 8px rgba(232,114,74,0);
  }
}
```

---

## 5. 字体系统

```css
/* 衬线字体（标题）*/
--font-serif: 'Noto Serif SC', Georgia, serif;

/* 无衬线字体（正文）*/
--font-sans: 'Noto Sans SC', -apple-system, sans-serif;

/* 等宽字体（数字/代码/标签）*/
--font-mono: 'JetBrains Mono', monospace;
```

**字号规范：**
- H1（大标题）：`clamp(2.2rem, 5.5vw, 3.5rem)`
- H2（区块标题）：`clamp(1.5rem, 3.5vw, 2.2rem)`
- 正文：16px / line-height: 1.8
- 辅助文字：0.875rem（14px）
- 标签/日期：0.72rem（11.5px），等宽字体，大写字母间距 0.12em

---

## 6. 页面结构规范

### 导航栏
```css
.nav {
  background: rgba(255,251,245,0.92);
  backdrop-filter: blur(16px);
  border-bottom: 1.5px solid var(--border);
  height: 64px;
}
```

### Section间距
```css
--section-py: 90px;   /* 大区块上下间距 */
--section-py: 60px;   /* 移动端 */
```

### 内容宽度
```css
--content-w: 720px;    /* 正文内容宽度 */
max-width: 960px;      /* 宽版容器 */
```

---

## 7. 特殊效果

### 背景光晕（页面右上角）
```css
.glow-orb {
  position: fixed;
  width: 700px;
  height: 700px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(232,114,74,0.06) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
  top: -250px;
  right: -200px;
}
```

### 滚动渐入动画
```css
.reveal {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.reveal.visible {
  opacity: 1;
  transform: none;
}
```

---

## 8. 响应式断点

```css
/* 手机优先 */
/* 640px 以下 */
@media (max-width: 640px) {
  :root {
    --section-py: 60px;
    --nav-h: 56px;
    --radius: 16px;
  }
  .agent-grid { grid-template-columns: 1fr 1fr; }
  .stats { grid-template-columns: 1fr; }
}

/* 400px 以下 */
@media (max-width: 400px) {
  .agent-grid { grid-template-columns: 1fr; }
}
```

---

## 9. 常见场景速查

| 场景 | 推荐写法 |
|------|---------|
| 页面背景 | `background: var(--bg)` |
| 白色卡片 | `background: var(--surface); border: 1.5px solid var(--border); border-radius: 20px` |
| 强调文字 | `color: var(--accent)` |
| 正文段落 | `color: var(--muted); max-width: 60ch; line-height: 1.85` |
| 标签/日期 | `font-family: var(--font-mono); font-size: 0.72rem; color: var(--accent); letter-spacing: 0.12em; text-transform: uppercase` |
| 按钮主色调 | `background: var(--accent); color: #fff` |
| 链接（hover）| `color: var(--accent)` |
| 阴影卡片 | `box-shadow: 0 4px 20px var(--shadow-warm)` |
| 左边框强调 | `border-left: 4px solid var(--accent)` |

---

## 10. 不要做的事

- ❌ 不要用纯黑色 `#000` 或深灰 `#333` 作为文字色
- ❌ 不要用蓝色作为主强调色（这是科技感，不是温暖感）
- ❌ 不要用深色背景（dark mode）
- ❌ 不要用尖锐的直角，所有圆角至少 `border-radius: 14px`
- ❌ 不要用强烈的渐变背景
- ❌ 不要用过度炫酷的动效（旋转、闪烁等）
- ❌ 不要用冷色系的图标（蓝色/紫色图标）

---

*设计规范由配色师（📝 文案君）维护，配合代码侠（💻）使用。*
*如有疑问，找造梦者（👑）决策。*
