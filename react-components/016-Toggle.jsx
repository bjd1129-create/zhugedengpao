import React, { useState } from 'react';

// ========================================
// React Component 016: Toggle Switch Component
// ========================================
export const Toggle = ({ 
  checked = false, 
  onChange,
  disabled = false,
  label,
  size = 'medium'
}) => {
  const sizes = {
    small: { track: 'w-8 h-4', thumb: 'w-3 h-3', translate: 'translate-x-4' },
    medium: { track: 'w-12 h-6', thumb: 'w-5 h-5', translate: 'translate-x-6' },
    large: { track: 'w-16 h-8', thumb: 'w-7 h-7', translate: 'translate-x-8' }
  };
  
  const { track, thumb, translate } = sizes[size];
  
  return (
    <label className={`flex items-center gap-3 ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}>
      <div 
        className={`${track} bg-gray-300 rounded-full relative transition-colors duration-300 ${
          checked ? 'bg-purple-600' : ''
        }`}
        onClick={() => !disabled && onChange(!checked)}
      >
        <div 
          className={`absolute top-0.5 left-0.5 ${thumb} bg-white rounded-full shadow-md transition-transform duration-300 ${
            checked ? translate : ''
          }`}
        />
      </div>
      {label && <span className="text-gray-700">{label}</span>}
    </label>
  );
};

export const ToggleGroup = ({ options, value, onChange }) => (
  <div className="flex gap-2">
    {options.map((option) => (
      <button
        key={option.value}
        onClick={() => onChange(option.value)}
        className={`px-4 py-2 rounded-lg font-medium transition-all ${
          value === option.value
            ? 'bg-purple-600 text-white shadow-lg'
            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
        }`}
      >
        {option.label}
      </button>
    ))}
  </div>
);