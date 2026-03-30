// ========================================
// Function 041: Download File
// ========================================
function downloadFile(content, filename, mimeType = 'text/plain') {
  const blob = content instanceof Blob ? content : new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

function downloadJSON(data, filename = 'data.json') {
  downloadFile(JSON.stringify(data, null, 2), filename, 'application/json');
}

function downloadImage(imageUrl, filename = 'image.png') {
  fetch(imageUrl)
    .then(res => res.blob())
    .then(blob => {
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      link.click();
      URL.revokeObjectURL(url);
    });
}

// Usage example
downloadFile('Hello World', 'hello.txt');
downloadJSON({ name: 'John', age: 30 });