import React from 'react';

// ========================================
// React Component 015: Tooltip Component
// ========================================
export const Tooltip = ({ 
  children, 
  content,
  position = 'top',
  delay = 200
}) => {
  const [isVisible, setIsVisible] = React.useState(false);
  const timeoutRef = React.useRef(null);
  
  const showTooltip = () => {
    timeoutRef.current = setTimeout(() => setIsVisible(true), delay);
  };
  
  const hideTooltip = () => {
    clearTimeout(timeoutRef.current);
    setIsVisible(false);
  };
  
  const positions = {
    top: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
    bottom: 'top-full left-1/2 -translate-x-1/2 mt-2',
    left: 'right-full top-1/2 -translate-y-1/2 mr-2',
    right: 'left-full top-1/2 -translate-y-1/2 ml-2'
  };
  
  const arrows = {
    top: 'top-full left-1/2 -translate-x-1/2 border-8 border-transparent border-t-gray-800',
    bottom: 'bottom-full left-1/2 -translate-x-1/2 border-8 border-transparent border-b-gray-800',
    left: 'left-full top-1/2 -translate-y-1/2 border-8 border-transparent border-l-gray-800',
    right: 'right-full top-1/2 -translate-y-1/2 border-8 border-transparent border-r-gray-800'
  };
  
  return (
    <div 
      className="relative inline-block"
      onMouseEnter={showTooltip}
      onMouseLeave={hideTooltip}
    >
      {children}
      {isVisible && (
        <div className={`absolute z-50 ${positions[position]}`}>
          <div className="bg-gray-800 text-white px-3 py-2 rounded-lg text-sm whitespace-nowrap shadow-lg">
            {content}
          </div>
          <div className={`absolute ${arrows[position]}`} style={{ borderWidth: '8px' }} />
        </div>
      )}
    </div>
  );
};