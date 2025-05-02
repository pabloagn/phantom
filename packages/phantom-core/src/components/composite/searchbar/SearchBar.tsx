// packages/phantom-core/src/components/composite/searchbar/SearchBar.tsx
// @ts-nocheck

// TODO: Implement SearchBar component

import React from 'react';

export interface SearchBarProps extends React.InputHTMLAttributes<HTMLInputElement> {
  onSearch?: (query: string) => void;
}

export const SearchBar: React.FC<SearchBarProps> = ({ className, onSearch, ...rest }) => {
  // Replace with actual SearchBar implementation later
  return <input type="search" className={className} {...rest} placeholder="Placeholder: SearchBar" />;
};

export default SearchBar;