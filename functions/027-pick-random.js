// ========================================
// Function 027: Pick Random from Array
// ========================================
function pickRandom(array) {
  return array[Math.floor(Math.random() * array.length)];
}

function pickRandomMultiple(array, count) {
  const shuffled = [...array].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, count);
}

// Usage example
pickRandom(['apple', 'banana', 'cherry']); // 'banana' (random)
pickRandomMultiple([1, 2, 3, 4, 5], 2); // [3, 1] (2 random items)