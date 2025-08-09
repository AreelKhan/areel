export type Site = {
  TITLE: string;
  DESCRIPTION: string;
  EMAIL: string;
  NUM_POSTS_ON_HOMEPAGE: number;
  SITEURL: string,
};

export type Metadata = {
  TITLE: string;
  DESCRIPTION: string;
};

export interface RawHeading {
  depth: number;
  slug: string;
  text: string;
}

export interface TocHeading extends RawHeading {
  subheadings: TocHeading[];
}
