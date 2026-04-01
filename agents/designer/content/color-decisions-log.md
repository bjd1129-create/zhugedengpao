# 配色决策日志
**版本：** v1.0
**建立时间：** 2026-03-31 11:58

每次重要配色决策必须记录。

---

## 决策记录

### 2026-03-31 | index-new.html 等29个HTML文件配色统一

**决策：** 将所有HTML文件中的硬编码 `#c0392b` 替换为品牌色 `#E07A5A`

**依据：**
- 品牌色定义：lobster-red 柔和版 = `#E07A5A`（来自 color-palette-2026-03-30.css）
- 70%规则：主色用于主要交互元素（按钮、链接hover、重要标题）
- CSS变量已在 css/style.css 正确定义为 `--accent: #E07A5A`

**执行：** `find . -name "*.html" -not -path "./archive/*" | xargs sed -i '' 's/#c0392b/#E07A5A/g'`

**结果：** 204处替换，29个文件受影响（archive/目录除外）

**副作用检查：**
- ✅ 品牌红色统一为柔和版
- ⚠️ archive/ 目录未修改（故意的，避免污染原始备份）

**配色占比验证：**
- E07A5A：用于CTA按钮hover、主要强调、tag背景
- FFFFFF：卡片背景保持白色
- FFF8E1/FFF0E3：页面背景保持暖黄

---

### 2026-03-31 v15 | mascot-greeting.png 生成

**决策：** 生成品牌吉祥物问候图，用于官网首页问候区域

**Prompt：** Garfield猫穿龙虾服的可爱吉祥物，挥手问候，温暖友好风格，品牌色 #E07A5A

**文件：** images/mascot-greeting.png（207KB，1024x1024）

**下一步：** 需在 index-new.html 或 hero 区域引用该图片

---

*下次更新：新的重要配色决策时*
