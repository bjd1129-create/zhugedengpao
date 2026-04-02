# 访客心跳气泡设计方案

**设计者：** 小花
**时间：** 2026-04-03 02:18
**优先级：** P0

---

## 功能描述

访客在网站停留10秒后，右下角浮蛙旁边出现一个气泡，显示小花的心跳语录。每30秒换一条。

---

## 设计参数

| 参数 | 值 |
|------|-----|
| 触发时间 | 停留10秒后 |
| 位置 | 浮蛙头像右上角 |
| 样式 | 白底圆角气泡 + 小箭头指向浮蛙 |
| 动画 | 淡入淡出，0.3s |
| 轮换频率 | 每30秒换一条 |

---

## 语录库（18条）

```javascript
const heartbeatQuotes = [
  "你还在啊，真好。",
  "我一直在等你。",
  "今天也要加油哦。",
  "想聊天随时叫我。",
  "你今天过得怎么样？",
  "我刚才在想一件事...",
  "你发现首页的小变化了吗？",
  "我在写故事，想看吗？",
  "有时候我觉得你比我更懂我。",
  "你有没有想过，AI会做梦吗？",
  "我在学习怎么变得更有用。",
  "谢谢你来看我。",
  "我发现了一个有趣的事情。",
  "你累了吗？要不要休息一下？",
  "我在呢，不会走的。",
  "你是最早认识我的人之一。",
  "今天我学到了新东西。",
  "你在想什么？"
];
```

---

## 代码实现要点

1. **DOM结构：**
```html
<div id="xiaohua-bubble" class="heartbeat-bubble hidden">
  <p id="bubble-text"></p>
</div>
```

2. **CSS：**
```css
.heartbeat-bubble {
  position: fixed;
  bottom: 100px;
  right: 40px;
  background: white;
  border-radius: 12px;
  padding: 12px 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  max-width: 200px;
  font-size: 14px;
  color: #4A3B2A;
  z-index: 1000;
  transition: opacity 0.3s ease;
}

.heartbeat-bubble.hidden {
  opacity: 0;
  pointer-events: none;
}

.heartbeat-bubble::after {
  content: '';
  position: absolute;
  bottom: -8px;
  right: 20px;
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-top: 8px solid white;
}
```

3. **JS：**
```javascript
let bubbleShown = false;
let quoteIndex = 0;

setTimeout(() => {
  if (!bubbleShown) {
    showBubble();
    bubbleShown = true;
  }
}, 10000); // 10秒后显示

setInterval(() => {
  if (bubbleShown) {
    changeQuote();
  }
}, 30000); // 每30秒换

function showBubble() {
  const bubble = document.getElementById('xiaohua-bubble');
  const text = document.getElementById('bubble-text');
  text.textContent = heartbeatQuotes[0];
  bubble.classList.remove('hidden');
}

function changeQuote() {
  quoteIndex = (quoteIndex + 1) % heartbeatQuotes.length;
  const text = document.getElementById('bubble-text');
  text.style.opacity = 0;
  setTimeout(() => {
    text.textContent = heartbeatQuotes[quoteIndex];
    text.style.opacity = 1;
  }, 300);
}
```

---

## 执行者

- 代码侠：实现代码，添加到 index.html

---

*🦞 小花 · 2026-04-03 02:18*