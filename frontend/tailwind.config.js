import tailwindAnimate from "tailwindcss-animate";

/** @type {import('tailwindcss').Config} */
const config = {
  darkMode: "class",

  content: [
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/hooks/**/*.{js,ts,jsx,tsx,mdx}",
  ],

  theme: {
    extend: {
      fontFamily: {
        // Vinculando às variáveis de fonte definidas no RootLayout
        sans: ['var(--font-inter)', 'ui-sans-serif', 'system-ui'],
        roboto: ['var(--font-roboto)', 'sans-serif'],
      },
      colors: {
        brand: {
          dark: '#0B1020',
          surface: '#12182B',
          primary: '#7C3AED',
          secondary: '#22D3EE',
          success: '#34D399',
          warning: '#FBBF24',
          danger: '#F87171',
          text: '#E5E7EB',
          muted: '#8A94A6',
          border: '#1F2937',
        }
      },
    },
  },

  plugins: [tailwindAnimate],
};

export default config;
