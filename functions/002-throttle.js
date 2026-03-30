// ========================================
// Function 002: Throttle
// ========================================
function throttle(func, limit) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// Usage example
const throttledScroll = throttle(() => {
  console.log('Scrolling...');
}, 100);
