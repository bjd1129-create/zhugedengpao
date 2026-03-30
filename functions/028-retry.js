// ========================================
// Function 028: Retry with Exponential Backoff
// ========================================
async function retry(fn, maxRetries = 3, baseDelay = 1000) {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries) throw error;
      const delay = baseDelay * Math.pow(2, attempt);
      await sleep(delay);
    }
  }
}

// Usage example
const fetchData = async () => {
  const response = await fetch('https://api.example.com/data');
  if (!response.ok) throw new Error('Failed');
  return response.json();
};

retry(fetchData, 3, 1000).then(console.log).catch(console.error);