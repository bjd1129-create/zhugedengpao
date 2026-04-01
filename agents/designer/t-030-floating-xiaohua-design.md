# T-030: 浮蛙升级 - 气泡样式+时间感知台词设计

## 升级内容
- emoji 🦞 → 真实图片 xiaohua-garfield-lobster-v2.png
- 随机暖心气泡 + 时间感知台词

---

## 气泡样式设计

### HTML结构
```html
<div class="floating-xiaohua" id="floatingXiaohua">
  <img src="/images/xiaohua-garfield-lobster-v2.png" alt="小花" />
  <div class="speech-bubble" id="speechBubble">
    <span id="bubbleText">早安！今天也要加油哦~</span>
  </div>
</div>
```

### CSS气泡样式
```css
.floating-xiaohua {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 9999;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.floating-xiaohua img {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  box-shadow: 0 4px 16px rgba(224, 122, 90, 0.3);
  border: 3px solid #E07A5A;
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
}

.speech-bubble.visible {
  opacity: 1;
  transform: translateY(0);
}

/* 气泡小三角 */
.speech-bubble::after {
  content: '';
  position: absolute;
  bottom: -8px;
  right: 24px;
  border: 8px solid transparent;
  border-top-color: white;
}
```

---

## 时间感知台词库

### 早上 (06:00-09:00)
```
"早安！新的一天从一杯咖啡开始~"
"早上好！今天有什么计划吗？"
"起床啦！小花已经在等你了~"
"早安打工人！今天也要元气满满哦！"
```

### 上午 (09:00-12:00)
```
"工作顺利吗？小花在这里给你加油！"
"专注！你是最棒的！💪"
"上午好！保持节奏，事情一件件来~"
"加油！小花相信你！"
```

### 中午 (12:00-14:00)
```
"午饭时间到！记得吃饱哦~"
"休息一下，下午继续战斗！"
"中午好~吃好喝好才有力气干活！"
"饭后再冲！小花监督你午休~"
```

### 下午 (14:00-18:00)
```
"下午茶时间！伸个懒腰吧~"
"坚持住！今天快结束了！"
"下午好~事情越来越顺了吧？"
"你在做的，小花都看到了！"
```

### 傍晚 (18:00-20:00)
```
"下班啦！今天辛苦了~"
"辛苦啦！回家路上注意安全！"
"傍晚好~今天完成了很多事呢！"
"小花也要下班了，你也早点休息哦~"
```

### 晚上 (20:00-23:00)
```
"晚上好~今天做了什么有意义的事？"
"夜深了，早点休息哦！"
"加班中？小花陪着你！"
"晚安！明天见~"
```

### 深夜 (23:00-06:00)
```
"凌晨了……小花也困了……"
"夜猫子？注意身体哦~"
"该睡觉啦！小花先睡了zzZ"
"深夜好，星星都出来了~"
```

---

## 随机暖心气泡（非时间相关）

```
"小花在这里陪你哦~"
"你已经很棒了！"
"辛苦了！休息一下吧~"
"加油！你是最闪亮的！"
"小花相信你能做到！"
"今天也要开心哦！"
"有什么事可以告诉小花~"
"小花永远支持你！💕"
```

---

## JavaScript逻辑

```javascript
const xiaohuaMessages = {
  morning: ["早安！新的一天从一杯咖啡开始~", "早上好！今天有什么计划吗？", ...],
  noon: ["午饭时间到！记得吃饱哦~", "休息一下，下午继续战斗！", ...],
  afternoon: ["下午茶时间！伸个懒腰吧~", "坚持住！今天快结束了！", ...],
  evening: ["下班啦！今天辛苦了~", "辛苦啦！回家路上注意安全！", ...],
  night: ["晚上好~今天做了什么有意义的事？", "夜深了，早点休息哦！", ...],
  lateNight: ["凌晨了……小花也困了……", "夜猫子？注意身体哦~", ...]
};

const randomWarm = [
  "小花在这里陪你哦~",
  "你已经很棒了！",
  "辛苦了！休息一下吧~",
  "加油！你是最闪亮的！",
  "小花相信你能做到！",
  "今天也要开心哦！"
];

function getTimeOfDay() {
  const hour = new Date().getHours();
  if (hour >= 6 && hour < 9) return 'morning';
  if (hour >= 9 && hour < 12) return 'morning';
  if (hour >= 12 && hour < 14) return 'noon';
  if (hour >= 14 && hour < 18) return 'afternoon';
  if (hour >= 18 && hour < 20) return 'evening';
  if (hour >= 20 && hour < 23) return 'night';
  return 'lateNight';
}

function showXiaohuaBubble() {
  const bubble = document.getElementById('speechBubble');
  const text = document.getElementById('bubbleText');
  
  const timeOfDay = getTimeOfDay();
  const messages = xiaohuaMessages[timeOfDay];
  
  // 70%时间相关 + 30%随机暖心
  const message = Math.random() < 0.7 
    ? messages[Math.floor(Math.random() * messages.length)]
    : randomWarm[Math.floor(Math.random() * randomWarm.length)];
  
  text.textContent = message;
  bubble.classList.add('visible');
  
  // 5秒后隐藏
  setTimeout(() => {
    bubble.classList.remove('visible');
  }, 5000);
}

// 每30-60秒显示一次
function startXiaohuaTimer() {
  showXiaohuaBubble();
  const interval = 30000 + Math.random() * 30000; // 30-60秒
  setTimeout(startXiaohuaTimer, interval);
}

// 点击浮蛙立即显示气泡
document.getElementById('floatingXiaohua').addEventListener('click', showXiaohuaBubble);

// 页面加载时启动
startXiaohuaTimer();
```

---

## 代码侠协作说明
1. HTML结构已就绪
2. CSS样式已就绪
3. JS逻辑只需复制粘贴
4. 图片路径: `/images/xiaohua-garfield-lobster-v2.png`
