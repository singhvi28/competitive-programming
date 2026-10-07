/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      colors: {
        dark: {
          900: '#07090e',
          850: '#0b0f19',
          800: '#111827',
          750: '#151e32',
          700: '#1f293d',
          600: '#374151',
        }
      }
    },
  },
  plugins: [],
}
