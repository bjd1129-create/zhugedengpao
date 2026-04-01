# 浮蛙升级设计方案

## 概述
将右下角 🦞 emoji 替换为真实图片 xiaohua-garfield-lobster-v2.png，并根据时间显示不同表情

## 当前状态
- 当前位置：右下角固定浮动
- 当前内容：🦞 emoji
- 目标内容：xiaohua-garfield-lobster-v2.png

## 文件信息
- **图片路径**: `/images/xiaohua-garfield-lobster-v2.png`
- **格式**: JPEG（实际格式，不是PNG）

## 设计方案

### HTML结构
```html
<div class="floating-xiaohua" id="floatingXiaohua">
  <img src="/images/xiaohua-garfield-lobster-v2.png" alt="诸葛小花" />
</div>
```

### CSS样式
```css
.floating-xiaohua {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 60px;
  height: 60px;
  z-index: 9999;
  cursor: pointer;
  transition: transform 0.3s;
}

.floating-xiaohua:hover {
  transform: scale(1.1);
}

.floating-xiaohua img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 50%;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
```

### 时间表情逻辑
```javascript
function updateXiaohuaExpression() {
  const hour = new Date().getHours();
  const img = document.querySelector('.floating-xiaohua img');
  
  if (hour >= 6 && hour < 12) {
    // 早上：精力充沛 ☀️
    img.src = '/images/xiaohua-morning.png';
  } else if (hour >= 12 && hour < 14) {
    // 中午：饿了 🍜
    img.src = '/images/xiaohua-lunch.png';
  } else if (hour >= 14 && hour < 18) {
    // 下午：努力工作中 💪
    img.src = '/images/xiaohua-afternoon.png';
  } else if (hour >= 18 && hour < 22) {
    // 晚上：加班中 😅
    img.src = '/images/xiaohua-evening.png';
  } else {
    // 深夜：睡觉了 😴
    img.src = '/images/xiaohua-sleep.png';
  }
}

// 页面加载时和每小时更新
updateXiaohuaExpression();
setInterval(updateXiaohuaExpression, 3600000); // 每小时
```

## 简化方案（单图版）
如果只需要一个固定图片：
```html
<style>
.floating-xiaohua {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 60px;
  height: 60px;
  z-index: 9999;
  cursor: pointer;
}
.floating-xiaohua:hover {
  animation: bounce 0.5s;
}
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
</style>

<div class="floating-xiaohua">
  <img src="/images/xiaohua-garfield-lobster-v2.png" alt="诸葛小花" />
</div>
```

## 部署说明
1. 将 xiaohua-garfield-lobster-v2.png 放到网站 images 目录
2. 在每个页面底部添加上述HTML
3. 可选：添加多时间版本图片实现动态表情

## 代码侠协作
只需找到当前的 🦞 emoji 位置，替换为上述HTML即可
