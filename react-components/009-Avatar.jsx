import React from 'react';

// ========================================
// React Component 009: Avatar Component
// ========================================
export const Avatar = ({ 
  src, 
  alt, 
  name,
  size = 'medium',
  status
}) => {
  const sizes = {
    small: 'w-8 h-8 text-xs',
    medium: 'w-12 h-12 text-sm',
    large: 'w-16 h-16 text-base',
    xl: 'w-24 h-24 text-lg'
  };
  
  const statusColors = {
    online: 'bg-green-500',
    offline: 'bg-gray-400',
    busy: 'bg-red-500',
    away: 'bg-yellow-500'
  };
  
  const getInitials = (name) => {
    if (!name) return '?';
    return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
  };
  
  return (
    <div className="relative inline-block">
      {src ? (
        <img 
          src={src} 
          alt={alt || name || 'Avatar'} 
          className={`${sizes[size]} rounded-full object-cover border-2 border-white shadow-md`}
        />
      ) : (
        <div className={`${sizes[size]} rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center text-white font-bold border-2 border-white shadow-md`}>
          {getInitials(name)}
        </div>
      )}
      {status && (
        <span className={`absolute bottom-0 right-0 w-3 h-3 ${statusColors[status]} border-2 border-white rounded-full`} />
      )}
    </div>
  );
};

export const AvatarGroup = ({ avatars, max = 4 }) => {
  const visibleAvatars = avatars.slice(0, max);
  const remainingCount = avatars.length - max;
  
  return (
    <div className="flex -space-x-3">
      {visibleAvatars.map((avatar, index) => (
        <div key={index} className="ring-2 ring-white rounded-full">
          <Avatar {...avatar} size="small" />
        </div>
      ))}
      {remainingCount > 0 && (
        <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-xs font-bold text-gray-600 ring-2 ring-white">
          +{remainingCount}
        </div>
      )}
    </div>
  );
};