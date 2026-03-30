// ========================================
// Function 023: Color Utilities (HEX to RGB)
// ========================================
function hexToRgb(hex) {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : null;
}

function rgbToHex(r, g, b) {
  return '#' + [r, g, b].map(x => {
    const hex = x.toString(16);
    return hex.length === 1 ? '0' + hex : hex;
  }).join('');
}

function lighten(hex, percent) {
  const { r, g, b } = hexToRgb(hex);
  return rgbToHex(
    Math.min(255, Math.round(r + (255 - r) * percent)),
    Math.min(255, Math.round(g + (255 - g) * percent)),
    Math.min(255, Math.round(b + (255 - b) * percent))
  );
}

function darken(hex, percent) {
  const { r, g, b } = hexToRgb(hex);
  return rgbToHex(
    Math.max(0, Math.round(r * (1 - percent))),
    Math.max(0, Math.round(g * (1 - percent))),
    Math.max(0, Math.round(b * (1 - percent)))
  );
}

// Usage example
hexToRgb('#667eea'); // { r: 102, g: 126, b: 234 }
lighten('#667eea', 0.2); // lighter shade
darken('#667eea', 0.2); // darker shade