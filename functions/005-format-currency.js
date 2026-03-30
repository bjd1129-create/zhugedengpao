// ========================================
// Function 005: Format Currency
// ========================================
function formatCurrency(amount, currency = 'USD', locale = 'en-US') {
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency: currency
  }).format(amount);
}

// Usage example
formatCurrency(1234.56); // $1,234.56
formatCurrency(1234.56, 'EUR', 'de-DE'); // 1.234,56 €
formatCurrency(1234.56, 'JPY', 'ja-JP'); // ¥1,235
