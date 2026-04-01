// ========================================
// Function 043: Debounce HTTP Request
// ========================================
const debouncedFetch = (() => {
  let timeout = null;
  let lastController = null;
  
  return (url, options = {}, delay = 300) => {
    return new Promise((resolve, reject) => {
      if (timeout) clearTimeout(timeout);
      if (lastController) lastController.abort();
      
      timeout = setTimeout(async () => {
        lastController = new AbortController();
        try {
          const response = await fetch(url, {
            ...options,
            signal: lastController.signal
          });
          resolve(response);
        } catch (error) {
          if (error.name !== 'AbortError') reject(error);
        }
      }, delay);
    });
  };
})();

// Usage example
debouncedFetch('/api/search?q=test').then(r => r.json());