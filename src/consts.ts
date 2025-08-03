import type { Metadata, Site } from "@types";

export const SITE: Site = {
  TITLE: "Areel Khan",
  DESCRIPTION: "Areel Khan's personal website.",
  EMAIL: "areel.khan.career@gmail.com",
  NUM_POSTS_ON_HOMEPAGE: 2,
  NUM_PUBLICATIONS_ON_HOMEPAGE: 3,
  SITEURL: 'https://astro-micro-academic.vercel.app' // Update here to link the RSS icon to your website rss
};

export const HIGHLIGHTAUTHOR = "Areel Khan"

export const HOME: Metadata = {
  TITLE: "Home",
  DESCRIPTION: "Areel Khan's personal website.",
};

export const BLOG: Metadata = {
  TITLE: "Blog",
  DESCRIPTION: "A collection of articles on topics I am passionate about.",
};

export const EXPERIENCE: Metadata = {
  TITLE: "Experience",
  DESCRIPTION: "Areel Khan's experience.",
};

export const RESUME: Metadata = {
  TITLE: "Resume",
  DESCRIPTION: "Areel Khan's resume.",
};

export const TAGS: Metadata = {
  TITLE: "TAGS",
  DESCRIPTION:
    "blog tag filter",
};