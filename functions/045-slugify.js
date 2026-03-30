// ========================================
// Function 045: Slugify String
// ========================================
function slugify(text) {
  return text
    .toString()
    .toLowerCase()
    .trim()
    .replace(/\s+/g, '-')
    .replace(/[^\w\-]+/g, '')
    .replace(/\-\-+/g, '-')
    .replace(/^-+/, '')
    .replace(/-+$/, '');
}

function unslugify(slug) {
  return slug.split('-').map(word => 
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ');
}

// Usage example
slugify('Hello World! This is a test.'); // 'hello-world-this-is-a-test'
unslugify('hello-world'); // 'Hello World'