// ========================================
// Function 048: Throttle Function Factory
// ========================================
function throttle(fn, wait, options = {}) {
  let timeout = null;
  let previous = 0;
  const { leading = true, trailing = true } = options;
  
  return function(...args) {
    const now = Date.now();
    
    if (!previous && !leading) previous = now;
    
    const remaining = wait - (now - previous);
    
    if (remaining <= 0 || remaining > wait) {
      if (timeout) {
        clearTimeout(timeout);
        timeout = null;
      }
      previous = now;
      fn.apply(this, args);
    } else if (!timeout && trailing) {
      timeout = setTimeout(() => {
        previous = leading ? Date.now() : 0;
        timeout = null;
        fn.apply(this, args);
      }, remaining);
    }
  };
}

// Usage example
const throttledHandler = throttle(handleScroll, 100, { leading: true, trailing: true });
window.addEventListener('scroll', throttledHandler);