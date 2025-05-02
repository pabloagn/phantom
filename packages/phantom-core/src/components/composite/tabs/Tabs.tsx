// packages/phantom-core/src/components/composite/tabs/Tabs.tsx
// @ts-nocheck

'use client';

import React, { useState, createContext, useContext } from 'react';

// Context for the Tabs
type TabsContextType = {
  activeTab: string;
  setActiveTab: (id: string) => void;
};

const TabsContext = createContext<TabsContextType | undefined>(undefined);

// Hook to access Tabs context
const useTabs = () => {
  const context = useContext(TabsContext);
  if (!context) {
    throw new Error('Tabs components must be used within a Tabs component');
  }
  return context;
};

export type TabsVariant = 'underline' | 'enclosed' | 'pills';
export type TabsOrientation = 'horizontal' | 'vertical';

export interface TabsProps {
  /**
   * The default active tab ID
   */
  defaultTabId: string;

  /**
   * Tab variant
   * @default 'underline'
   */
  variant?: TabsVariant;

  /**
   * Tab orientation
   * @default 'horizontal'
   */
  orientation?: TabsOrientation;

  /**
   * The content of the tabs
   */
  children: React.ReactNode;

  /**
   * Additional CSS class name for the tabs container
   */
  className?: string;
}

export const Tabs: React.FC<TabsProps> = ({
  defaultTabId,
  variant = 'underline',
  orientation = 'horizontal',
  children,
  className = '',
}) => {
  const [activeTab, setActiveTab] = useState(defaultTabId);

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div
        className={`${orientation === 'vertical' ? 'flex flex-row' : ''} ${className}`}
        role="tablist"
        aria-orientation={orientation}
      >
        {children}
      </div>
    </TabsContext.Provider>
  );
};

export interface TabListProps {
  /**
   * The tab list content
   */
  children: React.ReactNode;

  /**
   * Additional CSS class name for the tab list
   */
  className?: string;
}

export const TabList: React.FC<TabListProps> = ({ children, className = '' }) => {
  return (
    <div
      className={`flex ${
        orientation === 'vertical' ? 'flex-col border-r' : 'border-b'
      } ${className}`}
      role="tablist"
    >
      {children}
    </div>
  );
};

export interface TabProps {
  /**
   * Unique identifier for the tab
   */
  id: string;

  /**
   * The tab content
   */
  children: React.ReactNode;

  /**
   * Whether the tab is disabled
   * @default false
   */
  disabled?: boolean;

  /**
   * Additional CSS class name for the tab
   */
  className?: string;
}

export const Tab: React.FC<TabProps> = ({ id, children, disabled = false, className = '' }) => {
  const { activeTab, setActiveTab } = useTabs();
  const isActive = activeTab === id;

  const handleClick = () => {
    if (!disabled) {
      setActiveTab(id);
    }
  };

  // Get styles based on variant
  const getVariantStyles = variant => {
    switch (variant) {
      case 'enclosed':
        return isActive
          ? 'bg-white border-l border-t border-r rounded-t-lg -mb-px'
          : 'bg-gray-50 border-b';
      case 'pills':
        return isActive
          ? 'bg-primary-500 text-white rounded-full'
          : 'hover:bg-gray-100 hover:text-gray-700 rounded-full';
      case 'underline':
      default:
        return isActive
          ? 'border-b-2 border-primary-500 text-primary-500'
          : 'border-b-2 border-transparent hover:border-gray-300';
    }
  };

  return (
    <button
      role="tab"
      aria-selected={isActive}
      aria-controls={`panel-${id}`}
      id={`tab-${id}`}
      tabIndex={isActive ? 0 : -1}
      onClick={handleClick}
      disabled={disabled}
      className={`px-4 py-2 font-medium text-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-all duration-200 ease-in-out ${
        disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
      } ${getVariantStyles(variant)} ${className}`}
    >
      {children}
    </button>
  );
};

export interface TabPanelsProps {
  /**
   * The tab panels content
   */
  children: React.ReactNode;

  /**
   * Additional CSS class name for the tab panels container
   */
  className?: string;
}

export const TabPanels: React.FC<TabPanelsProps> = ({ children, className = '' }) => {
  return (
    <div className={`mt-4 ${orientation === 'vertical' ? 'flex-1 ml-6' : ''} ${className}`}>
      {children}
    </div>
  );
};

export interface TabPanelProps {
  /**
   * Unique identifier for the tab panel
   */
  id: string;

  /**
   * The tab panel content
   */
  children: React.ReactNode;

  /**
   * Additional CSS class name for the tab panel
   */
  className?: string;
}

export const TabPanel: React.FC<TabPanelProps> = ({ id, children, className = '' }) => {
  const { activeTab } = useTabs();
  const isActive = activeTab === id;

  if (!isActive) {
    return null;
  }

  return (
    <div
      role="tabpanel"
      id={`panel-${id}`}
      aria-labelledby={`tab-${id}`}
      tabIndex={0}
      className={className}
    >
      {children}
    </div>
  );
};

export default Tabs;
