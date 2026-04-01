// ========================================
// Function 034: Scroll To Element Smoothly
// ========================================
function scrollToElement(element, offset = 0) {
  const elementPosition = element.getBoundingClientRect().top;
  const offsetPosition = elementPosition + window.pageYOffset - offset;
  
  window.scrollTo({
    top: offsetPosition,
    behavior: 'smooth'
  });
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function scrollToBottom() {
  window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
}

// Usage example
const target = document.getElementById('section');
scrollToElement(target, 80); // With 80px offset
scrollToTop(); // Scroll to top of page
scrollToBottom(); // Scroll to bottom of page