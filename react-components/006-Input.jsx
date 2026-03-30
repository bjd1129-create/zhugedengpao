import React, { useState } from 'react';

// ========================================
// React Component 006: Input Component
// ========================================
export const Input = ({ 
  label, 
  type = 'text', 
  error,
  value,
  onChange,
  ...props 
}) => {
  const [isFocused, setIsFocused] = useState(false);
  
  return (
    <div className="relative mb-4">
      {label && (
        <label className="block text-sm font-medium text-gray-700 mb-1">
          {label}
        </label>
      )}
      <input
        type={type}
        value={value}
        onChange={onChange}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        className={`w-full px-4 py-3 border-2 rounded-lg transition-all duration-300 outline-none ${
          error 
            ? 'border-red-500 focus:border-red-600' 
            : isFocused 
              ? 'border-purple-500' 
              : 'border-gray-200 hover:border-gray-300'
        }`}
        {...props}
      />
      {error && (
        <p className="mt-1 text-sm text-red-500">{error}</p>
      )}
    </div>
  );
};

export const TextArea = ({ label, error, ...props }) => {
  return (
    <div className="relative mb-4">
      {label && (
        <label className="block text-sm font-medium text-gray-700 mb-1">
          {label}
        </label>
      )}
      <textarea
        className={`w-full px-4 py-3 border-2 rounded-lg transition-all duration-300 outline-none resize-none ${
          error ? 'border-red-500' : 'border-gray-200'
        }`}
        rows={4}
        {...props}
      />
      {error && <p className="mt-1 text-sm text-red-500">{error}</p>}
    </div>
  );
};