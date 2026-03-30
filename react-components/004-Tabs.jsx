import React, { useState } from 'react';

// ========================================
// React Component 004: Tabs Component
// ========================================
export const Tabs = ({ tabs }) => {
  const [activeTab, setActiveTab] = useState(0);
  
  return (
    <div>
      <div className="flex border-b border-gray-200">
        {tabs.map((tab, index) => (
          <button
            key={index}
            onClick={() => setActiveTab(index)}
            className={`px-6 py-3 font-medium transition-all duration-300 relative ${
              activeTab === index 
                ? 'text-purple-600' 
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            {tab.label}
            {activeTab === index && (
              <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-purple-600" />
            )}
          </button>
        ))}
      </div>
      <div className="p-6">
        {tabs[activeTab]?.content}
      </div>
    </div>
  );
};