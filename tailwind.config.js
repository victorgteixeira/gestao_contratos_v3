module.exports = {
  darkMode: 'class', // ou 'media' para seguir as preferências do sistema
  content: [
    './templates/**/*.html', // Inclua seus templates Django aqui
    './static/js/**/*.js',   // Se houver scripts com classes Tailwind
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
