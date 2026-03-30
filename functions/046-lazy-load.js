// ========================================
// Function 046: Lazy Load Images
// ========================================
function lazyLoadImages(selector = 'img[data-src]') {
  const images = document.querySelectorAll(selector);
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        img.removeAttribute('data-src');
        observer.unobserve(img);
      }
    });
  }, { rootMargin: '50px' });
  
  images.forEach(img => observer.observe(img));
  
  return () => observer.disconnect();
}

// Usage HTML: <img data-src="real-image.jpg" src="placeholder.jpg">
// Usage JS: lazyLoadImages();