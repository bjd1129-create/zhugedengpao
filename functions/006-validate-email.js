// ========================================
// Function 006: Validate Email
// ========================================
function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// Usage example
validateEmail('test@example.com'); // true
validateEmail('invalid-email'); // false
