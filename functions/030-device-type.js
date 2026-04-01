// ========================================
// Function 030: Detect Device Type
// ========================================
function getDeviceType() {
  const ua = navigator.userAgent;
  if (/(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(ua)) {
    return 'tablet';
  }
  if (/Mobile|Android|iP(hone|od)|IEMobile|Opera Mini/i.test(ua)) {
    return 'mobile';
  }
  return 'desktop';
}

function isMobile() {
  return getDeviceType() === 'mobile';
}

function isTablet() {
  return getDeviceType() === 'tablet';
}

function isDesktop() {
  return getDeviceType() === 'desktop';
}

// Usage example
getDeviceType(); // 'desktop' | 'mobile' | 'tablet'
isMobile(); // true or false