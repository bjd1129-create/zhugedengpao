// ========================================
// Function 007: Sleep / Delay
// ========================================
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Usage example (async function)
async function delayedLog() {
  console.log('Start');
  await sleep(2000);
  console.log('End after 2 seconds');
}
