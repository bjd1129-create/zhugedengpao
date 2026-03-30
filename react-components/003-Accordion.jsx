import React, { useState } from 'react';

// ========================================
// React Component 003: Accordion Component
// ========================================
export const Accordion = ({ items }) => {
  const [openIndex, setOpenIndex] = useState(null);
  
  return (
    <div className="space-y-2">
      {items.map((item, index) => (
        <div 
          key={index} 
          className="border border-gray-200 rounded-lg overflow-hidden"
        >
          <button
            onClick={() => setOpenIndex(openIndex === index ? null : index)}
            className="w-full flex items-center justify-between p-4 bg-gray-50 hover:bg-gray-100 transition-colors text-left"
          >
            <span className="font-semibold text-gray-800">{item.title}</span>
            <span 
              className={`transform transition-transform duration-300 ${openIndex === index ? 'rotate-180' : ''}`}
            >
              ▼
            </span>
          </button>
          <div 
            className={`overflow-hidden transition-all duration-300 ${openIndex === index ? 'max-h-96' : 'max-h-0'}`}
          >
            <div className="p-4 text-gray-600">
              {item.content}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};