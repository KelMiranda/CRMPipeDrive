/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      './templates/**/*.html', // Ruta de tus archivos HTML en Flask
      './static/**/*.js', // Opcional si tienes archivos JS estáticos
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

