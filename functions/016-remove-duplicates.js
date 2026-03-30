// ========================================
// Function 016: Remove Duplicates
// ========================================
function removeDuplicates(array) {
  return [...new Set(array)];
}

function removeDuplicatesBy(array, key) {
  const seen = new Set();
  return array.filter(item => {
    const value = item[key];
    if (seen.has(value)) return false;
    seen.add(value);
    return true;
  });
}

// Usage example
removeDuplicates([1, 2, 2, 3, 3, 4]); // [1, 2, 3, 4]
removeDuplicatesBy([{id:1}, {id:2}, {id:1}], 'id'); // [{id:1}, {id:2}]
