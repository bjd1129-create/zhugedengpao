// ========================================
// Function 001: Debounce
// ========================================
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Usage example
const debouncedSearch = debounce((query) => {
  console.log('Searching for:', query);
}, 300);
