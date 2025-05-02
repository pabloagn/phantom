// packages/phantomklange/src/components/layout/container.tsx

'use client';

import React from 'react';

interface ContainerProps {
  children: React.ReactNode;
  className?: string;
}

const Container: React.FC<ContainerProps> = ({
  children,
  className = ""
}) => {
  return (
    <div className={`container mx-auto px-6 ${className}`}>
      {children}
    </div>
  );
};

export default Container;
