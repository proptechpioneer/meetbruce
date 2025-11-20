/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./*/templates/**/*.html",
    "./application/**/*.py",
    "./static/**/*.js",
  ],
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Anek Latin', 'system-ui', '-apple-system', 'sans-serif'],
        'anek': ['Anek Latin', 'system-ui', '-apple-system', 'sans-serif'],
      },
      maxWidth: {
        '1440': '1440px',
      },
    },
  },
  plugins: [],
}