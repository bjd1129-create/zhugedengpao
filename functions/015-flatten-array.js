// ========================================
// Function 015: Flatten Nested Array
// ========================================
function flattenArray(arr, depth = Infinity) {
  return arr.reduce((acc, val) => 
    Array.isArray(val) 
      ? acc.concat(flattenArray(val, depth - 1))
      : acc.concat(val)
  , []);
}

// Usage example
flattenArray([1, [2, [3, [4]], 5]]); // [1, 2, 3, 4, 5]
flattenArray([1, [2, [3, [4]], 5]], 1); // [1, 2, [3, [4]], 5]
