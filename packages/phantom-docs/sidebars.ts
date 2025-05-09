// packages/phantom-docs/sidebars.ts

import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  mainSidebar: [
    {
      type: 'doc',
      id: '00-introduction',
      label: 'Introduction',
    },
    {
      type: 'doc',
      id: '01-monorepo-structure',
      label: 'Monorepo Structure',
    },
    {
      type: 'category',
      label: 'Phantom Core',
      link: {
        type: 'doc',
        id: 'phantom-core/00-overview',
      },
      items: [
        'phantom-core/01-api-reference',
        'phantom-core/02-usage-examples',
      ],
    },
    {
      type: 'category',
      label: 'Phantom Klänge',
      link: {
        type: 'doc',
        id: 'phantom-klange/00-overview',
      },
      items: [
        'phantom-klange/01-api-reference',
        'phantom-klange/02-usage-examples',
      ],
    },
    {
      type: 'doc',
      id: '02-system-architecture',
      label: 'System Architecture',
    },
  ],
};

export default sidebars;
