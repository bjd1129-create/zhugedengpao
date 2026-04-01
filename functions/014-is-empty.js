// ========================================
// Function 014: Check if Object is Empty
// ========================================
function isEmpty(obj) {
  if (obj === null || obj === undefined) return true;
  if (typeof obj === 'string') return obj.length === 0;
  if (Array.isArray(obj)) return obj.length === 0;
  if (typeof obj === 'object') return Object.keys(obj).length === 0;
  return false;
}

// Usage example
isEmpty({}); // true
isEmpty([]); // true
isEmpty(''); // true
isEmpty({ a: 1 }); // false
