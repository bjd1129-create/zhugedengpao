// ========================================
// Function 042: Form Validation Rules
// ========================================
const validators = {
  required: (value) => value !== null && value !== undefined && value !== '',
  minLength: (value, len) => String(value).length >= len,
  maxLength: (value, len) => String(value).length <= len,
  min: (value, num) => Number(value) >= num,
  max: (value, num) => Number(value) <= num,
  pattern: (value, regex) => new RegExp(regex).test(value),
  email: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
  url: (value) => {
    try { new URL(value); return true; } catch { return false; }
  },
  matches: (value, other) => value === other,
  oneOf: (value, options) => options.includes(value)
};

function validate(formData, rules) {
  const errors = {};
  
  for (const [field, fieldRules] of Object.entries(rules)) {
    const value = formData[field];
    const fieldErrors = [];
    
    for (const [rule, ruleValue] of Object.entries(fieldRules)) {
      if (validators[rule] && !validators[rule](value, ruleValue)) {
        fieldErrors.push(`${field} failed ${rule} validation`);
      }
    }
    
    if (fieldErrors.length > 0) {
      errors[field] = fieldErrors;
    }
  }
  
  return { valid: Object.keys(errors).length === 0, errors };
}

// Usage example
validate(
  { name: 'Jo', email: 'invalid' },
  {
    name: { required: true, minLength: 3 },
    email: { required: true, email: true }
  }
);