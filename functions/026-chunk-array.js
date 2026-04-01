// ========================================
// Function 026: Chunk Array
// ========================================
function chunkArray(array, size) {
  const chunks = [];
  for (let i = 0; i < array.length; i += size) {
    chunks.push(array.slice(i, i + size));
  }
  return chunks;
}

// Usage example
chunkArray([1, 2, 3, 4, 5, 6, 7], 3); // [[1,2,3], [4,5,6], [7]]
chunkArray('abcdef', 2); // [['a','b'], ['c','d'], ['e','f']]