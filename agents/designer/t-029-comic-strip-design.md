# T-029: 首页漫画连载专区 UI 设计方案

## 概述
首页漫画区实现"四格漫画×43张横向滚动"展示

## 设计方案

### 结构
```html
<!-- 漫画专区入口 -->
<section class="comic-strip-section">
  <h2>🦞 小花的打工日记</h2>
  
  <!-- 四格漫画横向滚动区 -->
  <div class="comic-scroll-container">
    <div class="comic-scroll-track" id="comicScrollTrack">
      <!-- 43张garfield_lobster图片 -->
      <div class="comic-card">
        <div class="comic-4panel">
          <img src="garfield_lobster_001.png" alt="第1格" />
          <img src="garfield_lobster_002.png" alt="第2格" />
          <img src="garfield_lobster_003.png" alt="第3格" />
          <img src="garfield_lobster_004.png" alt="第4格" />
        </div>
        <div class="comic-story-label">办公室篇 #1</div>
      </div>
      <!-- 更多comic-card... -->
    </div>
    
    <!-- 左右滚动按钮 -->
    <button class="scroll-btn left" onclick="scrollComic(-1)">◀</button>
    <button class="scroll-btn right" onclick="scrollComic(1)">▶</button>
  </div>
  
  <!-- 查看更多按钮 -->
  <a href="/comic.html" class="view-more-btn">查看完整漫画 →</a>
</section>
```

### CSS样式
```css
.comic-strip-section {
  padding: 40px 0;
  background: var(--bg-warm-yellow, #FFF8E1);
}

.comic-scroll-container {
  position: relative;
  overflow: hidden;
  margin: 20px 0;
}

.comic-scroll-track {
  display: flex;
  gap: 20px;
  overflow-x: auto;
  scroll-behavior: smooth;
  padding: 0 60px; /* 为按钮留空间 */
  scrollbar-width: none; /* Firefox隐藏滚动条 */
}

.comic-scroll-track::-webkit-scrollbar {
  display: none; /* Chrome/Safari隐藏滚动条 */
}

.comic-card {
  flex: 0 0 280px;
  background: white;
  border-radius: 16px;
  padding: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.comic-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.comic-4panel {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4px;
  border-radius: 8px;
  overflow: hidden;
}

.comic-4panel img {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
}

.scroll-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--lobster-red, #E07A5A);
  color: white;
  border: none;
  cursor: pointer;
  z-index: 10;
  opacity: 0.9;
}

.scroll-btn:hover {
  opacity: 1;
  transform: translateY(-50%) scale(1.1);
}

.scroll-btn.left { left: 10px; }
.scroll-btn.right { right: 10px; }
```

### JavaScript滚动逻辑
```javascript
function scrollComic(direction) {
  const track = document.getElementById('comicScrollTrack');
  const cardWidth = 300; // card宽度 + gap
  track.scrollBy({
    left: direction * cardWidth * 2, // 一次滚2个卡片
    behavior: 'smooth'
  });
}

// 自动轮播（可选，每5秒）
let autoScrollInterval;
function startAutoScroll() {
  autoScrollInterval = setInterval(() => {
    const track = document.getElementById('comicScrollTrack');
    const isNearEnd = track.scrollLeft + track.clientWidth >= track.scrollWidth - 50;
    if (isNearEnd) {
      track.scrollTo({ left: 0, behavior: 'smooth' });
    } else {
      scrollComic(1);
    }
  }, 5000);
}

// 鼠标悬停暂停自动滚动
document.querySelector('.comic-scroll-container').addEventListener('mouseenter', () => {
  clearInterval(autoScrollInterval);
});
```

### 响应式适配
```css
@media (max-width: 768px) {
  .comic-card {
    flex: 0 0 220px;
  }
  .scroll-btn {
    display: none; /* 移动端隐藏按钮，触摸滚动 */
  }
}
```

---

## 43张garfield_lobster分类建议

| 分类 | 文件范围 | 标签 |
|------|----------|------|
| 办公室篇 | 001-010 | 🏢 |
| 编程篇 | 011-020 | 💻 |
| 开会篇 | 021-030 | 📊 |
| 学习篇 | 031-040 | 📚 |
| 日常篇 | 041-043 | 🏠 |

---

## 代码侠协作说明
1. 43张图片URL: `/images/garfield_lobster_XXX_*.png`
2. 横向滚动CSS已就绪
3. JS滚动函数只需5行
