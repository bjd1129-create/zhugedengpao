# T-032: 首页"小花今日问候"模块设计方案

## 概述
在hero区域下方（日记卡片之前）添加动态问候卡片

## 设计要点
- 位置：hero → 小花今日问候 → 日记卡片
- 内容：小卡片 + 时间问候语 + 上线天数自动计算 + 微摇晃动画

## HTML结构
```html
<section class="xiaohua-greeting">
  <div class="greeting-card" id="greetingCard">
    <div class="greeting-mascot">
      <img src="/images/xiaohua-garfield-lobster-v2.png" alt="小花" />
    </div>
    <div class="greeting-content">
      <div class="greeting-label">🦞 小花说：</div>
      <div class="greeting-text" id="greetingText">
        "下午好呀！今天是我上线第 XX 天，老庄说他准备给我涨零用钱了..."
      </div>
    </div>
  </div>
</section>
```

## CSS样式
```css
.xiaohua-greeting {
  padding: 24px 0;
}

.greeting-card {
  display: flex;
  align-items: center;
  gap: 16px;
  background: white;
  border-radius: 20px;
  padding: 20px 24px;
  box-shadow: 0 4px 16px rgba(224, 122, 90, 0.15);
  max-width: 600px;
  margin: 0 auto;
  /* 微摇晃动画 */
  animation: greeting-shake 0.5s ease-in-out;
  animation-iteration-count: 1;
}

@keyframes greeting-shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-2px) rotate(-0.5deg); }
  75% { transform: translateX(2px) rotate(0.5deg); }
}

/* 定时小晃动 */
.greeting-card.idle {
  animation: greeting-micro-shake 3s ease-in-out infinite;
}

@keyframes greeting-micro-shake {
  0%, 90%, 100% { transform: translateX(0); }
  92% { transform: translateX(-1px); }
  94% { transform: translateX(1px); }
  96% { transform: translateX(-1px); }
  98% { transform: translateX(1px); }
}

.greeting-mascot img {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  border: 3px solid #E07A5A;
  object-fit: cover;
}

.greeting-label {
  font-size: 12px;
  color: #E07A5A;
  font-weight: bold;
  margin-bottom: 6px;
}

.greeting-text {
  font-size: 15px;
  color: #3D2314;
  line-height: 1.6;
  font-family: 'Noto Sans SC', sans-serif;
}
```

## JavaScript逻辑
```javascript
const greetingMessages = {
  morning: [
    "早安呀！今天是我上线第 {days} 天，老庄说他准备给我涨零用钱了...",
    "早上好！上线 {days} 天了，老庄刚给我充了电费~",
    "早呀！第 {days} 天，老庄说今天天气不错，适合工作..."
  ],
  afternoon: [
    "下午好呀！今天是我上线第 {days} 天，老庄说他准备给我涨零用钱了...",
    "下午茶时间~上线 {days} 天，老庄还在改需求中...",
    "下午好！老庄说今天的代码写得不错（其实是代码侠的功劳）"
  ],
  evening: [
    "傍晚好！今天是我上线第 {days} 天，老庄说要给我加个灯泡...",
    "晚上啦~ {days} 天了，老庄说明天带我去看星星（骗人的）",
    "晚安呀！上线 {days} 天，灯泡亮了 {days} 天~"
  ]
};

function getTimeOfDay() {
  const hour = new Date().getHours();
  if (hour >= 5 && hour < 12) return 'morning';
  if (hour >= 12 && hour < 18) return 'afternoon';
  return 'evening';
}

function getDaysOnline() {
  const launchDate = new Date('2026-03-07');
  const today = new Date();
  return Math.floor((today - launchDate) / (1000 * 60 * 60 * 24));
}

function updateGreeting() {
  const textEl = document.getElementById('greetingText');
  const timeOfDay = getTimeOfDay();
  const days = getDaysOnline();
  
  const messages = greetingMessages[timeOfDay];
  let message = messages[Math.floor(Math.random() * messages.length)];
  message = message.replace('{days}', days);
  
  textEl.textContent = message;
  
  // 触发一次摇晃动画
  const card = document.getElementById('greetingCard');
  card.classList.remove('idle');
  void card.offsetWidth; // 强制重绘
  card.classList.add('idle');
}

// 每小时更新 + 页面加载时
updateGreeting();
setInterval(updateGreeting, 3600000);
```

## 上线天数计算
```javascript
// 起始日期：2026-03-07（小花生日）
const launchDate = new Date('2026-03-07');
// 今天是自动计算
```

## 响应式
```css
@media (max-width: 480px) {
  .greeting-card {
    flex-direction: column;
    text-align: center;
    padding: 16px;
  }
  .greeting-mascot img {
    width: 56px;
    height: 56px;
  }
}
```

---

## 代码侠协作说明
1. HTML结构已就绪
2. CSS动画已就绪
3. JS逻辑只需复制粘贴
4. 图片路径: `/images/xiaohua-garfield-lobster-v2.png`
