import React from 'react';

// ========================================
// React Component 017: Alert Component
// ========================================
export const Alert = ({ 
  children, 
  variant = 'info',
  title,
  dismissible = false,
  onDismiss
}) => {
  const variants = {
    info: { bg: 'bg-blue-50', border: 'border-blue-200', icon: 'ℹ️', text: 'text-blue-800' },
    success: { bg: 'bg-green-50', border: 'border-green-200', icon: '✅', text: 'text-green-800' },
    warning: { bg: 'bg-yellow-50', border: 'border-yellow-200', icon: '⚠️', text: 'text-yellow-800' },
    error: { bg: 'bg-red-50', border: 'border-red-200', icon: '❌', text: 'text-red-800' }
  };
  
  const style = variants[variant] || variants.info;
  
  return (
    <div className={`${style.bg} ${style.border} border-l-4 ${style.text} p-4 rounded-lg flex gap-3`}>
      <span className="text-xl">{style.icon}</span>
      <div className="flex-1">
        {title && <h4 className="font-bold mb-1">{title}</h4>}
        <div className="text-sm">{children}</div>
      </div>
      {dismissible && (
        <button 
          onClick={onDismiss}
          className="text-gray-400 hover:text-gray-600"
        >
          ✕
        </button>
      )}
    </div>
  );
};