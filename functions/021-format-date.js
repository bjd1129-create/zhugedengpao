// ========================================
// Function 021: Format Date
// ========================================
function formatDate(date, format = 'YYYY-MM-DD') {
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const hours = String(d.getHours()).padStart(2, '0');
  const minutes = String(d.getMinutes()).padStart(2, '0');
  const seconds = String(d.getSeconds()).padStart(2, '0');
  
  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds);
}

// Usage example
formatDate(new Date(), 'YYYY-MM-DD'); // '2024-01-15'
formatDate(new Date(), 'HH:mm:ss'); // '14:30:45'
formatDate(new Date(), 'YYYY/MM/DD HH:mm'); // '2024/01/15 14:30'