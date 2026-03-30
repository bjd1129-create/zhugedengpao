// ========================================
// Function 050: Create FormData from Object
// ========================================
function toFormData(obj, nested = false) {
  const formData = new FormData();
  
  const append = (key, value) => {
    if (value instanceof Date) {
      formData.append(key, value.toISOString());
    } else if (value !== null && value !== undefined) {
      formData.append(key, value);
    }
  };
  
  for (const [key, value] of Object.entries(obj)) {
    if (Array.isArray(value)) {
      value.forEach((v, i) => append(`${key}[${i}]`, v));
    } else if (typeof value === 'object' && value !== null && !(value instanceof Blob)) {
      const nestedKey = nested ? `${key}` : key;
      for (const [nestedKey2, nestedVal] of Object.entries(value)) {
        append(`${nestedKey}[${nestedKey2}]`, nestedVal);
      }
    } else {
      append(key, value);
    }
  }
  
  return formData;
}

// Usage example
toFormData({ name: 'John', age: 30 });
toFormData({ user: { name: 'John', email: 'john@example.com' } });