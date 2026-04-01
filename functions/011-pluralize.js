// ========================================
// Function 011: Pluralize Word
// ========================================
function pluralize(count, singular, plural) {
  return count === 1 ? singular : (plural || `${singular}s`);
}

// Usage example
pluralize(1, 'item'); // 'item'
pluralize(5, 'item'); // 'items'
pluralize(2, 'child', 'children'); // 'children'
