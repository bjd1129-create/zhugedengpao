import React from 'react';

// ========================================
// React Component 008: Badge Component
// ========================================
export const Badge = ({ 
  children, 
  variant = 'default',
  size = 'medium',
  ...props 
}) => {
  const baseClasses = 'inline-flex items-center font-semibold rounded-full';
  
  const variants = {
    default: 'bg-gray-100 text-gray-700',
    primary: 'bg-purple-100 text-purple-700',
    success: 'bg-green-100 text-green-700',
    warning: 'bg-yellow-100 text-yellow-700',
    danger: 'bg-red-100 text-red-700',
    info: 'bg-blue-100 text-blue-700'
  };
  
  const sizes = {
    small: 'px-2 py-0.5 text-xs',
    medium: 'px-3 py-1 text-sm',
    large: 'px-4 py-1.5 text-base'
  };
  
  return (
    <span className={`${baseClasses} ${variants[variant]} ${sizes[size]}`} {...props}>
      {children}
    </span>
  );
};

export const StatusBadge = ({ status }) => {
  const statusMap = {
    active: { label: 'Active', variant: 'success' },
    pending: { label: 'Pending', variant: 'warning' },
    inactive: { label: 'Inactive', variant: 'default' },
    error: { label: 'Error', variant: 'danger' }
  };
  
  const { label, variant } = statusMap[status] || statusMap.inactive;
  
  return <Badge variant={variant}>{label}</Badge>;
};