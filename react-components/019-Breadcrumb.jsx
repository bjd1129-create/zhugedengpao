import React from 'react';

// ========================================
// React Component 019: Breadcrumb Component
// ========================================
export const Breadcrumb = ({ items, separator = '>' }) => (
  <nav className="flex items-center gap-2 text-sm">
    {items.map((item, index) => (
      <React.Fragment key={index}>
        {index > 0 && (
          <span className="text-gray-400">{separator}</span>
        )}
        {item.href ? (
          <a 
            href={item.href}
            className="text-purple-600 hover:text-purple-700 hover:underline"
          >
            {item.label}
          </a>
        ) : (
          <span className={index === items.length - 1 ? 'text-gray-800 font-medium' : 'text-gray-500'}>
            {item.label}
          </span>
        )}
      </React.Fragment>
    ))}
  </nav>
);

export const BreadcrumbWithIcons = ({ items }) => (
  <nav className="flex items-center gap-2 text-sm">
    {items.map((item, index) => (
      <React.Fragment key={index}>
        {index > 0 && (
          <span className="text-gray-400">/</span>
        )}
        <span className={index === items.length - 1 ? 'flex items-center gap-1 text-gray-800 font-medium' : 'flex items-center gap-1 text-purple-600'}>
          {item.icon && <span>{item.icon}</span>}
          {item.href ? (
            <a href={item.href} className="hover:underline">{item.label}</a>
          ) : (
            <span>{item.label}</span>
          )}
        </span>
      </React.Fragment>
    ))}
  </nav>
);