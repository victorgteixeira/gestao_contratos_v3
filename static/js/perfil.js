document.getElementById("alterar-dados-link").addEventListener("click", function(event) {
    event.preventDefault(); // Previne o comportamento padrão do link
    document.getElementById("alterar-dados").style.display = "block"; // Exibe o formulário de alteração
});

function fecharAlteracao() {
    document.getElementById("alterar-dados").style.display = "none"; // Oculta o formulário de alteração
}

function toggleAlterarForm() {
    var form = document.getElementById("alterarForm");
    // Alterna a visibilidade da tela de alteração de dados
    if (form.style.display === "none" || form.style.display === "") {
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
}
