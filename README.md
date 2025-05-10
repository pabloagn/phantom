# Phantom

<div align="center">

*An open-source initiative to build a deeply interconnected, queryable digital canon of human art and thought.*

</div>

<br/>
<div align="center">───────  §  ───────</div>
<br/>

## Vision & Motivation: Curating a Digital Canon

In an age awash with ephemeral content and algorithmic noise, Phantom seeks to carve out a space for enduring works of human creativity and intellect. We face a deluge of information, the fragmentation of cultural memory, and the rise of "AI slop"—content endlessly remixed without grounding in original substance. It's increasingly difficult to connect with the foundational art, literature, and ideas that shape our understanding of ourselves and the world.

Phantom is our response: an ambitious project to build an **open-source, canonical library**. We are not aiming to catalog *everything*, but rather to meticulously curate a collection of significant works – the touchstones of art, literature, philosophy, and science – and transform them into a unified, deeply interconnected knowledge graph.

Our core motivations are:

- **Combat Information Overload:** Provide a focused, high-signal resource amidst the noise, prioritizing depth and significance over sheer volume.
- **Preserve & Rediscover:** Create a persistent, accessible digital home for canonical works, safeguarding them against cultural amnesia and making them newly discoverable.
- **Enable Deep Exploration:** Move beyond keyword search. Allow users to explore the semantic relationships, thematic resonances, and intricate connections *between* works across different domains and eras.
- **Foster Meaningful Analysis:** Build a structured, vectorized representation of the canon, enabling novel forms of computational analysis, visualization, and understanding.
- **Offer an Open Resource:** Provide this curated and structured knowledge base as an open-source platform for researchers, students, artists, and the intellectually curious public.

Phantom aims to be more than a digital archive; it aspires to be a dynamic engine for exploring the heights of human expression and thought.

<br/>
<div align="center">───────  §  ───────</div>
<br/>

## Overview

This repository serves as the central coordination point for the entire Phantom system, providing:

- Design system and component library
- Documentation for all system components
- Configuration and standards
- Development environment setup

## Components

Phantom is structured as a monorepo using [pnpm](https://pnpm.io/) workspaces and [Turborepo](https://turbo.build/) for build orchestration. All components are located under the `packages/` directory.

The Phantom ecosystem consists of the following components:

- [**phantom-api**](./packages/phantom-api): API layer for accessing Phantom services
- [**phantom-canon**](./packages/phantom-canon): Core content catalog and canon management
- [**phantom-core**](./packages/phantom-core): Central hub, documentation, and design system
- [**phantom-eda**](./packages/phantom-eda): Exploratory data analysis tools
- [**phantom-editor**](./packages/phantom-editor): Content editing and management interface
- [**phantom-enrichment**](./packages/phantom-enrichment): Content enrichment and metadata generation
- [**phantom-explorer**](./packages/phantom-explorer): Interface for exploring the canon
- [**phantom-folio**](./packages/phantom-folio): User collections and reading lists
- [**phantom-glacier**](./packages/phantom-glacier): Digital asset storage
- [**phantom-intake**](./packages/phantom-intake): Content ingestion pipeline
- [**phantom-query**](./packages/phantom-query): Search and querying infrastructure
- [**phantom-rd**](./packages/phantom-rd): eBook reader component
- [**phantom-vector**](./packages/phantom-vector): Vector embedding and semantic search capabilities
- [**phantomklange**](./packages/phantomklange): Digital catalogue and user interface

## Getting Started

This project uses pnpm for package management and Turborepo for task running.

### Workflow 1: Initial Setup / After Major Dependency Changes

#### Clean

From monorepo root:

```bash
# Clean all packages from root directly
pnpm run clean
```

#### Install

From monorepo root:

```bash
# Install dependencies
pnpm install
```

#### Run

From monorepo root:

```bash
pnpm run build
```

### Workflow 2: Development - Working on @phantom/docs (with Hot Reload for Docs & Core)

#### Run

From monorepo root, and in one terminal:

```bash
# Run phantom-core in watch mode
pnpm --filter @phantom/core run watch:all
```

In another terminal:

```bash
# Run phantom-docs in watch mode
pnpm --filter @phantom/docs dev
```

### Workflow 3: Development - Working on phantomklange (with Hot Reload for Klange & Core)

From monorepo root, and in one terminal:

```bash
# Run phantomklange with core in watch mode
pnpm --filter phantomklange run dev:with-core
```

This ensures `@phantom/core` is built first, then `@phantom/docs` and `phantomklange` are built using the latest artifacts from `@phantom/core`.



### Workflow 4: Building for Production/Preview

From monorepo root:

```bash
# Build all packages
pnpm run build
```

## License

[MIT](./LICENSE)
