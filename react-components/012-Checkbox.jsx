import React, { useState } from 'react';

// ========================================
// React Component 012: Checkbox Component
// ========================================
export const Checkbox = ({ 
  label, 
  checked = false, 
  onChange,
  disabled = false,
  indeterminate = false
}) => {
  return (
    <label className={`flex items-center gap-3 cursor-pointer select-none ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}>
      <div className="relative">
        <input
          type="checkbox"
          checked={checked}
          onChange={onChange}
          disabled={disabled}
          className="sr-only"
        />
        <div 
          className={`w-6 h-6 rounded border-2 transition-all duration-200 flex items-center justify-center ${
            checked || indeterminate
              ? 'bg-purple-600 border-purple-600' 
              : 'border-gray-300 hover:border-purple-400'
          }`}
        >
          {checked && <span className="text-white text-sm font-bold">✓</span>}
          {indeterminate && !checked && <span className="text-white text-sm font-bold">—</span>}
        </div>
      </div>
      <span className="text-gray-700">{label}</span>
    </label>
  );
};

export const CheckboxGroup = ({ options, value = [], onChange }) => {
  const handleChange = (optionValue) => {
    const newValue = value.includes(optionValue)
      ? value.filter(v => v !== optionValue)
      : [...value, optionValue];
    onChange(newValue);
  };
  
  return (
    <div className="space-y-2">
      {options.map((option) => (
        <Checkbox
          key={option.value}
          label={option.label}
          checked={value.includes(option.value)}
          onChange={() => handleChange(option.value)}
        />
      ))}
    </div>
  );
};