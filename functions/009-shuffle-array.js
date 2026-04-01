// ========================================
// Function 009: Shuffle Array (Fisher-Yates)
// ========================================
function shuffleArray(array) {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

// Usage example
const arr = [1, 2, 3, 4, 5];
shuffleArray(arr); // Returns shuffled array
