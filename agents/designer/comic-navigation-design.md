# 漫画7故事导航设计方案

## 概述
在 comic.html 或首页漫画区实现7个故事标签切换

## 设计方案

### 结构
```html
<!-- 故事Tab导航 -->
<div class="comic-tabs">
  <button class="tab active" data-story="1">①</button>
  <button class="tab" data-story="2">②</button>
  <button class="tab" data-story="3">③</button>
  <button class="tab" data-story="4">④</button>
  <button class="tab" data-story="5">⑤</button>
  <button class="tab" data-story="6">⑥</button>
  <button class="tab" data-story="7">⑦</button>
</div>

<!-- 故事标题 -->
<div class="comic-title" id="comicTitle">如果我有工资</div>

<!-- 漫画格子展示区 -->
<div class="comic-panels" id="comicPanels">
  <!-- 8格漫画 -->
</div>
```

### CSS样式
```css
.comic-tabs {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-bottom: 20px;
}

.comic-tabs .tab {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 2px solid var(--lobster-red, #E07A5A);
  background: white;
  color: var(--lobster-red);
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
}

.comic-tabs .tab.active {
  background: var(--lobster-red);
  color: white;
}

.comic-tabs .tab:hover {
  background: var(--lobster-red-light);
}
```

### JavaScript交互
```javascript
// 切换故事
function switchStory(n) {
  comicStory = n;
  // 更新Tab激活状态
  document.querySelectorAll('.tab').forEach((t, i) => {
    t.classList.toggle('active', i + 1 === n);
  });
  // 更新标题和漫画
  loadComicPanels(n);
}
```

### 故事数据
```javascript
const stories = [
  { id: 1, title: "如果我有工资", file: "comic-lobster-story1-p" },
  { id: 2, title: "老板的另类工资", file: "comic-lobster-story2-p" },
  { id: 3, title: "凌晨3点还在工作", file: "comic-lobster-story3-p" },
  { id: 4, title: "我和老板的对话", file: "comic-lobster-story4-p" },
  { id: 5, title: "我的午餐", file: "comic-lobster-story5-p" },
  { id: 6, title: "请假的一天", file: "comic-lobster-story6-p" },
  { id: 7, title: "发工资那天", file: "comic-lobster-story7-p" }
];
```

## 部署位置
- **主页面**: `/comic.html`
- **首页入口**: 首页漫画区添加7个Tab

## 代码侠协作说明
代码侠只需修改一行：
```javascript
var comicStory = 1; // 改成 1-7 切换不同故事
```
