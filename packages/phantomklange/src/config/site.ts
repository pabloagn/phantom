// packages/phantomklange/src/config/site.ts

/**
 * Site configuration
 */

import { type ThemeKey } from "@phantom/core/themes";

export const siteConfig = {
    // Site Metadata
    name: "Phantomklänge",
    shortName: "Phantomklänge",
    description: "A digital archive of cultural artifacts, exploring the echoes of art, literature, and philosophy",
    url: "https://phantomklange.com",
    ogImage: "https://phantomklange.com/og.jpg",
    links: {
        twitter: "https://twitter.com/phantomklange",
        github: "https://github.com/phantomklange",
        instagram: "https://www.instagram.com/phantomklange",
        linkedin: "https://www.linkedin.com/company/phantomklange"
    },
    creator: "Pablo Aguirre",
    foundingYear: 2025,
    titleTemplate: "%s | Phantomklänge",
    defaultTitle: "Phantomklänge",
    defaultDescription: "A digital archive of human art and thought.",

    // Styles
    colorScheme: "dark" as ThemeKey
};

// export type SiteConfig = typeof siteConfig;
