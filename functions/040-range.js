// ========================================
// Function 040: Generate Range
// ========================================
function range(start, end, step = 1) {
  const result = [];
  if (step === 0) throw new Error('Step cannot be 0');
  
  if (end === undefined) {
    end = start;
    start = 0;
  }
  
  if (step > 0) {
    for (let i = start; i < end; i += step) {
      result.push(i);
    }
  } else {
    for (let i = start; i > end; i += step) {
      result.push(i);
    }
  }
  return result;
}

function rangeRight(start, end, step = 1) {
  return range(start, end, step).reverse();
}

// Usage example
range(5); // [0, 1, 2, 3, 4]
range(2, 6); // [2, 3, 4, 5]
range(1, 10, 2); // [1, 3, 5, 7, 9]
range(5, 1, -1); // [5, 4, 3, 2]