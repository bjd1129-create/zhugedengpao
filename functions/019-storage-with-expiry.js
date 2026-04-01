// ========================================
// Function 019: Local Storage with Expiry
// ========================================
const storage = {
  set(key, value, expiryMinutes = 60) {
    const item = {
      value,
      expiry: Date.now() + expiryMinutes * 60 * 1000
    };
    localStorage.setItem(key, JSON.stringify(item));
  },
  
  get(key) {
    const raw = localStorage.getItem(key);
    if (!raw) return null;
    
    const item = JSON.parse(raw);
    if (Date.now() > item.expiry) {
      localStorage.removeItem(key);
      return null;
    }
    return item.value;
  },
  
  delete(key) {
    localStorage.removeItem(key);
  }
};

// Usage example
storage.set('token', 'abc123', 30); // Expires in 30 minutes
storage.get('token'); // Returns value or null if expired
