// ========================================
// Function 032: Generate Random Color
// ========================================
function randomColor() {
  return '#' + Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0');
}

function randomColors(count) {
  return Array.from({ length: count }, () => randomColor());
}

const predefinedColors = ['#667eea', '#764ba2', '#f093fb', '#48dbfb', '#ff6b6b'];
function randomPredefinedColor() {
  return predefinedColors[Math.floor(Math.random() * predefinedColors.length)];
}

// Usage example
randomColor(); // '#a3c42e'
randomColors(3); // ['#ff0000', '#00ff00', '#0000ff']
randomPredefinedColor(); // '#667eea'