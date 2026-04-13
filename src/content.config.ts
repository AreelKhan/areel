import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const writings = defineCollection({
	loader: glob({ pattern: "**/*.mdx", base: "./src/content/writings" }),
	schema: z.object({
		title: z.string(),
		description: z.string(),
		date: z.coerce.date(),
		tags: z.array(z.string()),
		readTime: z.string(),
		featured: z.boolean().default(false),
		relatedWritings: z.array(z.string()).optional(),
		project: z.string().optional(),
	}),
});

const projects = defineCollection({
	loader: glob({ pattern: "**/*.mdx", base: "./src/content/projects" }),
	schema: z.object({
		title: z.string(),
		description: z.string(),
		tags: z.array(z.string()),
		featured: z.boolean().default(false),
		color: z.enum(["purple", "indigo"]),
		github: z.string().optional(),
		demo: z.string().optional(),
	}),
});

export const collections = { writings, projects };
