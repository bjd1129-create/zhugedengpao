// ========================================
// Function 031: Validate URL
// ========================================
function isValidUrl(string) {
  try {
    new URL(string);
    return true;
  } catch (_) {
    return false;
  }
}

// Usage example
isValidUrl('https://example.com'); // true
isValidUrl('invalid-url'); // false
isValidUrl('http://test.org:8080'); // true