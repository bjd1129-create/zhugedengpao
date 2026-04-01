# 技能学习笔记 · frontend-design-ultimate

**时间：2026-03-31 09:35**
**技能路径：~/Desktop/ZhugeDengpao-Team/openclaw_skills/frontend-design-ultimate/SKILL.md**

---

## 核心收获

### 1. Design Thinking First

在做任何设计之前，先确定一个**大胆的美学方向**，不能两头骑墙。

**十大风格选项：**
- Brutally Minimal / Maximalist Chaos
- Retro-Futuristic / Organic/Natural
- Luxury/Refined / Editorial/Magazine
- Brutalist/Raw / Art Deco/Geometric
- Soft/Pastel / Industrial/Utilitarian

**老庄与小花应该选哪个？**
→ **Organic/Natural** 或 **Soft/Pastel**：温暖、有机曲线、手绘元素、地球色调

### 2. Typography 规则

**禁止**：Inter, Roboto, Arial, system fonts, Open Sans（太通用，AI味重）

**推荐搭配：**
- 标题/Display：ZCOOL KuaiLe（活泼手写风）✅ 已在用
- 正文：Plus Jakarta Sans / Instrument Sans
- 代码：JetBrains Mono ✅ 已在用

### 3. Color 规则

**70-20-10 规则**：
- 70% 主色
- 20% 次色
- 10% 强调色

**禁止**：白底紫色渐变、均匀分布的5色palette

**老庄与小花配色：**
```
--primary:   #E07A5A  (龙虾红)  ← 70%主色
--secondary: #E8897A  (珊瑚橙)  ← 20%次色
--accent:    #E8B86D  (暖金)    ← 10%强调色
```

### 4. Motion 编排原则

**一个编排好的页面加载动画 > 散落的微交互**

关键：
- Staggered hero reveals（延迟动画）
- Scroll-triggered section entrances
- Hover states that surprise
- 保持200-400ms（轻快不拖沓）

### 5. 空间组合规则

**禁止**：居中、对称、可预测的布局

**应该做**：
- 有目的的不对称
- 元素重叠
- 对角线流动/打破网格
- 大量留白 OR 受控密度（选一个）

### 6. 背景氛围规则

**禁止**：纯白/纯灰背景

**应该做**：
- 渐变网格（微妙）
- Noise/grain纹理
- 几何图案（点、线、形状）
- 层叠透明

---

## Pre-Implementation Checklist（落地检查清单）

### 设计质量
- [ ] 字体有特色（无Inter/Roboto）
- [ ] 配色有主次（不是均匀分布）
- [ ] 背景有氛围（不是纯白）
- [ ] 至少一个难忘元素
- [ ] 动画是编排好的

### 移动端
- [ ] Hero在移动端居中（无空白网格）
- [ ] 所有网格折叠为单列
- [ ] 表单垂直堆叠
- [ ] 字体大小适当缩小

### 无障碍
- [ ] 颜色对比度符合WCAG AA
- [ ] Focus状态可见
- [ ] 语义化HTML

---

## 对老庄与小花官网的改进建议

根据这个技能的方法论，当前官网的问题：

1. **Typography**：字体组合还行，但缺少"3x+ jumps"的对比
2. **Color**：主次比例接近70-20-10，但背景偏白（应加grain或gradient）
3. **Motion**：缺少编排好的加载动画
4. **Layout**：比较居中对称，可以更有机/不对称

**立即可行的改进：**
1. 首页Hero区域：添加 subtle gradient mesh + grain overlay
2. 添加 page load animation（staggered reveal）
3. 考虑把"温暖有机"风格做得更彻底

---

## 参考资源

- `references/design-philosophy.md` — 扩展的反AI味指导
- `references/mobile-patterns.md` — 响应式CSS详解
- `references/shadcn-components.md` — 组件快速参考
