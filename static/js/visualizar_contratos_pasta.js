// Função para alternar a visibilidade dos contratos
function toggleContratos() {
    var list = document.getElementById('contratos-list');
    var icon = document.getElementById('toggle-icon');

    if (list.style.display === 'none' || list.style.display === '') {
        list.style.display = 'block'; 
        icon.textContent = '▲'; 
    } else {
        list.style.display = 'none'; 
        icon.textContent = '▼'; 
    }
}
