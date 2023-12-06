/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "node_modules/preline/dist/*.js"
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#7B4A3A",
          dark: "#482B21",
          foreground: "#FFFFFF"
        },
        secondary: "#946C60",
      }
    },
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("preline/plugin"),
  ],
}

