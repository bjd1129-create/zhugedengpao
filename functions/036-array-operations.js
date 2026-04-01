// ========================================
// Function 036: Array Intersection
// ========================================
function arrayIntersection(arr1, arr2) {
  const set2 = new Set(arr2);
  return [...new Set(arr1)].filter(item => set2.has(item));
}

function arrayDifference(arr1, arr2) {
  const set2 = new Set(arr2);
  return arr1.filter(item => !set2.has(item));
}

function arraySymmetricDifference(arr1, arr2) {
  return [...arrayDifference(arr1, arr2), ...arrayDifference(arr2, arr1)];
}

// Usage example
arrayIntersection([1, 2, 3], [2, 3, 4]); // [2, 3]
arrayDifference([1, 2, 3], [2]); // [1, 3]
arraySymmetricDifference([1, 2], [2, 3]); // [1, 3]