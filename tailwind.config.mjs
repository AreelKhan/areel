/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      fontFamily: {
        mono: ['"JetBrains Mono"', '"Fira Code"', 'ui-monospace', 'SFMono-Regular', 'monospace'],
      },
      colors: {
        terminal: {
          bg: '#121218',
          surface: '#1a1a24',
          border: '#2a2a3a',
          muted: '#6b6b80',
          text: '#e0e0e8',
          accent: '#a78bfa',
          dim: '#9898b0',
        },
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
};
