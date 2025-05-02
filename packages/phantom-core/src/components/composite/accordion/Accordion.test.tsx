// packages/phantom-core/src/components/composite/accordion/Accordion.test.tsx
// @ts-nocheck

import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Accordion, AccordionItem } from './Accordion';

describe('Accordion', () => {
  it('renders accordion items correctly', () => {
    render(
      <Accordion>
        <AccordionItem id="item1" header="Accordion Header 1">
          Accordion Content 1
        </AccordionItem>
        <AccordionItem id="item2" header="Accordion Header 2">
          Accordion Content 2
        </AccordionItem>
      </Accordion>
    );

    expect(screen.getByText('Accordion Header 1')).toBeInTheDocument();
    expect(screen.getByText('Accordion Header 2')).toBeInTheDocument();

    // Initially, content should be hidden
    expect(screen.queryByText('Accordion Content 1')).toBeInTheDocument();
    expect(screen.queryByText('Accordion Content 2')).toBeInTheDocument();

    const firstItem = screen.getByText('Accordion Content 1').closest('[role="region"]');
    const secondItem = screen.getByText('Accordion Content 2').closest('[role="region"]');

    expect(firstItem).toHaveAttribute('aria-hidden', 'true');
    expect(secondItem).toHaveAttribute('aria-hidden', 'true');
  });

  it('toggles content visibility when header is clicked', () => {
    render(
      <Accordion>
        <AccordionItem id="item1" header="Accordion Header 1">
          Accordion Content 1
        </AccordionItem>
      </Accordion>
    );

    const header = screen.getByText('Accordion Header 1');

    // Click to expand
    fireEvent.click(header);

    const content = screen.getByText('Accordion Content 1').closest('[role="region"]');
    expect(content).toHaveAttribute('aria-hidden', 'false');

    // Click to collapse
    fireEvent.click(header);
    expect(content).toHaveAttribute('aria-hidden', 'true');
  });

  it('allows multiple items to be expanded when allowMultiple is true', () => {
    render(
      <Accordion allowMultiple>
        <AccordionItem id="item1" header="Accordion Header 1">
          Accordion Content 1
        </AccordionItem>
        <AccordionItem id="item2" header="Accordion Header 2">
          Accordion Content 2
        </AccordionItem>
      </Accordion>
    );

    const header1 = screen.getByText('Accordion Header 1');
    const header2 = screen.getByText('Accordion Header 2');

    // Expand first item
    fireEvent.click(header1);

    const content1 = screen.getByText('Accordion Content 1').closest('[role="region"]');
    const content2 = screen.getByText('Accordion Content 2').closest('[role="region"]');

    expect(content1).toHaveAttribute('aria-hidden', 'false');
    expect(content2).toHaveAttribute('aria-hidden', 'true');

    // Expand second item (first should remain expanded)
    fireEvent.click(header2);

    expect(content1).toHaveAttribute('aria-hidden', 'false');
    expect(content2).toHaveAttribute('aria-hidden', 'false');
  });

  it('collapses other items when allowMultiple is false', () => {
    render(
      <Accordion allowMultiple={false}>
        <AccordionItem id="item1" header="Accordion Header 1">
          Accordion Content 1
        </AccordionItem>
        <AccordionItem id="item2" header="Accordion Header 2">
          Accordion Content 2
        </AccordionItem>
      </Accordion>
    );

    const header1 = screen.getByText('Accordion Header 1');
    const header2 = screen.getByText('Accordion Header 2');

    // Expand first item
    fireEvent.click(header1);

    const content1 = screen.getByText('Accordion Content 1').closest('[role="region"]');
    const content2 = screen.getByText('Accordion Content 2').closest('[role="region"]');

    expect(content1).toHaveAttribute('aria-hidden', 'false');
    expect(content2).toHaveAttribute('aria-hidden', 'true');

    // Expand second item (first should collapse)
    fireEvent.click(header2);

    expect(content1).toHaveAttribute('aria-hidden', 'true');
    expect(content2).toHaveAttribute('aria-hidden', 'false');
  });
});

export default Accordion;