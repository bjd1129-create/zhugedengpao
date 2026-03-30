import React from 'react';

// ========================================
// React Component 018: Pagination Component
// ========================================
export const Pagination = ({ 
  currentPage, 
  totalPages, 
  onPageChange,
  siblingsCount = 1
}) => {
  const range = (start, end) => {
    return Array.from({ length: end - start + 1 }, (_, i) => start + i);
  };
  
  const getPageNumbers = () => {
    const totalPageNumbers = siblingsCount * 2 + 5;
    
    if (totalPages <= totalPageNumbers) {
      return range(1, totalPages);
    }
    
    const leftSiblingIndex = Math.max(currentPage - siblingsCount, 1);
    const rightSiblingIndex = Math.min(currentPage + siblingsCount, totalPages);
    
    const showLeftDots = leftSiblingIndex > 2;
    const showRightDots = rightSiblingIndex < totalPages - 1;
    
    if (!showLeftDots && showRightDots) {
      const leftRange = range(1, 3 + siblingsCount * 2);
      return [...leftRange, '...', totalPages];
    }
    
    if (showLeftDots && !showRightDots) {
      const rightRange = range(totalPages - (2 + siblingsCount * 2), totalPages);
      return [1, '...', ...rightRange];
    }
    
    return [1, '...', ...range(leftSiblingIndex, rightSiblingIndex), '...', totalPages];
  };
  
  const pageNumbers = getPageNumbers();
  
  return (
    <div className="flex items-center gap-2">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="px-3 py-2 rounded-lg border hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        ← Prev
      </button>
      
      {pageNumbers.map((page, index) => (
        <React.Fragment key={index}>
          {page === '...' ? (
            <span className="px-3 py-2">...</span>
          ) : (
            <button
              onClick={() => onPageChange(page)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                currentPage === page
                  ? 'bg-purple-600 text-white'
                  : 'border hover:bg-gray-50'
              }`}
            >
              {page}
            </button>
          )}
        </React.Fragment>
      ))}
      
      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="px-3 py-2 rounded-lg border hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Next →
      </button>
    </div>
  );
};