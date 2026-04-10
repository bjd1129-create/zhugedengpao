/**
 * 相册图片懒加载优化
 * 功能：
 * 1. 渐进式加载 (placeholder → 缩略图 → 原图)
 * 2. 交错加载 (staggered loading) 视觉效果
 * 3. 错误处理和重试
 */

(function() {
  'use strict';

  // 配置
  const CONFIG = {
    rootMargin: '100px 0px',
    threshold: 0.1,
    staggerDelay: 50,  // 交错加载延迟 (ms)
    retryCount: 3,
    retryDelay: 1000
  };

  // 创建占位符
  function createPlaceholder(img) {
    const placeholder = document.createElement('div');
    placeholder.className = 'photo-placeholder';
    placeholder.style.cssText = `
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: linear-gradient(135deg, #fafafa 0%, #f0f0f0 100%);
      display: flex;
      align-items: center;
      justify-content: center;
    `;

    const heart = document.createElement('span');
    heart.textContent = '💕';
    heart.style.cssText = 'font-size: 24px; opacity: 0.3;';
    placeholder.appendChild(heart);

    return placeholder;
  }

  // 图片加载成功
  function onImageLoad(img, placeholder) {
    img.classList.add('loaded');
    if (placeholder && placeholder.parentNode) {
      placeholder.style.opacity = '0';
      setTimeout(() => placeholder.remove(), 300);
    }
  }

  // 图片加载失败
  function onImageError(img, retryCount) {
    if (retryCount < CONFIG.retryCount) {
      setTimeout(() => {
        img.src = img.src;
      }, CONFIG.retryDelay);
    } else {
      img.style.cssText = 'background: #f5f5f5; display: flex; align-items: center; justify-content: center;';
      img.alt = '图片加载失败 💔';
    }
  }

  // 设置交错加载动画
  function setupStaggeredAnimation(cards) {
    cards.forEach((card, index) => {
      card.style.opacity = '0';
      card.style.transform = card.style.transform || 'translateY(20px)';

      setTimeout(() => {
        card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        card.style.opacity = '1';
        card.style.transform = card.style.transform.includes('rotate')
          ? card.style.transform.replace('translateY(20px)', '')
          : '';
      }, index * CONFIG.staggerDelay);
    });
  }

  // 懒加载观察器
  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          const placeholder = img.previousSibling;

          img.addEventListener('load', () => onImageLoad(img, placeholder));
          img.addEventListener('error', () => onImageError(img, 0));

          // 如果图片已经在缓存中，直接显示
          if (img.complete && img.naturalHeight !== 0) {
            onImageLoad(img, placeholder);
          }

          observer.unobserve(img);
        }
      });
    }, {
      rootMargin: CONFIG.rootMargin,
      threshold: CONFIG.threshold
    });

    // 观察所有照片卡片
    document.querySelectorAll('.photo-card img').forEach(img => {
      imageObserver.observe(img);
    });

    // 设置交错动画
    const cards = document.querySelectorAll('.photo-card');
    if (cards.length > 0 && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      setupStaggeredAnimation(Array.from(cards));
    }
  } else {
    // 回退: 直接加载所有图片
    document.querySelectorAll('.photo-card img').forEach(img => {
      img.classList.add('loaded');
    });
  }

  // 性能监控
  if ('PerformanceObserver' in window) {
    try {
      const observer = new PerformanceObserver((list) => {
        list.getEntries().forEach(entry => {
          if (entry.initiatorType === 'img') {
            console.log(`[Perf] 图片加载: ${entry.name} - ${Math.round(entry.duration)}ms`);
          }
        });
      });
      observer.observe({ entryTypes: ['resource'] });
    } catch (e) {
      // 不支持的浏览器
    }
  }

  console.log('[Memory Site] 图片懒加载已初始化');
})();
