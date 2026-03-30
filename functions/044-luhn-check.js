// ========================================
// Function 044: Luhn Algorithm (Credit Card Check)
// ========================================
function isValidCreditCard(number) {
  const str = String(number).replace(/\D/g, '');
  if (str.length < 13 || str.length > 19) return false;
  
  let sum = 0;
  let isEven = false;
  
  for (let i = str.length - 1; i >= 0; i--) {
    let digit = parseInt(str[i], 10);
    
    if (isEven) {
      digit *= 2;
      if (digit > 9) digit -= 9;
    }
    
    sum += digit;
    isEven = !isEven;
  }
  
  return sum % 10 === 0;
}

// Usage example
isValidCreditCard('4111111111111111'); // true (test Visa)
isValidCreditCard('1234567890123456'); // false