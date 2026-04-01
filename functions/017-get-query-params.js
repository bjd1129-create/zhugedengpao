// ========================================
// Function 017: Get Query Parameters
// ========================================
function getQueryParams(url) {
  const params = {};
  const searchParams = new URL(url).searchParams;
  for (const [key, value] of searchParams) {
    params[key] = value;
  }
  return params;
}

// Usage example
getQueryParams('https://example.com?page=1&limit=10');
// { page: '1', limit: '10' }
