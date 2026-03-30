# 办公室页面视觉设计方案
**配色师出品 · 2026-03-30**

---

## 1. 页面定位与调性

### 核心定位
- **页面名称**：老庄与小花办公室（/office.html 改造）
- **副标题**：🏠 像家一样的AI工作室
- **目标感受**：温馨、真实、有爱 —— 就像推开朋友家的门，看到他们认真工作的样子

### 调性关键词
| 关键词 | 视觉表达 |
|--------|----------|
| 温馨 | 暖白底色 + 龙虾红点缀 + 柔和光晕 |
| 真实 | 真实的办公室场景照片（插画风格） |
| 有爱 | 花朵/绿植/咖啡等生活化元素 |
| 像家 | 木质桌面、家庭角落氛围、散落的小物件 |

---

## 2. 配色方案（基于现有 DESIGN.md 扩展）

### 核心色板
```css
/* === 已在 DESIGN.md 定义，直接复用 === */
--bg:          #FFFBF5   /* 暖白主背景 */
--bg-subtle:   #FFF8F0   /* 略暖次级背景 */
--bg-warm:     #FFF3E6   /* 暖橙泛白背景 */
--surface:     #FFFFFF   /* 卡片表面 */
--accent:      #E8724A   /* 龙虾红/珊瑚橙 */
--text:        #3D2314   /* 深棕文字 */
--muted:       #A07858   /* 辅助文字 */

/* === 新增：家的暖色调 === */
--home-cream:    #FFF5E8   /* 奶油白（家庭角落）*/
--home-wood:     #C4956A   /* 木质棕（书桌）*/
--home-wood-deep:#8B5E3C   /* 深木色（强调）*/
--home-green:    #7CB87A   /* 绿植绿 */
--home-green-dim:#E8F5E4   /* 浅绿背景 */
--home-gold:     #E8B86D   /* 暖金光晕 */
--home-glow:     rgba(232,184,109,0.15)  /* 暖光效果 */
```

### 氛围渐变
```css
/* 办公室温馨氛围渐变 */
--office-ambience:
  linear-gradient(135deg, #FFF8F0 0%, #FFF3E6 50%, #FFE8D6 100%);

/* 灯光光晕效果 */
--lamp-glow:
  radial-gradient(ellipse at top, rgba(255,220,150,0.20) 0%, transparent 60%);
```

---

## 3. 页面布局结构

### 整体布局
```
┌─────────────────────────────────────────────┐
│  导航栏（固定顶部，暖白毛玻璃）              │
├─────────────────────────────────────────────┤
│  Hero 区域                                  │
│  ┌─────────────────────────────────────┐    │
│  │  办公室场景大图（插画风格）          │    │
│  │  小花在电脑前工作 + 老庄在背景        │    │
│  │  春节元素点缀（小灯笼/福字）          │    │
│  │  温暖光线效果                         │    │
│  └─────────────────────────────────────┘    │
│  标题：老庄与小花的办公室                    │
│  副标题：🏠 像家一样的AI工作室              │
├─────────────────────────────────────────────┤
│  氛围标语区                                  │
│  "这里没有冰冷的工位，只有像家一样的工作台"    │
├─────────────────────────────────────────────┤
│  工作场景轮播/画廊                           │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐               │
│  │场景1│ │场景2│ │场景3│ │场景4│  →         │
│  └────┘ └────┘ └────┘ └────┘               │
│  文字：书桌一角 / 阳光角落 / 咖啡时光 / ...   │
├─────────────────────────────────────────────┤
│  小花工作台特写                              │
│  ┌─────────────────────────────────────┐    │
│  │  小花IP（大图）+ 工作状态描述         │    │
│  │  "正在用AI帮老庄写代码..."            │    │
│  └─────────────────────────────────────┘    │
├─────────────────────────────────────────────┤
│  办公室细节角落（拼图式卡片）                │
│  ┌────────┐ ┌────────┐ ┌────────┐          │
│  │☕咖啡杯 │ │🌱绿植   │ │📚书架  │          │
│  │龙年福字 │ │阳光角落 │ │温暖台灯│          │
│  └────────┘ └────────┘ └────────┘          │
├─────────────────────────────────────────────┤
│  团队状态（保留现有）                        │
│  ···                                         │
└─────────────────────────────────────────────┘
```

---

## 4. CSS 样式建议

### 4.1 Hero 区域
```css
.office-hero {
  position: relative;
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
  padding: 80px 24px 60px;
  text-align: center;
}

.office-hero__scene {
  position: relative;
  width: 100%;
  max-width: 900px;
  margin: 0 auto 48px;
  border-radius: 28px;
  overflow: hidden;
  box-shadow:
    0 8px 40px rgba(61,35,20,0.12),
    0 0 0 1px rgba(232,114,74,0.10);
}

/* 场景图片容器 */
.office-hero__scene img {
  width: 100%;
  height: auto;
  display: block;
}

/* 春节光晕叠加层 */
.office-hero__scene::after {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 20% 20%, rgba(255,220,150,0.15) 0%, transparent 40%),
    radial-gradient(ellipse at 80% 80%, rgba(232,114,74,0.08) 0%, transparent 40%);
  pointer-events: none;
}

/* 场景标题叠加 */
.office-hero__label {
  position: absolute;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(255,251,245,0.90);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(232,114,74,0.20);
  border-radius: 50px;
  padding: 8px 20px;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--accent);
  letter-spacing: 0.10em;
  white-space: nowrap;
}
```

### 4.2 氛围标语区
```css
.office-tagline {
  text-align: center;
  padding: 40px 24px;
  background: linear-gradient(135deg, var(--home-cream) 0%, #FFF8EE 100%);
  border-top: 1px solid rgba(232,114,74,0.10);
  border-bottom: 1px solid rgba(232,114,74,0.10);
  margin: 0;
}

.office-tagline p {
  font-family: var(--font-serif);
  font-size: clamp(1.1rem, 2.5vw, 1.4rem);
  color: var(--text-mid);
  max-width: 52ch;
  margin: 0 auto;
  line-height: 1.7;
}
```

### 4.3 场景轮播/画廊
```css
.office-gallery {
  padding: 60px 0;
  overflow: hidden;
}

.office-gallery__scroll {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  padding: 8px 24px 20px;
  scroll-snap-type: x mandatory;
  scrollbar-width: none;
}

.office-gallery__scroll::-webkit-scrollbar { display: none; }

.office-gallery__item {
  flex-shrink: 0;
  width: 260px;
  scroll-snap-align: start;
  border-radius: 20px;
  overflow: hidden;
  position: relative;
  box-shadow: 0 4px 20px var(--shadow-warm);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.office-gallery__item:hover {
  transform: translateY(-6px) scale(1.02);
  box-shadow: 0 16px 48px rgba(61,35,20,0.15);
}

.office-gallery__item img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  display: block;
}

.office-gallery__caption {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 40px 16px 14px;
  background: linear-gradient(transparent, rgba(61,35,20,0.70));
  color: #fff;
  font-size: 0.80rem;
  text-align: center;
}
```

### 4.4 小花工作台特写
```css
.office-xiaohua {
  padding: 60px 24px;
  max-width: 900px;
  margin: 0 auto;
}

.office-xiaohua__card {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 40px;
  align-items: center;
  background: var(--surface);
  border: 1.5px solid var(--border);
  border-radius: 28px;
  padding: 40px;
  box-shadow: 0 8px 32px var(--shadow-warm);
}

@media (max-width: 640px) {
  .office-xiaohua__card {
    grid-template-columns: 1fr;
    gap: 24px;
    padding: 28px 24px;
  }
}

.office-xiaohua__avatar {
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 8px 32px var(--accent-glow);
}

.office-xiaohua__avatar img {
  width: 100%;
  height: auto;
  display: block;
}

.office-xiaohua__content h3 {
  font-family: var(--font-serif);
  font-size: 1.5rem;
  color: var(--text);
  margin-bottom: 12px;
}

.office-xiaohua__status {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--green);
  margin-bottom: 16px;
}

.office-xiaohua__status::before {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--green);
  animation: warmPulse 2s ease-in-out infinite;
}

.office-xiaohua__desc {
  font-size: 0.95rem;
  color: var(--muted);
  line-height: 1.8;
}
```

### 4.5 办公室细节角落（拼图卡片）
```css
.office-corner-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  padding: 0 24px 80px;
  max-width: 960px;
  margin: 0 auto;
}

.office-corner-card {
  background: var(--surface);
  border: 1.5px solid var(--border);
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.3s ease;
  position: relative;
}

.office-corner-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 36px var(--shadow-warm);
  border-color: var(--home-wood);
}

.office-corner-card img {
  width: 100%;
  height: 160px;
  object-fit: cover;
  display: block;
}

.office-corner-card__body {
  padding: 18px 20px;
}

.office-corner-card__emoji {
  font-size: 1.8rem;
  margin-bottom: 8px;
  display: block;
}

.office-corner-card__title {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 6px;
}

.office-corner-card__desc {
  font-size: 0.80rem;
  color: var(--muted);
  line-height: 1.6;
}

/* 春节点缀卡片（特殊样式）*/
.office-corner-card--spring {
  border-color: rgba(232,114,74,0.25);
  background: linear-gradient(135deg, #FFFBF5 0%, #FFF5E8 100%);
}

.office-corner-card--spring::before {
  content: '';
  position: absolute;
  top: -20px;
  right: -20px;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(232,114,74,0.08) 0%, transparent 70%);
  pointer-events: none;
}
```

### 4.6 温暖光晕动画
```css
/* 背景暖光效果 */
.office-warm-orb {
  position: fixed;
  width: 600px;
  height: 600px;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    rgba(255,220,150,0.08) 0%,
    rgba(232,184,109,0.05) 40%,
    transparent 70%
  );
  pointer-events: none;
  z-index: 0;
}

.office-warm-orb--left {
  top: 20%;
  left: -300px;
}

.office-warm-orb--right {
  bottom: 10%;
  right: -250px;
  background: radial-gradient(
    circle,
    rgba(232,114,74,0.06) 0%,
    transparent 70%
  );
}

/* 春节灯笼摇曳动画 */
@keyframes lanternSway {
  0%, 100% { transform: rotate(-4deg); }
  50% { transform: rotate(4deg); }
}

.spring-lantern {
  animation: lanternSway 4s ease-in-out infinite;
  transform-origin: top center;
}

/* 场景入场动画 */
@keyframes sceneReveal {
  from {
    opacity: 0;
    transform: scale(0.96) translateY(12px);
  }
  to {
    opacity: 1;
    transform: none;
  }
}

.office-hero__scene {
  animation: sceneReveal 0.8s ease-out both;
}

.office-gallery__item {
  opacity: 0;
  animation: sceneReveal 0.6s ease-out forwards;
}

.office-gallery__item:nth-child(1) { animation-delay: 0.1s; }
.office-gallery__item:nth-child(2) { animation-delay: 0.2s; }
.office-gallery__item:nth-child(3) { animation-delay: 0.3s; }
.office-gallery__item:nth-child(4) { animation-delay: 0.4s; }
.office-gallery__item:nth-child(5) { animation-delay: 0.5s; }
```

---

## 5. 需要的图片素材列表

### 5.1 已有素材（可直接用）
```
/images/garfield_lobster_001_01_office_v1.png   ← 办公室场景1
/images/garfield_lobster_002_01_office_v2.png   ← 办公室场景2
/images/garfield_lobster_003_01_office_v3.png   ← 办公室场景3
/images/garfield_lobster_004_01_office_v4.png   ← 办公室场景4
/images/garfield_lobster_005_01_office_v5.png   ← 办公室场景5
/images/garfield_lobster_006_01_office_v6.png   ← 办公室场景6
/images/garfield_lobster_007_01_office_v7.png   ← 办公室场景7
/images/garfield_lobster_008_01_office_v8.png   ← 办公室场景8
/images/garfield_lobster_009_01_office_v9.png   ← 办公室场景9
/images/garfield_lobster_010_01_office_v10.png  ← 办公室场景10
/images/garfield_lobster_011_01_office_v11.png  ← 办公室场景11
/images/garfield_lobster_012_01_office_v12.png  ← 办公室场景12
/images/lobster.svg                              ← 龙虾SVG图标
/images/xiaohua.jpg                              ← 小花头像
/images/xiaohua_banner.jpg                       ← 小花Banner
```

### 5.2 需要新生成的素材

#### A. Hero 场景大图（1张）
```
描述：老庄与小花办公室全景
内容：
- 温馨的书房/办公室环境（木质书桌）
- 小花（穿龙虾衣服的加菲猫）坐在电脑前工作
- 背景有老庄的模糊身影（或者不在画面中）
- 电脑屏幕显示代码/AI工作界面
- 春节元素：小灯笼挂在角落、中国结、福字贴
- 阳光从窗户洒入、温暖的光线
- 桌上有咖啡杯、绿植（龟背竹/虎皮兰）
- 家庭书架/CD架角落

风格：插画/动漫风格，暖色调
尺寸：1200×600px 或更高
```

#### B. 场景轮播图（4-5张）
```
场景1：书桌一角
- 特写：电脑屏幕+咖啡杯+小龙虾吉祥物
- 文字：专注coding中

场景2：阳光角落
- 窗外阳光洒入、绿植、温暖光线
- 文字：午后时光

场景3：咖啡与代码
- 咖啡杯+键盘+眼镜
- 文字：咖啡助力

场景4：春节氛围
- 小灯笼+福字+年味布置
- 文字：龙年大吉

场景5：团队协作
- 小花和老庄一起工作的画面
- 文字：我们一起搞AI
```

#### C. 办公室细节图（4-6张）
```
1. 咖啡杯特写
   - 龙虾图案的马克杯
   - 旁边有饼干/小零食

2. 绿植角落
   - 龟背竹或虎皮兰
   - 阳光透进来的感觉

3. 温暖台灯
   - 复古台灯
   - 暖黄灯光洒在桌面上

4. 龙年福字
   - 红底金色福字
   - 贴在屏幕旁边

5. 小灯笼装饰
   - 红色小灯笼
   - 挂在书架上

6. 工作书籍
   - 技术书籍+植物
   - 放在书架上
```

---

## 6. 视觉氛围实现建议

### 6.1 温暖光感
- 在页面背景叠加淡黄色的渐变光晕
- 用 CSS `radial-gradient` 实现光点效果
- 右下角和左上角放置柔和的光晕元素

### 6.2 春节氛围
- 小灯笼用 CSS `animation` 实现轻微摇曳
- 福字用红色+金色边框
- 可以加入龙年贴纸元素

### 6.3 家的感觉
- 散落的物件（咖啡杯、笔记本、绿植）
- 暖色调的木质纹理（可用 CSS 渐变模拟）
- 不那么整齐的"真实"感

---

## 7. 交付物清单

| 序号 | 交付物 | 状态 | 备注 |
|------|--------|------|------|
| 1 | 本视觉设计方案文档 | ✅ 完成 | 本文件 |
| 2 | CSS 样式建议 | ✅ 完成 | 第4节 |
| 3 | 图片素材列表 | ✅ 完成 | 第5节 |
| 4 | 页面布局草图 | ✅ 完成 | 第3节ASCII图 |
| 5 | 新图生成 Prompt | ✅ 完成 | 见下方 |

---

## 附录：图片生成 Prompt 参考

### Hero 场景大图
```
A warm cozy home office illustration, Chinese New Year atmosphere.
A fat orange Garfield cat wearing a lobster red hoodie, sitting at
a wooden desk working on a computer. The computer screen shows
colorful code and AI interface. A red paper cutting (福字) is
posted on the wall. Small red Chinese lanterns hang in the corner.
A cup of coffee steams on the desk. A potted Monstera plant sits
near the window. Warm afternoon sunlight streams through the
window. Home bookshelf in the background with books and a small
cactus. Style: warm illustration, soft colors, Studio Ghibli
inspired. --ar 2:1
```

### 办公室一角
```
Cozy desk corner illustration, warm tones. A computer monitor
displays colorful interface. A red lobster-patterned mug sits
beside a mechanical keyboard. A small succulent plant and
reading glasses are nearby. Warm desk lamp glows. Style:
flat illustration, soft shadows, homey feeling.
```

---

*配色师出品 · 2026-03-30*
*如有调整需求，请联系配色师协作*
