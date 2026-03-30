// ========================================
// Function 035: URL Utilities
// ========================================
const urlUtils = {
  join(...parts) {
    return parts.join('/').replace(/\/+/g, '/');
  },
  
  params(url) {
    return new URL(url).searchParams;
  },
  
  param(url, key) {
    return new URL(url).searchParams.get(key);
  },
  
  addParams(url, params) {
    const urlObj = new URL(url);
    Object.entries(params).forEach(([key, value]) => {
      urlObj.searchParams.set(key, value);
    });
    return urlObj.toString();
  },
  
  removeParams(url, keys) {
    const urlObj = new URL(url);
    keys.forEach(key => urlObj.searchParams.delete(key));
    return urlObj.toString();
  }
};

// Usage example
urlUtils.join('https://example.com', 'api', 'users'); // 'https://example.com/api/users'
urlUtils.param('https://example.com?page=1', 'page'); // '1'
urlUtils.addParams('https://example.com', { page: 2, limit: 10 });