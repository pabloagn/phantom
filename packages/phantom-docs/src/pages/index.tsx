// packages/docs/src/pages/index.tsx

import type { ReactNode } from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';
import { Button as PhantomButton } from '@phantom/core';
import DocusaurusLink from '@docusaurus/Link';

import styles from './index.module.css';

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx('hero', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className={clsx('hero__title', styles.heroTitle)}>
          {siteConfig.title}
        </Heading>
        <p className={clsx('hero__subtitle', styles.heroSubtitle)}>{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <DocusaurusLink to="/introduction">
            <PhantomButton variant="outline">Get Started</PhantomButton>
          </DocusaurusLink>
        </div>
      </div>
    </header>
  );
}

// Section to highlight key areas of documentation
function KeySections() {
  const sections = [
    {
      title: 'Monorepo Structure',
      link: '/monorepo-structure',
      description: 'Understand the organization and architecture of our codebase.',
      // icon: '🏗️', // Example: You could use SVGs or font icons here
    },
    {
      title: 'Phantom Core',
      link: '/phantom-core/overview',
      description: 'Dive into the foundational elements and APIs of the core system.',
      // icon: '⚙️',
    },
    {
      title: 'Phantom Klänge',
      link: '/phantom-klange/overview',
      description: 'Explore the specifics of the Klänge package and its functionalities.',
      icon: '🎶',
    },
    {
      title: 'System Architecture',
      link: '/system-architecture',
      description: 'See how all components interact within the Phantom ecosystem.',
      icon: '↔️',
    },
  ];

  return (
    <section className={styles.keySections}>
      <div className="container">
        <div className="row">
          {sections.map((section, idx) => (
            <div key={idx} className={clsx('col col--3', styles.keySectionColumn)}>
              <div className={styles.keySectionCard}>
                {/* {section.icon && <span className={styles.keySectionIcon}>{section.icon}</span>} */}
                <Heading as="h3" className={styles.keySectionTitle}>
                  <Link to={section.link}>{section.title}</Link>
                </Heading>
                <p className={styles.keySectionDescription}>{section.description}</p>
                <Link
                  className={clsx(
                    'button button--outline button--secondary button--sm',
                    styles.keySectionButton
                  )}
                  to={section.link}
                >
                  Learn More →
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout title="Home" description={siteConfig.tagline}>
      <HomepageHeader />
      <main>
        {/* Remove HomepageFeatures if you're not using the default one */}
        {/* <HomepageFeatures /> */}
        <KeySections /> {/* Add our new key sections component */}
      </main>
    </Layout>
  );
}
