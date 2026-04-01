// ========================================
// Function 049: UUID Generator
// ========================================
function uuid() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

function uuidShort() {
  return Math.random().toString(36).substring(2, 15) + 
         Math.random().toString(36).substring(2, 15);
}

// Usage example
uuid(); // 'a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d'
uuidShort(); // 'm9x2p5q8r3t'