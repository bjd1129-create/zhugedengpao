// ========================================
// Function 013: Capitalize First Letter
// ========================================
function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

function capitalizeWords(str) {
  return str.split(' ').map(capitalize).join(' ');
}

// Usage example
capitalize('hello'); // 'Hello'
capitalizeWords('hello world'); // 'Hello World'
