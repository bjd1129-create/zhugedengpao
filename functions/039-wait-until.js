// ========================================
// Function 039: Wait Until Condition
// ========================================
async function waitUntil(fn, interval = 100, timeout = 5000) {
  return new Promise((resolve, reject) => {
    const startTime = Date.now();
    
    const check = () => {
      if (fn()) {
        resolve(true);
      } else if (Date.now() - startTime >= timeout) {
        reject(new Error('Timeout waiting for condition'));
      } else {
        setTimeout(check, interval);
      }
    };
    
    check();
  });
}

async function waitForElement(selector, timeout = 5000) {
  return waitUntil(
    () => document.querySelector(selector) !== null,
    100,
    timeout
  ).then(() => document.querySelector(selector));
}

// Usage example
await waitUntil(() => someAsyncValue !== null);
await waitForElement('#myElement');