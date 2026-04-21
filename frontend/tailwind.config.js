/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: '#FF6600',
        dark: '#1b1b1f',
        card: '#2a2a2e',
      }
    },
  },
  plugins: [],
}
