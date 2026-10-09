import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#F7F8FA",
        surface: "#FFFFFF",
        sidebar: "#F9FAFB",
        primaryText: "#17191F",
        secondaryText: "#656B76",
        mutedText: "#8A909B",
        border: "#E5E7EB",
        accent: "#315EFB",
        accentHover: "#284cd1",
        success: "#16845B",
        warning: "#B7791F",
        error: "#D64545",
        info: "#3975D7",
      },
      fontFamily: {
        sans: ['var(--font-inter)', 'sans-serif'],
        mono: ['var(--font-roboto-mono)', 'monospace'],
      },
      boxShadow: {
        'subtle': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
      }
    },
  },
  plugins: [],
};
export default config;
