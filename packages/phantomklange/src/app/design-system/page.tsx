'use client';

import React, { useState } from 'react';
import {
  // Layout components
  Container, Grid, Stack, Divider,

  // Typography components
  Heading, Paragraph,

  // Base components
  Button, Card, Input, Select, Checkbox, Radio,
  Toggle, Badge, Avatar, Alert, Modal, Tooltip,
  LoadingSpinner, Skeleton, Progress, Slider,
  Popover, Separator, Icon,

  // Any other available components
} from '@phantom/core/components';

export default function DesignSystemPage() {
  const [activeSection, setActiveSection] = useState('typography');
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Mock data for examples
  const avatarUrl = 'https://i.pravatar.cc/150';

  return (
    <main className="bg-phantom-carbon-990 text-phantom-neutral-50 min-h-screen pb-24">
      <header className="bg-phantom-carbon-950 py-12">
        <Container>
          <Heading level={1} className="text-4xl md:text-5xl font-light tracking-wide font-serif-alt">
            Phantom Design System
          </Heading>
          <Paragraph className="text-phantom-neutral-300 mt-4 font-serif-alt italic text-lg">
            A comprehensive showcase of all design system components
          </Paragraph>
        </Container>
      </header>

      <Container className="py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Navigation sidebar */}
          <aside className="md:col-span-1 bg-phantom-carbon-950 p-6 rounded-lg sticky top-8 h-fit">
            <nav>
              <ul className="space-y-2">
                {[
                  { id: 'typography', name: 'Typography' },
                  { id: 'buttons', name: 'Buttons' },
                  { id: 'inputs', name: 'Inputs & Forms' },
                  { id: 'layout', name: 'Layout' },
                  { id: 'feedback', name: 'Feedback' },
                  { id: 'navigation', name: 'Navigation' },
                  { id: 'data-display', name: 'Data Display' },
                  { id: 'overlay', name: 'Overlay' },
                ].map((section) => (
                  <li key={section.id}>
                    <button
                      onClick={() => setActiveSection(section.id)}
                      className={`w-full text-left px-4 py-2 rounded ${
                        activeSection === section.id
                          ? 'bg-phantom-primary-600 text-phantom-neutral-50'
                          : 'text-phantom-neutral-200 hover:bg-phantom-carbon-900'
                      }`}
                    >
                      {section.name}
                    </button>
                  </li>
                ))}
              </ul>
            </nav>
          </aside>

          {/* Main content */}
          <div className="md:col-span-3 space-y-12">
            {/* Typography Section */}
            {activeSection === 'typography' && (
              <section id="typography">
                <Heading level={2} className="text-3xl mb-8 font-serif-alt">
                  Typography
                </Heading>

                <Card className="p-8 mb-8">
                  <Heading level={3} className="mb-6 text-xl">Headings</Heading>
                  <div className="space-y-4">
                    <Heading level={1}>Heading 1 (h1)</Heading>
                    <Heading level={2}>Heading 2 (h2)</Heading>
                    <Heading level={3}>Heading 3 (h3)</Heading>
                    <Heading level={4}>Heading 4 (h4)</Heading>
                    <Heading level={5}>Heading 5 (h5)</Heading>
                    <Heading level={6}>Heading 6 (h6)</Heading>
                  </div>
                </Card>

                <Card className="p-8">
                  <Heading level={3} className="mb-6 text-xl">Paragraphs</Heading>
                  <div className="space-y-4">
                    <Paragraph>Default paragraph text. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam auctor, nisl eget ultricies lacinia, nunc nisl aliquam nisl, eget ultricies nisl nunc eget nisl.</Paragraph>
                    <Paragraph className="text-sm">Small paragraph text with text-sm class.</Paragraph>
                    <Paragraph className="text-lg">Large paragraph text with text-lg class.</Paragraph>
                    <Paragraph className="italic">Italic paragraph text with the italic class.</Paragraph>
                    <Paragraph className="font-bold">Bold paragraph text with the font-bold class.</Paragraph>
                    <Paragraph className="font-serif-alt">Alternate serif font paragraph text.</Paragraph>
                  </div>
                </Card>
              </section>
            )}

            {/* Buttons Section */}
            {activeSection === 'buttons' && (
              <section id="buttons">
                <Heading level={2} className="text-3xl mb-8 font-serif-alt">
                  Buttons
                </Heading>

                <Card className="p-8 mb-8">
                  <Heading level={3} className="mb-6 text-xl">Button Variants</Heading>
                  <div className="flex flex-wrap gap-4">
                    <Button variant="primary">Primary</Button>
                    <Button variant="secondary">Secondary</Button>
                    <Button variant="success">Success</Button>
                    <Button variant="warning">Warning</Button>
                    <Button variant="error">Error</Button>
                    <Button variant="ghost">Ghost</Button>
                  </div>
                </Card>

                <Card className="p-8 mb-8">
                  <Heading level={3} className="mb-6 text-xl">Button Sizes</Heading>
                  <div className="flex flex-wrap items-center gap-4">
                    <Button size="sm">Small</Button>
                    <Button size="md">Medium</Button>
                    <Button size="lg">Large</Button>
                  </div>
                </Card>

                <Card className="p-8 mb-8">
                  <Heading level={3} className="mb-6 text-xl">Button States</Heading>
                  <div className="flex flex-wrap gap-4">
                    <Button disabled>Disabled</Button>
                    <Button isLoading>Loading</Button>
                    <Button fullWidth className="mt-4">Full Width</Button>
                  </div>
                </Card>

                <Card className="p-8">
                  <Heading level={3} className="mb-6 text-xl">Button with Icons</Heading>
                  <div className="flex flex-wrap gap-4">
                    <Button leftIcon={<span>←</span>}>Left Icon</Button>
                    <Button rightIcon={<span>→</span>}>Right Icon</Button>
                    <Button leftIcon={<span>←</span>} rightIcon={<span>→</span>}>Both Icons</Button>
                  </div>
                </Card>
              </section>
            )}

            {/* Inputs & Forms Section */}
            {activeSection === 'inputs' && (
              <section id="inputs">
                <Heading level={2} className="text-3xl mb-8 font-serif-alt">
                  Inputs & Forms
                </Heading>

                <Card className="p-8 mb-8">
                  <Heading level={3} className="mb-6 text-xl">Text Inputs</Heading>
                  <div className="space-y-4">
                    <Input placeholder="Default input" />
                    <Input label="With Label" placeholder="Input with label" />
                    <Input
                      label="With Helper Text"
                      placeholder="Input with helper text"
                      helperText="This is some helper text to provide context."
                    />
                    <Input
                      label="Error State"
                      placeholder="Input with error"
                      error="This field is required"
                      isError
                    />
                    <Input
                      label="Disabled State"
                      placeholder="Disabled input"
                      disabled
                    />
                  </div>
                </Card>

                <Card className="p-8 mb-8">
                  <Heading level={3} className="mb-6 text-xl">Checkboxes & Radios</Heading>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-4">
                      <Heading level={4} className="text-lg mb-2">Checkboxes</Heading>
                      <Checkbox label="Default checkbox" />
                      <Checkbox label="Checked checkbox" checked />
                      <Checkbox label="Disabled checkbox" disabled />
                    </div>
                    <div className="space-y-4">
                      <Heading level={4} className="text-lg mb-2">Radio Buttons</Heading>
                      <Radio label="Option 1" name="radio-demo" value="1" />
                      <Radio label="Option 2" name="radio-demo" value="2" checked />
                      <Radio label="Disabled option" name="radio-demo" value="3" disabled />
                    </div>
                  </div>
                </Card>

                <Card className="p-8 mb-8">
                  <Heading level={3} className="mb-6 text-xl">Toggle & Slider</Heading>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-4">
                      <Heading level={4} className="text-lg mb-2">Toggle</Heading>
                      <Toggle label="Default toggle" />
                      <Toggle label="Checked toggle" checked />
                      <Toggle label="Disabled toggle" disabled />
                    </div>
                    <div className="space-y-4">
                      <Heading level={4} className="text-lg mb-2">Slider</Heading>
                      <Slider label="Default slider" min={0} max={100} value={50} />
                      <Slider label="Disabled slider" min={0} max={100} value={30} disabled />
                    </div>
                  </div>
                </Card>

                <Card className="p-8">
                  <Heading level={3} className="mb-6 text-xl">Select</Heading>
                  <div className="space-y-4">
                    <Select
                      label="Default select"
                      placeholder="Select an option"
                      options={[
                        { value: 'option1', label: 'Option 1' },
                        { value: 'option2', label: 'Option 2' },
                        { value: 'option3', label: 'Option 3' },
                      ]}
                    />
                    <Select
                      label="Disabled select"
                      placeholder="Select an option"
                      options={[
                        { value: 'option1', label: 'Option 1' },
                        { value: 'option2', label: 'Option 2' },
                      ]}
                      disabled
                    />
                  </div>
                </Card>
              </section>
            )}

            {/* Layout Section */}
            {activeSection === 'layout' && (
              <section id="layout">
                <Heading level={2} className="text-3xl mb-8 font-serif-alt">
                  Layout
                </Heading>

                <Card className="p-8 mb-8">
                  <Heading level={3} className="mb-6 text-xl">Container</Heading>
                  <div className="bg-phantom-carbon-950 p-4 rounded">
                    <Paragraph>This content is within a Container component. Containers provide a consistent width and padding.</Paragraph>
                  </div>
                </Card>

                <Card className="p-8 mb-8">
                  <Heading level={3} className="mb-6 text-xl">Grid</Heading>
                  <Grid columns={3} gap={4}>
                    {[1, 2, 3, 4, 5, 6].map((item) => (
                      <div key={item} className="bg-phantom-carbon-950 p-4 rounded">
                        <Paragraph>Grid Item {item}</Paragraph>
                      </div>
                    ))}
                  </Grid>
                </Card>

                <Card className="p-8 mb-8">
                  <Heading level={3} className="mb-6 text-xl">Stack</Heading>
                  <Stack direction="vertical" spacing={4}>
                    <div className="bg-phantom-carbon-950 p-4 rounded">
                      <Paragraph>Stack Item 1</Paragraph>
                    </div>
                    <div className="bg-phantom-carbon-950 p-4 rounded">
                      <Paragraph>Stack Item 2</Paragraph>
                    </div>
                    <div className="bg-phantom-carbon-950 p-4 rounded">
                      <Paragraph>Stack Item 3</Paragraph>
                    </div>
                  </Stack>
                </Card>

                <Card className="p-8">
                  <Heading level={3} className="mb-6 text-xl">Divider</Heading>
                  <Paragraph className="mb-4">Content above the divider</Paragraph>
                  <Divider />
                  <Paragraph className="mt-4">Content below the divider</Paragraph>
                </Card>
              </section>
            )}

            {/* Feedback Section */}
            {activeSection === 'feedback' && (
              <section id="feedback">
                <Heading level={2} className="text-3xl mb-8 font-serif-alt">
                  Feedback
                </Heading>

                <Card className="p-8 mb-8">
                  <Heading level={3} className="mb-6 text-xl">Alert</Heading>
                  <div className="space-y-4">
                    <Alert variant="info" title="Information">This is an informational alert.</Alert>
                    <Alert variant="success" title="Success">This is a success alert.</Alert>
                    <Alert variant="warning" title="Warning">This is a warning alert.</Alert>
                    <Alert variant="error" title="Error">This is an error alert.</Alert>
                  </div>
                </Card>

                <Card className="p-8 mb-8">
                  <Heading level={3} className="mb-6 text-xl">Loading Spinner</Heading>
                  <div className="grid grid-cols-5 gap-8">
                    <div className="flex flex-col items-center">
                      <LoadingSpinner size="xs" color="primary" />
                      <Paragraph className="mt-4 text-center">XS</Paragraph>
                    </div>
                    <div className="flex flex-col items-center">
                      <LoadingSpinner size="sm" color="primary" />
                      <Paragraph className="mt-4 text-center">SM</Paragraph>
                    </div>
                    <div className="flex flex-col items-center">
                      <LoadingSpinner size="md" color="primary" />
                      <Paragraph className="mt-4 text-center">MD</Paragraph>
                    </div>
                    <div className="flex flex-col items-center">
                      <LoadingSpinner size="lg" color="primary" />
                      <Paragraph className="mt-4 text-center">LG</Paragraph>
                    </div>
                    <div className="flex flex-col items-center">
                      <LoadingSpinner size="xl" color="primary" />
                      <Paragraph className="mt-4 text-center">XL</Paragraph>
                    </div>
                  </div>
                </Card>

                <Card className="p-8 mb-8">
                  <Heading level={3} className="mb-6 text-xl">Progress</Heading>
                  <div className="space-y-6">
                    <div>
                      <Paragraph className="mb-2">Default Progress (40%)</Paragraph>
                      <Progress value={40} max={100} />
                    </div>
                    <div>
                      <Paragraph className="mb-2">Success Progress (80%)</Paragraph>
                      <Progress value={80} max={100} variant="success" />
                    </div>
                    <div>
                      <Paragraph className="mb-2">Error Progress (20%)</Paragraph>
                      <Progress value={20} max={100} variant="error" />
                    </div>
                  </div>
                </Card>

                <Card className="p-8">
                  <Heading level={3} className="mb-6 text-xl">Skeleton</Heading>
                  <div className="space-y-4">
                    <Skeleton height="2rem" width="100%" />
                    <Skeleton height="1.5rem" width="75%" />
                    <Skeleton height="1.5rem" width="50%" />
                    <div className="flex space-x-4 mt-8">
                      <Skeleton height="4rem" width="4rem" borderRadius="50%" />
                      <div className="space-y-2 flex-1">
                        <Skeleton height="1.5rem" width="40%" />
                        <Skeleton height="1rem" width="90%" />
                        <Skeleton height="1rem" width="70%" />
                      </div>
                    </div>
                  </div>
                </Card>
              </section>
            )}

            {/* Data Display Section */}
            {activeSection === 'data-display' && (
              <section id="data-display">
                <Heading level={2} className="text-3xl mb-8 font-serif-alt">
                  Data Display
                </Heading>

                <Card className="p-8 mb-8">
                  <Heading level={3} className="mb-6 text-xl">Card</Heading>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <Card className="p-6">
                      <Heading level={4} className="text-lg mb-2">Basic Card</Heading>
                      <Paragraph>This is a basic card component that can be used to display content.</Paragraph>
                    </Card>
                    <Card className="p-6 bg-phantom-carbon-900">
                      <Heading level={4} className="text-lg mb-2">Card with Custom Background</Heading>
                      <Paragraph>Cards can have custom styles applied.</Paragraph>
                    </Card>
                  </div>
                </Card>

                <Card className="p-8 mb-8">
                  <Heading level={3} className="mb-6 text-xl">Badge</Heading>
                  <div className="flex flex-wrap gap-4">
                    <Badge variant="default">Default</Badge>
                    <Badge variant="primary">Primary</Badge>
                    <Badge variant="secondary">Secondary</Badge>
                    <Badge variant="success">Success</Badge>
                    <Badge variant="warning">Warning</Badge>
                    <Badge variant="error">Error</Badge>
                  </div>
                </Card>

                <Card className="p-8 mb-8">
                  <Heading level={3} className="mb-6 text-xl">Avatar</Heading>
                  <div className="flex flex-wrap gap-6">
                    <div className="flex flex-col items-center">
                      <Avatar src={avatarUrl} size="xs" />
                      <Paragraph className="mt-2">XS</Paragraph>
                    </div>
                    <div className="flex flex-col items-center">
                      <Avatar src={avatarUrl} size="sm" />
                      <Paragraph className="mt-2">SM</Paragraph>
                    </div>
                    <div className="flex flex-col items-center">
                      <Avatar src={avatarUrl} size="md" />
                      <Paragraph className="mt-2">MD</Paragraph>
                    </div>
                    <div className="flex flex-col items-center">
                      <Avatar src={avatarUrl} size="lg" />
                      <Paragraph className="mt-2">LG</Paragraph>
                    </div>
                    <div className="flex flex-col items-center">
                      <Avatar src={avatarUrl} size="xl" />
                      <Paragraph className="mt-2">XL</Paragraph>
                    </div>
                  </div>
                </Card>

                <Card className="p-8">
                  <Heading level={3} className="mb-6 text-xl">Separator</Heading>
                  <div className="space-y-6">
                    <div>
                      <Paragraph className="mb-2">Default Horizontal Separator</Paragraph>
                      <Separator />
                    </div>
                    <div className="h-20 flex items-center">
                      <Paragraph className="mr-4">Vertical Separator</Paragraph>
                      <Separator orientation="vertical" />
                      <Paragraph className="ml-4">Separated content</Paragraph>
                    </div>
                  </div>
                </Card>
              </section>
            )}

            {/* Overlay Section */}
            {activeSection === 'overlay' && (
              <section id="overlay">
                <Heading level={2} className="text-3xl mb-8 font-serif-alt">
                  Overlay
                </Heading>

                <Card className="p-8 mb-8">
                  <Heading level={3} className="mb-6 text-xl">Modal</Heading>
                  <div>
                    <Button onClick={() => setIsModalOpen(true)}>Open Modal</Button>
                    <Modal
                      isOpen={isModalOpen}
                      onClose={() => setIsModalOpen(false)}
                      title="Example Modal"
                    >
                      <div className="p-6">
                        <Paragraph>This is an example modal dialog. It can be used to display content that requires user attention.</Paragraph>
                        <div className="mt-6 flex justify-end">
                          <Button variant="ghost" onClick={() => setIsModalOpen(false)} className="mr-2">
                            Cancel
                          </Button>
                          <Button onClick={() => setIsModalOpen(false)}>
                            Confirm
                          </Button>
                        </div>
                      </div>
                    </Modal>
                  </div>
                </Card>

                <Card className="p-8 mb-8">
                  <Heading level={3} className="mb-6 text-xl">Tooltip</Heading>
                  <div className="flex flex-wrap gap-8">
                    <Tooltip content="This is a tooltip" placement="top">
                      <Button>Hover me (Top)</Button>
                    </Tooltip>
                    <Tooltip content="This is a tooltip" placement="right">
                      <Button>Hover me (Right)</Button>
                    </Tooltip>
                    <Tooltip content="This is a tooltip" placement="bottom">
                      <Button>Hover me (Bottom)</Button>
                    </Tooltip>
                    <Tooltip content="This is a tooltip" placement="left">
                      <Button>Hover me (Left)</Button>
                    </Tooltip>
                  </div>
                </Card>

                <Card className="p-8">
                  <Heading level={3} className="mb-6 text-xl">Popover</Heading>
                  <div className="flex gap-4">
                    <Popover
                      trigger={<Button>Click me</Button>}
                      content={
                        <div className="p-4 w-64">
                          <Heading level={4} className="text-lg mb-2">Popover Title</Heading>
                          <Paragraph>This is the content of the popover. It can contain any elements.</Paragraph>
                        </div>
                      }
                    />
                  </div>
                </Card>
              </section>
            )}

            {/* Navigation Section */}
            {activeSection === 'navigation' && (
              <section id="navigation">
                <Heading level={2} className="text-3xl mb-8 font-serif-alt">
                  Navigation
                </Heading>

                <Card className="p-8">
                  <Heading level={3} className="mb-6 text-xl">Navigation Examples</Heading>
                  <Paragraph>
                    Navigation components including tabs, breadcrumbs, pagination, and menus would be displayed here
                    when they become available in the design system.
                  </Paragraph>
                </Card>
              </section>
            )}
          </div>
        </div>
      </Container>
    </main>
  );
}
