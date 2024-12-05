document.addEventListener("DOMContentLoaded", function() {
    // Configuração do gráfico de pizza
    const dataPie = {
        labels: labels,
        datasets: [{
            label: 'Valor do Contrato (R$)',
            backgroundColor: [
                'rgba(75, 192, 192, 0.6)',
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(153, 102, 255, 0.6)',
                'rgba(255, 159, 64, 0.6)',
                'rgba(255, 120, 64, 0.6)',
                'rgba(120, 99, 132, 0.6)',
            ],
            borderColor: [
                'rgba(75, 192, 192, 1)',
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(255, 155, 64, 0.6)',
                'rgba(120, 99, 132, 0.6)',
            ],
            borderWidth: 1,
            data: dataValues,
        }]
    };

    const configPie = {
        type: 'pie',
        data: dataPie,
        options: {
            responsive: false,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Gastos por Contrato'
                }
            }
        }
    };
     
    const ctxPie = document.getElementById('gastosChart');
    if (ctxPie) {
        new Chart(ctxPie, configPie);
    }

    // Configuração do gráfico de colunas
    const dataColumn = {
        labels: labels,
        datasets: [{
            label: 'Valor do Contrato (R$)',
            backgroundColor: 'rgba(54, 162, 235, 0.6)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1,
            data: dataValues,
        }]
    };

    const configColumn = {
        type: 'bar',
        data: dataColumn,
        options: {
            responsive: false,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Distribuição de Gastos por Contrato'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    };

    const ctxColumn = document.getElementById('gastosColumnChart');
    if (ctxColumn) {
        new Chart(ctxColumn, configColumn);
    }
});

document.addEventListener("DOMContentLoaded", function() {
    // Configuração do gráfico de barras para categorias com maiores gastos
    const dataCategoria = {
        labels: categoriaLabels,
        datasets: [{
            label: 'Gastos Totais (R$)',
            backgroundColor: 'rgba(153, 102, 255, 0.6)',
            borderColor: 'rgba(153, 102, 255, 1)',
            borderWidth: 1,
            data: categoriaValues,
        }]
    };

    const configCategoria = {
        type: 'bar',
        data: dataCategoria,
        options: {
            responsive: false,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Categorias com Maiores Gastos'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    };

    const ctxCategoria = document.getElementById('categoriaGastosChart');
    if (ctxCategoria) {
        new Chart(ctxCategoria, configCategoria);
    }
});

document.addEventListener("DOMContentLoaded", function() {
    // Configuração do gráfico de pizza para categorias com maiores gastos
    const dataCategoriaPie = {
        labels: categoriaLabels,
        datasets: [{
            label: 'Gastos Totais por Categoria (R$)',
            backgroundColor: [
                'rgba(75, 192, 192, 0.6)',
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(153, 102, 255, 0.6)',
                'rgba(255, 159, 64, 0.6)',
                'rgba(120, 120, 120, 0.6)',
            ],
            borderColor: [
                'rgba(75, 192, 192, 1)',
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(120, 120, 120, 1)',
            ],
            borderWidth: 1,
            data: categoriaValues,
        }]
    };

    const configCategoriaPie = {
        type: 'pie',
        data: dataCategoriaPie,
        options: {
            responsive: false,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Distribuição de Gastos por Categoria'
                }
            }
        }
    };

    const ctxCategoriaPie = document.getElementById('categoriaGastosPieChart');
    if (ctxCategoriaPie) {
        new Chart(ctxCategoriaPie, configCategoriaPie);
    }
});



document.addEventListener("DOMContentLoaded", function() {
    // Configuração do gráfico de barras para fornecedores com maiores gastos
    const dataFornecedor = {
        labels: fornecedorLabels,
        datasets: [{
            label: 'Gastos Totais (R$)',
            backgroundColor: 'rgba(255, 99, 132, 0.6)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1,
            data: fornecedorValues,
        }]
    };

    const configFornecedor = {
        type: 'bar',
        data: dataFornecedor,
        options: {
            responsive: false,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Fornecedores com Maiores Gastos'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    };

    const ctxFornecedor = document.getElementById('fornecedorGastosChart');
    if (ctxFornecedor) {
        new Chart(ctxFornecedor, configFornecedor);
    }
});
