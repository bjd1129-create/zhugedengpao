# Footer"永远亮着一盏灯"设计方案

## 概述
在首页底部添加温馨Footer装饰，灯泡微光动画 + 暖心文字

## 设计要点
- 灯泡微光动画（SVG灯泡）
- 文字："欢迎常来，这里永远亮着一盏灯"
- 访客计数占位

## HTML结构
```html
<footer class="xiaohua-footer">
  <div class="footer-lamp">
    <svg class="lamp-icon" viewBox="0 0 40 50" xmlns="http://www.w3.org/2000/svg">
      <!-- 灯泡玻璃 -->
      <ellipse cx="20" cy="18" rx="14" ry="16" fill="#FFF8E1" class="lamp-glow"/>
      <!-- 灯泡底部 -->
      <rect x="14" y="32" width="12" height="6" rx="2" fill="#E8B86D"/>
      <!-- 灯丝 -->
      <path d="M16 20 Q20 14 24 20" stroke="#E07A5A" stroke-width="2" fill="none" class="lamp-filament"/>
      <!-- 底座 -->
      <rect x="12" y="38" width="16" height="8" rx="2" fill="#8B5E3C"/>
    </svg>
    <div class="lamp-glow-effect"></div>
  </div>
  
  <div class="footer-text">
    <p class="footer-main">欢迎常来，这里永远亮着一盏灯</p>
    <p class="footer-meta">
      🦞 小花的窝 · 建于 2026年3月7日 · 访客 No.<span id="visitorCount">-----</span>
    </p>
  </div>
</footer>
```

## CSS样式
```css
.xiaohua-footer {
  text-align: center;
  padding: 40px 20px;
  background: linear-gradient(180deg, #FFF8E1 0%, #FFF5E8 100%);
  margin-top: 60px;
}

/* 灯泡容器 */
.footer-lamp {
  position: relative;
  display: inline-block;
  margin-bottom: 16px;
}

.lamp-icon {
  width: 40px;
  height: 50px;
  position: relative;
  z-index: 2;
}

/* 灯泡发光效果 */
.lamp-glow {
  fill: #FFFDE7;
  filter: drop-shadow(0 0 6px #FFE082);
  animation: lamp-glow-pulse 2s ease-in-out infinite;
}

@keyframes lamp-glow-pulse {
  0%, 100% {
    fill: #FFFDE7;
    filter: drop-shadow(0 0 6px #FFE082);
  }
  50% {
    fill: #FFF8E1;
    filter: drop-shadow(0 0 12px #FFD54F);
  }
}

/* 灯丝闪烁 */
.lamp-filament {
  animation: lamp-filament-flicker 3s ease-in-out infinite;
}

@keyframes lamp-filament-flicker {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
  52% { opacity: 1; }
  70% { opacity: 0.8; }
}

/* 外围光晕 */
.lamp-glow-effect {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 60px;
  height: 60px;
  background: radial-gradient(circle, rgba(255,224,130,0.4) 0%, transparent 70%);
  border-radius: 50%;
  animation: lamp-aura 2s ease-in-out infinite;
  z-index: 1;
}

@keyframes lamp-aura {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.6; }
  50% { transform: translate(-50%, -50%) scale(1.2); opacity: 0.3; }
}

/* 文字样式 */
.footer-text {
  max-width: 500px;
  margin: 0 auto;
}

.footer-main {
  font-family: 'ZCOOL KuaiLe', 'Ma Shan Zheng', cursive;
  font-size: 18px;
  color: #3D2314;
  font-style: italic;
  margin-bottom: 12px;
  line-height: 1.5;
}

.footer-meta {
  font-size: 13px;
  color: #8B5A3C;
  margin: 0;
}

/* 访客计数 */
#visitorCount {
  color: #E07A5A;
  font-weight: bold;
}
```

## 访客计数（占位/假数据）
```javascript
// 方案A：假数据（代码侠可替换为真实计数）
function setVisitorCount() {
  const countEl = document.getElementById('visitorCount');
  if (countEl) {
    // 生成一个随机数作为占位
    const fakeCount = Math.floor(Math.random() * 500) + 100;
    countEl.textContent = fakeCount.toString().padStart(5, '0');
  }
}

// 方案B：接入Cloudflare Analytics
// countEl.textContent = cf.analytics.getVisitors().toString().padStart(5, '0');
```

## 响应式
```css
@media (max-width: 480px) {
  .footer-main {
    font-size: 16px;
  }
  .lamp-icon {
    width: 32px;
    height: 40px;
  }
}
```

---

## 代码侠协作说明
1. HTML+CSS已就绪
2. SVG灯泡图标已就绪（无需外部图片）
3. 访客计数可接入真实数据或先用假数据
4. 直接放在footer区域即可
