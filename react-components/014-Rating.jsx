import React from 'react';

// ========================================
// React Component 014: Rating Stars Component
// ========================================
export const Rating = ({ 
  value = 0, 
  max = 5,
  onChange,
  readOnly = false,
  size = 'medium'
}) => {
  const sizes = {
    small: 'text-lg',
    medium: 'text-2xl',
    large: 'text-4xl'
  };
  
  const handleClick = (index) => {
    if (!readOnly && onChange) {
      onChange(index + 1);
    }
  };
  
  return (
    <div className="flex gap-1">
      {Array.from({ length: max }).map((_, index) => {
        const isFilled = index < Math.floor(value);
        const isHalf = !isFilled && index < value;
        
        return (
          <span
            key={index}
            onClick={() => handleClick(index)}
            className={`${sizes[size]} cursor-pointer transition-transform hover:scale-110 ${
              readOnly ? 'cursor-default' : 'cursor-pointer'
            }`}
          >
            {isFilled ? (
              <span className="text-yellow-400">★</span>
            ) : isHalf ? (
              <span className="text-yellow-400">✫</span>
            ) : (
              <span className="text-gray-300">☆</span>
            )}
          </span>
        );
      })}
    </div>
  );
};

export const RatingWithLabel = ({ value, max = 5 }) => (
  <div className="flex items-center gap-2">
    <Rating value={value} max={max} readOnly />
    <span className="text-sm text-gray-600">({value}/{max})</span>
  </div>
);