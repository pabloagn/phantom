// packages/phantomklange/src/config/site.ts
// @ts-nocheck

/**
 * Site configuration (site name, author, description, socials, etc.)
 */

export const siteConfig = {
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
  themeColor: "#030407", // Carbon-990 color
  colorScheme: "dark",
  titleTemplate: "%s | Phantomklänge",
  defaultTitle: "Phantomklänge",
  defaultDescription: "A digital archive of human art and thought."
};

export type SiteConfig = typeof siteConfig;

export default siteConfig;
