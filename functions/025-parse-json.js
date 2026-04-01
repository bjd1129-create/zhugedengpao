// ========================================
// Function 025: Parse JSON Safe
// ========================================
function parseJSON(str, defaultValue = null) {
  try {
    return JSON.parse(str);
  } catch (e) {
    return defaultValue;
  }
}

// Usage example
parseJSON('{"valid": true}'); // { valid: true }
parseJSON('invalid json', {}); // {}
parseJSON('[1,2,3]'); // [1, 2, 3]