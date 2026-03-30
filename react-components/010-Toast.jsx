import React, { useState } from 'react';

// ========================================
// React Component 010: Toast Notification Component
// ========================================
export const Toast = ({ 
  message, 
  type = 'info',
  duration = 3000,
  onClose
}) => {
  const [isVisible, setIsVisible] = useState(true);
  
  const typeStyles = {
    info: 'bg-blue-500',
    success: 'bg-green-500',
    warning: 'bg-yellow-500',
    error: 'bg-red-500'
  };
  
  const icons = {
    info: 'ℹ️',
    success: '✅',
    warning: '⚠️',
    error: '❌'
  };
  
  React.useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(false);
      setTimeout(onClose, 300);
    }, duration);
    
    return () => clearTimeout(timer);
  }, [duration, onClose]);
  
  return (
    <div className={`fixed top-4 right-4 z-50 transform transition-all duration-300 ${
      isVisible ? 'translate-x-0 opacity-100' : 'translate-x-full opacity-0'
    }`}>
      <div className={`${typeStyles[type]} text-white px-6 py-4 rounded-lg shadow-2xl flex items-center gap-3 min-w-80`}>
        <span className="text-xl">{icons[type]}</span>
        <p className="flex-1">{message}</p>
        <button 
          onClick={() => {
            setIsVisible(false);
            onClose();
          }}
          className="text-white/80 hover:text-white text-lg"
        >
          ✕
        </button>
      </div>
    </div>
  );
};

export const ToastContainer = ({ toasts, onRemove }) => {
  return (
    <div className="fixed top-4 right-4 z-50 flex flex-col gap-3">
      {toasts.map((toast) => (
        <Toast 
          key={toast.id} 
          {...toast} 
          onClose={() => onRemove(toast.id)} 
        />
      ))}
    </div>
  );
};