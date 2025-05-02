// packages/phantom-core/src/components/composite/accordion/Accordion.tsx
// @ts-nocheck

'use client';

import React, { useState, createContext, useContext } from 'react';
import { ChevronDown } from 'lucide-react';

// Context for the Accordion
type AccordionContextType = {
  activeItems: string[];
  toggleItem: (id: string) => void;
  allowMultiple: boolean;
};

const AccordionContext = createContext<AccordionContextType | undefined>(undefined);

// Hook to access Accordion context
const useAccordion = () => {
  const context = useContext(AccordionContext);
  if (!context) {
    throw new Error('Accordion components must be used within an Accordion');
  }
  return context;
};

export interface AccordionProps {
  /**
   * The content of the accordion
   */
  children: React.ReactNode;

  /**
   * Allow multiple items to be open at the same time
   * @default false
   */
  allowMultiple?: boolean;

  /**
   * Default expanded items (by ID)
   * @default []
   */
  defaultItems?: string[];

  /**
   * Additional CSS class name
   */
  className?: string;
}

export const Accordion: React.FC<AccordionProps> = ({
  children,
  allowMultiple = false,
  defaultItems = [],
  className = '',
}) => {
  const [activeItems, setActiveItems] = useState<string[]>(defaultItems);

  const toggleItem = (id: string) => {
    if (allowMultiple) {
      setActiveItems(prevItems =>
        prevItems.includes(id)
          ? prevItems.filter(item => item !== id)
          : [...prevItems, id]
      );
    } else {
      setActiveItems(prevItems =>
        prevItems.includes(id) ? [] : [id]
      );
    }
  };

  return (
    <AccordionContext.Provider value={{ activeItems, toggleItem, allowMultiple }}>
      <div className={`divide-y divide-gray-200 dark:divide-gray-700 ${className}`}>
        {children}
      </div>
    </AccordionContext.Provider>
  );
};

export interface AccordionItemProps {
  /**
   * Unique identifier for the accordion item
   */
  id: string;

  /**
   * The header content for the accordion item
   */
  header: React.ReactNode;

  /**
   * The content to be displayed when the accordion item is expanded
   */
  children: React.ReactNode;

  /**
   * Additional CSS class name for the item
   */
  className?: string;
}

export const AccordionItem: React.FC<AccordionItemProps> = ({
  id,
  header,
  children,
  className = '',
}) => {
  const { activeItems, toggleItem } = useAccordion();
  const isExpanded = activeItems.includes(id);

  return (
    <div className={`border-0 ${className}`}>
      <h3>
        <button
          type="button"
          className="flex w-full items-center justify-between py-4 px-2 text-left font-medium text-gray-900 dark:text-white hover:bg-gray-50 dark:hover:bg-gray-800 focus:outline-none focus-visible:ring focus-visible:ring-primary-500 focus-visible:ring-opacity-75"
          onClick={() => toggleItem(id)}
          aria-expanded={isExpanded}
          aria-controls={`accordion-panel-${id}`}
        >
          <span>{header}</span>
          <ChevronDown
            className={`h-5 w-5 transition-transform duration-200 ${isExpanded ? 'rotate-180 transform' : ''}`}
          />
        </button>
      </h3>
      <div
        id={`accordion-panel-${id}`}
        className={`overflow-hidden transition-all duration-300 ease-in-out ${
          isExpanded ? 'max-h-96' : 'max-h-0'
        }`}
        aria-hidden={!isExpanded}
        role="region"
      >
        <div className="pb-4 pt-2 px-2">{children}</div>
      </div>
    </div>
  );
};

export default Accordion;
