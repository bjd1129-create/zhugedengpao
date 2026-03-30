// ========================================
// Function 008: Random Integer Between
// ========================================
function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Usage example
randomInt(1, 10); // Random integer between 1 and 10
randomInt(0, 100); // Random integer between 0 and 100
