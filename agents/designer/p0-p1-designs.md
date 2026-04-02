# P0: 访客心跳气泡设计方案（最终版）

## 功能
- 右下角浮蛙小花，每30秒弹出气泡
- 气泡停留10秒后消失

## HTML结构
```html
<div class="floating-xiaohua" id="floatingXiaohua">
  <img src="/images/xiaohua-garfield-lobster-v2.png" alt="小花" />
  <div class="speech-bubble" id="speechBubble">
    <span id="bubbleText">早安！今天也要加油哦~</span>
  </div>
</div>
```

## CSS样式
```css
.floating-xiaohua {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9999;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.floating-xiaohua img {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: 3px solid #E07A5A;
  box-shadow: 0 4px 16px rgba(224, 122, 90, 0.3);
  object-fit: cover;
  transition: transform 0.3s;
}

.floating-xiaohua:hover img {
  transform: scale(1.1);
}

.speech-bubble {
  position: absolute;
  bottom: 70px;
  right: 0;
  background: white;
  padding: 10px 16px;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  max-width: 200px;
  font-size: 14px;
  color: #3D2314;
  font-family: 'Noto Sans SC', sans-serif;
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 0.3s, transform 0.3s;
  pointer-events: none;
  white-space: nowrap;
}

.speech-bubble.visible {
  opacity: 1;
  transform: translateY(0);
}

/* 小三角 */
.speech-bubble::after {
  content: '';
  position: absolute;
  bottom: -8px;
  right: 24px;
  border: 8px solid transparent;
  border-top-color: white;
}
```

## 语录内容池（8条）
```javascript
const xiaohuaQuotes = [
  "早安！今天也要加油哦~",
  "工作累了就休息一下，小花陪着你",
  "你已经很棒了，给自己点个赞！",
  "今天做了什么有意义的事吗？",
  "小花相信你能做到的！",
  "记得喝水，记得休息~",
  "辛苦了！休息是为了走更远的路",
  "有什么我可以帮你的吗？"
];
```

## JavaScript逻辑
```javascript
const quotes = [
  "早安！今天也要加油哦~",
  "工作累了就休息一下，小花陪着你",
  "你已经很棒了，给自己点个赞！",
  "今天做了什么有意义的事吗？",
  "小花相信你能做到的！",
  "记得喝水，记得休息~",
  "辛苦了！休息是为了走更远的路",
  "有什么我可以帮你的吗？"
];

function showBubble() {
  const bubble = document.getElementById('speechBubble');
  const text = document.getElementById('bubbleText');
  text.textContent = quotes[Math.floor(Math.random() * quotes.length)];
  bubble.classList.add('visible');
  
  setTimeout(() => {
    bubble.classList.remove('visible');
  }, 10000); // 10秒后消失
}

function startBubbleTimer() {
  showBubble();
  setTimeout(startBubbleTimer, 30000); // 每30秒一次
}

// 点击立即显示
document.getElementById('floatingXiaohua').addEventListener('click', showBubble);

// 页面加载启动
startBubbleTimer();
```

## 配色（宫崎骏风格）
- 浮蛙边框：`#E07A5A`（珊瑚红）
- 气泡背景：`#FFFFFF`（纯白）
- 气泡文字：`#3D2314`（深棕）
- 发光效果：`rgba(224, 122, 90, 0.3)`

---

## P1: 漫画NEW徽章

```css
.tab-new-badge {
  display: inline-block;
  background: linear-gradient(135deg, #FF6B6B, #EE5A5A);
  color: white;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 8px;
  margin-left: 4px;
  font-weight: bold;
  animation: badge-pulse 2s ease-in-out infinite;
}

@keyframes badge-pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}
```

**HTML**: `<span class="tab-new-badge">✨ NEW</span>`

---

## P1: 日记随机翻看按钮

```css
.btn-random-diary {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: linear-gradient(135deg, #FFF8E1, #FFF0E3);
  color: #E07A5A;
  border: 2px solid #E07A5A;
  padding: 10px 20px;
  border-radius: 24px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-random-diary:hover {
  background: #E07A5A;
  color: white;
  transform: translateY(-2px);
}
```

**HTML**: `<button class="btn-random-diary">🎲 随机翻看某一天</button>`
