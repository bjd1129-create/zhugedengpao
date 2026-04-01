// ========================================
// Function 038: Sort by Property
// ========================================
function sortBy(arr, key, order = 'asc') {
  return [...arr].sort((a, b) => {
    const aVal = a[key];
    const bVal = b[key];
    
    if (aVal < bVal) return order === 'asc' ? -1 : 1;
    if (aVal > bVal) return order === 'asc' ? 1 : -1;
    return 0;
  });
}

function sortByMultiple(arr, keys) {
  return [...arr].sort((a, b) => {
    for (const key of keys) {
      if (a[key] < b[key]) return -1;
      if (a[key] > b[key]) return 1;
    }
    return 0;
  });
}

// Usage example
const users = [{name: 'John', age: 30}, {name: 'Jane', age: 25}];
sortBy(users, 'age'); // [{name: 'Jane', age: 25}, {name: 'John', age: 30}]
sortBy(users, 'age', 'desc');