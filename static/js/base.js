// base.js

document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById('menuToggle');
    const menuContainer = document.getElementById('menuContainer');

    // Adiciona o evento de clique para expandir ou recolher o menu
    menuToggle.addEventListener('click', function () {
        menuContainer.classList.toggle('expanded'); // Adiciona ou remove a classe 'expanded'
    });

    // Mostrar/ocultar submenus ao clicar
    const menuTitles = document.querySelectorAll('.menu-title > a');

    menuTitles.forEach(title => {
        title.addEventListener('click', function (e) {
            e.preventDefault();
            const submenu = this.nextElementSibling;

            // Alterna a visibilidade do submenu ao clicar
            if (submenu.style.display === "block") {
                submenu.style.display = "none"; // Oculta o submenu
            } else {
                submenu.style.display = "block"; // Exibe o submenu
            }
        });
    });
});
