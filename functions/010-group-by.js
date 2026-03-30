// ========================================
// Function 010: Group Array by Key
// ========================================
function groupBy(array, key) {
  return array.reduce((result, item) => {
    const group = item[key];
    if (!result[group]) {
      result[group] = [];
    }
    result[group].push(item);
    return result;
  }, {});
}

// Usage example
const users = [
  { name: 'John', age: 25 },
  { name: 'Jane', age: 25 },
  { name: 'Bob', age: 30 }
];
groupBy(users, 'age'); // { 25: [...], 30: [...] }
