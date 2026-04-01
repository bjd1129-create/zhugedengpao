// ========================================
// Function 004: Generate Unique ID
// ========================================
function generateId(prefix = 'id') {
  const timestamp = Date.now().toString(36);
  const randomStr = Math.random().toString(36).substring(2, 9);
  return `${prefix}_${timestamp}_${randomStr}`;
}

// Usage example
const userId = generateId('user'); // user_abc123_xyz789
const orderId = generateId('order'); // order_abc123_xyz789
