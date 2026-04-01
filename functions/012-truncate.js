// ========================================
// Function 012: Truncate String
// ========================================
function truncate(str, maxLength, suffix = '...') {
  if (str.length <= maxLength) return str;
  return str.slice(0, maxLength - suffix.length) + suffix;
}

// Usage example
truncate('Hello World', 8); // 'Hello...'
truncate('Hello World', 8, '>>>'); // 'Hello>>>'
