import React from 'react';

// ========================================
// React Component 013: Skeleton Loader Component
// ========================================
export const Skeleton = ({ 
  variant = 'text',
  width,
  height,
  className = ''
}) => {
  const baseClasses = 'animate-pulse bg-gradient-to-r from-gray-200 via-gray-100 to-gray-200 bg-[length:200%_100%] rounded';
  
  const variants = {
    text: 'h-4 w-full',
    title: 'h-8 w-3/4',
    avatar: 'w-12 h-12 rounded-full',
    image: 'w-full aspect-video rounded-lg',
    button: 'h-10 w-24 rounded-lg',
    card: 'h-40 w-full rounded-xl'
  };
  
  return (
    <div 
      className={`${baseClasses} ${variants[variant]} ${className}`}
      style={{ width, height }}
    />
  );
};

export const SkeletonCard = () => (
  <div className="bg-white rounded-xl shadow-lg p-6 space-y-4">
    <Skeleton variant="image" />
    <Skeleton variant="title" />
    <Skeleton variant="text" />
    <Skeleton variant="text" width="60%" />
  </div>
);

export const SkeletonList = ({ count = 3 }) => (
  <div className="space-y-4">
    {Array.from({ length: count }).map((_, i) => (
      <div key={i} className="flex items-center gap-4 p-4 bg-white rounded-lg shadow">
        <Skeleton variant="avatar" />
        <div className="flex-1 space-y-2">
          <Skeleton variant="title" width="40%" />
          <Skeleton variant="text" />
        </div>
      </div>
    ))}
  </div>
);